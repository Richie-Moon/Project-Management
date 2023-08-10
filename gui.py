import pygame
import sys
import ctypes

pygame.init()

# https://stackoverflow.com/questions/68831902/how-to-make-a-pygame-window-
# fullscreen-without-hiding-the-taskbar
screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
if sys.platform == "win32":
    HWND = pygame.display.get_wm_info()['window']
    SW_MAXIMIZE = 3
    ctypes.windll.user32.ShowWindow(HWND, SW_MAXIMIZE)

bg = pygame.image.load("assets/BGimage.png")


def main_menu():
    while True:
        pygame.display.set_caption("Mini Chess")

        mouse_pos = pygame.mouse.get_pos()
        screen.blit(bg, (0, 0))
        pygame.display.update()


main_menu()

pygame.quit()
