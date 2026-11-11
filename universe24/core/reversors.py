"""Generic reversor building blocks (stage 0.2). AUDIT maps on complete states: never stages of the forward
evolution, never fed back into a run. Exact integers only; no physics: which map acts on which gear is DATA.

A map is a ``StateMap``: ``X(state) -> State``; ``X @ Y`` is the composition X o Y (Y first).

(a) Per-gear maps (D = 6; R'(r) = D-2-r for even r, D-r for odd r; both remainder maps are involutions):
      "id"  (a, b, r)                        identity
      "M"   (b, a, D-1-r)                    time mirror; flips r mod 2; reversor of every b-only tensor
      "Mp"  (b, a, R'(r))                    M': parity-preserving time mirror; = universe24 time_reverse for D = 6
      "J"   (-a, -b, D-1-r)                  negation; a symmetry of odd tensors (no constants, no even degrees)
      "JR"  J o M' = (-b, -a, r xor 1)       (manager's definition, 09:14)
      "JM"  J o M  = (-b, -a, r)             (the "JR" of CLICK_TAXONOMY)
      "Jp"  (-a, -b, R'(r))                  parity-preserving negation (the J_D of CLICK_TAXONOMY)
      "rhoL0" (b, a, rho(r)), rho(r) = 4 + 2 (r mod 2) - r: the reference mirror.
            It fixes the reference vacuum remainder two and coincides with "Mp"
            on the six legal remainders. For b-only integer inputs it is a reversor;
            old-history inputs require their own theorem.
    ``GearwiseMap(tensor, {gear_name: map_name, ...}, default="id")``; ``uniform(tensor, name)``.
(b) ``GroupLinearMap(tensor, gears, matrix, r_rule=None, neg_r="M")``: at every node, the (a, b) values of the
    listed gear types are replaced by matrix @ (a, b) (the same integer matrix on a and on b). Remainders: target i
    takes ``rmap(r[source])`` from ``r_rule[i] = (source_index, rmap_name)`` with rmap_name in {"id", "M", "Mp"}.
    For a signed permutation matrix r_rule may be omitted: a +1 entry copies r, a -1 entry applies ``neg_r``
    ("M": D-1-r, as in J; "Mp": R'). Gears not listed are unchanged. Link gears are stored at nodes, so a link's gear
    block is a group like any other.
(c) ``SpatialMap(tensor, S)``: inversion x -> S - x (mod L) for node gears; a link gear of Yee axis k stored at x
    (link x .. x+e_k) goes to the base S - x - e_k (the link (x, x+e) maps to (S-x-e, S-x)). Values are moved, not
    changed (signs of oriented quantities are layer data: compose with (b)). Constructors: ``identity_map``,
    ``inversion_about_node(x0)`` (S = 2 x0), ``inversion_about_cube_centre(x0)`` (centre x0 + (1,1,1)/2,
    S = 2 x0 + (1,1,1); no fixed node), ``inversion_about_box_centre(L)`` (S = (L-1)(1,1,1): a cube-centre inversion
    for even L, a node inversion for odd L).
(d) ``reversor_check(X, F, states, n, central=())``: counts X F^n X F^n (s) == s, or == Z(s) for a declared central
    map Z (name, map), else a failure.
(e) ``is_fixed(X, state)``.
"""
from __future__ import annotations

from typing import Callable, Iterable, Sequence

import numpy as np

from .engine import I64, LIMIT, OBJ, State, _cast, _maxabs_rows
from .lattice import DIRECTIONS, lattice
from .tensor import Tensor

R_MAPS = ("id", "M", "Mp", "rhoL0")
GEAR_MAPS = {            # name: (swap a<->b, negate, remainder map applied AFTER the swap)
    "id": (False, False, "id"),
    "M": (True, False, "M"),
    "Mp": (True, False, "Mp"),
    "rhoL0": (True, False, "rhoL0"),
    "J": (False, True, "M"),
    "JR": (True, True, "JR"),
    "JM": (True, True, "id"),
    "Jp": (False, True, "Mp"),
}


def remainder_map(name: str, r: np.ndarray, D: int = 6) -> np.ndarray:
    """Exact remainder maps on 0..5. "JR" is 5 - R'(r) = r xor 1."""
    if type(D) is not int or D != 6:
        raise ValueError("remainder maps use the fixed divisor six")
    if name == "id":
        return r.copy()
    if name == "M":
        return (D - 1) - r
    if name == "Mp":
        return np.where(r % 2 == 0, (D - 2) - r, D - r)
    if name == "JR":
        return (D - 1) - np.where(r % 2 == 0, (D - 2) - r, D - r)
    if name == "rhoL0":
        return 4 + 2 * (r % 2) - r
    raise ValueError(f"unknown remainder map {name!r}; use one of {R_MAPS}")


