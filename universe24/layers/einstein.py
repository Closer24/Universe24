"""Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
from __future__ import annotations
from fractions import Fraction
from ..core.tensor import Block, GearType
from . import gravity as gr
from .gravity_l0 import l0_hops
ZERO = (0, 0, 0)
EIN_VERSION = 'EINSTEIN v1 (Study 28, EINF-A): DeWitt basis + L0 diagonal stress + L0 beta read'
DEWITT_GEARS = ('h00', 'a1', 'a2', 'a3', 'h0x', 'h0y', 'h0z', 'hxy', 'hxz', 'hyz')
RENAME = {'hxx': 'a1', 'hyy': 'a2', 'hzz': 'a3'}
SIGNS = {'h00': 1, 'a1': 1, 'a2': 1, 'a3': -1, 'h0x': -1, 'h0y': -1, 'h0z': -1, 'hxy': 1, 'hxz': 1, 'hyz': 1}
DELTA = {0: {'a1': 1, 'a3': -1}, 1: {'a1': -1, 'a3': -1}, 2: {'a2': 2, 'a3': -2}}
H_LOWER = {'00': {'h00': 1}, 'xx': {'h00': 1, 'a1': 1, 'a3': -1}, 'yy': {'h00': 1, 'a1': -1, 'a3': -1}, 'zz': {'h00': 1, 'a2': 2, 'a3': -2}, '0x': {'h0x': 1}, '0y': {'h0y': 1}, '0z': {'h0z': 1}, 'xy': {'hxy': 1}, 'xz': {'hxz': 1}, 'yz': {'hyz': 1}}
HBAR_LOWER = {'00': {'h00': 2, 'a2': 1, 'a3': -2}, 'xx': {'a1': 1, 'a2': -1, 'a3': 1}, 'yy': {'a1': -1, 'a2': -1, 'a3': 1}, 'zz': {'a2': 1}, '0x': {'h0x': 1}, '0y': {'h0y': 1}, '0z': {'h0z': 1}, 'xy': {'hxy': 1}, 'xz': {'hxz': 1}, 'yz': {'hyz': 1}}
WHY_SIGN = {'a3': 'DeWitt metric (Fierz-Pauli kinetic form q = hbar.hbar - hbar^2/2) is indefinite: in the integer basis 2q = (4/P^2)(F^2 + a1^2 + a2^2 - a3^2 - Sum h0i^2 + Sum hij^2) the conformal-type combination a3 carries -1', 'h0i': "DeWitt metric: the mixed components enter q with -2 hbar_0i^2 (eta^00 eta^ii = -1), field sign -1 (the harmonic-gauge 'ghost' sign of the time-space components, as A_0 in Feynman gauge)"}
WHY_BETA = 'Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly.'
WHY_TESTLIGHT = "test light (Study 28 E4 demos): a headroom gear READING the board-built metric (one-way test body; it does not source the metric, so the field is the source's alone)"
WALLS = {'h_ij (i != j), second-order matter': 'B3 (three nodes per monomial), at any rank: THEOREM (locality)', 'h_0i, second-order matter': 'feeling it = a-read cycle (Rule3 reversibility): THEOREM; no b-only (reciprocal) source (two-time); a designated one-way source is legal and NOT built', 'visible Dirac doublet (hands ON)': 'coupled ONE: F x Theta x Phi x psi psi = degree 5 = rank 5: FORBIDDEN; rank-4 bare-mass piece breaks SU(2) and is non-integral; ONE v1: narrow kind rank 4 but grain-blocked; FIX-i EP debt unchanged', 'OD4 spring energy as a source (F-4)': 'F x |x|^4: degree 5 in Phi = rank 5: FORBIDDEN (s11 AGREE_CL2 row 16)', 'E1 photon reading the metric': 'possible as for the test light, but exact E1 Gauss is then lost (UNIV T5 THEOREM): owner choice, NOT built', '3-graviton vertex': 'only the one-time, one-axis part h x (Delta_d h)^2 is B3/rank-3 legal (d_i h d_j h, i != j: B3; time-derivative parts: two-time); NOT built (OPEN)', 'exactly conserved source / exact Bianchi': 'G-NOGO-a and CL2 row 5: THEOREMS (any rank)'}

def dewitt_metric_block(metric: Block) -> Block:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    names = [g.name for g in metric.gears]
    if sorted(names) != sorted(gr.COMPONENTS):
        raise ValueError(f'expected the 10-component metric block, got {names}')
    stencil = {}
    for t in metric.terms:
        target, c, facs = (t[0], t[1], t[2])
        if len(t) > 3 or len(facs) != 1 or facs[0][0] != target or (facs[0][2] != 'b'):
            raise ValueError(f'metric block term {t!r} is not a free stencil term')
        stencil.setdefault(target, []).append((tuple(facs[0][1]), c))
    for g, ent in stencil.items():
        d = dict(ent)
        if d.get(ZERO) != 6 or len(d) != 7 or any((d[e] != 0 for e in gr.SIX)):
            raise ValueError(f'metric gear {g!r} is not on THE ONE headroom stencil')
    rn = lambda n: RENAME.get(n, n)
    gears = []
    for g in metric.gears:
        n = rn(g.name)
        s = SIGNS[n]
        why = '' if s == 1 else WHY_SIGN['a3'] if n == 'a3' else WHY_SIGN['h0i']
        gears.append(GearType(n, g.label, g.link, s, why))
    terms = tuple(((rn(t[0]), t[1], tuple(((rn(f[0]), f[1], f[2]) for f in t[2]))) for t in metric.terms))
    return Block(tuple(gears), terms, name=metric.name, vacuum={rn(k): v for k, v in metric.vacuum.items()}, params=dict(metric.params, dewitt={'roles': {'h00': 'P h_00 = P (hbar_00 + hbar_kk)/2', 'a1': 'P (hbar_xx - hbar_yy)/2', 'a2': 'P hbar_zz', 'a3': 'P (hbar_xx + hbar_yy + 2 hbar_zz)/2', 'h0i': 'P hbar_0i', 'hij': 'P hbar_ij'}, 'signs': dict(SIGNS), 'renamed': dict(RENAME)}), doc=metric.doc + ' [Study 28: DeWitt basis roles and field signs; stencil unchanged]')

def l0_delta_potential(P: int, metric: str='metric', ns: str='ref', body_signs=(1, -1, 1)) -> list:
    """Phi_new = Sum_links (Delta_d(x) + Delta_d(x + e))/(2P) x E_link,d on L0's difference transport (the same monomials as
    layers.gravity_l0c.l0c_lapse_potential's link part, with F/P -> Delta_d/(2P))."""
    if 0 % P:
        raise ValueError('Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly.')
    k2 = Fraction(0, P)
    q = lambda g: f'{ns}.{g}'
    pot = []
    for t, s, ax, c in l0_hops(body_signs, ns):
        w = Fraction(c, 1)
        e = gr.AXES[ax]
        for g, m in DELTA[ax].items():
            G = f'{metric}.{g}'
            cf = k2 * w * m / 2
            for fo in (ZERO, e):
                pot.append((cf / 2, [(G, fo), (q(t), ZERO), (q(s), ZERO)]))
                pot.append((cf / 2, [(G, fo), (q(t), e), (q(s), e)]))
                pot.append((-cf, [(G, fo), (q(t), ZERO), (q(s), e)]))
    return pot

