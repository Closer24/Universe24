"""Independent counterexamples and full-register audits for signal clocks.

The synthetic verdict fixtures test the observation contract only; they are
not closed-board constructions or evidence that the scientific target works.
The gather oracle uses the separate exact-matrix coupling construction.
"""
from itertools import product
import hashlib
import json
from pathlib import Path
import tempfile
import time
import unittest

from research.reference.algebra import DIRECTIONS, coupling as matrix_coupling
from research.signal_clocks.preparation import prepare
from research.signal_clocks.run import run_case, waiting_verdict
from universe24 import Channel, Cube, Coupling, Engine, State


def independent_gather(state, signs):
    reference = matrix_coupling(tuple(signs))
    side = state.cube.side
    background = tuple(state.background)
    old = dict(state.cells)
    inverse_ports = [{sender: receiver for receiver, sender in enumerate(row)}
                     for row in reference.ports]
    candidates = set(old)
    for (x, y, z, sender), value in old.items():
        if not value[1]:
            continue
        for d, (dx, dy, dz) in enumerate(DIRECTIONS):
            candidates.add(((x-dx) % side, (y-dy) % side, (z-dz) % side,
                            inverse_ports[d][sender]))
    result = {}
    for x, y, z, receiver in candidates:
        address = (x, y, z, receiver)
        a, b, r = old.get(address, background)
        u = sum(reference.weights[d][receiver] * old.get(
            ((x+dx) % side, (y+dy) % side, (z+dz) % side,
             reference.ports[d][receiver]), background)[1]
            for d, (dx, dy, dz) in enumerate(DIRECTIONS))
        numerator = 2*u+r
        quotient = numerator//6
        value = (b, quotient-a, numerator-6*quotient)
        if value != background:
            result[address] = value
    return State(Cube(side), Channel(*background), result)


def synthetic_record(horizon=16, event_times=(4, 10), initial_margin=30):
    """A declared observer trace, deliberately not an engine trajectory."""
    symbols = [(2, 2), (4, 0), (0, 4)]
    trace = []
    for step in range(horizon+1):
        writes = sum(t <= step for t in event_times)
        memory = symbols[writes % len(symbols)]
        incoming = [1, -1] if step+1 in event_times else [0, 0]
        trace.append({'step': step, 'memory': list(memory),
                      'next_input': incoming,
                      'six_inputs': [[{'b': value}] for value in incoming],
                      'arithmetic_events': []})
    return {'record_event_times': list(event_times), 'trace': trace,
            'arithmetic_events': [],
            'preparation': {'steps': horizon},
            'initial_boundary_margin': initial_margin,
            'minimum_boundary_margin': initial_margin-horizon}


