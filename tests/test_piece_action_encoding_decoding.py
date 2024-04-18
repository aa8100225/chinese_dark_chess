import unittest
from src.models.board import Board
from src.models.piece_action import PieceActionType, PieceAction
from src.handlers.piece_action_manager import PieceActionManager


class TestPieceActionEncodingDecoding(unittest.TestCase):
    def setUp(self):
        self.piece_action_manager = PieceActionManager(Board())
        self.all_possible_actions = []

        for action_type in (
            PieceActionType.EAT,
            PieceActionType.MOVE,
            PieceActionType.REVEAL,
        ):
            for i in range(4):
                for j in range(8):
                    if action_type in (PieceActionType.EAT, PieceActionType.MOVE):
                        self.all_possible_actions.extend(
                            [
                                PieceAction((i, j), action_type, (k, l))
                                for k in range(4)
                                for l in range(8)
                            ]
                        )
                    elif action_type == PieceActionType.REVEAL:
                        self.all_possible_actions.append(
                            PieceAction((i, j), action_type, (i, j))
                        )

    def test_unique_encoding(self):
        encoded_indices = [
            action.to_action_index() for action in self.all_possible_actions
        ]
        unique_indices = set(encoded_indices)
        self.assertEqual(
            len(encoded_indices),
            len(unique_indices),
            "There should be no duplicate indices.",
        )

    def test_encoding_decoding_match(self):
        for index in range(2080):
            decoded_action = self.piece_action_manager.decode_action_index(index)
            re_encoded_index = decoded_action.to_action_index()
            self.assertEqual(index, re_encoded_index, f"Mismatch at index {index}")

    def test_max_index_value(self):
        max_index = max(
            [action.to_action_index() for action in self.all_possible_actions]
        )
        self.assertEqual(
            max_index, 2079, "The maximum index should be 2079 for 2080 total actions."
        )


if __name__ == "__main__":
    unittest.main()
