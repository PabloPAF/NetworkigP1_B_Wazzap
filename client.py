import socket
import select
import sys

CLIENTHOST = 'rnbts-77-211-6-17.a.free.pinggy.link'  # update every 60 min
CLIENTPORT = 36471        # Same port as server from pinggy

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((CLIENTHOST, CLIENTPORT))
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
