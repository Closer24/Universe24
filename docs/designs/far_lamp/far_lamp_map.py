"""The far lamp through a detector, the arithmetic (read-only, the mathematician,
2026-09-21; docs/designs/far_lamp/BRIGHTNESS.md): what a detector at rest reads of
a lamp at rest at the distance d on the periodic GameBoard under the growing tick
wall of DERIVATIONS_BEAM.md section 15 (the rule as stated there, integers as in
growing_wall.py), and the reading against the Hubble diagram of the standard
lamps (the supernovae): (1) the stream's arrival rate and the content per click on
integers; (2) the closed forms of the flux and the effective luminosity distance,
their series and the effective deceleration number; (3) the shape of the distance
modulus against the flat Lambda-CDM curve (the stand-in for the measured Hubble
diagram) and against Milne, with the intercept free as in the supernova fits;
(4) two more readings after a detector: the stretch of a lamp's stream and the
surface brightness of a resolved source. No run; expansion-v1 is not built.

Run from the repository root:

    python docs/designs/far_lamp/far_lamp_map.py > docs/designs/far_lamp/far_lamp_map.out
"""

from __future__ import annotations

import math

# The integers of section 15's stream (growing_wall.py): a heading, rate 2 S_1 Q against the
# wall 2 T_D a, a = H_den + H_num t scaled by H_den; H = 1 / 400 per interval.
Q = 64
S1, T_D = 1, 110
H_NUM, H_DEN = 1, 400
C0 = Q / T_D  # the pace in Links per interval on the heading, 32 / 55
HUBBLE = C0 * H_DEN / H_NUM  # the Hubble length c_0 / H in Links, 232.7


def tick_wall_stream(distance: int, emitted: int = 400, content: int = 5, horizon: int = 200000):
    """Rows released one per interval from tick 0, each carrying the content its lamp stamped
    at birth (section 6.4: h s, unchanged in flight) and its own Manhattan accumulator against
    the tick wall 2 T_D a(t). Returns (arrival ticks, contents read at the click)."""
    arrivals, contents = [], []
    for birth in range(emitted):
        acc = T_D * H_DEN
        links = 0
        t = birth
        while links < distance and t < horizon:
            a_num = H_DEN + H_NUM * t
            acc += 2 * S1 * Q * H_DEN
            wall = 2 * T_D * a_num
            if acc >= wall:
                acc -= wall
                links += 1
            t += 1
        arrivals.append(t)
        contents.append(content)  # the flight is a translation of the row; its content is not touched
    return arrivals, contents


print(
    "1. THE STREAM OF A LAMP AT REST UNDER THE TICK WALL, READ BY A DETECTOR AT REST (integers of section 15)"
)
print(
    "   the lamp releases one row per interval, each of content 5 (h s stamped at birth); the detector counts clicks per interval and content per interval"
)
for d in (50, 100, 200, 300):
    arr, con = tick_wall_stream(d)
    window = arr[-1] - arr[0]
    rate = (len(arr) - 1) / window  # clicks per interval at the detector, the lamp's rate being 1
    z = math.exp(d / HUBBLE) - 1
    content_rate = sum(con[1:]) / window
    print(
        f"   d = {d:3d} Links: 1 + z = {1 / rate:.3f} (e^(H d / c_0) = {1 + z:.3f}); clicks per interval {rate:.4f} = 1 / (1 + z) -> {1 / (1 + z):.4f};"
        f" content per interval {content_rate:.4f} = 5 / (1 + z) -> {5 / (1 + z):.4f}; content per click {con[0]} (unchanged)"
    )
print(
    "   one factor 1 / (1 + z) on the count and one on the content, the same factor: the click's content does not fall with the redshift (6.4)"
)
print()

# 2. The closed forms, in units of the Hubble length c_0 / H.


def d_law(z: float) -> float:
    """The lamp's distance in original Nodes, d = (c_0 / H) ln(1 + z) (section 15.2's tick wall)."""
    return math.log1p(z)


