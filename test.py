import subprocess
import pyffish
import threading

import time


class Engine:
    def __init__(self, args: list):
        self.process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
        self.lock = threading.Lock()

    def write(self, message: str):
        with self.lock:
            self.process.stdin.write(message)
            self.process.stdin.flush()

    def read(self):
        while self.process.poll() is None:
            yield self.process.stdout.readline()


engine = Engine(["fairy-stockfish_x86-64-bmi2"])
engine.write("ucinewgame\n")
engine.write("setoption name UCI_Variant value losalamos")
engine.write(f"position {pyffish.start_fen('losalamos')}")
engine.write('go infinite')
time.sleep(5)
engine.write('stop')

print(engine.read())

