from typing import Optional, Tuple
from src.action_handler import ActionType
from src.game_state import GameState


class ActionDetector:
    def __init__(self, game_state: GameState) -> None:
        self.game_state = game_state

    def detect_action(self, position: Tuple[int, int]) -> Optional[ActionType]:
        piece = self.game_state.get_piece_by_coordinate(position[0], position[1])
        if piece is not None and piece.covered:
            return ActionType.REVEAL
        if self.game_state.is_piece_selected() and piece is None:
            return ActionType.MOVEMENT
        if self.game_state.is_piece_selected() and piece is not None:
            if self.game_state.is_ally_selected(piece):
                return ActionType.SELECTION
            return ActionType.EATING
        if piece is not None and self.game_state.is_ally_selected(piece):
            return ActionType.SELECTION
        return None
