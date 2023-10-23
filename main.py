import gui
try:
    gui.main_menu()
except Exception as e:
    print(gui.board.moves)
    raise e
