"""Audit harness (no intervention in any run): the LINKS FROZEN equivalence check.

``frozen_equivalence`` evolves two complete systems from their own initial snapshots with the ordinary engine and
compares them afterwards: (1) the base blocks alone, (2) base + extra blocks with the extra gears at their vacuum.
It is a comparison of two independent forward runs, never a stage of one."""
from __future__ import annotations
import numpy as np
from ..core.engine import OBJ, Engine, State
from ..core.tensor import Block, compose, vacuum_map

def frozen_equivalence(base: tuple[Block, ...], extra: tuple[Block, ...], base_state: State, steps: int) -> dict:
    """Run compose(*base) from base_state and compose(*base, *extra) from base_state + extra gears at (0, 0, r0).
    Returns counts of mismatches in the base sector and of deviations of the extra gears from their vacuum."""
    t_base = compose(*base)
    t_full = compose(*base, *extra)
    if t_full.names[:t_base.G] != t_base.names:
        raise ValueError('base gears must come first')
    r0 = vacuum_map(*extra)
    G0, N = (t_base.G, base_state.N)
    ex_names = t_full.names[G0:]
    vac_r = np.repeat(np.array([r0[n] for n in ex_names], dtype=OBJ)[:, None], N, axis=1)
    zeros = np.zeros((len(ex_names), N), dtype=OBJ)
    full = State(base_state.L, np.concatenate([base_state.a.astype(OBJ), zeros]), np.concatenate([base_state.b.astype(OBJ), zeros]), np.concatenate([base_state.r.astype(OBJ), vac_r]))
    e_base, e_full = (Engine(t_base), Engine(t_full))
    sb, sf = (base_state, full)
    base_bad = extra_dev = 0
    for _ in range(steps):
        sb, sf = (e_base.step(sb), e_full.step(sf))
        base_bad += int(np.sum(sf.a[:G0] != sb.a) + np.sum(sf.b[:G0] != sb.b) + np.sum(sf.r[:G0] != sb.r))
        extra_dev += int(np.sum(sf.a[G0:] != 0) + np.sum(sf.b[G0:] != 0) + np.sum(sf.r[G0:] != vac_r))
    return {'steps': steps, 'base_mismatches': base_bad, 'extra_deviations': extra_dev, 'frozen': base_bad == 0 and extra_dev == 0, 'G_base': G0, 'G_full': t_full.G, 'monomials_base': len(t_base), 'monomials_full': len(t_full)}
