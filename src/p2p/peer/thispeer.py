from p2p.peer.peer import Peer
from p2p.connection import Connection
from p2p.client.client import Client
from p2p.server.server import Server
from p2p.dataservice import DataService
from shared.pki.pki import PKI
import shared.util as util


class ThisPeer(Peer):

    def __init__(self, name:str, connection:Connection, is_boostrap_node:bool = False, pki:PKI=None):
        super().__init__(name, connection)

        self.running = False

        self.pki = pki
        self.is_bootstrap_node = is_boostrap_node

        self.data_service = DataService()
        self.data_service.start_service()
        active_peers = set([])
        active_peers.add(self.as_peer())

        self.data_service.add("active_peers", active_peers)

        self.client = Client(self.as_peer(), self.data_service, self.pki)
        self.server = Server(self.as_peer(), self.client, self.data_service, self.pki)


    def start_node(self) -> None:
        if not self.running:
            self.server.start_server()
            self.running = True

    def stop_node(self) -> None:
        if self.running:
            self.client.shutdown_server()
            self.server.stop_server()
            self.data_service.stop_service()

    def bootstrap_to_network(self, bootstrap_connections) -> None:
        peers_to_add = []
        for res in self.client.bootstrap_to_network(bootstrap_connections).values():
            peers_to_add += util.extract_data(res.text) 
        self.data_service.modify("active_peers", lambda v:v.update(set(peers_to_add)))

    def as_peer(self) -> Peer:
        return Peer(self.name, self.connection)
    
    