"""The two slits under the record click, as integers (read-only, the
mathematician, 2026-09-20): the registered `slits_low` world reconstructed
row by row (the lamp's five rows, the two openings' fans of 91, the walk
by the flight table, the phase by the pair form of `phase_per_link`, the
offers per set, the ladder of N = 64), then the same record under the
exact phase of the fraction-free law (one exact sum along the path, one
floor at the click) and under a finer birth wheel for u, so that the
four questions of TWO_SLITS.md are answered on numbers before any run.

Run from the repository root with PYTHONPATH=src:

    python docs/designs/fraction_free/two_slits_map.py > docs/designs/fraction_free/two_slits_map.out

Nothing here touches the engine; the tables C, S and `by_clock` are the
engine's own, imported so that the integers are the click's.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

from event_universe.core.integer import by_clock
from event_universe.core.phase import phase_cosines, phase_sines

Q = 64
N = 64
WORLD = Path(__file__).resolve().parents[3] / "examples" / "events" / "amplitude" / "slits_low.json"
SCREEN_X = 52
HEIGHT = 121
LAMP = (2, 60)
OPENINGS = ((8, 55), (8, 65))
WALL_X7 = {58, 60, 62}
# The registered world's numbers (`examples/events/amplitude/slits_low.json`
# on main, 2026-09-20): the pair form of the family's phase, the lamp's
# directions; the openings' fan is [1, 0] and the 90 primitive directions
# (a, b) with a >= 1, b != 0 and a + |b| <= 12.
PHASE_PER_LINK = (8591334592, 1073741824)
LAMP_DIRECTIONS = ((1, 0), (1, 1), (1, -1), (2, 1), (2, -1))
COS = phase_cosines(N)
SIN = phase_sines(N)

# The registered reading of `slits_low` (docs/EXPERIMENTS.md, series L2,
# 2026-09-20): the clicks over the 64 births by the ladder.
REGISTERED_SCREEN = {
    11: 1,
    29: 1,
    36: 1,
    43: 1,
    50: 1,
    56: 1,
    59: 1,
    60: 1,
    61: 2,
    70: 1,
    77: 1,
    82: 1,
    90: 1,
    107: 1,
}
REGISTERED_WALL = (11, 12, 11)
REGISTERED_FACES = (8, 7)


def resolution(vector: tuple[int, int]) -> int:
    """T_d = isqrt(3 |D|^2 Q^2), the flight table's resolution."""
    return math.isqrt(3 * (vector[0] ** 2 + vector[1] ** 2) * Q * Q)


def bresenham(vector: tuple[int, int]) -> list[tuple[int, int]]:
    """One period of the digital line (the engine's `_bresenham` in two
    dimensions: the axis furthest behind, the lowest axis first)."""
    s1 = abs(vector[0]) + abs(vector[1])
    line = []
    position = [0, 0]
    for j in range(s1):
        best = max(range(2), key=lambda i: (abs(vector[i]) * (j + 1) - s1 * abs(position[i]), -i))
        step = [0, 0]
        step[best] = 1 if vector[best] > 0 else -1
        position[best] += step[best]
        line.append((step[0], step[1]))
    return line


def manhattan_steps(tau: int, s1: int, t: int) -> int:
    """m(tau) = (2 tau S_1 Q + T_d) // (2 T_d)."""
    return (2 * tau * s1 * Q + t) // (2 * t)


def walk(start: tuple[int, int], vector: tuple[int, int], stop):
    """The row's walk from `start` along `vector`: at every interval of
    age the flight table's step (one Link or none); `stop(node)` names the
    end ('wall', 'screen', 'face') or None. Returns (end, node, age, the
    Manhattan steps made)."""
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


def stop_fan(node):
    if node[1] < 0 or node[1] >= HEIGHT:
        return "face"
    if node[0] == SCREEN_X:
        return "screen"
    return None


def stop_lamp(node):
    if node[0] == 7 and node[1] in WALL_X7:
        return "wall"
    if node in OPENINGS:
        return "opening"
    return None


def phase_by_clock(age: int, n: int, d: int) -> int:
    """The pair form as built: the sum of `by_clock` over the intervals of
    age (a floor per interval), mod N."""
    return sum(by_clock(a, n, d) for a in range(age)) % N


