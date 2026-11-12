"""Exact carry-aware continuity and a spatial Einstein counterexample.

The face-interaction law is a separately identified arithmetic control, not an
extension or physical certification of the shared Bianchi-I source tensor.
Run: python -m validation.conservation_closure.noether_spatial
"""
from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path

import numpy as np
import sympy as sp

from universe24.core import Engine, State, Tensor, check_reciprocity
from universe24.core.lattice import lattice
from universe24.system.bundle import canonical_bytes
from validation.generic_structure.interactions import (
    AXES, PotentialTerm, Variable, compile_potential, potential_value,
)
from validation.generic_structure.native_schedule import scalar_step
from . import common

ROOT = Path(__file__).resolve().parents[2]


def complete_charge(state):
    """An exact arithmetic momentum; not an assumed physical stress tensor."""
    return 6*(state.b.astype(object)-state.a.astype(object))+state.r


def charge_identity():
    a, b, r, u, rp = sp.symbols('a b r u rp')
    bp = (2*u+r-rp)/6-a
    residual = sp.expand(6*(bp-b)+rp-(6*(b-a)+r)-2*(u-6*b))
    assert residual == 0
    # No divisibility assumption is used: rp is the actual retained divmod
    # remainder, and this identity holds for arbitrary integer tensor input.
    checks = 0
    for aa in range(-2, 3):
        for bb in range(-2, 3):
            for rr in range(6):
                for uu in range(-13, 14):
                    ell, rn = divmod(2*uu+rr, 6)
                    assert 6*(ell-aa-bb)+rn-(6*(bb-aa)+rr) == 2*(uu-6*bb)
                    checks += 1
    return {'status': 'passed', 'symbolic_residual': str(residual),
            'all_remainder_signed_integer_checks': checks,
            'identity': 'Delta[6*(b-a)+r]=2*(u-6*b)',
            'covector_charge_condition':
                'For u_g=6*b_g+s_g*dPhi/db_g and a constant shift vector c, '
                'sum_x,g c_g*s_g*[6*(b_g-a_g)+r_g] is conserved if '
                'sum_x,g c_g*dPhi/db_g=0.'}


def face_interaction():
    """Phi=-sum_edges (g_tail+g_head)*(phi_head-phi_tail)^2."""
    phi, g = Variable('phi'), Variable('g')
    potential = []
    for edge in AXES:
        q, h = Variable('phi', edge), Variable('g', edge)
        for stiffness in (g, h):
            potential.extend(PotentialTerm(coefficient, (stiffness,)+pair)
                             for coefficient, pair in
                             ((-1, (q, q)), (2, (phi, q)), (-1, (phi, phi))))
    return compile_potential(['phi', 'g'], potential)


def incidence_operators(L):
    """Integer oriented incidence; audit arrays are not retained Engine state."""
    lat = lattice(L)
    edges = [(node, axis) for node in range(lat.N) for axis in range(3)]
    edge_index = {edge: i for i, edge in enumerate(edges)}
    boundary1 = np.zeros((lat.N, len(edges)), dtype=object)
    for column, (node, axis) in enumerate(edges):
        boundary1[node, column] = -1
        boundary1[lat.neighbour(node, 2*axis), column] = 1
    faces = [(node, i, j) for node in range(lat.N)
             for i, j in ((0, 1), (0, 2), (1, 2))]
    boundary2 = np.zeros((len(edges), len(faces)), dtype=object)
    for column, (node, i, j) in enumerate(faces):
        ni, nj = lat.neighbour(node, 2*i), lat.neighbour(node, 2*j)
        for edge, sign in (((node, i), 1), ((ni, j), 1),
                           ((nj, i), -1), ((node, j), -1)):
            boundary2[edge_index[edge], column] += sign
    assert not np.any(boundary1.dot(boundary2))
    return lat, edges, boundary1, boundary2


