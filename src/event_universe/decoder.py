"""The decoder's reads of the record, integers only (the owner's word: no float anywhere, every reading a quotient with its remainder or a count over a span): the record as read from the run's log alone (credits, births, refusals; the rows of the board's course; the Node lines), cut to an interval for a gate read as it first shows (`Record.to`), its own names for the planes (never the Node's), the species solved from a credit's frame and the nearest name; the verdicts' kinds and their one reader (kind_of, shown); the gates themselves are the table of gates.py, the rows read from the clicks clicks.py, the board's board.py and the widened rows predicates.py."""

from __future__ import annotations

from bisect import bisect_right
from collections import Counter
from typing import Any

from event_universe.circle import circle_of
from event_universe.core import paces, rule3
from event_universe.core.paces import sine_den
from event_universe.links import cross, turn_pair
from event_universe.rows import PLANE, QUARTET

MIL = 1000000  # readings in parts per million
HUNDRED = 100  # readings in hundredths
THOUSAND = 1000  # readings in thousandths
FEW = 10  # the fewest decoded credits for the dilation's two halves
SPANS = 20  # the fewest spans for the lengthening's two halves
HALF = 2  # a half: a count div 2, and a majority as a count times 2 above the whole
PAIR = 2  # two of a kind: the two ends of a Link, the two parts of a plane's pair, two bodies, two beats, two marks
THIRDS = 3  # the thirds of a run (its last third), of the half charge (T div 2 div 3)
QUARTERS = 4  # the quarters of a run (a body standing into the last quarter)
LIFTS = 3  # the three lifts of den's circle, the families forming when all three are born
LISTED = 8  # the most entries a row prints of a course (its first eight) and the eighths a course is sampled at
SHORT_LIST = 6  # the most falls and steps a row prints
FOUR_LISTED = 4  # the most returns the rows' reading prints
MAX = 2  # the index of the max in a row's min / mean / max
LEVELS_BACK = (
    2,
    1,
    0,
)  # the carrier's three levels read from the Node lines: before the interval, at its start, after it, as lines behind the interval's own
LINK_WALL_GAMMAS = 4  # the Link's wall in Gammas, links.py's wl = 4 gamma, mirrored here for the solve
KICK_WEIGHT = (
    12  # the law's weight of the kick, 12 p_0^2 G^2 (interval.py's form), mirrored here for the solve
)
REACH = 2  # the reach's weight, R_j = 2 p_i^2 Q_j G^2 (the law's form), mirrored here for the solve
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


