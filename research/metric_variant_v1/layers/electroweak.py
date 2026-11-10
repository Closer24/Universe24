"""ELECTROWEAK extensions of the chiral candidate (EW-BUILDER = HAND-M1): DECLARED CANDIDATES, DEFAULT OFF; every piece
is active only together with the chiral block (layers/chiral.py, itself DEFAULT OFF). TENSOR BLOCKS ONLY. NEW file;
no existing package file (layers/chiral.py included) is modified.

L3  Higgs hop (W mass): Psi = kH sum_{x,d} <Phi(x), U(x,d) Phi(x+e_d)>  - (cPhi/2) sum_x |Phi|^2 - (cW/2) sum_links |U|^2,
    cPhi = 6 kH A, cW = kH v^2 / A (exact vacuum balance: no linear term). Exactly SU(2)-covariant (Phi -> g Phi,
    U -> g U g'^-1). Rank 3, B3 link-local, reciprocal. The balance term -(cW/2)|U|^2 is the W mass term:
    predicted k = 0 shift of the link clock  d(cos w) = -cW/D, i.e. m_W^2 ~ 2 kH v^2/(A D) (m_W ~ g v).
L2b Graviweak, option (b) (HL-1 interim 12:22, "the lapse sets the Higgs, the Higgs sets the clocks"): with the lapse
    field F (U = F/(2P), the package convention):
      (cF/2) F(x) (|Phi(x)|^2 - v^2),             cF = -lam_H v^2 / P   (Higgs vev -> v sqrt(1 - F/P) = v (1 - U) + O(U^2))
      (cL/2) (F(x) + F(x+e)) (|U(x,d)|^2 - A^2),  cL = -lam_L A^2 / P   (link norm -> A sqrt(1 - (F_x+F_y)/P): factor 1 - 2U)
      -(1/(2P)) (F(x) + F(x+e)) (hop/2) b(x+e)^T P_d Pi_S b(x)   (the gauge-SINGLET half of the transport, direct form-C
                                                                 link factor; the doublet half gets it through |U|)
    Every term is SU(2)-invariant and rank 3. The doublet's mass and Wilson entries are NOT lapse-dressed directly (that
    breaks SU(2): HL-1's degree count); they follow the Higgs adiabatically. Use INSTEAD of matter_lapse_c for the
    doublet (compose_electroweak removes mlapse / mbeta of "matter"). oneway=True: designated one-way reads of a
    prescribed static F (MECHANISM, EP tests only).
L1  Hypercharge (analysis + algebra; see NOTES_electroweak.md): exact symmetries of the chiral potential are SU(2)_L
    (local), the custodial SU(2)_R (global: t_a on the Pi_S doublet, Phi -> Phi h^-1) and U(1)_(B-L) (J' on matter).
    Y/2 = T3_R + (B-L)/2; the photon Q = T3_L + T3_R + (B-L)/2 acts on matter as t3 + J' (vector-like; on "matter"
    = 2 J', on "matter2" = 0: the default E1 coupling) and on Phi as L_k - R_k, which annihilates the vev. A U(1) that
    gauges Y must act on the second-order Higgs (and the charged W must couple to Q): Study 4 A1 forbids that for E1's
    A0, so E1 cannot gauge Y exactly. Exact route: compact U(1)_Y links acting on matter (M(B) = B_re + B_im X_Y), on
    the Higgs (right multiplication) and, through Q, on nothing else: NOT built here (spec in NOTES_electroweak.md).
"""
from __future__ import annotations

from fractions import Fraction

import numpy as np

from ..core.tensor import Block, GearType
from .chiral import HIGGS, chiral_algebra
from .gauge import ALGEBRAS, Poly, deviation_terms, vec_dot
from .matter import matter_names

EW_DEFAULT_ON = False
AXES = ("x", "y", "z")
ZERO = (0, 0, 0)
UNIT = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
KH_DEFAULT = 1 << 10
ONEWAY_WHY = ("MECHANISM: prescribed static lapse F read one-way by the graviweak (b) couplings (EP test only; the "
              "reciprocal block is the physical candidate)")


def _names(coupling: Block, links: Block):
    hq = [coupling.qualify(h) for h in HIGGS]
    lq = {k: [links.qualify(f"U{AXES[k]}_{c}") for c in ("1", "i", "j", "k")] for k in range(3)}
    return hq, lq


