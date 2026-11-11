"""READ-ONLY observables for the CHOICE layer (nothing here changes a state or feeds back into a run).

* ``quotient``      ell of one gear type at every node for the update before -> after (= after.b + before.a);
* ``official``      the official click flags of one gear type (quotient != 0 AND triple changed: core's rule);
* ``kinds``         handedness kinds (0 = C0, 1 = C1, 2 = C2) of one gear type for an update;
* ``harmonic_V``    S5-P2R's visibility V = 2|c1|/c0 over the six phases;
* ``bit_gate``      the DESIGNED (non-Born) reader of F7: decodes (o_A, a) from the front at Bob's node;
* ``mutual_info``   I(X; Y) in bits from a joint count table.
"""
from __future__ import annotations

import math
from collections import Counter

import numpy as np

from ..core.engine import State, extract_clicks, handedness_kind
from ..core.tensor import Tensor


def _ints(row) -> np.ndarray:
    """exact copy of one gear row as int64 (raises if a value does not fit; never wraps)."""
    if row.dtype == np.int64:
        return row.copy()
    vals = [int(v) for v in row]
    if vals and max(max(vals), -min(vals)) >= 1 << 62:
        raise OverflowError("value outside int64; read it with the object array directly")
    return np.array(vals, dtype=np.int64)


def quotient(tensor: Tensor, before: State, after: State, gear: str, nodes=None) -> np.ndarray:
    g = tensor.gear_index(gear)
    q = _ints(after.b[g]) + _ints(before.a[g])
    return q if nodes is None else q[np.asarray(nodes, dtype=np.intp)]


def click_flags(tensor: Tensor, D: int, before: State, after: State) -> np.ndarray:
    """(G, N) arithmetic-click flags, including audit-labelled gears.
    Use observe.readout.official_clicks for the public label-filtered stream."""
    log = extract_clicks(tensor, D, before, after, 1, "official")
    flags = np.zeros((before.G, before.N), dtype=bool)
    flags[np.asarray(log.gear, dtype=np.intp), np.asarray(log.node, dtype=np.intp)] = True
    return flags


def official(tensor: Tensor, D: int, before: State, after: State, gear: str, nodes=None) -> np.ndarray:
    """Arithmetic-click flags of the requested gear; no metadata-label filtering."""
    log = extract_clicks(tensor, D, before, after, 1, "official")
    g = tensor.gear_index(gear)
    flags = np.zeros(before.N, dtype=bool)
    flags[np.asarray(log.node)[np.asarray(log.gear) == g]] = True
    return flags if nodes is None else flags[np.asarray(nodes, dtype=np.intp)]


def kinds(tensor: Tensor, D: int, before: State, after: State, gear: str, nodes=None) -> np.ndarray:
    g = tensor.gear_index(gear)
    delta = (np.asarray(after.r[g], dtype=object) - np.asarray(before.r[g], dtype=object)) % D
    k = handedness_kind(delta, D)
    return k if nodes is None else k[np.asarray(nodes, dtype=np.intp)]


def values(state: State, tensor: Tensor, gear: str, field: str = "b", nodes=None) -> np.ndarray:
    g = tensor.gear_index(gear)
    v = _ints(getattr(state, field)[g])
    return v if nodes is None else v[np.asarray(nodes, dtype=np.intp)]


def harmonic_V(P) -> float:
    """S5-P2R's visibility over the six phases s = 0..5: V = 2|c1|/c0, c_k = mean_s P(s) e^{-2 pi i k s/6}."""
    s = np.arange(6)
    P = np.asarray(P, dtype=float)
    c0 = P.mean()
    c1 = (P * np.exp(-2j * np.pi * s / 6)).mean()
    return 2 * abs(c1) / c0 if c0 else float("nan")


def mutual_info(joint: Counter) -> float:
    """I(X; Y) in bits from counts of (x, y) pairs."""
    n = sum(joint.values())
    px, py = Counter(), Counter()
    for (x, y), c in joint.items():
        px[x] += c
        py[y] += c
    return sum(c / n * math.log2(c * n / (px[x] * py[y])) for (x, y), c in joint.items() if c)


def bit_gate(front_b, pair, patterns) -> tuple:
    """DESIGNED reader (non-Born, F7 control): returns the (o_A, a) whose expected front pattern equals the observed
    front values ``front_b`` at Bob's node; ``patterns[(o, a)]`` are the candidate patterns for a in ``pair``.
    Raises if the decoding is ambiguous or fails (it never guesses)."""
    hits = [k for k, pat in patterns.items() if list(pat) == [int(v) for v in front_b]]
    if len(hits) != 1:
        raise ValueError(f"bit gate: {len(hits)} matching patterns")
    return hits[0]


__all__ = ["quotient", "click_flags", "official", "kinds", "values", "harmonic_V", "mutual_info", "bit_gate"]
