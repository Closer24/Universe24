"""Run eight integer channels: sourced homogeneous geometry and exact clocks."""
import argparse
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from universe24.core import Engine, State, Tensor
from universe24.prepare.conformal_flrw import prepare
from universe24.observe.conformal_flrw import sample


def encode(value):
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {k: encode(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(v) for v in value]
    return value


def run(out, *, steps=64, subdivision=16):
    if type(steps) is not int or steps < 1:
        raise ValueError('steps must be positive')
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    tensor, seed = prepare(subdivision=subdivision, q0=2*subdivision, dust=(1, 1, 2), radiation=3)
    engine, state = Engine(tensor), seed
    rows = []
    trace = out/'full_trace.jsonl.gz'
    with gzip.open(trace, 'wt') as stream:
        stream.write(json.dumps({'format': 'Universe24-compact-FLRW-full-state-v1',
                                'subdivision': subdivision, 'tensor': tensor.to_dict()})+'\n')
        for tick in range(steps+1):
            values = sample(state, subdivision=subdivision)
            assert values['einstein_residual'] == [0]*4
            assert values['friedmann_residual'] == 0
            rows.append({'tick': tick, **encode(values)})
            stream.write(json.dumps({'tick': tick, 'state': state.to_dict()})+'\n')
            if tick != steps:
                following = engine.step(state)
                assert engine.inverse_step(following).same_as(state)
                state = following
    assert engine.rewind(state, steps).same_as(seed)
    # Replay the serialized tensor and every complete (a,b,r) snapshot.
    with gzip.open(trace, 'rt') as stream:
        replay = Engine(Tensor.from_dict(json.loads(next(stream))['tensor']))
        replayed = State.from_dict(json.loads(next(stream))['state'])
        for record in stream:
            replayed = replay.step(replayed)
            assert replayed.same_as(State.from_dict(json.loads(record)['state']))
    paths = [Path(__file__).relative_to(ROOT)] + [Path(f'universe24/{s}.py') for s in
             ('layers/conformal_flrw', 'prepare/conformal_flrw', 'observe/conformal_flrw',
              'core/engine', 'core/tensor', 'core/lattice')]
    report = {'scope': 'prepared homogeneous flat FLRW dust plus radiation; not general ADM replacement',
              'channels': tensor.G, 'integer_registers_per_node': 3*tensor.G,
              'budget': 48, 'unused_budget': 48-tensor.G, 'padding_channels': 0,
              'steps': steps, 'subdivision': subdivision, 'tensor_fingerprint': tensor.fingerprint,
              'rank': tensor.rank, 'monomials': len(tensor),
              'exact_rewind': True, 'complete_trace_replay': True,
              'all_einstein_residuals_zero_in_declared_sector': True,
              'maximum_retained_integer_bits': max(abs(int(v)).bit_length() for v in state.b.flat),
              'sources': {'dust': [1, 1, 2], 'radiation_amplitude': 3},
              'samples': rows,
              'source_sha256': {str(p): hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},
              'limitations': ['Only homogeneous isotropic expanding flat solutions with zero cosmological constant.',
                  'Matter and antimatter are noninteracting pressureless species labels; no scalar charge, quantum fields or annihilation.',
                  'Radiation is an isotropic fluid with p=rho/3; no individual photon dynamics.',
                  'Null affine counter describes an analytic test ray x=eta-eta0; no moving packet or test-ray stress source.',
                  'No spatially varying gravity, black holes, gravitational waves or arbitrary initial data in this sector.',
                  'Eight fixed channels have unbounded integer bit lengths; geometry decoding alone is not complete state replay.']}
    (out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=ROOT/'runs/compact-flrw')
    parser.add_argument('--steps', type=int, default=64)
    parser.add_argument('--subdivision', type=int, default=16)
    args = parser.parse_args()
    report = run(args.out, steps=args.steps, subdivision=args.subdivision)
    print(json.dumps({k: report[k] for k in ('scope', 'channels', 'steps', 'exact_rewind',
                     'complete_trace_replay', 'all_einstein_residuals_zero_in_declared_sector')}, indent=2))
