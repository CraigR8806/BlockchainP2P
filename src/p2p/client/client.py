import requests
from requests import Response
import shared.util as util
from p2p.connection import Connection
from p2p.peer.peer import Peer
from p2p.dataservice import DataService
from shared.pki.pki import PKI
from logging import Logger
import typing as t

class Client:

    def __init__(self, parent_peer:Peer, data_service:DataService, pki:PKI):
        self.parent_peer = parent_peer
        self.data_service = data_service
        self.pki = pki

    def join_network(self, peers:t.Iterable[Peer], peer:Peer = None, logger:Logger = None) -> t.Dict[Peer, Response]:
        if peer is None:
            peer = self.parent_peer
        return self.post_some(peers, '/node/join', peer, logger=logger)

    def bootstrap_to_network(self, bootstrap_connections:t.Iterable[Connection], peer:Peer=None, logger:Logger = None) -> t.Dict[Peer, Response]:
        if peer is None:
            peer = self.parent_peer
        return self.post_some([Peer('any',c) for c in bootstrap_connections], '/node/join', peer, logger=logger)
        
            
    def shutdown_server(self) -> None:
        self.get_one(self.parent_peer.connection, '/api/shutdown')
    
    def request_transaction(self, transaction):
        pass
    
    def get_all(self, uri:str, logger:Logger = None) -> t.Dict[Peer, Response]:
        return self.get_some(self.data_service.deep_copy("active_peers"), uri, logger=logger)
    
    def get_some(self, peers:t.Iterable[Peer], uri:str, logger:Logger = None) -> t.Dict[Peer, Response]:
        responses={}
        for peer in peers:
            responses[peer] = self.__get(peer.connection, uri, logger=logger)
        return responses

    def get_one(self, connection:Connection, uri:str, params:t.Dict[str, str] = None, logger:Logger = None) -> Response:
        return self.__get(connection, uri, params=params, logger=logger)
    
    def post_all(self, uri:str, data:any, logger:Logger = None) -> t.Dict[Peer, Response]:
        return self.post_some(self.data_service.deep_copy("active_peers"), uri, data, logger=logger)

    def post_some(self, peers:t.Iterable[Peer], uri:str, data:any, logger:Logger = None) -> t.Dict[Peer, Response]:
        responses = {}
        for peer in peers:
            responses[peer] = self.__post(peer.connection, uri, data, logger=logger)
        return responses

    def post_one(self, connection:Connection, uri:str, data:any, logger:Logger = None) -> Response:
        return self.__post(connection, uri, data, logger=logger)

    def __get(self, connection:Connection, uri:str, params:t.Dict[str, str] = None, logger:Logger = None) -> Response:
        if logger:
                logger.debug("Making GET request to " + connection.host + ":" + str(connection.port))
        return requests.get(self.__build_url(connection, uri), headers={"Accept": "application/json"},
                            verify=self.pki.certificate_authority_path, cert=self.pki.get_cert(),
                            params=params)

    def __post(self, connection:Connection, uri:str, data:any, logger:Logger = None) -> Response:
        if logger:
                logger.debug("Making POST request to " + connection.host + ":" + str(connection.port))
        return requests.post(self.__build_url(connection, uri), util.jsonify_data(data), headers={"Accept": "application/json"},
                             verify=self.pki.certificate_authority_path, cert=self.pki.get_cert())
    
    def __build_url(self, connection:Connection, uri:str) -> str:
        return self.__get_protocol() + "://" + connection.host + ":" + str(connection.port) + "/" + uri
    
    def __get_protocol(self) -> str:
        return "http" if self.pki.get_ssl_context() is None else "https"

