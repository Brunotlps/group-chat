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
        background_color = '#1a1a1a'
        text_color = '#cccccc'
        button_color = '#357a38'

        self.root.configure(bg=background_color)
        
        # Define uma coluna para expandir com o redimensionamento da janela
        self.root.grid_columnconfigure(0, weight=1)
        
        self.text_box = Text(self.root, state='disabled', bg=background_color, fg=text_color, font=font_style, bd=2, relief='sunken') # Inicialmente desativada para evitar edição direta
        self.text_box.grid(row=0, column=0, padx=10, pady=10, sticky='nsew') # Ocupa a maior parte da janela

        self.text_field = Entry(self.root, bg='#fff', fg='#000000', font=font_style, bd=2, relief='sunken')
        self.text_field.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

        self.send_button = Button(self.root, text='Send', command=self.send_message, bg=button_color, fg='#fff', font=font_style, bd=2, relief='raised')
        self.send_button.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        self.text_field.bind("<Return>", self.enter_pressed)

        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0)
        self.root.mainloop()
    
    def connect(self):
        while True:

            try:
                received = self.client.recv(1024)
                if received == b"SALA":
                    self.client.send(self.name.encode())
                    self.client.send(self.chat_room.encode())
                else:
                    self.root.after(0,self.update_text_box, received.decode())
            except Exception as e:
                print(f"Error: {e}")
    
    def close(self):
        self.root.destroy()
        self.client.close()

    def send_message(self):
        message = self.text_field.get()
        self.text_field.delete(0, END)  # Limpa o campo de texto após o envio
        self.client.send(message.encode())
    
    def update_text_box(self, message):
        self.text_box.config(state='normal')
        self.text_box.insert('end', message)
        self.text_box.config(state='disabled')
        self.text_box.yview('end')  # Auto-scroll para o final


    def enter_pressed(self, event):
        self.send_message()
        

chat = Chat()
