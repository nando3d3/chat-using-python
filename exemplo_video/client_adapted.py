
import socket
import cv2
import pickle
import struct
import threading
import imutils
import numpy as np

def receive_video(client_socket):
    while True:
        try:
            # Recebe o tamanho do frame
            packet = client_socket.recv(8)
            if not packet:
                break
            msg_len = struct.unpack("Q", packet)[0]


            # Recebe o frame completo
            data = b""
            while len(data) < msg_len:
                packet = client_socket.recv(min(4*1024, msg_len - len(data)))
                if not packet: 
                    break
                data += packet

            if len(data) == msg_len:
                try:
                    frame = pickle.loads(data)
                    # No servidor, antes de enviar o fram
                    # Verifica se o frame é um array do NumPy
                    if isinstance(frame, np.ndarray):
                        cv2.imshow('Received Video', frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                except Exception as e:
                    print(f"Erro na deserialização: {e}")
            else:
                print("Frame incompleto recebido")
                
        except Exception as e:
            print(f"Exception: {e}")
            break
    client_socket.close()


send_lock = threading.Lock()

def send_video(vid, client_socket):
    with send_lock:
        while vid.isOpened():
            try:
                    img, frame = vid.read()
                    frame = imutils.resize(frame, width=380)
                    a = pickle.dumps(frame)
                    message = struct.pack("Q", len(a)) + a
                    # cv2.imshow(f"TO: {host_ip}",frame)
                    client_socket.sendall(message)
                   
            except:
                break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.0.6'  # Servidor IP
port = 5000
client_socket.connect((host_ip, port))

camera = False
if camera:
    vid = cv2.VideoCapture(0)
else:
    vid = cv2.VideoCapture('videos/Video Paradigmas.mp4')

# Iniciando threads para enviar e receber vídeo
threading.Thread(target=send_video, args=(vid, client_socket)).start()
threading.Thread(target=receive_video, args=(client_socket,)).start()
