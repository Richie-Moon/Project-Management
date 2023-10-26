import pygame
import pyffish

END = 2
FULL_MOVE_LEN = 4


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

    def update(self) -> None:
        self.LEFT = False
        self.RIGHT = False
        self.TOP = False
        self.BOTTOM = False

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

    def check_valid_moves(self, moves: list[tuple[int, int]],
                          board) -> list[tuple[int, int]]:

        valid_moves = pyffish.legal_moves(board.VARIANT, board.START_FEN,
                                          board.moves)

        moves_square = []

        for i in range(len(moves)):
            moves_square.append(board.coords_to_square(self.file, self.rank)
                                + board.coords_to_square(*moves[i]))

        moves_to_return = []

        black = True if board.user_side == 1 else False
        for i in range(len(moves_square)):
            move = moves_square[i]

            # For every move in moves_square, switch sides if user is playing
            # black. Then check if it's in the valid_moves list. If so, add
            # the co-ordinate version of the square into moves_to_return.

            if black:
                start_square = board.switch_side_square(move[:END])
                end_square = board.switch_side_square(move[END:])
                square = start_square + end_square
            else:
                square = move

            for item in valid_moves:
                if square == item[0:FULL_MOVE_LEN]:
                    moves_to_return.append(moves[i])

        # Set to remove duplicates from promotions.
        return list(set(moves_to_return))

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

        return self.check_valid_moves(moves, board)


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
                on_right_down = board.on_square(*move_down)
                if self.can_move(on_right_down):
                    moves.append(move_down)

            # 2 left, 1 down
            if self.file - 2 >= self.MIN_FILE:
                move_down = (self.file - 2, down)
                on_left_down = board.on_square(*move_down)
                if self.can_move(on_left_down):
                    moves.append(move_down)

        return self.check_valid_moves(moves, board)


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

        return self.check_valid_moves(moves, board)


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

        # Up and Left
        if not self.TOP:
            if not self.LEFT:
                while rank < self.MAX_RANK and file > self.MIN_FILE:
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

            # Up and Right
            file = self.file
            rank = self.rank
            if not self.RIGHT:
                while rank < self.MAX_RANK and file < self.MAX_FILE:
                    next_square = (file + 1, rank + 1)
                    on_square = board.on_square(*next_square)

                    if self.can_move(on_square):
                        moves.append(next_square)
                        file += 1
                        rank += 1
                        if (on_square is not None and
                                on_square.letter.isupper()
                                is self.letter.islower()):
                            break
                    else:
                        break

        rank = self.rank
        file = self.file

        if not self.BOTTOM:
            if not self.LEFT:
                # Down and left
                while rank > self.MIN_RANK and file > self.MIN_FILE:
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

            if not self.RIGHT:
                while rank > self.MIN_RANK and file < self.MAX_FILE:
                    next_square = (file + 1, rank - 1)
                    on_square = board.on_square(*next_square)

                    if self.can_move(on_square):
                        moves.append(next_square)
                        file += 1
                        rank -= 1
                        if (on_square is not None and
                                on_square.letter.isupper()
                                is self.letter.islower()):
                            break
                    else:
                        break

        return self.check_valid_moves(moves, board)


class King(Piece):
    def __init__(self, letter: str, file: int, rank: int,
                 image: pygame.Surface, w: int):
        super().__init__(letter, file, rank, image, w)

    def valid_moves(self, board) -> list:
        moves = []

        if not self.BOTTOM:
            move_down = self.rank - 1
            moves_down = [(self.file, move_down)]

            if not self.LEFT:
                moves_down.append((self.file - 1, move_down))
            if not self.RIGHT:
                moves_down.append((self.file + 1, move_down))

            for move in moves_down:
                if self.can_move(board.on_square(*move)):
                    moves.append(move)

        if not self.TOP:
            move_up = self.rank + 1
            moves_up = [(self.file, move_up)]

            if not self.LEFT:
                moves_up.append((self.file - 1, move_up))
            if not self.RIGHT:
                moves_up.append((self.file + 1, move_up))

            for move in moves_up:
                if self.can_move(board.on_square(*move)):
                    moves.append(move)

        # Can just check for adjacent square, diagonals were checked above
        if not self.LEFT:
            left = (self.file - 1, self.rank)
            if self.can_move(board.on_square(*left)):
                moves.append(left)

        if not self.RIGHT:
            right = (self.file + 1, self.rank)
            if self.can_move(board.on_square(*right)):
                moves.append(right)

        return self.check_valid_moves(moves, board)
