import pyffish
result = pyffish.legal_moves('losalamos', '6/1P5/6/K3k1/1p5/6 b - - 0 1', [])

print(result)

print((1, 2) + tuple('r'))
# import board
#
# b = board.Board()
# b.new_game(1)
# b.board = []
# b.fen_to_board("K5/qq4/6/6/k5/6 b - - 0 1", 1)
# b.board_fen = "K5/qq4/6/6/k5/6 b - - 0 1"
#
# print(b.check_end_game())
