import pygame
DOUBLE = 2
ADJUST = 20


class Button:
    def __init__(self, pos: tuple[float, float], text_input: str,
                 font: pygame.font.Font,
                 base_colour: tuple[int, int, int],
                 hover_colour: tuple[int, int, int],
                 bg_base_colour: tuple[int, int, int],
                 bg_hover_colour: tuple[int, int, int],
                 width: int, height: int,
                 transparent: bool) -> None:
        """
        :param pos: Position of button on screen.
        :param text_input: Text to display on button.
        :param font: pygame.font.Font instance of the font size and style.
        :param base_colour: Non-hover text colour.
        :param hover_colour: Hover text colour.
        :param bg_base_colour: Non-hover background colour
        :param bg_hover_colour: Hover background colour
        :param width: Width of button
        :param height: Height of button
        :param transparent: Whether the button bg is transparent.
        """
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

        self.rect.update(self.x_pos - width // DOUBLE,
                         self.y_pos - height // DOUBLE - width // ADJUST,
                         width, height)

        self.OPACITY = 85  # 255//3 = 85. 255 is the max opacity value.

        self.bg = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        if transparent:
            self.bg.set_alpha(self.OPACITY)

    def update(self, screen: pygame.Surface) -> None:
        """
        Blits the button background and button text onto the screen.
        """
        screen.blit(self.bg, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_position(self, position: tuple[int, int]) -> bool:
        """
        :param position: (x, y).
        Returns True if the position given is inside the button rectangle.
        """
        if (position[0] in range(self.rect.left, self.rect.right) and
                position[1] in range(self.rect.top, self.rect.bottom)):
            return True
        return False

    def change_colour(self, position: tuple[int, int]) -> None:
        """
        Checks if position is inside button. If it is, change the text and bg
        colours to their hovering colours. Else, change the colour to base
        colours.
        """
        if self.check_position(position):
            self.text = self.font.render(self.text_input, True,
                                         self.hovering_colour)
            self.bg.fill(self.bg_hover_colour)
        else:
            self.text = self.font.render(self.text_input, True,
                                         self.base_colour)
            self.bg.fill(self.bg_base_colour)
