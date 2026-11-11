"""Read-only observables for the Study 34 clock law (layers/clockgen.py; CLK-A). NEW file. Nothing here writes a state.

    lapse_sums(state, T)            exact B = Sum_x b(h00), A = Sum_x a(h00), R = Sum_x r(h00), H = Sum_x b(Th)
    k0_identity(E, before, after)   the summed Rule3 identity of the lapse, D (B' + A) = 2 Sum u + R - R' (exact, True/False)
    source_split(E, state, kappa)   S = Sum u(h00) - D B and its hand part kappa H (drive mode), exact ints
    hand_only_response(H, kappa, D) G(t) with G(t+1) = 2 G(t) - G(t-1) + 2 kappa H(t)/D, G(0) = G(-1) = 0 (Fractions)
    input_difference(E1, E0, state) Engine.inputs of two tensors on ONE state: the clock law's exact footprint
"""
from __future__ import annotations

from fractions import Fraction

import numpy as np

from ..core.engine import OBJ

LAPSE = "metric.h00"
HAND = "cosmic.Th"


def _isum(x) -> int:
    return int(np.asarray(x).astype(OBJ).sum())


def lapse_sums(state, tensor, lapse: str = LAPSE, hand: str = HAND) -> dict:
    g, h = tensor.gear_index(lapse), tensor.gear_index(hand)
    return {"B": _isum(state.b[g]), "A": _isum(state.a[g]), "R": _isum(state.r[g]), "H": _isum(state.b[h])}


def k0_identity(engine, before, after, tensor, lapse: str = LAPSE) -> bool:
    g = tensor.gear_index(lapse)
    U = _isum(np.asarray(engine.inputs(before))[g])
    D = engine.D
    return D * (_isum(after.b[g]) + _isum(before.a[g])) == 2 * U + _isum(before.r[g]) - _isum(after.r[g])


def source_split(engine, state, tensor, kappa: int, lapse: str = LAPSE, hand: str = HAND) -> dict:
    g, h = tensor.gear_index(lapse), tensor.gear_index(hand)
    U = _isum(np.asarray(engine.inputs(state))[g])
    S = U - engine.D * _isum(state.b[g])
    Hs = kappa * _isum(state.b[h])
    return {"S": S, "hand_part": Hs, "package_part": S - Hs}


def hand_only_response(H, kappa: int, D: int) -> list:
    """Exact hand-only lapse sum: the double sum of 2 kappa H / D from rest (Fractions)."""
    if type(D) is not int or D != 6:
        raise ValueError('this observer requires the fixed divisor six')
    G = [Fraction(0)]
    prev = Fraction(0)
    for t in range(len(H) - 1):
        nxt = 2 * G[-1] - prev + Fraction(2 * kappa * int(H[t]), D)
        prev = G[-1]
        G.append(nxt)
    return G


def input_difference(engine_new, engine_old, state) -> np.ndarray:
    """inputs(new) - inputs(old) on the SAME state (exact object array): the footprint of the added block."""
    return np.asarray(engine_new.inputs(state)).astype(OBJ) - np.asarray(engine_old.inputs(state)).astype(OBJ)


__all__ = ["lapse_sums", "k0_identity", "source_split", "hand_only_response", "input_difference"]
