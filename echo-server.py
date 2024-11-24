# Assignment 8 - IoT System
# Sophia Thomas 029081102
# Peter Kim 
# Due: 12/8/24 @ 11:55PM

import socket
import ipaddress
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://sophiathomas02:malibulost@smartdevices.a2nsj.mongodb.net/?retryWrites=true&w=majority&appName=SmartDevices"

# Create a new client and connect to the server
client = MongoClient(uri)

# Server sets up a listening socket
serverIP = input("Enter the server ip address: ")

serverPort = int(input("Enter port: "))

## creates listening socket (IPv4, tcp socket stream)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcpSock: 
    tcpSock.bind((serverIP, serverPort)) # binds the created socket to the host and port you want to listen to 
    print(f"binding: {serverIP}:{serverPort}")
    tcpSock.listen() # listen to a request for the server from this socket
    print("Server is listening for connections...")

    while True:
        incomingSocket, clientAddr = tcpSock.accept() 
        with incomingSocket: 
            print(f"Connected by {clientAddr}")
            while True: 
                data = incomingSocket.recv(1024) # Recieve data from client 
                if not data: 
                    print("Connection Lost")
                    print("Server is listening for new connections...")
                    break
                print(f"Recieved: {data.decode('utf-8')}")
                incomingSocket.sendall(data.upper()) # Send response to the client 
                print(f"Sent: {data.upper().decode('utf-8')}")
	
        