class Record:
    """The record as the decoder reads it: the two files' integers, the planes with a gap by their legs under the decoder's names, the log's credits and births, the rows of the board's course."""

    def __init__(self, run: dict[str, Any]) -> None:
        self.run = run
        self.den = int(run["den"])
        self.gamma, self.G, self.T = int(run["gamma"]), int(run["G"]), int(run["T"])
        rows = run["universe"]["rows"]
        planes = {
            tuple(int(x) for x in r["pair"])
            for r in rows
            if int(r["shape"]) in (PLANE, QUARTET) and r.get("pair")
        }
        gapped = sorted((sine_den(num, self.den), num) for num, den in planes if num != den)
        self.NL = len(gapped)
        self.NAMES: dict[int, tuple[str, int]] = {
            num: (f"gapped {k}", leg) for k, (leg, num) in enumerate(gapped)
        }
        self.NAMES[self.den] = ("gap 0", 0)
        self.line_num = [int(num) for num in run["planes"]]
        records = sorted(
            (r for r in rows if r.get("pair") and int(r["shape"]) in (PLANE, QUARTET)),
            key=lambda r: int(r["pair"][0]) == int(r["pair"][1]),
        )
        shapes = [int(r["shape"]) for r in records]
        assert [int(r["pair"][0]) for r in records] == self.line_num
        self.line_name = [
            self.NAMES[num][0] if shape == PLANE else f"shape-{shape} at {self.NAMES[num][0]}"
            for num, shape in zip(self.line_num, shapes, strict=True)
        ]
        self.log = run["log"]
        self.credits = [entry for entry in self.log if entry["event"] == "credit"]
        self.births = [entry for entry in self.log if entry["event"] == "birth"]
        self.takes = [entry for entry in self.log if entry["event"] in ("birth", "credit")]
        self.cube = int(run["cube"])
        self.rows = run["rows"]
        self.nodes = run.get("nodes", [])
        self.intervals = int(run["intervals"])
        self.w = rule3.wall_of(self.den, self.gamma, self.G)
        self.memo: dict[str, Any] = {}

    def to(self, i: int) -> Record:
        """The record cut to the intervals 1 to i (its log, its rows and its Node lines, each in the run's order, cut by a search on the interval), for a gate read as it first shows; the solves and the run back stay the whole record's."""
        cuts: dict[int, Record] = self.memo.setdefault("cuts", {})
        if i in cuts:
            return cuts[i]
        found = Record.__new__(Record)
        found.__dict__.update(self.__dict__)
        found.intervals = i
        for name in ("log", "credits", "births", "takes"):
            whole = getattr(self, name)
            setattr(found, name, whole[: bisect_right(whole, i, key=lambda e: int(e["i"]))])
        found.rows = self.rows[: bisect_right(self.rows, i, key=lambda r: int(r["i"]))]
        found.nodes = self.nodes[: bisect_right(self.nodes, i, key=lambda n: int(n["i"]))]
        cuts[i] = found
        return found

    def index(self, node: list[int] | tuple[int, ...]) -> int:
        """A Node's index in the Node lines from its (x, y, z)."""
        x, y, z = (int(n) for n in node)
        return x * self.cube * self.cube + y * self.cube + z

    def node(self, index: int) -> list[int]:
        """A Node's (x, y, z) from its index in the Node lines."""
        x = int(rule3.quotient(index, self.cube * self.cube))
        y = int(rule3.quotient(index - x * self.cube * self.cube, self.cube))
        return [x, y, index - (x * self.cube + y) * self.cube]

    def distance(self, a: tuple[int, ...], b: tuple[int, ...]) -> int:
        """The Link distance between two Nodes on the torus, the shorter way on every axis."""
        return sum(min(abs(x - y), self.cube - abs(x - y)) for x, y in zip(a, b, strict=True))

    def bodies_of(self) -> dict[tuple[tuple[int, ...], int], list[dict[str, Any]]]:
        """The credits grouped by (Node, line), a body's track, in the log's order; read once per cut."""
        key = f"bodies to {self.intervals}"
        if key not in self.memo:
            found: dict[tuple[tuple[int, ...], int], list[dict[str, Any]]] = {}
            for c in self.credits:
                found.setdefault((tuple(c["node"]), c["line"]), []).append(c)
            self.memo[key] = found
        bodies: dict[tuple[tuple[int, ...], int], list[dict[str, Any]]] = self.memo[key]
        return bodies

    def signs_of(self) -> list[int]:
        """The births' children's senses as signs of their Wronskians, in the births' order."""
        return [(w > 0) - (w < 0) for b in self.births for w in b["W_children"]]

    def takes_of(self) -> tuple[int, int]:
        """The sums over the births of what the takes took and what they booked."""
        return sum(b["taken"] for b in self.births), sum(b["booked"] for b in self.births)

    def born_of(self) -> Counter[str]:
        """The births by the species born (the plane's name)."""
        return Counter(self.line_name[b["line_pair"]] for b in self.births)

    def laid_at_nothing(self) -> list[int]:
        """The magnitude |W| of every child laid where its plane stood at nothing, in the births' order."""
        return [
            abs(w)
            for b in self.births
            for w, stood in zip(b["W_children"], b.get("stood", [[0], [0]]), strict=True)
            if not any(stood)
        ]

    def circle(self) -> list[tuple[int, int]]:
        """den's circle, read once per record (circle.circle_of)."""
        found: list[tuple[int, int]] = self.memo.setdefault("circle", circle_of(self.den))
        return found


def quot(a: int, b: int, scale: int = 1) -> int | None:
    """The integer reading of a / b: the quotient of the scaled numerator (the remainder dropped)."""
    return None if b == 0 else int(rule3.division_forward(a * scale, b, 0)[0])


def cmp_rat(p: Rational, q: Rational) -> int:
    """Order two rationals (n, d) with d > 0 by cross multiplication."""
    s = int(cross(p[0], p[1], q[0], q[1]))
    return (s > 0) - (s < 0)


def carrier_levels(record: Record, credit: dict[str, Any]) -> tuple[int, int, int]:
    """The carrier's three levels at the credit's Node from the record's Node lines: before the interval, at its start and after it (Gamma before the first interval)."""
    index, i = record.index(credit["node"]), int(credit["i"])
    lines = record.run["nodes"]
    found = [
        lines[i - 1 - back]["X"][index] if i - 1 - back >= 0 else record.gamma for back in LEVELS_BACK
    ]
    before, start, after = found
    return int(before), int(start), int(after)


