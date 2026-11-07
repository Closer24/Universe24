"""Run exact reliability checks into a new, never-overwritten evidence bundle."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import time
from .bundle import ROOT, compare_bundles, digest, read_json, validate_named, write_json
from universe24 import Channel, Coupling, Cube, Engine, State
from universe24.experiments import checkpoint_data, from_dict
from universe24.observation import clicks, signed_account


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def source_hashes():
    paths = []
    for folder in ('universe24', 'research/reference', 'research/reproducibility', 'tests'):
        paths.extend((ROOT / folder).rglob('*.py'))
    paths.extend((ROOT / 'research/building_blocks').glob('*.py'))
    paths.extend((ROOT / 'research/building_blocks').glob('*protocol*.json'))
    paths.append(ROOT / 'research/clockwork/viewer.html')
    paths.append(ROOT / '.github/workflows/clockwork.yml')
    paths.extend((ROOT / 'research/schemas').glob('*.json'))
    paths.extend((ROOT / 'research/reproducibility').glob('*.json'))
    paths.extend((ROOT / 'examples').glob('*.json'))
    paths.extend(ROOT / name for name in ('docs/MODEL.md', 'research/reflection_audit.py',
                 'research/reflection_audit_results.json', '.github/workflows/ci.yml'))
    return {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(set(paths))}


def check_engine():
    base = read_json(ROOT / 'research/reproducibility/base_engine.json')
    actual = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in (ROOT / 'universe24').rglob('*.py')}
    if actual != base['source_sha256']:
        raise ValueError('Engine differs from pinned baseline; use a separately reviewed protocol')
    return base


def checked_case(case, folder, deadline):
    # Config is an exact repository fixture, not code or a runtime controller.
    path = (ROOT / case['config']).resolve()
    path.relative_to(ROOT)
    config = read_json(path)
    experiment = from_dict(config)
    if experiment.steps != case['expected_steps']:
        raise ValueError('Fixture duration differs from frozen protocol')
    folder.mkdir()
    write_json(folder / 'input.json', config)
    engine, initial = experiment.engine, experiment.initial
    write_json(folder / 'initial.json', checkpoint_data(initial, engine, 0))
    state = initial
    first_return = None
    event_count = 0
    with (folder / 'trace.jsonl').open('x', encoding='utf-8') as trace:
        for t in range(experiment.steps + 1):
            if time.monotonic() > deadline:
                raise TimeoutError('Shared wall budget exhausted')
            trace.write(json.dumps({'t': t, 'state_sha256': digest(checkpoint_data(state, engine, t)),
                                    'Q': signed_account(state), 'arithmetic_events_so_far': event_count}, sort_keys=True) + '\n')
            if t == experiment.steps:
                break
            nxt = engine.advance(state)
            if engine.rewind(nxt) != state:
                write_json(folder / 'counterexample.json', {
                    'kind': 'one_step_inverse', 'step': t + 1, 'input': config,
                    'before': checkpoint_data(state, engine, t),
                    'after': checkpoint_data(nxt, engine, t + 1)})
                raise AssertionError('Exact inverse mismatch')
            event_count += len(list(clicks(state, nxt, t + 1)))
            state = nxt
            if first_return is None and state == initial:
                first_return = t + 1
    write_json(folder / 'final.json', checkpoint_data(state, engine, experiment.steps))
    result = {'id': case['id'], 'steps': experiment.steps,
              'first_full_state_return': first_return, 'expected_first_return': case['expected_first_return'],
              'final_equals_initial': state == initial, 'arithmetic_event_count': event_count,
              'full_state_inverse_pass': True,
              'pass': first_return == case['expected_first_return'] and state == initial}
    write_json(folder / 'result.json', result)
    return result, engine.coupling.fingerprint


def negative_claim():
    engine = Engine(Coupling((1, -1, 1)))
    initial = State(Cube(3), cells={(0, 0, 0, 0): Channel(0, 1, 2)})
    final = engine.advance(initial)
    delta = signed_account(final) - signed_account(initial)
    return {'claim': 'Q is conserved for every fixed sign triple and state',
            'scientific_outcome': 'refuted' if delta != 0 else 'not_refuted_by_witness',
            'observed_delta_Q': delta, 'expected_delta_Q': -8,
            'implementation_check_pass': delta == -8 and engine.rewind(final) == initial,
            'initial': checkpoint_data(initial, engine, 0), 'final': checkpoint_data(final, engine, 1)}


def suite_run(output, deadline):
    scratch = output / 'test-scratch'
    scratch.mkdir()
    env = dict(os.environ, U24_COUNTEREXAMPLE_DIR=str(output / 'counterexamples'),
               TMPDIR=str(scratch), TMP=str(scratch), TEMP=str(scratch))
    proc = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
                          cwd=ROOT, env=env, capture_output=True, text=True,
                          timeout=max(0.01, deadline - time.monotonic()))
    (output / 'tests.stdout.txt').write_text(proc.stdout, encoding='utf-8')
    (output / 'tests.stderr.txt').write_text(proc.stderr, encoding='utf-8')
    count = re.search(r'Ran (\d+) tests', proc.stderr)
    if proc.returncode and 'Declared 300 CPU second budget exhausted' in proc.stderr:
        raise TimeoutError('Independent trajectory CPU budget exhausted; logs retained')
    return {'executed': True, 'test_count': int(count.group(1)) if count else None,
            'returncode': proc.returncode, 'pass': proc.returncode == 0}


def reflection_run(output, deadline):
    # The historical audit writes beside __file__. Redirect its report without
    # modifying the repository or inserting any operation into forward evolution.
    command = ('import sys; import research.reflection_audit as a; '
               'a.__file__=sys.argv[1]; a.main()')
    proc = subprocess.run([sys.executable, '-c', command, str(output / 'reflection_audit.py')],
                          cwd=ROOT, capture_output=True, text=True,
                          timeout=max(0.01, deadline - time.monotonic()))
    (output / 'reflection.stdout.txt').write_text(proc.stdout, encoding='utf-8')
    (output / 'reflection.stderr.txt').write_text(proc.stderr, encoding='utf-8')
    if proc.returncode:
        raise AssertionError('Reflection audit failed; see logs')
    return read_json(output / 'reflection_audit_results.json') == read_json(ROOT / 'research/reflection_audit_results.json')


def run(output, allow_dirty=False, skip_tests=False):
    protocol = validate_named(read_json(ROOT / 'research/reproducibility/protocol.json'), 'protocol')
    base = check_engine()
    if protocol['base_engine_commit'] != base['engine_commit']:
        raise ValueError('Protocol baseline mismatch')
    if hashlib.sha256((ROOT / 'docs/MODEL.md').read_bytes()).hexdigest() != protocol['specification_sha256']:
        raise ValueError('Specification digest differs from frozen protocol')
    dirty = bool(git('status', '--porcelain', '--untracked-files=all'))
    if dirty and not allow_dirty:
        raise ValueError('Working tree is dirty; commit source or explicitly mark run exploratory with --allow-dirty')
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    (output / 'cases').mkdir()
    write_json(output / 'protocol.json', protocol)
    manifest = {'schema_version': 1, 'protocol_sha256': digest(protocol),
                'engine_commit': base['engine_commit'], 'checkout_commit': git('rev-parse', 'HEAD'),
                'working_tree_dirty': dirty, 'source_sha256': source_hashes(),
                'python': platform.python_version(), 'platform': platform.platform(),
                'command': sys.argv, 'coupling_fingerprints': {}}
    summary = {'schema_version': 1, 'protocol_id': protocol['protocol_id'],
               'execution_status': 'completed', 'implementation_status': 'failed',
               'scope': 'bundle_only' if skip_tests else 'full', 'cases': [],
               'negative_claim_result': {}, 'suite': {'executed': False},
               'reflection_certificate_equal': False, 'errors': []}
    start = time.monotonic()
    deadline = start + protocol['budget_wall_seconds']
    try:
        if not skip_tests:
            summary['suite'] = suite_run(output, deadline)
        for case in protocol['cases']:
            result, fingerprint = checked_case(case, output / 'cases' / case['id'], deadline)
            summary['cases'].append(result)
            manifest['coupling_fingerprints'][case['id']] = fingerprint
        summary['negative_claim_result'] = negative_claim()
        summary['reflection_certificate_equal'] = reflection_run(output, deadline)
        checks = [all(c['pass'] for c in summary['cases']),
                  summary['negative_claim_result']['implementation_check_pass'],
                  summary['reflection_certificate_equal'],
                  skip_tests or summary['suite'].get('pass', False)]
        if all(checks):
            summary['implementation_status'] = 'passed'
    except (TimeoutError, subprocess.TimeoutExpired) as error:
        summary.update(execution_status='budget_exhausted', implementation_status='inconclusive')
        summary['errors'].append(str(error))
    except Exception as error:
        summary['execution_status'] = 'error'
        summary['errors'].append(f'{type(error).__name__}: {error}')
    if source_hashes() != manifest['source_sha256']:
        summary.update(execution_status='error', implementation_status='failed')
        summary['errors'].append('Source files changed during execution; evidence is not a pinned run')
    write_json(output / 'manifest.json', validate_named(manifest, 'manifest'))
    write_json(output / 'result.json', validate_named(summary, 'result'))
    write_json(output / 'runtime.json', {'wall_seconds': time.monotonic() - start,
                                       'budget_wall_seconds': protocol['budget_wall_seconds']})
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--allow-dirty', action='store_true')
    parser.add_argument('--skip-tests', action='store_true', help='Evidence bundle only, not full acceptance')
    parser.add_argument('--compare-experiments', action='store_true', help='Ignore only suite/scope differences when comparing a bundle-only rerun')
    parser.add_argument('--compare', nargs=2, type=Path, metavar=('LEFT', 'RIGHT'))
    args = parser.parse_args()
    try:
        if args.compare:
            difference = compare_bundles(*args.compare, experiments_only=args.compare_experiments)
            print(json.dumps({'equal': difference is None, 'difference': difference}))
            return int(difference is not None)
        if args.output is None:
            parser.error('--output or --compare required')
        result = run(args.output, args.allow_dirty, args.skip_tests)
        print(json.dumps({'output': str(args.output), 'implementation_status': result['implementation_status'],
                          'execution_status': result['execution_status'], 'scope': result['scope']}))
        return int(result['implementation_status'] != 'passed')
    except (OSError, ValueError) as error:
        print(f'Reliability bundle: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