def exact_phase(made: int, s1: int, t: int, n: int, d: int) -> Fraction:
    """The fraction-free phase at the click: the rate times the exact time
    of the walk's last step, made x T_d / (S_1 Q) intervals, one rational."""
    return Fraction(n, d) * Fraction(made * t, s1 * Q)


def pearson(xs, ys) -> float:
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True))
    return sxy / math.sqrt(sxx * syy) if sxx and syy else float("nan")


def rungs(weights: list[int], steps: int) -> list[int]:
    """The ladder as built: b_k = (2 N C_k + T) // (2 T)."""
    total = sum(weights)
    found, cumulative = [], 0
    for value in weights:
        cumulative += value
        found.append((2 * steps * cumulative + total) // (2 * total))
    return found


def choose(found: list[int], u: int) -> int:
    for k, b in enumerate(found):
        if u < b:
            return k
    return len(found) - 1


def bit_reverse(value: int, bits: int) -> int:
    result = 0
    for _ in range(bits):
        result = (result << 1) | (value & 1)
        value >>= 1
    return result


def main() -> None:
    n, d = PHASE_PER_LINK
    lamp_dirs = list(LAMP_DIRECTIONS)
    fan = [(1, 0)] + [
        (a, b)
        for a in range(1, 12)
        for b in range(-11, 12)
        if b and a + abs(b) <= 12 and math.gcd(a, b) == 1
    ]
    if WORLD.exists():
        # The registered world, where the checkout carries it: the same numbers.
        world = json.loads(WORLD.read_text())
        assert tuple(world["families"][0]["phase_per_link"]) == PHASE_PER_LINK
        assert [
            tuple(v[:2]) for v in next(m for m in world["measured"] if "lamp" in m)["lamp"]["directions"]
        ] == lamp_dirs
        assert sorted(
            tuple(v[:2]) for v in next(m for m in world["measured"] if "table" in m)["directions"]
        ) == sorted(fan)
    print(f"slits_low: phase_per_link {n}/{d} = {n / d:.10f} steps per interval; fan {len(fan)}; N {N}")
    print(
        f"by_clock at that rate over 300 intervals: values {sorted({by_clock(a, n, d) for a in range(300)})}"
    )

    # 1. The lamp's leg.
    print("\n1. THE LAMP'S FIVE ROWS (born at phase u; the walk from (2, 60))")
    lamp_rows = []
    for vector in lamp_dirs:
        end, node, age, made = walk(LAMP, vector, stop_lamp)
        lamp_rows.append((vector, end, node, age, made))
        s1, t = sum(map(abs, vector)), resolution(vector)
        print(
            f"  {vector}: {end} at {node}, age {age}, steps {made}, phase {phase_by_clock(age, n, d)} (+u), exact {float(exact_phase(made, s1, t, n, d)) % N:.3f}"
        )

    # 2. The fans: every row's end, age and phase under both forms.
    print("\n2. THE TWO FANS OF 91 (re-released at the opening at age 0 with the leg's phase)")
    leg_phase = {
        node: phase_by_clock(age, n, d) for _, end, node, age, _ in lamp_rows if end == "opening"
    }
    leg_exact = {
        node: exact_phase(made, sum(map(abs, v)), resolution(v), n, d)
        for v, end, node, _, made in lamp_rows
        if end == "opening"
    }
    rows = []  # (opening index, vector, end, node, age, phase_built (without u), phase_exact (Fraction, without u))
    for o, opening in enumerate(OPENINGS):
        for vector in fan:
            end, node, age, made = walk(opening, vector, stop_fan)
            s1, t = sum(map(abs, vector)), resolution(vector)
            built = (leg_phase[opening] + phase_by_clock(age, n, d)) % N
            exact = (leg_exact[opening] + exact_phase(made, s1, t, n, d)) % N
            rows.append((o, vector, end, node, age, built, exact))
    ends = {}
    for row in rows:
        ends[row[2]] = ends.get(row[2], 0) + 1
    print(f"  ends: {ends}")
    screen_rows = {}
    for row in rows:
        if row[2] == "screen":
            screen_rows.setdefault(row[3][1], []).append(row)
    two = sorted(y for y, r in screen_rows.items() if len(r) >= 2)
    print(f"  pixels with rows {len(screen_rows)}, with two paths {len(two)}: {two}")
    whole = sum(1 for row in rows if row[2] == "screen" and row[6].denominator == 1)
    print(
        f"  screen rows whose exact phase is whole: {whole} of {ends['screen']}; the arrival's rounding per row, exact - built, in steps:"
    )
    diffs = sorted(
        round(
            float((row[6] - row[5]) % N if (row[6] - row[5]) % N < N / 2 else (row[6] - row[5]) % N - N),
            2,
        )
        for row in rows
        if row[2] == "screen"
    )
    print(
        f"    min {diffs[0]}, max {diffs[-1]}, |mean| {sum(map(abs, diffs)) / len(diffs):.2f} (one interval = 8 steps = 45 degrees)"
    )

    # 3. The per-pixel weights under the two phase forms, against the Euclidean cosine.
    print(
        "\n3. THE SCREEN'S WEIGHTS PER PIXEL (x 455, a birth's norm 1), built phase against exact phase"
    )
    c_links = Fraction(Q, resolution((1, 0)))  # Links per interval on a heading: 64/110
    wavelength = Fraction(N, n) * d * c_links  # Links per turn
    print(
        f"  the wavelength {float(wavelength):.4f} Links (8 intervals at {float(c_links):.4f} Links per interval); the openings 10 apart, the screen 44 away: the fringe spacing {float(wavelength) * 44 / 10:.2f} pixels"
    )

    def cosine(y: int) -> float:
        r1 = math.hypot(SCREEN_X - OPENINGS[0][0], y - OPENINGS[0][1])
        r2 = math.hypot(SCREEN_X - OPENINGS[1][0], y - OPENINGS[1][1])
        return 1 + math.cos(2 * math.pi * (r1 - r2) / float(wavelength))

    def weight_built(rows_at, u: int) -> int:
        x = sum(COS[(r[5] + u) % N] for r in rows_at)
        s = sum(SIN[(r[5] + u) % N] for r in rows_at)
        return x * x + s * s

    def weight_exact(rows_at, u: int, table: int) -> float:
        # One floor at the click on a table of `table` steps (the same
        # rounding the tables make), the birth phase u added exactly.
        z = 0j
        for r in rows_at:
            p = math.floor((r[6] + u) * table / N) % table
            z += complex(math.cos(2 * math.pi * p / table), math.sin(2 * math.pi * p / table))
        return abs(z) ** 2

    ys = sorted(screen_rows)
    built = [weight_built(screen_rows[y], 0) / 65536 for y in ys]
    exact64 = [weight_exact(screen_rows[y], 0, 64) for y in ys]
    exact_fine = [weight_exact(screen_rows[y], 0, 4096) for y in ys]
    cos = [cosine(y) for y in ys]
    incoherent = [len(screen_rows[y]) for y in ys]
    print(
        f"  Pearson over the {len(ys)} pixels with rows: built vs cosine {pearson(built, cos):.3f}, built vs incoherent {pearson(built, incoherent):.3f}"
    )
    print(
        f"    exact (table 64) vs cosine {pearson(exact64, cos):.3f}, exact (table 4096) vs cosine {pearson(exact_fine, cos):.3f}, exact vs incoherent {pearson(exact_fine, incoherent):.3f}"
    )
    two_i = [i for i, y in enumerate(ys) if len(screen_rows[y]) >= 2]
    print(
        f"  over the {len(two_i)} two-path pixels alone: built vs cosine {pearson([built[i] for i in two_i], [cos[i] for i in two_i]):.3f}, exact vs cosine {pearson([exact_fine[i] for i in two_i], [cos[i] for i in two_i]):.3f}"
    )
    print(
        "  the two-path pixels (y, exact phase difference in steps of 64, built difference, cosine, built weight, exact weight):"
    )
    for i in two_i:
        y = ys[i]
        a, b = screen_rows[y][0], screen_rows[y][1]
        dx = float((b[6] - a[6]) % N)
        db = (b[5] - a[5]) % N
        print(
            f"    {y:3d}: exact {dx:6.2f}  built {db:2d}  cos {cos[i]:.3f}  built {built[i]:.3f}  exact {exact_fine[i]:.3f}"
        )

    # 4. The ladder of the whole record under the built phase: the validation against the register.
    print("\n4. THE LADDER AS BUILT (N = 64, u = 0 .. 63): the clicks per set against the register")
    order = []  # (name, list of Node groups; each group a list of rows (phase field index))
    for vector, end, node, age, made in lamp_rows:
        if end == "wall":
            s1, t = sum(map(abs, vector)), resolution(vector)
            order.append(
                (f"wall {node}", [[(phase_by_clock(age, n, d), exact_phase(made, s1, t, n, d) % N)]])
            )
    for y in range(HEIGHT):
        at = screen_rows.get(y, [])
        order.append((f"screen_{y}", [[(r[5], r[6]) for r in at]] if at else []))
    for face, side in (("+y", HEIGHT - 1), ("-y", 0)):
        groups = {}
        for row in rows:
            if row[2] == "face" and (row[3][1] >= HEIGHT if side else row[3][1] < 0):
                groups.setdefault(row[3][0], []).append((row[5], row[6]))
        order.append((f"face {face}", list(groups.values())))

    def cell_weights(u: int, exact: bool) -> list[Fraction]:
        found = []
        for name, groups in order:
            m = 5 if name.startswith("wall") else 455
            total = Fraction(0)
            for group in groups:
                if exact:
                    z = 0j
                    for _, ph in group:
                        p = math.floor((ph + u) * 4096 / N) % 4096
                        z += complex(math.cos(2 * math.pi * p / 4096), math.sin(2 * math.pi * p / 4096))
                    total += Fraction(round(abs(z) ** 2 * 65536)) / (65536 * m)
                else:
                    x = sum(COS[(ph + u) % N] for ph, _ in group)
                    s = sum(SIN[(ph + u) % N] for ph, _ in group)
                    total += Fraction(x * x + s * s, 65536 * m)
            found.append(total)
        return found

    def clicks(wheel: int, births: int, exact: bool, reverse: bool):
        counts = [0] * len(order)
        for b in range(births):
            u_index = bit_reverse(b % wheel, wheel.bit_length() - 1) if reverse else b % wheel
            u = u_index * N // wheel if wheel >= N else u_index
            weights = cell_weights(u % N, exact)
            common = 1
            for w in weights:
                common = common * w.denominator // math.gcd(common, w.denominator)
            scaled = [int(w * common) for w in weights]
            counts[choose(rungs(scaled, wheel), u_index)] += 1
        return counts

    counts = clicks(N, N, False, False)
    wall = tuple(counts[i] for i, (name, _) in enumerate(order) if name.startswith("wall"))
    screen = {
        int(name.split("_")[1]): counts[i]
        for i, (name, _) in enumerate(order)
        if name.startswith("screen") and counts[i]
    }
    faces = tuple(counts[i] for i, (name, _) in enumerate(order) if name.startswith("face"))
    print(
        f"  wall {sum(wall)} {wall}, screen {sum(screen.values())} {screen}, faces {sum(faces)} {faces}"
    )
    print(
        f"  the register: wall {sum(REGISTERED_WALL)} {REGISTERED_WALL}, screen {sum(REGISTERED_SCREEN.values())} {REGISTERED_SCREEN}, faces {sum(REGISTERED_FACES)} {REGISTERED_FACES}"
    )
    print(
        f"  reproduced: {wall == REGISTERED_WALL and screen == REGISTERED_SCREEN and faces == REGISTERED_FACES}"
    )
    weights0 = cell_weights(0, False)
    total0 = sum(weights0)
    print(
        f"  the record's total {float(total0):.4f} of the birth norm; shares wall {float(sum(weights0[:3]) / total0):.3f}, screen {float(sum(weights0[3 : 3 + HEIGHT]) / total0):.3f}, faces {float(sum(weights0[3 + HEIGHT :]) / total0):.3f}"
    )
    screen_w = sorted(
        ((float(w / total0), i - 3) for i, w in enumerate(weights0[3 : 3 + HEIGHT], start=3) if w),
        reverse=True,
    )
    print(
        f"  the rung 1 / 2N = {1 / (2 * N):.5f} of the total; the largest screen cell {screen_w[0][0]:.5f} at y = {screen_w[0][1]}; screen cells above the rung: {sum(1 for w, _ in screen_w if w >= 1 / (2 * N))} of {len(screen_w)}"
    )
    lists = {
        tuple(clicks_u)
        for clicks_u in (
            [choose(rungs([int(w * 65536 * 455) for w in cell_weights(u, False)], N), u)]
            for u in range(N)
        )
    }
    print(
        f"  cells landed over the 64 births: {len(lists)} distinct; every later birth repeats them (u = ordinal mod 64, the offers the same for every record)"
    )

    # 5. The ladder under the finer wheel and the exact phase: the pinned prediction.
    print(
        "\n5. THE CLICKS UNDER A FINER WHEEL (u the bit-reversed ordinal on a wheel W) AND THE EXACT PHASE"
    )
    for exact in (False, True):
        for wheel, births in ((64, 64), (4096, 256), (4096, 4096)):
            counts = clicks(wheel, births, exact, wheel > N)
            screen_counts = [counts[3 + y] for y in range(HEIGHT)]
            wall = sum(counts[:3])
            faces = sum(counts[3 + HEIGHT :])
            hit = sum(1 for c in screen_counts if c)
            two_hits = [screen_counts[y] for y in two]
            single = [screen_counts[y] for y in ys if len(screen_rows[y]) == 1]
            label = "exact" if exact else "built"
            print(
                f"  {label} phase, W = {wheel}, {births} births: wall {wall}, screen {sum(screen_counts)} on {hit} pixels, faces {faces}; two-path pixels {two_hits}; single-path pixels min {min(single)} max {max(single)}"
            )
            if births == 4096:
                cos_two = [cosine(y) for y in two]
                print(
                    f"    Pearson(two-path counts, cosine) {pearson(two_hits, cos_two):.3f}; visibility over the two-path pixels (max - min) / (max + min) = {(max(two_hits) - min(two_hits)) / (max(two_hits) + min(two_hits)):.3f}"
                )
                print(
                    f"    screen counts y = 40 .. 80: {' '.join(str(screen_counts[y]) for y in range(40, 81))}"
                )

    # 6. The screen's fan: one direction per pixel from each opening (the
    # lattice's Huygens re-emission toward every Node of the screen), the
    # same law, the same click; the fringes under both phase forms.
    print(
        "\n6. THE SCREEN'S FAN: (44, y - opening) per pixel from each opening, 121 directions, multiplicity 5 x 121 = 605"
    )
    print(
        f"  the isotropy of the flight table on these directions: T_d / (Q sqrt 3 |D|) over the 121 directions within "
        f"{max(abs(resolution((44, y - 55)) / (Q * math.sqrt(3) * math.hypot(44, y - 55)) - 1) for y in range(HEIGHT)):.5f} of 1"
    )
    fringe_rows = {}
    for o, opening in enumerate(OPENINGS):
        for y in range(HEIGHT):
            vector = (SCREEN_X - opening[0], y - opening[1])
            end, node, age, made = walk(opening, vector, stop_fan)
            assert end == "screen"
            s1, t = sum(map(abs, vector)), resolution(vector)
            builtp = (leg_phase[opening] + phase_by_clock(age, n, d)) % N
            exactp = (leg_exact[opening] + exact_phase(made, s1, t, n, d)) % N
            fringe_rows.setdefault(node[1], []).append((o, vector, end, node, age, builtp, exactp))
    ys_all = list(range(HEIGHT))
    own = sum(1 for y in ys_all for r in fringe_rows.get(y, []) if r[1][1] + OPENINGS[r[0]][1] == y)
    print(
        f"  directions landing on their own pixel {own} of 242 (the others enter x = 52 one Node short, the digital line's last step in y); pixels with two rows {sum(1 for y in ys_all if len(fringe_rows.get(y, [])) == 2)}, with one {sum(1 for y in ys_all if len(fringe_rows.get(y, [])) == 1)}, with none {sum(1 for y in ys_all if not fringe_rows.get(y))}"
    )
    for y in ys_all:
        fringe_rows.setdefault(y, [])
    built_f = [weight_built(fringe_rows[y], 0) / 65536 for y in ys_all]
    exact_f = [weight_exact(fringe_rows[y], 0, 4096) for y in ys_all]
    exact_f64 = [weight_exact(fringe_rows[y], 0, 64) for y in ys_all]
    cos_f = [cosine(y) for y in ys_all]
    print(
        f"  Pearson with the Euclidean two-source cosine over the 121 pixels: built phase {pearson(built_f, cos_f):.3f}, exact phase on the table of 64 {pearson(exact_f64, cos_f):.3f}, exact on 4096 {pearson(exact_f, cos_f):.3f}"
    )
    err = sorted(
        abs(float(((r[1][6] - r[0][6]) - (r[1][5] - r[0][5]) + N / 2) % N - N / 2))
        for r in fringe_rows.values()
        if len(r) == 2
    )
    print(
        f"  the built difference against the exact difference per pixel: at most {err[-1]:.2f} steps, median {err[len(err) // 2]:.2f} (one interval = 8 steps)"
    )
    print("  weights x 605 per pixel, y = 40 .. 80 (built / exact / 2 (1 + cos)):")
    print("    built " + " ".join(f"{built_f[y]:.1f}" for y in range(40, 81)))
    print("    exact " + " ".join(f"{exact_f[y]:.1f}" for y in range(40, 81)))
    print("    cos   " + " ".join(f"{2 * cos_f[y]:.1f}" for y in range(40, 81)))
    order_f = [o for o in order if o[0].startswith("wall")] + [
        (f"screen_{y}", [[(r[5], r[6]) for r in fringe_rows[y]]] if fringe_rows[y] else [])
        for y in ys_all
    ]

    def cell_weights_f(u: int, exact: bool) -> list[Fraction]:
        found = []
        for name, groups in order_f:
            m = 5 if name.startswith("wall") else 605
            total = Fraction(0)
            for group in groups:
                if exact:
                    z = 0j
                    for _, ph in group:
                        p = math.floor((ph + u) * 4096 / N) % 4096
                        z += complex(math.cos(2 * math.pi * p / 4096), math.sin(2 * math.pi * p / 4096))
                    total += Fraction(round(abs(z) ** 2 * 65536)) / (65536 * m)
                else:
                    x = sum(COS[(ph + u) % N] for ph, _ in group)
                    sn = sum(SIN[(ph + u) % N] for ph, _ in group)
                    total += Fraction(x * x + sn * sn, 65536 * m)
            found.append(total)
        return found

    for exact in (False, True):
        for wheel, births in ((64, 64), (4096, 4096)):
            counts = [0] * len(order_f)
            for b in range(births):
                u_index = bit_reverse(b % wheel, wheel.bit_length() - 1) if wheel > N else b % wheel
                u = u_index * N // wheel if wheel >= N else u_index
                weights = cell_weights_f(u % N, exact)
                common = 1
                for w in weights:
                    common = common * w.denominator // math.gcd(common, w.denominator)
                counts[choose(rungs([int(w * common) for w in weights], wheel), u_index)] += 1
            screen_counts = counts[3:]
            label = "exact" if exact else "built"
            hit = sum(1 for c in screen_counts if c)
            print(
                f"  {label} phase, W = {wheel}, {births} births: wall {sum(counts[:3])}, screen {sum(screen_counts)} on {hit} pixels; Pearson(counts, cosine) {pearson(screen_counts, cos_f):.3f}"
            )
            if births == 4096:
                print(
                    f"    counts y = 40 .. 80: {' '.join(str(screen_counts[y]) for y in range(40, 81))}"
                )
                bright = [y for y in ys_all if cos_f[y] > 1.9]
                dark = [y for y in ys_all if cos_f[y] < 0.1]
                print(
                    f"    at the cosine's bright pixels {bright}: {[screen_counts[y] for y in bright]}; at its dark pixels {dark}: {[screen_counts[y] for y in dark]}"
                )

    # 7. The register's 0.368: the reading tool's cosine at the isotropic pace 1 / sqrt 3.
    wl = 8 / math.sqrt(3)
    cos_iso = [
        1 + math.cos(2 * math.pi * (math.hypot(44, y - 55) - math.hypot(44, y - 65)) / wl) for y in ys
    ]
    print(
        f"\n7. The cosine at the isotropic pace 1 / sqrt 3 (wavelength {wl:.4f}): built vs cosine over the 75 pixels {pearson(built, cos_iso):.3f} (the register's 0.368 is the reading tool's own cosine; the number here is this map's)"
    )


if __name__ == "__main__":
    main()
