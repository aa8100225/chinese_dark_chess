from enum import Enum, auto
from typing import Dict

import pygame

from src.settings import BOARD_IMAGE_PATH, COVERED_PIECE_IMAGE_PATH


class ImageKey(Enum):
    BOARD = auto()
    COVERED_PIECE = auto()


class AssetManager:
    def __init__(self) -> None:
        self.images: Dict[ImageKey, pygame.Surface] = {}
        self.load_images()

    def load_images(self) -> None:
        self.images[ImageKey.BOARD] = pygame.image.load(BOARD_IMAGE_PATH)
        self.images[ImageKey.COVERED_PIECE] = pygame.image.load(
            COVERED_PIECE_IMAGE_PATH
        )
        # 可以繼續加載更多的圖片

    def get_image(self, key: ImageKey) -> pygame.Surface | None:
        return self.images.get(key)
