"""GRAV-FIX (manager 12:12, BANG-2 finding): a drop-in beta = 1 auxiliary block whose G gear is DETUNED from the lapse
field. NEW file; layers/gravity.py (frozen) is imported read-only.

Mechanism (NOTES_gravity.md, GRAV-FIX T1): metric.h00 (F) and the default beta.G share the ONE headroom stencil, whose
corner mode k = (pi, pi, pi) sits at cos w = -1 + 2/Q (marginal); G's source -k Lap(F^2) contains -2k Fbar Lap f, so F's
corner component drives G's corner at the same frequency (resonance).
Fix: G gets a reduced face weight w_G (Laplacian form u = w_G Sum_6 G + (6Q - 6 w_G) G, i.e. b' + a = 2b + (w_G/3Q) Lap b)
and the source -(w_G/(2P)) Lap(F^2), so the static law is still G = F^2/(2P) EXACTLY (discrete Leibniz; beta = 1 kept),
while every G mode is slower than F's (c_G^2 = c_F^2 w_G/(Q-1)): no resonance at any k != 0 (S1-M2 Y15 rule).
(A) w_G = (Q-1)/2 (stencil B: corner at cos w = 1/Q); (B) w_G = 3(Q-1)/4 (corner at cos w = -1/2).
Same block name "beta", same gear "G", vacuum 3Q - 1: the default's matter read (mbeta) and e1d reference "beta.G" as before.
"""
from __future__ import annotations

from fractions import Fraction

from ..core.tensor import Block, GearType
from . import gravity as gr


def build_beta_detuned(*, Q: int, P: int, k: int, field: str, num: int = 1, den: int = 2, name: str = "beta",
                       gear: str = "G", r0: int | None = None) -> Block:
    """beta = 1 auxiliary G with face weight w_G = (Q - 1) num/den and one-way source -(w_G/(2P)) Lap(F^2)
    (designated G_SOURCE_WHY). Needs Q - 1 = 2Pk and k num/den an integer."""
    if Q - 1 != 2 * P * k:
        raise ValueError("needs Q - 1 = 2Pk")
    wG = Fraction((Q - 1) * num, den)
    kG = wG / (2 * P)
    if wG.denominator != 1 or kG.denominator != 1:
        raise ValueError("w_G and w_G/(2P) must be integers")
    wG, kG = int(wG), int(kG)
    r0 = 3 * Q - 1 if r0 is None else r0
    gq = f"{name}.{gear}"
    terms = gr.gradient_terms(gr.laplacian_form_potential(gear, Q, wG), what="beta detuned wave")
    src = gr.lap_potential(Fraction(-kG), gq, [(field, (0, 0, 0)), (field, (0, 0, 0))])
    terms += gr.gradient_terms(src, only=[gq], designation=gr.G_SOURCE_WHY, what="beta detuned source")
    return Block((GearType(gear, "audit"),), tuple(terms), name=name, vacuum={gear: r0},
                 params={"Q": Q, "P": P, "k": k, "field": field, "w_G": wG, "k_G": kG, "detune": f"{num}/{den}",
                         "reversor": {gear: "Mp"}},
                 doc="beta = 1 auxiliary G detuned from the lapse field (GRAV-FIX)", Q=Q)


def replace_beta(blocks, fixed: Block):
    """Return the block tuple with the block named fixed.name replaced (composition order kept)."""
    out, hit = [], False
    for b in blocks:
        if b.name == fixed.name:
            out.append(fixed)
            hit = True
        else:
            out.append(b)
    if not hit:
        raise KeyError(fixed.name)
    return tuple(out)