def build_higgs_hop(*, coupling: Block, links: Block, kH: int = KH_DEFAULT, name: str = "ehop") -> Block:
    """L3: the covariant Higgs hop through the weak links, with the exact vacuum balance (see module docstring)."""
    cp, lp = coupling.params, links.params
    Q, v, A = cp["Q"], cp["v"], lp["A"]
    D = 6 * Q
    if type(kH) is not int or kH < 0:
        raise ValueError("kH must be a non-negative int")
    if (kH * v * v) % A:
        raise ValueError("cW = kH v^2 / A must be an integer")
    cPhi, cW = 6 * kH * A, kH * v * v // A
    if cPhi + 12 * kH * A > 2 * D:
        raise ValueError("Higgs hop too strong for the Rule3 stability bound")
    H = ALGEBRAS["su2"]
    hq, lq = _names(coupling, links)
    Phi = lambda off: [Poly.var(h, off, v if c == 0 else 0) for c, h in enumerate(hq)]
    U = lambda k, off: [Poly.var(g, off, A if c == 0 else 0) for c, g in enumerate(lq[k])]
    pot = Poly()
    P0 = Phi(ZERO)
    for k in range(3):
        pot = pot + vec_dot(P0, H.prod(U(k, ZERO), Phi(UNIT[k]))) * kH
        Uk = U(k, ZERO)
        pot = pot - vec_dot(Uk, Uk) * Fraction(cW, 2)
    pot = pot - vec_dot(P0, P0) * Fraction(cPhi, 2)
    terms = deviation_terms(pot, D, {})
    return Block((), tuple(terms), name=name, Q=Q,
                 params={"Q": Q, "kH": kH, "v": v, "A": A, "cPhi": cPhi, "cW": cW, "coupling": coupling.name,
                         "links": links.name, "predicted_dcos_w_W": str(Fraction(-cW, D)),
                         "candidate": "DECLARED CANDIDATE, DEFAULT OFF (needs the chiral block)"},
                 doc="L3 covariant Higgs hop <Phi, U Phi'> + exact vacuum balance (W mass term -(cW/2)|U|^2)")


def build_graviweak_b(*, coupling: Block, links: Block, matter_blocks, field: str, P: int, lam_H: int | None = None,
                      lam_L: int = 4, oneway: bool = False, name: str = "gwb") -> Block:
    """L2 option (b): SU(2)-invariant rank-3 lapse couplings (see module docstring). ``field``: qualified name of the
    lapse field gear F (U = F/(2P)); ``matter_blocks``: the doublet members (both pairs)."""
    cp, lp = coupling.params, links.params
    Q, v, A, hop = cp["Q"], cp["v"], lp["A"], cp["hop"]
    lam_H = cp["lam_H"] if lam_H is None else lam_H
    D = 6 * Q
    if (lam_H * v * v) % P or (lam_L * A * A) % P:
        raise ValueError("cF = -lam_H v^2/P and cL = -lam_L A^2/P must be integers")
    cF, cL = -(lam_H * v * v) // P, -(lam_L * A * A) // P
    hq, lq = _names(coupling, links)
    F = lambda off: Poly.var(field, off)
    pot = Poly()
    Ph = [Poly.var(h, ZERO, v if c == 0 else 0) for c, h in enumerate(hq)]
    pot = pot + F(ZERO) * (vec_dot(Ph, Ph) - v * v) * Fraction(cF, 2)
    for k in range(3):
        Uk = [Poly.var(g, ZERO, A if c == 0 else 0) for c, g in enumerate(lq[k])]
        pot = pot + (F(ZERO) + F(UNIT[k])) * (vec_dot(Uk, Uk) - A * A) * Fraction(cL, 2)
    # singlet-half transport, direct link factor -(F_x + F_y)/(2P) on (hop/2) b(x+e)^T P_d Pi_S b(x), per pair
    alg = chiral_algebra()
    PiS16 = np.eye(16, dtype=np.int64) + alg["G5_16"] @ (alg["V"][:16, :16])
    from .matter import algebra as pair_alg
    Pd = pair_alg("pair")["P"]
    for mb in matter_blocks:
        mn = [mb.qualify(g) for g in matter_names("pair")]
        for k in range(3):
            M = Pd[k] @ PiS16
            rows, cols = np.nonzero(M)
            bil = Poly()
            for i, j in zip(rows, cols):
                bil = bil + Poly.var(mn[i], UNIT[k]) * Poly.var(mn[j], ZERO) * int(M[i, j])
            pot = pot - (F(ZERO) + F(UNIT[k])) * bil * Fraction(hop, 4 * P)
    terms = deviation_terms(pot, D, {})
    if oneway:
        kept = []
        for t in terms:
            if t[0] == field:
                continue
            if any(f[0] == field for f in t[2]):
                kept.append(t + ({"designated_one_way": ONEWAY_WHY},))
            else:
                kept.append(t)
        terms = kept
    return Block((), tuple(terms), name=name, Q=Q,
                 params={"Q": Q, "P": P, "field": field, "cF": cF, "cL": cL, "lam_H": lam_H, "lam_L": lam_L,
                         "oneway": oneway, "option": "(b): lapse x |Phi|^2, link factor x |U|^2, singlet-half hop",
                         "candidate": "DECLARED CANDIDATE, DEFAULT OFF (needs the chiral block)"},
                 doc="L2(b) graviweak: SU(2)-invariant rank-3 lapse couplings (Higgs sets the clocks)")


