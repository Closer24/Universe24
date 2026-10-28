"""The reckoner's reads of the chart, integers only (the owner's word: no float anywhere, every reading a quotient with its remainder or a count over a span): the chart as read from the run's log alone (chimes, fittings, jams; the rows of the great clock's course; the clock lines), cut to a tick for a gate read as it first shows (`Chart.to`), its own names for the hands (never the Clock's), the species reckoned from a chime's face and the nearest name; the verdicts' kinds and their one reader (kind_of, shown); the gates themselves are the table of gates.py, the rows read from the clicks clicks.py, the great clock's great_clock.py and the widened rows predicates.py."""

from __future__ import annotations

from bisect import bisect_right
from collections import Counter
from typing import Any

from event_universe.core import rates, rule3
from event_universe.core.rates import sine_rim
from event_universe.meshes import Mesh, cross, through_mesh
from event_universe.rim import rim_of
from event_universe.trains import HAND, rows_of

MIL = 1000000  # readings in parts per million
HUNDRED = 100  # readings in hundredths
THOUSAND = 1000  # readings in thousandths
FEW = 10  # the fewest reckoned chimes for the dilation's two halves
SPANS = 20  # the fewest spans for the lengthening's two halves
HALF = 2  # a half: a count div 2, and a majority as a count times 2 above the whole
PAIR = 2  # two of a kind: the two ends of a mesh, the two parts of a hand's ratio, two bobs, two beats, two marks
THIRDS = 3  # the thirds of a run (its last third), of the half sweep (T div 2 div 3)
QUARTERS = 4  # the quarters of a run (a bob wound into the last quarter)
LISTED = 8  # the most entries a row prints of a course (its first eight) and the eighths a course is sampled at
SHORT_LIST = 6  # the most falls and steps a row prints
FOUR_LISTED = 4  # the most returns the rows' reading prints
MAX = 2  # the index of the max in a row's min / mean / max
NOTCHES_BACK = (
    2,
    1,
    0,
)  # the regulator's three notches read from the clock lines: before the tick, at its start, after it, as lines behind the tick's own
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
    """The verdict of a row the chart cannot carry: NOT READ, why, and the predicate it would be read by; the one form of the words."""
    return f"{NOT} READ: {why}; the predicate: {predicate}"


def shown(verdict: str) -> bool:
    """A verdict that shows (whole or in part) in its own right: a row restating another gate's verdict shows no event line of its own, the gate it restates has the line."""
    return verdict.startswith("SHOWN")


