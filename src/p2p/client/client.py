import requests
from requests import Response
import shared.util as util
from p2p.connection import Connection
from p2p.peer.peer import Peer
from p2p.dataservice import DataService
from shared.pki.pki import PKI
from logging import Logger
from time import sleep
import typing as t

class Client:

    """
    Class representing the Client side of the P2P Node\n
    Provides P2P geared usage of the `requests` library\n

    ---
    FEILDS
    ---

    This class has no accessible fields
    """

    def __init__(self, parent_peer:Peer, data_service:DataService, pki:PKI):
        """
        Constructor for the Client class

        Args:
            parent_peer (Peer): The `Peer` representation of the `ThisPeer` that runs this `Client`
            data_service (DataService): The `DataService` provided by the parent `ThisPeer`
            pki (PKI): The `PKI` object
        """
        self.__parent_peer = parent_peer
        self.__data_service = data_service
        self.__pki = pki

    def join_network(self, peers:t.Iterable[Peer], peer:Peer = None, logger:Logger = None) -> t.Dict[Peer, Response]:
        """
        Makes the required requests to join a `Peer` the P2P network

        Args:
            peers (t.Iterable[Peer]): The `Peers` to send network join request to 
            peer (Peer, optional): The `Peer` to send with the network join request.  If none is supplied `ThisPeer` as `Peer` is used. Defaults to None.
            logger (Logger, optional): logger `!!!THIS WILL BE REMOVED IN FAVOR OF INSTANCE VARIABLE!!!`. Defaults to None.

        Returns:
            t.Dict[Peer, Response]: A `Dict` of `Peer` to that `Peer`'s `Response`
        """
        if peer is None:
            peer = self.__parent_peer
        return self.post_some(peers, '/node/join', peer, logger=logger)
            
    def shutdown_server(self) -> None:
        """
        Makes a request to the /api/shutdown endpoint of `ThisPeer`'s `Server`
        """
        self.get_one(self.__parent_peer.get_connection(), '/api/shutdown')
    
    def get_all(self, uri:str, logger:Logger = None) -> t.Dict[Peer, Response]:
        """
        Makes a `GET` request to the provided URI to all active `Peer`s

        Args:
            uri (str): The URI to use in the `GET` requests
            logger (Logger, optional): logger `!!!THIS WILL BE REMOVED IN FAVOR OF INSTANCE VARIABLE!!!`. Defaults to None.

        Returns:
            t.Dict[Peer, Response]: A `Dict` of `Peer` to that `Peer`'s `Response`
        """
        return self.get_some(self.__data_service.deep_copy("active_peers"), uri, logger=logger)
    
    def get_some(self, peers:t.Iterable[Peer], uri:str, logger:Logger = None) -> t.Dict[Peer, Response]:
        """
        Makes a `GET` request to the provided URI to the provided `set` of `Peer`s

        Args:
            peers (t.Iterable[Peer]): The `list` of `Peer`s to contact
            uri (str): The URI to use in the `GET` requests
            logger (Logger, optional): logger `!!!THIS WILL BE REMOVED IN FAVOR OF INSTANCE VARIABLE!!!`. Defaults to None.

        Returns:
            t.Dict[Peer, Response]: A `Dict` of `Peer` to that `Peer`'s `Response`
        """
        responses={}
        for peer in peers:
            responses[peer] = self.__get(peer.get_connection(), uri, logger=logger)
        return responses

    def get_one(self, connection:Connection, uri:str, params:t.Dict[str, str] = None, logger:Logger = None) -> Response:
        """
        Makes a `GET` request to the provided URI to the provided `Connection` `!!!I WANT TO CHANGE THIS TO PEER, BUT DEPENDENCY CHAIN SUCKS.  WILL REVIST!!!`

        Args:
            connection (Connection): The `Connection` on which to make the `GET` request
            uri (str): The URI to use in the `GET` request
            params (t.Dict[str, str], optional): Parameters to be used in the request. Defaults to None.
            logger (Logger, optional): logger `!!!THIS WILL BE REMOVED IN FAVOR OF INSTANCE VARIABLE!!!`. Defaults to None.

        Returns:
            Response: The `Response` from the request
        """
        return self.__get(connection, uri, params=params, logger=logger)
    
    def post_all(self, uri:str, data:any, logger:Logger = None) -> t.Dict[Peer, Response]:
        """
        Makes a `POST` request to the provided URI to all active `Peer`s

        Args:
            uri (str): The URI to use in the `POST` requests
            data (any): The data to apply to the `POST` requests
            logger (Logger, optional): logger `!!!THIS WILL BE REMOVED IN FAVOR OF INSTANCE VARIABLE!!!`. Defaults to None.

        Returns:
            t.Dict[Peer, Response]: A `Dict` of `Peer` to that `Peer`'s `Response`
        """
        return self.post_some(self.__data_service.deep_copy("active_peers"), uri, data, logger=logger)

    def post_some(self, peers:t.Iterable[Peer], uri:str, data:any, logger:Logger = None) -> t.Dict[Peer, Response]:
        """
        Makes a `POST` request to the provided URI to the provided `set` of `Peer`s

        Args:
            peers (t.Iterable[Peer]): The `list` of `Peer`s to contact
            uri (str): The URI to use in the `POST` requests
            data (any): The data to apply to the `POST` requests
            logger (Logger, optional): logger `!!!THIS WILL BE REMOVED IN FAVOR OF INSTANCE VARIABLE!!!`. Defaults to None.

        Returns:
            t.Dict[Peer, Response]: A `Dict` of `Peer` to that `Peer`'s `Response`
        """
        responses = {}
        for peer in peers:
            responses[peer] = self.__post(peer.get_connection(), uri, data, logger=logger)
        return responses

    def post_one(self, connection:Connection, uri:str, data:any, logger:Logger = None) -> Response:
        """
        Makes a `POST` request to the provided URI to the provided `Connection` `!!!I WANT TO CHANGE THIS TO PEER, BUT DEPENDENCY CHAIN SUCKS.  WILL REVIST!!!`

        Args:
            connection (Connection): The `Connection` on which to make the `POST` request
            uri (str): The URI to use in the `POST` request
            data (any): The data to apply to the `POST` request
            logger (Logger, optional): logger `!!!THIS WILL BE REMOVED IN FAVOR OF INSTANCE VARIABLE!!!`. Defaults to None.

        Returns:
            Response: The `Response` from the request
        """
        return self.__post(connection, uri, data, logger=logger)

    def __get(self, 
              connection:Connection, 
              uri:str, 
              params:t.Dict[str, str] = None,
              retry_on_fail:int = 3,
              wait_time_between_retries:float = 0.5,
              logger:Logger = None) -> Response:
        if logger:
                logger.debug("Making GET request to " + connection.get_host() + ":" + connection.get_port())
        return self.__retry_if_fail(lambda: requests.get(self.__build_url(connection, uri), headers={"Accept": "application/json"},
                                    verify=self.__pki.certificate_authority_path, cert=self.__pki.get_ssl_context(),
                                    params=params), retry_on_fail, wait_time_between_retries)

    def __post(self, 
               connection:Connection, 
               uri:str, 
               data:any,
               retry_on_fail:int = 3,
               wait_time_between_retries:float = 0.5,
               logger:Logger = None) -> Response:
        if logger:
                logger.debug("Making POST request to " + connection.get_host() + ":" + connection.get_port())

        return self.__retry_if_fail(lambda: requests.post(self.__build_url(connection, uri), util.jsonify_data(data),
                                    headers={"Accept": "application/json"},
                                    verify=self.__pki.certificate_authority_path, 
                                    cert=self.__pki.get_ssl_context()), retry_on_fail, wait_time_between_retries)
    

    def __retry_if_fail(self, func:t.Callable, retries:int, wait:float):
        attempts = 0
        success = False
        ret = None
        while not success and attempts <= retries:
            try:
                ret = func()
                success = True
            except:
                attempts+=1
                sleep(wait)

        return ret
    
    def __build_url(self, connection:Connection, uri:str) -> str:
        return self.__get_protocol() + "://" + connection.get_host() + ":" + connection.get_port() + "/" + uri
    
    def __get_protocol(self) -> str:
        return "http" if self.__pki.get_ssl_context() is None else "https"

