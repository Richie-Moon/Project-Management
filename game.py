import pygame

LIGHT = (207, 177, 129)
DARK = (129, 92, 60)
DEFAULT_POS = (0, 0)


class Square:
    def __init__(self, pos: tuple[int, int], light: bool,
                 w: int):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.light = light

        # Create correct sized rect at 0,0
        self.rect = pygame.Rect(DEFAULT_POS, (w, w))
        # Move self.rect to position.
        self.rect.center = pos

    def draw(self, screen: pygame.Surface):
        if self.light:
            pygame.draw.rect(screen, LIGHT, self.rect)
        if not self.light:
            pygame.draw.rect(screen, DARK, self.rect)


    def update(self, board: list[list]):
        pass
