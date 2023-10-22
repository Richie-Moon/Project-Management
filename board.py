import pyffish
import piece
from typing import Type
import engine
import pygame


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


class Board:
    def __init__(self) -> None:
        self.LETTER_TO_PIECE = {'p': piece.Pawn, 'n': piece.Knight,
                                'r': piece.Rook, 'q': piece.Queen,
                                'k': piece.King}
        self.NUM_TO_FILE = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f'}

        self.START_FEN: str = pyffish.start_fen('losalamos')
        self.board_fen = self.START_FEN
        self.board: list[list[Type[piece.Piece] | None]] = []
        self.moves: list[str] = []

        self.MAX_FILE = 6
        self.MAX_RANK = 6

        # 0 = white, 1 = black
        self.user_side: int = 0  # Could try other ways if int not good

        self.engine = engine.Engine(["fairy-stockfish_x86-64-bmi2"])

    def new_game(self, w: int) -> None:
        # Reset instance variables.
        self.board = []
        self.moves = []

        self.engine.new_game()
        self.fen_to_board(self.START_FEN, w)

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

    def move(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        # Could return something if needed (like piece, or captured piece)

        print(self.board)
        s_file, s_rank = start
        e_file, e_rank = end

        piece = self.board[s_file][s_rank]

        self.board[s_file][s_rank], self.board[e_file][e_rank] = None, piece

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
                             "and 5 (inclusive). ")

        return self.board[rank][file]

    def coords_to_square(self, file: int, rank: int) -> str:
        """
        Returns square from given file and rank. Uses 0 indexing.
        E.g. 0, 0 -> a1. 4, 2 -> e3.
        """
        # Add 1 because of 0 indexing.
        return self.NUM_TO_FILE[file] + str(rank + 1)
