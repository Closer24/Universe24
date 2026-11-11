"""Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
from __future__ import annotations
from fractions import Fraction
C2_DEFAULT_ON = False
C1_ADOPTED = False
from ..core.tensor import Block, GearType
from .gauge import AXES, UNIT, Poly, deviation_terms, vec_dot
Q8_LABEL = {'1': 0, 'i': 3, 'j': 6, '-1': 14, 'k': 17, '-k': 21, '-i': 33, '-j': 36}
Q8_ORDER = ('1', 'i', 'j', 'k', '-1', '-i', '-j', '-k')

def _ref():
    from universe24.algebra.coupling import coupling
    from universe24.algebra.group_2o import group
    return (coupling((1, 1, 1)), group())

def q8_mul_names():
    """Multiplication of Q8 element names, from universe24's 2O table (read-only)."""
    _, G = _ref()
    lab = Q8_LABEL
    inv = {v: k for k, v in lab.items()}
    return {(p, q): inv[G.multiplication[lab[p]][lab[q]]] for p in Q8_ORDER for q in Q8_ORDER}

def right_perm(qname: str) -> list[int]:
    """Label map of R_q: (R_q v)(g) = v(g q), i.e. new[g] = old[mul[g][q]]."""
    _, G = _ref()
    q = Q8_LABEL[qname]
    return [G.multiplication[g][q] for g in range(48)]

def _link_names(algebra: str):
    if algebra == 'ZQ8':
        comps = [c.replace('-', 'm') for c in Q8_ORDER]
    elif algebra == 'H':
        comps = ['1', 'i', 'j', 'k']
    else:
        raise ValueError("algebra must be 'ZQ8' or 'H'")
    return {k: [f'W{AXES[k]}_{c}' for c in comps] for k in range(3)}

def build_c2(*, kappa: int, lam: int=0, algebra: str='ZQ8', ref: str='ref', name: str='c2', field_label: str='audit') -> Block:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    if type(kappa) is not int or kappa < 0 or type(lam) is not int or (lam < 0):
        raise ValueError('kappa, lam must be non-negative ints')
    C, G = _ref()
    D = 6
    links = _link_names(algebra)
    rn = [f'{ref}.R{g:02d}' for g in range(48)]
    x0 = {}
    if kappa:
        if 1 % kappa:
            raise ValueError('Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly.')
        m = 1 // kappa
    else:
        m = 1
    if algebra == 'ZQ8':
        A = m
        for k in range(3):
            x0[links[k][0]] = A
    else:
        A = Fraction(m, 2)
    phi = Poly()
    for k in range(3):
        d = 2 * k
        e = UNIT[k]
        Wk = [Poly.var(g, (0, 0, 0), x0.get(g, 0)) for g in links[k]]
        if kappa:
            if algebra == 'ZQ8':
                for c, qn in enumerate(Q8_ORDER):
                    perm = right_perm(qn)
                    for g in range(48):
                        h = C.ports[d][g]
                        term = Poly.var(rn[g]) * Poly.var(rn[perm[h]], e) * (kappa * C.weights[d][g])
                        phi = phi + Wk[c] * term
                for g in range(48):
                    phi = phi - Poly.var(rn[g]) * Poly.var(rn[C.ports[d][g]], e) * (1 * C.weights[d][g])
            else:
                for c, qn in enumerate(('1', 'i', 'j', 'k')):
                    pp, pm = (right_perm(qn), right_perm('-' + qn if qn != '1' else '-1'))
                    for g in range(48):
                        h = C.ports[d][g]
                        bb = (Poly.var(rn[pp[h]], e) - Poly.var(rn[pm[h]], e)) * (kappa * C.weights[d][g])
                        phi = phi + Wk[c] * Poly.var(rn[g]) * bb
        phi = phi + vec_dot(Wk, Wk) * Fraction(D, 2)
        if lam:
            if algebra == 'ZQ8':
                N = vec_dot(Wk, Wk) - A * A
                phi = phi - N * N * Fraction(lam, 4)
            else:
                N = Wk[0] * m + vec_dot(Wk, Wk)
                phi = phi - N * N * Fraction(lam, 2)
    terms = deviation_terms(phi, D, x0)
    gears = [GearType(g, field_label, link=k) for k in range(3) for g in links[k]]
    r0 = 2
    params = {'kappa': kappa, 'lam': lam, 'algebra': algebra, 'ref': ref, 'A': A if algebra == 'ZQ8' else str(A), 'm': m, 'X0': dict(x0), 'r0': r0, 'reversor': {'ref.*': 'Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly.', 'new gears': 'Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly.', 'also exact': 'M on every gear (b-only tensor), not vacuum-fixing'}}
    doc = f"c2 dynamic base links ({algebra}): right-Q8 of the 48 labels made local; kappa = {kappa}, lam = {lam}; vacuum W = 0 is today's board bit for bit; " + 'Fixed integer group-link coupling; no gravitational interpretation asserted.'
    return Block(tuple(gears), tuple(terms), name=name, vacuum={g.name: r0 for g in gears}, params=params, doc=doc)

def build_c1_weights(*, kappa: int, lam: int=0, ref: str='ref', name: str='c1', field_label: str='audit') -> Block:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    C, _ = _ref()
    D = 6
    if kappa and 1 % kappa:
        raise ValueError('Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly.')
    A = 1 // kappa if kappa else 1
    rn = [f'{ref}.R{g:02d}' for g in range(48)]
    names = {k: [f'V{AXES[k]}_{g:02d}' for g in range(48)] for k in range(3)}
    x0 = {names[k][g]: A for k in range(3) for g in range(48)}
    phi = Poly()
    for k in range(3):
        d, e = (2 * k, UNIT[k])
        for g in range(48):
            V = Poly.var(names[k][g], (0, 0, 0), A)
            bb = Poly.var(rn[g]) * Poly.var(rn[C.ports[d][g]], e) * C.weights[d][g]
            if kappa:
                phi = phi + V * bb * kappa - bb * 1
            phi = phi + V * V * Fraction(D, 2)
            if lam:
                N = V * V - A * A
                phi = phi - N * N * Fraction(lam, 4)
    terms = deviation_terms(phi, D, x0)
    gears = [GearType(g, field_label, link=k) for k in range(3) for g in names[k]]
    r0 = 2
    return Block(tuple(gears), tuple(terms), name=name, vacuum={g.name: r0 for g in gears}, params={'kappa': kappa, 'lam': lam, 'A': A, 'X0': dict(x0), 'r0': r0, 'ref': ref}, doc='EXPLORATORY c1 port-weight register (48 gears per link axis); not adopted')
__all__ = ['build_c2', 'build_c1_weights', 'right_perm', 'q8_mul_names', 'Q8_LABEL', 'Q8_ORDER']
