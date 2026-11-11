"""Integer field and constraint preparation helpers. Former calibrated load/light and rounded clock presets are explicitly retired. No function runs the update."""
from __future__ import annotations

import math

import numpy as np

from ..core.engine import OBJ, State
from ..core.lattice import lattice

AXES = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
SPATIAL = ("x", "y", "z")


def _arrays(state: State):
    return state.a.astype(OBJ).copy(), state.b.astype(OBJ).copy(), state.r.astype(OBJ).copy()


def clock_w0(mu: int, carrier_sign: int = 1) -> float:
    """Vacuum frequency of an on-site clock u = +-6 b -+ mu b: cos w0 = 1 - mu/(6) (carrier 6); for the
    pi-carrier gear the envelope has the same w0 (b = (-1)^t c)."""
    return math.acos(1 - mu / (6))


def set_gear(a, b, tensor, name, L, xyz, va, vb):
    g = tensor.gear_index(name)
    n = lattice(L).index(*xyz)
    if any(type(v) is bool or not isinstance(v, (int, np.integer)) for v in (va,vb)):
        raise TypeError("gear data must be exact integers")
    a[g, n], b[g, n] = int(va), int(vb)


def ball(L, centre, radius):
    """Nodes within Euclidean distance <= radius of centre (periodic, minimal image), with their distances."""
    out = []
    R = int(math.ceil(radius))
    for dx in range(-R, R + 1):
        for dy in range(-R, R + 1):
            for dz in range(-R, R + 1):
                d = math.sqrt(dx * dx + dy * dy + dz * dz)
                if d <= radius + 1e-12:
                    out.append((((centre[0] + dx) % L, (centre[1] + dy) % L, (centre[2] + dz) % L), d))
    return out


def with_load(state: State, tensor, ns: str, mu: int, centre, radius: float, amp: int, anti: bool = False,
              profile: str = "smooth") -> State:
    """Retired rounded or scale-dependent preset; use explicit integer initial data."""
    raise NotImplementedError("This initial-data preset is retired; supply explicit integer initial data")


def with_clocks(state: State, tensor, gear: str, mu: int, positions, amp: int, phase: float = 0.0) -> State:
    """Retired rounded or scale-dependent preset; use explicit integer initial data."""
    raise NotImplementedError("This initial-data preset is retired; supply explicit integer initial data")


def light_dispersion(k: float) -> float:
    """Retired initial-data formula; no fixed-divisor replacement is established."""
    raise NotImplementedError("This preparation depended on the removed divisor scale; supply explicit integer initial data instead")


def with_light_pulse(state: State, tensor, gear: str, x0, axis: int, k: float, sigma: float, amp: int,
                     transverse: float | None = None, direction: int = 1) -> State:
    """Retired initial-data formula; no fixed-divisor replacement is established."""
    raise NotImplementedError("This preparation depended on the removed divisor scale; supply explicit integer initial data instead")


def od2_prepare_constraints(state: State, tensor, ns: str) -> State:
    """Constraint-satisfying accumulator data (S4 C1): set a(h0i) = b(h0i) + Div_i(a(hij)) and
    a(h00) = b(h00) + Div_0(a(h0i)) so that C^i(-1) = C^0(-1) = 0; the accumulators keep them 0 exactly."""
    a, b, r = _arrays(state)
    L = state.L
    T = tensor

    def get(arrx, n):
        return arrx[T.gear_index(f"{ns}.{n}")].reshape(L, L, L)

    def sh(X, off):
        out = X
        for ax, o in enumerate(off):
            if o:
                out = np.roll(out, -o, axis=ax)
        return out

    def hij(i, j):
        x, y = sorted((i, j))
        return get(a, "h" + SPATIAL[x] + SPATIAL[y])
    for i in range(3):
        d = sh(hij(i, i), AXES[i]) - hij(i, i)
        for j in range(3):
            if j != i:
                d = d + hij(j, i) - sh(hij(j, i), tuple(-v for v in AXES[j]))
        gi = T.gear_index(f"{ns}.h0{SPATIAL[i]}")
        a[gi] = (b[gi].reshape(L, L, L) + d).reshape(-1)
    div0 = 0
    for i in range(3):
        X = a[T.gear_index(f"{ns}.h0{SPATIAL[i]}")].reshape(L, L, L)
        div0 = div0 + X - sh(X, tuple(-v for v in AXES[i]))
    g0 = T.gear_index(f"{ns}.h00")
    a[g0] = (b[g0].reshape(L, L, L) + div0).reshape(-1)
    return State(L, a, b, r)


def static_field(L: int, source: np.ndarray) -> np.ndarray:
    """Retired initial-data formula; no fixed-divisor replacement is established."""
    raise NotImplementedError("This preparation depended on the removed divisor scale; supply explicit integer initial data instead")


def with_field(state: State, tensor, gear: str, F: np.ndarray) -> State:
    """Set a gear to a static configuration: a = b = F (MECHANISM preparation of a settled field)."""
    a, b, r = _arrays(state)
    g = tensor.gear_index(gear)
    flat = np.asarray(F, dtype=object).reshape(-1)
    a[g] = flat.copy()
    b[g] = flat.copy()
    return State(state.L, a, b, r)


def load_source(state: State, tensor, ns: str, mu: int, P: int, anti: bool = False) -> np.ndarray:
    """The lapse source of a load pair block, (mu/(2P)) (X^2 + Y^2) (negative for the pi-carrier anti-load), as an
    (L, L, L) object array (exact), computed from the initial data."""
    L = state.L
    X = state.b[tensor.gear_index(f"{ns}.X")].astype(object).reshape(L, L, L)
    Y = state.b[tensor.gear_index(f"{ns}.Y")].astype(object).reshape(L, L, L)
    if type(mu) is not int or type(P) is not int or P <= 0 or mu % (2 * P):
        raise ValueError("source coefficient mu/(2P) must be an exact integer")
    c = (mu // (2 * P)) * (-1 if anti else 1)
    return c * (X * X + Y * Y)


def with_static_load(state: State, tensor, ns: str, centre, radius: float, amp: int) -> State:
    """Retired rounded or scale-dependent preset; use explicit integer initial data."""
    raise NotImplementedError("This initial-data preset is retired; supply explicit integer initial data")


def static_load_source(state: State, tensor, ns: str, coeff: int) -> np.ndarray:
    L = state.L
    n = state.b[tensor.gear_index(f"{ns}.n")].astype(object).reshape(L, L, L)
    return coeff * n * n
