"""Exact bounded local motif-parity memory and history-dependent messages.

python -m experiments.complexity.structural_memory --out runs/complexity-research/02-memory
The declared protocol and proof are in docs/research/complexity/02-memory.md.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np

from universe24.core import Engine, State, Tensor
from universe24.observe.causal_wave import changed_sites, inside_cone

BASELINE = '7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2'
NAMES = ('mem.A', 'mem.B', 'mem.bit', 'mem.probe', 'mem.receiver', 'mem.readout')
O, E, W = (0, 0, 0), (1, 0, 0), (-1, 0, 0)
CASES = ('quiet', 'constant', 'coincident', 'separated', 'random', 'shuffled',
         'bit_probe_scale2', 'global_scale2')


def tensor(*, learning=True, memory_readout=True, boolean_memory=False):
    """Fixed before evolution; no parameters selected from observed results."""
    terms = []
    def f(name, offset=O):
        return (name, offset, 'b')
    for name in ('mem.A', 'mem.B', 'mem.probe', 'mem.readout'):
        terms.extend((name, 3, (f(name, offset),)) for offset in (E, W))
    terms.extend([('mem.bit', 6, (f('mem.bit'),)),
                  ('mem.receiver', 6, (f('mem.receiver'),))])
    if learning:
        for offset in (O, E):
            terms.append(('mem.bit', -6, (f('mem.bit'), f('mem.A', offset), f('mem.B', offset))))
            if boolean_memory:
                terms.append(('mem.bit', 3, (f('mem.A', offset), f('mem.B', offset))))
    drive = (f('mem.receiver'), f('mem.probe'))
    if memory_readout:
        if boolean_memory:
            terms.append(('mem.readout', -6, drive + (f('mem.bit'),)))
        else:
            drive += (f('mem.bit'),)
    terms.append(('mem.readout', 3, drive))
    return Tensor(NAMES, terms, strict_support=True)


def prepare(law, side, case, *, learning=True, bit_flip=False, boolean_memory=False):
    """Complete initial histories; no mid-run intervention or reseeding."""
    a = np.zeros((law.G, side**3), dtype=np.int64)
    b = a.copy()
    r = np.arange(law.G * side**3, dtype=np.int64).reshape(a.shape) % 6
    state = State(side, a, b, r)
    a, b = state.a, state.b
    ia, ib, im, ip, ig, ir = range(6)
    center = (side//2,) * 3
    target = state.lattice.index(*center)
    source = state.lattice.index(0, center[1], center[2])
    b[im] = 1
    b[ig, target] = 1
    # On L5, the motif flips target at t3, both local A/B histories are quiet
    # at t4, and the probe drives the readout at t5.
    b[ip, state.lattice.index(center[0]+1, center[1], center[2])] = 1
    mode = 'coincident' if case in ('bit_probe_scale2', 'global_scale2') else case
    if mode == 'constant':
        b[ia] = b[ib] = 1
    elif mode in ('coincident', 'separated'):
        b[ia, source] = 1
        b[ib, source if mode == 'coincident' else state.lattice.index(1, center[1], center[2])] = 1
    elif mode in ('random', 'shuffled'):
        rng = np.random.default_rng(1729)
        b[ia:ib+1] = rng.integers(0, 2, (2, side**3))
        if mode == 'shuffled':
            b[ib] = np.random.default_rng(1730).permutation(b[ib])
    elif mode != 'quiet':
        raise ValueError('unknown predeclared preparation')
    if bit_flip:
        b[im, target] = -1
    plus = state.lattice.shift_index(E)
    for gear in (ia, ib, ip):
        a[gear] = b[gear, plus]
    a[ig] = b[ig]
    a[im] = b[im] * (1 - 2*b[ia, plus]*b[ib, plus]) if learning else b[im]
    if case == 'bit_probe_scale2':
        for gear in (im, ip):
            a[gear] *= 2
            b[gear] *= 2
    elif case == 'global_scale2':
        a *= 2
        b *= 2
    if boolean_memory:
        if case in ('bit_probe_scale2', 'global_scale2'):
            raise ValueError('secondary Boolean handoff excludes amplitude-scaled memory preparations')
        a[im] = (1-a[im])//2
        b[im] = (1-b[im])//2
    return state


def digest(state):
    return hashlib.sha256(json.dumps(state.to_dict(), separators=(',', ':')).encode()).hexdigest()


def save_state(path, state):
    with gzip.open(path, 'wt') as stream:
        json.dump(state.to_dict(), stream, separators=(',', ':'))
        stream.write('\n')


def bit_metrics(state):
    values = np.sign(state.b[2]).astype(np.int64)
    edges = []
    for axis in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
        adjacent = values[state.lattice.shift_index(axis)]
        edges.extend(zip(values.tolist(), adjacent.tolist()))
    return {'site_sign_types': len(set(values.tolist())), 'edge_sign_types': len(set(edges)),
            'domain_walls': sum(a != b for a, b in edges), 'negative_sites': int(np.count_nonzero(values < 0)),
            'normalized_sign_fingerprint': hashlib.sha256(values.tobytes()).hexdigest()}


def run_case(out, side, case, *, steps=80, max_bits=128, learning=True,
             memory_readout=True, bit_flip=False, name=None):
    law = tensor(learning=learning, memory_readout=memory_readout)
    seed = prepare(law, side, case, learning=learning, bit_flip=bit_flip)
    state, engine = seed, Engine(law)
    case_name = name or f'L{side}-{case}'
    path = out/case_name
    path.mkdir(parents=True, exist_ok=True)
    (path/'tensor.json').write_text(json.dumps(law.to_dict(), indent=2)+'\n')
    save_state(path/'seed.json.gz', seed)
    target = seed.lattice.index(*((side//2,)*3))
    expected_bit_abs = 2 if case == 'bit_probe_scale2' else 1
    binary_sector = case != 'global_scale2'
    forward_shift = seed.lattice.shift_index(W)
    records = [{'tick': 0, 'bit': list(seed.gear(2, target)), 'readout': list(seed.gear(5, target)),
                'bit_metrics': bit_metrics(seed)}]
    states = [seed]
    click_kinds, periods, first_return = Counter(), [], None
    max_seen_bits, quiet_durable = 0, True
    for tick in range(1, steps+1):
        after = engine.step(state)
        if binary_sector:
            for gear in (0, 1, 3):
                assert np.array_equal(after.b[gear], state.b[gear, forward_shift])
            expected = state.b[2]*(1 - 2*state.b[0]*state.b[1]) if learning else state.b[2]
            assert np.array_equal(after.b[2], expected)
            assert all(abs(int(v)) == expected_bit_abs for v in after.b[2])
            quiet = (state.b[0]*state.b[1] == 0)
            quiet_durable &= bool(np.array_equal(after.b[2, quiet], state.b[2, quiet]))
        assert np.array_equal(after.r, seed.r)
        clicks = engine.clicks(state, after, tick)
        click_kinds.update(map(int, clicks.kind))
        event = [(int(q), int(k)) for g, n, q, k in
                 zip(clicks.gear, clicks.node, clicks.quotient, clicks.kind) if g == 5 and n == target]
        bits = after.max_abs().bit_length()
        max_seen_bits = max(max_seen_bits, bits)
        records.append({'tick': tick, 'bit': list(after.gear(2, target)),
            'readout': list(after.gear(5, target)), 'local_A': list(state.gear(0, target)),
            'local_B': list(state.gear(1, target)), 'local_probe': list(state.gear(3, target)),
            'readout_event': event, 'max_bits': bits, 'bit_metrics': bit_metrics(after)})
        if all(np.array_equal(getattr(after, field)[:3], getattr(seed, field)[:3]) for field in ('a', 'b', 'r')):
            periods.append(tick)
        if first_return is None and after.same_as(seed):
            first_return = tick
        state = after
        states.append(state)
        if bits > max_bits:
            break
    assert engine.rewind(state, len(records)-1).same_as(seed)
    if binary_sector and len(records) > 2*side:
        assert 2*side in periods
    save_state(path/'final.json.gz', state)
    report = {'name': case_name, 'L': side, 'case': case, 'learning': learning,
        'memory_readout': memory_readout, 'bit_flip': bit_flip,
        'requested_updates': steps, 'completed_updates': len(records)-1,
        'stop_reason': 'bit_limit_after_complete_update' if max_seen_bits > max_bits else 'horizon',
        'binary_signal_proof_applies': binary_sector, 'max_bits': max_seen_bits,
        'quiet_bit_durability_verified': quiet_durable if binary_sector else None,
        'memory_subsystem_return_updates': periods, 'first_full_state_return': first_return,
        'click_kind_counts': {f'C{k}': click_kinds[k] for k in (0,1,2)},
        'complete_rewind_exact': True, 'seed_sha256': digest(seed), 'final_sha256': digest(state),
        'tensor_fingerprint': law.fingerprint, 'strict_support_violations': len(law.support_violations()),
        'source_A_population': int(seed.b[0].sum()), 'source_B_population': int(seed.b[1].sum()),
        'initial_coincidences': int(np.count_nonzero(seed.b[0]*seed.b[1])), 'records': records}
    (path/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    return report, states


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=Path('runs/complexity-research/02-memory'))
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)
    cases, trajectories = [], {}
    for side in (3, 5):
        for case in CASES:
            report, states = run_case(args.out, side, case)
            cases.append(report)
            trajectories[report['name']] = states
    # Matched counterfactual controls fixed before running.
    for case in ('coincident', 'separated'):
        for mode in ('no_learning', 'no_memory_readout'):
            name = 'L5-'+case+'-'+mode
            report, states = run_case(args.out, 5, case, learning=mode != 'no_learning',
                memory_readout=mode != 'no_memory_readout', name=name)
            cases.append(report)
            trajectories[name] = states
    for flip in (False, True):
        name = 'L5-quiet-matched-bit-'+str(int(flip))
        report, states = run_case(args.out, 5, 'quiet', bit_flip=flip, name=name)
        cases.append(report)
        trajectories[name] = states
    target = trajectories['L5-coincident'][0].lattice.index(2, 2, 2)
    history_a, history_b = trajectories['L5-coincident'], trajectories['L5-separated']
    # At the readout's old snapshot the signal histories, probe, receiver and
    # readout are identical locally; only the retained bit differs.
    for gear in (0, 1, 3, 4, 5):
        assert history_a[4].gear(gear, target) == history_b[4].gear(gear, target)
    assert history_a[4].gear(2, target) != history_b[4].gear(2, target)
    assert int(history_a[5].b[5, target]) == -1 and int(history_b[5].b[5, target]) == 1
    future_readout_equal_without_memory = True
    for a, b in zip(trajectories['L5-coincident-no_memory_readout'], trajectories['L5-separated-no_memory_readout']):
        for field in ('a', 'b', 'r'):
            future_readout_equal_without_memory &= bool(np.array_equal(getattr(a, field)[5], getattr(b, field)[5]))
    assert future_readout_equal_without_memory
    same, flipped = trajectories['L5-quiet-matched-bit-0'], trajectories['L5-quiet-matched-bit-1']
    initial_support = [same[0].lattice.coords(n) for n in changed_sites(same[0], flipped[0])]
    assert initial_support == [(2, 2, 2)]
    for tick, (a, b) in enumerate(zip(same, flipped)):
        assert all(inside_cone(a.lattice, node, initial_support, tick) for node in changed_sites(a, b))
        for gear in (0, 1, 3, 4):
            assert all(np.array_equal(getattr(a, field)[gear], getattr(b, field)[gear]) for field in ('a', 'b', 'r'))
    assert int(same[5].b[5, target]) == 1 and int(flipped[5].b[5, target]) == -1
    neighbor = same[0].lattice.index(3, 2, 2)
    assert int(same[6].b[5, neighbor]) == 1 and int(flipped[6].b[5, neighbor]) == -1
    scale_sign_equal = True
    for side in (3, 5):
        for a,b in zip(trajectories[f'L{side}-coincident'], trajectories[f'L{side}-bit_probe_scale2']):
            scale_sign_equal &= bool(np.array_equal(np.sign(a.b[2]), np.sign(b.b[2])))
            assert np.array_equal(b.b[5], 4*a.b[5])
    assert scale_sign_equal
    # Secondary exact 0/1 encoding requested by the rotor peer after the
    # primary grid; its fixed coefficients/domain are separately declared.
    boolean_handoff = []
    for side in (3, 5):
        for case in ('coincident', 'separated'):
            law = tensor(boolean_memory=True)
            state = prepare(law, side, case, boolean_memory=True)
            seed, engine = state, Engine(law)
            path = args.out/f'boolean-L{side}-{case}'
            path.mkdir(parents=True, exist_ok=True)
            (path/'tensor.json').write_text(json.dumps(law.to_dict(), indent=2)+'\n')
            save_state(path/'seed.json.gz', seed)
            for tick, signed in enumerate(trajectories[f'L{side}-{case}']):
                if tick:
                    state = engine.step(state)
                for field in ('a', 'b'):
                    assert np.array_equal(getattr(signed, field)[2], 1-2*getattr(state, field)[2])
                for field in ('a', 'b', 'r'):
                    other = [0,1,3,4,5]
                    assert np.array_equal(getattr(signed, field)[other], getattr(state, field)[other])
                assert np.array_equal(state.r, seed.r)
                assert all(int(v) in (0,1) for v in state.b[2])
            assert engine.rewind(state, 80).same_as(seed)
            save_state(path/'final.json.gz', state)
            boolean_handoff.append({'L': side, 'case': case, 'updates': 80,
                'both_memory_histories_match_signed_encoding': True,
                'all_other_triples_match': True, 'complete_rewind_exact': True,
                'seed_sha256': digest(seed), 'final_sha256': digest(state),
                'tensor_fingerprint': law.fingerprint})
    root = Path(__file__).resolve().parents[2]
    report = {'baseline_main': BASELINE, 'candidate': 'bounded local motif-parity memory',
        'proof_domain': 'Binary A,B with prepared a=F^-1(b); bit/probe amplitudes may be rescaled separately.',
        'runs': cases, 'all_rewinds_exact': all(c['complete_rewind_exact'] for c in cases),
        'history_intervention': {'compared_old_snapshot': 4, 'same_local_complete_signals': True,
            'later_receiver_b_at_tick5': [-1, 1], 'readouts_equal_when_memory_coupling_removed': True},
        'same_signal_bit_intervention': {'initial_difference_support': initial_support,
            'first_receiver_response_tick': 5, 'neighbor_message_tick': 6,
            'complete_state_difference_cones_verified': True},
        'bit_probe_scale_control': {'normalized_memory_signs_equal': scale_sign_equal,
                                   'readout_magnitude_factor': 4},
        'secondary_boolean_handoff': boolean_handoff,
        'unbounded_complexity_claimed': False, 'new_C2_mechanism_claimed': False,
        'source_sha256': {name: hashlib.sha256((root/name).read_bytes()).hexdigest() for name in
            ('experiments/complexity/structural_memory.py', 'universe24/core/engine.py',
             'universe24/core/tensor.py', 'universe24/observe/causal_wave.py')}}
    (args.out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'cases': len(cases), 'all_rewinds_exact': report['all_rewinds_exact'],
        'secondary_boolean_encoding_cases': len(boolean_handoff),
        'bounded_memory_and_intervention_passed': True,
        'stops': [{'case': c['name'], 'updates': c['completed_updates'], 'bits': c['max_bits']} for c in cases
                  if c['stop_reason'] != 'horizon'],
        'source_sha256': report['source_sha256']}, indent=2))


if __name__ == '__main__':
    main()
