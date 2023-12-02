from p2p.client.client import Client
from p2p.peer.peer import Peer
from p2p.connection import Connection
from p2p.dataservice import DataService
from blockchain.data.blockchain import Blockchain
from blockchain.data.block import Block, BlockData
from blockchain.peerstate import PeerStateEnum
import shared.util as util
from time import time
import typing as t
from http import HTTPStatus

# NEEDS COMMENTING


class BlockchainClient:
    def __init__(
        self,
        self_as_peer: Peer,
        client: Client,
        chain: Blockchain,
        data_service: DataService,
    ):
        self.__self_as_peer = self_as_peer
        self.__client = client
        self.__chain = chain
        self.__data_service = data_service

    def synchronize_chain(self, bootstrap_connection: Connection) -> None:
        start = self.__chain.chain_length()
        end = util.extract_data(
            self.__client.get_one(bootstrap_connection, "/chain/length").text
        )

        if start < end:
            blocks = util.extract_data(
                self.__client.get_one(
                    bootstrap_connection,
                    "/chain/blocks",
                    {"start": str(start), "end": str(end)},
                ).text
            )

            self.__chain.commit_blocks(blocks)

        self.__data_service.modify(
            "state", lambda v: v.change_state(PeerStateEnum.VALIDATING)
        )

        if not self.__chain.is_chain_valid():
            self.__data_service.modify(
                "state", lambda v: v.change_state(PeerStateEnum.ERROR)
            )

    def vote_new_block(self, block: Block) -> None:
        self.__client.post_all(
            "/chain/new_block_vote", {"vote": block.hash, "peer": self.__self_as_peer}
        )

    def request_transaction(self, data: BlockData):
        self.__client.post_all("/chain/request_transaction", {"block_data": data})

    def request_last_committed(self, peers_to_ask: t.Iterable[Peer]) -> Block:
        block = None
        while block is None and len(peers_to_ask):
            response = self.__client.get_one(
                peers_to_ask.pop().get_connection(), "/chain/last_committed"
            )
            if response.status_code != HTTPStatus.OK:
                continue

            block = util.extract_data(response.json())

        return block
