import random
from typing import Tuple
from src.board import Board
from src.piece import Piece
from src.player import Player, PlayerColor


class GameState:
    def __init__(self) -> None:
        self.pause = False
        self.end_game = False
        self.board = Board()
        self.idle_steps = 0
        self.players = [Player("Player 1"), Player("Player 2")]
        self.current_player_index = random.choice([0, 1])
        self.is_color_assign = False
        self.selected_piece: Tuple[int, int] = (-1, -1)

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
        # print("Reset Game")
        self.pause = False
        self.end_game = False
        self.board.initailization()
        self.idle_steps = 0
        self.current_player_index = random.choice([0, 1])
        self.is_color_assign = False
        self.selected_piece = (-1, -1)

    def is_piece_selected(self) -> bool:
        return (-1, -1) != self.selected_piece

    def de_selected(self) -> None:
        self.selected_piece = (-1, -1)

    def player_toggler(self) -> None:
        self.current_player_index = (self.current_player_index + 1) % 2
