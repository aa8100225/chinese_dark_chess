import random
from enum import Enum, auto
from typing import Optional


class PlayerColor(Enum):
    RED = auto()
    BLACK = auto()

    def get_opposite_color(self) -> "PlayerColor":
        return PlayerColor.BLACK if self == PlayerColor.RED else PlayerColor.RED


class Player:
    def __init__(self, name: str):
        self.name = name
        self.color: Optional[PlayerColor] = None
        self.is_current_player: bool = False

    def assign_color(self, color: PlayerColor) -> None:
        self.color = color

    def toggle_current_player(self) -> None:
        self.is_current_player = not self.is_current_player

    def __repr__(self) -> str:
        return f"{self.name} ({'RED' if self.color == PlayerColor.RED else 'BLACK'})"
