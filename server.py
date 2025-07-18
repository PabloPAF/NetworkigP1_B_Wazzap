import socket
import select
import sys

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 12345      # Arbitrary non-privileged port

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Server listening on {HOST}:{PORT}")

client_socket, client_address = server_socket.accept()
print(f"Connected to {client_address}")

sockets_list = [sys.stdin, client_socket]

while True:
    read_sockets, _, _ = select.select(sockets_list, [], [])

    for sock in read_sockets:
        if sock == client_socket:
            message = sock.recv(1024)
            if not message:
                print("Client disconnected.")
                server_socket.close()
                sys.exit()
            print(f"Client: {message.decode().strip()}")
        else:
            msg = sys.stdin.readline()
            client_socket.send(msg.encode())


