"""Toy: rule B's scheduler on a full board (Animate; the Boss's 6494549592 item 4: "The scheduler on a full board
has to be sized by the depth of its chains, not three passes fixed"; Animate's 10.5 item 6: every band of agreeing
histories must part at one Node-clock, and the probe must look for a band that does not).

A line of Node-clocks; light runs one site a tick. Each birth lays a pair (the shared hand e1 x e2 - e2 x e1) or a
triple (e1 x e1 x e1 + e2 x e2 x e2); each twin rides one site a tick to its detector and waits there `late` ticks;
its take is a whole click. Each detector's setting is a split click one tick before its take: free (its own light's
digit, over its two frames) or a machine that sets its frame from an outcome it heard by light, a take strictly
inside its past light cone. The sizes sigma_f are the Gaussian norms of the hand's whole-number overlaps with the
frames' spinors (ANIMATE-B-RECORD); every sigma_b is 1. Every draw is law 9's: the rank count of a digit over the
weights' running sums, the digit the stream's number modulo the weights' sum.

Two schedulers of rule B, each by the runner's passes (forward, then back and forward again as often as needed):
  J, joint: a birth draws all its parts at once, when every one of its parties' settings has come back;
  L, layered: at each backward pass, a birth draws, at once, the parts whose settings have come back, conditional on
     the parts it drew before, the frames of the parts still out silent. The law is unchanged, because the sizes of
     a subset of parts summed over the rest are the same in every frame of the rest (no signal); every layer's draw
     is checked against every frame the parts still out may take, exactly.
Part 1: two crossed births, each one's early outcome setting the other's late frame. Part 2: random full boards.
Part 3: two quanta reaching one absorber's one free slot at one tick, the case the forward order leaves open.

usage: python -I scheduler.py
"""

import hashlib
import random
import sys
from fractions import Fraction
from functools import cache
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ANIMATE-B-RECORD"))
from b_record import BEE, BEE2, GHZ, SINGLET, X, Y, Z, size  # noqa: E402  the hands, the frames, sigma_f

SIGNS = (1, -1)
HANDS = {"pair": SINGLET, "triple": GHZ}
PAIR_FRAMES = ((Z, X), (BEE, BEE2))  # a, a' at the first party; b, b' at the second (draft D)
TRIPLE_FRAMES = ((X, Y),) * 3
RULE = {1: 0, -1: 1}  # a machine sets its first frame where it heard +, its second where it heard -


def law9(weights, n):
    """Law 9: d = n modulo the weights' sum, the part the rank count of d over the running sums."""
    d, total = n % sum(weights), 0
    for part, w in enumerate(weights):
        total += w
        if d < total:
            return part
    raise ValueError("no part")


class Digits:
    """A fixed stream of numbers, SHA-256 of a label and a counter (the vernier's stand-in)."""

    def __init__(self, label):
        self.label, self.count = label, 0

    def next(self):
        self.count += 1
        return int.from_bytes(hashlib.sha256(f"{self.label}:{self.count}".encode()).digest()[:8], "big")


@cache
def subset_sizes(hand, frames, known, chosen):
    """The sizes of the chosen parties' joint signs, the first chosen outermost: sigma_f with the known parties'
    signs held (pairs of party and sign), summed over the signs of the parties neither known nor chosen."""
    held = dict(known)
    rest = [p for p in range(len(frames)) if p not in held and p not in chosen]
    sizes = []
    for signs in product(SIGNS, repeat=len(chosen)):
        total = 0
        for others in product(SIGNS, repeat=len(rest)):
            full = held | dict(zip(chosen, signs, strict=True)) | dict(zip(rest, others, strict=True))
            total += size(HANDS[hand], list(frames), [full[p] for p in range(len(frames))])
        sizes.append(total)
    return tuple(sizes)


def shares(sizes):
    return [Fraction(w, sum(sizes)) for w in sizes]


