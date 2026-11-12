"""One source-only massive full-frame candidate shared by the November audits.

Only preparation and passive observations live here. The existing Engine and
system bundle execute the immutable tensor; no supported physical model is added.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import tempfile

import numpy as np

from universe24.core import Engine
from universe24.system.bundle import canonical_bytes, create_bundle
from universe24.system.decoder import default_protocol
from universe24.system.runtime import run_bundle, verify_run
from validation.geometry.team48 import refinement_integer_projective as projective
from . import formulation

ROOT = Path(__file__).resolve().parents[2]
BASE_PIN = formulation.BASE_PIN
FIELDS = formulation.FIELDS


def build45(*, dt=F(1, 64), dx=F(1, 4), mass_squared=1,
            cosmological=0, coupling=1):
    return formulation.build45(dt=dt, dx=dx, mass_squared=mass_squared,
        cosmological=cosmological, coupling=coupling)


def weak_values(program, *, L=3):
    """Exact homogeneous initial constraints: rho=3/100, H=6/100-2rho=0."""
    values = np.zeros((len(program.fields), L**3), dtype=object)
    for a in range(3):
        values[program.fields.index(f'B{a}{a}'), :] = F(1)
        values[program.fields.index(f'K{a}{a}'), :] = F(-1, 10)
    values[program.fields.index('phi'), :] = F(1, 5)
    values[program.fields.index('dust_amplitude'), :] = F(1, 10)
    return values


def weak_seed(program, *, L=3, denominator=100, mixed_remainders=True):
    carry = np.array([[(g+n) % 6 if mixed_remainders else 0 for n in range(L**3)]
                      for g in range(program.tensor.G)], dtype=object)
    return projective.prepare(program, weak_values(program, L=L), L=L,
        denominator=denominator, remainders=carry)


def decode_fields(program, state, *, node=0):
    if state.G != len(program.fields)+1 or not 0 <= node < state.N:
        raise ValueError('Wrong allocation or node')
    denominator = int(state.b[0, 0])
    if (denominator <= 0 or not np.all(state.b[0] == denominator)
            or not np.all(state.a[0] == state.a[0, 0])):
        raise ValueError('The passive projective readout requires a uniform positive denominator')
    # Reduce only the requested node; large integer gcd work is observational.
    return {name: F(int(state.b[i+1, node]), denominator)
            for i, name in enumerate(program.fields)}


def channel_manifest(program):
    rows = []
    denominator = program.tensor.names[0]
    for index, name in enumerate(program.tensor.names):
        field = name.removeprefix('projective.')
        if index == 0:
            owner, purpose = 'encoding', 'Common denominator and reversible memory; no physical clock'
        elif field.startswith(('B', 'K', 'G')):
            owner, purpose = 'geometry', 'Shared full-frame geometry numerator '+field
        elif field == 'dust_amplitude':
            owner, purpose = 'dust', 'Normal dust amplitude; density is its square'
        elif field.startswith(('E', 'M', 'A')):
            owner, purpose = 'electromagnetism', 'Shared-metric electromagnetic numerator '+field
        else:
            owner, purpose = 'massive_scalar', 'Shared-metric scalar numerator '+field
        rows.append({'index': index, 'name': name, 'label': program.tensor.labels[index],
                     'owner': owner, 'purpose': purpose, 'retained_registers': ['a','b','r'],
                     'readout_dependencies': [denominator] if index == 0 else [denominator, name]})
    assert len(rows) == 45
    return rows


def make_bundle(program, seed):
    # This metadata describes one exact handoff, not arbitrary caller models.
    expected = build45(dt=program.dt, dx=program.dx)
    if program.tensor.fingerprint != expected.tensor.fingerprint:
        raise ValueError('The common massive bundle requires mass_squared=1 and the unmodified corrected law')
    if not seed.same_as(weak_seed(program, L=seed.L)):
        raise ValueError('The common bundle metadata requires the declared complete weak seed')
    return create_bundle(program.tensor, seed, channels=channel_manifest(program),
        protocol=default_protocol(), model={
            'id': 'completion.massive-full45', 'version': 'nov12-1',
            'domain': 'Corrected full-frame massive Einstein-scalar-dust-Maxwell research candidate',
            'status': 'research; physical acceptance unresolved',
            'physical_step': str(program.dt), 'spatial_step': str(program.dx),
            'mass_squared': '1', 'coordinate_convention': 'synchronous lapse 1, shift 0',
            'metric': 'gamma_inverse=B.T*B, from the same retained full B used by all matter',
            'initial_data': 'weak homogeneous constrained slice; old registers zero',
            'channels': 45, 'unallocated_channels': 3, 'apparatus_channels': 0,
            'physical_clock': 'passive scalar diagnostics only; no accepted detector',
            'baseline_commit': BASE_PIN})


def audit(*, steps=3):
    """Actual system runtime, independent scalar oracle and complete replay."""
    program = build45()
    seed = weak_seed(program)
    fields = decode_fields(program, seed)
    _, constraints, diagnostic = formulation.equations(fields, lambda *_: F(0))
    assert all(value == 0 for value in constraints.values())
    engine, state = Engine(program.tensor), seed
    bits, states = [], [seed]
    for _ in range(steps):
        expected = formulation.previous.scalar_oracle(program.tensor, state)
        after = engine.step(state)
        assert after.same_as(expected) and engine.inverse_step(after).same_as(state)
        assert np.array_equal(after.r, seed.r)
        bits.append(max(abs(int(v)).bit_length() for array in (after.a, after.b, after.r) for v in array.flat))
        state = after
        states.append(state)
    assert engine.rewind(state, steps).same_as(seed)
    bundle = make_bundle(program, seed)
    parent = ROOT/'runs/completion/runtime'
    parent.mkdir(parents=True, exist_ok=True)
    output = Path(tempfile.mkdtemp(prefix='massive45-', dir=parent))/'run'
    report = run_bundle(bundle, output, steps)
    assert verify_run(output) == report
    import gzip
    from universe24.core import exact_json
    with gzip.open(output/'full_trace.jsonl.gz', 'rt') as stream:
        count = 0
        for count, line in enumerate(stream, 1):
            row = exact_json.loads(line)
            assert row['before'] == states[count-1].to_dict()
            assert row['after'] == states[count].to_dict()
        assert count == steps
    result = {'baseline': BASE_PIN, 'channels': program.tensor.G,
        'retained_integers_per_node': 135, 'degree': program.degree,
        'monomials': len(program.tensor), 'mass_squared': 1,
        'dt': str(program.dt), 'dx': str(program.dx),
        'tensor_sha256': program.tensor.fingerprint,
        'seed_sha256': hashlib.sha256(canonical_bytes(seed.to_dict())).hexdigest(),
        'bundle_id': bundle.bundle_id, 'ownership': channel_manifest(program),
        'strict_face_support': not program.tensor.support_violations(),
        'initial_all_constraints_zero': True, 'initial_rho': str(diagnostic['rho']),
        'steps': steps, 'nodes': seed.N, 'all_remainders_retained': True,
        'independent_scalar_oracle': True, 'complete_rewind': True,
        'existing_system_runtime_and_saved_trace_equal': True,
        'runtime_report': report, 'max_bits_by_step': bits,
        'limitations': ['No nonlinear discrete constraint preservation theorem.',
                        'Unmodified time map has an unstable wave branch.',
                        'Unmodified metric update can become singular.',
                        'Passive clock readout is not an operational detector.']}
    path = ROOT/'runs/completion/00_common45.json'
    path.write_text(json.dumps(result, indent=2)+'\n')
    return result


if __name__ == '__main__':
    result = audit()
    print(json.dumps({key: result[key] for key in ('channels','mass_squared','tensor_sha256',
        'seed_sha256','bundle_id','existing_system_runtime_and_saved_trace_equal','max_bits_by_step')}, indent=2))
