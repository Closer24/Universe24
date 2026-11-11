"""Einstein-derived homogeneous radiation dynamics in the unchanged Engine.

Optional, off-default, symmetry-reduced sector; NOT a general Regge solver.
Run: python experiments/geometry/einstein_friedmann.py --out runs/geometry/friedmann
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import argparse
from fractions import Fraction
import hashlib
import json
import platform
import numpy as np
import sympy as sp
from universe24.core import Engine, State, Tensor
from universe24.core.lattice import ZERO
from universe24.core.reciprocity import check_reciprocity
from experiments.geometry.friedmann_derivation import audit
from experiments.geometry.full_gr_audit import audit as full_gr_audit
from experiments.geometry.simplex_metric import (
    signed_intervals, metric_from_intervals, straight_path_refinement,
)

REFINEMENTS = (1, 2, 4, 8)
NAMES = ('geometry.scale', 'matter.radiation', 'clock.proper')
CLOCK_JUSTIFICATION = ('Passive comoving proper-time quadrature. The clock is a retained '
                       'counter with no stress-energy and no backreaction on the FLRW sector.')


def build(n=1, L=6, Q=1):
    if type(n) is not int or n not in REFINEMENTS:
        raise ValueError(f'n must be one of {REFINEMENTS}')
    if type(L) is not int or L < 3 or type(Q) is not int or Q <= 0:
        raise ValueError('L>=3 and Q>0 must be integers')
    D = 6 * Q
    b = lambda name: (name, ZERO, 'b')
    meta = {'designated_one_way': CLOCK_JUSTIFICATION}
    terms = [(name, D, (b(name),)) for name in NAMES]
    terms += [('clock.proper', D, (b('geometry.scale'),), meta),
              ('clock.proper', -D, (('geometry.scale', ZERO, 'a'),), meta)]
    tensor = Tensor(NAMES, terms, Q=Q, strict_support=True)
    assert tensor.rank == 2 and check_reciprocity(tensor).ok
    return tensor, {'n': n, 'L': L, 'Q': Q, 'D': D, 'scale': 64*n,
                    'steps': 8*n, 'dt': f'1/{n}'}


def validate_sector(state, p):
    """Initial-data/readout contract only; never called inside Engine.step."""
    if state.G != 3 or state.L != p['L']:
        raise ValueError('wrong board shape')
    if not (np.all(state.a == state.a[:, :1]) and np.all(state.b == state.b[:, :1])):
        raise ValueError('FLRW requires homogeneous a,b; arbitrary r is allowed')
    if np.any(state.r < 0) or np.any(state.r >= p['D']):
        raise ValueError('remainders must lie in [0,D)')
    A, E, C = (int(value) for value in state.b[:, 0])
    previous_A, previous_E, previous_C = (int(value) for value in state.a[:, 0])
    if min(A, previous_A) <= 0:
        raise ValueError('physical FLRW chart requires positive scale')
    B = A - previous_A
    if E != previous_E or E != 3 * p['n']**2 * B**2:
        raise ValueError('Einstein lapse constraint or constant comoving energy violated')
    if C - previous_C != A + previous_A:
        raise ValueError('proper clock is inconsistent with the metric')


def prepare(p, slope=8, energy=None):
    """Prepare constrained data; the Engine subsequently evolves autonomously.

    `energy` may be specified independently, in integer units. Invalid pairs
    are rejected here, not projected or repaired during evolution.
    """
    if type(slope) is not int or (energy is not None and type(energy) is not int):
        raise ValueError('integer slope and energy are required')
    A = 2 * p['scale']
    E = 3 * p['n']**2 * slope**2 if energy is None else energy
    a = np.tile(np.array([A-slope, E, -2*A+slope], dtype=object)[:, None], (1, p['L']**3))
    b = np.tile(np.array([A, E, 0], dtype=object)[:, None], (1, p['L']**3))
    r = (17 * np.arange(b.size).reshape(b.shape) + 5) % p['D']
    state = State(p['L'], a, b, r)
    validate_sector(state, p)
    return state


def local_readout(state, after, p, node=0):
    """Exact continuum decoder for the affine homogeneous solution family.

    Acceleration is measured from three retained time slices. T is computed
    from the independent energy gear and the assumed radiation equation of state.
    """
    S, n = p['scale'], p['n']
    A, E, C = (int(v) for v in state.b[:, node])
    a = Fraction(A, S)
    if a <= 0:
        raise ValueError('the physical metric is singular at a=0')
    velocity = Fraction(n * (A-int(state.a[0, node])), S)
    acceleration = Fraction(n*n * (int(after.b[0, node])-2*A+int(state.a[0, node])), S)
    energy = Fraction(E, S*S)
    tau = Fraction(C, 2*S*n)
    rho = energy / a**4
    G = [3*velocity**2/a**2] + [(velocity**2-2*a*acceleration)/a**2]*3
    T = [energy/a**2] + [energy/(3*a**2)]*3
    residual = [[G[i]-T[i] if i == j else Fraction(0) for j in range(4)] for i in range(4)]
    return {'scale': a, 'velocity': velocity, 'acceleration': acceleration,
            'comoving_energy': energy, 'proper_time': tau, 'rho': rho,
            'pressure': rho/3, 'G_diagonal': G, 'T_diagonal': T,
            'Einstein_residual': residual,
            'R': 6*acceleration/a**3,
            'Kretschmann': 12*((a*acceleration-velocity**2)**2+velocity**4)/a**8}


def link_readout(a, h=Fraction(1)):
    """Lengths and angles are local tangent data, not finite geodesic distances."""
    a, h = sp.Rational(a), sp.Rational(h)
    metric = sp.diag(-a*a, a*a, a*a, a*a)
    basis = sp.diag(h/2, h, h, h)
    lengths = signed_intervals(metric, basis)
    reconstructed = metric_from_intervals(lengths, basis)
    assert reconstructed == metric
    return {'signed_squared_tangent_intervals': {f'{i}-{j}': str(v) for (i, j), v in lengths.items()},
            'metric': [[str(v) for v in reconstructed.row(i)] for i in range(4)],
            'spatial_edge_length': str(a*h), 'spatial_angle_cosines': ['0', '0', '0'],
            'exact_metric_reconstruction': True}


def jsonable(value):
    if isinstance(value, (Fraction, sp.Rational)):
        return str(value)
    if isinstance(value, dict):
        return {key: jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [jsonable(item) for item in value]
    return value


def run_case(n, slope=8, out=None, L=6):
    tensor, p = build(n, L=L)
    seed = prepare(p, slope)
    if min(int(seed.b[0, 0]), int(seed.b[0, 0]) + (p['steps']+1)*slope) <= 0:
        raise ValueError('requested observation window crosses a=0')
    engine = Engine(tensor, p['Q'])
    state = seed
    history, samples = [], []
    node_checks = 0
    for tick in range(p['steps']+1):
        # Only this unchanged Engine call produces the next state.
        after = engine.step(state)
        assert engine.inverse_step(after).same_as(state)
        validate_sector(state, p)
        np.testing.assert_array_equal(state.r, seed.r)
        assert np.all(after.b == after.b[:, :1])
        row = local_readout(state, after, p)
        assert all(v == 0 for line in row['Einstein_residual'] for v in line)
        eta = Fraction(tick, n)
        assert row['scale'] == 2 + row['velocity']*eta
        assert row['proper_time'] == 2*eta + row['velocity']*eta**2/2
        assert row['scale']**2 == 4 + 2*row['velocity']*row['proper_time']
        assert row['rho']*row['scale']**4 == row['comoving_energy']
        # A comoving timelike edge is a geodesic: this integrated length is exact.
        proper_edge = Fraction(int(after.b[2, 0])-int(state.b[2, 0]), 2*p['scale']*n)
        assert proper_edge == Fraction(int(after.b[0, 0])+int(state.b[0, 0]), 2*p['scale']*n)
        row.update(tick=tick, conformal_time=eta, next_comoving_proper_edge=proper_edge,
                   links=link_readout(row['scale'], Fraction(1, n)))
        # Homogeneity was checked on every retained a,b at all nodes, so this
        # exact readout applies to all L^3 nodes, regardless of their remainders.
        node_checks += state.N
        samples.append(jsonable(row))
        history.append(np.stack([state.a, state.b, state.r]))
        if tick < p['steps']:
            state = after
    assert engine.rewind(state, p['steps']).same_as(seed)
    result = {'parameters': p, 'slope_integer': slope, 'tensor_fingerprint': tensor.fingerprint,
              'rank': tensor.rank, 'monomials': len(tensor.monomials), 'gears': list(tensor.names),
              'support_violations': tensor.support_violations(),
              'clock_one_way_designation': CLOCK_JUSTIFICATION,
              'reciprocity_with_designated_clock': check_reciprocity(tensor).ok,
              'all_rewinds_exact': True, 'max_Einstein_residual': '0',
              'node_snapshots_checked': node_checks, 'samples': samples}
    if out is not None:
        out = Path(out)
        out.mkdir(parents=True, exist_ok=True)
        tag = f'n{n}_slope{slope}'
        trace = np.stack(history)
        # Saving arbitrary precision as decimal strings avoids pickle.
        stored = trace.astype(str) if trace.dtype == object else trace
        np.savez_compressed(out/f'{tag}_states.npz', states=stored)
        result['trace_dtype'] = str(stored.dtype)
        (out/f'{tag}.json').write_text(json.dumps(result, indent=2)+'\n')
    return result


def negative_controls():
    tensor, p = build()
    engine = Engine(tensor, p['Q'])
    # Preserve an affine geometry while supplying the wrong independent matter energy.
    wrong_source = prepare(p)
    wrong_source.a[1] += 1
    wrong_source.b[1] += 1
    after = engine.step(wrong_source)
    residual = local_readout(wrong_source, after, p)['Einstein_residual']
    maximum = max(abs(v) for row in residual for v in row)
    assert maximum > 0 and engine.inverse_step(after).same_as(wrong_source)
    rejected = False
    try:
        validate_sector(wrong_source, p)
    except ValueError:
        rejected = True
    assert rejected
    # A tensor modification remains invertible but no longer follows Einstein's action.
    terms = [(tensor.names[m.target], m.coeff,
              tuple((tensor.names[f.gear], f.offset, f.field) for f in m.factors))
             for m in tensor.monomials]
    terms.append(('geometry.scale', p['D'], ()))
    changed = Engine(Tensor(NAMES, terms, Q=p['Q'], strict_support=True), p['Q'])
    seed = prepare(p)
    forced = changed.step(seed)
    force_residual = local_readout(seed, forced, p)['Einstein_residual']
    force_max = max(abs(v) for row in force_residual for v in row)
    assert force_max > 0 and changed.inverse_step(forced).same_as(seed)
    return {'wrong_source_max_Einstein_residual': str(maximum),
            'wrong_source_rewinds_exactly': True, 'wrong_source_rejected_by_initial_constraint': rejected,
            'added_force_max_Einstein_residual': str(force_max), 'added_force_rewinds_exactly': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=Path('runs/geometry/friedmann'))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    symbolic = audit()
    cases = [run_case(n, slope, args.out) for n in REFINEMENTS for slope in (0, 8, 16, -8)]
    report = {'scope': 'Einstein-derived k=Lambda=0 homogeneous perfect-radiation sector only; no general Regge solver',
              'derivation': symbolic, 'negative_controls': negative_controls(),
              'general_nonlinear_GR_observer': full_gr_audit(),
              'finite_straight_path_refinement': straight_path_refinement(),
              'node_snapshots_checked': sum(case['node_snapshots_checked'] for case in cases),
              'all_16_Einstein_components_exact_at_every_checked_node': True,
              'cases': [{key: value for key, value in case.items() if key != 'samples'} for case in cases],
              'python': platform.python_version(), 'numpy': np.__version__, 'sympy': sp.__version__,
              'source_sha256': {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in (
                  'experiments/geometry/einstein_friedmann.py',
                  'experiments/geometry/friedmann_derivation.py',
                  'experiments/geometry/simplex_metric.py',
                  'experiments/geometry/full_gr_audit.py',
                  'universe24/core/engine.py', 'universe24/core/tensor.py')}}
    (args.out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    (args.out/'tensor.json').write_text(json.dumps(build()[0].to_dict(), indent=2)+'\n')
    print(json.dumps({'node_snapshots_checked': report['node_snapshots_checked'],
                      'derivation_checks': symbolic['checks'], 'negative_controls': report['negative_controls']}, indent=2))


if __name__ == '__main__':
    main()
