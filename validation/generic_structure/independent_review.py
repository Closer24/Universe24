"""Cross-module review controls; no production changes or physics promotion.

Run: python -m validation.generic_structure.independent_review
"""
from fractions import Fraction as F
from dataclasses import replace
from hashlib import sha256
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp

from universe24.core import Engine, GearType, State
from universe24.core.lattice import lattice
from validation.generic_structure import constraint_certificate as constraints
from validation.generic_structure import frame_primitive as frame
from validation.generic_structure import interactions
from validation.generic_structure import native_schedule as native
from validation.generic_structure import packet_clock as packet
from validation.generic_structure import symmetry_sector as sectors

ROOT = Path(__file__).resolve().parents[2]


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def rejected(callback):
    try:
        callback()
    except (ValueError, TypeError, AssertionError):
        return True
    raise AssertionError('An invalid review control was accepted')


def signed_face_potential():
    """Different potential, negative field sign, y-face and signed rank-one drift."""
    V, T = interactions.Variable, interactions.PotentialTerm
    x, yn = V('x'), V('y', (0, 1, 0))
    potential = [T(F(-3, 2), (x, x)), T(2, (x, yn, yn))]
    compiled = interactions.compile_potential(
        [GearType('x'), GearType('y', sign=-1,
          sign_why='Independent signed-gradient compiler control; no physical energy identification.')],
        potential, add_inertial=False)
    force_terms = native.interaction_force_terms(compiled)
    law, certificate = native.compile_schedule(2, [[2, -1]], [[1], [-2]], force_terms)
    a, b, r = (np.zeros((law.G, 27), dtype=object) for _ in range(3))
    for g in range(2):
        for node in range(27):
            a[g, node] = (node + 2*g) % 5 - 2
            b[g, node] = (2*node + g) % 5 - 2
    for g in range(law.G):
        r[g] = [(g+node) % 6 for node in range(27)]
    seed = State(3, a, b, r)
    engine, state, lat = Engine(law), seed.copy(), lattice(3)
    comparisons = 0
    for period in range(3):
        old = state.copy()
        # Independent target construction from the declared potential, with
        # no call to the schedule's force evaluator or macro oracle.
        position = old.a[:2].astype(object)+old.b[:2].astype(object)
        quotient = (4*old.a[0].astype(object)-2*old.a[1].astype(object)+old.r[2])//6
        drifted = position.copy()
        drifted[0] += quotient
        drifted[1] -= 2*quotient
        force = np.empty((2, 27), dtype=object)
        for node in range(27):
            px, py, pz = lat.coords(node)
            plus, minus = lat.index(px, py+1, pz), lat.index(px, py-1, pz)
            force[0, node] = -3*drifted[0, node]+2*drifted[1, plus]**2
            force[1, node] = -4*drifted[0, minus]*drifted[1, node]
        momentum = 6*old.a[:2].astype(object)+old.r[:2]+2*force
        aa, bb, rr = (values.astype(object).copy() for values in (old.a, old.b, old.r))
        aa[:2], bb[:2], rr[:2] = momentum//6, drifted-momentum//6, momentum % 6
        expected = State(3, aa, bb, rr)
        state = engine.run(state, 9)
        require(state.same_as(expected), f'Signed cross-module macro mismatch at period {period}')
        require(engine.rewind(state, 9).same_as(old), 'Signed cross-module inverse mismatch')
        comparisons += 3*state.G*state.N
    require(engine.rewind(state, 27).same_as(seed), 'Signed cross-module complete rewind')
    return {'status': 'passed', 'channels': law.G, 'periods': 3,
            'complete_integer_comparisons': comparisons,
            'potential': '-3*x_i^2/2 + 2*x_i*y_(i+ey)^2, summed over nodes',
            'field_signs': [1, -1], 'read_matrix': [[2, -1]], 'copy_matrix': [[1], [-2]],
            'all_six_carries': True, 'face_direction': 'y, including periodic seams',
            'tensor_fingerprint': certificate['tensor_fingerprint'],
            'full_rewind': True}


