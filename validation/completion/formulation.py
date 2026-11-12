"""Exact source-only formulation checks beyond the PR50 flat-vacuum audit.

Run ``python -m validation.completion.formulation``. No supported law is changed.
"""
from fractions import Fraction as F
import hashlib
import importlib
import json
from pathlib import Path

import sympy as s
import numpy as np

from universe24.algebra import frame_equations as frame
from validation.geometry.team48 import matter_dust_square

previous = importlib.import_module('validation.research_eight.07_hyperbolic_symbol')
FIELDS = matter_dust_square.FIELDS_CHARGED
ROOT = Path(__file__).resolve().parents[2]
BASE_PIN = '62202fdccdd9a40d5dbbec104de6f97d9587a999'


def equations(fields, partial, *, mass_squared=1, cosmological=0, coupling=1):
    """Explicitly massive, full-frame corrected source equations (44 fields)."""
    return previous.corrected_charged(fields, partial, mass_squared=mass_squared,
        cosmological=cosmological, coupling=coupling)


def build45(*, dt=F(1, 16), dx=F(1, 4), mass_squared=1,
            cosmological=0, coupling=1):
    """Static integer tensor, ordinary Engine, no runtime constraint projection."""
    def rhs(fields, partial):
        return equations(fields, partial, mass_squared=mass_squared,
            cosmological=cosmological, coupling=coupling)
    return previous.projective.compile_projective(FIELDS, rhs, dt=dt, dx=dx, degree=2)


def principal(background, direction):
    jets = dict(zip(FIELDS, s.symbols('j:44')))
    rhs, _, _ = equations(background,
        lambda name, axis: direction[axis] * jets[name])
    return s.Matrix([rhs[name] for name in FIELDS]).jacobian(list(jets.values()))


def zero_matrix(matrix):
    return matrix.applyfunc(s.expand) == s.zeros(*matrix.shape)


def principal_audit():
    """Exact polynomial identities, arbitrary fields/frame/covector, not samples."""
    background = dict(zip(FIELDS, s.symbols('v:44', real=True)))
    n = s.symbols('nx ny nz', real=True)
    B = s.Matrix(3, 3, lambda a, i: background[f'B{a}{i}'])
    k = tuple(B * s.Matrix(n))
    full = principal(background, n)
    unit = {name: s.Integer(int(name.startswith('B') and name[1] == name[2]))
            for name in FIELDS}
    transformed = principal(unit, k)
    assert zero_matrix(full - transformed)
    A = principal(unit, n)
    assert A[:24, 24:] == s.zeros(24, 20)
    assert A[24:, :24] == s.zeros(20, 24)
    geom, matter = A[:24, :24], A[24:, 24:]
    radius = sum(v*v for v in n)
    assert zero_matrix(matter**3 - radius*matter)
    square = geom**2
    annihilator = geom
    for coefficient in (s.Integer(1), s.Rational(1, 2), s.Rational(1, 8)):
        annihilator = (annihilator * (square-coefficient*radius*s.eye(24))).applyfunc(s.expand)
    assert zero_matrix(annihilator)
    return {'arbitrary_background_exact_frame_covariance': True,
            'geometry_matter_principal_cross_blocks_zero': True,
            'matter_annihilator': 'Am*(Am^2-|B*n|^2 I)=0',
            'full44_annihilator': 'A*(A^2-r^2 I)*(A^2-r^2 I/2)*(A^2-r^2 I/8)=0; r^2=|B*n|^2',
            'mass_squared': 1,
            'scope': 'Frozen continuum principal system; uniform on compact sets of invertible B. No discrete stability claim.'}


def homogeneous_background(*, sourced=True):
    fields = {name: s.Integer(0) for name in FIELDS}
    for a in range(3):
        fields[f'B{a}{a}'] = s.Integer(1)
        fields[f'K{a}{a}'] = s.Integer(-int(sourced))
    if sourced:
        fields['Pi_phi'], fields['dust_amplitude'] = s.Integer(2), s.Integer(1)
    return fields


