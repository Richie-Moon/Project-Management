import pygame
import sys
import ctypes
from button import Button
from typing import Literal

# Constants
BLACK = (0, 0, 0)

TITLE_SIZE = 150
HALF = 2
TITLE_POSITION = 8

BUTTON_TEXT_SIZE = 120
TEXT_BASE_COLOUR = (255, 255, 255)
TEXT_HOVER_COLOUR = (0, 0, 0)

BUTTON_BASE_COLOUR = (0, 0, 0)
BUTTON_HOVER_COLOUR = (255, 255, 255)

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


def get_font(size: int,
             style: Literal["Bold", "Medium", "Regular", "SemiBold"] =
             "Regular") -> pygame.font.Font:
    style = style.capitalize()
    return pygame.font.Font(f"assets/fonts/Ruwudu-{style}.ttf", size)


# https://stackoverflow.com/questions/20002242/how-to-scale-images-to-
# screen-size-in-pygame
def scale_image(image, size):
    iwidth, iheight = image.get_size()
    scale = max(size[0] / iwidth, size[1] / iheight)
    new_size = round(iwidth * scale), round(iheight * scale)
    scaled_image = pygame.transform.smoothscale(image, new_size)
    image_rect = scaled_image.get_rect(center=(size[0] // 2, size[1] // 2))
    return scaled_image, image_rect


def display_title():
    title_text_1 = get_font(TITLE_SIZE, "Bold").render("MINI", True,
                                                       "white")
    title_text_2 = get_font(TITLE_SIZE, "Bold").render(
        "CHESS", True, "white")

    title_1_rect = title_text_1.get_rect(center=(w / HALF, h /
                                                 TITLE_POSITION))
    title_2_rect = title_text_2.get_rect(center=(w / HALF,
                                                 h / TITLE_POSITION +
                                                 TITLE_SIZE))
    screen.blit(title_text_1, title_1_rect)
    screen.blit(title_text_2, title_2_rect)


def main_menu():
    screen.fill(BLACK)
    pygame.display.set_caption("Mini Chess")

    # Set scaled background image.
    bg_scaled, rect = scale_image(bg, (w, h))
    # Play button
    play_button = Button(pos=(w // HALF, h // HALF), text_input="PLAY",
                         font=get_font(BUTTON_TEXT_SIZE),
                         base_colour=TEXT_BASE_COLOUR,
                         hover_colour=TEXT_HOVER_COLOUR,
                         bg_base_colour=BUTTON_BASE_COLOUR,
                         bg_hover_colour=BUTTON_HOVER_COLOUR,
                         transparent=True)

    pygame.display.update()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(bg_scaled, rect)

        display_title()

        play_button.change_colour(mouse_pos)
        play_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif (event.type == pygame.MOUSEBUTTONUP and
                  play_button.check_position(mouse_pos) is True):
                play()

        pygame.display.update()


def settings():
    while True:
        moouse_pos = pygame.mouse.get_pos()
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


def play():
    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(BLACK)

        play_text = get_font(50).render("This is the PLAY screen. ",
                                        True, "white")
        screen.blit(play_text, play_text.get_rect(center=(w//2, h//2)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()


main_menu()