def quotient_factorization_counterexample():
    """BA=I is necessary, but floors do not commute with a basis change."""
    A, B = [[1, 1], [0, 1]], [[1, -1], [0, 1]]
    require(sp.Matrix(B)*sp.Matrix(A) == sp.eye(2), 'Factorization fixture')
    law, certificate = native.compile_schedule(2, A, B)
    a, b, r = (np.zeros((law.G, 27), dtype=object) for _ in range(3))
    a[0], a[1] = 1, 2
    seed = State(3, a, b, r)
    engine = Engine(law)
    after = engine.run(seed, 9)
    drift = after.a[:2]+after.b[:2]-seed.a[:2]-seed.b[:2]
    require(np.all(drift[0] == 1) and np.all(drift[1] == 0), 'Floor-factorization witness')
    require(certificate['independent_quotient_necessary_matrix_condition'], 'Necessary condition absent')
    require(not certificate['independent_componentwise_quotient_certified'], 'Unjustified sufficient condition')
    require(engine.rewind(after, 9).same_as(seed), 'Counterexample rewind')
    override_rejected = rejected(lambda: native.compile_schedule(2, A, B, budget=91))
    return {'status': 'expected_failure_reproduced', 'BA': 'I_2',
            'old_a': [1, 2], 'workspace_carries': [0, 0],
            'actual_drift': [1, 0], 'independent_floor_a_over_3_drift': [0, 0],
            'complete_rewind': True, 'hard_cap_override_rejected': override_rejected,
            'scope': 'Specific n+r+3 compiler layout; no universal channel lower bound'}


def forged_force_certificate():
    x = interactions.Variable('x')
    compiled = interactions.compile_potential(
        ['x'], [interactions.PotentialTerm(F(-1, 2), (x, x))])
    # Keep a genuine tensor and its matching fingerprint, changing only the
    # claimed semantics. Fingerprint equality cannot detect this forgery.
    certificate = dict(compiled.certificate)
    certificate['response'] = 'u_i=sign_i*dPhi/db_i'
    forged = replace(compiled, certificate=certificate)
    require(forged.tensor.fingerprint == certificate['tensor_fingerprint'], 'Forged fixture hash')
    rejected(lambda: native.interaction_force_terms(forged))
    return {'status': 'rejected',
            'forgery': 'Relabel genuine inertial-plus-force tensor as pure gradient while preserving matching tensor hash',
            'required_authority': 'Recomputed gradient from actual declared potential and gear signs'}


def constraint_history_counterexample():
    law = constraints.build('cubic_null_rotation')
    values = np.array([[1]*27, [0]*27, [0]*27], dtype=object)
    seed = State(3, values.copy(), values.copy(), np.zeros_like(values))
    engine = Engine(law)
    after = engine.step(seed)
    old_Q = constraints.quadratic('cubic_null_rotation', seed.b[:, 0])
    next_Q = constraints.quadratic('cubic_null_rotation', after.b[:, 0])
    require(old_Q == 0 and next_Q == -8, 'Cubic null incompatible-history witness')
    require(engine.inverse_step(after).same_as(seed), 'Cubic null witness inverse')
    certificates = {kind: constraints.symbolic_certificate(kind)
                    for kind in ('linear_lorentz', 'cubic_null_rotation')}
    return {'status': 'passed_with_expected_failure', 'positive_symbolic_certificates': certificates,
            'unprepared_cubic_null': {'Q_old_a': 0, 'Q_old_b': 0, 'Q_next_b': -8,
                                    'complete_inverse': True},
            'interpretation': 'Separate constraints on two slices do not replace their encoding relation'}


