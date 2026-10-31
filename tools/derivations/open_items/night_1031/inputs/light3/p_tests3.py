"""LIGHT3's tests of the echo rule's logic, on records built by hand in light3/tests (a test's, never a world), each
balanced so that the decoder's guard (sides.paired) passes it: every meeting written at both ends, q -1 at the giver
and +1 at the taker, teeth 1 and 1 at the edge key 3 (summing to the key less 1). A meeting is (round, giver, taker,
kind), a clock (site, train). The readers' cases are rebuilt from their own event lists (light2_math/m_built.py H1 to
H4; light2_phys/p_ring_test.py's two rings; light2_phys/out/dump_ring180k_echo.txt, copied to tests/readers/), with
an own meeting added where a case needs its train to meet at its site. Read by p_light3, unchanged."""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import p_light3 as rule  # noqa: E402


def build(path, events):
    """A record of the events: per (round, site, train) its line, own sides by u, across sides by (place, u)."""
    lines = {}
    for r, g, k, kind in events:
        for me, other, q in ((g, k, -1), (k, g, 1)):
            line = lines.setdefault((r, me[0], me[1]), {"sides": [], "across": []})
            if kind == "own":
                line["sides"].append([other[1], q, 1, 1])
            else:
                line["across"].append([other[1], other[0], q, 1, 1])
    trains = sorted({t for _, _, t in lines})
    with path.open("w", encoding="utf-8") as out:
        out.write(json.dumps({"kind": "header", "trains": [{"index": t, "key": 3} for t in trains]}) + "\n")
        for (r, s, t), held in sorted(lines.items()):
            held["sides"].sort()
            held["across"].sort(key=lambda e: (e[1], e[0]))
            q = sum(e[1] for e in held["sides"]) + sum(e[2] for e in held["across"])
            out.write(json.dumps({"kind": "click", "round": r, "site": s, "train": t, "q": q, **held}) + "\n")
        out.write(json.dumps({"kind": "end"}) + "\n")


def mesh(r, g, k):
    return (r, g, k, "mesh")


def steady(clocks, rounds):
    """Own meetings: each matter clock (s, 2) meets its held clock (s, 1) at every round given, giving."""
    return [(r, c, (c[0], 1), "own") for c in clocks for r in rounds]


def ring_lap(n):
    """The mathematician's H1: one front round a ring of n places, matter (train 2) at even places, the medium
    (train 0) at odd ones, one link a round, each clock taking from one side and giving to the other."""
    ev = []
    for r in range(1, n + 1):
        x, y = r - 1, r % n
        ev.append(mesh(r, (x, 2), (y, 0)) if r % 2 == 1 else mesh(r, (x, 0), (y, 2)))
    return ev + steady([(x, 2) for x in range(0, n, 2)], [1])


def mathematician(rows):
    """The mathematician's events (r, x, tx, y, ty), giver (x, tx) and taker (y, ty), with every train-2 clock given
    one own meeting at round 1, as his builder gives every train-2 line its own side."""
    ev = [mesh(r, (x, tx), (y, ty)) for r, x, tx, y, ty in rows]
    twos = sorted({c for _, g, k, _ in ev for c in (g, k) if c[1] == 2})
    return ev + steady(twos, [min(r for r, *_ in rows)])


def physicist(rows):
    """The physicist's events (r, x, tx, y, ty, q), with every train-2 clock given one own meeting at round 1."""
    return mathematician([(r, x, tx, y, ty) for r, x, tx, y, ty, q in rows])


