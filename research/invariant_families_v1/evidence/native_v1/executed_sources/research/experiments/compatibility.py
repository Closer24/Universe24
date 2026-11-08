"""Reassemble all 44 retained interfaces and compare every recorded full state."""
import argparse
import hashlib
import json
from pathlib import Path

from .interfaces import signal_case_spec, paired_case_spec
from .run import run_experiment, write_json
from research.presenter.export import bundle, write_bundle

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT/'research/signal_clocks/evidence'


def retained_specs():
    for family in ('counter_memory', 'toggle_confirmation'):
        manifest = json.loads((EVIDENCE/family/'candidate_manifest.json').read_text())
        for item in manifest['runs']:
            yield family, item['id'], signal_case_spec(item['case'], tuple(item['mask']), identifier=item['id'])
    manifest = json.loads((EVIDENCE/'paired_blocker/candidate_manifest.json').read_text())
    for case in manifest['cases']:
        yield 'paired_blocker', case['id'], paired_case_spec(case)


def _event(event):
    return {**event, 'quotient': int(event['quotient'])}


def check(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    source = EVIDENCE/'interfaces_presenter_final/experiments.json'
    raw = source.read_bytes()
    old = {e['id']: e for e in json.loads(raw)['experiments']}
    report = {'format': 'universe24-component-compatibility-v1', 'passed': False,
              'historical_bundle_sha256': hashlib.sha256(raw).hexdigest(), 'cases': []}
    recordings = []
    for family, identifier, spec in retained_specs():
        # Readouts are fixed before the new run to the exact retained definitions.
        spec['readouts'] = old[identifier]['readouts']
        result = run_experiment(spec)
        recorded = result['experiment']
        legacy = json.loads((EVIDENCE/family/'cases'/identifier/'result.json').read_text())
        observer = result['observations']['source.signal' if family == 'paired_blocker' else 'receiver.memory']
        checks = {
            'full_frames_equal': recorded['frames'] == old[identifier]['frames'],
            'tensor_equal': recorded['coupling'] == old[identifier]['coupling'],
            'background_equal': recorded['background'] == old[identifier]['background'],
            'fixed_readouts_equal': recorded['readouts'] == old[identifier]['readouts'],
            'all_record_changes_equal': observer['record_event_times'] == legacy['record_event_times'],
            'all_arithmetic_events_equal': [_event(e) for e in observer['arithmetic_events']] == legacy['arithmetic_events'],
            'full_inverse_and_rewind': recorded['provenance']['full_rewind_equal'],
        }
        comparable = []
        for row in observer['trace']:
            comparable.append({'step': row['step'],
                               'detector': [[int(a),int(b),r] for a,b,r in row['detector']],
                               'memory': row['memory'], 'next_input': [int(v) for v in row['next_input']],
                               'six_inputs': [[{**term, 'b': int(term['b'])} for term in port] for port in row['six_inputs']],
                               'arithmetic_events': [_event(e) for e in row['arithmetic_events']]})
        checks['all_observed_inputs_and_counter_triples_equal'] = comparable == legacy['trace']
        report['cases'].append({'id': identifier, 'checks': checks,
                                'frames': len(recorded['frames']), 'passed': all(checks.values())})
        recordings.append(recorded)
    report['experiments'] = len(recordings)
    report['frames'] = sum(len(e['frames']) for e in recordings)
    report['inverse_transitions'] = report['frames']-len(recordings)
    report['historical_input_unchanged'] = source.read_bytes() == raw
    report['passed'] = len(recordings) == 44 and report['frames'] == 1868 and report['historical_input_unchanged'] and all(c['passed'] for c in report['cases'])
    write_json(output/'report.json', report)
    if not report['passed']:
        raise AssertionError('Retained interface equivalence failed; inspect report.json')
    write_bundle(output/'experiments.json', bundle(recordings, title='Generic assembly: all 44 retained interfaces'))
    print(json.dumps({key: value for key, value in report.items() if key != 'cases'}, indent=2))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    check(parser.parse_args().output)
