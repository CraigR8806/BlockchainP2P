from application.p2p_impl.events.bc_event import BlockchainEvent, BlockchainEventType


class JoinEvent(BlockchainEvent):
    def __init__(self, data: any):
        super().__init__(BlockchainEventType.JOIN)
        self.data = data
        pass
