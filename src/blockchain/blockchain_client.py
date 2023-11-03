from p2p.client.client import Client
from p2p.connection import Connection
from blockchain.data.block import Block
from blockchain.data.blockchain import Blockchain
import shared.util as util
import typing as t

class BlockchainClient:


    def __init__(self, client:Client, chain:Blockchain):
        self.client = client
        self.chain = chain

    def synchronize_chain(self, bootstrap_connection: Connection) -> None:
        start = self.chain.chain_length()
        end = util.extract_data(self.client.get_one(bootstrap_connection, "/chain/length").text)

        if start < end:
            blocks = util.extract_data(self.client.get_one(bootstrap_connection, "/chain/blocks", {"start":str(start), "end":str(end)}).text)

            self.chain.commit_blocks(blocks)

    


    