def edge_oracle(field, lat, edges):
    """Differentiate each undirected positive face once, independently."""
    force = np.zeros(field.shape, dtype=object)
    flux = np.zeros(len(edges), dtype=object)
    for index, (tail, axis) in enumerate(edges):
        head = lat.neighbour(tail, 2*axis)
        delta = int(field[0, head])-int(field[0, tail])
        stiffness = int(field[1, head])+int(field[1, tail])
        edge_response = 2*stiffness*delta
        force[0, tail] += edge_response
        force[0, head] -= edge_response
        force[1, tail] -= delta*delta
        force[1, head] -= delta*delta
        # boundary1 has -1 at tail,+1 at head, hence Delta pi=-boundary1 J.
        flux[index] = 2*edge_response
    return force, flux


def face_audit(steps=4):
    compiled = face_interaction()
    law = compiled.tensor
    lat, edges, boundary1, boundary2 = incidence_operators(3)
    a = np.array([[(node+2*g) % 5-2 for node in range(lat.N)] for g in range(2)], dtype=object)
    b = np.array([[(2*node+g) % 7-3 for node in range(lat.N)] for g in range(2)], dtype=object)
    r = np.array([[(node+g) % 6 for node in range(lat.N)] for g in range(2)], dtype=object)
    seed = State(3, a, b, r)
    state, engine = seed, Engine(law)
    initial_total = int(sum(complete_charge(seed)[0]))
    rows, changed_carries = [], False
    for step in range(steps):
        force, flux = edge_oracle(state.b, lat, edges)
        assert np.array_equal(engine.inputs(state), 6*state.b.astype(object)+force)
        after = engine.step(state)
        assert after.same_as(scalar_step(state, law))
        assert engine.inverse_step(after).same_as(state)
        change = complete_charge(after)-complete_charge(state)
        assert np.array_equal(change, 2*force)
        assert np.array_equal(change[0], -boundary1.dot(flux))
        assert int(sum(complete_charge(after)[0])) == initial_total
        assert not np.any(boundary2.T.dot(boundary1.T.dot(state.b[0].astype(object))))
        assert np.any(flux) and np.any(change[0])
        changed_carries |= not np.array_equal(after.r, state.r)
        rows.append({'tick': step+1, 'total_complete_phi_charge': initial_total,
                     'charge_omitting_remainders': int(sum(6*(after.b[0].astype(object)-after.a[0]))),
                     'sum_phi_remainders': int(sum(after.r[0])),
                     'max_abs_edge_current': max(abs(int(x)) for x in flux),
                     'nodes_with_nonzero_charge_change': int(np.count_nonzero(change[0])),
                     'official_arithmetic_clicks': len(engine.clicks(state, after, step+1)),
                     'max_retained_bits': common.complete_bits(after),
                     'potential_value': str(potential_value(compiled, after.b, 3))})
        state = after
    assert engine.rewind(state, steps).same_as(seed)
    assert changed_carries
    initial_without = int(sum(6*(seed.b[0].astype(object)-seed.a[0])))
    assert any(row['charge_omitting_remainders'] != initial_without for row in rows)

    # Erasing the reaction on g preserves this phi charge, but is no longer
    # the gradient of the one declared reciprocal potential.
    bad_terms = [m for m in law.monomials if m.target == 0]
    bad_terms.append(('g', 6, (('g', (0, 0, 0), 'b'),)))
    bad = Tensor(law.gears, bad_terms, strict_support=True)
    reciprocity = check_reciprocity(bad)
    assert not reciprocity.ok
    bad_engine = Engine(bad)
    bad_after = bad_engine.step(seed)
    assert bad_engine.inverse_step(bad_after).same_as(seed)
    assert int(sum(complete_charge(bad_after)[0])) == initial_total
    expected_g = 2*edge_oracle(seed.b, lat, edges)[0][1]
    assert not np.array_equal((complete_charge(bad_after)-complete_charge(seed))[1], expected_g)
    return {'status': 'passed', 'scope': 'separate reciprocal arithmetic face law, not sourced Einstein',
            'sourced_claim': False,
            'tensor_sha256': law.fingerprint,
            'seed_sha256': sha256(canonical_bytes(seed.to_dict())).hexdigest(),
            'channels': law.G, 'retained_integers_per_node': 3*law.G,
            'nodes': lat.N, 'face_edges': len(edges), 'degree': law.rank-1,
            'strict_single_face_support': not law.support_violations(),
            'all_six_carry_classes': True, 'carries_actually_change': changed_carries,
            'scalar_oracle_and_all_inverses': True, 'complete_rewind': True,
            'independent_edge_derivative_and_local_continuity': True,
            'boundary_squared_zero_and_curl_gradient_zero': True,
            'initial_complete_charge': initial_total,
            'initial_charge_without_remainders': initial_without, 'rows': rows,
            'removed_reaction_control': {'tensor_sha256': bad.fingerprint,
                'still_exactly_reversible': True, 'still_preserves_phi_charge': True,
                'reciprocity': 'failed_as_expected', 'reciprocal_g_response': 'failed_as_expected'},
            'physical_energy_conservation': 'not_established',
            'stable_continuum_limit': 'not_established',
            'note': 'Incidence matrices and edge currents are passive audit values; no retained link bank was added.'}


