from abc import ABC, abstractmethod
from blockchain.data.block import Block
from p2p.connection import Connection
import typing as t


class DatabaseInterface(ABC):


    def __init__(self, database_connection:Connection, database:str):
        self.database_connection = database_connection
        self.database = database


    @abstractmethod
    def commit_block(self, block:Block) -> None:
        pass

    @abstractmethod
    def commit_blocks(self, blocks:t.Iterable[Block]) -> None:
        pass

    @abstractmethod
    def get_block(self, index:int) -> Block:
        pass

    @abstractmethod
    def get_blocks(self, indicies:t.Iterable[int]) -> t.Iterable[Block]:
        pass

    @abstractmethod
    def get_chain_length(self) -> int:
        pass




    