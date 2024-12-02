from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os
import mongoDBkey as key
from datetime import datetime, timedelta

# Query all devices' names from metadata 
def get_device_names(metadata):
    query = {"customAttributes.type": "DEVICE"}
    devices = metadata.find(query)

    # Storing device names in a list 
    device_names = []
    for device in devices: 
        device_names.append(device["customAttributes"]["name"])
    
    return device_names

# Query 1: What is the average moisture inside my kitchen fridge in the past three hours?
def fridge_moisture(virtual, fridge_name): 
    # Get the date for 3 hours ago
    three_hours_ago = datetime.now() - timedelta(hours=3)
    three_hours_ago_unit = int(three_hours_ago.timestamp())    
    pass 


# Query 2: What is the average water consumption per cycle in my smart dishwasher?
def avg_water_consumption(): 
    pass 


# Query 3: Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?
def electricity_consumption(devices):
    pipeline = [
        {
            "$lookup": {
                "from": "IoTSmartDevices_metadata",
                "localField": "payload.parent_asset_uid",
                "foreignField": "assetUid",
                "as": "device_info"
            }
        },
        {
            "$unwind": "$device_info"
        },
        {
            "$project": {
                "device": "$device_info.customAttributes.name",
                "electricity": {
                    "$add": [
                        { "$convert": { "input": "$payload.Ammeter", "to": "double", "onError": 0, "onNull": 0 } },
                        { "$convert": { "input": "$payload.Ammeter2", "to": "double", "onError": 0, "onNull": 0 } },
                        { "$convert": { "input": "$payload.Ammeter3", "to": "double", "onError": 0, "onNull": 0 } }
                    ]
                },
                "parent_asset_uid": "$payload.parent_asset_uid"
            }
        },
        {
            "$group": {
                "_id": "$parent_asset_uid",
                "device": { "$first": "$device" },
                "total_electricity": { "$sum": "$electricity" }
            }
        },
        {
            "$sort": { "total_electricity": -1 }
        },
        {
            "$limit": 1
        }
    ]

    result = list(devices.aggregate(pipeline))
    print(result)

    if result:
        print(f"Device with highest electricity consumption: {result[0]['device']} with {result[0]['total_electricity']:.2f} amps")
    else:
        print("No electricity data available.")


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

    # Device names
    device_names = get_device_names(metadata)

    if msg == "What is the average moisture inside my kitchen fride in the past three hours?": 
        fridge_moisture(virtual, "Smart_Fridge1")
    elif msg == "What is the average water consumption per cycle in my smart dishwasher?":
        avg_water_consumption(virtual)
    elif msg == "What device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?":
        electricity_consumption(virtual)


if __name__=="__main__":
    main()