class StateMap:
    """Base class: a map of complete states. ``X @ Y`` = X o Y."""

    name = "map"

    def __call__(self, state: State) -> State:
        raise NotImplementedError

    def __matmul__(self, other: "StateMap") -> "StateMap":
        return Composite([other, self])

    def __repr__(self):
        return f"<{type(self).__name__} {self.name}>"


class Composite(StateMap):
    def __init__(self, maps_in_order: Sequence[StateMap]):
        flat = []
        for m in maps_in_order:
            flat.extend(m.maps if isinstance(m, Composite) else [m])
        self.maps = flat
        self.name = " o ".join(m.name for m in reversed(flat))

    def __call__(self, state: State) -> State:
        for m in self.maps:
            state = m(state)
        return state


class FunctionMap(StateMap):
    def __init__(self, fn: Callable[[State], State], name: str = "fn"):
        self.fn, self.name = fn, name

    def __call__(self, state: State) -> State:
        return self.fn(state)


# --------------------------------------------------------------------------------------------- (a) per-gear maps
class GearwiseMap(StateMap):
    def __init__(self, tensor: Tensor, choices: dict | None = None, default: str = "id"):
        self.D = 6
        self.G = tensor.G
        choices = dict(choices or {})
        per = [default] * tensor.G
        for name, m in choices.items():
            per[tensor.gear_index(name)] = m
        for m in per:
            if m not in GEAR_MAPS:
                raise ValueError(f"unknown per-gear map {m!r}; use one of {sorted(GEAR_MAPS)}")
        self.per = tuple(per)
        self.name = default if not choices else f"gearwise({default}; {len(choices)} set)"

    def __call__(self, state: State) -> State:
        if state.G != self.G:
            raise ValueError("state does not match the tensor")
        dtype = OBJ if OBJ in (state.a.dtype, state.b.dtype) else I64     # a and b rows may be swapped
        A0, B0 = _cast(state.a, dtype), _cast(state.b, dtype)
        r_dtype = OBJ if state.r.dtype == OBJ else I64
        a, b, r = A0.copy(), B0.copy(), _cast(state.r, r_dtype).copy()
        for g, m in enumerate(self.per):
            swap, neg, rm = GEAR_MAPS[m]
            ag, bg = (B0[g], A0[g]) if swap else (A0[g], B0[g])
            a[g], b[g] = (-ag, -bg) if neg else (ag, bg)
            r[g] = remainder_map(rm, state.r[g], self.D)
        return State._raw(state.L, a, b, r)


def uniform(tensor: Tensor, name: str) -> GearwiseMap:
    """The same per-gear map on every gear type."""
    gm = GearwiseMap(tensor, default=name)
    gm.name = name
    return gm


# --------------------------------------------------------------------------------------- (b) linear group maps
class GroupLinearMap(StateMap):
    def __init__(self, tensor: Tensor, gears: Sequence[str], matrix: Sequence[Sequence[int]],
                 r_rule: Sequence[tuple[int, str]] | None = None, neg_r: str = "M", name: str = "linear"):
        self.D, self.G, self.name = 6, tensor.G, name
        self.idx = [tensor.gear_index(g) for g in gears]
        k = len(self.idx)
        if len(set(self.idx)) != k:
            raise ValueError("repeated gear in a group map")
        A = [list(row) for row in matrix]
        if len(A) != k or any(len(row) != k for row in A) or any(type(v) is not int for row in A for v in row):
            raise ValueError("matrix must be k x k Python ints")
        self.A = A
        if r_rule is None:
            r_rule = []
            for row in A:
                nz = [(j, v) for j, v in enumerate(row) if v != 0]
                if len(nz) != 1 or nz[0][1] not in (1, -1):
                    raise ValueError("r_rule is required unless the matrix is a signed permutation")
                r_rule.append((nz[0][0], "id" if nz[0][1] == 1 else neg_r))
            if sorted(j for j, _ in r_rule) != list(range(k)):
                raise ValueError("not a signed permutation")
        if len(r_rule) != k or any(not (0 <= j < k) or rm not in R_MAPS for j, rm in r_rule):
            raise ValueError("r_rule must give (source index, remainder map) per target")
        self.r_rule = [(int(j), rm) for j, rm in r_rule]
        self.rowsum = max(sum(abs(v) for v in row) for row in A)

    def __call__(self, state: State) -> State:
        if state.G != self.G:
            raise ValueError("state does not match the tensor")
        rows = self.idx
        big = max(_maxabs_rows(state.a[rows]) + _maxabs_rows(state.b[rows]) + [0])
        dtype = I64 if (state.a.dtype == I64 and state.b.dtype == I64 and self.rowsum * big < LIMIT
                        and self.rowsum < LIMIT) else OBJ
        r_dtype = OBJ if state.r.dtype == OBJ else I64
        a, b, r = _cast(state.a, dtype).copy(), _cast(state.b, dtype).copy(), _cast(state.r, r_dtype).copy()
        A0, B0 = _cast(state.a, dtype), _cast(state.b, dtype)
        for i, gi in enumerate(rows):
            acc_a = np.zeros(state.N, dtype=dtype)
            acc_b = np.zeros(state.N, dtype=dtype)
            for j, v in enumerate(self.A[i]):
                if v:
                    acc_a = acc_a + v * A0[rows[j]]
                    acc_b = acc_b + v * B0[rows[j]]
            a[gi], b[gi] = acc_a, acc_b
            src, rm = self.r_rule[i]
            r[gi] = remainder_map(rm, state.r[rows[src]], self.D)
        return State(state.L, a, b, r)


