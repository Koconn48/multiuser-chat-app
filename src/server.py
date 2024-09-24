'''
CS 3700 - Networking & Distributed Computing - Fall 2024
Instructor: Thyago Mota
Student(s):
Description: Project 1 - Multiuser Chat: Server
'''

from socket import socket, AF_INET, SOCK_DGRAM
from datetime import datetime

# "constants"
MCAST_ADDR  = '224.1.1.1'
MCAST_PORT  = 2241
SERVER_ADDR = '0.0.0.0'
SERVER_PORT = 4321
BUFFER      = 1024

if __name__ == '__main__': 
    
    # suggested dictionary to keep track of logged in users
    users = {}

    # TODO #1 create the 2 sockets: one to receive messages from the clients and another one to send messages to the clients (using the mcast group:port); make sure the socket that receives messages is bound to (SERVER_ADDR, SERVER_PORT)

    # TODO #2 implement the communication protocol
    