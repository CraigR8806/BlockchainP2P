from p2p.peer.thispeer import ThisPeer
from p2p.connection import Connection
from flask import request
from blockchain.diagnostics.diagnostics import Diagnostics
from shared.pki.pki import PKI
from blockchain.data.blockchain import Blockchain

class FullChainPeer(ThisPeer):

    def __init__(self, name:str, connection:Connection, 
                 database_connection:Connection, database:str, 
                 collection:str, diagnostics:bool=None, pki:PKI=None,
                 bootstrap:bool=True):
        super().__init__(name, connection, pki)
        self.server.add_get_endpoint("/getBlocks", "getBlocks", self.__get_blocks)

        if diagnostics:
            self.diagnostics = Diagnostics(self.server)

        self.chain = Blockchain(database_connection, database, collection, bootstrap)

    def __get_blocks(self):
        self.logger.info(request.args)
        return self.server.build_response(200, request.args)


    