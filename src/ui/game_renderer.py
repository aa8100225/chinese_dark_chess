from typing import List, Optional, Tuple
import pygame  # type: ignore
from src.ui.assets_manager import AssetManager, ImageKey
from src.game_state import GameState, GameStatus
from src.models.player import PlayerColor
from src.config.settings import WINDOW_HEIGHT, WINDOW_WIDTH

# Constants for drawing
BOARD_SCALE_HEIGHT_FACTOR = 0.78
BOARD_ROW_NUMS = 4
BOARD_COL_NUMS = 8

RESET_BUTTON_DIMENSIONS = (100, 50)
ANCHOR_POINT_OF_RESET_BUTTON = ((WINDOW_WIDTH - RESET_BUTTON_DIMENSIONS[0]) / 2, 10)

PIECE_SCALING_FACTOR = 0.9
PIECE_HORIZONTAL_PADDING = 3.2
PIECE_VERTICAL_PADDING = 25
PIECE_VERTICAL_OFFSET_DIVSDOR = 1.2
PIECE_HORIZONTAL_OFFSET_DIVSDOR = 2


class GameRenderer:

    def __init__(
        self,
        game_state: GameState,
        screen: pygame.Surface,
        assets_manager: AssetManager,
    ):
        self.game_state = game_state
        self.screen = screen
        self.assets_manager = assets_manager

        self.scaled_board = self.scale_board_image()
        self.piece_size = self.assets_manager.get_image(
            ImageKey.COVERED_PIECE
        ).get_width()

    def render(self) -> None:
        """Render the main elements of the game screen."""
        self.screen.fill((245, 245, 220))  # 白樺木
        self.draw_player_infos()
        self.draw_reset_button()
        self.draw_board()
        self.draw_pieces()
        self.draw_game_status()
        pygame.display.flip()

    def draw_board(self) -> None:
        self.screen.blit(self.scaled_board, (20, WINDOW_HEIGHT // 5))

    def scale_board_image(self):
        """Scale the board image to fit the game window size."""
        board_image = self.assets_manager.get_image(ImageKey.BOARD)
        scaled_board = pygame.transform.scale(
            board_image,
            (WINDOW_WIDTH - 40, int(WINDOW_HEIGHT * BOARD_SCALE_HEIGHT_FACTOR)),
        )
        return scaled_board

    def draw_player_infos(self) -> None:
        radius = 20
        triangle_height = 30
        # Player 1 left
        player1_color = (0, 0, 255)  # Blue
        head_center_x1 = 30
        head_center_y1 = 30
        self.draw_player_icon(
            head_center_x1, head_center_y1, radius, triangle_height, player1_color
        )
        self.draw_player_names(
            head_center_x1, head_center_y1, self.game_state.players[0].name, 0
        )
        self.draw_current_player_indicator(head_center_x1, head_center_y1, 0)

        # Player 2 right
        player2_color = (50, 240, 50)  # Green
        head_center_x2 = self.screen.get_width() - 30
        head_center_y2 = 30
        self.draw_player_icon(
            head_center_x2, head_center_y2, radius, triangle_height, player2_color
        )
        self.draw_player_names(
            head_center_x2, head_center_y2, self.game_state.players[1].name, 1
        )
        self.draw_current_player_indicator(head_center_x2, head_center_y2, 1)

    def draw_player_names(
        self, head_center_x: int, head_center_y: int, name: str, player_index: int
    ) -> None:
        font = pygame.font.Font(None, 24)
        name_surface = font.render(name, True, (0, 0, 0))
        name_x = (
            head_center_x
            - name_surface.get_width() / 2
            + (5 if player_index == 0 else -5)
        )  # name placed below the player icon
        name_y = head_center_y + 60  #
        self.screen.blit(name_surface, (name_x, name_y))

    def draw_player_icon(
        self,
        head_center_x: int,
        head_center_y: int,
        radius: int,
        triangle_height: int,
        color: Tuple[int, int, int],
    ) -> None:

        pygame.draw.circle(self.screen, color, (head_center_x, head_center_y), radius)
        triangle_top = (head_center_x, head_center_y + radius - 5)
        triangle_left = (
            head_center_x - radius,
            head_center_y + radius + triangle_height,
        )
        triangle_right = (
            head_center_x + radius,
            head_center_y + radius + triangle_height,
        )
        pygame.draw.polygon(
            self.screen, color, [triangle_top, triangle_left, triangle_right]
        )

    def draw_current_player_indicator(self, x: int, y: int, player_number: int) -> None:

        if self.game_state.current_player_index != player_number:
            return  # not current player turn

        indicator_color = (200, 200, 200)  # default color
        if self.game_state.is_color_assign:
            indicator_color = (
                (255, 0, 0)
                if self.game_state.get_current_player().color == PlayerColor.RED
                else (0, 0, 0)
            )
        points: List[Tuple[int, int]]
        # arrow indicator
        if player_number == 0:
            points = [(x + 30, y), (x + 50, y - 10), (x + 50, y + 10)]
        else:
            points = [(x - 30, y), (x - 50, y - 10), (x - 50, y + 10)]

        pygame.draw.polygon(self.screen, indicator_color, points)

    def draw_reset_button(self) -> None:
        button_width, button_height = RESET_BUTTON_DIMENSIONS
        button_x, button_y = ANCHOR_POINT_OF_RESET_BUTTON
        button_color = (70, 70, 70)  # iron gray

        pygame.draw.rect(
            self.screen,
            button_color,
            (button_x, button_y, button_width, button_height),
            border_radius=10,
        )

        font = pygame.font.Font(None, 24)
        text_surface = font.render("Reset", True, (255, 255, 255))
        text_x = button_x + (button_width - text_surface.get_width()) / 2
        text_y = button_y + (button_height - text_surface.get_height()) / 2
        self.screen.blit(text_surface, (text_x, text_y))

    def is_reset_button_pressed(self, pos: Tuple[int, int]) -> bool:
        button_width, button_height = RESET_BUTTON_DIMENSIONS
        button_x, button_y = ANCHOR_POINT_OF_RESET_BUTTON
        x, y = pos
        return (
            button_x <= x <= button_x + button_width
            and button_y <= y <= button_y + button_height
        )

    def piece_offset_calculate(self) -> Tuple[int, int]:
        scaled_piece_size = int(self.piece_size * PIECE_SCALING_FACTOR)
        offset_x: int = (
            int(
                WINDOW_WIDTH
                - BOARD_COL_NUMS * scaled_piece_size
                - (BOARD_COL_NUMS - 1) * PIECE_HORIZONTAL_PADDING
            )
            // PIECE_HORIZONTAL_OFFSET_DIVSDOR
        )
        offset_y: int = int(
            int(
                WINDOW_HEIGHT
                - BOARD_ROW_NUMS * scaled_piece_size
                - (BOARD_ROW_NUMS - 1) * PIECE_VERTICAL_PADDING
            )
            // PIECE_VERTICAL_OFFSET_DIVSDOR
        )
        return (offset_x, offset_y)

    def draw_pieces(self) -> None:
        scaled_piece_size = int(self.piece_size * PIECE_SCALING_FACTOR)
        offset_x, offset_y = self.piece_offset_calculate()

        for i in range(BOARD_ROW_NUMS):
            for j in range(BOARD_COL_NUMS):
                selected: bool = (i, j) == self.game_state.selected_piece
                piece = self.game_state.get_piece_by_coordinate(i, j)
                # Calculate the position for placing the piece
                piece_x = offset_x + j * (scaled_piece_size + PIECE_HORIZONTAL_PADDING)
                piece_y = offset_y + i * (scaled_piece_size + PIECE_VERTICAL_PADDING)

                if piece is not None:
                    # Scale and blit the piece onto the screen
                    scaled_piece = pygame.transform.scale(
                        self.assets_manager.get_piece_image(piece),
                        (scaled_piece_size, scaled_piece_size),
                    )
                    self.screen.blit(scaled_piece, (piece_x, piece_y))
                    if selected:  # Highlight selected piece with a rectangle
                        indicator_color = (255, 20, 147)
                        pygame.draw.rect(
                            self.screen,
                            indicator_color,
                            (
                                piece_x + 3,
                                piece_y + 3,
                                scaled_piece_size - 5,
                                scaled_piece_size - 5,
                            ),
                            3,
                        )
                else:
                    # Draw a smaller black cross at the position if there's no piece
                    cross_size = scaled_piece_size // 12
                    center_x = piece_x + scaled_piece_size // 2
                    center_y = piece_y + scaled_piece_size // 2

                    pygame.draw.line(
                        self.screen,
                        (0, 0, 0),  # Black color
                        (center_x - cross_size, center_y),
                        (center_x + cross_size, center_y),
                        width=5,  # Line thickness
                    )
                    pygame.draw.line(
                        self.screen,
                        (0, 0, 0),  # Black color
                        (center_x, center_y - cross_size),
                        (center_x, center_y + cross_size),
                        width=5,  # Line thickness
                    )

    def get_clicked_square(
        self, mouse_pos: Tuple[int, int]
    ) -> Optional[Tuple[int, int]]:

        scaled_piece_size = int(self.piece_size * PIECE_SCALING_FACTOR)
        offset_x, offset_y = self.piece_offset_calculate()

        relative_x = mouse_pos[0] - offset_x
        relative_y = mouse_pos[1] - offset_y

        if (
            0
            <= relative_x
            < BOARD_COL_NUMS * scaled_piece_size
            + (BOARD_COL_NUMS - 1) * PIECE_HORIZONTAL_PADDING
            and 0
            <= relative_y
            < BOARD_ROW_NUMS * scaled_piece_size
            + (BOARD_ROW_NUMS - 1) * PIECE_VERTICAL_PADDING
        ):

            col = int(relative_x // (scaled_piece_size + PIECE_HORIZONTAL_PADDING))
            row = int(relative_y // (scaled_piece_size + PIECE_VERTICAL_PADDING))
            return row, col

        return None

    def draw_game_status(self) -> None:
        if self.game_state.game_status == GameStatus.ONGOING:
            return
        status_text = "Game Over: "
        if self.game_state.game_status == GameStatus.RED_WIN:
            status_text += "Red Wins!"
        elif self.game_state.game_status == GameStatus.BLACK_WIN:
            status_text += "Black Wins !"
        else:
            status_text += "Draw."

        text_x = WINDOW_WIDTH // 2
        text_y = RESET_BUTTON_DIMENSIONS[1] + ANCHOR_POINT_OF_RESET_BUTTON[1] + 30

        font = pygame.font.Font(None, 36)
        text_surface = font.render(status_text, True, (128, 0, 128))
        text_rect = text_surface.get_rect(center=(text_x, text_y))
        self.screen.blit(text_surface, text_rect)
