"""Write the worlds of the orbit series D under the law of the ray, on the
plane, with the width of the push.

Six worlds of one base (README.md here; the entry "D, the orbit under the
law of the ray, on the plane (2026-09-19)" in docs/EXPERIMENTS.md): a heavy
fixed source of a phase-less free family at the centre of a 121 x 121 x 1
board with the z axis periodic (the coupling series' plane), releasing a
ballistic fan of rays on every primitive in-plane direction (a, b, 0) with
0 < a^2 + b^2 <= P^2 (P = 8: the fan is uniform in angle, unlike the
primitive vectors of a square), one shell of `directions` rays every
1 / RATE intervals (content M = 2^10 at `release` [1, 2^10 x 10]: `by_clock`
gives one ray per direction at the ages 10, 20, ...), so the net emission
into the plane is q = directions x RATE units per interval; and a light
free probe of content 1 at radius r on +x with the tangential momentum
[0, p, 0] chosen for a circular orbit under the measured push law (the
derivation in README.md, written before the runs): with the push per
interval m x q x C / (2 pi r) toward the source (series C: flow x 2 pi r /
q = 1.00 +- 0.10, C = 1 taken) and the speed p / (S x m + p) per axis, a
circular orbit needs p^2 / (S m + p) = m q C / (2 pi), so with n = p / m

    n = (A + sqrt(A^2 + 4 S A)) / 2,  A = q C / (2 pi),

independent of r (a 1 / r force on the plane: the same speed at every
radius, T proportional to r, k = 2). The worlds: `s<S>_r<r>` for S in 1, 8,
32 and r in 12, 24, the momentum the nearest whole number to n (the grain
of the push: whole units of m per arriving unit of flow). `suspension` 0:
the clock's count is not read, the push law alone moves the probe.

    python examples/events/orbit/make_worlds.py
"""

from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIDE = 121
SHAPE = [SIDE, SIDE, 1]
BOUNDARY = {"z": "periodic"}
CENTRE = (60, 60, 0)
K = 1 << 22
N = 64
SOURCE = 1 << 10
# One shell of the fan every 10 intervals: `by_clock(age, SOURCE, RELEASE_D)`.
RELEASE_D = SOURCE * 10
RATE = SOURCE / RELEASE_D
FAN_RADIUS = 8
# Five expected periods of the slowest world (S = 32 at r = 24: 687), 4 s
# of host time per run at 1 ms per interval.
TICKS = 4000
WIDTHS = (1, 8, 32)
RADII = (12, 24)
# The tool's constant of the flow on the plane, flow x 2 pi r / q (series C).
FLOW_CONSTANT = 1.0
Json = dict[str, object]


def fan(radius: int) -> list[list[int]]:
    """Every primitive in-plane direction (a, b, 0) with 0 < a^2 + b^2 <=
    radius^2, in a fixed order (by angle from +x)."""
    found = []
    for a in range(-radius, radius + 1):
        for b in range(-radius, radius + 1):
            if (a or b) and a * a + b * b <= radius * radius and math.gcd(abs(a), abs(b)) == 1:
                found.append([a, b, 0])
    found.sort(key=lambda v: math.atan2(v[1], v[0]) % (2 * math.pi))
    return found


FAN = fan(FAN_RADIUS)
# The declared table beyond the six headings (the in-plane headings are the
# table's own entries 2 .. 5).
HEADINGS = {(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)}
DECLARED = [v for v in FAN if tuple(v) not in HEADINGS]
EMISSION = len(FAN) * RATE


def orbit_momentum(width: int) -> tuple[float, int]:
    """The circular-orbit momentum in units of the probe's content, from
    the derivation of the README: the real root and the nearest whole."""
    a = EMISSION * FLOW_CONSTANT / (2 * math.pi)
    n = (a + math.sqrt(a * a + 4 * width * a)) / 2
    return n, max(1, round(n))


def expected_period(width: int, radius: int) -> float:
    """2 pi r / v with v = n / (S + n) for the whole n."""
    _, n = orbit_momentum(width)
    return 2 * math.pi * radius * (width + n) / n


def world(width: int, radius: int) -> Json:
    _, n = orbit_momentum(width)
    return {
        "law": "rays",
        "model_id": f"rays-orbit-s{width}-r{radius}-plane-v1",
        "shape": list(SHAPE),
        "boundary": dict(BOUNDARY),
        "ticks": TICKS,
        "K": K,
        "N": N,
        "release": [1, RELEASE_D],
        "suspension": 0,
        "width": width,
        "directions": [list(v) for v in DECLARED],
        "families": [{"name": "m", "kind": "free", "charge": 0, "phase": False}],
        "measured": [
            {
                "position": list(CENTRE),
                "family": "m",
                "amount": SOURCE,
                "phase": 0,
                "fixed": True,
                "directions": [list(v) for v in FAN],
            },
            {
                "position": [CENTRE[0] + radius, CENTRE[1], CENTRE[2]],
                "family": "m",
                "amount": 1,
                "phase": 0,
                "fixed": False,
                "momentum": [0, n, 0],
            },
        ],
    }


def worlds() -> dict[str, Json]:
    return {f"s{width}_r{radius}": world(width, radius) for width in WIDTHS for radius in RADII}


def main() -> None:
    print(f"fan: {len(FAN)} directions ({len(DECLARED)} declared), q = {EMISSION:.2f} per interval")
    for width in WIDTHS:
        real, whole = orbit_momentum(width)
        speed = whole / (width + whole)
        periods = ", ".join(f"T({r}) = {expected_period(width, r):.0f}" for r in RADII)
        print(f"S = {width}: n = {real:.3f} -> p = {whole}, v = {speed:.3f} per axis, {periods}")
    for name, document in worlds().items():
        path = HERE / f"{name}.json"
        path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
        print(path.relative_to(HERE.parents[2]))


if __name__ == "__main__":
    main()
