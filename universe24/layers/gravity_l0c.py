"""FORM C: the owner-approved universal lapse ON L0 (decision 3, "l0_lapse = W"; spec agreed by both Study 7
physicists, manager 11:2x). NEW file; template layers/gravity_l0.py (B1-GRAV, imported read-only). Tensor blocks only.

L0 in the port-DIFFERENCE (Laplacian) form at the ONE headroom weight Q - 1:
    Phi_L0 = (D/2) |b|^2 - ((Q-1)/2) [ b^T M0 b + b^T T b ],      D = 6Q,
    M0 = 6*1 - Sum_d W_d           (L0's MASS MATRIX: the k = 0 part; symmetric; +++ has one zero mode = the light,
                                    the handed class (1,-1,1) none: L0 fully gapped)
    T  = Sum_d W_d (1 - shift_d)   (the DIFFERENCE transport; 0 at k = 0)
so at F = 0:  u = D b - (Q-1)(6 - S) b = 6 b + (Q-1) S b  (S = Sum_d W_d shift_d): the ports at weight Q - 1 plus the
on-site carrier remainder 6 b, i.e. layers.gravity.headroom_potential's stencil on L0's signed ports (ONE cone c_Q).
Clock law at F = 0: 4 sin^2(w/2) = (Q-1)/(3Q) * eig(M0 + T(k)).

FORM C lapse (U = F/(2P), the B1-GRAV convention N = 1 - U):
    clock factor (1 - 2U) = 1 - F(x)/P on M0 (on-site), link factor (1 - 4U) = 1 - (F(x) + F(x+e))/P on T (per link),
    Phi_int = ((Q-1)/P) [ F(x) (3|b(x)|^2 - Sum_hops w b_t(x) b_s(x))
                         + Sum_hops (F(x) + F(x+e)) w ((b_t(x) b_s(x) + b_t(x+e) b_s(x+e))/2 - b_t(x) b_s(x+e)) ],
coefficients (Q-1)/P = 2k and k (integers for Q - 1 = 2Pk). Uniform F: every massive band at rest obeys
sin(w/2) = sqrt(1 - 2U) sin(w0/2) EXACTLY (T(0) = 0); light (+++ zero mode of M0) speed sqrt(1 - 4U), i.e. gamma = 1.
Neither the pure difference form (one factor on M0 + T) nor B1-GRAV's site/hop split (N on S(0), N/psi^2 on the
symmetric difference) gets both in the official sign-cycle click reading (Study 7, ONE-P2 N12/N12b).
"""
from __future__ import annotations

from fractions import Fraction

from ..core.tensor import Block
from . import gravity as gr
from .gravity_l0 import l0_hops
from .reference import build_reference

ZERO = (0, 0, 0)
L0C_READ_WHY = ("form-C L0 clock TEST read (one-way): a static prescribed lapse gear read by L0 clocks; the "
                "reciprocal block (oneway=False) is checked separately")


def build_l0c(*, Q: int, body_signs=(1, -1, 1), name: str = "ref", label: str = "official") -> Block:
    """L0 in form C at F = 0: today's ports x (Q - 1)/Q plus the on-site 6 b. Vacuum (0, 0, 3Q - 1) (ONE-VACUUM).
    ``label``: the passive readout label of the 48 gears ("audit" = dark: L0 clicks audit-only, OD1-type)."""
    ref = build_reference(Q=Q, body_signs=body_signs, name=name, label=label)
    terms = []
    for t in ref.terms:
        target, c, factors = t[0], t[1], t[2]
        if c % Q:
            raise ValueError("reference entry not a multiple of Q")
        terms.append((target, (c // Q) * (Q - 1), factors))
    for g in ref.gears:
        terms.append((g.name, 6, ((g.name, ZERO, "b"),)))
    return Block(ref.gears, tuple(terms), name=name, vacuum={g.name: 3 * Q - 1 for g in ref.gears},
                 params={"Q": Q, "body_signs": tuple(body_signs), "form": "C", "weight": "Q-1", "onsite": 6,
                         "label": label, "reversor": {g.name: "Mp" for g in ref.gears}},
                 doc="L0 in form C: ports at Q - 1 + on-site 6 (headroom stencil on L0's signed ports)", Q=Q)


def m0_matrix(body_signs=(1, -1, 1)):
    """L0's mass matrix M0 = 6*1 - Sum_d W_d (integer 48 x 48, symmetric), from universe24's coupling (read-only)."""
    import numpy as np
    from universe24.algebra.coupling import coupling
    C = coupling(tuple(body_signs))
    S0 = np.zeros((48, 48), dtype=np.int64)
    for d in range(6):
        for g in range(48):
            S0[C.ports[d][g], g] += C.weights[d][g]
    return 6 * np.eye(48, dtype=np.int64) - S0


def l0c_lapse_potential(Q: int, P: int, field: str, ns: str = "ref", body_signs=(1, -1, 1)) -> list:
    """Phi_int of form C (module docstring) as (c, [(gear, offset), ...])."""
    if (Q - 1) % P:
        raise ValueError("needs (Q - 1)/P an integer (Q - 1 = 2Pk)")
    k2 = Fraction(Q - 1, P)
    q = lambda g: f"{ns}.{g}"
    pot = []
    for g in range(48):
        nm = q(f"R{g:02d}")
        pot.append((3 * k2, [(field, ZERO), (nm, ZERO), (nm, ZERO)]))
    for t, s, ax, c in l0_hops(Q, body_signs, ns):
        w = Fraction(c, Q)
        e = gr.AXES[ax]
        pot.append((-k2 * w, [(field, ZERO), (q(t), ZERO), (q(s), ZERO)]))
        for fo in (ZERO, e):
            pot.append((k2 * w / 2, [(field, fo), (q(t), ZERO), (q(s), ZERO)]))
            pot.append((k2 * w / 2, [(field, fo), (q(t), e), (q(s), e)]))
            pot.append((-k2 * w, [(field, fo), (q(t), ZERO), (q(s), e)]))
    return pot


def build_l0c_lapse(*, Q: int, P: int, field: str, ns: str = "ref", body_signs=(1, -1, 1), oneway: bool = False,
                    name: str = "lapseL0") -> Block:
    """The form-C lapse ON L0. oneway=False: reciprocal (L0's energy sources F; Newton III). oneway=True: only L0
    reads F (clock test; designated)."""
    pot = l0c_lapse_potential(Q, P, field, ns, body_signs)
    if oneway:
        only = [f"{ns}.R{g:02d}" for g in range(48)]
        terms = gr.gradient_terms(pot, only=only, designation=L0C_READ_WHY, what="L0 form-C lapse")
    else:
        terms = gr.gradient_terms(pot, what="L0 form-C lapse")
    return Block((), tuple(terms), name=name, Q=Q,
                 params={"Q": Q, "P": P, "field": field, "body_signs": tuple(body_signs), "oneway": oneway,
                         "form": "C", "clock_factor": "1 - 2U on M0", "link_factor": "1 - 4U on T", "U": "F/(2P)"},
                 doc="form-C lapse on L0: (1 - 2U) on M0 = 6 - Sum W_d, (1 - 4U) on the difference transport")


__all__ = ["build_l0c", "build_l0c_lapse", "l0c_lapse_potential", "m0_matrix", "L0C_READ_WHY"]
