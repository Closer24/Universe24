"""Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
from __future__ import annotations
from ..core.tensor import Block, GearType
O = (0, 0, 0)
OBSERVER = 'observer detector: records without back-action (Study 5 D3)'
DRIVE = "common drive: the DC source sets the pair's shared remainder (token born from the vacuum, Study 5 B6/T4); it does not read the detectors"
SEQ = 'sequential router link gear: reads the arriving intensity stream without back-action (observer, S5-O2)'
PAR = 'parallel-read control exit gear: reads its intensity without back-action (observer, Study 5 B7 control)'
IMPRINT = "choice-front imprint (F7): P2R's two-update kick q*(b_C - a_C), -q*a_C, gated by the photon marker on the neighbour link; one-way, the front does not push back on Alice's detectors or setting clock"
EMIT = "choice-front emission (F7): Alice's front clock drives the front fibre one-way through an exact two-node source (b_F(x) - a_F(x+e)); the far side reads the front without back-action"
WPATH = 'Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly.'
GATED = 'observer detector: records without back-action (Study 5 D3); read once, gated by a flash (rank 4)'
DEC = "observer detector with the D12b gated readout of the kicked arm (P_dec, rank 4): records without back-action on the arms (Study 5 D3); the 90-degree kick is in the readout (P_dec's declared equivalence)"

def _f(g, off=O, field='b'):
    return (g, tuple(off), field)

def _one_way(t, c, facs, why):
    return (t, c, tuple(facs), {'designated_one_way': why})

def _neg(off):
    return tuple((-v for v in off))

def _axis(axis):
    if axis not in (0, 1, 2):
        raise ValueError('axis must be 0, 1 or 2')
    e = [0, 0, 0]
    e[axis] = 1
    return tuple(e)

def _square_terms(target, coeff, xs, ys, sign, why, extra=()):
    """coeff * extra * sum_j (x_j + sign*y_j)^2 as monomials (designated with ``why``)."""
    out = []
    ext = tuple(extra)
    for x, y in zip(xs, ys):
        out.append(_one_way(target, coeff, ext + (_f(x), _f(x)), why))
        out.append(_one_way(target, 2 * sign * coeff, ext + (_f(x), _f(y)), why))
        out.append(_one_way(target, coeff, ext + (_f(y), _f(y)), why))
    return out

def build_clock_ring(*, period: int=6, prefix: str='X', name: str | None='ring', label: str='official') -> Block:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    if period == 6:
        gears = [f'{prefix}{j}' for j in range(3)]
        terms = [(g, 3, (_f(g),)) for g in gears]
    elif period == 4:
        gears = [f'{prefix}{j}' for j in range(2)]
        terms = []
    else:
        raise ValueError('period must be 6 or 4')
    return Block(tuple((GearType(g, label) for g in gears)), tuple(terms), name=name, vacuum={g: 0 for g in gears}, params={'period': period, 'prefix': prefix}, doc=f"period-{period} C0 clock ring (u = {('Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly.' if period == 6 else '0')})")

def build_fibre(*, axis: int=0, components=('F',), name: str | None='fibre', label: str='official') -> Block:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    e = _axis(axis)
    terms = []
    for c in components:
        terms.append((c, 3, (_f(c, _neg(e)),)))
        terms.append((c, 3, (_f(c, e),)))
    return Block(tuple((GearType(c, label) for c in components)), tuple(terms), name=name, vacuum={c: 0 for c in components}, params={'axis': axis, 'components': tuple(components)}, doc="exact C0 d'Alembert fibre")

def build_born_router(*, kappa: int, arm1, arm2, form: str='opposite', name: str | None='router', vacuum_r: int=0) -> Block:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    if form not in ('opposite', 'mirror'):
        raise ValueError("form must be 'opposite' or 'mirror'")
    sm = -1 if form == 'opposite' else 1
    terms = _square_terms('dP', kappa, arm1, arm2, +1, OBSERVER) + _square_terms('dM', sm * kappa, arm1, arm2, -1, OBSERVER)
    return Block((GearType('dP'), GearType('dM')), tuple(terms), name=name, vacuum={'dP': vacuum_r, 'dM': vacuum_r}, params={'kappa': kappa, 'form': form, 'arm1': tuple(arm1), 'arm2': tuple(arm2)}, doc=f'rank-3 |psi|^2 detector pair ({form} form), observer')

def build_common_drive(*, w: int, detectors, name: str | None='drive') -> Block:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    terms = [('S', 6, (_f('S'),))] + [_one_way(d, w, (_f('S'),), DRIVE) for d in detectors]
    return Block((GearType('S'),), tuple(terms), name=name, vacuum={'S': 0}, params={'w': w, 'detectors': tuple(detectors)}, doc='DC common drive')

def build_sequential_router(*, kappa: int, stream: str, name: str | None='seq') -> Block:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    return Block((GearType('Lk'),), (_one_way('Lk', kappa, (_f(stream),), SEQ),), name=name, vacuum={'Lk': 0}, params={'kappa': kappa, 'stream': stream}, doc='sequential shared-remainder router')

def build_parallel_router(*, kappa: int, streams, name: str | None='par') -> Block:
    """Parallel-read CONTROL: exit gears E1..En read their own intensities in the same update with one shared token:
    E1 input -kappa I1 (clicks iff lam < 2 kappa I1), E2..En input +kappa I_k. Designated one-way (observer)."""
    gears, terms = ([], [])
    for k, s in enumerate(streams):
        g = f'E{k + 1}'
        gears.append(GearType(g))
        terms.append(_one_way(g, -kappa if k == 0 else kappa, (_f(s),), PAR))
    return Block(tuple(gears), tuple(terms), name=name, vacuum={g.name: 0 for g in gears}, params={'kappa': kappa, 'streams': tuple(streams)}, doc='parallel-read control')
EMIT_LIGHT = "choice-front emission (F7, light carrier): Alice's front clock drives the headroom light one-way (u_P += gamma b_F); the far side reads the front without back-action"

def build_f7(*, kappa: int, axis: int=0, name: str | None='f7', bob_gate: bool=False, carrier: str='fibre', gamma: int=0) -> Block:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    e = _axis(axis)
    me = _neg(e)
    PH, C, F, P, B = ([f'{s}{j}' for j in range(3)] for s in ('PH', 'C', 'F', 'P', 'B'))
    gears = [GearType(g) for g in PH] + [GearType('PG', 'audit')] + [GearType(g) for g in C]
    gears += [GearType('dAp'), GearType('dAm')] + [GearType(g) for g in F] + [GearType(g) for g in P]
    gears += [GearType(g) for g in B] + [GearType('dBp'), GearType('dBm')]
    if bob_gate:
        gears.append(GearType('BG', 'audit'))
    if carrier not in ('fibre', 'light'):
        raise ValueError("carrier must be 'fibre' or 'light'")
    terms = []
    fibres = PH + ['PG'] + (P if carrier == 'fibre' else []) + (['BG'] if bob_gate else [])
    for g in fibres:
        terms += [(g, 3, (_f(g, me),)), (g, 3, (_f(g, e),))]
    if carrier == 'light':
        from ..core.lattice import DIRECTIONS
        for g in P:
            terms += [(g, 0, (_f(g, d),)) for d in DIRECTIONS] + [(g, 6, (_f(g),))]
    for g in C + F + B:
        terms.append((g, 3, (_f(g),)))
    for j in range(3):
        terms.append(_one_way('dAp', kappa, (_f(PH[j]), _f(PH[j])), OBSERVER))
        terms.append(_one_way('dAp', kappa, (_f(PH[j]), _f(C[j])), OBSERVER))
        terms.append(_one_way('dAm', -kappa, (_f(PH[j]), _f(PH[j])), OBSERVER))
        terms.append(_one_way('dAm', kappa, (_f(PH[j]), _f(C[j])), OBSERVER))
    for j in range(3):
        for d in ('dAp', 'dAm'):
            terms.append(_one_way(F[j], 3, (_f('PG', me), _f(d), _f(C[j])), IMPRINT))
            terms.append(_one_way(F[j], -3 * 1, (_f('PG', me), _f(d), _f(C[j], O, 'a')), IMPRINT))
            terms.append(_one_way(F[j], -3 * 1, (_f('PG', me, 'a'), _f(d, O, 'a'), _f(C[j], O, 'a')), IMPRINT))
    for j in range(3):
        if carrier == 'fibre':
            terms.append(_one_way(P[j], 3, (_f(F[j]),), EMIT))
            terms.append(_one_way(P[j], -3 * 1, (_f(F[j], e, 'a'),), EMIT))
        else:
            terms.append(_one_way(P[j], gamma, (_f(F[j]),), EMIT_LIGHT))
    gB = (_f('BG'),) if bob_gate else ()
    whyB = GATED if bob_gate else OBSERVER
    for j in range(3):
        terms.append(_one_way('dBp', kappa, gB + (_f(B[j]), _f(B[j])), whyB))
        terms.append(_one_way('dBp', kappa, gB + (_f(B[j]), _f(P[j])), whyB))
        terms.append(_one_way('dBm', -kappa, gB + (_f(B[j]), _f(B[j])), whyB))
        terms.append(_one_way('dBm', kappa, gB + (_f(B[j]), _f(P[j])), whyB))
    return Block(tuple(gears), tuple(terms), name=name, vacuum={g.name: 0 for g in gears}, params={'kappa': kappa, 'axis': axis, 'bob_gate': bob_gate, 'carrier': carrier, 'gamma': gamma}, doc='F7 light-cone choice' + (' (one-shot gated Bob)' if bob_gate else ''))

def build_which_path_W(*, arm, N: int, name: str | None='W') -> Block:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    m = 1
    gears, terms = ([], [])
    for j in range(N):
        w, x = (f'W{j}', arm[j % len(arm)])
        gears.append(GearType(w))
        terms.append(_one_way(w, 3 * m, (_f(x),), WPATH))
        terms.append(_one_way(x, 3, (_f(w),), WPATH))
    return Block(tuple(gears), tuple(terms), name=name, vacuum={g.name: 0 for g in gears}, params={'Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly.': 1, 'arm': tuple(arm), 'N': N}, doc='M2-2 which-path gears')

def build_gated_pair(*, kappa: int, arm1, arm2, gate: str, name: str | None='exit') -> Block:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    g = (_f(gate),)
    terms = _square_terms('dP', kappa, arm1, arm2, +1, GATED, g) + _square_terms('dM', kappa, arm1, arm2, -1, GATED, g)
    return Block((GearType('dP'), GearType('dM')), tuple(terms), name=name, vacuum={'dP': 0, 'dM': 0}, params={'kappa': kappa, 'arm1': tuple(arm1), 'arm2': tuple(arm2), 'gate': gate}, doc='gated exit pair (observer)')

def _rot(names, c):
    """(R^c X)_j as (sign, gear name) for the 90-degree pair rotation R: (X0, X1) -> (X1, -X0)."""
    v = [(1, names[0]), (1, names[1])]
    for _ in range(c % 4):
        v = [v[1], (-v[0][0], v[0][1])]
    return v

def build_dec_toy(*, c: int, name: str | None='dec') -> Block:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    X1, X2 = (['X1_0', 'X1_1'], ['X2_0', 'X2_1'])
    gears = [GearType(g) for g in X1 + X2] + [GearType(g) for g in ('W1', 'W2', 'dP', 'dM')]
    terms = []
    for wn, arm in (('W1', X1), ('W2', X2)):
        for x in arm:
            terms.append(_one_way(wn, 6, (_f(x), _f(x)), OBSERVER))
    for target, sgn in (('dP', 1), ('dM', -1)):
        for wn, U, V in (('W1', _rot(X1, c), [(1, X2[0]), (1, X2[1])]), ('W2', [(1, X1[0]), (1, X1[1])], _rot(X2, c))):
            for (su, u), (sv, v) in zip(U, V):
                terms.append(_one_way(target, 3, (_f(wn), _f(u), _f(u)), DEC))
                terms.append(_one_way(target, 3, (_f(wn), _f(v), _f(v)), DEC))
                terms.append(_one_way(target, 6 * sgn * su * sv, (_f(wn), _f(u), _f(v)), DEC))
    return Block(tuple(gears), tuple(terms), name=name, vacuum={g.name: 0 for g in gears}, params={'c': c}, doc='D12b QM-deviation toy (P_dec)')

def _pmul(p, q):
    """product of two polynomials {tuple(sorted gear names): int coeff}."""
    out = {}
    for k1, c1 in p.items():
        for k2, c2 in q.items():
            k = tuple(sorted(k1 + k2))
            out[k] = out.get(k, 0) + c1 * c2
    return {k: c for k, c in out.items() if c}

def _padd(*ps):
    out = {}
    for p in ps:
        for k, c in p.items():
            out[k] = out.get(k, 0) + c
    return {k: c for k, c in out.items() if c}

def _pscale(p, a):
    return {k: a * c for k, c in p.items() if a * c}

def build_spring_backaction_router(*, kappa: int, lam: int, arm1, arm2, name: str | None='bs') -> Block:
    """(ii) BACK-ACTING reciprocal detector pair with a COMPLETE OD4 spring (manager ruling 2, 09:5x):

        Phi = kappa b_dP |U|^2 + kappa b_dM |V|^2 - (lam/4) [ (b_dP^2 + |U|^2)^2 + (b_dM^2 + |V|^2)^2 ],

    U = X1 + X2, V = X1 - X2, field signs s(dP) = +1, s(dM) = -1, X0 = 0 (deviation form: no constant, vacuum fixed).
    u = s dPhi/db for every gear (the self-quartics -lam b_d^3 and -lam |U|^2 U_j are included). No designation."""
    if type(lam) is not int or lam < 0:
        raise ValueError('lam must be a non-negative int')
    U = [{(x,): 1, (y,): 1} for x, y in zip(arm1, arm2)]
    V = [{(x,): 1, (y,): -1} for x, y in zip(arm1, arm2)]
    U2 = _padd(*[_pmul(u, u) for u in U])
    V2 = _padd(*[_pmul(v, v) for v in V])
    P, M = ({('dP',): 1}, {('dM',): 1})
    sP = _padd(_pmul(P, P), U2)
    sM = _padd(_pmul(M, M), V2)
    u = {}
    u['dP'] = _padd(_pscale(U2, kappa), _pscale(_pmul(sP, P), -lam))
    u['dM'] = _pscale(_padd(_pscale(V2, kappa), _pscale(_pmul(sM, M), -lam)), -1)
    for j, (x, y) in enumerate(zip(arm1, arm2)):
        back_U = _padd(_pscale(_pmul(P, U[j]), 2 * kappa), _pscale(_pmul(sP, U[j]), -lam))
        back_V = _padd(_pscale(_pmul(M, V[j]), 2 * kappa), _pscale(_pmul(sM, V[j]), -lam))
        u[x] = _padd(back_U, back_V)
        u[y] = _padd(back_U, _pscale(back_V, -1))
    terms = [(t, c, tuple((_f(gn) for gn in key))) for t, poly in u.items() for key, c in sorted(poly.items())]
    gears = (GearType('dP'), GearType('dM', sign=-1, sign_why='opposite-sign detector of the paired link clock: its input is -kappa|X1-X2|^2 (equal remainders, Study 5 B3/T4); s = -1 makes the pair the gradient of one potential'))
    return Block(gears, tuple(terms), name=name, vacuum={'dP': 0, 'dM': 0}, params={'kappa': kappa, 'lam': lam, 'arm1': tuple(arm1), 'arm2': tuple(arm2)}, doc='back-acting reciprocal detector pair with a complete OD4 spring (rank 4)')

def build_backaction_router(*, kappa: int, g: int, arm1, arm2, name: str | None='ba') -> Block:
    """(ii) BACK-ACTING reciprocal detector pair from Universe24 potential (no designation):

        Phi = kappa b_dP |U|^2 + kappa b_dM |V|^2 - (g/2) (b_dP^2 |U|^2 + b_dM^2 |V|^2),  U = X1 + X2, V = X1 - X2,

    field signs s(dP) = +1, s(dM) = -1 (u_dM = -dPhi/db_dM = -kappa |V|^2 + g b_dM |V|^2: the opposite-sign detector).
    The arms feel u_x = dPhi/dx: the click pushes back. g = 0: rank 3 (Study 5's reciprocal coupling, D3); g = 2 kappa:
    rank 4 and sign-definite (2(kappa b - (g/2) b^2) <= 0 for every integer b, OD4 / S5-O4). Matched as the router."""
    terms = []
    gears = (GearType('dP'), GearType('dM', sign=-1, sign_why='opposite-sign detector of the paired link clock: its input is -kappa|X1-X2|^2 (equal remainders, Study 5 B3/T4); s = -1 makes the pair the gradient of one potential'))
    for x, y in zip(arm1, arm2):
        for tgt, s_y, s_t in (('dP', 1, 1), ('dM', -1, -1)):
            for fac, cf in (((_f(x), _f(x)), 1), ((_f(x), _f(y)), 2 * s_y), ((_f(y), _f(y)), 1)):
                terms.append((tgt, s_t * kappa * cf, fac))
                terms.append((tgt, -s_t * g * cf, (_f(tgt),) + fac))
        for tgt, s_v in ((x, 1), (y, -1)):
            for src in (x, y):
                s_src = 1 if src == x else -1
                terms.append((tgt, 2 * kappa, (_f('dP'), _f(src))))
                terms.append((tgt, 2 * kappa * s_v * s_src, (_f('dM'), _f(src))))
                terms.append((tgt, -g, (_f('dP'), _f('dP'), _f(src))))
                terms.append((tgt, -g * s_v * s_src, (_f('dM'), _f('dM'), _f(src))))
    return Block(gears, tuple(terms), name=name, vacuum={'dP': 0, 'dM': 0}, params={'kappa': kappa, 'g': g, 'arm1': tuple(arm1), 'arm2': tuple(arm2)}, doc=f'back-acting reciprocal detector pair (rank {(4 if g else 3)})')
MIRROR = {'build_clock_ring': "Mp (M', parity-preserving) per gear; exact (b-only); C0: any constant remainder works", 'build_fibre': 'Mp per gear; exact (b-only)', 'build_born_router': 'Mp per gear (and M); exact (b-only); kinds are mirror-even (TC.2 log check with M)', 'build_common_drive': 'Mp per gear; exact (b-only)', 'build_sequential_router': 'Mp per gear; exact (b-only)', 'build_parallel_router': 'Mp per gear; exact (b-only)', 'build_which_path_W': 'Mp per gear; exact (b-only)', 'build_gated_pair': 'Mp per gear; exact (b-only)', 'build_dec_toy': 'M (and Mp) per gear; exact (b-only)', 'build_backaction_router': 'Mp per gear; exact (b-only); NOT J-odd (even-degree terms), so no JR/JM', 'build_spring_backaction_router': 'Mp per gear; exact (b-only); NOT J-odd', 'build_f7': 'NONE KNOWN: a-read gears (gated kick, emission); per-gear M/Mp are NOT reversors (TC.12); the staged inverse is exact (rewind in every run); a staggered map for these a-read gears is OPEN'}
VACUUM_NOTE = 'Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly.'
__all__ = ['MIRROR', 'VACUUM_NOTE', 'OBSERVER', 'build_clock_ring', 'build_fibre', 'build_born_router', 'build_common_drive', 'build_sequential_router', 'build_parallel_router', 'build_f7', 'build_which_path_W', 'build_gated_pair', 'build_dec_toy', 'build_backaction_router', 'build_spring_backaction_router']
