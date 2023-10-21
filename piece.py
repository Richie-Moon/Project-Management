class Piece:
    def __init__(self, letter: str, file: int, rank: int):
        self.letter = letter
        self.file = file  # 0-5
        self.rank = rank  # 0-5

        self.LEFT = False
        self.RIGHT = False
        self.TOP = False
        self.BOTTOM = False

        self.MAX_FILE = 5
        self.MAX_RANK = 5
        self.MIN_FILE = 0
        self.MIN_RANK = 0

        if self.file == self.MIN_FILE:
            self.LEFT = True
        elif self.file == self.MAX_FILE:
            self.RIGHT = True

        if self.rank == self.MIN_RANK:
            self.BOTTOM = True
        elif self.rank == self.MAX_RANK:
            self.TOP = True

    def square(self) -> tuple[int, int]:
        return self.file, self.rank

    # def print_info(self):
    #     print(self.file)
    #     print(self.rank)


class Pawn(Piece):
    def __init__(self, letter: str, file: int, rank: int):
        super().__init__(letter, file, rank)

    def valid_moves(self, board) -> list:
        moves = []

        if self.letter.isupper():  # White
            next_square = (self.file, self.rank + 1)
            left = (self.file - 1, self.rank + 1)
            right = (self.file + 1, self.rank + 1)
        else:  # Black
            next_square = (self.file, self.rank - 1)
            left = (self.file - 1, self.rank - 1)
            right = (self.file + 1, self.rank - 1)

        on_next_square = board.on_square(*next_square)

        if on_next_square is None:
            moves.append(next_square)

        # Skip checking for captures on left/right if the piece is on the
        # left/right most file.
        if not self.LEFT:
            on_left = board.on_square(*left)
            # If there is a piece and the piece is not the same colour.
            if (on_left and on_left.letter.isupper() is not
                    self.letter.isupper()):
                moves.append(left)
        if not self.RIGHT:
            on_right = board.on_square(*right)
            if (on_right and on_right.letter.isupper() is not
                    self.letter.isupper()):
                moves.append(right)

        return moves


class Knight(Piece):
    def __init__(self, letter: str, file: int, rank: int):
        super().__init__(letter, file, rank)

    def valid_moves(self) -> list:
        moves = []
        return moves


class Rook(Piece):
    def __init__(self, letter: str, file: int, rank: int):
        super().__init__(letter, file, rank)

    def valid_moves(self) -> list:
        moves = []
        return moves


class Queen(Piece):
    def __init__(self, letter: str, file: int, rank: int):
        super().__init__(letter, file, rank)

    def valid_moves(self) -> list:
        moves = []
        return moves


class King(Piece):
    def __init__(self, letter: str, file: int, rank: int):
        super().__init__(letter, file, rank)

    def valid_moves(self) -> list:
        moves = []
        return moves


