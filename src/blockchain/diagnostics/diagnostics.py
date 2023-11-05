from p2p.server.server import Server
from blockchain.data.blockchain import Blockchain
from flask import Response, request

# NEEDS COMMENTING

class Diagnostics:

    def __init__(self, server:Server, chain:Blockchain):
        self.__server = server
        self.__chain = chain
        self.__server.add_get_endpoint("/diag/node/list", "nodeList", self.__list_nodes)
        self.__server.add_get_endpoint("/diag/node/name", "nodeName", self.__get_name)
        self.__server.add_get_endpoint("/diag/node/connection", "nodeConnection", self.__get_connection)
        self.__server.add_get_endpoint("/diag/node/uptime", "nodeUptime", self.__uptime)
        self.__server.add_get_endpoint("/diag/node/state", "nodeState", self.__state)
        self.__server.add_get_endpoint("/diag/node/chain/length", "chainlength", self.__chain_length)
        self.__server.add_get_endpoint("/diag/node/chain/block", "getblock", self.__get_block)
        self.__server.add_get_endpoint("/diag/node/chain/blocks", "getblocks", self.__get_blocks)



    def __list_nodes(self) -> Response:
        return self.__server.build_response(200, self.__server.get_data_service().deep_copy("active_peers"))

    def __get_name(self) -> Response:
        return self.__server.build_response(200, {"name": self.__server.get_parent_peer().get_name()})
    
    def __get_connection(self) -> Response:
        return self.__server.build_response(200, self.__server.get_parent_peer().get_connection())
    
    def __uptime(self) -> Response:
        return self.__server.build_response(200, {"uptime":self.__server.uptime()})
    
    def __state(self) -> Response:
        return self.__server.build_response(200, {"state":self.__server.get_data_service().deep_copy("state").get_state()})
    
    def __chain_length(self) -> Response:
        return self.__server.build_response(200, {"chain_length":self.__chain.chain_length()})
    
    def __get_block(self) -> Response:
        index = int(request.args.get("index"))
        return self.__server.build_response(200, self.__chain.get_block(index))
    
    def __get_blocks(self) -> Response:
        start = int(request.args.get("start"))
        end = int(request.args.get("end"))

        blocks = self.__chain.get_blocks(start, end)
        return self.__server.build_response(200, blocks)
    


