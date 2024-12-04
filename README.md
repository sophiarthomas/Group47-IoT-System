# Group47 IoT System

Welcome to the Group47 IoT System repository! This project is an implementation of an Internet of Things (IoT) system designed to manage and analyze data from smart devices such as refrigerators, dishwashers, and other home appliances.

## Features

- **Binary Tree Data Management**: Efficient storage and search of IoT device metadata using a binary tree.
- **MongoDB Integration**: Querying device data and metadata from a MongoDB database.
- **Data Analysis**:
  - Average moisture calculation for refrigerators.
  - Average water consumption for dishwashers.
  - Electricity consumption comparison among devices.
- **Python Implementation**: Leveraging Python for robust backend logic.

## Technologies Used

- **Python**: Core programming language.
- **MongoDB**: NoSQL database for storing IoT device data.
- **Binary Search Tree**: Efficient in-memory data management.
- **Pymongo**: MongoDB Python driver for querying the database.


## Getting Started

### Prerequisites

- Python 3.9 or later
- MongoDB Atlas or a local MongoDB instance
- `pip` for installing dependencies
- Ensure `.env` file is configured with required keys
    ```bash
    MONGODB_URI=<your_mongodb_uri>
### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sophiarthomas/Group47-IoT-System.git
   cd Group47-IoT-System


## Running the System

### Database
- Start MongoDB database
    - MongoDB Atlas: Configure Atlas cluster and add your database URI to the .env file

### Server
    python server.py
    Enter the server ip address: <IP ADDRESS>
    Enter port: <PORT>

### Client
    python client.py
    Enter the server ip address: <IP ADDRESS>
    Enter port: <PORT>

