"""ROUTE B (owner, 13:2x): exact LOCAL SU(2)_L x U(1)_Y electroweak block. DECLARED CANDIDATE, DEFAULT OFF until reviewed.

EW-BUILDER (HAND-M1). TENSOR BLOCKS ONLY. NEW file; no existing package file is modified (layers/chiral.py,
layers/electroweak.py, layers/system.py untouched). E1 is retired as a separate photon: the photon is the unbroken
combination of the U(2) link's W3 and B directions.

Fields per node (D = 6Q for every gear; deviation form; vacuum remainders 3Q - 1):
  matter, matter2   the doublet (two 16-channel Dirac pairs; layers/matter.build_matter, read-only). Doublet index = pair.
                    M2(C) acts through R(M) = Re M (x) 1_16 + Im M (x) J' (an exact real-algebra homomorphism,
                    R(M)^T = R(M^dagger)); t1 = R(EPS), t2 = R(i SX), t3 = R(i SZ) (layers/chiral.py), J'_32 = R(i 1).
  V<a>_<mu>         ONE U(2) link per face, 8 real gears: V = sum_mu v_mu E_mu, E = (1, EPS, iSX, iSZ, i, iEPS, -SX, -SZ).
  P<a><b>_<mu>      U(2) 2-path gears (one per ordered axis pair), the plaquette halves (B1-GAUGE construction in M2(C)).
  B<a>_re/_im       the charge-2 U(1) link LOCKED to det V (carries the e_R hop).
  X<a>_<c>          Xi  ~ V(x,a)^dagger col1(x)        (hybrid doublet; rank-3 lock)    } the charged Wilson-Yukawa
  Y<a>_<c>          Xi' ~ V(x,a) col1(x + e_a)         (hybrid doublet; rank-3 lock)    } at rank 3
  H_1, H_i, H_j, H_k  the Higgs quaternion; M(Phi) = R^-1(rho(Phi)) = (col1 | col2): col2 has Y = +1 (the lepton
                    doublet's), col1 has Y = -1.
Local gauge group G = g e^{i theta} in U(2) at every node:
  L doublet b_L -> R(G) b_L;  e_R -> det G e_R;  nu_R -> nu_R;  M(Phi) -> G M(Phi) diag(1/det G, 1);
  V(x,a) -> G(x) V G(x+e)^dagger;  P(x;a,b) -> G(x) P G(x+e_a+e_b)^dagger;  B(x,a) -> det G(x) B conj(det G(x+e));
  Xi(x,a) -> G(x+e) Xi / det G(x);  Xi'(x,a) -> G(x) Xi' / det G(x+e).
Physical potential (sum over x and the three axes a; <X, Y> = (1/2) Re Tr(X^dagger Y) = component dot product):
  matter (deviation parts; the vacuum parts are build_matter's own Wilson-Dirac entries, bit for bit):
    (kappa/2)  b(x+e)^T P_a R(W^dagger) Pi_W b(x)              L transport through V   (W = V - A1)
    (kappa_e/2) b(x+e)^T P_a R1(conj B~) Pi_S P1 b(x)          e_R transport through B  (B~ = B - B0)
    (ytot/2) b^T [rho(phi) Pi_W W0 + W0 Pi_W rho(phi)^T] b     on-site Yukawa (+ on-site Wilson), as layers/chiral.py
    -(w/2)  b(x+e)^T [rho(phi(x+e)) Pi_W W0 P2 + P2 W0 Pi_W rho(phi(x))^T] b(x)      nu Wilson-Yukawa (no link needed)
    -(w'/2) b(x+e)^T [R(C(Xi~(x,a))) Pi_W W0 P1 + P1 W0 Pi_W R(C(Xi'~(x,a)))^T] b(x) e   Wilson-Yukawa through the hybrids
  bosons (full physical form; deviation_terms removes D X0.X and asserts the vacuum is static):
    ((D - c_U - c_V)/2)|V|^2 - (lam/4) Tr((V^dag V - A^2)^2)    link inertia + OD4 MATRIX spring (contains |det V|^2)
    kappa_P <P(x;a,b), V(x,a) V(x+e_a,b)> + (c_P/2)|P|^2 + beta <P(a,b), P(b,a)>          2-path gears
    kH Re(col2(x)^dag V(x,a) col2(x+e)) - (cPhi/2)|Phi|^2 + (D/2)|Phi|^2 - (lam_H/4)(|Phi|^2 - v^2)^2   Higgs (+ OD4)
    kXi Re(Xi^dag V^dag col1(x)) + kXi Re(Xi'^dag V col1(x+e)) + ((D - M_Xi)/2)(|Xi|^2 + |Xi'|^2)       hybrid locks
    kB Re(conj(B) det V) + ((D - M_B)/2)|B|^2                                                 det-locked charge-2 link
Every term is rank <= 3 except the two OD4 springs. b-only, reciprocal (one potential), B3-local.
VACUUM (isotropic by construction): V0 = A 1, P0 = kappa_P A^2/(D - c_P - beta) 1, Phi0 = v 1, B0, Xi0 = Xi'0 = (xi0, 0).
  The Higgs hop pulls the NEUTRAL slot (col2 vev, slot 2) by kH v^2; the two hybrid locks pull the CHARGED slot (col1 vev,
  slot 1) by 2 kXi v xi0. With 2 kXi xi0 = kH v the pull is proportional to 1 (the -SZ component cancels exactly), so the
  isotropic balance c_V A = 2 kH v^2 + 2 kB B0 A keeps V0 = A 1: no distorted link vacuum, no cubic tuning, and the 2-path
  vacuum stays P0 1. xi0 = kXi A v/M_Xi, B0 = kB A^2/M_B, cPhi = 6 kH A + 6 kXi A xi0/v.
Defaults (Q = 2^33 + 1): A = v = 2^16, kH = 2^10, kXi = 2^13, M_Xi = 2^33 (xi0 = 2^12, w' = wilson/xi0 = 2^18),
  kB = 2^14, M_B = 2^30 (B0 = 2^16, kappa_e = hop/B0 = 2^15), lam = 2 (matrix spring: radial stiffness 4 lam A^2 = 2^35, the
  su2 block's), lam_H = 4, 2-paths kappa_P = 256, c_P = 0, beta = D - 2^33 (B1-GAUGE's regime: linearly stable, photon
  massless but FROZEN, v ~ 8e-4 c_Q). kappa_P = 2^17 (EM-C6b's propagating u1 regime) is linearly UNSTABLE for U(2) 2-paths
  (their Hermitian sector is tachyonic, h ~ -0.1 D): do not use.
OPTION plaquette=True (owner 14:37: "four links around one elementary plaquette, no matter factor"): no 2-paths; relays
  R(x;a,b) ~ V(x+e_a,b) with a difference lock -(M_R/2)|R - V(x+e_a,b)|^2 (R = V' statically: no pull, no balance) and the
  split plaquette -w ||V(x,a) R(x;a,b) - V(x,b) R(x;b,a)||^2 on site (B3: one node); w_B > 0 adds the det-shadow kinetic
  term: relays S(x;a,b) ~ B(x+e_a,b) and -w_B |B(x,a) S(x;a,b) - B(x,b) S(x;b,a)|^2. Exact covariance holds; but every relay
  is a full Rule3 gear (inertia D, ONE divisor), so the photon inertia is multiplied (link + 2 relay copies) and
  v_gamma ~ 0.33 c_Q at band-legal strengths (EWB6b); w > 1 breaks the band edge without a corner counter-term (OPEN).
  corner_form="sym4" is ONE-LIGHT-A's symmetric split plaquette, (w/2)(four corners) - 2w <V_a R_ab, V_b R_ba>, all on site
  through relays: best band-legal photon 0.408 c_Q (EWB6c: M_R = 2^34, w = w_B = 1, lam = 1). CEILING c_Q/sqrt(3) even for
  ideal relays (inertia x3): ONE light on c_Q is NOT reached under B3 + one divisor (declared OPEN; NOTES_electroweak_b.md).
Declared limitations: graviweak couplings are NOT included (Study 18: the norm couplings make the uniform lapse tachyonic,
  and the covariant dressing of the e_R hop / fermion mass is below the integer grain at P = 2^20); the composed system
  therefore leaves the doublet without a lapse coupling (OPEN). The photon speed is whatever the 2-path regime gives
  (no Wilson plaquette at rank <= 3: ONE-LIGHT finals); one light on c_Q is NOT claimed.
"""
from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

