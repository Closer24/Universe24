"""Generic exact Rule3 gear engine for ONE divisor D = 6Q and ONE tensor (core/tensor.py).

The only state-changing primitive, applied to every gear of every node from the SAME previous complete snapshot:

    K = 2u,   ell, r' = divmod(K + r, D),   a' = b,   b' = ell - a

with u the tensor polynomial (core/tensor.py). There is no branch on gear names, labels, links or blocks: the
engine sees only integer arrays. Exactness: numpy int64 is used only when an exact Python-int bound on |K + r| (from
per-gear maxima and the absolute coefficients) is below 2^62; otherwise the same step runs on Python ints (numpy
object arrays). No floating point anywhere.

Also here (audit / readout, never stages of the forward evolution):
* ``inverse_step``: staged exact inverse (old b = new a; stage by stage r = (r' - K) mod D, ell = (K + r - r')/D,
  old a = ell - b'), in the a-read order of ``Tensor.stages``;
* ``mirror``: per gear M(a, b, r) = (b, a, D - 1 - r);
* ``clicks``: passive click readout from two snapshots (see ``ClickLog``).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .lattice import Lattice, OFFSETS, lattice as _lattice
from .tensor import Tensor

LIMIT = 1 << 62
I64 = np.dtype(np.int64)
OBJ = np.dtype(object)

KIND_NAMES = ("C0", "C1", "C2")


# ======================================================================== exact arrays
def _maxabs(arr: np.ndarray) -> int:
    """Exact max |x| as a Python int. Never np.abs on int64: np.abs(int64(-2^63)) is -2^63 (stage 0.1 fix)."""
    if arr.size == 0:
        return 0
    return max(int(arr.max()), -int(arr.min()))


def exact_array(values, shape=None) -> np.ndarray:
    """Integer array: int64 if every |x| < 2^62, else Python ints in an object array. Rejects floats and bools.
    Non-array input (nested lists/tuples) is read as Python ints (object dtype), never float-inferred by numpy."""
    arr = values if isinstance(values, np.ndarray) else np.array(values, dtype=OBJ)
    if arr.dtype == OBJ:
        flat = arr.ravel()
        for v in flat:
            if type(v) is not int:
                if isinstance(v, np.integer):
                    continue
                raise TypeError(f"exact integers only, got {type(v).__name__}")
        arr = np.array([int(v) for v in flat], dtype=OBJ).reshape(arr.shape)
        if _maxabs(arr) < LIMIT:
            arr = arr.astype(I64)
    elif arr.dtype.kind in "iu":
        if _maxabs(arr) >= LIMIT:
            arr = np.array([int(v) for v in arr.ravel()], dtype=OBJ).reshape(arr.shape)
        else:
            arr = arr.astype(I64)
    else:
        raise TypeError(f"exact integers only, got dtype {arr.dtype}")
    if shape is not None and arr.shape != tuple(shape):
        raise ValueError(f"expected shape {tuple(shape)}, got {arr.shape}")
    return arr


def _maxabs_rows(arr: np.ndarray) -> list[int]:
    """Exact per-row max |x| (Python ints), via max and min (see _maxabs)."""
    if arr.shape[1] == 0:
        return [0] * arr.shape[0]
    return [max(int(hi), -int(lo)) for hi, lo in zip(arr.max(axis=1), arr.min(axis=1))]


def _fits(arr: np.ndarray) -> bool:
    return _maxabs(arr) < LIMIT


def _cast(arr: np.ndarray, dtype) -> np.ndarray:
    return arr if arr.dtype == dtype else arr.astype(dtype)


# ======================================================================== state
class State:
    """Complete state: arrays a, b, r of shape (G, L**3) (gear type, flat node index), exact integers."""

    __slots__ = ("L", "a", "b", "r")

    def __init__(self, L: int, a, b, r):
        lat = _lattice(L)
        a = exact_array(a)
        if a.ndim != 2 or a.shape[1] != lat.N:
            raise ValueError(f"expected arrays of shape (G, {lat.N})")
        self.L = L
        self.a = a
        self.b = exact_array(b, a.shape)
        self.r = exact_array(r, a.shape)

    @classmethod
    def _raw(cls, L: int, a: np.ndarray, b: np.ndarray, r: np.ndarray) -> "State":
        """Internal constructor without re-validation (arrays produced by the engine itself)."""
        s = object.__new__(cls)
        s.L, s.a, s.b, s.r = L, a, b, r
        return s

    @property
    def G(self) -> int:
        return self.a.shape[0]

    @property
    def N(self) -> int:
        return self.a.shape[1]

    @property
    def lattice(self) -> Lattice:
        return _lattice(self.L)

    def copy(self) -> "State":
        return State._raw(self.L, self.a.copy(), self.b.copy(), self.r.copy())

    def same_as(self, other: "State") -> bool:
        """Exact equality of every retained component (dtype-agnostic)."""
        return (isinstance(other, State) and other.L == self.L and other.a.shape == self.a.shape
                and bool(np.array_equal(self.a, other.a)) and bool(np.array_equal(self.b, other.b))
                and bool(np.array_equal(self.r, other.r)))

    def gear(self, g: int, n: int) -> tuple[int, int, int]:
        return (int(self.a[g, n]), int(self.b[g, n]), int(self.r[g, n]))

    def max_abs(self) -> int:
        return max(max(_maxabs_rows(self.a), default=0), max(_maxabs_rows(self.b), default=0))

    def to_dict(self) -> dict:
        return {"L": self.L,
                "a": [[int(v) for v in row] for row in self.a],
                "b": [[int(v) for v in row] for row in self.b],
                "r": [[int(v) for v in row] for row in self.r]}

    @classmethod
    def from_dict(cls, data: dict) -> "State":
        return cls(data["L"], np.array(data["a"], dtype=OBJ), np.array(data["b"], dtype=OBJ),
                   np.array(data["r"], dtype=OBJ))


# ======================================================================== compiled tensor
class _Plan:
    """Vectorised evaluation of u for a subset of monomials on one lattice."""

    def __init__(self, tensor: Tensor, monomials, lat: Lattice):
        self.G = tensor.G
        self.N = lat.N
        rows: dict[tuple[int, int, int], int] = {}            # (field 0=a/1=b, gear, offset index) -> row
        for m in monomials:
            for f in m.factors:
                key = (1 if f.field == "b" else 0, f.gear, OFFSETS.index(f.offset))
                if key not in rows:
                    rows[key] = len(rows)
        self.S = len(rows)
        groups: dict[tuple[int, int], tuple[list, list]] = {}
        for (fid, gear, oi), row in rows.items():
            gr = groups.setdefault((fid, oi), ([], []))
            gr[0].append(row)
            gr[1].append(gear)
        self.gathers = [(fid, np.array(rws, dtype=np.intp), np.array(gs, dtype=np.intp), lat.shift_index(OFFSETS[oi]))
                        for (fid, oi), (rws, gs) in sorted(groups.items())]
        self.src_field = np.zeros(self.S, dtype=np.intp)
        self.src_gear = np.zeros(self.S, dtype=np.intp)
        for (fid, gear, oi), row in rows.items():
            self.src_field[row] = fid
            self.src_gear[row] = gear
        self.degree_groups = []
        targets_all = set()
        for k in range(4):
            ms = sorted((m for m in monomials if m.degree == k), key=lambda m: m.target)
            if not ms:
                continue
            tg = np.array([m.target for m in ms], dtype=np.intp)
            targets_all.update(tg.tolist())
            starts = np.flatnonzero(np.r_[True, tg[1:] != tg[:-1]]).astype(np.intp)
            utg = tg[starts]
            segs = [(int(t), int(s0), int(s1)) for t, s0, s1 in zip(utg, starts, np.r_[starts[1:], len(ms)])]
            coeff_obj = np.array([m.coeff for m in ms], dtype=OBJ)
            fits = all(abs(m.coeff) < LIMIT for m in ms)
            coeff_i64 = coeff_obj.astype(I64) if fits else None
            fac = np.array([[rows[(1 if f.field == "b" else 0, f.gear, OFFSETS.index(f.offset))] for f in m.factors]
                            for m in ms], dtype=np.intp).reshape(len(ms), k)
            self.degree_groups.append((k, fac, starts, utg, coeff_i64, coeff_obj, np.abs(coeff_obj), segs))
        self.targets = np.array(sorted(targets_all), dtype=np.intp)
        self.coeffs_fit = all(g[4] is not None for g in self.degree_groups)

    def bound(self, maxabs_a: list[int], maxabs_b: list[int]) -> int:
        """Exact Python-int bound on max_t |u_t| (every partial product and partial sum is below it, too)."""
        if not self.degree_groups:
            return 0
        M = np.array([max(1, (maxabs_b if fid else maxabs_a)[g]) for fid, g in zip(self.src_field, self.src_gear)],
                     dtype=OBJ)
        tot = np.zeros(self.G, dtype=OBJ)
        for k, fac, starts, utg, _ci, _co, cabs, _segs in self.degree_groups:
            tb = cabs.copy()
            for j in range(k):
                tb = tb * M[fac[:, j]]
            tot[utg] += np.add.reduceat(tb, starts)
        return int(max(tot))

    def evaluate(self, a: np.ndarray, b: np.ndarray, dtype) -> np.ndarray:
        """u of shape (G, N); rows that are no target of this plan are 0."""
        u = np.zeros((self.G, self.N), dtype=dtype)
        if self.S:
            X = np.empty((self.S, self.N), dtype=dtype)
            for fid, rws, gs, idx in self.gathers:
                F = b if fid else a
                X[rws] = F[np.ix_(gs, idx)]
        for k, fac, _starts, _utg, ci, co, _cabs, segs in self.degree_groups:
            c = ci if dtype == I64 else co
            if k == 0:
                for t, s0, s1 in segs:
                    u[t] += sum(int(v) for v in co[s0:s1])
                continue
            vals = X[fac[:, 0]]
            for j in range(1, k):
                vals = vals * X[fac[:, j]]
            vals = vals * c[:, None]
            for t, s0, s1 in segs:                       # per-target segment sums (rows sorted by target)
                u[t] += vals[s0:s1].sum(axis=0)
        return u


class _Compiled:
    def __init__(self, tensor: Tensor, lat: Lattice):
        self.forward = _Plan(tensor, tensor.monomials, lat)
        self.stages = []
        for stage in tensor.stages:
            ss = set(stage)
            plan = _Plan(tensor, [m for m in tensor.monomials if m.target in ss], lat)
            self.stages.append((plan, np.array(stage, dtype=np.intp)))


# ======================================================================== clicks (passive readout)
@dataclass(frozen=True)
class ClickLog:
    """Passive readout of one update (before -> after). Never fed back into the dynamics.

    Columns (one row per gear instance): ``gear`` (type index), ``node`` (flat index), ``kind`` (0 = C0, 1 = C1,
    2 = C2), ``quotient`` (= after.b + before.a = ell), ``changed`` (triple changed), ``label`` (the gear type's
    readout label, "official" or "audit"). ``stream`` is "official" (click iff quotient != 0 AND the triple changed:
    the Q=1 arithmetic convention) or "raw" (every ell != 0, NON-OFFICIAL).
    Rows are sorted by (x, y, z, gear), lexicographic event order.
    """
    step: int
    L: int
    stream: str
    gear: np.ndarray
    node: np.ndarray
    kind: np.ndarray
    quotient: np.ndarray
    changed: np.ndarray
    label: tuple

    def __len__(self):
        return len(self.gear)

    def rows(self) -> list[tuple]:
        lat = _lattice(self.L)
        return [(self.step, lat.coords(int(n)), int(g), int(k), int(q), lab)
                for g, n, k, q, lab in zip(self.gear, self.node, self.kind, self.quotient, self.label)]

    def select(self, label: str) -> "ClickLog":
        keep = np.array([lab == label for lab in self.label], dtype=bool)
        return ClickLog(self.step, self.L, self.stream, self.gear[keep], self.node[keep], self.kind[keep],
                        self.quotient[keep], self.changed[keep], tuple(l for l, k in zip(self.label, keep) if k))


def handedness_kind(delta_mod_D: np.ndarray, D: int) -> np.ndarray:
    """kind of a turn delta = (r' - r) mod D taken in (-D/2, D/2]: C0 if delta in {0, D/2}, C1 if 0 < delta < D/2,
    C2 if -D/2 < delta < 0 (CLICK_TAXONOMY section 1; for D = 6 equal to ((r' - r)//2) mod 3)."""
    half = D // 2
    d = delta_mod_D
    return np.where((d == 0) | (d == half), 0, np.where(d < half, 1, 2)).astype(np.int64)


def extract_clicks(tensor: Tensor, D: int, before: State, after: State, step: int = 1,
                   stream: str = "official") -> ClickLog:
    if stream not in ("official", "raw"):
        raise ValueError("stream must be 'official' or 'raw' (raw = every ell != 0, non-official)")
    if before.a.shape != after.a.shape or before.L != after.L:
        raise ValueError("snapshots of different shape")
    big = not all(_fits(x) for x in (before.a, after.b))
    quot = (_cast(after.b, OBJ) + _cast(before.a, OBJ)) if big else after.b + before.a
    changed = (before.a != after.a) | (before.b != after.b) | (before.r != after.r)
    hit = np.asarray(quot != 0, dtype=bool)
    if stream == "official":
        hit &= np.asarray(changed, dtype=bool)
    # order rows by (node, gear) == (x, y, z, gear)
    node_idx, gear_idx = np.nonzero(hit.T)
    # Reloading small remainders compacts them to int64 even when D is much
    # larger. Cast before subtracting/modulo so readout is storage-independent.
    r_dtype = OBJ if D >= LIMIT else I64
    delta = (_cast(after.r[gear_idx, node_idx], r_dtype)
             - _cast(before.r[gear_idx, node_idx], r_dtype)) % D
    kind = handedness_kind(delta, D)
    labels = tensor.labels
    return ClickLog(step, before.L, stream, gear_idx, node_idx, kind, quot[gear_idx, node_idx],
                    np.asarray(changed, dtype=bool)[gear_idx, node_idx], tuple(labels[g] for g in gear_idx))


# ======================================================================== engine
class Engine:
    """Rule3 on every gear, one divisor D = 6Q, one tensor. No physics, no per-type branch."""

    def __setattr__(self, name, value):
        if name in ("tensor", "Q", "D") and hasattr(self, name):
            raise AttributeError("Engine law is fixed; construct a new engine before a run")
        object.__setattr__(self, name, value)

    def __delattr__(self, name):
        if name in ("tensor", "Q", "D"):
            raise AttributeError("Engine law is fixed")
        object.__delattr__(self, name)

    def __init__(self, tensor: Tensor, Q: int = 1):
        if not isinstance(tensor, Tensor):
            raise TypeError("expected a validated Tensor")
        if type(Q) is not int or Q < 1:
            raise ValueError("Q must be a positive int (D = 6Q)")
        if tensor.Q is not None and tensor.Q != Q:
            raise ValueError(f"ONE divisor: the tensor was built with Q = {tensor.Q}, the engine was given Q = {Q}")
        self.tensor = tensor
        self.Q = Q
        self.D = 6 * Q
        self._compiled: dict[int, _Compiled] = {}
        self.stats = {"int64_steps": 0, "pyint_steps": 0, "inverse_int64_steps": 0, "inverse_pyint_steps": 0}

    def _comp(self, L: int) -> _Compiled:
        c = self._compiled.get(L)
        if c is None:
            c = self._compiled[L] = _Compiled(self.tensor, _lattice(L))
        return c

    def _check(self, state: State):
        if not isinstance(state, State):
            raise TypeError("expected a State")
        if state.G != self.tensor.G:
            raise ValueError(f"state has {state.G} gear types, tensor has {self.tensor.G}")
        if state.r.size and (int(state.r.min()) < 0 or int(state.r.max()) >= self.D):
            raise ValueError("remainders must lie in 0..D-1")

    # ------------------------------------------------------------------ forward
    def inputs(self, state: State) -> np.ndarray:
        """u of every gear (read-only diagnostic), exact."""
        self._check(state)
        plan = self._comp(state.L).forward
        dtype = self._dtype(plan, state.a, state.b, [state.r])
        return plan.evaluate(_cast(state.a, dtype), _cast(state.b, dtype), dtype)

    def _dtype(self, plan: _Plan, a, b, extra) -> np.dtype:
        if not plan.coeffs_fit or self.D >= LIMIT // 8:
            return OBJ
        ma, mb = _maxabs_rows(a), _maxabs_rows(b)
        if max(ma + mb, default=0) >= LIMIT or not all(_fits(x) for x in extra):
            return OBJ
        return I64 if 2 * plan.bound(ma, mb) + 2 * self.D < LIMIT else OBJ

    def step(self, state: State) -> State:
        """One synchronous update of every gear from the same previous snapshot."""
        self._check(state)
        plan = self._comp(state.L).forward
        dtype = self._dtype(plan, state.a, state.b, [state.r])
        self.stats["int64_steps" if dtype == I64 else "pyint_steps"] += 1
        a, b, r = _cast(state.a, dtype), _cast(state.b, dtype), _cast(state.r, dtype)
        t = 2 * plan.evaluate(a, b, dtype) + r
        ell = t // self.D
        return State._raw(state.L, b.copy(), ell - a, t - ell * self.D)

    def run(self, state: State, steps: int, history: bool = False):
        if type(steps) is not int or steps < 0:
            raise ValueError("steps must be a non-negative int")
        out = [state] if history else None
        for _ in range(steps):
            state = self.step(state)
            if history:
                out.append(state)
        return out if history else state

    # ------------------------------------------------------------------ audit maps
    def inverse_step(self, state: State) -> State:
        """Staged exact inverse (audit / recovery only)."""
        self._check(state)
        comp = self._comp(state.L)
        D = self.D
        dtype = I64 if (all(_fits(x) for x in (state.a, state.b)) and D < LIMIT // 8
                        and all(p.coeffs_fit for p, _ in comp.stages)) else OBJ
        b_old = _cast(state.a, dtype).copy()
        a_old = np.zeros_like(b_old)
        r_old = np.zeros_like(b_old)
        mb = _maxabs_rows(b_old)
        for plan, targets in comp.stages:
            if dtype == I64:
                ma = _maxabs_rows(a_old)
                if not 2 * plan.bound(ma, mb) + 2 * D < LIMIT:
                    dtype = OBJ
                    b_old, a_old, r_old = b_old.astype(OBJ), a_old.astype(OBJ), r_old.astype(OBJ)
            u = plan.evaluate(a_old, b_old, dtype)
            K = 2 * u[targets]
            rn = _cast(state.r[targets], dtype)
            bn = _cast(state.b[targets], dtype)
            ro = (rn - K) % D
            ell = (K + ro - rn) // D
            a_old[targets] = ell - bn
            r_old[targets] = ro
        self.stats["inverse_int64_steps" if dtype == I64 else "inverse_pyint_steps"] += 1
        return State._raw(state.L, a_old, b_old, r_old)

    def rewind(self, state: State, steps: int) -> State:
        if type(steps) is not int or steps < 0:
            raise ValueError("steps must be a non-negative int")
        for _ in range(steps):
            state = self.inverse_step(state)
        return state

    def mirror(self, state: State) -> State:
        """M(a,b,r)=(b,a,D-1-r); a reversor for b-only inputs, not general old-a tensors."""
        self._check(state)
        r = _cast(state.r, OBJ if self.D >= LIMIT else I64)
        return State._raw(state.L, state.b.copy(), state.a.copy(), (self.D - 1) - r)

    # ------------------------------------------------------------------ preparation helpers (initial data only)
    def vacuum(self, L: int, r0) -> State:
        """All gears at (0, 0, r0[type]); r0 is a dict name -> remainder or a sequence over gear types."""
        lat = _lattice(L)
        G = self.tensor.G
        if isinstance(r0, dict):
            vals = [r0[name] for name in self.tensor.names]
        else:
            vals = list(r0)
        if len(vals) != G or any(type(v) is not int or not 0 <= v < self.D for v in vals):
            raise ValueError("need one remainder 0..D-1 per gear type")
        r = np.repeat(np.array(vals, dtype=OBJ)[:, None], lat.N, axis=1)
        z = np.zeros((G, lat.N), dtype=OBJ)
        return State(L, z, z.copy(), r)

    # ------------------------------------------------------------------ passive readout
    def clicks(self, before: State, after: State, step: int = 1, stream: str = "official") -> ClickLog:
        return extract_clicks(self.tensor, self.D, before, after, step, stream)
