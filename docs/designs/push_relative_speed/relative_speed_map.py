"""The integer map of change 2, "the push reads the crowd the body is in, at
the relative speed" (the G2 physicist's RULES.md section 2 on
`claude/series-g2-stars` at 5322dc4), read by the mathematician on
2026-09-20 before any engine run. Standalone: `by_clock` restated, the
flight table's pace taken from the engine's own `flight_table` (the one
import), exact integers and fractions (a report of the host, never a
physical fallback). Output beside this file: `relative_speed_map.out`.

Sections:
  A. the dwell of a beam's row at a Node on a heading, d(x) in {1, 2}: the
     presence at a fixed Node is d(x) per interval, and the period-sum
     identity of RULES.md holds over the 32 Nodes of a spatial period, not
     over the 55 intervals at one Node;
  B. the bar of the finding over 200 intervals: the law's arrivals, the
     proposal's presence at the relative speed, the smallest alternative
     (the arrivals at the relative speed) and the crossing count as the
     host's control, at rest on a dwell-1 and a dwell-2 Node, receding at
     0.30 and 0.45, approaching at 0.30, co-moving at c, outrunning;
  C. the gate set's deuteron (`weak/j3_deuteron.json`, the 284 fan): the
     first read of a body at one Link under the proposal against today's,
     per unit of amount and column value, exact.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

from event_universe.events.nature_beam import flight_table, unit_label

Q = 64
T_HEADING = math.isqrt(3 * Q * Q)  # 110
ROOT = Path(__file__).resolve().parents[3]


def by_clock(age: int, numerator: int, denominator: int) -> int:
    return ((age + 1) * numerator) // denominator - (age * numerator) // denominator


def m_heading(tau: int) -> int:
    """Links made by age tau on a heading: (2 tau Q + T) // (2 T)."""
    return (2 * tau * Q + T_HEADING) // (2 * T_HEADING)


def dwell(x: int) -> int:
    """The number of ages at which a row on a heading is at the x-th Node."""
    return sum(1 for tau in range(0, 4 * x + 8) if m_heading(tau) == x)


def section(title: str) -> None:
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


# --------------------------------------------------------------------------
section("A. The dwell on a heading: presence at a fixed Node is d(x) in {1, 2}")
dwells = [dwell(x) for x in range(1, 65)]
print("d(x) for x = 1 .. 64:", "".join(str(d) for d in dwells))
period = dwells[:32]
print(
    f"one spatial period of 32 Nodes: {period.count(2)} Nodes of dwell 2, {period.count(1)} of dwell 1,"
    f" the sum {sum(period)} = 55 intervals of the flight period"
)
print(
    "the identity claimed: 55 arrivals at a Node become 55 x 55 / 32 =",
    Fraction(55 * 55, 32),
    "row-intervals of presence;",
)
print(
    "   at ONE Node over 55 intervals the presence is 55 x d(x) =",
    "55 or 110",
    "row-intervals, never",
    float(Fraction(55 * 55, 32)),
)
print(
    "   over the 32 Nodes of a spatial period (one interval): presence",
    sum(period),
    "rows; x c = 32 / 55 ->",
    Fraction(sum(period) * 32, 55),
    "= the 32 arrivals: exact, remainder 0",
)
print(
    "   at one Node: presence x c per interval = d(x) x 32 / 55 =",
    Fraction(32, 55),
    "or",
    Fraction(64, 55),
    "of the beam's rate: -41.8 % or +16.4 %, a factor, not a remainder",
)

# --------------------------------------------------------------------------
section("B. The bar of the finding, 200 intervals, on a heading (the standalone map)")


def bar(x0: int, p: int, D: int, ticks: int = 200, warm: int = 400) -> dict[str, int]:
    """A fixed source at x = 0 releasing one row per interval on +x (born at
    every interval from 1, a row born at t is at Node m_heading(t' - t) at
    interval t'); a free body of momentum p (signed, label units along +x)
    and step divisor D = Q S M + |p| starting at x0 at interval `warm`
    (the beam's front long past), stepping by the step rule
    by_clock(age - 1, |p|, D) with its age counted from 1 at `warm`, after
    the rows' walk and the readings of the interval (the engine's order).
    Returns the counts over `ticks` intervals: the law's arrivals, the
    proposal's presence-at-relative-speed reading (by_clock per interval
    on the pair (|32 D - 55 p|, 55 D)), the alternative's
    arrivals-at-relative-speed reading (the pair (|32 D - 55 p|, 32 D)),
    and the host's crossing count (rows whose order against the body
    changes: a control with memory, not a rule)."""
    num = abs(32 * D - 55 * p)
    x_body = x0
    age = 0
    arrivals_total = presence_total = proposal = alternative = crossings = 0
    # A row born at t sits at m_heading(t' - t); we track its position each interval.
    births = list(range(1, warm + ticks + 1))
    previous_side: dict[int, int] = {}
    for t in range(1, warm + ticks + 1):
        positions = {b: m_heading(t - b) for b in births if b <= t}
        if t > warm:
            arrivals = sum(
                1 for b, x in positions.items() if x == x_body and (b == t or m_heading(t - 1 - b) != x)
            )
            presence = sum(1 for x in positions.values() if x == x_body)
            arrivals_total += arrivals
            presence_total += presence
            proposal += by_clock(age, presence * num, 55 * D)
            alternative += by_clock(age, arrivals * num, 32 * D)
        # The crossing control: the sign of (row - body) before and after this interval's walk.
        for b, x in positions.items():
            side = (x > x_body) - (x < x_body)
            if side and b in previous_side and previous_side[b] and side != previous_side[b]:
                crossings += 1 if t > warm else 0
            if side:
                previous_side[b] = side
        if t >= warm:
            # The body's step of the interval, after the readings (the frame's _move).
            age += 1
            if p and by_clock(age - 1, abs(p), D) == 1:
                x_body += 1 if p > 0 else -1
    return {
        "arrivals": arrivals_total,
        "presence": presence_total,
        "proposal": proposal,
        "alternative": alternative,
        "crossings": crossings,
        "x_end": x_body,
    }


