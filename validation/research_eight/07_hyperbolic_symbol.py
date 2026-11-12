"""Exact principal-symbol research and an isolated 45-channel candidate.

No production change. The candidate fixes a continuum principal-symbol defect;
it does not certify discrete constraints, metric positivity, or efficient bits.
Run: python -m validation.research_eight.07_hyperbolic_symbol
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import numpy as np
import sympy as s

from universe24.algebra import frame_equations as frame
from universe24.core import Engine, State
from universe24.core.lattice import lattice
from validation.geometry.team48 import geometry_triangular as triangular
from validation.geometry.team48 import matter_charged, matter_dust_square
from validation.geometry.team48 import refinement_integer_projective as projective

ROOT = Path(__file__).resolve().parents[2]
DIRECTIONS = ((1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 2, 3))


def add_constraints(rhs, constraints, ricci):
    """Precompiled RHS changes, zero on the declared continuum constraints."""
    result = dict(rhs)
    for a in range(3):
        for b in range(a, 3):
            result[f'K{a}{b}'] += F(1, 2)*(ricci[b][a]-ricci[a][b])
    for name in result:
        if name.startswith('G') and len(name) == 4:
            a, b, c = map(int, name[1:])
            result[name] -= F(1, 4)*(int(a == c)*constraints[f'M{b}']
                                      -int(b == c)*constraints[f'M{a}'])
    return result


def symbol(module, direction, corrected=False):
    fields = {name: s.Integer(int(name.startswith('B') and name[1] == name[2]))
              for name in module.FIELDS}
    jet = dict(zip(fields, s.symbols(f'z:{len(fields)}')))
    rhs, constraints, ricci = module.equations(fields, lambda name, axis: direction[axis]*jet[name])
    if corrected:
        rhs = add_constraints(rhs, constraints, ricci)
    return s.Matrix([rhs[name] for name in fields]).jacobian(list(jet.values()))


def spectrum(matrix):
    rows = [{'speed': str(value), 'algebraic': multiplicity,
             'geometric': len((matrix-value*s.eye(matrix.rows)).nullspace()),
             'real': bool(value.is_real)}
            for value, multiplicity in matrix.eigenvals().items()]
    return {'eigenspaces': rows,
            'real_diagonalizable': all(row['real'] and row['algebraic'] == row['geometric'] for row in rows),
            'ranks_A_A2_A3': [matrix.rank(), (matrix**2).rank(), (matrix**3).rank()]}


def symbol_audit():
    results = {}
    for label, module in (('full24', frame), ('triangular20', triangular)):
        for corrected in (False, True):
            key = label+('_constraint_added' if corrected else '_original')
            results[key] = [{'direction': direction, **spectrum(symbol(module, direction, corrected))}
                            for direction in DIRECTIONS]
    assert not all(row['real_diagonalizable'] for row in results['triangular20_original'])
    assert all(row['real_diagonalizable'] for row in results['full24_constraint_added'])
    assert not results['triangular20_constraint_added'][-1]['real_diagonalizable']

    # General-direction square-free annihilator; not a sampled-direction claim.
    n = s.symbols('nx ny nz', real=True)
    matrix = symbol(frame, n, True)
    square, radius, identity = matrix**2, sum(v*v for v in n), s.eye(matrix.rows)
    annihilator = matrix
    for coefficient in (s.Integer(1), s.Rational(1, 2), s.Rational(1, 8)):
        annihilator = (annihilator*(square-coefficient*radius*identity)).applyfunc(s.expand)
    assert annihilator == s.zeros(matrix.rows)
    x = s.Symbol('lambda')
    for direction in DIRECTIONS:
        value = sum(v*v for v in direction)
        actual = symbol(frame, direction, True).charpoly(x).as_expr()
        expected = x**14*(x*x-value)**2*(x*x-s.Rational(value, 2))*(x*x-s.Rational(value, 8))**2
        assert s.expand(actual-expected) == 0

    # Independent transparent Jordan witness, with no eigensolver needed.
    names = triangular.FIELDS
    unit = lambda name: s.eye(len(names))[:, names.index(name)]
    matrix = symbol(triangular, (0, 0, 1))
    v2, v1, v0 = unit('G010'), -unit('K12'), 2*unit('G122')
    assert matrix*v2 == v1 and matrix*v1 == v0 and matrix*v0 == s.zeros(len(names), 1)
    eps = s.Symbol('eps')
    fields = {name: s.Integer(int(name.startswith('B') and name[1] == name[2]))+eps*v2[i]
              for i, name in enumerate(names)}
    _, constraints, _ = triangular.equations(fields, lambda name, axis: int(axis == 2)*eps*v2[names.index(name)])
    defects = {name: str(s.diff(value, eps).subs(eps, 0)) for name, value in constraints.items()
               if s.diff(value, eps).subs(eps, 0) != 0}
    assert any(name.startswith('C') for name in defects)
    # Transverse-traceless data are a constraint-consistent principal control.
    tt = unit('K00')-unit('K11')
    assert (symbol(triangular, (0, 0, 1), True)-matrix)*tt == s.zeros(len(names), 1)
    return {'direction_tests': results, 'all_direction_square_free_annihilator': True,
            'annihilator': 'A (A^2-|n|^2 I) (A^2-|n|^2 I/2) (A^2-|n|^2 I/8)=0',
            'original_triangular_Jordan_chain': ['G010', '-K12', '2G122', '0'],
            'Jordan_seed_linear_constraint_defects': defects,
            'TT_constraint_consistent_principal_change': 0,
            'scope': 'Continuum frozen principal symbol; not raw integer-microstep or full discrete stability.'}


def corrected_charged(fields, partial, *, mass_squared=0, cosmological=0, coupling=1):
    rhs, constraints, diagnostic = matter_dust_square.equations(
        fields, partial, base_equations=matter_charged.equations,
        mass_squared=mass_squared, cosmological=cosmological, coupling=coupling)
    return add_constraints(rhs, constraints, diagnostic['ricci']), constraints, diagnostic


def build45():
    fields = matter_dust_square.FIELDS_CHARGED
    assert len(fields) == 44
    return projective.compile_projective(fields, corrected_charged,
                                         dt=F(1, 16), dx=F(1, 4), degree=2)


def scalar_oracle(tensor, state):
    """Literal Python integer monomials/divmod, never Engine evaluation."""
    lat = lattice(state.L)
    shifts = {factor.offset: lat.shift_index(factor.offset)
              for term in tensor.monomials for factor in term.factors}
    out, carry = np.zeros(state.b.shape, dtype=object), np.zeros(state.r.shape, dtype=object)
    for node in range(state.N):
        inputs = [0]*state.G
        for term in tensor.monomials:
            value = term.coeff
            for factor in term.factors:
                array = state.a if factor.field == 'a' else state.b
                value *= int(array[factor.gear, shifts[factor.offset][node]])
            inputs[term.target] += value
        for g in range(state.G):
            quotient, remainder = divmod(2*inputs[g]+int(state.r[g, node]), 6)
            out[g, node], carry[g, node] = quotient-int(state.a[g, node]), remainder
    return State(state.L, state.b, out, carry)


def compile_audit():
    program = build45()
    tensor = program.tensor
    assert tensor.G == 45 and not tensor.support_violations() and tensor.rank-1 <= 3
    assert not any(f.field == 'a' for m in tensor.monomials for f in m.factors)
    rng = np.random.default_rng(7002026)
    values = rng.integers(-2, 3, size=(44, 27)).astype(object)
    for i, name in enumerate(program.fields):
        if name.startswith('B'):
            values[i] = np.full(27, int(name[1] == name[2]), dtype=object)
    remainder = np.array([[(g+node) % 6 for node in range(27)] for g in range(45)], dtype=object)
    seed = projective.prepare(program, values, L=3, denominator=16, remainders=remainder)
    engine, state = Engine(tensor), seed
    largest = 0
    for _ in range(3):
        expected, after = scalar_oracle(tensor, state), engine.step(state)
        assert after.same_as(expected) and engine.inverse_step(after).same_as(state)
        assert np.array_equal(after.r, seed.r)
        largest = max(largest, max(abs(int(v)).bit_length() for ar in (after.a, after.b, after.r) for v in ar.flat))
        state = after
    assert engine.rewind(state, 3).same_as(seed)

    # Nonlinear homogeneous sourced, constraint-consistent RHS equality control.
    f = {name: s.Integer(0) for name in program.fields}
    for a in range(3):
        f[f'B{a}{a}'], f[f'K{a}{a}'] = s.Integer(1), s.Integer(-1)
    f['Pi_phi'], f['dust_amplitude'] = s.Integer(2), s.Integer(1)
    original, constraints, _ = matter_dust_square.equations(f, lambda *_: s.Integer(0),
        base_equations=matter_charged.equations, mass_squared=0)
    corrected, _, _ = corrected_charged(f, lambda *_: s.Integer(0))
    assert all(constraints[k] == 0 for k in ('H', 'M0', 'M1', 'M2'))
    assert original == corrected
    return {'channels': tensor.G, 'retained_integers_per_node': 3*tensor.G,
            'monomials': len(tensor), 'degree': tensor.rank-1,
            'strict_face_support': True, 'old_a_inputs': False,
            'tensor_sha256': tensor.fingerprint, 'static_multiplier': program.multiplier,
            'steps': 3, 'nodes': 27, 'independent_scalar_oracle': True,
            'all_six_remainders_and_full_rewind': True, 'max_retained_bits': largest,
            'homogeneous_sourced_constraint_surface_RHS_equality': True,
            'metric_positivity': 'not_established', 'nonlinear_discrete_constraint_propagation': 'not_established',
            'bit_growth': 'unchanged_projective_obstruction', 'operational_apparatus': 'not_implemented'}


def main():
    result = {'scope': 'Source-only symbol repair candidate; no installed model or physical acceptance.',
              'principal_symbol': symbol_audit(), 'actual_45channel_Engine': compile_audit(),
              'Euler_wave_gain_squared': '1+h^2*omega^2; no imaginary-axis absolute stability',
              'time_discretization_scope': 'Euler leading branch only; complete projective amplification needs its own proof.',
              'source_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in (Path(__file__), ROOT/'universe24/algebra/frame_equations.py',
                                         ROOT/'validation/geometry/team48/geometry_triangular.py')}}
    out = ROOT/'runs/research_eight/07_hyperbolic_symbol.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'output': str(out), 'all_direction_symbol_identity': True,
                      'engine': result['actual_45channel_Engine']}, indent=2))


if __name__ == '__main__':
    main()