def run(board, joint, numbers):
    """The passes of one scheduler: the outcomes and frames, the passes and steps, the layers' checks; or None where
    no birth can draw and parts are still out (a deadlock)."""
    births, dets = board["births"], board["dets"]
    frame, outcome = {}, {}
    drawn = {b: {} for b in range(len(births))}
    checks = [0, 0]  # a layer's law against a frame of the parts still out: checked, and equal
    passes, steps = 1, max(d["take"] - births[d["birth"]]["tick"] for d in dets)

    def set_frames():
        for i, d in enumerate(dets):
            if i not in frame and (d["heard"] is None or d["heard"] in outcome):
                free = d["heard"] is None
                frame[i] = law9([1, 1], numbers(("det", i))) if free else d["rule"][outcome[d["heard"]]]

    set_frames()
    while len(outcome) < len(dets):
        now = []
        for b, birth in enumerate(births):
            parties = birth["parties"]
            back = tuple(k for k, i in enumerate(parties) if i in frame and k not in drawn[b])
            if not back or (joint and len(back) < len(parties)):
                continue
            frames = tuple(
                birth["frames"][k][frame[i]] if i in frame else Z for k, i in enumerate(parties)
            )
            held = tuple(sorted(drawn[b].items()))
            sizes = subset_sizes(birth["hand"], frames, held, back)
            out = [k for k, i in enumerate(parties) if i not in frame]
            for picks in product(range(2), repeat=len(out)) if not joint else ():
                other = list(frames)
                for k, pick in zip(out, picks, strict=True):
                    other[k] = birth["frames"][k][pick]
                checks[0] += 1
                checks[1] += shares(sizes) == shares(
                    subset_sizes(birth["hand"], tuple(other), held, back)
                )
            signs = list(product(SIGNS, repeat=len(back)))[law9(sizes, numbers(("birth", b)))]
            for k, s in zip(back, signs, strict=True):
                drawn[b][k] = s
                outcome[parties[k]] = s
                now.append(dets[parties[k]]["take"] - birth["tick"])
        if not now:
            return None
        passes, steps = passes + 2, steps + 2 * max(now)
        set_frames()
    return {"frame": frame, "outcome": outcome, "passes": passes, "steps": steps, "checks": checks}


def depth(board):
    """The longest chain of settings: a free setting 1, a machine one more than the take it heard."""
    known, dets = {}, board["dets"]
    while len(known) < len(dets):
        for i, d in enumerate(dets):
            if i not in known and (d["heard"] is None or d["heard"] in known):
                known[i] = 1 if d["heard"] is None else known[d["heard"]] + 1
    return max(known.values())


def detector(birth, b, site, late, heard=None):
    take = birth["tick"] + abs(site - birth["site"]) + late
    return {"birth": b, "site": site, "late": late, "take": take, "heard": heard, "rule": RULE}


def nature(frames, signs):
    """Nature's joint law of the singlet at two frames in axis form (rho, spin): (r r' - s t spin . spin') / 4 r r'."""
    (r1, s1), (r2, s2) = frames
    dot = sum(a * b for a, b in zip(s1, s2, strict=True))
    return Fraction(r1 * r2 - signs[0] * signs[1] * dot, 4 * r1 * r2)


def axis(frame):
    """A frame's axis form from its spinor (p, q): rho = |p|^2 + |q|^2 and spin (2 conj(p) q, |p|^2 - |q|^2)."""
    (p0, p1), (q0, q1) = frame
    w = (p0 * q0 + p1 * q1, p0 * q1 - p1 * q0)
    return p0 * p0 + p1 * p1 + q0 * q0 + q1 * q1, (
        2 * w[0],
        2 * w[1],
        p0 * p0 + p1 * p1 - q0 * q0 - q1 * q1,
    )


# Part 1: two crossed births


def crossed():
    """Q at site 50 and P at 100, both at tick 0. Q's first twin is taken at site 40 (tick 10), its second at 150
    (tick 100); P's first at 120 (tick 20), its second at 10 (tick 90). Q's second frame is set by P's first outcome,
    heard by light (30 sites in 79 ticks), and P's second by Q's first; each birth's two takes are spacelike."""
    q = {"site": 50, "tick": 0, "hand": "pair", "frames": PAIR_FRAMES, "parties": [0, 1]}
    p = {"site": 100, "tick": 0, "hand": "pair", "frames": PAIR_FRAMES, "parties": [2, 3]}
    dets = [
        detector(q, 0, 40, 0),
        detector(q, 0, 150, 0, 2),
        detector(p, 1, 120, 0),
        detector(p, 1, 10, 0, 0),
    ]
    for d in dets:
        h = dets[d["heard"]] if d["heard"] is not None else None
        assert h is None or h["take"] + abs(h["site"] - d["site"]) < d["take"] - 1, (
            "heard outside the past cone"
        )
    return {"births": [q, p], "dets": dets}


