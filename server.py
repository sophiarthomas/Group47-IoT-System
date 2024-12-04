# Assignment 8 - IoT System
# Sophia Thomas 029081102
# Peter Khim 
# Due: 12/8/24 @ 11:55PM
import socket
import ipaddress
from databaseQuery import fridge_moisture, avg_water_consumption, electricity_consumption
import databaseQuery as query 
from binaryTree import load_data_to_tree, get_all_devices_as_dict, get_fridge_devices


def main():
    myTCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        try:
            server_ip = input("Enter the server IP address: ")
            ipaddress.ip_address(server_ip)
            break
        except ValueError:
            print("Invalid IP Address. Try Again.")

    while True:
        try:
            server_port = int(input("Enter the server port number: "))
            if 1 <= server_port <= 65535:
                break
            else:
                print("Port number must be between 1 and 65535. Try Again.")
        except ValueError:
            print("Port number must be an integer. Try Again.")

    myTCPSocket.bind((server_ip, server_port))
    print(f"Server up on {server_ip}:{server_port}.")

    myTCPSocket.listen(1)

    tree = load_data_to_tree()
    devices_dict = get_all_devices_as_dict(tree)

    while True:
        print("Waiting for connection.")
        incomingSocket, incomingAddress = myTCPSocket.accept()
        print(f"Connected to {incomingAddress}")

        while True:
            data = incomingSocket.recv(1024).decode('utf-8')
            if not data:
                break

            print(f"Received query: {data}")

            # Directly call the relevant functions
            if "average moisture" in data.lower():
                # response = fridge_moisture(tree)
                ##########################################
                fridge_devices = get_fridge_devices(devices_dict)
                if not fridge_devices:
                    response = "No fridge devices found in the system."
                else:
                    options = "\n".join([f"{i+1}. {fridge}" for i, fridge in enumerate(fridge_devices)])
                    incomingSocket.send(f"Which fridge do you want to check?\n{options}".encode('utf-8'))

                    # Receive the user's choice
                    choice = incomingSocket.recv(1024).decode('utf-8').strip()
                    try:
                        selected_index = int(choice) - 1
                        if 0 <= selected_index < len(fridge_devices):
                            selected_uid = list(devices_dict.keys())[selected_index]
                            response = fridge_moisture(tree, device_uid=selected_uid) ## Fridge Moisture needs reworking
                        else:
                            response = "Invalid selection."
                    except ValueError:
                        response = "Invalid input. Please enter a number."
                ##########################################
            elif "average water consumption" in data.lower():
                response = avg_water_consumption(tree)

            elif "consumed more electricity" in data.lower():
                response = electricity_consumption(tree)

            elif "shutdown" in data.lower():
                    response = "Shutting down server."
                    incomingSocket.send(response.encode('utf-8'))
                    incomingSocket.close()
                    myTCPSocket.close()
                    print("Server shut down.")
                    return
            else:
                response = "Invalid query. Please send one of the valid queries."

            incomingSocket.send(response.encode('utf-8'))
            print(f"Sent response: {response}")

        incomingSocket.close()
        print(f"Connection with {incomingAddress} terminated.")

if __name__ == "__main__":
	main()
