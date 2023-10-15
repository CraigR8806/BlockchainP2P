from hashlib import sha256
import jsonpickle



class Block:

    def __init__(self, timestamp, data:any, previous_hash=None):
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.data = data

        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return sha256(jsonpickle.encode(self).encode('utf-8')).hexdigest()
