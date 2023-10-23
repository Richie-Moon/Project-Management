import pygame


class Piece:
    def __init__(self, letter: str, file: int, rank: int,
                 image: pygame.Surface, w: float):
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

        self.w = w
        self.image = pygame.transform.smoothscale(image, (w, w))

        self.update()

    def square(self) -> tuple[int, int]:
        return self.file, self.rank

    def update(self):
        if self.file == self.MIN_FILE:
            self.LEFT = True
        elif self.file == self.MAX_FILE:
            self.RIGHT = True

        if self.rank == self.MIN_RANK:
            self.BOTTOM = True
        elif self.rank == self.MAX_RANK:
            self.TOP = True

    def can_move(self, square) -> bool:
        """If there is no piece on the square, or the piece is an enemy
        piece"""
        if square is None or square.letter.isupper() is \
                self.letter.islower():
            return True
        return False

    # def print_info(self):
    #     print(self.file)
    #     print(self.rank)


class Pawn(Piece):
    def __init__(self, letter: str, file: int, rank: int,
                 image: pygame.Surface, w: int):
        super().__init__(letter, file, rank, image, w)

    def valid_moves(self, board) -> list:
        moves = []

        next_square = (self.file, self.rank + 1)
        left = (self.file - 1, self.rank + 1)
        right = (self.file + 1, self.rank + 1)

        on_next_square = board.on_square(*next_square)

        if on_next_square is None:
            moves.append(next_square)

        # Skip checking for captures on left/right if the piece is on the
        # left/right most file.
        if not self.LEFT:
            on_left = board.on_square(*left)
            # If there is a piece and the piece is not the same colour.
            if (on_left and on_left.letter.isupper() is
                    not self.letter.isupper()):
                moves.append(left)

        if not self.RIGHT:
            on_right = board.on_square(*right)
            if (on_right and on_right.letter.isupper() is not
                    self.letter.isupper()):
                moves.append(right)

        return moves


class Knight(Piece):
    def __init__(self, letter: str, file: int, rank: int,
                 image: pygame.Surface, w: int):
        super().__init__(letter, file, rank, image, w)

    def valid_moves(self, board) -> list:
        moves = []

        if not self.RIGHT:
            right = self.file + 1

            # 2 up, 1 right
            if self.rank + 2 <= self.MAX_RANK:
                move_right = (right, self.rank + 2)
                on_up_right = board.on_square(*move_right)
                if self.can_move(on_up_right):
                    moves.append(move_right)

            # 2 down, 1 right
            if self.rank - 2 >= self.MIN_RANK:
                move_right = (right, self.rank - 2)
                on_down_right = board.on_square(*move_right)
                if self.can_move(on_down_right):
                    moves.append(move_right)

        if not self.LEFT:
            left = self.file - 1

            # 2 up, 1 left
            if self.rank + 2 <= self.MAX_RANK:
                move_left = (left, self.rank + 2)
                on_up_left = board.on_square(*move_left)
                if self.can_move(on_up_left):
                    moves.append(move_left)

            # 2 down, 1 left
            if self.rank - 2 >= self.MIN_RANK:
                move_left = (left, self.rank - 2)
                on_down_left = board.on_square(*move_left)
                if self.can_move(on_down_left):
                    moves.append(move_left)

        if not self.TOP:
            up = self.rank + 1

            # 2 right, 1 up
            if self.file + 2 <= self.MAX_FILE:
                move_up = (self.file + 2, up)
                on_right_up = board.on_square(*move_up)
                if self.can_move(on_right_up):
                    moves.append(move_up)

            # 2 left, 1 up
            if self.file - 2 >= self.MIN_FILE:
                move_up = (self.file - 2, up)
                on_left_up = board.on_square(*move_up)
                if self.can_move(on_left_up):
                    moves.append(move_up)

        if not self.BOTTOM:
            down = self.rank - 1

            # 2 right, 1 down
            if self.file + 2 <= self.MAX_FILE:
                move_down = (self.file + 2, down)
                on_right_down = board.on_square(move_down)
                if self.can_move(on_right_down):
                    moves.append(move_down)

            # 2 left, 1 down
            if self.file - 2 >= self.MIN_FILE:
                move_down = (self.file - 2, down)
                on_left_down = board.on_square(move_down)
                if self.can_move(on_left_down):
                    moves.append(move_down)

        return moves


