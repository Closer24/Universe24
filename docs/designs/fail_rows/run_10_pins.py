"""The pins of row 10 (the single opening under the one click) before any
run, from the declared worlds `opening_w27.json` and `opening_w9.json`
beside this file (docs/designs/fail_rows/RUN_10.md, section 3; STEP 1: no
run, no engine line).

The register's own algebra on the loaded worlds: the lamp's rows walked
by the flight table (the closed form m(tau) = (2 tau S_1 Q + T_d) // (2
T_d) on the engine's digital line, `docs/designs/fraction_free/
two_slits_map.py`), the leg's whole phase (the sum of `by_clock` over the
intervals of age) plus the lamp's declared turn, zero mod N at every
opening Node (the plane front); the fan rows re-emitted at every opening
Node on the declared directions with the equal split, each read at its
end (a screen pixel or a face) at the exact phase of BEAM_LAW note 45
(one floor at the click, floor(n made T_d / (d S_1 Q)), on the tables of
N = 64); the record's weight per cell by the click's bilinear form (the
sum per Node of |sum amount x (C, S)[phase]|^2, the pointer's square);
the records' cells by the engine's own `rungs` and `cell_of`
(`event_universe.events.amplitude`) on the golden wheel u = ordinal x 2531
mod 4096 with the rows' birth phase u mod 64. Nothing here runs the
engine; the tables and the ladder are imported so that the integers are
the click's. The same machinery, on `slits_huygens`, reproduced the
registered run of 2026-09-21 bit for bit (`docs/designs/paper_criteria/
slits_huygens_pin.py`).

What it derives, per world: (1) the world's constants (the phase per
interval, the period, the pace on the axis, the wavelength in Links, the
Fresnel number); (2) the legs (direction, Node, age, whole phase, turn,
the sum 0); (3) the fan (the directions, the ends, no blocked row); (4)
the first record's weights (u = 0): the shares screen / faces, the
screen profile, its full width at half maximum in s = sin theta and the
product w x FWHM / lambda; (5) THE PIN: the clicks of the records 1 to
4096 per cell (deterministic: the same 4096 u on the same 64 ladders),
the screen counts per pixel, their FWHM in s and the product; beside it,
as computations of the continuum for the same w and lambda, the
Fraunhofer array factor's product (0.886 in the far field) and the
Euclidean exact sum over the w emitters at L on the 161 pixels (DERIVATIONS_
BEAM 22.2's 0.916 at w = 27). Every number printed is a computation,
labelled so; the run at head compares its DETECTOR counts with (5).

Run from the repository root with PYTHONPATH=src:

    python docs/designs/fail_rows/run_10_pins.py > docs/designs/fail_rows/run_10_pins.out
"""

from __future__ import annotations

import cmath
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "docs" / "designs" / "fraction_free"))

from two_slits_map import bresenham, manhattan_steps, resolution  # noqa: E402

from event_universe.core.integer import by_clock  # noqa: E402
from event_universe.core.phase import phase_cosines, phase_sines  # noqa: E402
from event_universe.events.amplitude import cell_of, rungs  # noqa: E402

Q = 64  # the label's scale, the flight table's
SCALE = 32  # AMPLITUDE_SCALE: cancels in every ratio, kept so the numerators are the click's
WORLDS = ("opening_w27", "opening_w9")
RECORDS = 4096  # the pin's records: one full turn of the golden wheel
FAR_FIELD = 0.886  # the Fraunhofer constant (NATURE row 10; DERIVATIONS_BEAM 22.2)
NEAR_FIELD_W27 = 0.916  # 22.2's exact Euclidean sum at w = 27, L = 108
PIN_W27 = (0.92, 0.03)  # 22.2's pin at w = 27 under the one click
PIN_W9 = (0.886, 0.03)  # 22.2's pin at w = 9
REFUTES_BELOW = 0.85  # 22.2: a product below 0.85 at any width at or above lambda refutes


def phase_whole(age: int, n: int, d: int) -> int:
    """The phase column after `age` intervals of the pair form: the sum of
    `by_clock` over the intervals (floor(age n / d)), the whole part."""
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


