"""Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
from __future__ import annotations
from math import gcd
from ..core.lattice import DIRECTIONS
from ..core.tensor import Block, GearType
from .matter import _block, _face, algebra, matter_names
A_NAMES = ('A_x', 'A_y', 'A_z')
PHI = 'Phi'
ZERO = (0, 0, 0)
REVERSOR_EM = {'matter': "K o M' (layers.matter.REVERSOR_MATTER)", 'A_d': "M' = (b, a, R'(r))", 'Phi': '(a, b, r) -> (-Phi_next, -Phi.b, r), Phi_next = 2 Phi.b - Phi.a - div A.b + div A.a', 'central': 'X^2 = Jp on the matter gears', 'vacuum': 'Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly.', 'alternative': 'Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly.', 'implementation': 'prepare.em.x_reversor / prepare.em.x_reversor_core (core/reversors building blocks)'}
WHY_PHI_READ = 'E1 centred potential read (s4 A7/P-iv): the matter reads the Lorenz ACCUMULATOR Phi, which has no matter source by design (the charge reaches Phi only through the exact current -> A -> D_t Phi = -div A); a lattice transpose (Phi sourced by the on-site density) would break the exact Lorenz C == 0 (s4 A6). Unavoidable in E1; reciprocal in the continuum (Newton III via CF-1).'
WHY_A_READ = 'E1 on-site alpha.A (and the div A part of the centred potential): its lattice transpose (an on-site current) is NOT the exactly conserved current; the conserved current of on-site-coupled matter is the A-free link hopping current (s4 A4). The literal transpose of that current (linear Peierls) adds a rank-4 diamagnetic current and loses exact continuity/Gauss (s4 D4: 57,718/58,000); no finite rank closes. Unavoidable in E1; reciprocal in the continuum.'
WHY_SOURCE = 'E1 source = the EXACT free hopping current of the matter (s4 A4): exact continuity, Lorenz and dressed Gauss. Its literal partner (Peierls action) breaks them (D4). It is the continuum transpose of the on-site alpha.A action; Newton III needs only a species-independent source/action ratio (CF-1).'
WHY_ACC = 'Lorenz ACCUMULATOR (first-order-in-time relation D_t Phi = -div A, rounding-free, s4 A6): Phi is slaved to A; a reciprocal partner would add grad Phi to the A wave equation and leave Lorenz gauge.'
WHY_BLIND = 'CONTROL ONLY (S4-P R17 / S4-M E8): charge-blind action with no matching source; breaks Newton III'
WHY_DRIVER = 'MECHANISM: prescribed current (driver gear = initial data of a sourceless marginal/linear gear) feeding the A source; a prescribed current has no reaction by construction'

def _hs_ws(hop: int, wilson: int) -> tuple[int, int, int]:
    g = gcd(hop, wilson)
    if g == 0:
        raise ValueError('matter with hop = wilson = 0 has no current')
    return (hop // g, wilson // g, g)

def build_em(*, matter: Block | None, g_phi: int, g_A: int, sigma: int, stencil: str='headroom', vector: str='onsite', blind: int=0, name: str='em', label: str='audit', r0: int | None=None) -> Block:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    for nm, v in (('g_phi', g_phi), ('g_A', g_A), ('sigma', sigma), ('blind', blind)):
        if type(v) is not int:
            raise TypeError(f'{nm} must be a Python int')
    if stencil not in ('headroom', 'edge'):
        raise ValueError("stencil must be 'headroom' or 'edge'")
    if vector not in ('onsite', 'peierls'):
        raise ValueError("vector must be 'onsite' or 'peierls'")
    D = 6
    r0 = 2 if r0 is None else r0
    gears = [GearType(A_NAMES[k], label, k) for k in range(3)] + [GearType(PHI, label)]
    terms = []
    w_nb, w_on = (0, 6) if stencil == 'headroom' else (1, 0)
    for k in range(3):
        for f in DIRECTIONS:
            terms.append((A_NAMES[k], w_nb, ((A_NAMES[k], f, 'b'),)))
        if w_on:
            terms.append((A_NAMES[k], w_on, ((A_NAMES[k], ZERO, 'b'),)))
    terms.append((PHI, 6, ((PHI, ZERO, 'b'),)))
    for k in range(3):
        back = _face(k, -1)
        terms.append((PHI, -3 * 1, ((A_NAMES[k], ZERO, 'b'),), {'designated_one_way': WHY_ACC}))
        terms.append((PHI, 3, ((A_NAMES[k], back, 'b'),), {'designated_one_way': WHY_ACC}))
        terms.append((PHI, 3, ((A_NAMES[k], ZERO, 'a'),)))
        terms.append((PHI, -3 * 1, ((A_NAMES[k], back, 'a'),)))
    params = {'g_phi': g_phi, 'g_A': g_A, 'sigma': sigma, 'stencil': stencil, 'vector': vector, 'blind': blind, 'label': label, 'r0': r0, 'matter': None if matter is None else matter.name, 'reversor': REVERSOR_EM}
    if matter is not None:
        mp = matter.params
        if mp.get('species') != 'pair':
            raise ValueError("EM couples to the charged species: the 16-channel pair (species='pair')")
        alg = algebra('pair')
        n = alg['n']
        mn = [matter.qualify(x) for x in matter_names('pair')]
        hs, ws, g = _hs_ws(mp['hop'], mp['wilson'])
        params.update({'hop': mp['hop'], 'wilson': mp['wilson'], 'hs': hs, 'ws': ws, 'g': g})
        V, PJp, Jp, P, W0 = (alg['V'], alg['PJp'], alg['Jp'], alg['P'], alg['W0'])
        Ms = [Jp @ (hs * P[d] - ws * W0) for d in range(3)]
        if sigma:
            for d in range(3):
                fwd = _face(d, +1)
                for i in range(n):
                    for j in range(n):
                        if Ms[d][i, j]:
                            terms.append((A_NAMES[d], int(sigma * Ms[d][i, j]), ((mn[i], fwd, 'b'), (mn[j], ZERO, 'b')), {'designated_one_way': WHY_SOURCE}))
        for i in range(n):
            for j in range(n):
                if not V[i, j] or not g_phi:
                    continue
                c = int(g_phi * V[i, j])
                terms.append((mn[i], 3 * c, ((PHI, ZERO, 'b'), (mn[j], ZERO, 'b')), {'designated_one_way': WHY_PHI_READ}))
                terms.append((mn[i], -c, ((PHI, ZERO, 'a'), (mn[j], ZERO, 'b'))))
                for k in range(3):
                    back = _face(k, -1)
                    terms.append((mn[i], -c, ((A_NAMES[k], ZERO, 'b'), (mn[j], ZERO, 'b')), {'designated_one_way': WHY_A_READ}))
                    terms.append((mn[i], c, ((A_NAMES[k], back, 'b'), (mn[j], ZERO, 'b')), {'designated_one_way': WHY_A_READ}))
                    terms.append((mn[i], c, ((A_NAMES[k], ZERO, 'a'), (mn[j], ZERO, 'b'))))
                    terms.append((mn[i], -c, ((A_NAMES[k], back, 'a'), (mn[j], ZERO, 'b'))))
        if vector == 'onsite' and g_A:
            for d in range(3):
                back = _face(d, -1)
                for i in range(n):
                    for j in range(n):
                        if PJp[d][i, j]:
                            c = int(g_A * PJp[d][i, j])
                            terms.append((mn[i], c, ((A_NAMES[d], ZERO, 'b'), (mn[j], ZERO, 'b')), {'designated_one_way': WHY_A_READ}))
                            terms.append((mn[i], c, ((A_NAMES[d], back, 'b'), (mn[j], ZERO, 'b')), {'designated_one_way': WHY_A_READ}))
        elif vector == 'peierls' and sigma:
            for d in range(3):
                fwd, back = (_face(d, +1), _face(d, -1))
                for i in range(n):
                    for j in range(n):
                        if Ms[d][j, i]:
                            terms.append((mn[i], int(sigma * Ms[d][j, i]), ((A_NAMES[d], ZERO, 'b'), (mn[j], fwd, 'b'))))
                        if Ms[d][i, j]:
                            terms.append((mn[i], int(sigma * Ms[d][i, j]), ((A_NAMES[d], back, 'b'), (mn[j], back, 'b'))))
            terms = [t[:3] if len(t) == 4 and t[0] in A_NAMES and (t[3]['designated_one_way'] == WHY_SOURCE) else t for t in terms]
        if blind:
            for i in range(n):
                terms.append((mn[i], blind, ((PHI, ZERO, 'b'), (mn[i], ZERO, 'b')), {'designated_one_way': WHY_BLIND}))
    vac = {nm: r0 for nm in A_NAMES + (PHI,)}
    return _block(gears, terms, name, vac, params, 'E1: Lorenz-gauge A_i link gears (headroom stencil) + rounding-free Lorenz accumulator Phi + time-centred potential read + on-site alpha.A; source = exact free hopping current')

def build_current_driver(*, em: Block, axis: int, kappa: int, coupling: int, name: str='drive', r0: int | None=None) -> Block:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    if axis not in (0, 1, 2):
        raise ValueError('axis must be 0, 1 or 2')
    D = 6
    if type(kappa) is not int or not -D <= kappa <= D or type(coupling) is not int:
        raise ValueError('kappa must be an int in [-D, D], coupling an int')
    r0 = 2 if r0 is None else r0
    target = em.qualify(A_NAMES[axis])
    terms = [('S', kappa, (('S', ZERO, 'b'),)), (target, coupling, (('S', ZERO, 'b'),), {'designated_one_way': WHY_DRIVER})]
    return _block([GearType('S', 'audit')], terms, name, {'S': r0}, {'axis': axis, 'kappa': kappa, 'coupling': coupling, 'em': em.name, 'r0': r0, 'MECHANISM': True}, 'MECHANISM: prescribed current driver gear')
