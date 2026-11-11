"""E1 sourced by the LAPSE-DRESSED link current (INTEGRATOR, manager ruling 10:5x: local charge conservation in
curved spacetime). TENSOR BLOCKS ONLY; layers/em.py (frozen) is imported read-only and its block is extended.

In the gravity-coupled system the matter's link potential is f_d b(x)^T N_d b(x+e_d) with
    f_d(x) = 1 - (F(x) + F(x+e_d))/(2P) + (9/16) (G(x) + G(x+e_d))/P      (B1-GRAV: lapse c_link 1/2; beta read 9/16)
so the exact J' current is f_d j_d and E1's source sigma s_d must become sigma f_d s_d. The extra terms (rank 4,
b-only, link-local, designated one-way like E1's own source) are added here. Integer only for sigma in 2^24 Z at
P = 2^20 (hs = hop/g = 8, ws = wilson/g = 1): sigma = 2^24 is DECLARED (B1-EM's default 2^8 cannot carry the dressing).
"""
from __future__ import annotations
from fractions import Fraction
from ..core.tensor import Block
from .em import WHY_SOURCE, build_em
from .matter import _face, algebra, matter_names
WHY_DRESSED = "E1 source dressed by the lapse/beta link factor (INTEGRATOR, C5): the exact J' current of the gravity-coupled matter is f_d j_d; one-way like E1's source"
C_LAPSE = Fraction(1, 2)
C_BETA = Fraction(9, 16)

def build_em_dressed(*, matter: Block, g_phi: int, g_A: int, sigma: int, P: int, lapse: str='metric.h00', beta: str | None='beta.G', name: str='em') -> Block:
    base = build_em(matter=matter, g_phi=g_phi, g_A=g_A, sigma=sigma, name=name)
    hs, ws = (base.params['hs'], base.params['ws'])
    alg = algebra('pair')
    Jp, Pm, W0 = (alg['Jp'], alg['P'], alg['W0'])
    mn = [matter.qualify(x) for x in matter_names('pair')]
    extra = []
    fields = [(lapse, -C_LAPSE)] + ([(beta, C_BETA)] if beta else [])
    for d in range(3):
        M = Jp @ (hs * Pm[d] - ws * W0)
        fwd = _face(d, +1)
        for i in range(16):
            for j in range(16):
                if not M[i, j]:
                    continue
                for fld, c in fields:
                    coef = Fraction(sigma * int(M[i, j])) * c / P
                    if coef.denominator != 1:
                        raise ValueError(f'dressed source coefficient {coef} is not an integer: sigma must be in 2^24 Z at P = 2^20 (got sigma = {sigma})')
                    for off in ((0, 0, 0), fwd):
                        extra.append((f"A_{'xyz'[d]}", int(coef), ((fld, off, 'b'), (mn[i], fwd, 'b'), (mn[j], (0, 0, 0), 'b')), {'designated_one_way': WHY_DRESSED}))
    return Block(base.gears, base.terms + tuple(extra), name=base.name, vacuum=dict(base.vacuum), params={**base.params, 'dressed': {'P': P, 'lapse': lapse, 'beta': beta, 'c_lapse': str(C_LAPSE), 'c_beta': str(C_BETA)}}, doc=base.doc + ' + lapse/beta-dressed source (rank 4, designated)')
__all__ = ['build_em_dressed', 'WHY_DRESSED']
