# CN Assignment 1 - Chat Application (Socket Programming)

**Name:** Muhammad Hammad Butt  
**CMS ID:** 501399  
**GitHub Username:** HammadCodez  
**Repository:** [CN-Assignment1-MuhammadHammadButt-501399](https://github.com/HammadCodez/CN-Assignment1-MuhammadHammadButt-501399)

---

## Overview

This project is a **multi-client chat application** created in Python using socket programming.  
It allows multiple users to connect to a single server and chat in real time.  
The application supports both **broadcast** messages (visible to everyone) and **private** messages (using `@username`).  
Each user receives **join** and **leave** notifications automatically.

The server handles multiple clients simultaneously using **threads**, ensuring that the chat remains live and responsive even when several clients send messages together.

---

## Features

Multi-client chat system using sockets and threading  
Broadcast messages (everyone except sender)  
Private messaging via `@username message`  
Join and leave notifications for all users  
`/list` command to show currently connected users  
`/quit` command for clean disconnection  
Error handling for duplicate usernames and invalid messages  
Informative, human-friendly server logs and console outputs

---

## How to Run the Project

### Step 1 — Start the Server

Open a terminal in your project folder and run:

```bash
python3 server.py

You will see:

[+] Server started on 0.0.0.0:7777. Waiting for connections...

Step 2 — Start the Clients

Open new terminal windows for each client and run:

python3 client.py 127.0.0.1 7777


Each client will:

Enter a username

Start chatting instantly

Commands (for the client)
Command	Description
/list	Shows all currently connected usernames
/quit	Disconnects cleanly from the chat
@username message	Sends a private message to that user
(Any other message)	Broadcasts to all users

Screenshots & Evidence

All proof of functionality is placed in the screenshots/ folder.
The following screenshots are included:

01_server_running.png — Server started successfully

02_clients_connected.png — Two clients joined

03_broadcast_message.png — Broadcast working

04_private_message.png — Private message between clients

05_list_users.png - listiing all the connected users

06_duplicate_username.png — Duplicate username error

07_leave_notification.png — Leave message visible to others

08_abrupt_network_or_other_quit.png - when client leaves for any reason
```
