"""Exact Bell-reader audit of actual causal-wave Engine transitions.

python -m experiments.quantum.bell_cone_audit --out runs/bell-cone
Read BELL_CONE_PROTOCOL.md: gain settings and binary readers are explicit
audit constructions, not an entangled source / quantum measurement model.
"""
import argparse
from collections import defaultdict
from fractions import Fraction
import gzip
import hashlib
from itertools import product
import json
from pathlib import Path

import numpy as np

from universe24.core import Engine, State
from universe24.layers.causal_wave import with_causal_wave, LANES
from universe24.observe.causal_wave import changed_sites, inside_cone
from universe24.prepare.causal_wave import prepare_causal_wave


def sources(case):
    if case == 'literal_unit':
        return [('unit', 1, 1)]
    if case == 'shared_sign':
        return [(str(s), s, s) for s in (-1, 1)]
    if case != 'selection_stress':
        raise ValueError('unknown source control')
    payload = {(0, 1): 1, (0, -1): -2, (1, 1): 2, (1, -1): -1}
    return [(f'{i},{j},{s}', payload[i, s], payload[j, s * (-1)**(i*j)])
            for i, j, s in product((0, 1), (0, 1), (-1, 1))]


def digest(state, indices):
    values = [getattr(state, field)[indices].tolist() for field in ('a', 'b', 'r')]
    return hashlib.sha256(json.dumps(values, separators=(',', ':')).encode()).hexdigest()


def prepare_trial(tensor, distance, payloads, settings, *, literal=False, silent=False):
    if type(distance) is not int or distance < 1:
        raise ValueError('distance must be a positive integer')
    if len(settings) != 2 or any(type(v) is not int or v not in (0, 1) for v in settings):
        raise ValueError('two binary settings required')
    L = 4 * distance + 1
    center = (2 * distance,) * 3
    sites = [(center[0] + sign * distance, center[1], center[2]) for sign in (-1, 1)]
    empty = State(L, *[np.zeros((tensor.G, L**3), dtype=np.int64) for _ in range(3)])
    packets = [] if silent else [('nx', center, payloads[0]), ('px', center, payloads[1])]
    seed = prepare_causal_wave(empty, tensor, packets=packets, detectors=sites)
    marker = tensor.gear_index('wave.detector')
    nodes = [seed.lattice.index(*site) for site in sites]
    for node, choice in zip(nodes, settings):
        seed.a[marker, node] = seed.b[marker, node] = 1 if literal else 1 + choice
    return seed, nodes


def trial(engine, distance, payloads, settings, *, literal=False):
    tensor = engine.tensor
    seed, nodes = prepare_trial(tensor, distance, payloads, settings, literal=literal)
    silent, _ = prepare_trial(tensor, distance, payloads, settings, literal=literal, silent=True)
    initial_silent = silent
    footprint = [seed.lattice.coords(n) for n in changed_sites(seed, silent)]
    memory = tensor.gear_index('wave.memory')
    packets = [tensor.gear_index('wave.' + lane) for lane in LANES]
    state = seed
    first_click = [None, None]
    arrival = []
    for tick in range(1, distance + 1):
        after, after_silent = engine.step(state), engine.step(silent)
        assert all(inside_cone(seed.lattice, n, footprint, tick)
                   for n in changed_sites(after, after_silent))
        clicks = engine.clicks(state, after, tick).select('official')
        events = {int(n): (int(q), int(k)) for g, n, q, k
                  in zip(clicks.gear, clicks.node, clicks.quotient, clicks.kind) if g == memory}
        for side, node in enumerate(nodes):
            if node in events and first_click[side] is None:
                first_click[side] = tick
            if tick < distance:
                assert node not in events and after.gear(memory, node) == (0, 0, 2)
            else:
                event = events.get(node)
                q, kind = event if event is not None else (0, None)
                arrival.append({'node': node, 'xyz': list(seed.lattice.coords(node)),
                    'before': list(state.gear(memory, node)), 'after': list(after.gear(memory, node)),
                    'quotient': q, 'kind': kind, 'click': event is not None,
                    'outcome': 1 if q >= 0 else -1, 'C2': kind == 2})
        state, silent = after, after_silent
    assert engine.rewind(state, distance).same_as(seed)
    assert engine.rewind(silent, distance).same_as(initial_silent)
    return {'settings': list(settings), 'payloads': list(payloads), 'arrival_microtick': distance,
            'first_clicks': first_click, 'detectors': arrival,
            'source_triples_sha256': digest(seed, packets),
            'complete_seed_sha256': digest(seed, list(range(tensor.G))),
            'complete_final_sha256': digest(state, list(range(tensor.G))),
            'cone_verified': True, 'rewind_exact': True}


