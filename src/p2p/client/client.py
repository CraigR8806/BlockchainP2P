import requests
import shared.util as util

class Client:

    def __init__(self, parent_node):
        self.parent_node = parent_node

    def join_network(self, bootstrap_connections, peer=None):
        if peer is None:
            peer = self.parent_node.as_peer()
        for connection in bootstrap_connections:
            response = requests.post("https://" + connection.host + ":" + str(connection.port) + "/node/join",
                                     util.jsonify_data(peer), verify='/apps/node/pki/ca.pem', cert=('/apps/node/pki/node.pem', '/apps/node/pki/node.key'))
            
    def shutdown_server(self):
        requests.get("http://localhost:" + self.parent_node.connection.port + "/api/shutdown")
    
    def request_transaction(self, transaction):
        pass

