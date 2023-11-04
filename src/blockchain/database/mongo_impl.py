from blockchain.database.database_interface import DatabaseInterface
from blockchain.data.block import Block
from p2p.connection import Connection
from pymongo import MongoClient
import shared.util as util
from logging import Logger
import typing as t





class MongoDatabaseImpl(DatabaseInterface):

    """
    Blockchain database interface implementation for MongoDB

    ---
    FIELDS
    ---
    
    This class has no accessible fields
    """

    def __init__(self, database_connection:Connection, database:str, collection:str):
        """
        Constructor for MongoDatabaseImpl

        Args:
            database_connection (Connection): Connection object representing how to communicate with the database
            database (str): Database name
            collection (str): Collection name
        """
        super().__init__(database_connection, "mongodb", database)
        self.__collection = collection

        self.__client = MongoClient(self._database_connection_string)
        self.__collection = self.__client[database][collection]


    def commit_block(self, block:Block) -> None:
        """
        Saves `Block` to database

        Args:
            block (Block): The `Block` to save
        """
        self.__collection.insert_many([util.documentify_data(block)])

    def commit_blocks(self, blocks:t.Iterable[Block]) -> None:
        """
        Saves `list` of `Block`s to the database

        Args:
            blocks (t.Iterable[Block]): The `list` of `Block`s to save
        """
        self.__collection.insert_many(util.documentify_data(blocks))

    def get_block(self, index:int) -> Block:
        """
        Retrieves `Block` from database

        Args:
            index (int): index of `Block` on `Blockchain` to retrieve

        Returns:
            Block: The requested `Block`
        """
        return util.dataify_document(self.__collection.find_one({"index":index}))
    
    def get_blocks(self, indicies:t.Iterable[int]) -> t.Iterable[Block]:
        """
        Retrieves `Block`s from database

        Args:
            indicies (t.Iterable[int]): `list` of indicies for `Block`s on `Blockchain` to retrieve

        Returns:
            t.Iterable[Block]: The request `Block`s
        """
        return [util.dataify_document(b) for b in list(self.__collection.find({ "index": { "$in" : indicies }}))]

    def get_chain_length(self) -> int:
        """
        Retrieves the total `Blockchain` length

        Returns:
            int: The length of the `Blockchain` in the database
        """
        return self.__collection.count_documents({})
    
