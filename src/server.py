'''
CS 3700 - Networking & Distributed Computing - Fall 2024
Instructor: Thyago Mota
Student(s): Kevin O'Connell
Description: Project 1 - Multiuser Chat: Server
'''

from socket import socket, IP_MULTICAST_TTL, IPPROTO_IP, AF_INET, SOCK_DGRAM
from datetime import datetime
from threading import Thread
import sys

# "constants"
MCAST_ADDR  = '224.1.1.1'
MCAST_PORT  = 2241
SERVER_ADDR = '0.0.0.0'
SERVER_PORT = 4321
BUFFER      = 1024

class Server:
    def __init__(self):
        self.running = True
        # suggested dictionary to keep track of logged in users
        self.users = {}

        # TODO #1 create the 2 sockets: one to receive messages from the clients and another one to send messages to the clients (using the mcast group:port); make sure the socket that receives messages is bound to (SERVER_ADDR, SERVER_PORT)
        self.unicast_socket = socket(AF_INET, SOCK_DGRAM)
        self.unicast_socket.bind((SERVER_ADDR, SERVER_PORT))

        self.mcast_socket = socket(AF_INET, SOCK_DGRAM)
        self.mcast_socket.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, 1)

        self.multicast_group = (MCAST_ADDR, MCAST_PORT)

        print(f'Multiuser server is ready on {SERVER_ADDR}:{SERVER_PORT}!')

    def start(self):
        console_thread = Thread(target=self.listen_for_console_input)
        console_thread.start()

        # TODO #2 implement the communication protocol
        while self.running:
            try:
                data, addr = self.unicast_socket.recvfrom(BUFFER)
                msg = data.decode().split(',', 1)
                msg_type = msg[0]

                if msg_type == 'login':
                    if len(msg) < 2:
                        continue
                    user = msg[1]
                    self.users[addr] = user
                    print(f"{datetime.now()} login request has arrived from {user}@{addr}")
                    self.mcast_socket.sendto(f"welcome,{user}".encode(), self.multicast_group)

                elif msg_type == 'msg':
                    if len(msg) < 2:
                        continue
                    user_msg = msg[1]
                    user = self.users.get(addr, "Unknown")
                    print(f"{datetime.now()} msg \"{user_msg}\" has arrived from user: {user}@{addr}")
                    self.mcast_socket.sendto(f"msg,{user}: {user_msg}".encode(), self.multicast_group)

                elif msg_type == 'list':
                    user_list = ",".join(self.users.values())
                    user = self.users.get(addr, "Unknown")
                    print(f"{datetime.now()} list request has arrived from user: {user}@{addr}")
                    self.unicast_socket.sendto(f"list,{user_list}".encode(), addr)

                elif msg_type == 'exit':
                    user = self.users.pop(addr, "Unknown")
                    print(f"{datetime.now()} exit request has arrived from {user}@{addr}")
                    self.mcast_socket.sendto(f"bye,{user}".encode(), self.multicast_group)

            except OSError:
                break

        self.unicast_socket.close()
        self.mcast_socket.close()
        print("Server has shut down.")

    def listen_for_console_input(self):
        while self.running:
            command = input()
            if command.strip().lower() == 'exit,':
                print("Shutdown command received. Shutting down the server...")
                self.running = False
                self.unicast_socket.close()
                break

if __name__ == '__main__':
    server = Server()
    server.start()