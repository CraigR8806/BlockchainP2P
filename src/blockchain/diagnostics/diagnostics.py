from p2p.server.server import Server
from p2p.server.endpoint import Endpoint
from p2p.dataservice import DataService
from blockchain.data.blockchain import Blockchain
from flask import Response, request
from http import HTTPStatus

# NEEDS COMMENTING


class Diagnostics:
    def __init__(self, server: Server, chain: Blockchain, data_service: DataService):
        self.__server = server
        self.__chain = chain
        self.__data_service = data_service
        self.__server.add_endpoint(
            Endpoint(
                "/diag/node/list",
                "nodeList",
                Endpoint.MethodEnum.GET,
                {"nodes": "List of nodes"},
                {},
            ),
            self.__list_nodes,
        )
        self.__server.add_endpoint(
            Endpoint(
                "/diag/node/name",
                "nodeName",
                Endpoint.MethodEnum.GET,
                {"name": "This node's name"},
                {},
            ),
            self.__get_name,
        )
        self.__server.add_endpoint(
            Endpoint(
                "/diag/node/connection",
                "nodeConnection",
                Endpoint.MethodEnum.GET,
                {"connection": "This node's connection"},
                {},
            ),
            self.__get_connection,
        )
        self.__server.add_endpoint(
            Endpoint(
                "/diag/node/uptime",
                "nodeUptime",
                Endpoint.MethodEnum.GET,
                {"uptime": "The uptime of the node"},
                {},
            ),
            self.__uptime,
        )
        self.__server.add_endpoint(
            Endpoint(
                "/diag/node/state",
                "nodeState",
                Endpoint.MethodEnum.GET,
                {"state": "The reported state of the node"},
                {},
            ),
            self.__state,
        )
        self.__server.add_endpoint(
            Endpoint(
                "/diag/node/chain/length",
                "chainlength",
                Endpoint.MethodEnum.GET,
                {"chain_length": "The length of the chain"},
                {},
            ),
            self.__chain_length,
        )
        self.__server.add_endpoint(
            Endpoint(
                "/diag/node/chain/block",
                "getblock",
                Endpoint.MethodEnum.GET,
                {"block": "The Block at the index provided"},
                {"index": "The index of the block requested"},
            ),
            self.__get_block,
        )
        self.__server.add_endpoint(
            Endpoint(
                "/diag/node/chain/blocks",
                "getblocks",
                Endpoint.MethodEnum.GET,
                {"block": "List of blocks being returned"},
                {"indicies": "List of indicies of the requested blocks"},
            ),
            self.__get_blocks,
        )
        self.__server.add_endpoint(
            Endpoint(
                "/diag/node/endpoints",
                "The Available Endpoints",
                Endpoint.MethodEnum.GET,
                {"endpoints": "List of endpoints"},
                {},
            ),
            self.__get_endpoints,
        )
        self.__server.add_endpoint(
            Endpoint(
                "/diag/data_service/highest_queue",
                "The Highest Queue in DataService",
                Endpoint.MethodEnum.GET,
                {"TODO": "TODO"},
                {"TODO": "TODO"},
            ),
            self.__get_highest_queue,
        )
        self.__server.add_endpoint(
            Endpoint(
                "/diag/data_service/watch_map",
                "The Watch Map from DataService",
                Endpoint.MethodEnum.GET,
                {"TODO": "TODO"},
                {"TODO": "TODO"},
            ),
            self.__get_watch_map,
        )

    def __list_nodes(self) -> Response:
        return self.__server.build_response(
            HTTPStatus.OK, self.__server.get_data_service().deep_copy("active_peers")
        )

    def __get_name(self) -> Response:
        return self.__server.build_response(
            HTTPStatus.OK, {"name": self.__server.get_parent_peer().get_name()}
        )

    def __get_connection(self) -> Response:
        return self.__server.build_response(
            HTTPStatus.OK, self.__server.get_parent_peer().get_connection()
        )

    def __uptime(self) -> Response:
        return self.__server.build_response(
            HTTPStatus.OK, {"uptime": self.__server.uptime()}
        )

    def __state(self) -> Response:
        return self.__server.build_response(
            HTTPStatus.OK,
            {"state": self.__server.get_data_service().deep_copy("state").get_state()},
        )

    def __chain_length(self) -> Response:
        return self.__server.build_response(
            HTTPStatus.OK, {"chain_length": self.__chain.chain_length()}
        )

    def __get_block(self) -> Response:
        index = int(request.args.get("index"))
        return self.__server.build_response(
            HTTPStatus.OK, self.__chain.get_block(index)
        )

    def __get_blocks(self) -> Response:
        start = int(request.args.get("start"))
        end = int(request.args.get("end"))

        blocks = self.__chain.get_blocks(start, end)
        return self.__server.build_response(HTTPStatus.OK, blocks)

    def __get_endpoints(self) -> Response:
        return self.__server.build_response(
            HTTPStatus.OK, {"endpoints": self.__server.get_endpoints()}
        )

    def __get_highest_queue(self) -> Response:
        return self.__server.build_response(
            HTTPStatus.OK, self.__data_service._get_highest_queue_count()
        )

    def __get_watch_map(self) -> Response:
        return self.__server.build_response(
            HTTPStatus.OK, self.__data_service._get_watch_map()
        )
