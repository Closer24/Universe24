"""massive-rows-v1, round 2 of the design: the numbers the physics-rule review
asked for (read-only, the mathematician, 2026-09-21; the review's M4, M5, S2,
S4; docs/designs/massive_rows/DESIGN.md). (A) The primitive's identity on the
pin world's table: the massive rule at E'_0 = 0 with p = Q D against Flight's
(2 S_1 Q, 2 T_D), and with the photon's label u_D in its place. (B) The
arrivals by the accumulator rule on the engine's own Bresenham lines
(`direction_flight`, the one import): the lamp leg to the openings, the
re-release's first rows per screen pixel, the first `click` line at the centre
and the first-fringe pixels, the longest row of a record, the completion of the
last birth. (C) Pearson with the two-source cosine on the declared Farey fan at
de Broglie's wavelength h / p, by the same walk for the photon at its own
rate (the registered 0.895 the check of the method). (D) The bounds. (E) The
host cost with the corrected run. Every number a GAMEBOARD reading of the
design or the detector's expected reading, labelled; no run.

Run from the repository root:

    PYTHONPATH=src python docs/designs/massive_rows/massive_rows_round2_map.py > docs/designs/massive_rows/massive_rows_round2_map.out
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from event_universe.core.integer import integer_root
from event_universe.events.nature_beam import direction_flight

ROOT = Path(__file__).resolve().parents[3]
WORLD = json.loads(
    (ROOT / "examples" / "events" / "amplitude" / "slits_huygens.json").read_text("utf-8")
)
Q, N = 64, 64
S, M, H, P = 1, 64, 1024, 220
E0 = Q * S * M
HEADINGS = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
SHAPE = WORLD["shape"]
SCREEN_X = 52
LAMP = [m for m in WORLD["measured"] if "lamp" in m][0]
OPENINGS = [m for m in WORLD["measured"] if m.get("table")]
WALLS = {
    tuple(m["position"][:2]) for m in WORLD["measured"] if m["family"] == "wall" and not m.get("table")
}
OPENING_NODES = {tuple(m["position"][:2]) for m in OPENINGS}
PHOTON_RATE = tuple(WORLD["families"][0]["phase_per_link"])  # the pair n / d, steps per interval of age


def scaled_unit(vector, scale):
    n = sum(c * c for c in vector)
    out = []
    for a in vector:
        t = 2 * scale * abs(a)
        k = (integer_root(t * t // n) + 1) // 2
        out.append(k if a >= 0 else -k)
    return tuple(out)


table = HEADINGS + [tuple(v) for v in WORLD["directions"]]
flight = direction_flight(tuple(table))
index_of = {d: i for i, d in enumerate(table)}
p_of = {d: scaled_unit(d, P) for d in table}
e_of = {d: integer_root(E0 * E0 + 3 * sum(c * c for c in p_of[d])) for d in table}

print("A. THE PRIMITIVE'S IDENTITY ON THE PIN WORLD'S TABLE (the review's F1, M4)")
same_qd = sum(
    1
    for d in table
    if (2 * sum(abs(Q * c) for c in d), 2 * integer_root(3 * sum((Q * c) ** 2 for c in d)))
    == (2 * int(flight.manhattan[index_of[d]]) * Q, 2 * int(flight.resolution[index_of[d]]))
)
same_ud = sum(
    1
    for d in table
    if (
        2 * sum(abs(int(c)) for c in flight.labels[index_of[d]]),
        2 * integer_root(3 * sum(int(c) ** 2 for c in flight.labels[index_of[d]])),
    )
    == (2 * int(flight.manhattan[index_of[d]]) * Q, 2 * int(flight.resolution[index_of[d]]))
)
print(
    f"   the massive rule at E'_0 = 0 with p = Q D (the flight vector): the rate 2 |Q D|_1 = 2 S_1 Q and the wall 2 isqrt(3 |Q D|^2) = 2 T_D on {same_qd} of {len(table)} directions"
)
print(
    f"   with the photon's LABEL u_D (unit_label, |u_D| = Q within the rounding) in place of Q D: the same pair on {same_ud} of {len(table)} (the six headings alone): the photon uses two vectors, the flight vector Q D and the label u_D; the massive row one, p_D"
)
print()


def walk(start, d, stop):
    """The Bresenham line of d from `start` (x, y) on the engine's own line
    (`flight.lines`), one unit step per Manhattan Link, until `stop` names an
    end: returns (the end, the Node, the Manhattan Links made, the Links per axis)."""
    i = index_of[d]
    s1 = int(flight.manhattan[i])
    line = flight.lines[i, :s1]
    x, y = start
    per_axis = [0, 0, 0]
    made = 0
    while True:
        step = line[made % s1]
        x += int(step[0])
        y += int(step[1])
        per_axis[0] += abs(int(step[0]))
        per_axis[1] += abs(int(step[1]))
        made += 1
        end = stop((x, y))
        if end:
            return end, (x, y), made, per_axis


def stop_lamp(node):
    if node in WALLS:
        return "wall"
    if node in OPENING_NODES:
        return "opening"
    if node[0] < 0 or node[0] >= SHAPE[0] or node[1] < 0 or node[1] >= SHAPE[1]:
        return "face"
    return ""


def stop_fan(node):
    if node[0] == SCREEN_X:
        return "screen"
    if node[0] < 0 or node[0] >= SHAPE[0] or node[1] < 0 or node[1] >= SHAPE[1]:
        return "face"
    if node in WALLS and node[0] != SCREEN_X:
        return "wall"
    return ""


def age_of(made, d, massive):
    """The first age tau at which the accumulator's count reaches `made`
    Links: massive, (2 tau |p_D|_1 + E'_D) // (2 E'_D) >= made; the photon,
    (2 tau S_1 Q + T_D) // (2 T_D) >= made (Flight.accumulator)."""
    i = index_of[d]
    if massive:
        rate, wall = 2 * sum(abs(c) for c in p_of[d]), 2 * e_of[d]
        start = e_of[d]
    else:
        rate, wall = 2 * int(flight.manhattan[i]) * Q, 2 * int(flight.resolution[i])
        start = int(flight.resolution[i])
    return max(0, -(-(made * wall - start) // rate))


print(
    "B. THE ARRIVALS BY THE ACCUMULATOR RULE ON THE ENGINE'S OWN BRESENHAM LINES (the review's F7, M5 a-c)"
)
lamp_xy = tuple(LAMP["position"][:2])
legs = {}
for d in [tuple(v) for v in LAMP["lamp"]["directions"]]:
    end, node, made, _ = walk(lamp_xy, d, stop_lamp)
    legs[d] = (end, node, made)
    print(
        f"   the lamp's direction {d}: {end} at {node} after {made} Manhattan Links; the age of that Link: massive {age_of(made, d, True)}, the photon {age_of(made, d, False)}"
    )
reaching = {d: v for d, v in legs.items() if v[0] == "opening"}
lamp_leg_m = max(age_of(v[2], d, True) for d, v in reaching.items())
lamp_leg_p = max(age_of(v[2], d, False) for d, v in reaching.items())
print(
    f"   the rows that reach an opening: {sorted(reaching)}; the lamp leg {lamp_leg_m} intervals (massive) and {lamp_leg_p} (the photon); the first birth at tick 1, so the first re-release at the tick {1 + lamp_leg_m} (the photon's {1 + lamp_leg_p}: the run's 14)"
)
print()

fan = [tuple(v) for v in OPENINGS[0]["directions"]]
weights = OPENINGS[0]["table"]["light"]["weights"]
first_click = {}
rows_per_pixel = {}
longest = 0
longest_d = None
for opening in OPENINGS:
    o = tuple(opening["position"][:2])
    for d, w in zip(fan, weights, strict=True):
        end, node, made, per_axis = walk(o, d, stop_fan)
        tau = age_of(made, d, True)
        if tau > longest:
            longest, longest_d = tau, (d, end, node)
        if end == "screen":
            y = node[1]
            first_click[y] = min(first_click.get(y, 10**9), tau)
            rows_per_pixel.setdefault(y, []).append((o, d, w, made, per_axis, tau))
t0 = 1 + lamp_leg_m
for y in (60, 37, 83, 36, 84):
    print(
        f"   the screen pixel {y}: the first row's arrival {first_click[y]} intervals after the re-release, the first `click` line at screen_{y} about the tick {t0 + first_click[y]} ({len(rows_per_pixel[y])} rows land there)"
    )
print(
    f"   the longest row of a record: {longest} intervals, {longest_d[0]} to the {longest_d[1]} at {longest_d[2]}; a record born at the tick b completes about b + {lamp_leg_m} + {longest}: the 4096th birth about {4096 + lamp_leg_m + longest}, so every record of 4096 births gathers within about {4096 + lamp_leg_m + longest + 50} intervals (section 23.3's 5100 counted from the opening; the design's first round 5250)"
)
print(
    f"   the same count for the photon: the longest {max(age_of(walk(tuple(op['position'][:2]), d, stop_fan)[2], d, False) for op in OPENINGS for d in fan)} after the re-release at {1 + lamp_leg_p}: the registered run's records open at 4300 are those born after about {4300 - 1 - lamp_leg_p - max(age_of(walk(tuple(op['position'][:2]), d, stop_fan)[2], d, False) for op in OPENINGS for d in fan)} (149 registered)"
)
print()


def pearson(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True))
    return sxy / math.sqrt(sxx * syy) if sxx and syy else float("nan")


def massive_phase(per_axis, d):
    """The turn accumulator's count: floor(N sum_a |p_a| n_a / h) mod N (one floor over the axes)."""
    p = p_of[d]
    total = N * (abs(p[0]) * per_axis[0] + abs(p[1]) * per_axis[1])
    return (total // H) % N


def photon_phase(made, d):
    """The exact phase at the click (nature_beam.exact_phase): floor(n made T_D / (d S_1 Q)) mod N."""
    i = index_of[d]
    n, den = PHOTON_RATE
    s1, t = int(flight.manhattan[i]), int(flight.resolution[i])
    return ((n * made * t) // (den * s1 * Q)) % N


def leg_phase(d, massive):
    end, node, made = legs[d]
    if massive:
        _, _, _, per_axis = walk(lamp_xy, d, stop_lamp)
        return massive_phase(per_axis, d)
    return photon_phase(made, d)


print(
    "C. PEARSON WITH THE TWO-SOURCE COSINE ON THE DECLARED FAREY FAN (the review's M5 d): the weights per pixel from the rows that land there, the phases on the table of 64"
)
lam_m = H / P
lam_p = 64 / (PHOTON_RATE[0] / PHOTON_RATE[1] * math.sqrt(3))
print(
    f"   de Broglie's lambda = h / p = {lam_m:.4f} Links; the photon's at its rate {PHOTON_RATE[0]} / {PHOTON_RATE[1]} steps per interval of age at the pace 1 / sqrt 3: {lam_p:.4f}"
)
ys = list(range(SHAPE[1]))
cosine = []
for y in ys:
    l1, l2 = (
        math.hypot(SCREEN_X - o[0], y - o[1])
        for o in (tuple(OPENINGS[0]["position"][:2]), tuple(OPENINGS[1]["position"][:2]))
    )
    cosine.append(1 + math.cos(2 * math.pi * (l2 - l1) / lam_m))
for label, massive in (("massive", True), ("the photon", False)):
    leg = {tuple(v): leg_phase(tuple(v), massive) for v in reaching}
    leg_by_opening = {legs[d][1]: leg[d] for d in reaching}
    weights_px = []
    for y in ys:
        vx = vy = 0.0
        for o, d, w, made, per_axis, _tau in rows_per_pixel.get(y, []):
            phase = (
                leg_by_opening[o] + (massive_phase(per_axis, d) if massive else photon_phase(made, d))
            ) % N
            vx += w * math.cos(2 * math.pi * phase / N)
            vy += w * math.sin(2 * math.pi * phase / N)
        weights_px.append(vx * vx + vy * vy)
    with_rows = [y for y in ys if rows_per_pixel.get(y)]
    two = [y for y in ys if len({o for o, *_ in rows_per_pixel.get(y, [])}) == 2]
    r_all = pearson([weights_px[y] for y in with_rows], [cosine[y] for y in with_rows])
    r_two = pearson([weights_px[y] for y in two], [cosine[y] for y in two])
    bright = sorted(with_rows, key=lambda y: -weights_px[y])[:6]
    print(
        f"   {label}: Pearson over the {len(with_rows)} pixels with rows {r_all:.3f}, over the {len(two)} two-path pixels {r_two:.3f}; the brightest pixels {sorted(bright)}"
    )
print(
    "   the registered photon on this fan: the weights' 0.895, the counts' 0.891 (L2b); the design's first-round 0.96 +- 0.02 was the screen fan's map number and is withdrawn"
)
print()

print("D. THE BOUNDS (the review's section 3)")
pmax = max(sum(c * c for c in p_of[d]) for d in table)
print(
    f"   max p_D . p_D over the table {pmax}; E'^2 = {max(e_of.values()) ** 2}; the flight accumulator below 2 E' + 2 |p|_1 = {2 * max(e_of.values()) + 2 * max(sum(abs(c) for c in p_of[d]) for d in table)}; acc_turn below h + max |p_a| N = {H + max(max(abs(c) for c in p_of[d]) for d in table) * N}; the label per row amount x |p_D| at most {max(weights)} x {max(math.sqrt(sum(c * c for c in p_of[d])) for d in table):.0f}; all within 2^62"
)
print()

print("E. THE HOST COST WITH THE CORRECTED RUN (host numbers)")
photon_life = (
    1
    + lamp_leg_p
    + max(
        age_of(walk(tuple(op["position"][:2]), d, stop_fan)[2], d, False) for op in OPENINGS for d in fan
    )
)
massive_life = 1 + lamp_leg_m + longest
run = 4096 + lamp_leg_m + longest + 50
print(
    f"   a record's longest row lives {massive_life} intervals from its birth against the photon's {photon_life} ({massive_life / photon_life:.1f} times); slits_huygens ran 4300 intervals in 1334 s; slits_matter at 4096 births and {run} intervals: about {1334 / 4300 * massive_life / photon_life * run / 3600:.1f} hours; at 1024 births and {1024 + lamp_leg_m + longest + 50} intervals: about {1334 / 4300 * massive_life / photon_life * (1024 + lamp_leg_m + longest + 50) / 3600:.1f} hours"
)
print(
    "   the lamp's births: its clock reads its held content (by_clock over K = 2^30), 320 units spent per birth, so about 4096 x 4096 x 320 / (2 x 2^30) = 2.5 self-creations fewer by the 4096th interval: 4096 births take about 4099 intervals (the review's S4, about 5)"
)
