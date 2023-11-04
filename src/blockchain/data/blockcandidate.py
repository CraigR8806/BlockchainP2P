from blockchain.data.block import Block


class BlockCandidate:

    def __init__(self, block:Block = None):
        self.block = block
        self.processed = False


    def update(self, block:Block, processed:bool) -> 'BlockCandidate':
        self.block = block
        self.processed = processed
        return self

    def is_processed(self) -> bool:
        return self.processed
    
    def cadidate(self) -> Block:
        return self.block