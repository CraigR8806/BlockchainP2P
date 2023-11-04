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

    """
    Class representing the Server side of the P2P Node\n
    Spawns a thread using `start_server` method to run the server on\n
    To propertly collapse the execution stack, run `stop_server` method\n

    ---

    This class allows clients to this class to define more endpoints on the server\n
    allowing this class still be generic to P2P structure, but be 'extensable'\n
    allowing for more specific usages.

    ---

    ---
    FIELDS
    ---

    This class has no accessible fields
    """

    def __init__(self, parent_peer:Peer, client:Client, data_service:DataService, pki:PKI):
        """
        Constructor for Server

        Args:
            parent_peer (Peer): The `Peer` representation of the `ThisPeer` that runs this `Server`
            client (Client): The `Client` provided by the parent `ThisPeer`
            data_service (DataService): The `DataService` provided by the parent `ThisPeer`
            pki (PKI): The `PKI` object
        """
        self.__parent_peer = parent_peer
        self.__data_service = data_service
        self.__client = client
        self.__pki = pki
        
        self.__app = Flask(__name__)
        self.add_post_endpoint("/node/join", "node_join", self.__node_join)
        self.add_get_endpoint("/api/shutdown", "shutdown", self.__shutdown_server)

        self.__running = False
    

    def start_server(self) -> None:
        """
        Starts the server `Thread`
        """
        self.__start_time = time.time()
        self.__server_thread = threading.Thread(target=self.__app.run, 
                                              kwargs=
                                              {
                                                  'host':self.__parent_peer.get_connection().get_host(),
                                                  'port':self.__parent_peer.get_connection().get_port(),
                                                  'ssl_context':self.__pki.get_ssl_context()
                                              })
        self.__server_thread.start()
        self.__running = True

    def stop_server(self) -> None:
        """
        Stops the server `Thread`
        """
        self.__server_thread.join()
        self.__running = False
    

    def add_post_endpoint(self, uri:str, name:str, func:t.Callable) -> None:
        """
        Adds a `POST` endpoint to the server

        Args:
            uri (str): The endpoint URI
            name (str): The endpoint name
            func (t.Callable): What to do when the endpoint is requested
        """
        self.__app.add_url_rule(uri, name, func, methods=["POST"])

    def add_get_endpoint(self, uri:str, name:str, func:t.Callable) -> None:
        """
        Adds a `GET` endpoint to the server

        Args:
            uri (str): The endpoint URI
            name (str): The endpoint name
            func (t.Callable): What to do when the endpoint is requested
        """
        self.__app.add_url_rule(uri, name, func, methods=["GET"])


    def __node_join(self) -> Response:
        """
        Definition for /node/join `POST` endpoint\n
        Consumes the POST parameters which should consist of a `Peer` object\n
        Adds that `Peer` object to the active `Peer`s `set` and notifies all active `Peer`s\n

        Returns:
            Response: All active `Peer`s
        """
        peer = util.extract_data(request.get_data(as_text=True))
        current_active_peers = self.__data_service.deep_copy("active_peers")
        
        if peer not in current_active_peers:
            self.__data_service.modify("active_peers", lambda v:v.add(peer))
            current_active_peers = self.__data_service.deep_copy("active_peers")
            responses = self.__client.join_network([p for p in current_active_peers if p != self.__parent_peer], peer, logger=self.__app.logger)
            for p in responses:
                self.__data_service.modify("active_peers", lambda v:v.update(util.extract_data(responses[p].text)))
            current_active_peers = self.__data_service.deep_copy("active_peers")

        return self.build_response(200, current_active_peers)
    
    def __shutdown_server() -> None:
        """
        Definition for /api/shutdown `GET` endpoint

        Raises:
            RuntimeError: If not running werkzeug server implementation under the `Flask` hood
        """
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()


    def build_response(self, response_code:int, response_obj:t.Dict[t.Any, t.Any]) -> Response:
        """
        A nice simple way to put together a `Flask` `Response` object

        Args:
            response_code (int): The response code to send back to client
            response_obj (t.Dict[t.Any, t.Any]): The body of the response

        Returns:
            Response: A `Flask` `Response` object
        """
        return Response(
            response=util.jsonify_data(response_obj),
            status=response_code,
            mimetype="application/json"
        )
    

    def uptime(self) -> t.Dict[str, int]:
        """
        Diagnostics to see how long the server has been live for\n
        `!!!THIS WILL BE REMOVED!!!`

        Returns:
            t.Dict[str, int]: A human readable representation of the amount of time the server has been up
        """
        delta=time.time() - self.__start_time
        return { "year": math.floor(delta/31536000),
                    "month": math.floor(delta/2629746)%12,
                    "day": math.floor(delta/86400)%30,
                    "hour": math.floor(delta/3600)%24,
                    "minute": math.floor(delta/60)%60,
                    "second": math.floor(delta%60) }
    
    def get_data_service(self) -> DataService:
        """
        Accessor for `DataService` instance variable

        Returns:
            DataService: The servers `DataService` reference
        """
        return self.__data_service
    
    def get_parent_peer(self) -> Peer:
        """
        Accessor for the parent `Peer` object

        Returns:
            Peer: The parent `Peer` object
        """
        return self.__parent_peer
       
    


