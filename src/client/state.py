from enum import Enum, auto

class State(Enum):
    """ States to manage client """
    Connected = auto()
    Signed = auto()
    Disconnected = auto()

    def __str__(self) -> str:
        return f'state: {self.name}'

