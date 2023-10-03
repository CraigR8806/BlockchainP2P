import jsonpickle
from flask import Flask, request
import threading
from multiprocessing import Process


class Server:

    def __init__(self, parent_node):
        self.parent_node = parent_node
        self.server_thread = Process(target=self.run)


    def update_chain(self, chain):
        pass


    

    def start_server(self):
        self.server_thread.start()

    def stop_server(self):
        self.server_thread.terminate()
        self.server_thread.join()
        

    def run(self):
        app = Flask(__name__)

        @app.route('/node/join', methods=['POST'])
        def node_join():
            
            peer = jsonpickle.decode(request.get_data())['peer']
            if peer not in self.parent_node.get_active_peers():
                self.parent_node.add_peer(peer)
                self.parent_node.client.join_network([p.connection for p in self.parent_node.get_active_peers() if p != self.parent_node.as_peer()], peer)
            return jsonpickle.encode({'peers': self.parent_node.get_active_peers()}) 

         

        app.run(port=self.parent_node.connection.port)
