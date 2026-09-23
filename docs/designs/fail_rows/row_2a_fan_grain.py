"""Row 2a's fan-grain share, by the algebra and no run (the chief physicist,
2026-09-23, the Boss's order on the finding of RUN_10.md: the register's
Farey fan of width 48 has no direction within atan(1 / 47) = 1.22 degrees
of the axis).

The registered two-slit visibility of NATURE row 2a, 0.966 in the clicks
of `slits_huygens` against nature's 0.98 (Grangier 1986) and the ideal 1,
was read on the openings' Farey fan of width 48 weighted by angle. This
script runs the same pin machinery as `docs/designs/paper_criteria/
slits_huygens_pin.py` (the lamp's rows walked by the flight table, the
re-emission's whole phase, the exact phase at the click, the click's
bilinear form, the engine's own `rungs` and `cell_of` on the golden
wheel; reproduced the registered run bit for bit) on the registered world
with the openings' fan alone replaced: (a) the registered fan (the check:
wall 882, screen 1711, faces 1503, the visibility 0.9659); (b) the same
construction (the Farey fan weighted by the angle gap of its neighbours)
at larger widths, the continuum of the fan by angle; (c) fans uniform in
angle by SELECTION and unweighted (one direction per grain, the nearest
of the full fan within `direction_bound`), the loadable form under the
record form's ceiling (a weighted fan's norm squared must stay within
2^62 - 1 at load; the selected fan is not in that product). For each fan:
the clicks of the records 1 to 4096 per cell, the visibility over the
criterion's bright and dark pixels, the Pearson with the two-source
cosine, the first record's weights' visibility. Every number a
COMPUTATION; the run at head is the only DETECTOR reading and none is
made here.

Run from the repository root with PYTHONPATH=src:

    python docs/designs/fail_rows/row_2a_fan_grain.py > docs/designs/fail_rows/row_2a_fan_grain.out
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "docs" / "designs" / "fraction_free"))
sys.path.insert(0, str(ROOT / "docs" / "designs" / "paper_criteria"))

from slits_huygens_pin import (  # noqa: E402
    BRIGHT,
    COS,
    DARK,
    GOLDEN,
    HEIGHT,
    REGISTERED_TOTALS,
    SCALE,
    SCREEN_X,
    SIN,
    WORLD,
    N,
    W,
    cosine,
    exact_whole,
    phase_whole,
    walk,
)
from two_slits_map import pearson, resolution  # noqa: E402

from event_universe.events.amplitude import cell_of  # noqa: E402

FLIGHT_Q = 64
SLOPE = 13  # HUYGENS_SLOPE = 2 x 6 + 1: the admitted directions have |b| <= 13 a
GRAIN = 1 << 18  # HUYGENS_GRAIN, the angle weights' scale
MOMENTUM_BOUND = (1 << 62) - 1
REGISTERED_VISIBILITY = 0.9659
NATURE = 0.98
Vector = tuple[int, int]


def farey_fan(width: int) -> list[Vector]:
    """The full primitive fan a + |b| <= width, in angle order."""
    full = [
        (a, b)
        for a in range(1, width + 1)
        for b in range(-width, width + 1)
        if a + abs(b) <= width and math.gcd(a, b) == 1
    ]
    full.sort(key=lambda v: math.atan2(v[1], v[0]))
    return full


def weighted_fan(width: int) -> tuple[list[Vector], list[int]]:
    """The register's construction (`make_worlds.huygens_fan`) at any
    width: the admitted directions within the slope with the integer
    angle weight int(GRAIN x the mean of 3 Q^2 / (T_v T_w) over the two
    neighbours), the sine of the neighbours' gap (Farey neighbours have
    the cross product 1)."""
    full = farey_fan(width)
    weights = {}
    for i, v in enumerate(full):
        neighbours = [full[j] for j in (i - 1, i + 1) if 0 <= j < len(full)]
        gaps = [Fraction(3 * FLIGHT_Q * FLIGHT_Q, resolution(v) * resolution(w)) for w in neighbours]
        if len(gaps) == 1:
            gaps = gaps * 2
        weights[v] = int(GRAIN * sum(gaps) / 2)
    admitted = [v for v in full if abs(v[1]) <= SLOPE * v[0]]
    return admitted, [weights[v] for v in admitted]


def selected_fan(width: int, grain_degrees: float) -> list[Vector]:
    """One direction per grain of angle over the registered fan's angular
    range (|b| <= 13 a, +- 85.6 degrees), the nearest of the full fan
    a + |b| <= width; unweighted."""
    full = [v for v in farey_fan(width) if abs(v[1]) <= SLOPE * v[0]]
    angles = [math.degrees(math.atan2(b, a)) for a, b in full]
    half = math.degrees(math.atan(SLOPE))
    steps = int(round(2 * half / grain_degrees))
    chosen: list[Vector] = []
    for k in range(steps + 1):
        target = -half + k * grain_degrees
        nearest = min(range(len(full)), key=lambda i: (abs(angles[i] - target), i))
        if full[nearest] not in chosen:
            chosen.append(full[nearest])
    return chosen


def read_fan(world: dict[str, object], fan: list[Vector], weights: list[int]) -> dict[str, object]:
    """The pin machinery of `slits_huygens_pin.py` on the world with the
    openings' fan and weights replaced: the clicks of 4096 records."""
    n, d = world["families"][0]["phase_per_link"]
    lamp = next(m for m in world["measured"] if "lamp" in m)
    lamp_at = (lamp["position"][0], lamp["position"][1])
    lamp_dirs = [(v[0], v[1]) for v in lamp["lamp"]["directions"]]
    walls = {}
    openings = []
    for number, m in enumerate(world["measured"]):
        if "lamp" in m:
            continue
        node = (m["position"][0], m["position"][1])
        if "table" in m:
            openings.append(node)
        else:
            walls[node] = number
    screen = {(SCREEN_X, y): f"screen_{y}" for y in range(HEIGHT)}
    norm = sum(a * a for a in weights)
    lamp_m = len(lamp_dirs)

    def stop_lamp(node):
        if node in openings:
            return "opening"
        if node in walls:
            return "wall"
        if node in screen:
            return "screen"
        return None

    def stop_fan(node):
        if node[1] < 0:
            return "face:-y"
        if node[1] >= HEIGHT:
            return "face:+y"
        if node in screen:
            return "screen"
        if node in walls or node in openings:
            return "blocked"
        return None

    rows: list[tuple[str, tuple[int, int], int, int]] = []
    leg = {}
    for v in lamp_dirs:
        end, node, age, made = walk(lamp_at, v, stop_lamp)
        s1, t = sum(map(abs, v)), resolution(v)
        if end == "opening":
            leg[node] = phase_whole(age, n, d) % N
        elif end == "wall":
            rows.append((f"measured:{walls[node]}", node, 1, exact_whole(made, s1, t, n, d) % N))
        else:
            raise RuntimeError(f"the lamp's row {v} ends at {end} {node}")
    blocked = 0
    for opening in sorted(openings):
        for v, a in zip(fan, weights, strict=True):
            end, node, age, made = walk(opening, v, stop_fan)
            if end == "blocked":
                blocked += 1
                continue
            s1, t = sum(map(abs, v)), resolution(v)
            phi = (leg[opening] + exact_whole(made, s1, t, n, d)) % N
            rows.append((screen[node] if end == "screen" else end, node, a, phi))
    measured_cells = sorted(
        {r[0] for r in rows if r[0].startswith("measured")}, key=lambda s: int(s.split(":")[1])
    )
    order = measured_cells + [f"screen_{y}" for y in range(HEIGHT)] + ["face:+y", "face:-y"]
    multiplicity = {name: (lamp_m if name.startswith("measured") else lamp_m * norm) for name in order}
    by_cell: dict[str, dict[tuple[int, int], list[tuple[int, int]]]] = {}
    for name, node, a, phi in rows:
        by_cell.setdefault(name, {}).setdefault(node, []).append((a, phi))

    def numerators(u: int) -> list[int]:
        found = []
        for name in order:
            total = 0
            for node_rows in by_cell.get(name, {}).values():
                x = sum(SCALE * a * COS[(phi + u) % N] for a, phi in node_rows)
                y = sum(SCALE * a * SIN[(phi + u) % N] for a, phi in node_rows)
                total += x * x + y * y
            found.append(total)
        return found

    ladders = {}
    for u in range(N):
        nums = numerators(u)
        pairs = [(v, multiplicity[name]) for v, name in zip(nums, order, strict=True)]
        ladders[u] = pairs
    unit = SCALE * SCALE * 65536
    weights0 = [Fraction(v, m * unit) for v, m in ladders[0]]
    total0 = sum(weights0)
    screen_w = [float(weights0[order.index(f"screen_{y}")]) for y in range(HEIGHT)]
    bright_w = sum(screen_w[y] for y in BRIGHT) / len(BRIGHT)
    dark_w = sum(screen_w[y] for y in DARK) / len(DARK)
    counts = [0] * len(order)
    for b in range(W):
        u = (b * GOLDEN) % W
        k = cell_of(ladders[u % N], W, u)
        assert k is not None
        counts[k] += 1
    screen_counts = [counts[order.index(f"screen_{y}")] for y in range(HEIGHT)]
    wall = sum(counts[order.index(nm)] for nm in measured_cells)
    faces = counts[order.index("face:+y")] + counts[order.index("face:-y")]
    bright = sum(screen_counts[y] for y in BRIGHT) / len(BRIGHT)
    dark = sum(screen_counts[y] for y in DARK) / len(DARK)
    cos = [cosine(y) for y in range(HEIGHT)]
    return {
        "directions": len(fan),
        "norm": norm,
        "ceiling": norm * norm <= MOMENTUM_BOUND,
        "blocked": blocked,
        "wall": wall,
        "screen": sum(screen_counts),
        "faces": faces,
        "visibility": (bright - dark) / (bright + dark),
        "visibility_weights": (bright_w - dark_w) / (bright_w + dark_w),
        "pearson": pearson(screen_counts, cos),
        "dark_mean": dark,
        "bright_mean": bright,
        "screen_share": sum(screen_w) / float(total0),
    }