def fwhm_in_s(profile: list[float], centre: int, distance: int) -> tuple[float, int, float, float]:
    """The full width at half maximum of a screen profile in s = sin theta
    (the pixel y at the angle theta with tan theta = (y - centre) / L),
    the half-maximum crossings interpolated linearly between pixels:
    (the width, the peak pixel, the left crossing, the right crossing)."""
    s = [(y - centre) / math.hypot(distance, y - centre) for y in range(len(profile))]
    peak = max(range(len(profile)), key=lambda y: (profile[y], -abs(y - centre)))
    half = profile[peak] / 2
    i = peak
    while i > 0 and profile[i] >= half:
        i -= 1
    left = s[i] + (half - profile[i]) * (s[i + 1] - s[i]) / (profile[i + 1] - profile[i])
    j = peak
    while j < len(profile) - 1 and profile[j] >= half:
        j += 1
    right = s[j - 1] + (profile[j - 1] - half) * (s[j] - s[j - 1]) / (profile[j - 1] - profile[j])
    return right - left, peak, left, right


def array_factor_product(w: int, wavelength: float) -> float:
    """The Fraunhofer array factor [sin(pi w s / lambda) / (w sin(pi s /
    lambda))]^2 of w emitters one Link apart: its FWHM in s times w /
    lambda, found on a fine grid of s (the far-field limit, 0.886 for w
    well above lambda)."""
    grain = 1e-5
    s = 0.0
    while True:
        s += grain
        value = (math.sin(math.pi * w * s / wavelength) / (w * math.sin(math.pi * s / wavelength))) ** 2
        if value <= 0.5:
            return 2 * s * w / wavelength


def euclidean_sum_product(
    w: int, wavelength: float, distance: int, height: int, centre: int
) -> tuple[float, list[float]]:
    """The exact Euclidean sum over the w emitters at (0, centre + j) read
    at the distance L on the `height` pixels, |sum_j exp(2 pi i r_j /
    lambda)|^2 (22.2's (C), the near field at this Fresnel number): the
    product w x FWHM / lambda and the profile."""
    half = w // 2
    profile = []
    for y in range(height):
        total = sum(
            cmath.exp(2j * math.pi * math.hypot(distance, y - centre - j) / wavelength)
            for j in range(-half, half + 1)
        )
        profile.append(abs(total) ** 2)
    width, _, _, _ = fwhm_in_s(profile, centre, distance)
    return width * w / wavelength, profile