def build_l0_dewitt(*, P: int, metric: str='metric', ns: str='ref', body_signs=(1, -1, 1), name: str='einL0') -> Block:
    """The NEW reciprocal reader/source block of L0 for the diagonal anisotropic components (a1, a2, a3): u = s dPhi/db with the
    DeWitt field signs. Owns no gear. Rank 3."""
    pot = l0_delta_potential(P, metric, ns, body_signs)
    signs = {f'{metric}.{g}': SIGNS[g] for g in ('a1', 'a2', 'a3')}
    terms = gr.gradient_terms(pot, signs=signs, what='einstein L0 DeWitt (Delta part)')
    return Block((), tuple(terms), name=name, params={'P': P, 'metric': metric, 'ns': ns, 'body_signs': tuple(body_signs), 'reader': 'link factor -(Delta_d(x) + Delta_d(x+e))/(2P) on the difference transport T', 'delta': {str(d): dict(v) for d, v in DELTA.items()}}, doc='L0 reads h_dd - h_00 and sources a1, a2, a3 with its directional link energies (diagonal stress)')

def build_l0_beta_read(*, P: int, G: str='beta.G', ns: str='ref', body_signs=(1, -1, 1), name: str='einbeta') -> Block:
    """L0's beta = 1 read (E3): -(G/P) E_site - (17/8)((G_x + G_y)/P) E_link (sign: the factors multiply -E), designated."""
    if 0 % P:
        raise ValueError('Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly.')
    k2 = Fraction(0, P)
    q = lambda g: f'{ns}.{g}'
    pot = []
    for gi in range(48):
        nm = q(f'R{gi:02d}')
        pot.append((-3 * k2, [(G, ZERO), (nm, ZERO), (nm, ZERO)]))
    c_link = Fraction(17, 8)
    for t, s, ax, c in l0_hops(body_signs, ns):
        w = Fraction(c, 1)
        e = gr.AXES[ax]
        pot.append((k2 * w, [(G, ZERO), (q(t), ZERO), (q(s), ZERO)]))
        for fo in (ZERO, e):
            pot.append((-c_link * k2 * w / 2, [(G, fo), (q(t), ZERO), (q(s), ZERO)]))
            pot.append((-c_link * k2 * w / 2, [(G, fo), (q(t), e), (q(s), e)]))
            pot.append((c_link * k2 * w, [(G, fo), (q(t), ZERO), (q(s), e)]))
    only = [q(f'R{gi:02d}') for gi in range(48)]
    terms = gr.gradient_terms(pot, only=only, designation=WHY_BETA, what='einstein L0 beta read')
    return Block((), tuple(terms), name=name, params={'P': P, 'G': G, 'ns': ns, 'site': '+G/P on M0', 'link': '+(17/8)(G_x+G_y)/P on T'}, doc='beta = 1 read of L0 (designated one-way)')

