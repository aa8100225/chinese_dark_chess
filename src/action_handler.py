from enum import Enum, auto
from typing import Optional, Tuple
from src.game_state import GameState
from src.piece import Piece, PieceColor
from src.player import PlayerColor


class ActionType(Enum):
    MOVEMENT = auto()
    SELECTION = auto()
    EATING = auto()
    REVEAL = auto()


class ActionHandler:
    def __init__(self, game_state: GameState) -> None:
        self.game_state = game_state

    def handle_action(
        self, position: Tuple[int, int], action_type: Optional[ActionType]
    ) -> None:
        piece: Optional[Piece] = (
            None
            if action_type is None
            else self.game_state.get_piece_by_coordinate(position[0], position[1])
        )
        match action_type:
            case ActionType.MOVEMENT:
                pass
            case ActionType.SELECTION:
                pass
            case ActionType.EATING:
                pass
            case ActionType.REVEAL:
                if piece is None:
                    return
                self.action_reveal(piece)

    def action_reveal(self, piece: Piece) -> None:
        piece.reveal()
        player_color = (
            PlayerColor.RED
            if piece.piece_color == PieceColor.RED
            else PlayerColor.BLACK
        )
        self.game_state.color_assign(player_color)
        self.game_state.player_toggler()
        self.game_state.de_selected()
