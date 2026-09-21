"""Section 20 of DERIVATIONS_BEAM.md: the periodic universe against the
measured numbers. Host arithmetic; no run.

(A) A periodic GameBoard under the growing wall (section 15's world:
    the box L = 301 Links, H = 1 / 400 per interval, the tick wall):
    the causal reach (c_0 / H) ln(1 + H t), the windings inside it, the
    images of one lamp and their redshifts z = exp(H n L / c_0) - 1.
(B) Nature's bounds on a torus: the last-scattering diameter and the
    matched-circle bound on the fundamental domain (Planck 2015 XVIII:
    R_i > 0.97 chi_rec for a flat torus, so L > 1.94 chi_rec).
(C) Section 19.3's note: the mean square charge radius of the quarks
    design's three shapes (the line, the corner, the face-diagonal
    triangle) about the charge centroid.
"""

from __future__ import annotations

import math
from pathlib import Path

C0 = 1 / math.sqrt(3)
H = 1 / 400
BOX = 301
CHI_REC = 14.0  # Gpc comoving, the radius of the last-scattering surface


def reach(t: float) -> float:
    return (C0 / H) * math.log(1 + H * t)


def images_within(radius: float) -> int:
    n = int(radius // BOX)
    count = 0
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            for k in range(-n, n + 1):
                if (i, j, k) != (0, 0, 0) and BOX * math.sqrt(i * i + j * j + k * k) <= radius:
                    count += 1
    return count


def radius2(charges: list[float], points: list[tuple[float, ...]]) -> float:
    total = sum(charges)
    dims = len(points[0])
    if abs(total) > 1e-12:
        centre = [
            sum(q * p[a] for q, p in zip(charges, points, strict=True)) / total for a in range(dims)
        ]
    else:
        centre = [sum(p[a] for p in points) / len(points) for a in range(dims)]
    return sum(
        q * sum((p[a] - centre[a]) ** 2 for a in range(dims))
        for q, p in zip(charges, points, strict=True)
    )


def main() -> None:
    out = [
        "(A) The periodic board under the growing wall: L = 301, H = 1 / 400, the Hubble length c_0 / H = 233 Links"
    ]
    for t in (1000, 3000, 10000, 100000):
        r = reach(t)
        out.append(
            f"  t = {t}: the reach {r:.0f} Links = {r / BOX:.2f} boxes, images of one lamp inside it {images_within(r)}"
        )
    out.append("  the redshift of the n-th image along an axis, z = exp(H n L / c_0) - 1:")
    for n in (1, 2, 3):
        out.append(f"    n = {n}: z = {math.exp(H * n * BOX / C0) - 1:.2f}")
    out.append(
        f"  the reach saturates at (c_0 / H) ln(1 + H t): {reach(1e6):.0f} Links at t = 10^6, {reach(1e9):.0f} at 10^9"
    )

    out.append("")
    out.append("(B) Nature's bounds on a cubic torus")
    out.append(f"  the last-scattering diameter 2 chi_rec = {2 * CHI_REC:.0f} Gpc comoving")
    out.append(
        f"  matched circles, Planck 2015 XVIII: R_i > 0.97 chi_rec, so the box L > {2 * 0.97 * CHI_REC:.1f} Gpc = {0.97:.2f} of the diameter"
    )
    out.append(
        "  Cornish, Spergel, Starkman and Komatsu 2004: no matched circles, the box beyond 24 Gpc"
    )
    out.append(
        f"  the last-scattering volume over the box's at the bound: (1 / 0.97)^3 = {(0.97) ** -3:.2f}: "
        "the first image at or beyond the surface"
    )

    out.append("")
    out.append(
        "(C) The quarks design's three shapes: the mean square charge radius about the charge centroid (Link^2)"
    )
    line = [(-1.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 0.0, 0.0)]
    corner = [(1.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0)]
    triangle = [(1.0, 1.0, 0.0), (0.0, 1.0, 1.0), (1.0, 0.0, 1.0)]
    for shape, pts in (("line", line), ("corner", corner), ("triangle", triangle)):
        for name, q in (
            ("u d u / d at the centre", [2 / 3, -1 / 3, 2 / 3]),
            ("d u d / u at the centre", [-1 / 3, 2 / 3, -1 / 3]),
            ("u u d / d at an end", [2 / 3, 2 / 3, -1 / 3]),
            ("d d u / u at an end", [-1 / 3, -1 / 3, 2 / 3]),
        ):
            out.append(f"  {shape:<9} {name:<26} r^2 = {radius2(q, pts):+.4f}")
    Path(__file__).with_suffix(".out").write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
