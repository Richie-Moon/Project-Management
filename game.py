import pygame

LIGHT = (207, 177, 129)
DARK = (129, 92, 60)
GRAY = (211, 211, 211, 160)

HALF = 0.5
CIRCLE_RADIUS = 5


class Square:
    def __init__(self, pos: tuple[int, int], light: bool, w: int, file: int,
                 rank: int):
        """

        :param pos: x and y co-ordinates for the top-left corner of square.
        :param light: Whether the light is light (True) or dark (False)
        :param w: Width of the square.
        :param file: The file co-ordinate of the square. Must be 0-5 inclusive.
        :param rank: The rank co-ordinate of the square. Must be 0-5 inclusive.
        """
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.light: bool = light
        self.w = w

        self.dot: bool = False

        self.file = file
        self.rank = rank
        self.coords = (file, rank)

        # Create rect object for square
        self.rect = pygame.Rect(self.x_pos, self.y_pos, w, w)

        self.has_piece: bool = False

        # Surface for dot (required for transparency).
        self.dot_surface = pygame.Surface((w, w), pygame.SRCALPHA)

    def draw(self, screen: pygame.Surface, image: pygame.Surface = None):
        if self.light:
            pygame.draw.rect(screen, LIGHT, self.rect)
        if not self.light:
            pygame.draw.rect(screen, DARK, self.rect)

        if self.has_piece:
            screen.blit(image, self.rect)

        if self.dot:
            pygame.draw.circle(self.dot_surface, GRAY,
                               (self.dot_surface.get_width() * HALF,
                                self.dot_surface.get_width() * HALF),
                               self.w // CIRCLE_RADIUS)

            screen.blit(self.dot_surface, self.rect)

    def check_position(self, position: tuple[int, int]) -> bool:
        if (position[0] in range(self.rect.left, self.rect.right) and
                position[1] in range(self.rect.top, self.rect.bottom)):
            return True
        return False

    # For testing
    def show_coords(self, screen: pygame.Surface, text: pygame.font.Font):
        text = text.render(f"{self.file}, {self.rank}", True, 'black')
        rect = text.get_rect(center=(self.x_pos + self.w // 2,
                                     self.y_pos + self.w // 2))
        screen.blit(text, rect)
