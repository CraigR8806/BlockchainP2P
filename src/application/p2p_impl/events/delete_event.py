from application.p2p_impl.events.bc_event import BlockchainEvent, BlockchainEventType


class DeleteEvent(BlockchainEvent):
    def __init__(self, data: any):
        super().__init__(BlockchainEventType.DELETE)
        self.data = data
        pass

