# Assignment 5 - Interprocess Communication
# Sophia Thomas 029081102
# Due: 10/20/24 @ 11:55PM

import socket
import ipaddress

# Client initiates a connection
while True:
    try: 
        serverIP = input("Enter the server ip address: ")
        ipaddress.ip_address(serverIP)
        False
        break
    except ValueError: 
         print("Error: Invalid IP address. Try again.")

while True: 
    serverPort = int(input("Enter port: "))
    try:
        if 1 <= serverPort <= 65535:  # Check if port is in valid range
            break  # Exit the loop if port is valid
        else:
            print("Error: Port number must be between 1 and 65535. Try again.")
    except ValueError:
        print("Error: Port number must be an integer. Try again.")


maxBytesToRecieve = 1024

# with statement closes the socket when client terminates connection 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcpSock: 
    tcpSock.connect((serverIP, serverPort))
    
# Data is exchanged
    messaging = True

    while messaging: 
        msg = input("Enter a message to send the server: ")
        tcpSock.sendto(bytearray(str(msg), encoding="utf-8"), (serverIP, serverPort))
        serverResponse = tcpSock.recv(maxBytesToRecieve)
        print(f"Received: {serverResponse.decode('utf-8')}")
        


            



