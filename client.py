#!/usr/bin/env python3
"""
client.py
Simple chat client to connect to the threaded server.
Usage: python3 client.py [server_ip] [port]
Defaults: 127.0.0.1 7777

Client features:
 - Prompt for username (sent to server)
 - Receiver thread to print incoming messages in readable format
 - Sender (main thread) reads stdin and sends messages
 - Supports:
    - @username message  -> private
    - /list              -> ask server for user list
    - /quit              -> exit
Author: Muhammad Hammad Butt (501399)
"""

import socket
import threading
import sys
import time

def pretty_print_server_msg(raw):
    """Parse server protocol and print nicely for the user."""
    raw = raw.strip()
    if not raw:
        return
    # Protocol: TYPE|... fields ...
    parts = raw.split('|')
    typ = parts[0]
    if typ == "ENTERNAME":
        print(parts[1] if len(parts) > 1 else "Server requests username.")
    elif typ == "OK":
        print(parts[1] if len(parts) > 1 else "OK from server.")
    elif typ == "SYSTEM":
        # SYSTEM|timestamp|message
        t = time.strftime('%H:%M:%S', time.localtime(int(parts[1]))) if len(parts) > 1 else ''
        msg = parts[2] if len(parts) > 2 else ''
        print(f"[SYSTEM {t}] {msg}")
    elif typ == "MSG":
        # MSG|from|timestamp|message
        frm = parts[1] if len(parts) > 1 else 'unknown'
        t = time.strftime('%H:%M:%S', time.localtime(int(parts[2]))) if len(parts) > 2 else ''
        body = parts[3] if len(parts) > 3 else ''
        print(f"[{t}] {frm}: {body}")
    elif typ == "PRV":
        # PRV|from|to|timestamp|message
        frm = parts[1] if len(parts) > 1 else 'unknown'
        t = time.strftime('%H:%M:%S', time.localtime(int(parts[3]))) if len(parts) > 3 else ''
        body = parts[4] if len(parts) > 4 else ''
        print(f"[{t}] [PRIVATE] {frm} -> you: {body}")
    elif typ == "SENTPRV":
        # confirmation of sending private message
        to = parts[1] if len(parts) > 1 else ''
        t = time.strftime('%H:%M:%S', time.localtime(int(parts[2]))) if len(parts) > 2 else ''
        body = parts[3] if len(parts) > 3 else ''
        print(f"[{t}] [PRIVATE][you -> {to}]: {body}")
    elif typ == "USERS":
        users = parts[1] if len(parts) > 1 else ''
        print(f"[USERS] {users}")
    elif typ == "ERR":
        code = parts[1] if len(parts) > 1 else 'ERROR'
        msg = parts[2] if len(parts) > 2 else ''
        print(f"[ERROR {code}] {msg}")
    else:
        # Unrecognized format: print raw
        print("RAW>", raw)

def receiver_loop(sock):
    """Thread function to receive messages from server."""
    try:
        while True:
            data = sock.recv(4096)
            if not data:
                print("[!] Disconnected from server.")
                break
            text = data.decode('utf-8')
            # server may send multiple lines; split
            for line in text.splitlines():
                pretty_print_server_msg(line)
    except Exception as e:
        print("[!] Receiver error:", e)
    finally:
        try:
            sock.close()
        except:
            pass
        # end the program if receiver stops
        sys.exit(0)

def main():
    server_ip = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
    server_port = int(sys.argv[2]) if len(sys.argv) > 2 else 7777

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((server_ip, server_port))
    except Exception as e:
        print(f"[!] Could not connect to {server_ip}:{server_port} -> {e}")
        return

    # Start receiver thread
    t = threading.Thread(target=receiver_loop, args=(sock,), daemon=True)
    t.start()

    # Wait for server to ask for name (or send immediately)
    # We'll read prompt from server by small sleep to allow first message to be displayed
    time.sleep(0.3)

    # Enter username
    name = input("Enter username: ").strip()
    if not name:
        print("Username cannot be empty. Exiting.")
        sock.close()
        return
    sock.sendall((name + "\n").encode('utf-8'))

    # Main send loop
    try:
        while True:
            line = input()
            if not line:
                continue
            if line.strip() == "/quit":
                sock.sendall(b"/quit\n")
                print("[*] Quitting... bye.")
                break
            # send raw line
            sock.sendall((line + "\n").encode('utf-8'))
            # small yield
            time.sleep(0.01)
    except KeyboardInterrupt:
        try:
            sock.sendall(b"/quit\n")
        except:
            pass
    finally:
        try:
            sock.close()
        except:
            pass
        # give receiver thread a moment to exit
        time.sleep(0.2)

if __name__ == "__main__":
    main()
