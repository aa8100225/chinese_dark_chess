from enum import Enum, auto
import random
from typing import Tuple
from src.board import Board
from src.piece import Piece, PieceColor
from src.piece_action import PieceAction
from src.piece_action_manager import PieceActionManager
from src.player import Player, PlayerColor


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
