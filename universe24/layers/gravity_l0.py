"""The universal lapse ON L0 (the 48 reference channels): a NEW file (gravity follow-up, manager 10:4x). Tensor blocks
only. Pre-registered in NOTES_gravity.md ("L0-EP").

Facts used:
* ONE-VACUUM embedding (Study 7 / ONE-M1, ONE-M2, R-M2): L0 embedded as (a, b, r) -> (a, b, Q r + s), s = Q - 1, is
  today's board bit for bit, its vacuum is (0, 0, 3Q - 1) like every layer's, and R' is an exact mirror even with FINE
  couplings into L0 (no q-lattice rule). The embedding is initial data (Block.vacuum); the tensor is unchanged.
* L0's u has no carrier term: b' + a = (1/3) Sum (signed ports) b, i.e. L0 is a pi/2-carrier ("first-order")
  network; the lapse factors are the first-order ones: clock factor N = 1 - U on the MASS part, link factor
  N/psi^2 = 1 - 2U on the TRANSPORT part (gamma = 1).
* L0's ports carry its mass and its transport at once. The split used here is an identity of the free tensor:
  c b_t(x) b_s(x+e) = c b_t(0) b_s(0) [mass: the k = 0 value, on-site] + c [b_t(x) b_s(x+e) - (b_t(x) b_s(x) +
  b_t(x+e) b_s(x+e))/2] [symmetric difference: transport]; the lapse multiplies the two parts differently.
* THEOREM (ONE-P1; integrality): with L0's ports at weight Q w (Q odd) the exact lapse needs coefficients Q w / (2P) and
  Q w / (4P): never integers for P = 2^m, m >= 1 (and gcd(Q, Q - 1) = 1 forbids a common P with the headroom gears).
  So an EXACT universal lapse on today's weights does not exist. Two minimal changes:
  (R) mode="rounded": L0 keeps weight Q (today's board bit for bit when F = 0); the lapse uses (Q - 1) w = 2Pk w in place
      of Q w: L0's clock and link factors are 1 - U (Q-1)/Q and 1 - 2U (Q-1)/Q: EP violated by the relative 1/Q.
  (W) mode="weight": L0's ports take the ONE headroom weight Q - 1 (``build_l0_weight``): the same lapse is exactly
      universal; L0's cone becomes c_Q (one cone with every field); cost: L0 is today's board only in its vacuum.
"""
from __future__ import annotations

from fractions import Fraction

from ..core.tensor import Block, GearType
from . import gravity as gr
from .reference import build_reference

ZERO = (0, 0, 0)
L0_READ_WHY = ("L0-EP clock TEST read (one-way): a static prescribed lapse gear read by L0 / matter clocks; the "
               "reciprocal block (oneway=False) is checked separately")


def l0_hops(Q: int, body_signs=(1, 1, 1), ns: str = "ref") -> list[tuple]:
    """L0's free potential Phi_L0 = Sum_x Sum_hops c b_t(x) b_s(x + e_axis) as (t, s, axis, c) with c = Q w (local gear
    names R00..R47), read from the reference block itself (generic interface spec_from_block)."""
    ref = build_reference(Q=Q, body_signs=body_signs, name=ns)
    spec = gr.spec_from_block(ref, Q=Q, order=1, carrier={g.name: 0 for g in ref.gears})
    return list(spec.hops)


def build_l0_weight(*, Q: int, body_signs=(1, 1, 1), name: str = "ref") -> Block:
    """Mode (W): the 48 reference channels with port weight (Q - 1) w instead of Q w (the ONE headroom weight).
    Vacuum (0, 0, 3Q - 1) (ONE-VACUUM). NOT today's board except in its vacuum."""
    ref = build_reference(Q=Q, body_signs=body_signs, name=name)
    terms = []
    for t in ref.terms:
        target, c, factors = t[0], t[1], t[2]
        if c % Q:
            raise ValueError("reference entry not a multiple of Q")
        terms.append((target, (c // Q) * (Q - 1), factors))
    return Block(ref.gears, tuple(terms), name=name, vacuum={g.name: 3 * Q - 1 for g in ref.gears},
                 params={"Q": Q, "body_signs": tuple(body_signs), "weight": "Q-1", "reversor": {g.name: "Mp"
                                                                                               for g in ref.gears}},
                 doc="L0 with the headroom port weight Q - 1 (mode W of the L0 lapse)", Q=Q)


def l0_lapse_potential(Q: int, P: int, field: str, ns: str = "ref", gamma: str = "GR", body_signs=(1, 1, 1)) -> list:
    """Phi_int on L0 with the split mass/transport and the effective weight (Q - 1) w (both modes):
    -(1/2)(F/P) Phi_mass - c_link ((F_x + F_y)/P) Phi_transport, c_link = 1/2 (GR) or 1/4 (1911)."""
    c_site = Fraction(1, 2)
    c_link = Fraction(1, 2) if gamma == "GR" else Fraction(1, 4)
    pot = []
    q = lambda g: f"{ns}.{g}"
    for t, s, ax, c in l0_hops(Q, body_signs, ns):
        w = Fraction(c, Q)
        ce = (Q - 1) * w                        # the effective (rounded) weight
        e = gr.AXES[ax]
        mass = [(ce, [(q(t), ZERO), (q(s), ZERO)])]
        trans = [(ce, [(q(t), ZERO), (q(s), e)]), (-ce / 2, [(q(t), ZERO), (q(s), ZERO)]),
                 (-ce / 2, [(q(t), e), (q(s), e)])]
        for cc, mono in mass:
            pot.append((-c_site * cc / P, [(field, ZERO)] + mono))
        for cc, mono in trans:
            pot.append((-c_link * cc / P, [(field, ZERO)] + mono))
            pot.append((-c_link * cc / P, [(field, e)] + mono))
    return pot


def build_l0_lapse(*, Q: int, P: int, field: str, ns: str = "ref", gamma: str = "GR", body_signs=(1, 1, 1),
                   oneway: bool = False, name: str = "lapseL0") -> Block:
    """The universal lapse ON L0 (modes R and W share this block; they differ only in L0's own weight).
    oneway=False: reciprocal (L0's energy sources F: Newton III). oneway=True: only L0 reads F (clock test)."""
    if Q - 1 != 2 * P * ((Q - 1) // (2 * P)):
        raise ValueError("needs Q - 1 = 2Pk")
    if ((Q - 1) // (2 * P)) % 2:
        raise ValueError("needs k even (the symmetric transport split halves the coefficient)")
    pot = l0_lapse_potential(Q, P, field, ns, gamma, body_signs)
    if oneway:
        only = [f"{ns}.R{g:02d}" for g in range(48)]
        terms = gr.gradient_terms(pot, only=only, designation=L0_READ_WHY, what="L0 lapse")
    else:
        terms = gr.gradient_terms(pot, what="L0 lapse")
    return Block((), tuple(terms), name=name, Q=Q,
                 params={"Q": Q, "P": P, "field": field, "gamma": gamma, "oneway": oneway,
                         "effective_weight": "Q-1 (mode R: rounded on weight-Q L0; mode W: exact on weight-(Q-1) L0)"},
                 doc="universal lapse on L0: N on the k = 0 mass part, N/psi^2 on the difference transport part")
