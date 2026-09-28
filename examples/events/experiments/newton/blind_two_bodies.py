"""THE BLIND EXPECTATION of two whole bodies' fall, from the law's line and the files alone, before any run. Newton's fall a = Delta |d omega_b / dc| grad(c): Delta the band's curvature at k = 0 (cos omega = (num / 3 den) SUM cos k), d omega_b / dc from Rule3's coefficients at the body's centre pace and its own rotation (2 cos omega_b = (S(p) + 2 R(p) K) / w, K the mode's neighbour sum solved from the record), grad(c) the other body's content, every held row it sources at rest (THE START's solver at each row's divisor) averaged over this body's Nodes weighted by their counts; both bodies fall toward each other, the closing of their centroids integrated from rest until their faces touch. Usage: blind_two.py <world.json> (reads <world>.mode.json, writes <world>.expectation.json)."""

import json
import math
import sys
from pathlib import Path

import numpy as np

from event_universe.features.start import rest
from event_universe.world_files import world_files

path = Path(sys.argv[1])
world = json.loads(path.read_text())
mode = json.loads(path.with_suffix(".mode.json").read_text())
universe = world_files(world)[world["universe"]]
rows = {f["name"]: f for f in universe["families"]}
gamma = int(universe["integers"]["node_clock"])
shape = tuple(world["shape"])
wrap = tuple(world["boundary"][a] == "periodic" for a in "xyz")
gravity = rows["gravity"]
g_pair = tuple(gravity["pair"])
g_div = int(gravity["held"]["divisor"])
num, den = mode["bodies"][0]["pair"]
w = 6 * den * gamma * gamma


def S(p):
    return 12 * den * gamma * gamma - 6 * (p * p + gamma * gamma) * (den - num) - 12 * num * p * p


def R(p):
    return 2 * num * p * p


def dS(p):
    return -12 * p * (den - num) - 24 * num * p


def dR(p):
    return 4 * num * p


counts, centres = [], []
for body in world["measured"]:
    arr = np.zeros(shape, dtype=np.int64)
    for entry in body["nodes"]:
        arr[tuple(entry["node"])] = entry["count"]
    counts.append(arr)
    centres.append(tuple(int(v) for v in np.unravel_index(int(arr.argmax()), shape)))
held = [
    (tuple(row["pair"]), int(row["held"]["divisor"]))
    for row in rows.values()
    if isinstance(row.get("held"), dict) and row["held"].get("count") == "content"
]
# each body's content alone: every held row it sources (the pace reads them all, gravity's long reach and
# the binding row's short one); the gravity row alone beside it for the reading
fields = [
    sum(
        np.asarray(rest(c, pair, divisor_wrap[0], divisor_wrap[1]).levels, dtype=float)
        for pair, *divisor_wrap in ((pair, wrap, divisor) for pair, divisor in held)
    )
    for c in counts
]
gravity_alone = [np.asarray(rest(c, g_pair, wrap, g_div).levels, dtype=float) for c in counts]


def gravity_gradient(i):
    other, total, weight = gravity_alone[1 - i], 0.0, 0.0
    for (x, y, z), count in zip(
        zip(*np.nonzero(counts[i]), strict=True), counts[i][np.nonzero(counts[i])], strict=True
    ):
        total += count * slope_at(other, min(max(int(x), 1), shape[0] - 2), y, z)
        weight += count
    return total / weight


def content_at(i):  # every held row's rest of both bodies at body i's centre
    total = 0
    for row in rows.values():
        held = row.get("held")
        if isinstance(held, dict) and held.get("count") == "content":
            total += int(
                np.asarray(
                    rest(counts[0] + counts[1], tuple(row["pair"]), wrap, int(held["divisor"])).levels
                )[centres[i]]
            )
    return total


def slope(i):
    a, level = mode["bodies"][i]["clock"]
    two_cos = a / level
    omega = math.acos(two_cos / 2)
    p = gamma - content_at(i)
    K = (w * two_cos - S(p)) / (2 * R(p))
    d_two_cos_dp = (dS(p) + 2 * dR(p) * K) / w
    return abs(d_two_cos_dp) / (2 * math.sin(omega)), p, omega, K


