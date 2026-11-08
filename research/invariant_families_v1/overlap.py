"""Frozen four-mask overlap of exact invariant families under baseline Rule3."""
from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import signal
import subprocess
import time

from universe24 import Channel, Coupling, Cube, Engine, State
from universe24.observation.clicks import clicks
from research.reference.algebra import algebra, coupling, DIRECTIONS
from research.presenter.export import capture, bundle
from research.experiments.run import recorded_states

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL = ROOT / 'research/clock_selection/invariant_overlap_protocol.json'
CP = Coupling((1, 1, 1))
ENGINE = Engine(CP)


class BudgetStop(RuntimeError):
    pass


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)


def write(path, value, compressed=False):
    path = Path(path)
    if path.exists():
        raise FileExistsError(path)
    data = (canonical(value) + '\n').encode()
    if compressed:
        data = gzip.compress(data, mtime=0)
    temporary = path.with_name(path.name + '.partial')
    temporary.write_bytes(data)
    temporary.replace(path)


def addresses(side=4):
    return [(*xyz, g) for xyz in itertools.product(range(side), repeat=3)
            for g in range(48)]


def patterns(aa):
    rotations = algebra().rotations
    return ([(1, 0, -1, 0)[a[0] % 4] for a in aa],
            [rotations[a[3]][1][1] for a in aa])


def donors(aa, side, tensor):
    index = {a: i for i, a in enumerate(aa)}
    return [[index[(*tuple((a[j] + DIRECTIONS[d][j]) % side for j in range(3)),
                   tensor.ports[d][a[3]])] for d in range(6)] for a in aa]


def initial(mask, aa=None):
    aa = addresses() if aa is None else aa
    vs, vi = patterns(aa)
    s, i = map(int, mask)
    return State(Cube(4), cells={a: Channel(0, s*x + i*y, 2)
                               for a, x, y in zip(aa, vs, vi)})


def scalar_oracle(steps):
    result = [(0, 1, 2)]
    for _ in range(steps):
        a, b, r = result[-1]
        q, rem = divmod(8*b + r, 6)
        result.append((b, q-a, rem))
    return result


def encode(triple, sign):
    a, b, r = triple
    return triple if sign == 1 else (-a, -b, 4-r+2*(r % 2)) if sign == -1 else (0, 0, 2)