def linear_constraint_matrices(background, direction, *, require_constrained=True):
    """Return C, L and material time derivative Cdot along homogeneous RHS.

    For perturbation exp(i n.x), delta_c=C(t,n) delta_u and
    delta_c_dot=(Cdot+C L) delta_u. Omitting Cdot on sourced expanding
    backgrounds would test a different, frozen non-solution background.
    """
    z = s.symbols('z:44')
    eps, t = s.symbols('eps t')
    drift, base_constraints, _ = equations(background, lambda *_: s.Integer(0))
    if require_constrained:
        assert all(s.expand(v) == 0 for v in base_constraints.values())
    fields = {name: background[name]+t*drift[name]+eps*z[j]
              for j, name in enumerate(FIELDS)}
    rhs, constraints, _ = equations(fields,
        lambda name, axis: eps*s.I*direction[axis]*z[FIELDS.index(name)])
    rhs1 = [s.diff(rhs[name], eps).subs({eps: 0, t: 0}) for name in FIELDS]
    constraint1 = [s.diff(value, eps).subs(eps, 0) for value in constraints.values()]
    Ctime = s.Matrix(constraint1).jacobian(z)
    C = Ctime.subs(t, 0)
    Cdot = Ctime.diff(t).subs(t, 0)
    L = s.Matrix(rhs1).jacobian(z)
    return tuple(constraints), C, L, Cdot


def constraint_audit():
    q = s.symbols('q', real=True, nonzero=True)
    rows = []
    for sourced in (False, True):
        for direction in ((0, 0, q), (0, 0, 0)):
            names, C, L, Cdot = linear_constraint_matrices(
                homogeneous_background(sourced=sourced), direction)
            kernel = C.nullspace()
            N = s.Matrix.hstack(*kernel)
            residual = (Cdot+C*L)*N
            passed = zero_matrix(residual)
            rows.append({'sourced': sourced, 'direction': [str(v) for v in direction],
                         'constraints': len(names), 'constraint_rank': C.rank(),
                         'kernel_dimension': N.cols, 'kernel_invariant': passed,
                         'nonzero_residual_entries': sum(s.expand(v) != 0 for v in residual)})
            if not passed:
                rows[-1]['first_residual'] = next(str(s.factor(v)) for v in residual if s.expand(v) != 0)
    return rows


def homogeneous_family_audit():
    """All real massive isotropic backgrounds satisfying H=0; zero branches included.

    The only poles in a kernel basis are explicitly checked against each
    stratum's nonzero parameters. Every residual numerator is divisible by H.
    """
    k, f, p, q = s.symbols('k f p q', real=True, nonzero=True)
    d = s.symbols('d', real=True)
    rows = []
    for has_f, has_p in ((True, True), (False, True), (True, False), (False, False)):
        fv, pv = f if has_f else s.Integer(0), p if has_p else s.Integer(0)
        background = homogeneous_background(sourced=False)
        for a in range(3):
            background[f'K{a}{a}'] = k
        background.update(phi=fv, Pi_phi=pv, dust_amplitude=d)
        H = 6*k*k-fv*fv-pv*pv-2*d*d
        for direction in ((0, 0, q), (0, 0, 0)):
            names, C, L, Cdot = linear_constraint_matrices(background, direction, require_constrained=False)
            N = s.Matrix.hstack(*C.nullspace())
            residual = (Cdot+C*L)*N
            denominators = set()
            for value in N:
                denominator = s.factor(s.denom(s.cancel(value)))
                assert denominator.is_nonzero is True
                denominators.add(str(denominator))
            nonzero = []
            for i in range(residual.rows):
                for j in range(residual.cols):
                    value = s.factor(residual[i, j])
                    if value != 0:
                        numerator, denominator = s.fraction(value)
                        assert s.rem(numerator, H, d) == 0
                        assert names[i] == 'H'
                        assert denominator.is_nonzero is True
                        nonzero.append({'row': names[i], 'column': j,
                                        'residual_over_H': str(s.cancel(value/H))})
            rows.append({'phi_nonzero': has_f, 'Pi_phi_nonzero': has_p,
                         'nonzero_frequency': bool(direction[2]),
                         'kernel_dimension': N.cols, 'basis_denominators': sorted(denominators),
                         'residuals_divisible_by_background_H': True,
                         'off_constraint_residuals': nonzero})
    # Background closure makes this a family of actual homogeneous solutions.
    kdot, fdot, pdot, ddot = 3*k*k-(f*f+d*d)/2, p, 3*k*p-f, 3*k*d/2
    H = 6*k*k-f*f-p*p-2*d*d
    assert s.expand(s.diff(H,k)*kdot+s.diff(H,f)*fdot+s.diff(H,p)*pdot+s.diff(H,d)*ddot-6*k*H) == 0
    return {'branches': rows, 'homogeneous_H_dot': '6*k*H',
            'scope': 'Linear continuous-time constraints along regular homogeneous isotropic massive scalar/dust backgrounds; all Fourier directions by spatial rotation and affine coordinate covariance. Not nonlinear/discrete propagation.'}


