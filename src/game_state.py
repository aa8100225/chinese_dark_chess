import copy
from enum import Enum, auto
import random
from typing import List, Tuple
from src.models.board import Board
from src.models.piece import Piece, PieceColor
from src.models.piece_action import PieceAction, PieceActionType
from src.handlers.piece_action_manager import PieceActionManager
from src.models.player import Player, PlayerColor


class GameStatus(Enum):
    ONGOING = auto()
    RED_WIN = auto()
    BLACK_WIN = auto()
    DRAW = auto()


class GameState:
    def __init__(self) -> None:
        self.game_status = GameStatus.ONGOING
        self.board = Board()
        self.piece_action_manager = PieceActionManager(self.board)
        self.idle_steps = 0
        self.players = [Player("Player 1"), Player("Player 2")]
        self.current_player_index = random.choice([0, 1])
        self.is_color_assign = False
        self.selected_piece: Tuple[int, int] = (-1, -1)
        self.rest_piece_of_red_aligment_player = 16
        self.rest_piece_of_black_aligment_player = 16

    def get_piece_by_coordinate(self, row: int, col: int) -> Piece | None:
        return self.board.get_piece_by_coordinate(row, col)

    def color_assign(self, color: PlayerColor) -> None:
        if self.is_color_assign:
            return
        self.players[self.current_player_index].assign_color(color)
        next_player_index = (self.current_player_index + 1) % 2
        self.players[next_player_index].assign_color(color.get_opposite_color())
        self.is_color_assign = True

    def get_current_player(self) -> Player:
        return self.players[self.current_player_index]

    def reset_game(self) -> None:
        self.game_status = GameStatus.ONGOING
        self.board.initailization()
        self.reset_idle_steps()
        self.current_player_index = random.choice([0, 1])
        self.is_color_assign = False
        self.selected_piece = (-1, -1)
        self.piece_action_manager = PieceActionManager(self.board)
        self.rest_piece_of_black_aligment_player = 16
        self.rest_piece_of_red_aligment_player = 16

    def is_piece_selected(self) -> bool:
        return (-1, -1) != self.selected_piece

    def de_selected(self) -> None:
        self.selected_piece = (-1, -1)

    def piece_selected(self, position: Tuple[int, int]) -> None:
        self.selected_piece = position

    def player_toggler(self) -> None:
        self.current_player_index = (self.current_player_index + 1) % 2

    def is_ally_selected(self, piece: Piece) -> bool:
        return (
            PieceColor.RED == piece.piece_color
            if self.get_current_player().color == PlayerColor.RED
            else PieceColor.BLACK == piece.piece_color
        )

    def reset_idle_steps(self) -> None:
        self.idle_steps = 0

    def idle_steps_increment(self) -> None:
        self.idle_steps += 1

    def is_valid_action(self, piece_action: PieceAction) -> bool:
        return self.piece_action_manager.is_valid_action(
            piece_action, self.get_current_player().color
        )

    def implement_action(self, piece_action: PieceAction) -> None:
        self.piece_action_manager.implement_action(piece_action)

    def next_state(self, piece_action: PieceAction) -> "GameState":
        """AI"""
        self.implement_action(piece_action)
        piece = self.board.get_piece_by_coordinate(
            piece_action.current_position[0], piece_action.current_position[1]
        )
        if piece_action.piece_action_type == PieceActionType.EAT:
            self.rest_piece_of_aligment_decrease()
        if (
            piece_action.piece_action_type == PieceActionType.REVEAL
            and piece is not None
        ):
            player_color = (
                PlayerColor.RED
                if piece.piece_color == PieceColor.RED
                else PlayerColor.BLACK
            )
            self.color_assign(player_color)

        self.update_actions_set()
        self.player_toggler()
        self.de_selected()
        if piece_action.piece_action_type in (
            PieceActionType.EAT,
            PieceActionType.REVEAL,
        ):
            self.reset_idle_steps()
        else:
            self.idle_steps_increment()

        self.update_game_status()
        return self

    def update_actions_set(self) -> None:
        self.piece_action_manager.update_action_set()

    def rest_piece_of_aligment_decrease(self) -> None:
        match (self.get_current_player().color):
            case PlayerColor.RED:
                self.rest_piece_of_black_aligment_player -= 1
            case PlayerColor.BLACK:
                self.rest_piece_of_red_aligment_player -= 1

    def update_game_status(self) -> None:
        if self.idle_steps >= 17:
            self.game_status = GameStatus.DRAW
            return
        if (
            self.rest_piece_of_red_aligment_player <= 0
            or not self.piece_action_manager.player_has_any_valid_action(
                PlayerColor.RED
            )
        ):
            self.game_status = GameStatus.BLACK_WIN
        elif (
            self.rest_piece_of_black_aligment_player <= 0
            or not self.piece_action_manager.player_has_any_valid_action(
                PlayerColor.BLACK
            )
        ):
            self.game_status = GameStatus.RED_WIN
        else:
            self.game_status = GameStatus.ONGOING

    def get_board_features(self) -> List[int]:
        return self.board.get_board_features(self.get_current_player().color)

    def get_legal_actions(self) -> List[int]:
        return self.piece_action_manager.get_legal_actions(
            self.get_current_player().color
        )

    def generate_action_by_index(self, index: int) -> PieceAction:
        return self.piece_action_manager.decode_action_index(index)

    def get_value_and_terminated(self) -> Tuple[int, bool]:
        match (self.game_status):
            case GameStatus.ONGOING:
                return (0, False)
            case GameStatus.DRAW:
                return (0, True)
        return (1, True)

    def __deepcopy__(self, memo):
        # 使用__new__避免調用__init__方法
        new_game_state = type(self).__new__(self.__class__)
        memo[id(self)] = new_game_state

        new_game_state.board = copy.deepcopy(self.board, memo)
        new_game_state.piece_action_manager = PieceActionManager(new_game_state.board)

        new_game_state.game_status = self.game_status
        new_game_state.idle_steps = self.idle_steps
        new_game_state.current_player_index = self.current_player_index
        new_game_state.is_color_assign = self.is_color_assign
        new_game_state.selected_piece = self.selected_piece
        new_game_state.rest_piece_of_red_aligment_player = (
            self.rest_piece_of_red_aligment_player
        )
        new_game_state.rest_piece_of_black_aligment_player = (
            self.rest_piece_of_black_aligment_player
        )

        new_game_state.players = [Player("Player 1"), Player("Player 2")]
        if self.players[0].color is not None:
            new_game_state.players[0].assign_color(self.players[0].color)
        if self.players[1].color is not None:
            new_game_state.players[1].assign_color(self.players[1].color)

        return new_game_state
