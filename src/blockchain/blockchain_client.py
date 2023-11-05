from p2p.client.client import Client
from p2p.connection import Connection
from p2p.dataservice import DataService
from blockchain.data.blockchain import Blockchain
from blockchain.peerstate import PeerStateEnum
import shared.util as util
import typing as t

# NEEDS COMMENTING

class BlockchainClient:


    def __init__(self, client:Client, chain:Blockchain, data_service:DataService):
        self.__client = client
        self.__chain = chain
        self.__data_service = data_service

    def synchronize_chain(self, bootstrap_connection: Connection) -> None:
        start = self.__chain.chain_length()
        end = util.extract_data(self.__client.get_one(bootstrap_connection, "/chain/length").text)

        if start < end:
            blocks = util.extract_data(self.__client.get_one(bootstrap_connection, "/chain/blocks", {"start":str(start), "end":str(end)}).text)

            self.__chain.commit_blocks(blocks)

        self.__data_service.modify("state", lambda v:v.change_state(PeerStateEnum.VALIDATING))

        if not self.__chain.is_chain_valid():
            self.__data_service.modify("state", lambda v:v.change_state(PeerStateEnum.ERROR))
            

        

    


    