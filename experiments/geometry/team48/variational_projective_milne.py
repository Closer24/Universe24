"""Exact projective vacuum Milne subflow, not general sourced Einstein GR.

Three integer gears represent the rational frame B11=C*S/D, K11=-P*S/D.
The unchanged Engine advances D by P on a prepared invariant manifold.
This is an exact restricted geometry solution, with no observer feedback.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from universe24.core import Engine, State, Tensor
from universe24.algebra.frame_equations import FIELDS, equations

NAMES = ('milne.P', 'milne.C', 'milne.D')


def build():
    return Tensor(NAMES, [(name, 6, ((name, (0, 0, 0), 'b'),)) for name in NAMES],
                  strict_support=True)


def prepare(subdivision, L=3):
    if type(subdivision) is not int or subdivision < 1:
        raise ValueError('positive integer subdivision required')
    current, previous = [1, 1, 2*subdivision], [1, 1, 2*subdivision-1]
    a, b = (np.repeat(np.array(row, dtype=object)[:, None], L**3, axis=1)
            for row in (previous, current))
    r = np.arange(3*L**3).reshape(3, L**3) % 6
    return State(L, a, b, r)


def decode(state, subdivision):
    """Passive rational coordinates only; never fed into Engine."""
    p, c, d = (int(state.b[i, 0]) for i in range(3))
    if d == 0:
        raise ValueError('projective coordinate singularity')
    fields = {name: F(0) for name in FIELDS}
    fields.update(B00=F(c*subdivision, d), B11=F(1), B22=F(1),
                  K00=F(-p*subdivision, d))
    return fields


def symbolic_checks():
    time, step = sp.symbols('time step', positive=True)
    fields = {name: sp.Integer(0) for name in FIELDS}
    fields.update(B00=1/time, B11=sp.Integer(1), B22=sp.Integer(1), K00=-1/time)
    rhs, constraints, _ = equations(fields, lambda name, axis: 0)
    assert all(sp.simplify(sp.diff(fields[name], time)-rhs[name]) == 0 for name in FIELDS)
    assert all(sp.simplify(value) == 0 for value in constraints.values())
    # Independent spacetime calculation, using no frame-equation residuals.
    metric = sp.diag(-1, time*time, 1, 1)
    inverse = metric.inv()
    def derivative(value, axis):
        return sp.diff(value, time) if axis == 0 else 0
    connection = [[[sp.simplify(sum(inverse[a, d]*(
        derivative(metric[d, c], b)+derivative(metric[d, b], c)
        -derivative(metric[b, c], d))/2 for d in range(4)))
        for c in range(4)] for b in range(4)] for a in range(4)]
    ricci = sp.Matrix(4, 4, lambda b, d: sp.simplify(sum(
        derivative(connection[a][b][d], a)-derivative(connection[a][b][a], d)
        +sum(connection[a][a][c]*connection[c][b][d]
             -connection[a][d][c]*connection[c][b][a] for c in range(4))
        for a in range(4))))
    assert ricci == sp.zeros(4)
    kappa, frame = sp.symbols('kappa frame')
    next_kappa = kappa/(1-step*kappa)
    next_frame = frame/(1-step*kappa)
    assert sp.simplify(next_kappa.subs(kappa, -1/time)+1/(time+step)) == 0
    assert sp.simplify(next_frame.subs({kappa: -1/time, frame: 1/time})-1/(time+step)) == 0
    return {'frame_evolution_all_24': True, 'all_frame_constraints': True,
            'independent_spacetime_Ricci_all_16_zero': True,
            'exact_Riccati_map': {'K_next': str(next_kappa), 'B_next': str(next_frame)}}


def audit(out):
    tensor = build()
    engine = Engine(tensor)
    rows = []
    for subdivision in (1, 2, 4, 16, 64, 256):
        seed, state = prepare(subdivision), prepare(subdivision)
        timestep = F(1, subdivision)
        for tick in range(1, subdivision+1):
            previous_fields = decode(state, subdivision)
            before = state
            state = engine.step(state)
            assert engine.inverse_step(state).same_as(before)
            assert np.array_equal(state.r, seed.r)
            assert int(state.b[2, 0]) == 2*subdivision+tick
            assert int(state.b[2, 0]-state.a[2, 0]) == int(state.b[0, 0])
            fields = decode(state, subdivision)
            denominator = 1-timestep*previous_fields['K00']
            assert fields['B00'] == previous_fields['B00']/denominator
            assert fields['K00'] == previous_fields['K00']/denominator
            _, constraints, _ = equations(fields, lambda name, axis: 0)
            assert all(value == 0 for value in constraints.values())
            assert fields['B00'] > 0  # Other diagonal entries are one.
        assert engine.rewind(state, subdivision).same_as(seed)
        rows.append({'subdivision': subdivision, 'physical_proper_time_interval': '1',
                     'final_B00': str(fields['B00']), 'final_K00': str(fields['K00']),
                     'final_det_B': str(fields['B00']), 'exact_constraints_every_step': True,
                     'exact_Riccati_every_step': True, 'exact_rewind': True})
    assert all(row['final_B00'] == '1/3' and row['final_K00'] == '-1/3' for row in rows)
    bad = prepare(4)
    bad.a[:] = bad.b
    following = engine.step(bad)
    assert int(following.b[2, 0]-following.a[2, 0]) != int(following.b[0, 0])
    assert engine.inverse_step(following).same_as(bad)
    report = {'scope': 'exact projective homogeneous vacuum Milne solution; not general GR',
              'channels': tensor.G, 'retained_integers_per_node': 3*tensor.G,
              'monomials': len(tensor), 'rank': tensor.rank,
              'tensor_fingerprint': tensor.fingerprint,
              'strict_single_edge': not tensor.support_violations(),
              'same_tensor_for_every_subdivision': True,
              'symbolic': symbolic_checks(), 'refinement': rows,
              'off_prepared_history_control': {'history_constraint_failed': True, 'exact_rewind': True},
              'limitations': ['Homogeneous diagonal vacuum sector only; spatial curvature and all matter sources vanish.',
                  'Rational passive decoding is essential; physical B and K are not retained integer gears.',
                  'A general sourced or spatially varying RHS does not close in these three projective fields.',
                  'Nondegeneracy holds only while D is nonzero; the tested expanding branch has D positive.',
                  'Correct prepared slopes are necessary; arbitrary reversible initial history need not describe the solution.'],
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2)+'\n')
    return report


if __name__ == '__main__':
    print(json.dumps(audit(ROOT/'runs/team48/variational/projective_milne.json'), indent=2))