from ..core.tensor import Block, GearType
from .chiral import HIGGS, HOP, MASS, Q_DEFAULT, WILSON, build_partner, chiral_algebra
from .gauge import Poly, deviation_terms
from .matter import algebra as pair_algebra, matter_names

EWB_DEFAULT_ON = False
AXES = ("x", "y", "z")
ZERO = (0, 0, 0)
UNIT = ((1, 0, 0), (0, 1, 0), (0, 0, 1))

# ------------------------------------------------------------------------------------------------ M2(C) structure
_I2 = np.eye(2, dtype=complex)
_EPS = np.array([[0, 1], [-1, 0]], dtype=complex)        # layers/chiral.py EPS (t1 = R(EPS))
_SX = np.array([[0, 1], [1, 0]], dtype=complex)
_SZ = np.array([[1, 0], [0, -1]], dtype=complex)
BASIS = (_I2, _EPS, 1j * _SX, 1j * _SZ, 1j * _I2, 1j * _EPS, -_SX, -_SZ)
COMP = ("1", "e", "x", "z", "i", "ie", "mx", "mz")         # gear-name suffixes of the 8 link components
DCOMP = ("ur", "ui", "dr", "di")                          # doublet components (up/down, re/im)
GEN = {"t1": _EPS, "t2": 1j * _SX, "t3": 1j * _SZ, "Y": 1j * _I2}   # anti-Hermitian generators (Y in doublet units)


