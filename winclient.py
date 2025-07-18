import socket
import threading

CLIENTHOST = 'rnznb-77-211-6-17.a.free.pinggy.link'  # update every 60 min
CLIENTPORT = 35733  # Same port as server from pinggy

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024)
            if not message:
                print("Disconnected from server.")
                break
            print(f"Server: {message.decode().strip()}")
        except:
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((CLIENTHOST, CLIENTPORT))
print("Connected to server.")

# Starte Thread für Nachrichtenempfang
threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

# Haupt-Thread: Benutzer-Eingabe
while True:
    msg = input()
    if msg.strip().lower() == 'exit':
        break
    client_socket.send(msg.encode())

client_socket.close()
