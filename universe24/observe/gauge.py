"""Read-only observables and AUDIT maps for the compact gauge layers (layers/gauge.py, layers/links.py).

Nothing here changes a state in place or feeds anything back into a run (AGENTS item 10). The gauge maps return NEW
states; they are audit maps (bit-exact covariance checks), never stages of a forward evolution.

Exact discrete Noether (Gauss) identity, for every integer anti-Hermitian generator X and node x:
    J^X_x(t) = D * sum_c a_c(t) (T^X_x b(t))_c        (two-time charge; a(t) = b(t-1); PHYSICAL values X0 + stored)
    J^X_x(t+1) - J^X_x(t) = sum_c b_c(t) (T^X_x (r(t) - r(t+1)))_c           (the remainder term, exact integers)
T^X_x acts by X on the matter at x, by left multiplication on the links and 2-paths leaving x, and by MINUS right
multiplication on the links and 2-paths arriving at x (Kogut-Susskind: E_L out - E_R in - rho). Proof: Rule3 gives
D (b(t+1) + b(t-1)) = 2 dPhi/db + (r(t) - r(t+1)); Phi is invariant under the infinitesimal local symmetry and T is
antisymmetric (one divisor D for every gear), so the discrete Noether charge changes only by the remainder term.
"""
from __future__ import annotations
import numpy as np
from ..core.engine import OBJ, State
from ..core.lattice import lattice
from ..core.tensor import Tensor
from ..layers.gauge import ALGEBRAS, AXES, UNIT, gear_names
LIMIT = 1 << 62

def rprime(r: np.ndarray, D: int) -> np.ndarray:
    """R'(r) = D - 2 - r (even r), D - r (odd r): the remainder map of a negated gear (commutes with Rule3)."""
    if type(D) is not int or D != 6:
        raise ValueError('this observer requires the fixed divisor six')
    r = np.asarray(r)
    return np.where(r % 2 == 0, D - 2 - r, D - r)

