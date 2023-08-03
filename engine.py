import subprocess
import pyffish
import threading
from typing import Generator, Any

# https://github.com/fairy-stockfish/FairyFishGUI/blob/main/fairyfishgui.py


class Engine:
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


engine = Engine(["fairy-stockfish_x86-64-bmi2"])
engine.write("ucinewgame\n")
engine.write("setoption name UCI_Variant value losalamos\n")
engine.write(f"position startpos\n")
engine.write("d\n")
engine.write('go movetime 2000\n')

for i in engine.read():
    print(i)