def pin_world(path: Path) -> None:
    name = path.stem
    world = json.loads(path.read_text())
    n_steps = world["N"]
    cos, sin = phase_cosines(n_steps), phase_sines(n_steps)
    light = next(f for f in world["families"] if f["name"] == "light")
    n, d = light["phase_per_link"]
    lamp = next(m for m in world["measured"] if "lamp" in m)
    lamp_at = (lamp["position"][0], lamp["position"][1])
    lamp_dirs = [(v[0], v[1]) for v in lamp["lamp"]["directions"]]
    lamp_turns = lamp["lamp"]["turns"]
    wheel = lamp["lamp"]["wheel"]
    rate = lamp["lamp"]["rate"]
    width_x, height, _ = world["shape"]
    openings: dict[tuple[int, int], list[tuple[int, int]]] = {}
    walls: dict[tuple[int, int], int] = {}
    for number, m in enumerate(world["measured"]):
        if "lamp" in m:
            continue
        node = (m["position"][0], m["position"][1])
        if "table" in m:
            assert m["table"] == {"light": "rerelease"}, m["table"]
            openings[node] = [(v[0], v[1]) for v in m["directions"]]
        else:
            walls[node] = number
    wall_x = min(x for x, _ in openings)
    screen_x = max(x for x, _ in walls)
    screen = {(screen_x, y): f"screen_{y}" for y in range(height)}
    assert all(det["positions"] == [[screen_x, y, 0]] for y, det in enumerate(world["detectors"]))
    assert all(det["reading"] == "sum" for det in world["detectors"])
    w = len(openings)
    centre = sum(y for _, y in openings) // w
    distance = screen_x - wall_x
    fan = next(iter(openings.values()))
    assert all(v == fan for v in openings.values())

    # 1. The world's constants (COMPUTATION from the declared integers).
    period = Fraction(n_steps * d, n)  # intervals per turn of the circle
    t_axis = resolution((1, 0))
    pace_axis = Fraction(Q, t_axis)  # Links per interval on the axis
    wavelength = float(period * pace_axis)
    fresnel = w * w / (wavelength * distance)
    ways = len(lamp_dirs)
    norm = len(fan)
    print(
        f"{name}: w = {w} Nodes at x = {wall_x}, y = {centre - w // 2} .. {centre + w // 2}; the screen at x = {screen_x},"
        f" L = {distance} Links, {height} pixels; N = {n_steps}; phase_per_link {n} / {d} = {n / d:.6f} steps per interval,"
        f" the period {float(period):.5f} intervals; the pace on the axis S_1 Q / T_(1,0) = {Q} / {t_axis} = {float(pace_axis):.5f}"
        f" Links per interval; lambda = {wavelength:.4f} Links (22.2: 8 c = 4.655); the Fresnel number w^2 / (lambda L) = {fresnel:.3f};"
        f" the lamp at {lamp_at} on {ways} directions with turns, the rate {rate}, the wheel {wheel};"
        f" the fan {norm} directions per opening Node, the equal split (norm {norm}); the record's multiplicity {ways} x {norm} = {ways * norm}"
    )

    # 2. The legs: every lamp row lands on its opening Node in phase.
    def stop_lamp(node):
        if node in openings:
            return "opening"
        if node in walls:
            return "wall"
        return None

    print("\nTHE LEGS (GAMEBOARD, the flight table; the phases COMPUTATION on the tables):")
    reached = {}
    for v, turn in zip(lamp_dirs, lamp_turns, strict=True):
        end, node, age, made = walk(lamp_at, v, stop_lamp)
        assert end == "opening", (v, end, node)
        leg = phase_whole(age, n, d)
        total = (leg + turn) % n_steps
        assert total == 0, (v, leg, turn)
        assert node not in reached
        reached[node] = v
        print(
            f"  the row on {v} reaches {node} at the age {age} after {made} Links, the leg's whole phase {leg}"
            f" ({leg % n_steps} mod {n_steps}), the turn {turn}: the phase at the opening {total} + u"
        )
    assert set(reached) == set(openings)
    print(
        f"  every opening Node reached by exactly one row: {len(reached)} of {w}; the front at the phase u on every one"
    )

    # 3. The fan: every re-emitted row's end and exact phase (u = 0).
    def stop_fan(node):
        if node[1] < 0:
            return "face:-y"
        if node[1] >= height:
            return "face:+y"
        if node in screen:
            return "screen"
        if node in walls or node in openings:
            return "blocked"
        if node[0] >= width_x:
            return "face:+x"
        return None

    rows: list[tuple[str, tuple[int, int], int]] = []
    blocked = 0
    angles = sorted(math.degrees(math.atan2(b, a)) for a, b in fan)
    grains = [b - a for a, b in zip(angles[:-1], angles[1:], strict=True)]
    for opening in sorted(openings):
        for v in fan:
            end, node, age, made = walk(opening, v, stop_fan)
            if end == "blocked":
                blocked += 1
                continue
            s1, t = sum(map(abs, v)), resolution(v)
            phi = exact_whole(made, s1, t, n, d) % n_steps
            rows.append((screen[node] if end == "screen" else end, node, phi))
    on_screen = sum(1 for r in rows if r[0].startswith("screen"))
    print(
        f"\nTHE FAN (COMPUTATION): {norm} directions from {angles[0]:.2f} to {angles[-1]:.2f} degrees, the grain"
        f" {min(grains):.3f} .. {max(grains):.3f} degrees (about {math.radians(max(grains)):.4f} in s at the axis;"
        f" 22.2's 47-direction fan 0.083); {len(rows)} rows per record, {on_screen} end on the screen,"
        f" {len(rows) - on_screen} on the faces, {blocked} blocked (expected 0)"
    )

    # The cells in the ladder's order (engine.py: the measured events
    # outside every declared detector by number, none with weight here,
    # then the declared detectors, then the faces in Port order).
    order = [f"screen_{y}" for y in range(height)] + ["face:+y", "face:-y"]
    assert {r[0] for r in rows} <= set(order), {r[0] for r in rows} - set(order)
    multiplicity = ways * norm
    by_cell: dict[str, dict[tuple[int, int], list[int]]] = {}
    for cell, node, phi in rows:
        by_cell.setdefault(cell, {}).setdefault(node, []).append(phi)

    def numerators(u: int) -> list[int]:
        found = []
        for cell in order:
            total = 0
            for phis in by_cell.get(cell, {}).values():
                x = sum(SCALE * cos[(phi + u) % n_steps] for phi in phis)
                y = sum(SCALE * sin[(phi + u) % n_steps] for phi in phis)
                total += x * x + y * y
            found.append(total)
        return found

    ladders = {}
    for u in range(n_steps):
        nums = numerators(u)
        pairs = [(v, multiplicity) for v in nums]
        ladders[u] = (pairs, rungs(pairs, wheel[1])[0])

    # 4. The first record (u = 0): the shares and the screen profile.
    pairs0, rungs0 = ladders[0]
    unit = SCALE * SCALE * 65536
    weights0 = [Fraction(v, m * unit) for v, m in pairs0]
    total0 = sum(weights0)
    screen_w = [float(weights0[y]) for y in range(height)]
    faces_w = float(weights0[height] + weights0[height + 1])
    width0, peak0, left0, right0 = fwhm_in_s(screen_w, centre, distance)
    product0 = width0 * w / wavelength
    print(
        f"\n4. THE FIRST RECORD (u = 0), a computation: the total {float(total0):.3f} of the birth norm;"
        f" the shares screen {sum(screen_w) / float(total0):.3f} / faces {faces_w / float(total0):.3f};"
        f" the peak at y = {peak0} with {screen_w[peak0] / float(total0):.4f} of the total; the half-maximum crossings"
        f" at s = {left0:.4f} and {right0:.4f}: FWHM(sin theta) = {width0:.4f}, w x FWHM / lambda = {product0:.3f}"
    )
    print(
        "   the screen weights y = "
        f"{centre - 20} .. {centre + 20} (per mille of the total): "
        + " ".join(f"{1000 * screen_w[y] / float(total0):.1f}" for y in range(centre - 20, centre + 21))
    )

    # 5. THE PIN: the clicks of the records 1 .. 4096 on the golden wheel.
    counts = [0] * len(order)
    for b in range(RECORDS):
        u = (b * wheel[0]) % wheel[1]
        pairs, _ = ladders[u % n_steps]
        k = cell_of(pairs, wheel[1], u)
        assert k is not None
        counts[k] += 1
    screen_counts = [counts[y] for y in range(height)]
    faces_counts = (counts[height], counts[height + 1])
    width, peak, left, right = fwhm_in_s([float(c) for c in screen_counts], centre, distance)
    product = width * w / wavelength
    expected0 = [rungs0[k] - (rungs0[k - 1] if k else 0) for k in range(len(order))]
    worst = max(abs(c - e) for c, e in zip(counts, expected0, strict=True))
    lit = [y for y in range(height) if screen_counts[y]]
    print(
        f"\n5. THE CLICKS OF THE RECORDS 1 .. {RECORDS} UNDER THE GOLDEN WHEEL, a computation of what the detectors read:"
        f" screen {sum(screen_counts)} on {len(lit)} pixels (y = {lit[0]} .. {lit[-1]}), faces {sum(faces_counts)} {faces_counts};"
        f" against the first record's rungs the worst cell off by {worst}"
    )
    print(f"   every screen pixel's count: {screen_counts}")
    print(
        f"   the peak at y = {peak} ({screen_counts[peak]} clicks); the half-maximum crossings at s = {left:.4f} and {right:.4f}:"
        f" FWHM(sin theta) = {width:.4f}; THE PIN w x FWHM / lambda = {product:.3f}"
    )

    # Beside it: the continuum for the same w and lambda.
    far = array_factor_product(w, wavelength)
    near, _ = euclidean_sum_product(w, wavelength, distance, height, centre)
    registered = PIN_W27 if w == 27 else PIN_W9
    print(
        f"\n   BESIDE IT (COMPUTATION, the continuum at this w and lambda): the Fraunhofer array factor's product {far:.3f}"
        f" (the far field, 22.2's {FAR_FIELD}); the Euclidean exact sum over the {w} emitters at L = {distance} on the {height} pixels"
        f" {near:.3f}"
        + (f" (22.2's {NEAR_FIELD_W27})" if w == 27 else "")
        + f"; 22.2's pin for this width {registered[0]} +- {registered[1]};"
        f" the pixel's grain in s at the axis 1 / L = {1 / distance:.4f}, {100 / distance / width:.0f} percent of the FWHM"
    )
    inside = abs(product - registered[0]) <= registered[1]
    print(
        f"   the clicks' product against 22.2's pin: {'inside' if inside else 'OUTSIDE'} the band"
        f" ({product:.3f} against {registered[0]} +- {registered[1]}); against the refuting bound {REFUTES_BELOW}: "
        + ("above" if product >= REFUTES_BELOW else "BELOW")
    )
    print(
        "   THE PIN FOR THIS WORLD (the algebra's, before the run at head): the counts per cell as printed, bit for bit"
        f" (the same {RECORDS} u on the same {n_steps} ladders), and from them w x FWHM(sin theta) / lambda = {product:.3f};"
        " a differing count refutes the chain of section 1 of RUN_10.md, and no number moves to it."
    )


def main() -> None:
    for name in WORLDS:
        pin_world(HERE / f"{name}.json")
        print()


if __name__ == "__main__":
    main()
