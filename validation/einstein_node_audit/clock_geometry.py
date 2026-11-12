"""Exact kinematic controls, not an Engine clock or a derivation of gravity.

Run: python -m validation.einstein_node_audit.clock_geometry
"""
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path

import sympy as s

from universe24.observe.metric_clocks import rate_squared


def curvature(metric, coordinates):
    """Independent coordinate Christoffel/Riemann calculation, signature -+++."""
    inverse = metric.inv()
    dim = len(coordinates)
    gamma = [[[s.simplify(sum(inverse[a, d] * (
        s.diff(metric[d, c], coordinates[b])
        + s.diff(metric[d, b], coordinates[c])
        - s.diff(metric[b, c], coordinates[d])) / 2
        for d in range(dim))) for c in range(dim)]
        for b in range(dim)] for a in range(dim)]
    riemann = {}
    for a in range(dim):
        for b in range(dim):
            for c in range(dim):
                for d in range(dim):
                    riemann[a, b, c, d] = s.simplify(
                        s.diff(gamma[a][d][b], coordinates[c])
                        - s.diff(gamma[a][c][b], coordinates[d])
                        + sum(gamma[a][c][e] * gamma[e][d][b]
                              - gamma[a][d][e] * gamma[e][c][b]
                              for e in range(dim)))
    ricci = s.Matrix(dim, dim, lambda b, d:
                     sum(riemann[a, b, a, d] for a in range(dim)))
    scalar = s.simplify(sum(inverse[b, d] * ricci[b, d]
                            for b in range(dim) for d in range(dim)))
    return gamma, riemann, ricci, scalar


def metric_from_rates(measure, epsilon=F(1, 10)):
    """Ten quadratic-form evaluations in a fixed known chart reconstruct g.

    This is an algebraic identifiability oracle. In this audit measure is the
    existing passive readout; no independent physical apparatus is claimed.
    All sampled velocities must be timelike for an operational interpretation.
    """
    zero = (F(0),) * 3
    baseline = measure(zero)
    metric = [[F(0) for _ in range(4)] for _ in range(4)]
    metric[0][0] = -baseline
    singles = []
    for i in range(3):
        positive, negative = list(zero), list(zero)
        positive[i], negative[i] = epsilon, -epsilon
        plus, minus = measure(positive), measure(negative)
        singles.append(plus)
        metric[0][i + 1] = metric[i + 1][0] = -(plus - minus)/(4*epsilon)
        metric[i + 1][i + 1] = -(plus + minus - 2*baseline)/(2*epsilon**2)
    for i in range(3):
        for j in range(i + 1, 3):
            velocity = list(zero)
            velocity[i] = velocity[j] = epsilon
            entry = -(measure(velocity) - singles[i] - singles[j] + baseline)/(2*epsilon**2)
            metric[i + 1][j + 1] = metric[j + 1][i + 1] = entry
    return metric


