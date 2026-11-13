"""Exact joint 2O action on 48 node channels and the periodic cube.

Channel index g is the label in algebra.group_2o.group().quaternions.
For every bank v in (a,b,r): (A_k v)[k*g, R_k x] = v[g,x].
This is an unsigned permutation, including the central element -1.
The coefficient certificate is a polynomial identity, not sampled evolution.
"""
from functools import lru_cache

import numpy as np

from universe24.algebra.group_2o import group, rotate
from .engine import State
from .tensor import Factor, Tensor

CONTRACT = "2O-left-regular-cube/1"


class SymmetryError(ValueError):
    """A declared 2O action is unsupported or a polynomial breaks it."""


def act(state: State, k: int) -> State:
    """Return A_k(state), preserving all integers and all six remainder values."""
    if state.G != 48:
        raise SymmetryError(f"2O action requires exactly 48 channels; got {state.G}")
    if type(k) is not int or not 0 <= k < 48:
        raise SymmetryError("2O group label must be an integer in 0..47")
    algebra = group()
    # Gather from k^-1*g and R_k^-1*x rather than scatter into the destination.
    inverse = algebra.inverses[k]
    gears = np.array(algebra.multiplication[inverse], dtype=np.intp)
    xyz = state.lattice.all_coords() @ np.array(algebra.rotations[inverse]).T
    xyz %= state.L
    nodes = (xyz[:, 0] * state.L + xyz[:, 1]) * state.L + xyz[:, 2]
    banks = [getattr(state, bank)[np.ix_(gears, nodes)] for bank in ("a", "b", "r")]
    return State(state.L, *banks)


@lru_cache(maxsize=64)
def require_equivariant(tensor: Tensor) -> None:
    """Check every coefficient under all 48 group elements, on any cube size.

This version represents node channels only, with one common passive readout
label. Yee links need a different action including base-node translations;
they cannot silently inherit this certificate. Names and reciprocity signs
are audit metadata and do not define amplitude transformations.
"""
    if tensor.G != 48:
        raise SymmetryError(f"{CONTRACT}: exactly 48 channels required; got {tensor.G}")
    if any(gear.link is not None for gear in tensor.gears):
        raise SymmetryError(f"{CONTRACT}: only node channels are represented")
    if len(set(tensor.labels)) != 1:
        raise SymmetryError(f"{CONTRACT}: passive labels must be invariant on the 48-channel orbit")
    original = {(m.target, m.factors): m.coeff for m in tensor.monomials}
    algebra = group()
    for k in range(48):
        permutation, rotation = algebra.multiplication[k], algebra.rotations[k]
        for monomial in tensor.monomials:
            target = permutation[monomial.target]
            factors = tuple(sorted(Factor(permutation[f.gear], rotate(rotation, f.offset), f.field)
                                   for f in monomial.factors))
            actual = original.get((target, factors), 0)
            if actual != monomial.coeff:
                raise SymmetryError(
                    f"{CONTRACT}: covariance failed at group label {k}, "
                    f"target {monomial.target}->{target}, factors={factors!r}: "
                    f"expected coefficient {monomial.coeff}, found {actual}")
