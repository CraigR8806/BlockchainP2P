from p2p.peer.thispeer import ThisPeer
from p2p.connection import Connection
from flask import request, Response
from blockchain.diagnostics.diagnostics import Diagnostics
from shared.pki.pki import PKI
from blockchain.data.blockchain import Blockchain
from blockchain.peerstate import PeerState, PeerStateEnum
from blockchain.blockchain_client import BlockchainClient

class FullChainPeer(ThisPeer):

    def __init__(self, name:str, connection:Connection, 
                 database_connection:Connection, database_name:str, 
                 collection:str, diagnostics:bool=None, pki:PKI=None,
                 is_bootstrap_node:bool=True):
        super().__init__(name, connection, is_bootstrap_node, pki)
        self.data_service.add("state", PeerState(PeerStateEnum.STARTING), asyync=True)
        self.server.add_get_endpoint("/chain/blocks", "/chain/blocks", self.__get_blocks)
        self.server.add_get_endpoint("/chain/length", "/chain/length", self.__chain_length)


        self.chain = Blockchain(database_connection, database_name, collection, is_bootstrap_node)
        self.chain_client = BlockchainClient(self.client, self.chain, self.data_service)

        if diagnostics:
            self.diagnostics = Diagnostics(self.server, self.chain)

    def synchronize_chain(self, bootstrap_connection:Connection, post_sync_state:PeerStateEnum = PeerStateEnum.READY) -> None:
        self.data_service.modify("state", lambda v:v.change_state(PeerStateEnum.SYNCHRONIZING))
        self.chain_client.synchronize_chain(bootstrap_connection)
        self.data_service.modify("state", lambda v:v.change_state(post_sync_state))

    def validate_chain(self, post_validate_state:PeerStateEnum = PeerStateEnum.READY) -> bool:
        self.data_service.modify("state", lambda v:v.change_state(PeerStateEnum.SYNCHRONIZING))
        # validate it using chain method
        self.data_service.modify("state", lambda v:v.change_state(post_validate_state))
        pass


    def __get_blocks(self) -> Response:
        start = int(request.args.get("start"))
        end = int(request.args.get("end"))

        blocks = self.chain.get_blocks(start, end)
        return self.server.build_response(200, blocks)
    
    def __chain_length(self) -> Response:
        return self.server.build_response(200, self.chain.chain_length())


    