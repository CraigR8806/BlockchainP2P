from application.p2p_impl.events.bc_event import BlockchainEvent, BlockchainEventType


class PublishEvent(BlockchainEvent):
    def __init__(self, data: any):
        super().__init__(BlockchainEventType.PUBLISH)
        self.data = data
        pass