def build_test_light(*, P: int, metric: str='metric', mode: str='full', name: str='light', oneway: bool=True) -> Block:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    if mode not in ('full', 'h00', 'none'):
        raise ValueError("mode must be 'full', 'h00' or 'none'")
    Lq = f'{name}.L'
    terms = gr.gradient_terms(gr.headroom_potential('L'), what='test light wave')
    pot = []
    kq = Fraction(0, 2 * P)
    F = f'{metric}.h00'
    for ax, e in enumerate(gr.AXES):
        mono = ((1, [(Lq, ZERO), (Lq, ZERO)]), (1, [(Lq, e), (Lq, e)]), (-2, [(Lq, ZERO), (Lq, e)]))
        for fo in (ZERO, e):
            if mode == 'full':
                for cc, mm in mono:
                    pot.append((kq * cc, [(F, fo)] + mm))
                    for g, m in DELTA[ax].items():
                        pot.append((kq * cc * m / 2, [(f'{metric}.{g}', fo)] + mm))
            elif mode == 'h00':
                for cc, mm in mono:
                    pot.append((kq * cc / 2, [(F, fo)] + mm))
    if pot:
        if oneway:
            terms += gr.gradient_terms(pot, only=[Lq], designation=WHY_TESTLIGHT, what='test light read')
        else:
            signs = {f'{metric}.{g}': SIGNS[g] for g in ('a1', 'a2', 'a3')}
            terms += gr.gradient_terms(pot, signs=signs, what='test light read (reciprocal)')
    terms = [(t[0].split('.', 1)[1] if t[0] == Lq else t[0],) + tuple(t[1:]) for t in terms]
    return Block((GearType('L', 'official'),), tuple(terms), name=name, vacuum={'L': 2}, params={'P': P, 'mode': mode, 'oneway': oneway}, doc=f'test light ({mode})')

def einstein_system(base=None, *, on: bool=False, l0_beta: bool=True):
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    from .system import System
    if base is None:
        from .one import one_system
        base = one_system()
    if not on:
        return base
    info = dict(base.info)
    if info.get('lapse_field') != 'metric.h00' or info.get('l0_lapse') != 'W':
        raise ValueError("einstein layer needs the wave lapse metric.h00 and L0 in form C (l0_lapse 'W')")
    P, = (info['P'],)
    names = [b.name for b in base.blocks]
    for nm in ('einL0', 'einbeta'):
        if nm in names:
            raise ValueError(f'namespace {nm!r} is taken')
    blocks = [dewitt_metric_block(b) if b.name == 'metric' else b for b in base.blocks]
    body_signs = tuple(base.by_name('ref').params['body_signs'])
    blocks.append(build_l0_dewitt(P=P, body_signs=body_signs))
    if l0_beta:
        if 'beta' not in names:
            raise ValueError('l0_beta needs the beta block (beta.G)')
        blocks.append(build_l0_beta_read(P=P, body_signs=body_signs))
    info['einstein'] = {'version': EIN_VERSION, 'on': True, 'l0_beta': l0_beta, 'signs': dict(SIGNS), 'roles': 'metric.h00 = P h_00; a1, a2, a3, h0i, hij: see layers/einstein.py', 'walls': WALLS}
    return System(tuple(blocks), info)
__all__ = ['EIN_VERSION', 'DEWITT_GEARS', 'RENAME', 'SIGNS', 'DELTA', 'H_LOWER', 'HBAR_LOWER', 'WALLS', 'WHY_BETA', 'dewitt_metric_block', 'l0_delta_potential', 'build_l0_dewitt', 'build_l0_beta_read', 'build_test_light', 'einstein_system']