def dl_law(z: float) -> float:
    """The law's effective luminosity distance: flux = L / (4 pi d^2 (1 + z)), so d_L = d sqrt(1 + z)."""
    return d_law(z) * math.sqrt(1 + z)


def dl_law_two(z: float) -> float:
    """The hypothetical second factor (a content that followed the frequency in flight, no such rule
    in the six, 6.4): flux = L / (4 pi d^2 (1 + z)^2), d_L = d (1 + z); the flat coasting form."""
    return d_law(z) * (1 + z)


def dl_milne(z: float) -> float:
    """Milne, the empty coasting universe of the relativistic form: d_L = (c / H)(z + z^2 / 2)."""
    return z + z * z / 2


def dl_lcdm(z: float, omega_m: float = 0.3, steps: int = 2000) -> float:
    """Flat Lambda-CDM, d_L = (1 + z) (c / H) integral dz' / E(z'), E = sqrt(omega_m (1 + z')^3 + 1 - omega_m)."""
    h = z / steps
    total = 0.0
    for i in range(steps + 1):
        zz = i * h
        w = 1 if i in (0, steps) else (4 if i % 2 else 2)
        total += w / math.sqrt(omega_m * (1 + zz) ** 3 + 1 - omega_m)
    return (1 + z) * total * h / 3


def dl_eds(z: float) -> float:
    """Einstein-de Sitter, matter only: d_L = 2 (c / H)(1 + z)(1 - 1 / sqrt(1 + z))."""
    return 2 * (1 + z) * (1 - 1 / math.sqrt(1 + z))


MODELS = [
    ("the law, one factor (the rule as stated)", dl_law, "d_L = (c_0 / H) ln(1 + z) sqrt(1 + z)"),
    ("the hypothetical second factor (not in the six)", dl_law_two, "d_L = (c_0 / H) (1 + z) ln(1 + z)"),
    ("Milne (empty, coasting, curved)", dl_milne, "d_L = (c / H)(z + z^2 / 2)"),
    (
        "flat Lambda-CDM, Omega_m = 0.3 (the measured curve's stand-in)",
        dl_lcdm,
        "d_L = (1 + z)(c / H) int dz / E(z)",
    ),
    ("Einstein-de Sitter (matter only)", dl_eds, "d_L = 2 (c / H)(1 + z)(1 - 1 / sqrt(1 + z))"),
]

print(
    "2. THE CLOSED FORMS (units of the Hubble length c / H) AND THE EFFECTIVE DECELERATION NUMBER q read from the second order, d_L = (c / H)(z + (1 - q) z^2 / 2 + ...)"
)


def q_effective(fn) -> float:
    """The second-order coefficient by finite differences at small z: (1 - q) / 2 = (d_L - z) / z^2."""
    eps = 1e-3
    c2 = (fn(eps) - eps) / (eps * eps)
    return 1 - 2 * c2


for name, fn, formula in MODELS:
    q = q_effective(fn)
    row = "  ".join(f"z = {z:.2f}: {fn(z):.4f}" for z in (0.1, 0.5, 1.0, 1.5))
    print(f"   {name:58s} {formula:44s} q_eff = {q:+.2f};  {row}")
print(
    "   the law's series: ln(1 + z) sqrt(1 + z) = z - z^3 / 24 + ...: the z^2 term is zero, so the brightness reads q_eff = +1 although the flight's z(d) is Milne's (q = 0, 15.4);"
)
print(
    "   the missing energy factor is the whole difference: with it the law would be the flat coasting form (q_eff = 0), without it the lamp is brighter by (1 + z)"
)
print()

