import pyffish
# result = pyffish.gives_check('losalamos', "K5/6/6/6/6/1q4 w - - 0 1", ['a6a5', 'b1a1'])
# result = pyffish.game_result('losalamos', pyffish.start_fen('losalamos'), [])

result = pyffish.has_insufficient_material('losalamos', "K5/6/6/6/6/k5 w - - 0 1", [])

print(result)
