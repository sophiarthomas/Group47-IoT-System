# Assignment 8 - IoT System
# Sophia Thomas 029081102
# Peter Khim 
# Due: 12/8/24 @ 11:55PM

import socket
import ipaddress
from pymongo import MongoClient

client = MongoClient('mongodb+srv://peterkhim:eucalyptus@smartdevices.a2nsj.mongodb.net/')
db = client['test']
data_collection = db['IoTSmartDevices_virtual']
metadata_collection = db['IoTSmartDevices_metadata']

def get_device_info(device_id):		# This way we can tell what device connects with what sensors.
	device = metadata_collection.find_one({" ": device_id}) # " " is parentID or uID, need to figure out which one we want.
	if device:
		return device
	return None

def calculate_average_moisture(device_id):  # Query 1
	pass

def calculate_average_water_consumption(device_id): # Query 2
	pass

def compare_device_power(): # Query 3
	pass

def handle_query(query):
	if "average moisture" in query.lower():
		return calculate_average_moisture("kitchen_fridge")
	elif "average water consumption" in query.lower():
		return calculate_average_water_consumption("dishwasher")
	elif "device consumed more electricty" in query.lower():
		return compare_device_power()
	else:
		return "Sorry, this query cannot be processed. Please try one of the following: [LIST OF VALID QUERIES, THIS MUST BE CHANGED BUT LAZY RN!!!!!!]"

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

	while True:
		print("Waiting for connection.")
		incomingSocket, incomingAddress = myTCPSocket.accept()
		print(f"Connected to {incomingAddress}")

		while True:
			data = incomingSocket.recv(1024).decode('utf-8')
			if not data:
				break

		print(f"Recieved query: {data}")

		response = handle_query(data)

		incomingSocket.send(response.encode('utf-8'))
		print(f"Sent respose: {response}")

	incomingSocket.close()
	print(f"Connection with {incomingAddress} terminated.")

if __name__ == "__main__":
	main()
