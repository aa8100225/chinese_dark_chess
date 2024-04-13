# pylint: disable=no-member
import pygame  # type: ignore


def handle_events() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True
