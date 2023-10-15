from p2p.peer.thispeer import ThisPeer
from p2p.connection import Connection
from flask import request
from blockchain.diagnostics.diagnostics import Diagnostics
from shared.pki.pki import PKI
from blockchain.database.mongo_impl import MongoDatabaseImpl

class FullChainPeer(ThisPeer):

    def __init__(self, name:str, connection:Connection, database_connection:Connection, database:str, collection:str, diagnostics:bool=None, pki:PKI=None):
        super().__init__(name, connection, pki)
        self.server.add_get_endpoint("/getBlocks", "getBlocks", self.__get_blocks)

        if diagnostics:
            self.diagnostics = Diagnostics(self.server)

        self.database = MongoDatabaseImpl(database_connection.host, database_connection.port, database, collection)

        print("Loaded blockchain from database.  Chain length is: " + str(self.database.get_chain_length()))

        

    def __get_blocks(self):
        self.logger.info(request.args)
        return self.server.build_response(200, request.args)


    