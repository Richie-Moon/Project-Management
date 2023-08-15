import pyffish
import piece
from typing import Type
import engine


class Board:
    def __init__(self) -> None:
        self.LETTER_TO_PIECE = {'p': piece.Pawn, 'n': piece.Knight,
                                'r': piece.Rook, 'q': piece.Queen,
                                'k': piece.King}
        self.NUM_TO_FILE = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f'}

        self.START_BOARD: str = pyffish.start_fen('losalamos')
        self.board_fen = self.START_BOARD
        self.board: list[list[Type[piece.Piece] | None]] = []
        self.moves: list[str] = []

        self.MAX_FILE = 6
        self.MAX_RANK = 6

        self.engine = engine.Engine(["fairy-stockfish_x86-64-bmi2"])

    def new_game(self) -> None:
        # Reset instance variables.
        self.board = []
        self.moves = []

        self.engine.new_game()
        self.fen_to_board(self.START_BOARD)

    def fen_to_board(self, fen: str):
        # Splits the extra info off from the end of the fen
        split_fen = fen.split(' ')
        # Splits each rank into its own item in the list.
        split_fen = split_fen[0].split('/')
        split_fen.reverse()

        for i in range(self.MAX_FILE):
            rank_list = []
            rank = split_fen[i]
            for item in rank:
                try:
                    empty_squares = int(item)
                    rank_list.extend([None] * empty_squares)
                except ValueError:
                    rank_list.append(self.LETTER_TO_PIECE
                                     [item.lower()](item, len(rank_list), i))

            self.board.append(rank_list)

    def update_board(self):
        pass

    def on_square(self, file: int, rank: int) -> Type[piece.Piece] | None:
        """
        Checks whether a square (given by file and rank) is occupied by a
        piece. Returns the piece instance, if there is a piece on the square.
        Otherwise, returns None. Uses 0 indexing.
        """
        return self.board[rank][file]

    def coords_to_square(self, file: int, rank: int) -> str:
        """
        Returns square from given file and rank. Uses 0 indexing.
        E.g. 0, 0 -> a1. 4, 2 -> e3.
        """
        # Add 1 because of 0 indexing.
        return self.NUM_TO_FILE[file] + str(rank + 1)
