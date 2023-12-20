import os
import json
import socket

class ServerManager():
    
    def enter_server(self):
            self.mode = None
            os.system('cls||clear')
            with open('src/resources/servers.json') as f:
                data = json.load(f)
            print('Servers: ', end="")
            for servers in data:
                print(servers, end=" ")
            print('\nServer Name:',end=" ")
            server_name = input()
            print('Nickname:', end=" ")
            self.nickname = input()
            if self.nickname == 'admin':
                print("Enter Password for Admin:", end=" ")
                self.password = input()
            self.comm_mode()
            ip = data[server_name]["ip"]
            port = data[server_name]["port"]
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((ip, port))

    def comm_mode(self):
        while True:
            os.system('cls||clear')
            option = input("Ativar câmera?:\n(1)Sim\n(2)Não\n")
            option = int(option)
            if option == 2:
                self.mode = 'chat'
                break
            elif option == 1:
                self.mode = 'video'
                break
    
    def add_server(self):
            os.system('cls||clear')
            server_name = input("Enter a name for the server:")
            server_ip = input("Enter the ip address of the server:")
            server_port = int(input("Enter the port number of the server:"))

            with open('src/resources/servers.json', 'r') as f:
                data = json.load(f)
            with open('src/resources/servers.json', 'w') as f:
                data[server_name] = {"ip": server_ip, "port": server_port}
                json.dump(data, f, indent=4)