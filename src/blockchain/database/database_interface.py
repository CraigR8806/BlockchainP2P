from abc import ABC, abstractmethod
from blockchain.data.block import Block
from blockchain.data.blockchain import Blockchain
import typing as t


class DatabaseInterface(ABC):


    def __init__(self, host:str, port:int, database:str):
        self.host = host
        self.port = port
        self.database = database


    @abstractmethod
    def commit_block(self, block:Block) -> None:
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




    