import random
from typing import List, Optional, Tuple
from src.piece import Piece, PieceColor, pieces_config_hepler


class Board:
    """
    chess board
    """

    def __init__(self) -> None:
        self.board_of_pieces: List[Piece | None] = []
        self.initailization()

    def initailization(self) -> None:
        self.board_of_pieces = []
        key_index: int = 0
        for piece_color in [PieceColor.RED, PieceColor.BLACK]:
            for key, value in pieces_config_hepler(piece_color).items():
                count = value.get("count")
                image = value.get("image")
                if count is not None and image is not None:
                    for _ in range(count):
                        self.board_of_pieces.append(
                            Piece(key_index, key, piece_color, image)
                        )
                        key_index += 1
                else:
                    print(f"Error: Missing 'count' or 'image' for {key}")
        random.shuffle(self.board_of_pieces)

    def to_index(self, row: int, col: int) -> int:
        return row * 8 + col

    def to_coordinates(self, index: int) -> Tuple[int, int]:
        row = index // 8
        col = index % 8
        return (row, col)

    def get_piece_by_coordinate(self, row: int, col: int) -> Piece | None:
        return self.board_of_pieces[self.to_index(row, col)]

    def get_board_of_pieces(self) -> List[Optional[Piece]]:
        return self.board_of_pieces