class Chart:
    """The chart as the reckoner reads it: the two files' integers, the sprung hands by their legs under the reckoner's names, the log's chimes and fittings, the rows of the great clock's course."""

    def __init__(self, run: dict[str, Any]) -> None:
        self.run = run
        self.rim = int(run["den"])
        self.action = int(run["universe"]["integers"]["quantum_action"])
        self.full_rate, self.G, self.key = int(run["gamma"]), int(run["G"]), int(run["T"])
        trains = rows_of(run["universe"])
        ratios = {
            tuple(int(x) for x in r["pair"]) for r in trains if int(r["shape"]) == HAND and r.get("pair")
        }
        sprung = sorted((sine_rim(pinion, self.rim), pinion) for pinion, rim in ratios if pinion != rim)
        self.NL = len(sprung)
        self.NAMES: dict[int, tuple[str, int]] = {
            pinion: (f"gapped {k}", leg) for k, (leg, pinion) in enumerate(sprung)
        }
        self.NAMES[self.rim] = ("gap 0", 0)
        self.gear_pinion = [int(pinion) for pinion in run["planes"]]
        hands = sorted(
            (r for r in trains if r.get("pair") and int(r["shape"]) == HAND),
            key=lambda r: int(r["pair"][0]) == int(r["pair"][1]),
        )
        sizes = [int(r["shape"]) for r in hands]
        assert [int(r["pair"][0]) for r in hands] == self.gear_pinion
        self.gear_name = [
            self.NAMES[pinion][0] if size == HAND else f"shape-{size} at {self.NAMES[pinion][0]}"
            for pinion, size in zip(self.gear_pinion, sizes, strict=True)
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
        """The chart cut to the ticks 1 to i (its log, its rows and its clock lines, each in the run's order, cut by a search on the tick), for a gate read as it first shows; the reckonings and the rewind stay the whole chart's."""
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

    def index(self, clock: list[int] | tuple[int, ...]) -> int:
        """A clock's index in the clock lines from its (x, y, z)."""
        x, y, z = (int(n) for n in clock)
        return x * self.cube * self.cube + y * self.cube + z

    def clock(self, index: int) -> list[int]:
        """A clock's (x, y, z) from its index in the clock lines."""
        x = int(rule3.carries(index, self.cube * self.cube))
        y = int(rule3.carries(index - x * self.cube * self.cube, self.cube))
        return [x, y, index - (x * self.cube + y) * self.cube]

    def distance(self, a: tuple[int, ...], b: tuple[int, ...]) -> int:
        """The mesh distance between two clocks on the torus, the shorter way on every axis."""
        return sum(min(abs(x - y), self.cube - abs(x - y)) for x, y in zip(a, b, strict=True))

    def bobs_of(self) -> dict[tuple[tuple[int, ...], int], list[dict[str, Any]]]:
        """The chimes grouped by (clock, gear), a bob's track, in the log's order; read once per cut."""
        key = f"bodies to {self.ticks}"
        if key not in self.memo:
            found: dict[tuple[tuple[int, ...], int], list[dict[str, Any]]] = {}
            for c in self.chimes:
                found.setdefault((tuple(c["node"]), c["line"]), []).append(c)
            self.memo[key] = found
        bobs: dict[tuple[tuple[int, ...], int], list[dict[str, Any]]] = self.memo[key]
        return bobs

    def first_stopped(self) -> dict[int, int]:
        """The first stopped tick of every clock that stops (the mesh rate 0, BH-S1's mask on the clock lines), the clock's index to the tick; the one reader of the standstill's clocks for rows 14, 34 and 61."""
        first: dict[int, int] = {}
        for line in self.clocks:
            for at in line["frozen"]:
                first.setdefault(int(at), int(line["i"]))
        return first

    def stopped_masks(self) -> dict[int, set[int]]:
        """The frozen set every close reads, by the close's interval (BH-S1 with FR-S1): the Node line of the interval i carries the set at its end, which the close of i + 1 reads at its start, so a credit or a birth of the interval i stands against the line of i - 1 and never its own (the dial adds nothing at a Node in it, the one identity of every click line); the former read against the same interval's line, one interval late, kept by name; read once per cut."""
        key = f"masks to {self.ticks}"
        if key not in self.memo:
            self.memo[key] = {
                int(line["i"]) + 1: {int(at) for at in line["frozen"]} for line in self.clocks
            }
        masks: dict[int, set[int]] = self.memo[key]
        return masks

    @staticmethod
    def slack_of(fitting: dict[str, Any]) -> bool | None:
        """Whether every end of a fitting closes by its signed slack (EX-S1 under the wave: unwound + the slack before - the slack after = tallied, an unspringing's two ends in its `takes`), None where an end carries no slack."""
        ends = fitting.get("takes", [fitting])
        if any("remainder" not in end for end in ends):
            return None
        return all(e["taken"] + e["remainder_was"] - e["remainder"] == e["booked"] for e in ends)

    def sweeps_of(self) -> list[tuple[int, int]]:
        """The two fitted hands' own sweeps at every fitting, in the fittings' order (H-Children-Charge-Bug-1, the Boss's 6410696786): a fitted hand advanced by the fitted hand's advance carries its sense times half the key (the sweep of its own two notches), a fitted hand advanced as the exact unwind at -1 (an unspringing's unsprung hand, the gear's `exact_lay` at its end) carries 0; the log's W_children is the chart's sweep at the clock after the advance (the standing notch's and the cross term in it) and is read for the residue by name, never for the sign."""

        def own(b: dict[str, Any], k: int) -> int:
            exact = b.get("exact_lay", [None, None])[k] is not None
            return 0 if exact else int(b["senses"][k]) * (self.action // HALF)

        return [(own(b, 0), own(b, 1)) for b in self.fittings]

    def signs_of(self) -> list[int]:
        """The fittings' fitted hands' senses as the signs of their own sweeps, in the fittings' order (0 for a fitted hand advanced as unsprung)."""
        return [sign(w) for pair in self.sweeps_of() for w in pair]

    def unwinds_of(self) -> tuple[int, int]:
        """The sums over the fittings of what the unwinds unwound and what they tallied."""
        return sum(b["taken"] for b in self.fittings), sum(b["booked"] for b in self.fittings)

    def fitted_of(self) -> Counter[str]:
        """The fittings by the species fitted (the hand's name)."""
        return Counter(self.gear_name[b["line_pair"]] for b in self.fittings)

    def lifts_fitted(self) -> list[str]:
        """The lifts fitted: the distinct sprung hands with a fitting, the unsprung hand (light, no lift) left out; the lifts the calibre names are its sprung hands, the rim's typed points (self.NL), the former constant 3 the toy calibre's count of them (the Boss's task of 2026-10-27, 10:1x UTC: the number read from the chart and no file of src)."""
        unsprung = self.NAMES[self.rim][0]
        return sorted(name for name in self.fitted_of() if name != unsprung)

    def advanced_at_nothing(self) -> list[int]:
        """The magnitude |W| of every fitted hand advanced where its hand stood at nothing, in the fittings' order."""
        return [
            abs(w)
            for b in self.fittings
            for w, stood in zip(b["W_children"], b.get("stood", [[0], [0]]), strict=True)
            if not any(stood)
        ]

    def rim_points(self) -> list[tuple[int, int]]:
        """The rim's points, read once per chart (rim.rim_of)."""
        found: list[tuple[int, int]] = self.memo.setdefault("circle", rim_of(self.rim))
        return found


def carries(a: int, b: int, scale: int = 1) -> int | None:
    """The integer reading of a / b: the carries of the scaled numerator (the fine tooth dropped)."""
    return None if b == 0 else int(rule3.carries(a * scale, b))


def sign(x: int) -> int:
    """The sign of an integer: -1, 0 or 1."""
    return (x > 0) - (x < 0)


def cmp_rat(p: Rational, q: Rational) -> int:
    """Order two rationals (n, d) with d > 0 by cross multiplication."""
    return sign(int(cross(p[0], p[1], q[0], q[1])))


def regulator_notches(chart: Chart, chime: dict[str, Any]) -> tuple[int, int, int]:
    """The regulator's three notches at the chime's clock from the chart's clock lines: before the tick, at its start and after it (the full rate before the first tick)."""
    index, i = chart.index(chime["node"]), int(chime["i"])
    lines = chart.run["nodes"]
    found = [
        lines[i - 1 - back]["X"][index] if i - 1 - back >= 0 else chart.full_rate
        for back in NOTCHES_BACK
    ]
    before, start, after = found
    return int(before), int(start), int(after)


def reckon(chart: Chart, chime: dict[str, Any]) -> Rational | None:
    """The species from the face in exact integers under the driven gears' symmetric form (tick.py's), the hand's face: a driven gear's momentum P_in = W_in (a_now - a_before) + fine - W_in div 2 at the mean teeth W_in = (teeth div 2)(stretch_before + stretch_now), the impulse P_out = P_in + stretch_now F with F = SUM_j R_j (m_j - z) - D z, the one carry a_next = a_now + (P_out + W_out div 2) div W_out at W_out = (teeth div 2)(stretch_now + stretch_next); from the chart's notches v = a_next - a_now gives stretch_now F to the fine teeth's width, E = v W_out - W_in (a_now - a_before), and F is linear in pinion: pinion = (E + 12 rim rate^2 G^2 z stretch_now) / ((A + 12 rate^2 G^2 z) stretch_now) with A = SUM_j 2 mesh_rate^2 Q_j G^2 (m_j - z) over the turned pulls; x = pinion / rim as the rational (N, D), D > 0."""
    f, load = chime["frame"], chime["content"]
    if "re_now" not in f:
        return None
    full_rate, rim, unit = chart.full_rate, chart.rim, chart.G
    rate, mesh_rate = rates.rate(full_rate, load), rates.mesh_rate(full_rate, load)
    w = chart.teeth
    x_b, x_n, x_x = regulator_notches(chart, chime)
    w_in, w_out = rule3.mean_teeth_of(w, x_b, x_n), rule3.mean_teeth_of(w, x_n, x_x)
    zb = (f["re_start_before"], f["im_start_before"])
    zn = (f["re_start_now"], f["im_start_now"])
    zx = (
        f["re_now"],
        f["im_now"],
    )  # the state after the step is the notches now (CL-S2, the Boss's 6417815695 and David's e03b70401: the former `stepped` field was the state the turnover replaced, equal to the notches now at every chime of a clock that did not turn over, and is struck; the reader reads what the algebra fixes)
    if zn == (0, 0):
        return None
    scale, offsets, odd, pawls = f["X"], f["phases"], f["odd"], f["frames"]
    e = tuple((zx[k] - zn[k]) * w_out - w_in * (zn[k] - zb[k]) for k in range(PAIR))
    weight = rule3.spring(0, 1, rate, unit)
    grips = rule3.gearing(1, rim, full_rate, rate, mesh_rate, tuple(f["factors"]), unit).grips
    a_re = a_im = 0
    for spoke, (a, b) in enumerate(zip(f["re_neighbours_start"], f["im_neighbours_start"], strict=True)):
        at = Mesh(None, pawls[spoke], offsets[spoke][0], offsets[spoke][1], odd[spoke])
        m = through_mesh([a, pawls[spoke] * b], at, scale, full_rate)
        a_re, a_im = a_re + grips[spoke] * (m[0] - zn[0]), a_im + grips[spoke] * (m[1] - zn[1])
    p = (e[0] + weight * rim * zn[0] * x_n, e[1] + weight * rim * zn[1] * x_n)
    q = ((a_re + weight * zn[0]) * x_n, (a_im + weight * zn[1]) * x_n)
    qq = q[0] * q[0] + q[1] * q[1]
    if qq == 0:
        return None
    return (p[0] * q[0] + p[1] * q[1], qq * rim)


def nearest(chart: Chart, x: Rational, beat: int = 0) -> str:
    """The name whose pinion / rim lies nearest the rational x = (N, D): the smallest |N rim - pinion D|, all integers; a chime with a rest beat is a bob's and never the unsprung hand's (pm1's reader item: light has no chime line), so the unsprung hand's name is left out where the beat is above 0."""
    n, d = x
    named = [
        (num, name) for num, (name, leg) in chart.NAMES.items() if not (beat > 0 and num == chart.rim)
    ]
    return min(named, key=lambda kv: abs(cross(n, d, kv[0], chart.rim)))[1]


def middle(xs: list[Rational]) -> Rational:
    """The middle of sorted rationals, the mean of the two middle ones at an even count."""
    k = len(xs)
    if k % HALF:
        return xs[k // HALF]
    p, q = xs[k // HALF - 1], xs[k // HALF]
    return (p[0] * q[1] + q[0] * p[1], HALF * p[1] * q[1])


def reckoned_chimes(
    chart: Chart,
) -> tuple[list[tuple[dict[str, Any], str, Rational]], int, int, list[int | None]]:
    """Every chime's species reckoned from its face: the reckoned (chime, name, x), the count read right, the count within the one-click floor, and each chime's floor on x in parts per million."""
    rim, gear_pinion = chart.rim, chart.gear_pinion
    reckoned = []
    right = within = 0
    floors: list[int | None] = []
    reckonings = chart.memo.setdefault("solve", {})
    for c in sorted(chart.chimes, key=lambda c: int(c["i"])):
        if id(c) not in reckonings:
            reckonings[id(c)] = reckon(chart, c)
        x = reckonings[id(c)]
        if x is None:
            continue
        name = nearest(chart, x, int(c["beat"]))
        right += name == chart.gear_name[c["line"]]
        reckoned.append((c, name, x))
        n, d = x
        pinion = gear_pinion[c["line"]]
        within += (n * rim - pinion * d) ** PAIR <= PAIR * (chart.teeth * rim) ** PAIR * d
        floors.append(
            rule3.largest_below(
                (PAIR * chart.teeth * chart.teeth * rim * rim * MIL * MIL) // (d * pinion * pinion)
            )
            if pinion
            else None
        )
    return reckoned, right, within, floors


if (
    __name__ == "__main__"
):  # the kit's documented command (the Boss's 6416894866: the reckoner owed a main entry): the gates of a chart file, one line each, as `python -m event_universe.gates`
    import sys

    from event_universe.gates import main

    main(sys.argv)
