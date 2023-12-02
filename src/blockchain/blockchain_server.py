from p2p.server.server import Server, Capability
from p2p.dataservice import DataService
from p2p.server.endpoint import Endpoint
from blockchain.peerstate import PeerStateEnum
from blockchain.data.block import Block, BlockData
from blockchain.data.blockchain import Blockchain
from blockchain.blockchain_client import BlockchainClient
import shared.util as util
from flask import Response, request
from http import HTTPStatus
from time import time


class BlockchainServer:
    def __init__(
        self,
        server: Server,
        chain: Blockchain,
        data_service: DataService,
        blockchain_client: BlockchainClient,
    ):
        self.__server = server
        self.__server.add_capability(
            Capability(
                "BlockchainInformation",
                "BlockchainInformation/BlockchainInformation.js",
            )
        )

        self.__chain = chain
        self.__data_service = data_service
        self.__blockchain_client = blockchain_client

        self.__server.add_endpoint(
            Endpoint(
                "/chain/blocks",
                "Get Blocks in Range",
                Endpoint.MethodEnum.GET,
                {"blocks": "List of returned blocks"},
                {"indicies": "List of indicies of the requested blocks"},
            ),
            self.__get_blocks,
        )
        self.__server.add_endpoint(
            Endpoint(
                "/chain/length",
                "Get Chain Length",
                Endpoint.MethodEnum.GET,
                {"chain_length": "Length of the chain"},
                {},
            ),
            self.__chain_length,
        )
        self.__server.add_endpoint(
            Endpoint(
                "/chain/request_transaction",
                "New Block Request",
                Endpoint.MethodEnum.POST,
                {"TODO": "TODO"},
                {"TODO": "TODO"},
            ),
            self.__request_transaction,
        )
        self.__server.add_endpoint(
            Endpoint(
                "/chain/new_block_vote",
                "Block Vote Submission",
                Endpoint.MethodEnum.POST,
                {"TODO": "TODO"},
                {"TODO": "TODO"},
            ),
            self.__new_block_vote,
        )
        self.__server.add_endpoint(
            Endpoint(
                "/chain/last_committed",
                "Request Last Block Committed",
                Endpoint.MethodEnum.GET,
                {"TODO": "TODO"},
                {"TODO": "TODO"},
            ),
            self.__request_last_committed,
        )
        self.__server.add_endpoint(
            Endpoint(
                "/chain/new_block_data",
                "Instruct Peer to Request new Block Data",
                Endpoint.MethodEnum.POST,
                {"TODO": "TODO"},
                {"TODO": "TODO"},
            ),
            self.__new_block_data,
        )
        self.__server.add_endpoint(
            Endpoint(
                "/chain/validate",
                "Validate Chain",
                Endpoint.MethodEnum.GET,
                {"TODO": "TODO"},
                {"TODO": "TODO"},
            ),
            self.__validate_chain,
        )

    def __get_blocks(self) -> Response:
        start = int(request.args.get("start"))
        end = int(request.args.get("end"))

        blocks = self.__chain.get_blocks(start, end)
        return self.__server.build_response(HTTPStatus.OK, blocks)

    def __chain_length(self) -> Response:
        return self.__server.build_response(HTTPStatus.OK, self.__chain.chain_length())

    def __request_transaction(self) -> Response:
        block_data = util.extract_data(request.get_data(as_text=True))["block_data"]
        self.__chain.add_to_change_pool(block_data)
        return self.__server.build_response(HTTPStatus.OK, None)

    def __new_block_vote(self) -> Response:
        data = util.extract_data(request.get_data(as_text=True))
        peer = data["peer"]
        vote = data["vote"]
        if self.__data_service.deep_copy("vote_map")[peer] != 0:
            self.__data_service.modify(
                "vote_map_buffer", lambda v: v.update({peer: vote})
            )
        else:
            self.__data_service.modify("vote_map", lambda v: v.update({peer: vote}))

        return self.__server.build_response(HTTPStatus.OK, None)

    def __request_last_committed(self) -> Response:
        block = self.__chain.get_latest_block()
        return self.__server.build_response(HTTPStatus.OK, block)

    def __new_block_data(self) -> Response:
        block_data = BlockData(
            util.extract_data(request.get_data(as_text=True))["block_data"]
        )
        self.__blockchain_client.request_transaction(block_data)
        return self.__server.build_response(HTTPStatus.OK, {})

    def __validate_chain(self) -> Response:
        return self.__server.build_response(
            HTTPStatus.OK, self.__chain.is_chain_valid()
        )
