"""One six-channel complete-state homogeneous Einstein candidate.

The physical fields are a constrained spinor decode, not the old full45
numerators. Only the unchanged Engine evolves the retained state. Projective
bit growth is retained and reported; no operational detector is supplied.
"""
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import tempfile

import numpy as np

from universe24.core import Engine
from universe24.system.bundle import create_bundle, canonical_bytes
from universe24.system.decoder import default_protocol
from universe24.system.runtime import run_bundle, verify_run
from validation.geometry.team48 import refinement_integer_projective as projective
from validation.completion.formulation import previous
from . import constrained_coordinates as coordinates

ROOT = Path(__file__).resolve().parents[2]
BASE_PIN = '4c2abdda08c4212d08896bd2bd933a7c8dd42c1c'
FIELDS = coordinates.FIELDS


def build(*, dt=F(1, 24)):
    # Validate BEFORE cache lookup: Fraction(1,32)==0.03125 and Fraction(1)==True.
    if type(dt) not in (int, F):
        raise TypeError('Use an exact rational timestep')
    return _build_exact(F(dt))


@lru_cache(maxsize=32)
def _build_exact(dt):
    return projective.compile_projective(FIELDS, coordinates.equations,
        dt=dt, dx=F(1), degree=3)


def prepare(program, *, L=3, denominator=4, values=None):
    if values is None:
        values = {'sa': F(1), 'sb': F(0), 'sc': F(0), 'se': F(0), 'beta': F(0)}
    if set(values) != set(FIELDS):
        raise ValueError('The complete five-coordinate seed must be supplied')
    current = np.array([[values[name]]*(L**3) for name in FIELDS], dtype=object)
    carries = np.array([[(g+n) % 6 for n in range(L**3)] for g in range(6)], dtype=object)
    return projective.prepare(program, current, L=L, denominator=denominator,
                              remainders=carries)


def decode_coordinates(program, state, *, node=0):
    if state.G != 6 or not 0 <= node < state.N:
        raise ValueError('Wrong allocation or node')
    denominator = int(state.b[0, 0])
    if denominator <= 0 or not np.all(state.b[0] == denominator) or not np.all(state.a[0] == state.a[0, 0]):
        raise ValueError('The declared positive uniform projective domain is required')
    return {name: F(int(state.b[i+1, node]), denominator) for i, name in enumerate(FIELDS)}


def decode(program, state, *, node=0):
    return coordinates.physical(decode_coordinates(program, state, node=node))


def complete_bits(state):
    return max(abs(int(v)).bit_length() for arr in (state.a, state.b, state.r) for v in arr.flat)


def trace(*, dt=F(1, 24), steps=3, denominator=4, values=None, oracle=True):
    if type(steps) is not int or steps < 0:
        raise ValueError('An integer nonnegative step count is required')
    program = build(dt=dt)
    seed = prepare(program, denominator=denominator, values=values)
    states, physical = [seed], [decode(program, seed)]
    engine, state = Engine(program.tensor), seed
    for _ in range(steps):
        old = state
        state = engine.step(old)
        if oracle:
            assert state.same_as(previous.scalar_oracle(program.tensor, old))
        assert engine.inverse_step(state).same_as(old)
        assert np.array_equal(state.r, seed.r)
        decoded = decode(program, state)
        assert coordinates.constraint(decoded) == 0
        assert decoded['k'] <= 0 and decoded['beta'] <= physical[-1]['beta']
        # The declared sector is homogeneous despite its differing inert carries.
        assert all(np.all(row == row[0]) for row in state.a)
        assert all(np.all(row == row[0]) for row in state.b)
        states.append(state)
        physical.append(decoded)
    assert engine.rewind(state, steps).same_as(seed)
    return {'program': program, 'seed': seed, 'states': states, 'physical': physical,
            'bits': [complete_bits(s) for s in states]}


