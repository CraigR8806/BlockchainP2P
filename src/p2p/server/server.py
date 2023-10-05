import jsonpickle
from flask import Flask, request
import threading



class Server:

    def __init__(self, parent_node):
        self.parent_node = parent_node
        
        self.app = Flask(__name__)
        self.add_post_endpoint("/node/join", "node_join", self.__node_join)
        self.add_get_endpoint("/api/shutdown", "shutdown", self.__shutdown_server)


    def update_chain(self, chain):
        pass
    

    def start_server(self):
        self.server_thread = threading.Thread(target=self.app.run, kwargs={'port':self.parent_node.connection.port})
        self.server_thread.start()

    def stop_server(self):
        self.parent_node.client.shutdown_server()
        self.server_thread.join()
    

    def add_post_endpoint(self, uri:str, name:str, func):
        self.app.add_url_rule(uri, name, func, methods=["POST"])

    def add_get_endpoint(self, uri:str, name:str, func):
        self.app.add_url_rule(uri, name, func, methods=["GET"])


    def __node_join(self):
        peer = jsonpickle.decode(request.get_data())['peer']
        if peer not in self.parent_node.get_active_peers():
            self.parent_node.add_peer(peer)
            self.parent_node.client.join_network([p.connection for p in self.parent_node.get_active_peers() if p != self.parent_node.as_peer()], peer)
        return jsonpickle.encode({'peers': self.parent_node.get_active_peers()})
    
    def __shutdown_server():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
