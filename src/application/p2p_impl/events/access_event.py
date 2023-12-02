from application.p2p_impl.events.bc_event import BlockchainEvent, BlockchainEventType


class AccessEvent(BlockchainEvent):
    def __init__(self, data: any):
        super().__init__(BlockchainEventType.ACCESS)
        self.data = data
        pass
