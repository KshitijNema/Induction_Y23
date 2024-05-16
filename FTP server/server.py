import socket
import threading
import time
import os

#constants
DEFAULT_PORT = 9988
FORMAT = 'utf-8'
HEADER_LENGTH = 10
DISCONNECT_MESSAGE = "disconnect"

#server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', DEFAULT_PORT))

def handle_client(client_socket, client_address, users, passwords, banned_users):
    print(f"New connection: {client_address}")
    connected = True
    client_socket.send("You are connected to the server. Please provide your credentials.".encode(FORMAT))

    while connected:
        #authorization
        auth_status = authorize(client_socket, users, passwords, banned_users)
        if auth_status == 0:
            break

        #ater successful authorization, handle client commands
        if auth_status == 1:  #regular user
            while True:
                try:
                    command = client_socket.recv(1024).decode(FORMAT)
                    if command == "LIST":
                        list_files(client_socket)
                    elif command.startswith("RETR"):
                        _, filename = command.split(' ', 1)
                        retrieve_file(client_socket, filename.strip())
                    elif command.startswith("STOR"):
                        _, filename = command.split(' ', 1)
                        store_file(client_socket, filename)
                    elif command == "QUIT":
                        print(f"Client {client_address} disconnected")
                        client_socket.close()
                        connected = False
                        break
                    else:
                        print("Unknown command received.")
                        break

                except Exception as e:
                    print(f"Error occurred: {e}")
                    break

def authorize(client_socket, users, passwords, banned_users):
    username = client_socket.recv(1024).decode(FORMAT)
    password = client_socket.recv(1024).decode(FORMAT)

    if username in users and username not in banned_users:
        if password == passwords[users.index(username)]:
            if password == "letmesleep" and username == "admin":
                client_socket.send("11".encode(FORMAT))
                return 2  #admin access
            else:
                client_socket.send("10".encode(FORMAT))  #successful login
                return 1  #regular user
        else:
            client_socket.send("Invalid credentials".encode(FORMAT))
            client_socket.close()
            return 0  #invalid credentials
    elif username not in banned_users:
        client_socket.send("3".encode(FORMAT))  #prompt to register
        res = client_socket.recv(1024).decode(FORMAT)
        if res == "1":
            users.append(username)
            passwords.append(password)
            print(users)
            print(passwords)
            return 1  #fegular user
        else:
            client_socket.close()
            return 0  #registration denied
    else:
        client_socket.send("4".encode(FORMAT))
        return 0  #banned user

def list_files(client_socket):
    files = os.listdir("./")
    client_socket.send("\n".join(files).encode())

def retrieve_file(client_socket, file_path):
    client_socket.send(file_path.encode())
    time.sleep(0.1)
    with open(file_path, 'rb') as f:
        data = f.read()
        client_socket.sendall(data)

def store_file(client_socket, file_path):
    data = client_socket.recv(1024).decode()
    with open(str(file_path), 'w') as f:
        f.write(data)
    client_socket.send(b"File stored successfully!")

def ban_user(username, banned_users):
    banned_users.append(username)

def unban_user(username, banned_users):
    banned_users.remove(username)

def delete_user(username, users, passwords):
    i = users.index(username)
    users.remove(username)
    passwords.pop(i)

def add_user(username, password, users, passwords):
    users.append(username)
    passwords.append(password)

def start_server():
    server_socket.listen()
    print("Server is listening")
    users = ['admin']
    passwords = ['letmesleep']
    banned_users = []

    while True:
        client_socket, client_address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address, users, passwords, banned_users))
        thread.start()
        print(f'Active clients: {threading.active_count() - 1}')

print("Server is starting...")
start_server()
