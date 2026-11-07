"""Separate prospective +++/+-+ comparison with valid singleton gates."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import time

from research.components import GuidedPacketSource, TensorSpec, plain
from research.experiments.run import assemble, recorded_states, run_experiment
from research.presenter.export import bundle, state_sha256
from universe24 import Channel, Coupling, State
from . import interactions as base

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL = HERE/'interaction_protocol_signed.json'


def sign_name(signs):
    return ''.join('p' if s == 1 else 'm' for s in signs)


def packet_component(method, signs, present, direction=1):
    seed_signs = signs if method == 'tensor_aware' else (1, 1, 1)
    source = GuidedPacketSource(present=present, tensor=TensorSpec.from_signs(seed_signs))
    cells = []
    for address, value in source.cells:
        if direction == -1:
            value = Channel(-value.b, -value.a, value.r)
        cells.append([*address, *value])
    return {'name': 'packet', 'recipe': 'Patch', 'at': [48, 64, 64],
            'params': {'kind': 'signal-source', 'cells': cells,
                       'ports': plain(source.ports), 'sources': plain(source.sources)}}


def observer_protocol(signs):
    protocol = json.loads(base.PROTOCOL.read_text())
    protocol['board']['body_signs'] = list(signs)
    return protocol


def case_spec(case):
    spec = base.case_spec(case)
    signs = tuple(case['body_signs'])
    spec['board']['body_signs'] = list(signs)
    spec['components'][1] = packet_component(case['seed_method'], signs, case['control'][0] == '1')
    if case['seed_method'] == 'tensor_aware':
        coupling = Coupling(signs)
        center = (64, 65, 64)
        h = coupling.ports[2][0]
        q = coupling.weights[3][h]
        phase = case['phase']
        ab = ((0, q), (q, 0), (0, -q), (-q, 0))[phase]
        if case['control'][1] == '0':
            ab = (0, 0)
        cells = {tuple(row[:4]): tuple(row[4:]) for row in spec['components'][0]['params']['cells']}
        cells[(*center, h)] = (*ab, case['clock_remainder'])
        for d, delta in enumerate(base.DIRECTIONS):
            xyz = tuple(center[j]+delta[j] for j in range(3))
            r = 0 if d == 3 else 2
            if phase in (1, 2):
                r += 2*q*coupling.weights[d][h]
            if not 0 <= r < 6:
                raise ValueError('Unsafe tensor-aware clock remainder preparation')
            cells[(*xyz, coupling.ports[d][h])] = (0, 0, r)
        spec['components'][0]['params']['cells'] = [[*a, *v] for a, v in sorted(cells.items())]
    spec['title'] = 'Fixed tensor comparison: '+spec['id']
    spec['description'] = 'Same full seeds and separately tensor-aware preparations; invalid singleton transport cannot count as cancellation.'
    spec['provenance'] = {'protocol_sha256': hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
                          'seed_method': case['seed_method'], 'fixed_body_signs': list(signs)}
    return spec


def carrier_spec(method, signs, direction):
    identity = f'carrier-{method}-{sign_name(signs)}-{direction}'
    return {'format': 'universe24-assembly-experiment-v1', 'id': identity, 'title': identity,
            'description': 'Pristine whole-board signed carrier translation check.',
            'board': {'side': 129, 'background': [0, 0, 2], 'body_signs': list(signs)},
            'steps': 8, 'components': [
                {'name': 'guide', 'recipe': 'GuideSegment', 'at': [0, 64, 64],
                 'params': {'start': 0, 'stop': 128, 'sockets': [48, 49, 50, 51], 'remainder_pair': [0, 4]}},
                packet_component(method, signs, True, direction)],
            'detectors': [], 'view': {'port': 'packet.packet'},
            'provenance': {'protocol_sha256': hashlib.sha256(PROTOCOL.read_bytes()).hexdigest()},
            'budget': {'max_frames': 9, 'max_cells': 500000, 'max_bytes': 67108864, 'max_seconds': 30}}


def geometries(protocol):
    for method, signs, r, phase in itertools.product(protocol['seed_methods'], protocol['tensor_choices'],
                                                    protocol['family']['clock_remainders'], protocol['family']['clock_phases']):
        yield {'id': f'signed-{method}-{sign_name(signs)}-r{r}-p{phase}',
               'seed_method': method, 'body_signs': signs, 'clock_remainder': r, 'phase': phase,
               'stage': 'signed', 'guide_target_channel': 0, 'compensation_direction': None}


def signed_packet_matches(state, x, direction, signs):
    cells = {(xx, 64, 64, g): Channel(0, 0, r) for xx in range(x-1, x+5)
             for g, r in ((0, 0), (14, 4))}
    source = GuidedPacketSource(tensor=TensorSpec.from_signs(signs))
    for address, value in source.cells:
        if direction == -1:
            value = Channel(-value.b, -value.a, value.r)
        cells[(address[0]+x, address[1]+64, address[2]+64, address[3])] = value
    expected = {a: v for a, v in cells.items() if v != Channel(0, 0, 2)}
    actual = {a: v for a, v in state.cells.items()
              if x-1 <= a[0] <= x+4 and abs(a[1]-64) <= 1 and abs(a[2]-64) <= 1}
    return actual == expected


def observe(case, prepared, states):
    observation = base.observe(observer_protocol(case['body_signs']), case, prepared, states)
    carriers = []
    for direction, x in ((1, 72), (-1, 56)):
        for start in range(18, 38):
            if all(signed_packet_matches(states[start+k], x+direction*k, direction, case['body_signs']) for k in range(4)):
                carriers.append({'start': start, 'through': start+3, 'direction': direction,
                                 'outlet_x': x, 'full_local_template_equal': True})
    observation['outgoing_carriers'] = carriers
    observation['forward_outlet_active_steps'] = [t for t in range(20, 41)
                                                  if any(v.a or v.b for v in states[t].node((72, 64, 64)))]
    observation['forward_outlet_C'] = [e for e in observation['all_C']
                                      if 20 <= e['step'] <= 40 and e['address'][:3] == [72, 64, 64]]
    return observation


def run(output):
    output = Path(output)
    protocol_raw = PROTOCOL.read_bytes()
    protocol = json.loads(protocol_raw)
    output.mkdir(parents=True, exist_ok=False)
    (output/'records').mkdir()
    (output/'protocol.json').write_bytes(protocol_raw)
    sources = [Path(__file__), PROTOCOL, Path(base.__file__), base.PROTOCOL,
               *sorted((ROOT/'universe24').rglob('*.py')), *sorted((ROOT/'research/components').glob('*.py')),
               ROOT/'research/experiments/run.py', ROOT/'research/presenter/export.py']
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    cases = list(geometries(protocol))
    registration = {'format': 'universe24-staged-signed-registration-v1',
                    'protocol_sha256': hashlib.sha256(protocol_raw).hexdigest(),
                    'source_sha256': hashes, 'registered_cases': 136, 'geometries': cases,
                    'registered_before_capture': True,
                    'base_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()}
    base.write_json(output/'registration.json', registration)
    started_cpu, started_wall = time.process_time(), time.monotonic()
    ledger, carrier_results, groups, examples = [], [], [], []
    used = 0

    def save(wrapper, meta):
        nonlocal used
        raw = base.canonical(wrapper).encode()
        compressed = gzip.compress(raw, mtime=0)
        record = 'records/'+wrapper['spec']['id']+'.json.gz'
        (output/record).write_bytes(compressed)
        used += len(compressed)
        states = recorded_states(wrapper['experiment'])
        ledger.append({'id': wrapper['spec']['id'], 'record': record, 'metadata': meta,
                       'record_sha256': hashlib.sha256(raw).hexdigest(),
                       'record_gzip_sha256': hashlib.sha256(compressed).hexdigest(),
                       'initial_state_sha256': state_sha256(states[0]),
                       'final_state_sha256': state_sha256(states[-1]),
                       'frames': len(states), 'transitions': len(states)-1,
                       'full_state_inverse': wrapper['experiment']['provenance']['full_rewind_equal']})

    carrier_pass = {}
    for method, signs, direction in itertools.product(protocol['seed_methods'], protocol['tensor_choices'], (1, -1)):
        spec = carrier_spec(method, signs, direction)
        recorded = run_experiment(spec)
        states = recorded_states(recorded['experiment'])
        initial = states[0]
        equality = []
        for t, state in enumerate(states):
            expected = State(initial.cube, initial.background,
                             {((a[0]+direction*t) % 129, *a[1:]): v for a, v in initial.cells.items()})
            equality.append(state == expected)
        assessment = {'seed_method': method, 'body_signs': signs, 'direction': direction,
                      'complete_translation_equal': all(equality), 'state_equal_by_step': equality}
        carrier_pass[(method, tuple(signs), direction)] = all(equality)
        carrier_results.append(assessment)
        save({'format': 'universe24-staged-signed-carrier-v1', 'spec': spec, 'assembly': recorded['assembly'],
              'experiment': recorded['experiment'], 'observations': {'translation_equal_by_state': equality},
              'assessment': assessment}, {'family': 'pristine_carrier', **assessment})
    reason = None
    for geometry in cases:
        if time.process_time()-started_cpu >= protocol['budget']['max_cpu_seconds']:
            reason = 'cpu_budget'
            break
        rows = []
        for mask in ('00', '10', '01', '11'):
            case = {**geometry, 'control': mask}
            spec = case_spec(case)
            prepared = assemble(spec)
            recorded = run_experiment(spec)
            states = recorded_states(recorded['experiment'])
            observation = observe(case, prepared, states)
            if observation['active_boundary_hits']:
                raise AssertionError('Unexpected active boundary return')
            rows.append({'case': case, 'spec': spec, 'assembly': recorded['assembly'],
                         'experiment': recorded['experiment'], 'states': states, 'observations': observation})
        assessment = base.compare_group(rows)
        by = {r['case']['control']: r for r in rows}
        valid_carrier = carrier_pass[(geometry['seed_method'], tuple(geometry['body_signs']), 1)]
        eligible = valid_carrier and assessment['clock_only_full_state_period4']
        active = {mask: bool(r['observations']['forward_outlet_active_steps']) for mask, r in by.items()}
        assessment.update(pristine_forward_carrier_valid=valid_carrier, singleton_gates_passed=eligible,
                          strict_forward_cancellation=bool(eligible and active['10'] and not active['00']
                                                           and not active['01'] and not active['11']),
                          forward_outlet_active={mask: r['observations']['forward_outlet_active_steps'] for mask, r in by.items()},
                          forward_carrier_suppression=bool(eligible
                              and any(c['direction'] == 1 for c in assessment['outgoing_carriers']['10'])
                              and not any(c['direction'] == 1 for c in assessment['outgoing_carriers']['11'])))
        for row in rows:
            save({'format': 'universe24-staged-signed-interaction-v1', 'spec': row['spec'],
                  'assembly': row['assembly'], 'experiment': row['experiment'],
                  'observations': row['observations'], 'assessment': assessment}, row['case'])
            if (geometry['seed_method'] == 'tensor_aware' and geometry['clock_remainder'] == 0 and geometry['phase'] == 1):
                examples.append(row['experiment'])
        groups.append(assessment)
        print(f"{len(ledger)}/136 {geometry['id']} eligible={eligible} cancellation={assessment['strict_forward_cancellation']}", flush=True)
        if used > protocol['budget']['max_recorded_bytes']-5000000:
            reason = 'data_budget'
            break
    if any(hashlib.sha256((ROOT/p).read_bytes()).hexdigest() != sha for p, sha in hashes.items()):
        raise RuntimeError('Execution source changed during signed comparison')
    result = {'format': 'universe24-staged-signed-result-v1', 'status': 'completed' if reason is None else 'budget_stopped',
              'stop_reason': reason, 'protocol_sha256': registration['protocol_sha256'], 'registered_cases': 136,
              'completed_cases': len(ledger), 'cases': ledger, 'carrier_checks': carrier_results, 'groups': groups,
              'not_run_geometries': cases[len(groups):],
              'singleton_eligible_groups': sum(g['singleton_gates_passed'] for g in groups),
              'strict_forward_cancellation_groups': sum(g['strict_forward_cancellation'] for g in groups),
              'forward_carrier_suppression_groups': sum(g['forward_carrier_suppression'] for g in groups),
              'retained_record_groups': sum(bool(g['retained_records']) for g in groups),
              'displayed_experiments': len(examples), 'cpu_seconds': time.process_time()-started_cpu,
              'wall_seconds': time.monotonic()-started_wall,
              'scope': 'Fixed signed-tensor comparison; invalid carriers are not canceled signals. No global gauge equivalence or physical-light claim.'}
    base.write_json(output/'result.json', result)
    (output/'experiments.json').write_text(base.canonical(bundle(examples, title='The Presenter: fixed tensor comparison'))+'\n')
    if sum(p.stat().st_size for p in output.rglob('*') if p.is_file()) > protocol['budget']['max_recorded_bytes']:
        raise RuntimeError('Signed comparison data budget exceeded')
    print(base.canonical({k: result[k] for k in ('completed_cases', 'singleton_eligible_groups',
                                               'strict_forward_cancellation_groups', 'retained_record_groups', 'cpu_seconds')}), flush=True)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    return run(parser.parse_args(argv).output)


if __name__ == '__main__':
    main()
