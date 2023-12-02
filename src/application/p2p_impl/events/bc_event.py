from application.p2p_impl.events.access_event import AccessEvent
from application.p2p_impl.events.delete_event import DeleteEvent
from application.p2p_impl.events.join_event import JoinEvent
from application.p2p_impl.events.modify_event import ModifyEvent
from application.p2p_impl.events.publish_event import PublishEvent
from blockchain.data.block import BlockData
from enum import Enum
import typing as t
from abc import ABC

# NEEDS COMMENTING


class BlockchainEventType(Enum):
    class __BlockchainEventTypeMeta:
        def __init__(self, index: int, clazz: t.Type):
            self.index = index
            self.clazz = clazz

    JOIN = (__BlockchainEventTypeMeta(0, JoinEvent),)
    PUBLISH = (__BlockchainEventTypeMeta(1, PublishEvent),)
    MODIFY = (__BlockchainEventTypeMeta(2, ModifyEvent),)
    DELETE = (__BlockchainEventTypeMeta(3, DeleteEvent),)
    ACCESS = __BlockchainEventTypeMeta(4, AccessEvent)


class BlockchainEvent(BlockData, ABC):
    def __init__(self, event_type: BlockchainEventType):
        self.event_type = event_type
