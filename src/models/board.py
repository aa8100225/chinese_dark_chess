import copy
import random
from typing import List, Optional, Tuple
from src.models.piece import Piece, PieceColor
from src.models.player import PlayerColor


class Board:
    """
    Represents a chess board, managing the placement and state of pieces.
    This includes initialization of pieces, shuffling for game start,
    and utilities for piece location and feature extraction based on game rules.
    """

    def __init__(self) -> None:
        # using 1D array store 4*8 pieces of board grids
        self.pieces: List[Optional[Piece]] = []
        self.initailization()

    def initailization(self) -> None:
        self.pieces = []
        key_index: int = 0
        for piece_color in [PieceColor.RED, PieceColor.BLACK]:
            for piece_type, count in Piece.piece_counts.items():
                for _ in range(count):
                    self.pieces.append(Piece(key_index, piece_type, piece_color))
                    key_index += 1

        random.shuffle(self.pieces)

    def to_index(self, row: int, col: int) -> int:
        return row * 8 + col

    def to_coordinates(self, index: int) -> Tuple[int, int]:
        row = index // 8
        col = index % 8
        return (row, col)

    def get_piece_by_coordinate(self, row: int, col: int) -> Piece | None:
        return self.pieces[self.to_index(row, col)]

    def get_all_pieces_status(self) -> List[Optional[Piece]]:
        """
        Retrieves the status of all board positions, returning a list of Pieces or None.
        This includes both occupied and unoccupied positions on the chessboard.
        """
        return self.pieces
