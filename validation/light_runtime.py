"""Independent observations of the installed light component's canonical runs."""
import gzip
import json
from pathlib import Path

import numpy as np

from universe24.core import State, exact_json
from universe24.light import make_light_bundle, electromagnetic_fields
from universe24.system.runtime import run_bundle, verify_run
from universe24.system.bundle import load_bundle


def inspect(path, *, replay=True):
    path = Path(path)
    report = verify_run(path) if replay else json.loads((path / 'validation.json').read_text())
    bundle = load_bundle(path / 'bundle')
    p = bundle.model['preparation']
    expected = make_light_bundle(**{k: p[k] for k in ('L', 'axis', 'sign', 'polarization', 'center', 'order', 'amplitude')})
    if expected.bundle_id != bundle.bundle_id:
        raise ValueError('Light interpretation differs from complete prepared inputs')
    seed = bundle.seed
    carrier, L, axis, sign = p['carrier'], p['L'], p['axis'], p['sign']
    energies, first, positions = [], {}, []
    with gzip.open(path / 'full_trace.jsonl.gz', 'rt') as stream:
        for tick, line in enumerate(stream, 1):
            transition = exact_json.loads(line)
            after = State.from_dict(transition['after'])
            expected_field = np.roll(seed.b[carrier].reshape(L, L, L), sign * tick, axis=axis).reshape(-1)
            if not np.array_equal(after.b[carrier], expected_field) or not np.array_equal(after.r, seed.r):
                raise ValueError('Saved light did not translate exactly with retained carries')
            if np.any(np.delete(after.b, carrier, axis=0)):
                raise ValueError('Unexpected extra stream excitation')
            e, b = electromagnetic_fields(after)
            if any(e[axis]) or any(sum(e[i] * b[i] for i in range(3))) or any(sum(e[i] ** 2 - b[i] ** 2 for i in range(3))):
                raise ValueError('Saved field is not the declared transverse null plane wave')
            energy = sum((e * e + b * b).flat)
            energies.append(str(energy))
            positions.append((p['center'] + sign * tick) % L)
    if len(set(energies)) != 1:
        raise ValueError('Plane-wave energy changed')
    counts = {'C0': 0, 'C1': 0, 'C2': 0}
    with gzip.open(path / 'clicks.jsonl.gz', 'rt') as stream:
        for line in stream:
            event = exact_json.loads(line)
            counts[event['kind']] += 1
            if event['channel'] != carrier:
                raise ValueError('An unexcited stream emitted a click')
            key = event['xyz'][axis]
            first.setdefault(str(key), event['step'])
    return {'run_id': report['run_id'], 'bundle_id': report['bundle_id'], 'tensor_hash': report['tensor_hash'],
            'model_contract': report['model_contract'], 'channels': 48, 'retained_integers_per_node': 144,
            'idle_channels': 0, 'steps': report['steps'], 'nodes': seed.N,
            'coordinate_speed': sign, 'exact_one_face_translation': 'passed',
            'transverse_null_field': 'passed', 'exact_plane_energy': 'passed',
            'unfiltered_click_classes': counts, 'first_click_tick_by_axis_coordinate': first,
            'center_positions_mod_L': positions, 'twice_energy_by_step': energies,
            'maximum_integer_bits': max(report['maximum_integer_bits_by_step']),
            'physical_gates': {'specified_2o_covariance': 'passed', 'axis_null_propagation': 'passed',
                               'arbitrary_direction_maxwell_limit': 'not_tested',
                               'dynamic_einstein_source': 'not_tested', 'photon_detector': 'not_tested',
                               'general_physical_acceptance': 'blocked'}}


def collect(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)
    cases = {}
    for axis, name in enumerate('xyz'):
        bundle = make_light_bundle(L=9, axis=axis, center=3, order=2)
        run_bundle(bundle, out / name, 4)
        cases[name] = inspect(out / name, replay=False)
    result = {'cases': cases, 'comparisons': {'same_tensor': len({v['tensor_hash'] for v in cases.values()}) == 1,
                                             'all_axes_exact_unit_speed': all(v['coordinate_speed'] == 1 for v in cases.values())},
              'physical_gates': cases['x']['physical_gates']}
    (out / 'light.json').write_text(json.dumps(result, indent=2) + '\n')
    return result
