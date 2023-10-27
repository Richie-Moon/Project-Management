import subprocess
import threading
from typing import Generator, Any
import os

# https://github.com/fairy-stockfish/FairyFishGUI/blob/main/fairyfishgui.py
# Note: Engine knows which side to calculate for using FEN.

BEST_MOVE_POS = 1


class Engine:
    def __init__(self, path: list) -> None:
        """
        Initialise the engine.
        :param path: The path to the .exe file of the engine.
        """

        self.process = subprocess.Popen(path,
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        universal_newlines=True)
        self.lock = threading.Lock()

        # Initialise the engine.
        self.write('uci\n')

        self.DEFAULT_ELO: int = 800
        self.elo = self.DEFAULT_ELO
        self.moves = []

        # The amount of time for the engine to think. Given in milliseconds.
        self.move_time: int = 1500

        self.write("setoption name UCI_LimitStrength value true\n")
        self.change_elo(self.DEFAULT_ELO)

    def write(self, message: str) -> None:
        """
        Write a command to the engine.
        :param message: The command to send.
        :return:
        """
        with self.lock:
            self.process.stdin.write(message)
            self.process.stdin.flush()

    def read(self) -> Generator[str, Any, None]:
        """
        Reads responses from the engine. This function should not be used, as
        it is a generator, it will continue to respond with lines from the
        engine. Instead, use response().
        :return: Will continue to output lines from the engine.
        """
        while self.process.poll() is None:
            yield self.process.stdout.readline()

    def new_game(self) -> None:
        """
        Starts a new game. Initialises the engine: sets variant to losalamos,
        sets the position to the starting position and sets engine elo to
        default.
        """

        self.write("ucinewgame\n")

        self.write("setoption name UCI_Variant value losalamos\n")
        self.write(f"position startpos\n")

    def is_ready(self) -> bool:
        """
        Sends the isready command to the engine.
        :return: Returns True if the engine is ready. Returns False otherwise.
        """
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
        """
        Returns a specific line from the engine if it contains the phrase
        given.
        :param phrase: The phrase to search for, and return.
        :return:
        """
        for line in self.read():
            # print(line)
            if phrase in line:
                return line

    def update(self, fen: str) -> None:
        """
        Update the engines internal board.
        :param fen: The FEN string of the current position.
        """
        self.write(f"position fen {fen}")
        # Need this here to work??? IDK why but the engine freezes without it.
        self.write('d\n')

    def get_move(self) -> str:
        """
        Calculates the best next move.
        :return: Returns the best calculated move in LAN.
        """
        self.write(f"go movetime {self.move_time}\n")
        best_move = self.response("bestmove")
        # best_move is in the format 'bestmove a1a2 ponder b1b2'.
        return best_move.split()[BEST_MOVE_POS]
