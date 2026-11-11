"""Bounded detector/C2 audit of current main; does not change production laws.

python -m experiments.research.six_lens_clicks --out runs/six-lens/02-clicks
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from universe24.core import Engine, State, Tensor
from universe24.layers.causal_wave import LANES, with_causal_wave
from universe24.prepare.causal_wave import prepare_causal_wave

BASELINE = '7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2'


def empty(tensor, side):
    return State(side, *[np.zeros((tensor.G, side**3), dtype=np.int64) for _ in range(3)])


def fingerprint(state):
    return hashlib.sha256(json.dumps(state.to_dict(), separators=(',', ':')).encode()).hexdigest()


def scalar_cycle():
    tensor = Tensor(['scalar'], [('scalar', 2, ())])
    engine, seed = Engine(tensor), empty(tensor, 3)
    seed.r[:] = 2
    state, records = seed, []
    for tick in range(1, 49):
        after = engine.step(state)
        assert all(np.all(field == field[0, 0]) for field in (after.a, after.b, after.r))
        events = engine.clicks(state, after, tick)
        records.append({'tick': tick, 'before': state.gear(0, 0), 'after': after.gear(0, 0),
                        'kinds': events.kind[events.node == 0].tolist(),
                        'quotients': events.quotient[events.node == 0].tolist()})
        state = after
        if tick % 3 == 0:
            assert state.same_as(seed)
    assert engine.rewind(state, 48).same_as(seed)
    assert sum(len(r['kinds']) for r in records) == 32
    assert all(k == 2 for r in records for k in r['kinds'])
    return {'tensor': tensor.to_dict(), 'seed': seed.to_dict(), 'updates': 48,
            'distinct_complete_states': len({tuple(r['after']) for r in records}),
            'exact_full_state_period': 3, 'C2_events_per_node': 32,
            'all_nodes_identical_at_every_update': True, 'rewind_exact': True,
            'records': records}


def scalar_classes():
    rows = []
    for input_u in range(-6, 7):
        tensor = Tensor(['scalar'], [('scalar', input_u, ())])
        engine = Engine(tensor)
        for remainder in range(6):
            seed = empty(tensor, 3)
            seed.r[:] = remainder
            after = engine.step(seed)
            event = engine.clicks(seed, after)
            delta = (after.gear(0, 0)[2] - remainder) % 6
            assert delta == (2 * input_u) % 6
            assert len(event) == seed.N * int((2 * input_u + remainder) // 6 != 0)
            if len(event):
                assert int(event.kind[0]) == input_u % 3
            assert engine.inverse_step(after).same_as(seed)
            rows.append({'u': input_u, 'r': remainder, 'after': after.gear(0, 0),
                         'delta_r_mod_six': delta, 'click_kind': int(event.kind[0]) if len(event) else None})
    return {'transitions': len(rows), 'all_inverse_checks_exact': True, 'rows': rows}


def packet_run(packets, detectors, *, steps=8, residue=2, compare_unmarked=False):
    tensor, side = with_causal_wave(), 13
    engine = Engine(tensor)
    seed = prepare_causal_wave(empty(tensor, side), tensor, packets=packets, detectors=detectors)
    memory = tensor.gear_index('wave.memory')
    seed.r[memory] = residue
    state = seed
    other = prepare_causal_wave(empty(tensor, side), tensor, packets=packets, detectors=[])
    other.r[memory] = residue
    lane_ids = [tensor.gear_index('wave.' + lane) for lane in LANES]
    nodes = [seed.lattice.index(*xyz) for xyz in detectors]
    records, all_events = [], []
    for tick in range(1, steps + 1):
        inputs = engine.inputs(state)
        after = engine.step(state)
        events = engine.clicks(state, after, tick).select('official')
        memory_events = {int(n): {'kind': int(k), 'quotient': int(q)}
                         for g, n, k, q in zip(events.gear, events.node, events.kind, events.quotient)
                         if int(g) == memory}
        all_events.extend({'tick': tick, 'node': n, **event} for n, event in memory_events.items())
        for node in nodes:
            records.append({'tick': tick, 'node': node, 'u_memory': int(inputs[memory, node]),
                'before': state.gear(memory, node), 'after': after.gear(memory, node),
                'event': memory_events.get(node)})
        if compare_unmarked:
            other = engine.step(other)
            for field in ('a', 'b', 'r'):
                assert np.array_equal(getattr(after, field)[lane_ids], getattr(other, field)[lane_ids])
        state = after
    assert engine.rewind(state, steps).same_as(seed)
    return {'packets': packets, 'detectors': detectors, 'initial_memory_residue': residue,
            'steps': steps, 'seed_sha256': fingerprint(seed), 'final_sha256': fingerprint(state),
            'rewind_exact': True,
            'packet_triples_equal_to_unmarked_control_at_every_step': True if compare_unmarked else None,
            'events': all_events, 'records': records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=Path('runs/six-lens/02-clicks'))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    target = (3, 6, 6)
    sweep = []
    for payload in (-2, -1, 0, 1, 2, 3):
        for residue in range(6):
            result = packet_run([('px', (0, 6, 6), payload)], [target], steps=3, residue=residue)
            assert all(row['event'] is None and row['before'] == row['after']
                       for row in result['records'] if row['tick'] < 3)
            row = result['records'][-1]
            assert row['u_memory'] == 2 * payload
            sweep.append({'payload': payload, 'residue': residue, 'no_early_memory_change_or_click': True,
                          'rewind_exact': result['rewind_exact'], **row})
    sequential = packet_run([('px', (0, 6, 6), 1)], [target, (6, 6, 6)], compare_unmarked=True)
    assert [row['tick'] for row in sequential['events']] == [3, 6]
    repeated = packet_run([('px', (0, 6, 6), 1)], [target], steps=45, compare_unmarked=True)
    arrivals = [r for r in repeated['records'] if r['u_memory']]
    assert [r['tick'] for r in arrivals] == [3, 16, 29, 42]
    assert [r['tick'] for r in repeated['events']] == [3, 29, 42]
    assert next(r for r in repeated['records'] if r['tick'] == 29)['after'] == (0, 0, 2)
    quiet = packet_run([], [target], steps=8)
    assert not quiet['events'] and all(r['after'] == (0, 0, 2) for r in quiet['records'])
    cancelling = packet_run([('px', (0, 6, 6), 1), ('nx', (6, 6, 6), -1)], [target], steps=8)
    assert not cancelling['events'] and all(r['after'] == (0, 0, 2) for r in cancelling['records'])
    report = {'baseline_main': BASELINE, 'scope': 'Detector/C2 audit; no production law changes or Born/Bell claim.',
              'scalar_periodic_C2': scalar_cycle(), 'scalar_arithmetic_classification': scalar_classes(),
              'packet_payload_remainder_sweep': sweep, 'sequential_receivers': sequential,
              'repeated_packet': repeated, 'quiet': quiet, 'cancelling_signed_arms': cancelling}
    root = Path(__file__).resolve().parents[2]
    source_files = [__file__, str(root/'universe24/core/engine.py'),
                    str(root/'universe24/layers/causal_wave.py'), str(root/'universe24/prepare/causal_wave.py')]
    report['source_sha256'] = {str(Path(f).relative_to(root)): hashlib.sha256(Path(f).read_bytes()).hexdigest()
                              for f in source_files}
    (args.out/'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'scalar_period': 3, 'scalar_C2_events_per_node_in_48_updates': 32,
        'scalar_transitions_checked': 78, 'packet_sweep_cases': len(sweep),
        'sequential_detector_clicks': [r['tick'] for r in sequential['events']],
        'return_arrivals': [r['tick'] for r in arrivals],
        'return_clicks': [r['tick'] for r in repeated['events']],
        'all_rewinds_exact': True, 'no_backreaction_on_packets': True}, indent=2))


if __name__ == '__main__':
    main()
