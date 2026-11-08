"""Independent exact-matrix review of finite periodic carrier recurrence."""
from __future__ import annotations
import argparse
from functools import lru_cache
import gzip
import hashlib
import json
from pathlib import Path
import resource
import time

from research.clock_selection.audit import (
    ROOT, Snapshot, canonical, coupling, declared_initial, digest, file_digest,
    load, native_digest, packet, source_control, translated,
)
from research.reference.algebra import DIRECTIONS
from research.staged_blocks.audit import audit_record, interaction_observations

PROTOCOL_SHA = 'd549d19abb26563271af88184c4d54aad72d975807dc48396112dec941a8644a'


def planned_cases():
    cases = []
    for side in (48, 50, 52, 54):
        stage = 'discovery' if side < 52 else 'holdout'
        common = dict(side=side, stage=stage, phase=2, clock_remainder=0,
                      guide_target_channel=0, compensation_direction=None)
        cases.append(dict(common, id=f'ring-pristine-L{side}', control='10', pristine=True))
        cases.extend(dict(common, id=f'ring-L{side}', control=mask, pristine=False)
                     for mask in ('00', '10', '01', '11'))
    return cases


def expected_initial(case):
    side, mask = case['side'], case['control']
    c = side//2
    x = c-16
    seed = declared_initial({'board': {'side': side, 'background': [0, 0, 2], 'body_signs': [1, 1, 1]},
        'components': [
            {'name': 'guide', 'recipe': 'GuideSegment', 'at': [0, c, c], 'params': {
                'start': 0, 'stop': side-1, 'sockets': list(range(x, x+4)), 'remainder_pair': [0, 4]}},
            {'name': 'packet', 'recipe': 'GuidedPacketSource', 'at': [x, c, c],
             'params': {'present': mask[0] == '1'}}]})
    if case['pristine']:
        return seed
    cells = dict(seed.cells)
    center, h = (c, c+1, c), 2
    cells[(*center, h)] = (0, -1 if mask[1] == '1' else 0, 0)
    matrix = coupling((1, 1, 1))
    for d, delta in enumerate(DIRECTIONS):
        position = tuple(center[j]+delta[j] for j in range(3))
        recipient = [g for g in range(48) if matrix.ports[d ^ 1][g] == h]
        assert len(recipient) == 1
        cells[(*position, recipient[0])] = (0, 0, (0 if d == 3 else 2)+2)
    return Snapshot(side, (0, 0, 2), cells)


@lru_cache(maxsize=256)
def wrapped_packet(side, origin, c):
    # Build an entirely interior independent template, then translate each
    # complete address modulo L. This includes all six spatial faces at wrap.
    return {((a[0]-10+origin) % side, (a[1]-10+c) % side,
             (a[2]-10+c) % side, a[3]): v for a, v in packet(side, 10, 10, 10).items()}


def wrapped_matches(state, origin, c):
    side = state.side
    xs = {(origin+d) % side for d in range(-1, 5)}
    yz = {(c+d) % side for d in (-1, 0, 1)}
    actual = {a: v for a, v in state.cells.items() if a[0] in xs and a[1] in yz and a[2] in yz}
    return actual == wrapped_packet(side, origin % side, c)


