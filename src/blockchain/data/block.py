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

    def calculate_hash(self):
        return sha256(jsonpickle.encode(self).encode('utf-8')).hexdigest()
    
    def as_document(self):
        return {
            "timestamp":self.timestamp,
            "previous_hash":self.previous_hash,
            "data":self.data.as_document() if type(self.data) not in (str, int, bool) else self.data,
            "index":self.index,
            "hash":self.hash
        }
