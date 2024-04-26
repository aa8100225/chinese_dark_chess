import asyncio
from enum import Enum, auto
from typing import Optional, Tuple
from src.ai.agent import Agent
from src.game_state import GameState
from src.models.piece import Piece, PieceColor
from src.models.piece_action import PieceAction, PieceActionType
from src.models.player import PlayerColor


class ActionType(Enum):
    """Player Action"""

    MOVEMENT = auto()
    SELECTION = auto()
    EATING = auto()
    REVEAL = auto()


class ActionHandler:
    def __init__(self, game_state: GameState, agent: Optional[Agent]) -> None:
        self.game_state = game_state
        self.agent = agent

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

    async def ai_action(self) -> None:
        if self.agent is None:
            return

        piece_action = self.agent.predict(self.game_state)
        if not self.game_state.is_valid_action(piece_action):
            print(
                "!!!!!!!!!!!!!!!!!!!!!!!!! Invalid Action Occurred !!!!!!!!!!!!!!!!!!!!!!!!!"
            )

        if PieceActionType.REVEAL != piece_action.piece_action_type:
            self.handle_action(piece_action.current_position, ActionType.SELECTION)

        await asyncio.sleep(0.0)
        match (piece_action.piece_action_type):
            case PieceActionType.EAT:
                action_type = ActionType.EATING
            case PieceActionType.MOVE:
                action_type = ActionType.MOVEMENT
            case PieceActionType.REVEAL:
                action_type = ActionType.REVEAL
        self.handle_action(piece_action.next_position, action_type)
