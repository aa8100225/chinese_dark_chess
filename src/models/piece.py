from enum import Enum, auto


class PieceType(Enum):
    """
    Enumeration for piece types.
    The order of types is critical as it determines their relative strength.
    """

    GENERAL = auto()  # 將/帥
    ADVISOR = auto()  # 士/仕
    ELEPHANT = auto()  # 象/相
    CHARIOT = auto()  # 車/俥
    HORSE = auto()  # 馬/傌
    CANNON = auto()  # 砲/炮
    SOLDIER = auto()  # 卒/兵

    def can_defeat(self, enemy: "PieceType") -> bool:
        """Determines if a piece can defeat another piece based on game rules."""
        result = False
        match self:
            case PieceType.GENERAL:
                result = (
                    PieceType.GENERAL.value <= enemy.value < PieceType.SOLDIER.value
                )
            case PieceType.ADVISOR:
                result = enemy.value >= PieceType.ADVISOR.value
            case PieceType.ELEPHANT:
                result = enemy.value >= PieceType.ELEPHANT.value
            case PieceType.CHARIOT:
                result = enemy.value >= PieceType.CHARIOT.value
            case PieceType.HORSE:
                result = enemy.value >= PieceType.HORSE.value
            case PieceType.SOLDIER:
                result = enemy in {PieceType.SOLDIER, PieceType.GENERAL}
            case PieceType.CANNON:
                result = True
        return result


class PieceColor(Enum):
    RED = auto()
    BLACK = auto()

    def opposite_color(self) -> "PieceColor":
        return PieceColor.BLACK if self == PieceColor.RED else PieceColor.RED


class Piece:
    """
    Represents a chess piece, including its type, color, and current state (covered or revealed).
    """

    # Number of each type of piece on each side.
    piece_counts = {
        PieceType.GENERAL: 1,
        PieceType.ADVISOR: 2,
        PieceType.ELEPHANT: 2,
        PieceType.CHARIOT: 2,
        PieceType.HORSE: 2,
        PieceType.CANNON: 2,
        PieceType.SOLDIER: 5,
    }

    def __init__(
        self,
        key: int,
        piece_type: PieceType,
        piece_color: PieceColor,
    ):
        self.key = key
        self.piece_type = piece_type
        self.piece_color = piece_color
        self.covered = True

    def reveal(self) -> None:
        self.covered = False

    def __repr__(self) -> str:
        return f"{self.piece_color} {self.piece_type.name}"
