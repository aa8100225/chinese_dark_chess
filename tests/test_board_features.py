import unittest

from src.models.board import Board
from src.models.player import PlayerColor


class TestBoardFeatures(unittest.TestCase):
    def test_board_features_perspective(self):
        board = Board()
        board.initailization()
        all_pieces_status = board.get_all_pieces_status()
        self.assertEqual(len(all_pieces_status), 32)

        reveal_positions = [2, 3, 10, 12, 17, 19, 20, 24, 25, 27, 28]
        replace_none_positions = [0, 4, 5, 9, 16, 23, 29, 31]
        for index in reveal_positions:
            piece = all_pieces_status[index]
            if piece is not None:
                piece.reveal()
        for index in replace_none_positions:
            all_pieces_status[index] = None

        red_features = board.get_board_features(PlayerColor.RED)
        black_features = board.get_board_features(PlayerColor.BLACK)

        # This checks if the features list for one color is the negative of the other,
        # considering non-empty, uncovered positions
        for red_value, black_value in zip(red_features, black_features):
            if red_value in (0, 100):  # Skip empty or covered positions
                continue
            self.assertEqual(red_value, -black_value)


if __name__ == "__main__":
    unittest.main()
