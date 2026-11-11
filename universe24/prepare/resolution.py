"""Initial-data embedding/recovery for a global tensor resolution lift.

These functions return independent states and never advance or alter a run.
The map E_M(a,b,r)=(a,b,M*r) is injective, not a surjection onto all states
at divisor M*D. Its inverse is defined only for remainders divisible by M.
"""
from __future__ import annotations

import numpy as np

from ..core.engine import State
from ..core.tensor import Tensor
from ..layers.resolution import _source_parameters


def _check_state(state: State, tensor: Tensor, D: int) -> None:
    if not isinstance(state, State):
        raise TypeError("expected a State")
    if state.G != tensor.G:
        raise ValueError(f"state has {state.G} gear types, source tensor has {tensor.G}")
    if state.r.size and (int(state.r.min()) < 0 or int(state.r.max()) >= D):
        raise ValueError(f"state remainders must lie in 0..{D - 1}")


def lift_state(state: State, tensor: Tensor, factor: int, *, Q: int | None = None) -> State:
    """Embed an explicit source seed: keep a,b and multiply r by ``factor``.

    ``tensor`` is the unscaled source tensor. This is the seed paired with
    ``layers.resolution.lift_tensor(tensor, factor, Q=Q)``. In particular,
    M*(3Q-1) is usually NOT the new builder vacuum 3*M*Q-1.
    """
    source_Q = _source_parameters(tensor, factor, Q)
    _check_state(state, tensor, 6 * source_Q)
    # Cast before multiplying: both the factor and product can exceed int64.
    remainder = state.r.astype(object) * factor
    return State(state.L, state.a.copy(), state.b.copy(), remainder)


def unlift_state(state: State, tensor: Tensor, factor: int, *, Q: int | None = None) -> State:
    """Recover a source state only from the image of the resolution embedding.

    ``tensor`` is again the unscaled source tensor. Divisibility is necessary
    and sufficient for membership in this state embedding, but is NOT a
    claim that an arbitrary subsequently coupled history follows the original
    dynamics. Added interactions require their own analysis.
    """
    source_Q = _source_parameters(tensor, factor, Q)
    _check_state(state, tensor, 6 * source_Q * factor)
    remainder = state.r.astype(object)
    if np.any(remainder % factor != 0):
        raise ValueError("state is outside the resolution image: a remainder is not divisible by factor")
    return State(state.L, state.a.copy(), state.b.copy(), remainder // factor)


__all__ = ["lift_state", "unlift_state"]
