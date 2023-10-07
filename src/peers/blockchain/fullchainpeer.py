from p2p.peer.thispeer import ThisPeer
from p2p.connection import Connection
from flask import request,logging
from peers.blockchain.diagnostics.diagnostics import Diagnostics

class FullChainPeer(ThisPeer):

    def __init__(self, name:str, connection:Connection, diagnostics:bool=None):
        super().__init__(name, connection)
        self.logger = self.server.app.logger
        self.server.add_get_endpoint("/getBlocks", "getBlocks", self.__get_blocks)

        if diagnostics:
            self.diagnostics = Diagnostics(self.server)

        

        

    def __get_blocks(self):
        self.logger.info(request.args)
        return self.server.build_response(200, request.args)


    