from flask import Flask, request, Response
from p2p.peer.peer import Peer
import threading
import shared.util as util



class Server:

    def __init__(self, parent_node):
        self.parent_node = parent_node
        
        self.app = Flask(__name__)
        self.add_post_endpoint("/node/join", "node_join", self.__node_join)
        self.add_get_endpoint("/api/shutdown", "shutdown", self.__shutdown_server)


    def update_chain(self, chain):
        pass
    

    def start_server(self):
        self.server_thread = threading.Thread(target=self.app.run, 
                                              kwargs=
                                              {
                                                  'host':self.parent_node.connection.host,
                                                  'port':self.parent_node.connection.port,
                                                  'ssl_context':self.parent_node.pki.get_ssl_context()
                                              })
        self.server_thread.start()

    def stop_server(self):
        self.server_thread.join()
    

    def add_post_endpoint(self, uri:str, name:str, func):
        self.app.add_url_rule(uri, name, func, methods=["POST"])

    def add_get_endpoint(self, uri:str, name:str, func):
        self.app.add_url_rule(uri, name, func, methods=["GET"])


    def __node_join(self):
        peer = util.extract_data(request.get_data(as_text=True))
        if peer not in self.parent_node.get_active_peers():
            self.parent_node.add_peer(peer)
            self.parent_node.client.join_network([p.connection for p in self.parent_node.get_active_peers() if p != self.parent_node.as_peer()], peer)
        return self.build_response(200, self.parent_node.get_active_peers())
    
    def __shutdown_server():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()


    def build_response(self, response_code:int, response_obj:dict) -> Response:
        return Response(
            response=util.jsonify_data(response_obj),
            status=response_code,
            mimetype="application/json"
        )
    
    


