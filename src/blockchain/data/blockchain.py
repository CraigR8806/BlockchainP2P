from blockchain.data.block import Block
from blockchain.data.blockcandidate import BlockCandidate
from hashlib import sha256
from random import randint
from blockchain.database.mongo_impl import MongoDatabaseImpl

class Blockchain:

    def __init__(self, database_connection, database, collection, bootstrap):

        self.database = MongoDatabaseImpl(database_connection, database, collection)
        if not bootstrap and self.database.get_chain_length() == 0:
            self.database.commit_block(self.create_genesis_block())

        print("Loaded blockchain from database.  Chain length is: " + str(self.database.get_chain_length()))

        self.change_pool = set([])
        self.candidate = None

    def create_genesis_block(self):
        return Block("01/01/2017", "Genesis block", 0, "0")
    
    def get_latest_block(self):
        return self.chain[-1]
    
    def addNewBlock(self, block:Block):
        self.prepare_block_for_chain(block)
        self.chain.append(block)

    def is_chain_valid(self, index:int=-1):
        if index == -1:
            index = len(self.chain) - 1

        current_block = self.chain[index]
        result = False

        if index > 0:
            previous_block = self.chain[index - 1]
            result = (current_block.hash == current_block.calculateHash() and
                      current_block.previous_hash == previous_block.hash and
                      self.is_chain_valid(index - 1))
        else:
            result = current_block.hash == self.create_genesis_block().hash

        return result

    def add_to_change_pool(self, block):
        self.change_pool.add(BlockCandidate(block))


    def process_pool(self):
        unprocessed = [bc for bc in self.change_pool if not bc.processed]
        block = None
        if len(unprocessed):
            index = randint(0, len(unprocessed)-1)
            block = unprocessed[index].block
            self.prepare_block_for_chain(block)
            unprocessed[index].processed = True

        return block



    def prepare_block_for_chain(self, block:Block):
        block.previous_hash = self.get_latest_block().hash
        block.hash = block.calculate_hash()