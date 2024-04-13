from typing import List, Optional, Tuple
import pygame  # type: ignore
from src.assets_manager import AssetManager, ImageKey
from src.game_state import GameState
from src.player import PlayerColor
from src.settings import WINDOW_HEIGHT, WINDOW_WIDTH


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

    def render(self) -> None:
        self.screen.fill((245, 245, 220))  # 白樺木
        self.draw_player_infos()
        self.draw_reset_button()
        self.draw_board()
        self.draw_pieces()
        pygame.display.flip()

    def draw_board(self) -> None:
        scaled_board = pygame.transform.scale(
            self.assets_manager.get_image(ImageKey.BOARD),
            (WINDOW_WIDTH - 40, WINDOW_HEIGHT * 0.78),
        )
        self.screen.blit(scaled_board, (20, WINDOW_HEIGHT // 5))

    def draw_player_infos(self) -> None:

        radius = 20
        triangle_height = 30
        # Player 1 left
        player1_color = (0, 0, 255)  # 藍色
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
        player2_color = (50, 240, 50)  # 綠色
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
        font = pygame.font.Font(None, 24)  # 選擇合適的字體和大小
        name_surface = font.render(name, True, (0, 0, 0))
        name_x = (
            head_center_x
            - name_surface.get_width() / 2
            + (5 if player_index == 0 else -5)
        )  # 名稱置中於人像下方
        name_y = head_center_y + 60  # 人像底部向下一定距離
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
            return  # 非當前玩家

        indicator_color = (200, 200, 200)  # 白色
        if self.game_state.is_color_assign:
            indicator_color = (
                (255, 0, 0)
                if self.game_state.get_current_player().color == PlayerColor.RED
                else (0, 0, 0)
            )
        points: List[Tuple[int, int]]
        # 繪製箭頭
        if player_number == 0:
            points = [(x + 30, y), (x + 50, y - 10), (x + 50, y + 10)]
        else:
            points = [(x - 30, y), (x - 50, y - 10), (x - 50, y + 10)]

        pygame.draw.polygon(self.screen, indicator_color, points)

    def draw_reset_button(self) -> None:
        button_width, button_height = 100, 50
        button_x = (WINDOW_WIDTH - button_width) / 2
        button_y = 10
        button_color = (70, 70, 70)  # 鐵灰色

        # 畫一個有圓角的矩形作為按鈕
        pygame.draw.rect(
            self.screen,
            button_color,
            (button_x, button_y, button_width, button_height),
            border_radius=10,
        )

        # 在按鈕上添加文字
        font = pygame.font.Font(None, 24)
        text_surface = font.render("Reset", True, (255, 255, 255))  # 白色文字
        text_x = button_x + (button_width - text_surface.get_width()) / 2
        text_y = button_y + (button_height - text_surface.get_height()) / 2
        self.screen.blit(text_surface, (text_x, text_y))

    def is_reset_button_pressed(self, pos: Tuple[int, int]) -> bool:
        button_width, button_height = 100, 50
        button_x = (WINDOW_WIDTH - button_width) / 2
        button_y = 10
        x, y = pos
        return (
            button_x <= x <= button_x + button_width
            and button_y <= y <= button_y + button_height
        )

    def draw_pieces(self) -> None:
        piece_size = self.assets_manager.get_image(ImageKey.COVERED_PIECE).get_width()
        scaled_piece_size = int(piece_size * 0.9)  # 將圖片縮小為原來的 90%
        horizontal_padding = 3.2  # 調整水平間距
        vertical_padding = 25  # 調整垂直間距
        offset_x = (WINDOW_WIDTH - 8 * scaled_piece_size - 7 * horizontal_padding) // 2
        offset_y = (WINDOW_HEIGHT - 4 * scaled_piece_size - 3 * vertical_padding) // 1.2

        for i in range(4):
            for j in range(8):
                selected: bool = (i, j) == self.game_state.selected_piece
                piece = self.game_state.get_piece_by_coordinate(i, j)
                # Calculate the position for placing the piece
                piece_x = offset_x + j * (scaled_piece_size + horizontal_padding)
                piece_y = offset_y + i * (scaled_piece_size + vertical_padding)

                if piece is not None:
                    # Scale and blit the piece onto the screen
                    scaled_piece = pygame.transform.scale(
                        self.assets_manager.get_image(
                            ImageKey.COVERED_PIECE if piece.covered else piece.image_key
                        ),
                        (scaled_piece_size, scaled_piece_size),
                    )
                    self.screen.blit(scaled_piece, (piece_x, piece_y))
                    if selected:
                        indicator_color = (255, 20, 147)  # 粉紫色
                        pygame.draw.rect(
                            self.screen,
                            indicator_color,
                            (
                                piece_x + 3,
                                piece_y + 3,
                                scaled_piece_size - 5,
                                scaled_piece_size - 5,
                            ),
                            3,  # 框的粗细
                        )
                else:
                    # Draw a smaller black cross at the position
                    cross_size = (
                        scaled_piece_size // 12
                    )  # Define the size of the cross arms
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

        piece_size = self.assets_manager.get_image(ImageKey.COVERED_PIECE).get_width()
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

        return None
