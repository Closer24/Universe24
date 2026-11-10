"""The Dirac matter's universal lapse with the Wilson term in the DIFFERENCE form ("form C for matter"). ADOPTED in the
v2 DEFAULT (manager ruling R1, 11:43: reciprocal version; B1-GRAV's split kept as the contrast mode). NEW file;
B1-GRAV's lapse (layers/gravity.py) is not changed.

Finding (tests/test_l0c.py, C3): B1-GRAV's matter lapse puts the clock factor on the whole on-site entry
(mass + 6 wilson) W0 and the link factor on the Wilson hops, so the Wilson matter's rest clock gets
m (1 - U) + 6 w U: N_rest = 1 - U (1 - 6w/m), not 1 - U (non-universal with L0's form C).
Here the matter potential is split as
    Phi_m = (m/2) b^T W0 b                                   (mass, on site)          x (1 - U(x))
          + (w/2) Sum_links (b(x) - b(y))^T W0 (b(x) - b(y))  (Wilson Laplacian)       x (1 - (F(x) + F(y))/(2P))
          + hop Sum_x Sum_d b(x + e_d)^T P_d b(x)             (sin-Dirac transport)    x (1 - (F(x) + F(x+e))/(2P))
(U = F/(2P)), which is build_matter's u at F = 0. At rest N = 1 - U exactly; light speed factor 1 - 2U (gamma = 1).
The beta = 1 read (second order, one-way designated as in B1-GRAV's build_beta) uses the SAME split: +G/(4P) on the mass
term, +(9/16)(G_x + G_y)/P on hops + Wilson difference, so every clock factor sits on the mass term only.
Integer coefficients need m in 4P Z, w in 2P Z, hop in 2P Z (default: m/(4P) = 4915, w/(4P) = 256, hop/(2P) = 1024).
"""
from __future__ import annotations

from fractions import Fraction

from ..core.tensor import Block
from . import gravity as gr
from .matter import _face, algebra, matter_names

ZERO = (0, 0, 0)
WHY_C = ("Dirac matter clock TEST read (one-way) of a static prescribed lapse gear; Wilson in difference form "
         "(proposal); the reciprocal block (oneway=False) is checked separately")
G_READ_C_WHY = ("beta=1 auxiliary G read by first-order (Dirac) matter, Wilson in difference form (clock factor +G/(4P) on "
                "the mass term, link factor +(9/16)(G_x+G_y)/P on hops + Wilson difference): a reciprocal partner would "
                "source G with the matter energy, giving G = F^2/(2P) - F at FIRST order and destroying the lapse; the "
                "reciprocal equivalent is the OD4 quartic (B1-GRAV build_beta_rank4)")


def matter_split_c(matter: Block):
    """(site potential, [(axis, link potential)]) of the matter in the difference form (qualified gear names)."""
    mp = matter.params
    m, w, hop = mp["mass"], mp["wilson"], mp["hop"]
    alg = algebra(mp.get("species", "pair"))
    W0, Pd = alg["W0"], alg["P"]
    names = [matter.qualify(x) for x in matter_names(mp.get("species", "pair"))]
    n = len(names)
    site = [(Fraction(m, 2) * int(W0[i, j]), [(names[i], ZERO), (names[j], ZERO)])
            for i in range(n) for j in range(n) if W0[i, j]]
    links = []
    for d in range(3):
        e = _face(d, +1)
        lp = []
        for i in range(n):
            for j in range(n):
                if W0[i, j] and w:                       # (w/2)[bx W0 bx + by W0 by - 2 bx W0 by]
                    c = Fraction(w, 2) * int(W0[i, j])
                    lp.append((c, [(names[i], ZERO), (names[j], ZERO)]))
                    lp.append((c, [(names[i], e), (names[j], e)]))
                    lp.append((-2 * c, [(names[i], ZERO), (names[j], e)]))
                if Pd[d][i, j] and hop:                  # hop b(x+e)_i P_d[i,j] b(x)_j
                    lp.append((Fraction(hop * int(Pd[d][i, j])), [(names[i], e), (names[j], ZERO)]))
        links.append((d, e, lp))
    return site, links, names


def matter_lapse_c_potential(*, matter: Block, P: int, field: str) -> list:
    """-(1/2)(F/P) Phi_site - (1/2)((F_x + F_y)/P) Phi_link (first-order matter, gamma = 1)."""
    site, links, _ = matter_split_c(matter)
    uF = Fraction(1, 2 * P)
    pot = [(-uF * c, [(field, ZERO)] + mono) for c, mono in site]
    for _d, e, lp in links:
        for fo in (ZERO, e):
            pot += [(-uF * c, [(field, fo)] + mono) for c, mono in lp]
    return pot


def build_matter_lapse_c(*, Q: int, P: int, field: str, matter: Block, oneway: bool = True,
                         name: str = "mlapseC", why: str = WHY_C) -> Block:
    pot = matter_lapse_c_potential(matter=matter, P=P, field=field)
    if oneway:
        only = [matter.qualify(x) for x in matter_names(matter.params.get("species", "pair"))]
        terms = gr.gradient_terms(pot, only=only, designation=why, what="matter lapse C")
    else:
        terms = gr.gradient_terms(pot, what="matter lapse C")
    return Block((), tuple(terms), name=name, Q=Q,
                 params={"Q": Q, "P": P, "field": field, "oneway": oneway, "form": "C (Wilson difference)"},
                 doc="Dirac matter lapse with the Wilson term in difference form (clock factor on the mass term only)")


def build_matter_beta_read_c(*, Q: int, P: int, G: str, matter: Block, name: str = "mbetaC") -> Block:
    """The beta = 1 read of the matter in the SAME split (B1-GRAV beta_matter_factors(1) = (1/4, 9/16)); one-way,
    designated with G_READ_C_WHY (the first-order factors actually used; its reciprocal form is the OD4 quartic)."""
    c_site, c_link = gr.beta_matter_factors(1)
    site, links, names = matter_split_c(matter)
    read = [(c_site * c / P, [(G, ZERO)] + mono) for c, mono in site]
    for _d, e, lp in links:
        for go in (ZERO, e):
            read += [(c_link * c / P, [(G, go)] + mono) for c, mono in lp]
    terms = gr.gradient_terms(read, only=names, designation=G_READ_C_WHY, what="matter beta read C")
    return Block((), tuple(terms), name=name, Q=Q, params={"Q": Q, "P": P, "G": G, "form": "C (Wilson difference)"},
                 doc="beta = 1 read of the matter, Wilson in difference form (one-way, designated)")


__all__ = ["build_matter_lapse_c", "build_matter_beta_read_c", "matter_lapse_c_potential", "matter_split_c",
           "WHY_C", "G_READ_C_WHY"]
