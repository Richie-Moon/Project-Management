import board

fen = "rnqknr/p1pppp/1p4/1P4/P1PPPP/RNQKNR w - - 0 1"

b = board.Board()
b.fen_to_board(fen)

piece = b.on_square(1, 2)
print("Start square: " + piece.square())

print(piece.valid_moves(b))

