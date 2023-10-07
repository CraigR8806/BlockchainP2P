from p2p.peer.peer import Peer
from p2p.connection import Connection
from p2p.client.client import Client
from p2p.server.server import Server
import time
import math

class ThisPeer(Peer):

    def __init__(self, name:str, connection:Connection):
        super().__init__(name, connection)

        self.running = False

        
        self.client = Client(self)
        self.server = Server(self)

        self.active_peers = set([])
        self.active_peers.add(self.as_peer())

        self.start_time = None


    def start_node(self):
        if not self.running:
            self.server.start_server()
            self.start_time = time.time()
            self.running = True

    def stop_node(self):
        if self.running:
            self.client.shutdown_server()
            self.server.stop_server()

    def join_network(self, bootstrap_connections):
        self.client.join_network(bootstrap_connections)

    def add_peer(self, peer):
        self.active_peers.add(peer)

    def get_active_peers(self):
        return self.active_peers

    def as_peer(self):
        return Peer(self.name, self.connection)
    
    def uptime(self):
        if self.running:
            delta=time.time() - self.start_time
            return { "year": math.floor(delta/31536000),
                     "month": math.floor(delta/2629746)%12,
                     "day": math.floor(delta/86400)%30,
                     "hour": math.floor(delta/3600)%24,
                     "minute": math.floor(delta/60)%60,
                     "second": math.floor(delta%60) }
        else:
            return {"year":0,
                    "month":0,
                    "day":0,
                    "hour":0,
                    "minute":0,
                    "second":0 }