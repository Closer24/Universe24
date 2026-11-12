"""Independent clock-geometry review and a deliberately nonmetric impostor.

This is a source-only oracle. It does not generate retained apparatus or advance
an Engine state. Run: python -m validation.einstein_node_audit.independent_review
"""
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path

import sympy as s

from validation.einstein_node_audit.clock_geometry import curvature, metric_from_rates


def audit():
    a, x, t = s.symbols('a x t', nonzero=True, real=True)
    y, z, h = s.symbols('y z H', real=True)
    coordinates = (t, x, y, z)
    # Independent coordinate pullback: no connection or Riemann routine enters
    # this verification that the Rindler metric is flat on its stated chart.
    inertial_coordinates = s.Matrix([(x+1/a)*s.sinh(a*t),
                                    (x+1/a)*s.cosh(a*t), y, z])
    jacobian = inertial_coordinates.jacobian(coordinates)
    pulled_back = (jacobian.T*s.diag(-1, 1, 1, 1)*jacobian).applyfunc(s.simplify)
    assert pulled_back == s.diag(-(1+a*x)**2, 1, 1, 1)

    # Compare every component against the independently specified constant-
    # curvature identity, rather than accepting only its scalar contraction.
    metric = s.diag(-1, *([s.exp(2*h*t)]*3))
    _, riemann, _, _ = curvature(metric, coordinates)
    for aa in range(4):
        for bb in range(4):
            for cc in range(4):
                for dd in range(4):
                    expected = h*h*((1 if aa == cc else 0)*metric[bb, dd]
                                    -(1 if aa == dd else 0)*metric[bb, cc])
                    assert s.simplify(riemann[aa, bb, cc, dd]-expected) == 0

    epsilon = F(1, 10)
    velocities = [(F(0),)*3]
    for i in range(3):
        for sign in (-1, 1):
            velocity = [F(0)]*3
            velocity[i] = sign*epsilon
            velocities.append(tuple(velocity))
    for i in range(3):
        for j in range(i+1, 3):
            velocity = [F(0)]*3
            velocity[i] = velocity[j] = epsilon
            velocities.append(tuple(velocity))
    design = s.Matrix([[1, *v, *(value*value for value in v),
                        v[0]*v[1], v[0]*v[2], v[1]*v[2]] for v in velocities])
    assert design.rank() == 10
    assert design[:1, :].rank() == 1
    assert all(design[:row, :].col_join(design[row+1:, :]).rank() == 9
               for row in range(10))

    # Independent quadratic contraction; includes non-Lorentzian matrices to
    # verify algebra only. Physical clock interpretation is not asserted here.
    for seed in range(20):
        candidate = [[F(0)]*4 for _ in range(4)]
        for i in range(4):
            for j in range(i, 4):
                candidate[i][j] = candidate[j][i] = F((seed+1)*(i+1)-(j+1), i+j+1)

        def independent_readout(velocity):
            tangent = [F(1), *velocity]
            return -sum(candidate[i][j]*tangent[i]*tangent[j]
                        for i in range(4) for j in range(4))

        assert metric_from_rates(independent_readout) == candidate

    # Falsifier: ten exact rate measurements fit a quadratic form but do not
    # prove that an arbitrary physical mechanism obeys a metric clock law.
    flat = [[-F(1), 0, 0, 0], [0, F(1), 0, 0],
            [0, 0, F(1), 0], [0, 0, 0, F(1)]]

    def nonmetric_readout(velocity):
        vx = velocity[0]
        return 1-sum(value*value for value in velocity)+vx*(vx*vx-epsilon*epsilon)

    for velocity in velocities:
        assert nonmetric_readout(velocity) == 1-sum(value*value for value in velocity)
        assert nonmetric_readout(velocity) > 0
    assert metric_from_rates(nonmetric_readout) == flat
    held_out = (F(1, 8), F(0), F(0))
    predicted = 1-sum(value*value for value in held_out)
    actual = nonmetric_readout(held_out)
    assert actual > 0 and predicted > 0 and actual != predicted
    result = {
        'schema': 'universe24/einstein-node/independent-review/1',
        'checks': {
            'rindler_flatness_independent_coordinate_pullback': 'passed',
            'de_sitter_all_256_constant_curvature_components': 'passed',
            'ten_velocity_design_rank_10': 'passed',
            'stationary_design_rank_1': 'passed',
            'every_missing_sample_rank_9': 'passed',
            'twenty_exact_symmetric_metric_reconstructions': 'passed',
            'nonmetric_impostor_fits_ten_samples': 'passed_negative_control',
            'held_out_velocity_rejects_impostor': 'passed',
        },
        'negative_control': {
            'added_nonmetric_term': 'v_x (v_x^2 - epsilon^2)',
            'epsilon': str(epsilon),
            'held_out_velocity': list(map(str, held_out)),
            'metric_prediction_squared_rate': str(predicted),
            'nonmetric_squared_rate': str(actual),
            'difference': str(actual-predicted),
        },
        'scope': 'Algebraic identifiability assumes a quadratic clock law in a known chart; it is not evidence for an operational material clock.',
        'physical_acceptance': 'not_established',
    }
    root = Path(__file__).resolve().parents[2]
    paths = [Path(__file__).resolve(), Path(__file__).with_name('clock_geometry.py')]
    result['source_sha256'] = {str(path.relative_to(root)): sha256(path.read_bytes()).hexdigest()
                              for path in paths}
    return result


if __name__ == '__main__':
    result = audit()
    destination = Path('runs/einstein-node/08_independent_review.json')
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'checks': result['checks'], 'evidence': str(destination)}, indent=2))
