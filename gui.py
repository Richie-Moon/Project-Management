import datetime
import os

import pygame
import sys
import ctypes
from button import Button, ImageButton
from typing import Literal
import board
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.toggle import Toggle
from pygame_widgets.textbox import TextBox
from game import Square
import numpy as np

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
MENU_TEXT_SIZE: int = 50

BACK_POS = (150, 100)
BACK_WIDTH = 250
BACK_HEIGHT = 100
BACK_FONT_SIZE = 50

NUM_FILES = 6
NUM_RANKS = 6
NUM_SQUARES = 36
MOVE_LEN = 2

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


def is_even(num: int) -> bool:
    """
    Returns True if `num` is even, False if it's odd.
    :param num: Number to check.
    :return:
    """
    if num % 2 == 0:
        return True
    return False


def coords_to_index(coords: tuple[int, int]) -> int:
    """
    Creates a 6x6 ndarray, and return the index of the coords supplied.
    :param coords: The co-ordinates of the needed index.
    :return: Integer Index corresponding to the co-ordinates given.
    """
    INVERSE = 5
    array = np.arange(NUM_SQUARES).reshape(NUM_FILES, NUM_RANKS)

    # 5 - y co-ord is required due to the ndarray going top to bottom, but the
    # coords being given in bottom to top.
    formatted = (coords[0], INVERSE - coords[1])

    # the [::-1] just reverses the list to the form (y,x) instead of (x,y).
    # Is needed due to the way the ndarray is formatted.
    formatted = formatted[::-1]

    return array[formatted]


def display_title(line1: str, line2: str,
                  style: Literal["Bold", "Medium", "Regular", "SemiBold"]) \
        -> None:
    """
    Displays the title to the main menu.
    """

    title_text_1 = get_font(TITLE_SIZE, style).render(line1, True, WHITE)
    title_text_2 = get_font(TITLE_SIZE, style).render(line2, True, WHITE)

    title_1_rect = title_text_1.get_rect(center=(w * HALF, h /
                                                 TITLE_POSITION))
    title_2_rect = title_text_2.get_rect(center=(w * HALF,
                                                 h / TITLE_POSITION +
                                                 TITLE_SIZE))
    screen.blit(title_text_1, title_1_rect)
    screen.blit(title_text_2, title_2_rect)


blurred_bg_scaled, blurred_bg_rect = scale_image(blurred_bg, (w, h))

