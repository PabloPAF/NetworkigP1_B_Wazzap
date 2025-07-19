import socket
import select
import sys

CLIENTHOST = 'rnjhv-37-120-77-135.a.free.pinggy.link'  # update every 60 min
CLIENTPORT = 37677       # Same port as server from pinggy



username = input("Enter your username: ").strip()
password = input("Enter server password: ").strip()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((CLIENTHOST, CLIENTPORT))

client_socket.send(f"{username}::{password}".encode())

print("Connected to server.")

sockets_list = [sys.stdin, client_socket]

while True:
    read_sockets, _, _ = select.select(sockets_list, [], [])

    for sock in read_sockets:
        if sock == client_socket:
            message = sock.recv(1024)
            if not message:
                print("Disconnected from server.")
                sys.exit()
            print(f"Server: {message.decode().strip()}")
        else:
            msg = sys.stdin.readline()
            client_socket.send(msg.encode())
