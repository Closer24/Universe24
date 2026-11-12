"""Same-law massive45 clock-port audit, with no retained apparatus claim.

All floating phase values are passive readouts. The Engine and its complete
integer state never read them. A periodic scalar diagnostic is not automatically
an operational measurement of elapsed proper time.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import importlib
import json
import math
from pathlib import Path

import sympy as sp

from universe24.core import Engine
from validation.geometry.team48 import refinement_integer_projective as projective


def invariants(fields):
    """Exact U(1)-invariant local expressions from one retained slice."""
    x, y, px, py = (F(fields[name]) for name in ('phi', 'chi', 'Pi_phi', 'Pi_chi'))
    intensity, radial, momentum2, charge = x*x+y*y, x*px+y*py, px*px+py*py, x*py-y*px
    assert intensity*momentum2-radial*radial == charge*charge
    return intensity, radial, momentum2, charge


def identities():
    x, y, px, py, k, m = sp.symbols('x y px py K m', real=True)
    I, S, P, charge_invariant = x*x+y*y, x*px+y*py, px*px+py*py, x*py-y*px
    rhs = (px, py, k*px-m*m*x, k*py-m*m*y)
    derivative = lambda f: sp.expand(sum(sp.diff(f, v)*dv for v, dv in zip((x,y,px,py), rhs)))
    assert derivative(I) == 2*S
    assert sp.expand(derivative(S)-(P+k*S-m*m*I)) == 0
    assert sp.expand(derivative(charge_invariant)-k*charge_invariant) == 0
    # Circular flat controls have constant intensity despite nonzero internal phase.
    t, amplitude = sp.symbols('t A', real=True)
    circular_I = amplitude**2*(sp.cos(m*t)**2+sp.sin(m*t)**2)
    assert sp.trigsimp(circular_I-amplitude**2) == 0
    # Radial charge_invariant=0 clock phase: theta=arg((m^2 I-P)-2 i m S)/2.
    # General charge_invariant gives a different denominator; do not silently assume radial motion.
    X, Y = m*m*I-P, -2*m*S
    numerator = sp.expand((X*derivative(Y)-Y*derivative(X))/2)
    denominator = sp.expand(X*X+Y*Y)
    expected = m*((P+m*m*I)**2-4*m*m*charge_invariant*charge_invariant)-k*m*S*(P+m*m*I)
    assert sp.expand(numerator-expected) == 0
    assert sp.expand(denominator-((P+m*m*I)**2-4*m*m*charge_invariant*charge_invariant)) == 0
    return {'I_dot': '2 S', 'S_dot': 'P_squared + trace(K) S - m_squared I',
            'Q_dot_homogeneous': 'trace(K) charge_invariant',
            'radial_phase_rate_Q_zero': 'm - trace(K)*m*S/(m_squared*I+P_squared)',
            'radial_domain': 'm>0, charge_invariant=0, m_squared*I+P_squared>0',
            'circular_flat_intensity_is_constant': True,
            'zero_source_phase_is_undefined': True,
            'massless_has_no_mass_period': True,
            'scope': 'homogeneous continuum identities, not discrete clock calibration'}


def pointer_budget():
    """Exact source-degree/energy check for the open two-slot proposal in #45."""
    q, p, x, y, g, omega, mass = sp.symbols('q p x y g omega mass', real=True)
    I = x*x+y*y
    potential = sp.Rational(1,2)*mass**2*I+sp.Rational(1,2)*omega**2*q*q+g*q*I
    minimized = sp.expand(potential.subs(q, -g*I/omega**2))
    assert sp.simplify(minimized-(mass**2*I/2-g*g*I*I/(2*omega**2))) == 0
    # This is a source ledger, not a new coupled tensor accepted by this audit.
    return {'base_channels': 45, 'homogeneous_pointer_q_p': 2,
            'one_record_slot': 1, 'proposed_total': 48,
            'potential_polynomial_degree': sp.Poly(potential, q,x,y).total_degree(),
            'full_transported_real_scalar_total': 50,
            'minimized_total_potential': str(minimized),
            'globally_bounded_energy': False,
            'compiler_and_metric_backreaction': 'not_tested_here',
            'spatial_momentum_balance': 'open',
            'status': 'proposal_only_not_attached_to_board_tensor'}


