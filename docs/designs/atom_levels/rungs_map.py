"""The three rungs of atom-level-v1 under the virial form (docs/designs/
atom_levels/LEVELS.md sections 2 (b) and 5): the atoms generator
(`examples/events/atoms/make_worlds.py`, which imports series H's fan, flux
count and orbit arithmetic) is the one source of every number here, as
it is for `hydrogen_r12_centred.json`. For the radii 3, 7 and 12: the
flux the electron's three Nodes receive, the orbit under form B's drive
(the centred world's own momentum rule), the closure 2 pi p r = j h
against the world's action, the period, the level in phase steps at the
rule's pair, the lines and their ratio, the fan's departure, the grain.
Every number is a COMPUTATION from the generator (GAMEBOARD by formula
until a detector clicks); no run. Bohr's, Balmer's and Kepler's forms
appear only as the thing compared with (record 817).

Run from the repository root:

    PYTHONPATH=src python docs/designs/atom_levels/rungs_map.py > docs/designs/atom_levels/rungs_map.out
"""

from __future__ import annotations

import importlib.util
import math
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    "atoms_make_worlds", ROOT / "examples" / "events" / "atoms" / "make_worlds.py"
)
GEN = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(GEN)

Q, N, SHELL, RATIO, WIDTH = GEN.Q, GEN.N, GEN.SHELL, GEN.RATIO, GEN.WIDTH
ELECTRON = GEN.ELECTRON
RUNGS = (3, 7, 12)  # the radii at whole Links where the shell mean puts j = 2, 3, 4
PAIRS = ((256, 1), (512, 1))  # the rule's pair [n_l, d_l], the Boss's two candidates
FLUX_EXPONENT = 1.83  # the register's ring flux r^-k (ALGEBRA.md section 2 (d), GAMEBOARD)
ALIAS = N // 2


def level_steps(n_l: int, d_l: int, delta_a: int, count: int) -> int:
    """The level in phase steps, the exact integer form of section 2 (b):
    floor(n_l Delta A / (2 h d_l T)) with Delta A the action gained over
    the loop (j N h on a closed loop) and T the count since the previous
    return."""
    return (n_l * delta_a) // (2 * ACTION * d_l * count)


def balmer(exponent: float, j: int, i: int) -> float:
    """The ratio of two lines when the level goes as j^-exponent (2 in the
    shell mean; (2 k - 2) / (3 - k) under a flux r^-k), for the pairs
    (j, 2) over (3, 2)."""
    line = lambda a, b: b**-exponent - a**-exponent  # noqa: E731
    return line(j, i) / line(3, 2)


derived = GEN.derive()
count = derived["count"]
ACTION = int(derived["action"])
print(
    f"[COMPUTATION] the world's action h = 16 p_B(8) = {ACTION} (the generator's rule); N = {N}; Q = {Q}; S = {WIDTH}; M = {ELECTRON}"
)

rungs: dict[int, dict[str, float]] = {}
for r in RUNGS:
    flux = GEN.BOHR.body_flux(count, r)
    orbit = GEN.orbit_form_b((1 + RATIO) * Q * flux * r / SHELL, r)
    p = int(orbit["p"])
    j = 2 * math.pi * p * r / ACTION
    period = orbit["period"]
    side = GEN.BOHR.side_for(r)
    ticks = GEN.ticks_for(period)
    rungs[r] = {
        "flux": flux,
        "p": p,
        "j": j,
        "T": period,
        "side": side,
        "ticks": ticks,
        "v": orbit["speed"],
    }
    print(
        f"[COMPUTATION] r = {r}: E_body = {flux:.3f} entries per shell; p_B = {p}; v = {orbit['speed']:.5f} Links per interval; "
        f"j = 2 pi p r / h = {j:.4f} (the shell mean's 4 sqrt(r / 12) = {4 * math.sqrt(r / 12):.4f}); T = 2 pi r / v = {period:.1f}; "
        f"kicks per loop = {period / SHELL:.1f}; side {side} (c = {side // 2}), the electron at (c + {r}, c, c); ticks {ticks}"
    )

