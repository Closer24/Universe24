"""Click-only observations, calibrated retained memory, and ambiguity controls.

The observer functions below read arithmetic clicks only. Preparation, runtime
replay and comparisons with the independent full-state detector observer belong
to the audit harness, not to the observer's information or to Engine evolution.
No inferred amplitude or observation is fed back to the running model.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from universe24.core import State
from universe24.core.symmetry import CONTRACT
from universe24.detection import make_detector_bundle, observe_detector_run
from universe24.light import light_tensor, make_light_bundle
from universe24.system.bundle import create_bundle
from universe24.system.decoder import default_protocol
from universe24.system.runtime import run_bundle
from universe24.observer import (read_clicks, inspect_click_file, compare_click_files,
                                 reconstruct_memory_from_clicks)
from validation.light_link_resonance import build_tensor, prepare, make_bundle

ROOT = Path(__file__).resolve().parents[1]


def _light_control(seed, name):
    law = light_tensor()
    return create_bundle(
        law, seed,
        channels=[{'index': g, 'name': gear.name, 'label': gear.label,
                   'owner': 'click-observer-audit', 'purpose': 'complete regular amplitude and histories'}
                  for g, gear in enumerate(law.gears)],
        protocol=default_protocol(),
        model={'id': 'click-observer-control', 'version': '1', 'role': 'research',
               'symmetry': CONTRACT, 'domain': name,
               'scope': 'information in arithmetic clicks, not a physical detector claim'})


def collect(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)
    source_paths = [Path(__file__), ROOT/'validation/light_link_resonance.py',
                    ROOT/'universe24/light.py', ROOT/'universe24/detection.py',
                    ROOT/'universe24/observer.py']
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths}
    specs = []
    for value in (1, 2):
        seed = State(3, np.full((48, 27), value, dtype=object),
                     np.full((48, 27), value, dtype=object), np.ones((48, 27), dtype=int))
        specs.append((f'stationary-{value}', _light_control(seed, 'distinct constant stationary seed'), 2))
    baseline = make_light_bundle(L=7, axis=0, sign=1, polarization=1, center=2, order=2)
    for remainder in (1, 2):
        seed = baseline.seed.copy()
        seed.a += 1
        seed.b += 1
        seed.r[:] = remainder
        specs.append((f'light-remainder-{remainder}', _light_control(seed, 'same light, distinct hidden carries'), 6))
    parameters = dict(gradient=3, spring=3, optical=0, backreaction=False, phase_gate=True)
    phase_law = build_tensor(**parameters)
    for amplitude in (0, 1):
        seed, metadata = prepare(L=3, amplitude=amplitude, paused_history=True)
        specs.append((f'phase-amplitude-{amplitude}', make_bundle(phase_law, seed, parameters, metadata), 8))
    for name, amplitude, armed in [('armed', 1, True), ('no-light', 0, True),
                                    ('unarmed', 1, False), ('double-amplitude', 2, True)]:
        bundle = make_detector_bundle(L=5, root=0, light_position=0, arm_position=3,
                                      amplitude=amplitude, armed=armed)
        specs.append((f'detector-{name}', bundle, 8))
    runs, detectors = {}, {}
    for name, bundle, steps in specs:
        destination = out/name
        replay = run_bundle(bundle, destination, steps)
        observation = inspect_click_file(destination/'clicks.jsonl.gz')
        runs[name] = {'run_id': replay['run_id'], 'tensor_hash': replay['tensor_hash'],
                      'steps': steps, 'maximum_integer_bits': max(replay['maximum_integer_bits_by_step']),
                      'replay_checks': replay['checks'], 'runtime_source_hashes': replay['source_hashes'],
                      'click_only': observation}
        if name.startswith('detector-'):
            inferred = reconstruct_memory_from_clicks(destination/'clicks.jsonl.gz',
                memory_channel=bundle.model['roles']['memory'], node_count=bundle.seed.N, steps=steps)
            full = observe_detector_run(destination)
            keys = ('step', 'node', 'kind', 'memory_before', 'memory_after', 'energy_to_memory', 'arithmetic_event_id')
            if [{k: event[k] for k in keys} for event in inferred['events']] != [
                    {k: event[k] for k in keys} for event in full['events']]:
                raise AssertionError('click-only memory changes differ from full-state audit')
            if inferred['accounts'] != [{'step': row['step'], 'memory_account': row['memory']}
                                        for row in full['accounts'][1:]]:
                raise AssertionError('click-only memory accounts differ from full-state audit')
            inferred['independent_full_state_comparison'] = 'passed'
            (destination/'click-only-memory.json').write_text(json.dumps(inferred, indent=2)+'\n')
            detectors[name] = inferred
        print(f'{name}: {steps} steps; {observation["events"]} arithmetic clicks', flush=True)

    def compare(a, b):
        return compare_click_files(out/a/'clicks.jsonl.gz', out/b/'clicks.jsonl.gz')

    stationary = compare('stationary-1', 'stationary-2')
    carries = compare('light-remainder-1', 'light-remainder-2')
    phase = compare('phase-amplitude-0', 'phase-amplitude-1')
    same_first = (runs['phase-amplitude-0']['click_only']['first_recorded_step_by_node_address'] ==
                  runs['phase-amplitude-1']['click_only']['first_recorded_step_by_node_address'])
    if not stationary['entire_canonical_record_lists_equal'] or stationary['left_events']:
        raise AssertionError('stationary ambiguity control changed')
    if not carries['complete_observational_payloads_equal'] or not carries['left_events'] or carries['entire_canonical_record_lists_equal']:
        raise AssertionError('nonempty hidden-carry ambiguity control changed')
    if phase['complete_observational_payloads_equal'] or not same_first:
        raise AssertionError('clock/background observation control changed')
    if detectors['detector-no-light']['outcomes']['capture'] or detectors['detector-unarmed']['outcomes']['capture']:
        raise AssertionError('negative detector control produced capture')
    if detectors['detector-armed']['outcomes'] != detectors['detector-double-amplitude']['outcomes']:
        raise AssertionError('amplitude changed occupied-cell transfer count')
    result = {
        'schema': 'universe24/click-observer-audit/1', 'source_hashes': hashes, 'runs': runs,
        'comparisons': {'stationary_distinct_seeds': stationary, 'nonempty_distinct_carries': carries,
                        'phase_clock_vs_clock_plus_light': phase,
                        'phase_first_click_by_node_unchanged_by_light': same_first},
        'click_only_retained_memory': detectors,
        'gates': {'click_only_memory_on_calibrated_nonnegative_sector': 'passed',
                  'same_clicks_identify_unique_latent_state': 'failed',
                  'raw_first_click_is_light_arrival': 'failed',
                  'raw_click_count_is_capture_count': 'failed',
                  'dark_matter_identification_from_dark_clicks': 'not_tested',
                  'proper_clock_or_einstein_metric_from_clicks': 'not_tested',
                  'photon_number_or_born_measure': 'not_tested',
                  'general_physical_acceptance': 'blocked'},
        'scope': 'different tensors remain separate controls; click-only inference never feeds the Engine',
    }
    if hashes != {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths}:
        raise AssertionError('audited sources changed during collection')
    (out/'results.json').write_text(json.dumps(result, indent=2)+'\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--out', type=Path)
    action.add_argument('--clicks', type=Path)
    args = parser.parse_args()
    if args.clicks:
        print(json.dumps(inspect_click_file(args.clicks), indent=2))
    else:
        result = collect(args.out)
        print(json.dumps({'runs': len(result['runs']), 'gates': result['gates']}, indent=2))
