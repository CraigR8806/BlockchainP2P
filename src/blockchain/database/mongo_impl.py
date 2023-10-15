from blockchain.database.database_interface import DatabaseInterface
from blockchain.data.block import Block
from p2p.connection import Connection
from pymongo import MongoClient
import shared.util as util
import typing as t





class MongoDatabaseImpl(DatabaseInterface):

    def __init__(self, database_connection:Connection, database:str, collection:str):
        super().__init__(database_connection, database)
        self.collection = collection

        self.client = MongoClient("mongodb://" + self.database_connection.host + ":" + str(self.database_connection.port))
        self.collection = self.client[database][collection]


    def commit_block(self, block:Block) -> None:
        self.collection.insert_one(util.documentify_data(block))

    def get_block(self, index:int) -> Block:
        return self.collection.find_one({"index":index})
    
    def get_blocks(self, indicies:t.Iterable[int]) -> t.Iterable[Block]:
        self.collection.find({ "index": { "$in" : indicies }})

    def get_chain_length(self) -> int:
        return self.collection.count_documents({})
    
