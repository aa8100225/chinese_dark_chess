from enum import Enum, auto
from typing import Tuple


class PieceActionType(Enum):
    """Piece Action"""

    MOVE = auto()
    EAT = auto()
    REVEAL = auto()


class PieceAction:
    def __init__(
        self,
        current_position: Tuple[int, int],
        piece_action_type: PieceActionType,
        next_position: Tuple[int, int],
    ) -> None:
        self.current_position = current_position
        self.piece_action_type = piece_action_type
        self.next_position = next_position

    def generate_hash_key(self) -> str:
        return f"{self.current_position}-{self.piece_action_type.name}-{self.next_position}"