print(
    "[COMPUTATION] the level at each rung, L = floor(n_l Delta A / (2 h d_l T)) with Delta A = j N h on the closed loop, T the period rounded"
)
levels: dict[tuple[int, int], dict[int, int]] = {}
for n_l, d_l in PAIRS:
    levels[(n_l, d_l)] = {}
    for r in RUNGS:
        j_whole = round(rungs[r]["j"])
        t = round(rungs[r]["T"])
        delta_a_read = int(
            round(rungs[r]["j"] * N * ACTION)
        )  # the closure as the generator's j gives it
        l_read = level_steps(n_l, d_l, delta_a_read, t)
        l_exact = Fraction(n_l * N * j_whole, 2 * t * d_l)
        levels[(n_l, d_l)][r] = l_read
        print(
            f"  [{n_l}, {d_l}] r = {r}: L = {l_read} steps from the generator's j {rungs[r]['j']:.4f} and T {t} "
            f"(the whole rung's n_l N j / (2 T) = {float(l_exact):.2f}); alias bound {ALIAS}"
        )
    l3, l7, l12 = (levels[(n_l, d_l)][r] for r in RUNGS)
    ratio = Fraction(l3 - l12, l3 - l7)
    print(
        f"  [{n_l}, {d_l}] the lines: s(4 to 2) = L_2 - L_4 = {l3 - l12}, s(3 to 2) = L_2 - L_3 = {l3 - l7}, "
        f"the ratio {ratio} = {float(ratio):.4f}, the grain's band 1 / {l3 - l7} = {1 / (l3 - l7):.4f}"
    )
    ratio_limit = Fraction(3, 16) / Fraction(5, 36)
    print(
        f"  the shell mean's ratio from the whole rungs 2, 3, 4: {ratio_limit} = {float(ratio_limit)} (Balmer's, on the comparison side)"
    )

print(
    "[COMPUTATION] the ratio of the two levels' ladder as the generator's own j and T give it (no whole rung assumed)"
)
for r in RUNGS:
    print(
        f"  r = {r}: j / (2 T) = {rungs[r]['j'] / (2 * rungs[r]['T']):.6f} circles per interval; against the rung-4 value x (4 / j)^2: {rungs[12]['j'] / (2 * rungs[12]['T']) * (4 / rungs[r]['j']) ** 2:.6f}"
    )
g = lambda r: rungs[r]["j"] / (2 * rungs[r]["T"])  # noqa: E731
print(
    f"  the ratio (L_2 - L_4) / (L_2 - L_3) from the generator's own numbers, before the floor: {(g(3) - g(12)) / (g(3) - g(7)):.4f}"
)

print("[COMPUTATION] the fan's departure: a level ~ j^-e with e = (2 k - 2) / (3 - k) under a flux r^-k")
for k in (2.0, FLUX_EXPONENT, 1.69, 1.5, 1.35):
    e = (2 * k - 2) / (3 - k)
    print(
        f"  k = {k}: e = {e:.3f}; (4 to 2) / (3 to 2) = {balmer(e, 4, 2):.4f}; (5 to 2) / (3 to 2) = {balmer(e, 5, 2):.4f}"
    )

print(
    "[COMPUTATION] the pulse's grain per rung: the proton's shells per loop and the kick per shell in degrees of the momentum"
)
for r in RUNGS:
    kick = math.degrees(rungs[r]["flux"] * (1 + RATIO) * Q * ELECTRON / rungs[r]["p"])
    print(f"  r = {r}: {rungs[r]['T'] / SHELL:.1f} shells per loop, {kick:.2f} degrees per shell")

print("[COMPUTATION] the bounds: n_l Delta A and 2 h d_l T against 2^62")
for n_l, d_l in PAIRS:
    print(
        f"  [{n_l}, {d_l}]: n_l x 8 N h = {n_l * 8 * N * ACTION:.3e}; 2 h d_l x 10^4 = {2 * ACTION * d_l * 10**4:.3e}; 2^62 = {2**62:.3e}"
    )
