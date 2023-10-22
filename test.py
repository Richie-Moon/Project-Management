# from typing import Iterable
#
# # txt = "info depth 16 seldepth 21 multipv 1 score cp 7 nodes 560203 nps 279681 hashfull 325 tbhits 0 time 2003 pv c2c3 b5b4 d2d3 b4c3 b1c3 b6a4 c1c2 a4c3 b2c3 e5e4 a1b1 a6b6 b1b6 c6b6 c2b3 b6b3 a2b3"
# txt = "bestmove c2c3"
#
# INFO_KEYWORDS = {'depth': int, 'seldepth': int, 'multipv': int, 'nodes': int,
#                  'nps': int, 'time': int, 'score': list, 'pv': list}
#
# items = txt.split()
# if len(items) > 1 and items[0] == 'info' and items[1] != 'string':
#     key = None
#     values = []
#     info = {}
#     for i in items[1:] + ['']:
#         if not i or i in INFO_KEYWORDS:
#             if key:
#                 if values and not issubclass(INFO_KEYWORDS[key], Iterable):
#                     values = values[0]
#                 info[key] = INFO_KEYWORDS[key](values)
#             key = i
#             values = []
#         else:
#             values.append(i)
#     print(info)
# print('returned None')

import gui
x = 0
y = 0
print(gui.coords_to_index((x, y)))
