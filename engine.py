import subprocess
import threading
from typing import Generator, Any

# https://github.com/fairy-stockfish/FairyFishGUI/blob/main/fairyfishgui.py
# Note: Engine knows which side to calculate for using FEN.

BEST_MOVE_POS = 1


class Engine:
    engine_vars = {'depth': int}

    def __init__(self, path: list) -> None:
        self.process = subprocess.Popen(path, stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        universal_newlines=True)
        self.lock = threading.Lock()

        # Initialise the engine.
        self.write('uci\n')

        self.DEFAULT_ELO: int = 800
        self.elo = self.DEFAULT_ELO
        self.moves = []

        # The amount of time for the engine to think. Given in milliseconds.
        self.move_time: int = 2000

        self.new_game()
        self.change_elo(self.DEFAULT_ELO)

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

        self.write("setoption name UCI_LimitStrength value true\n")

    def is_ready(self) -> bool:
        self.write("isready\n")
        if self.response("readyok"):
            return True
        else:
            return False

    def change_elo(self, elo: int) -> None:
        """
        Changes the elo strength of the engine.
        :param elo: The elo that the engine should play at. Must be between
         500 and 2850
        """
        self.write(f"setoption name UCI_Elo value {elo}\n")
        self.elo = elo

    # def get_position(self) -> str:
    #     self.write("d\n")
    #     line = self.response("Fen: ")
    #     return line.split(" ", 1)[1]

    def response(self, phrase: str):
        for line in self.read():
            # print(line)
            if phrase in line:
                return line

    def update(self, moves: list):
        """
        :param moves: The move to make on the board, given in LAN
         (Long Algebraic Notation).
        """
        moves_str = " ".join(moves)
        self.write(f"position startpos move {moves_str}\n")

    def get_move(self) -> str:
        """
        Calculates the best next move.
        :return: Returns the best calculated move in LAN.
        """
        self.write(f"go movetime {self.move_time}\n")
        best_move = self.response("bestmove")
        # best_move is in the format 'bestmove a1a2 ponder b1b2'.
        return best_move.split()[BEST_MOVE_POS]