def preflight(p):
    assert p['family']['side'] == 4 and p['family']['steps'] == 12
    assert p['family']['source_masks'] == ['00', '10', '01', '11']
    assert CP.fingerprint == p['baseline']['tensor_fingerprint']
    ref = coupling((1, 1, 1))
    assert (CP.ports, CP.weights) == (ref.ports, ref.weights)
    aa = addresses()
    vs, vi = patterns(aa)
    dd = donors(aa, 4, ref)
    assert Counter(vi[:48]) == {-1: 8, 0: 32, 1: 8}
    for pattern in (vs, vi):
        assert set(pattern) == {-1, 0, 1}
        for a, indexes, value in zip(aa, dd, pattern):
            assert sum(ref.weights[d][a[3]]*pattern[j]
                       for d, j in enumerate(indexes)) == 4*value
    complete = {}
    for mask in p['family']['source_masks']:
        state = initial(mask, aa)
        s, i = map(int, mask)
        values = [tuple(state.cells.get(a, state.background)) for a in aa]
        assert all(v == (0, s*x+i*y, 2) for v, x, y in zip(values, vs, vi))
        complete[mask] = values
    expected_db = [1 if x == y == 1 else -1 if x == y == -1 else 0
                   for x, y in zip(vs, vi)]
    assert Counter(expected_db) == {-1: 128, 0: 2816, 1: 128}
    changed = subprocess.check_output(['git', 'diff', '--name-only',
        p['baseline']['core_baseline_commit'], '--', 'universe24'], cwd=ROOT, text=True)
    assert not changed.strip(), 'Core differs from declared baseline'
    return {'status': 'passed_static_preflight', 'new_native_trajectories': 0,
            'addresses_checked': len(aa), 'pattern_eigenvalues': [4, 4],
            'internal_counts_per_node': {'-1': 8, '0': 32, '1': 8},
            'first_counter_defect_prediction': dict(sorted(Counter(expected_db).items())),
            'complete_initial_states': complete,
            'tensor': {'ports': CP.ports, 'weights': CP.weights, 'fingerprint': CP.fingerprint},
            'protocol_sha256': hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
            'producer_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


def check_budget():
    if time.process_time() > 17:
        raise BudgetStop('Producer CPU reserve reached; native checkpoints retained')


def observe(mask, states):
    aa = addresses()
    vs, vi = patterns(aa)
    ref = coupling((1, 1, 1))
    dd = donors(aa, 4, ref)
    dense = [[tuple(state.cells.get(a, state.background)) for a in aa] for state in states]
    trace = scalar_oracle(12)
    errors = []
    mismatch_counts = Counter()

    def mismatch(kind, detail):
        mismatch_counts[kind] += 1
        if len(errors) < 16:
            errors.append({'kind': kind, **detail})

    if mask in ('00', '10', '01'):
        pattern = [0]*len(aa) if mask == '00' else vs if mask == '10' else vi
        for t, frame in enumerate(dense):
            for a, actual, sign in zip(aa, frame, pattern):
                expected = encode(trace[t], sign)
                if actual != expected:
                    mismatch('standalone_full_state', {'state': t, 'address': a,
                             'actual': actual, 'expected': expected})
    all_inputs, all_C, event_checks = [], [], []
    for t, (old, new) in enumerate(zip(states, states[1:]), 1):
        check_budget()
        native_sums = ENGINE.input_sums(old)
        actual_inputs = [native_sums.get(a, 0) for a in aa]
        all_inputs.append(actual_inputs)
        old_values, new_values = dense[t-1], dense[t]
        expected_events = []
        terms_by_index = []
        for k, (a, indexes, before, after) in enumerate(zip(aa, dd, old_values, new_values)):
            terms = [ref.weights[d][a[3]]*old_values[j][1] for d, j in enumerate(indexes)]
            terms_by_index.append(terms)
            u = sum(terms)
            if actual_inputs[k] != u:
                mismatch('native_input', {'update': t, 'address': a,
                         'actual': actual_inputs[k], 'expected': u})
            q = after[1] + before[0]
            expected_after = (before[1], (2*u+before[2])//6-before[0], (2*u+before[2]) % 6)
            if after != expected_after:
                mismatch('independent_local_transition', {'update': t, 'address': a,
                         'actual': after, 'expected': expected_after})
            if q and before != after:
                expected_events.append((a, u % 3, q))
            if t == 1:
                s, i = map(int, mask)
                expected_u = 4*(s*vs[k]+i*vi[k])
                if u != expected_u:
                    mismatch('first_input_prediction', {'address': a, 'actual': u,
                             'expected': expected_u})
        native_events = sorted((e.address, e.kind, e.quotient) for e in clicks(old, new, t))
        matched = native_events == expected_events
        if not matched:
            mismatch('raw_C_list', {'update': t, 'actual_count': len(native_events),
                     'expected_count': len(expected_events)})
        event_checks.append({'update': t, 'complete_list_equal': matched,
                             'native_count': len(native_events), 'expected_count': len(expected_events)})
        index = {a: k for k, a in enumerate(aa)}
        for a, kind, q in native_events:
            k = index[a]
            all_C.append({'step': t, 'address': a, 'kind': kind, 'ell': q,
                          'before': old_values[k], 'after': new_values[k],
                          'u': actual_inputs[k], 'six_signed_donor_values': terms_by_index[k]})
    equalities = [[i, j] for i in range(len(states)) for j in range(i+1, len(states))
                  if states[i] == states[j]]
    return {'mask': mask, 'address_order': 'lexicographic x,y,z,g; all 3072 addresses',
            'all_native_input_sums': all_inputs, 'all_C': all_C,
            'C_counts': {str(k): sum(row['kind'] == k for row in all_C) for k in range(3)},
            'event_checks': event_checks, 'mismatch_counts': dict(mismatch_counts),
            'first16_counterexamples': errors, 'all_registered_checks_pass': not mismatch_counts,
            'scalar_oracle': trace if mask != '11' else None,
            'exact_whole_state_equalities': equalities}, dense


def defects(frames):
    aa = addresses()
    vs, vi = patterns(aa)
    rows = []
    expected_db = [1 if x == y == 1 else -1 if x == y == -1 else 0
                   for x, y in zip(vs, vi)]
    for t in range(13):
        check_budget()
        values = [[frames['11'][t][k][j]-frames['10'][t][k][j]
                   -frames['01'][t][k][j]+frames['00'][t][k][j]
                   for k in range(len(aa))] for j in range(3)]
        rows.append({'state': t, 'D_a': values[0], 'D_b': values[1], 'D_r': values[2],
                     'histograms': {name: dict(sorted(Counter(value).items()))
                                    for name, value in zip(('D_a', 'D_b', 'D_r'), values)}})
    first = rows[1]
    passing = (first['D_a'] == [0]*len(aa) and first['D_b'] == expected_db
               and first['D_r'] == [-6*v for v in expected_db])
    return {'address_order': 'lexicographic x,y,z,g; all 3072 addresses',
            'states': rows, 'first_step_predictions_pass': passing,
            'later_arrays_scope': 'Descriptive fixed follow-up; no later additive closure is assumed.'}


def source_hashes():
    paths = [Path(__file__), HERE/'overlap_budget.py', HERE/'__init__.py', PROTOCOL,
             ROOT/'research/reference/algebra.py', ROOT/'research/reference/__init__.py']
    for directory in ('universe24', 'research/presenter', 'research/experiments', 'research/components'):
        paths.extend((ROOT/directory).rglob('*.py'))
    return {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(set(paths))}


def run(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    (output/'native').mkdir()
    (output/'records').mkdir()
    p = json.loads(PROTOCOL.read_text())
    frozen = source_hashes()
    (output/'protocol.json').write_bytes(PROTOCOL.read_bytes())
    for relative in frozen:
        target = output/'executed_sources'/relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT/relative).read_bytes())
    ledger, native, examples, dense = [], [], [], {}
    failure = None
    primary = False
    try:
        registration = {'source_sha256': frozen, 'preflight': preflight(p),
                        'checkout_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                        'registered_before_first_native_step': True}
        write(output/'registration.json', registration)
        for mask in p['family']['source_masks']:
            check_budget()
            case = {'id': 'overlap-'+mask, 'mask': mask, 'side': 4, 'steps': 12, 'seed': None}
            experiment = capture(ENGINE, initial(mask), 12, id=case['id'],
                title='Invariant overlap: '+mask, description=p['scope'],
                view={'position': [0, 0, 0], 'channel': 0}, max_frames=13,
                max_cells=39936, max_bytes=4*1024*1024, max_seconds=30)
            experiment['provenance'].update({'overlap_case': case,
                'protocol_sha256': registration['preflight']['protocol_sha256']})
            native_path = output/'native'/(case['id']+'.json.gz')
            write(native_path, {'case': case, 'experiment': experiment}, compressed=True)
            native.append({'id': case['id'], 'mask': mask, 'record': str(native_path.relative_to(output)),
                           'sha256': hashlib.sha256(native_path.read_bytes()).hexdigest()})
            write(output/('checkpoint-'+mask+'.json'), {'native_checkpoints': native,
                  'observed_masks': [row['mask'] for row in ledger],
                  'captured_but_not_observed': [row['mask'] for row in native
                      if row['mask'] not in {r['mask'] for r in ledger}]})
            observations, dense[mask] = observe(mask, recorded_states(experiment))
            record_path = output/'records'/(case['id']+'.json.gz')
            write(record_path, {'case': case, 'observations': observations,
                  'native_record': str(native_path.relative_to(output)),
                  'native_sha256': native[-1]['sha256']}, compressed=True)
            ledger.append({'id': case['id'], 'mask': mask, 'record': str(record_path.relative_to(output)),
                'sha256': hashlib.sha256(record_path.read_bytes()).hexdigest(),
                'all_registered_checks_pass': observations['all_registered_checks_pass'],
                'full_rewind_equal': experiment['provenance']['full_rewind_equal'],
                'all_inverse_frames_equal': all(frame['audit']['inverse_equal'] for frame in experiment['frames'][1:]),
                'C_counts': observations['C_counts']})
            examples.append(experiment)
            if sum(f.stat().st_size for f in output.rglob('*') if f.is_file()) > 12*1024*1024:
                raise BudgetStop('Storage reserve reached; completed native data retained')
            print(f'{len(ledger)}/4 overlap-{mask}', flush=True)
        interaction = defects(dense)
        write(output/'interaction_defects.json.gz', interaction, compressed=True)
        primary = interaction['first_step_predictions_pass']
        write(output/'experiments.json', bundle(examples, title='The Presenter: invariant-family overlap'))
    except Exception as error:
        failure = {'type': type(error).__name__, 'message': str(error),
                   'mask': locals().get('mask')}
        write(output/'failure.json', failure)
    unchanged = source_hashes() == frozen
    result = {'status': 'completed' if len(ledger) == 4 and failure is None else 'inconclusive',
              'failure': failure, 'completed_cases': len(ledger), 'cases': ledger,
              'native_checkpoints': native, 'sources_unchanged': unchanged,
              'first_step_predictions_pass': primary,
              'accepted': len(ledger) == 4 and failure is None and unchanged and primary
                  and all(r['all_registered_checks_pass'] and r['full_rewind_equal']
                          and r['all_inverse_frames_equal'] for r in ledger),
              'captured_but_not_observed': [r['mask'] for r in native if r['mask'] not in {v['mask'] for v in ledger}],
              'not_captured': [m for m in p['family']['source_masks'] if m not in {v['mask'] for v in native}],
              'scope': p['scope'], 'child_cpu_seconds_at_result': time.process_time(),
              'independent_audit_required': True}
    write(output/'result.json', result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--preflight-output', type=Path)
    mode.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.preflight_output:
        args.preflight_output.parent.mkdir(parents=True, exist_ok=True)
        write(args.preflight_output, preflight(json.loads(PROTOCOL.read_text())))
    else:
        def exhausted(signum, frame):
            raise BudgetStop('CPU soft limit reached; prior native checkpoints retained')
        signal.signal(signal.SIGXCPU, exhausted)
        run(args.output)


if __name__ == '__main__':
    main()
