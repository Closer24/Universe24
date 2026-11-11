"""Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
from __future__ import annotations
import numpy as np
from ..core.lattice import DIRECTIONS
from ..core.tensor import Block, GearType
I2 = np.eye(2, dtype=np.int64)
SZ = np.diag([1, -1]).astype(np.int64)
SX = np.array([[0, 1], [1, 0]], dtype=np.int64)
EPS = np.array([[0, 1], [-1, 0]], dtype=np.int64)

def _quat_left():
    """Integer 4x4 matrices of LEFT multiplication by i, j, k on (1, i, j, k)."""
    Li = np.zeros((4, 4), np.int64)
    Lj = np.zeros((4, 4), np.int64)
    Lk = np.zeros((4, 4), np.int64)
    for src, (dst, s) in enumerate([(1, 1), (0, -1), (3, 1), (2, -1)]):
        Li[dst, src] = s
    for src, (dst, s) in enumerate([(2, 1), (3, -1), (0, -1), (1, 1)]):
        Lj[dst, src] = s
    for src, (dst, s) in enumerate([(3, 1), (2, 1), (1, -1), (0, -1)]):
        Lk[dst, src] = s
    return (Li, Lj, Lk)

def _quat_right(q):
    """Integer 4x4 matrix of RIGHT multiplication p -> p q for q = (w, x, y, z)."""
    w, x, y, z = q
    return np.array([[w, -x, -y, -z], [x, w, z, -y], [y, -z, w, x], [z, y, -x, w]], dtype=np.int64)
QL = _quat_left()
P8 = tuple((np.kron(L, SZ) for L in QL))
W08 = np.kron(np.eye(4, dtype=np.int64), SX)
J8 = np.kron(_quat_right((0, 1, 0, 0)), I2)
K8 = np.kron(_quat_right((0, 0, 1, 0)), I2)
P16 = tuple((np.kron(I2, p) for p in P8))
W016 = np.kron(I2, W08)
J16 = np.kron(I2, J8)
JP16 = np.kron(EPS, np.eye(8, dtype=np.int64))
V16 = J16 @ JP16
PJP16 = tuple((p @ JP16 for p in P16))
K16 = np.kron(I2, K8)
C16 = np.diag([1] * 8 + [-1] * 8).astype(np.int64)
SPECIES = ('pair', 'single')
REVERSOR_MATTER = {'matter': "K o M' : M' = (b, a, R'(r)) per gear, then K = 1_2 (x) R_j (x) 1_2 (signed permutation; a negated channel takes R' again, so its r is unchanged overall)", 'central': "X^2 = Jp on every matter gear ((a, b, r) -> (-a, -b, R'(r)); K^2 = -1, Kramers)", 'vacuum': 'Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly.', 'implementation': 'prepare.em.x_reversor(..., em_ns=None) / prepare.em.x_reversor_core'}

def algebra(species: str='pair') -> dict:
    """The integer matrices of one species (copies; numpy int64)."""
    if species == 'pair':
        return {'P': [p.copy() for p in P16], 'W0': W016.copy(), 'J': J16.copy(), 'Jp': JP16.copy(), 'V': V16.copy(), 'PJp': [m.copy() for m in PJP16], 'K': K16.copy(), 'C': C16.copy(), 'n': 16}
    if species == 'single':
        return {'P': [p.copy() for p in P8], 'W0': W08.copy(), 'J': J8.copy(), 'K': K8.copy(), 'n': 8}
    raise ValueError(f'species must be one of {SPECIES}')

def check_algebra() -> dict:
    """Exact integer checks of the pair algebra (AGREE_M A1-A3; M1 criteria E1)."""
    eye = np.eye(16, dtype=np.int64)
    ok = {}
    ok['P_antisymmetric'] = all((np.array_equal(p.T, -p) for p in P16))
    ok['W0_symmetric_involution'] = np.array_equal(W016.T, W016) and np.array_equal(W016 @ W016, eye)
    for nm, M in (('J', J16), ('Jp', JP16)):
        ok[nm + '_complex_structure'] = np.array_equal(M @ M, -eye) and np.array_equal(M.T, -M)
        ok[nm + '_commutes_with_P_W0'] = all((np.array_equal(M @ X, X @ M) for X in list(P16) + [W016]))
    ok['J_Jp_commute'] = np.array_equal(J16 @ JP16, JP16 @ J16)
    ok['V_symmetric'] = np.array_equal(V16.T, V16)
    ok['PJp_symmetric'] = all((np.array_equal(m.T, m) for m in PJP16))
    ok['couplings_commute_with_J_and_Jp'] = all((np.array_equal(m @ X, X @ m) for m in [V16] + list(PJP16) for X in (J16, JP16)))
    ok['signed_permutations'] = all((((np.abs(m) == 1).sum(0) == 1).all() and ((np.abs(m) == 1).sum(1) == 1).all() for m in [V16, W016, J16, JP16, K16] + list(PJP16) + list(P16)))
    ok['K_anticommutes_J'] = np.array_equal(K16 @ J16, -J16 @ K16)
    ok['K_commutes_Jp_P_W0'] = all((np.array_equal(K16 @ X, X @ K16) for X in [JP16, W016] + list(P16)))
    ok['K_squared_minus_one_Kramers'] = np.array_equal(K16 @ K16, -eye)
    ok['C_flips_Jp'] = np.array_equal(C16 @ JP16 @ C16, -JP16)
    ok['C_commutes_J_P_W0'] = all((np.array_equal(C16 @ X, X @ C16) for X in [J16, W016] + list(P16)))
    ok['single_block_commutant_J_only'] = np.array_equal(J8 @ J8, -np.eye(8, dtype=np.int64))
    return {k: bool(v) for k, v in ok.items()}

def matter_names(species: str='pair') -> tuple[str, ...]:
    """Local gear names: X0..X7 (one 8-block) and, for the pair, Y0..Y7 (the second block; C negates Y)."""
    if species == 'pair':
        return tuple((f'X{i}' for i in range(8))) + tuple((f'Y{i}' for i in range(8)))
    if species == 'single':
        return tuple((f'X{i}' for i in range(8)))
    raise ValueError(f'species must be one of {SPECIES}')

def _face(d: int, sign: int) -> tuple[int, int, int]:
    return DIRECTIONS[2 * d] if sign > 0 else DIRECTIONS[2 * d + 1]

def _block(gears, terms, name, vacuum, params, doc):
    """Construct a fixed-six tensor block."""
    return Block(tuple(gears), tuple(terms), name=name, vacuum=vacuum, params=params, doc=doc)

def default_hop() -> int:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    return 1

def build_matter(*, hop: int, mass: int, wilson: int=0, species: str='pair', name: str='matter', label: str='official', r0: int | None=None) -> Block:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    for nm, v in (('hop', hop), ('mass', mass), ('wilson', wilson)):
        if type(v) is not int:
            raise TypeError(f'{nm} must be a Python int')
    alg = algebra(species)
    n = alg['n']
    names = matter_names(species)
    D = 6
    r0 = 2 if r0 is None else r0
    if type(r0) is not int or not 0 <= r0 < D:
        raise ValueError('r0 must be in 0..D-1')
    terms = []
    P, W0 = (alg['P'], alg['W0'])
    for i in range(n):
        for d in range(3):
            for j in range(n):
                if P[d][i, j] and hop:
                    terms.append((names[i], int(hop * P[d][i, j]), ((names[j], _face(d, -1), 'b'),)))
                if P[d][j, i] and hop:
                    terms.append((names[i], int(hop * P[d][j, i]), ((names[j], _face(d, +1), 'b'),)))
                if W0[i, j] and wilson:
                    terms.append((names[i], int(-wilson * W0[i, j]), ((names[j], _face(d, +1), 'b'),)))
                    terms.append((names[i], int(-wilson * W0[i, j]), ((names[j], _face(d, -1), 'b'),)))
        for j in range(n):
            if W0[i, j] and (mass or wilson):
                c = int((mass + 6 * wilson) * W0[i, j])
                if c:
                    terms.append((names[i], c, ((names[j], (0, 0, 0), 'b'),)))
    return _block([GearType(nm, label) for nm in names], terms, name, {nm: r0 for nm in names}, {'hop': hop, 'mass': mass, 'wilson': wilson, 'species': species, 'label': label, 'r0': r0, 'reversor': REVERSOR_MATTER}, 'free first-order Dirac matter (sin-Dirac transport + mass + Wilson), Study 4 E1 matter')

def build_static_lapse_mechanism(*, matter: Block, coupling: int=1, name: str='lapse', r0: int | None=None) -> Block:
    """MECHANISM (labelled; never evidence): a PRESCRIBED static lapse acting on the matter's REST CLOCK.

    One node gear N per node with u_N = D * N.b (a marginal gear: K = 2 D N.b = 0 mod D, no rounding; it stays exactly
    static when prepared with N.a = N.b). The matter reads it on its on-site mass entries:
        u_matter(x) += coupling * N.b(x) * W0 b(x)        (rank 3, on-site; the clock's mass entry m -> m + c N(x))
    so a prepared profile N(x) is a static position-dependent shift of the rest clock (Study 4 PR-21 'lapse on the
    mass', charge-blind). The read is ONE-WAY (N is not sourced by matter): designated, MECHANISM. The position
    dependence lives in the initial data of N (the tensor stays translation invariant).
    """
    if type(coupling) is not int:
        raise TypeError('coupling must be a Python int')
    D = 6
    r0 = 2 if r0 is None else r0
    sp = matter.params['species']
    alg = algebra(sp)
    mnames = [matter.qualify(nm) for nm in matter_names(sp)]
    why = "MECHANISM: prescribed static lapse (frozen marginal gear, initial data only) read by the matter's rest clock; a prescribed field has no reaction by construction (Study 4 PR-21)"
    terms = [('N', D, (('N', (0, 0, 0), 'b'),))]
    W0 = alg['W0']
    for i in range(alg['n']):
        for j in range(alg['n']):
            if W0[i, j]:
                terms.append((mnames[i], int(coupling * W0[i, j]), (('N', (0, 0, 0), 'b'), (mnames[j], (0, 0, 0), 'b')), {'designated_one_way': why}))
    return _block([GearType('N', 'audit')], terms, name, {'N': r0}, {'coupling': coupling, 'matter': matter.name, 'r0': r0, 'MECHANISM': True}, "MECHANISM: prescribed static lapse on the matter's on-site mass entries")

def _local(block: Block, ref: str) -> str:
    pre = f'{block.name}.' if block.name else ''
    return ref[len(pre):] if pre and ref.startswith(pre) else ref

def rest_clock_terms(block: Block) -> list[tuple]:
    """MATTER INTERFACE: the matter block's ON-SITE entries (mass + on-site Wilson part): (target, coeff, source)."""
    out = []
    for t in block.terms:
        target, coeff, factors = (t[0], t[1], t[2])
        if len(factors) == 1 and tuple(factors[0][1]) == (0, 0, 0):
            out.append((target, coeff, factors[0][0]))
    return out

def transport_terms(block: Block) -> dict:
    """MATTER INTERFACE: the matter block's LINK entries keyed by face offset: {offset: [(target, coeff, source)]}."""
    out = {}
    for t in block.terms:
        target, coeff, factors = (t[0], t[1], t[2])
        if len(factors) == 1 and tuple(factors[0][1]) != (0, 0, 0):
            out.setdefault(tuple(factors[0][1]), []).append((target, coeff, factors[0][0]))
    return out

def link_hamiltonian(params: dict, d: int) -> np.ndarray:
    """H_d = hop P_d - wilson W0 (integer matrix): the matter's link block (x, x + e_d), Psi_link = b(x+e)^T H_d b(x)."""
    alg = algebra(params['species'])
    return params['hop'] * alg['P'][d] - params['wilson'] * alg['W0']

def bloch_matrix(params: dict, k) -> np.ndarray:
    """B(k) (complex, n x n): the free u-operator on e^{ik.x} v (floats; analysis/preparation only)."""
    alg = algebra(params['species'])
    B = np.zeros((alg['n'], alg['n']), complex)
    for d in range(3):
        B += params['hop'] * (np.exp(-1j * k[d]) * alg['P'][d] + np.exp(1j * k[d]) * alg['P'][d].T)
        B += params['wilson'] * (2 - 2 * np.cos(k[d])) * alg['W0']
    return B + params['mass'] * alg['W0']
