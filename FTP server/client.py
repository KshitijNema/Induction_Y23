import socket
import threading
import time
import pickle
IP=socket.gethostbyname(socket.gethostname())
PORT=9988
FORMAT='utf-8'
HEADER=10
DISCONNECT_MESSAGE="disconnect"

ADDR=(IP,PORT)

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect(ADDR)
#welcome message
print(client.recv(1024).decode(FORMAT))
def send(msg):
    message=msg.encode(FORMAT)
    client.send(message)

def RETR(client,path):
    data = client.recv(1024).decode()

    with open(path,'w') as f:
        data = client.recv(1024).decode()
        f.write(data)

def STOR(client,path):
    with open(path,'rb') as f:
        data = f.read()
        client.sendall(data)

def authorization():

    user=input("Enter username:")
    send(user)
    passw=input("Enter password:")
    send(passw)
    s=client.recv(1024).decode(FORMAT)
    if s=="11":
        print("Logged in as admin")
        return 1
    elif s=="10":
        print("Login successful")
        return 0

    elif s=="3":
        print("You are a new user do you want to sign up.\nIf yes press 1,else 0")
        ch=int(input("1/0:"))
        if ch==1:
            send("1")
            print("Registered as a new user")
        else :
            send("hfjd")
            print("Thank you")
            client.close()

        return 0
    elif s=="4":
        print("You are banned from the server")
        client.close()

    else :
        print("Invalid credentials ")
        client.close()


def LIST(client):
    print(client.recv(1024).decode(FORMAT))


def RETR(client,path):
    data = client.recv(1024).decode()

    with open(path,'w') as f:
        data = client.recv(1024).decode()
        f.write(data)

    print("File retrieved succesfully!")




role=authorization()

# After successful authorization, take user commands
if role==0:
    while True:
        command = input("Enter a command (LIST, RETR <filename>, STOR <filename>or QUIT): ").strip()
        send(command)
        if command == "LIST":
            LIST(client)
        elif command.startswith("RETR"):
            _, filename = command.split(' ', 1)

            RETR(client,filename.strip())
        elif command.startswith("STOR"):
            _, filename = command.split(' ', 1)

            STOR(client,filename)
        elif command == "QUIT":
            print("Disconnecting from the server...")
            break
        else:
            print("Invalid command. Please try again.")
if role == 1:
    while True:
        command = input("Enter a command (ADDUSER <username> <password>, DELUSER <username>, BAN <username>,UNBAN <username>,QUIT): ").strip()
        send(command)
        if command.startswith("ADDUSER"):
            _, username, password = command.split(' ', 2)
            print(f"{username} is successfully added to the server")


        elif command.startswith("DELUSER"):
            _, username = command.split(' ', 1)
            print(f"{username} is deleted from the server")

        elif command.startswith("BAN"):
            _, username = command.split(' ', 1)
            print(f"{username} is banned from the server")

        elif command.startswith("UNBAN"):
            _, username = command.split(' ', 1)
            print(f"{username} is unbanned from the server")


        elif command == "QUIT":
            print("Disconnecting from the server...")
            break
        else:
            print("Invalid command. Please try again.")


client.close()