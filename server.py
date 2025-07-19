import socket
import select
import time

SERVERHOST = '0.0.0.0'
SERVERPORT = 12345
PASSWORD = "1234"
history = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVERHOST, SERVERPORT))
server_socket.listen()

print(f" Server listening on {SERVERHOST}:{SERVERPORT}")

sockets_list = [server_socket]
clients = {}  # client_socket: username


def broadcast(sender_socket, message):
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode())
            except:
                pass


while True:
    read_sockets, _, _ = select.select(sockets_list, [], [])

    for sock in read_sockets:
        if sock == server_socket:
            client_socket, client_address = server_socket.accept()
            sockets_list.append(client_socket)

            try:
                auth = client_socket.recv(1024).decode().strip()
                username, passwd = auth.split("::", 1)
                failed_attempts = 0

                if passwd != PASSWORD:
                    client_socket.send("Wrong password. bye.\n".encode())
                    print(f"{username} got kicked out")
                    client_socket.close()
                    sockets_list.remove(client_socket)
                    continue

                clients[client_socket] = username
                print(f"{username} connected from {client_address}")
                broadcast(client_socket, f"{username} just joined")
                client_socket.send("connected.\n".encode())

            except Exception as e:
                print(f"Error during authentication: {e}")
                client_socket.close()
                sockets_list.remove(client_socket)

        else:
            try:
                message = sock.recv(1024)
                if not message:
                    raise ConnectionResetError()

                user = clients.get(sock, "unknown")
                msg = message.decode().strip()

                # Handle private message
                if msg.startswith("/msg "):
                    parts = msg.split(" ", 2)
                    if len(parts) >= 3:
                        target_user = parts[1]
                        private_msg = parts[2]
                        target_socket = None
                        for s, uname in clients.items():
                            if uname == target_user:
                                target_socket = s
                                break
                        if target_socket:
                            try:
                                target_socket.send(f"[PM from {user}] {private_msg}\n".encode())
                                sock.send(f"[PM to {target_user}] {private_msg}\n".encode())
                            except Exception as e:
                                print(f"Error sending PM: {e}")
                        else:
                            sock.send(f"[Server] User {target_user} not found.\n".encode())
                    continue

                # Normal broadcast
                timestamp = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
                print(f"[{timestamp} {user}]: {msg}")
                broadcast(sock, f"{user}: {msg}")
                history.append(f"{timestamp} {user}: {msg}")
                if msg == "download":
                    print(f"f User {user} requested downloading chat history")
                    with open("chat_history.txt", "a") as f:
                        f.write(f"{history}")
            except:
                user = clients.get(sock, "unknown")
                print(f"{user} disconnected.")
                broadcast(sock,f"{user} left")
                if sock in clients:
                    del clients[sock]
                if sock in sockets_list:
                    sockets_list.remove(sock)
                sock.close()
