"""The growing wall, the arithmetic (read-only, the derivation mathematician,
2026-09-21; DERIVATIONS_BEAM.md section 15): (1) the three integer forms of a
wall that grows (with the row's age, with its birth tick, with the tick) as
streams of rows on one Manhattan accumulator, the arrival spacing read as
1 + z; (2) the registered 25 stars of G2's `coasting_none` (their z read and
the light's age tau, the hubble_stars README) against the growing wall's
z = tau / (T - tau) at the README's T = 440 and at the registered fit
H (t_0 + T_0) = 1.026; (3) the presence of an eternal source in a periodic
world with and without the growing wall (Seeliger). No run.

Run from the repository root:

    python docs/designs/derivations_beam/growing_wall.py > docs/designs/derivations_beam/growing_wall.out
"""

from __future__ import annotations

import math

Q = 64
S1, T_D = 1, 110  # a heading: rate 2 S_1 Q, wall 2 T_D, c = Q / T_D = 32 / 55
H_NUM, H_DEN = 1, 400  # H = 1 / 400 per interval, a declared constant


def stream(form: str, distance: int, emitted: int = 400, horizon: int = 200000) -> list[int]:
    """Rows emitted one per interval from tick 0 on a heading; each carries its own Manhattan
    accumulator (started at T_D, rate 2 S_1 Q) against a wall 2 T_D a with a the growth factor of
    the form: 'age' (a = 1 + H age), 'birth' (a = 1 + H t_birth, fixed), 'tick' (a = 1 + H t).
    Returns the arrival ticks at the distance (in Links); the integers exact (a scaled by H_DEN)."""
    arrivals = []
    for birth in range(emitted):
        acc = T_D * H_DEN
        links = 0
        t = birth
        while links < distance and t < horizon:
            if form == "age":
                a_num = H_DEN + H_NUM * (t - birth)
            elif form == "birth":
                a_num = H_DEN + H_NUM * birth
            else:
                a_num = H_DEN + H_NUM * t
            acc += 2 * S1 * Q * H_DEN
            wall = 2 * T_D * a_num
            if acc >= wall:
                acc -= wall
                links += 1
            t += 1
        arrivals.append(t)
    return arrivals


print(
    "1. THE THREE FORMS OF THE GROWING WALL ON A STREAM (H = 1/400 per interval; rows one per interval; 1 + z = the arrival spacing)"
)
for form in ("age", "birth", "tick"):
    for d in (100, 300):
        arr = stream(form, d)
        spacing = (arr[-1] - arr[0]) / (len(arr) - 1)
        tau = arr[0]
        if form == "age":
            expected = 1.0
        elif form == "birth":
            expected = 1 + H_NUM / H_DEN * d * T_D / Q
        else:
            expected = math.exp(H_NUM / H_DEN * d * T_D / Q)
        print(
            f"  wall with the {form:5s}: distance {d} Links, first arrival at tick {tau}, spacing {spacing:.3f} (1 + z), the formula's {expected:.3f}"
        )
print(
    "  the age wall gives every row the same flight and no redshift; the birth wall gives z = H d / c_0, the tick wall 1 + z = a(t_r) / a(t_e) = e^(H d / c_0), the Milne form z = tau / (1 / H + t_r - tau)"
)

