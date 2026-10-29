"""Probe: a band joined by a hand and by a slot at once (Animate; the Boss's hunt of 13:55 UTC, the record and the
clicks: "the band joined by a hand and a slot at once"; ANIMATE-SCHEDULER/README.md, part 5), under decision 40 (b), a
full slot refusing after the draw, and under the weighing it withdrew, a full slot weighing 0, for contrast.

A pair at site 50 (tick 5): its near twin meets a two-way detector, + taken at site 45 and - at site 55, both at tick
10; its far twin is taken at site 100 (tick 55), outside the near setting's future cone. A spread quantum born at site
65 (tick 0) reaches x (site 75) and site 55 at tick 10, shares 1 and 1. Site 55 has one free slot at tick 10.

Under (b), run() in scheduler.py: the pair is drawn at its birth and the quantum at its own, each over sigma_f; then
the slot, both its parts drawn, takes one of its arrivals by its own law-9 draw over equal weights and refuses the
other, back to its giver. Under the withdrawn weighing, the three parts are one band, drawn over sigma_f times 0 where
the slot is past its free count (computed here from band_weights, as the contrast).

Read: the far twin's law (its + share) for each pair of frames, the near twin's a and the far twin's b, over every
digit, with the slot and with no slot limit. No signal asks that the far twin's law at b be the same at every a.

usage: python -I hand_slot.py
"""

import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scheduler as s  # noqa: E402  the one rule

SLOT = (55, 10)
# the Node-clocks that draw, each over a multiple of every room it meets (the pair's is 58 or 116)
SPANS = ((("birth", 0), 116), (("birth", 1), 2), (("slot", *SLOT), 2))


def board(limited):
    pair = {"site": 50, "tick": 5, "hand": s.PAIR_HAND, "frames": s.PAIR_BASES, "parts": [0, 1]}
    near = {"birth": 0, "heard": (), "ends": [(45, 10), SLOT]}  # + at 45, - at 55
    far = s.detector(pair, 0, 100, 0)
    source = {"site": 65, "tick": 0, "parts": [2]}
    quantum = s.spread(source, 1, [(75, 1), (55, 1)])
    return {"births": [pair, source], "parts": [near, far, quantum], "slots": {SLOT: limited}}


def share(counts, test):
    return Fraction(sum(c for key, c in counts.items() if test(key)), sum(counts.values()))


def law(fa, fb, limited):
    """Decision 40 (b), run() at every digit of the pair's birth, the quantum's and the slot: the far and the near
    twin's + shares, the shares the slot refused (the near twin's, the quantum's), and whether the slot ever took
    past its free count."""
    b, counts = board(limited), {}
    for digits in product(*[range(n) for _, n in SPANS]):
        given = dict(zip([key for key, _ in SPANS], digits, strict=True)) | {
            ("det", 0): fa,
            ("det", 1): fb,
        }
        out = s.run(b, False, lambda key, given=given: given.get(key, 0))
        assert out["frame"] == {0: fa, 1: fb, 2: 0}, "the frames as given"
        key = (tuple(out["drawn"][i] for i in range(3)), tuple(sorted(out["refused"])))
        counts[key] = counts.get(key, 0) + 1
    takes = [[b["parts"][i]["ends"][e] for i, e in enumerate(k) if i not in r] for k, r in counts]
    return (
        share(counts, lambda key: key[0][1] == 0),
        share(counts, lambda key: key[0][0] == 0),
        share(counts, lambda key: 0 in key[1]),
        share(counts, lambda key: 2 in key[1]),
        all(t.count(SLOT) <= limited for t in takes),
    )


def withdrawn(board_, band, frame, slot, free):
    """The withdrawn weighing, for contrast: the band's sigma_f times 0 where the slot is past its free count."""
    histories, weights = s.band_weights(board_, band, frame, {})
    ends = [[board_["parts"][i]["ends"][e] for i, e in zip(band, h, strict=True)] for h in histories]
    return histories, [w * (e.count(slot) <= free) for w, e in zip(weights, ends, strict=True)]


def law_withdrawn(fa, fb, limited):
    """The far and the near twin's + shares under the withdrawn weighing, the three parts one band."""
    histories, weights = withdrawn(board(limited), [0, 1, 2], {0: fa, 1: fb, 2: 0}, SLOT, limited)
    counts = dict(zip(histories, weights, strict=True))
    return share(counts, lambda h: h[1] == 0), share(counts, lambda h: h[0] == 0)


def tie():
    """Part 3's tie, two independent quanta at z's one free slot, B born at site 30 (tick 0): A's click at x (site 4,
    tick 6), spacelike to B's birth, under (b) and under the withdrawn weighing; and A at z (site 20, tick 10), on
    B's birth's light cone, taken or refused under (b)."""
    alone = s.quanta([[(4, 2), (20, 3)]], {(20, 10): 1})
    one, _ = s.drawn_law(alone, [(("birth", 0), 5)])
    pair = s.quanta([[(4, 2), (20, 3)], [(36, 3), (20, 2)]], {(20, 10): 1})
    two, _ = s.drawn_law(pair, [(("birth", 0), 5), (("birth", 1), 5), (("slot", 20, 10), 2)])
    histories, weights = withdrawn(pair, [0, 1], {0: 0, 1: 0}, (20, 10), 1)
    old = share(dict(zip(histories, weights, strict=True)), lambda h: h[0] == 0)

    def at(law_, end):
        return sum(p for key, p in law_.items() if key[0] == end)

    return {
        "x": (at(one, (0, False)), at(two, (0, False)), old),
        "z": (at(one, (1, False)), at(two, (1, False)), at(two, (1, True))),
    }


def main():
    print(
        "A band joined by a hand and a slot at once (part 5's board), under decision 40 (b), a full slot refusing"
    )
    print("after the draw; the withdrawn weighing, a full slot weighing 0, for contrast")
    for limited, name in ((2, "no slot limit (two free)"), (1, "one free slot at site 55")):
        print(f"  {name}:")
        for fb, fa in product(range(2), range(2)):
            far, near, near_out, quantum_out, kept = law(fa, fb, limited)
            old_far, old_near = law_withdrawn(fa, fb, limited)
            print(
                f"    a{fa}, b{fb}: far + {far} (withdrawn {old_far}), near + {near} (withdrawn {old_near});"
                f" refused: near {near_out}, quantum {quantum_out}; slot kept {kept}"
            )
    rows = tie()
    print("Part 3's tie, two independent quanta at z's one free slot, B born at site 30 (tick 0):")
    alone, born, old = rows["x"]
    print(
        f"  A's click at x (site 4, tick 6), spacelike to B's birth: B not born {alone}; B born {born}"
        f" (withdrawn {old})"
    )
    alone, taken, refused = rows["z"]
    print(
        f"  A at z (site 20, tick 10), on B's birth's light cone: B not born, taken {alone}; B born, taken"
        f" {taken}, refused {refused}"
    )


if __name__ == "__main__":
    main()
