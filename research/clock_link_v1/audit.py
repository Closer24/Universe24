"""Fresh bounded reconstruction audit; original deleted local receipts are not used."""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from universe24 import State
from universe24.observation.clicks import classify
from research.components import BoardSpec, finalize, plain
from research.component_families.oracle import step as independent_step, click as independent_click
from research.clock_link_v1.components import (assemble_clock_link, clock_link_parts,
                                              echo_parity, target_record)
from research.clock_link_v1.exact import closed_state, s

BACKGROUND = (0, 0, 2)
BASE_COMMIT = '37fe77be8f489ba722ac687ff544b3956352e62f'


def sparse(state):
    return {a: tuple(v) for a, v in state.cells.items()}


def digest(state):
    rows = [[*a, *v] for a, v in sorted(state.items())]
    return hashlib.sha256(json.dumps(rows, separators=(',', ':')).encode()).hexdigest()


def pins():
    files = [*sorted((ROOT/'universe24').rglob('*.py')),
             *sorted((ROOT/'research/clock_link_v1').glob('*.py')),
             ROOT/'research/component_families/oracle.py',
             ROOT/'research/reference/algebra.py',
             *sorted((ROOT/'research/components').glob('*.py'))]
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}


def check_case(D, side, delay, source, terminated):
    P, Q = 4*(D+1), 2*(D+1)
    horizon = 2*P+delay if source else 1
    parameters = dict(distance=D, side=side, delay=delay, source_present=source,
                      terminated=terminated)
    prepared = assemble_clock_link(**parameters)
    engine, state = prepared.engine, prepared.initial
    initial = state
    origin = (4,4,4)
    addresses = {'source': (*origin,0), 'port': (5,4,4,0), 'target': (4+D,4,4,0)}
    events = {k: [] for k in addresses}
    hashes = []
    all_events = 0
    complete_formula_states = 0
    for t in range(horizon+1):
        old = sparse(state)
        hashes.append(digest(old))
        if not source:
            assert state == initial
        elif terminated and t >= delay:
            tau = t-delay
            assert old == closed_state(D,tau,side)
            complete_formula_states += 1
            src = state.at(addresses['source'])
            assert (src.a,src.b) == (s(tau-1) if tau else 0,s(tau))
            assert echo_parity(src) == (tau//Q)%2
            cycle = tau%P
            expected = 4 if D+2 <= cycle <= 3*D+1 else (
                1 if D <= cycle <= D+1 or 3*D+2 <= cycle <= 3*D+3 else 0)
            assert target_record(state.at(addresses['target'])) == expected
            if tau%P == 0:
                assert old == closed_state(D,0,side)
        elif source and not terminated and t >= delay:
            assert echo_parity(state.at(addresses['source'])) == 0
        if t == horizon:
            break
        next_state = engine.advance(state)
        new = sparse(next_state)
        assert independent_step(old,side) == new
        assert engine.rewind(next_state) == state
        assert independent_step(new,side,reverse=True) == old
        for address in old.keys() | new.keys():
            before = state.at(address)
            after = next_state.at(address)
            native = classify(before,after)
            kind = independent_click(tuple(before),tuple(after))
            assert (native[0] if native else None) == kind
            if native is not None:
                all_events += 1
        for name,address in addresses.items():
            event = classify(state.at(address),next_state.at(address))
            if event is not None:
                events[name].append([t+1,*event])
        state = next_state
    assert not events['source']
    if source and terminated:
        expected_port = sorted([[delay+1+n*Q,1,1] for n in range(4)] +
                               [[delay+2*D+1+n*Q,2,-1] for n in range(4)])
        expected_target = sorted([[delay+D+n*Q,1,1] for n in range(4)] +
                                 [[delay+D+2+n*Q,2,-1] for n in range(4)])
        assert events['port'] == expected_port
        assert events['target'] == expected_target
    elif source:
        assert events['port'] == [[delay+1,1,1]]
        assert events['target'] == [[delay+D,1,1]]
    else:
        assert not any(events.values())
    backward = sparse(state)
    for t in range(horizon-1,-1,-1):
        state = engine.rewind(state)
        backward = independent_step(backward,side,reverse=True)
        assert sparse(state) == backward
        assert digest(backward) == hashes[t]
    assert state == initial
    return {'parameters': parameters, 'seed': None, 'horizon': horizon,
            'complete_states': len(hashes), 'transitions': horizon,
            'full_state_sha256': hashes, 'native_events_recomputed': all_events,
            'complete_formula_states': complete_formula_states,
            'events': events, 'coupling_fingerprint': engine.coupling.fingerprint,
            'initial_sparse': [[*a,*v] for a,v in sorted(sparse(initial).items())],
            'background': list(BACKGROUND), 'forward_inverse_full_rewind': True}


def composition_check():
    side = 389
    a = clock_link_parts(distance=20,side=side,origin=(4,4,4),name_prefix='a-')
    b = clock_link_parts(distance=28,side=side,origin=(48,16,48),delay=1,
                         orientation=4,name_prefix='b-')
    prepared = finalize(BoardSpec(side),a+b)
    separate = [finalize(BoardSpec(side),parts) for parts in (a,b)]
    state = prepared.initial
    isolated = [p.initial for p in separate]
    hashes = []
    for t in range(234):
        old = sparse(state)
        fragments = [sparse(x) for x in isolated]
        assert not (fragments[0].keys() & fragments[1].keys())
        assert old == {**fragments[0],**fragments[1]}
        hashes.append(digest(old))
        if t < 233:
            new = prepared.engine.advance(state)
            assert independent_step(old,side) == sparse(new)
            assert prepared.engine.rewind(new) == state
            assert independent_step(sparse(new),side,reverse=True) == old
            state = new
            isolated = [p.engine.advance(x) for p,x in zip(separate,isolated)]
    backward = sparse(state)
    for t in range(232,-1,-1):
        state = prepared.engine.rewind(state)
        backward = independent_step(backward,side,reverse=True)
        assert sparse(state) == backward and digest(backward) == hashes[t]
    assert state == prepared.initial
    return {'complete_states': 234, 'transitions':233, 'full_state_sha256':hashes,
            'manifest': plain(prepared.manifest),
            'scope':'Separated coexistence, not inter-link interaction',
            'independent_forward_inverse_full_rewind':True}


def run():
    source_pins = pins()
    cases = [check_case(*args) for args in itertools.product(
        (14,20,28),(389,431),(0,1),(False,True),(False,True))]
    for a,b in itertools.combinations(cases,2):
        pa,pb = a['parameters'],b['parameters']
        if {k:v for k,v in pa.items() if k!='side'} == {k:v for k,v in pb.items() if k!='side'}:
            assert a['full_state_sha256'] == b['full_state_sha256']
    composition = composition_check()
    assert pins() == source_pins
    return {'format':'universe24-clock-link-reconstruction-v1','status':'PASS',
            'base_commit':BASE_COMMIT,'prior_local_receipts_reused':False,
            'provenance':'Fresh reproduction after workspace maintenance; historical local counts are not this evidence.',
            'protocol':{'distances':[14,20,28],'sides':[389,431],'delays':[0,1],
                        'masks':'all source/termination combinations',
                        'active_horizon':'twice the canonical finite-guide period plus startup delay; same horizon for nonperiodic long-guide controls',
                        'null_horizon':1,'background':[0,0,2],'body_signs':[1,1,1],
                        'seed':None,'readouts':'fixed before this recovery audit',
                        'max_cpu_seconds':180,'max_output_bytes':104857600},
            'summary':{'cases':len(cases),'complete_states':sum(c['complete_states'] for c in cases),
                       'transitions':sum(c['transitions'] for c in cases),
                       'native_events_recomputed':sum(c['native_events_recomputed'] for c in cases),
                       'complete_formula_states':sum(c['complete_formula_states'] for c in cases),
                       'paired_size_comparisons':24},
            'source_sha256':source_pins,'cases':cases,'composition':composition,
            'physical_light_or_gravity_derived':False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    if args.output and args.output.exists():
        raise FileExistsError('Refusing to overwrite an existing receipt')
    start = time.process_time()
    result = run()
    elapsed = time.process_time()-start
    assert elapsed < 180, 'Audit CPU budget exceeded'
    serialized = (json.dumps(result,indent=2)+'\n').encode('utf-8')
    assert len(serialized) <= 104857600, 'Receipt output byte budget exceeded'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open('xb') as handle:
            handle.write(serialized)
    print(json.dumps({'status':result['status'],'summary':result['summary'],
                      'composition_states':result['composition']['complete_states'],
                      'cpu_seconds_after_imports':elapsed,
                      'receipt_bytes':len(serialized),
                      'output':str(args.output) if args.output else None},indent=2))


if __name__ == '__main__':
    main()
