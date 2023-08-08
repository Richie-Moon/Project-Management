class Piece:
    def __init__(self, letter: str, file: int, rank: int):
        self.letter = letter
        self.file = file
        self.rank = rank

        # do I even need this idk
        # if self.letter.isupper():
        #   self.starting_rank = 0  # Default for all pieces other than pawns.
        # elif self.letter.islower():
        #     self.starting_rank = 5


class Pawn(Piece):
    def __init__(self, letter: str, file: int, rank: int):
        super().__init__(letter, file, rank)
        self.starting_rank = 1

    def valid_moves(self) -> list:
        if self.letter.isupper():
            moves = []
            # do da stuff
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