class GaugeView:
    """Index bookkeeping of one compact gauge layer inside a composed tensor (read-only)."""

    def __init__(self, tensor: Tensor, params: dict, name: str):
        self.tensor = tensor
        self.p = dict(params)
        self.group = params['group']
        self.alg = ALGEBRAS[self.group]
        self.D = 6
        self.A = params['A']
        self.name = name
        matter, links, paths = gear_names(self.group, params['use_P'])
        q = (lambda g: f'{name}.{g}') if name else lambda g: g
        self.matter = [tensor.gear_index(q(g)) for g in matter]
        self.links = {k: [tensor.gear_index(q(g)) for g in links[k]] for k in range(3)}
        self.paths = {key: [tensor.gear_index(q(g)) for g in v] for key, v in paths.items()}
        X0 = params.get('X0', {})
        self.x0 = np.zeros(tensor.G, dtype=object)
        for g, v in X0.items():
            self.x0[tensor.gear_index(q(g))] = v
        self.own = sorted(self.matter + [i for v in self.links.values() for i in v] + [i for v in self.paths.values() for i in v])

    def phys(self, arr: np.ndarray, gears) -> np.ndarray:
        """Physical values (vacuum value X0 added) of the listed gear rows, as Python-int object arrays."""
        idx = list(gears)
        out = arr[idx].astype(object)
        return out + self.x0[idx][:, None]

    def pieces(self, X) -> list:
        """T^X_x as pieces (offset, src gear, dst gear, coeff): (T b)_dst(x+o) += coeff * b_src(x+o)."""
        alg = self.alg
        out = []
        M = alg.act_matrix(X)
        for i in range(alg.n):
            for j in range(alg.n):
                if M[i][j]:
                    out.append(((0, 0, 0), self.matter[j], self.matter[i], M[i][j]))
        Lm, Rm = (alg.left_matrix(X), alg.right_matrix(X))
        for k in range(3):
            back = tuple((-e for e in UNIT[k]))
            for c in range(alg.m):
                for b in range(alg.m):
                    if Lm[c][b]:
                        out.append(((0, 0, 0), self.links[k][b], self.links[k][c], Lm[c][b]))
                    if Rm[c][b]:
                        out.append((back, self.links[k][b], self.links[k][c], -Rm[c][b]))
        for (k1, k2), gl in self.paths.items():
            back = tuple((-a - b for a, b in zip(UNIT[k1], UNIT[k2])))
            for c in range(alg.m):
                for b in range(alg.m):
                    if Lm[c][b]:
                        out.append(((0, 0, 0), gl[b], gl[c], Lm[c][b]))
                    if Rm[c][b]:
                        out.append((back, gl[b], gl[c], -Rm[c][b]))
        return out

    def charge(self, state: State, X, parts: str='all') -> np.ndarray:
        """J^X_x(t) = D sum a (T b) at every node x (flat order), exact Python ints. parts: 'all', 'matter',
        'links' (links leaving x left-multiplied, arriving right-multiplied) or 'paths'."""
        return self._bilinear(state.a, state.b, X, parts, scale=self.D, L=state.L)

    def remainder_term(self, s0: State, s1: State, X) -> np.ndarray:
        """sum_c b_c(t) (T (r(t) - r(t+1)))_c at every node x, exact."""
        dr = s0.r.astype(object) - s1.r.astype(object)
        return self._bilinear(s0.b, dr, X, 'all', scale=1, L=s0.L, second_is_raw=True)

    def _bilinear(self, first, second, X, parts, scale, L, second_is_raw=False):
        lat = lattice(L)
        sel = {'all': None, 'matter': set(self.matter), 'links': {i for v in self.links.values() for i in v}, 'paths': {i for v in self.paths.values() for i in v}}[parts]
        by_off: dict = {}
        for off, src, dst, coef in self.pieces(X):
            if sel is not None and dst not in sel:
                continue
            by_off.setdefault(off, []).append((src, dst, coef))
        J = np.zeros(lat.N, dtype=object)
        for off, lst in by_off.items():
            F = np.zeros(lat.N, dtype=object)
            for src, dst, coef in lst:
                fa = first[dst].astype(object) + self.x0[dst]
                fb = second[src].astype(object) + (0 if second_is_raw else self.x0[src])
                F = F + coef * fa * fb
            J = J + F[lat.shift_index(off)]
        return scale * J

    def gauss_check(self, history: list, gens=None) -> dict:
        """Check the exact identity at every node, generator and update of a stored history."""
        gens = self.alg.generators if gens is None else gens
        checks = fails = 0
        max_J = max_R = 0
        for t in range(len(history) - 1):
            s0, s1 = (history[t], history[t + 1])
            for label, X in gens:
                lhs = self.charge(s1, X) - self.charge(s0, X)
                rhs = self.remainder_term(s0, s1, X)
                bad = int(np.sum(lhs != rhs))
                fails += bad
                checks += len(lhs)
                max_R = max(max_R, max((abs(int(v)) for v in rhs)))
                max_J = max(max_J, max((abs(int(v)) for v in self.charge(s0, X))))
        return {'checks': checks, 'failures': fails, 'max_abs_J': max_J, 'max_abs_remainder_term': max_R}

    def link_matrix(self, state: State, k: int, field: str='b') -> np.ndarray:
        """Physical link components, shape (m, N), Python ints."""
        return self.phys(getattr(state, field), self.links[k])

    def link_norm2(self, state: State, field: str='b') -> np.ndarray:
        """|U|^2 (Frobenius) per link, shape (3, N), exact ints."""
        return np.array([np.sum(self.link_matrix(state, k, field) ** 2, axis=0) for k in range(3)], dtype=object)

    def link_unitarity(self, state: State) -> float:
        """max over links of |U^dag U - A^2|_F / A^2 (float, report only)."""
        alg, A = (self.alg, self.A)
        worst = 0.0
        for k in range(3):
            Um = self.link_matrix(state, k)
            for n in range(Um.shape[1]):
                u = [int(v) for v in Um[:, n]]
                N = alg.prod(alg.dagger(u), u)
                N = [N[c] - A * A * alg.one[c] for c in range(alg.m)]
                worst = max(worst, float(sum((v * v for v in N))) ** 0.5 / (A * A))
        return worst

    def wilson(self, state: State, k1: int, k2: int) -> np.ndarray:
        """<U(x,k1) U(x+e1,k2), U(x,k2) U(x+e2,k1)> = Re Tr(U1 U2 (U3 U4)^dag) at every x: exact, gauge invariant."""
        lat = lattice(state.L)
        alg = self.alg
        U1 = self.link_matrix(state, k1)
        U2 = self.link_matrix(state, k2)[:, lat.shift_index(UNIT[k1])]
        U3 = self.link_matrix(state, k2)
        U4 = self.link_matrix(state, k1)[:, lat.shift_index(UNIT[k2])]
        out = np.zeros(lat.N, dtype=object)
        for n in range(lat.N):
            a = alg.prod(list(U1[:, n]), list(U2[:, n]))
            b = alg.prod(list(U3[:, n]), list(U4[:, n]))
            out[n] = sum((int(x) * int(y) for x, y in zip(a, b)))
        return out

    def gauge_map(self, state: State, gfield) -> State:
        """psi(x) -> g(x) psi(x), U(x,k) -> g(x) U g(x+e_k)^dag, P(x;k1,k2) -> g(x) P g(x+e_k1+e_k2)^dag on the PHYSICAL
        values (deviation form: an integer affine map), applied to a and b; remainders follow the signed permutation
        (R' on negated components). gfield: sequence of algebra vectors (entries 0, +-1), one per node. Returns a NEW
        state; other gears are copied unchanged."""
        alg, D = (self.alg, self.D)
        lat = lattice(state.L)
        a, b, r = (state.a.astype(object), state.b.astype(object), state.r.astype(object))
        na, nb, nr = (a.copy(), b.copy(), r.copy())

        def apply(rows, n, M, x0vec):
            src_a = [a[g, n] + x0vec[i] for i, g in enumerate(rows)]
            src_b = [b[g, n] + x0vec[i] for i, g in enumerate(rows)]
            for i, gi in enumerate(rows):
                (j, s), = [(j, M[i][j]) for j in range(len(rows)) if M[i][j]]
                na[gi, n] = s * src_a[j] - x0vec[i]
                nb[gi, n] = s * src_b[j] - x0vec[i]
                nr[gi, n] = r[rows[j], n] if s == 1 else int(rprime(np.array(r[rows[j], n]), D))

        def two_sided(g, h):
            Lm, Rm = (alg.left_matrix(g), alg.right_matrix(alg.dagger(h)))
            return [[sum((Lm[i][k] * Rm[k][j] for k in range(alg.m))) for j in range(alg.m)] for i in range(alg.m)]
        for n in range(lat.N):
            x = lat.coords(n)
            g = list(gfield[n])
            apply(self.matter, n, alg.act_matrix(g), [0] * alg.n)
            for k in range(3):
                h = list(gfield[lat.index(*(x[i] + UNIT[k][i] for i in range(3)))])
                apply(self.links[k], n, two_sided(g, h), [self.x0[i] for i in self.links[k]])
            for (k1, k2), rows in self.paths.items():
                h = list(gfield[lat.index(*(x[i] + UNIT[k1][i] + UNIT[k2][i] for i in range(3)))])
                apply(rows, n, two_sided(g, h), [self.x0[i] for i in rows])
        return State(state.L, na, nb, nr)