def audit_snapshots(board):
    """Read exact board fields; never infer an operational click clock."""
    rows = []
    for snapshot in board['snapshots']:
        values = []
        for node in snapshot['nodes']:
            I, S, P, charge_invariant = invariants(node['fields_exact'])
            values.append((I, S, P, charge_invariant))
        assert all(value == values[0] for value in values), 'clock fixture must be homogeneous'
        I, S, P, charge_invariant = values[0]
        phase = None if I+P == 0 or charge_invariant != 0 else math.atan2(float(-2*S), float(I-P))/2
        rows.append({'step': snapshot['step'], 'time_exact': snapshot['time_exact'],
                     'I': str(I), 'S': str(S), 'P_squared': str(P), 'charge_invariant': str(charge_invariant),
                     'principal_radial_phase': phase})
    return {'samples': rows, 'additional_retained_channels': 0,
            'full_period_resolved': False, 'phase_winding_register': 'absent',
            'proper_time_from_clicks': 'not_implemented',
            'moving_clock': 'not_implemented',
            'scope': 'passive same-run invariant diagnostics only'}


def same_law_rotation_audit(steps=4):
    from .run import build_program, prepare_seed
    program = build_program()
    seed = prepare_seed(program)
    pairs = [('phi','chi'), ('Pi_phi','Pi_chi')]+[(f'Xi_phi{i}',f'Xi_chi{i}') for i in range(3)]
    def rotate_state(state):
        answer = state.copy()
        for left, right in pairs:
            i, j = 1+program.fields.index(left), 1+program.fields.index(right)
            for source, target in ((state.a, answer.a), (state.b, answer.b)):
                target[i], target[j] = -source[j].copy(), source[i].copy()
        return answer
    rotated = rotate_state(seed)
    initial_rotated = rotated.copy()
    engine = Engine(program.tensor)
    oracle = importlib.import_module('validation.research_eight.07_hyperbolic_symbol').scalar_oracle
    left, right = seed.copy(), rotated
    maximum_bits = 0
    for step in range(steps+1):
        assert rotate_state(left).same_as(right)
        lvalue, rvalue = projective.readout(program, left), projective.readout(program, right)
        for node in range(seed.N):
            lf, rf = ({name: ar[i,node] for i,name in enumerate(program.fields)} for ar in (lvalue,rvalue))
            assert invariants(lf) == invariants(rf)
        maximum_bits = max(maximum_bits, left.max_abs().bit_length(), right.max_abs().bit_length())
        if step == steps:
            break
        for state in (left, right):
            after = engine.step(state)
            assert after.same_as(oracle(program.tensor, state))
            assert engine.inverse_step(after).same_as(state)
        left, right = engine.step(left), engine.step(right)
    assert engine.rewind(left, steps).same_as(seed)
    assert engine.rewind(right, steps).same_as(initial_rotated)
    return {'channels': program.tensor.G, 'tensor_sha256': program.tensor.fingerprint,
            'mass_squared': 1, 'steps': steps, 'nodes': seed.N,
            'integer_quarter_turn_equivariance': True,
            'I_S_charge_and_geometry_invariant': True,
            'independent_integer_oracle': True, 'complete_rewind': True,
            'maximum_retained_bits': maximum_bits,
            'scope': 'same massive45 law; this checks global phase rotation, not local gauge closure'}


def audit(board=None):
    report = {'schema': 'universe24/geodesic-board/clocks/1',
              'identities': identities(), 'same_law': same_law_rotation_audit(),
              'apparatus_allocation': pointer_budget(),
              'operational_clock_gate': 'not_established'}
    if board is not None:
        if board['metadata']['tensor_sha256'] != report['same_law']['tensor_sha256']:
            raise ValueError('Clock audit cannot borrow evidence from a different tensor')
        report['same_run'] = audit_snapshots(board)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--board', type=Path, default=Path('runs/geodesic_board/board_data.json'))
    parser.add_argument('--out', type=Path, default=Path('runs/geodesic_board/clock-audit.json'))
    args = parser.parse_args()
    source = args.board
    board = json.loads(source.read_text()) if source.exists() else None
    report = audit(board)
    output = args.out
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
