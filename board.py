import pyffish
import piece


class Board:
    def __init__(self):
        self.START_BOARD: str = pyffish.start_fen('losalamos')  # default starting position in fen.
        self.board_fen = self.START_BOARD
        self.board: list[list[piece.Piece | None]] = []  # 2D list of the board
        self.moves: list[str] = []

        self.MAX_FILE = 6
        self.MAX_RANK = 6

    def new_game(self):
        self.board = []
        self.moves = []

        # Splits the extra info off from the end of the fen
        split_fen = self.START_BOARD.split(' ')
        # Splits each rank into its own item in the list.
        split_fen = split_fen[0].split('/')
        split_fen.reverse()

        for i in range(self.MAX_RANK):
            for j in range(self.MAX_FILE):
                rank = split_fen[i]
                for item in rank:
                    try:
                        item = int(item)
                        # TODO append None item num of times
                    except ValueError:
                        # there is a piece
                        pass


    def make_move(self, start, end):
        # convert to fen changes?
        pass

    def on_square(self, file, rank) -> piece.Piece | None:
        """
        Checks whether a square (given by file and rank) is occupied by a
        piece. Returns the piece instance, if there is a piece on the square.
        Otherwise, returns None.
        """
        pass

board = Board()
board.new_game()