def fixed_points(order):
    """J's histories that agree with themselves: guess both early outcomes, draw each birth whole with its parts in
    the order given (the first party's sign outermost, or the second's), and keep the guesses each draw returns."""
    counts, law, span = (
        {},
        {},
        116,
    )  # 116 is a multiple of every room (58 and 116): each digit is met alike
    for fq, fp, nq, np_ in product(range(2), range(2), range(span), range(span)):
        found = []
        for gq, gp in product(SIGNS, SIGNS):
            drawn = []
            for f, guess, n in ((fq, gp, nq), (fp, gq, np_)):
                frames = (PAIR_FRAMES[0][f], PAIR_FRAMES[1][RULE[guess]])
                signs = list(product(SIGNS, SIGNS))[law9(subset_sizes("pair", frames, (), order), n)]
                drawn.append(dict(zip(order, signs, strict=True)))
            if drawn[0][0] == gq and drawn[1][0] == gp:
                found.append((fq, fp, RULE[gp], RULE[gq], gq, drawn[0][1], gp, drawn[1][1]))
        counts[len(found)] = counts.get(len(found), 0) + 1
        for key in found if len(found) == 1 else ():
            law[key] = law.get(key, 0) + 1
    return counts, law, 4 * span * span


def natures(law, total):
    """Whether a law over (Q's free frame, P's, Q's second, P's second, and the four outcomes) is nature's sequential
    law: each free frame 1/2, each first outcome 1/2, each second outcome its row given the first."""
    exact = True
    for (fq, fp, fq2, fp2, s1, t1, s2, t2), n in law.items():
        fr_q = [axis(PAIR_FRAMES[0][fq]), axis(PAIR_FRAMES[1][fq2])]
        fr_p = [axis(PAIR_FRAMES[0][fp]), axis(PAIR_FRAMES[1][fp2])]
        exact &= Fraction(n, total) == Fraction(1, 4) * nature(fr_q, (s1, t1)) * nature(fr_p, (s2, t2))
    return exact and sum(law.values()) == total


def part1():
    board = crossed()
    print(
        "Part 1: two crossed births, each one's early outcome setting the other's late frame (spacelike pairs)"
    )
    stuck = run(board, True, lambda key: 0) is None
    print(
        f"  J as the runner builds it, pass by pass: it deadlocks, each birth waiting for the other's outcome: {stuck}"
    )
    print(
        "  J as a history that agrees with itself (guess both early outcomes, keep the guesses the draws return):"
    )
    for name, order in (
        ("the first party's sign outermost, the cause's order", (0, 1)),
        ("the second's outermost", (1, 0)),
    ):
        counts, law, total = fixed_points(order)
        shown = ", ".join(f"{n} with {k}" for k, n in sorted(counts.items()))
        said = f"; its law nature's: {natures(law, total)}" if set(counts) == {1} else ""
        print(f"    {name}: of {total} free frames and digits, {shown}{said}")
    law, total = {}, 0
    # L's first layer draws over rooms 2 (at z) and 4 (at x), its second over 29 and 58: 4 and 58 meet each alike
    for fq, fp, n1q, n1p, n2q, n2p in product(
        range(2), range(2), range(4), range(4), range(58), range(58)
    ):
        stream = {("det", 0): [fq], ("det", 2): [fp], ("birth", 0): [n1q, n2q], ("birth", 1): [n1p, n2p]}
        used = dict.fromkeys(stream, 0)

        def numbers(key, stream=stream, used=used):
            used[key] += 1
            return stream[key][used[key] - 1]

        out = run(board, False, numbers)
        key = (fq, fp, out["frame"][1], out["frame"][3]) + tuple(out["outcome"][i] for i in range(4))
        law[key], total = law.get(key, 0) + 1, total + 1
    passes = run(board, False, lambda key: 0)["passes"]
    print(
        f"  L, each part drawn as its setting comes back: one history at every one of {total} digit sets, {passes} passes;"
    )
    print(f"    its law is nature's sequential law: {natures(law, total)}")
    print()


# Part 2: random full boards


