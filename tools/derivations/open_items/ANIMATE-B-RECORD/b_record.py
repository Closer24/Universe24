"""Toy: a record written by B's draw, for the decoder to read (Animate; the Boss's asks of 09:39 and 10:06 UTC on
2026-10-29, #2187 6493239195 item 4 and 6493783603; Animate's 6494185513 item 5).

B is the draw at the Node-clock where the parts were one (decision 31; reading 15 settled by the Boss): the backward
half brings each detector's frame back to the source, the draw there is law 9's over sigma_f sigma_b, and each twin
carries its own outcome out. This writer stands in for the engine and writes what the record would hold, in the
schema 1.1's line kinds with the 1.2 fields proposed (6494185513 item 2):
  - the lay: a whole click at the source laying the pair, the triple or the quantum;
  - the split click at the source: its parts the joint outcomes (a sign per party; for one quantum, 1 at the absorber
    that takes it), sizes (sigma_f), back (sigma_b, G6), c over room and drawn (law 9), and the frames brought back,
    each with its detector's site;
  - each detector's setting chosen late, a split click of its own light over its two frames (axes);
  - each detector's take, a whole click naming the lay it takes from (birth, G5), with the frame it took in (detector)
    and the part it took (written), in 1.1's axis form.
Nothing is typed but the frames and the hands: sigma_f is the Gaussian norm of the hand's whole-number overlap with
the frames' spinors (the singlet's sizes are David's (4, 25, 25, 4), (9, 49, 49, 9) and (49, 9, 9, 49), toys-5
4f5886b94). Every sigma_b is 1: each detector takes whatever comes, so the future past the frames is silent.

The forms written beside B, each the control of a reading: F, one forward board with the history kept (the twins'
direction, the triple's answers and each absorber's draw made forward alone, no frames brought back, no back), and
four writers that each break one thing of B: signal (the pair's sizes moved by TILT toward the second twin's + where
the first detector chose a', and toward its - where it chose a), stale (every fourth pair's second frame brought back is the one its detector did not
choose), early (every setting chosen REACH rounds before its birth) and off (the drawn part is the rank count of the
digit after c).

usage: python -I b_record.py [folder]  (writes the six records there, or in a temporary folder, and reads each)
"""

import hashlib
import json
import sys
import tempfile
from itertools import product
from pathlib import Path

ORDER = "z fastest: the site (x sy + y) sz + z"  # the runner's (src/tensor24/runner/run.py)
SIDES = (32, 32, 32)
REACH = 8  # the Meshes from each source to each of its detectors; light runs one Mesh a tick
GAP = 2 * REACH + 2  # the rounds between two births at one source
FIRST = (
    REACH + 1
)  # the first birth, so that an early choice, REACH rounds before it, stands on the record
BIRTHS = 2048  # births at each source
KINDS = ("whole", "split", "turnover", "rate", "books")  # the schema's order of kinds within a round
FORMS = ("B", "F", "signal", "stale", "early", "off")
TILT = 4  # the signal writer's tilt in the pair's whole-number sizes: the least size at a is 4


def site(x, y, z):
    return (x * SIDES[1] + y) * SIDES[2] + z


# Gaussian integers as (re, im); a frame is its + spinor (p, q), the - spinor (-conj q, conj p)
def gmul(u, v):
    return (u[0] * v[0] - u[1] * v[1], u[0] * v[1] + u[1] * v[0])


def conj(u):
    return (u[0], -u[1])


def gnorm(u):
    return u[0] * u[0] + u[1] * u[1]


def spinor(frame, sign):
    p, q = frame
    return frame if sign == 1 else ((-q[0], q[1]), (p[0], -p[1]))


def reading(frame, sign=1):
    """The frame in 1.1's axis form: rho = |p|^2 + |q|^2 and the spin (2 conj(p) q, |p|^2 - |q|^2), signed."""
    p, q = frame
    w = gmul(conj(p), q)
    spin = (2 * w[0], 2 * w[1], gnorm(p) - gnorm(q))
    return {"rho": gnorm(p) + gnorm(q), "spin": [sign * c for c in spin]}


