import sys

# pylint: disable=no-member
import pygame
from src.game import configure_game
from src.events import handle_events


def main() -> None:
    """
    Description
    """

    logger, screen = configure_game()

    try:
        running = True
        while running:
            running = handle_events()
            screen.fill((0, 0, 0))
            pygame.display.flip()
    except Exception as e:
        logger.error("An error occurred: %s", str(e))
    finally:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()
