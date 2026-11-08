"""Independent full-state audit of frozen clock-selection studies.

Uses the existing exact-matrix oracle, not production routing, preparation,
scalar evolution or study assessment. This module never drives a board.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import platform
import resource
import subprocess
import time

from research.component_review.audit import Snapshot
from research.message_mechanism.audit import declared_initial, input_terms
from research.reference.algebra import DIRECTIONS, coupling
from research.staged_blocks.audit import audit_record, all_events, source_control

ROOT = Path(__file__).resolve().parents[2]
V1_SHA = '1a66353f1400fb3f02869142f41290ab5d534b091be29e6bdd6a7ffc368fa805'


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def file_digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def native_digest(state):
    return digest({'side': state.side,
        'background': [str(state.background[0]), str(state.background[1]), state.background[2]],
        'cells': [[*a, str(v[0]), str(v[1]), v[2]] for a, v in sorted(state.cells.items())]})


def load(path):
    path = Path(path)
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.suffix == '.gz' else raw)


def planned_cases():
    cases = [dict(id=f'write-probe-pristine-L321-gap{gap}', side=321,
        clock_remainder=0, phase=0, writer_delay=1, gap=gap, stage='pristine',
        guide_target_channel=0, compensation_direction=None, control='11')
        for gap in range(32, 36)]
    for phase, gap, mask in itertools.product(range(4), range(32, 36), ('00', '10', '01', '11')):
        cases.append(dict(id=f'write-probe-L321-r0-p{phase}-d1-gap{gap}', side=321,
            clock_remainder=0, phase=phase, writer_delay=1, gap=gap, stage='encounter',
            guide_target_channel=0, compensation_direction=None, control=mask))
    return cases


def geometry(case):
    c = case['side']//2
    center = (c, c+1, c)
    matrix = coupling((1, 1, 1))
    recipients = [g for g in range(48) if matrix.ports[3][g] == 0]
    assert recipients == [2]
    nodes = (center, *(tuple(center[j]+delta[j] for j in range(3)) for delta in DIRECTIONS))
    return c, center, 2, nodes


def expected_initial(case):
    side, mask = case['side'], case['control']
    c, center, h, nodes = geometry(case)
    writer = c-16-case['writer_delay']
    probe = writer-case['gap']
    sockets = [*range(writer, writer+4), *range(probe, probe+4)]
    components = [{'name': 'guide', 'recipe': 'GuideSegment', 'at': [0, c, c],
        'params': {'start': 0, 'stop': side-1, 'sockets': sockets, 'remainder_pair': [0, 4]}},
        *[{'name': name, 'recipe': 'GuidedPacketSource', 'at': [x, c, c],
           'params': {'present': bit == '1'}} for name, x, bit in zip(('writer', 'probe'), (writer, probe), mask)]]
    seed = declared_initial({'board': {'side': side, 'background': [0, 0, 2],
                                      'body_signs': [1, 1, 1]}, 'components': components})
    if case['stage'] == 'pristine':
        return seed
    cells = dict(seed.cells)
    phase = case['phase']
    cells[(*center, h)] = (*((0, 1), (1, 0), (0, -1), (-1, 0))[phase], case['clock_remainder'])
    matrix = coupling((1, 1, 1))
    for d, position in enumerate(nodes[1:]):
        recipients = [g for g in range(48) if matrix.ports[d ^ 1][g] == h]
        assert len(recipients) == 1
        g = recipients[0]
        remainder = (0 if d == 3 else 2) + (2*matrix.weights[d ^ 1][g] if phase in (1, 2) else 0)
        assert 0 <= remainder < 6
        cells[(*position, g)] = (0, 0, remainder)
    return Snapshot(side, (0, 0, 2), cells)


@lru_cache(maxsize=256)
def packet(side, x, y, z, direction=1):
    prepared = declared_initial({'board': {'side': side}, 'components': [
        {'name': 'guide', 'recipe': 'GuideSegment', 'at': [0, y, z],
         'params': {'start': x-1, 'stop': x+4, 'sockets': list(range(x, x+4)), 'remainder_pair': [0, 4]}},
        {'name': 'packet', 'recipe': 'GuidedPacketSource', 'at': [x, y, z]}]})
    if direction == 1:
        return dict(prepared.cells)
    return dict(Snapshot(side, (0, 0, 2), {a: (-v[1], -v[0], v[2]) for a, v in prepared.cells.items()}).cells)


def matches(state, x, y, z, direction=1):
    actual = {a: v for a, v in state.cells.items()
        if x-1 <= a[0] <= x+4 and abs(a[1]-y) <= 1 and abs(a[2]-z) <= 1}
    return actual == packet(state.side, x, y, z, direction)


def translated(state, amount):
    return Snapshot(state.side, state.background,
        {((a[0]+amount) % state.side, *a[1:]): v for a, v in state.cells.items()})


def observations(case, states):
    if case['stage'] == 'pristine':
        return {'complete_translation': all(s == translated(states[0], t) for t, s in enumerate(states))}
    c, center, h, nodes = geometry(case)
    positions = set(nodes)
    addresses = [(*node, g) for node in nodes for g in range(48)]
    region = [[list(state.at(a)) for a in addresses] for state in states]
    ctr = [list(state.at((*center, h))) for state in states]
    matrix = coupling((1, 1, 1))
    inverse = [{sender: receiver for receiver, sender in enumerate(row)} for row in matrix.ports]
    events = [dict(step=e['step'], address=e['address'], kind=e['kind'], ell=int(e['quotient']))
              for e in all_events(states)[0]]
    boundary, inputs = [], []
    for t, old in enumerate(states[:-1], 1):
        external = []
        for source, triple in sorted(old.cells.items()):
            if not triple[1] or source[:3] in positions:
                continue
            for d, delta in enumerate(DIRECTIONS):
                position = tuple((source[j]+delta[j]) % old.side for j in range(3))
                if position not in positions:
                    continue
                g = inverse[d ^ 1][source[3]]
                external.append({'target': [*position, g], 'source': list(source),
                                 'term': matrix.weights[d ^ 1][g]*triple[1]})
        boundary.append({'update': t, 'nonzero_external_terms': external})
        sums, terms = input_terms(old, [(*center, h)], (1, 1, 1))
        inputs.append({'update': t, 'terms': [{'source': v['address'], 'term': v['weight']*int(v['b'])}
                                             for v in terms[0]], 'u': sums[0]})
    carriers = []
    for direction, x in ((1, c+8), (-1, c-8)):
        for start in range(18, len(states)-3):
            if all(matches(states[start+k], x+direction*k, c, c, direction) for k in range(4)):
                carriers.append({'start': start, 'direction': direction, 'outlet_x': x,
                                 'through': start+3, 'full_local_template_equal': True})
    hits = [{'step': t, 'address': list(a)} for t, state in enumerate(states)
            for a, v in state.cells.items() if any(v[:2]) and any(q in (0, state.side-1) for q in a[:3])]
    probe_x = c-16-case['writer_delay']-case['gap']
    incoming = [{'step': case['gap']+k, 'origin_x': probe_x+case['gap']+k,
                 'match': matches(states[case['gap']+k], probe_x+case['gap']+k, c, c)} for k in (4, 5, 6, 7)]
    T = 24+case['writer_delay']+case['gap']
    forward = [{'step': T+k, 'origin_x': c+8+k, 'match': matches(states[T+k], c+8+k, c, c)} for k in range(4)]
    chosen = [{k: e[k] for k in ('step', 'kind', 'ell')} for e in events
              if e['address'] == [c+8, c, c, 0] and T-3 <= e['step'] <= T+4]
    expected_C = [dict(step=T-3, kind=2, ell=-1), dict(step=T+1, kind=1, ell=1)]
    hold = dict(start=32, through=40,
        complete_region_period4=all(region[t] == region[t+4] for t in range(32, 37)),
        center_unit_counter_norm=all(a*a+b*b == 1 for a, b, r in ctr[32:41]),
        other_counter_pairs_zero=all(not any(v[:2]) for frame in region[32:41] for j, v in enumerate(frame) if j != h),
        every_external_term_zero=all(not row['nonzero_external_terms'] for row in boundary[32:40]),
        center_u_and_ell_zero=all(inputs[t]['u'] == 0 and ctr[t+1][1]+ctr[t][0] == 0 for t in range(32, 40)))
    margin = min(min(q, case['side']-1-q) for a, v in states[0].cells.items() if any(v[:2]) for q in a[:3])
    return dict(region_nodes=[list(n) for n in nodes], region_addresses=[list(a) for a in addresses],
        region_trace=region, center_address=[*center, h], center_trace=ctr, center_inputs=inputs,
        boundary_inputs=boundary, all_C=events, center_C=[e for e in events if e['address'] == [*center, h]],
        candidate_holds=[], outgoing_carriers=carriers, active_boundary_hits=hits,
        incoming=incoming, registered_output=forward, registered_C_window=[T-3, T+4],
        registered_output_C=chosen, expected_output_C=expected_C,
        initial_active_boundary_margin=margin, hold=hold)


def assess_case(case, out):
    if case['stage'] == 'pristine':
        return {'pristine_translation': out['complete_translation']}
    carrier = all(v['match'] for v in out['registered_output'])
    raw = out['registered_output_C'] == out['expected_output_C']
    return dict(incoming_contract=all(v['match'] == (case['control'][1] == '1') for v in out['incoming']),
        complete_hold=all(v for k, v in out['hold'].items() if k not in ('start', 'through')),
        exact_output_carrier=carrier, exact_output_C_signature=raw, carrier_plus_C=carrier and raw,
        strict_initial_causal_margin=out['initial_active_boundary_margin'] > 80,
        no_active_boundary_contact=not out['active_boundary_hits'])


def assess_group(rows, claim):
    by = {r['case']['control']: r for r in rows}
    assert set(by) == {'00', '01', '10', '11'}
    case = rows[0]['case']
    c = case['side']//2
    for bit, name in enumerate(('writer', 'probe')):
        x = c-16-case['writer_delay']-(case['gap'] if bit else 0)
        allowed = [(xx, c, c, g) for xx in range(x, x+4) for g in (0, 14)]
        for other in '01':
            on = ('1'+other) if bit == 0 else (other+'1')
            off = ('0'+other) if bit == 0 else (other+'0')
            source_control(by[on]['states'][0], by[off]['states'][0], allowed)
    union = set().union(*(r['states'][0].cells for r in rows))
    matched = all(len({r['states'][0].at(a)[2] for r in rows}) == 1 for a in union)
    baseline = all(by['00']['states'][t] == by['00']['states'][t+4] for t in range(77))
    checks = all(r['assessment'][k] for r in rows for k in ('incoming_contract', 'complete_hold',
                  'strict_initial_causal_margin', 'no_active_boundary_contact'))
    changed = all(by['11']['observations']['region_trace'][t] != by['01']['observations']['region_trace'][t]
                  for t in range(32, 41))
    no_leak = all(not by[m]['assessment']['exact_output_carrier'] for m in ('00', '10'))
    carrier_diff = by['11']['assessment']['exact_output_carrier'] != by['01']['assessment']['exact_output_carrier']
    combined_diff = by['11']['assessment']['carrier_plus_C'] != by['01']['assessment']['carrier_plus_C']
    raw_diff = by['11']['assessment']['exact_output_C_signature'] != by['01']['assessment']['exact_output_C_signature']
    gate = matched and baseline and checks and changed and no_leak and carrier_diff
    pred_joint = case['gap'] % 4 == 2
    pred_probe = (case['phase']+case['writer_delay']+case['gap']) % 4 == 2
    return dict(geometry={k: v for k, v in case.items() if k != 'control'},
        matched_initial_remainders=matched, clock_only_complete_period4=baseline,
        all_input_hold_boundary_contracts=checks, retained_full_region_differs=changed,
        writer_only_and_null_output_absent=no_leak, carrier_discriminator=gate,
        carrier_and_C_discriminator=gate and combined_diff, raw_C_discriminator=gate and raw_diff,
        direction='enabled' if by['11']['assessment']['exact_output_carrier'] else 'suppressed',
        predicted_joint_carrier=pred_joint, predicted_probe_only_carrier=pred_probe,
        carrier_prediction_matches=by['11']['assessment']['exact_output_carrier'] == pred_joint and
                                   by['01']['assessment']['exact_output_carrier'] == pred_probe,
        cases={m: r['assessment'] for m, r in by.items()},
        full_final_hashes={m: native_digest(r['states'][-1]) for m, r in by.items()}, claim_limit=claim)


def audit(study, output, max_cpu_seconds=600):
    study, output = Path(study), Path(output)
    assert not output.exists(), 'Audit output already exists'
    start, wall = time.process_time(), time.monotonic()
    report = dict(format='universe24-clock-selection-independent-audit-v1', passed=False,
        independent_auditor_sha256=file_digest(__file__), cpu_budget_seconds=max_cpu_seconds,
        execution_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        python=platform.python_version(), platform=platform.platform(), studies=[], records=[], groups=[], failure=None,
        scope='Independent exact-state replay, original frozen predicates, control masks and result correspondence; scientific success is separate.')
    try:
        p, result, registration = [load(study/f) for f in ('protocol.json', 'result.json', 'registration.json')]
        assert file_digest(study/'protocol.json') == V1_SHA == registration['protocol_sha256']
        report['protocol_sha256'] = V1_SHA
        assert registration['protocol_canonical_sha256'] == digest(p)
        assert registration['cases'] == planned_cases()
        assert result['registered_cases'] == 68 and result['completed_cases'] == len(result['cases'])
        assert result['not_run_cases'] == planned_cases()[result['completed_cases']:]
        sources = registration['source_sha256']
        for relative, expected in sources.items():
            assert file_digest(ROOT/relative) == expected, ('Producer source changed', relative)
        assert file_digest(study/'executed_search.py') == sources['research/clock_selection/search.py']
        report['source_sha256'] = sources
        collected, groups = [], []
        pristine_passes = 0
        for index, entry in enumerate(result['cases']):
            if time.process_time()-start > max_cpu_seconds:
                raise TimeoutError('Independent replay CPU budget exhausted')
            case = planned_cases()[index]
            assert entry['case'] == case
            path = study/entry['record']
            assert path.resolve().is_relative_to(study.resolve())
            raw = gzip.decompress(path.read_bytes())
            assert hashlib.sha256(raw).hexdigest() == entry['record_sha256']
            assert file_digest(path) == entry['record_gzip_sha256']
            record = json.loads(raw)
            assert record['case'] == case and record['protocol_sha256'] == V1_SHA
            integrity, states = audit_record({k: v for k, v in record.items() if k != 'observations'},
                expected_initial=expected_initial(case), deadline=start+max_cpu_seconds)
            out = observations(case, states)
            assert out == record['observations'], ('Observation mismatch', case['id'], case['control'],
                [k for k in out if out[k] != record['observations'].get(k)])
            assessment = assess_case(case, out)
            assert assessment == record['assessment'] == entry['assessment']
            assert native_digest(states[0]) == entry['initial_state_sha256']
            assert native_digest(states[-1]) == entry['final_state_sha256']
            assert entry['frames'] == len(states) and entry['transitions'] == len(states)-1
            assert entry['full_state_inverse'] is True
            report['records'].append(dict(id=entry['id'], case=case, integrity=integrity, assessment=assessment))
            if case['stage'] == 'pristine':
                pristine_passes += int(assessment['pristine_translation'])
                assert record['group_assessment'] is None
            else:
                collected.append(dict(case=case, states=states, observations=out, assessment=assessment,
                                      saved_group=record['group_assessment']))
                if len(collected) == 4:
                    group = assess_group(collected, p['claim'])
                    assert all(r['saved_group'] == group for r in collected)
                    assert result['groups'][len(groups)] == group
                    groups.append(group)
                    report['groups'].append(group)
                    collected.clear()
            print(canonical({'audited_records': index+1, 'registered': 68}), flush=True)
        assert not collected, 'Incomplete four-control group'
        assert len(groups) == len(result['groups'])
        assert result['pristine_passes'] == pristine_passes
        for result_key, group_key in [('carrier_discriminator_groups', 'carrier_discriminator'),
                ('carrier_and_C_discriminator_groups', 'carrier_and_C_discriminator'),
                ('raw_C_discriminator_groups', 'raw_C_discriminator'), ('predictions_matched', 'carrier_prediction_matches')]:
            assert result[result_key] == sum(g[group_key] for g in groups)
        assert result['source_hashes_unchanged'] is True
        assert all(file_digest(ROOT/path) == sha for path, sha in sources.items())
        assert result['status'] == 'completed' and len(report['records']) == 68
        report.update(passed=True, full_states=sum(r['integrity']['states'] for r in report['records']),
            transitions=sum(r['integrity']['forward_transitions'] for r in report['records']),
            full_rewinds=len(report['records']), sources_unchanged=True)
    except Exception as exc:
        report['failure'] = f'{type(exc).__name__}: {exc}'
    report.update(cpu_seconds=time.process_time()-start, wall_seconds=time.monotonic()-wall,
        peak_resident_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, sort_keys=True, indent=2)+'\n')
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--study', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--max-cpu-seconds', type=float, default=600)
    args = parser.parse_args(argv)
    result = audit(args.study, args.output, args.max_cpu_seconds)
    print(canonical({k: result[k] for k in ('passed', 'failure', 'cpu_seconds')}))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
