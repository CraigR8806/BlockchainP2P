import requests
import jsonpickle

class Client:

    def __init__(self, parent_node):
        self.parent_node = parent_node

    def join_network(self, bootstrap_connections, peer=None):
        if peer is None:
            peer = self.parent_node.as_peer()
        for connection in bootstrap_connections:
            response = requests.post("http://" + connection.ip_address + ":" + connection.port + "/node/join",
                                     jsonpickle.encode({'peer': peer}))
    
    def request_transaction(self, transaction):
        pass

