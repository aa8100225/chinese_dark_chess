from typing import Dict, List, Optional, Tuple

from src.models.board import Board
from src.models.piece import Piece, PieceColor, PieceType
from src.models.piece_action import PieceAction, PieceActionType
from src.models.player import PlayerColor


class PieceActionManager:
    def __init__(self, board: Board) -> None:
        self.board = board
        self.red_alignment_action: Dict[str, PieceAction] = {}
        self.black_alignment_action: Dict[str, PieceAction] = {}
        self.neutral_action: Dict[str, PieceAction] = {}
        self.initialization()

    def initialization(self) -> None:
        self.update_action_set()

    def update_action_set(self) -> None:
        self.red_alignment_action = {}
        self.black_alignment_action = {}
        self.neutral_action = {}
        for index, piece in enumerate(self.board.get_all_pieces_status()):
            position = self.board.to_coordinates(index)
            if piece is None:
                continue
            if piece.covered:
                piece_action = PieceAction(position, PieceActionType.REVEAL, position)
                self.neutral_action[piece_action.generate_hash_key()] = piece_action
            else:
                if piece.piece_color == PieceColor.RED:
                    # movement
                    self.red_alignment_action.update(
                        self.generate_movement_piece_action(position)
                    )
                    # eating
                    self.red_alignment_action.update(
                        self.generate_eating_piece_action(position, piece)
                    )
                else:
                    # movement
                    self.black_alignment_action.update(
                        self.generate_movement_piece_action(position)
                    )
                    # eating
                    self.black_alignment_action.update(
                        self.generate_eating_piece_action(position, piece)
                    )

    def generate_movement_piece_action(
        self, position: Tuple[int, int]
    ) -> Dict[str, PieceAction]:
        dirs = [-1, 0, 1, 0, -1]
        piece_actions: Dict[str, PieceAction] = {}
        for i in range(4):
            next_x = position[0] + dirs[i]
            next_y = position[1] + dirs[i + 1]
            if (
                next_x < 0
                or next_x >= 4
                or next_y < 0
                or next_y >= 8
                or self.board.get_piece_by_coordinate(next_x, next_y) is not None
            ):
                continue
            piece_action = PieceAction(position, PieceActionType.MOVE, (next_x, next_y))
            piece_actions[piece_action.generate_hash_key()] = piece_action
        return piece_actions

    def generate_eating_piece_action(
        self, position: Tuple[int, int], piece: Piece
    ) -> Dict[str, PieceAction]:
        piece_actions: Dict[str, PieceAction] = {}
        # Special handling for the cannon piece type
        if PieceType.CANNON == piece.piece_type:
            for next_x, next_y in self.generate_cannon_potential_attack_positions(
                position
            ):
                enemy_piece = self.board.get_piece_by_coordinate(next_x, next_y)
                if (
                    enemy_piece is None
                    or enemy_piece.covered
                    or enemy_piece.piece_color == piece.piece_color
                ):
                    continue
                piece_action = PieceAction(
                    position, PieceActionType.EAT, (next_x, next_y)
                )
                piece_actions[piece_action.generate_hash_key()] = piece_action
            return piece_actions
        # Handling for all pieces except cannons
        dirs = [-1, 0, 1, 0, -1]
        for i in range(4):
            next_x = position[0] + dirs[i]
            next_y = position[1] + dirs[i + 1]
            if next_x < 0 or next_x >= 4 or next_y < 0 or next_y >= 8:
                continue
            enemy_piece = self.board.get_piece_by_coordinate(next_x, next_y)
            if (
                enemy_piece is not None
                and not enemy_piece.covered
                and enemy_piece.piece_color == piece.piece_color.opposite_color()
                and piece.piece_type.can_defeat(enemy_piece.piece_type)
            ):
                piece_action = PieceAction(
                    position, PieceActionType.EAT, (next_x, next_y)
                )
                piece_actions[piece_action.generate_hash_key()] = piece_action
        return piece_actions

    def generate_cannon_potential_attack_positions(
        self, position: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        potential_targets: List[Tuple[int, int]] = []
        dirs = [-1, 0, 1, 0, -1]

        for i in range(4):
            jump_over = False
            current_x, current_y = position
            while True:
                current_x += dirs[i]
                current_y += dirs[i + 1]
                if not (0 <= current_x < 4 and 0 <= current_y < 8):
                    break
                next_piece = self.board.get_piece_by_coordinate(current_x, current_y)
                if next_piece is None:
                    continue
                if not jump_over:
                    jump_over = True
                else:
                    potential_targets.append((current_x, current_y))
                    break
        return potential_targets

    def is_valid_action(
        self, piece_action: PieceAction, player_color: Optional[PlayerColor]
    ) -> bool:
        key = piece_action.generate_hash_key()
        return key in self.neutral_action or (
            key in self.black_alignment_action
            if PlayerColor.BLACK == player_color
            else key in self.red_alignment_action
        )

    def implement_action(self, piece_action: PieceAction) -> None:
        current_position = self.board.to_index(
            piece_action.current_position[0], piece_action.current_position[1]
        )
        next_position = self.board.to_index(
            piece_action.next_position[0], piece_action.next_position[1]
        )
        pieces: List[Optional[Piece]] = self.board.get_all_pieces_status()
        match (piece_action.piece_action_type):
            case PieceActionType.EAT | PieceActionType.MOVE:
                pieces[next_position], pieces[current_position] = (
                    pieces[current_position],
                    None,
                )
            case PieceActionType.REVEAL:
                piece = pieces[current_position]
                if piece is not None:
                    piece.reveal()
            case _:
                # raise Exception("Invalid Action ", piece_action.piece_action_type)
                print("Invalid Action ", piece_action.piece_action_type)

    def player_has_any_valid_action(self, player_color: PlayerColor) -> bool:
        if len(self.neutral_action) > 0:
            return True
        match (player_color):
            case PlayerColor.RED:
                return len(self.red_alignment_action) > 0
            case PlayerColor.BLACK:
                return len(self.black_alignment_action) > 0

    def decode_action_index(self, index: int) -> PieceAction:
        start = index // 65
        action_offset = index % 65  # bias
        if action_offset < 32:
            end = action_offset
            return PieceAction(
                self.board.to_coordinates(start),
                PieceActionType.MOVE,
                self.board.to_coordinates(end),
            )
        if action_offset < 64:
            end = action_offset - 32
            return PieceAction(
                self.board.to_coordinates(start),
                PieceActionType.EAT,
                self.board.to_coordinates(end),
            )

        end = start
        return PieceAction(
            self.board.to_coordinates(start),
            PieceActionType.REVEAL,
            self.board.to_coordinates(end),
        )

    def get_legal_actions(self, player_color: Optional[PlayerColor]) -> List[int]:
        result: List[int] = []
        for action in self.neutral_action.values():
            result.append(action.to_action_index())
        if player_color is not None:
            for action in (
                self.black_alignment_action.values()
                if PlayerColor.BLACK == player_color
                else self.red_alignment_action.values()
            ):
                result.append(action.to_action_index())
        return result
