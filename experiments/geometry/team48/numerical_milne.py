"""Independent temporally consistent Milne counterexample for Frame48.

The exact vacuum initial pair comes from one smooth solution. It loses frame
invertibility under actual integer Engine evolution while every sampled
constraint remains zero. No production equations or decoder are changed.
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

from experiments.geometry.full_gr_audit import einstein_from_jet, symbolic_jet
from universe24.algebra.frame_equations import FIELDS, equations
from universe24.core import Engine, State, Tensor
from universe24.layers.frame48 import compile_frame48
from universe24.observe.frame48 import bank_values, diagnostics, inverse_metric_at
from universe24.prepare.frame48 import flat_values, prepare


def independent_metric_check():
    t, x, y, z = coordinates = sp.symbols('t x y z', real=True)
    # This coordinate embedding independently establishes flatness for t>0.
    embedding = sp.Matrix([t*sp.cosh(x), t*sp.sinh(x), y, z])
    jacobian = embedding.jacobian(coordinates)
    metric = sp.simplify(jacobian.T*sp.diag(-1, 1, 1, 1)*jacobian)
    assert metric == sp.diag(-1, t*t, 1, 1)
    fields = {name: sp.Integer(0) for name in FIELDS}
    fields.update(B00=1/t, B11=sp.Integer(1), B22=sp.Integer(1), K00=-1/t)
    rhs, constraints, _ = equations(fields, lambda name, axis: 0)
    assert all(sp.simplify(rhs[name]-value.diff(t)) == 0 for name, value in fields.items())
    assert all(sp.simplify(value) == 0 for value in constraints.values())
    for instant in (sp.Rational(1, 2), 1, sp.Rational(3, 2), 2):
        oracle = einstein_from_jet(*symbolic_jet(metric, coordinates,
                                  {t: instant, x: 0, y: 0, z: 0}))
        assert oracle['G'] == sp.zeros(4)
        assert all(value == 0 for a in oracle['Riemann'] for b in a for c in b for value in c)
    return {'metric': 'diag(-1,t^2,1,1)',
            'embedding': 'T=t*cosh(x), X=t*sinh(x), Y=y, Z=z',
            'valid_domain': 't>0; no future degeneracy in this exact chart',
            'independent_4d_Einstein_and_Riemann_zero': True,
            'frame_equations_satisfied_by_exact_history': True}


def run(out=None):
    independent = independent_metric_check()
    program = compile_frame48(dt=F(1, 2), dx=F(1, 2))
    previous, current = flat_values(3), flat_values(3)
    previous[FIELDS.index('B00')] = 2
    previous[FIELDS.index('K00')] = -2
    current[FIELDS.index('K00')] = -1
    # Both complete physical slices exactly sample the SAME future-expanding
    # Milne solution at t=1/2 and t=1, separated by the declared dt.
    remainders = np.arange(48*27).reshape(48, 27) % 6
    seed = prepare(program, previous, current, L=3, remainders=remainders)
    engine, state = Engine(program.tensor), seed
    trace = [{'tensor': program.tensor.to_dict(), 'dt': str(program.dt), 'dx': str(program.dx)}]
    rows = []
    for step in range(4):
        trace.append({'step': step, 'state': state.to_dict()})
        values = bank_values(state)
        instant = F(1)+step*program.dt
        diag = diagnostics(values, L=3, dx=program.dx)
        B00, K00 = (int(values[FIELDS.index(name), 0]) for name in ('B00', 'K00'))
        rows.append({'step': step, 'time': str(instant), 'B00': B00, 'K00': K00,
                     'reference_B00': str(1/instant), 'reference_K00': str(-1/instant),
                     'absolute_B00_error': str(abs(F(B00)-1/instant)), **diag})
        assert diag['all_discrete_constraints_zero']
        assert np.array_equal(state.r, seed.r)
        if step == 2:
            assert B00 == K00 == 0 and diag['singular_nodes'] == 27
            try:
                inverse_metric_at(values)
            except ValueError:
                pass
            else:
                raise AssertionError('Singular metric should be rejected')
        if step < 3:
            after = engine.step(state)
            assert engine.inverse_step(after).same_as(state)
            state = after
    assert engine.rewind(state, 3).same_as(seed)
    # The full tensor/seed trace, not the geometric readout, reconstructs state.
    replay = Engine(Tensor.from_dict(trace[0]['tensor']))
    replayed = State.from_dict(trace[1]['state'])
    for row in trace[2:]:
        replayed = replay.step(replayed)
        assert replayed.same_as(State.from_dict(row['state']))
    paths = [Path(__file__).relative_to(ROOT), Path('universe24/layers/frame48.py'),
             Path('universe24/algebra/frame_equations.py'), Path('universe24/core/engine.py')]
    report = {'scope': 'Actual integer Frame48 counterexample with a temporally consistent exact vacuum pair',
              'independent_metric': independent, 'channels': program.tensor.G,
              'tensor_fingerprint': program.tensor.fingerprint,
              'dt': str(program.dt), 'dx': str(program.dx), 'samples': rows,
              'first_singular_update': 2, 'all_sampled_constraints_zero': True,
              'complete_rewind_exact': True, 'complete_trace_replay_exact': True,
              'conclusion': 'Time-consistent initialization alone does not repair Frame48. Constraint residuals alone do not certify a valid metric.',
              'source_sha256': {str(p): hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}}
    if out is not None:
        out = Path(out)
        out.mkdir(parents=True, exist_ok=True)
        (out/'milne_report.json').write_text(json.dumps(report, indent=2)+'\n')
        (out/'milne_full_trace.jsonl').write_text(''.join(json.dumps(row)+'\n' for row in trace))
    return report


if __name__ == '__main__':
    result = run(ROOT/'runs/team48/numerical')
    print(json.dumps({key: result[key] for key in ('channels', 'dt', 'dx', 'first_singular_update',
                    'all_sampled_constraints_zero', 'complete_rewind_exact', 'conclusion')}, indent=2))
