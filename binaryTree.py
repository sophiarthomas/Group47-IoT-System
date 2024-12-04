from pymongo import MongoClient
import os
from dotenv import load_dotenv
import mongoDBkey as mongo

class TreeNode:
    def __init__(self, key, data=None):
        self.key = key
        self.data = data
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, key, data=None):
        if not self.root:
            self.root = TreeNode(key, data)
        else:
            self._insert(self.root, key, data)

    def _insert(self, current_node, key, data):
        if key < current_node.key:
            if current_node.left is None:
                current_node.left = TreeNode(key, data)
            else:
                self._insert(current_node.left, key, data)
        elif key > current_node.key:
            if current_node.right is None:
                current_node.right = TreeNode(key, data)
            else:
                self._insert(current_node.right, key, data)
        else:
            current_node.data = data

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, current_node, key):
        if current_node is None:
            return None
        elif key == current_node.key:
            return current_node.data
        elif key < current_node.key:
            return self._search(current_node.left, key)
        else:
            return self._search(current_node.right, key)

    def in_order_traversal(self):
        nodes = []
        self._in_order_traversal(self.root, nodes)
        return nodes

    def _in_order_traversal(self, current_node, nodes):
        if current_node:
            self._in_order_traversal(current_node.left, nodes)
            nodes.append(current_node.data)
            self._in_order_traversal(current_node.right, nodes)


def load_data_to_tree():
    """
    Load Data from MongoDB and Build Tree
    Args: None
    Returns: BinaryTree
    """
    # Load environment variables from .env file
    load_dotenv()

    uri = os.getenv("MONGODB_URI")
    if not uri:
        raise EnvironmentError("MONGODB_URI is not set in the environment or .env file.")

    # Create a new client and connect to the server
    client = MongoClient(uri, tlsAllowInvalidCertificates=True) # REMOVE WHEN DONE

    # Database
    db = client[mongo.database]
    virtual_collection = db[mongo.virtual]
    metadata_collection = db[mongo.metadata]

    virtual_documents = virtual_collection.find()
    metadata_documents = metadata_collection.find()

    metadata_dict = {str(doc['assetUid']): doc for doc in metadata_documents}

    tree = BinaryTree()

    devices_by_metadata = {}

    for doc in virtual_documents:
        key = doc["_id"]
        parent_asset_uid = doc['payload'].get('parent_asset_uid')

        if parent_asset_uid:
            if parent_asset_uid not in devices_by_metadata:
                devices_by_metadata[parent_asset_uid] = []
            devices_by_metadata[parent_asset_uid].append(doc)

    for parent_asset_uid, virtual_devices in devices_by_metadata.items():
        metadata = metadata_dict.get(str(parent_asset_uid))
        combined_data = {
            'virtual_devices': virtual_devices,
            'metadata': metadata
        }

        tree.insert(str(parent_asset_uid), combined_data)

    return tree

def get_all_devices_as_dict(tree):
    """
    Retrieves all devices from the binary search tree as a dictionary.
    Args:
        tree (BinaryTree): The binary tree containing devices.
    Returns:
        dict: A dictionary where keys are assetUid values and values are device names.
    """
    nodes = tree.in_order_traversal()
    devices_dict = {}

    for node_data in nodes:
        if node_data:  # Ensure the node has data
            metadata = node_data.get('metadata', {})
            asset_uid = metadata.get('assetUid')
            device_name = metadata.get('customAttributes', {}).get('name', 'Unknown Device')
            
            # Skip devices without a valid name or assetUid
            if asset_uid and device_name != 'Unknown Device':
                devices_dict[asset_uid] = device_name

    return devices_dict

# if __name__ == "__main__":
#     tree = load_data_to_tree()

#     parent_asset_uid_to_search = "48o-2q4-78n-rvv"
#     result = tree.search(parent_asset_uid_to_search)

#     if result:
#         print(f"Found {parent_asset_uid_to_search}:")
#         print(result)
#     else:
#         print(f"No {parent_asset_uid_to_search}!!!!!!!!!!!!.")