def r32(M) -> np.ndarray:
    """Real 32x32 doublet representation R(M) = Re M (x) 1_16 + Im M (x) J'_16 (integer for Gaussian-integer M)."""
    Jp = pair_algebra("pair")["Jp"]
    E16 = np.eye(16, dtype=np.int64)
    re = np.rint(np.real(M)).astype(np.int64)
    im = np.rint(np.imag(M)).astype(np.int64)
    return np.kron(re, E16) + np.kron(im, Jp)


def m2c_coords(M) -> list:
    """Real coordinates of a complex 2x2 matrix in BASIS (exact for Gaussian-integer entries)."""
    a, b, c, d = M[0, 0], M[0, 1], M[1, 0], M[1, 1]
    # E0 = 1, E1 = EPS, E2 = iSX, E3 = iSZ, E4 = i, E5 = iEPS, E6 = -SX, E7 = -SZ
    v0 = (a.real + d.real) / 2
    v7 = -(a.real - d.real) / 2
    v4 = (a.imag + d.imag) / 2
    v3 = (a.imag - d.imag) / 2
    v1 = (b.real - c.real) / 2
    v6 = -(b.real + c.real) / 2
    v5 = (b.imag - c.imag) / 2
    v2 = (b.imag + c.imag) / 2
    return [v0, v1, v2, v3, v4, v5, v6, v7]


def _check_basis():
    for mu, E in enumerate(BASIS):
        co = m2c_coords(E)
        assert all(abs(co[n] - (1 if n == mu else 0)) < 1e-12 for n in range(8)), mu
    t = chiral_algebra()["t"]
    assert np.array_equal(r32(_EPS), t[0]) and np.array_equal(r32(1j * _SX), t[1]) and np.array_equal(r32(1j * _SZ), t[2])
    return True


# ------------------------------------------------------------------------------------------------ complex polynomials
class Cx:
    """Complex number with Poly (or rational) real and imaginary parts (construction-time only)."""
    __slots__ = ("re", "im")

    def __init__(self, re, im=0):
        self.re = re if isinstance(re, Poly) else Poly.const(re)
        self.im = im if isinstance(im, Poly) else Poly.const(im)

    def __add__(self, o):
        return Cx(self.re + o.re, self.im + o.im)

    def __sub__(self, o):
        return Cx(self.re - o.re, self.im - o.im)

    def __mul__(self, o):
        if isinstance(o, Cx):
            return Cx(self.re * o.re - self.im * o.im, self.re * o.im + self.im * o.re)
        o = complex(o)
        cr, ci = Fraction(o.real).limit_denominator(1), Fraction(o.imag).limit_denominator(1)
        return Cx(self.re * cr - self.im * ci, self.re * ci + self.im * cr)

    def conj(self):
        return Cx(self.re, -self.im)


def cmat_from(vars8):
    """2x2 complex matrix (list of lists of Cx) sum_mu vars8[mu] BASIS[mu]."""
    out = [[Cx(0), Cx(0)], [Cx(0), Cx(0)]]
    for mu, E in enumerate(BASIS):
        for i in range(2):
            for j in range(2):
                e = E[i, j]
                if e != 0:
                    out[i][j] = out[i][j] + Cx(vars8[mu]) * e
    return out


def cvec_from(vars4):
    return [Cx(vars4[0], vars4[1]), Cx(vars4[2], vars4[3])]


def mmul(X, Y):
    return [[X[i][0] * Y[0][j] + X[i][1] * Y[1][j] for j in range(2)] for i in range(2)]


def mvec(X, v):
    return [X[i][0] * v[0] + X[i][1] * v[1] for i in range(2)]


def dag(X):
    return [[X[j][i].conj() for j in range(2)] for i in range(2)]


def det2(X):
    return X[0][0] * X[1][1] - X[0][1] * X[1][0]


def vdot_re(u, w):
    """Re(u^dagger w) for complex 2-vectors."""
    s = u[0].conj() * w[0] + u[1].conj() * w[1]
    return s.re


def minner(X, Y):
    """<X, Y> = (1/2) Re Tr(X^dagger Y) (= component dot product in BASIS)."""
    s = Cx(0)
    for i in range(2):
        for j in range(2):
            s = s + X[i][j].conj() * Y[i][j]
    return s.re * Fraction(1, 2)


def higgs_matrix(H4):
    """M(Phi) = Phi0 1 + Phi1 EPS + Phi2 iSX + Phi3 iSZ (R(M(Phi)) = rho(Phi) of layers/chiral.py)."""
    return cmat_from([H4[0], H4[1], H4[2], H4[3], 0, 0, 0, 0])


