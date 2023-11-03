from blockchain.data.block import Block
from blockchain.data.blockcandidate import BlockCandidate
from blockchain.database.mongo_impl import MongoDatabaseImpl
from hashlib import sha256
from random import randint
from logging import Logger
import typing as t

class Blockchain:

    def __init__(self, database_connection, database, collection, is_bootstrap_node):

        self.database = MongoDatabaseImpl(database_connection, database, collection)
        if is_bootstrap_node and self.database.get_chain_length() == 0:
            self.database.commit_block(self.create_genesis_block())

        print("Loaded blockchain from database.  Chain length is: " + str(self.database.get_chain_length()))

        self.change_pool = set([])
        self.candidate = None

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
    
    def get_latest_block(self):
        # REVISE
        # return self.chain[-1]
        pass
    
    def addNewBlock(self, block:Block):
        # REVISE
        # self.prepare_block_for_chain(block)
        # self.chain.append(block)
        pass

    def is_chain_valid(self, index:int=-1):
        # REVISE
        # if index == -1:
        #     index = len(self.chain) - 1

        # current_block = self.chain[index]
        # result = False

        # if index > 0:
        #     previous_block = self.chain[index - 1]
        #     result = (current_block.hash == current_block.calculateHash() and
        #               current_block.previous_hash == previous_block.hash and
        #               self.is_chain_valid(index - 1))
        # else:
        #     result = current_block.hash == self.create_genesis_block().hash

        # return result
        pass

    def add_to_change_pool(self, block:Block) -> None:
        self.change_pool.add(BlockCandidate(block))


    def process_pool(self) -> Block:
        unprocessed = [bc for bc in self.change_pool if not bc.processed]
        block = None
        if len(unprocessed):
            index = randint(0, len(unprocessed)-1)
            block = unprocessed[index].block
            self.prepare_block_for_chain(block)
            unprocessed[index].processed = True

        return block



    def prepare_block_for_chain(self, block:Block) -> None:
        # REVISE
        # block.previous_hash = self.get_latest_block().hash
        # block.hash = block.calculate_hash()
        pass