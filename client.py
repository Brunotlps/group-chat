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

        font_style = ('Helvetica', 14)
        background_color = '#f0f0f0'
        text_color = '#333333'
        button_color = '#4CAF50'

        self.root.configure(bg=background_color)
        
        # Define uma coluna para expandir com o redimensionamento da janela
        self.root.grid_columnconfigure(0, weight=1)
        
        self.text_box = Text(self.root, state='disabled', bg='#fff', fg=text_color, font=font_style, bd=2, relief='sunken') # Inicialmente desativada para evitar edição direta
        self.text_box.grid(row=0, column=0, padx=10, pady=10, sticky='nsew') # Ocupa a maior parte da janela

        self.text_field = Entry(self.root, bg='#fff', fg=text_color, font=font_style, bd=2, relief='sunken')
        self.text_field.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

        self.send_button = Button(self.root, text='Send', command=self.send_message, bg=button_color, fg='#fff', font=font_style, bd=2, relief='raised')
        self.send_button.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0)
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
