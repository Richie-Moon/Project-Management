class Piece:
    def __init__(self, letter: str, file: int, rank: int):
        self.letter = letter
        self.file = file  # 0-5
        self.rank = rank  # 0-5
        self.num_to_file = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f'}

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

    def square(self):
        return self.num_to_file[self.file] + str(self.rank + 1)

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

        if on_next_square is None:  # TODO change this
            moves.append(self.num_to_file[self.file] + str(self.rank + 2))

        # Skip checking for captures on left/right if the piece is on the
        # left/right most file.
        if not self.LEFT:
            on_left = board.on_square(*left)
            if on_left:
                moves.append((self.file - 1, self.rank + 2))
        if not self.RIGHT:
            on_right = board.on_square(*right)
            if on_right:
                moves.append(self.num_to_file[self.file + 1] + str(self.rank + 2))

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


