"""Prepare massive corrected45 inputs and inspect one unified saved run.

All evolution uses universe24.system.runtime.run_bundle. Fractions and floats
below are passive diagnostics, never inputs to an evolution callback. This
finite homogeneous fixture is not an accepted general Einstein model.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import gzip
import hashlib
import importlib
import json
from pathlib import Path

import numpy as np
import sympy as sp

from universe24.core import exact_json
from universe24.core.lattice import lattice
from universe24.system.bundle import create_bundle, state_from_data
from universe24.system.decoder import default_protocol
from universe24.system.runtime import run_bundle, verify_run
from validation.geometry.team48 import matter_dust_square
from validation.geometry.team48 import refinement_integer_projective as projective
from .geodesics import build_geodesics
from .board import render_board

ROOT = Path(__file__).resolve().parents[2]
SYMBOL = importlib.import_module('validation.research_eight.07_hyperbolic_symbol')
SCHEMA = 'universe24/geodesic-board/1'


def build_program(dt=F(1, 32), dx=F(1, 4), mass_squared=1):
    """One corrected full-frame law, with mass explicit in its fingerprint."""
    if type(mass_squared) is not int or mass_squared < 0:
        raise ValueError('mass_squared must be a nonnegative integer')
    for value in (dt, dx):
        if isinstance(value, (float, bool, np.floating, np.bool_)):
            raise TypeError('Step and spacing must be exact positive rational values')
        if F(value) <= 0:
            raise ValueError('Step and spacing must be positive')

    def equations(fields, partial):
        return SYMBOL.corrected_charged(fields, partial, mass_squared=mass_squared)

    return projective.compile_projective(matter_dust_square.FIELDS_CHARGED,
                                         equations, dt=dt, dx=dx, degree=2)


def prepare_seed(program, L=3, denominator=32):
    """Massive constrained slice: rho=3, K=-I, B=I, phi=2, dust=1.

    The old a bank is a zero encoding-memory boundary, not an earlier metric.
    Every remainder class occurs. The seed solves the massive m²=1 slice,
    not arbitrary choices of the compiler's mass parameter.
    """
    values = np.zeros((len(program.fields), lattice(L).N), dtype=object)
    for i, name in enumerate(program.fields):
        if name.startswith('B'):
            values[i, :] = int(name[1] == name[2])
        elif name.startswith('K'):
            values[i, :] = -int(name[1] == name[2])
        elif name == 'phi':
            values[i, :] = 2
        elif name == 'dust_amplitude':
            values[i, :] = 1
    carry = np.array([[(g+n) % 6 for n in range(lattice(L).N)]
                      for g in range(program.tensor.G)], dtype=object)
    return projective.prepare(program, values, L=L, denominator=denominator,
                              remainders=carry)


def fields_readout(program, state):
    return projective.readout(program, state)


def channel_manifest(program):
    rows = []
    for i, name in enumerate(program.tensor.names):
        field = name.removeprefix('projective.')
        if i == 0:
            owner = 'geometry.projective_encoding'
        elif field.startswith(('B', 'K', 'G')):
            owner = 'geometry.shared_frame'
        elif field == 'dust_amplitude':
            owner = 'matter.normal_dust'
        elif field.startswith(('E', 'M', 'A')):
            owner = 'matter.electromagnetic'
        else:
            owner = 'matter.charged_scalar'
        rows.append({'index': i, 'name': name, 'owner': owner,
                     'purpose': 'Retained projective numerator '+field if i else
                                'Common denominator and reversible encoding memory',
                     'label': program.tensor.labels[i],
                     'retained_registers': ['a', 'b', 'r'],
                     'readout_dependencies': list(dict.fromkeys([program.tensor.names[0], name]))})
    assert len(rows) == 45
    return rows


def read_snapshot(program, state, step, *, mass_squared=1):
    """Exact field diagnostics and floating display values from saved state."""
    values = fields_readout(program, state)
    index = {name: i for i, name in enumerate(program.fields)}
    lat = lattice(state.L)
    rows = []
    for node in range(state.N):
        fields = {name: values[i, node] for name, i in index.items()}

        def partial(name, axis):
            return (values[index[name], lat.neighbour(node, 2*axis)]
                    - values[index[name], lat.neighbour(node, 2*axis+1)])/(2*program.dx)

        _, constraints, diagnostic = SYMBOL.corrected_charged(
            fields, partial, mass_squared=mass_squared)
        B = sp.Matrix([[fields[f'B{a}{i}'] for i in range(3)] for a in range(3)])
        inverse = B.T*B
        if inverse.det() == 0:
            raise ValueError('Degenerate metric: refusing to invent a geodesic display')
        gamma = inverse.inv()
        positive = all(gamma[:k, :k].det() > 0 for k in (1, 2, 3))
        if not positive:
            raise ValueError('Non-positive spatial metric: readout domain failed')
        as_float = lambda matrix: [[float(v) for v in row] for row in matrix.tolist()]
        rho, dust = diagnostic['rho'], diagnostic['dust_density']
        rows.append({'node': node, 'position': [float(program.dx*x) for x in lat.coords(node)],
                     'B': as_float(B), 'gamma': as_float(gamma), 'gamma_inverse': as_float(inverse),
                     'gamma_exact': [[str(v) for v in row] for row in gamma.tolist()],
                     'K': [[float(fields[f'K{min(a,b)}{max(a,b)}']) for b in range(3)] for a in range(3)],
                     'rho': float(rho), 'dust_density': float(dust),
                     'scalar_energy': float(rho-dust-diagnostic['rho_maxwell']),
                     'electric_charge': float(diagnostic['electric_charge']),
                     'stress': [[float(v) for v in row] for row in diagnostic['stress']],
                     'constraints': {name: float(value) for name, value in constraints.items()},
                     'constraints_exact': {name: str(value) for name, value in constraints.items()},
                     'fields_exact': {name: str(value) for name, value in fields.items()},
                     'metric_positive': bool(positive)})
    homogeneous = all(row['fields_exact'] == rows[0]['fields_exact'] for row in rows)
    first = rows[0]
    return {'step': step, 'time': float(step*program.dt), 'time_exact': str(step*program.dt),
            'homogeneous': homogeneous, 'gamma': first['gamma'],
            'energy_density': first['rho'], 'dust_density': first['dust_density'],
            'charge': first['electric_charge'], 'hamiltonian_constraint': first['constraints']['H'],
            'nodes': rows}


def run(out, *, steps=4, dt=F(1, 32), dx=F(1, 4)):
    if type(steps) is not int or not 1 <= steps <= 8:
        raise ValueError('This finite fixture permits 1..8 updates; no unbounded cost claim')
    out = Path(out)
    if out.exists() and any(out.iterdir()):
        raise ValueError('Evidence output must be new or empty')
    out.mkdir(parents=True, exist_ok=True)
    program = build_program(dt=dt, dx=dx, mass_squared=1)
    seed = prepare_seed(program)
    assert program.tensor.G == 45 and not program.tensor.support_violations()
    assert set(int(v) for v in seed.r.flat) == set(range(6))
    model = {'id': 'universe24.corrected45-massive-evidence', 'version': '1',
             'domain': 'Finite homogeneous massive scalar plus normal dust, synchronous gauge; proposal evidence',
             'mass_squared': 1, 'units': 'c=8*pi*G=1',
             'physical_step': str(program.dt), 'coordinate_spacing': str(program.dx),
             'metric': 'g=-dt^2+gamma_ij dx^i dx^j; gamma_inverse=B.T B',
             'total_channels': 45, 'retained_integers_per_node': 135,
             'apparatus_channels': 0, 'hidden_evolution_state': 0,
             'old_a_boundary': 'zero encoding memory, not a physical earlier slice',
             'status': 'finite research fixture; general Einstein and quantum gates open'}
    bundle = create_bundle(program.tensor, seed, channels=channel_manifest(program),
                           protocol=default_protocol(), model=model)
    report = run_bundle(bundle, out/'runtime', steps)
    assert verify_run(out/'runtime') == report
    states = [seed]
    with gzip.open(out/'runtime/full_trace.jsonl.gz', 'rt', encoding='utf-8') as stream:
        for record_line in stream:
            record = exact_json.loads(record_line)
            before, after = state_from_data(record['before']), state_from_data(record['after'])
            assert before.same_as(states[-1])
            assert SYMBOL.scalar_oracle(program.tensor, before).same_as(after)
            states.append(after)
    snapshots = [read_snapshot(program, state, step) for step, state in enumerate(states)]
    assert all(snapshot['homogeneous'] for snapshot in snapshots)
    assert snapshots[0]['nodes'][0]['constraints_exact']['H'] == '0'
    # Independent reduced-FLRW algebra: B'=1-h, k'=-1+h/2,
    # phi'=2, pi'=-2h, d'=1-3h/2, hence C'=6k'^2-pi'^2-phi'^2-2d'^2=-7h².
    first_defect = -7*program.dt**2
    assert F(snapshots[1]['nodes'][0]['constraints_exact']['H']) == first_defect
    source_names = ('validation/geodesic_board/run.py',
                    'validation/research_eight/07_hyperbolic_symbol.py',
                    'validation/geometry/team48/refinement_integer_projective.py',
                    'validation/geometry/team48/matter_dust_square.py',
                    'validation/geometry/team48/matter_charged.py',
                    'validation/geometry/team48/matter_equations.py',
                    'universe24/algebra/frame_equations.py')
    result = {'schema': SCHEMA, 'title': 'Universe24 — shared-metric event board',
              'metadata': {'tensor_sha256': program.tensor.fingerprint, 'channels': 45,
                           'nodes': seed.N, 'steps': steps, 'mass_squared': 1,
                           'terms': len(program.tensor), 'degree': program.tensor.rank-1,
                           'max_bits': max(report['maximum_integer_bits_by_step']),
                           'dt': str(program.dt), 'dx': str(program.dx), 'position_units': 'physical_coordinates',
                           'units': model['units'], 'metric_convention': model['metric']},
              'provenance': {'run_id': report['run_id'], 'bundle_id': bundle.bundle_id,
                             'tensor_sha256': program.tensor.fingerprint,
                             'trace_sha256': report['files']['full_trace.jsonl.gz'],
                             'source_sha256': {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                                               for name in source_names}},
              'snapshots': snapshots, 'runtime_validation': report,
              'independent_first_step_control': {'initial_constraint': '0',
                                                  'predicted_H': str(first_defect),
                                                  'observed_H': snapshots[1]['nodes'][0]['constraints_exact']['H'],
                                                  'matches': True},
              'acceptance_gates': {'integer_local_reversible_execution': 'passed',
                                   'same_tensor_massive_source_and_metric': 'passed',
                                   'independent_scalar_oracle': 'passed',
                                   'metric_positive_on_saved_run': 'passed',
                                   'exact_discrete_Einstein_constraints': 'failed',
                                   'general_Einstein_convergence': 'not_tested',
                                   'retained_geodesic_probe': 'not_implemented',
                                   'operational_material_clock': 'not_implemented',
                                   'Born_Bell_quantum_dynamics': 'not_implemented'},
              'limitations': ['Passive geodesics reconstruct motion in the saved metric; no probe evolves inside the tensor.',
                              'The homogeneous source has zero charge; Maxwell and charged fields are allocated but not excited.',
                              'Projective integer bit growth limits the horizon.',
                              'Initial Einstein constraints hold; finite-step constraint drift remains visible.',
                              'Arithmetic clicks are not physical detector outcomes.']}
    result['geodesics'] = build_geodesics(snapshots)
    (out/'board_data.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    render_board(result, out/'board.html')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=ROOT/'runs/geodesic_board')
    parser.add_argument('--steps', type=int, default=4)
    args = parser.parse_args()
    result = run(args.out, steps=args.steps)
    print(json.dumps({'output': str(args.out), 'metadata': result['metadata'],
                      'acceptance_gates': result['acceptance_gates']}, indent=2))


if __name__ == '__main__':
    main()
