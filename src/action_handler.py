from enum import Enum, auto
from typing import Optional, Tuple
from src.game_state import GameState
from src.piece import Piece, PieceColor
from src.piece_action import PieceAction, PieceActionType
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
                self.action_move(position)
            case ActionType.SELECTION:
                self.action_selection(position)
            case ActionType.EATING:
                self.action_eat(position)
            case ActionType.REVEAL:
                if piece is None:
                    return
                self.action_reveal(position, piece)

    def action_eat(self, next_position: Tuple[int, int]) -> None:
        piece_action = PieceAction(
            self.game_state.selected_piece, PieceActionType.EAT, next_position
        )
        if not self.game_state.is_valid_action(piece_action):
            return
        self.game_state.implement_action(piece_action)
        self.game_state.rest_piece_of_aligment_decrease()
        self.game_state.update_actions_set()
        self.game_state.player_toggler()
        self.game_state.de_selected()
        self.game_state.reset_idle_steps()
        self.game_state.update_game_status()

    def action_move(self, next_position: Tuple[int, int]) -> None:
        piece_action = PieceAction(
            self.game_state.selected_piece, PieceActionType.MOVE, next_position
        )
        if not self.game_state.is_valid_action(piece_action):
            return
        self.game_state.implement_action(piece_action)
        self.game_state.update_actions_set()
        self.game_state.player_toggler()
        self.game_state.de_selected()
        self.game_state.idle_steps_increment()
        self.game_state.update_game_status()

    def action_reveal(self, position: Tuple[int, int], piece: Piece) -> None:
        piece_action = PieceAction(position, PieceActionType.REVEAL, position)
        if not self.game_state.is_valid_action(piece_action):
            return
        self.game_state.implement_action(piece_action)
        player_color = (
            PlayerColor.RED
            if piece.piece_color == PieceColor.RED
            else PlayerColor.BLACK
        )
        self.game_state.color_assign(player_color)
        self.game_state.player_toggler()
        self.game_state.de_selected()
        self.game_state.reset_idle_steps()
        self.game_state.update_actions_set()
        self.game_state.update_game_status()

    def action_selection(self, position: Tuple[int, int]) -> None:
        self.game_state.piece_selected(position)
