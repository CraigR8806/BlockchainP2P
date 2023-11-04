from p2p.connection import Connection
from p2p.dataservice import DataService
from blockchain.data.block import Block
from blockchain.data.blockcandidate import BlockCandidate
from blockchain.database.mongo_impl import MongoDatabaseImpl
from hashlib import sha256
from random import randint
from logging import Logger
import typing as t

class Blockchain:

    def __init__(self, 
                 database_connection:Connection, 
                 data_service:DataService,
                 database_name:str, 
                 collection:str, 
                 is_bootstrap_node:bool):

        self.database = MongoDatabaseImpl(database_connection, database_name, collection)
        if is_bootstrap_node and self.database.get_chain_length() == 0:
            self.database.commit_block(self.create_genesis_block())

        self.data_service = data_service

        self.change_pool = "chain_change_pool"
        self.candidate = "chain_candidate"

        self.data_service.add(self.change_pool, set([]))
        self.data_service.add(self.candidate, BlockCandidate())

        print("Loaded blockchain from database.  Chain length is: " + str(self.database.get_chain_length()))


    def create_genesis_block(self) -> Block:
        return Block("01/01/2017", "Genesis block", 0, "0")
    
    def chain_length(self) -> int:
        return self.database.get_chain_length()
    
    def commit_block(self, block:Block) -> None:
        self.database.commit_block(block)

    def commit_blocks(self, blocks:t.Iterable[Block]) -> None:
        self.database.commit_blocks(blocks)

    def get_block(self, index:int) -> Block:
        return self.database.get_block(index)
    
    def get_blocks(self, start:int, end:int) -> t.Iterable[Block]:
        return self.get_blocks_with_indicies(list(range(start, end)))

    def get_blocks_with_indicies(self, indicies:t.Iterable[int]) -> t.Iterable[Block]:
        return self.database.get_blocks(indicies)
    
    def get_latest_block(self) -> Block:
        return self.get_block(self.chain_length() - 1)

    def is_chain_valid(self, index:int=-1) -> bool:
        if index == -1:
            index = self.chain_length() - 1

        current_block = self.get_block(index)
        result = False

        if index > 0:
            previous_block = self.get_block(index - 1)
            result = (current_block.hash == current_block.calculateHash() and
                      current_block.previous_hash == previous_block.hash and
                      self.is_chain_valid(index - 1))
        else:
            result = current_block.hash == self.create_genesis_block().hash

        return result

    def add_to_change_pool(self, block:Block) -> None:
        self.data_service.modify(self.change_pool, lambda v:v.add(BlockCandidate(block)))


    def process_pool(self) -> Block:
        change_pool_copy = self.data_service.deep_copy(self.change_pool)
        unprocessed = [bc for bc in change_pool_copy if not bc.is_processed()]
        block = None
        if len(unprocessed):
            index = randint(0, len(unprocessed)-1)
            candidate = unprocessed[index]
            self.data_service.modify(self.change_pool, lambda v:v.remove(candidate), asyync=True)
            self.data_service.modify(self.candidate, lambda v:v.update(candidate.candidate().copy_of(), candidate.is_processed()))
            block = unprocessed[index].candidate()
            self.prepare_block_for_chain(block)
            unprocessed[index].processed = True


        return block



    def prepare_block_for_chain(self, block:Block) -> None:
        block.previous_hash = self.get_latest_block().hash
        block.hash = block.calculate_hash()