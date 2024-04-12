from typing import Optional, Tuple

# pylint: disable=no-member

import pygame  # type: ignore
from src.logger import setup_error_logger
from src.settings import (
    CAPTION,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    BOARD_IMAGE_PATH,
    COVERED_PIECE_IMAGE_PATH,
    FPS,
)


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(CAPTION)
        self.error_logger = setup_error_logger(__name__)
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.board = pygame.image.load(BOARD_IMAGE_PATH)
        self.covered_piece = pygame.image.load(COVERED_PIECE_IMAGE_PATH)
        self.running = True

    def run(self) -> None:
        while self.running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    clicked_square = self.get_clicked_square(mouse_pos)
                    if clicked_square is not None:
                        print("Clicked square:", clicked_square)

            self.screen.fill((245, 245, 220))  # 白樺木
            scaled_board = pygame.transform.scale(
                self.board, (WINDOW_WIDTH - 40, WINDOW_HEIGHT * 0.78)
            )
            self.screen.blit(scaled_board, (20, WINDOW_HEIGHT // 5))

            self.place_covered_pieces()
            pygame.display.flip()

        pygame.quit()

    def place_covered_pieces(self) -> None:

        piece_size = self.covered_piece.get_width()
        scaled_piece_size = int(piece_size * 0.9)  # 將圖片縮小為原來的 90%
        horizontal_padding = 3.2  # 調整水平間距
        vertical_padding = 25  # 調整垂直間距
        offset_x = (WINDOW_WIDTH - 8 * scaled_piece_size - 7 * horizontal_padding) // 2
        offset_y = (WINDOW_HEIGHT - 4 * scaled_piece_size - 3 * vertical_padding) // 1.2

        for i in range(4):
            for j in range(8):
                # Calculate the position for placing the piece
                piece_x = offset_x + j * (scaled_piece_size + horizontal_padding)
                piece_y = offset_y + i * (scaled_piece_size + vertical_padding)
                # Scale and blit the piece onto the screen
                scaled_piece = pygame.transform.scale(
                    self.covered_piece, (scaled_piece_size, scaled_piece_size)
                )
                self.screen.blit(
                    scaled_piece,
                    (piece_x, piece_y),
                )

    def get_clicked_square(
        self, mouse_pos: Tuple[int, int]
    ) -> Optional[Tuple[int, int]]:

        piece_size = self.covered_piece.get_width()
        scaled_piece_size = int(piece_size * 0.9)
        horizontal_padding = 3.2
        vertical_padding = 25
        offset_x = (WINDOW_WIDTH - 8 * scaled_piece_size - 7 * horizontal_padding) // 2
        offset_y = (WINDOW_HEIGHT - 4 * scaled_piece_size - 3 * vertical_padding) // 1.2

        relative_x = mouse_pos[0] - offset_x
        relative_y = mouse_pos[1] - offset_y

        if (
            0 <= relative_x < 8 * scaled_piece_size + 7 * horizontal_padding
            and 0 <= relative_y < 4 * scaled_piece_size + 3 * vertical_padding
        ):

            col = int(relative_x // (scaled_piece_size + horizontal_padding))
            row = int(relative_y // (scaled_piece_size + vertical_padding))
            return row, col
        else:
            return None
