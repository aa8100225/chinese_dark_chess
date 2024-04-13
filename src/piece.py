from enum import Enum, auto


class PieceType(Enum):
    GENERAL = auto()
    ADVISOR = auto()
    ELEPHANT = auto()
    HORSE = auto()
    CHARIOT = auto()
    CANNON = auto()
    SOLDIER = auto()


class Piece:
    def __init__(self, piece_type: PieceType, player: str):
        self.piece_type = piece_type
        self.player = player  # 'red' or 'black'
        self.covered = True  # 初始狀態，棋子是覆蓋的

    def uncover(self) -> None:
        self.covered = False

    def __repr__(self) -> str:
        return f"{self.player} {self.piece_type.name}"