def triangular21_negative_audit():
    """Keeping the dropped ninth G does not remove the oblique gauge defect."""
    triangular = previous.triangular
    names = tuple(name for name in frame.FIELDS if name not in triangular.ZERO_FIELDS)
    values = {name: s.Integer(int(name.startswith('B') and name[1] == name[2]))
              for name in frame.FIELDS}
    jets = dict(zip(names, s.symbols('j:21')))
    rows = []
    for direction in ((1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 2, 3)):
        def partial(name, axis):
            return 0 if name in triangular.ZERO_FIELDS else direction[axis]*jets[name]
        rhs, constraints, ricci = frame.equations(values, partial)
        rhs = triangular.rotate_rhs(values, partial, previous.add_constraints(rhs, constraints, ricci))
        A = s.Matrix([rhs[name] for name in names]).jacobian(list(jets.values()))
        ranks = [A.rank(), (A*A).rank()]
        rows.append({'direction': direction, 'rank_A': ranks[0], 'rank_A_squared': ranks[1],
                     'zero_Jordan_block': ranks[0] != ranks[1]})
    assert all(not row['zero_Jordan_block'] for row in rows[:3])
    assert all(row['zero_Jordan_block'] for row in rows[3:])
    return rows


def compile_audit():
    program = build45()
    tensor = program.tensor
    assert tensor.G == 45 and tensor.rank-1 <= 3
    assert not tensor.support_violations()
    assert not any(f.field == 'a' for term in tensor.monomials for f in term.factors)
    rng = np.random.default_rng(12112026)
    values = rng.integers(-2, 3, size=(44, 27)).astype(object)
    for i, name in enumerate(FIELDS):
        if name.startswith('B'):
            values[i] = np.full(27, int(name[1] == name[2]), dtype=object)
    remainders = np.array([[(g+n) % 6 for n in range(27)] for g in range(45)], dtype=object)
    seed = previous.projective.prepare(program, values, L=3, denominator=16, remainders=remainders)
    engine, state = previous.Engine(tensor), seed
    max_bits = 0
    for _ in range(3):
        exact = previous.scalar_oracle(tensor, state)
        after = engine.step(state)
        assert exact.same_as(after)
        assert engine.inverse_step(after).same_as(state)
        assert np.array_equal(after.r, remainders)
        max_bits = max(max_bits, max(abs(int(v)).bit_length() for arr in (after.a, after.b, after.r) for v in arr.flat))
        state = after
    assert engine.rewind(state, 3).same_as(seed)
    return {'tensor_sha256': tensor.fingerprint, 'fields': 44, 'channels': 45,
            'retained_integers_per_node': 135, 'degree': tensor.rank-1,
            'monomials': len(tensor), 'multiplier': program.multiplier,
            'mass_squared': 1, 'strict_face_support': True, 'old_a_reads': False,
            'steps': 3, 'nodes': 27, 'all_six_remainders': True,
            'independent_scalar_oracle': True, 'full_rewind': True,
            'max_retained_bits': max_bits,
            'nonlinear_discrete_constraints': 'not_established',
            'metric_nondegeneracy_all_time': 'not_established'}


def main():
    result = {'baseline': BASE_PIN, 'principal': principal_audit(),
              'linear_constraints': constraint_audit(), 'massive45': compile_audit(),
              'homogeneous_sourced_family': homogeneous_family_audit(),
              'triangular21_negative_control': triangular21_negative_audit()}
    result['source_sha256'] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in (Path(__file__), ROOT/'validation/research_eight/07_hyperbolic_symbol.py',
                  ROOT/'validation/geometry/team48/matter_equations.py')}
    path = ROOT/'runs/completion/01_formulation.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
