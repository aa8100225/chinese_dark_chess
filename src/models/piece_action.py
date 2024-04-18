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

    def to_action_index(self) -> int:
        start = self.coordiante_to_index_of_board(self.current_position)
        end = self.coordiante_to_index_of_board(self.next_position)
        base_index = start * 65

        match (self.piece_action_type):
            case PieceActionType.MOVE:
                offset = end
            case PieceActionType.EAT:
                offset = 32 + end
            case PieceActionType.REVEAL:
                offset = 64

        return base_index + offset

    def coordiante_to_index_of_board(self, position: Tuple[int, int]) -> int:
        return position[0] * 8 + position[1]
