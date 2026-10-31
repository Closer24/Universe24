"""GEN4b probe: three small clock facts for the fold, in whole numbers (Rule3's carry the one division).
Part 1: R(h) + R(h^-1) squared is senses x I exactly (its two rates +-r2).
Part 2: each kind's quarter-turn character over its dimension, chi(g) / dim on the lift h = (1 + i) / r2 and on -h,
        in Z[r2] pairs halved by the carry: the board's prediction for reading 6, with the whole-speed controls.
Part 3: probe_gen4 part C's rows relabelled by the count the spring moved: EMPTY where it moved none.
"""
import contextlib
import io

import numpy as np

with contextlib.redirect_stdout(io.StringIO()):
    import probe_gen4 as g4
from probe_half2 import CHI, INDEX, M1, MUL, act_round, carry, draw


def part1():
    mats, reps = g4.train24()
    r = g4.right_h(reps)
    rr = r + r.T
    print("PART 1: R(h) + R(h^-1)")
    print(f"  (R(h) + R(h^-1))^2 = 2 I (senses x I): {(rr.dot(rr) == 2 * np.eye(24, dtype=object)).all()}")


def part2():
    h = INDEX[((0, 1), (0, 1), (0, 0), (0, 0))]
    print("PART 2: chi(g) / dim on a quarter turn's two lifts, h = (1 + i) / r2 and -h, as p + q r2")
    for name in ("A1", "T1", "E1/2", "E5/2", "G3/2"):
        dim = CHI[name][INDEX[((2, 0), (0, 0), (0, 0), (0, 0))]][0]
        row = []
        for g in (h, MUL[M1][h]):
            p, q = CHI[name][g]
            # chi / dim: report the pair and the dimension; the r2 parts halved where dim is 2
            row.append(f"({p} + {q} r2) / {dim}")
        print(f"  {name}: on h {row[0]}, on -h {row[1]}")


def part3():
    mats, reps = g4.train24()
    r = g4.right_h(reps)
    rr = r + r.T
    print("PART 3: probe_gen4 part C's two dials, labelled by the counts the spring moved")
    for w in (1000000, 3):
        couple = rr - 2 * w * np.eye(24, dtype=object)
        vals, _ = draw(41 + 1000 + 400, 48, 1000)
        state = (np.array(vals[:24], dtype=object), np.array(vals[24:], dtype=object), 0 * np.array(vals[:24], dtype=object))
        moved = 0
        for _ in range(400):
            new = act_round(state, w, couple)
            moved += int((new[0] != -state[1]).sum())
            state = new
        label = "EMPTY: the spring moved no count" if moved == 0 else "the carry rounds"
        print(f"  W = {w}, 400 rounds: counts the spring moved {moved}: {label}")


part1()
part2()
part3()
