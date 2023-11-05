from enum import Enum

# NEEDS COMMENTING

class PeerStateEnum(Enum):
        STARTING = 0
        SYNCHRONIZING = 1
        VALIDATING = 2
        READY = 3
        ERROR = 4

class PeerState:

    def __init__(self, intial_state:PeerStateEnum):
        self.__state = intial_state

    def get_state(self) -> PeerStateEnum:
        return self.__state.name
    
    def change_state(self, new_state:PeerStateEnum) -> None:
        self.__state = new_state

    def is_state(self, state:PeerStateEnum) -> bool:
        return self.__state is state

    def not_state(self, state:PeerStateEnum) -> bool:
        return not self.is_state(state)

    