class Rook(Piece):
    def __init__(self, letter: str, file: int, rank: int,
                 image: pygame.Surface, w: int):
        super().__init__(letter, file, rank, image, w)

    def valid_moves(self, board) -> list:
        moves = []

        # Check upwards
        rank = self.rank
        while rank < self.MAX_RANK:
            next_square = (self.file, rank + 1)
            on_next_square = board.on_square(*next_square)

            # If there is no piece on the next square.
            if on_next_square is None:
                moves.append(next_square)
                rank += 1
            # If there is an enemy piece on the next square
            elif on_next_square.letter.isupper() is self.letter.islower():
                moves.append(next_square)
                break
            else:
                break

        # Check downwards
        rank = self.rank
        while rank > self.MIN_RANK:
            next_square = (self.file, rank - 1)
            on_next_square = board.on_square(*next_square)

            if on_next_square is None:
                moves.append(next_square)
                rank -= 1
            elif on_next_square.letter.isupper() is self.letter.islower():
                moves.append(next_square)
                break
            else:
                break

        # Check left
        file = self.file
        while file > self.MIN_FILE:
            next_square = (file - 1, self.rank)
            on_next_square = board.on_square(*next_square)

            if on_next_square is None:
                moves.append(next_square)
                file -= 1
            elif on_next_square.letter.isupper() is self.letter.islower():
                moves.append(next_square)
                break
            else:
                break

        # Check right
        file = self.file
        while file < self.MAX_FILE:
            next_square = (file + 1, self.rank)
            on_next_square = board.on_square(*next_square)

            if on_next_square is None:
                moves.append(next_square)
                file += 1
            elif on_next_square.letter.isupper() is self.letter.islower():
                moves.append(next_square)
                break
            else:
                break

        return moves


class Queen(Piece):
    def __init__(self, letter: str, file: int, rank: int,
                 image: pygame.Surface, w: int):
        super().__init__(letter, file, rank, image, w)

    def valid_moves(self, board) -> list:
        moves = []

        # Steal rook movement code
        temp_rook = Rook(self.letter, self.file, self.rank, self.image,
                         int(self.w))
        moves.extend(temp_rook.valid_moves(board))
        del temp_rook

        # Diagonals
        file = self.file
        rank = self.rank

        while rank < self.MAX_RANK:
            # Up and Left
            while file > self.MIN_FILE:
                next_square = (file - 1, rank + 1)
                on_square = board.on_square(*next_square)

                if self.can_move(on_square):
                    moves.append(next_square)
                    file -= 1
                    rank += 1

                    if on_square is not None and on_square.letter.isupper() \
                            is self.letter.islower():
                        break
                else:
                    break

            # TODO prematurely breaks out of while loop if rank hits max_rank
            #  first (doesn't run code below). Might have to try `if not
            #  self.RIGHT/LEFT` etc

            # Up and Right
            file = self.file
            rank = self.rank

            while file < self.MAX_FILE:
                next_square = (file + 1, rank + 1)
                on_square = board.on_square(*next_square)

                if self.can_move(on_square):
                    moves.append(next_square)
                    file += 1
                    rank += 1
                    if on_square is not None and on_square.letter.isupper() \
                            is self.letter.islower():
                        break
                else:
                    break

        rank = self.rank
        file = self.file

        while rank > self.MIN_RANK:
            # Down and left
            while file > self.MIN_FILE:
                next_square = (file - 1, rank - 1)
                on_square = board.on_square(*next_square)

                if self.can_move(on_square):
                    moves.append(next_square)
                    file -= 1
                    rank -= 1
                    if on_square is not None and \
                            on_square.letter.isupper() is \
                            self.letter.islower():
                        break
                else:
                    break

            # Down and Right
            file = self.file
            rank = self.rank

            while file < self.MAX_FILE:
                next_square = (file + 1, rank - 1)
                on_square = board.on_square(*next_square)

                if self.can_move(on_square):
                    moves.append(next_square)
                    file += 1
                    rank -= 1
                    if on_square is not None and on_square.letter.isupper() \
                            is self.letter.islower():
                        break
                else:
                    break

        return moves


class King(Piece):
    def __init__(self, letter: str, file: int, rank: int,
                 image: pygame.Surface, w: int):
        super().__init__(letter, file, rank, image, w)

    def valid_moves(self, board) -> list:
        moves = []
        return moves
