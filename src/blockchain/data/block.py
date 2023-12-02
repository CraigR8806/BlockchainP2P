from blockchain.database.document_entry import DocumentEntry
from time import time
from abc import ABC
from hashlib import sha256
import typing as t
import jsonpickle

# NEEDS COMMENTING


class BlockData(ABC):
    def __init__(self, data: t.Any):
        self.data = data

    def __eq__(self, other: "BlockData"):
        return hash(self) == hash(other)

    def __ne__(self, other: "BlockData"):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.data)


class Block(DocumentEntry):
    def __init__(
        self,
        block_data: BlockData,
        timestamp: float = False,
        index: int = -1,
        previous_hash=None,
    ):
        self.data = block_data
        self.timestamp = timestamp or time()
        self.previous_hash = previous_hash
        self.index = index

        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        return sha256(self.__data_for_hash().encode("utf-8")).hexdigest()

    def copy_of(self) -> "Block":
        out = Block(self.timestamp, self.data, self.index, self.previous_hash)
        out.hash = self.hash
        return out

    def __data_for_hash(self) -> str:
        return (
            jsonpickle.encode(self.data)
            + jsonpickle.encode(self.index)
            + jsonpickle.encode(self.previous_hash)
        )

    def __eq__(self, other: "Block"):
        return hash(self) == hash(other)

    def __ne__(self, other: "Block"):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.calculate_hash())