Z, X, Y = ((1, 0), (0, 0)), ((1, 0), (1, 0)), ((1, 0), (0, 1))  # the axes z, x and y
BEE, BEE2 = ((5, 0), (2, 0)), ((5, 0), (-2, 0))  # (20, 0, 21) / 29 and (-20, 0, 21) / 29
SINGLET = {(0, 1): (1, 0), (1, 0): (-1, 0)}  # e1 x e2 - e2 x e1, the shared hand the 24 forces (David)
GHZ = {(0, 0, 0): (1, 0), (1, 1, 1): (1, 0)}  # e1 x e1 x e1 + e2 x e2 x e2, put in by hand
PAIR = {
    "train": 0,
    "at": site(16, 16, 16),
    "hand": SINGLET,
    "parties": ((site(8, 16, 16), (Z, X)), (site(24, 16, 16), (BEE, BEE2))),
}
TRIPLE = {
    "train": 1,
    "at": site(16, 16, 4),
    "hand": GHZ,
    "parties": tuple((site(*place), (X, Y)) for place in ((8, 16, 4), (24, 16, 4), (16, 24, 4))),
}
SPREAD = {
    "train": 2,
    "at": site(16, 16, 28),
    "absorbers": ((site(8, 16, 28), 5), (site(24, 16, 28), 3), (site(16, 8, 28), 2)),
}
CHOOSERS = 3
DIRECTIONS = [tuple(s * e for e in axis) for axis in ((1, 0, 0), (0, 1, 0), (0, 0, 1)) for s in (1, -1)]
CARDS = (
    "the twins: the shared hand e1 x e2 - e2 x e1",
    "the triples: the shared hand e1 x e1 x e1 + e2 x e2 x e2",
    "the spread quantum",
    "the choosers' light",
)


def size(hand, frames, signs):
    """sigma_f: the Gaussian norm of the hand's whole-number overlap with the frames' spinors at the signs."""
    total = (0, 0)
    for bits, amplitude in hand.items():
        term = amplitude
        for frame, sign, bit in zip(frames, signs, bits, strict=True):
            term = gmul(term, conj(spinor(frame, sign)[bit]))
        total = (total[0] + term[0], total[1] + term[1])
    return gnorm(total)


def law9(weights, d):
    """Law 9: the part at digit d, the rank count of d over the weights' running sums."""
    total = 0
    for part, w in enumerate(weights):
        total += w
        if d < total:
            return part
    raise ValueError("a digit past the weights' sum")


class Digits:
    """A fixed stream of fair digits, SHA-256 of a label and a counter (the vernier's stand-in), by rejection."""

    def __init__(self, label):
        self.label, self.count, self.left = label, 0, b""

    def below(self, bound):
        span = 1 << 32
        while True:
            while len(self.left) < 4:
                self.left += hashlib.sha256(f"{self.label}:{self.count}".encode()).digest()
                self.count += 1
            x, self.left = int.from_bytes(self.left[:4], "big"), self.left[4:]
            if x < span - span % bound:
                return x % bound


def split(r, at, train, sizes, digits, back=True, off=False, **fields):
    """A split click's line: sizes, back (sigma_b, all 1), c over room, drawn by law 9 (or off by one)."""
    room = sum(sizes)
    c = digits.below(room)
    line = {"kind": "split", "round": r, "site": at, "count": r, "train": train, "sizes": sizes}
    line |= {"back": [1] * len(sizes)} if back else {}
    line |= {"c": c, "room": room, "drawn": law9(sizes, (c + 1) % room if off else c)}
    return line | fields


def whole(r, at, train, birth=None, frame=None, sign=1):
    """A whole click's line: the lay (no birth) or a take naming its birth (G5), with its frame and its part."""
    line = {"kind": "whole", "round": r, "site": at, "count": r, "train": train, "q": 1}
    if birth is not None:
        line["birth"] = list(birth)
    if frame is not None:
        line["detector"] = {"train": train} | reading(frame)
        line["written"] = {"train": train} | reading(frame, sign)
    return line


def chosen(lines, r0, place, frames, digits, form):
    """A detector's late setting: its light's split click over its two frames, REACH - 1 rounds after the birth."""
    when = r0 - REACH if form == "early" else r0 + REACH - 1
    axes = [reading(frame) for frame in frames]
    line = split(when, place, CHOOSERS, [1, 1], digits, back=form != "F", axes=axes)
    lines.append(line)
    return frames[line["drawn"]]


def entangled(lines, source, r0, k, form, digits):
    """One pair or triple: the lay, the late settings, the draw at the source over sigma_f sigma_b, the takes."""
    train, at, parties = source["train"], source["at"], source["parties"]
    lines.append(whole(r0, at, train))
    used = [chosen(lines, r0, place, frames, digits[place], form) for place, frames in parties]
    brought = list(used)
    if form == "stale" and train == 0 and k % 4 == 0:
        brought[1] = [f for f in parties[1][1] if f != used[1]][0]
    if form == "F":
        signs = forward(lines, source, r0, used, digits)
    else:
        parts = list(product((1, -1), repeat=len(parties)))
        sizes = [size(source["hand"], brought, signs) for signs in parts]
        if form == "signal" and train == 0:
            tilt = TILT if used[0] == X else -TILT
            sizes = [w + tilt * signs[1] for w, signs in zip(sizes, parts, strict=True)]
        frames = [{"site": place} | reading(f) for (place, _), f in zip(parties, brought, strict=True)]
        line = split(r0, at, train, sizes, digits[at], off=form == "off", parts=parts, frames=frames)
        lines.append(line)
        signs = parts[line["drawn"]]
    for (place, _), frame, sign in zip(parties, used, signs, strict=True):
        lines.append(whole(r0 + REACH, place, train, (r0, at), frame, sign))


