from blockchain.data.block import Block, BlockData



# NEEDS COMMENTING


class BlockCandidate:
    def __init__(self, block_data: BlockData = None):
        self.block_data = block_data
        self.processed = False

    def process(self, index: int, previous_hash: str) -> Block:
        block = Block(self.block_data, index=index, previous_hash=previous_hash)
        self.processed = True
        return block

    def revert(self) -> None:
        self.processed = False

    def is_processed(self) -> bool:
        return self.processed

    def __eq__(self, other: "BlockCandidate"):
        return hash(self) == hash(other)

    def __ne__(self, other: "BlockCandidate"):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.block_data)