def main() -> None:
    world = json.loads(WORLD.read_text())
    opening = next(m for m in world["measured"] if "table" in m)
    registered = [(v[0], v[1]) for v in opening["directions"]]
    registered_w = list(opening["table"]["light"]["weights"])
    print(
        "row 2a, the fan's grain share, COMPUTATION (the pin machinery of slits_huygens_pin.py on the registered world with the"
        " openings' fan alone replaced; no run). The criterion: the clicks' visibility (mean bright - mean dark) / (mean bright"
        f" + mean dark) over the two-source cosine's bright pixels {BRIGHT} and dark pixels {DARK}; nature {NATURE}, the ideal 1."
    )
    print(
        f"the fan's angular range: |b| <= {SLOPE} a, +- {math.degrees(math.atan(SLOPE)):.1f} degrees; the registered fan's"
        f" smallest angle off the axis atan(1 / 47) = {math.degrees(math.atan(1 / 47)):.2f} degrees, the pixel at the screen's"
        f" distance 44 Links {math.degrees(math.atan(1 / 44)):.2f} degrees\n"
    )
    header = (
        "fan | directions | norm A | A^2 within 2^62 - 1 (loadable weighted) | wall / screen / faces of 4096 |"
        " dark mean | bright mean | VISIBILITY of the clicks | the weights' visibility | Pearson(counts, cosine)"
    )
    print(header)
    fans: list[tuple[str, list[Vector], list[int]]] = [
        ("registered: width 48, weighted by angle", registered, registered_w)
    ]
    for width in (110, 220):
        admitted, weights = weighted_fan(width)
        fans.append((f"weighted by angle, width {width}", admitted, weights))
    for width, grain in ((48, 0.25), (330, 0.25), (330, 0.15)):
        chosen = selected_fan(width, grain)
        fans.append(
            (f"selected one per {grain} deg, width {width}, unweighted", chosen, [1] * len(chosen))
        )
    results = {}
    for name, fan, weights in fans:
        r = read_fan(world, fan, weights)
        results[name] = r
        print(
            f"{name} | {r['directions']} | {r['norm']} | {r['ceiling']} | {r['wall']} / {r['screen']} / {r['faces']} |"
            f" {r['dark_mean']:.2f} | {r['bright_mean']:.2f} | {r['visibility']:.4f} | {r['visibility_weights']:.4f} |"
            f" {r['pearson']:.3f}" + (f" | blocked {r['blocked']}" if r["blocked"] else "")
        )
    reg = results["registered: width 48, weighted by angle"]
    reproduced = (
        reg["wall"] == REGISTERED_TOTALS["wall"]
        and reg["screen"] == REGISTERED_TOTALS["screen"]
        and reg["faces"] == REGISTERED_TOTALS["faces"]
        and abs(reg["visibility"] - REGISTERED_VISIBILITY) < 5e-4
    )
    print(
        f"\nthe registered fan reproduces the registered run (wall 882, screen 1711, faces 1503, the visibility 0.9659): {reproduced}"
    )
    best = max(results.values(), key=lambda r: r["visibility"])
    print(
        f"the largest visibility among the fans tried {best['visibility']:.4f}; the registered {reg['visibility']:.4f};"
        f" nature {NATURE}; the ideal 1. The fan-grain share of the shortfall 1 - {reg['visibility']:.4f} = {1 - reg['visibility']:.4f}:"
        f" at most {best['visibility'] - reg['visibility']:.4f} by the fans tried, {(best['visibility'] - reg['visibility']) / (1 - reg['visibility']):.0%} of it."
    )


if __name__ == "__main__":
    main()