def audit_retained_case(folder):
    """Recompute every retained register and detector observation independently."""
    folder = Path(folder)
    report = json.loads((folder/'result.json').read_text())
    checkpoints = [json.loads(line) for line in
                   (folder/'states.jsonl').read_text().splitlines()]
    case = report['preparation']
    assert len(checkpoints) == len(report['trace']) == case['steps']+1
    for which, checkpoint in [('initial', checkpoints[0]), ('final', checkpoints[-1])]:
        assert json.loads((folder/f'{which}.json').read_text()) == checkpoint
        raw = json.dumps(checkpoint, sort_keys=True, separators=(',', ':')).encode()
        assert hashlib.sha256(raw).hexdigest() == report[f'{which}_sha256']
    signs = tuple(case.get('body_signs', (1, 1, 1)))
    reference = matrix_coupling(signs)
    engine = Engine(Coupling(signs))
    detector = [tuple(address) for address in report['locations']['detector']]
    source_initial, initial = None, None
    previous, old_memory = None, None
    records, arithmetic = [], []
    margin = case['side']
    period_states = []
    for t, (checkpoint, row) in enumerate(zip(checkpoints, report['trace'])):
        cp = checkpoint['experiment']
        assert checkpoint['completed_steps'] == row['step'] == t
        assert cp['side'] == case['side']
        assert tuple(cp['coupling_signs']) == signs
        assert checkpoint['coupling_fingerprint'] == engine.coupling.fingerprint
        cells = {(*entry['position'], entry['channel']): tuple(entry['state'])
                 for entry in cp['seed_changes']}
        assert len(cells) == len(cp['seed_changes'])
        state = State(Cube(cp['side']), Channel(*cp['background']), cells)
        if initial is None:
            initial = state
            if 'channel' in case and 'source_offsets' not in case:
                origin = (case['side']//2,)*3
                g = case['channel']
                source_initial = State(Cube(case['side']), Channel(0, 0, 2),
                                       {(*origin, g): Channel(0, 1, 2)})
                locations = {'detector': [(*origin, g), (*origin, (g+1) % 48)]}
            elif 'variants' in case:
                source_initial = independently_prepared_fork(case)
                origin = (case['side']//2,)*3
                locations = {'detector': [(*origin, 0), (*origin, 14)]}
            else:
                _, source_initial, locations = prepare(case, tuple(report['source_mask']))
            assert state == source_initial
            assert detector == locations['detector']
            initial_margin = min(min(c, case['side']-1-c)
                                 for address in cells for c in address[:3])
            assert initial_margin == report['initial_boundary_margin']
            assert initial_margin > case['steps']
        else:
            assert independent_gather(previous, signs) == state, (folder, t)
            assert engine.rewind(state) == previous
        if cells:
            margin = min(margin, min(min(c, case['side']-1-c)
                                    for address in cells for c in address[:3]))
        triples = [state.at(address) for address in detector]
        memory = [triple.r for triple in triples]
        assert row['memory'] == memory
        assert row['detector'] == [list(triple) for triple in triples]
        expected_inputs, expected_terms = [], []
        for x, y, z, channel in detector:
            terms = []
            for d, (dx, dy, dz) in enumerate(DIRECTIONS):
                address = ((x+dx) % state.cube.side, (y+dy) % state.cube.side,
                           (z+dz) % state.cube.side, reference.ports[d][channel])
                terms.append({'direction': d, 'address': list(address),
                              'weight': reference.weights[d][channel],
                              'b': state.at(address).b})
            expected_terms.append(terms)
            expected_inputs.append(sum(term['weight']*term['b'] for term in terms))
        assert row['next_input'] == expected_inputs
        assert row['six_inputs'] == expected_terms
        step_arithmetic = []
        if previous is not None:
            if memory != old_memory:
                records.append(t)
            for address, new in zip(detector, triples):
                old = previous.at(address)
                quotient = new.b+old.a
                if quotient and new != old:
                    step_arithmetic.append({'step': t, 'address': list(address),
                        'kind': ((new.r-old.r)//2) % 3, 'quotient': quotient})
            arithmetic.extend(step_arithmetic)
        assert row['arithmetic_events'] == step_arithmetic
        previous, old_memory = state, memory
        if 'channel' in case and 'source_offsets' not in case:
            if period_states:
                prior = period_states[-1]
                assert all(state.at(address).b+prior.at(address).a == 0
                           for address in prior.cells.keys() | state.cells.keys())
            period_states.append(state)
    assert report['record_event_times'] == records
    assert report['arithmetic_events'] == arithmetic
    assert report['minimum_boundary_margin'] == margin
    assert report['entire_board_stationary'] == all(
        checkpoint['experiment']['seed_changes'] == checkpoints[0]['experiment']['seed_changes']
        for checkpoint in checkpoints)
    assert report['inverse_audited'] is True
    assert report['all_one_step_inverses'] is True
    assert report['complete_rewind'] is True
    rewound = previous
    for _ in range(case['steps']):
        rewound = engine.rewind(rewound)
    assert rewound == initial
    if period_states:
        assert all(state != initial for state in period_states[1:4])
        assert all(period_states[t] == period_states[t-4] for t in range(4, len(period_states)))
        assert not arithmetic
    return {'path': str(folder), 'frames': len(checkpoints),
            'independent_full_state_transitions': len(checkpoints)-1,
            'record_event_times': records,
            'arithmetic_event_times': sorted({event['step'] for event in arithmetic}),
            'states_sha256': hashlib.sha256((folder/'states.jsonl').read_bytes()).hexdigest(),
            'passed': True}


def independently_prepared_fork(case):
    """Construct the frozen fork specification without its production generator."""
    origin = (case['side']//2,)*3
    cells = {}
    for index, sign in enumerate((-1, 1)):
        if 'isolated_side' in case and case['isolated_side'] != sign:
            continue
        for distance in range(1, 7):
            position = (origin[0]+sign*distance, origin[1], origin[2])
            if isinstance(case['variants'][index], str):
                pairs = {'O': (4, 0), 'N': (2, 2), 'R': (0, 4)}
                pair = pairs[case['variants'][index]] if distance in (2, 3) else pairs['O']
                for g, r in zip((0, 14), pair):
                    cells[(*position, g)] = (0, 0, r)
                continue
            r = case['variants'][index] if distance in (2, 3) else 4
            if sign == case.get('test_side') and distance in case.get('flips', []):
                r = (r+2) % 6
            cells[(*position, 0)] = (0, 0, r)
            cells[(*position, 14)] = (0, 0, 0)
    probe = case.get('probe', {'source_at_origin': {'0': (0, 1, 2), '14': (0, -1, 2)}})
    for channel, triple in probe['source_at_origin'].items():
        a, b, r = triple
        cells[(*origin, int(channel))] = (a, b, r) if case['source_present'] else (0, 0, r)
    return State(Cube(case['side']), Channel(0, 0, 2), cells)


def audit_cooperation(folder):
    """Recompute all frozen calibration scores and held-out outlet decisions."""
    folder = Path(folder)
    report = json.loads((folder/'result.json').read_text())
    manifest = json.loads((folder/'candidate_manifest.json').read_text())
    protocol = json.loads((folder/'protocol.json').read_text())
    assert protocol['budget']['run_count'] == len(manifest['cases']) == 54
    assert protocol['heldout']['output_window'] == [10, 15]
    states, full_audits = {}, []
    for case in manifest['cases']:
        path = folder/'cases'/case['id']
        full_audits.append(audit_retained_case(path))
        saved = json.loads((path/'result.json').read_text())
        assert saved['preparation'] == case
        states[case['id']] = []
        for line in (path/'states.jsonl').read_text().splitlines():
            cp = json.loads(line)['experiment']
            cells = {(*e['position'], e['channel']): tuple(e['state']) for e in cp['seed_changes']}
            states[case['id']].append(State(Cube(cp['side']), Channel(*cp['background']), cells))
    def output(identifier, sign, lo, hi):
        series = states[identifier]
        middle = series[0].cube.side//2
        position = (middle+6*sign, middle, middle)
        return [series[t].at((*position, g)).b for t in range(lo, hi+1) for g in range(48)]
    scores = {}
    saved_scores = json.loads((folder/'calibration_scores.json').read_text())
    assert saved_scores == report['calibration_scores']
    for sign in (-1, 1):
        for variant in (0, 2, 4):
            vectors = {subset: output(f'cal-{sign}-{variant}-{subset}', sign, 6, 9)
                       for subset in ('none', 'i', 'j', 'ij')}
            mixed = [both-first-second+base for both, first, second, base in zip(
                vectors['ij'], vectors['i'], vectors['j'], vectors['none'])]
            score = int(any(mixed))
            scores[sign, variant] = score
            saved = saved_scores[f'{sign},{variant}']
            assert saved['vectors'] == vectors and int(saved['score']) == score
            assert saved['nonzero_pairs'] == ([[0, 1]] if score else [])
    reference = matrix_coupling((1, 1, 1))
    def terms(state, address):
        x, y, z, g = address
        result = []
        for d, (dx, dy, dz) in enumerate(DIRECTIONS):
            source = ((x+dx) % state.cube.side, (y+dy) % state.cube.side,
                      (z+dz) % state.cube.side, reference.ports[d][g])
            result.append({'direction': d, 'address': list(source),
                           'weight': reference.weights[d][g], 'b': state.at(source).b})
        return result
    categories = {}
    for comparison in report['comparisons']:
        left, right = comparison['variants']
        probe = comparison['probe']
        identifier = comparison['id']
        control = f'null-{left}-{right}'
        assert all(state == states[control][0] for state in states[control])
        pair_scores = [scores[-1, left], scores[1, right]]
        assert pair_scores == comparison['scores']
        vectors, isolated = {}, {}
        for sign, variant in ((-1, left), (1, right)):
            signal, baseline = output(identifier, sign, 10, 15), output(control, sign, 10, 15)
            vectors[str(sign)] = [a-b for a, b in zip(signal, baseline)]
            isolated[str(sign)] = output(f'isolated-{sign}-{variant}-{probe}', sign, 10, 15)
            assert comparison['early_b_vectors'][str(sign)] == output(identifier, sign, 6, 9)
        assert comparison['late_probe_induced_b_vectors'] == vectors
        assert comparison['late_isolated_b_vectors'] == isolated
        eligible = pair_scores[0] != pair_scores[1]
        high = -1 if pair_scores[0] > pair_scores[1] else 1
        low = -high
        active = {sign: any(vector) for sign, vector in vectors.items()}
        strict = eligible and active[str(high)] and not active[str(low)]
        suppressed = eligible and not active[str(low)] and any(isolated[str(low)])
        witnesses = []
        if eligible:
            joint = states[identifier]
            separate = states[f'isolated-{low}-{left if low < 0 else right}-{probe}']
            middle = joint[0].cube.side//2
            for t in range(10, 16):
                for g in range(48):
                    address = (middle+low*6, middle, middle, g)
                    old, new = joint[t-1].at(address), joint[t].at(address)
                    if old.a or old.b or new.b:
                        continue
                    jt = terms(joint[t-1], address)
                    products = [term['weight']*term['b'] for term in jt]
                    if sum(products) or not any(products):
                        continue
                    it = terms(separate[t-1], address)
                    iu = sum(term['weight']*term['b'] for term in it)
                    io, inn = separate[t-1].at(address), separate[t].at(address)
                    if not iu or not inn.b:
                        continue
                    witnesses.append({'step': t, 'address': list(address),
                        'joint': {'old': list(old), 'next': list(new), 'u': 0,
                                  'ell': new.b+old.a, 'terms': jt},
                        'isolated': {'old': list(io), 'next': list(inn), 'u': iu,
                                     'ell': inn.b+io.a, 'terms': it}})
        assert comparison['input_cancellation_witnesses'] == witnesses
        category = ('tie' if not eligible else 'higher_only' if strict else
                    'both_transmit' if all(active.values()) else
                    'both_quiet' if not any(active.values()) else 'lower_only')
        assert comparison['category'] == category
        assert comparison['strict_higher_score_only'] == strict
        assert comparison['isolated_to_joint_suppression'] == suppressed
        assert comparison['strong_cancellation_selection'] == (strict and suppressed and bool(witnesses))
        categories[category] = categories.get(category, 0)+1
    summary = report['summary']
    assert summary['runs_completed'] == summary['runs_registered'] == 54
    assert summary['forward_steps'] == sum(a['independent_full_state_transitions'] for a in full_audits) == 666
    assert summary['eligible_comparisons'] == 12-categories.get('tie', 0)
    assert summary['ties'] == categories.get('tie', 0)
    assert summary['strict_higher_only'] == categories.get('higher_only', 0)
    assert summary['strong_cancellation_selection'] == sum(c['strong_cancellation_selection'] for c in report['comparisons'])
    return {'passed': True, 'cases': full_audits,
            'calibration_scores': {f'{sign},{v}': score for (sign, v), score in scores.items()},
            'categories': categories, 'independent_full_state_transitions': 666,
            'result_sha256': hashlib.sha256((folder/'result.json').read_bytes()).hexdigest()}


def audit_toggle_confirmation(folder):
    """Verify the fresh, narrower two-symbol protocol without changing v2."""
    folder = Path(folder)
    result = json.loads((folder/'result.json').read_text())
    protocol = json.loads((folder/'protocol.json').read_text())
    assert protocol['protocol_id'] == 'U24-SIGNAL-TOGGLE-CONFIRM-v1'
    assert protocol['preparation']['horizon'] == 40
    groups, cases = [], []
    for d1, d2 in protocol['preparation']['fresh_distance_pairs']:
        runs = {}
        for mask in ('00', '10', '01', '11'):
            path = folder/'cases'/f'toggle-{d1}-{d2}-s{mask}'
            cases.append(audit_retained_case(path))
            run = json.loads((path/'result.json').read_text())
            case = run['preparation']
            assert case['side'] == 201 and case['steps'] == 40
            assert case['source_offsets'] == [-d1, d2]
            assert case['target_remainders'] == [4, 0]
            assert case['source_ab'] == [[0, 1], [0, 1]]
            assert case['guide_mode'] == 'between_sources'
            assert run['source_mask'] == [digit == '1' for digit in mask]
            times = {'00': [], '10': [d1], '01': [d2], '11': [d1, d2+2]}[mask]
            assert run['record_event_times'] == times
            assert sorted({e['step'] for e in run['arithmetic_events']}) == times
            for row in run['trace']:
                writes = sum(t <= row['step'] for t in times)
                assert row['memory'] == ([0, 4] if writes % 2 else [4, 0])
            quiet = set()
            if times:
                quiet.update(range(times[0]-4, times[0]-1))
                for t in times:
                    quiet.update(range(t, t+4))
                    assert run['trace'][t-1]['next_input'] != [0, 0]
            assert all(run['trace'][t]['next_input'] == [0, 0] for t in quiet)
            if mask == '00':
                assert run['entire_board_stationary']
            runs[mask] = run
        both = runs['11']['trace']
        assert both[d1-1]['next_input'] != runs['01']['trace'][d1-1]['next_input']
        assert both[d2+1]['next_input'] != runs['10']['trace'][d2+1]['next_input']
        changed_terms = [t for t in range(40)
                         if both[t]['six_inputs'] != runs['10']['trace'][t]['six_inputs']]
        changed_sums = [t for t in range(40)
                        if both[t]['next_input'] != runs['10']['trace'][t]['next_input']]
        actual = next(g for g in result['groups'] if g['distance_pair'] == [d1, d2])
        assert actual['passed'] is True and actual['event_source_counterfactuals'] == [True, True]
        evidence = actual['second_source_input_evidence']
        assert evidence['first_six_term_difference_old_step'] == changed_terms[0]
        assert evidence['all_old_steps_with_term_differences'] == changed_terms
        assert evidence['first_net_input_difference_old_step'] == changed_sums[0]
        assert evidence['joint_arrival_terms'] == both[d2-1]['six_inputs']
        assert evidence['source1_only_arrival_terms'] == runs['10']['trace'][d2-1]['six_inputs']
        # This extra magnitude readout was noticed after search. Retain it as
        # exploratory data; it cannot retrospectively become an acceptance test.
        magnitudes = [[a*a+b*b for a, b, r in row['detector']] for row in both]
        groups.append({'distance_pair': [d1, d2], 'passed': True,
                       'ticks': [d1, d2+2],
                       'second_source_first_input_term_difference_old_step': changed_terms[0],
                       'second_source_first_net_difference_old_step': changed_sums[0],
                       'terms_at_naive_arrival_same_as_source1_only':
                           both[d2-1]['six_inputs'] == runs['10']['trace'][d2-1]['six_inputs'],
                       'posthoc_counter_magnitude_diagnostic': {
                           'definition': 'a*a+b*b separately at each detector channel; not energy.',
                           'not_a_preregistered_acceptance_rule': True,
                           'levels_at_initial_and_two_ticks': [magnitudes[t] for t in (0, d1, d2+2)],
                           'change_times': [t for t in range(1, 41) if magnitudes[t] != magnitudes[t-1]]}})
    assert len(cases) == 12
    assert sum(c['independent_full_state_transitions'] for c in cases) == 480
    return {'passed': True, 'scope': 'Fresh two-symbol toggle confirmation; original three-symbol protocol remains failed.',
            'cases': cases, 'groups': groups, 'independent_full_state_transitions': 480,
            'result_sha256': hashlib.sha256((folder/'result.json').read_bytes()).hexdigest()}


def audit_counter_memory(folder):
    folder = Path(folder)
    report = json.loads((folder/'result.json').read_text())
    protocol = json.loads((folder/'protocol.json').read_text())
    assert protocol['protocol_id'] == 'U24-COUNTER-MEMORY-CONFIRM-v1'
    cases, groups = [], []
    for d1, d2 in protocol['preparation']['distance_pairs']:
        runs = {}
        for mask in ('00', '10', '01', '11'):
            path = folder/'cases'/f'counter-memory-{d1}-{d2}-s{mask}'
            cases.append(audit_retained_case(path))
            run = json.loads((path/'result.json').read_text())
            case = run['preparation']
            assert case['side'] == 221 and case['steps'] == 48
            assert case['source_offsets'] == [-d1, d2]
            assert case['source_ab'] == [[0, 1], [0, 1]]
            assert case['target_remainders'] == [4, 0]
            assert case['guide_mode'] == 'between_sources'
            assert run['source_mask'] == [digit == '1' for digit in mask]
            times = {'00': [], '10': [d1], '01': [d2], '11': [d1, d2+2]}[mask]
            assert run['record_event_times'] == times
            assert sorted({e['step'] for e in run['arithmetic_events']}) == times
            magnitudes = []
            for row in run['trace']:
                t = row['step']
                writes = sum(tick <= t for tick in times)
                expected = [0, 1, 4][writes]
                values = [a*a+b*b for a, b, _ in row['detector']]
                magnitudes.append(values)
                assert values == [expected, expected]
                assert row['memory'] == ([0, 4] if writes % 2 else [4, 0])
            for before, after in zip(run['trace'], run['trace'][1:]):
                for (a, b, r), (na, nb, nr) in zip(before['detector'], after['detector']):
                    carry = nb+a
                    assert na*na+nb*nb-a*a-b*b == carry*carry-2*a*carry
            quiet = set()
            if times:
                quiet.update(range(times[0]-4, times[0]-1))
                for tick in times:
                    quiet.update(range(tick, tick+4))
                    assert run['trace'][tick-1]['next_input'] != [0, 0]
            assert all(run['trace'][t]['next_input'] == [0, 0] for t in quiet)
            if mask == '00':
                assert run['entire_board_stationary']
            claimed = next(g for g in report['groups'] if g['distance_pair'] == [d1, d2])['runs'][mask]
            assert claimed['magnitudes'] == magnitudes and claimed['passed']
            runs[mask] = run
        both = runs['11']['trace']
        assert both[d1-1]['next_input'] != runs['01']['trace'][d1-1]['next_input']
        assert both[d2+1]['next_input'] != runs['10']['trace'][d2+1]['next_input']
        first_terms = next(t for t in range(48) if both[t]['six_inputs'] != runs['10']['trace'][t]['six_inputs'])
        first_sum = next(t for t in range(48) if both[t]['next_input'] != runs['10']['trace'][t]['next_input'])
        groups.append({'distance_pair': [d1, d2], 'ticks': [d1, d2+2], 'passed': True,
                       'magnitude_levels': [0, 1, 4], 'retained_through': 48,
                       'first_second_source_term_difference_old_step': first_terms,
                       'first_second_source_net_difference_old_step': first_sum})
    assert len(cases) == 8
    assert report['summary']['passed'] and report['summary']['forward_steps'] == 384
    return {'passed': True, 'cases': cases, 'groups': groups,
            'independent_full_state_transitions': 384,
            'phase_scope': 'Registered gaps 8 and 12; no arbitrary-phase or indefinitely reusable count claim.',
            'result_sha256': hashlib.sha256((folder/'result.json').read_bytes()).hexdigest()}


def audit_paired_blocker(folder):
    folder = Path(folder)
    report = json.loads((folder/'result.json').read_text())
    manifest = json.loads((folder/'candidate_manifest.json').read_text())
    assert len(manifest['cases']) == 24
    states, audits = {}, []
    for case in manifest['cases']:
        path = folder/'cases'/case['id']
        audits.append(audit_retained_case(path))
        states[case['id']] = []
        for line in (path/'states.jsonl').read_text().splitlines():
            cp = json.loads(line)['experiment']
            cells = {(*e['position'], e['channel']): tuple(e['state']) for e in cp['seed_changes']}
            states[case['id']].append(State(Cube(cp['side']), Channel(*cp['background']), cells))
    observations = {}
    for case in manifest['cases']:
        if not case['source_present']:
            assert all(state == states[case['id']][0] for state in states[case['id']])
            continue
        series = states[case['id']]
        if case['kind'] == 'joint':
            baseline = states[f'paired-{case["variants"][0]}-{case["variants"][1]}-s0']
            signs = (-1, 1)
        else:
            quiet_case = dict(case, source_present=False)
            quiet = independently_prepared_fork(quiet_case)
            baseline = [quiet]*41
            signs = (case['isolated_side'],)
        observations[case['id']] = {}
        for sign in signs:
            position = (50+6*sign, 50, 50)
            first, deltas = None, []
            for t in range(6, 41):
                row = []
                for g in range(48):
                    actual = series[t].at((*position, g))
                    absent = baseline[t].at((*position, g))
                    diff = [a-b for a, b in zip(actual, absent)]
                    row.append(diff)
                    if first is None and any(diff):
                        component = next(i for i, value in enumerate(diff) if value)
                        first = {'step': t, 'channel': g, 'component': 'abr'[component],
                                 'difference': diff[component], 'actual': list(actual),
                                 'baseline': list(absent)}
                deltas.append(row)
            transmitted = any(triple[1] for row in deltas for triple in row)
            observed = {'counter_transmission': transmitted, 'weak_b_block': not transmitted,
                        'strong_complete_outlet_block': first is None, 'first_leak': first,
                        'window': [6, 40], 'all_48_delta_triples': deltas}
            assert report['observations'][case['id']][str(sign)] == observed
            observations[case['id']][str(sign)] = observed
    for sign in (-1, 1):
        assert observations[f'paired-isolated-{sign}-O'][str(sign)]['counter_transmission']
        assert observations[f'paired-isolated-{sign}-N'][str(sign)]['strong_complete_outlet_block']
    assert observations['paired-O-N-s1']['-1']['counter_transmission']
    assert observations['paired-O-N-s1']['1']['strong_complete_outlet_block']
    assert observations['paired-N-O-s1']['1']['counter_transmission']
    assert observations['paired-N-O-s1']['-1']['strong_complete_outlet_block']
    reference = matrix_coupling((1, 1, 1))
    def input_terms(state, address):
        x, y, z, g = address
        return [reference.weights[d][g]*state.at(((x+dx) % state.cube.side,
                 (y+dy) % state.cube.side, (z+dz) % state.cube.side,
                 reference.ports[d][g])).b for d, (dx, dy, dz) in enumerate(DIRECTIONS)]
    suppression = []
    for case in manifest['cases']:
        if case['kind'] != 'joint' or not case['source_present']:
            continue
        for sign, label in zip((-1, 1), case['variants']):
            isolated = f'paired-isolated-{sign}-{label}'
            active = observations[isolated][str(sign)]['counter_transmission']
            quiet = observations[case['id']][str(sign)]['strong_complete_outlet_block']
            if not (active and quiet):
                continue
            witnesses = []
            for t in range(6, 41):
                for g in range(48):
                    address = (50+6*sign, 50, 50, g)
                    old, new = states[case['id']][t-1].at(address), states[case['id']][t].at(address)
                    if old.a or old.b or new.b:
                        continue
                    products = input_terms(states[case['id']][t-1], address)
                    if sum(products) == 0 and any(products):
                        isolated_u = sum(input_terms(states[isolated][t-1], address))
                        if isolated_u and states[isolated][t].at(address).b:
                            witnesses.append((t, g))
            # These retained runs have no exact local cancellation witness.
            assert not witnesses
            suppression.append((case['id'], isolated, sign))
    assert len(suppression) == 6
    assert {(e['joint'], e['isolated'], e['side']) for e in report['cancellation']} == set(suppression)
    assert all(not e['input_witnesses'] and not e['demonstrated_input_cancellation'] for e in report['cancellation'])
    assert report['summary']['overall_passed'] and report['summary']['forward_steps'] == 960
    return {'passed': True, 'cases': audits, 'independent_full_state_transitions': 960,
            'full_outlet_comparison': 'All48 complete (a,b,r) triples against source-absent state at every step6..40.',
            'isolated_open_and_neutral_block': True, 'both_orientation_compositions': True,
            'isolated_active_to_joint_quiet_cases': 6, 'local_input_cancellation_witnesses': 0,
            'written_memory_router_proven': False,
            'result_sha256': hashlib.sha256((folder/'result.json').read_bytes()).hexdigest()}


def audit_search_summary(folder):
    """Check all saved local arithmetic/verdicts, not unstored full search states."""
    folder = Path(folder)
    data = json.loads((folder/'search_results.json').read_text())
    manifest = json.loads((folder/'candidate_manifest.json').read_text())
    summary = data['summary']
    assert summary['candidates_completed'] == len(data['candidates'])
    assert summary['candidates_total'] == manifest['candidate_count']
    assert summary['candidates_completed'] == summary['candidates_total']
    assert [entry['case'] for entry in data['candidates']] == manifest['candidates']
    masks = [(False, False), (True, False), (False, True), (True, True)]
    counts = {'record': 0, 'guarded': 0}
    transitions, unique_initials = 0, set()
    for entry in data['candidates']:
        case, runs = entry['case'], entry['runs']
        assert len(runs) == 4
        checks = []
        for mask, run in zip(masks, runs):
            assert tuple(run['source_mask']) == mask
            rows = run['detector_trace']
            assert len(rows) == case['steps']+1
            assert [row[0] for row in rows] == list(range(len(rows)))
            assert rows[0][1:3] == case['target_remainders']
            pair = [(0, 0, r) for r in case['target_remainders']]
            events, arithmetic = [], []
            origin = [case['side']//2]*3
            for t in range(1, len(rows)):
                following = []
                for index, (a, b, r) in enumerate(pair):
                    u = rows[t-1][3+index]
                    q, remainder = divmod(2*u+r, 6)
                    new = (b, q-a, remainder)
                    following.append(new)
                    if q and new != (a, b, r):
                        arithmetic.append({'step': t, 'address': origin+[0 if index == 0 else 14],
                                           'kind': u % 3, 'quotient': q})
                assert [new[2] for new in following] == rows[t][1:3]
                if rows[t][1:3] != rows[t-1][1:3]:
                    events.append(t)
                pair = following
            assert events == run['record_event_times']
            assert arithmetic == run['arithmetic_events']
            unique_initials.add((run['initial_sha256'], case['steps']))
            transitions += case['steps']
            windows = [w for enabled, w in zip(mask, case['arrival_windows']) if enabled]
            correct = len(events) == len(windows)
            arrivals = correct and all(lo <= t <= hi for t, (lo, hi) in zip(events, windows))
            symbols = [tuple(rows[0][1:3])] + [tuple(rows[t][1:3]) for t in events]
            distinct = correct and len(set(symbols)) == len(windows)+1
            spacing = correct and (not events or (
                events[0] >= 4 and all(b-a >= 5 for a, b in zip(events, events[1:]))
                and case['steps']-events[-1] >= 4))
            quiet = set()
            if events:
                quiet.update(range(events[0]-4, events[0]-1))
                for t in events:
                    quiet.update(range(t, t+4))
            quiet_ok = all(0 <= t < case['steps'] and rows[t][3:5] == [0, 0] for t in quiet)
            incident = all(rows[t-1][3:5] != [0, 0] for t in events)
            record = all((correct, arrivals, distinct, spacing, quiet_ok, incident,
                          run['initial_boundary_margin'] > case['steps']))
            c_times = {e['step'] for e in arithmetic}
            guarded = record and c_times == set(events)
            claimed = entry['verdict']['controls'][str(mask)]
            assert claimed['record_milestone_passed'] == record
            assert claimed['guarded_click_milestone_passed'] == guarded
            checks.append((record, guarded))
        both_events = runs[3]['record_event_times'][:2]
        counterfactual = [runs[3]['detector_trace'][t-1][3:5] !=
                          runs[2 if i == 0 else 1]['detector_trace'][t-1][3:5]
                          for i, t in enumerate(both_events)]
        independent = len(counterfactual) == 2 and all(counterfactual)
        stationary = runs[0]['entire_board_stationary']
        inverses = all(run['all_one_step_inverses'] and run['complete_rewind'] for run in runs)
        record_group = stationary and inverses and independent and all(c[0] for c in checks)
        guarded_group = stationary and inverses and independent and all(c[1] for c in checks)
        assert entry['verdict']['record_only_criteria_passed'] == record_group
        assert entry['verdict']['guarded_click_criteria_passed'] == guarded_group
        counts['record'] += record_group
        counts['guarded'] += guarded_group
    assert counts['record'] == summary['record_only_candidates']
    assert counts['guarded'] == summary['guarded_click_candidates']
    assert len(unique_initials) == summary['unique_audited_trajectories']
    assert sum(steps for _, steps in unique_initials) == summary['audited_forward_steps']
    return {'scope': 'All saved detector recurrences and criterion decisions; full search states were not retained.',
            'candidates': len(data['candidates']), 'local_trajectory_views': 4*len(data['candidates']),
            'local_transition_views': transitions,
            'record_candidates': counts['record'], 'guarded_candidates': counts['guarded'],
            'unique_engine_audited_trajectories': len(unique_initials),
            'search_results_sha256': hashlib.sha256((folder/'search_results.json').read_bytes()).hexdigest(),
            'passed': True}


class SignalClockIndependentReviewTests(unittest.TestCase):
    def test_one_unit_source_has_period_four_without_any_guarded_click(self):
        from universe24.observation.clicks import clicks
        phases = ((0, 1), (1, 0), (0, -1), (-1, 0))
        for signs in product((-1, 1), repeat=3):
            reference = matrix_coupling(signs)
            engine = Engine(Coupling(signs))
            inverse_ports = [{sender: receiver for receiver, sender in enumerate(row)}
                             for row in reference.ports]
            for side in (3, 5):
                origin = (side//2,)*3
                for channel in range(48):
                    source = (*origin, channel)
                    initial = State(Cube(side), Channel(0, 0, 2),
                                    {source: Channel(0, 1, 2)})
                    recipients = {}
                    for d, direction in enumerate(DIRECTIONS):
                        receiver = inverse_ports[d][channel]
                        address = (*tuple((x-dx) % side for x, dx in zip(origin, direction)),
                                   receiver)
                        recipients[address] = reference.weights[d][receiver]
                    self.assertEqual(len(recipients), 6)
                    state = initial
                    for step in range(1, 5):
                        new = engine.advance(state)
                        a, b = phases[step % 4]
                        cells = {source: Channel(a, b, 2)}
                        if step % 4 in (1, 2):
                            cells.update({address: Channel(0, 0, 2+2*weight)
                                          for address, weight in recipients.items()})
                        expected = State(initial.cube, initial.background, cells)
                        self.assertEqual(new, expected)
                        self.assertEqual(list(clicks(state, new, step)), [])
                        self.assertTrue(all(new.at(address).b+state.at(address).a == 0
                                            for address in state.cells.keys() | new.cells.keys()))
                        self.assertEqual(engine.rewind(new), state)
                        if step < 4:
                            self.assertNotEqual(new, initial)
                        state = new
                    self.assertEqual(state, initial)

    def test_retained_audit_rejects_hidden_state_and_input_corruption(self):
        case = {'id': 'independent-retained', 'side': 101, 'extent': 20,
                'steps': 12, 'source_offsets': [-4, 10],
                'source_ab': [(0, 1), (1, 0)],
                'target_remainders': [2, 2], 'body_signs': [1, 1, 1]}
        scratch = Path(__file__).resolve().parents[1]/'runs'
        scratch.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='signal-review-', dir=scratch) as tmp:
            folder = Path(tmp)/'case'
            run_case(case, (True, True), deadline_cpu=time.process_time()+30,
                     audit=True, output=folder)
            verified = audit_retained_case(folder)
            self.assertEqual(verified['independent_full_state_transitions'], 12)
            path = folder/'states.jsonl'
            original = path.read_text()
            checkpoints = [json.loads(line) for line in original.splitlines()]
            checkpoints[1]['experiment']['seed_changes'].append(
                {'position': [2, 3, 4], 'channel': 47, 'state': [0, 0, 3]})
            path.write_text('\n'.join(json.dumps(c) for c in checkpoints)+'\n')
            with self.assertRaises(AssertionError):
                audit_retained_case(folder)
            path.write_text(original)
            result_path = folder/'result.json'
            result = json.loads(result_path.read_text())
            result['trace'][3]['six_inputs'][0][0]['b'] += 1
            result_path.write_text(json.dumps(result))
            with self.assertRaises(AssertionError):
                audit_retained_case(folder)

    def test_four_prearrival_states_are_not_five(self):
        fixture = synthetic_record()
        self.assertTrue(waiting_verdict(fixture, [(4, 5), (10, 11)])[
            'record_milestone_passed'])

    def test_silent_record_edges_do_not_satisfy_the_guarded_click_goal(self):
        fixture = synthetic_record()
        verdict = waiting_verdict(fixture, [(4, 5), (10, 11)])
        self.assertTrue(verdict['record_milestone_passed'])
        self.assertFalse(verdict['guarded_click_milestone_passed'])

    def test_observed_empty_boundary_does_not_certify_causal_margin(self):
        fixture = synthetic_record(initial_margin=16)
        fixture['minimum_boundary_margin'] = 1
        self.assertFalse(waiting_verdict(fixture, [(4, 5), (10, 11)])['passed'])

    def test_unsampled_declared_horizon_cannot_pass(self):
        fixture = synthetic_record()
        fixture['preparation']['steps'] = 32
        self.assertFalse(waiting_verdict(fixture, [(4, 5), (10, 11)])['passed'])

    def test_an_extra_memory_edge_cannot_be_observer_gated_away(self):
        fixture = synthetic_record(event_times=(4, 10, 15))
        self.assertFalse(waiting_verdict(fixture, [(4, 5), (10, 11)])['passed'])

    def test_new_preparation_masks_change_only_initial_source_counters(self):
        case = {'id': 'independent-mask', 'side': 101, 'extent': 20,
                'steps': 16, 'source_offsets': [-4, 10],
                'source_ab': [(0, 1), (1, 0)],
                'target_remainders': [2, 2], 'body_signs': [1, 1, 1]}
        _, both, locations = prepare(case, (True, True))
        for mask in product((False, True), repeat=2):
            engine, initial, found = prepare(case, mask)
            self.assertEqual(found, locations)
            expected = dict(both.cells)
            for enabled, position in zip(mask, locations['sources']):
                if not enabled:
                    for channel in (0, 14):
                        address = (*position, channel)
                        expected[address] = Channel(0, 0, both.at(address).r)
            self.assertEqual(initial, State(both.cube, both.background, expected))
            # Separate matrix gather, production full inverse, all sparse
            # remainders retained. This finite interface check claims no pass
            # of the two-arrival scientific criterion.
            state = initial
            for _ in range(12):
                expected_state = independent_gather(state, case['body_signs'])
                actual = engine.advance(state)
                self.assertEqual(actual, expected_state)
                self.assertEqual(engine.rewind(actual), state)
                state = actual
            for _ in range(12):
                state = engine.rewind(state)
            self.assertEqual(state, initial)

    def test_remainder_writes_and_arithmetic_clicks_are_distinct(self):
        from universe24.core.rule3 import forward
        from universe24.observation.clicks import classify
        rest = Channel(0, 0, 0)
        silent_write = forward(rest, 1)
        carry_without_remainder_write = forward(rest, 3)
        self.assertEqual(silent_write, Channel(0, 0, 2))
        self.assertIsNone(classify(rest, silent_write))
        self.assertEqual(carry_without_remainder_write, Channel(0, 1, 0))
        self.assertEqual(classify(rest, carry_without_remainder_write), (0, 1))


if __name__ == '__main__':
    unittest.main()
