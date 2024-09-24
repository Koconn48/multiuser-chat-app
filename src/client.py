'''
CS 3700 - Networking & Distributed Computing - Fall 2024
Instructor: Thyago Mota
Student(s):
Description: Project 1 - Multiuser Chat: Client
'''

from socket import *
from struct import pack
from datetime import datetime
import tkinter as tk
from tkinter import *
from threading import Thread, Semaphore
import sys

# "constants"
MCAST_ADDR  = '224.1.1.1'
MCAST_PORT  = 2241
SERVER_PORT = 4321
BUFFER      = 1024
GEOMETRY    = '570x400'

# the semaphore!
s = Semaphore(1)

class Window(Tk):
    def __init__(self, server_addr):
        super().__init__()

        # TODO #3 create the unicast UDP socket to send messages to the server
        

        # TODO #4 save the server address in an instance variable
        

        # TODO #5 build the GUI 
        

    # TODO #6 read the input text field, update the text box, and send the message to the server using the unicast UDP socket
    def enter(self, event):
        pass

    # TODO #7 updated the text box avoiding race conditions
    def update(self, msg):
        pass

    def exit(self):
        self.destroy()

class FromServerThread(Thread): 

    def __init__(self, window): 
        Thread.__init__(self)

        # TODO #8 create the mcast UDP socket to receive messages from the server; bind the socket to MCAST_PORT
        
        
        # formats MCAST_ADDR to a network format
        # group = inet_aton(MCAST_ADDR) 
        # formats the multicast group into a multicast request structure (mreq)
        # mreq = pack('4sL', group, INADDR_ANY)
        # TODO #9 configure the socket to read from the multicast group; uncomment and make changes in the line below based on how you named your socket's variable
        # self.from_server.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq)

        # TODO #10 save the window reference in an instance variable 
        


    # TODO #11 read from the socket and update the window's text box
    def run(self): 
        while True: 
            pass
            
if __name__ == '__main__': 

    if len(sys.argv) <= 1: 
        print(f'Use: {sys.argv[0]} server_address')
        sys.exit(1)
    server_addr = sys.argv[1].lower()

    window = Window(server_addr)
    from_server_thread = FromServerThread(window)
    from_server_thread.start()
    window.mainloop()
