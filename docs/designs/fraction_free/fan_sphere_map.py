"""The 3D integer form of the fan law on the register's 290-direction fan
(read-only, the mathematician, 2026-09-21; TWO_SLITS.md section 10). The
fan is F_6 in space, every primitive (a, b, c) with |a| + |b| + |c| <= 6.
Every direction's weight is the measure of its Voronoi cell on the sphere
of directions: the cell's vertices are the circumcentres of D with its
Delaunay neighbours, the vectors c = (D1 x D2) |D3| + (D2 x D3) |D1| +
(D3 x D1) |D2| at the grain G (integer exactly, as D1 x D2 + D2 x D3 +
D3 x D1, only for three directions of equal length: the plane through
three UNIT points is not the plane through the integer points), the
Delaunay triangles from the convex hull of the unit points, and the cell's area is
the sum of the solid angles of the triangles (D, c_i, c_i+1) by Van
Oosterom-Strackee, tan(Omega / 2) = |a . (b x c)| / (|a| |b| |c| + (a . b)
|c| + (a . c) |b| + (b . c) |a|), with the lengths at the grain G by isqrt
and tan x = x at the triangles' small angles (the same approximation the
plane form makes, arcsin x = x). The integer weight is the floor of the
cell's area at the grain G_w. The map gives the 290 weights by direction
class, their sum, the max / min ratio, the exact equality within each
class under the 48 symmetries, the agreement with the exact spherical
areas and with a fine sphere sample, and the check that the plane form
3 Q^2 / (T_d T_d') is the restriction of the 3D form to the great circle
z = 0.

Run from the repository root:

    python docs/designs/fraction_free/fan_sphere_map.py > docs/designs/fraction_free/fan_sphere_map.out
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

P = 6
Q = 64
G = (
    1 << 5
)  # the grain of the lengths (isqrt) in the area formula; with the vectors at the scale S every load-time product stays within 2^62
SCALE = (
    1 << 14
)  # every vector of a triangle is brought to the length S = 2^14 before the area formula (the formula is homogeneous)
G_W = 1 << 15  # the grain of the weights (steradians x G_W)
G_C = (
    1 << 24
)  # the grain of the lengths inside the circumcentre: the three cross products nearly cancel on a small triangle, so the vertex needs the lengths to 2^-24 (a load-time host integer, at most 2^30)

Vec = tuple[int, int, int]


def cross(a: Vec, b: Vec) -> Vec:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def dot(a: Vec, b: Vec) -> int:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def add(a: Vec, b: Vec) -> Vec:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def reduce(v: Vec) -> Vec:
    g = math.gcd(math.gcd(abs(v[0]), abs(v[1])), abs(v[2]))
    return (v[0] // g, v[1] // g, v[2] // g)


def fan_of(width: int) -> list[Vec]:
    return [
        (a, b, c)
        for a in range(-width, width + 1)
        for b in range(-width, width + 1)
        for c in range(-width, width + 1)
        if (a, b, c) != (0, 0, 0)
        and abs(a) + abs(b) + abs(c) <= width
        and math.gcd(math.gcd(abs(a), abs(b)), abs(c)) == 1
    ]


def length(v: Vec) -> int:
    """G |v| rounded down, in integers."""
    return math.isqrt(G * G * dot(v, v))


def scaled(v: Vec) -> Vec:
    """v brought to the length S = 2^14 by one isqrt, each component rounded
    to the nearest integer symmetrically (the same rounding under every
    sign flip and permutation, so the 48 symmetries hold exactly)."""
    norm = math.isqrt(dot(v, v))
    out = []
    for x in v:
        q = (2 * abs(x) * SCALE + norm) // (2 * norm)
        out.append(q if x >= 0 else -q)
    return (out[0], out[1], out[2])


def solid_angle_integer(a: Vec, b: Vec, c: Vec) -> Fraction:
    """The triangle's solid angle by Van Oosterom-Strackee with the lengths
    at the grain G and tan x = x: 2 G^3 |a . (b x c)| / den, a rational."""
    a, b, c = scaled(a), scaled(b), scaled(c)
    numerator = abs(dot(a, cross(b, c)))
    la, lb, lc = length(a), length(b), length(c)
    den = la * lb * lc + G * G * (dot(a, b) * lc + dot(a, c) * lb + dot(b, c) * la)
    return Fraction(2 * G**3 * numerator, den)


def exact_area(d: Vec, centres: list[np.ndarray]) -> float:
    """The cell's exact area: the unit circumcentres in angular order
    around D, the sum of the triangles' solid angles (Van Oosterom-Strackee
    in floating point, the reference the integer form is checked against)."""
    fd = np.array(d, float)
    fd /= np.linalg.norm(fd)
    axis = np.array([1.0, 0, 0]) if abs(fd[0]) < 0.9 else np.array([0, 1.0, 0])
    e1 = np.cross(fd, axis)
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(fd, e1)
    ring = sorted(centres, key=lambda c: math.atan2(np.dot(c, e2), np.dot(c, e1)))
    total = 0.0
    for i, b in enumerate(ring):
        c = ring[(i + 1) % len(ring)]
        num = abs(np.dot(fd, np.cross(b, c)))
        den = 1 + np.dot(fd, b) + np.dot(fd, c) + np.dot(b, c)
        total += 2 * math.atan2(num, den)
    return total


def circumcentre(d1: Vec, d2: Vec, d3: Vec) -> Vec:
    """The circumcentre on the sphere of three directions, as an integer
    vector at the grain G: the normal of the plane through the three UNIT
    points, (u1 x u2 + u2 x u3 + u3 x u1) x |D1| |D2| |D3| = (D1 x D2) |D3|
    + (D2 x D3) |D1| + (D3 x D1) |D2|, the lengths by isqrt at G (exact,
    with the plain sum of cross products, only when the three lengths are
    equal); oriented toward D1."""

    def l_c(v: Vec) -> int:
        return math.isqrt(G_C * G_C * dot(v, v))

    parts = (
        tuple(x * l_c(d3) for x in cross(d1, d2)),
        tuple(x * l_c(d1) for x in cross(d2, d3)),
        tuple(x * l_c(d2) for x in cross(d3, d1)),
    )
    centre: Vec = add(add(parts[0], parts[1]), parts[2])  # type: ignore[arg-type]
    if dot(centre, d1) < 0:
        centre = (-centre[0], -centre[1], -centre[2])
    return reduce(centre) if centre != (0, 0, 0) else centre


def exact_circumcentre(d1: Vec, d2: Vec, d3: Vec) -> np.ndarray:
    u = [np.array(v, float) / np.linalg.norm(v) for v in (d1, d2, d3)]
    n = np.cross(u[0], u[1]) + np.cross(u[1], u[2]) + np.cross(u[2], u[0])
    if np.dot(n, u[0]) < 0:
        n = -n
    return n / np.linalg.norm(n)


EXACT: dict[Vec, list[np.ndarray]] = {}


def voronoi_vertices(fan: list[Vec]) -> dict[Vec, list[Vec]]:
    """The cell vertices of every direction: the circumcentres of the
    Delaunay triangles at D (the faces of the convex hull of the unit
    points: for points on a sphere the hull is the Delaunay
    triangulation; a cocircular quadruple is split arbitrarily and its
    two triangles share one circumcentre, so the duplicates are dropped)."""
    from scipy.spatial import ConvexHull

    units = np.array(fan, float)
    units /= np.linalg.norm(units, axis=1)[:, None]
    hull = ConvexHull(units)
    vertices: dict[Vec, set[Vec]] = {v: set() for v in fan}
    for i, j, k in hull.simplices:
        d1, d2, d3 = fan[i], fan[j], fan[k]
        centre = circumcentre(d1, d2, d3)
        exact = exact_circumcentre(d1, d2, d3)
        for d in (d1, d2, d3):
            if centre not in vertices[d]:
                vertices[d].add(centre)
                EXACT.setdefault(d, []).append(exact)
    return {d: sorted(vs) for d, vs in vertices.items()}


def ordered(d: Vec, vs: list[Vec]) -> list[Vec]:
    """The cell's vertices in angular order around D (the order only)."""
    fd = np.array(d, float)
    fd /= np.linalg.norm(fd)
    axis = np.array([1.0, 0, 0]) if abs(fd[0]) < 0.9 else np.array([0, 1.0, 0])
    e1 = np.cross(fd, axis)
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(fd, e1)
    angles = []
    for v in vs:
        fv = np.array(v, float)
        angles.append(math.atan2(np.dot(fv, e2), np.dot(fv, e1)))
    return [v for _, v in sorted(zip(angles, vs, strict=True))]


