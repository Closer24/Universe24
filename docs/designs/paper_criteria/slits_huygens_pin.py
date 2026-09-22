"""The pin of NATURE row 2a for `slits_huygens`'s OWN fan, derived before
any run (the criteria runner, 2026-09-22, on the paper's referee point 6:
"the pin derived for this world's fan, not the screen's").

The register's own algebra applied to the registered world: the lamp's
five rows walked by the flight table (the closed form m(tau) = (2 tau S_1
Q + T_d) // (2 T_d), `docs/designs/fraction_free/two_slits_map.py`), the
two openings' re-emission on the world's declared Farey fan of width 48
with the world's declared integer angle weights (the split's `weights`,
each fan row's amount), the phase of every row at its click by BEAM_LAW
note 45 (the re-emission carries the leg's whole phase; one floor at the
click, floor(n made T_d / (d S_1 Q)), on the tables of N = 64), the
record's birth coordinate u = ordinal x 2531 mod 4096 on the golden wheel
with the rows' birth phase u mod 64 (note 46), the cells' weights by the
click's bilinear form on the tables (the sum per Node of |sum amount x
(C, S)[phase]|^2 over the set's multiplicity), and the ladder's rungs and
cell by the engine's own `rungs` and `cell_of` (`event_universe.events.
amplitude`), the same integers as the click's. Nothing here runs the
engine; the tables and the ladder are imported so that the integers are
the click's.

What it derives, in order: (1) the first record's total and shares and
the screen weights' Pearson and visibility under the exact phase (the
register's screen share 0.418 and peak 0.012; the 2026-09-20 pin under
the built phase, 2.677, 0.224 / 0.410 / 0.366, 0.895 and 0.954, printed
as history); (2) the first 64 births' clicks (wall 14, screen 27, faces
23, the register's totals for the run of 2026-09-21);
(3) the 4096 births' counts per cell under the golden wheel and the
exact phase, against the registered run of 2026-09-21 (wall 882, screen
1711 on 107 pixels, faces 1503; the counts y = 40 .. 80; the bright and
dark pixels), and from them THE PIN: the clicks' visibility (mean bright
- mean dark) / (mean bright + mean dark) over the two-source cosine's
bright pixels (y = 35 .. 38, 59 .. 61, 82 .. 85) and dark pixels (13 ..
20, 48 .. 50, 70 .. 72, 100 .. 107), the criterion of NATURE row 2a, for
THIS world's fan. Every number printed is a computation (the algebra's),
labelled so; the run at head compares its DETECTOR counts with it.

Run from the repository root with PYTHONPATH=src:

    python docs/designs/paper_criteria/slits_huygens_pin.py > docs/designs/paper_criteria/slits_huygens_pin.out
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "docs" / "designs" / "fraction_free"))

from two_slits_map import bresenham, manhattan_steps, pearson, resolution  # noqa: E402

from event_universe.core.integer import by_clock  # noqa: E402
from event_universe.core.phase import phase_cosines, phase_sines  # noqa: E402
from event_universe.events.amplitude import cell_of, rungs  # noqa: E402

WORLD = ROOT / "examples" / "events" / "amplitude" / "slits_huygens.json"
Q = 64
N = 64
W = 4096
GOLDEN = 2531
HEIGHT = 121
SCREEN_X = 52
SCALE = 32  # AMPLITUDE_SCALE: cancels in every ratio, kept so the numerators are the click's
COS = phase_cosines(N)
SIN = phase_sines(N)

# The two-source cosine's bright and dark pixels (NATURE row 2a; the
# amplitude README, L2b): the groups the visibility is read over.
BRIGHT = [35, 36, 37, 38, 59, 60, 61, 82, 83, 84, 85]
DARK = [13, 14, 15, 16, 17, 18, 19, 20, 48, 49, 50, 70, 71, 72, 100, 101, 102, 103, 104, 105, 106, 107]

# The registered run of 2026-09-21 (docs/EXPERIMENTS.md, L2b re-registered
# under the birth wheel; examples/events/amplitude/README.md): the counts
# at y = 40 .. 80, the bright and the dark pixels' counts, the totals.
REGISTERED_40_80 = [
    int(v)
    for v in "29 41 28 27 19 15 8 6 3 0 1 5 7 15 18 20 36 45 51 51 49 51 51 45 36 20 18 15 7 5 1 0 3 6 9 14 19 26 29 42 28".split()
]
REGISTERED_BRIGHT = [41, 19, 42, 38, 51, 49, 51, 39, 42, 20, 40]
REGISTERED_DARK = [3, 1, 0, 0, 0, 0, 0, 0, 3, 0, 1, 1, 0, 3, 0, 0, 0, 0, 0, 1, 0, 2]
REGISTERED_TOTALS = {"wall": 882, "screen": 1711, "faces": 1503, "screen pixels": 107}
REGISTERED_FIRST_64 = {"wall": 14, "screen": 27, "faces": 23}
REGISTERED_FIRST_64_PIXELS = [
    2,
    25,
    31,
    33,
    35,
    37,
    39,
    41,
    43,
    47,
    56,
    57,
    59,
    60,
    61,
    63,
    64,
    74,
    77,
    79,
    81,
    83,
    85,
    87,
    89,
    97,
    119,
]


def cosine(y: int) -> float:
    """The Euclidean two-source form 1 + cos(2 pi (r1 - r2) / lambda) at
    the pixel y, lambda = 8 intervals at the heading's pace 64 / 110."""
    wavelength = 8 * 64 / 110
    r1 = math.hypot(SCREEN_X - 8, y - 55)
    r2 = math.hypot(SCREEN_X - 8, y - 65)
    return 1 + math.cos(2 * math.pi * (r1 - r2) / wavelength)


