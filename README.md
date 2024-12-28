# Peer-to-Peer File Sharing System with Centralized Index

This repository implements a peer-to-peer file sharing system with a centralized server. The system facilitates reliable messaging, file discovery, and file transfers among connected clients, using a centralized index for client management and communication.

---

## Features

### 1. Reliable Messaging
- Clients can exchange messages through the centralized server, ensuring seamless communication between peers.

### 2. File Discovery
- The system enables clients to discover files available across the network using the centralized server's index.

### 3. File Transfers
- Clients can upload files to the server or request files from other peers via the server, which acts as an intermediary to facilitate transfers.

### 4. Centralized Index
- The server maintains a list of active clients and their connections, enabling efficient routing of messages and file transfers.

---

## Architecture
The system consists of:
1. **Server**:
   - Manages client connections.
   - Maintains an index of active clients and available files.
   - Facilitates messaging and file transfers between clients.

2. **Client**:
   - Connects to the server to send messages, upload files, and request files.
   - Supports user commands for interaction with the system.

3. **Utility Functions**:
   - Provides helper methods for message formatting, file handling, and data transfer protocols.

---

## Files

### 1. `server.py`
- Implements the server-side logic for managing clients, routing messages, and handling file requests.

### 2. `client.py`
- Implements the client-side logic for connecting to the server, sending commands, and interacting with other clients.

### 3. `util.py`
- Contains utility functions for message encoding/decoding, error handling, and file management.

---

## Usage

### 1. Running the Server
Start the server using:
```bash
python3 server.py