def observations(case, states):
    side, c = case['side'], case['side']//2
    bp = {'board': {'side': side, 'background': [0, 0, 2], 'body_signs': [1, 1, 1]},
        'geometry': {'clock_x': c, 'clock_y': c+1, 'clock_z': c, 'row_y': c, 'row_z': c,
                     'forward_outlet_x': c+8, 'backward_outlet_x': c-8},
        'readouts': {'eligible_hold_starts': []}}
    data = interaction_observations(bp, case, states)
    track = [wrapped_matches(s, c-16+t, c) for t, s in enumerate(states)]
    cycles = []
    for n in (0, 1, 2):
        shift = n*side
        start, end = shift+32, shift+40
        region, center = data['region_trace'], data['center_trace']
        checks = dict(complete_lag_four=all(region[t] == region[t+4] for t in range(start, end-3)),
            unit_clock_r0=all(a*a+b*b == 1 and r == 0 for a, b, r in center[start:end+1]),
            other_pairs_zero=all(not any(v[:2]) for f in region[start:end+1] for g, v in enumerate(f) if g != 2),
            individual_external_terms_zero=all(not data['boundary_inputs'][t]['nonzero_external_terms'] for t in range(start, end)),
            center_u_zero=all(data['center_inputs'][t]['u'] == 0 for t in range(start, end)),
            center_ell_zero=all(center[t+1][1]+center[t][0] == 0 for t in range(start, end)))
        events = [[e['step'], e['kind'], e['ell']] for e in data['all_C']
                  if e['address'] == [c+8, c, c, 0] and shift+21 <= e['step'] <= shift+28]
        incoming = [track[shift+t] for t in (4, 5, 6, 7)]
        outgoing = [track[shift+t] for t in (24, 25, 26, 27)]
        cycles.append(dict(cycle=n, incoming_matches=incoming, incoming_complete=all(incoming),
            outgoing_matches=outgoing, outgoing_complete=all(outgoing),
            continuous_return=None if n == 0 else all(track[24+(n-1)*side:8+n*side]),
            hold_start=start, hold_through=end, hold_checks=checks, complete_hold=all(checks.values()),
            outlet_C=events, exact_outlet_C_signature=events == [[shift+21, 2, -1], [shift+25, 1, 1]]))
    return dict(data, packet_tracking=track, cycles=cycles,
        pristine_full_translation=case['pristine'] and all(s == translated(states[0], t) for t, s in enumerate(states)))


def assess_group(rows, claim):
    by = {r['case']['control']: r for r in rows}
    assert set(by) == {'00', '01', '10', '11'}
    side = rows[0]['case']['side']
    c = side//2
    initial = {m: r['states'][0] for m, r in by.items()}
    for on, off in (('10', '00'), ('11', '01')):
        source_control(initial[on], initial[off], [(x, c, c, g) for x in range(c-16, c-12) for g in (0, 14)])
    for on, off in (('01', '00'), ('11', '10')):
        source_control(initial[on], initial[off], [(c, c+1, c, 2)])
    addresses = set().union(*(s.cells for s in initial.values()))
    matched = all(len({s.at(a)[2] for s in initial.values()}) == 1 for a in addresses)
    delta = {m: {a for a in addresses if initial[m].at(a)[:2] != initial['00'].at(a)[:2]} for m in ('10', '01')}
    expected_packet = {(x, c, c, g) for x in range(c-16, c-12) for g in (0, 14)}
    masks = (delta['10'] == expected_packet and delta['01'] == {(c, c+1, c, 2)}
        and all(initial['11'].at(a)[k] == initial['10'].at(a)[k]+initial['01'].at(a)[k]-initial['00'].at(a)[k]
                for a in addresses for k in (0, 1)))
    null = all(s == initial['00'] for s in by['00']['states'])
    quiet = by['01']['states']
    period = all(quiet[t] == quiet[t+4] for t in range(len(quiet)-4))
    controls = matched and masks and null and period
    traces = {m: r['observations']['cycles'] for m, r in by.items()}
    first = traces['11'][0]
    returns = []
    for n in (1, 2):
        cur, prev = traces['11'][n], traces['11'][n-1]
        returned = bool(first['incoming_complete'] and first['outgoing_complete'] and cur['continuous_return'])
        eligible = returned and cur['incoming_complete'] and prev['complete_hold']
        comparator = traces['10'][n]['incoming_complete']
        differs = cur['outgoing_complete'] != traces['10'][n]['outgoing_complete']
        returns.append(dict(cycle=n, genuine_return=returned, phase_prediction_eligible=eligible,
            predicted_output=side % 4 == 2, observed_output=cur['outgoing_complete'],
            conditional_prediction_matches=None if not eligible else cur['outgoing_complete'] == (side % 4 == 2),
            packet_only_input_valid=comparator, output_differs_from_packet_only=differs,
            bounded_clock_conditioned_return=bool(controls and eligible and comparator and differs),
            raw_C_signature=cur['exact_outlet_C_signature']))
    return dict(side=side, stage=rows[0]['case']['stage'], matched_remainders=matched,
        exact_source_masks=masks, null_static=null, clock_only_period_four=period, control_checks=controls,
        returns=returns, all_full_state_inverses=True,
        full_final_hashes={m: native_digest(r['states'][-1]) for m, r in by.items()}, claim_limit=claim)


