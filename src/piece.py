from enum import Enum, auto
from typing import Any, Dict

from src.assets_manager import ImageKey


class PieceType(Enum):
    GENERAL = auto()
    ADVISOR = auto()
    ELEPHANT = auto()
    CHARIOT = auto()
    HORSE = auto()
    CANNON = auto()
    SOLDIER = auto()

    def can_defeat(self, enemy: "PieceType") -> bool:
        result = False
        match self:
            case PieceType.GENERAL:
                result = (
                    PieceType.GENERAL.value <= enemy.value < PieceType.SOLDIER.value
                )
            case PieceType.ADVISOR:
                result = enemy.value >= PieceType.ADVISOR.value
            case PieceType.ELEPHANT:
                result = enemy.value >= PieceType.GENERAL.value
            case PieceType.CHARIOT:
                result = enemy.value >= PieceType.CHARIOT.value
            case PieceType.HORSE:
                result = enemy.value >= PieceType.HORSE.value
            case PieceType.SOLDIER:
                result = enemy in {PieceType.SOLDIER, PieceType.GENERAL}
            case PieceType.CANNON:
                result = True
        return result


class PieceColor(Enum):
    RED = auto()
    BLACK = auto()

    def opposite_color(self) -> "PieceColor":
        return PieceColor.BLACK if self == PieceColor.RED else PieceColor.RED


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