cos0 = num / den
delta = (num / (3 * den)) / math.sqrt(1 - cos0 * cos0)  # the band's curvature at k = 0


def slope_at(field, j, y, z):
    return (field[j + 1, y, z] - field[j - 1, y, z]) / 2


def grad(
    i, shift
):  # the other body's field gradient along x over body i's Nodes shifted by `shift` Links (toward the other)
    other = fields[1 - i]
    total, weight = 0.0, 0.0
    for (x, y, z), count in zip(
        zip(*np.nonzero(counts[i]), strict=True), counts[i][np.nonzero(counts[i])], strict=True
    ):
        xs = x + shift
        xi = int(math.floor(xs))
        f = xs - xi
        xi = min(max(xi, 1), shape[0] - 3)

        total += count * ((1 - f) * slope_at(other, xi, y, z) + f * slope_at(other, xi + 1, y, z))
        weight += count
    return total / weight


slopes = [slope(0), slope(1)]
sign = [1.0, -1.0]  # body 0 falls toward +x, body 1 toward -x


def faces(arr):
    xs = np.nonzero(arr.sum(axis=(1, 2)))[0]
    return int(xs.min()), int(xs.max())


gap = faces(counts[1])[0] - faces(counts[0])[1] - 1
x = [0.0, 0.0]
v = [0.0, 0.0]
t = 0
path_closing, path_each = {}, {}
while x[0] + x[1] < gap and t < 5000:
    for i in (0, 1):
        g = grad(i, sign[i] * x[i]) * sign[i]  # the gradient in the direction of the other body
        v[i] += delta * slopes[i][0] * g
        x[i] += v[i]
    t += 1
    if t in (25, 50, 75, 100, 125, 150, 175, 200, 250, 300, 400, 500, 600):
        path_closing[t] = round(x[0] + x[1], 3)
        path_each[t] = [round(x[0], 3), round(x[1], 3)]
blind = {
    "status": "BLIND: written from the law's line and the files before any run; GAMEBOARD readings",
    "row": "NEWTON'S FALL OF TWO WHOLE BODIES: each body the fixed point of its binding row on its Nodes (the generator), each falling in the other's content (every held row the other sources, gravity's long reach and the binding row's short one, the pace reads them all) at a = Delta |d omega_b / dc| grad(c) toward the other; the closing of the two count-weighted centroids along x from rest; the touch when the bodies' faces meet",
    "delta_band_curvature": round(delta, 4),
    "bodies": [
        {
            "centre": list(centres[i]),
            "nodes": int(np.count_nonzero(counts[i])),
            "quanta": int(counts[i].sum()),
            "clock": mode["bodies"][i]["clock"],
            "two_cos": round(mode["bodies"][i]["clock"][0] / mode["bodies"][i]["clock"][1], 4),
            "centre_pace": slopes[i][1],
            "d_omega_dc": f"{slopes[i][0]:.3e}",
            "mode_neighbour_sum_K": round(slopes[i][3], 4),
            "gradient_at_start_levels_per_link": round(grad(i, 0.0) * sign[i], 4),
            "gravity_alone_gradient_at_start": round(gravity_gradient(i) * sign[i], 4),
            "acceleration_at_start": f"{delta * slopes[i][0] * grad(i, 0.0) * sign[i]:.3e}",
        }
        for i in (0, 1)
    ],
    "gap_links_at_start": gap,
    "closing_links_at_intervals": path_closing,
    "each_body_links_at_intervals": path_each,
    "touch_interval_blind": t,
    "band": "the engine's centroids within 30 percent of the closing at every listed interval, the touch within 30 percent; a finding otherwise",
}
path.with_suffix(".expectation.json").write_text(json.dumps(blind, indent=1))
print(json.dumps({k: v for k, v in blind.items() if k not in ("row", "status")}))
