"""Independent validation of full-input WRITE-to-PROBE controls and results."""
from __future__ import annotations
import argparse
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import resource
import time
from research.clock_selection import audit as v1
from research.clock_selection.audit import (
    ROOT, Snapshot, canonical, declared_initial, digest, file_digest, load,
    native_digest, packet, source_control,
)
from research.message_mechanism.audit import input_terms
from research.staged_blocks.audit import audit_record

PROTOCOL_SHA = '0eb38141335bb7fac46dd3af283293114175d60896e77747bc0d27858e16a232'


def planned_cases():
    result = [dict(id=f'full-input-pristine-gap{gap}', side=337, clock_remainder=0,
        phase=0, writer_delay=2, gap=gap, stage='pristine', guide_target_channel=0,
        compensation_direction=None, control='11', clock_present=False) for gap in range(36, 40)]
    for side, phase, gap, clock, mask in itertools.product((337, 353), range(4), range(36, 40),
                                                         (True, False), ('00', '10', '01', '11')):
        result.append(dict(id=f'write-probe-L{side}-r0-p{phase}-d2-gap{gap}-clock{int(clock)}',
            side=side, clock_remainder=0, phase=phase, writer_delay=2, gap=gap,
            stage='encounter', guide_target_channel=0, compensation_direction=None,
            clock_present=clock, control=mask))
    return result


def footprints(case):
    c, side = case['side']//2, case['side']
    result = {}
    for name, x in (('writer', c-16-case['writer_delay']), ('probe', c-16-case['writer_delay']-case['gap'])):
        local = declared_initial({'board': {'side': side}, 'components': [
            {'name': name, 'recipe': 'GuidedPacketSource', 'at': [x, c, c]}]})
        result[name] = set(local.cells)
        assert len(result[name]) == 24
    assert not (result['writer'] & result['probe'])
    return result


def vacant(address, c):
    return (0, 0, 0 if address[1:3] == (c, c) and address[3] == 0 else
                   4 if address[1:3] == (c, c) and address[3] == 14 else 2)


def expected_initial(case):
    seed = v1.expected_initial(case)
    if case['stage'] == 'pristine':
        return seed
    cells, c = dict(seed.cells), case['side']//2
    for name, bit in zip(('writer', 'probe'), case['control']):
        if bit == '0':
            for address in footprints(case)[name]:
                cells[address] = vacant(address, c)
    if not case['clock_present']:
        center = (c, c+1, c, 2)
        cells[center] = (0, 0, cells[center][2])
    return Snapshot(case['side'], (0, 0, 2), cells)


def stationary_observations(case, states):
    assert all(s == states[0] for s in states)
    assert all(not any(v[:2]) for v in states[0].cells.values())
    c, center, h, nodes = v1.geometry(case)
    addresses = [(*n, g) for n in nodes for g in range(48)]
    region = [list(states[0].at(a)) for a in addresses]
    ctr = list(states[0].at((*center, h)))
    _, donors = input_terms(states[0], [(*center, h)], (1, 1, 1))
    terms = [{'source': v['address'], 'term': 0} for v in donors[0]]
    probe_x = c-16-case['writer_delay']-case['gap']
    T = 24+case['writer_delay']+case['gap']
    return dict(region_nodes=[list(n) for n in nodes], region_addresses=[list(a) for a in addresses],
        region_trace=[region for s in states], center_address=[*center, h], center_trace=[ctr for s in states],
        center_inputs=[dict(update=t, terms=terms, u=0) for t in range(1, len(states))],
        boundary_inputs=[dict(update=t, nonzero_external_terms=[]) for t in range(1, len(states))],
        all_C=[], center_C=[], candidate_holds=[], outgoing_carriers=[], active_boundary_hits=[],
        incoming=[dict(step=case['gap']+k, origin_x=probe_x+case['gap']+k, match=False) for k in (4, 5, 6, 7)],
        registered_output=[dict(step=T+k, origin_x=c+8+k, match=False) for k in range(4)],
        registered_C_window=[T-3, T+4], registered_output_C=[],
        expected_output_C=[dict(step=T-3, kind=2, ell=-1), dict(step=T+1, kind=1, ell=1)],
        initial_active_boundary_margin=None, hold=dict(start=32, through=40, complete_region_period4=True,
            center_unit_counter_norm=False, other_counter_pairs_zero=True,
            every_external_term_zero=True, center_u_and_ell_zero=True))