def spatial_obstruction():
    """Pointwise Friedmann identity does not supply spatial momentum constraints."""
    x = sp.symbols('x', real=True)
    denominator = x*x+x+1
    shear = ((x*x-1)/denominator, -x*(x+2)/denominator, (2*x+1)/denominator)
    assert sp.simplify(sum(shear)) == 0
    assert sp.simplify(sum(s*s for s in shear)-2) == 0
    V, U, D, P = sp.Rational(7, 3), sp.Integer(4), sp.Integer(1), sp.Integer(2)
    constraint_residual = sp.simplify(U*U-3*D*V-sp.Rational(3, 2)*(P*P+sum(s*s for s in shear)))
    momentum_x = sp.simplify(sp.diff(2*U/(3*V)-shear[0]/V, x))
    assert constraint_residual == 0 and momentum_x.subs(x, 0) == -sp.Rational(3, 7)

    program, seed = common.build(24), common.prepare(common.build(24))
    a, b, r = (array.astype(object).copy() for array in (seed.a, seed.b, seed.r))
    patterns = ((-1, 0, 1), (0, -1, 1), (1, -1, 0))
    for node in range(seed.N):
        sx, sy, _ = patterns[seed.lattice.coords(node)[0]]
        for array in (a, b):
            array[6, node], array[7, node] = sx, sy
    varied = State(3, a, b, r)
    try:
        common.read_conserved(program, varied)
    except ValueError as error:
        rejection = str(error)
    else:
        raise AssertionError('a spatially varying seed entered the homogeneous physical domain')
    engine, state, q_checks = Engine(program.tensor), varied, 0
    for tick in range(4):
        for node in range(state.N):
            W, dust, scalar = (int(state.b[g, node]) for g in (0, 1, 2))
            s1, s2 = (int(state.b[g, node]) for g in (6, 7))
            J = W-int(state.a[0, node])+3*dust
            invariant = J*J-12*dust*W-24*program.N**2*(scalar*scalar+s1*s1+s2*s2+(s1+s2)**2)
            assert invariant == 0
            q_checks += 1
        if tick < 3:
            after = engine.step(state)
            assert after.same_as(common.scalar_step(state))
            assert engine.inverse_step(after).same_as(state)
            state = after
    assert engine.rewind(state, 3).same_as(varied)
    centered = []
    for node in range(varied.N):
        right, left = varied.lattice.neighbour(node, 0), varied.lattice.neighbour(node, 1)
        derivative = F(int(varied.b[6, right])-int(varied.b[6, left]), 2)
        centered.append(-derivative/F(7, 3))
    expected = {F(3, 14), -F(3, 7)}
    assert set(centered) == expected
    return {'status': 'passed_negative_control',
            **common.identity(program, seed),
            'negative_seed_sha256': sha256(canonical_bytes(varied.to_dict())).hexdigest(),
            'tensor_is_the_shared_Bianchi_tensor': True,
            'homogeneous_physical_reader_rejection': rejection,
            'actual_onsite_Q_zero_checks': q_checks, 'executed_steps': 3,
            'scalar_oracle_and_complete_rewind': True,
            'initial_metric': 'spatially constant V^(2/3)*delta_ij; retained I=0',
            'initial_scalar_gradient_and_matter_momentum': 'zero',
            'smooth_shear_family': [str(s) for s in shear],
            'smooth_pointwise_Q': str(constraint_residual),
            'smooth_momentum_x_at_x0': str(momentum_x.subs(x, 0)),
            'centered_unit_grid_momentum_values': sorted(str(v) for v in expected),
            'spatial_Einstein_acceptance': 'failed',
            'limitation': 'The smooth initial-data counterexample is exact; the lattice values are a stated centered-difference diagnostic, not a new accepted discrete ADM formulation.'}


