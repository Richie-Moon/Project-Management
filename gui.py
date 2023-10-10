import pygame
import sys
import ctypes
from button import Button, ImageButton
from typing import Literal
import board
import pygame_widgets
from pygame_widgets.slider import Slider

# Constants
# Colours are stored as tuple[r, g, b] integer values.
BLACK: tuple[int, int, int] = (0, 0, 0)
WHITE: tuple[int, int, int] = (255, 255, 255)


TITLE_SIZE: int = 150
TITLE_POSITION: int = 8

BUTTON_TEXT_SIZE: int = 100
TEXT_BASE_COLOUR: tuple[int, int, int] = (255, 255, 255)
TEXT_HOVER_COLOUR: tuple[int, int, int] = (0, 0, 0)

BUTTON_BASE_COLOUR: tuple[int, int, int] = (0, 0, 0)
BUTTON_HOVER_COLOUR: tuple[int, int, int] = (255, 255, 255)
DARK_GRAY = (16, 16, 16)

BUTTON_GAP: int = 40
HALF: float = 0.5
DOUBLE: int = 2
HEIGHT: int = 160
MENU_BUTTON_WIDTH: int = 530
MENU_BUTTON_HEIGHT: int = 150


board = board.Board()

pygame.init()

# https://stackoverflow.com/questions/68831902/how-to-make-a-pygame-window-
# fullscreen-without-hiding-the-taskbar
screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
if sys.platform == "win32":
    HWND = pygame.display.get_wm_info()['window']
    SW_MAXIMIZE = 3
    ctypes.windll.user32.ShowWindow(HWND, SW_MAXIMIZE)

info = pygame.display.Info()
h = info.current_h
w = info.current_w

bg = pygame.image.load("assets/bg.jpg")
blurred_bg = pygame.image.load("assets/bg_blurred.png")


def get_font(size: int,
             style: Literal["Bold", "Medium", "Regular", "SemiBold"] =
             "Regular") -> pygame.font.Font:
    """
    :param size: Size of the font.
    :param style: Thickness of the font. Must be one of 'Bold', 'Medium',
     'Regular' or 'SemiBold'. Defaults to 'Regular'.

    Returns a pygame Font instance with the desired style and size.
    """

    style = style.capitalize()
    return pygame.font.Font(f"assets/fonts/Ruwudu-{style}.ttf", size)


