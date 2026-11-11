"""Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
from __future__ import annotations
from fractions import Fraction
from ..core.tensor import Block
from . import gravity as gr
from .gauge import ALGEBRAS, UNIT, Poly, build_gauge, gear_names, vec_dot
ZERO = (0, 0, 0)
GAUGE_GROUPS = ('su2', 'su3', 'u1')
FORMS = ('site', 'cov', 'vac')
UNIVERSALITY_DEFAULT_ON = False
WHY_TEST = 'UNIVERSALITY TEST read (one-way) of a static PRESCRIBED lapse gear (as matter_lapse_c WHY_C); the reciprocal block (oneway=False) is the composed form'

def rest_coefficient(params: dict) -> int:
    """M = mass + 6 kappa A: the k = 0 rest coefficient of the gauge matter in the vacuum (cos w0 = M/D)."""
    return params['mass'] + 6 * params['kappa'] * params['A']

def universality_mass(params: dict, P: int) -> int:
    """The automatic normalization-dependent calibration is retired."""
    raise NotImplementedError('calibration removed; choose an explicit integral fixed-six tensor')

def _poly_to_pot(poly: Poly) -> list:
    pot = []
    for key, c in poly.t.items():
        if not key:
            if c:
                raise ValueError('lapse composite has a constant term')
            continue
        pot.append((c, [(g, off) for g, off in key]))
    return pot

def gauge_lapse_potential(block: Block, *, P: int, field: str, form: str='site') -> list:
    """Phi_L of U1 for one compact gauge layer block (qualified gear names), as (coeff, [(gear, offset), ...])."""
    if form not in FORMS:
        raise ValueError(f'form must be one of {FORMS}')
    p = block.params
    group = p['group']
    if group not in GAUGE_GROUPS:
        raise ValueError('not a compact gauge layer block')
    alg = ALGEBRAS[group]
    A, kappa = (p['A'], p['kappa'])
    M = rest_coefficient(p)
    matter, links, _paths = gear_names(group, p['use_P'])
    q = block.qualify
    x0 = {g: A * alg.one[c] for k in range(3) for c, g in enumerate(links[k])}
    uF = Fraction(-1, 2 * P)

    def psi(off):
        return [Poly.var(q(g), off) for g in matter]
    Fx = Poly.var(field, ZERO)
    p0 = psi(ZERO)
    total = Fx * vec_dot(p0, p0) * (uF * Fraction(M, 2))
    if form in ('cov', 'vac'):
        for k in range(3):
            e = UNIT[k]
            pe = psi(e)
            if form == 'cov':
                Uk = [Poly.var(q(g), ZERO, x0[g]) for g in links[k]]
            else:
                Uk = [Poly.const(A * alg.one[c]) for c in range(alg.m)]
            H = vec_dot(p0, alg.apply(Uk, pe)) * kappa - (vec_dot(p0, p0) + vec_dot(pe, pe)) * Fraction(kappa * A, 2)
            total = total + (Fx + Poly.var(field, e)) * H * uF
    return _poly_to_pot(total)

def _integrality_hint(p: dict, P: int, form: str) -> str:
    M = rest_coefficient(p)
    bad = []
    if M % (4 * P):
        bad.append(f'M = mass + 6 kappa A = {M} not in 4P Z (M/(4P) = {Fraction(M, 4 * P)})')
    if form in ('cov', 'vac') and p['kappa'] * p['A'] % (4 * P):
        bad.append(f"kappa A = {p['kappa'] * p['A']} not in 4P Z")
    if form == 'cov' and p['kappa'] % (2 * P):
        bad.append(f"kappa = {p['kappa']} not in 2P Z (kappa/(2P) = {Fraction(p['kappa'], 2 * P)}): the covariant link factor on the gauge part kappa <psi, W psi> is not an integer coefficient")
    return '; '.join(bad) or 'integral'

def build_gauge_lapse(*, block: Block, P: int, field: str, form: str='site', oneway: bool=False, name: str | None=None, why: str=WHY_TEST) -> Block:
    """U1 for one compact gauge layer. oneway=False: ONE potential, reciprocal (the gauge matter sources F).
    oneway=True: only the gauge gears read F (designated; for a static PRESCRIBED lapse gear in tests)."""
    p = block.params
    pot = gauge_lapse_potential(block, P=P, field=field, form=form)
    hint = _integrality_hint(p, P, form)
    try:
        if oneway:
            matter, links, paths = gear_names(p['group'], p['use_P'])
            own = [block.qualify(g) for g in matter + [g for k in range(3) for g in links[k]] + [g for v in paths.values() for g in v]]
            terms = gr.gradient_terms(pot, only=own, designation=why, what=f"universality lapse ({p['group']})")
        else:
            terms = gr.gradient_terms(pot, what=f"universality lapse ({p['group']})")
    except ValueError as exc:
        raise ValueError(f'universality form {form!r} on {block.name!r} is NOT integral at P = {P}: {hint}') from exc
    return Block((), tuple(terms), name=name or f'ulapse_{block.name}', params={'P': P, 'field': field, 'form': form, 'oneway': oneway, 'group': p['group'], 'M': rest_coefficient(p), 'integrality': hint}, doc=f"universal lapse of the {p['group']} matter, form {form} (clock 1 - U on M |psi|^2 / 2" + ('' if form == 'site' else ', link 1 - 2U on the difference composite H') + ')')

def photon_lapse_potential(em: Block, *, P: int, field: str) -> list:
    """The automatic normalization-dependent calibration is retired."""
    raise NotImplementedError('calibration removed; choose an explicit integral fixed-six tensor')

def build_photon_lapse(*, em: Block, P: int, field: str, oneway: bool=False, name: str='ulight', why: str=WHY_TEST) -> Block:
    """Retired normalization-dependent calibration; no fixed-six equivalence is asserted."""
    raise NotImplementedError('this automatic large-divisor calibration was removed; supply an explicit fixed-six tensor instead')

def universality_blocks(blocks, info: dict, *, gauge_form: str='site', photon: bool=True):
    """Retired normalization-dependent calibration; no fixed-six equivalence is asserted."""
    raise NotImplementedError('this automatic large-divisor calibration was removed; supply an explicit fixed-six tensor instead')

def compose_universality(system, *, on: bool=UNIVERSALITY_DEFAULT_ON, **kw):
    """NEW System with the universality candidate (on=True), else ``system`` unchanged."""
    if not on:
        return system
    from .system import System
    blocks, info = universality_blocks(list(system.blocks), system.info, **kw)
    return System(tuple(blocks), info)
__all__ = ['build_gauge_lapse', 'build_photon_lapse', 'gauge_lapse_potential', 'photon_lapse_potential', 'rest_coefficient', 'universality_mass', 'universality_blocks', 'compose_universality', 'FORMS', 'GAUGE_GROUPS', 'UNIVERSALITY_DEFAULT_ON', 'WHY_TEST']
