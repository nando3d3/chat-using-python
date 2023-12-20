import socket, cv2, pickle, struct
import threading
import pyshine as ps
import cv2
from time import sleep

class Server():
    def __init__(self, host = 'localhost', port = 5000, qnt_users = 10):
        self.host = host
        self.port = port
        self.qnt_users = qnt_users
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET is IPv4 and SOCK_STREAM is TCP
        self.server.bind((self.host, self.port)) # associa o socket a um endereço específico
        self.server.listen()
        self.clients = []
        self.nicknames = []
    
    def broadcast(self, message):
        for client in self.clients:
            client.send(message)
    
    def handle_client(self, client):
    
        while True:
            try:
                message = client.recv(1024)
                mess_decode = message.decode('ascii')

                if mess_decode.startswith('KICK'):
                    if self.nicknames[self.clients.index(client)] == 'admin':
                        name_to_kick = mess_decode[5:]
                        self.kick_user(name_to_kick)
                    else:
                        client.send('Command Refused!'.encode('ascii'))
                elif mess_decode.startswith('BAN'):
                    if self.nicknames[self.clients.index(client)] == 'admin':
                        name_to_ban = mess_decode[4:]
                        self.kick_user(name_to_ban)
                        with open('src/resources/bans.txt', 'a') as f:
                            f.write(f'{name_to_ban}\n')
                        print(f'{name_to_ban} was banned by the Admin!')
                    else:
                        client.send('Command Refused!'.encode('ascii'))
                elif mess_decode != '':
                    self.broadcast(message)  # As soon as message received, broadcast it.

            except socket.error:
                if client in self.clients:
                    index = self.clients.index(client)
                    # Index is used to remove client from list after getting disconnected
                    self.clients.remove(client)
                    client.close()
                    nickname = self.nicknames[index]
                    self.broadcast(f'{nickname} left the Chat!'.encode('ascii'))
                    self.nicknames.remove(nickname)
                    break
    
    def show_client(self, client_socket, addr):
        try:
            data = b""
            payload_size = struct.calcsize("Q")
            while True:
                while len(data) < payload_size:
                    packet = client_socket.recv(4*1024) # 4K
                    if not packet: break
                    data+=packet
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q",packed_msg_size)[0]
                
                while len(data) < msg_size:
                    data += client_socket.recv(4*1024)
                frame_data = data[:msg_size]
                data  = data[msg_size:]
                frame = pickle.loads(frame_data)
                text  =  f"CLIENT: {addr}"
                frame = ps.putBText(frame,text,10,10,vspace=10,hspace=1,font_scale=0.7,
                        background_RGB=(255,0,0),text_RGB=(255,250,250))	
                cv2.imshow(f"FROM {addr}",frame)
                key = cv2.waitKey(1) & 0xFF
                if key  == ord('q'):
                    break
            self.clients.remove(client_socket)
            client_socket.close()
        except Exception as e:
            self.clients.remove(client_socket)
            print(f"CLINET {addr} DISCONNECTED: {e}")
            pass

            # while True:
            #     print("SHOWING CLIENT")
                
            #     while True:
            #         while len(data) < len(b"VIDEO:"):
            #             print("RECEIVING DATA")
            #             packet = client_socket.recv(4 * 1024)
            #             if not packet:
            #                 break
            #             data += packet
                        
            #         if data.startswith(b"VIDEO:"):
            #             print("VIDEO RECEIVED")

            #             packed_msg_size = data[:payload_size]
            #             data = data[payload_size:]
            #             msg_size = struct.unpack("Q",packed_msg_size)[0]
                        
            #             while len(data) < msg_size:
            #                 data += client_socket.recv(4*1024)
            #             frame_data = data[:msg_size]
            #             data  = data[msg_size:]
            #             frame = pickle.loads(frame_data)
            #             text  =  f"CLIENT: {addr}"
            #             frame = ps.putBText(frame,text,10,10,vspace=10,hspace=1,font_scale=0.7,
            #                     background_RGB=(255,0,0),text_RGB=(255,250,250))	
            #             cv2.imshow(f"FROM {addr}",frame)
            #             key = cv2.waitKey(1) & 0xFF
            #             if key  == ord('q'):
            #                 break
            #         elif data.startswith(b"MESSAGE:"):
            #             print("MESSAGE RECEIVED")
            #             data = data[8:]
            #             print(data)
            #             break
            #         else:
            #             self.clients.remove(client_socket)
            #             client_socket.close()

        except Exception as e:
            self.clients.remove(client_socket)
            print(f"CLIENT {addr} DISCONNECTED: {e}")

    def receive(self):
        
        while True:
            client, address = self.server.accept()
            print(f"Connected with {str(address)}")

            if len(self.clients) < self.qnt_users:
                client.send('NICK'.encode('ascii'))
                nickname = client.recv(1024).decode('ascii')

                if nickname == 'admin':
                    client.send('PASS'.encode('ascii'))
                    password = client.recv(1024).decode('ascii')

                    if password != 'admin':
                        client.send('REFUSE'.encode('ascii'))
                        client.close()
                        continue

                self.nicknames.append(nickname)
                self.clients.append(client)

                self.broadcast(f"{nickname} joined the chat!".encode('ascii'))
                client.send('Connected to the server!'.encode('ascii'))

                try:
                    message = client.recv(1024)
                    mess_decode = message.decode('ascii')
                    print(mess_decode)
                    if "COMM_MODE video" in mess_decode:
                        video_thread = threading.Thread(target=self.show_client, args=(client, address,))
                        video_thread.start()
                        
                    else:
                        thread = threading.Thread(target=self.handle_client, args=(client,))
                        thread.start()
                
                except Exception as e:
                    pass

            else:
                print(f'{str(address)} was refused to connect: too many clients')
                client.send('Too many clients!'.encode('ascii'))
                sleep(3)
                client.close()
    
    def start(self):
        print(f'Server is listening on {self.host}:{self.port}')
        self.receive()
        
def main():
    server = Server(
        host = "0.0.0.0",
        qnt_users=10
    )
    
    server.start()
    
if __name__ == "__main__":
    main()