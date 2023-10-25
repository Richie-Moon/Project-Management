# import pyffish
# result = pyffish.gives_check('losalamos', "K5/6/6/6/6/1q4 w - - 0 1", ['a6a5', 'b1a1'])
# # result = pyffish.game_result('losalamos', pyffish.start_fen('losalamos'), [])
#
#
# print(result)
import board

b = board.Board()
b.new_game(1)
b.board = []
b.fen_to_board("K5/qq4/6/6/k5/6 b - - 0 1", 1)
b.board_fen = "K5/qq4/6/6/k5/6 b - - 0 1"

print(b.check_end_game())