def observations(case, states):
    if case['stage'] == 'pristine':
        return v1.observations(case, states)
    active = sum(bool(any(v[:2])) for v in states[0].cells.values())
    out = v1.observations(case, states) if active else stationary_observations(case, states)
    out['initial_active_counter_count'] = active
    c = case['side']//2
    excluded = {tuple(n) for n in out['region_nodes']}
    near = []
    for offset in (-6, -5, -4):
        x = c+offset
        t = 16+case['writer_delay']+case['gap']+offset
        expected = {a: v for a, v in packet(case['side'], x, c, c).items() if a[:3] not in excluded}
        actual = {a: v for a, v in states[t].cells.items() if x-1 <= a[0] <= x+4 and
                  abs(a[1]-c) <= 1 and abs(a[2]-c) <= 1 and a[:3] not in excluded}
        near.append(dict(step=t, origin_x=x, match=actual == expected))
    out['near_incoming'] = near
    return out


def assess_case(case, out):
    if case['stage'] == 'pristine':
        return {'pristine_translation': out['complete_translation']}
    exact = all(r['match'] for r in out['registered_output'])
    raw = out['registered_output_C'] == out['expected_output_C']
    margin = out['initial_active_boundary_margin']
    return dict(incoming_contract=all(r['match'] == (case['control'][1] == '1') for r in out['incoming']),
        near_incoming_contract=all(r['match'] == (case['control'][1] == '1') for r in out['near_incoming']),
        complete_hold=all(v for k, v in out['hold'].items() if k not in ('start', 'through')),
        exact_output_carrier=exact, exact_output_C_signature=raw, carrier_plus_C=exact and raw,
        strict_initial_causal_margin=margin is None or margin > 88,
        no_active_boundary_contact=not out['active_boundary_hits'])


def preparation_check(case, states):
    union = set().union(*(s.cells for s in states.values()))
    allowed = footprints(case)
    tests = []
    c = case['side']//2
    for index, name in enumerate(('writer', 'probe')):
        for other in ('0', '1'):
            off = '0'+other if index == 0 else other+'0'
            on = '1'+other if index == 0 else other+'1'
            changed = {a for a in union if states[off].at(a) != states[on].at(a)}
            tests.append(dict(source=name, other_present=other, changed_addresses=len(changed),
                outside_declared_footprint_equal=changed <= allowed[name],
                absent_footprint_pristine=all(states[off].at(a) == vacant(a, c) for a in allowed[name])))
    return dict(cases=tests,
        passed=all(t['outside_declared_footprint_equal'] and t['absent_footprint_pristine'] for t in tests),
        full_initial_remainders_identical=all(len({s.at(a)[2] for s in states.values()}) == 1 for a in union))


def assess_group(rows, claim):
    by = {r['case']['control']: r for r in rows}
    assert set(by) == {'00', '01', '10', '11'}
    case = rows[0]['case']
    prep = preparation_check(case, {m: r['states'][0] for m, r in by.items()})
    baseline = all(by['00']['states'][t] == by['00']['states'][t+4] for t in range(85))
    input_ok = all(r['assessment'][k] for r in rows for k in ('incoming_contract', 'near_incoming_contract',
                      'strict_initial_causal_margin', 'no_active_boundary_contact'))
    hold = all(r['assessment']['complete_hold'] for r in rows)
    changed = all(by['11']['observations']['region_trace'][t] != by['01']['observations']['region_trace'][t]
                  for t in range(32, 41))
    no_leak = all(not by[m]['assessment']['exact_output_carrier'] for m in ('00', '10'))
    joint, probe = by['11']['assessment'], by['01']['assessment']
    different = joint['exact_output_carrier'] != probe['exact_output_carrier']
    gate = case['clock_present'] and prep['passed'] and baseline and input_ok and hold and changed and no_leak and different
    pred_joint = case['gap'] % 4 == 2
    pred_probe = (case['phase']+case['writer_delay']+case['gap']) % 4 == 2
    return dict(geometry={k: v for k, v in case.items() if k != 'control'}, preparation_equivalence=prep,
        clock_only_complete_period4=baseline, all_input_boundary_contracts=input_ok, all_complete_holds=hold,
        retained_full_region_differs=changed, writer_only_and_null_output_absent=no_leak,
        carrier_discriminator=gate, enabling_gate=gate and joint['exact_output_carrier'],
        suppressing_gate=gate and not joint['exact_output_carrier'],
        carrier_and_C_discriminator=gate and joint['carrier_plus_C'] != probe['carrier_plus_C'],
        raw_C_discriminator=gate and joint['exact_output_C_signature'] != probe['exact_output_C_signature'],
        raw_carrier_difference_without_eligibility=different, clock_off_comparison_only=not case['clock_present'],
        predicted_joint_carrier=pred_joint if case['clock_present'] else None,
        predicted_probe_only_carrier=pred_probe if case['clock_present'] else None,
        carrier_prediction_matches=(joint['exact_output_carrier'] == pred_joint and probe['exact_output_carrier'] == pred_probe)
            if case['clock_present'] else None,
        cases={m: r['assessment'] for m, r in by.items()},
        full_final_hashes={m: native_digest(r['states'][-1]) for m, r in by.items()}, claim_limit=claim)


