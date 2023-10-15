from blockchain.database.database_interface import DatabaseInterface
from blockchain.data.block import Block
from pymongo import MongoClient
import shared.util as util
import typing as t





class MongoDatabaseImpl(DatabaseInterface):

    def __init__(self, host:str, port:int, database:str, collection:str):
        super().__init__(host, port, database)
        self.collection = collection

        self.client = MongoClient("mongodb://" + self.host + ":" + str(self.port))
        self.collection = self.client[database][collection]


    def commit_block(self, block:Block) -> None:
        self.collection.insert_one(util.jsonify_data(block))

    def get_block(self, index:int) -> Block:
        return util.extract_data(self.collection.find_one({"index":index}))
    
    def get_blocks(self, indicies:t.Iterable[int]) -> t.Iterable[Block]:
        self.collection.find({ "index": { "$in" : indicies }})

    def get_chain_length(self) -> int:
        return self.collection.count_documents({})
    
