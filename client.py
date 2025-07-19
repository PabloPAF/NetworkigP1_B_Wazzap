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
print("You joined the chat.")

sockets_list = [sys.stdin, client_socket]

while True:
    read_sockets, _, _ = select.select(sockets_list, [], [])

    for sock in read_sockets:
        if sock == client_socket:
            message = sock.recv(1024)
            if not message:
                print("Disconnected from server.")
                sys.exit()
            decoded_message = message.decode().strip()
            if "]" in decoded_message:
                try:
                    timestamp_part, after_bracket = decoded_message.split("]", 1)
                    timestamp = timestamp_part.strip("[").strip()
                    after_bracket = after_bracket.strip()
                    if ":" in after_bracket:
                        sender, content = after_bracket.split(":", 1)
                        sender = sender.strip()
                        content = content.strip()
                        if sender.lower() == username.lower():
                            print(f"You | {timestamp} : {content}")
                        else:
                            print(f"{sender} | {timestamp} : {content}")
                    else:
                        print(decoded_message)
                except Exception:
                    print(decoded_message)
            else:
                print(decoded_message)
        else:
            msg = sys.stdin.readline()
            client_socket.send(msg.encode())
            # Clear the previous typed line
            import sys
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
            # Print locally with timestamp
            import time
            timestamp = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
            print(f"You | {timestamp} : {msg.strip()}")
