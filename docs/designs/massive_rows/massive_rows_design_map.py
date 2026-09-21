"""massive-rows-v1, the design's numbers (read-only, the mathematician,
2026-09-21; docs/designs/massive_rows/DESIGN.md): the momentum label per
direction of the pin world's fan (the unit vector at the scale p, the rule of
`unit_label` with p in place of Q), the energy E' = isqrt(E'_0^2 + 3 p . p)
per direction, the flight's rate and wall, the pace's isotropy over the fan,
the turn per axis Link, the bounds against the register's ceiling, what the
click places, the lamp's budget, the pin's arrival ticks with the
lamp-to-opening flight counted, and the host cost against slits_huygens. The
directions are read from examples/events/amplitude/slits_huygens.json (the
pin world's plane); the integer root is the engine's own. No run.

Run from the repository root:

    PYTHONPATH=src python docs/designs/massive_rows/massive_rows_design_map.py > docs/designs/massive_rows/massive_rows_design_map.out
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from event_universe.core.integer import integer_root

ROOT = Path(__file__).resolve().parents[3]
WORLD = json.loads(
    (ROOT / "examples" / "events" / "amplitude" / "slits_huygens.json").read_text("utf-8")
)
Q, N = 64, 64
S, M = 1, 64  # the pin's width and the family's content per unit of amount
E0 = Q * S * M  # the rest energy in the identity's units, 4096
H = 1024  # the action
P = 220  # the declared momentum per row, label units
CEILING = 2**62 - 1
HEADINGS = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def scaled_unit(vector: tuple[int, int, int], scale: int) -> tuple[int, int, int]:
    """The integer vector nearest scale x D / |D| by `unit_label`'s rule with
    `scale` in place of Q: k(|a|) = (isqrt((2 scale |a|)^2 // n) + 1) // 2, the sign restored."""
    n = sum(c * c for c in vector)
    found = []
    for a in vector:
        t = 2 * scale * abs(a)
        k = (integer_root(t * t // n) + 1) // 2
        found.append(k if a >= 0 else -k)
    return found[0], found[1], found[2]


def energy(e0: int, p: tuple[int, int, int]) -> int:
    return integer_root(e0 * e0 + 3 * sum(c * c for c in p))


fan = [tuple(v) for v in WORLD["directions"]]
lamp = [m for m in WORLD["measured"] if "lamp" in m][0]
lamp_dirs = [tuple(v) for v in lamp["lamp"]["directions"]]
table = HEADINGS + fan
print(
    "1. THE MOMENTUM LABEL AND THE ENERGY PER DIRECTION OF THE PIN WORLD'S TABLE (load-time integers, the class of T_D's)"
)
print(
    f"   the table: the six headings and the {len(fan)} declared directions of slits_huygens (the openings' Farey fan by angle); the lamp's own {len(lamp_dirs)}: {lamp_dirs}"
)
print(f"   E'_0 = Q S M = {E0} (S = {S}, M = {M}); p = {P}; h = {H}; N = {N}")
rows = []
for d in table:
    p = scaled_unit(d, P)
    mag = math.sqrt(sum(c * c for c in p))
    e = energy(E0, p)
    l1 = sum(abs(c) for c in p)
    rows.append((d, p, mag, e, l1))
mags = [r[2] for r in rows]
es = [r[3] for r in rows]
paces = [r[2] / r[3] for r in rows]
print(
    f"   |p_D| over the table: {min(mags):.2f} to {max(mags):.2f} (the rounding within sqrt 3 / 2 = 0.87 of {P}: {100 * (max(mags) - P) / P:.2f} percent at most)"
)
print(
    f"   E'_D = isqrt(E'_0^2 + 3 p_D . p_D): {min(es)} to {max(es)} (W = {E0 * E0 + 3 * P * P} at |p| = {P} exactly: E' = {integer_root(E0 * E0 + 3 * P * P)}); gamma = E' / E'_0 = {integer_root(E0 * E0 + 3 * P * P) / E0:.5f}"
)
print(
    f"   the Euclidean pace |p_D|_2 / E'_D: {min(paces):.5f} to {max(paces):.5f}, the mean {sum(paces) / len(paces):.5f} (the isotropy the rounding's: {100 * (max(paces) - min(paces)) / (sum(paces) / len(paces)):.2f} percent spread); the photon's 1 / sqrt 3 = {1 / math.sqrt(3):.4f}, this pace {sum(paces) / len(paces) * math.sqrt(3):.4f} c"
)
print("   examples (D: p_D, |p_D|, E', the rate |p_D|_1, the wall E', the Manhattan pace |p|_1 / E'):")
for d, p, mag, e, l1 in rows[:3] + [r for r in rows if r[0] in lamp_dirs][:5] + rows[-2:]:
    print(f"      {d}: {p}, {mag:.2f}, {e}, {l1}, {e}, {l1 / e:.5f}")
print()

print("2. THE TURN PER AXIS LINK AND THE FLIGHT'S ACCUMULATOR (the row's two rates)")
print(
    f"   the turn: at a Link crossed on the axis a the phase turns by_drive(acc_turn, |p_a| N, h) steps: on a heading |p| N / h = {P * N} / {H} = {P * N / H:.2f} steps per Link; de Broglie's wavelength h / p = {H / P:.4f} Links (the photon world's 4.654)"
)
print(
    "   the flight: the accumulator's rate 2 |p_D|_1 against the wall 2 E'_D, started at E'_D (today's convention, rate 2 S_1 Q against 2 T_D at the half): the photon case E'_0 = 0 with p = Q D gives the rate 2 S_1 Q and the wall 2 isqrt(3 Q^2 |D|^2) = 2 T_D to the integer, one primitive for every row"
)
print(
    f"   the bounds: E'^2 = {integer_root(E0 * E0 + 3 * P * P) ** 2} < 2^62; the turn's numerator |p_a| N <= {P * N} and the accumulator below h + |p_a| N; the phase-count vectors of the click as today"
)
print()

print("3. WHAT THE CLICK PLACES, AND THE BOOKS")
w = [m for m in WORLD["measured"] if m.get("table")][0]["table"]["light"]["weights"]
print(
    f"   the openings re-release an arriving row of amount w as {len(w)} rows of amounts w a_i (the weights {min(w)} to {max(w)}, the sum {sum(w)}) with the multiplicity m x A, A = sum a_i^2 = {sum(x * x for x in w)}: the copies of one quantum over the fan, as the photon's"
)
print(
    f"   at the click the chosen row's direction D gives the momentum p_D and the content placed is ONE quantum, M = {M} (the family's quantum per unit of the birth's amount 1), whatever the amplitude weight w a_i of the chosen row; the rest of the record's units are cancelled as the photon's are (the books: initial + released = current + escaped + absorbed + cancelled)"
)
print(
    "   the recoil at a re-release: the wall takes p_D' - p_D per re-emitted row on its own momentum (fixed: no step), as it takes the photon's; the lamp takes -p_D per row born"
)
births, per_birth = 4096, len(lamp_dirs)
print(
    f"   the lamp's budget: {births} births x {per_birth} rows x {M} = {births * per_birth * M} units of content at the births; the lamp's amount {lamp['amount']} (content {lamp['amount'] * M}) holds it {lamp['amount'] * M / (births * per_birth * M):.0f} times over"
)
print()

print(
    "4. THE PIN'S ARRIVALS WITH THE LAMP-TO-OPENING FLIGHT COUNTED (section 23.3 counts from the opening)"
)
pace = P / integer_root(E0 * E0 + 3 * P * P)
lamp_x, opening_x, screen_x = lamp["position"][0], 8, 52
to_opening = (opening_x - lamp_x) / pace
for name, y_pixel in (("the centre pixel 60", 60.0), ("the first-fringe pixel 36.7", 36.7)):
    paths = [math.hypot(screen_x - opening_x, y_pixel - y0) for y0 in (55, 65)]
    arrivals = [path / pace for path in paths]
    print(
        f"   {name}: the paths from the openings {paths[0]:.2f} and {paths[1]:.2f} Links, {arrivals[0]:.0f} and {arrivals[1]:.0f} intervals at the pace {pace:.5f} (section 23.3's numbers); the lamp at x = {lamp_x} to the opening at x = {opening_x}: {opening_x - lamp_x} Links more, {to_opening:.0f} intervals (the photon's {(opening_x - lamp_x) / (64 / 110):.0f}), so the first click at the tick about {1 + to_opening + min(arrivals):.0f} to {1 + to_opening + max(arrivals):.0f}"
    )
print(
    f"   the last birth at 4096 arrives by about 4096 + {to_opening:.0f} + 978 = {4096 + to_opening + 978:.0f}: the run needs about 5250 intervals (section 23.3's 5100 counted from the opening)"
)
print()

print("5. THE HOST COST AGAINST slits_huygens (host numbers)")
photon_life, matter_life = (
    44.28 / (64 / 110) + (opening_x - lamp_x) / (64 / 110),
    44.28 / pace + to_opening,
)
ratio = matter_life / photon_life
print(
    f"   a row lives from its birth to its click about {photon_life:.0f} intervals for the photon and {matter_life:.0f} for the massive row ({ratio:.1f} times), so with a birth per interval the rows in flight at once are {ratio:.1f} times slits_huygens' and the work per interval with them"
)
print(
    f"   slits_huygens ran 4300 intervals in 1334 s (0.31 s per interval); slits_matter at 4096 births and about 5250 intervals: about {1334 / 4300 * ratio * 5250 / 3600:.1f} hours; at 1024 births (the wheel [633, 1024], the golden rate at W = 1024) and about 2200 intervals: about {1334 / 4300 * ratio * 2200 / 3600:.1f} hours; the records in proportion"
)
