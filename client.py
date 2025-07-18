import socket
import select
import sys

HOST = '127.0.0.1'  # Server IP address
PORT = 12345        # Same port as server

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("[*] Connected to server.")

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
