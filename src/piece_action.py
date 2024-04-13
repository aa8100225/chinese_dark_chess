from enum import Enum, auto


class ActionType(Enum):
    MOVE = auto()
    EAT = auto()
    REVEAL = auto()


class PieceAction:
    def __init__(self) -> None:
        pass