def score(rows, mode):
    if mode not in ('all_arrival_clicks', 'C2_all_emissions', 'C2_coincidences_only'):
        raise ValueError('unknown reader')
    cells = {}
    for x, y in product((0, 1), repeat=2):
        group = [row for row in rows if row['settings'] == [x, y]]
        pairs = []
        for row in group:
            a, b = row['detectors']
            if mode == 'C2_coincidences_only' and not (a['C2'] and b['C2']):
                continue
            values = tuple(d['outcome'] if (d['click'] if mode == 'all_arrival_clicks' else d['C2'])
                           else 1 for d in (a, b))
            pairs.append(values)
        n = len(pairs)
        cells[f'{x}{y}'] = {'emitted': len(group), 'included': n,
            'both_C2': sum(all(d['C2'] for d in row['detectors']) for row in group),
            'E': str(Fraction(sum(a*b for a, b in pairs), n)) if n else None,
            'mean_A': str(Fraction(sum(a for a, b in pairs), n)) if n else None,
            'mean_B': str(Fraction(sum(b for a, b in pairs), n)) if n else None}
    complete = all(cell['E'] is not None for cell in cells.values())
    S = abs(sum(sign * Fraction(cells[key]['E']) for key, sign
                in (('00', 1), ('01', 1), ('10', 1), ('11', -1)))) if complete else None
    nonsignalling = (all(cells[f'{x}0']['mean_A'] == cells[f'{x}1']['mean_A'] for x in (0, 1))
                    and all(cells[f'0{y}']['mean_B'] == cells[f'1{y}']['mean_B'] for y in (0, 1))) if complete else None
    return {'cells': cells, 'S': str(S) if S is not None else None,
            'selected_marginals_nonsignalling': nonsignalling,
            'interpretation': 'conditional sample; ordinary bound 2 cannot be applied without its sampling assumptions'
                if mode == 'C2_coincidences_only' else 'every emission included; local no-detection assignment +1'}


def audit(distance=3):
    tensor = with_causal_wave()
    engine = Engine(tensor)
    cases, records = {}, {}
    for case in ('literal_unit', 'shared_sign', 'selection_stress'):
        rows = []
        for label, pa, pb in sources(case):
            for x, y in product((0, 1), repeat=2):
                row = trial(engine, distance, (pa, pb), (x, y), literal=case == 'literal_unit')
                row.update(source_label=label, trial_id=f'{case}:{label}:{x}{y}')
                rows.append(row)
        by_source = defaultdict(list)
        for row in rows:
            by_source[row['source_label']].append(row)
        for group in by_source.values():
            assert len(group) == 4 and len({r['source_triples_sha256'] for r in group}) == 1
            for side in (0, 1):
                for setting in (0, 1):
                    local = [r['detectors'][side] for r in group if r['settings'][side] == setting]
                    assert local[0] == local[1], 'remote choice changed local result'
        readers = {mode: score(rows, mode) for mode in
                   ('all_arrival_clicks', 'C2_all_emissions', 'C2_coincidences_only')}
        cases[case] = {'emissions': len(rows), 'source_labels': len(by_source),
            'independent_setting_enumeration': True, 'local_results_independent_of_remote_setting': True,
            'no_click_before_arrival': all(r['first_clicks'] == [distance, distance] for r in rows),
            'all_cones_and_rewinds_verified': True, 'readers': readers}
        records[case] = rows
    values = sorted({a0*b0 + a0*b1 + a1*b0 - a1*b1
                     for a0, a1, b0, b1 in product((-1, 1), repeat=4)})
    report = {'scope': 'Audit readers of an existing local tensor, not a quantum analyzer or entangled-source implementation.',
        'tensor_fingerprint': tensor.fingerprint, 'distance': distance, 'L': 4*distance+1,
        'detector_separation': 2*distance, 'measurement_deadline': distance,
        'local_response_tables': {'enumerated': 16, 'CHSH_values': values, 'maximum_abs': max(map(abs, values))},
        'cases': cases, 'physical_Bell_violation_demonstrated': False,
        'selection_stress_is_deliberately_constructed': True}
    return report, records


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=Path('runs/bell-cone'))
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)
    report, records = audit()
    from experiments.quantum.born_reference import quantum_reference, stochastic_local_bound, router_calibration
    report['stochastic_local_bound'] = stochastic_local_bound()
    with gzip.open(args.out/'born_reference_events.jsonl.gz', 'wt') as stream:
        report['quantum_reference'] = quantum_reference(records['literal_unit'][0]['first_clicks'],
            record_sink=lambda row: stream.write(json.dumps(row, separators=(',', ':'))+'\n'))
    report['quantum_reference']['sample_log'] = 'born_reference_events.jsonl.gz'
    report['quadratic_router_calibration'] = router_calibration()
    root = Path(__file__).resolve().parents[2]
    files = ['experiments/quantum/BELL_CONE_PROTOCOL.md', 'experiments/quantum/bell_cone_audit.py',
             'experiments/quantum/born_reference.py', 'universe24/layers/choice.py',
             'universe24/core/engine.py', 'universe24/core/tensor.py', 'universe24/core/lattice.py',
             'universe24/tests/test_bell_born_reference.py', 'universe24/layers/causal_wave.py',
             'universe24/prepare/causal_wave.py', 'universe24/observe/causal_wave.py']
    report['source_sha256'] = {name: hashlib.sha256((root/name).read_bytes()).hexdigest() for name in files}
    (args.out/'trials.json').write_text(json.dumps(records, indent=2)+'\n')
    (args.out/'tensor.json').write_text(json.dumps(with_causal_wave().to_dict(), indent=2)+'\n')
    report['artifact_sha256'] = {name: hashlib.sha256((args.out/name).read_bytes()).hexdigest()
        for name in ('trials.json', 'tensor.json', 'born_reference_events.jsonl.gz')}
    (args.out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({case: {reader: value['S'] for reader, value in result['readers'].items()}
                      for case, result in report['cases'].items()}, indent=2))
    print(json.dumps({'quantum_reference_CHSH': report['quantum_reference']['exact_CHSH'],
                      'sample_CHSH': report['quantum_reference']['sample_CHSH'],
                      'local_stochastic_bound': report['stochastic_local_bound']['maximum_expected_CHSH'],
                      'router_Born_click_law_derived': False}, indent=2))


if __name__ == '__main__':
    main()
