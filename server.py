#!/usr/bin/env python3
"""
server.py
Simple threaded chat server using Python sockets.
Features:
 - Multiple clients (thread per client)
 - Unique usernames enforced
 - Broadcast messages (everyone except sender)
 - Private messages using: @username message
 - /list command to get current users
 - /quit to disconnect cleanly
 - Join/Leave notifications
 - Basic error handling and cleanup
Author: Muhammad Hammad Butt (501399) - Use, study, and customize.
"""

import socket
import threading
import time
import traceback

HOST = '0.0.0.0'   # listen on all interfaces
PORT = 7777        # default port; change if needed

# Global structures
clients = {}       # username -> socket
clients_lock = threading.Lock()

def safe_send(sock, text):
    """Send text to a socket, handle broken pipes gracefully."""
    try:
        sock.sendall(text.encode('utf-8'))
    except Exception:
        # Best effort: find the username for this socket and remove it
        remove_username = None
        with clients_lock:
            for u, s in list(clients.items()):
                if s is sock:
                    remove_username = u
                    break
        if remove_username:
            remove_client(remove_username)

def broadcast_system(message):
    """Broadcast a system message (JOIN/LEAVE etc.) in a simple format."""
    payload = f"SYSTEM|{int(time.time())}|{message}"
    with clients_lock:
        for user, sock in list(clients.items()):
            safe_send(sock, payload + '\n')

def broadcast_message(from_user, message):
    """Broadcast a normal message to everyone except sender."""
    payload = f"MSG|{from_user}|{int(time.time())}|{message}"
    with clients_lock:
        for user, sock in list(clients.items()):
            if user == from_user:
                continue
            safe_send(sock, payload + '\n')

def send_private(from_user, to_user, message):
    """Send a private message if recipient exists; return True if sent."""
    with clients_lock:
        target_sock = clients.get(to_user)
    if target_sock:
        payload = f"PRV|{from_user}|{to_user}|{int(time.time())}|{message}"
        safe_send(target_sock, payload + '\n')
        return True
    return False

def list_users():
    """Return a comma-separated string of connected usernames."""
    with clients_lock:
        return ','.join(clients.keys())

def remove_client(username):
    """Remove a client from the dictionary and notify others."""
    sock = None
    with clients_lock:
        sock = clients.pop(username, None)
    if sock:
        try:
            sock.close()
        except:
            pass
        broadcast_system(f"{username} has left the chat.")

def handle_client(conn, addr):
    """Main handler for each client connection."""
    conn.settimeout(None)
    username = None
    try:
        # Step 1: ask for username
        safe_send(conn, "ENTERNAME|Please enter your desired username:\n")
        raw = conn.recv(1024)
        if not raw:
            conn.close()
            return
        name = raw.decode('utf-8').strip()
        if not name:
            safe_send(conn, "ERR|EMPTY_NAME|Username cannot be empty\n")
            conn.close()
            return

        # Enforce uniqueness
        with clients_lock:
            if name in clients:
                safe_send(conn, "ERR|DUPLICATE_NAME|Username taken\n")
                conn.close()
                return
            clients[name] = conn
            username = name

        # Welcome and notify others
        safe_send(conn, f"OK|Welcome {username}! You can type /list, /quit, or @username message for private.\n")
        broadcast_system(f"{username} has joined the chat.")

        # Receive loop
        while True:
            data = conn.recv(4096)
            if not data:
                break
            text = data.decode('utf-8').strip()
            if not text:
                continue

            # Commands
            if text == "/quit":
                # Clean exit
                break
            if text == "/list":
                users = list_users()
                safe_send(conn, f"USERS|{users}\n")
                continue

            # Private message (starts with @username space)
            if text.startswith('@'):
                parts = text.split(' ', 1)
                to_part = parts[0][1:].strip()  # recipient
                body = parts[1] if len(parts) > 1 else ''
                if not to_part:
                    safe_send(conn, "ERR|MALFORMED_PRIVATE|Usage: @username message\n")
                    continue
                sent = send_private(username, to_part, body)
                if sent:
                    # echo back to sender that private was sent
                    safe_send(conn, f"SENTPRV|{to_part}|{int(time.time())}|{body}\n")
                else:
                    safe_send(conn, f"ERR|NO_USER|User '{to_part}' not found\n")
                continue

            # Otherwise broadcast
            broadcast_message(username, text)

    except (ConnectionResetError, ConnectionAbortedError):
        # client disconnected abruptly
        pass
    except Exception as e:
        # unexpected error - log server-side, but keep running
        print("Exception in client handler:", e)
        traceback.print_exc()
    finally:
        if username:
            remove_client(username)
        else:
            try:
                conn.close()
            except:
                pass

def start_server(host=HOST, port=PORT):
    """Start listening for new clients and spawn threads for each."""
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((host, port))
    server_sock.listen(50)
    print(f"[+] Server started on {host}:{port}. Waiting for connections...")

    try:
        while True:
            conn, addr = server_sock.accept()
            # Spawn a thread for each client
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print("\n[!] Server shutting down (KeyboardInterrupt).")
    finally:
        # Close all client sockets
        with clients_lock:
            for s in clients.values():
                try:
                    s.close()
                except:
                    pass
            clients.clear()
        server_sock.close()

if __name__ == "__main__":
    start_server()
