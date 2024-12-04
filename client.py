# Assignment 8 - IoT System
# Sophia Thomas 029081102
# Peter Khim 
# Due: 12/8/24 @ 11:55PM

import socket
import ipaddress

# Valid quieries
valid_queries = [
    "What is the average moisture inside my kitchen fride in the past three hours?", 
    "What is the average water consumption per cycle in my smart dishwasher?",
    "What device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?",
    "Shutdown"
    ]

def display_valid_queires(): 
    print("Please try one of the following queries: ")
    for i, query in enumerate(valid_queries): 
        print(f"{i+1}. {query}")

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
    print("Connection to server established.")

    
# Data is exchanged
    messaging = True
    user_input = 0
    
    while messaging: 
        print("\nEnter your query (1, 2, 3, 4): ")
        display_valid_queires()
        user_input = int(input(">> "))

        if user_input in range(1, len(valid_queries)+1): 
            query = valid_queries[user_input-1]
            tcpSock.send(query.encode('utf-8'))
            
            while True: 
                serverResponse = tcpSock.recv(maxBytesToRecieve).decode('utf-8')
                print(f"Server: {serverResponse}") 

                if "check" in serverResponse.lower(): 
                    user_follow_up = input("followup >> ")
                    tcpSock.send(user_follow_up.encode('utf-8'))
                else: 
                    break

            if "shutdown" in query.lower():
                print("Shutting down connection.")
                break
        else: 
            print("Invalid query. Try again.")
        #     tcpSock.sendto(bytearray(str(valid_queries[user_input-1]), encoding="utf-8"), (serverIP, serverPort))
        #     serverResponse = tcpSock.recv(maxBytesToRecieve)
        #     print(f"Received: {serverResponse.decode('utf-8')}")
        # else: 
        #     print("Sorry, this query cannot be processed. Try again.")
        
        


            



