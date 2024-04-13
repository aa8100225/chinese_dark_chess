from enum import Enum, auto
from typing import Any, Dict

from src.assets_manager import ImageKey


class PieceType(Enum):
    GENERAL = auto()
    ADVISOR = auto()
    ELEPHANT = auto()
    HORSE = auto()
    CHARIOT = auto()
    CANNON = auto()
    SOLDIER = auto()


class PieceColor(Enum):
    RED = auto()
    BLACK = auto()


def pieces_config_hepler(piece_color: PieceColor) -> Dict[PieceType, Dict[str, Any]]:
    return {
        PieceType.GENERAL: {
            "count": 1,
            "image": (
                ImageKey.RED_GENERAL
                if piece_color == PieceColor.RED
                else ImageKey.BLACK_GENERAL
            ),
        },
        PieceType.ADVISOR: {
            "count": 2,
            "image": (
                ImageKey.RED_ADVISOR
                if piece_color == PieceColor.RED
                else ImageKey.BLACK_ADVISOR
            ),
        },
        PieceType.ELEPHANT: {
            "count": 2,
            "image": (
                ImageKey.RED_ELEPAHNT
                if piece_color == PieceColor.RED
                else ImageKey.BLACK_ELEPAHNT
            ),
        },
        PieceType.CHARIOT: {
            "count": 2,
            "image": (
                ImageKey.RED_CHARIOT
                if piece_color == PieceColor.RED
                else ImageKey.BLACK_CHARIOT
            ),
        },
        PieceType.HORSE: {
            "count": 2,
            "image": (
                ImageKey.RED_HORSE
                if piece_color == PieceColor.RED
                else ImageKey.BLACK_HORSE
            ),
        },
        PieceType.CANNON: {
            "count": 2,
            "image": (
                ImageKey.RED_CANNON
                if piece_color == PieceColor.RED
                else ImageKey.BLACK_CANNON
            ),
        },
        PieceType.SOLDIER: {
            "count": 5,
            "image": (
                ImageKey.RED_SOILDER
                if piece_color == PieceColor.RED
                else ImageKey.BLACK_SOILDER
            ),
        },
    }


class Piece:
    """
    Chess Piece
    """

    def __init__(
        self,
        key: int,
        piece_type: PieceType,
        piece_color: PieceColor,
        image_key: ImageKey,
    ):
        self.key = key
        self.image_key = image_key
        self.piece_type = piece_type
        self.piece_color = piece_color
        self.covered = True

    def reveal(self) -> None:
        self.covered = False

    def __repr__(self) -> str:
        return f"{self.piece_color} {self.piece_type.name}"
