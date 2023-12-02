from abc import ABC, abstractmethod
from blockchain.data.block import Block
from p2p.connection import Connection
import typing as t


class DatabaseInterface(ABC):

    """
    Abstract class defining what implementations must conform to

    ---
    FIELDS
    ---

    This class has no accessible fields
    """

    def __init__(
        self, database_connection: Connection, database_protocol: str, database: str
    ):
        """
        Constructor for DatabaseInterface

        Args:
            database_connection (Connection): Connection object representing how to communicate with the database
            database_protocol (str): Protocol to use to communicate with the database
            database (str): The database name
        """
        self._database_connection_string = (
            database_protocol
            + "://"
            + database_connection.get_host()
            + ":"
            + database_connection.get_port()
        )
        self._database = database

    @abstractmethod
    def commit_block(self, block: Block) -> None:
        """
        Saves `Block` to database

        Args:
            block (Block): The `Block` to save
        """
        pass

    @abstractmethod
    def commit_blocks(self, blocks: t.Iterable[Block]) -> None:
        """
        Saves `list` of `Block`s to the database

        Args:
            blocks (t.Iterable[Block]): The `list` of `Block`s to save
        """
        pass

    @abstractmethod
    def get_block(self, index: int) -> Block:
        """
        Retrieves `Block` from database

        Args:
            index (int): index of `Block` on `Blockchain` to retrieve

        Returns:
            Block: The requested `Block`
        """
        pass

    @abstractmethod
    def get_blocks(self, indicies: t.Iterable[int]) -> t.Iterable[Block]:
        """
        Retrieves `Block`s from database

        Args:
            indicies (t.Iterable[int]): `list` of indicies for `Block`s on `Blockchain` to retrieve

        Returns:
            t.Iterable[Block]: The request `Block`s
        """
        pass

    @abstractmethod
    def get_chain_length(self) -> int:
        """
        Retrieves the total `Blockchain` length

        Returns:
            int: The length of the `Blockchain` in the database
        """
        pass
