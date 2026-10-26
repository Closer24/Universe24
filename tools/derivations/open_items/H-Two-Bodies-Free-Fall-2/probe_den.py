"""W2 probe: the 54-bit den's circle, its families, and the speed of one interval on a 7-cube (no births)."""
import json, sys, time
from pathlib import Path
import numpy as np
from event_universe import meeting_board, world_files
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from event_universe.loader import circle

DEN = int(sys.argv[1]); CUBE = int(sys.argv[2]); N = int(sys.argv[3])
folder = Path("/dev/shm/tmp/w2_probe"); folder.mkdir(parents=True, exist_ok=True)
world_files.REPOSITORY_ROOT = folder
(folder / "u.json").write_text(json.dumps({"integers": {"den": DEN, "node_clock": 1000, "quantum_action": 36000}}))
(folder / "w.json").write_text(json.dumps({"universe": "u.json", "shape": [CUBE] * 3, "intervals": N}))
print("factors", circle.factors(DEN))
t0 = time.time()
board = Lattice(load_world(folder / "w.json"), output=None)
print("load s", round(time.time() - t0, 2), "families", len(board.families), "width bits", board.world.width.bit_length())
for i, f in enumerate(board.families):
    num, den = f.pair
    print(i, f.name, "g=%.4f" % ((den - num) / den), "lines", f.lines, "records", f.records, "quanta", f.quanta, "held", f.held, "plane", f.plane)
meeting_board.child_of = lambda b, i, v, w: ()  # the toy's births refused by name
t0 = time.time()
for k in range(N):
    board.step()
print("steps", N, "s per interval", round((time.time() - t0) / N, 3), "interval", board.interval)
