import socket
import select

SERVERHOST = '0.0.0.0'
SERVERPORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVERHOST, SERVERPORT))
server_socket.listen()

print(f"Server listening on {SERVERHOST}:{SERVERPORT}")

# Keep track of connected sockets
sockets_list = [server_socket]
clients = {}

def broadcast(sender_socket, message):
    for client_socket in clients:
        if client_socket != sender_socket:
            client_socket.send(message)

while True:
    read_sockets, _, _ = select.select(sockets_list, [], [])

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            sockets_list.append(client_socket)
            clients[client_socket] = client_address
            print(f"Accepted connection from {client_address}")
        else:
            try:
                message = notified_socket.recv(1024)
                if not message:
                    raise ConnectionResetError()
                print(f"[{clients[notified_socket]}]: {message.decode().strip()}")
                broadcast(notified_socket, message)
            except:
                print(f"Connection closed from {clients[notified_socket]}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                notified_socket.close()