def exact_sector_review():
    sector = sectors.common45_sector()
    seed = sectors.seed_from_rows(sector, [3, -2, 4, 1, -3, 2], [4, 1, -2, 3, 2, -1])
    full = sector.embed(seed)
    big, small = Engine(sector.full), Engine(sector.reduced)
    require(sector.project(full).same_as(seed), 'Projection not inverse on image')
    require(big.inverse_step(full).same_as(sector.embed(small.inverse_step(seed))), 'Reverse conjugacy')
    require(big.step(full).same_as(sector.embed(small.step(seed))), 'Forward conjugacy')
    bad_carries = []
    for carry in (-1, 6):
        bad = seed.copy()
        bad.r = bad.r.astype(object)
        bad.r[0, 0] = carry
        rejected(lambda: sector.embed(bad))
        bad_carries.append(carry)
    physical = sectors.seed_from_rows(sector, [0]*6, [4, 4, -4, 8, 0, 4])
    require(sectors.physical_constraint(physical) == 0, 'Physical source fixture')
    defect = sectors.physical_constraint(small.step(physical))
    require(defect == F(-7, 4096), 'Reduced lab lost physical failure')
    return {'status': 'passed', 'full_channels': 45, 'restricted_channels': 6,
            'full_histories_and_carries': True, 'forward_and_reverse_conjugacy': True,
            'illegal_carries_rejected': bad_carries, 'preserved_constraint_defect': str(defect),
            'generic_45channel_compression': False}


def packet_review():
    # Independent centered numerical derivative of the scalar dispersion,
    # compared to the implementation's group-velocity expression.
    k, delta = math.pi/7, 1e-4
    frequency = lambda q: math.asin(math.sqrt(4*math.sin(q)**2+1)/6)
    derivative = (frequency(k-2*delta)-8*frequency(k-delta)
                  +8*frequency(k+delta)-frequency(k+2*delta))/(12*delta)
    _, velocity, _ = packet.spectrum(k)
    require(abs(derivative-velocity) < 1e-10, 'Independent spectral group derivative')
    result = packet.run_packet(L=24, carrier=4, axis=2, steps=24)
    require(result['packet_is_localized_along_one_axis_only'], 'Packet scope missing')
    require(not result['same_law_as_common45'], 'Separate wave law promoted')
    return {'status': 'passed', 'independent_group_derivative_error': abs(derivative-velocity),
            'actual_packet_control': result,
            'scope': 'One-axis localization on a three-dimensional lattice; fixed discrete mass/spacing, no curved common45 claim'}


def frame_review():
    symbolic = frame.symbolic()
    negatives = frame.negatives()
    actual = frame.actual(steps=3)
    return {'status': 'passed', 'symbolic': symbolic, 'negative_controls': negatives,
            'channels': actual['channels'], 'scalar_comparisons': actual['scalar_oracle_comparisons'],
            'full_rewind': actual['complete_step_inverse_and_rewind'],
            'scope': 'Prepared onsite frame shears; determinant and metric domain only'}


def audit():
    result = {'schema': 'universe24/generic-structure/independent-review/1',
              'baseline_pin': '8c53e69f4b466dcbd2da7dab7e3c365bd9731766',
              'signed_potential_to_native_schedule': signed_face_potential(),
              'forged_force_certificate': forged_force_certificate(),
              'matrix_factorization_is_not_floor_factorization': quotient_factorization_counterexample(),
              'complete_history_constraint': constraint_history_counterexample(),
              'exact_restricted_sector': exact_sector_review(),
              'packet': packet_review(), 'frame_domain': frame_review(),
              'production_changes': False, 'physical_acceptance': 'not_established'}
    paths = sorted((ROOT/'validation/generic_structure').glob('*.py'))
    result['source_sha256'] = {str(path.relative_to(ROOT)): sha256(path.read_bytes()).hexdigest()
                              for path in paths}
    return result


if __name__ == '__main__':
    result = audit()
    destination = ROOT/'runs/generic-structure/independent_review.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': 'passed_with_explicit_counterexamples',
                      'evidence': str(destination.relative_to(ROOT)),
                      'physical_acceptance': result['physical_acceptance']}, indent=2))
