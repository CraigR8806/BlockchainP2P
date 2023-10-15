from blockchain.data.block import Block


class BlockCandidate:

    def __init__(self, block:Block):
        self.block = block
        self.processed = False
