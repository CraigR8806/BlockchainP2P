from application.p2p_impl.events.bc_event import BlockchainEvent, BlockchainEventType


class ModifyEvent(BlockchainEvent):
    def __init__(self, data: any):
        super().__init__(BlockchainEventType.MODIFY)
        self.data = data
        pass
