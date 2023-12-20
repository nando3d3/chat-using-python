# Python Chat 🐍 : A Python-Based Chat Room


This is an advanced Python-based Secure Chat room. The project is entirely based on the Socket Progamming; done using Python. A server is set to the listening mode, with a specific IP Address and Port number (that can be edited in the script) and clients are made to connect to the server, after which they are promopted to enter a nickname. The messages are then broadcasted to all the clients present. 

### 👉 Introduction

#### 👉 Sockets
<b> Sockets </b> and the socket API are used to send messages across a network. They provide a form of inter-process communication (IPC). The network can be a logical, local network to the computer, or one that’s physically connected to an external network, with its own connections to other networks. The obvious example is the Internet, which you connect to via your ISP. <br><br>
<img align="center" height=300px src=https://github.com/IamLucif3r/Chat-On/blob/main/assets/Python-Sockets-Tutorial_Watermarked.webp> <br>
Image Credit:[Real Python](https://realpython.com/python-sockets/)

#### 👉 TCP Socket
In the diagram below, given the sequence of socket API calls and data flow for TCP:
<br><br>
<img align="center" src=https://github.com/IamLucif3r/Chat-On/blob/main/assets/Screenshot%20at%202021-05-21%2010-47-40.png height=500px>

## 👉 Environment Setup

1. Setup python 3.10.x on your system.

2. Create a virtual environment using the following command:
``` shell
python3 -m venv venv
```
3. Activate the virtual environment using the following command:
``` shell
source venv/bin/activate
```
4. Install the requirements using the following command:
``` shell
pip3 install -r requirements.txt
```

## 👉 Usage

1. We will have to start our Server first.
``` shell
python3 main_server.py
```
<b>Note: </b> Before running the server, make sure to edit the IP address and Port number. By default it is running on Localhost:5555 <br><br>
2. Run the Client file, to start the conversation. 
``` Shell
python3 main_client.py
```
<br>
3. Now Enter a nickname and start your chatting. 


