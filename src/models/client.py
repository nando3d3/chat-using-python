import socket,cv2, pickle,struct
import imutils
import threading
from src.models.server_manager import ServerManager
import os
from time import sleep
class Client(ServerManager):
    def __init__(self):
        self.client = None
        self.nickname = None
        self.password = None
        self.stop_thread = False
        
    def receive(self):
        while True:
            if self.stop_thread:
                break
            try:
                message = self.client.recv(1024).decode('ascii')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('ascii'))
                    next_message = self.client.recv(1024).decode('ascii')
                    if next_message == 'PASS':
                        self.client.send(self.password.encode('ascii'))
                        if self.client.recv(1024).decode('ascii') == 'REFUSE':
                            print("Connection is Refused !! Wrong Password")
                            return
                    elif next_message == 'BAN':
                        print('Connection Refused due to Ban')
                        self.client.close()
                        return
                else:
                    print(message)
            except socket.error:
                print('Error Occured while Connecting')
                self.client.close()
                break
    
    def write(self):
        while True:
            if self.stop_thread:
                break
            message = f'{self.nickname}: {input("")}'
            if message[len(self.nickname)+2:].startswith('/'):
                if self.nickname == 'admin':
                    if message[len(self.nickname)+2:].startswith('/kick'):
                        self.client.send(f'KICK {message[len(self.nickname)+2+6:]}'.encode('ascii'))
                    elif message[len(self.nickname)+2:].startswith('/ban'):
                        self.client.send(f'BAN {message[len(self.nickname)+2+5:]}'.encode('ascii'))
                else:
                    print("Commands can only be executed by the admin")
            else:
                self.client.send(message.encode('ascii'))
                print('Mensagem enviada: ', message)

    def video(self):
        vid = cv2.VideoCapture(0)
        while (vid.isOpened()):
            try:
                img, frame = vid.read()
                frame = imutils.resize(frame,width=380)
                a = pickle.dumps(frame)
                message = struct.pack("Q",len(a))+a
                self.client.sendall(message)
                #cv2.imshow(f"TO: {host_ip}",frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    self.client.close()
            except:
                print('VIDEO FINISHED!')
                break
    

    # def video(self):
    #     vid = cv2.VideoCapture(0)
    #     while vid.isOpened():
    #         try:
    #             _, frame = vid.read()
    #             frame = imutils.resize(frame, width=380)
    #             a = pickle.dumps(frame)
                
    #             # Adicionando um marcador para indicar que é um vídeo
    #             video_marker = b"VIDEO:"
    #             message = video_marker + struct.pack("Q", len(a)) + a
                
    #             self.client.sendall(message)
                
    #             key = cv2.waitKey(1) & 0xFF
    #             if key == ord("q"):
    #                 self.client.close()
    #         except:
    #             print('VIDEO FINISHED!')
    #             break
    


    def start(self):
        while True:
            os.system('cls||clear')
            option = input("(1)Enter server\n(2)Add server\n")
            if option == '1':
                self.enter_server()
                break
            elif option == '2':
                self.add_server()

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
        write_thread = threading.Thread(target=self.write)
        write_thread.start()

        if self.client:
            self.client.send(f"COMM_MODE {self.mode}".encode('ascii'))
            
        if self.mode == 'video':
            video_thread = threading.Thread(target=self.video)
            video_thread.start()    


def main():
    Client().start()
    
if __name__ == "__main__":
    main()