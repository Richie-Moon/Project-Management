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

info = pygame.display.Info()
h = info.current_h
w = info.current_w

bg = pygame.image.load("assets/bg.jpg")


# https://stackoverflow.com/questions/20002242/how-to-scale-images-to-screen-size-in-pygame
def transformScaleKeepRatio(image, size):
    iwidth, iheight = image.get_size()
    scale = max(size[0] / iwidth, size[1] / iheight)
    new_size = (round(iwidth * scale), round(iheight * scale))
    scaled_image = pygame.transform.smoothscale(image, new_size)
    image_rect = scaled_image.get_rect(center = (size[0] // 2, size[1] // 2))
    return scaled_image, image_rect


def main_menu():
    while True:
        pygame.display.set_caption("Mini Chess")

        mouse_pos = pygame.mouse.get_pos()
        image, rect = transformScaleKeepRatio(bg, (w, h))
        screen.blit(image, rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()

main_menu()

pygame.quit()