def class_of(v: Vec) -> Vec:
    return tuple(sorted((abs(v[0]), abs(v[1]), abs(v[2])), reverse=True))  # type: ignore[return-value]


def main() -> None:
    fan = fan_of(P)
    print(
        f"F_{P} in space: {len(fan)} directions; the vectors at the scale S = 2^{SCALE.bit_length() - 1}, the grains G = 2^{G.bit_length() - 1} (lengths), G_C = 2^{G_C.bit_length() - 1} (the circumcentre), G_w = 2^{G_W.bit_length() - 1} (weights)"
    )
    vertices = voronoi_vertices(fan)
    counts = {len(vs) for vs in vertices.values()}
    print(
        f"cell vertices per direction: {sorted(counts)}; the vertex vectors' largest component {max(abs(c) for vs in vertices.values() for v in vs for c in v)}"
    )
    weights: dict[Vec, int] = {}
    area_int: dict[Vec, Fraction] = {}
    area_exact: dict[Vec, float] = {}
    for d, vs in vertices.items():
        ring = ordered(d, vs)
        total = Fraction(0)
        for i, c1 in enumerate(ring):
            c2 = ring[(i + 1) % len(ring)]
            total += solid_angle_integer(d, c1, c2)
        exact = exact_area(d, EXACT[d])
        area_int[d] = total
        area_exact[d] = exact
        weights[d] = int(total * G_W)
    sphere = sum(area_exact.values())
    print(
        f"the cells' exact areas sum to {sphere:.6f} sr (4 pi = {4 * math.pi:.6f}): the cells tile the sphere"
    )
    worst = max(abs(float(area_int[d]) / area_exact[d] - 1) for d in fan)
    print(
        f"the integer form against the exact spherical areas: within {worst:.2e} of 1 on every direction"
    )
    # By class.
    classes: dict[Vec, list[Vec]] = {}
    for d in fan:
        classes.setdefault(class_of(d), []).append(d)
    print(
        "\nclass | members | weight (integer, the same on every member) | share of the sum | x equal share | exact area (sr)"
    )
    total_w = sum(weights.values())
    symmetric = True
    for key in sorted(classes, key=lambda k: (sum(k), k)):
        members = classes[key]
        ws = {weights[d] for d in members}
        if len(ws) != 1:
            symmetric = False
        w = weights[members[0]]
        print(
            f"{key} | {len(members):2d} | {w:6d} | {w / total_w:.5f} | x{w * len(fan) / total_w:.2f} | {area_exact[members[0]]:.5f}"
        )
    wmin, wmax = min(weights.values()), max(weights.values())
    print(
        f"\nsum of the weights {total_w} (4 pi x G_w = {int(4 * math.pi * G_W)}); min {wmin} max {wmax}; max / min {wmax / wmin:.2f}"
    )
    print(
        f"A = sum of squares {sum(w * w for w in weights.values())} (2^{sum(w * w for w in weights.values()).bit_length()}); 2^31 = {1 << 31}: within the load-time ceiling for two re-emitters {sum(w * w for w in weights.values()) <= 1 << 31}"
    )
    print(f"equal weights within every class under the 48 symmetries: {symmetric}")
    longest = max(length(scaled(v)) for vs in vertices.values() for v in vs)
    den_max = 0
    num_max = 0
    for d0, vs in vertices.items():
        d = scaled(d0)
        for c1 in (scaled(v) for v in vs):
            for c2 in (scaled(v) for v in vs):
                if c1 == c2:
                    continue
                den = length(d) * length(c1) * length(c2) + G * G * (
                    dot(d, c1) * length(c2) + dot(d, c2) * length(c1) + dot(c1, c2) * length(d)
                )
                den_max = max(den_max, den)
                num_max = max(num_max, 2 * G**3 * abs(dot(d, cross(c1, c2))))
    print(
        f"the integer sizes at load: a length at most {longest} (2^{longest.bit_length()}), "
        f"a denominator at most 2^{den_max.bit_length()}, the numerator 2 G^3 |a . (b x c)| at most 2^{num_max.bit_length()}"
    )
    # The plane form as the restriction to the great circle z = 0.
    print(
        "\nthe great circle z = 0: the plane fan F_6, the angle between Farey neighbours by the 3D cross product against 3 Q^2 / (T_d T_d')"
    )
    plane = sorted([v for v in fan if v[2] == 0 and v[0] >= 1], key=lambda v: math.atan2(v[1], v[0]))

    def t_of(v: Vec) -> int:
        return math.isqrt(3 * dot(v, v) * Q * Q)

    worst_plane = 0.0
    for a, b in zip(plane, plane[1:], strict=False):
        cr = cross(a, b)
        assert abs(cr[2]) == 1, (a, b, cr)  # Farey neighbours
        exact_angle = math.asin(1 / math.sqrt(dot(a, a) * dot(b, b)))
        plane_form = 3 * Q * Q / (t_of(a) * t_of(b))
        three_d = math.atan2(math.sqrt(dot(cr, cr)), dot(a, b))
        assert abs(three_d - exact_angle) < 1e-12, (a, b)
        worst_plane = max(worst_plane, abs(plane_form / three_d - 1))
    print(
        f"  {len(plane)} directions on the half circle, {len(plane) - 1} Farey gaps; the 3D angle atan2(|D x D'|, D . D') equals the exact arcsin(1 / (|D| |D'|)) identically (|D x D'| = 1 in the plane), and the plane form 3 Q^2 / (T_d T_d') is within {worst_plane:.4f} of it (isqrt's rounding of T_d): the plane form is the 3D form's restriction"
    )
    # A fine sphere sample as the second check.
    M = 400000
    i = np.arange(M) + 0.5
    phi = np.arccos(1 - 2 * i / M)
    theta = math.pi * (1 + 5**0.5) * i
    pts = np.stack([np.cos(theta) * np.sin(phi), np.sin(theta) * np.sin(phi), np.cos(phi)], 1)
    units = np.array(fan, float)
    units /= np.linalg.norm(units, axis=1)[:, None]
    nearest = np.argmax(pts @ units.T, axis=1)
    share = np.bincount(nearest, minlength=len(fan)) / M
    worst_sample = max(abs(weights[d] / total_w - share[k]) / share[k] for k, d in enumerate(fan))
    print(
        f"\na sphere sample of {M} points: the integer weights' shares within {worst_sample:.3f} of the sampled cells (the sample's own noise)"
    )


if __name__ == "__main__":
    main()
