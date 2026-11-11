"""One coupled matter/frame tensor; complete replay and failed physical gates."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from universe24.algebra.frame_matter import FIELDS, equations
from universe24.core import Engine
from universe24.core.channels import ChannelAssembly, Component
from universe24.layers.frame_matter import compile_matter_frame
from universe24.prepare.frame_matter import flat_values, prepare, increment
from universe24.observe.frame_matter import bank_values, diagnostics


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'))+'\n').encode()


def continuum_reference():
    """Floating homogeneous scalar-Kasner check, NOT an integer Engine run."""
    powers = (2/3, 1/3, 0)
    def exact(t):
        values = np.zeros(35)
        for i, p in enumerate(powers):
            values[FIELDS.index(f'B{i}{i}')] = t**(-p)
            values[FIELDS.index(f'K{i}{i}')] = -p/t
        values[FIELDS.index('phi')] = (2/3)*np.log(t)
        values[FIELDS.index('Pi')] = (2/3)/t
        return values
    rows = []
    for steps in (16, 32, 64):
        dt = 1/steps
        previous, current = exact(1-dt), exact(1)
        for _ in range(steps):
            rhs, _, _ = equations(dict(zip(FIELDS, current)), lambda name, i: 0, mass_squared=0)
            previous, current = current, previous+2*dt*np.array([float(rhs[name]) for name in FIELDS])
        rows.append({'steps': steps, 'dt': f'1/{steps}',
                     'maximum_error_at_t2': float(np.max(np.abs(current-exact(2))))})
    return {'role': 'floating homogeneous consistency only, not spatial/general/Rule3 convergence',
            'mass_squared': 0, 'runs': rows,
            'errors_decrease': all(b['maximum_error_at_t2'] < a['maximum_error_at_t2']
                                   for a, b in zip(rows, rows[1:]))}


def audit(out=None):
    program = compile_matter_frame()
    assembly = ChannelAssembly([Component('coupled_frame_matter', program.tensor,
        'one frame with mutually coupled complex scalar and normal dust; experimental', 'audit')])
    manifest = assembly.manifest()
    manifest['metric_authorities'] = ['coupled_frame_matter.B']
    manifest['bank_semantics'] = {'X': 'previous 35-field slice', 'Y': 'current 35-field slice'}
    manifest['retained_components_per_slice'] = {'inverse_triad': 9, 'extrinsic_curvature': 6,
        'spatial_connection': 9, 'complex_scalar_and_frame_gradients': 10, 'signed_dust_amplitude': 1}
    manifest['dust_density'] = 'dust_amplitude squared; sign retained, no clipping'
    manifest['clock_apparatus_channels'] = 0
    L, cases = 3, {}
    flat = flat_values(L)
    cases['flat'] = (flat, flat.copy(), 24)
    coupled = flat.copy()
    for name, value in (('phi', 1), ('Pi', 2), ('chi', -1), ('Pi_chi', 1), ('dust_amplitude', 2)):
        coupled[FIELDS.index(name)] = value
    cases['complex_scalar_and_dust'] = (coupled, coupled.copy(), 4)
    rng = np.random.default_rng(70)
    pair = [rng.integers(-1, 2, size=(35, L**3)).astype(object) for _ in range(2)]
    cases['spatial_matter'] = (*pair, 3)
    constrained = flat.copy()
    for name, value in (('K00', -1), ('K11', -1), ('phi', 1), ('Pi', 1)):
        constrained[FIELDS.index(name)] = value
    cases['constrained_slice_pair'] = (constrained, constrained.copy(), 1)
    dust = flat.copy()
    dust[FIELDS.index('K00')], dust[FIELDS.index('dust_amplitude')] = -2, 1
    cases['signed_dust_nonnegative_density'] = (dust, dust.copy(), 1)
    gradient = flat.copy()
    gradient[FIELDS.index('K00')] = 1
    gradient[FIELDS.index('Pi')] = 2*rng.integers(-2, 3, L**3).astype(object)
    # phi=Q=0 satisfies both scalar-gradient constraints at the initial slice.
    cases['scalar_gradient_failure'] = (gradient, gradient.copy(), 1)
    results, engine = {}, Engine(assembly.tensor)
    for name, (old, current, steps) in cases.items():
        r = np.arange(70*L**3).reshape(70, L**3) % 6
        seed = assembly.pack({'coupled_frame_matter': prepare(program, old, current, L=L, remainders=r)})
        state, observations, largest_bits = seed, [], 0
        trace = [encoded({'format': 'Universe24-matter-frame-trace-v1', 'case': name,
                          'tensor': assembly.tensor.to_dict(), 'manifest': manifest,
                          'dt': str(program.dt), 'dx': str(program.dx), 'mass_squared': str(program.mass_squared)})]
        classes = {str(i): 0 for i in range(3)}
        for tick in range(steps+1):
            local = assembly.extract(state, 'coupled_frame_matter')
            trace.append(encoded({'tick': tick, 'state': state.to_dict()}))
            observations.append(diagnostics(bank_values(local), L=L))
            largest_bits = max(largest_bits, state.max_abs().bit_length())
            if tick == steps:
                break
            expected = old+increment(program, current, local.lattice)
            after = engine.step(state)
            decoded = assembly.extract(after, 'coupled_frame_matter')
            assert np.array_equal(bank_values(decoded, 'X'), current)
            assert np.array_equal(bank_values(decoded), expected)
            assert np.array_equal(after.r, seed.r)
            assert engine.inverse_step(after).same_as(state)
            clicks = engine.clicks(state, after, tick+1).select('audit')
            for kind in range(3):
                classes[str(kind)] += int(np.count_nonzero(clicks.kind == kind))
            old, current, state = current, expected, after
        assert engine.rewind(state, steps).same_as(seed)
        assert all(row['negative_dust_nodes'] == 0 and Fraction(row['minimum_rho']) >= 0
                   for row in observations)
        payload = b''.join(trace)
        if out is not None:
            Path(out).mkdir(parents=True, exist_ok=True)
            (Path(out)/f'{name}.jsonl').write_bytes(payload)
        results[name] = {'steps': steps, 'complete_snapshots': steps+1,
                         'exact_pair_map': True, 'exact_rewind': True, 'remainders_frozen': True,
                         'maximum_integer_bits': largest_bits, 'audit_click_classes': classes,
                         'observations': observations if steps <= 4 else [observations[0], observations[-1]],
                         'trace_sha256': hashlib.sha256(payload).hexdigest()}
    rejections = {}
    for dt, dx in ((Fraction(1, 2), Fraction(1, 2)), (Fraction(1, 16), Fraction(1))):
        try:
            compile_matter_frame(dt=dt, dx=dx)
        except ValueError as exc:
            rejections[f'dt={dt},dx={dx}'] = str(exc)
        else:
            raise AssertionError('Integer refinement barrier changed')
    sources = [Path(__file__).relative_to(ROOT)] + [Path(f'universe24/{p}.py') for p in (
        'algebra/frame_equations', 'algebra/frame_matter', 'algebra/null_covector',
        'layers/frame_matter', 'prepare/frame48', 'prepare/frame_matter',
        'observe/frame48', 'observe/frame_matter', 'core/engine', 'core/tensor',
        'core/lattice', 'core/channels', 'tests/test_frame_matter')]
    return {'schema': 'Universe24-matter-frame-v1',
            'base_commit': '7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2',
            'channels': 70, 'monomials': len(program.tensor), 'input_degree': 2,
            'tensor_fingerprint': assembly.tensor.fingerprint, 'manifest': manifest,
            'cases': results, 'refinement_rejections': rejections,
            'continuum_reference': continuum_reference(),
            'gates': {'exact_reversible_integer_pair_map': True,
                      'strict_single_edge_support': not assembly.tensor.support_violations(),
                      'bidirectional_scalar_dust_coupling': True,
                      'single_frame_geometry_in_candidate': True,
                      'general_constraint_preservation': False,
                      'scalar_gradient_constraint_preservation': False,
                      'dust_density_nonnegative_by_square_encoding': True,
                      'nonnegative_total_energy_density': True,
                      'nondegeneracy_preservation': False,
                      'local_discrete_energy_and_charge_balance': False,
                      'arbitrary_integer_spacetime_refinement': False,
                      'operational_metric_clock': False,
                      'general_einstein_solver_validated': False},
            'source_sha256': {str(p): hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=ROOT/'runs/frame-matter')
    args = parser.parse_args()
    report = audit(args.out)
    (args.out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ('channels', 'monomials', 'gates', 'continuum_reference')}, indent=2))
