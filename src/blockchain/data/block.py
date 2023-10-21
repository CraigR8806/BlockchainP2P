from hashlib import sha256
from blockchain.database.document_entry import DocumentEntry
import jsonpickle
import json



class Block(DocumentEntry):

    def __init__(self, timestamp, data:any, index:int, previous_hash=None):
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.data = data
        self.index = index

        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return sha256(jsonpickle.encode(self).encode('utf-8')).hexdigest()