# pylint: disable=no-member

import pygame  # type: ignore
from src.action_detector import ActionDetector
from src.action_handler import ActionHandler
from src.assets_manager import AssetManager, ImageKey
from src.game_renderer import GameRenderer
from src.game_state import GameState, GameStatus
from src.logger import setup_error_logger
from src.settings import (
    CAPTION,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FPS,
)


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(CAPTION)
        self.error_logger = setup_error_logger(__name__)
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_state = GameState()
        self.action_detector = ActionDetector(self.game_state)
        self.action_handler = ActionHandler(self.game_state)
        self.assets_manager = AssetManager()
        self.game_renderer = GameRenderer(
            self.game_state, self.screen, self.assets_manager
        )
        self.covered_piece = self.assets_manager.get_image(ImageKey.COVERED_PIECE)
        self.running = True

    def run(self) -> None:
        while self.running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.game_renderer.is_reset_button_pressed(mouse_pos):
                        self.game_state.reset_game()
                    else:
                        if self.game_state.game_status != GameStatus.ONGOING:
                            continue
                        clicked_square = self.game_renderer.get_clicked_square(
                            mouse_pos
                        )
                        if clicked_square is not None:
                            print("Clicked square:", clicked_square)
                            action_type = self.action_detector.detect_action(
                                clicked_square
                            )
                            self.action_handler.handle_action(
                                clicked_square, action_type
                            )
            self.game_renderer.render()

        pygame.quit()