def forward(lines, source, r0, used, digits):
    """F: the pair's direction or the triple's answers drawn at the birth, each detector reading them alone."""
    train, at, parties = source["train"], source["at"], source["parties"]
    if train == 0:
        line = split(r0, at, train, [1] * len(DIRECTIONS), digits[at], back=False, parts=DIRECTIONS)
        lines.append(line)
        lam, signs = DIRECTIONS[line["drawn"]], []
        for n, ((place, _), frame) in enumerate(zip(parties, used, strict=True)):
            spin, rho = reading(frame)["spin"], reading(frame)["rho"]
            mu = sum(m * s for m, s in zip(lam, spin, strict=True)) * (1 if n == 0 else -1)
            own = split(r0 + REACH, place, train, [rho + mu, rho - mu], digits[place], back=False)
            lines.append(own | {"parts": [[1], [-1]]})
            signs.append((1, -1)[own["drawn"]])
        return signs
    answers = list(product((1, -1), repeat=2 * len(parties)))
    line = split(r0, at, train, [1] * len(answers), digits[at], back=False, parts=answers)
    lines.append(line)
    held = answers[line["drawn"]]
    return [
        held[2 * n + frames.index(f)]
        for n, ((_, frames), f) in enumerate(zip(parties, used, strict=True))
    ]


def spread(lines, r0, form, digits):
    """One quantum over three absorbers: one draw at the source under B, each absorber alone under F."""
    train, at, absorbers = SPREAD["train"], SPREAD["at"], SPREAD["absorbers"]
    lines.append(whole(r0, at, train))
    weights = [w for _, w in absorbers]
    if form == "F":
        for place, w in absorbers:
            own = split(r0 + REACH, place, train, [w, sum(weights) - w], digits[place], back=False)
            lines.append(own | {"parts": [[1], [0]]})
            if own["drawn"] == 0:
                lines.append(whole(r0 + REACH, place, train, (r0, at)))
        return
    parts = [[int(n == m) for m in range(len(absorbers))] for n in range(len(absorbers))]
    frames = [{"site": place} for place, _ in absorbers]
    line = split(r0, at, train, weights, digits[at], off=form == "off", parts=parts, frames=frames)
    lines.append(line)
    lines.append(whole(r0 + REACH, absorbers[line["drawn"]][0], train, (r0, at)))


def record(form):
    """The record's lines under one form: the header, the events in the schema's order, the end."""
    places = [PAIR["at"], TRIPLE["at"], SPREAD["at"]]
    places += [p for p, _ in PAIR["parties"] + TRIPLE["parties"]] + [p for p, _ in SPREAD["absorbers"]]
    digits = {
        place: Digits(f"{place}") for place in places
    }  # one stream per Node-clock, alike in every form
    lines = []
    for k in range(BIRTHS):
        r0 = FIRST + GAP * k
        entangled(lines, PAIR, r0, k, form, digits)
        entangled(lines, TRIPLE, r0, k, form, digits)
        spread(lines, r0, form, digits)
    lines.sort(key=lambda e: (e["round"], KINDS.index(e["kind"]), e["site"], e["train"]))
    cards = [
        {"index": n, "label": label, "kinds": [], "part": 0, "winding": 1}
        for n, label in enumerate(CARDS)
    ]
    head = {"kind": "header", "record": f"b_record_{form}.jsonl", "major": 1, "minor": 2}
    head |= {"engine": f"a toy beside the engine: ANIMATE-B-RECORD/b_record.py, form {form}"}
    head |= {"runner": "synchronous", "files": [], "sides": list(SIDES), "order": ORDER, "trains": cards}
    text = "".join(json.dumps(line) + "\n" for line in lines)
    end = {
        "kind": "end",
        "rounds": FIRST + GAP * (BIRTHS - 1) + REACH,
        "digest": hashlib.sha256(text.encode()).hexdigest(),
    }
    return json.dumps(head) + "\n" + text + json.dumps(end) + "\n"


def main():
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import b_readings

    with tempfile.TemporaryDirectory() as temporary:
        folder = Path(sys.argv[1] if len(sys.argv) > 1 else temporary)
        folder.mkdir(parents=True, exist_ok=True)
        paths = {}
        for form in FORMS:
            paths[form] = folder / f"b_record_{form}.jsonl"
            paths[form].write_text(record(form), encoding="utf-8")
        b_readings.report(paths)
        print()
        print(
            f"B's record, its first births (rounds {FIRST} to {FIRST + REACH}): the lays and the sources' split clicks"
        )
        print(f"at {FIRST}, the late settings at {FIRST + REACH - 1}, the takes at {FIRST + REACH}")
        for text in paths["B"].read_text(encoding="utf-8").splitlines()[1:]:
            if json.loads(text)["round"] > FIRST + REACH:
                break
            print(f"  {text}")


if __name__ == "__main__":
    main()