x_d1 = next(x for x in range(30, 64) if dwell(x) == 1)
x_d2 = next(x for x in range(30, 64) if dwell(x) == 2)
cases = [
    (f"at rest on a dwell-1 Node (x = {x_d1})", x_d1, 0, 1, Fraction(0)),
    (f"at rest on a dwell-2 Node (x = {x_d2})", x_d2, 0, 1, Fraction(0)),
    ("receding at 0.30", 40, 30, 100, Fraction(30, 100)),
    ("receding at 0.45", 40, 45, 100, Fraction(45, 100)),
    ("approaching at 0.30", 120, -30, 100, Fraction(-30, 100)),
    ("co-moving at c = 32 / 55", 40, 32, 55, Fraction(32, 55)),
    ("outrunning at 0.75", 40, 75, 100, Fraction(75, 100)),
]
c = Fraction(32, 55)
print(
    f"{'case':38s} {'law':>5s} {'presence':>8s} {'proposal':>8s} {'alt':>5s} {'cross':>5s}  expected (c - v)/c x 200"
)
for name, x0, p, D, v in cases:
    r = bar(x0, p, D)
    expected = float(abs(c - v) / c * 200)
    print(
        f"{name:38s} {r['arrivals']:5d} {r['presence']:8d} {r['proposal']:8d} {r['alternative']:5d} {r['crossings']:5d}  {expected:6.1f}   (x from {x0} to {r['x_end']})"
    )
print("the law reads the arrivals, 1.000 per interval whatever the motion (the finding, reproduced);")
print(
    "the proposal at rest reads d(x) x 32 / 55 of the rate, 116 or 232 of 200, by the Node it sits on;"
)
print(
    "the alternative (the same pair on the arrivals, normalised to 1 at rest) reads 200 at rest at every Node"
)
print("   and the crossing rate when moving; the host's crossing count is the control.")

# --------------------------------------------------------------------------
section("C. The gate set's deuteron (weak/j3_deuteron.json): the first read at one Link")
world = json.loads((ROOT / "examples/events/weak/j3_deuteron.json").read_text(encoding="utf-8"))
vectors = tuple(tuple(v) for v in world["directions"])
headings = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
table = flight_table(((0, 0, 0), (0, 0, 0)) + headings + vectors)
today = Fraction(0)
proposal_sum = Fraction(0)
count = 0
for index in range(2, 2 + len(headings) + len(vectors)):
    vector = tuple(int(v) for v in table.vectors[index])
    if tuple(int(v) for v in table.steps[index][0]) != (1, 0, 0):
        continue  # the first step is not +x: the row does not reach the neighbour on +x
    count += 1
    s1, t_d = int(table.manhattan[index]), int(table.resolution[index])
    ages = [tau for tau in range(1, 4 * s1 + 8) if int(table.manhattan_steps(index, tau)) == 1]
    d1 = len(ages)  # the dwell at the first Node
    a = abs(vector[0])
    pace_x = Fraction(a * Q, t_d)  # Links along x per interval: a / S_1 of S_1 Q / T_d
    ux = int(unit_label(vector)[0])
    today += ux
    proposal_sum += d1 * pace_x * ux
print(
    f"directions whose first step is +x: {count}; today's push per unit and per column value U(1) = sum u_x = {today} (the register's 3008)"
)
print(
    f"the proposal's read per unit: sum dwell_d x c_{{d,x}} x u_x = {proposal_sum} = {float(proposal_sum):.3f}; the ratio {float(proposal_sum / today):.4f}"
)
print(
    f"the deuteron's registered push 310 967 280 640 would read about {int(310967280640 * proposal_sum / today):,} per interval (to the floor's grain)"
)
print(
    "(the fan's rows are at their first Node for 1 or 2 ages by their own periods; the pair per direction is (a Q, T_d))"
)