def matter_colour(view: GaugeView, state: State, X) -> int:
    """Total matter-only charge sum_x J^X_x(matter)."""
    return int(sum(view.charge(state, X, 'matter')))

def field_colour(view: GaugeView, state: State, X) -> int:
    """Total charge carried by links + 2-paths (sum over x of the link/2-path parts)."""
    return int(sum(view.charge(state, X, 'links')) + (sum(view.charge(state, X, 'paths')) if view.paths else 0))
__all__ = ['GaugeView', 'rprime', 'matter_colour', 'field_colour']

class C2View:
    """Noether charges, gauge maps and link readouts for ref + c2 (layers/links.py). Read-only / audit maps."""

    def __init__(self, tensor: Tensor, params: dict, name: str='c2'):
        from ..layers.links import Q8_ORDER, _link_names, q8_mul_names, right_perm
        self.tensor = tensor
        self.p = dict(params)
        self.algebra = params['algebra']
        self.D = 6
        self.name = name
        ref = params['ref']
        self.ref = [tensor.gear_index(f'{ref}.R{g:02d}') for g in range(48)]
        ln = _link_names(self.algebra)
        self.links = {k: [tensor.gear_index(f'{name}.{g}') for g in ln[k]] for k in range(3)}
        self.x0 = np.zeros(tensor.G, dtype=object)
        if self.algebra == 'ZQ8':
            for k in range(3):
                self.x0[self.links[k][0]] = params['A']
        else:
            from fractions import Fraction
            for k in range(3):
                self.x0[self.links[k][0]] = Fraction(params['m'], 2)
        self.Q8 = Q8_ORDER
        self.qmul = q8_mul_names()
        self.right_perm = right_perm

    def pieces(self, a: int) -> list:
        e = ('i', 'j', 'k')[a - 1]
        out = []
        pp, pm = (self.right_perm(e), self.right_perm('-' + e))
        for g in range(48):
            out.append(((0, 0, 0), self.ref[pp[g]], self.ref[g], 1))
            out.append(((0, 0, 0), self.ref[pm[g]], self.ref[g], -1))
        if self.algebra == 'ZQ8':
            idx = {q: i for i, q in enumerate(self.Q8)}
            for k in range(3):
                back = tuple((-v for v in UNIT[k]))
                rows = self.links[k]
                for q in self.Q8:
                    for s, t in ((1, e), (-1, '-' + e)):
                        out.append(((0, 0, 0), rows[idx[q]], rows[idx[self.qmul[t, q]]], s))
                        out.append((back, rows[idx[q]], rows[idx[self.qmul[q, t]]], -s))
        else:
            alg = ALGEBRAS['su2']
            X = [0, 0, 0, 0]
            X[a] = 2
            Lm, Rm = (alg.left_matrix(X), alg.right_matrix(X))
            for k in range(3):
                back = tuple((-v for v in UNIT[k]))
                rows = self.links[k]
                for c in range(4):
                    for b in range(4):
                        if Lm[c][b]:
                            out.append(((0, 0, 0), rows[b], rows[c], Lm[c][b]))
                        if Rm[c][b]:
                            out.append((back, rows[b], rows[c], -Rm[c][b]))
        return out

    def _bil(self, first, second, a, scale, L, raw=False, parts='all'):
        lat = lattice(L)
        refset = set(self.ref)
        by_off: dict = {}
        for off, src, dst, coef in self.pieces(a):
            if parts == 'ref' and dst not in refset:
                continue
            if parts == 'links' and dst in refset:
                continue
            by_off.setdefault(off, []).append((src, dst, coef))
        J = np.zeros(lat.N, dtype=object)
        for off, lst in by_off.items():
            F = np.zeros(lat.N, dtype=object)
            for src, dst, coef in lst:
                F = F + coef * (first[dst].astype(object) + self.x0[dst]) * (second[src].astype(object) + (0 if raw else self.x0[src]))
            J = J + F[lat.shift_index(off)]
        return scale * J

    def charge(self, state: State, a: int, parts: str='all') -> np.ndarray:
        return self._bil(state.a, state.b, a, self.D, state.L, parts=parts)

    def remainder_term(self, s0: State, s1: State, a: int) -> np.ndarray:
        dr = s0.r.astype(object) - s1.r.astype(object)
        return self._bil(s0.b, dr, a, 1, s0.L, raw=True)

    def gauss_check(self, history: list) -> dict:
        checks = fails = 0
        for t in range(len(history) - 1):
            for a in (1, 2, 3):
                lhs = self.charge(history[t + 1], a) - self.charge(history[t], a)
                rhs = self.remainder_term(history[t], history[t + 1], a)
                fails += int(np.sum(lhs != rhs))
                checks += len(lhs)
        return {'checks': checks, 'failures': fails}

    def link_norm2(self, state: State) -> np.ndarray:
        """|U|^2 of the PHYSICAL link (ZQ8: A[1] + W; H: m/2 + W), shape (3, N)."""
        out = []
        for k in range(3):
            rows = self.links[k]
            vals = state.b[rows].astype(object) + self.x0[rows][:, None]
            out.append(np.sum(vals * vals, axis=0))
        return np.array(out, dtype=object)

    def gauge_map_zq8(self, state: State, kfield) -> State:
        """LOCAL Q8 (ZQ8 form): b(x) -> R_k(x) b(x) (new[g] = old[g k]) on a, b, r of the 48 labels; link components
        q -> k q k'^-1 (k' = k(x+e)); physical U = A[1] + W, so W -> perm(W) + A([k k'^-1] - [1]). Pure permutations:
        remainders move with their values. kfield: Q8 element names, one per node."""
        assert self.algebra == 'ZQ8'
        lat = lattice(state.L)
        a, b, r = (state.a.astype(object), state.b.astype(object), state.r.astype(object))
        na, nb, nr = (a.copy(), b.copy(), r.copy())
        idx = {q: i for i, q in enumerate(self.Q8)}
        inv = {q: [p for p in self.Q8 if self.qmul[q, p] == '1'][0] for q in self.Q8}
        A = self.p['A']
        for n in range(lat.N):
            k = kfield[n]
            perm = self.right_perm(k)
            for g in range(48):
                na[self.ref[g], n] = a[self.ref[perm[g]], n]
                nb[self.ref[g], n] = b[self.ref[perm[g]], n]
                nr[self.ref[g], n] = r[self.ref[perm[g]], n]
            x = lat.coords(n)
            for kk in range(3):
                k2 = kfield[lat.index(*(x[i] + UNIT[kk][i] for i in range(3)))]
                rows = self.links[kk]
                for q in self.Q8:
                    dst = idx[self.qmul[self.qmul[k, q], inv[k2]]]
                    na[rows[dst], n] = a[rows[idx[q]], n] + (A if q == '1' else 0)
                    nb[rows[dst], n] = b[rows[idx[q]], n] + (A if q == '1' else 0)
                    nr[rows[dst], n] = r[rows[idx[q]], n]
                na[rows[0], n] -= A
                nb[rows[0], n] -= A
        return State(state.L, na, nb, nr)

    def gauge_map_h(self, state: State, kfield, centre_only: bool) -> State:
        """H form: b(x) -> R_k(x) b(x); U -> k U k'^-1 as a quaternion (signed permutation, R' on negated
        components). Integer only for k(x) = k(x+e) (global) or k in {+-1} (local centre, W -> -W - m)."""
        assert self.algebra == 'H'
        from fractions import Fraction
        alg = ALGEBRAS['su2']
        names = {'1': (1, 0, 0, 0), '-1': (-1, 0, 0, 0), 'i': (0, 1, 0, 0), '-i': (0, -1, 0, 0), 'j': (0, 0, 1, 0), '-j': (0, 0, -1, 0), 'k': (0, 0, 0, 1), '-k': (0, 0, 0, -1)}
        lat = lattice(state.L)
        a, b, r = (state.a.astype(object), state.b.astype(object), state.r.astype(object))
        na, nb, nr = (a.copy(), b.copy(), r.copy())
        A = Fraction(self.p['m'], 2)
        for n in range(lat.N):
            k = kfield[n]
            perm = self.right_perm(k)
            for g in range(48):
                na[self.ref[g], n] = a[self.ref[perm[g]], n]
                nb[self.ref[g], n] = b[self.ref[perm[g]], n]
                nr[self.ref[g], n] = r[self.ref[perm[g]], n]
            x = lat.coords(n)
            for kk in range(3):
                k2 = kfield[lat.index(*(x[i] + UNIT[kk][i] for i in range(3)))]
                g1, g2 = (list(names[k]), list(names[k2]))
                Lm, Rm = (alg.left_matrix(g1), alg.right_matrix(alg.dagger(g2)))
                M = [[sum((Lm[i][t] * Rm[t][j] for t in range(4))) for j in range(4)] for i in range(4)]
                rows = self.links[kk]
                x0 = [A, 0, 0, 0]
                for i in range(4):
                    (j, s), = [(j, M[i][j]) for j in range(4) if M[i][j]]
                    va = s * (a[rows[j], n] + x0[j]) - x0[i]
                    vb = s * (b[rows[j], n] + x0[j]) - x0[i]
                    if Fraction(va).denominator != 1 or Fraction(vb).denominator != 1:
                        raise ValueError('non-integer gauge image: H-form local maps are integer only for the centre')
                    na[rows[i], n], nb[rows[i], n] = (int(va), int(vb))
                    nr[rows[i], n] = r[rows[j], n] if s == 1 else int(rprime(np.array(r[rows[j], n]), self.D))
        return State(state.L, na, nb, nr)

