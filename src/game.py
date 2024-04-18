# pylint: disable=no-member

import asyncio
from logging import Logger
from typing import Optional
import pygame  # type: ignore
from src.handlers.action_detector import ActionDetector
from src.handlers.action_handler import ActionHandler
from src.ai.agent import Agent
from src.ui.assets_manager import AssetManager
from src.ui.game_renderer import GameRenderer
from src.game_state import GameState, GameStatus
from src.config.settings import (
    AI_SIGNAL_DELAY,
    CAPTION,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FPS,
)


class Game:
    AI_ACTION_EVENT = pygame.USEREVENT + 1

    def __init__(self, ai_model_path: str, play_with_ai: bool, logger: Logger) -> None:
        pygame.init()
        pygame.display.set_caption(CAPTION)
        self.play_with_ai = play_with_ai
        self.error_logger = logger
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_state: GameState
        self.agent: Optional[Agent]
        self.action_detector: ActionDetector
        self.action_handler: ActionHandler
        self.assets_manager: AssetManager
        self.game_renderer: GameRenderer
        self.initialization(ai_model_path)

        self.running = True

    def initialization(self, ai_model_path: str) -> None:
        self.game_state = GameState()
        self.agent = Agent(ai_model_path) if self.play_with_ai else None
        self.action_detector = ActionDetector(self.game_state)
        self.action_handler = ActionHandler(self.game_state, self.agent)
        self.assets_manager = AssetManager()
        self.game_renderer = GameRenderer(
            self.game_state, self.screen, self.assets_manager
        )

    def run(self) -> None:
        self.sent_signal_to_ai()
        while self.running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == Game.AI_ACTION_EVENT:
                    if (
                        self.game_state.game_status == GameStatus.ONGOING
                        and self.is_ai_turn()
                    ):
                        asyncio.run(self.action_handler.ai_action())
                    pygame.time.set_timer(Game.AI_ACTION_EVENT, 0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.game_renderer.is_reset_button_pressed(mouse_pos):
                        self.game_state.reset_game()
                        self.sent_signal_to_ai()
                    else:
                        if (
                            self.game_state.game_status != GameStatus.ONGOING
                            or self.is_ai_turn()
                        ):
                            continue
                        clicked_square = self.game_renderer.get_clicked_square(
                            mouse_pos
                        )
                        if clicked_square is not None:
                            action_type = self.action_detector.detect_action(
                                clicked_square
                            )
                            self.action_handler.handle_action(
                                clicked_square, action_type
                            )
                            self.sent_signal_to_ai()

            self.game_renderer.render()

        pygame.quit()

    def sent_signal_to_ai(self) -> None:
        if not self.is_ai_turn():
            return
        pygame.time.set_timer(Game.AI_ACTION_EVENT, AI_SIGNAL_DELAY)

    def is_ai_turn(self) -> bool:
        return self.play_with_ai and self.game_state.current_player_index == 0