# ------------------------------------------------------------------------------------------- (c) spatial maps
class SpatialMap(StateMap):
    """x -> S - x (mod L); link gears of axis k re-based to S - x - e_k. S = None: identity."""

    def __init__(self, tensor: Tensor, S: tuple[int, int, int] | None, name: str = "spatial"):
        self.G, self.S, self.name = tensor.G, S, name
        self.links = [g.link for g in tensor.gears]
        self._dest = {}

    def destinations(self, L: int) -> list[np.ndarray]:
        cached = self._dest.get(L)
        if cached is None:
            lat = lattice(L)
            xyz = lat.all_coords()
            per_kind = {}
            for k in set(self.links):
                if self.S is None:
                    dest = np.arange(lat.N)
                else:
                    e = (0, 0, 0) if k is None else DIRECTIONS[2 * k]
                    t = [(self.S[i] - xyz[:, i] - e[i]) % L for i in range(3)]
                    dest = (t[0] * L + t[1]) * L + t[2]
                per_kind[k] = dest.astype(np.intp)
            cached = self._dest[L] = [per_kind[k] for k in self.links]
        return cached

    def __call__(self, state: State) -> State:
        if state.G != self.G:
            raise ValueError("state does not match the tensor")
        dest = self.destinations(state.L)
        a, b, r = np.empty_like(state.a), np.empty_like(state.b), np.empty_like(state.r)
        for g in range(self.G):
            a[g, dest[g]] = state.a[g]
            b[g, dest[g]] = state.b[g]
            r[g, dest[g]] = state.r[g]
        return State._raw(state.L, a, b, r)


def identity_map(tensor: Tensor) -> SpatialMap:
    return SpatialMap(tensor, None, "identity")


def inversion_about_node(tensor: Tensor, x0=(0, 0, 0)) -> SpatialMap:
    return SpatialMap(tensor, tuple(2 * v for v in x0), f"P_node{tuple(x0)}")


def inversion_about_cube_centre(tensor: Tensor, x0=(0, 0, 0)) -> SpatialMap:
    return SpatialMap(tensor, tuple(2 * v + 1 for v in x0), f"P_cube{tuple(x0)}+1/2")


def inversion_about_box_centre(tensor: Tensor, L: int) -> SpatialMap:
    return SpatialMap(tensor, (L - 1, L - 1, L - 1), f"P_box(L={L})")


# ------------------------------------------------------------------------------------------- (d), (e) checkers
def reversor_check(X: Callable[[State], State], F, states: Iterable[State], n: int,
                   central: Sequence[tuple[str, Callable[[State], State]]] = ()) -> dict:
    """Count X F^n X F^n (s) == s ("identity"), == Z(s) for a declared central map ("central"), else "failures".
    F is an Engine (its .step is used) or a callable state -> state."""
    step = F.step if hasattr(F, "step") else F
    out = {"n": n, "states": 0, "identity": 0, "central": {name: 0 for name, _ in central}, "failures": 0}
    for s in states:
        t = s
        for _ in range(n):
            t = step(t)
        t = X(t)
        for _ in range(n):
            t = step(t)
        t = X(t)
        out["states"] += 1
        if t.same_as(s):
            out["identity"] += 1
            continue
        for name, Z in central:
            if t.same_as(Z(s)):
                out["central"][name] += 1
                break
        else:
            out["failures"] += 1
    out["ok"] = out["failures"] == 0
    return out


def is_fixed(X: Callable[[State], State], state: State) -> bool:
    return X(state).same_as(state)
