from enum import Enum, auto
from typing import Dict

import pygame  # type: ignore

from src.models.piece import Piece, PieceColor, PieceType
from src.config.settings import (
    BLACK_ADVISOR_PIECE_IMAGE_PATH,
    BLACK_CANNON_PIECE_IMAGE_PATH,
    BLACK_CHARIOT_PIECE_IMAGE_PATH,
    BLACK_ELEPHANT_PIECE_IMAGE_PATH,
    BLACK_GENERAL_PIECE_IMAGE_PATH,
    BLACK_HORSE_PIECE_IMAGE_PATH,
    BLACK_SOILDER_PIECE_IMAGE_PATH,
    BOARD_IMAGE_PATH,
    COVERED_PIECE_IMAGE_PATH,
    RED_ADVISOR_PIECE_IMAGE_PATH,
    RED_CANNON_PIECE_IMAGE_PATH,
    RED_CHARIOT_PIECE_IMAGE_PATH,
    RED_ELEPHANT_PIECE_IMAGE_PATH,
    RED_GENERAL_PIECE_IMAGE_PATH,
    RED_HORSE_PIECE_IMAGE_PATH,
    RED_SOILDER_PIECE_IMAGE_PATH,
)


class ImageKey(Enum):
    BOARD = auto()  # 棋盤
    COVERED_PIECE = auto()  # 蓋牌
    RED_GENERAL = auto()  # (紅)帥
    RED_ADVISOR = auto()  # (紅)仕
    RED_ELEPAHNT = auto()  # (紅)相
    RED_CHARIOT = auto()  # (紅)俥
    RED_HORSE = auto()  # (紅)傌
    RED_CANNON = auto()  # (紅)炮
    RED_SOILDER = auto()  # (紅)兵
    BLACK_GENERAL = auto()  # (黑)將
    BLACK_ADVISOR = auto()  # (黑)士
    BLACK_ELEPAHNT = auto()  # (黑)象
    BLACK_CHARIOT = auto()  # (黑)車
    BLACK_HORSE = auto()  # (黑)馬
    BLACK_CANNON = auto()  # (黑)砲
    BLACK_SOILDER = auto()  # (黑)卒


class AssetManager:
    def __init__(self) -> None:
        self.images: Dict[ImageKey, pygame.Surface] = {}
        self.load_images()

    def load_images(self) -> None:
        self.images[ImageKey.BOARD] = pygame.image.load(BOARD_IMAGE_PATH)
        self.images[ImageKey.COVERED_PIECE] = pygame.image.load(
            COVERED_PIECE_IMAGE_PATH
        )
        self.images[ImageKey.RED_GENERAL] = pygame.image.load(
            RED_GENERAL_PIECE_IMAGE_PATH
        )
        self.images[ImageKey.RED_ADVISOR] = pygame.image.load(
            RED_ADVISOR_PIECE_IMAGE_PATH
        )
        self.images[ImageKey.RED_ELEPAHNT] = pygame.image.load(
            RED_ELEPHANT_PIECE_IMAGE_PATH
        )
        self.images[ImageKey.RED_CHARIOT] = pygame.image.load(
            RED_CHARIOT_PIECE_IMAGE_PATH
        )
        self.images[ImageKey.RED_HORSE] = pygame.image.load(RED_HORSE_PIECE_IMAGE_PATH)
        self.images[ImageKey.RED_CANNON] = pygame.image.load(
            RED_CANNON_PIECE_IMAGE_PATH
        )
        self.images[ImageKey.RED_SOILDER] = pygame.image.load(
            RED_SOILDER_PIECE_IMAGE_PATH
        )

        self.images[ImageKey.BLACK_GENERAL] = pygame.image.load(
            BLACK_GENERAL_PIECE_IMAGE_PATH
        )
        self.images[ImageKey.BLACK_ADVISOR] = pygame.image.load(
            BLACK_ADVISOR_PIECE_IMAGE_PATH
        )
        self.images[ImageKey.BLACK_ELEPAHNT] = pygame.image.load(
            BLACK_ELEPHANT_PIECE_IMAGE_PATH
        )
        self.images[ImageKey.BLACK_CHARIOT] = pygame.image.load(
            BLACK_CHARIOT_PIECE_IMAGE_PATH
        )
        self.images[ImageKey.BLACK_HORSE] = pygame.image.load(
            BLACK_HORSE_PIECE_IMAGE_PATH
        )
        self.images[ImageKey.BLACK_CANNON] = pygame.image.load(
            BLACK_CANNON_PIECE_IMAGE_PATH
        )
        self.images[ImageKey.BLACK_SOILDER] = pygame.image.load(
            BLACK_SOILDER_PIECE_IMAGE_PATH
        )

    def get_image(self, key: ImageKey) -> pygame.Surface:
        if key not in self.images:
            return pygame.image.load(COVERED_PIECE_IMAGE_PATH)

        return self.images.get(key)

    def get_piece_image(self, piece: Piece) -> pygame.Surface:
        if piece.covered:
            return self.get_image(ImageKey.COVERED_PIECE)
        image_key: ImageKey
        match (piece.piece_type):
            case PieceType.GENERAL:
                image_key = (
                    ImageKey.RED_GENERAL
                    if piece.piece_color == PieceColor.RED
                    else ImageKey.BLACK_GENERAL
                )
            case PieceType.ADVISOR:
                image_key = (
                    ImageKey.RED_ADVISOR
                    if piece.piece_color == PieceColor.RED
                    else ImageKey.BLACK_ADVISOR
                )
            case PieceType.ELEPHANT:
                image_key = (
                    ImageKey.RED_ELEPAHNT
                    if piece.piece_color == PieceColor.RED
                    else ImageKey.BLACK_ELEPAHNT
                )
            case PieceType.CHARIOT:
                image_key = (
                    ImageKey.RED_CHARIOT
                    if piece.piece_color == PieceColor.RED
                    else ImageKey.BLACK_CHARIOT
                )
            case PieceType.HORSE:
                image_key = (
                    ImageKey.RED_HORSE
                    if piece.piece_color == PieceColor.RED
                    else ImageKey.BLACK_HORSE
                )
            case PieceType.CANNON:
                image_key = (
                    ImageKey.RED_CANNON
                    if piece.piece_color == PieceColor.RED
                    else ImageKey.BLACK_CANNON
                )
            case PieceType.SOLDIER:
                image_key = (
                    ImageKey.RED_SOILDER
                    if piece.piece_color == PieceColor.RED
                    else ImageKey.BLACK_SOILDER
                )
        return self.get_image(image_key)
