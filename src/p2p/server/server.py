from flask import Flask, request, Response
from p2p.peer.peer import Peer
from p2p.client.client import Client
from shared.pki.pki import PKI
from p2p.dataservice import DataService
import threading
import shared.util as util



class Server:

    def __init__(self, parent_peer:Peer, client:Client, data_service:DataService, pki:PKI):
        self.parent_peer = parent_peer
        self.data_service = data_service
        self.client = client
        self.pki = pki
        
        self.app = Flask(__name__)
        self.add_post_endpoint("/node/join", "node_join", self.__node_join)
        self.add_get_endpoint("/api/shutdown", "shutdown", self.__shutdown_server)


    def update_chain(self, chain):
        pass
    

    def start_server(self):
        self.server_thread = threading.Thread(target=self.app.run, 
                                              kwargs=
                                              {
                                                  'host':self.parent_peer.connection.host,
                                                  'port':self.parent_peer.connection.port,
                                                  'ssl_context':self.pki.get_ssl_context()
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
        current_active_peers = self.data_service.deep_copy("active_peers")
        if peer not in current_active_peers:
            self.data_service.modify("active_peers", lambda v:v.add(peer))
            current_active_peers = self.data_service.deep_copy("active_peers")
            self.client.join_network([p.connection for p in current_active_peers if p != self.parent_peer], peer)
        return self.build_response(200, current_active_peers)
    
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
    
    