def bianchi_charge_connection():
    """Apply the generic complete-state identity to the primary source law."""
    data = common.trace(24)
    states = data['states']
    checks = 0
    for before, after in zip(states, states[1:]):
        change = complete_charge(after)-complete_charge(before)
        for node in range(before.N):
            D = int(before.b[1, node])
            J = int(before.b[0, node])-int(before.a[0, node])+3*D
            assert int(complete_charge(before)[0, node]) == 6*J-18*D+int(before.r[0, node])
            assert int(change[0, node]) == 36*D
            assert all(int(change[g, node]) == 0 for g in range(1, before.G))
            checks += before.G
    return {'status': 'passed', **common.identity(data['program'], data['seed']),
            'same_state_generic_identity_checks': checks,
            'volume_complete_charge': 'pi_W=6*J-18*D+r_W',
            'volume_charge_increment': 'Delta pi_W=36*D',
            'other_complete_charge_increments': 'zero',
            'interpretation': 'The source law has an exact balance law, not conservation of volume momentum. Its physical P,D,S and quadratic constraint remain separate identified invariants.'}


def main():
    result = {'schema': 'universe24/conservation-closure/noether-spatial/1',
              'carry_identity': charge_identity(), 'face_continuity': face_audit(),
              'same_candidate_balance': bianchi_charge_connection(),
              'same_tensor_spatial_negative': spatial_obstruction(),
              'sources': [
                  'https://arxiv.org/pdf/math/9807080#page=32',
                  'https://thesis.caltech.edu/1885/03/thesis_hirani.pdf#page=46',
                  'https://people-lux.obspm.fr/gourgoulhon/pdf/form3p1.pdf#page=177'],
              'verdict': 'Exact local charge transport and exact homogeneous source invariants do not jointly establish a spatial Einstein system.'}
    sources = [Path(__file__), Path(common.__file__),
               ROOT/'validation/generic_structure/interactions.py',
               ROOT/'validation/generic_structure/native_schedule.py']
    result['source_sha256'] = {str(path.relative_to(ROOT)): sha256(path.read_bytes()).hexdigest()
                               for path in sources}
    output = ROOT/'runs/conservation_closure/noether_spatial.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'carry_identity': result['carry_identity']['status'],
                      'face_channels': result['face_continuity']['channels'],
                      'face_charge': result['face_continuity']['initial_complete_charge'],
                      'spatial_momentum_residual': result['same_tensor_spatial_negative']['smooth_momentum_x_at_x0'],
                      'spatial_Einstein_acceptance': 'failed_as_expected'}, indent=2))


if __name__ == '__main__':
    main()