def audit():
    t, x, y, z = s.symbols('t x y z', real=True)
    a, h = s.symbols('a H', nonzero=True, real=True)
    coordinates = (t, x, y, z)
    _, flat_r, _, flat_scalar = curvature(s.diag(-1, 1, 1, 1), coordinates)
    assert all(value == 0 for value in flat_r.values())
    lapse = 1 + a*x
    rindler_g, rindler_r, _, rindler_scalar = curvature(
        s.diag(-lapse**2, 1, 1, 1), coordinates)
    assert all(value == 0 for value in rindler_r.values())
    assert rindler_g[1][0][0] == a*lapse
    assert s.diff(lapse, x) == a
    de_sitter = s.diag(-1, *([s.exp(2*h*t)] * 3))
    _, curved_r, curved_ricci, curved_scalar = curvature(de_sitter, coordinates)
    assert curved_scalar == 12*h*h
    assert curved_r[1, 0, 1, 0] == -h*h
    assert curved_ricci == 3*h*h*de_sitter

    # An exact off-diagonal Lorentzian metric in an ADM chart, c=1.
    spatial = [[F(2), F(1, 3), F(0)],
               [F(1, 3), F(3), F(1, 7)],
               [F(0), F(1, 7), F(4)]]
    shift, alpha = (F(1, 5), F(-1, 6), F(1, 9)), F(7, 4)
    cov = [sum(spatial[i][j]*shift[j] for j in range(3)) for i in range(3)]
    metric = [[-alpha*alpha + sum(cov[i]*shift[i] for i in range(3)), *cov]]
    metric += [[cov[i], *spatial[i]] for i in range(3)]
    sampled = []

    def read(velocity):
        result = rate_squared(metric, velocity)
        assert result > 0
        sampled.append({'velocity': list(map(str, velocity)), 'rate_squared': str(result)})
        return result

    recovered = metric_from_rates(read)
    assert recovered == metric
    assert len(sampled) == 10
    # Held-out prediction is independent of the ten recovery samples.
    held_out = []
    for velocity in [(F(1, 8), F(-1, 12), F(1, 16)),
                     (F(-1, 7), F(1, 20), F(-1, 15))]:
        expected = rate_squared(metric, velocity)
        assert expected > 0 and rate_squared(recovered, velocity) == expected
        held_out.append({'velocity': list(map(str, velocity)), 'rate_squared': str(expected)})
    # A stationary readout cannot detect nine independently variable components.
    wrong = [row.copy() for row in metric]
    wrong[1][2] += F(1, 5)
    wrong[2][1] += F(1, 5)
    assert rate_squared(wrong) == rate_squared(metric)
    v = (F(1, 10), F(1, 10), F(0))
    assert rate_squared(wrong, v) != rate_squared(metric, v)
    result = {
        'scope': 'exact continuum/readout controls; no new retained clock, Engine law or physical acceptance',
        'checks': {
            'rindler_nonuniform_clocks_zero_riemann': 'passed',
            'equal_rest_rates_flat_and_de_sitter_different_curvature': 'passed',
            'de_sitter_einstein_lambda_3H_squared': 'passed',
            'ten_timelike_rates_reconstruct_all_metric_entries': 'passed',
            'held_out_rate_predictions': 'passed',
            'stationary_only_wrong_metric_rejected_by_moving_rates': 'passed',
        },
        'rindler': {'domain': '1+a*x>0', 'clock_rate': str(lapse),
                    'coordinate_acceleration_connection': str(rindler_g[1][0][0]),
                    'riemann_nonzero_entries': 0, 'ricci_scalar': str(rindler_scalar)},
        'same_rest_clock_control': {
            'flat_rate': '1', 'de_sitter_rate': '1',
            'flat_ricci_scalar': str(flat_scalar), 'de_sitter_ricci_scalar': str(curved_scalar),
            'de_sitter_tidal_R_x_t_x_t': str(curved_r[1, 0, 1, 0]),
            'interpretation': 'de Sitter is a kinematic/Einstein-Lambda oracle, not a current Universe24 solution'},
        'tomography': {'input_metric': [[str(v) for v in row] for row in metric],
                       'recovered_metric': [[str(v) for v in row] for row in recovered],
                       'samples': sampled, 'held_out': held_out,
                       'apparatus_status': 'not_tested: samples call the passive readout'},
        'physical_gates': {'operational_clock': 'not_tested', 'engine_geodesics': 'not_tested',
                           'einstein_limit': 'not_tested'},
    }
    root = Path(__file__).resolve().parents[2]
    files = [Path(__file__).resolve(), root/'universe24/observe/metric_clocks.py']
    result['source_sha256'] = {str(p.relative_to(root)): sha256(p.read_bytes()).hexdigest() for p in files}
    return result


if __name__ == '__main__':
    result = audit()
    out = Path('runs/einstein-node/clock_geometry.json')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'checks': result['checks'], 'evidence': str(out)}, indent=2))
