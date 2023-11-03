from enum import Enum

class PeerStateEnum(Enum):
        STARTING = 0
        SYNCHRONIZING = 1
        VALIDATING = 2
        READY = 3
        ERROR = 4

class PeerState:

    def __init__(self, intial_state:PeerStateEnum):
        self.state = intial_state

    def get_state(self) -> PeerStateEnum:
        return self.state.name
    
    def change_state(self, new_state:PeerStateEnum) -> None:
        self.state = new_state

    def is_state(self, state:PeerStateEnum) -> bool:
        return self.state is state

    def not_state(self, state:PeerStateEnum) -> bool:
        return not self.is_state(state)

    

