# The server its gonna be a open socket that keep listening and sending messages

import socket
import threading

HOST = 'localhost'
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen()

name_of_the_rooms = {}

def broadcast(chat_room, message):

    if isinstance(message, str):
        message = message.encode()
    for client_socket in name_of_the_rooms[chat_room]:
        try:
            client_socket.send(message)
        except Exception as e:
            print(f"Error : {e}")

def first_message(name, chat_room, client):
    while True:
        message = client.recv(1024)
        message = f'{name}: {message.decode()}\n'
        broadcast(chat_room, message)

while True:
    
    client, addr = server.accept()
    client.send(b'SALA')
    name = client.recv(1024).decode()
    chat_room = client.recv(1024).decode()
    
    if chat_room not in name_of_the_rooms.keys():
        name_of_the_rooms[chat_room] = []

    name_of_the_rooms[chat_room].append(client)

    print(f'{name} logged in the chat room {chat_room} | INFO {addr}')
    broadcast(chat_room, f'{name}: enter the chat room!\n')
    
    thread = threading.Thread(target=first_message, args=(name, chat_room, client))
    thread.start()