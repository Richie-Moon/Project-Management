import piece


class Board:
    def __init__(self):
        self.DEFAULT_BOARD = ""  # default starting position in fen.
        self.board = ""  # fen string?

    def make_move(self, start, end):
        # convert to fen changes?
        pass

    def is_occupied(self, file, rank) -> bool | piece.Piece:
        """
        Checks whether a square (given by file and rank) is occupied by a
        piece. Returns the piece instance, if there is a piece on the square.
        Otherwise, returns False.
        """
        pass