def layer_census(tensor: Tensor, prefix: str) -> dict:
    """Static census of the monomials TARGETING gears whose name starts with ``prefix`` (ARCH R3/R4/R6 items):
    degree histogram, constants, monomials with an a-factor (two-time reads), max entries per row from Universe24 face
    neighbour (OD3 placement), rank-4 (degree-3) monomial count, physical supports wider than one link."""
    from ..core.lattice import DIRECTIONS
    names = tensor.names
    rows = [i for i, n in enumerate(names) if n.startswith(prefix)]
    rowset = set(rows)
    deg = [0, 0, 0, 0]
    a_reads, consts = ([], 0)
    per_face: dict = {}
    for m in tensor.monomials:
        if m.target not in rowset:
            continue
        deg[m.degree] += 1
        if m.degree == 0:
            consts += 1
        if any((f.field == 'a' for f in m.factors)):
            a_reads.append(m)
        d = m.direction
        if d is not None:
            per_face[m.target, d] = per_face.get((m.target, d), 0) + 1
    bad = [m for m in tensor.support_violations() if m.target in rowset]
    return {'targets': len(rows), 'monomials_by_degree': deg, 'constants': consts, 'a_read_monomials': len(a_reads), 'max_entries_per_row_per_face': max(per_face.values(), default=0), 'rows_with_more_than_one_entry_from_one_face': sum((1 for v in per_face.values() if v > 1)), 'rank4_monomials': deg[3], 'physical_support_wider_than_one_link': len(bad)}

def joint_mirror(tensor: Tensor, ref_prefix: str='ref.'):
    """The declared reversor as DATA: rhoL0 on the reference gears, M' on every other (b-only) gear. Audit map."""
    from ..core.reversors import GearwiseMap
    return GearwiseMap(tensor, {n: 'rhoL0' if n.startswith(ref_prefix) else 'Mp' for n in tensor.names})
