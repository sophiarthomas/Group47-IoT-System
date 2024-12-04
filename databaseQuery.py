from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os
import mongoDBkey as key
from datetime import datetime, timedelta
from binaryTree import load_data_to_tree, get_all_devices_as_dict

# Query 1: What is the average moisture inside my kitchen fridge in the past three hours?
def fridge_moisture(tree):
    # Get the timestamp for 3 hours ago
    time = datetime.now()
    most_recent_timestamp = int(time.timestamp())
    #most_recent_timestamp = 1733203151
    three_hours_ago_timestamp = int(most_recent_timestamp - (3 * 3600))

    virtual_devices = tree.in_order_traversal()
    total_moisture = 0
    count = 0

    for virtual_device in virtual_devices:
        for device in virtual_device.get('virtual_devices', []):
            if 'payload' in device:
                payload = device['payload']
                timestamp = int(payload['timestamp'])

                if three_hours_ago_timestamp <= timestamp <= most_recent_timestamp:
                    if 'Moisture Meter - Water' in payload:
                        moisture_value = float(payload['Moisture Meter - Water'])
                        total_moisture += moisture_value
                        count += 1
            #         else:
            #             print(f"No Moisture Meter data found in payload: {payload}")
            #     else:
            #         print(f"Dataset timestamp {timestamp} is outside the range.")
            # else:
            #     print('No payload found in this device')

    # Calculate the average moisture.
    if count > 0:
        average_moisture = total_moisture / count
        print(f"Average Moisture Meter value in last 3 hours: {average_moisture}%")
    else:
        print("No valid Moisture Meter data within the specified time range.")


# Query 2: What is the average water consumption per cycle in my smart dishwasher?
def avg_water_consumption(virtual):
    pass


# Query 3: Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?
def electricity_consumption(tree):

    devices_of_interest = get_all_devices_as_dict(tree)
    # {
    #     "hvx-7ku-6h2-618": "Smart Fridge 1",
    #     "a0a655ff-d2a6-404e-81af-a992405c9859": "Smart Fridge 2",
    #     "48o-2q4-78n-rvv": "Washer"
    # }

    consumption_data = {device_name: 0 for device_name in devices_of_interest.values()}

    virtual_devices = tree.in_order_traversal()

    for node_data in virtual_devices:
        virtual_devices = node_data.get('virtual_devices', [])

        for device in virtual_devices:
            parent_asset_uid = device['payload'].get('parent_asset_uid', '')
            if parent_asset_uid in devices_of_interest:
                ammeter_key = 'Ammeter' if 'Ammeter' in device['payload'] else 'Ammeter2'
                if ammeter_key in device['payload']:
                    consumption = float(device['payload'][ammeter_key])
                    device_name = devices_of_interest[parent_asset_uid]
                    consumption_data[device_name] += consumption

    if consumption_data:
        max_device = max(consumption_data, key=consumption_data.get)
        max_consumption = consumption_data[max_device]
        print(f"Device with highest electricity consumption: {max_device} with {max_consumption} kWh")
    else:
        print("No relevant devices found.")


def main(msg):
    # # Load environment variables from .env file
    # load_dotenv()

    # uri = os.getenv("MONGODB_URI")
    # if not uri:
    #     raise EnvironmentError("MONGODB_URI is not set in the environment or .env file.")

    # # Create a new client and connect to the server
    # client = MongoClient(uri, tlsAllowInvalidCertificates=True) # REMOVE WHEN DONE

    # # Database
    # db = client[key.database]

    # # Collections
    # devices = db[key.devices]
    # metadata = db[key.metadata]
    # virtual = db[key.virtual]

    # Load data into tree
    tree = load_data_to_tree()

    if msg == "What is the average moisture inside my kitchen fridge in the past three hours?":
        fridge_moisture(tree)
    elif msg == "What is the average water consumption per cycle in my smart dishwasher?":
        avg_water_consumption(tree)
    elif msg == "What device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?":
        electricity_consumption(tree)


if __name__ == "__main__":
    main("What device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?")
