"""Initial data for the compact gauge layers and the dynamic base links (AGENTS item 9: data only).

Every function returns a NEW State built before a run; nothing here runs the engine or touches a running state.
States are complete (a, b, r) for every gear; link values are written in deviation form (stored = physical - X0).
"""
from __future__ import annotations

import random

import numpy as np

from ..core.engine import OBJ, State
from ..core.lattice import lattice
from ..core.tensor import Block, Tensor
from ..layers.gauge import ALGEBRAS, gear_names
from . import vacuum_state


def _q(name, g):
    return f"{name}.{g}" if name else g


def gauge_vacuum(tensor: Tensor, L: int, *blocks: Block) -> State:
    """The joint vacuum with each block's explicit remainder in zero through five."""
    return vacuum_state(tensor, L, *blocks)


def random_gauge_state(tensor: Tensor, block: Block, base: State, seed: int, amp_matter: int, amp_noise: int,
                       amp_path: int = 0, unit_links: bool = True, random_r: bool = True) -> State:
    """Copy of ``base`` with the gauge layer of ``block`` filled with random data:
    matter a, b uniform in [-amp_matter, amp_matter]; links U = A*g + noise with g a random unit of the integer
    gauge group (unit_links) or g = 1, noise uniform in [-amp_noise, amp_noise] (stored W = U - A*1); 2-path
    deviations uniform in [-amp_path, amp_path]; remainders uniform in 0..D-1 (random_r) or left as in base."""
    rng = random.Random(seed)
    p = block.params
    alg = ALGEBRAS[p["group"]]
    D = 6
    A = p["A"]
    matter, links, paths = gear_names(p["group"], p["use_P"])
    a, b, r = base.a.astype(OBJ), base.b.astype(OBJ), base.r.astype(OBJ)
    N = base.N
    nm = block.name
    for g in matter:
        i = tensor.gear_index(_q(nm, g))
        a[i] = [rng.randint(-amp_matter, amp_matter) for _ in range(N)]
        b[i] = [rng.randint(-amp_matter, amp_matter) for _ in range(N)]
        if random_r:
            r[i] = [rng.randrange(D) for _ in range(N)]
    for k in range(3):
        rows = [tensor.gear_index(_q(nm, g)) for g in links[k]]
        for n in range(N):
            for fld in (a, b):
                g = rng.choice(alg.group) if unit_links else alg.one
                for c, i in enumerate(rows):
                    fld[i, n] = A * g[c] - A * alg.one[c] + rng.randint(-amp_noise, amp_noise)
            if random_r:
                for i in rows:
                    r[i, n] = rng.randrange(D)
    for key, names in paths.items():
        for g in names:
            i = tensor.gear_index(_q(nm, g))
            a[i] = [rng.randint(-amp_path, amp_path) for _ in range(N)]
            b[i] = [rng.randint(-amp_path, amp_path) for _ in range(N)]
            if random_r:
                r[i] = [rng.randrange(D) for _ in range(N)]
    return State(base.L, a, b, r)


def set_gears(state: State, tensor: Tensor, values: dict) -> State:
    """Copy with values[(qualified gear name, (x, y, z))] = (a, b) or (a, b, r) set. Data only."""
    a, b, r = state.a.astype(OBJ), state.b.astype(OBJ), state.r.astype(OBJ)
    lat = lattice(state.L)
    for (name, xyz), val in values.items():
        g, n = tensor.gear_index(name), lat.index(*xyz)
        a[g, n], b[g, n] = val[0], val[1]
        if len(val) > 2:
            r[g, n] = val[2]
    return State(state.L, a, b, r)


def set_link(state: State, tensor: Tensor, block: Block, xyz, k: int, U_ab, ) -> State:
    """Copy with the PHYSICAL link U(x, k) set to (U_a, U_b) (algebra vectors); stored W = U - A*1."""
    p = block.params
    alg = ALGEBRAS[p["group"]]
    _, links, _ = gear_names(p["group"], p["use_P"])
    Ua, Ub = U_ab
    vals = {}
    for c, g in enumerate(links[k]):
        vals[(_q(block.name, g), tuple(xyz))] = (Ua[c] - p["A"] * alg.one[c], Ub[c] - p["A"] * alg.one[c])
    return set_gears(state, tensor, vals)


def set_matter(state: State, tensor: Tensor, block: Block, xyz, psi_a, psi_b) -> State:
    p = block.params
    matter, _, _ = gear_names(p["group"], p["use_P"])
    vals = {(_q(block.name, g), tuple(xyz)): (psi_a[c], psi_b[c]) for c, g in enumerate(matter)}
    return set_gears(state, tensor, vals)


__all__ = ["gauge_vacuum", "random_gauge_state", "set_gears", "set_link", "set_matter"]
