"""The decoder's reads of the record, integers only (the owner's word: no float anywhere, every reading a quotient with its remainder or a count over a span): the record as read from the run's log alone (credits, births, refusals; the rows of the board's course; the Node lines), cut to an interval for a gate read as it first shows (`Record.to`), its own names for the planes (never the Node's), the species solved from a credit's frame and the nearest name; the verdicts' kinds and their one reader (kind_of, shown); the gates themselves are the table of gates.py, the rows read from the clicks clicks.py, the board's board.py and the widened rows predicates.py."""

from __future__ import annotations

from bisect import bisect_right
from collections import Counter
from typing import Any

from event_universe.core import rates, rule3
from event_universe.core.rates import sine_rim
from event_universe.meshes import Mesh, cross, through_mesh
from event_universe.rim import rim_of
from event_universe.trains import HAND

MIL = 1000000  # readings in parts per million
HUNDRED = 100  # readings in hundredths
THOUSAND = 1000  # readings in thousandths
FEW = 10  # the fewest decoded credits for the dilation's two halves
SPANS = 20  # the fewest spans for the lengthening's two halves
HALF = 2  # a half: a count div 2, and a majority as a count times 2 above the whole
PAIR = 2  # two of a kind: the two ends of a Link, the two parts of a plane's pair, two bodies, two beats, two marks
THIRDS = 3  # the thirds of a run (its last third), of the half charge (T div 2 div 3)
QUARTERS = 4  # the quarters of a run (a body standing into the last quarter)
LISTED = 8  # the most entries a row prints of a course (its first eight) and the eighths a course is sampled at
SHORT_LIST = 6  # the most falls and steps a row prints
FOUR_LISTED = 4  # the most returns the rows' reading prints
MAX = 2  # the index of the max in a row's min / mean / max
NOTCHES_BACK = (
    2,
    1,
    0,
)  # the carrier's three levels read from the Node lines: before the interval, at its start, after it, as lines behind the interval's own
Rational = tuple[int, int]
NOT = "NOT"  # the word a verdict begins with where the gate is not shown, read or reached
KINDS = (
    "SHOWN in part",
    f"{NOT} SHOWN",
    f"{NOT} REACHED",
    f"{NOT} READ",
    "SHOWN",
)  # the verdicts' kinds, the longer first
RESTATED = (
    "as gate"  # a verdict restating another gate's begins so, the gate's number and a colon after it
)


def kind_of(verdict: str) -> str:
    """A verdict's kind (SHOWN, SHOWN in part, or NOT with SHOWN, READ or REACHED), a restated row's by the gate it restates; the one reader of the kind from the words."""
    words = verdict.split(": ", 1)[1] if verdict.startswith(RESTATED) else verdict
    return next((kind for kind in KINDS if words.startswith(kind)), f"{NOT} READ")


def cause_of(verdict: str) -> str:
    """The verdict's own words after its kind, the cause where not SHOWN, one clause."""
    words = verdict.split(": ", 1)[1] if verdict.startswith(RESTATED) else verdict
    kind = kind_of(verdict)
    if words.startswith(kind):
        words = words[len(kind) :]
    return words.strip(" :;").split(";")[0].strip()


def unread_words(why: str, predicate: str) -> str:
    """The verdict of a row the record cannot carry: NOT READ, why, and the predicate it would be read by; the one form of the words."""
    return f"{NOT} READ: {why}; the predicate: {predicate}"


def shown(verdict: str) -> bool:
    """A verdict that shows (whole or in part) in its own right: a row restating another gate's verdict shows no event line of its own, the gate it restates has the line."""
    return verdict.startswith("SHOWN")


