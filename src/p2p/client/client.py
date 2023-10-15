import requests
from requests import Response
import shared.util as util
from p2p.connection import Connection
from p2p.peer.peer import Peer
import typing as t

class Client:

    def __init__(self, parent_node):
        self.parent_node = parent_node

    def join_network(self, bootstrap_connections:t.Iterable[Connection], peer=None):
        if peer is None:
            peer = self.parent_node.as_peer()
        response = self.post_some([Peer('any',c) for c in bootstrap_connections], '/node/join', peer)
            
            
    def shutdown_server(self):
        self.get_one(self.parent_node.connection, '/api/shutdown')
    
    def request_transaction(self, transaction):
        pass
    
    def get_all(self, uri:str) -> t.Dict[Peer, Response]:
        return self.get_some(self.parent_node.active_peers, uri)
    
    def get_some(self, peers:t.Iterable[Peer], uri:str) -> t.Dict[Peer, Response]:
        responses={}
        for peer in peers:
            responses[peer] = self.__get(peer.connection, uri)

        return responses

    def get_one(self, connection:Connection, uri:str) -> Response:
        return self.__get(connection, uri)
    
    def post_all(self, uri:str, data:any) -> t.Dict[Peer, Response]:
        return self.post_some(self.parent_node.active_peers, uri, data)

    def post_some(self, peers:t.Iterable[Peer], uri:str, data:any) -> t.Dict[Peer, Response]:
        responses = {}
        for peer in peers:
            responses[peer] = self.__post(peer.connection, uri, data)

    def post_one(self, connection:Connection, uri:str, data:any) -> Response:
        return self.__post(connection, uri, data)
    

    def __get(self, connection:Connection, uri:str) -> Response:
        return requests.get(self.__build_url(connection, uri), 
                            verify=self.parent_node.pki.certificate_authority_path, cert=self.parent_node.pki.get_cert())

    def __post(self, connection:Connection, uri:str, data:any) -> Response:
        return requests.post(self.__build_url(connection, uri), util.jsonify_data(data), 
                             verify=self.parent_node.pki.certificate_authority_path, cert=self.parent_node.pki.get_cert())
    
    def __build_url(self, connection:Connection, uri:str):
        return self.__get_protocol() + "://" + connection.host + ":" + str(connection.port) + "/" + uri
    
    def __get_protocol(self):
        return "http" if self.parent_node.pki.get_ssl_context() is None else "https"