back_button = Button(pos=BACK_POS, text_input="Back",
                     font=get_font(BACK_FONT_SIZE, "SemiBold"),
                     base_colour=TEXT_BASE_COLOUR,
                     hover_colour=TEXT_HOVER_COLOUR,
                     bg_base_colour=BUTTON_BASE_COLOUR,
                     bg_hover_colour=BUTTON_HOVER_COLOUR,
                     width=BACK_WIDTH,
                     height=BACK_HEIGHT,
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

        display_title("MINI", "CHESS", "Bold")

        play_button.change_colour(mouse_pos)
        play_button.update(screen)

        tutorial_button.change_colour(mouse_pos)
        tutorial_button.update(screen)

        settings_button.change_colour(mouse_pos)
        settings_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if play_button.check_position(mouse_pos) is True:
                    settings(from_play=True)
                elif tutorial_button.check_position(mouse_pos) is True:
                    tutorial()
                elif settings_button.check_position(mouse_pos) is True:
                    settings(from_play=False)

        pygame.display.update()


def settings(from_play: bool) -> None:
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

    IMAGE_SIZE = 8
    white_image = pygame.image.load("assets/pieces/white/K.svg")
    side_white_image, side_white_rect = scale_image(white_image, (
        white_image.get_height() // IMAGE_SIZE,
        white_image.get_width() // IMAGE_SIZE))

    side_white = ImageButton(pos=(w * HALF - side_white_image.get_width()
                                  * HALF, h * HALF - BUTTON_GAP * DOUBLE),
                             text_input="",
                             font=get_font(BUTTON_TEXT_SIZE),
                             base_colour=BLACK,
                             hover_colour=WHITE, bg_base_colour=BLACK,
                             bg_hover_colour=WHITE,
                             width=side_white_image.get_width(),
                             height=side_white_image.get_height(),
                             transparent=True, image=side_white_image)

    black_image = pygame.image.load("assets/pieces/black/k.svg")
    side_black_image, side_black_rect = scale_image(black_image, (
        black_image.get_height() // IMAGE_SIZE,
        black_image.get_width() // IMAGE_SIZE))

    side_black = ImageButton(pos=(w * HALF + side_black_rect.height * HALF,
                                  h * HALF - BUTTON_GAP * DOUBLE),
                             text_input="",
                             font=get_font(BUTTON_TEXT_SIZE),
                             base_colour=BLACK,
                             hover_colour=WHITE, bg_base_colour=BLACK,
                             bg_hover_colour=WHITE,
                             width=side_black_rect.width,
                             height=side_black_rect.height,
                             transparent=True, image=side_black_image)

    if board.user_side == 0:
        side_white.enable()
    elif board.user_side == 1:
        side_black.enable()

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

    # Toggle Settings
    TOGGLE_WIDTH = 60
    TOGGLE_HEIGHT = 25
    TOGGLE_X_ADJUST = 3
    TOGGLE_Y_ADJUST = 15

    # Colourblind setting
    colourblind_text = get_font(MENU_TEXT_SIZE).render("Colourblind Mode",
                                                       True, WHITE)

    colourblind_rect = colourblind_text.get_rect(
        center=(w * HALF - TOGGLE_WIDTH * 1, side_black.y_pos -
                BUTTON_GAP * DOUBLE * DOUBLE))

    toggle = Toggle(screen, int(w * HALF + TOGGLE_WIDTH * TOGGLE_X_ADJUST),
                    colourblind_rect.top + TOGGLE_Y_ADJUST, TOGGLE_WIDTH,
                    TOGGLE_HEIGHT)

    while True:
        screen.fill(BLACK)

        screen.blit(blurred_bg_scaled, blurred_bg_rect)

        display_title("SETTINGS", "", "Medium")

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

        # Side selection setting
        side_select_text = get_font(MENU_TEXT_SIZE).render("Side Select",
                                                           True, WHITE)
        side_select_rect = side_select_text.get_rect(
            center=(w * HALF, side_white.y_pos - BUTTON_GAP * DOUBLE))

        # Engine Difficulty Setting
        difficulty_text = get_font(MENU_TEXT_SIZE).render("Engine Difficulty",
                                                          True, WHITE)
        difficulty_text_rect = difficulty_text.get_rect(
            center=(w * HALF, slider.get('y') - BUTTON_GAP))

        slider_value_text = get_font(MENU_TEXT_SIZE).render(str(
            slider.getValue()), True, 'white')

        slider_text_rect = slider_value_text.get_rect(
            center=(w * HALF, slider.get('y') + BUTTON_GAP * DOUBLE))

        events = pygame.event.get()
        pygame_widgets.update(events)
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                # Back buttons pressed
                if back_button.check_position(mouse_pos) is True:
                    toggle.hide()
                    slider.hide()
                    return

                # White side selected
                elif side_white.check_position(mouse_pos) is True:
                    side_white.enable()
                    side_black.disable()
                    board.user_side = 0

                # Black side selected
                elif side_black.check_position(mouse_pos) is True:
                    side_black.enable()
                    side_white.disable()
                    board.user_side = 1

                # Play button pressed
                elif from_play and play_button.check_position(mouse_pos) \
                        is True:
                    board.engine.change_elo(slider.getValue())
                    slider.hide()
                    toggle.hide()
                    play(toggle.getValue())
                    return

                # Done button pressed
                elif not from_play and done_button.check_position(mouse_pos) \
                        is True:
                    board.engine.change_elo(slider.getValue())
                    slider.hide()
                    toggle.hide()
                    return

            screen.blit(side_select_text, side_select_rect)

            screen.blit(slider_value_text, slider_text_rect)
            screen.blit(difficulty_text, difficulty_text_rect)

            screen.blit(colourblind_text, colourblind_rect)

            # Has to be indented so that the slider draws first
            # (otherwise causes flickering)
            pygame.display.update()



def tutorial():
    """
    The tutorial screen. Tells the user how each of the pieces move, how
    promotion works, as well as the rules of chess.
    """

    pygame.display.set_caption("Tutorial")
    path = "assets/pieces/white/"
    TUTO_TEXT_SIZE = 40

    while True:
        screen.fill(BLACK)
        screen.blit(blurred_bg_scaled, blurred_bg_rect)

        mouse_pos = pygame.mouse.get_pos()

        back_button.update(screen)
        back_button.change_colour(mouse_pos)

        img_size = 70

        title_size = 100
        title = get_font(title_size, "Medium").render("TUTORIAL", True, WHITE)
        title_rect = title.get_rect(center=(w * HALF, h / TITLE_POSITION))
        screen.blit(title, title_rect)

        intro = get_font(TUTO_TEXT_SIZE).render(
            "Los Alamos Chess is a chess variant played on a 6x6 board "
            "without bishops.", True, WHITE)
        intro_rect = intro.get_rect(center=(w * HALF, title_rect.bottom))
        screen.blit(intro, intro_rect)

        goal = get_font(TUTO_TEXT_SIZE).render(
            "The goal of the game is to checkmate the opponent's king.",
            True, WHITE)
        TXT_ADJUST = 15
        LINE_BREAK = 40
        goal_rect = goal.get_rect(center=(w * HALF, intro_rect.bottom +
                                          TXT_ADJUST))
        screen.blit(goal, goal_rect)

        pawn_img = scale_image(pygame.image.load(f"{path}P.svg"),
                               (img_size, img_size))
        pawn_img_rect = pawn_img[1]
        pawn = get_font(TUTO_TEXT_SIZE).render(
            "Pawns are the most basic piece.", True, WHITE)
        pawn_rect = pawn.get_rect(center=(w * HALF, goal_rect.bottom +
                                          TXT_ADJUST + LINE_BREAK))
        pawn2 = get_font(TUTO_TEXT_SIZE).render(
            "They can move 1 square up, and can capture enemy pieces "
            "diagonally.", True, WHITE)
        pawn2_rect = pawn2.get_rect(center=(w * HALF, pawn_rect.bottom +
                                            TXT_ADJUST))
        pawn_img_rect.center = (pawn_rect.left - img_size * HALF, pawn_rect.y
                                + TXT_ADJUST)
        screen.blit(pawn_img[0], pawn_img_rect)
        screen.blit(pawn, pawn_rect)
        screen.blit(pawn2, pawn2_rect)

        rook_img = scale_image(pygame.image.load(f"{path}R.svg"),
                               (img_size, img_size))
        rook_img_rect = rook_img[1]
        rook = get_font(TUTO_TEXT_SIZE).render(
            "The rook can move vertically and horizontally for any number of "
            "squares.", True, WHITE)
        rook_rect = rook.get_rect(center=(w * HALF, pawn2_rect.bottom +
                                          TXT_ADJUST + LINE_BREAK))
        rook_img_rect.center = (rook_rect.left - img_size * HALF,
                                rook_rect.y + TXT_ADJUST)
        screen.blit(rook, rook_rect)
        screen.blit(rook_img[0], rook_img_rect)

        knight = get_font(TUTO_TEXT_SIZE).render(
            "The knight moves 2 squares in one direction, and 1 square in "
            "another, like an 'L'.", True, WHITE)
        knight_rect = knight.get_rect(center=(w * HALF, rook_rect.bottom +
                                              TXT_ADJUST + LINE_BREAK))
        knight_img = scale_image(pygame.image.load(f"{path}N.svg"),
                                 (img_size, img_size))
        knight_img_rect = knight_img[1]
        knight_img_rect.center = (knight_rect.left - img_size * HALF,
                                  knight_rect.y + TXT_ADJUST)
        knight2 = get_font(TUTO_TEXT_SIZE).render("They can jump over other "
                                                  "pieces.", True, WHITE)
        knight2_rect = knight2.get_rect(center=(w * HALF, knight_rect.bottom +
                                                TXT_ADJUST))
        screen.blit(knight_img[0], knight_img_rect)
        screen.blit(knight, knight_rect)
        screen.blit(knight2, knight2_rect)

        queen = get_font(TUTO_TEXT_SIZE).render(
            "The queen can move horizontally, vertically, and diagonally.",
            True, WHITE)
        queen_img = scale_image(pygame.image.load(f"{path}Q.svg"),
                                (img_size, img_size))
        queen_img_rect = queen_img[1]
        queen_rect = queen.get_rect(center=(w * HALF, knight2_rect.bottom +
                                            TXT_ADJUST + LINE_BREAK))
        queen_img_rect.center = (queen_rect.left - img_size * HALF,
                                 queen_rect.y + TXT_ADJUST)
        screen.blit(queen_img[0], queen_img_rect)
        screen.blit(queen, queen_rect)

        king = get_font(TUTO_TEXT_SIZE).render(
            "The king is the most important piece. It can move 1 square in any"
            " direction. ", True, WHITE)
        king_rect = king.get_rect(center=(w * HALF, queen_rect.bottom
                                          + TXT_ADJUST + LINE_BREAK))
        king_img = scale_image(pygame.image.load(f"{path}K.svg"),
                               (img_size, img_size))
        king_img_rect = king_img[1]
        king_img_rect.center = (king_rect.left - img_size * HALF,
                                king_rect.y + TXT_ADJUST)

        screen.blit(king_img[0], king_img_rect)
        screen.blit(king, king_rect)

        promo = get_font(TUTO_TEXT_SIZE).render(
            "If a pawn reaches the other end of the board, it will "
            "promote to a more powerful piece", True, WHITE)
        promo_rect = promo.get_rect(center=(w * HALF, king_rect.bottom +
                                            TXT_ADJUST + LINE_BREAK))
        screen.blit(promo, promo_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if back_button.check_position(mouse_pos):
                    return

        pygame.display.update()


def play(cb_mode: bool) -> None:
    """
    The current game board.
    """

    def reset_squares():
        for sq in squares:
            sq.dot = False

    def reset_shade():
        for sq in squares:
            sq.shade = False

    def save_game(name: str, game_result: int, end_reason: str) -> None:
        path = "games"
        num_games = len(os.listdir(path))
        datetime_now = datetime.datetime.now()

        formatted_date = datetime_now.strftime("%d %B %Y")
        formatted_time = datetime_now.strftime("%I:%M.%S %p")

        if not bool(board.user_side):
            white = name
            black = "Fairy-Stockfish"
        else:
            white = "Fairy-Stockfish"
            black = name

        if game_result == DRAW:
            winner = "Draw "
        elif game_result == WHITE_WIN:
            winner = "White wins "
        else:
            winner = "Black wins "

        with open(f"{path}/{name}{num_games + 1}.txt", 'x') as file:
            file.write(f"User: {name}\n\n")
            file.write(f"Date: {formatted_date}\n")
            file.write(f"Time: {formatted_time}\n\n")
            file.write(f"Engine ELO: {board.engine.elo}\n\n")
            file.write(f"White: {white}\n")
            file.write(f"Black: {black}\n")
            file.write(f"Result: {winner}{end_reason}\n\n")

            count = 1
            for move in board.moves:
                file.write(f"{count}. {move} ")
                count += 1

    screen.fill(BLACK)

    pygame.display.set_caption("Play")

    # The rect containing the full board. Resizes to fit window.
    TOPLEFT = (0, 0)
    board_rect = pygame.Rect(TOPLEFT, (h, h))
    square_width: int = board_rect.width // NUM_FILES
    board.new_game(square_width)

    if board.engine.is_ready() is False:
        print("Engine failed to start or is not ready")
        return

    # Draw board
    squares: list[Square] = []
    for i in range(NUM_FILES):
        for j in range(NUM_RANKS):
            # If both square coords are even or odd, they are light.
            # Otherwise, it is dark.
            if ((is_even(i) and is_even(j)) or
                    (not is_even(i) and not is_even(j))):
                light = True
            else:
                light = False

            sq = Square((j * square_width, i * square_width), light,
                        square_width, j, NUM_RANKS - 1 - i, cb_mode, False)

            sq.draw(screen)
            squares.append(sq)

    selected_piece = None
    selected_square = None
    user_captured = []
    engine_captured = []

    TXT_SIZE = 70
    WHITE_WIN = 0
    BLACK_WIN = 1
    DRAW = -1

    while True:
        screen.fill(BLACK)

        # Place images pieces onto board
        for square in squares:
            piece = board.board[square.rank][square.file]
            if piece is not None:
                square.has_piece = True
                square.draw(screen, piece.image)
            else:
                square.has_piece = False
                square.draw(screen)

        LEFT = board_rect.right + BUTTON_GAP * DOUBLE

        game_end = board.check_end_game()
        if game_end is not None:
            result = game_end['result']
            reason = game_end['reason']
            texts = []

            # The user won
            if (result == WHITE_WIN and board.user_side == 0) or \
                    (result == BLACK_WIN and board.user_side == 1):
                win = "YOU WIN!"
                col = (124, 252, 0)
            elif result == DRAW:
                win = "Draw"
                col = (130, 130, 130)
            else:
                win = "You lose"
                col = (255, 0, 0)

            reason_text = get_font(MENU_TEXT_SIZE).render(reason, True, WHITE)
            reason_rect = reason_text.get_rect(left=LEFT, centery=h * HALF)
            texts.append(reason_text)

            win_text = get_font(TXT_SIZE, "SemiBold").render(win, True, col)
            win_rect = win_text.get_rect(centerx=reason_rect.centerx,
                                         bottom=reason_rect.top)
            texts.append(win_text)

            GRAY = (70, 70, 70)
            LIGHT_GRAY = (140, 140, 140)
            TEMP = 0
            SMALL_FONT_SIZE = 30

            enter_name = get_font(SMALL_FONT_SIZE).render("Enter Name: ", True,
                                                          WHITE)
            enter_name_rect = enter_name.get_rect(centerx=reason_rect.centerx,
                                                  top=reason_rect.bottom)
            texts.append(enter_name)

            disclaimer = get_font(SMALL_FONT_SIZE).render(
                "Do not enter sensitive information", True, WHITE)
            disclaimer_rect = disclaimer.get_rect(centerx=reason_rect.centerx,
                                                  top=enter_name_rect.bottom)
            texts.append(disclaimer)

            textbox = TextBox(screen, TEMP,
                              disclaimer_rect.bottom,
                              BACK_WIDTH, BACK_HEIGHT,
                              font=get_font(MENU_TEXT_SIZE),
                              colour=LIGHT_GRAY, textColour=WHITE)

            save_exit_button = Button(
                pos=(reason_rect.centerx,
                     textbox.getY() + BUTTON_GAP * 4),
                text_input="Save Game",
                font=get_font(MENU_TEXT_SIZE),
                base_colour=TEXT_BASE_COLOUR,
                hover_colour=TEXT_HOVER_COLOUR,
                bg_base_colour=GRAY,
                bg_hover_colour=LIGHT_GRAY,
                width=BACK_WIDTH, height=BACK_HEIGHT,
                transparent=False)

            textbox.setX(reason_rect.centerx - textbox.getWidth() * HALF)

            contain_surface = pygame.Surface((w - board_rect.w, h))
            contain_surface.fill(BLACK)

            while True:
                mouse_pos = pygame.mouse.get_pos()

                screen.blit(contain_surface, (board_rect.right, 0))

                save_exit_button.update(screen)
                save_exit_button.change_colour(mouse_pos)

                screen.blit(win_text, win_rect)
                screen.blit(reason_text, reason_rect)
                screen.blit(enter_name, enter_name_rect)
                screen.blit(disclaimer, disclaimer_rect)

                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONUP:
                        # Button clicked
                        if save_exit_button.check_position(mouse_pos):
                            save_game(textbox.getText(), result, reason)
                            textbox.hide()
                            return
                pygame_widgets.update(events)
                pygame.display.update()

        # Display Engine Info
        info_text = get_font(TXT_SIZE).render("Fairy-Stockfish", True, WHITE)
        info_rect = info_text.get_rect(left=LEFT, top=BUTTON_GAP * DOUBLE)
        screen.blit(info_text, info_rect)

        elo_text = get_font(MENU_TEXT_SIZE).render(f"ELO: {board.engine.elo}",
                                                   True, WHITE)
        elo_rect = elo_text.get_rect(left=LEFT, top=info_rect.bottom)
        screen.blit(elo_text, elo_rect)

        # Display Turn
        if board.turn:
            side_text = get_font(TXT_SIZE).render("Your", True, WHITE)

        else:
            side_text = get_font(TXT_SIZE).render("Opponent", True, WHITE)

        TXT_ADJUST = 10

        turn_text = get_font(TXT_SIZE).render("Turn", True, WHITE)

        turn_rect = turn_text.get_rect(left=LEFT, bottom=h - BUTTON_GAP)
        side_rect = side_text.get_rect(centerx=turn_rect.centerx,
                                       bottom=turn_rect.top + TXT_ADJUST)

        screen.blit(side_text, side_rect)
        screen.blit(turn_text, turn_rect)

        pygame.display.update()

        if board.turn is False:
            start, end = board.engine_move()
            reset_shade()
            squares[coords_to_index(start)].shade = True
            squares[coords_to_index(end)].shade = True
            continue

        # # Show square coords for testing.
        # for sq in squares:
        #     sq.show_coords(screen, get_font(30))

        # Pygame event loop
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()

                for square in squares:
                    clicked = square.check_position(mouse_pos)
                    if clicked:
                        if square.has_piece:
                            piece = board.board[square.rank][square.file]
                            # if the piece is not the users colour
                            if piece.letter.isupper() is not bool(
                                    board.user_side):
                                reset_squares()
                                selected_piece = piece
                                selected_square = square
                                valid_moves = piece.valid_moves(board)
                                for location in valid_moves:
                                    squares[coords_to_index(location
                                                            [:MOVE_LEN])].dot \
                                        = True

                        if square.dot:
                            # move selected piece to dot.
                            captured = board.move((selected_piece.file,
                                                   selected_piece.rank),
                                                  (square.file, square.rank))
                            reset_shade()
                            square.shade = True
                            selected_square.shade = True
                            if captured is not None:
                                # will be True if user playing white, False if
                                # user playing black.
                                user_side = not board.user_side
                                if user_side is captured.letter.islower():
                                    user_captured.append(captured)
                                else:
                                    engine_captured.append(captured)

                            square.has_piece = True
                            squares[coords_to_index((selected_piece.file,
                                                     selected_piece.rank))]. \
                                has_piece = False

                            selected_piece.file = square.file
                            selected_piece.rank = square.rank
                            selected_piece.update()

                            reset_squares()

        pygame.display.update()
