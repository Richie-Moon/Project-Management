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
        # self.write('uci\n')  Parse the engine response first.

    def write(self, message: str) -> None:
        with self.lock:
            self.process.stdin.write(message)
            self.process.stdin.flush()

    def read(self) -> Generator[str, Any, None]:
        while self.process.poll() is None:
            yield self.process.stdout.readline()

    def new_game(self) -> None:
        self.write("ucinewgame\n")
        self.write("setoption name UCI_Variant value losalamos\n")
        self.write(f"position startpos\n")

    def change_elo(self, elo: int):
        self.write("")

    @classmethod
    def parse(cls, line: str):
        items = line.split()

        if len(items) == 1:
            pass


engine = Engine(["fairy-stockfish_x86-64-bmi2"])
engine.new_game()
engine.write('go movetime 2000\n')
time.sleep(3)

for i in engine.read():
    print(i)
    try:
        if i.split()[0] == 'bestmove':
            print(i)
    except IndexError:
        pass

