from p2p.peer.thispeer import ThisPeer
from p2p.connection import Connection
from flask import request, Response
from blockchain.diagnostics.diagnostics import Diagnostics
from shared.pki.pki import PKI
from blockchain.data.blockchain import Blockchain
from blockchain.peerstate import PeerState, PeerStateEnum
from blockchain.blockchain_client import BlockchainClient

# NEEDS COMMENTING

class FullChainPeer(ThisPeer):

    def __init__(self, name:str, connection:Connection, 
                 database_connection:Connection, database_name:str, 
                 collection:str, diagnostics:bool=None, pki:PKI=None,
                 is_bootstrap_node:bool=True):
        super().__init__(name, connection, is_bootstrap_node, pki)
        self._data_service.add("state", PeerState(PeerStateEnum.STARTING), asyync=True)
        self._server.add_get_endpoint("/chain/blocks", "/chain/blocks", self.__get_blocks)
        self._server.add_get_endpoint("/chain/length", "/chain/length", self.__chain_length)


        self.__chain = Blockchain(database_connection, self._data_service, database_name, collection, self._is_bootstrap_node)
        self.__chain_client = BlockchainClient(self._client, self.__chain, self._data_service)

        if diagnostics:
            self.__diagnostics = Diagnostics(self._server, self.__chain)

    def synchronize_chain(self, bootstrap_connection:Connection, post_sync_state:PeerStateEnum = PeerStateEnum.READY) -> None:
        self._data_service.modify("state", lambda v:v.change_state(PeerStateEnum.SYNCHRONIZING))
        self.__chain_client.synchronize_chain(bootstrap_connection)
        self._data_service.modify("state", lambda v:v.change_state(post_sync_state))

    def validate_chain(self, post_validate_state:PeerStateEnum = PeerStateEnum.READY) -> bool:
        self._data_service.modify("state", lambda v:v.change_state(PeerStateEnum.SYNCHRONIZING))
        # validate it using chain method
        self._data_service.modify("state", lambda v:v.change_state(post_validate_state))
        pass


    def __get_blocks(self) -> Response:
        start = int(request.args.get("start"))
        end = int(request.args.get("end"))

        blocks = self.__chain.get_blocks(start, end)
        return self._server.build_response(200, blocks)
    
    def __chain_length(self) -> Response:
        return self._server.build_response(200, self.__chain.chain_length())


    