"""Read-only observables and exact checks for the Einstein layer (layers/einstein.py; Study 28, EINF-A). Nothing here changes a
state that is fed back into a run (AGENTS item 10). Exact integer / Fraction statements unless labelled "float diagnostic".

The current inertial fixed-six baseline is not a derivation of Einstein dynamics.

* stored_to_h / stored_to_hbar: P h_{mu nu} and P hbar_{mu nu} from the ten stored metric gears (exact integer combinations).
* dewitt_check: 2 q(hbar) = (4/P^2)(F^2 + a1^2 + a2^2 - a3^2 - Sum h0i^2 + Sum hij^2) and h = TR(hbar) on random integers.
* source_of_stored / sources_hbar: s_g = u_g - stencil (exact) and the hbar sources Box hbar = 2 s_hbar + ledger.
* conservation_defect: D_mu s^{mu nu} of the board's metric source (exact integer diagnostic; not assumed zero).
* b3_offdiagonal_wall, two_time_cycle_wall: the two walls, demonstrated by the package's own validators.
* polarisation_count: exact (sympy) count on an imposed null-momentum and harmonic-constraint ansatz. This is not a
  proof that the interacting integer dynamics enforces those constraints or propagates only two physical modes.
"""
from __future__ import annotations
import random
from fractions import Fraction
import numpy as np
from ..core.engine import OBJ, State
from ..core.tensor import AcyclicityError, LocalityError, Tensor
from ..layers.einstein import H_LOWER, HBAR_LOWER, SIGNS
ETA = {'0': -1, 'x': 1, 'y': 1, 'z': 1}
PAIRS = ('00', '0x', '0y', '0z', 'xx', 'yy', 'zz', 'xy', 'xz', 'yz')

def _comb(vals: dict, table: dict) -> dict:
    return {k: sum((c * vals[g] for g, c in row.items())) for k, row in table.items()}

def stored_to_h(vals: dict) -> dict:
    """{pair: P h_pair} (lower indices) from {gear: value} (values may be ints or numpy arrays)."""
    return _comb(vals, H_LOWER)

def stored_to_hbar(vals: dict) -> dict:
    """{pair: P hbar_pair} (lower indices)."""
    return _comb(vals, HBAR_LOWER)

def dewitt_q(hb: dict) -> Fraction:
    """q(hbar) = hbar_{mu nu} hbar^{mu nu} - (1/2) hbar^2 (eta = diag(-1, 1, 1, 1)), exact."""
    tot = Fraction(0)
    for p in PAIRS:
        m, n = (p[0], p[1])
        w = ETA[m] * ETA[n] * (1 if m == n else 2)
        tot += w * Fraction(hb[p]) ** 2
    tr = sum((ETA[p[0]] * Fraction(hb[p]) for p in ('00', 'xx', 'yy', 'zz')))
    return tot - tr * tr / 2

def trace_reverse(hb: dict) -> dict:
    tr = sum((ETA[p[0]] * Fraction(hb[p]) for p in ('00', 'xx', 'yy', 'zz')))
    return {p: Fraction(hb[p]) - (Fraction(ETA[p[0]], 2) * tr if p[0] == p[1] else 0) for p in PAIRS}

def dewitt_check(trials: int=200, seed: int=7) -> dict:
    """Exact: 2 q(hbar) == (4/P^2) Sum_g s_g g^2 (P = 1 here: the map is homogeneous) and h == TR(hbar)."""
    rng = random.Random(seed)
    bad_q = bad_tr = 0
    for _ in range(trials):
        vals = {g: rng.randint(-10 ** 6, 10 ** 6) for g in SIGNS}
        hb = stored_to_hbar(vals)
        h = stored_to_h(vals)
        lhs = 2 * dewitt_q(hb)
        rhs = 4 * sum((SIGNS[g] * vals[g] ** 2 for g in SIGNS))
        bad_q += int(lhs != rhs)
        tr = trace_reverse(hb)
        bad_tr += int(any((tr[p] != h[p] for p in PAIRS)))
    return {'trials': trials, 'dewitt_identity_failures': bad_q, 'trace_reversal_failures': bad_tr, 'signature': (sum((1 for s in SIGNS.values() if s > 0)), sum((1 for s in SIGNS.values() if s < 0)))}

def _arr(state: State, tensor: Tensor, name: str, fld: str='b') -> np.ndarray:
    g = tensor.gear_index(name)
    L = state.L
    return getattr(state, fld)[g].astype(OBJ).reshape(L, L, L)

def _sh(X, off):
    out = X
    for ax, o in enumerate(off):
        if o:
            out = np.roll(out, -o, axis=ax)
    return out
AX = ((1, 0, 0), (0, 1, 0), (0, 0, 1))

def source_of_stored(engine, state: State, ns: str='metric') -> dict:
    """s_g = u_g - [6 b_g] for the ten stored gears (exact, read-only)."""
    u = engine.inputs(state)
    T = engine.tensor
    L = state.L
    out = {}
    for g in SIGNS:
        nm = f'{ns}.{g}'
        b = _arr(state, T, nm)
        out[g] = u[T.gear_index(nm)].astype(OBJ).reshape(L, L, L) - (6 * b)
    return out

