"""Toy: rule B's scheduler on a full board, one rule for every band (Animate; the Boss's 6494549592 item 4: "The
scheduler on a full board has to be sized by the depth of its chains, not three passes fixed"; Animate's 10.5 item 6:
every band of agreeing histories must part at one Node-clock; the owner's word to Animate of 2026-10-29, 11:5x UTC,
in Hebrew, in translation: "The rule must be generic").

The one rule: the parts that share a hand (one birth's twins) or a slot (one absorber at one tick, reachable by more
parts than it has free) form a band. Each band is decided by one law-9 draw over the products sigma_f sigma_b of its
joint histories, conditional on what is drawn, at the Node-clock where its parts are one (its birth, or the slots that
join it, their digits summed), in the pass in which its products come in. Where only some of one birth's parts are
in (their settings), those are drawn first, over the products summed over the rest: lawful, because a subset's sizes
summed over the rest are the same in every frame of the rest (no signal); every such draw is checked against every
frame the parts still out may take, exactly. Nothing else is typed: a full slot weighs 0 by sigma_b, and the place of
a draw is where its parts are one.

A line of Node-clocks; light runs one site a tick. A birth lays a pair (the shared hand e1 x e2 - e2 x e1), a triple
(e1 x e1 x e1 + e2 x e2 x e2) or one quantum spread over absorbers. Each twin rides one site a tick to its detector and
waits there `late` ticks; its take is a whole click. Each part's setting is a split click one tick before its take,
one law-9 draw over its frames: its own light's sizes (1 each) times, at each take it heard by light (strictly inside
its past light cone), the sizes its rule gives that take's end. A setting that hears nothing is free (its digit picks
among its two frames); one that hears a take sets the frame its rule names for it (a machine); a spread quantum's
setting has one frame, its absorbers' own lines. sigma_f is one formula for every hand: the Gaussian norm of the hand's
whole-number overlap with its parties' ends, each end a line of its party's frame (a twin's spinor along its axis,
ANIMATE-B-RECORD; an absorber's own line), summed over the lines a hand carries untaken; sigma_b is an absorber's free
slots. Every draw is law 9's: the rank count of a digit over the weights' running sums, the digit a number modulo
their sum.

The scheduler J, for contrast, draws a birth's band only when all its parts are in.
Part 1: two crossed births, each one's early outcome setting the other's late frame. Part 2: random full boards.
Part 3: one quantum alone, two quanta at one absorber's one free slot at one tick, and a chain of three such quanta.

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
from b_record import BEE, BEE2, GHZ, SINGLET, X, Y, Z, conj, gmul, gnorm, spinor  # noqa: E402

SIGNS = (1, -1)  # a twin's ends: 0 is + along its frame, 1 is -
PAIR_FRAMES = ((Z, X), (BEE, BEE2))  # a, a' at the first party; b, b' at the second (draft D), as axes
TRIPLE_FRAMES = ((X, Y),) * 3
# a machine's sizes over its frames at each end of the take it heard: its first frame at +, its second at -
RULE = ((1, 0), (0, 1))
REVERSE = ((0, 1), (1, 0))


def hand(amplitudes):
    """A hand: per joint line of its parties, a whole-number Gaussian amplitude over the lines it carries untaken
    (one for a twin's hand), in a fixed order."""
    return tuple(sorted(amplitudes.items()))


def basis(axis):
    """A twin's frame: its two spinors along the axis, + and - (ends 0 and 1)."""
    return (spinor(axis, 1), spinor(axis, -1))


def lines(count):
    """A party's own lines, count of them, each a whole-number vector: an absorber's own line of a spread quantum,
    or the silent frame of a part whose setting is still out (z for a twin)."""
    out = []
    for r in range(count):
        row = [(0, 0)] * count
        row[r] = (1, 0)
        out.append(tuple(row))
    return tuple(out)


def squares(share):
    """A whole share as a Gaussian norm over two lines: the first four squares that sum to it (Lagrange)."""
    roots = range(share + 1)
    return next(
        ((a, b), (c, d))
        for a, b, c, d in product(roots, repeat=4)
        if a * a + b * b + c * c + d * d == share
    )


PAIR_HAND = hand({bits: (a,) for bits, a in SINGLET.items()})
TRIPLE_HAND = hand({bits: (a,) for bits, a in GHZ.items()})
PAIR_BASES = tuple(tuple(basis(a) for a in party) for party in PAIR_FRAMES)
TRIPLE_BASES = tuple(tuple(basis(a) for a in party) for party in TRIPLE_FRAMES)


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


def size(hand_, bases, ends):
    """sigma_f, one formula for every hand: the Gaussian norm of the hand's whole-number overlap with its parties'
    ends (each end a line of its party's frame), summed over the lines the hand carries untaken."""
    total = [(0, 0)] * len(hand_[0][1])
    for bits, amplitude in hand_:
        factor = (1, 0)
        for frame, end, bit in zip(bases, ends, bits, strict=True):
            factor = gmul(factor, conj(frame[end][bit]))
        total = [
            (t[0] + u[0], t[1] + u[1])
            for t, u in zip(total, (gmul(a, factor) for a in amplitude), strict=True)
        ]
    return sum(gnorm(t) for t in total)


@cache
def subset_sizes(hand_, bases, known, chosen):
    """The sizes of the chosen parties' joint ends, the first chosen outermost: sigma_f with the known parties' ends
    held (pairs of party and end), summed over the ends of the parties neither known nor chosen."""
    held = dict(known)
    rest = [p for p in range(len(bases)) if p not in held and p not in chosen]
    sizes = []
    for picks in product(*[range(len(bases[p])) for p in chosen]):
        total = 0
        for others in product(*[range(len(bases[p])) for p in rest]):
            full = held | dict(zip(chosen, picks, strict=True)) | dict(zip(rest, others, strict=True))
            total += size(hand_, bases, [full[p] for p in range(len(bases))])
        sizes.append(total)
    return tuple(sizes)


def shares(sizes):
    return [Fraction(w, sum(sizes)) for w in sizes]


def detector(birth, b, site, late, heard=()):
    """A twin: taken at its detector, + or - along the frame its setting sets (its two ends, the frame's two lines,
    at one site and tick). Its setting hears the takes in heard, pairs of a part and its rule (none: a free one)."""
    take = birth["tick"] + abs(site - birth["site"]) + late
    return {
        "birth": b,
        "site": site,
        "late": late,
        "take": take,
        "heard": heard,
        "ends": [(site, take), (site, take)],
    }


def spread(birth, b, absorbers):
    """One quantum spread over absorbers (site, share), taken at one of them, each absorber one of its ends. Its hand
    holds at each absorber the share as a Gaussian norm over two lines it carries and no absorber here resolves; its
    setting has one frame, its absorbers' own lines, and hears nothing."""
    birth["hand"] = hand({(k,): squares(w) for k, (_, w) in enumerate(absorbers)})
    birth["frames"] = ((lines(len(absorbers)),),)
    return {
        "birth": b,
        "heard": (),
        "ends": [(s, birth["tick"] + abs(s - birth["site"])) for s, _ in absorbers],
    }


def frames_of(board, b, frame):
    """A birth's frames, each part's silent (its own lines) where its setting is still out."""
    birth = board["births"][b]
    return tuple(
        birth["frames"][k][frame[i]] if i in frame else lines(len(birth["frames"][k][0]))
        for k, i in enumerate(birth["parts"])
    )


def band_weights(board, band, frame, taken):
    """The band's joint histories (one end per part) and their products sigma_f sigma_b, conditional on what is
    taken: each birth's sigma_f summed over its parts still out, and each limited slot's sigma_b, 0 where full."""
    births, parts = board["births"], board["parts"]
    histories = list(product(*[range(len(parts[i]["ends"])) for i in band]))
    factors = []  # per birth: the places of its parts in the band, and its sigma_f at each of their picks
    for b in sorted({parts[i]["birth"] for i in band}):
        birth = births[b]
        where = [n for n, i in enumerate(band) if parts[i]["birth"] == b]
        party = {i: k for k, i in enumerate(birth["parts"])}
        held = tuple(sorted((party[i], e) for i, e in taken.items() if i in party))
        chosen = tuple(party[band[n]] for n in where)
        sizes = subset_sizes(birth["hand"], frames_of(board, b, frame), held, chosen)
        picks = product(*[range(len(parts[band[n]]["ends"])) for n in where])
        factors.append((where, dict(zip(picks, sizes, strict=True))))
    slots = board.get("slots", {})
    held_ends = [parts[i]["ends"][e] for i, e in taken.items()]
    weights = []
    for history in histories:
        weight = 1
        for where, table in factors:
            weight *= table[tuple(history[n] for n in where)]
        ends = held_ends + [parts[band[n]]["ends"][e] for n, e in enumerate(history)]
        for slot, free in slots.items():
            weight *= ends.count(slot) <= free
        weights.append(weight)
    return histories, weights


def bands(board, ready, taken, joint):
    """The bands among the parts in: one birth's parts together, joined by every limited slot that more of them may
    reach than it has free; each with the Node-clocks where its parts are one (its birth, or the slots that join it)."""
    births, parts = board["births"], board["parts"]
    root = {i: i for i in ready}

    def find(i):
        while root[i] != i:
            i = root[i]
        return i

    for birth in births:
        mine = [i for i in birth["parts"] if i in root]
        for i in mine[1:]:
            root[find(i)] = find(mine[0])
    joined = []
    for slot, free in board.get("slots", {}).items():
        near = [i for i in ready if slot in parts[i]["ends"]]
        held = sum(parts[i]["ends"][e] == slot for i, e in taken.items())
        if near and len(near) + held > free:
            joined.append((slot, near))
            for i in near[1:]:
                root[find(i)] = find(near[0])
    found = {}
    for i in ready:
        found.setdefault(find(i), []).append(i)
    out = []
    for members in sorted(found.values()):
        owners = sorted({parts[i]["birth"] for i in members})
        if joint and any(
            j not in members and j not in taken for b in owners for j in births[b]["parts"]
        ):
            continue
        slots = [("slot", *slot) for slot, near in joined if set(near) <= set(members)]
        out.append((sorted(members), [("birth", owners[0])] if len(owners) == 1 else slots))
    return out


def drawn_weights(board, band, nodes, frame, taken, joint):
    """A band's histories and products, with its no-signal checks where it is one birth's entangled parts drawn as
    their settings come in: against every frame the parts still out may take. Kept per board, since a board's
    runs meet the same bands again."""
    key = (joint, tuple(band), tuple(sorted(frame.items())), tuple(sorted(taken.items())))
    memo = board.setdefault("memo", {})
    if key not in memo:
        births, parts = board["births"], board["parts"]
        histories, weights = band_weights(board, band, frame, taken)
        b, checked = parts[band[0]]["birth"], [0, 0]
        if not joint and nodes == [("birth", b)]:
            out = [k for k, i in enumerate(births[b]["parts"]) if i not in frame]
            for picks in product(*[range(len(births[b]["frames"][k])) for k in out]):
                other = dict(frame) | {
                    births[b]["parts"][k]: pick for k, pick in zip(out, picks, strict=True)
                }
                checked[0] += 1
                checked[1] += shares(weights) == shares(band_weights(board, band, other, taken)[1])
        memo[key] = (histories, weights, checked)
    return memo[key]


def run(board, joint, numbers):
    """The passes of the one rule (J: a birth's band only when all its parts are in): the ends taken and the frames,
    the passes and steps, the no-signal checks; or None where no band can draw and parts are still out (a deadlock)."""
    births, parts = board["births"], board["parts"]
    frame, taken = {}, {}
    checks = [0, 0]  # a layer's law against a frame of the parts still out: checked, and equal
    passes = 1
    steps = max(e[1] - births[p["birth"]]["tick"] for p in parts for e in p["ends"])

    def set_frames():
        """Each setting whose heard takes are in: law 9 over its frames, its own light's sizes times its rules'."""
        for i, p in enumerate(parts):
            if i not in frame and all(j in taken for j, _ in p["heard"]):
                birth = births[p["birth"]]
                weights = [1] * len(birth["frames"][birth["parts"].index(i)])
                for j, rule in p["heard"]:
                    weights = [w * r for w, r in zip(weights, rule[taken[j]], strict=True)]
                frame[i] = law9(weights, numbers(("det", i)))

    set_frames()
    while len(taken) < len(parts):
        ready = [i for i in range(len(parts)) if i in frame and i not in taken]
        now = []
        for band, nodes in bands(board, ready, taken, joint):
            histories, weights, checked = drawn_weights(board, band, nodes, frame, taken, joint)
            checks[0], checks[1] = checks[0] + checked[0], checks[1] + checked[1]
            history = histories[law9(weights, sum(numbers(node) for node in nodes))]
            for i, e in zip(band, history, strict=True):
                taken[i] = e
                now.append(parts[i]["ends"][e][1] - births[parts[i]["birth"]]["tick"])
        if not now:
            return None
        passes, steps = passes + 2, steps + 2 * max(now)
        set_frames()
    return {
        "frame": frame,
        "taken": taken,
        "passes": passes,
        "steps": steps,
        "checks": checks,
    }


def depth(board):
    """The longest chain of settings: each one more than the deepest setting whose take it heard (a free one 1)."""
    known, parts = {}, board["parts"]
    while len(known) < len(parts):
        for i, d in enumerate(parts):
            if i not in known and all(j in known for j, _ in d["heard"]):
                known[i] = 1 + max((known[j] for j, _ in d["heard"]), default=0)
    return max(known.values())


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
    q = {"site": 50, "tick": 0, "hand": PAIR_HAND, "frames": PAIR_BASES, "parts": [0, 1]}
    p = {"site": 100, "tick": 0, "hand": PAIR_HAND, "frames": PAIR_BASES, "parts": [2, 3]}
    parts = [
        detector(q, 0, 40, 0),
        detector(q, 0, 150, 0, ((2, RULE),)),
        detector(p, 1, 120, 0),
        detector(p, 1, 10, 0, ((0, RULE),)),
    ]
    for d in parts:
        for j, _ in d["heard"]:
            h = parts[j]
            assert h["take"] + abs(h["site"] - d["site"]) < d["take"] - 1, "heard outside the past cone"
    return {"births": [q, p], "parts": parts}


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
        for gq, gp in product(range(2), range(2)):  # the guessed ends of both early takes
            drawn = []
            for f, guess, n in ((fq, gp, nq), (fp, gq, np_)):
                bases = (PAIR_BASES[0][f], PAIR_BASES[1][law9(RULE[guess], 0)])
                ends = list(product(range(2), range(2)))[
                    law9(subset_sizes(PAIR_HAND, bases, (), order), n)
                ]
                drawn.append(dict(zip(order, ends, strict=True)))
            if drawn[0][0] == gq and drawn[1][0] == gp:
                seconds = (law9(RULE[gp], 0), law9(RULE[gq], 0))
                signs = (SIGNS[gq], SIGNS[drawn[0][1]], SIGNS[gp], SIGNS[drawn[1][1]])
                found.append((fq, fp, *seconds, *signs))
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
    # the first draws' rooms are 2 (at z) and 4 (at x), the second's 29 and 58: 4 and 58 meet each digit alike
    for fq, fp, n1q, n1p, n2q, n2p in product(
        range(2), range(2), range(4), range(4), range(58), range(58)
    ):
        stream = {("det", 0): [fq], ("det", 2): [fp], ("birth", 0): [n1q, n2q], ("birth", 1): [n1p, n2p]}
        stream |= {
            ("det", 1): [0],
            ("det", 3): [0],
        }  # the machines' own digits: their rule's sizes decide
        used = dict.fromkeys(stream, 0)

        def numbers(key, stream=stream, used=used):
            used[key] += 1
            return stream[key][used[key] - 1]

        out = run(board, False, numbers)
        key = (fq, fp, out["frame"][1], out["frame"][3]) + tuple(
            SIGNS[out["taken"][i]] for i in range(4)
        )
        law[key], total = law.get(key, 0) + 1, total + 1
    passes = run(board, False, lambda key: 0)["passes"]
    print(
        f"  the one rule, each part drawn as its setting comes back: one history at every one of {total} digit sets, {passes} passes;"
    )
    print(f"    its law is nature's sequential law: {natures(law, total)}")
    print()


# Part 2: random full boards


def random_board(rng, count, line, machines):
    """Births of pairs and triples at random sites and ticks; each detector at its own site and take tick; a share of
    the detectors are machines hearing a random take strictly inside their past light cone."""
    board, used = {"births": [], "parts": []}, set()
    for b in range(count):
        triple = rng.random() < 0.3
        birth = {
            "site": rng.randrange(line),
            "tick": rng.randrange(24),
            "hand": TRIPLE_HAND if triple else PAIR_HAND,
        }
        birth["frames"], birth["parts"] = (TRIPLE_BASES if triple else PAIR_BASES), []
        for _ in range(3 if triple else 2):
            d = detector(birth, b, rng.randrange(line), rng.randrange(4))
            while (d["site"], d["take"]) in used:
                d = detector(birth, b, rng.randrange(line), rng.randrange(4))
            used.add((d["site"], d["take"]))
            birth["parts"].append(len(board["parts"]))
            board["parts"].append(d)
        board["births"].append(birth)
    parts = board["parts"]
    for d in parts:
        heard = [
            j for j, h in enumerate(parts) if h["take"] + abs(h["site"] - d["site"]) < d["take"] - 1
        ]
        if heard and rng.random() < machines:
            d["heard"] = ((rng.choice(heard), RULE if rng.random() < 0.5 else REVERSE),)
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


# Part 3: quanta at absorbers' free slots


def drawn_law(board, spans):
    """The one rule run at every digit of the Node-clocks that draw (each over its span): the law of the ends taken,
    and whether every quantum is taken once and no slot past its free count, at every digit."""
    law, whole = {}, True
    for digits in product(*[range(n) for _, n in spans]):
        given = dict(zip([key for key, _ in spans], digits, strict=True))
        out = run(board, False, lambda key, given=given: given.get(key, 0))
        ends = [board["parts"][i]["ends"][out["taken"][i]] for i in range(len(board["parts"]))]
        whole &= len(out["taken"]) == len(board["parts"])
        whole &= all(ends.count(slot) <= free for slot, free in board.get("slots", {}).items())
        key = tuple(out["taken"][i] for i in range(len(board["parts"])))
        law[key] = law.get(key, 0) + 1
    total = sum(law.values())
    return {key: Fraction(n, total) for key, n in sorted(law.items())}, whole


def quanta(absorbers, slots):
    """Births of one spread quantum each, at sites 10, 30, 50, ...; absorbers per quantum (site, share)."""
    board = {"births": [], "parts": [], "slots": slots}
    for b, ends in enumerate(absorbers):
        birth = {"site": 10 + 20 * b, "tick": 0, "parts": [b]}
        board["parts"].append(spread(birth, b, ends))
        board["births"].append(birth)
    return board


def named(board, law):
    names = {4: "x", 20: "z", 36: "y", 40: "z2", 56: "w"}
    return ", ".join(
        "/".join(names[board["parts"][i]["ends"][e][0]] for i, e in enumerate(key)) + f" {p}"
        for key, p in law.items()
    )


def part3():
    print(
        "Part 3: quanta at absorbers' free slots, every draw by the one rule (run() above, nothing added)"
    )
    alone = quanta([[(4, 2), (20, 3)]], {(20, 10): 1})
    law, whole = drawn_law(alone, [(("birth", 0), 5)])
    print(
        f"  A alone over x and z (sizes 2 and 3), its band its own birth: {named(alone, law)}: Born; whole {whole}"
    )
    a, b = {"x": 2, "z": 3}, {"y": 3, "z": 2}
    counts = {}
    for na, nb in product(range(30), range(30)):  # 30 is a multiple of every room (5, 2 and 3)
        found = 0
        for ha, hb in product(a, b):
            wa = [
                a["x"],
                a["z"] * (hb != "z"),
            ]  # each source alone, z's slot as the other leaves it
            wb = [b["y"], b["z"] * (ha != "z")]
            found += (
                ("x", "z")[law9(wa, na)] == ha
                and ("y", "z")[law9(wb, nb)] == hb
                and (ha, hb) != ("z", "z")
            )
        counts[found] = counts.get(found, 0) + 1
    shown = ", ".join(f"{n} with {k}" for k, n in sorted(counts.items()))
    print("  A and B (y and z, sizes 3 and 2), both reaching z at one tick, where one slot is free:")
    print(
        f"    each source drawing alone, the slot as sigma_b: of 900 digit pairs, {shown} histories that agree"
    )
    tie = quanta([[(4, 2), (20, 3)], [(36, 3), (20, 2)]], {(20, 10): 1})
    law, whole = drawn_law(tie, [(("slot", 20, 10), 19)])
    print(
        f"    the one rule, their band drawn at z where they are one: {named(tie, law)}; whole {whole}"
    )
    chain = quanta(
        [[(4, 2), (20, 3)], [(20, 2), (40, 2)], [(40, 3), (56, 2)]],
        {(20, 10): 1, (40, 10): 1},
    )
    law, whole = drawn_law(chain, [(("slot", 20, 10), 40), (("slot", 40, 10), 40)])
    print(
        "  a chain: A over x and z (2, 3), B over z and z2 (2, 2), C over z2 and w (3, 2), one slot free at z and at z2:"
    )
    print(
        f"    the one rule, one band drawn at z and z2, their digits summed: {named(chain, law)}; whole {whole}"
    )


def main():
    print(
        "Rule B's scheduler on a full board, one rule for every band: each band drawn once, where its parts are"
    )
    print("one, each part as its setting comes back (L); J, for contrast, draws each birth whole")
    print()
    part1()
    part2()
    part3()


if __name__ == "__main__":
    main()
