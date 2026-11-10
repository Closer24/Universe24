"""INITIAL DATA ONLY for the gravity layer (AGENTS item 9): builders of preparations (static load, atom clocks, light
pulses, constraint-satisfying accumulator data). Nothing here runs the engine or touches a running state. Every
gear value is an exact Python int; floats are used only to compute the rounded INITIAL numbers (preparation)."""
from __future__ import annotations

import math

import numpy as np

from ..core.engine import OBJ, State
from ..core.lattice import lattice

AXES = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
SPATIAL = ("x", "y", "z")


def _arrays(state: State):
    return state.a.astype(OBJ).copy(), state.b.astype(OBJ).copy(), state.r.astype(OBJ).copy()


def clock_w0(Q: int, mu: int, carrier_sign: int = 1) -> float:
    """Vacuum frequency of an on-site clock u = +-6Q b -+ mu b: cos w0 = 1 - mu/(6Q) (carrier 6Q); for the
    pi-carrier gear the envelope has the same w0 (b = (-1)^t c)."""
    return math.acos(1 - mu / (6 * Q))


def set_gear(a, b, tensor, name, L, xyz, va, vb):
    g = tensor.gear_index(name)
    n = lattice(L).index(*xyz)
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


def with_load(state: State, tensor, ns: str, Q: int, mu: int, centre, radius: float, amp: int, anti: bool = False,
              profile: str = "smooth") -> State:
    """Circulating clock pairs (X, Y) on a ball (MECHANISM preparation of a static load): X = A cos(w0 t),
    Y = A sin(w0 t) (anti: times (-1)^t, the pi-carrier pair), so X^2 + Y^2 = A^2 at the start; A(d) =
    amp (1 - d^2/R'^2), R' = radius + 1 ('smooth') or amp ('flat')."""
    a, b, r = _arrays(state)
    L = state.L
    w0 = clock_w0(Q, mu)
    for xyz, d in ball(L, centre, radius):
        A = amp * (1 - (d / (radius + 1)) ** 2) if profile == "smooth" else amp
        A = int(round(A))
        sgn = -1 if anti else 1
        set_gear(a, b, tensor, f"{ns}.X", L, xyz, sgn * round(A * math.cos(w0)), A)
        set_gear(a, b, tensor, f"{ns}.Y", L, xyz, sgn * round(-A * math.sin(w0)), 0)
    return State(L, a, b, r)


def with_clocks(state: State, tensor, gear: str, Q: int, mu: int, positions, amp: int, phase: float = 0.0) -> State:
    """On-site test clocks at the given nodes: b = A cos(phase), a = A cos(phase - w0) (vacuum frequency)."""
    a, b, r = _arrays(state)
    w0 = clock_w0(Q, mu)
    for xyz in positions:
        set_gear(a, b, tensor, gear, state.L, xyz, round(amp * math.cos(phase - w0)), round(amp * math.cos(phase)))
    return State(state.L, a, b, r)


def light_dispersion(Q: int, k: float) -> float:
    """Frequency of the headroom light along an axis: cos w = 1 - ((Q-1)/(3Q)) (1 - cos k)."""
    return math.acos(1 - (Q - 1) / (3 * Q) * (1 - math.cos(k)))


def with_light_pulse(state: State, tensor, gear: str, Q: int, x0, axis: int, k: float, sigma: float, amp: int,
                     transverse: float | None = None, direction: int = 1) -> State:
    """A light packet moving along +axis (direction=+1) or -axis: b = A env cos(k s), a = A env(s + v) cos(k s + w)
    with s the coordinate along the axis relative to x0 (periodic minimal image), env Gaussian (sigma) times an
    optional transverse Gaussian (plane-like front when transverse is None)."""
    a, b, r = _arrays(state)
    L = state.L
    w = light_dispersion(Q, k)
    v = (Q - 1) / (3 * Q) * math.sin(k) / math.sin(w)        # group velocity
    xyz = lattice(L).all_coords()
    g = tensor.gear_index(gear)
    for n, (x, y, z) in enumerate(xyz):
        rel = [((c - c0 + L // 2) % L) - L // 2 for c, c0 in zip((x, y, z), x0)]
        s = rel[axis] * direction
        tr = 1.0
        if transverse is not None:
            tr = math.exp(-sum(rel[i] ** 2 for i in range(3) if i != axis) / (2 * transverse ** 2))
        env0 = math.exp(-s * s / (2 * sigma ** 2)) * tr
        envm = math.exp(-(s + v) ** 2 / (2 * sigma ** 2)) * tr
        b[g, n] = int(round(amp * env0 * math.cos(k * s)))
        a[g, n] = int(round(amp * envm * math.cos(k * s + w)))
    return State(L, a, b, r)


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


def static_field(L: int, Q: int, source: np.ndarray) -> np.ndarray:
    """Rounded static lattice solution of 2(Q-1) Lap F + 2 s = 0 on the torus for a given (L, L, L) source array
    (its mean is removed: a closed board has no static state with net source). Float FFT used ONLY to compute
    initial numbers (preparation); returns Python ints."""
    s = np.asarray(source, dtype=float)
    kk = 2 * np.pi * np.fft.fftfreq(L)
    lam = (2 * np.cos(kk)[:, None, None] + 2 * np.cos(kk)[None, :, None] + 2 * np.cos(kk)[None, None, :] - 6)
    lam[0, 0, 0] = 1.0
    Fk = np.fft.fftn(s - s.mean()) / ((Q - 1) * -lam)
    Fk[0, 0, 0] = 0
    F = np.real(np.fft.ifftn(Fk))
    return np.vectorize(lambda v: int(round(v)), otypes=[object])(F)


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
    c = (mu // (2 * P)) * (-1 if anti else 1)
    return c * (X * X + Y * Y)


def with_static_load(state: State, tensor, ns: str, centre, radius: float, amp: int) -> State:
    """Static density gear values n = A(d) = amp (1 - d^2/(radius+1)^2) on a ball, a = b = n (holds its value)."""
    a, b, r = _arrays(state)
    L = state.L
    for xyz, d in ball(L, centre, radius):
        A = int(round(amp * (1 - (d / (radius + 1)) ** 2)))
        set_gear(a, b, tensor, f"{ns}.n", L, xyz, A, A)
    return State(L, a, b, r)


def static_load_source(state: State, tensor, ns: str, coeff: int) -> np.ndarray:
    L = state.L
    n = state.b[tensor.gear_index(f"{ns}.n")].astype(object).reshape(L, L, L)
    return coeff * n * n