def audit(study, output, budget=600):
    study, output = Path(study), Path(output)
    assert not output.exists()
    start, wall = time.process_time(), time.monotonic()
    report = dict(format='universe24-clock-recurrence-independent-audit-v1', passed=False, failure=None,
        auditor_sha256=file_digest(__file__), helper_sha256=file_digest(ROOT/'research/clock_selection/audit.py'),
        records=[], groups=[], protocol_sha256=PROTOCOL_SHA, cpu_budget_seconds=budget)
    try:
        p, result, registration = [load(study/f) for f in ('protocol.json', 'result.json', 'registration.json')]
        assert file_digest(study/'protocol.json') == PROTOCOL_SHA == registration['protocol_sha256']
        assert registration['cases'] == planned_cases()
        hashes = registration['source_sha256']
        assert all(file_digest(ROOT/path) == sha for path, sha in hashes.items()), 'Producer source changed'
        report['source_sha256'] = hashes
        assert result['registered_cases'] == 20 and result['completed_cases'] == len(result['cases'])
        assert result['not_run_cases'] == planned_cases()[result['completed_cases']:]
        current, groups, pristine = [], [], 0
        for i, entry in enumerate(result['cases']):
            if time.process_time()-start > budget:
                raise TimeoutError('Independent recurrence audit budget exhausted')
            case = planned_cases()[i]
            assert entry['case'] == case
            path = study/entry['record']
            assert path.resolve().is_relative_to(study.resolve())
            raw = gzip.decompress(path.read_bytes())
            assert hashlib.sha256(raw).hexdigest() == entry['record_sha256']
            assert file_digest(path) == entry['record_gzip_sha256']
            record = json.loads(raw)
            assert record['case'] == case and record['protocol_sha256'] == PROTOCOL_SHA
            integrity, states = audit_record({k: v for k, v in record.items() if k != 'observations'},
                expected_initial=expected_initial(case), deadline=start+budget)
            out = observations(case, states)
            assert out == record['observations'], ('Observation mismatch', entry['id'],
                [k for k in out if out[k] != record['observations'].get(k)])
            assert native_digest(states[0]) == entry['initial_state_sha256']
            assert native_digest(states[-1]) == entry['final_state_sha256']
            assert entry['frames'] == len(states) == 2*case['side']+41
            assert entry['transitions'] == len(states)-1 and entry['full_state_inverse'] is True
            assert entry['pristine_full_translation'] == out['pristine_full_translation']
            report['records'].append(dict(id=entry['id'], case=case, integrity=integrity,
                cycles=out['cycles'], pristine_full_translation=out['pristine_full_translation']))
            pristine += int(out['pristine_full_translation'])
            if not case['pristine']:
                current.append(dict(case=case, states=states, observations=out))
                if len(current) == 4:
                    group = assess_group(current, p['claim'])
                    assert result['groups'][len(groups)] == group
                    groups.append(group)
                    report['groups'].append(group)
                    current.clear()
            print(canonical({'audited_records': i+1, 'registered': 20}), flush=True)
        assert not current and len(groups) == len(result['groups'])
        assert result['pristine_translation_passes'] == pristine
        assert result['genuine_returns'] == sum(r['genuine_return'] for g in groups for r in g['returns'])
        assert result['bounded_clock_conditioned_returns'] == sum(r['bounded_clock_conditioned_return'] for g in groups for r in g['returns'])
        assert all(file_digest(ROOT/path) == sha for path, sha in hashes.items())
        assert result['status'] == 'completed' and len(report['records']) == 20
        report.update(passed=True, full_states=sum(r['integrity']['states'] for r in report['records']),
            transitions=sum(r['integrity']['forward_transitions'] for r in report['records']),
            full_rewinds=20, sources_unchanged=True, boundary_scope='Periodic wrapping is intentional and retained.')
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
