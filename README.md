# CN Assignment 1: Multi-Client Chat Application

A robust, multi-client, real-time chat application built with Python socket programming and threading, featuring both broadcast and private messaging capabilities.

## Author Information

- **Author:** Muhammad Hammad Butt
- **CMS ID:** 501399
- **Section:** SE-15-B
- **Course:** Computer Networks (EE-353)
- **GitHub Username:** HammadCodez
- **Repository:** CN-Assignment1-MuhammadHammadButt-501399

---

## 1. Overview

This project implements a fully functional multi-client chat system designed to meet the requirements of the Computer Networks (EE-353) assignment. The system leverages Python's built-in `socket` and `threading` libraries to enable multiple clients to connect to a single server and exchange messages in real time.

The server efficiently manages all client connections concurrently, handles user states, and relays messages between participants. The client provides an intuitive command-line interface that allows users to seamlessly send and receive messages while maintaining clear visual separation between different message types.

### Core Capabilities

- **Broadcast Messaging:** Send messages to all connected users
- **Private Messaging:** Direct messages using `@username` syntax
- **Real-time Notifications:** System-wide join and leave announcements
- **Robust Error Handling:** Comprehensive handling for duplicate usernames and connection issues
- **User Management:** Real-time user listing and status monitoring

## 2. Feature Set

### Multi-Client Architecture

- The server spawns a dedicated thread for each connected client, supporting multiple concurrent users without blocking operations

### User Identity Management

- Server-enforced unique usernames with immediate rejection of duplicate names
- Graceful handling of username conflicts during connection

### Messaging System

- **Broadcast Messages:** Default behavior for all non-command messages
- **Private Messaging:** Targeted communication using `@username message` format
- **System Messages:** Automated notifications for user join/leave events

### User Interface & Commands

- **User Listing:** `/list` command displays all currently connected users
- **Graceful Exit:** `/quit` command enables clean disconnection from server
- **Formatted Output:** Clear visual distinction between message types with labels and timestamps

### Reliability Features

- Robust error handling for abrupt disconnections (network failure, force quit)
- Thread-safe operations preventing race conditions in shared resources
- Automatic cleanup of disconnected client resources

## 3. Technical Architecture

### System Components

The application is structured into two primary components that work in concert to deliver the chat experience.

#### Server Implementation (`server.py`)

**Network Configuration**

- Binds to `0.0.0.0` (all network interfaces) on port `7777`
- Listens for incoming TCP connections with configurable backlog

**Concurrency Model**

- Utilizes `threading.Thread` to handle each client connection independently
- Maintains non-blocking operation regardless of client count

**State Management**

- Global dictionary structure: `clients = {username: socket}`
- Centralized storage for all active client connections and their metadata

**Thread Safety**

- `threading.Lock()` ensures atomic operations on shared `clients` dictionary
- Prevents race conditions during concurrent access scenarios

#### Client Implementation (`client.py`)

**Dual-Thread Architecture**

1. **Receiver Thread:** Continuously listens for incoming server messages
2. **Main Thread:** Handles user input and message transmission

**Message Processing**

- `pretty_print_server_msg()` function parses server protocol
- Applies human-readable formatting with type labels (`[PRIVATE]`, `[SYSTEM]`)
- Formats timestamps for improved user experience

### Communication Protocol

A lightweight, pipe-delimited protocol facilitates clear message differentiation between server and clients:

> `TYPE|field1|field2|...`

**Protocol Examples:**

- `SYSTEM|1678886400|Hammad has joined the chat.`
- `MSG|Ali|1678886405|Hello everyone!`
- `PRV|Bilal|Ali|1678886410|This is a private message.`
- `USERS|Hammad,Ali,Bilal`
  ( name could be any )

## 4. Project Structure

```
CN-Assignment1-MuhammadHammadButt-501399/
├── server.py              # Main threaded server implementation
├── client.py              # Client application with UI
├── README.md              # Comprehensive documentation
├── testplan.txt           # Detailed test cases and validation results
├── requirements.txt       # Python version and dependency information
└── screenshots/           # Visual evidence of test execution
```

## 5. Installation & Execution

### Prerequisites

- **Python 3.8 or higher** (Developed and tested with Python 3.10.0)
- **No external dependencies** - utilizes only Python standard libraries:
  - `socket`, `threading`, `time`, `sys`

### Deployment Instructions

#### Step 1: Server Initialization

Navigate to the project directory and execute:

```bash
python3 server.py
```

**Expected Server Output:**

```
[+] Server started on 0.0.0.0:7777. Waiting for connections...
```

#### Step 2: Client Connection

For each client, open a new terminal window and run:

```bash
python3 client.py 127.0.0.1 7777
```

_Note: IP and port parameters default to `127.0.0.1:7777` if omitted_

The client will prompt for a username. After successful validation (non-duplicate), the chat interface becomes active.

### Client Command Reference

| Command             | Description                                |
| ------------------- | ------------------------------------------ |
| `/list`             | Display all currently connected users      |
| `/quit`             | Cleanly disconnect from chat server        |
| `@username message` | Send private message to specified user     |
| Any other text      | Broadcast message to all chat participants |

## 6. Testing & Validation

A comprehensive test plan (`testplan.txt`) was executed to validate all system functionality. All test scenarios passed successfully.

### Test Coverage Summary

- **Server Startup:** Verification of server initialization and connection acceptance
- **Broadcast Messaging:** Confirmation of message delivery to all connected clients
- **Private Messaging:** Validation of targeted message delivery to specific users
- **Username Management:** Testing of duplicate username rejection mechanism
- **User Listing:** Verification of accurate connected user enumeration
- **Graceful Disconnection:** Testing of clean exit procedures and notifications
- **Robustness Testing:** Validation of system stability during abrupt disconnections

_Complete test evidence and screenshots available in the `screenshots/` directory._

## 7. Development Insights

### Technical Challenges

**Concurrency Management**

- Implemented thread synchronization using `threading.Lock` to prevent race conditions in shared data structures
- Ensured atomic operations on the client dictionary during connection/disconnection events

**Connection Reliability**

- Developed robust disconnection handling for various failure scenarios (network issues, forced termination)
- Implemented comprehensive exception handling to maintain server stability

**Protocol Design**

- Created an efficient, extensible text-based protocol for message type differentiation
- Balanced simplicity with functionality in communication schema

### Key Learnings

**TCP/IP Socket Programming**

- Gained practical experience in low-level network programming
- Understood socket lifecycle management and data transmission protocols

**Concurrent Programming**

- Mastered thread synchronization techniques for shared resource protection
- Learned to design thread-safe applications in Python

**Software Engineering Practices**

- Enhanced skills in project architecture and modular design
- Appreciated the importance of comprehensive documentation and systematic testing methodologies

---

_This project demonstrates practical implementation of fundamental computer networking concepts while emphasizing software reliability and user experience._
