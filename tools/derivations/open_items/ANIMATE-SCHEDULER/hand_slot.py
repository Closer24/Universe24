"""Probe: a band joined by a hand and by a slot at once, drawn by the one rule (Animate; the Boss's hunt of 13:55
UTC, the record and the clicks: "the band joined by a hand and a slot at once"; ANIMATE-SCHEDULER/README.md, part 5).

A pair at site 50 (tick 5): its near twin meets a two-way detector, + taken at site 45 and - at site 55, both at tick
10; its far twin is taken at site 100 (tick 55), outside the near setting's future cone. A spread quantum born at site
65 (tick 0) reaches x (site 75) and site 55 at tick 10, shares 1 and 1. Site 55 has one free slot at tick 10, so the
pair's hand and the slot join the three parts into one band, drawn once at the slot by run().

Read: the far twin's law (its + share) for each pair of frames, the near twin's a and the far twin's b, over every
digit of the slot, with the slot and with no slot limit. No signal asks that the far twin's law at b be the same at
every a.

usage: python -I hand_slot.py
"""

import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scheduler as s  # noqa: E402  the one rule

SLOT = (55, 10)


def board(limited):
    pair = {"site": 50, "tick": 5, "hand": s.PAIR_HAND, "frames": s.PAIR_BASES, "parts": [0, 1]}
    near = {"birth": 0, "heard": (), "ends": [(45, 10), SLOT]}  # + at 45, - at 55
    far = s.detector(pair, 0, 100, 0)
    source = {"site": 65, "tick": 0, "parts": [2]}
    quantum = s.spread(source, 1, [(75, 1), (55, 1)])
    return {"births": [pair, source], "parts": [near, far, quantum], "slots": {SLOT: limited}}


def law(fa, fb, limited):
    """The one rule run at every digit of the slot: the far and the near twin's + shares, the room, and whether the
    slot was ever filled past its free count."""
    b = board(limited)
    frame = {0: fa, 1: fb, 2: 0}
    _, weights = s.band_weights(b, [0, 1, 2], frame, {})
    room, counts = sum(weights), {}
    for n in range(room):
        given = {("det", 0): fa, ("det", 1): fb}
        out = s.run(b, False, lambda key, n=n, given=given: given.get(key, n))
        assert out["frame"] == frame, "the frames as given"
        key = tuple(out["taken"][i] for i in range(3))
        counts[key] = counts.get(key, 0) + 1
    kept = all([b["parts"][i]["ends"][k[i]] for i in range(3)].count(SLOT) <= limited for k in counts)
    far = Fraction(sum(c for k, c in counts.items() if k[1] == 0), room)
    near = Fraction(sum(c for k, c in counts.items() if k[0] == 0), room)
    return far, near, room, kept


def main():
    print("A band joined by a hand and a slot at once, drawn at the slot by the one rule")
    for limited, name in ((2, "no slot limit (two free)"), (1, "one free slot at site 55")):
        print(f"  {name}:")
        for fb in range(2):
            cells = []
            for fa in range(2):
                far, near, room, kept = law(fa, fb, limited)
                cells.append(f"a{fa}: far + {far}, near + {near} (room {room}, slot kept {kept})")
            print(f"    b{fb}: " + "; ".join(cells))


if __name__ == "__main__":
    main()
