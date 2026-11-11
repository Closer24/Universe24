"""Explicit integer preparations for local communication and the reference model.

Preparation chooses an initial pattern and never runs the update, changes the
coupling tensor, or inserts later signals. The former multi-sector physics
preparation is not reinterpreted as a divisor-six seed.
"""
from __future__ import annotations
import random
from ..core import State
from . import vacuum_state


def reference_seed(system, tensor, L: int, *, bang: str = "pulse", rng_seed: int = 13):
    """Complete pulse, standing, or vacuum data; no particle identification."""
    if bang not in ("pulse", "standing", "none"):
        raise ValueError("fixed-divisor preparations are pulse, standing, or none; old physics seeds were retired")
    if type(rng_seed) is not int:
        raise TypeError("rng_seed must be an integer")
    seed = vacuum_state(tensor, L, *system.blocks)
    a, b, r = (array.astype(object).copy() for array in (seed.a, seed.b, seed.r))
    if system.info.get('communication', False):
        from .communication import message_seed
        from ..layers.communication import LANES
        if bang == 'standing':
            raise ValueError('standing is a reference preparation; select communication=False')
        origin = (L // 2,) * 3
        packets = [(lane, origin, 3) for lane in LANES] if bang == 'pulse' else []
        prepared = message_seed(seed, tensor, packets)
        return prepared, dict(kind=bang, origin=list(origin), amplitude=3 if packets else 0,
                              packets=[dict(lane=lane, origin=list(xyz), payload=value)
                                       for lane, xyz, value in packets],
                              rng_seed=rng_seed, rng_seed_used=False,
                              all_seed_arithmetic='integers',
                              interpretation='initial local messages; no cosmic age or carried clock')
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


__all__ = ["reference_seed"]
