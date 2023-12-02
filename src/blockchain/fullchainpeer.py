from p2p.peer.thispeer import ThisPeer
from p2p.peer.peer import Peer
from p2p.connection import Connection
from blockchain.diagnostics.diagnostics import Diagnostics
from shared.pki.pki import PKI
from blockchain.data.blockchain import Blockchain
from blockchain.peerstate import PeerState, PeerStateEnum
from blockchain.blockchain_client import BlockchainClient
from blockchain.blockchain_server import BlockchainServer
from time import sleep
import threading
import typing as t


# NEEDS COMMENTING


class FullChainPeer(ThisPeer):
    VOTE_FACTOR = 0.51

    def __init__(
        self,
        name: str,
        connection: Connection,
        database_connection: Connection,
        database_name: str,
        collection: str,
        diagnostics: bool = None,
        pki: PKI = None,
        is_bootstrap_node: bool = True,
    ):
        super().__init__(name, connection, is_bootstrap_node, pki)
        self.__state = "state"
        self.__vote_map = "vote_map"
        self.__vote_map_buffer = "vote_map_buffer"
        self._data_service.upsert(
            self.__state, PeerState(PeerStateEnum.STARTING), asyync=True
        )
        self.__chain = Blockchain(
            database_connection,
            self._data_service,
            database_name,
            collection,
            self._is_bootstrap_node,
        )
        self.__chain_client = BlockchainClient(
            self.as_peer(), self._client, self.__chain, self._data_service
        )
        self.__chain_server = BlockchainServer(
            self._server, self.__chain, self._data_service, self.__chain_client
        )
        self.__pool_processing_thread = threading.Thread(target=self.__pool_processing)
        self.__vote_checking_thread = threading.Thread(target=self.__checking_vote)
        self._data_service.upsert(self.__vote_map, {})
        self._data_service.upsert(self.__vote_map_buffer, {})
        self.__request_last_commited = -1

        if diagnostics:
            self.__diagnostics = Diagnostics(
                self._server, self.__chain, self._data_service
            )

    def start_node(self) -> bool:
        if super().start_node():
            self.__pool_processing_thread.start()
            self.__vote_checking_thread.start()

    def stop_node(self) -> None:
        super().stop_node()
        self.__pool_processing_thread.join(10)
        self.__vote_checking_thread.join(10)

    def __pool_processing(self) -> None:
        while self._running:
            sleep(1)

            votes = self._data_service.deep_copy(self.__vote_map)
            buffer = self._data_service.deep_copy(self.__vote_map_buffer)
            if self._data_service.deep_copy(self.__state).not_state(
                PeerStateEnum.WAITING_FOR_VOTES
            ):
                block = self.__chain.process_pool()
                if block is not None:
                    self.__chain_client.vote_new_block(block)
                    self._data_service.modify(
                        self.__state,
                        lambda v: v.change_state(PeerStateEnum.WAITING_FOR_VOTES),
                    )

    def __active_peer_watcher(self) -> None:
        active_peers = self._data_service.deep_copy(self._active_peers)
        vote_map = self._data_service.deep_copy(self.__vote_map)
        vote_map_additions = {}
        for peer in active_peers:
            if peer not in vote_map:
                vote_map_additions.update({peer: 0})

        self._data_service.modify(
            self.__vote_map, lambda v: v.update(vote_map_additions)
        )
        self._data_service.modify(
            self.__vote_map_buffer, lambda v: v.update(vote_map_additions)
        )
        for peer in vote_map.keys():
            if peer not in active_peers:
                self._data_service.modify(self.__vote_map, lambda v: v.remove(peer))
                self._data_service.modify(
                    self.__vote_map_buffer, lambda v: v.remove(peer)
                )

    def __checking_vote(self) -> None:
        self.__active_peers_watch_uuid = self._data_service.watch(
            self._active_peers, self.__active_peer_watcher
        )
        while self._running:
            sleep(1)
            if self.__request_last_commited >= 0:
                if self.__request_last_commited > 2:
                    block = self.__chain_client.request_last_committed(
                        self.__peers_to_ask[0]
                    )
                    self.__chain.commit_block(block)
                    self.__voting_round_complete()
                else:
                    self.__request_last_commited += 1

            elif self._data_service.deep_copy(self.__state).is_state(
                PeerStateEnum.WAITING_FOR_VOTES
            ):
                vote_map = self._data_service.deep_copy(self.__vote_map)
                hash_votes = {}
                votes_cast = 0
                for vote in vote_map.values():
                    if vote != 0:
                        votes_cast += 1
                        hash_votes[vote] = hash_votes.get(vote, 0) + 1

                if votes_cast < len(vote_map.items()):
                    continue

                new_block_hash = None
                vote_limit = int(len(vote_map.items()) * FullChainPeer.VOTE_FACTOR)
                for hashh, tally in hash_votes.items():
                    if tally >= vote_limit:
                        new_block_hash = hashh
                        break

                if new_block_hash is not None:
                    if self.__chain.does_match_candidate(new_block_hash):
                        self.__chain.candidate_approved()
                    else:
                        self.__peers_to_ask = [
                            peer
                            for peer, vote in vote_map.items()
                            if vote == new_block_hash
                        ]
                        self.__request_last_commited = 0

                self.__voting_round_complete()

    def __clear_vote(self, vm):
        for peer in vm.keys():
            vm[peer] = 0

    def __voting_round_complete(self):
        self._data_service.modify(
            self.__state, lambda v: v.change_state(PeerStateEnum.READY)
        )
        self._data_service.modify(self.__vote_map, self.__clear_vote)
        vote_map_buffer = self._data_service.deep_copy(self.__vote_map_buffer)

        for peer, vote in vote_map_buffer.items():
            if vote != 0:
                self._data_service.modify(
                    self.__vote_map, lambda v: v.update({peer: vote})
                )

        self._data_service.modify(self.__vote_map_buffer, self.__clear_vote)
        self.__request_last_commited = -1

    def synchronize_chain(
        self,
        bootstrap_connection: Connection,
        post_sync_state: PeerStateEnum = PeerStateEnum.READY,
    ) -> None:
        self._data_service.modify(
            self.__state, lambda v: v.change_state(PeerStateEnum.SYNCHRONIZING)
        )
        self.__chain_client.synchronize_chain(bootstrap_connection)
        self._data_service.modify(
            self.__state, lambda v: v.change_state(post_sync_state)
        )

    def validate_chain(
        self, post_validate_state: PeerStateEnum = PeerStateEnum.READY
    ) -> bool:
        self._data_service.modify(
            self.__state, lambda v: v.change_state(PeerStateEnum.VALIDATING)
        )
        is_chain_valid = self.__chain.is_chain_valid()
        self._data_service.modify(
            self.__state, lambda v: v.change_state(post_validate_state)
        )
        return is_chain_valid
