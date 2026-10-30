"""Probe: the decoder's cone check by click (src/tensor24/decoder/measure.py) on a hand and a slot at once, as records
over every digit, under decision 40 (b) and under the weighing it withdrew (Animate; ANIMATE-SCHEDULER, part 5).

The board of hand_slot.py with a cone-sound near detector: a pair at site 50 (tick 10), its near twin's + taken at
site 44 and - at site 46, both at tick 16, its setting at site 45 (tick 14) inside both clicks' past cones; its far
twin taken at site 150 (tick 110), its setting at tick 109. A quantum born at site 56 (tick 6) reaches x (site 66) and
site 46 at tick 16, shares 1 and 1; site 46 has one free slot at tick 16. Each digit of every Node-clock that draws is
one lay, a few hundred rounds apart, written as schema 1.2's lines: the lays, the settings (split clicks with axes),
the takes (naming their lay) and the refusals (Books lines naming their lay).

usage: python -I cone_read.py
"""

import sys
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[3] / "src"))
sys.path.insert(0, str(HERE))
import hand_slot as hs  # noqa: E402  the withdrawn weighing, as the contrast
import scheduler as s  # noqa: E402  the one rule
from tensor24.decoder import measure, records  # noqa: E402

SLOT = (46, 16)


def board(limited):
    pair = {"site": 50, "tick": 10, "hand": s.PAIR_HAND, "frames": s.PAIR_BASES, "parts": [0, 1]}
    near = {"birth": 0, "heard": (), "ends": [(44, 16), SLOT]}  # + at 44, - at 46
    far = s.detector(pair, 0, 150, 0)
    source = {"site": 56, "tick": 6, "parts": [2]}
    quantum = s.spread(source, 1, [(66, 1), (46, 1)])
    return {"births": [pair, source], "parts": [near, far, quantum], "slots": {SLOT: limited}}


def axis(spinor):
    rho, spin = s.axis(spinor)
    return {"rho": rho, "spin": list(spin)}


def lines_of(n, fa, fb, drawn, refused):
    """One lay's lines, the pair laid at round base + 10 and the quantum at base + 6."""
    base = 1 + 200 * n
    pair_lay, quantum_lay = [base + 10, 50], [base + 6, 56]
    out = [
        {"kind": "whole", "round": base + 10, "site": 50, "count": 1, "train": 0, "q": 1},
        {"kind": "whole", "round": base + 6, "site": 56, "count": 1, "train": 1, "q": 1},
    ]
    for at, site, frames, drawn_frame, part in ((14, 45, 0, fa, 0), (109, 150, 1, fb, 1)):
        axes = [axis(s.basis(a)[0]) for a in s.PAIR_FRAMES[frames]]
        line = {"kind": "split", "round": base + at, "site": site, "count": 1, "train": 0}
        out.append(line | {"members": [[*pair_lay, part]], "axes": axes, "drawn": drawn_frame})
    parts = board(1)["parts"]
    for i, e in drawn.items():
        site, tick = parts[i]["ends"][e]
        lay, train = (quantum_lay, 1) if i == 2 else (pair_lay, 0)
        event = {"round": base + tick, "site": site, "train": train}
        if i in refused:
            out.append({"kind": "books"} | event | {"kept": 1, "birth": lay})
            continue
        if i == 2:
            frame, written = {"rho": 1, "spin": [0, 0, 1]}, {"rho": 1, "spin": [0, 0, 1 - e - e]}
        else:
            a = s.PAIR_FRAMES[i][(fa, fb)[i]]
            frame, written = axis(s.basis(a)[0]), axis(s.basis(a)[e])
        take = {"kind": "whole"} | event | {"count": 1, "q": 1, "birth": lay}
        out.append(take | {"detector": frame, "written": written})
    return out


def record(withdrawn):
    """Every digit of every Node-clock that draws, one lay each: under (b) run() at the pair's birth, the quantum's
    and the slot; under the withdrawn weighing one band over its products, the slot weighing 0 where full."""
    lines, n = [], 0
    for fa, fb in product(range(2), range(2)):
        b = board(1)
        if withdrawn:
            histories, weights = hs.withdrawn(b, [0, 1, 2], {0: fa, 1: fb, 2: 0}, SLOT, 1)
            runs = [(dict(enumerate(histories[s.law9(weights, d)])), {}) for d in range(348)]
        else:
            runs = []
            for d0, d1, d2 in product(range(116), range(2), range(2)):
                given = {
                    ("det", 0): fa,
                    ("det", 1): fb,
                    ("birth", 0): d0,
                    ("birth", 1): d1,
                    ("slot", *SLOT): d2,
                }
                out = s.run(b, False, lambda key, given=given: given.get(key, 0))
                runs.append((out["drawn"], out["refused"]))
        for drawn, refused in runs:
            lines += lines_of(n, fa, fb, drawn, refused)
            n += 1
    lines.sort(key=records.place)
    head = {"kind": "header", "record": "cone_read", "major": 1, "minor": 1, "sides": [1, 1, 256]}
    return records.Record(head, lines, {"kind": "end", "rounds": lines[-1]["round"]})


def main():
    print("The decoder's cone check by click on a hand and a slot at once, every digit one lay")
    for withdrawn, name in (
        (False, "decision 40 (b), a full slot refusing after the draw"),
        (True, "the withdrawn weighing"),
    ):
        found = measure.cone_check(record(withdrawn))
        print(f"  {name}: {found['kind']}")
        print(f"    {found['cause']}")


if __name__ == "__main__":
    main()
