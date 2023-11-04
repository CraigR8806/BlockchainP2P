from hashlib import sha256
from blockchain.database.document_entry import DocumentEntry
import jsonpickle

class Block(DocumentEntry):

    def __init__(self, timestamp, data:any, index:int, previous_hash=None):
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.data = data
        self.index = index

        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        return sha256(jsonpickle.encode(self).encode('utf-8')).hexdigest()
    
    def copy_of(self) -> 'Block':
        out = Block(self.timestamp, self.data, self.index, self.previous_hash)
        out.hash = self.hash
        return out