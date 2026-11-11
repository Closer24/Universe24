"""Explicit integer preparations for the fixed-divisor reference default.

Preparation chooses an initial pattern and never runs the update, changes the
coupling tensor, or inserts later signals. The former multi-sector physics
preparation is not reinterpreted as a divisor-six seed.
"""
from __future__ import annotations
import random
from ..core import State
from . import vacuum_state


def one_seed(system, tensor, L: int, *, bang: str = "pulse", rng_seed: int = 13):
    """Complete pulse, standing, or vacuum data; no particle identification."""
    if bang not in ("pulse", "standing", "none"):
        raise ValueError("fixed-divisor preparations are pulse, standing, or none; old physics seeds were retired")
    if type(rng_seed) is not int:
        raise TypeError("rng_seed must be an integer")
    seed = vacuum_state(tensor, L, *system.blocks)
    a, b, r = (array.astype(object).copy() for array in (seed.a, seed.b, seed.r))
    rng = random.Random(rng_seed)
    gear = rng.randrange(tensor.G)
    node = seed.lattice.index(L//2, L//2, L//2)
    if bang == "pulse":
        a[gear, node] = b[gear, node] = 3
    elif bang == "standing":
        for index, (x, y, z) in enumerate(seed.lattice.all_coords()):
            a[gear, index] = b[gear, index] = 3 if (int(x)+int(y)+int(z)) % 2 == 0 else -3
    return State(L, a, b, r), dict(kind=bang, rng_seed=rng_seed, gear=tensor.names[gear],
        origin=list(seed.lattice.coords(node)), amplitude=3 if bang != "none" else 0,
        all_seed_arithmetic="integers", c2=[0,0,0],
        interpretation="generic reference-lattice preparation; no particle or cosmological identification")


__all__ = ["one_seed"]