def identity(program, seed):
    return {'tensor_sha256': program.tensor.fingerprint,
            'seed_sha256': hashlib.sha256(canonical_bytes(seed.to_dict())).hexdigest(),
            'dt': str(program.dt), 'denominator': int(seed.b[0, 0]),
            'channels': program.tensor.G, 'retained_integers_per_node': 3*program.tensor.G}


def make_bundle(program, seed):
    if program.tensor.fingerprint != build(dt=program.dt).tensor.fingerprint:
        raise ValueError('The bundle metadata requires the selected spinor law')
    if not seed.same_as(prepare(program, L=seed.L)):
        raise ValueError('The bundle metadata requires the declared complete seed')
    rows = []
    for index, name in enumerate(program.tensor.names):
        rows.append({'index': index, 'name': name, 'label': program.tensor.labels[index],
            'owner': 'encoding' if index == 0 else 'shared_geometry_matter_coordinates',
            'purpose': 'Retained denominator/history' if index == 0 else 'Constrained Einstein coordinate '+FIELDS[index-1],
            'retained_registers': ['a','b','r'],
            'readout_dependencies': list(program.tensor.names)})
    return create_bundle(program.tensor, seed, channels=rows, protocol=default_protocol(), model={
        'id': 'unified-law.homogeneous-spinor6', 'version': '1',
        'domain': 'Homogeneous isotropic expanding neutral massive scalar and comoving dust',
        'status': 'source-only constrained research candidate; no general physical acceptance',
        'baseline_commit': BASE_PIN, 'proper_time_step': str(program.dt),
        'mass_squared': 1, 'lapse': 1, 'shift': 0,
        'metric': 'B=exp(beta); inverse spatial metric=exp(2beta)*I',
        'physical_decoder': 'validation.unified_law.constrained_coordinates.physical',
        'constraint': '6*k^2-p^2-phi^2-2*dust^2 identically zero for the physical decoder',
        'apparatus_channels': 0, 'proper_clock_detector': 'not implemented',
        'bit_cost': 'projective cubic denominator grows exponentially in update count'})


def main():
    data = trace()
    program, seed = data['program'], data['seed']
    bundle = make_bundle(program, seed)
    parent = ROOT/'runs/unified_law/runtime'
    parent.mkdir(parents=True, exist_ok=True)
    out = Path(tempfile.mkdtemp(prefix='spinor6-', dir=parent))/'run'
    report = run_bundle(bundle, out, 3)
    assert verify_run(out) == report
    import gzip
    from universe24.core import exact_json
    with gzip.open(out/'full_trace.jsonl.gz', 'rt') as stream:
        count = 0
        for count, line in enumerate(stream, 1):
            row = exact_json.loads(line)
            assert row['before'] == data['states'][count-1].to_dict()
            assert row['after'] == data['states'][count].to_dict()
        assert count == 3
    result = {'baseline': BASE_PIN, **identity(program, seed),
        'degree': program.degree, 'monomials': len(program.tensor),
        'multiplier': program.multiplier, 'nodes': seed.N, 'steps': 3,
        'strict_face_support': not program.tensor.support_violations(),
        'all_six_carries_and_independent_oracle': True, 'complete_rewind': True,
        'existing_runtime_complete_states_match_scalar_oracle': True,
        'constraint_zero_every_step': True, 'beta_nonincreasing_every_step': True,
        'bits': data['bits'], 'physical_samples': [{k: str(v) for k,v in row.items()} for row in data['physical']],
        'bundle_id': bundle.bundle_id, 'runtime_report': report,
        'source_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (Path(__file__), Path(coordinates.__file__))},
        'scope': 'One homogeneous sourced candidate; no spatial wave, general GR or operational detector claim'}
    path = ROOT/'runs/unified_law/00_common.json'
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ('channels','tensor_sha256','seed_sha256','degree','monomials','multiplier','bits','constraint_zero_every_step')}, indent=2))


if __name__ == '__main__':
    main()
