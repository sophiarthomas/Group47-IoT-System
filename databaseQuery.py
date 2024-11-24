from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os
import mongoDBkey as key
from datetime import datetime, timedelta

# Query 1: What is the average moisture inside my kitchen fridge in the past three hours?
def fridge_moisture(): 
    # Get the date for 3 hours ago
    three_hours_ago = datetime.now() - timedelta(hours=3)
    pass 


# Query 2: What is the average water consumption per cycle in my smart dishwasher?
def avg_water_consumption(): 
    pass 


# Query 3: Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?
def electricity_consumption(): 
    pass 


def main(msg): 
    # Load environment variables from .env file
    load_dotenv()

    uri = os.getenv("MONGODB_URI")
    if not uri:
        raise EnvironmentError("MONGODB_URI is not set in the environment or .env file.")

    # Create a new client and connect to the server
    client = MongoClient(uri)

    # Database 
    db = client[key.database]

    # Collections 
    devices = db[key.devices]
    metadata = db[key.metadata]
    virtual = db[key.virtual]

    # Example 1: Query for the metadata of the Smart Fridge 
    query = {"customAttributes.name": "Smart Fridge"}
    document = metadata.find_one(query)
    print(document)

    if msg == "What is the average moisture inside my kitchen fride in the past three hours?": 
        fridge_moisture()
    elif msg == "What is the average water consumption per cycle in my smart dishwasher?":
        avg_water_consumption()
    elif msg == "What device consumed more electriciy among my three IoT devices (two refrigerators and a dishwasher)?":
        electricity_consumption()


if __name__=="__main__":
    main()