from p2p.peer.peer import Peer
from p2p.connection import Connection
from p2p.client.client import Client
from p2p.server.server import Server


class ThisPeer(Peer):

    def __init__(self, name:str, connection:Connection):
        super().__init__(name, connection)

        self.running = False

        self.client = Client(self)
        self.server = Server(self)

        self.active_peers = set([])
        self.active_peers.add(self.as_peer())


    def start_node(self):
        if not self.running:
            self.server.start_server()
            self.running = True

    def stop_node(self):
        if self.running:
            self.server.stop_server()

    def join_network(self, bootstrap_connections):
        self.client.join_network(bootstrap_connections)

    def add_peer(self, peer):
        self.active_peers.add(peer)

    def get_active_peers(self):
        return self.active_peers

    def as_peer(self):
        return Peer(self.name, self.connection)