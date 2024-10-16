import socket, threading

from tkinter import *
import tkinter
from tkinter import simpledialog


class Chat:
    def __init__(self):

        HOST = 'localhost'
        PORT = 55555
        
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        
        login = Tk()
        login.withdraw()
        
        self.window_loaded = False
        self.active = True

        self.name = simpledialog.askstring('name', 'Enter your name: ', parent=login)
        self.chat_room = simpledialog.askstring('chat_room', 'Enter the chat room: ', parent=login)

    def window(self):
        pass

chat = Chat()