def random_board(rng, count, line, machines):
    """Births of pairs and triples at random sites and ticks; each detector at its own site and take tick; a share of
    the detectors are machines hearing a random take strictly inside their past light cone."""
    board, used = {"births": [], "dets": []}, set()
    for b in range(count):
        triple = rng.random() < 0.3
        birth = {
            "site": rng.randrange(line),
            "tick": rng.randrange(24),
            "hand": "triple" if triple else "pair",
        }
        birth["frames"], birth["parties"] = (TRIPLE_FRAMES if triple else PAIR_FRAMES), []
        for _ in range(3 if triple else 2):
            d = detector(birth, b, rng.randrange(line), rng.randrange(4))
            while (d["site"], d["take"]) in used:
                d = detector(birth, b, rng.randrange(line), rng.randrange(4))
            used.add((d["site"], d["take"]))
            birth["parties"].append(len(board["dets"]))
            board["dets"].append(d)
        board["births"].append(birth)
    dets = board["dets"]
    for d in dets:
        heard = [j for j, h in enumerate(dets) if h["take"] + abs(h["site"] - d["site"]) < d["take"] - 1]
        if heard and rng.random() < machines:
            d["heard"], d["rule"] = rng.choice(heard), RULE if rng.random() < 0.5 else {1: 1, -1: 0}
    return board


def part2():
    print(
        "Part 2: random full boards (a line of 96 sites; 12 births, about a third of them triples; detectors 0 to 3"
    )
    print("ticks late; 0, 30, 60 or 90 percent of the detectors machines)")
    rng, rows = random.Random(2026), {}
    for b in range(400):
        board = random_board(rng, 12, 96, (0.0, 0.3, 0.6, 0.9)[b % 4])
        digits = {}

        def numbers(key, digits=digits, b=b):
            return digits.setdefault(key, Digits(f"{b}:{key}")).next()

        layered, joint = run(board, False, numbers), run(board, True, numbers)
        row = rows.setdefault(depth(board), [0, 0, set(), 0, 0, 0])
        row[0] += 1
        row[1] += layered["passes"] == 1 + 2 * depth(board)
        row[2].add(layered["passes"])
        row[3] += layered["checks"][0]
        row[4] += layered["checks"][1]
        row[5] += joint is None
    print("  depth  boards  L: passes = 1 + 2 depth  L's passes  L: layers checked, equal  J deadlocks")
    for d in sorted(rows):
        n, fit, seen, checked, equal, stuck = rows[d]
        print(
            f"  {d:5d}  {n:6d}  {fit:23d}  {str(sorted(seen)):10s}  {checked:13d}, {equal:5d}  {stuck:11d}"
        )
    print(
        "  L finishes every board; J finishes only where no birth waits on an outcome its own parts wait for"
    )
    print()


# Part 3: two quanta at one absorber's one free slot


def part3():
    a, b = {"x": 2, "z": 3}, {"y": 3, "z": 2}
    print(
        "Part 3: two quanta, one free slot: A spread over absorbers x and z (sizes 2 and 3), B over y and z (3 and 2),"
    )
    print("both reaching z at one tick, where one slot is free")
    counts, span = {}, 30  # 30 is a multiple of every room (5, 2 and 3)
    for na, nb in product(range(span), range(span)):
        found = 0
        for ha, hb in product(a, b):
            if ha == hb == "z":
                continue  # one slot
            wa = [a["x"], a["z"] * (hb != "z")]  # sigma_b at z: its free slot as the quantum arrives
            wb = [b["y"], b["z"] * (ha != "z")]
            found += ("x", "z")[law9(wa, na)] == ha and ("y", "z")[law9(wb, nb)] == hb
        counts[found] = counts.get(found, 0) + 1
    shown = ", ".join(f"{n} with {k}" for k, n in sorted(counts.items()))
    print(
        f"  the slot as sigma_b, each source drawing alone: of {span * span} digit pairs, {shown} histories that agree"
    )
    print(
        "  where two agree, they differ only in which quantum z takes: they part at z, so z's own click must decide,"
    )
    print(
        "  over sizes that reach z along the quanta's own paths. One candidate, z drawing once over the joint histories:"
    )
    joint = {("x", "y"): a["x"] * b["y"], ("z", "y"): a["z"] * b["y"], ("x", "z"): a["x"] * b["z"]}
    laws = ", ".join(f"{ha}{hb} {Fraction(w, sum(joint.values()))}" for (ha, hb), w in joint.items())
    print(
        f"    {laws}: one history at every digit, each quantum taken once; whether it is the rule is David's"
    )


def main():
    print(
        "Rule B's scheduler on a full board: J draws each birth whole, L draws each part as its setting comes back"
    )
    print()
    part1()
    part2()
    part3()


if __name__ == "__main__":
    main()
