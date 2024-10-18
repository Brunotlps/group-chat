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

        thread = threading.Thread(target=self.connect)
        thread.start()
        self.window()

    def window(self):
        self.root = Tk()
        self.root.geometry('800x800')
        self.root.title('Chat')
        
        self.text_box = Text(self.root)
        self.text_box.place(relx=0.05, rely=0.01, width=700, height=600)

        self.text_field = Entry(self.root)
        self.text_field.place(relx=0.05, rely=0.8, width=500, height=20)

        self.send_button = Button(self.root, text='Send', command=self.send_message)
        self.send_button.place(relx=0.7, rely=0.8, width=100, height=20)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.root.mainloop()
    
    def connect(self):
        while True:

            received = self.client.recv(1024)
            if received == b'SALA': # Ponto de bug aqui, caso um usuário envie a mensagem 'SALA'
                self.client.send(self.chat_room.encode())
                self.client.send(self.name.encode())
            else:
                try:
                    self.text_box.insert('end', received.decode())
                except:
                    pass

    def close(self):
        
        self.root.destroy()
        self.client.close()

    def send_message(self):
        
        message = self.text_field.get()
        self.client.send(message.encode())

        

chat = Chat()
