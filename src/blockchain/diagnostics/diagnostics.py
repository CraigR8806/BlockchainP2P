from p2p.server.server import Server
from blockchain.data.blockchain import Blockchain
from flask import Response, request

class Diagnostics:

    def __init__(self, server:Server, chain:Blockchain):
        self.server = server
        self.chain = chain
        self.server.add_get_endpoint("/diag/node/list", "nodeList", self.__list_nodes)
        self.server.add_get_endpoint("/diag/node/name", "nodeName", self.__get_name)
        self.server.add_get_endpoint("/diag/node/connection", "nodeConnection", self.__get_connection)
        self.server.add_get_endpoint("/diag/node/uptime", "nodeUptime", self.__uptime)
        self.server.add_get_endpoint("/diag/node/state", "nodeState", self.__state)
        self.server.add_get_endpoint("/diag/node/chain/length", "chainlength", self.__chain_length)
        self.server.add_get_endpoint("/diag/node/chain/block", "getblock", self.__get_block)
        self.server.add_get_endpoint("/diag/node/chain/blocks", "getblocks", self.__get_blocks)



    def __list_nodes(self) -> Response:
        return self.server.build_response(200, self.server.data_service.deep_copy("active_peers"))

    def __get_name(self) -> Response:
        return self.server.build_response(200, {"name": self.server.parent_peer.name})
    
    def __get_connection(self) -> Response:
        return self.server.build_response(200, self.server.parent_peer.connection)
    
    def __uptime(self) -> Response:
        return self.server.build_response(200, {"uptime":self.server.uptime()})
    
    def __state(self) -> Response:
        return self.server.build_response(200, {"state":self.server.data_service.deep_copy("state").get_state()})
    
    def __chain_length(self) -> Response:
        return self.server.build_response(200, {"chain_length":self.chain.chain_length()})
    
    def __get_block(self) -> Response:
        index = int(request.args.get("index"))
        return self.server.build_response(200, self.chain.get_block(index))
    
    def __get_blocks(self) -> Response:
        start = int(request.args.get("start"))
        end = int(request.args.get("end"))

        blocks = self.chain.get_blocks(start, end)
        return self.server.build_response(200, blocks)
    


