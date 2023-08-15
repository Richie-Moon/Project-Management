import board
import pyffish

fen = "rnqknr/pp1ppp/2p3/1P1P2/P1P1PP/RNQKNR b - - 0 2"
# fen = pyffish.start_fen('losalamos')

b = board.Board()
b.fen_to_board(fen)

piece = b.on_square(2, 3)
print("Start square: " + b.coords_to_square(*piece.square()))

moves = piece.valid_moves(b)
print(moves)
for square in moves:
    print(b.coords_to_square(*square))

