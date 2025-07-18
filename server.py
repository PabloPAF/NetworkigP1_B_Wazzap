import socket
import select
import sys

SERVERHOST = '0.0.0.0'
SERVERPORT = 12345

PASSWORD = "1234"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVERHOST, SERVERPORT))
server_socket.listen()

print(f"Server listening on {SERVERHOST}:{SERVERPORT}")

# Keep track of connected sockets
sockets_list = [server_socket]
clients = {}
usernames = {}

def broadcast(sender_socket, message):
    for client_socket in clients:
        if client_socket != sender_socket:
            client_socket.send(message)

while True:
    read_sockets, _, _ = select.select(sockets_list, [], [])


    for sock in read_sockets:
        if sock == server_socket:
            client_socket, client_address = server_socket.accept()
            sockets_list.append(client_socket)
            auth = client_socket.recv(1024).decode().strip()
            username, passwd = auth.split("::", 1)
            if passwd != PASSWORD:
                client_socket.send("Wrong password. Connection refused.\n".encode())
                client_socket.close()
                sockets_list.remove(client_socket)
                continue
            clients[client_socket] = username
            print(f"{username} connected from {client_address}")
            broadcast(client_socket, f"🟢 {username} has joined the chat.")
            print(f"Accepted connection from {client_address}")
    else:
        try:
            message = sock.recv(1024)
            if not message:
                print("Client disconnected.")
                server_socket.close()
                sys.exit()
                print(f"Client: {message.decode().strip()}")
            else:
                msg = sys.stdin.readline()
                client_socket.send(msg.encode())
        except:
            print(f"Connection closed from {clients[sock]}")
            sockets_list.remove(sock)
            del clients[sock]
            sock.close()