A, B, M = (0, 2), (2, 2), (1, 0)
ECHO = [mesh(1, A, M), mesh(2, M, B), mesh(3, B, M), mesh(4, M, A)]
CASES = {
    "L1 echo, A and B steady clicking clocks": ECHO + steady([A, B], range(1, 6)),
    "L2 A not quiet (A gives light between)": ECHO + [mesh(3, A, M)] + steady([A, B], range(1, 6)),
    "L3 no give at B": [e for e in ECHO if e[0] != 3] + steady([A, B], range(1, 6)),
    "L4 the back link in B's give's round": ECHO[:3] + [mesh(3, M, A)] + steady([A, B], range(1, 6)),
    "L5 a front out along a line, never back": [mesh(1, A, M), mesh(2, M, B), mesh(3, B, (3, 0)),
                                                mesh(4, (3, 0), (4, 2))] + steady([A, B, (4, 2)], range(1, 6)),
    "H1 one front round a ring of 6 (math)": ring_lap(6),
    "H1b one front round a ring of 10 (math)": ring_lap(10),
    "H2 a line 0..4 turned at place 4 only (math)": mathematician([
        (1, 0, 2, 1, 0), (2, 1, 0, 2, 2), (3, 2, 2, 3, 0), (4, 3, 0, 4, 2),
        (5, 4, 2, 3, 0), (6, 3, 0, 2, 2), (7, 2, 2, 1, 0), (8, 1, 0, 0, 2)]),
    "H3 a hop between two clocks of place 1 that never meet (math)": mathematician([
        (1, 0, 2, 1, 0), (2, 1, 2, 2, 0), (3, 2, 0, 3, 2), (4, 3, 2, 2, 0), (5, 2, 0, 1, 2), (6, 1, 0, 0, 2)]),
    "H4 two media, train 0 out and train 3 back (math)": mathematician([
        (1, 0, 2, 1, 0), (2, 1, 0, 2, 2), (3, 2, 2, 1, 3), (4, 1, 3, 0, 2)]),
    "R4 one front once round a ring of four (phys)": physicist([
        (1, 0, 2, 1, 0, 1), (2, 1, 0, 2, 2, 1), (3, 2, 2, 3, 0, 1), (4, 3, 0, 0, 2, 1)]),
    "R6 two halves through the antipode of a ring of six (phys)": physicist([
        (1, 0, 2, 1, 0, 1), (1, 0, 2, 5, 0, 1), (2, 1, 0, 2, 2, 1), (2, 5, 0, 4, 2, 1), (3, 2, 2, 3, 0, 1),
        (3, 4, 2, 3, 0, 1), (4, 3, 0, 4, 2, 1), (4, 3, 0, 2, 2, 1), (5, 4, 2, 5, 0, 1), (5, 2, 2, 1, 0, 1),
        (6, 5, 0, 0, 2, 1), (6, 1, 0, 0, 2, 1)]),
    # the physicist's ring180k echo, its meetings as dump_ring180k_echo.txt lists them (rounds 112 to 124), the tied
    # clocks given one own meeting at round 100: the uniform relay of matter, no reflector laid
    "U the uniform relay, ring180k's rounds 112 to 124 (phys)": [
        mesh(112, (16, 2), (17, 0)), mesh(113, (16, 0), (15, 2)), mesh(114, (18, 2), (17, 0)),
        mesh(116, (17, 0), (18, 2)), mesh(118, (18, 2), (17, 0)), mesh(119, (17, 0), (18, 2)),
        mesh(123, (18, 2), (17, 0)), mesh(124, (17, 0), (16, 2))] + steady([(15, 2), (16, 2), (18, 2)], [100]),
}


def main():
    folder = HERE.joinpath("tests")
    folder.mkdir(exist_ok=True)
    for n, (name, events) in enumerate(CASES.items(), start=1):
        path = folder.joinpath(f"case{n:02d}.jsonl")
        build(path, events)
        clicks, cause = rule.read(path)
        meets = rule.meetings(clicks)
        medium, matter = rule.eligible(meets)
        med_t = sorted({c[1] for c in medium})
        out = []
        for directed, turn in ((False, True), (True, True), (False, False)):
            found, _, _ = rule.echoes(meets, medium, matter, directed, turn)
            label = ("directed" if directed else "meetings") + (", turn" if turn else ", no turn")
            pairs = sorted({(e[0], e[2], e[3], e[4]) for e in found})
            out.append(f"{label}: {'SHOWN ' + str(pairs) if found else 'NOT SHOWN'}")
        first = rule.echoes(meets, medium, matter, False, True)[0]
        counts = f"; A's own count, B's hold: {(first[0][7], first[0][8])}" if first else ""
        print(f"case{n:02d} {name}: guard {cause or 'well formed'}; medium trains {med_t}; " + "; ".join(out) + counts)


if __name__ == "__main__":
    main()
