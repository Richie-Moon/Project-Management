import subprocess
import pyffish
import threading
from typing import Generator, Any
import time

# https://github.com/fairy-stockfish/FairyFishGUI/blob/main/fairyfishgui.py


class Engine:
    engine_vars = {'depth': int}

    def __init__(self, path: list) -> None:
        self.process = subprocess.Popen(path, stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        universal_newlines=True)
        self.lock = threading.Lock()

        # Initialise the engine.
        self.write('uci\n')

        self.DEFUALT_ELO: int = 1000  # TODO this is a temp value.
        self.moves = []

    def write(self, message: str) -> None:
        with self.lock:
            self.process.stdin.write(message)
            self.process.stdin.flush()

    def read(self) -> Generator[str, Any, None]:
        while self.process.poll() is None:
            yield self.process.stdout.readline()

    def new_game(self) -> None:
        """
        Starts a new game. Initialises the engine: sets variant to losalamos,
        sets the position to the startpos and sets engine elo to default.
        """

        self.write("ucinewgame\n")
        self.write("setoption name UCI_Variant value losalamos\n")
        self.write(f"position startpos\n")

        self.write("setoption name UCI_LimitStrength value true")
        self.change_elo(self.DEFUALT_ELO)

    def change_elo(self, elo: int) -> None:
        """
        Changes the elo strength of the engine.
        :param elo: The elo that the engine should play at. Must be between
        500 and 2850
        """
        self.write(f"setoption UCI_Elo value {elo}")

    def get_position(self) -> str:
        self.write("d\n")
        line = self.response("Fen: ")
        return line.split(" ", 1)[1]

    def response(self, phrase: str):
        for line in self.read():
            if phrase in line:
                return line

    def move(self, fen: str, move: str):
        """
        :param fen: The current board in FEN notation.
        :param move: The move to make on the board, given in LAN
        (Long Algebraic Notation).
        """
        self.write(f"position {fen} moves {move}")

# engine = Engine(["fairy-stockfish_x86-64-bmi2"])
# engine.new_game()
# engine.write('go movetime 2000\n')
# time.sleep(3)
#
# print(engine.get_position())