def build_test_lapse_field(*, Q: int, name: str = "lapsef") -> Block:
    """A minimal lapse field for stand-alone tests: one node gear F, inertia (D/2) F^2 (marginal), vacuum 0."""
    D = 6 * Q
    return Block((GearType("F", "audit"),), (("F", D, (("F", ZERO, "b"),)),), name=name, vacuum={"F": 3 * Q - 1},
                 params={"Q": Q, "role": "test lapse field (marginal node gear)"}, doc="test lapse field", Q=Q)


# ======================================================================== L1 generators (algebra only)
def hypercharge_generators() -> dict:
    """Antisymmetric generator matrices (integer) on (matter 32 channels) and on the Higgs quaternion (4):
    L3 = t3 P_W (x2: t3 PiW), R3 = t3 P_S (x2: t3 PiS) with Higgs -R_k (x2), BL = J' (x2) with Higgs 0,
    Q = L3 + R3 + BL (x2) with Higgs L_k - R_k (x2): the photon (annihilates the vev v.1)."""
    alg = chiral_algebra()
    t3, PiW, PiS, Jp = alg["t"][2], alg["PiW"], alg["PiS"], alg["Jp"]
    H = ALGEBRAS["su2"]
    Lk = np.array(H.left_matrix((0, 0, 0, 1)), dtype=np.int64)
    Rk = np.array(H.right_matrix((0, 0, 0, 1)), dtype=np.int64)
    Z4 = np.zeros((4, 4), np.int64)
    return {"L3": (t3 @ PiW, 2 * Lk), "R3": (t3 @ PiS, -2 * Rk), "BL": (2 * Jp, Z4),
            "Q": (t3 @ PiW + t3 @ PiS + 2 * Jp, 2 * Lk - 2 * Rk)}


def compose_electroweak(system, *, on: bool = EW_DEFAULT_ON, higgs_hop: bool = True, graviweak: bool = True,
                        kH: int = KH_DEFAULT, gwb_lam_H: int | None = 0, gwb_lam_L: int = 0):
    """FIX-i (owner decision v8-1, 14:37 UTC; s18/AGREE_STAB.md): gwb is built with lam_H = lam_L = 0 (singlet-half hop
    kept); gwb_lam_H=None, gwb_lam_L=4 rebuild the earlier L2(b) default (contrast only).
    Return a NEW System: the chiral candidate (layers/chiral.compose_with_default, partner_lapse=False) + L3 Higgs hop
    + L2(b) graviweak couplings on the system's lapse field, with the default matter lapse blocks of "matter"
    ("mlapse", "mbeta": they dress the bare mass and would break SU(2)) REMOVED. on=False: system unchanged.
    The beta = 1 read of the doublet is not re-built in form (b) (OPEN; declared)."""
    if not on:
        return system
    from .chiral import compose_with_default
    from .system import System
    sysc = compose_with_default(system, on=True, partner_lapse=False)
    blocks = [b for b in sysc.blocks if b.name not in ("mlapse", "mbeta")]
    coup, links = sysc.by_name("chiral"), sysc.by_name("wsu2")
    if higgs_hop:
        blocks.append(build_higgs_hop(coupling=coup, links=links, kH=kH))
    info = dict(sysc.info)
    if graviweak and system.info.get("gravity"):
        blocks.append(build_graviweak_b(coupling=coup, links=links,
                                        matter_blocks=[sysc.by_name("matter"), sysc.by_name("matter2")],
                                        field=system.info["lapse_field"], P=system.info["P"],
                                        lam_H=gwb_lam_H, lam_L=gwb_lam_L,
                                        oneway=(system.info.get("lapse") == "od2")))
        info["electroweak_fix_i"] = {"gwb_lam_H": gwb_lam_H, "gwb_lam_L": gwb_lam_L,
                                     "record": "owner decision v8-1, 14:37 UTC, FIX-i per s18/AGREE_STAB.md"}
        info["electroweak_lapse"] = ("L2(b): lapse x |Phi|^2 and link factor x |U|^2 + singlet-half hop factor; "
                                     "default mlapse/mbeta of 'matter' removed; beta read of the doublet OPEN")
    info["electroweak"] = {"status": "DECLARED CANDIDATE, DEFAULT OFF", "higgs_hop": higgs_hop, "kH": kH,
                           "graviweak": graviweak, "hypercharge": "analysis only (E1 cannot gauge Y: NOTES)"}
    return System(system.Q, tuple(blocks), info)


__all__ = ["EW_DEFAULT_ON", "KH_DEFAULT", "build_higgs_hop", "build_graviweak_b", "build_test_lapse_field",
           "hypercharge_generators", "compose_electroweak"]