# https://stackoverflow.com/questions/20002242/how-to-scale-images-to-
# screen-size-in-pygame
def scale_image(image: pygame.Surface, size: tuple[int, int]) \
        -> tuple[pygame.Surface, pygame.Rect]:
    """
    Scales an image to the desired size (given by tuple[width, height])
    without distorting the width/height. Returns the scaled image and it's
    bounding rectangle.
    """
    iwidth, iheight = image.get_size()
    scale = max(size[0] / iwidth, size[1] / iheight)
    new_size = round(iwidth * scale), round(iheight * scale)
    scaled_image = pygame.transform.smoothscale(image, new_size)
    image_rect = scaled_image.get_rect(center=(size[0] // 2, size[1] // 2))
    return scaled_image, image_rect


def display_title() -> None:
    """
    Displays the title to the main menu.
    """

    title_text_1 = get_font(TITLE_SIZE, "Bold").render("MINI", True,
                                                       "white")
    title_text_2 = get_font(TITLE_SIZE, "Bold").render(
        "CHESS", True, "white")

    title_1_rect = title_text_1.get_rect(center=(w * HALF, h /
                                                 TITLE_POSITION))
    title_2_rect = title_text_2.get_rect(center=(w * HALF,
                                                 h / TITLE_POSITION +
                                                 TITLE_SIZE))
    screen.blit(title_text_1, title_1_rect)
    screen.blit(title_text_2, title_2_rect)


blurred_bg_scaled, blurred_bg_rect = scale_image(blurred_bg, (w, h))

back_button = Button(pos=(150, 100), text_input="Back",
                     font=get_font(50, "SemiBold"),
                     base_colour=TEXT_BASE_COLOUR,
                     hover_colour=TEXT_HOVER_COLOUR,
                     bg_base_colour=BUTTON_BASE_COLOUR,
                     bg_hover_colour=BUTTON_HOVER_COLOUR,
                     width=250,
                     height=100,
                     transparent=True)


def main_menu() -> None:
    """
    Displays the main menu. Has the play, settings and tutorial button.
    """
    screen.fill(BLACK)

    # Set scaled background image.
    bg_scaled, rect = scale_image(bg, (w, h))

    # Play button
    play_button = Button(pos=(w * HALF, h * HALF),
                         text_input="PLAY",
                         font=get_font(BUTTON_TEXT_SIZE),
                         base_colour=TEXT_BASE_COLOUR,
                         hover_colour=TEXT_HOVER_COLOUR,
                         bg_base_colour=BUTTON_BASE_COLOUR,
                         bg_hover_colour=BUTTON_HOVER_COLOUR,
                         width=MENU_BUTTON_WIDTH,
                         height=MENU_BUTTON_HEIGHT,
                         transparent=True)

    # Tutorial button
    tutorial_button = Button(pos=(w * HALF, (h * HALF) + HEIGHT + BUTTON_GAP),
                             text_input="TUTORIAL",
                             font=get_font(BUTTON_TEXT_SIZE),
                             base_colour=TEXT_BASE_COLOUR,
                             hover_colour=TEXT_HOVER_COLOUR,
                             bg_base_colour=BUTTON_BASE_COLOUR,
                             bg_hover_colour=BUTTON_HOVER_COLOUR,
                             width=MENU_BUTTON_WIDTH,
                             height=MENU_BUTTON_HEIGHT,
                             transparent=True)

    # Settings button
    settings_button = Button(pos=(w * HALF, (h * HALF) + (HEIGHT * DOUBLE) +
                                  BUTTON_GAP * DOUBLE),
                             text_input="SETTINGS",
                             font=get_font(BUTTON_TEXT_SIZE),
                             base_colour=TEXT_BASE_COLOUR,
                             hover_colour=TEXT_HOVER_COLOUR,
                             bg_base_colour=BUTTON_BASE_COLOUR,
                             bg_hover_colour=BUTTON_HOVER_COLOUR,
                             width=MENU_BUTTON_WIDTH,
                             height=MENU_BUTTON_HEIGHT,
                             transparent=True)

    while True:
        pygame.display.set_caption("Mini Chess")

        mouse_pos = pygame.mouse.get_pos()
        screen.blit(bg_scaled, rect)

        display_title()

        play_button.change_colour(mouse_pos)
        play_button.update(screen)

        tutorial_button.change_colour(mouse_pos)
        tutorial_button.update(screen)

        settings_button.change_colour(mouse_pos)
        settings_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if play_button.check_position(mouse_pos) is True:
                    settings(from_play=True)
                elif tutorial_button.check_position(mouse_pos) is True:
                    tutorial()
                elif settings_button.check_position(mouse_pos) is True:
                    settings(from_play=False)

        pygame.display.update()


def settings(from_play: bool) -> None:
    screen.fill(BLACK)
    pygame.display.set_caption("Settings")

    if from_play:
        play_button = Button(pos=(w * HALF, h * HALF + HEIGHT * DOUBLE +
                                  BUTTON_GAP),
                             text_input="PLAY",
                             font=get_font(BUTTON_TEXT_SIZE, "Medium"),
                             base_colour=TEXT_BASE_COLOUR,
                             hover_colour=TEXT_HOVER_COLOUR,
                             bg_base_colour=BUTTON_BASE_COLOUR,
                             bg_hover_colour=BUTTON_HOVER_COLOUR,
                             width=MENU_BUTTON_WIDTH,
                             height=MENU_BUTTON_HEIGHT,
                             transparent=True)
    elif not from_play:
        done_button = Button(pos=(w * HALF, h * HALF + HEIGHT * DOUBLE +
                                  BUTTON_GAP),
                             text_input="Done",
                             font=get_font(BUTTON_TEXT_SIZE, "Medium"),
                             base_colour=TEXT_BASE_COLOUR,
                             hover_colour=TEXT_HOVER_COLOUR,
                             bg_base_colour=BUTTON_BASE_COLOUR,
                             bg_hover_colour=BUTTON_HOVER_COLOUR,
                             width=MENU_BUTTON_WIDTH,
                             height=MENU_BUTTON_HEIGHT,
                             transparent=True)

    side_white_image = pygame.image.load("assets/pieces/white/king.png")
    side_white = ImageButton(pos=(w * HALF - side_white_image.get_height()
                                  * HALF, h * HALF),
                             text_input="",
                             font=get_font(20), base_colour=BLACK,
                             hover_colour=WHITE, bg_base_colour=BLACK,
                             bg_hover_colour=WHITE,
                             width=side_white_image.get_width(),
                             height=side_white_image.get_height(),
                             transparent=True, image=side_white_image)

    side_black_image = pygame.image.load("assets/pieces/black/king.png")
    side_black = ImageButton(pos=(w * HALF, h * HALF), text_input="",
                             font=get_font(20), base_colour=BLACK,
                             hover_colour=WHITE, bg_base_colour=BLACK,
                             bg_hover_colour=WHITE,
                             width=side_black_image.get_width(),
                             height=side_black_image.get_height(),
                             transparent=True, image=side_black_image)

    MENU_TEXT_SIZE: int = 50

    # Slider Settings
    SLIDER_LENGTH: int = 400
    SLIDER_WIDTH: int = 20
    SLIDER_MIN, SLIDER_MAX = 500, 2800
    STEP: int = 100
    SLIDER_POS = 3

    slider = Slider(screen, int(w * HALF - SLIDER_LENGTH * HALF),
                    int(h * HALF + BUTTON_GAP * SLIDER_POS), SLIDER_LENGTH,
                    SLIDER_WIDTH, min=SLIDER_MIN, max=SLIDER_MAX, step=STEP,
                    initial=board.engine.elo, handleColour=DARK_GRAY)

    while True:
        screen.blit(blurred_bg_scaled, blurred_bg_rect)

        mouse_pos = pygame.mouse.get_pos()

        back_button.update(screen)
        back_button.change_colour(mouse_pos)

        side_black.update(screen)
        side_black.change_colour(mouse_pos)

        side_white.update(screen)
        side_white.change_colour(mouse_pos)

        if from_play:
            play_button.change_colour(mouse_pos)
            play_button.update(screen)
        elif not from_play:
            done_button.change_colour(mouse_pos)
            done_button.update(screen)

        # Engine Difficulty Setting
        difficulty_text = get_font(MENU_TEXT_SIZE).render("Engine Difficulty",
                                                          True, 'white')
        difficulty_text_rect = difficulty_text.get_rect(center=(w * HALF,
                                                                slider.get('y')
                                                                - BUTTON_GAP))
        slider_value_text = get_font(MENU_TEXT_SIZE).render(str(
            slider.getValue()), True, 'white')
        slider_text_rect = slider_value_text.get_rect(center=(w * HALF,
                                                              slider.get('y') +
                                                              BUTTON_GAP *
                                                              DOUBLE))
        for event in pygame.event.get():
            pygame_widgets.update(event)

            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                # Back buttons pressed
                if back_button.check_position(mouse_pos) is True:
                    slider.hide()
                    return

                # White side selected
                elif side_black.check_position(mouse_pos) is True:
                    # TODO give this info to board
                    pass

                # Black side selected
                elif side_black.check_position(mouse_pos) is True:
                    # TODO give this info to board
                    pass

                # Play button pressed
                elif from_play and play_button.check_position(mouse_pos) \
                        is True:
                    board.engine.change_elo(slider.getValue())
                    slider.hide()
                    play()
                    return

                # Done button pressed
                elif not from_play and done_button.check_position(mouse_pos) \
                        is True:
                    board.engine.change_elo(slider.getValue())
                    slider.hide()
                    return

            screen.blit(slider_value_text, slider_text_rect)
            screen.blit(difficulty_text, difficulty_text_rect)

            # Has to be indented so that the slider draws first
            # (otherwise causes flickering)
            pygame.display.update()


def tutorial():
    """
    The tutorial screen. Tells the user how each of the pieces move, how
    promotion works, as well as the rules of chess.
    """
    screen.fill(BLACK)
    screen.blit(blurred_bg_scaled, blurred_bg_rect)
    pygame.display.set_caption("Tutorial")

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()


def play() -> None:
    """
    The current game board.
    """
    board.new_game()
    screen.fill(BLACK)

    while True:
        pygame.display.set_caption("Play")

        mouse_pos = pygame.mouse.get_pos()

        # TODO this is temporary
        play_text = get_font(50).render("This is the PLAY screen.",
                                        True, "white")
        screen.blit(play_text, play_text.get_rect(center=(w // 2, h // 2)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()
