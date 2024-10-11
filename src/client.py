'''
CS 3700 - Networking & Distributed Computing - Fall 2024
Instructor: Thyago Mota
Student(s): Kevin O'Connell
Description: Project 1 - Multiuser Chat: Client
'''

import socket
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

        self.username = None
        self.logged_in = False

        # TODO #5 build the GUI
        self.title("CS3700: Multiuser Chat")
        self.geometry(GEOMETRY)
        self.text_box = Text(self)
        self.text_box.pack(pady=10, padx=10, expand=True, fill='both')
        self.input_field = Entry(self)
        self.input_field.pack(side="left", pady=10, padx=10, expand=True, fill="x")
        self.input_field.bind("<Return>", self.enter)
        self.send_button = Button(self, text="Send", command=self.enter)
        self.send_button.pack(side="right", padx=10)
        self.protocol("WM_DELETE_WINDOW", self.exit)

        # TODO #3 create the unicast UDP socket to send messages to the server
        self.unicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # TODO #4 save the server address in an instance variable
        self.server_addr = (server_addr, SERVER_PORT)

        self.from_server_thread = FromServerThread(self)
        self.from_server_thread.start()
        self.from_server_unicast_thread = FromServerUnicastThread(self)
        self.from_server_unicast_thread.start()
    
    def enter(self, event=None):
        msg = self.input_field.get()
        if msg:
            # TODO #6 read the input text field, update the text box, and send the message to the server using the unicast UDP socket
            if not self.logged_in:
                if msg.startswith("login,") and len(msg.split(",", 1)) == 2:
                    self.username = msg.split(",", 1)[1].strip()
                    if self.username:
                        self.unicast_socket.sendto(msg.encode(), self.server_addr)
                        self.logged_in = True
                        self.update(f"You are logged in as {self.username}\n")
                        self.title(f"CS3700: {self.username}'s Chat")
                    else:
                        self.update("Invalid login command. Usage: login,<username>\n")
                else:
                    self.update("You must log in first using: login,<username>\n")
            else:
                if msg == "list,":
                    self.unicast_socket.sendto(b"list,", self.server_addr)
                elif msg == "exit,":
                    self.unicast_socket.sendto(f"exit,{self.username}".encode(), self.server_addr)
                    self.unicast_socket.close()
                    self.from_server_thread.stop()
                    self.from_server_unicast_thread.stop()
                    self.destroy()
                    return
                elif msg.startswith("msg,") and len(msg.split(",", 1)) == 2:
                    message_content = msg.split(",", 1)[1]
                    self.update(f"-> {message_content}\n")
                    self.unicast_socket.sendto(msg.encode(), self.server_addr)
                else:
                    self.update("Invalid command. Use 'msg,<message>', 'list,', or 'exit,'\n")
            self.input_field.delete(0, 'end')

    def update(self, msg):
        # TODO #7 updated the text box avoiding race conditions
        s.acquire()
        self.text_box.insert(END, msg)
        self.text_box.yview(END)
        s.release()

    def exit(self):
        if self.logged_in:
            self.unicast_socket.sendto(f"exit,{self.username}".encode(), self.server_addr)
        self.unicast_socket.close()
        self.from_server_thread.stop()
        self.from_server_unicast_thread.stop()
        self.destroy()

class FromServerThread(Thread): 
    def __init__(self, window): 
        Thread.__init__(self)
        # TODO #10 save the window reference in an instance variable
        self.window = window
        self.running = True

        # TODO #8 create the mcast UDP socket to receive messages from the server; bind the socket to MCAST_PORT
        self.mcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.mcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.mcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except AttributeError:
            print("SO_REUSEPORT not available on this system.")
        except OSError as e:
            print(f"Could not set SO_REUSEPORT: {e}")
        self.mcast_socket.bind((MCAST_ADDR, MCAST_PORT))
        
        # formats MCAST_ADDR to a network format
        # group = inet_aton(MCAST_ADDR) 
        group = socket.inet_aton(MCAST_ADDR)

        # formats the multicast group into a multicast request structure (mreq)
        # mreq = pack('4sL', group, INADDR_ANY)
        mreq = pack('4sL', group, socket.INADDR_ANY)

        # TODO #9 configure the socket to read from the multicast group; uncomment and make changes in the line below based on how you named your socket's variable
        # self.from_server.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq)
        self.mcast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        self.mcast_socket.settimeout(1)

    def run(self): 
        # TODO #11 read from the socket and update the window's text box
        while self.running: 
            try:
                data, addr = self.mcast_socket.recvfrom(BUFFER)
                msg = data.decode()
                self.window.update(f"<- {msg}\n")
            except socket.timeout:
                continue
            except OSError:
                break
        self.mcast_socket.close()

    def stop(self):
        self.running = False
        self.mcast_socket.close()

class FromServerUnicastThread(Thread):
    def __init__(self, window):
        Thread.__init__(self)
        self.window = window
        self.running = True

        self.unicast_socket = window.unicast_socket
        self.unicast_socket.settimeout(1)

    def run(self):
        while self.running:
            try:
                data, addr = self.unicast_socket.recvfrom(BUFFER)
                msg = data.decode()
                self.window.update(f"<- {msg}\n")
            except socket.timeout:
                continue
            except OSError:
                break

    def stop(self):
        self.running = False

if __name__ == '__main__': 
    if len(sys.argv) <= 1: 
        print(f'Use: {sys.argv[0]} server_address')
        sys.exit(1)
    server_addr = sys.argv[1].lower()

    window = Window(server_addr)
    window.mainloop()