def audit(study, output, budget=600):
    study, output = Path(study), Path(output)
    assert not output.exists()
    start, wall = time.process_time(), time.monotonic()
    report = dict(format='universe24-clock-selection-independent-audit-v2', passed=False, failure=None,
        auditor_sha256=file_digest(__file__), helper_sha256=file_digest(v1.__file__),
        protocol_sha256=PROTOCOL_SHA, records=[], groups=[], clock_mask_checks=[], cpu_budget_seconds=budget)
    try:
        p, result, reg = [load(study/f) for f in ('protocol.json', 'result.json', 'registration.json')]
        assert file_digest(study/'protocol.json') == PROTOCOL_SHA == reg['protocol_sha256']
        assert digest(p) == reg['protocol_canonical_sha256'] and reg['cases'] == planned_cases()
        source_hashes = reg['source_sha256']
        assert all(file_digest(ROOT/f) == h for f, h in source_hashes.items())
        report['source_sha256'] = source_hashes
        assert result['registered_cases'] == 260 and result['completed_cases'] == len(result['cases'])
        assert result['not_run_cases'] == planned_cases()[result['completed_cases']:]
        equivalence = load(study/'preparation_equivalence.json')
        current, groups, clock_on, pristine = [], [], {}, 0
        for i, entry in enumerate(result['cases']):
            if time.process_time()-start > budget:
                raise TimeoutError('Independent V2 CPU budget exhausted')
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
            assessment = assess_case(case, out)
            assert assessment == entry['assessment'] == record['assessment']
            assert native_digest(states[0]) == entry['initial_state_sha256']
            assert native_digest(states[-1]) == entry['final_state_sha256']
            assert entry['frames'] == len(states) == (9 if case['stage'] == 'pristine' else 89)
            assert entry['transitions'] == len(states)-1 and entry['full_state_inverse'] is True
            report['records'].append(dict(id=entry['id'], case=case, integrity=integrity, assessment=assessment))
            if case['stage'] == 'pristine':
                pristine += int(assessment['pristine_translation'])
                assert record['group_assessment'] is None
            else:
                key = (case['side'], case['phase'], case['gap'], case['control'])
                if case['clock_present']:
                    clock_on[key] = states[0]
                else:
                    c = case['side']//2
                    source_control(clock_on[key], states[0], [(c, c+1, c, 2)])
                    report['clock_mask_checks'].append(dict(case=case['id'].replace('clock0', 'clock1')+'-'+case['control'], passed=True))
                current.append(dict(case=case, states=states, observations=out, assessment=assessment,
                                    saved_group=record['group_assessment']))
                if len(current) == 4:
                    group = assess_group(current, p['claim'])
                    assert all(r['saved_group'] == group for r in current)
                    assert result['groups'][len(groups)] == group
                    assert equivalence['groups'][case['id']] == group['preparation_equivalence']
                    groups.append(group)
                    report['groups'].append(group)
                    current.clear()
            if (i+1) % 4 == 0:
                print(canonical({'audited_records': i+1, 'registered': 260}), flush=True)
        assert not current and len(groups) == len(result['groups'])
        assert report['clock_mask_checks'] == equivalence['clock_masks']
        assert pristine == result['pristine_passes']
        for a, b in [('carrier_discriminator_groups', 'carrier_discriminator'), ('enabling_groups', 'enabling_gate'),
                     ('suppressing_groups', 'suppressing_gate'), ('raw_C_discriminator_groups', 'raw_C_discriminator')]:
            assert result[a] == sum(g[b] for g in groups)
        assert all(file_digest(ROOT/f) == h for f, h in source_hashes.items())
        assert result['status'] == 'completed' and len(report['records']) == 260
        report.update(passed=True, sources_unchanged=True,
            full_states=sum(r['integrity']['states'] for r in report['records']),
            transitions=sum(r['integrity']['forward_transitions'] for r in report['records']), full_rewinds=260,
            claim_limit=p['claim'], near_input_scope='Clock-region nodes excluded exactly as preregistered; not proof of exclusive clock mediation.')
    except Exception as exc:
        report['failure'] = f'{type(exc).__name__}: {exc}'
    report.update(cpu_seconds=time.process_time()-start, wall_seconds=time.monotonic()-wall,
                  peak_resident_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, sort_keys=True, indent=2)+'\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--study', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--max-cpu-seconds', type=float, default=600)
    args = parser.parse_args()
    result = audit(args.study, args.output, args.max_cpu_seconds)
    print(canonical({k: result[k] for k in ('passed', 'failure', 'cpu_seconds')}))
    raise SystemExit(0 if result['passed'] else 1)
