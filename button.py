import pygame
BORDER: int = 30
DOUBLE = 2
WIDTH = 530


class Button:
    def __init__(self, pos: tuple[float, float], text_input: str,
                 font: pygame.font.Font,
                 base_colour: tuple[int, int, int],
                 hover_colour: tuple[int, int, int],
                 bg_base_colour: tuple[int, int, int],
                 bg_hover_colour: tuple[int, int, int],
                 screen_width: float,
                 transparent: bool) -> None:
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_colour, self.hovering_colour = base_colour, hover_colour
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_colour)

        self.bg_base_colour = bg_base_colour
        self.bg_hover_colour = bg_hover_colour

        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.rect = self.text_rect.copy()

        h = self.text_rect.height
        self.rect.update(screen_width // 2 - WIDTH // 2,
                         self.text_rect.top - BORDER, WIDTH, h)

        print(self.rect.height)

        self.OPACITY = 85  # 255//3 = 85. 255 is the max opacity value.

        self.bg = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        if transparent:
            self.bg.set_alpha(self.OPACITY)

    def update(self, screen: pygame.Surface) -> None:
        screen.blit(self.bg, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_position(self, position: tuple[int, int]) -> bool:
        if (position[0] in range(self.rect.left, self.rect.right) and
                position[1] in range(self.rect.top, self.rect.bottom)):
            return True
        return False

    def change_colour(self, position: tuple[int, int]) -> None:
        if self.check_position(position):
            self.text = self.font.render(self.text_input, True,
                                         self.hovering_colour)
            self.bg.fill(self.bg_hover_colour)
        else:
            self.text = self.font.render(self.text_input, True,
                                         self.base_colour)
            self.bg.fill(self.bg_base_colour)
