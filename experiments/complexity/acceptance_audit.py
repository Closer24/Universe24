"""Read-only complexity acceptance controls; no Engine feedback or resets.

The original recurrent-bursts-v1 thresholds are unchanged. Unknown evidence
is never promoted to a passing causal or quantum mechanism.
"""
import argparse
from collections import deque
from functools import reduce
from fractions import Fraction
from itertools import combinations_with_replacement, product
from math import gcd
import gzip
import hashlib
import json
from pathlib import Path
from random import Random

import numpy as np
from universe24.core import Engine, State, Tensor
from experiments.cosmology.recurrent_bursts import run_case
from experiments.quantum.bell_cone_audit import audit as bell_audit


KEYS = ('site_pattern_types', 'edge_pattern_types', 'persistent_pattern_types')


def structure(state, rows, old=()):
    """Independent exact implementation of the already frozen diagnostics."""
    signs = tuple(tuple(int(state.b[g, n] > 0)-int(state.b[g, n] < 0)
                        for g in rows) for n in range(state.N))
    weights = [sum(abs(int(state.b[g, n])) for g in rows) for n in range(state.N)]
    total = sum(weights)
    ball = max((sum(weights[j] for j in {n, *(state.lattice.neighbour(n, d)
                     for d in range(6))}) for n in range(state.N)), default=0)
    sites = {s for s in signs if any(s)}
    edges = {tuple(sorted((signs[n], signs[state.lattice.neighbour(n, d)])))
        for n in range(state.N) for d in (0, 2, 4)
        if any(signs[n]) or any(signs[state.lattice.neighbour(n, d)])}
    persistent = {s for n, s in enumerate(signs) if any(s) and len(old) == 2
                  and old[0][n] == old[1][n] == s}
    flat = [int(v) for g in rows for v in state.b[g]]
    scale = reduce(gcd, map(abs, flat), 0) or 1
    normalized = [v//scale for v in flat]
    return {'reference_mass': str(total), 'compact_ball_mass': str(ball),
        'compact': bool(total and 4*ball >= 3*total),
        'dispersed': bool(total and 2*ball < total),
        'site_pattern_types': len(sites), 'edge_pattern_types': len(edges),
        'persistent_pattern_types': len(persistent),
        'normalized_fingerprint': hashlib.sha256(json.dumps(normalized, separators=(',', ':')).encode()).hexdigest()}, signs


def cycles(samples):
    initial, dispersed, events = False, False, []
    for row in samples:
        if row['compact']:
            if not initial:
                initial = True
            elif dispersed:
                events.append(row)
            dispersed = False
        elif row['dispersed'] and initial:
            dispersed = True
    return events


def scoreboard(samples, *, rewind=None, local_causality=None,
               retained_past_affects_future=None, feedback_reassembly=None,
               stagnation_attribution=None, frozen_model=None,
               organization_controls=None):
    events = cycles(samples)
    vectors = [tuple(r[k] for k in KEYS) for r in events]
    growth = len(events) >= 4 and all(v[2] > 0 for v in vectors)
    growth = growth and all(all(b >= a for a, b in zip(left, right)) and left != right
                           for left, right in zip(vectors, vectors[1:]))
    values = {'four_reference_reassemblies': len(events) >= 4,
        'original_componentwise_growth_and_persistence': growth,
        'complete_rewind': rewind, 'local_causal_attribution': local_causality,
        'retained_past_affects_future': retained_past_affects_future,
        'feedback_changes_reference_reassemblies': feedback_reassembly,
        'stagnation_trigger_attribution': stagnation_attribution,
        'fixed_law_and_complete_preparation': frozen_model,
        'organization_distinguished_from_noise': organization_controls}
    statuses = {k: 'unknown' if v is None else 'pass' if v else 'fail' for k, v in values.items()}
    overall = 'fail' if 'fail' in statuses.values() else 'unknown' if 'unknown' in statuses.values() else 'pass'
    return {'reassembly_updates': [r['update'] for r in events],
        'reassembly_vectors': vectors, 'gates': statuses, 'complete_goal': overall}


def replay_case(directory):
    """Replay a cosmology-shaped exported run, rederive metrics and inverse."""
    directory = Path(directory)
    report = json.loads((directory/'report.json').read_text())
    tensor = Tensor.from_json((directory/'tensor.json').read_text(), strict_support=True)
    with gzip.open(directory/'initial.json.gz', 'rt') as f:
        seed = State.from_dict(json.load(f))
    with gzip.open(directory/'final.json.gz', 'rt') as f:
        final = State.from_dict(json.load(f))
    engine, state = Engine(tensor), seed.copy()
    rows = [g for g, name in enumerate(tensor.names) if name.startswith('ref.')]
    history, samples = deque(maxlen=2), []
    for tick, declared in enumerate(report['samples']):
        row, signs = structure(state, rows, tuple(history))
        history.append(signs)
        row['update'] = tick
        for key, value in row.items():
            if key in declared:
                assert declared[key] == value, (directory.name, tick, key, value, declared[key])
        samples.append(row)
        if tick < len(report['samples'])-1:
            state = engine.step(state)
    assert state.same_as(final)
    exact = engine.rewind(state, len(samples)-1).same_as(seed)
    assert exact
    result = scoreboard(samples, rewind=True, frozen_model=True)
    result.update(independent_metrics_verified=True, independently_replayed_updates=len(samples)-1,
                  full_final_state_matches=True, tensor_fingerprint=tensor.fingerprint,
                  maximum_counter_bits=report.get('maximum_counter_bits'))
    return result


def replay_trace(directory):
    """Verify every saved (a,b,r) against its fixed tensor, not report flags."""
    directory = Path(directory)
    tensor = Tensor.from_json((directory/'tensor.json').read_text(), strict_support=True)
    seed = State.from_dict(json.loads((directory/'seed.json').read_text()))
    engine, states = Engine(tensor), []
    for tick, line in enumerate((directory/'full_trace.jsonl').read_text().splitlines()):
        row = json.loads(line)
        assert row['microtick'] == tick
        state = State.from_dict(row['state'])
        assert state.same_as(seed if tick == 0 else engine.step(states[-1]))
        states.append(state)
    assert states and engine.rewind(states[-1], len(states)-1).same_as(seed)
    return {'steps_verified': len(states)-1, 'every_complete_snapshot_replayed': True,
        'complete_rewind': True, 'degree': tensor.rank-1,
        'single_edge_violations': len(tensor.support_violations())}, tensor, states


def audit_stagnation(directory):
    directory = Path(directory)
    labels = ('stagnant', 'changing', 'stagnant_label_swap', 'disconnected', 'unmarked')
    checked, tensors, traces = {}, {}, {}
    for label in labels:
        checked[label], tensors[label], traces[label] = replay_trace(directory/label)
    tensor = tensors['stagnant']
    g_message = tensor.gear_index('message.x')
    g_source = tensor.gear_index('source.x')
    g_alarm = tensor.gear_index('sensor.alarm')
    g_marker = tensor.gear_index('source.marker')
    for label in labels:
        engine = Engine(tensors[label])
        for state in traces[label]:
            a, b = state.a[g_source], state.b[g_source]
            assert np.all((a == 0) | (a == 1)) and np.all((b == 0) | (b == 1))
            expected = 3*state.b[g_marker]*(a == b)
            assert np.array_equal(engine.inputs(state)[g_alarm], expected)
    for label in ('changing', 'disconnected', 'unmarked'):
        assert all(not np.any(s.b[g_message]) for s in traces[label])
    assert any(np.any(s.b[g_message]) for s in traces['stagnant'])
    assert all(np.array_equal(a.b[g_message], b.b[g_message]) for a, b in
               zip(traces['stagnant'], traces['stagnant_label_swap']))
    assert all(np.array_equal(a.b[g_alarm], b.b[g_alarm]) for a, b in
               zip(traces['stagnant'], traces['disconnected']))
    left, right = traces['stagnant'], traces['changing']
    initial_changed = np.flatnonzero(np.any((left[0].a != right[0].a)
        | (left[0].b != right[0].b) | (left[0].r != right[0].r), axis=0))
    origins = [left[0].lattice.coords(int(n)) for n in initial_changed]
    for tick, (a, b) in enumerate(zip(left, right)):
        changed = np.flatnonzero(np.any((a.a != b.a) | (a.b != b.b) | (a.r != b.r), axis=0))
        for n in changed:
            xyz = a.lattice.coords(int(n))
            distance = min(sum(min(abs(x-y), a.L-abs(x-y)) for x, y in zip(xyz, origin)) for origin in origins)
            assert distance <= tick
    return {'cases': checked, 'local_history_equality_to_alarm_to_message': 'pass',
        'matched_source_label_and_disconnected_controls': 'pass',
        'complete_state_intervention_cone': 'pass',
        'structural_complexity_stagnation': 'fail: period-two input remains changing without structural growth',
        'reassembly_attribution': 'unknown: no reference reassembly mechanism in this prototype',
        'complete_recurrent_complexity_goal': 'not demonstrated'}


def audit_born(path):
    """Recompute all published weights and scalar clicks from exported phases."""
    report = json.loads(Path(path).read_text())
    vectors = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
    expected_phases = {p for n in (1, 2, 3) for p in combinations_with_replacement(range(6), n)}
    assert {tuple(b['phases']) for b in report['branches']} == expected_phases
    branches = []
    for b in report['branches']:
        phases = b['phases']
        x, y = (sum(vectors[p][i] for p in phases) for i in (0, 1))
        q = x*x+x*y+y*y
        assert q == b['q'] == b['pair_contrast']
        branches.append({'q': q, 'histories': len(phases), 'distinct_histories': len(set(phases)),
                         'persistent_pairs': len(phases)**2, 'pair_contrast': q})
    for key, declared in report['grid'].items():
        parts = key.split(':'); mode, metric = parts[:2]
        lam = Fraction(parts[2].split('=')[1]) if mode == 'postweight' else None
        checked, mismatches, maximum = 0, 0, Fraction(0)
        for a, b in product(branches, repeat=2):
            if a['q']+b['q'] == 0:
                continue
            expected = Fraction(a['q'], a['q']+b['q'])
            wa, wb = (a[metric], b[metric]) if mode == 'direct' else (
                a['q']*(1+lam*a[metric]), b['q']*(1+lam*b[metric]))
            error = abs(expected-Fraction(wa, wa+wb))
            checked += 1; mismatches += int(error != 0); maximum = max(maximum, error)
        assert (checked, mismatches, str(maximum)) == (declared['pairs_checked'], declared['mismatches'], declared['maximum_TV'])
    for row in report['engine']['rows']:
        q = row['input_q']
        quotients = [(2*q+r)//6 for r in range(6)]
        assert row['quotients'] == quotients
        assert row['events_per_6_remainders'] == sum(v != 0 for v in quotients)
    assert report['Born_probability_rule_derived'] is False and report['Bell_violation_claimed'] is False
    return {'branches_independently_reconstructed': len(branches),
        'all_13_probability_grids_recomputed': True, 'pairs_per_grid': checked,
        'all_498_scalar_readouts_verified': True,
        'signed_phase_intensity_identity': 'pass under the declared harmonic kernel',
        'unsigned_complexity_as_Born_weight': 'fail on declared grid',
        'nontrivial_complexity_postweight_of_fixed_state': 'fail on declared grid',
        'Born_sampling_derived': 'fail: observed click law is min(1,q/3), not a derived normalized branch law',
        'Bell_mechanism': 'unknown: no joint quantum measurement mechanism is implemented',
        'independent_Engine_inverse_reexecution': 'not done by this checker; reported and source-inspected only',
        'scope': 'The harmonic kernel incorporates phase geometry. Its successful identity does not establish a complexity preference or justify dropping Bell premises.'}


def load_trajectory(directory, report=None):
    directory = Path(directory)
    if report is None:
        report = json.loads((directory/'report.json').read_text())
    tensor = Tensor.from_json((directory/'tensor.json').read_text(), strict_support=True)
    def state_file(names):
        for name in names:
            p = directory/name
            if p.exists():
                with (gzip.open(p, 'rt') if p.suffix == '.gz' else p.open()) as f:
                    return State.from_dict(json.load(f))
        raise FileNotFoundError((directory, names))
    seed = state_file(('initial.json.gz', 'seed.json.gz', 'seed.json'))
    final = state_file(('final.json.gz', 'final.json'))
    steps = report.get('completed_updates', report.get('updates', report.get('parameters', {}).get('steps')))
    assert type(steps) is int
    engine, states = Engine(tensor), [seed]
    for _ in range(steps):
        states.append(engine.step(states[-1]))
    assert states[-1].same_as(final) and engine.rewind(final, steps).same_as(seed)
    trace = directory/'trace.jsonl.gz'
    if not trace.exists():
        trace = directory/'full_trace.jsonl.gz'
    if trace.exists():
        with gzip.open(trace, 'rt') as stream:
            exported = [json.loads(line) for line in stream]
        assert len(exported) == len(states)
        for tick, (row, state) in enumerate(zip(exported, states)):
            assert row.get('tick', row.get('microtick')) == tick and State.from_dict(row['state']).same_as(state)
    return tensor, states, {'complete_seed_final_and_inverse_replayed': True,
        'steps': steps, 'all_exported_snapshots_verified': trace.exists()}


def audit_peers(base):
    base = Path(base)
    result, tables = {}, {}
    for group in ('02-memory', '03-reassembly', '04-organization'):
        cases, trajectories, unassessed = {}, {}, []
        source_directory = base/group
        if group == '03-reassembly' and (source_directory/'verified'/'summary.json').exists():
            source_directory = source_directory/'verified'
        supplemental = {}
        if group == '02-memory':
            aggregate = json.loads((source_directory/'report.json').read_text())
            supplemental = {f"boolean-L{r['L']}-{r['case']}": r
                            for r in aggregate['secondary_boolean_handoff']}
        for directory in sorted(source_directory.iterdir()):
            if directory.is_dir() and (directory/'tensor.json').exists():
                if not (directory/'report.json').exists() and directory.name not in supplemental:
                    unassessed.append(directory.name)
                    continue
                tensor, states, item = load_trajectory(directory, supplemental.get(directory.name))
                trajectories[directory.name] = (tensor, states)
                if group == '03-reassembly':
                    item['original_metrics'] = replay_case(directory)
                    assert item['original_metrics']['complete_goal'] == 'fail'
                cases[directory.name] = item
        assert cases
        result[group] = {'cases': cases, 'independently_replayed_case_count': len(cases),
                         'artifact_directory': str(source_directory),
                         'directories_without_case_report_not_assessed': unassessed}
        tables[group] = trajectories
    mem = tables['02-memory']
    boolean_checks = []
    for L, label in product((3, 5), ('coincident', 'separated')):
        signed_tensor, signed = mem[f'L{L}-{label}']
        boolean_tensor, boolean = mem[f'boolean-L{L}-{label}']
        assert signed_tensor.names == boolean_tensor.names
        bit = signed_tensor.gear_index('mem.bit')
        other = [g for g in range(signed_tensor.G) if g != bit]
        assert len(signed) == len(boolean) == 81
        for a, b in zip(signed, boolean):
            for field in ('a', 'b'):
                assert np.array_equal(getattr(a, field)[bit], 1-2*getattr(b, field)[bit])
            for field in ('a', 'b', 'r'):
                assert np.array_equal(getattr(a, field)[other], getattr(b, field)[other])
        boolean_checks.append({'L': L, 'case': label, 'updates': 80,
            'both_memory_histories_match_signed_encoding': True,
            'all_other_triples_match': True})
    result['02-memory']['independent_boolean_handoff_comparisons'] = boolean_checks
    tensor, left = mem['L5-coincident']; _, right = mem['L5-separated']
    center = left[0].lattice.index(2, 2, 2)
    for name in ('mem.A', 'mem.B', 'mem.probe', 'mem.receiver', 'mem.readout'):
        g = tensor.gear_index(name)
        assert left[4].gear(g, center) == right[4].gear(g, center)
    bit, readout = (tensor.gear_index(n) for n in ('mem.bit', 'mem.readout'))
    assert left[4].b[bit, center] == -right[4].b[bit, center]
    assert [int(s[5].b[readout, center]) for s in (left, right)] == [-1, 1]
    _, a = mem['L5-coincident-no_memory_readout']; _, b = mem['L5-separated-no_memory_readout']
    assert all(np.array_equal(x.b[readout], y.b[readout]) for x, y in zip(a, b))
    result['02-memory']['same_current_local_signal_different_past_changes_future'] = 'pass'
    result['02-memory']['memory_read_disconnection_removes_difference'] = 'pass'
    _, a = mem['L5-quiet-matched-bit-0']; _, b = mem['L5-quiet-matched-bit-1']
    assert_cones(a, b)
    result['02-memory']['complete_state_intervention_cone'] = 'pass'
    result['02-memory']['unbounded_growth_of_structural_memory'] = 'fail: finite parity feature recurs'
    rotor = tables['03-reassembly']
    effects = []
    for L in (3, 5):
        for connected in (0, 1):
            tensor, a = rotor[f'L{L}_routing{connected}_memory0']
            _, b = rotor[f'L{L}_routing{connected}_memory1']
            rows = [g for g, n in enumerate(tensor.names) if n.startswith('comm.')]
            first = next((tick for tick, (x, y) in enumerate(zip(a, b))
                if not np.array_equal(x.b[rows], y.b[rows])), None)
            assert first == (2 if connected else None)
            assert_cones(a, b)
            effects.append({'L': L, 'routing_connected': bool(connected), 'first_message_difference': first})
    result['03-reassembly']['memory_interventions'] = effects
    result['03-reassembly']['complete_state_intervention_cones'] = 'pass'
    result['03-reassembly']['structural_growth'] = 'fail in every frozen run'
    org = tables['04-organization']
    for L in (3, 5, 7):
        tensor, a = org[f'L{L}-coherent']; _, b = org[f'L{L}-no_read']
        keep = [g for g, name in enumerate(tensor.names) if name != 'response']
        assert all(all(np.array_equal(getattr(x, f)[keep], getattr(y, f)[keep])
            for f in ('a', 'b', 'r')) for x, y in zip(a, b))
        response = tensor.gear_index('response')
        assert all(not np.any(x.b[response]) for x in b)
        memory = [g for g, name in enumerate(tensor.names) if name.startswith('memory.')]
        p3, _ = structure(a[3*L], memory)
        p6, _ = structure(a[6*L], memory)
        assert p3['normalized_fingerprint'] == p6['normalized_fingerprint']
    result['04-organization']['disconnected_read_keeps_memory_and_carriers'] = 'pass'
    result['04-organization']['cycle3_vs_cycle6_primitive_memory_shape'] = 'identical at L3/L5/L7; later size alone is rejected'
    result['04-organization']['original_complete_goal'] = 'fail: no memory feedback to carriers or sustained original growth'
    interventions = []
    for L in (3, 5, 7):
        path = base/'04-organization'/f'L{L}-memory-intervention'
        tensor = Tensor.from_json((path/'tensor.json').read_text(), strict_support=True)
        engine = Engine(tensor)
        seeds = [State.from_dict(s) for s in json.loads((path/'seeds.json').read_text())]
        finals = [State.from_dict(s) for s in json.loads((path/'finals.json').read_text())]
        with gzip.open(path/'trace.jsonl.gz', 'rt') as f:
            exported = [json.loads(line) for line in f]
        states, trajectories, differences = seeds, [[], []], []
        retained = [g for g, name in enumerate(tensor.names) if not name.startswith('memory.')]
        assert all(np.array_equal(getattr(seeds[0], field)[retained], getattr(seeds[1], field)[retained])
                   for field in ('a', 'b', 'r'))
        carriers = [g for g, name in enumerate(tensor.names) if name.startswith('carrier.')]
        response = tensor.gear_index('response')
        for tick, row in enumerate(exported):
            assert tick == row['tick']
            assert all(state.same_as(State.from_dict(saved)) for state, saved in zip(states, row['states']))
            assert all(np.array_equal(getattr(states[0], f)[carriers], getattr(states[1], f)[carriers]) for f in ('a', 'b', 'r'))
            if any(not np.array_equal(getattr(states[0], f)[response], getattr(states[1], f)[response])
                   for f in ('a', 'b', 'r')):
                differences.append(tick)
            for i, state in enumerate(states):
                trajectories[i].append(state)
            if tick < len(exported)-1:
                states = [engine.step(state) for state in states]
        assert all(s.same_as(f) and engine.rewind(s, len(exported)-1).same_as(seed)
                   for s, f, seed in zip(states, finals, seeds))
        assert_cones(*trajectories)
        assert differences == {3: [2, 3], 5: [], 7: [3, 4, 5, 6, 7]}[L]
        interventions.append({'L': L, 'response_difference_ticks': differences,
            'only_memory_initially_changed': True, 'same_carriers_at_all_times': True,
            'complete_trace_and_inverse_replayed': True, 'complete_state_cones': True})
    result['04-organization']['separately_verified_memory_intervention_pairs'] = interventions
    result['04-organization']['directories_without_case_report_not_assessed'] = []
    return result


def assert_cones(left, right):
    """Bound complete-state differences from their complete initial footprint."""
    initial = np.flatnonzero(np.any((left[0].a != right[0].a)
        | (left[0].b != right[0].b) | (left[0].r != right[0].r), axis=0))
    origins = [left[0].lattice.coords(int(n)) for n in initial]
    for tick, (a, b) in enumerate(zip(left, right)):
        changed = np.flatnonzero(np.any((a.a != b.a) | (a.b != b.b) | (a.r != b.r), axis=0))
        for n in changed:
            xyz = a.lattice.coords(int(n))
            assert origins
            distance = min(sum(min(abs(x-y), a.L-abs(x-y)) for x, y in zip(xyz, origin)) for origin in origins)
            assert distance <= tick


def audit_sensor_rotor(directory):
    """Separately declared follow-up: independently replay the composed law."""
    directory = Path(directory)
    aggregate = json.loads((directory/'report.json').read_text())
    cases, tables = {}, {}
    for label, declared in aggregate['cases'].items():
        tensor, states, verified = load_trajectory(directory/label)
        history, samples = deque(maxlen=2), []
        refs = [g for g, n in enumerate(tensor.names) if n.startswith('ref.')]
        comm = [g for g, n in enumerate(tensor.names) if n.startswith('comm.')]
        source = [g for g, n in enumerate(tensor.names) if n.startswith('source.')]
        alarm = tensor.gear_index('sensor.alarm')
        connected = declared['parameters']['connected']
        initial_mass = sum(states[0].b[comm].flat)
        for tick, state in enumerate(states):
            row, signs = structure(state, refs, tuple(history))
            history.append(signs); row['update'] = tick; samples.append(row)
            for key, value in row.items():
                if key in declared['frames'][tick]:
                    assert declared['frames'][tick][key] == value, (label, tick, key)
            assert np.array_equal(state.r, states[0].r)
            assert sum(state.b[comm].flat) == initial_mass
            for field in ('a', 'b'):
                values = getattr(state, field)[source+[alarm]]
                assert np.all((values == 0) | (values == 1))
                wire = getattr(state, field)[tensor.gear_index('message.x')]
                assert not np.any(wire)
            for axis_id, axis in enumerate(('x', 'y', 'z')):
                for bank in ('X', 'Y'):
                    names = [f'{kind}.{axis}.{bank}' for kind in
                             ('comm.plus', 'comm.minus', 'memory', 'ref.density')]
                    ids = [tensor.gear_index(n) for n in names]
                    for field in ('a', 'b'):
                        p, n, m, density = getattr(state, field)[ids]
                        assert all(np.all((v == 0) | (v == 1)) for v in (p, n, m))
                        assert np.array_equal(density, p+n)
                    if tick == len(states)-1:
                        continue
                    p, n, m, density = state.b[ids]
                    if bank == 'Y':
                        swap = np.logical_xor(m.astype(bool), state.b[alarm].astype(bool)) if connected else m.astype(bool)
                        expected = (np.where(swap, n, p), np.where(swap, p, n),
                                    np.logical_xor(m.astype(bool), np.logical_xor(p.astype(bool), n.astype(bool))).astype(int), density)
                        target = 'X'
                    else:
                        offset = tuple(-int(k == axis_id) for k in range(3))
                        pp = p[state.lattice.shift_index(offset)]
                        nn = n[state.lattice.shift_index(tuple(-k for k in offset))]
                        expected = (pp, nn, m, density+pp+nn-p-n)
                        target = 'Y'
                    targets = [tensor.gear_index(f'{kind}.{axis}.{target}') for kind in
                               ('comm.plus', 'comm.minus', 'memory', 'ref.density')]
                    assert all(np.array_equal(states[tick+1].b[g], value) for g, value in zip(targets, expected))
        result = scoreboard(samples, rewind=True, frozen_model=True)
        assert result['complete_goal'] == 'fail'
        assert not declared['independent_reference_board'] and not declared['full_goal_demonstrated']
        verified.update(original_metrics=result, bounded_prepared_domain_all_complete_states=True,
                        independent_Boolean_forward_map_all_steps=True,
                        fixed_message_occupancy=True, single_edge_support=True)
        cases[label] = verified
        tables[label] = (tensor, states)
    comparisons = []
    for L, connected, memory in product((3, 5), (0, 1), (0, 1)):
        tensor, left = tables[f'L{L}-static1-connected{connected}-memory{memory}']
        _, right = tables[f'L{L}-static0-connected{connected}-memory{memory}']
        comm = [g for g, n in enumerate(tensor.names) if n.startswith('comm.')]
        refs = [g for g, n in enumerate(tensor.names) if n.startswith('ref.')]
        first = lambda rows: next((t for t, (a, b) in enumerate(zip(left, right))
                                  if not np.array_equal(a.b[rows], b.b[rows])), None)
        assert first(comm) == (2 if connected else None)
        assert first(refs) == (3 if connected else None)
        payload = [tensor.gear_index(f'source.{n}') for n in ('x', 'y')]
        control = [tensor.gear_index(f'source.{n}') for n in ('c', 'd')]
        for a, b in zip(left, right):
            for rows in (payload, control):
                assert np.array_equal(np.abs(a.b[rows]).sum(axis=0), np.abs(b.b[rows]).sum(axis=0))
        assert_cones(left, right)
        comparisons.append({'L': L, 'connected': bool(connected), 'memory_intervention': bool(memory),
            'first_message_difference': first(comm), 'first_density_difference': first(refs),
            'matched_local_amplitude': True, 'complete_state_cones': True})
    for L, stagnant, memory in product((3, 5), (0, 1), (0, 1)):
        tensor, a = tables[f'L{L}-static{stagnant}-connected0-memory{memory}']
        _, b = tables[f'L{L}-static{stagnant}-connected1-memory{memory}']
        source = [g for g, n in enumerate(tensor.names) if n.startswith('source.') or n == 'sensor.alarm']
        assert all(all(np.array_equal(getattr(x, f)[source], getattr(y, f)[source])
            for f in ('a', 'b', 'r')) for x, y in zip(a, b))
    memory_cones = 0
    for L, stagnant, connected in product((3, 5), (0, 1), (0, 1)):
        tensor, a = tables[f'L{L}-static{stagnant}-connected{connected}-memory0']
        _, b = tables[f'L{L}-static{stagnant}-connected{connected}-memory1']
        assert_cones(a, b); memory_cones += len(a)
        source = [g for g, n in enumerate(tensor.names) if n.startswith('source.') or n == 'sensor.alarm']
        assert all(all(np.array_equal(getattr(x, f)[source], getattr(y, f)[source])
            for f in ('a', 'b', 'r')) for x, y in zip(a, b))
    assert len(cases) == 16
    return {'separate_followup': True, 'cases': cases,
        'independently_replayed_updates': sum(r['steps'] for r in cases.values()),
        'complete_snapshots_verified': sum(r['steps']+1 for r in cases.values()),
        'history_controls': comparisons, 'source_independent_of_connection_and_memory': True,
        'memory_intervention_cone_snapshots': memory_cones,
        'local_history_alarm_scattering_density_chain': 'pass in the frozen Boolean domain',
        'general_structural_stagnation_detection': 'fail: equality of adjacent samples is weaker',
        'independent_reference_reassembly': 'fail: retained density mirrors message occupancy',
        'original_structural_growth': 'fail in all 16 cases',
        'predictive_organization_on_held_out_cases': 'unknown',
        'Born_or_Bell': 'unknown: not tested by this mechanism'}


def controls(out):
    results = {}
    declared = [('baseline', dict(L=5, steps=70)),
                ('periodic_shell', dict(L=7, steps=70, family='periodic_control')),
                ('scaled_periodic_shell', dict(L=7, steps=70, family='periodic_control', amplitude=6)),
                ('no_messages', dict(L=5, steps=30, amplitude=0))]
    for name, args in declared:
        report = run_case(out=out/name, **args)
        results[name] = replay_case(out/name)
        results[name]['full_state_returns'] = report['full_state_returns']
        assert results[name]['complete_goal'] == 'fail'
    left, right = (json.loads((out/n/'report.json').read_text()) for n in
                   ('periodic_shell', 'scaled_periodic_shell'))
    assert [s['normalized_fingerprint'] for s in left['samples']] == [s['normalized_fingerprint'] for s in right['samples']]
    assert results['periodic_shell']['reassembly_vectors'] == results['scaled_periodic_shell']['reassembly_vectors']

    # A genuine fixed-six integer counter is not spatial structural growth.
    tensor = Tensor(['ref.counter'], [('ref.counter', 6, (('ref.counter', (0, 0, 0), 'b'),))], strict_support=True)
    engine = Engine(tensor)
    seed = engine.vacuum(5, [0])
    seed.b[0, seed.lattice.index(2, 2, 2)] = 1
    state, history, samples, bits = seed.copy(), deque(maxlen=2), [], []
    for tick in range(49):
        row, signs = structure(state, [0], tuple(history))
        history.append(signs)
        row['update'] = tick
        samples.append(row)
        bits.append(state.max_abs().bit_length())
        if tick < 48:
            state = engine.step(state)
    assert engine.rewind(state, 48).same_as(seed)
    assert len({r['normalized_fingerprint'] for r in samples}) == 1
    results['growing_integer_counter'] = scoreboard(samples, rewind=True, frozen_model=True)
    results['growing_integer_counter'].update(initial_bits=bits[0], final_bits=bits[-1], final_b=int(state.b.max()))
    assert results['growing_integer_counter']['complete_goal'] == 'fail'

    # Projecting onto b can erase the local visible value without losing state.
    empty_law = Engine(Tensor(['memory'], [], strict_support=True))
    s = empty_law.vacuum(3, [2])
    s.b[0, 0] = 1
    nxt = empty_law.step(s)
    assert nxt.gear(0, 0) == (1, 0, 2) and empty_law.inverse_step(nxt).same_as(s)
    results['vanishing_visible_memory'] = {'before': s.gear(0, 0), 'after': nxt.gear(0, 0),
        'visible_b_zero': True, 'complete_information_lost': False, 'exact_inverse': True,
        'useful_future_effect': 'unknown; an explicit coupled readout is required'}

    # Measurement-only controls: no claim that these sampled fields are a law.
    rng = Random(20261111)
    shape = (16, 5**3)
    old, noise, repeat = deque(maxlen=2), [], []
    fixed = np.array([[rng.choice((-1, 1)) for _ in range(shape[1])] for _ in range(shape[0])], dtype=object)
    histories = deque(maxlen=2)
    for tick in range(10):
        b = np.array([[rng.choice((-1, 1)) for _ in range(shape[1])] for _ in range(shape[0])], dtype=object)
        sample = State(5, np.zeros(shape, dtype=object), b, np.zeros(shape, dtype=object))
        row, signs = structure(sample, list(range(16)), tuple(old))
        old.append(signs); row['update'] = tick; noise.append(row)
        stable = State(5, np.zeros(shape, dtype=object), fixed, np.zeros(shape, dtype=object))
        row, signs = structure(stable, list(range(16)), tuple(histories))
        histories.append(signs); row['update'] = tick; repeat.append(row)
    assert max(r['persistent_pattern_types'] for r in noise) == 0
    results['independent_noise_measurement_only'] = scoreboard(noise, frozen_model=False, organization_controls=False)
    results['static_random_pattern_measurement_only'] = scoreboard(repeat, frozen_model=False, organization_controls=False)
    results['independent_noise_measurement_only']['maximum_site_diversity'] = max(r['site_pattern_types'] for r in noise)
    results['static_random_pattern_measurement_only']['maximum_persistence'] = max(r['persistent_pattern_types'] for r in repeat)

    bell, records = bell_audit(distance=1)
    scores = bell['cases']['selection_stress']['readers']
    assert scores['C2_all_emissions']['S'] == '3/2' and scores['C2_coincidences_only']['S'] == '4'
    results['postselected_C2'] = {'all_emission_S': '3/2', 'selected_S': '4',
        'included_per_setting': [c['included'] for c in scores['C2_coincidences_only']['cells'].values()],
        'emitted_per_setting': [c['emitted'] for c in scores['C2_coincidences_only']['cells'].values()],
        'Born_or_complexity_derivation': 'fail; conditional sample is not a physical law'}
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=Path('runs/complexity-research/06-acceptance'))
    parser.add_argument('--replay', type=Path)
    parser.add_argument('--stagnation', type=Path)
    parser.add_argument('--born', type=Path)
    parser.add_argument('--peer-root', type=Path)
    parser.add_argument('--sensor-rotor', type=Path)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    if sum(v is not None for v in (args.replay, args.stagnation, args.born, args.peer_root, args.sensor_rotor)) > 1:
        parser.error('choose one replay mode')
    if args.sensor_rotor:
        result = audit_sensor_rotor(args.sensor_rotor)
    elif args.peer_root:
        result = audit_peers(args.peer_root)
    elif args.born:
        result = audit_born(args.born)
    elif args.stagnation:
        result = audit_stagnation(args.stagnation)
    elif args.replay:
        result = replay_case(args.replay)
    else:
        result = {'production_baseline': '7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2',
            'protocol': 'recurrent-bursts-v1; supplemented, not replaced, by complexity/PROTOCOL.md',
            'controls': controls(args.out),
            'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    root = Path(__file__).resolve().parents[2]
    provenance_paths = [Path(__file__), *sorted((root/'universe24/core').glob('*.py')),
                       *sorted((root/'experiments/complexity').glob('*.py')),
                       root/'experiments/cosmology/recurrent_bursts.py',
                       root/'experiments/cosmology/PROTOCOL.md',
                       root/'experiments/complexity/PROTOCOL.md']
    result['auditor_provenance'] = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in provenance_paths}
    (args.out/'report.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
