
import socket
import threading
import struct
import pickle
import cv2
import imutils

# Inicialização do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)
port = 5000
socket_address = (host_ip, port)
server_socket.bind(socket_address)
server_socket.listen()
print("Listening at", socket_address)

# Lista para manter os clientes conectados
clients = []

clients_lock = threading.Lock()

# Função para broadcast
def broadcast(frame, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(frame)
            except:
                clients.remove(client)

# Thread para cada cliente
def client_thread(client_socket):
    while True:
        try:
            # Recebendo dados do cliente
            packet = client_socket.recv(8)
            if not packet: break
            msg_len = struct.unpack("Q", packet)[0]
            data = b""
            if msg_len > 10 * 1024 * 1024:  # 10MB
                print(f"Tamanho da mensagem muito grande: {msg_len}. Descartando...")
                continue  # Pula para 

            while len(data) < msg_len:
                packet = client_socket.recv(4*1024)  # 4K chunks
                data += packet
            # Broadcast do frame recebido
            

            message = struct.pack("Q", len(data)) + data
            # No servidor, antes de enviar o frame
            broadcast(message, client_socket)
        except:
            break
    client_socket.close()

# Aceitar conexões de clientes
while True:
    client_socket, addr = server_socket.accept()
    print(f"Connected to {addr}")
    clients.append(client_socket)
    threading.Thread(target=client_thread, args=(client_socket,)).start()
