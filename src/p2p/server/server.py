from flask import Flask, request, Response
from p2p.peer.peer import Peer
from p2p.client.client import Client
from shared.pki.pki import PKI
from p2p.dataservice import DataService
import threading
import shared.util as util
import time
import math
import typing as t



class Server:

    def __init__(self, parent_peer:Peer, client:Client, data_service:DataService, pki:PKI):
        self.parent_peer = parent_peer
        self.data_service = data_service
        self.client = client
        self.pki = pki
        
        self.app = Flask(__name__)
        self.add_post_endpoint("/node/join", "node_join", self.__node_join)
        self.add_get_endpoint("/api/shutdown", "shutdown", self.__shutdown_server)

        self.running = None
    

    def start_server(self) -> None:
        self.start_time = time.time()
        self.server_thread = threading.Thread(target=self.app.run, 
                                              kwargs=
                                              {
                                                  'host':self.parent_peer.connection.host,
                                                  'port':self.parent_peer.connection.port,
                                                  'ssl_context':self.pki.get_ssl_context()
                                              })
        self.server_thread.start()

    def stop_server(self) -> None:
        self.server_thread.join()
    

    def add_post_endpoint(self, uri:str, name:str, func:t.Callable) -> None:
        self.app.add_url_rule(uri, name, func, methods=["POST"])

    def add_get_endpoint(self, uri:str, name:str, func:t.Callable) -> None:
        self.app.add_url_rule(uri, name, func, methods=["GET"])


    def __node_join(self) -> Response:
        peer = util.extract_data(request.get_data(as_text=True))
        current_active_peers = self.data_service.deep_copy("active_peers")
        self.app.logger.warning("here's the peer " + peer.name)
        
        if peer not in current_active_peers:
            self.data_service.modify("active_peers", lambda v:v.add(peer))
            current_active_peers = self.data_service.deep_copy("active_peers")
            responses = self.client.join_network([p for p in current_active_peers if p != self.parent_peer], peer, logger=self.app.logger)
            self.app.logger.warning("before adding them " + str(current_active_peers))
            for p in responses:
                self.data_service.modify("active_peers", lambda v:v.update(util.extract_data(responses[p].text)))
            current_active_peers = self.data_service.deep_copy("active_peers")
            self.app.logger.warning("after adding them " + str(current_active_peers))

        return self.build_response(200, current_active_peers)
    
    def __shutdown_server() -> None:
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()


    def build_response(self, response_code:int, response_obj:t.Dict[t.Any, t.Any]) -> Response:
        return Response(
            response=util.jsonify_data(response_obj),
            status=response_code,
            mimetype="application/json"
        )
    

    def uptime(self) -> t.Dict[str, int]:
        delta=time.time() - self.start_time
        return { "year": math.floor(delta/31536000),
                    "month": math.floor(delta/2629746)%12,
                    "day": math.floor(delta/86400)%30,
                    "hour": math.floor(delta/3600)%24,
                    "minute": math.floor(delta/60)%60,
                    "second": math.floor(delta%60) }
       
    


