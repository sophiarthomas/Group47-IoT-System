class TreeNode:
    def __init__(self, name, asset_uid):
        self.name = name
        self.asset_uid = asset_uid
        self.left = None
        self.right = None

class BinarySearchTree: 
    def __init__(self):
        self.root = None

    def insert(self, name, asset_uid):
        """Insert a device into the tree"""
        new_node = TreeNode(name, asset_uid)
        if self.root is None: 
            self.root = new_node
        else: 
            self._insert_recursive(self.root, new_node)

    def _insert_recursive(self, current, new_node):
        if new_node.name < current.name: 
            if current.left is None: 
                current.left = new_node
            else: 
                self._insert_recursive(current.left, new_node)
        else: 
            if current.right is None: 
                current.right = new_node
            else: 
                self._insert_recursive(current.right, new_node)

    def search(self, name):
        """Search for a device by name"""
        return self._search_recursive(self.root, name)

    def _search_recursive(self, current, name):
        if current is None: 
            return None
        if current.name == name: 
            return current
        elif name < current.name: 
            return self._search_recursive(current.left, name) 
        else: 
            return self._search_recursive(current.right, name)

    def inorder_traversal(self):
        """Return an in-order traversal of the tree"""
        devices = []
        self._inorder_recursive(self.root, devices)
        return devices

    def _inorder_recursive(self, current, devices):
        if current is not None: 
            self._inorder_recursive(current.left, devices)
            devices.append((current.name, current.asset_uid))
            self._inorder_recursive(current.right, devices)

def build_device_tree(metadata):
    """Build a binary search tree from metadata"""
    tree = BinarySearchTree()
    query = {"customAttributes.type": "DEVICE"}
    devices = metadata.find(query)

    for device in devices: 
        name = device["customAttributes"]["name"]
        asset_uid = device["assetUid"]
        tree.insert(name, asset_uid)
    
    return tree 