# 2. The registered stars: z read and tau (the hubble_stars README, coasting_none, the late window).
stars = [
    ("s_px1", 0.0573, 0.0611, 22.6),
    ("s_mx1", 0.0764, 0.0745, 30.0),
    ("s_py1", 0.0955, 0.0937, 37.1),
    ("s_my1", 0.1146, 0.1146, 44.1),
    ("s_pz1", 0.1337, 0.1353, 50.7),
    ("s_mz1", 0.1528, 0.1533, 57.1),
    ("s_px2", 0.1719, 0.1706, 63.4),
    ("s_mx2", 0.1910, 0.1905, 69.4),
    ("s_py2", 0.2101, 0.2102, 75.0),
    ("s_my2", 0.2292, 0.2264, 80.7),
    ("s_pz2", 0.2483, 0.2478, 86.2),
    ("s_mz2", 0.2674, 0.2636, 91.6),
    ("s_px3", 0.2865, 0.2857, 96.7),
    ("s_mx3", 0.3056, 0.3039, 101.7),
    ("s_py3", 0.3247, 0.3257, 106.7),
    ("s_my3", 0.3438, 0.3450, 111.3),
    ("s_pz3", 0.3628, 0.3654, 115.8),
    ("s_mz3", 0.3819, 0.3822, 120.6),
    ("s_px4", 0.4010, 0.3999, 124.7),
    ("s_mx4", 0.4201, 0.4179, 128.9),
    ("s_py4", 0.4392, 0.4368, 133.0),
    ("s_my4", 0.4583, 0.4583, 136.8),
    ("s_pz4", 0.4774, 0.4743, 140.9),
    ("s_mz4", 0.4965, 0.4922, 144.5),
]
print(
    "\n2. THE 24 THROWN STARS OF coasting_none AT REST UNDER THE GROWING TICK WALL: z = tau / (T - tau)"
)
for T in (440.0, 440.0 / 1.026):
    res = [z - tau / (T - tau) for _, _, z, tau in stars]
    rms = math.sqrt(sum(r * r for r in res) / len(res))
    worst = max(res, key=abs)
    print(
        f"  T = {T:.1f}: rms {rms:.4f}, worst {worst:+.4f} ({stars[[abs(r) for r in res].index(abs(worst))][0]}); the README's grain 0.003, its fit's rms 0.0019"
    )
# the birth-fixed wall's form, z = H tau / (1 + z)... against the same stars with the same H: z = tau / T
res = [z - tau / (440.0 / 1.026) for _, _, z, tau in stars]
print(
    f"  the birth wall's form z = H tau at the same H: rms {math.sqrt(sum(r * r for r in res) / len(res)):.4f}, worst {max(res, key=abs):+.4f}: refuted by the far stars"
)
print(
    "  the thrown coasting star's own relation: z = v / c and tau = v (T - tau) / c give z = tau / (T - tau), the same Milne form: the two models coincide in z(tau)"
)

# 3. Seeliger: the presence at a Node at the distance d0 from an eternal source in a periodic world of
# extent L, summed over the periodic images (k_x, k_y, k_z) within the light's reach.
print(
    "\n3. SEELIGER IN A PERIODIC WORLD (an eternal source of q rows per interval, a periodic cube of extent 301; the presence at 10 Links, summed over the periodic images the light has reached)"
)
c0 = Q / T_D
h = H_NUM / H_DEN
L = 301
for growing in (False, True):
    for t in (1000, 3000, 10000):
        reach = c0 * t if not growing else (c0 / h) * math.log(1 + h * t)
        kmax = int(reach / L) + 1
        total = 0.0
        images = 0
        for kx in range(-kmax, kmax + 1):
            for ky in range(-kmax, kmax + 1):
                for kz in range(-kmax, kmax + 1):
                    d = math.sqrt((10 + kx * L) ** 2 + (ky * L) ** 2 + (kz * L) ** 2)
                    if d > reach:
                        continue
                    flux = 1 / (4 * math.pi * d * d)
                    if growing:
                        flux *= math.exp(-h * d / c0)
                    total += flux
                    images += 1
        print(
            f"  {'growing wall' if growing else 'static      '}, after {t:6d} intervals: the light's reach {reach:7.0f} Links, images {images:6d}, presence {total:.6f} (units of q dwell)"
        )
print(
    "  static: the images within reach grow as (2 c_0 t / L)^3 and their fluxes 1 / d^2 sum to about 4 pi c_0 t / L^3 beyond the first: the presence grows without bound, linearly in t (Seeliger);"
)
print(
    "  growing wall: the reach saturates at (c_0 / H) ln(1 + H t) and each image's flux is cut off by e^(-H d / c_0) at the Hubble length c_0 / H = 233 Links: the sum converges (the nearest image and a tail)"
)