class Chart:
    """The record as the decoder reads it: the two files' integers, the planes with a gap by their legs under the decoder's names, the log's credits and births, the rows of the board's course."""

    def __init__(self, run: dict[str, Any]) -> None:
        self.run = run
        self.rim = int(run["den"])
        self.action = int(run["universe"]["integers"]["quantum_action"])
        self.full_rate, self.G, self.key = int(run["gamma"]), int(run["G"]), int(run["T"])
        rows = run["universe"]["rows"]
        planes = {
            tuple(int(x) for x in r["pair"]) for r in rows if int(r["shape"]) == HAND and r.get("pair")
        }
        gapped = sorted((sine_rim(num, self.rim), num) for num, den in planes if num != den)
        self.NL = len(gapped)
        self.NAMES: dict[int, tuple[str, int]] = {
            num: (f"gapped {k}", leg) for k, (leg, num) in enumerate(gapped)
        }
        self.NAMES[self.rim] = ("gap 0", 0)
        self.gear_pinion = [int(num) for num in run["planes"]]
        records = sorted(
            (r for r in rows if r.get("pair") and int(r["shape"]) == HAND),
            key=lambda r: int(r["pair"][0]) == int(r["pair"][1]),
        )
        shapes = [int(r["shape"]) for r in records]
        assert [int(r["pair"][0]) for r in records] == self.gear_pinion
        self.gear_name = [
            self.NAMES[num][0] if shape == HAND else f"shape-{shape} at {self.NAMES[num][0]}"
            for num, shape in zip(self.gear_pinion, shapes, strict=True)
        ]
        self.log = run["log"]
        self.chimes = [entry for entry in self.log if entry["event"] == "credit"]
        self.fittings = [entry for entry in self.log if entry["event"] == "birth"]
        self.unwinds = [entry for entry in self.log if entry["event"] in ("birth", "credit")]
        self.cube = int(run["cube"])
        self.rows = run["rows"]
        self.clocks = run.get("nodes", [])
        self.ticks = int(run["intervals"])
        self.teeth = rule3.teeth_of(self.rim, self.full_rate, self.G)
        self.memo: dict[str, Any] = {}

    def to(self, i: int) -> Chart:
        """The record cut to the intervals 1 to i (its log, its rows and its Node lines, each in the run's order, cut by a search on the interval), for a gate read as it first shows; the solves and the run back stay the whole record's."""
        cuts: dict[int, Chart] = self.memo.setdefault("cuts", {})
        if i in cuts:
            return cuts[i]
        found = Chart.__new__(Chart)
        found.__dict__.update(self.__dict__)
        found.ticks = i
        for name in ("log", "chimes", "fittings", "unwinds"):
            whole = getattr(self, name)
            setattr(found, name, whole[: bisect_right(whole, i, key=lambda e: int(e["i"]))])
        found.rows = self.rows[: bisect_right(self.rows, i, key=lambda r: int(r["i"]))]
        found.clocks = self.clocks[: bisect_right(self.clocks, i, key=lambda n: int(n["i"]))]
        cuts[i] = found
        return found

    def index(self, node: list[int] | tuple[int, ...]) -> int:
        """A Node's index in the Node lines from its (x, y, z)."""
        x, y, z = (int(n) for n in node)
        return x * self.cube * self.cube + y * self.cube + z

    def clock(self, index: int) -> list[int]:
        """A Node's (x, y, z) from its index in the Node lines."""
        x = int(rule3.carries(index, self.cube * self.cube))
        y = int(rule3.carries(index - x * self.cube * self.cube, self.cube))
        return [x, y, index - (x * self.cube + y) * self.cube]

    def distance(self, a: tuple[int, ...], b: tuple[int, ...]) -> int:
        """The Link distance between two Nodes on the torus, the shorter way on every axis."""
        return sum(min(abs(x - y), self.cube - abs(x - y)) for x, y in zip(a, b, strict=True))

    def bobs_of(self) -> dict[tuple[tuple[int, ...], int], list[dict[str, Any]]]:
        """The credits grouped by (Node, line), a body's track, in the log's order; read once per cut."""
        key = f"bodies to {self.ticks}"
        if key not in self.memo:
            found: dict[tuple[tuple[int, ...], int], list[dict[str, Any]]] = {}
            for c in self.chimes:
                found.setdefault((tuple(c["node"]), c["line"]), []).append(c)
            self.memo[key] = found
        bodies: dict[tuple[tuple[int, ...], int], list[dict[str, Any]]] = self.memo[key]
        return bodies

    def first_stopped(self) -> dict[int, int]:
        """The first frozen interval of every Node that freezes (the Link pace 0, BH-S1's mask on the Node lines), the Node's index to the interval; the one reader of the horizon's Nodes for rows 14, 34 and 61."""
        first: dict[int, int] = {}
        for line in self.clocks:
            for at in line["frozen"]:
                first.setdefault(int(at), int(line["i"]))
        return first

    def sweeps_of(self) -> list[tuple[int, int]]:
        """The two children's own charges at every birth, in the births' order (H-Children-Charge-Bug-1, the Boss's 6410696786): a child laid by the child's lay carries its sense times half the quantum of action (the Wronskian of its own two levels), a child laid as the exact take at -1 (a merger's light, the line's `exact_lay` at its end) carries 0; the log's W_children is the record's Wronskian at the Node after the lay (the standing level's and the cross term in it) and is read for the residue by name, never for the sign."""

        def own(b: dict[str, Any], k: int) -> int:
            exact = b.get("exact_lay", [None, None])[k] is not None
            return 0 if exact else int(b["senses"][k]) * (self.action // HALF)

        return [(own(b, 0), own(b, 1)) for b in self.fittings]

    def signs_of(self) -> list[int]:
        """The births' children's senses as the signs of their own charges, in the births' order (0 for a child laid as light)."""
        return [sign(w) for pair in self.sweeps_of() for w in pair]

    def unwinds_of(self) -> tuple[int, int]:
        """The sums over the births of what the takes took and what they booked."""
        return sum(b["taken"] for b in self.fittings), sum(b["booked"] for b in self.fittings)

    def fitted_of(self) -> Counter[str]:
        """The births by the species born (the plane's name)."""
        return Counter(self.gear_name[b["line_pair"]] for b in self.fittings)

    def lifts_fitted(self) -> list[str]:
        """The lifts born: the distinct gapped planes with a birth, the plane at the gap 0 (light, no lift) left out; the lifts the universe names are its gapped planes, the typed points of den's circle (self.NL), the former constant 3 the toy universe's count of them (the Boss's task of 2026-10-27, 10:1x UTC: the number read from the record and no file of src)."""
        light = self.NAMES[self.rim][0]
        return sorted(name for name in self.fitted_of() if name != light)

    def advanced_at_nothing(self) -> list[int]:
        """The magnitude |W| of every child laid where its plane stood at nothing, in the births' order."""
        return [
            abs(w)
            for b in self.fittings
            for w, stood in zip(b["W_children"], b.get("stood", [[0], [0]]), strict=True)
            if not any(stood)
        ]

    def rim_points(self) -> list[tuple[int, int]]:
        """den's circle, read once per record (circle.circle_of)."""
        found: list[tuple[int, int]] = self.memo.setdefault("circle", rim_of(self.rim))
        return found


def carries(a: int, b: int, scale: int = 1) -> int | None:
    """The integer reading of a / b: the quotient of the scaled numerator (the remainder dropped)."""
    return None if b == 0 else int(rule3.carries(a * scale, b))


def sign(x: int) -> int:
    """The sign of an integer: -1, 0 or 1."""
    return (x > 0) - (x < 0)


def cmp_rat(p: Rational, q: Rational) -> int:
    """Order two rationals (n, d) with d > 0 by cross multiplication."""
    return sign(int(cross(p[0], p[1], q[0], q[1])))


def regulator_notches(record: Chart, credit: dict[str, Any]) -> tuple[int, int, int]:
    """The carrier's three levels at the credit's Node from the record's Node lines: before the interval, at its start and after it (Gamma before the first interval)."""
    index, i = record.index(credit["node"]), int(credit["i"])
    lines = record.run["nodes"]
    found = [
        lines[i - 1 - back]["X"][index] if i - 1 - back >= 0 else record.full_rate
        for back in NOTCHES_BACK
    ]
    before, start, after = found
    return int(before), int(start), int(after)


def reckon(record: Chart, credit: dict[str, Any]) -> Rational | None:
    """The species from the frame in exact integers under the symmetric ride (interval.py's form), the plane's frame: a riding line's momentum P_in = W_in (a_now - a_before) + r - W_in div 2 at the mean wall W_in = (w div 2)(X_before + X_now), the kick P_out = P_in + X_now F with F = SUM_j R_j (m_j - z) - D z, the one division a_next = a_now + (P_out + W_out div 2) div W_out at W_out = (w div 2)(X_now + X_next); from the record's levels v = a_next - a_now gives X_now F to the remainders' width, E = v W_out - W_in (a_now - a_before), and F is linear in num: num = (E + 12 den p_0^2 G^2 z X_now) / ((A + 12 p_0^2 G^2 z) X_now) with A = SUM_j 2 p_i^2 Q_j G^2 (m_j - z) over the turned arrivals; x = num / den as the rational (N, D), D > 0."""
    f, content = credit["frame"], credit["content"]
    if "re_now" not in f:
        return None
    gamma, den, unit = record.full_rate, record.rim, record.G
    p0, pi = rates.rate(gamma, content), rates.mesh_rate(gamma, content)
    w = record.teeth
    x_b, x_n, x_x = regulator_notches(record, credit)
    w_in, w_out = rule3.mean_teeth_of(w, x_b, x_n), rule3.mean_teeth_of(w, x_n, x_x)
    zb = (f["re_start_before"], f["im_start_before"])
    zn = (f["re_start_now"], f["im_start_now"])
    zx = (
        f["re_now"],
        f["im_now"],
    )  # the state after the step is the levels now (CL-S2, the Boss's 6417815695 and David's e03b70401: the former `stepped` field was the state the swap replaced, equal to the levels now at every credit of a Node that did not turn, and is struck; the reader reads what the algebra fixes)
    if zn == (0, 0):
        return None
    scale, phases, odd, frames = f["X"], f["phases"], f["odd"], f["frames"]
    e = tuple((zx[k] - zn[k]) * w_out - w_in * (zn[k] - zb[k]) for k in range(PAIR))
    weight = rule3.spring(0, 1, p0, unit)
    reaches = rule3.gearing(1, den, gamma, p0, pi, tuple(f["factors"]), unit).grips
    a_re = a_im = 0
    for port, (a, b) in enumerate(zip(f["re_neighbours_start"], f["im_neighbours_start"], strict=True)):
        at = Mesh(None, frames[port], phases[port][0], phases[port][1], odd[port])
        m = through_mesh([a, frames[port] * b], at, scale, gamma)
        a_re, a_im = a_re + reaches[port] * (m[0] - zn[0]), a_im + reaches[port] * (m[1] - zn[1])
    p = (e[0] + weight * den * zn[0] * x_n, e[1] + weight * den * zn[1] * x_n)
    q = ((a_re + weight * zn[0]) * x_n, (a_im + weight * zn[1]) * x_n)
    qq = q[0] * q[0] + q[1] * q[1]
    if qq == 0:
        return None
    return (p[0] * q[0] + p[1] * q[1], qq * den)


def nearest(record: Chart, x: Rational, beat: int = 0) -> str:
    """The name whose num / den lies nearest the rational x = (N, D): the smallest |N den - num D|, all integers; a credit with a rest beat is a body's and never the gap-0 plane's (pm1's reader item: light has no credit line), so the gap-0 name is left out where the beat is above 0."""
    n, d = x
    named = [
        (num, name) for num, (name, leg) in record.NAMES.items() if not (beat > 0 and num == record.rim)
    ]
    return min(named, key=lambda kv: abs(cross(n, d, kv[0], record.rim)))[1]


def middle(xs: list[Rational]) -> Rational:
    """The middle of sorted rationals, the mean of the two middle ones at an even count."""
    k = len(xs)
    if k % HALF:
        return xs[k // HALF]
    p, q = xs[k // HALF - 1], xs[k // HALF]
    return (p[0] * q[1] + q[0] * p[1], HALF * p[1] * q[1])


def reckoned_chimes(
    record: Chart,
) -> tuple[list[tuple[dict[str, Any], str, Rational]], int, int, list[int | None]]:
    """Every credit's species solved from its frame: the decoded (credit, name, x), the count read right, the count within the one-click floor, and each credit's floor on x in parts per million."""
    den, line_num = record.rim, record.gear_pinion
    decoded = []
    right = within = 0
    floors: list[int | None] = []
    solved = record.memo.setdefault("solve", {})
    for c in sorted(record.chimes, key=lambda c: int(c["i"])):
        if id(c) not in solved:
            solved[id(c)] = reckon(record, c)
        x = solved[id(c)]
        if x is None:
            continue
        name = nearest(record, x, int(c["beat"]))
        right += name == record.gear_name[c["line"]]
        decoded.append((c, name, x))
        n, d = x
        num = line_num[c["line"]]
        within += (n * den - num * d) ** PAIR <= PAIR * (record.teeth * den) ** PAIR * d
        floors.append(
            rule3.largest_below(
                (PAIR * record.teeth * record.teeth * den * den * MIL * MIL) // (d * num * num)
            )
            if num
            else None
        )
    return decoded, right, within, floors


if (
    __name__ == "__main__"
):  # the kit's documented command (the Boss's 6416894866: the decoder owed a main entry): the gates of a record file, one line each, as `python -m event_universe.gates`
    import sys

    from event_universe.gates import main

    main(sys.argv)
