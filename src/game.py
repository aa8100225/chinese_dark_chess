# pylint: disable=no-member
import logging

import pygame
from src.logger import setup_error_logger
from src.settings import CAPTION, SCREEN_HEIGHT, SCREEN_WIDTH


def configure_game() -> tuple[logging.Logger, pygame.Surface]:
    pygame.init()
    error_logger = setup_error_logger(__name__)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(CAPTION)
    return error_logger, screen
