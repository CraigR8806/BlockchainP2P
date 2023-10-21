from p2p.peer.peer import Peer
from p2p.connection import Connection
from p2p.client.client import Client
from p2p.server.server import Server
from p2p.dataservice import DataService
from shared.pki.pki import PKI
import time
import math

class ThisPeer(Peer):

    def __init__(self, name:str, connection:Connection, pki:PKI=None):
        super().__init__(name, connection)

        self.running = False

        self.pki = pki

        print("In constuctor for thispeer")
        self.data_service = DataService()
        self.data_service.start_service()
        active_peers = set([])
        active_peers.add(self.as_peer())

        self.data_service.add("active_peers", active_peers)

        self.client = Client(self.as_peer(), self.data_service, self.pki)
        self.server = Server(self.as_peer(), self.client, self.data_service, self.pki)


    def start_node(self):
        if not self.running:
            self.server.start_server()
            self.running = True

    def stop_node(self):
        if self.running:
            self.client.shutdown_server()
            self.server.stop_server()
            self.data_service.stop_service()

    def join_network(self, bootstrap_connections):
        self.client.join_network(bootstrap_connections)

    def as_peer(self):
        return Peer(self.name, self.connection)
    
    