import pygame


class Button:
    def __init__(self, image: pygame.Surface | None, pos: tuple[int],
                 text_input: str, font: pygame.font.Font, base_colour: str,
                 hover_colour: str):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_colour, self.hovering_colour = base_colour, hover_colour
        self.text_input = text_input
        self.text = self.font.render(text=self.text_input, antialias=True,
                                     color=self.base_colour)

        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen: pygame.Surface):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_position(self, position: tuple[int, int]):
        if (position[0] in range(self.rect.left, self.rect.right) and
                position[1] in range(self.rect.top, self.rect.bottom)):
            return True
        return False

    def change_colour(self, position: tuple[int, int]):
        if self.check_position(position):
            self.text = self.font.render(text=self.text_input, antialias=True,
                                         color=self.hovering_colour)
        else:
            self.text = self.font.render(text=self.text_input, antialias=True,
                                         color=self.base_colour)
