from p2p.connection import Connection
from shared.pki.pki import PKI
from blockchain.fullchainpeer import FullChainPeer


class ProductPeer(FullChainPeer):
    def __init__(
        self,
        name: str,
        connection: Connection,
        database_connection: Connection,
        database_name: str,
        collection: str,
        diagnostics: bool = None,
        pki: PKI = None,
        is_bootstrap_node: bool = True,
    ):
        super().__init(
            name,
            connection,
            database_connection,
            database_name,
            collection,
            diagnostics,
            pki,
            is_bootstrap_node,
        )
