from p2p.peer.peer import Peer
from p2p.connection import Connection
from p2p.client.client import Client
from p2p.server.server import Server
from p2p.dataservice import DataService
from shared.pki.pki import PKI
import shared.util as util
import typing as t


class ThisPeer(Peer):

    """
    Representation of this actual P2P node\n
    Inherits from the parent `Peer` class\n
    Manages the `Server`, `Client`, and `DataService` for the P2P node

    ---
    FIELDS
    ---

    This class has no accessible fields

    """

    def __init__(self, name:str, connection:Connection, is_boostrap_node:bool = False, pki:PKI=None):
        """
        Constructor for `ThisPeer` class

        Args:
            name (str): The name of the `Peer`
            connection (Connection): The `Connection` object used to contact the `Peer`
            is_boostrap_node (bool, optional): If this `Peer` is bootstrap node. Defaults to False.
            pki (PKI, optional): The `PKI` object. Defaults to None.
        """
        super().__init__(name, connection)

        self._running = False

        self._pki = pki
        self._is_bootstrap_node = is_boostrap_node

        self._data_service = DataService()
        self._data_service.start_service()
        active_peers = set([])
        active_peers.add(self.as_peer())

        self._data_service.add("active_peers", active_peers)

        self._client = Client(self.as_peer(), self._data_service, self._pki)
        self._server = Server(self.as_peer(), self._client, self._data_service, self._pki)


    def start_node(self) -> None:
        """
        Starts the `Server`
        """
        if not self._running:
            self._server.start_server()
            self._running = True

    def stop_node(self) -> None:
        """
        Stops the `Server`\n
        Stops the `DataService`
        """
        if self._running:
            self._client.shutdown_server()
            self._server.stop_server()
            self._data_service.stop_service()

    def bootstrap_to_network(self, bootstrap_connections:t.Iterable[Connection]) -> None:
        """
        Uses the `Client` to make the required requests to join this node to the network

        Args:
            bootstrap_connections (t.Iterable[Connection): `list` of `Connection`s to use to bootstrap
        """
        peers_to_add = []
        for res in self._client.join_network([Peer('any',c) for c in bootstrap_connections]).values():
            peers_to_add += util.extract_data(res.text) 
        self._data_service.modify("active_peers", lambda v:v.update(set(peers_to_add)))

    def as_peer(self) -> Peer:
        """
        Retrieves a `Peer` representation of `ThisPeer`

        Returns:
            Peer: A `Peer` representation of `ThisPeer`
        """
        return Peer(self.get_name(), self.get_connection())
    
    