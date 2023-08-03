import board


class Piece:
    def __init__(self, piece_type, side):
        self.type = piece_type
        self.side = side
        self.file = 'e'
        self.rank = 5  # Get this info from board class/method

        self.starting_file = 'e'
        if self.type == 'white':
            self.starting_rank = 2
        elif self.type == 'black':
            self.starting_rank = 6


class Pawn(Piece):
    def __init__(self):
        super().__init__("pawn", "white")

    def valid_moves(self) -> list:
        if self.side == 'white':
            moves = []
            moves.append(self.file + str(self.rank + 1))

            return moves