# ------------------------------------------------------------------------------------------------ parameters
def ewb_params(Q: int = Q_DEFAULT, *, hop: int = HOP, wilson: int = WILSON, mass: int = MASS, A: int = 1 << 16,
               v: int = 1 << 16, kH: int = 1 << 10, kXi: int = 1 << 13, M_Xi: int = 1 << 33, kB: int = 1 << 14,
               M_B: int = 1 << 30, lam: int = 2, lam_H: int = 4, kappa_P: int = 256, c_P: int = 0,
               beta: int | None = None, plaquette: bool = False, w_plaq: int = 1, relay_delta: int = 8,
               M_R: int = 1 << 34, relay_form: str = "diff", w_B: int = 0, relay_scale: tuple = (1, 1),
               corner_form: str = "split") -> dict:
    """Integer parameters with every vacuum identity checked (raises otherwise)."""
    D = 6 * Q
    if Q < 3 or Q % 2 == 0:
        raise ValueError("ONE ODD Q")
    beta = D - (1 << 33) if beta is None else beta
    if hop % A or wilson % v or mass % (2 * v):
        raise ValueError("hop = kappa A, wilson = w v, mass = 2 y v must be integral")
    kappa, w, y = hop // A, wilson // v, mass // (2 * v)
    if kappa % 2 or w % 2:
        raise ValueError("kappa and w must be even (Pi = 2 P)")
    if (kXi * A * v) % M_Xi:
        raise ValueError("xi0 = kXi A v / M_Xi must be an integer")
    xi0 = kXi * A * v // M_Xi
    if 2 * kXi * xi0 != kH * v:
        raise ValueError("isotropy: the hybrid locks must pull the charged slot as the Higgs hop pulls the neutral one "
                         "(2 kXi xi0 = kH v)")
    if (kB * A * A) % M_B:
        raise ValueError("B0 = kB A^2 / M_B must be an integer")
    B0 = kB * A * A // M_B
    if hop % B0 or (hop // B0) % 2:
        raise ValueError("kappa_e = hop / B0 must be an even integer")
    if wilson % xi0 or (wilson // xi0) % 2:
        raise ValueError("w' = wilson / xi0 must be an even integer")
    if (2 * kH * v * v) % A:
        raise ValueError("c_V = (2 kH v^2 + 2 kB B0 A)/A must be an integer")
    c_V = (2 * kH * v * v) // A + 2 * kB * B0
    if (6 * kXi * A * xi0) % v:
        raise ValueError("cPhi must be an integer")
    cPhi = 6 * kH * A + 6 * kXi * A * xi0 // v
    sn, sd = relay_scale
    if plaquette and relay_form == "diff":
        kappa_P = 0
        if (A * sn) % sd or (M_R * sn * sn) % (sd * sd) or (B0 * sn) % sd:
            raise ValueError("relay scale s = sn/sd needs integer R0 = s A, s B0 and M_R s^2")
        R0, kappa_R = A * sn // sd, M_R              # -(M_R/2)|R - s V'|^2: R = s V' statically, no pull, no balance
    elif plaquette:
        kappa_P = 0                                  # the approved plaquette kind replaces the rank-3 2-path relays
        R0 = A - relay_delta
        if (M_R * R0) % A:
            raise ValueError("relay lock kappa_R = M_R R0 / A must be an integer")
        kappa_R = M_R * R0 // A
        if (2 * kappa_R * R0) % A:
            raise ValueError("relay balance 2 kappa_R R0 / A must be an integer")
        c_V += 2 * kappa_R * R0 // A
    else:
        R0 = kappa_R = 0
    dP = D - c_P - beta
    if kappa_P and (dP <= 0 or (kappa_P * A * A) % dP):
        raise ValueError("P0 = kappa_P A^2/(D - c_P - beta) must be a positive integer")
    P0 = kappa_P * A * A // dP if kappa_P else 0
    c_U = 4 * kappa_P * P0
    return {"Q": Q, "D": D, "hop": hop, "wilson": wilson, "mass": mass, "A": A, "v": v, "kappa": kappa, "w": w, "y": y,
            "ytot": y + 3 * w, "kH": kH, "kXi": kXi, "M_Xi": M_Xi, "xi0": xi0, "w_xi": wilson // xi0, "kB": kB,
            "M_B": M_B, "B0": B0, "kappa_e": hop // B0, "lam": lam, "lam_H": lam_H, "kappa_P": kappa_P, "c_P": c_P,
            "beta": beta, "P0": P0, "c_U": c_U, "c_V": c_V, "cPhi": cPhi, "plaquette": plaquette, "w_plaq": w_plaq,
            "R0": R0, "M_R": M_R if plaquette else 0, "kappa_R": kappa_R, "relay_form": relay_form,
            "w_B": w_B if plaquette else 0, "relay_scale": (sn, sd), "corner_form": corner_form,
            "c_over_cQ_linear": (R0 / A) * (w_plaq ** 0.5) if plaquette else None}


def gear_names(plaquette: bool = False, det_shadow: bool = False):
    g = []
    for a in range(3):
        g += [f"V{AXES[a]}_{c}" for c in COMP]
    if not plaquette:
        for a in range(3):
            for b in range(3):
                if a != b:
                    g += [f"P{AXES[a]}{AXES[b]}_{c}" for c in COMP]
    for a in range(3):
        g += [f"B{AXES[a]}_re", f"B{AXES[a]}_im"]
    for a in range(3):
        g += [f"X{AXES[a]}_{c}" for c in DCOMP]
    for a in range(3):
        g += [f"Y{AXES[a]}_{c}" for c in DCOMP]
    if plaquette:
        for a in range(3):
            for b in range(3):
                if a != b:
                    g += [f"R{AXES[a]}{AXES[b]}_{c}" for c in COMP]
        if det_shadow:
            for a in range(3):
                for b in range(3):
                    if a != b:
                        g += [f"S{AXES[a]}{AXES[b]}_re", f"S{AXES[a]}{AXES[b]}_im"]
    g += list(HIGGS)
    return g


# ------------------------------------------------------------------------------------------------ the block
def build_ewb(*, Q: int = Q_DEFAULT, matter: Block, partner: Block, name: str = "ewb", label: str = "audit",
              use_P: bool = True, **kw) -> Block:
    """The route-B block: all new gears (U(2) links, 2-paths, B, Xi, Xi', Higgs) and every coupling (module docstring)."""
    prm = ewb_params(Q, hop=matter.params["hop"], wilson=matter.params["wilson"], mass=matter.params["mass"], **kw)
    for p_ in (matter.params, partner.params):
        if (p_["hop"], p_["wilson"], p_["mass"], p_["Q"]) != (prm["hop"], prm["wilson"], prm["mass"], Q):
            raise ValueError("matter and partner must carry the block's (Q, hop, wilson, mass): vacuum identity")
    _check_basis()
    D, A, v = prm["D"], prm["A"], prm["v"]
    q = lambda g: f"{name}.{g}"
    x0 = {q(f"V{AXES[a]}_1"): A for a in range(3)}
    if use_P:
        for a in range(3):
            for b in range(3):
                if a != b and prm["P0"]:
                    x0[q(f"P{AXES[a]}{AXES[b]}_1")] = prm["P0"]
    for a in range(3):
        x0[q(f"B{AXES[a]}_re")] = prm["B0"]
        x0[q(f"X{AXES[a]}_ur")] = prm["xi0"]
        x0[q(f"Y{AXES[a]}_ur")] = prm["xi0"]
    x0[q("H_1")] = v
    if prm["plaquette"]:
        for a in range(3):
            for b in range(3):
                if a != b:
                    x0[q(f"R{AXES[a]}{AXES[b]}_1")] = prm["R0"]
                    if prm["w_B"]:
                        x0[q(f"S{AXES[a]}{AXES[b]}_re")] = prm["B0"] * prm["relay_scale"][0] // prm["relay_scale"][1]

    var = lambda g, off=ZERO: Poly.var(q(g), off, x0.get(q(g), 0))
    dev = lambda g, off=ZERO: Poly.var(q(g), off)                     # deviation only (matter couplings)
    Vm = lambda a, off=ZERO: cmat_from([var(f"V{AXES[a]}_{c}", off) for c in COMP])
    Pm = lambda a, b, off=ZERO: cmat_from([var(f"P{AXES[a]}{AXES[b]}_{c}", off) for c in COMP])
    Bc = lambda a, off=ZERO: Cx(var(f"B{AXES[a]}_re", off), var(f"B{AXES[a]}_im", off))
    Xv = lambda a, off=ZERO: cvec_from([var(f"X{AXES[a]}_{c}", off) for c in DCOMP])
    Yv = lambda a, off=ZERO: cvec_from([var(f"Y{AXES[a]}_{c}", off) for c in DCOMP])
    Hq = lambda off=ZERO: [var(h, off) for h in HIGGS]
    col = lambda Mx, j: [Mx[0][j], Mx[1][j]]

    phi = Poly()
    # ---------------------------------------------------------------- bosonic sector (full physical form)
    H0 = Hq()
    M0 = higgs_matrix(H0)
    nH = sum((h * h for h in H0), Poly())
    phi = phi + nH * Fraction(D - prm["cPhi"], 2)
    if prm["lam_H"]:
        dn = nH - v * v
        phi = phi - dn * dn * Fraction(prm["lam_H"], 4)
    for a in range(3):
        V = Vm(a)
        nV = minner(V, V)
        phi = phi + nV * Fraction(D - prm["c_U"] - prm["c_V"], 2)
        if prm["lam"]:
            N = mmul(dag(V), V)
            N = [[N[i][j] - (Cx(A * A) if i == j else Cx(0)) for j in range(2)] for i in range(2)]
            tr = Poly()
            for i in range(2):
                for j in range(2):
                    tr = tr + (N[i][j] * N[j][i]).re
            phi = phi - tr * Fraction(prm["lam"], 4)
        Me = higgs_matrix(Hq(UNIT[a]))
        phi = phi + vdot_re(col(M0, 1), mvec(V, col(Me, 1))) * prm["kH"]           # Higgs hop through V (col2)
        X, Y = Xv(a), Yv(a)
        phi = phi + vdot_re(X, mvec(dag(V), col(M0, 0))) * prm["kXi"]                # Xi  ~ V^dag col1(x)
        phi = phi + vdot_re(Y, mvec(V, col(Me, 0))) * prm["kXi"]                     # Xi' ~ V col1(x+e)
        nX = vdot_re(X, X) + vdot_re(Y, Y)
        phi = phi + nX * Fraction(D - prm["M_Xi"], 2)
        B = Bc(a)
        phi = phi + (B.conj() * det2(V)).re * prm["kB"]                              # B locked to det V
        phi = phi + (B.re * B.re + B.im * B.im) * Fraction(D - prm["M_B"], 2)
    if prm["plaquette"]:
        # relays R(x;a,b) ~ V(x+e_a, b) (rank-2 lock, B3: one face link) and the SPLIT PLAQUETTE on site (approved rank-4
        # kind: the four links around one elementary plaquette, two of them carried by relays; no matter factor):
        #   Psi -= w ||V(x,a) R(x;a,b) - V(x,b) R(x;b,a)||^2   (|| ||^2 = component norm = (1/2) Re Tr), a < b
        Rm = lambda a, b, off=ZERO: cmat_from([var(f"R{AXES[a]}{AXES[b]}_{c}", off) for c in COMP])
        for a in range(3):
            for b in range(3):
                if a == b:
                    continue
                Rab = Rm(a, b)
                if prm["relay_form"] == "diff":
                    sc = Fraction(*prm["relay_scale"])
                    Vf = Vm(b, UNIT[a])
                    dR = [[Rab[i][j] - Vf[i][j] * sc for j in range(2)] for i in range(2)]
                    phi = phi + minner(Rab, Rab) * Fraction(D, 2) - minner(dR, dR) * Fraction(prm["kappa_R"], 2)
                else:
                    phi = phi + minner(Rab, Vm(b, UNIT[a])) * prm["kappa_R"]
                    phi = phi + minner(Rab, Rab) * Fraction(D - prm["M_R"], 2)
                if prm["w_B"]:
                    # det-shadow kinetic term: relays S(x;a,b) ~ B(x+e_a, b) (diff lock) and the U(1) split plaquette
                    Sab = Cx(var(f"S{AXES[a]}{AXES[b]}_re"), var(f"S{AXES[a]}{AXES[b]}_im"))
                    Bf = Bc(b, UNIT[a])
                    scB = Fraction(*prm["relay_scale"])
                    dS = Sab - Cx(Bf.re * scB, Bf.im * scB)
                    phi = phi + (Sab.re * Sab.re + Sab.im * Sab.im) * Fraction(D, 2)
                    phi = phi - (dS.re * dS.re + dS.im * dS.im) * Fraction(prm["kappa_R"], 2)
                    if a < b:
                        Sba = Cx(var(f"S{AXES[b]}{AXES[a]}_re"), var(f"S{AXES[b]}{AXES[a]}_im"))
                        if prm["corner_form"] == "sym4":
                            # ONE-LIGHT-A's symmetric form: 4 corners at weight 1/2 + the cross term (U(1): |z|^2)
                            n2 = lambda z: z.re * z.re + z.im * z.im
                            X1, X2 = Bc(a) * Sab, Bc(b) * Sba
                            cr = (X1.conj() * X2).re
                            corners = n2(X1) + n2(X2) + n2(Bc(a).conj() * Bc(b)) + n2(Sab * Sba.conj())
                            phi = phi - (corners * Fraction(1, 2) - cr * 2) * prm["w_B"]
                        else:
                            dP = Bc(a) * Sab - Bc(b) * Sba
                            phi = phi - (dP.re * dP.re + dP.im * dP.im) * prm["w_B"]
                if a < b and prm["corner_form"] == "sym4":
                    # ONE-LIGHT-A's symmetric split plaquette (s19): (w/2)(4 corners) - 2w <V_a R_ab, V_b R_ba>
                    Rba = Rm(b, a)
                    X1, X2 = mmul(Vm(a), Rab), mmul(Vm(b), Rba)
                    C3, C4 = mmul(dag(Vm(a)), Vm(b)), mmul(Rab, dag(Rba))
                    corners = minner(X1, X1) + minner(X2, X2) + minner(C3, C3) + minner(C4, C4)
                    phi = phi - (corners * Fraction(1, 2) - minner(X1, X2) * 2) * prm["w_plaq"]
                elif a < b:
                    Dm = mmul(Vm(a), Rab)
                    Dm2 = mmul(Vm(b), Rm(b, a))
                    Dm = [[Dm[i][j] - Dm2[i][j] for j in range(2)] for i in range(2)]
                    phi = phi - minner(Dm, Dm) * prm["w_plaq"]
    if use_P and prm["kappa_P"]:
        for a in range(3):
            for b in range(3):
                if a == b:
                    continue
                Pab = Pm(a, b)
                phi = phi + minner(Pab, mmul(Vm(a), Vm(b, UNIT[a]))) * prm["kappa_P"]
                phi = phi + minner(Pab, Pab) * Fraction(prm["c_P"], 2)
                if a < b:
                    phi = phi + minner(Pab, Pm(b, a)) * prm["beta"]
    # ---------------------------------------------------------------- matter couplings (deviation parts)
    alg = chiral_algebra()
    Pd, W0, PiW, PiS = alg["P"], alg["W0"], alg["PiW"], alg["PiS"]
    P1 = np.kron(np.diag([1, 0]).astype(np.int64), np.eye(16, dtype=np.int64))
    P2 = np.kron(np.diag([0, 1]).astype(np.int64), np.eye(16, dtype=np.int64))
    Jp16 = pair_algebra("pair")["Jp"]
    J1 = np.kron(np.diag([1, 0]).astype(np.int64), Jp16)
    mnames = [matter.qualify(x) for x in matter_names("pair")] + [partner.qualify(x) for x in matter_names("pair")]
    bvec = lambda off: [Poly.var(g, off) for g in mnames]

    def bil(left, M, right):
        out = Poly()
        rows, cols = np.nonzero(M)
        for i, j in zip(rows, cols):
            out = out + left[i] * right[j] * int(M[i, j])
        return out

    b0 = bvec(ZERO)
    RT = [r32(E).T for E in BASIS]                                # R(E_mu^dagger) = R(E_mu)^T
    for a in range(3):
        be = bvec(UNIT[a])
        for mu in range(8):                                       # L transport: (kappa/2) b'^T P R(W^dag) Pi_W b
            M = Pd[a] @ RT[mu] @ PiW
            phi = phi + dev(f"V{AXES[a]}_{COMP[mu]}") * bil(be, M, b0) * Fraction(prm["kappa"], 2)
        Me1 = Pd[a] @ PiS @ P1                                    # e_R transport: (kappa_e/2) b'^T P R1(conj B~) Pi_S P1 b
        Me2 = Pd[a] @ (-J1) @ PiS @ P1
        phi = phi + dev(f"B{AXES[a]}_re") * bil(be, Me1, b0) * Fraction(prm["kappa_e"], 2)
        phi = phi + dev(f"B{AXES[a]}_im") * bil(be, Me2, b0) * Fraction(prm["kappa_e"], 2)
    rho = [r32(BASIS[c]) for c in range(4)]                       # rho(e_c), c = 0..3 (quaternion units)
    for c in range(4):                                            # on-site Yukawa (+ on-site Wilson), as layers/chiral.py
        M = rho[c] @ PiW @ W0
        phi = phi + dev(HIGGS[c]) * (bil(b0, M, b0) + bil(b0, M.T, b0)) * Fraction(prm["ytot"], 2)
    for a in range(3):
        be = bvec(UNIT[a])
        for c in range(4):                                        # nu Wilson-Yukawa (column 2 = nu_R; no link)
            M1 = rho[c] @ PiW @ W0 @ P2
            M2 = P2 @ W0 @ PiW @ rho[c].T
            phi = phi + dev(HIGGS[c], UNIT[a]) * bil(be, M1, b0) * Fraction(-prm["w"], 2)
            phi = phi + dev(HIGGS[c]) * bil(be, M2, b0) * Fraction(-prm["w"], 2)
        for k, cc in enumerate(DCOMP):                            # e Wilson-Yukawa through Xi (L at x+e) and Xi' (L at x)
            Cm = np.zeros((2, 2), dtype=complex)
            Cm[k // 2, 0] = 1 if k % 2 == 0 else 1j               # C(Xi): first column = the doublet
            RC = r32(Cm)
            M1 = RC @ PiW @ W0 @ P1
            M2 = P1 @ W0 @ PiW @ RC.T
            phi = phi + dev(f"X{AXES[a]}_{cc}") * bil(be, M1, b0) * Fraction(-prm["w_xi"], 2)
            phi = phi + dev(f"Y{AXES[a]}_{cc}") * bil(be, M2, b0) * Fraction(-prm["w_xi"], 2)
    terms = deviation_terms(phi, D, x0)
    gears = []
    for g in gear_names(prm["plaquette"], bool(prm["w_B"])):
        link = None
        if g[0] in "VBXY":
            link = AXES.index(g[1])
        if g.startswith("P") or g.startswith("R") or g.startswith("S") or g in HIGGS:
            link = None
        gears.append(GearType(g, label, link=link) if link is not None else GearType(g, label))
    r0 = 3 * Q - 1
    params = dict(prm, matter=matter.name, partner=partner.name, use_P=use_P,
                  X0={k: val for k, val in x0.items()}, candidate="ROUTE B: DECLARED CANDIDATE, DEFAULT OFF",
                  default_on=EWB_DEFAULT_ON)
    return Block(tuple(gears), tuple(terms), name=name, vacuum={g: r0 for g in gear_names(prm["plaquette"], bool(prm["w_B"]))}, params=params,
                 doc="route B: exact local SU(2)_L x U(1)_Y (U(2) links, det-locked B, hybrid Xi/Xi', Higgs)", Q=Q)


def ewb_blocks(Q: int = Q_DEFAULT, *, matter: Block | None = None, include_matter: bool = False, **kw) -> tuple:
    """(matter2, ewb) [preceded by matter]. ``matter``: the existing first doublet member (default_system's "matter")."""
    from .matter import build_matter
    if matter is None:
        matter = build_matter(Q=Q, hop=HOP, mass=MASS, wilson=WILSON, species="pair", name="matter")
    partner = build_partner(Q, hop=matter.params["hop"], wilson=matter.params["wilson"], mass=matter.params["mass"],
                            name="matter2")
    blk = build_ewb(Q=Q, matter=matter, partner=partner, **kw)
    return ((matter, partner, blk) if include_matter else (partner, blk))


def compose_electroweak_b(system, *, on: bool = EWB_DEFAULT_ON, **kw):
    """NEW System: the base system (hands OFF: default_system(chiral=False, electroweak=False)) with E1 ("em") retired,
    the form-C matter lapse of "matter" ("mlapse", "mbeta": it dresses the bare L-R mass, breaking SU(2) x U(1)_Y)
    removed, and route B appended. on=False: unchanged. No graviweak coupling (declared OPEN, Study 18)."""
    if not on:
        return system
    from .system import System
    if any(b.name in ("chiral", "wsu2", "gwb", "ehop") for b in system.blocks):
        raise ValueError("compose route B onto the hands-OFF base (chiral=False, electroweak=False)")
    matter = system.by_name("matter")
    blocks = [b for b in system.blocks if b.name not in ("em", "mlapse", "mbeta")]
    new = ewb_blocks(system.Q, matter=matter, **kw)
    blocks += list(new)
    info = dict(system.info)
    info["electroweak_b"] = {"status": "ROUTE B DECLARED CANDIDATE, DEFAULT OFF",
                             "retired": "E1 (em block): the photon is the unbroken W3/B combination of the U(2) link",
                             "removed": ["em", "mlapse", "mbeta"], "graviweak": "none (OPEN, Study 18)",
                             "params": {k: new[-1].params[k] for k in ("A", "v", "kH", "kXi", "xi0", "kB", "B0", "kappa_P",
                                                                      "P0", "lam", "lam_H", "c_V", "cPhi")}}
    return System(system.Q, tuple(blocks), info)


# ------------------------------------------------------------------------------------------------ generators (data only)
def generator_actions(gen: str) -> dict:
    """Integer real matrices (x2) of the infinitesimal local transformation of generator ``gen`` in {t1, t2, t3, Y}
    at a node, for every field kind (keys: matter (32), higgs (4), link_left / link_right (8x8), B_left / B_right (2),
    doublet (4), xi_phase (4: -Tr X on a doublet)). The photon Q = (t3 + Y)/2 is the half-sum of the t3 and Y laws."""
    if gen not in GEN:
        raise ValueError("gen must be t1, t2, t3 or Y (Q = (t3 + Y)/2 is their half-sum)")
    X = GEN[gen]
    X2 = 2 * X
    tau2 = int(round(np.trace(X2).imag))                           # Tr(2X) = i tau2
    alg = chiral_algebra()
    J1 = np.kron(np.diag([1, 0]).astype(np.int64), pair_algebra("pair")["Jp"])
    # matter (x2): 2 db = R(X) Pi_W b + (Tr X / i) J1 Pi_S b   [P_W = Pi_W/2; e_R -> det G e_R]
    matter = r32(X) @ alg["PiW"] + (tau2 // 2) * J1 @ alg["PiS"]
    # link left / right multiplication (x2)
    def lin_map(f):
        M = np.zeros((8, 8), dtype=np.int64)
        for nu, E in enumerate(BASIS):
            co = m2c_coords(f(E))
            for mu in range(8):
                val = co[mu]
                assert abs(val - round(val)) < 1e-12
                M[mu, nu] = int(round(val))
        return M
    link_left = lin_map(lambda E: X2 @ E)
    link_right = lin_map(lambda E: -E @ X2)
    # Higgs: dM = X M - Tr(X) M E11 (x2), on the 4 quaternion components
    E11 = np.diag([1, 0]).astype(complex)
    higgs = np.zeros((4, 4), dtype=np.int64)
    for c in range(4):
        dM = X2 @ BASIS[c] - np.trace(X2) * BASIS[c] @ E11
        co = m2c_coords(dM)
        assert all(abs(co[m]) < 1e-12 for m in range(4, 8)), "Higgs action left the quaternion form"
        for m in range(4):
            higgs[m, c] = int(round(co[m]))
    # doublet (complex 2-vector, components ur, ui, dr, di) under X2
    def dmat(Mc):
        R = np.zeros((4, 4), dtype=np.int64)
        for j in range(4):
            e = np.zeros(2, dtype=complex)
            e[j // 2] = 1 if j % 2 == 0 else 1j
            y = Mc @ e
            for i in range(4):
                val = y[i // 2].real if i % 2 == 0 else y[i // 2].imag
                R[i, j] = int(round(val))
        return R
    doublet = dmat(X2)
    xi_phase = dmat(-np.trace(X2) * np.eye(2))
    B_left = np.array([[0, -tau2], [tau2, 0]], dtype=np.int64)     # multiplication by i tau2 (x2: Tr(2X))
    B_right = -B_left
    return {"matter": matter.astype(np.int64), "higgs": higgs, "link_left": link_left, "link_right": link_right,
            "B_left": B_left, "B_right": B_right, "doublet": doublet, "xi_phase": xi_phase}


__all__ = ["EWB_DEFAULT_ON", "BASIS", "GEN", "r32", "m2c_coords", "ewb_params", "build_ewb", "ewb_blocks",
           "compose_electroweak_b", "generator_actions", "gear_names"]