def phase_whole(age: int, n: int, d: int) -> int:
    """The phase column after `age` intervals of the pair form: the sum of
    by_clock over the intervals (floor(age n / d)), the whole part."""
    return sum(by_clock(a, n, d) for a in range(age))


def exact_whole(made: int, s1: int, t: int, n: int, d: int) -> int:
    """The click's one floor (BEAM_LAW note 45): floor(n made T_d / (d S_1 Q))."""
    return (n * made * t) // (d * s1 * Q)


def walk(start, vector, stop):
    """The row's walk from `start` along the 2D vector by the flight table:
    (end, node, age, Links made)."""
    line = bresenham(vector)
    s1, t = len(line), resolution(vector)
    node = start
    made = 0
    tau = 0
    while True:
        tau += 1
        if manhattan_steps(tau, s1, t) > made:
            step = line[made % s1]
            node = (node[0] + step[0], node[1] + step[1])
            made += 1
            end = stop(node)
            if end is not None:
                return end, node, tau, made
        if tau > 10_000:
            raise RuntimeError("no end")


def main() -> None:
    world = json.loads(WORLD.read_text())
    n, d = world["families"][0]["phase_per_link"]
    lamp = next(m for m in world["measured"] if "lamp" in m)
    assert lamp["lamp"]["wheel"] == [GOLDEN, W], lamp["lamp"]["wheel"]
    lamp_at = (lamp["position"][0], lamp["position"][1])
    lamp_dirs = [(v[0], v[1]) for v in lamp["lamp"]["directions"]]
    walls = {}
    openings = {}
    for number, m in enumerate(world["measured"]):
        if "lamp" in m:
            continue
        node = (m["position"][0], m["position"][1])
        if "table" in m:
            openings[node] = (
                number,
                [(v[0], v[1]) for v in m["directions"]],
                m["table"]["light"]["weights"],
            )
        else:
            walls[node] = number
    screen = {(52, y): f"screen_{y}" for y in range(HEIGHT)}
    assert all(det["positions"] == [[52, y, 0]] for y, det in enumerate(world["detectors"]))
    weights_a = next(iter(openings.values()))[2]
    fan_a = sum(a * a for a in weights_a)
    lamp_m = len(lamp_dirs)
    print(
        f"slits_huygens: phase_per_link {n}/{d}; the lamp at {lamp_at} on {lamp_m} directions, the wheel [{GOLDEN}, {W}];"
        f" the openings {sorted(openings)} on {len(weights_a)} directions each, the angle weights {min(weights_a)} .. {max(weights_a)},"
        f" A = sum a^2 = {fan_a}; the fan rows' multiplicity {lamp_m} x A = {lamp_m * fan_a}; the walls {len(walls)} Nodes"
    )

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

    # 1. The rows: (cell name, Node, amount, the phase without the birth phase).
    rows: list[tuple[str, tuple[int, int], int, int]] = []
    leg = {}
    for v in lamp_dirs:
        end, node, age, made = walk(lamp_at, v, stop_lamp)
        s1, t = sum(map(abs, v)), resolution(v)
        if end == "opening":
            leg[node] = phase_whole(age, n, d) % N
            print(
                f"  the lamp's row {v} reaches the opening {node} at the age {age}, the leg's whole phase {leg[node]}"
            )
        elif end == "wall":
            phi = exact_whole(made, s1, t, n, d) % N
            rows.append((f"measured:{walls[node]}", node, 1, phi))
            print(
                f"  the lamp's row {v} ends at the wall {node} (measured {walls[node]}) at the age {age}, the click's phase {phi}"
            )
        else:
            raise RuntimeError(f"the lamp's row {v} ends at {end} {node}")
    blocked = 0
    for opening, (_, fan, weights) in sorted(openings.items()):
        for v, a in zip(fan, weights, strict=True):
            end, node, age, made = walk(opening, v, stop_fan)
            s1, t = sum(map(abs, v)), resolution(v)
            if end == "blocked":
                blocked += 1
                continue
            phi = (leg[opening] + exact_whole(made, s1, t, n, d)) % N
            name = screen[node] if end == "screen" else end
            rows.append((name, node, a, phi))
    print(
        f"  fan rows {sum(1 for r in rows if not r[0].startswith('measured'))} ({blocked} blocked, expected 0), wall rows {sum(1 for r in rows if r[0].startswith('measured'))}"
    )

    # The ladder's order (engine.py: the measured events outside every
    # declared detector by number, the declared detectors, the faces in
    # Port order): the cells that can carry weight, in that order.
    measured_cells = sorted(
        {r[0] for r in rows if r[0].startswith("measured")}, key=lambda s: int(s.split(":")[1])
    )
    order = measured_cells + [f"screen_{y}" for y in range(HEIGHT)] + ["face:+y", "face:-y"]
    multiplicity = {name: (lamp_m if name.startswith("measured") else lamp_m * fan_a) for name in order}
    by_cell: dict[str, dict[tuple[int, int], list[tuple[int, int]]]] = {}
    for name, node, a, phi in rows:
        by_cell.setdefault(name, {}).setdefault(node, []).append((a, phi))

    def numerators(u: int) -> list[int]:
        """Per cell the click's numerator at the birth phase u mod N: the sum
        over the cell's Nodes of X^2 + Y^2, X = sum SCALE x amount x C[phase]."""
        found = []
        for name in order:
            total = 0
            for node_rows in by_cell.get(name, {}).values():
                x = sum(SCALE * a * COS[(phi + u) % N] for a, phi in node_rows)
                y = sum(SCALE * a * SIN[(phi + u) % N] for a, phi in node_rows)
                total += x * x + y * y
            found.append(total)
        return found

    unit = SCALE * SCALE * 65536  # one row of amount 1 at multiplicity 1
    ladders = {}
    for u in range(N):
        nums = numerators(u)
        pairs = [(v, multiplicity[name]) for v, name in zip(nums, order, strict=True)]
        ladders[u] = (pairs, rungs(pairs, W)[0])

    # 1. The first record (u = 0): the total and the shares; the screen weights.
    pairs0, rungs0 = ladders[0]
    weights0 = [Fraction(v, m * unit) for v, m in pairs0]
    total0 = sum(weights0)

    def share(names: set[str]) -> float:
        return float(sum(w for w, nm in zip(weights0, order, strict=True) if nm in names) / total0)

    print(
        f"\n1. THE FIRST RECORD (u = 0) UNDER THE EXACT PHASE, a computation: the total {float(total0):.4f} of the birth norm;"
        f" the shares wall {share(set(measured_cells)):.3f} / screen {share({f'screen_{y}' for y in range(HEIGHT)}):.3f}"
        f" / faces {share({'face:+y', 'face:-y'}):.3f} (the register's screen share under the exact phase 0.418;"
        " the 2026-09-20 pin under the BUILT phase, history: 2.677 and 0.224 / 0.410 / 0.366)"
    )
    screen_w = [float(weights0[order.index(f"screen_{y}")]) for y in range(HEIGHT)]
    cos = [cosine(y) for y in range(HEIGHT)]
    bright_w = sum(screen_w[y] for y in BRIGHT) / len(BRIGHT)
    dark_w = sum(screen_w[y] for y in DARK) / len(DARK)
    peak = max(range(HEIGHT), key=lambda y: screen_w[y])
    print(
        f"   the screen weights under the exact phase: Pearson with the two-source cosine {pearson(screen_w, cos):.3f};"
        f" the visibility (mean bright - mean dark) / (mean bright + mean dark) {(bright_w - dark_w) / (bright_w + dark_w):.3f};"
        f" the peak at y = {peak} at {screen_w[peak] / float(total0):.5f} of the total (the register's 0.012 under the exact phase;"
        " under the BUILT phase of 2026-09-20, history: Pearson 0.895, visibility 0.954, the peak y = 59 at 0.01204)"
    )

    # 2 and 3. The clicks under the golden wheel: the cell of u by the engine's cell_of.
    def clicks(births: int) -> list[int]:
        counts = [0] * len(order)
        for b in range(births):
            u = (b * GOLDEN) % W
            pairs, _ = ladders[u % N]
            k = cell_of(pairs, W, u)
            assert k is not None
            counts[k] += 1
        return counts

    def summary(counts: list[int]) -> tuple[int, dict[int, int], tuple[int, int]]:
        wall = sum(counts[order.index(nm)] for nm in measured_cells)
        scr = {
            y: counts[order.index(f"screen_{y}")]
            for y in range(HEIGHT)
            if counts[order.index(f"screen_{y}")]
        }
        faces = (counts[order.index("face:+y")], counts[order.index("face:-y")])
        return wall, scr, faces

    counts64 = clicks(64)
    wall, scr, faces = summary(counts64)
    walls_by_cell = [counts64[order.index(nm)] for nm in measured_cells]
    print(
        f"\n2. THE FIRST 64 BIRTHS UNDER THE GOLDEN WHEEL AND THE EXACT PHASE, a computation: wall {wall} {tuple(walls_by_cell)},"
        f" screen {sum(scr.values())} on {len(scr)} pixels {sorted(scr)}, faces {sum(faces)} {faces};"
        f" the register's totals for the run of 2026-09-21: wall {REGISTERED_FIRST_64['wall']}, screen {REGISTERED_FIRST_64['screen']},"
        f" faces {REGISTERED_FIRST_64['faces']}, reproduced: {wall == 14 and sum(scr.values()) == 27 and sum(faces) == 23};"
        f" the pixel list of the 2026-09-20 run under the BUILT phase and the wheel [1, 64], history: {REGISTERED_FIRST_64_PIXELS}"
    )

    counts = clicks(W)
    wall, scr, faces = summary(counts)
    screen_counts = [counts[order.index(f"screen_{y}")] for y in range(HEIGHT)]
    bright = [screen_counts[y] for y in BRIGHT]
    dark = [screen_counts[y] for y in DARK]
    visibility = (sum(bright) / len(bright) - sum(dark) / len(dark)) / (
        sum(bright) / len(bright) + sum(dark) / len(dark)
    )
    print(
        f"\n3. THE 4096 BIRTHS UNDER THE GOLDEN WHEEL AND THE EXACT PHASE, a computation: wall {wall}, screen {sum(scr.values())} on {len(scr)} pixels,"
        f" faces {sum(faces)} {faces}; registered wall {REGISTERED_TOTALS['wall']}, screen {REGISTERED_TOTALS['screen']} on {REGISTERED_TOTALS['screen pixels']}, faces {REGISTERED_TOTALS['faces']}"
    )
    print(f"   the counts y = 40 .. 80: {' '.join(str(screen_counts[y]) for y in range(40, 81))}")
    print(f"   registered:              {' '.join(map(str, REGISTERED_40_80))}")
    print(f"   equal on y = 40 .. 80: {screen_counts[40:81] == REGISTERED_40_80}")
    print(
        f"   the bright pixels {bright} (registered {REGISTERED_BRIGHT}); the dark {dark} (registered {REGISTERED_DARK})"
    )
    print(
        f"   Pearson(counts, cosine) {pearson(screen_counts, cos):.3f} (registered 0.891);"
        f" THE VISIBILITY OF THE CLICKS {visibility:.4f} (registered 0.966)"
    )
    print(f"   every screen pixel's count: {screen_counts}")
    print(f"   the wall cells {[counts[order.index(nm)] for nm in measured_cells]}, the faces {faces}")
    # The band: the counts against the first record's rungs (the expected
    # counts 4096 x weight / total), the registered statement "within 2".
    expected0 = [rungs0[k] - (rungs0[k - 1] if k else 0) for k in range(len(order))]
    worst = max(abs(c - e) for c, e in zip(counts, expected0, strict=True))
    print(
        f"   against the first record's rungs (the expected counts): the worst cell off by {worst} (registered: within 2)"
    )
    exact_match = (
        screen_counts[40:81] == REGISTERED_40_80
        and bright == REGISTERED_BRIGHT
        and dark == REGISTERED_DARK
        and wall == REGISTERED_TOTALS["wall"]
        and sum(scr.values()) == REGISTERED_TOTALS["screen"]
        and sum(faces) == REGISTERED_TOTALS["faces"]
    )
    print(f"\n   THE COMPUTATION REPRODUCES THE REGISTERED RUN OF 2026-09-21: {exact_match}")
    print(
        "\nTHE PIN FOR THIS WORLD'S FAN (the algebra's, before the run at head): the clicks' visibility over the"
        f" named bright and dark pixels {visibility:.4f}, the counts per cell as printed above, bit for bit"
        " (the ladder is deterministic: the same 4096 u on the same 64 ladders); the criterion of NATURE row 2a:"
        " FAIL against the measured 0.98 (Grangier, Roger and Aspect 1986) and the ideal 1 by the algebra itself,"
        f" {0.98 - visibility:.3f} below the measured and {1 - visibility:.3f} below the ideal; the run at head confirms the"
        " integers or refutes the closed form (a count off its pinned cell by more than the rungs' own width, one click)."
    )


if __name__ == "__main__":
    main()