def solve(record: Record, credit: dict[str, Any]) -> Rational | None:
    """The species from the frame in exact integers under the symmetric ride (interval.py's form), a plane's frame alone (a quartet's credit carries its bilinears, its species owed by name): a riding line's momentum P_in = W_in (a_now - a_before) + r - W_in div 2 at the mean wall W_in = (w div 2)(X_before + X_now), the kick P_out = P_in + X_now F with F = SUM_j R_j (m_j - z) - D z, the one division a_next = a_now + (P_out + W_out div 2) div W_out at W_out = (w div 2)(X_now + X_next); from the record's levels v = a_next - a_now gives X_now F to the remainders' width, E = v W_out - W_in (a_now - a_before), and F is linear in num: num = (E + 12 den p_0^2 G^2 z X_now) / ((A + 12 p_0^2 G^2 z) X_now) with A = SUM_j 2 p_i^2 Q_j G^2 (m_j - z) over the turned arrivals; x = num / den as the rational (N, D), D > 0."""
    f, content = credit["frame"], credit["content"]
    if "re_now" not in f:
        return None
    gamma, den, unit = record.gamma, record.den, record.G
    p0, pi = paces.clock(gamma, content), paces.link_pace(gamma, content)
    w = rule3.wall_of(den, gamma, unit)
    x_b, x_n, x_x = carrier_levels(record, credit)
    w_in, w_out = (w // HALF) * (x_b + x_n), (w // HALF) * (x_n + x_x)
    zb = (f["re_start_before"], f["im_start_before"])
    zn = (f["re_start_now"], f["im_start_now"])
    zx = (f["re_stepped"], f["im_stepped"])
    if zn == (0, 0):
        return None
    scale, phases, odd, frames = f["X"], f["phases"], f["odd"], f["frames"]
    wl = LINK_WALL_GAMMAS * gamma
    e = tuple((zx[k] - zn[k]) * w_out - w_in * (zn[k] - zb[k]) for k in range(PAIR))
    weight = KICK_WEIGHT * p0 * p0 * unit * unit
    a_re = a_im = 0
    for port, (a, b) in enumerate(zip(f["re_neighbours_start"], f["im_neighbours_start"], strict=True)):
        m: Rational = (a, frames[port] * b)
        m = turn_pair(m[0], m[1], phases[port][0], phases[port][1], scale)
        n = odd[port]
        m = turn_pair(m[0], m[1], wl * wl - n * n, PAIR * wl * n, wl * wl + n * n)
        reach = REACH * pi * pi * f["factors"][port]
        a_re, a_im = a_re + reach * (m[0] - zn[0]), a_im + reach * (m[1] - zn[1])
    p = (e[0] + weight * den * zn[0] * x_n, e[1] + weight * den * zn[1] * x_n)
    q = ((a_re + weight * zn[0]) * x_n, (a_im + weight * zn[1]) * x_n)
    qq = q[0] * q[0] + q[1] * q[1]
    if qq == 0:
        return None
    return (p[0] * q[0] + p[1] * q[1], qq * den)


def nearest(record: Record, x: Rational, beat: int = 0) -> str:
    """The name whose num / den lies nearest the rational x = (N, D): the smallest |N den - num D|, all integers; a credit with a rest beat is a body's and never the gap-0 plane's (pm1's reader item: light has no credit line), so the gap-0 name is left out where the beat is above 0."""
    n, d = x
    named = [
        (num, name) for num, (name, leg) in record.NAMES.items() if not (beat > 0 and num == record.den)
    ]
    return min(named, key=lambda kv: abs(cross(n, d, kv[0], record.den)))[1]


def middle(xs: list[Rational]) -> Rational:
    """The middle of sorted rationals, the mean of the two middle ones at an even count."""
    k = len(xs)
    if k % HALF:
        return xs[k // HALF]
    p, q = xs[k // HALF - 1], xs[k // HALF]
    return (p[0] * q[1] + q[0] * p[1], HALF * p[1] * q[1])


def decoded_credits(
    record: Record,
) -> tuple[list[tuple[dict[str, Any], str, Rational]], int, int, list[int | None]]:
    """Every credit's species solved from its frame: the decoded (credit, name, x), the count read right, the count within the one-click floor, and each credit's floor on x in parts per million."""
    den, line_num = record.den, record.line_num
    decoded = []
    right = within = 0
    floors: list[int | None] = []
    solved = record.memo.setdefault("solve", {})
    for c in sorted(record.credits, key=lambda c: int(c["i"])):
        if id(c) not in solved:
            solved[id(c)] = solve(record, c)
        x = solved[id(c)]
        if x is None:
            continue
        name = nearest(record, x, int(c["beat"]))
        right += name == record.line_name[c["line"]]
        decoded.append((c, name, x))
        n, d = x
        num = line_num[c["line"]]
        within += (n * den - num * d) ** PAIR <= PAIR * (record.w * den) ** PAIR * d
        floors.append(
            rule3.largest_below((PAIR * record.w * record.w * den * den * MIL * MIL) // (d * num * num))
            if num
            else None
        )
    return decoded, right, within, floors
