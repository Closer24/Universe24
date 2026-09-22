"""The map of scaled-coupling-v1 (docs/designs/atom_levels/SCALED_COUPLING.md):
what one declared scale of the push's constant does to the ladder of the
atom's levels on the lattice, from the atoms generator's own arithmetic
(`examples/events/atoms/make_worlds.py`, series H's fan, flux count and
orbit; nothing copied). For the scales 4, 2, 1, 1/2 and 1/4 of the push:
the radius of each rung at the same action h (a_j ~ 1 / kappa), the
nearest whole radius, the flux the electron's three Nodes receive there
and its departure from the inverse square anchored at r = 12 (the fan's
grain), the orbit under the scaled push (the momentum, the closure 2 pi p
r / h, the period), the proton's shells per loop (the pulse's grain), the
level at [512, 1], the board's side and the ticks of five turns, and a
host estimate scaled from the registered r = 12 run (145 s for 7500 ticks
on 53^3, three runs sharing the host; 77 s alone). Every number is a
COMPUTATION (GAMEBOARD by formula); no run. Bohr's and Kepler's forms on
the comparison side only (record 817).

Run from the repository root:

    PYTHONPATH=src python docs/designs/atom_levels/scaled_coupling_map.py > docs/designs/atom_levels/scaled_coupling_map.out
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

Q, N, SHELL, RATIO = GEN.Q, GEN.N, GEN.SHELL, GEN.RATIO
SCALES = (Fraction(4), Fraction(2), Fraction(1), Fraction(1, 2), Fraction(1, 4))
RUNGS = (2, 3, 4, 5, 6)
REACH = 60  # the flux count's reach in Links (the largest radius mapped, plus the margin)
PAIR = 512  # n_l of the level's pair [512, 1]
BASE_SECONDS, BASE_TICKS, BASE_SIDE = 77.0, 7500, 53  # RUN_CENTRED.md: 77 s alone for 7500 ticks on 53^3

directions = GEN.BOHR.fan(GEN.BOHR.FAN_LOW, GEN.BOHR.FAN_HIGH)
count = GEN.BOHR.entries_per_node(directions, REACH)
derived_action = (
    4
    * int(GEN.orbit_form_b((1 + RATIO) * Q * GEN.BOHR.body_flux(count, 8) * 8 / SHELL, 8)["p"])
    * 8
    // 2
)
print(
    f"[COMPUTATION] the action h = 16 p_B(8) = {derived_action}; the flux at r = 12: {GEN.BOHR.body_flux(count, 12):.3f} entries per shell"
)
flux12 = GEN.BOHR.body_flux(count, 12)

print(
    "[COMPUTATION] the fan's grain by radius: the flux the three Nodes receive against the inverse square anchored at r = 12 (E_12 x 144 / r^2)"
)
for r in (3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 19, 24, 27, 32, 40, 48):
    flux = GEN.BOHR.body_flux(count, r)
    print(
        f"  r = {r}: {flux:.3f} against {flux12 * 144 / r / r:.3f}, {(flux / (flux12 * 144 / r / r) - 1) * 100:+.1f} percent"
    )

for scale in SCALES:
    print(
        f"[COMPUTATION] the push's constant scaled by {scale} (kappa x {scale}; the same h; a_j x {1 / scale})"
    )
    for j in RUNGS:
        a_j = 12 * (j / 4) ** 2 / float(scale)
        r = max(1, round(a_j))
        if r > REACH - 12:
            print(
                f"  rung {j}: a_j = {a_j:.2f} Links, beyond the map's reach ({REACH - 12} Links); "
                f"the board would exceed {GEN.BOHR.side_for(REACH - 12)}^3"
            )
            continue
        flux = GEN.BOHR.body_flux(count, r)
        orbit = GEN.orbit_form_b((1 + RATIO) * Q * flux * r / SHELL * float(scale), r)
        p = int(orbit["p"])
        closure = 2 * math.pi * p * r / derived_action
        period = orbit["period"]
        side = GEN.BOHR.side_for(r)
        ticks = max(GEN.BOHR.LEAST_TICKS, int(math.ceil(5 * period / 100.0)) * 100)
        level = (PAIR * N * closure) / (2 * period)
        seconds = BASE_SECONDS * (side / BASE_SIDE) ** 3 * ticks / BASE_TICKS
        grain = (flux / (flux12 * 144 / r / r) - 1) * 100
        print(
            f"  rung {j}: a_j = {a_j:.2f} Links, the world at r = {r} (side {side}); the flux {flux:.2f} ({grain:+.0f} percent off the inverse square); "
            f"p = {p}; the closure {closure:.3f} (the whole {j}); T = {period:.0f}; {period / SHELL:.0f} shells per loop, {360 * SHELL / period:.1f} degrees per shell; "
            f"the level {level:.1f} steps at [512, 1]; five turns {ticks} ticks, about {seconds / 60:.0f} min"
        )
