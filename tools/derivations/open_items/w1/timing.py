"""The cost of one interval of the bare 7-cube at a den (hand w1): the lines per Node, the kind, the width, and seconds per interval over a few intervals with the sea standing, so that the den of the toy is chosen by measurement (BRIEF_w: the 54-bit den, or the top tier's if too slow)."""

from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import w1lib  # noqa: E402

den = int(sys.argv[1]) if len(sys.argv) > 1 else w1lib.DEN54
cube = int(sys.argv[2]) if len(sys.argv) > 2 else 7
steps = int(sys.argv[3]) if len(sys.argv) > 3 else 5
folder = Path("/dev/shm/tmp/w1") / f"timing_{den}_{cube}"
t0 = time.time()
board = w1lib.board_of(folder, den, cube, steps)
t1 = time.time()
world = board.world
lines = sum(len(s.lines) for s in board.states)
print(f"den {den} ({den.bit_length()} bits) cube {cube}: load {t1 - t0:.2f} s, kind {world.kind.__name__ if hasattr(world.kind, '__name__') else world.kind}, width {world.width.bit_length()} bits, A {world.amplitude_bound}, families {len(board.families)}, lines standing {lines}")
for row in w1lib.point_families(board):
    if 0.5 < row[4] < 0.95:
        print("  point", row)
t2 = time.time()
for _ in range(steps):
    board.step()
t3 = time.time()
print(f"{steps} intervals in {t3 - t2:.2f} s: {(t3 - t2) / steps:.3f} s per interval; interval {board.interval}")