# 3. The shape of the distance modulus against the stand-in for the measured Hubble diagram.
print(
    "3. THE SHAPE OF THE HUBBLE DIAGRAM, mu = 5 log10 d_L + const, the constant free as in the supernova fits (the lamp's absolute content and H are one number)"
)
grid = [
    0.01 + 0.01 * i for i in range(150)
]  # z from 0.01 to 1.50, the range of the supernova compilations
reference = [5 * math.log10(dl_lcdm(z)) for z in grid]
print(
    "   against flat Lambda-CDM at Omega_m = 0.3 (positive = the model's lamp fainter than the stand-in at that z after the intercept is fitted):"
)
for name, fn, _ in MODELS:
    mu = [5 * math.log10(fn(z)) for z in grid]
    offset = sum(r - m for r, m in zip(reference, mu, strict=True)) / len(grid)
    resid = [m + offset - r for m, r in zip(mu, reference, strict=True)]
    rms = math.sqrt(sum(r * r for r in resid) / len(resid))
    worst = max(resid, key=abs)
    at = {
        z: resid[i]
        for i, z in enumerate(grid)
        if abs(z - round(z, 1)) < 1e-9 and round(z, 1) in (0.1, 0.5, 1.0, 1.5)
    }
    marks = "  ".join(f"z = {z:.1f}: {v:+.3f}" for z, v in sorted(at.items()))
    print(f"   {name:58s} rms {rms:.3f} mag, worst {worst:+.3f} mag;  {marks}")
print(
    "   the supernova compilations pin the shape to about 0.02 mag per bin over this range (Pantheon+, 1701 lamps); Milne is excluded by them at many sigma, the law's one-factor form lies farther from the stand-in than Milne and on the same side (too bright at high z)"
)
print()

# The same shape read as a difference of two readings, without any model in between:
print(
    "   the reading that needs no fit: the lamp at z = 0.5 against the lamp at z = 0.05 (a ratio of two fluxes, the intercept cancels)"
)
for name, fn, _ in MODELS:
    dm = 5 * math.log10(fn(0.5) / fn(0.05))
    print(f"   {name:58s} mu(0.5) - mu(0.05) = {dm:.3f} mag")
print()

# 4. Two more readings after a detector.
print("4. TWO MORE READINGS AFTER A DETECTOR")
arr, _ = tick_wall_stream(300, emitted=400)
stretch = (arr[-1] - arr[0]) / 399
print(
    f"   (a) the stretch of a lamp's stream: a stream of 400 rows released over 400 intervals arrives over {arr[-1] - arr[0]} intervals at 300 Links, the factor {stretch:.3f} = 1 + z;"
)
print(
    "       nature: the supernova light curves are stretched by (1 + z)^(0.97 +- 0.10) (Blondin and others 2008): the law gives the same factor exactly, a reading it passes"
)
print(
    "   (b) the surface brightness of a resolved source (the flux over the angular area): the board's Nodes are fixed and the fan's lines are fixed (15.5), so a ruler of l Nodes at the distance d subtends l / d,"
)
print(
    "       the angular-diameter distance is d = (c_0 / H) ln(1 + z) and the surface brightness falls as (1 + z)^-1; the relativistic form gives (1 + z)^-4 (Tolman), the measured exponent between 2.3 and 3.1 in the bands before any correction, consistent with 4 once the sources' own brightening with look-back time is removed (Lubin and Sandage 2001)"
)
for z in (0.1, 0.5, 1.0):
    da_lcdm = dl_lcdm(z) / (1 + z) ** 2
    print(
        f"       z = {z:.1f}: the law's angular-diameter distance {d_law(z):.3f}, flat Lambda-CDM's {da_lcdm:.3f} (units c / H): the law's ruler looks {da_lcdm / d_law(z):.2f} times as large; the surface brightness (1 + z)^-1 = {1 / (1 + z):.3f} against (1 + z)^-4 = {(1 + z) ** -4:.3f}"
    )
print()
print(
    "5. THE VERDICT: after a detector the gap does not close, it widens: the lamp's brightness reads q_eff = +1 (the rule as stated) against the measured -0.55, and the one rule that would bring it to q_eff = 0 (the content following the frequency in flight) is not one of the six (6.4); the stretch of the stream is the one reading the law passes exactly"
)
