from p2p.connection import Connection
from p2p.dataservice import DataService
from blockchain.data.block import Block, BlockData
from blockchain.data.blockcandidate import BlockCandidate
from blockchain.database.mongo_impl import MongoDatabaseImpl
from hashlib import sha256
from random import randint
import typing as t
from datetime import datetime


# NEEDS COMMENTING


class Blockchain:
    def __init__(
        self,
        database_connection: Connection,
        data_service: DataService,
        database_name: str,
        collection: str,
        is_bootstrap_node: bool,
    ):
        self.__database = MongoDatabaseImpl(
            database_connection, database_name, collection
        )
        if is_bootstrap_node and self.__database.get_chain_length() == 0:
            self.__database.commit_block(self.__create_genesis_block())

        self.__data_service = data_service

        self.__change_pool = "chain_change_pool"
        self.__candidate = "chain_candidate"

        self.__data_service.upsert(self.__change_pool, set([]))
        self.__data_service.upsert(self.__candidate, BlockCandidate())

        print(
            "Loaded blockchain from database.  Chain length is: "
            + str(self.__database.get_chain_length())
        )

    def __create_genesis_block(self) -> Block:
        utc_time = datetime.strptime(
            "2017-01-01T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        epoch_time = (utc_time - datetime(1970, 1, 1)).total_seconds()
        return Block(BlockData("Genesis block"), epoch_time, 0, "0")

    def chain_length(self) -> int:
        return self.__database.get_chain_length()

    def commit_block(self, block: Block) -> None:
        self.__database.commit_block(block)

    def commit_blocks(self, blocks: t.Iterable[Block]) -> None:
        self.__database.commit_blocks(blocks)

    def get_block(self, index: int) -> Block:
        return self.__database.get_block(index)

    def get_blocks(self, start: int, end: int) -> t.Iterable[Block]:
        return self.get_blocks_with_indicies(list(range(start, end)))

    def get_blocks_with_indicies(self, indicies: t.Iterable[int]) -> t.Iterable[Block]:
        return self.__database.get_blocks(indicies)

    def get_latest_block(self) -> Block:
        return self.get_block(self.chain_length() - 1)

    def is_chain_valid(self, index: int = -1) -> bool:
        if index == -1:
            index = self.chain_length() - 1

        current_block = self.get_block(index)
        result = False

        if index > 0:
            previous_block = self.get_block(index - 1)
            result = (
                current_block.hash == current_block.calculate_hash()
                and current_block.previous_hash == previous_block.hash
                and self.is_chain_valid(index - 1)
            )
        else:
            result = current_block.hash == self.__create_genesis_block().hash

        return result

    def add_to_change_pool(self, block_data: BlockData) -> None:
        self.__data_service.modify(
            self.__change_pool, lambda v: v.add(BlockCandidate(block_data))
        )

    def process_pool(self) -> Block:
        change_pool_copy = self.__data_service.deep_copy(self.__change_pool)
        unprocessed = [bc for bc in change_pool_copy if not bc.is_processed()]
        block = None
        if len(unprocessed):
            index = randint(0, len(unprocessed) - 1)
            candidate = unprocessed[index]

            block = self.prepare_block_for_chain(candidate)
            self.__data_service.upsert(self.__candidate, block)

        return block

    def does_match_candidate(self, hashh: str) -> bool:
        return self.__data_service.deep_copy(self.__candidate).hash == hashh

    def candidate_approved(self) -> None:
        block = self.__data_service.deep_copy(self.__candidate)
        change_pool = self.__data_service.deep_copy(self.__change_pool)

        print("---------------------------------------------------------")
        print(list(change_pool)[0].block_data)
        print(block.data)
        print(block.data == list(change_pool)[0].block_data)
        print("---------------------------------------------------------")

        self.__data_service.modify(
            self.__change_pool, lambda v: v.remove(BlockCandidate(block.data))
        )

        self.commit_block(block)

    def prepare_block_for_chain(self, block_candidate: BlockCandidate) -> None:
        return block_candidate.process(
            self.chain_length(), self.get_latest_block().hash
        )
