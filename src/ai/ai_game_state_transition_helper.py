from typing import List, Optional, Tuple
import numpy as np
from src.ai.piece_action_code import PIECE_ACTION_DECODE_ACTION, PIECE_ACTION_ENCODE
from src.game_state import GameState
from src.models.piece import PieceColor
from src.models.player import PlayerColor


class AIGameStateTransitionHelper:

    def __init__(self) -> None:
        self.row_count = 4
        self.column_count = 8
        self.action_size = 456

    def to_coordinates(self, index: int) -> Tuple[int, int]:
        row = index // 8
        col = index % 8
        return (row, col)

    def get_initial_state(self, game_state: GameState) -> np.ndarray:
        state = np.zeros((3, 4, 8)).astype(int)
        for index, piece in enumerate(game_state.board.get_all_pieces_status()):
            row, col = self.to_coordinates(index)
            if piece is None:
                state[0][row][col] = 0
                state[1][row][col] = 0
            else:
                state[0][row][col] = 100 if piece.covered else piece.piece_type.value
                state[1][row][col] = (piece.piece_type.value) + (
                    10 if piece.piece_color == PieceColor.RED else 20
                )
        current_player = game_state.get_current_player()
        current_player_index = game_state.current_player_index
        # current player
        state[2][0][0] = 1 if current_player_index == 0 else 2
        turn = state[2][0][0]
        next_turn = self.get_enemy_player_index(turn)
        # current player color
        state[2][0][turn] = (
            0
            if current_player.color is None
            else (1 if current_player.color == PlayerColor.RED else 2)
        )
        # next player color
        state[2][0][next_turn] = (
            0
            if current_player.color is None
            else (2 if current_player.color == PlayerColor.RED else 1)
        )
        # rest pieces number of current player
        state[2][0][3 if turn == 1 else 4] = (
            16
            if current_player.color is None
            else (
                game_state.rest_piece_of_red_aligment_player
                if current_player.color == PlayerColor.RED
                else game_state.rest_piece_of_black_aligment_player
            )
        )
        # rest pieces number of next player
        state[2][0][3 if next_turn == 1 else 4] = (
            16
            if current_player.color is None
            else (
                game_state.rest_piece_of_black_aligment_player
                if current_player.color == PlayerColor.RED
                else game_state.rest_piece_of_red_aligment_player
            )
        )
        state[2][0][5] = game_state.idle_steps
        return state

    def get_enemy_player_index(self, index: int) -> int:
        if index == 1:
            return 2
        return 1

    def get_enemy_player_color(self, index: int) -> int:
        if index == 0:
            return 0  # not assign color
        if index == 1:
            return 2
        return 1

    def get_next_state(self, state: np.ndarray, action: int) -> np.ndarray:
        action_decode = PIECE_ACTION_DECODE_ACTION[action]
        if action_decode[1] == 0:  # reveal
            row, col = action_decode[0]
            state[0][row][col] = state[1][row][col] % 10
            state[2][0][5] = 0
            if state[2][0][1] == 0:  # assing color
                current_player = state[2][0][0]
                opisite_player = self.get_enemy_player_color(state[2][0][0])
                state[2][0][current_player] = state[1][row][col] / 10
                state[2][0][opisite_player] = self.get_enemy_player_color(
                    state[2][0][current_player]
                )
        elif action_decode[1] == 1:  # move
            row1, col1 = action_decode[0]
            row2, col2 = action_decode[2]
            state[0][row1][col1], state[0][row2][col2] = (
                state[0][row2][col2],
                state[0][row1][col1],
            )
            state[1][row1][col1], state[1][row2][col2] = (
                state[1][row2][col2],
                state[1][row1][col1],
            )
            state[2][0][5] += 1
        elif action_decode[1] == 2:  # eat
            row1, col1 = action_decode[0]
            row2, col2 = action_decode[2]
            state[0][row1][col1], state[0][row2][col2] = 0, state[0][row1][col1]
            state[1][row1][col1], state[1][row2][col2] = 0, state[1][row1][col1]
            state[2][0][5] = 0
            current_player = state[2][0][0]
            if current_player == 1:
                state[2][0][4] -= 1
            else:
                state[2][0][3] -= 1
        return state

    def get_valid_moves(self, state: np.ndarray) -> np.ndarray:
        action_mask = np.zeros(456, dtype=np.uint8)
        action_mask[self.calculate_valid_action(state, state[2][0][0])] = 1
        return action_mask

    def calculate_valid_action(self, state: np.ndarray, player: int) -> List[int]:
        color = state[2][0][player]
        actions = []
        for row in range(4):
            for col in range(8):
                if state[0][row][col] == 0:
                    continue
                if state[0][row][col] == 100:  # covered
                    actions.append(
                        PIECE_ACTION_ENCODE[f"({row},{col})-REVEAL-({row},{col})"]
                    )
                elif state[1][row][col] // 10 == color:
                    actions.extend(self.generate_move_action(state, row, col))
                    actions.extend(self.generate_eat_action(state, player, row, col))
        return actions

    def generate_move_action(self, state: np.ndarray, row: int, col: int) -> List[int]:
        dirs = [-1, 0, 1, 0, -1]
        actions = []
        for i in range(4):
            next_x = row + dirs[i]
            next_y = col + dirs[i + 1]
            if (
                next_x < 0
                or next_x >= 4
                or next_y < 0
                or next_y >= 8
                or state[0][next_x][next_y] != 0
            ):
                continue
            actions.append(
                PIECE_ACTION_ENCODE[f"({row},{col})-MOVE-({next_x},{next_y})"]
            )
        return actions

    def generate_eat_action(
        self, state: np.ndarray, player: int, row: int, col: int
    ) -> List[int]:
        actions = []
        if state[0][row][col] == 6:
            for next_x, next_y in self.generate_cannon_potential_attack_positions(
                state, row, col
            ):
                enemy_piece1 = state[0][next_x][next_y]
                enemy_piece2 = state[1][next_x][next_y]

                if enemy_piece1 == 100 or (enemy_piece2 // 10) == state[2][0][player]:
                    continue
                actions.append(
                    PIECE_ACTION_ENCODE[f"({row},{col})-EAT-({next_x},{next_y})"]
                )
            return actions
        dirs = [-1, 0, 1, 0, -1]
        for i in range(4):
            next_x = row + dirs[i]
            next_y = col + dirs[i + 1]
            if next_x < 0 or next_x >= 4 or next_y < 0 or next_y >= 8:
                continue
            enemy_piece1 = state[0][next_x][next_y]
            enemy_piece2 = state[1][next_x][next_y]
            if (
                enemy_piece1 != 0
                and enemy_piece1 != 100
                and (enemy_piece2 // 10) != state[2][0][player]
                and self.can_defeat(state[0][row][col], enemy_piece1)
            ):
                actions.append(
                    PIECE_ACTION_ENCODE[f"({row},{col})-EAT-({next_x},{next_y})"]
                )
        return actions

    def can_defeat(self, mine: int, enemy: int) -> bool:
        match (mine):
            case 1:
                return mine <= enemy < 7
            case 2 | 3 | 4 | 5:
                return mine <= enemy
            case 7:
                return enemy in (7, 1)
        return False

    def generate_cannon_potential_attack_positions(
        self, state: np.ndarray, row: int, col: int
    ):
        potential_targets: List[Tuple[int, int]] = []
        dirs = [-1, 0, 1, 0, -1]

        for i in range(4):
            jump_over = False
            current_x, current_y = row, col
            while True:
                current_x += dirs[i]
                current_y += dirs[i + 1]
                if not (0 <= current_x < 4 and 0 <= current_y < 8):
                    break
                next_piece = state[0][current_x][current_y]
                if next_piece == 0:
                    continue
                if not jump_over:
                    jump_over = True
                else:
                    potential_targets.append((current_x, current_y))
                    break
        return potential_targets

    def check_win(
        self, state: np.ndarray, action: Optional[int], current: bool = False
    ):
        if action is None:
            return False
        check_player = (
            state[2][0][0] if current else self.get_enemy_player_index(state[2][0][0])
        )
        check_player_has_piece_amount = (
            state[2][0][3] if check_player == 1 else state[2][0][4]
        )
        return (
            check_player_has_piece_amount == 0
            or len(self.calculate_valid_action(state, check_player)) == 0
        )

    def get_value_and_terminated(
        self, state: np.ndarray, action: Optional[int], current: bool = False
    ) -> Tuple[int, bool]:
        if self.check_win(state, action, current):
            return abs(state[2][0][3] - state[2][0][4]), True
        if state[2][0][5] >= 30:
            return 0, True
        return 0, False

    def get_opponent(self, player: int) -> int:
        return -player

    def get_opponent_value(self, value: int) -> int:
        return -value

    def change_perspective(self, state: np.ndarray) -> np.ndarray:
        state[2][0][0] = 2 if state[2][0][0] == 1 else 1
        return state

    def get_encoded_state(self, state: np.ndarray) -> np.ndarray:
        features = np.array(state[0])
        color = state[2][0][state[2][0][0]]
        for row in range(4):
            for col in range(8):
                if state[0][row][col] == 0 or state[0][row][col] == 100:
                    continue
                features[row][col] *= 1 if ((state[1][row][col] // 10) == color) else -1

        channels = 16
        encoded_features = np.zeros(
            (channels, features.shape[0], features.shape[1]), dtype=np.float32
        )
        # No Piece
        encoded_features[0] = (features == 0).astype(np.float32)
        # "Red pieces" and "Black pieces" each with numbers 1 to 7.
        # "The positive and negative signs are based on both sides. "From our perspective, all our pieces will be positive."
        for i in range(1, 8):
            encoded_features[i] = (features == i).astype(np.float32)
            encoded_features[i + 7] = (features == -i).astype(np.float32)
        # Covered Piece
        encoded_features[15] = (features == 100).astype(np.float32)
        return encoded_features

    def count_covered_pieces_number(self, state: np.ndarray) -> int:
        return np.count_nonzero(state[0] == 100)
