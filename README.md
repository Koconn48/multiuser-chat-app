# Multiuser UDP Chat Application (Python)

This project is a Python-based multiuser desktop chat application using UDP sockets with both unicast and multicast communication. It features a graphical user interface (GUI) on the client side and a command-line server. The client is multithreaded to support real-time message sending and receiving.

## 🚀 How to Run

Start the server:
python3 src/server.py

Start the client:
python3 src/client.py localhost

## Overview

- The server receives messages via unicast UDP and broadcasts them using multicast.
- The client uses a multithreaded GUI (e.g., Tkinter), enabling users to interact while also receiving messages in real time.
- Users are uniquely identified by their login name.
- All messages are publicly broadcasted to all active users (no private messaging).

## Communication Protocol

Client ➡️ Server
- login,<user> — Register user
- msg,<msg> — Send a message
- list, — Request user list
- exit, — Leave the chat

Server ➡️ Client
- welcome,<user> — Notify new login
- msg,<msg> — Broadcast message
- bye,<user> — Notify user left
- list,<user1>,<user2>,... — Send active user list

## GUI Features

- Differentiates between incoming (<-) and outgoing (->) messages
- Input field for composing messages
- Simple and intuitive layout using Python GUI libraries

## Concurrency

- GUI runs on the main thread
- A separate thread listens for multicast messages
- Proper synchronization avoids race conditions

## Testing Notes

- The client should work with another team’s server, and vice versa
- The system supports multiple simultaneous users

## Project Rubric Coverage

- Proper creation and binding of server/client sockets
- Full support for all message types (login, msg, list, exit)
- GUI implementation for the client
- Concurrency and thread-safe GUI updates
