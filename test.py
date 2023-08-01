# class Pawn:
#     def __init__(self, side):
#         self.side = side
#         self.file = 'e'
#         self.rank = 5
#
#     def valid_moves(self):
#         if self.side == 'white':
#             moves = []
#             moves.append(self.file + str(self.rank + 1))
#
#             return moves
#
#
# class Rook:
#     def __init__(self, side):
#         self.side = side
#         self.file = 'a'
#         self.rank = 1
#
#     def valid_moves(self):
#         moves = []
#         for i in range(8):
#             moves.append(self.file + str(i))  # a1, a2, etc
#             moves.append(num_to_letter[i] + str(self.rank))  # a1, b1, c1, etc
#
#         return moves
#
#
# num_to_letter = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g',
#                  7: 'h'}

