import pyffish
import piece
from typing import Type
import engine
import pygame
from piece import Piece


def reverse_items(items: list[str]) -> list[str]:
    """
    Returns the given list with every item reversed.
    :param items: The items to reverse, given in a list.
    :return:
    """
    reversed_items = []
    for item in items:
        reversed_items.append(item[::-1])

    return reversed_items


LEN_SQUARE = 2


class Board:
    def __init__(self) -> None:
        self.LETTER_TO_PIECE = {'p': piece.Pawn, 'n': piece.Knight,
                                'r': piece.Rook, 'q': piece.Queen,
                                'k': piece.King}
        self.NUM_TO_FILE: dict[int, str] = {0: 'a', 1: 'b', 2: 'c', 3: 'd',
                                            4: 'e', 5: 'f'}
        self.FILE_TO_NUM: dict[str, int] = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                                            'e': 4, 'f': 5}

        self.VARIANT = 'losalamos'

        self.START_FEN: str = pyffish.start_fen(self.VARIANT)
        self.board_fen = self.START_FEN
        self.board: list[list[Type[piece.Piece] | None]] = []
        self.moves: list[str] = []

        self.MAX_FILE = 6
        self.MAX_RANK = 6

        # 0 = white, 1 = black
        self.user_side: int = 0  # Could try other ways if int not good
        self.turn = True

        self.engine = engine.Engine(["fairy-stockfish_x86-64-bmi2"])

    def new_game(self, w: int) -> None:
        # Reset instance variables.
        self.board = []
        self.moves = []

        self.engine.new_game()
        self.fen_to_board(self.START_FEN, w)

        if self.user_side == 0:
            self.turn = True
        else:
            self.turn = False

    def fen_to_board(self, fen: str, w: int):
        # Split the extra info off from the end of the fen
        split_fen = fen.split(' ')
        # Splits each rank into its own item in the list.
        split_fen = split_fen[0].split('/')

        if self.user_side == 0:
            split_fen.reverse()
        else:
            split_fen = reverse_items(split_fen)

        for i in range(self.MAX_FILE):
            rank_list = []
            rank = split_fen[i]
            for item in rank:
                try:
                    empty_squares = int(item)
                    rank_list.extend([None] * empty_squares)
                except ValueError:
                    if item.isupper():
                        path = "assets/pieces/white/"
                    else:
                        path = "assets/pieces/black/"
                    img = pygame.image.load(f"{path}{item}.svg")
                    rank_list.append(self.LETTER_TO_PIECE
                                     [item.lower()]
                                     (item, len(rank_list), i, img, w))

            self.board.append(rank_list)

    def move(self, start: tuple[int, int], end: tuple[int, int]) -> \
            Type[Piece] | None:
        """

        :param start: The co-ordinates of the piece to move.
        :param end: The co-ordinates of where the piece should move to.
        :return: The captured Piece, if there was one. None, if there wasn't
        """

        s_file, s_rank = start
        e_file, e_rank = end

        piece = self.board[s_rank][s_file]
        captured = self.board[e_rank][e_file]

        self.board[s_rank][s_file], self.board[e_rank][e_file] = None, piece

        if self.turn:
            start_square = self.coords_to_square(s_file, s_rank)
            end_square = self.coords_to_square(e_file, e_rank)
            if self.user_side == 1:
                self.moves.append(self.switch_side_square(start_square) +
                                  self.switch_side_square(end_square))
            else:
                self.moves.append(start_square + end_square)

        self.engine.update(self.moves)
        self.board_fen = pyffish.get_fen(self.VARIANT, self.START_FEN,
                                         self.moves)

        self.turn = not self.turn
        return captured

    def engine_move(self) -> None:
        best_move = self.engine.get_move()
        # This won't work for promotions. Add len check?
        start = best_move[:LEN_SQUARE]  # first 2 chars
        end = best_move[LEN_SQUARE:]  # last 2 chars

        start_coords = self.square_to_coords(start)
        end_coords = self.square_to_coords(end)

        self.moves.append(start + end)
        if self.user_side == 1:
            self.move(self.switch_side(start_coords),
                      self.switch_side(end_coords))
        else:
            self.move(start_coords, end_coords)

    def switch_side(self, move: tuple[int, int]):
        old_file = move[0]
        old_rank = move[1]

        new_file = self.MAX_FILE - 1 - old_file
        new_rank = self.MAX_RANK - 1 - old_rank

        return new_file, new_rank

    def on_square(self, file: int, rank: int) -> Type[piece.Piece] | None:
        """
        Checks whether a square (given by file and rank) is occupied by a
        piece. Returns the piece instance, if there is a piece on the square.
        Otherwise, returns None. Uses 0 indexing.
        """
        if type(file) != int or type(rank) != int:
            raise TypeError("Please provide integers for parameters `file` "
                            "and `rank`. ")

        if (file < 0 or file > self.MAX_FILE - 1) or \
                (rank < 0 or rank > self.MAX_RANK - 1):
            raise ValueError("Parameters `file` and `rank` must be between 0 "
                             f"and 5 (inclusive). File: {file}, Rank: {rank}")

        return self.board[rank][file]

    def coords_to_square(self, file: int, rank: int) -> str:
        """
        Returns square from given file and rank. Uses 0 indexing.
        E.g. 0, 0 -> a1. 4, 2 -> e3.
        """
        # Add 1 because of 0 indexing.
        return self.NUM_TO_FILE[file] + str(rank + 1)

    def switch_side_square(self, square: str) -> str:
        """

        :param square: The square to switch side
        :return: The switched square
        """
        file, rank = self.square_to_coords(square)

        new_file, new_rank = self.switch_side((file, rank))
        return self.coords_to_square(new_file, new_rank)

    def square_to_coords(self, square: str) -> tuple[int, int]:
        file = self.FILE_TO_NUM[square[0]]
        rank = int(square[1]) - 1
        return file, rank

    def check_end_game(self):
        # TODO
        # Draw by insufficient material
        insufficient_mat = pyffish.has_insufficient_material(self.VARIANT,
                                                             self.board_fen,
                                                             [])

    def print_board(self):
        for rank in self.board:
            txt = ""
            for file in rank:
                if file is None:
                    txt += "0 "
                else:
                    txt += f"{file.letter} "
            print(txt)
        print()