def conservation_defect(engine, s0: State, s1: State, ns: str='metric') -> dict:
    """D_mu s^{mu nu} for the hbar sources at t (s0) and t+1 (s1), in the package's Yee placement (observe.gravity.div_spatial
    conventions: h0i on links -> backward difference; hii nodes -> forward; hij plaquettes -> backward). Exact integers (in
    units of P x the stored-gear source). Returns max |defect| per nu and max |s| for scale."""
    a = stored_to_hbar(source_of_stored(engine, s0, ns))
    b = stored_to_hbar(source_of_stored(engine, s1, ns))
    sp = 'xyz'
    res = {}
    smax = max((int(np.max(np.abs(v))) for v in a.values()))
    for nu in '0xyz':
        key0 = '00' if nu == '0' else ''.join(sorted('0' + nu, key='0xyz'.index))
        d = b[key0] - a[key0]
        for i, c in enumerate(sp):
            e = AX[i]
            p = ''.join(sorted(c + nu, key='0xyz'.index)) if nu != '0' else '0' + c
            X = a[p]
            if nu == '0' or c != nu:
                d = d + X - _sh(X, tuple((-v for v in e)))
            else:
                d = d + _sh(X, e) - X
        res[nu] = int(np.max(np.abs(d)))
    res['max_abs_source'] = smax
    return res

def b3_offdiagonal_wall() -> dict:
    """An off-diagonal stress bilinear d_x phi d_y phi as Universe24 monomial needs the factors at +e_x and +e_y: LocalityError."""
    from ..core.tensor import TensorBuilder
    tb = TensorBuilder()
    tb.gear('hxy')
    tb.gear('phi')
    try:
        tb.term('hxy', 1, ('phi', (1, 0, 0), 'b'), ('phi', (0, 1, 0), 'b'))
        return {'wall': False}
    except LocalityError as exc:
        return {'wall': True, 'error': str(exc)}

def two_time_cycle_wall() -> dict:
    """A shift coupling of second-order matter: h0x sourced by the momentum density (reads a of phi) AND phi reading h0x's
    two-time product (reads a of h0x): a cycle of a-reads -> AcyclicityError (no staged exact inverse)."""
    try:
        Tensor(['h0x', 'phi'], [('h0x', 1, (('phi', (0, 0, 0), 'a'), ('phi', (1, 0, 0), 'b'))), ('phi', 1, (('h0x', (0, 0, 0), 'a'), ('phi', (1, 0, 0), 'b')))])
        return {'wall': False}
    except AcyclicityError as exc:
        return {'wall': True, 'error': str(exc)}

def polarisation_count(ks=((3, 4, 0), (1, 2, 2), (2, 3, 6))) -> list:
    """For each nonzero spatial K, impose K_0 = c |K|. The integer tuples represent scaled lattice momenta; they are
    not required to be allowed modes of a particular finite periodic board. This null ansatz is motivated by the
    free, remainder-free stencil symbol 4 sin^2(w/2) = c^2 Sum 4 sin^2(k_d/2).
    On the ten-dimensional space of hbar, count the imposed harmonic constraint K^mu hbar_{mu nu}=0, the gauge
    directions K_mu xi_nu + K_nu xi_mu - eta K.xi inside it, and the linearised Riemann rank on its nullspace.
    The legacy result key 'physical_polarisations' names that last algebraic rank. It does not establish dynamical
    constraint preservation, source conservation or a physical graviton in Rule3. Time is rescaled as x^0=c t."""
    import sympy as sp
    out = []
    for K in ks:
        k2 = sum((v * v for v in K))
        kn = sp.sqrt(k2)
        Kl = [kn] + list(K)
        eta = sp.diag(-1, 1, 1, 1)
        Ku = [eta[m, m] * Kl[m] for m in range(4)]
        idx = [(m, n) for m in range(4) for n in range(m, 4)]
        H = sp.symbols('h0:10')

        def hm(m, n):
            i = idx.index((min(m, n), max(m, n)))
            return H[i]
        cons = [sum((Ku[m] * hm(m, n) for m in range(4))) for n in range(4)]
        Cm = sp.Matrix([[sp.diff(cn, h) for h in H] for cn in cons])
        xi = sp.symbols('x0:4')
        Kxi = sum((Ku[m] * xi[m] for m in range(4)))
        gauge = [Kl[m] * xi[n] + Kl[n] * xi[m] - eta[m, n] * Kxi for m, n in idx]
        Gm = sp.Matrix([[sp.diff(g, x) for x in xi] for g in gauge])
        trh = sum((eta[m, m] * hm(m, m) for m in range(4)))

        def hl(m, n):
            return hm(m, n) - sp.Rational(1, 2) * eta[m, n] * trh
        R = []
        for m in range(4):
            for n in range(m + 1, 4):
                for r in range(4):
                    for s in range(r + 1, 4):
                        R.append(sp.Rational(1, 2) * (Kl[n] * Kl[r] * hl(m, s) + Kl[m] * Kl[s] * hl(n, r) - Kl[m] * Kl[r] * hl(n, s) - Kl[n] * Kl[s] * hl(m, r)))
        Rm = sp.Matrix([[sp.diff(x, h) for h in H] for x in R])
        ns_ = Cm.nullspace()
        Nmat = sp.Matrix.hstack(*ns_)
        rank_R_on_cons = (Rm * Nmat).rank()
        gauge_in_cons = (Cm * Gm).is_zero_matrix
        riemann_kills_gauge = (Rm * Gm).is_zero_matrix
        out.append({'K': K, 'constraint_rank': Cm.rank(), 'constraint_surface_dim': len(ns_), 'gauge_rank': Gm.rank(), 'gauge_inside_constraint': bool(gauge_in_cons), 'riemann_kills_gauge': bool(riemann_kills_gauge), 'physical_polarisations': int(rank_R_on_cons)})
    return out
__all__ = ['stored_to_h', 'stored_to_hbar', 'dewitt_q', 'trace_reverse', 'dewitt_check', 'source_of_stored', 'conservation_defect', 'b3_offdiagonal_wall', 'two_time_cycle_wall', 'polarisation_count']
