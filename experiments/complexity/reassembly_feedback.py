"""Bounded reversible message rotors and retained density, not a complexity law."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import argparse
from collections import Counter, deque
import gzip
import hashlib
from itertools import product
import json
import numpy as np
from universe24.core import Engine, State, Tensor
from experiments.cosmology.recurrent_bursts import structural_snapshot, ReassemblyTracker, progressive_reassemblies

AXES = ('x', 'y', 'z')
KINDS = ('comm.plus', 'comm.minus', 'memory', 'ref.density')
NAMES = tuple(f'{kind}.{axis}.{bank}' for axis in AXES for bank in ('X', 'Y') for kind in KINDS)
ZERO = (0, 0, 0)


def build(*, connected=True):
    terms = []
    for axis_id, axis in enumerate(AXES):
        e = tuple(int(k == axis_id) for k in range(3))
        for target_bank, source_bank, inverse_collision, inverse_stream in (
                ('X', 'Y', False, True), ('Y', 'X', True, False)):
            names = {k: f'{k}.{axis}.{source_bank}' for k in KINDS}
            p, n, m, density = (names[k] for k in KINDS)
            def add(kind, coefficient, *factors):
                terms.append((f'{kind}.{axis}.{target_bank}', 3*coefficient,
                    tuple((name, off, 'b') for name, off in factors)))
            # Local C or C^-1. The inverse rotor uses the new memory's complement.
            for kind, here, other in (('comm.plus', p, n), ('comm.minus', n, p)):
                if not connected:
                    add(kind, 1, (here, ZERO))
                elif inverse_collision:
                    add(kind, 1, (other, ZERO))
                    add(kind, 1, (m, ZERO), (here, ZERO))
                    add(kind, -1, (m, ZERO), (other, ZERO))
                else:
                    add(kind, 1, (here, ZERO))
                    add(kind, 1, (m, ZERO), (other, ZERO))
                    add(kind, -1, (m, ZERO), (here, ZERO))
            for coefficient, factors in ((1,(m,)),(1,(p,)),(1,(n,)),(-2,(p,n)),
                    (-2,(m,p)),(-2,(m,n)),(4,(m,p,n))):
                add('memory', coefficient, *((g,ZERO) for g in factors))
            add('ref.density', 1, (density, ZERO))
            # S or S^-1: stream opposite message directions, retain memory,
            # and update the separate density register by discrete continuity.
            for kind, g, direction in (('comm.plus',p,e), ('comm.minus',n,tuple(-v for v in e))):
                off = direction if inverse_stream else tuple(-v for v in direction)
                add(kind, 1, (g, off))
                add('ref.density', 1, (g, off))
                add('ref.density', -1, (g, ZERO))
            add('memory', 1, (m, ZERO))
            add('ref.density', 1, (density, ZERO))
    return Tensor(NAMES, terms, strict_support=True)


def map_fields(fields, lattice, *, connected=True, inverse=False):
    """Independent first-order specification F(X,Y)=(C(Y),S(X))."""
    result = np.empty_like(fields)
    def g(kind, axis, bank): return NAMES.index(f'{kind}.{axis}.{bank}')
    for axis_id, axis in enumerate(AXES):
        e = tuple(int(k == axis_id) for k in range(3))
        collision_source, collision_target = ('X','Y') if inverse else ('Y','X')
        p,n,m,r = (fields[g(k,axis,collision_source)] for k in KINDS)
        selector = (1-m if inverse else m) if connected else 0
        vals = (p+selector*(n-p), n+selector*(p-n),
                m+p+n-2*p*n-2*m*p-2*m*n+4*m*p*n, r)
        for kind,value in zip(KINDS,vals): result[g(kind,axis,collision_target)] = value
        stream_source, stream_target = ('Y','X') if inverse else ('X','Y')
        p,n,m,r = (fields[g(k,axis,stream_source)] for k in KINDS)
        off = e if inverse else tuple(-v for v in e)
        pp = p[lattice.shift_index(off)]
        nn = n[lattice.shift_index(tuple(-v for v in off))]
        for kind,value in zip(KINDS,(pp,nn,m,r+pp+nn-p-n)):
            result[g(kind,axis,stream_target)] = value
    return result


def prepare(*, L=5, connected=True, memory_intervention=False, messages=True):
    tensor = build(connected=connected)
    empty = Engine(tensor).vacuum(L, [0]*tensor.G)
    b = empty.b.astype(object)
    center = (L//2,)*3
    node = empty.lattice.index(*center)
    for axis in AXES:
        for bank in ('X','Y'):
            for kind in ('comm.plus','comm.minus'):
                b[tensor.gear_index(f'{kind}.{axis}.{bank}'),node] = int(messages)
            b[tensor.gear_index(f'ref.density.{axis}.{bank}'),node] = 2*int(messages)
    if memory_intervention:
        target = empty.lattice.index(center[0]+1,center[1],center[2])
        for bank in ('X','Y'): b[tensor.gear_index(f'memory.x.{bank}'),target] = 1
    a = map_fields(b,empty.lattice,connected=connected,inverse=True)
    r = np.arange(tensor.G*L**3).reshape(tensor.G,L**3)%6
    return tensor,State(L,a,b,r)


def run_case(path, *, L=5, connected=True, memory_intervention=False, messages=True, steps=160, max_bits=128):
    path=Path(path);path.mkdir(parents=True,exist_ok=True)
    tensor,seed=prepare(L=L,connected=connected,memory_intervention=memory_intervention,messages=messages)
    engine=Engine(tensor);state=seed;hist=deque(maxlen=2);tracker=ReassemblyTracker()
    ref=[i for i,n in enumerate(NAMES) if n.startswith('ref.')]
    comm=[i for i,n in enumerate(NAMES) if n.startswith('comm.')]
    memory=[i for i,n in enumerate(NAMES) if n.startswith('memory.')]
    samples=[];returns=[];classes=Counter();initial_mass=sum(map(int,seed.b[comm].flat))
    message_hashes=[];stop_reason='requested_horizon';bounded=True
    for tick in range(steps+1):
        obs,signature=structural_snapshot(state,ref,tuple(hist));hist.append(signature)
        obs.update(update=tick,maximum_counter_bits=state.max_abs().bit_length())
        tracker.observe(obs);samples.append(obs)
        if obs['maximum_counter_bits'] > max_bits:
            stop_reason='counter_bit_limit';bounded=False
            break
        assert set(map(int,state.b[comm+memory].flat)) <= {0,1}
        assert set(map(int,state.b[ref].flat)) <= {0,1,2}
        assert sum(map(int,state.b[comm].flat)) == initial_mass
        for axis in AXES:
            for bank in ('X','Y'):
                p,n,_,r=(tensor.gear_index(f'{k}.{axis}.{bank}') for k in KINDS)
                assert np.array_equal(state.b[r],state.b[p]+state.b[n])
        message_hashes.append(hashlib.sha256(json.dumps(state.b[comm].tolist()).encode()).hexdigest())
        if tick and state.same_as(seed):returns.append(tick)
        if tick==steps:break
        after=engine.step(state)
        assert np.array_equal(after.b,map_fields(state.b,state.lattice,connected=connected))
        assert np.array_equal(after.r,state.r)
        log=engine.clicks(state,after,tick+1).select('official');classes.update(map(int,log.kind))
        state=after
    assert engine.rewind(state,tick).same_as(seed)
    report={'parameters':dict(L=L,connected=connected,memory_intervention=memory_intervention,messages=messages,steps=steps,max_bits=max_bits),
        'completed_updates':tick,'stop_reason':stop_reason,'tensor_fingerprint':tensor.fingerprint,
        'gears':tensor.G,'monomials':len(tensor.monomials),'strict_support_violations':len(tensor.support_violations()),
        'old_a_dependencies':False,'exact_rewind':True,'all_steps_match_first_order_specification':True,
        'bounded_Boolean_and_density_sector':bounded,'constant_total_message_occupancy':initial_mass,
        'remainders_retained':True,'click_classes':{f'C{k}':classes[k] for k in range(3)},
        'maximum_counter_bits':max(x['maximum_counter_bits'] for x in samples),
        'reference_reassemblies':tracker.events,'full_state_returns':returns,'message_hashes':message_hashes,
        'gates':{'recurrent_density_episodes':len(tracker.events)>=4,
                 'growing_structural_proxies':progressive_reassemblies(tracker.events),
                 'complete_information_recovery':True,'stagnation_trigger_demonstrated':False,
                 'independent_reference_board':False},
        'user_goal_demonstrated':False,'samples':samples}
    (path/'tensor.json').write_text(tensor.to_json()+'\n')
    for name,s in (('initial',seed),('final',state)):
        with gzip.open(path/(name+'.json.gz'),'wt') as stream:json.dump(s.to_dict(),stream)
    (path/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def main(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    # Exhaust all local Boolean collisions independently of the tensor.
    local_outputs=set()
    for p,n,m in product((0,1),repeat=3):
        pp,nn=p+m*(n-p),n+m*(p-n)
        mm=m+p+n-2*p*n-2*m*p-2*m*n+4*m*p*n
        local_outputs.add((pp,nn,mm))
        old=(pp+(1-mm)*(nn-pp),nn+(1-mm)*(pp-nn),
             mm+pp+nn-2*pp*nn-2*mm*pp-2*mm*nn+4*mm*pp*nn)
        assert old==(p,n,m)
    assert len(local_outputs)==8
    # Nonuniform invariant-sector checks beyond the concentrated fixtures.
    rng=np.random.default_rng(20261111)
    random_checks=0
    for L,connected in product((3,5),(False,True)):
        tensor,prototype=prepare(L=L,connected=connected)
        engine=Engine(tensor)
        for _ in range(2):
            b=rng.integers(0,2,size=prototype.b.shape).astype(object)
            for axis in AXES:
                for bank in ('X','Y'):
                    p,n,_,r=(tensor.gear_index(f'{k}.{axis}.{bank}') for k in KINDS)
                    b[r]=b[p]+b[n]
            a=map_fields(b,prototype.lattice,connected=connected,inverse=True)
            assert np.array_equal(map_fields(a,prototype.lattice,connected=connected),b)
            seed=State(L,a,b,prototype.r);state=seed
            for _ in range(8):
                after=engine.step(state)
                assert np.array_equal(after.b,map_fields(state.b,state.lattice,connected=connected))
                assert np.array_equal(after.r,state.r)
                state=after
            assert engine.rewind(state,8).same_as(seed)
            random_checks+=1
    cases={}
    for L,connected,perturbed in product((3,5),(False,True),(False,True)):
        name=f'L{L}_routing{int(connected)}_memory{int(perturbed)}'
        r=run_case(out/name,L=L,connected=connected,memory_intervention=perturbed)
        cases[name]=r
        print(name,len(r['reference_reassemblies']),r['full_state_returns'],flush=True)
    cases['quiet']=run_case(out/'quiet',messages=False)
    comparisons=[]
    for L,connected in product((3,5),(False,True)):
        a,b=(cases[f'L{L}_routing{int(connected)}_memory{k}'] for k in (0,1))
        different=[t for t,(x,y) in enumerate(zip(a['message_hashes'],b['message_hashes'])) if x!=y]
        density_changes=[t for t,(x,y) in enumerate(zip(a['samples'],b['samples']))
                         if x['normalized_fingerprint']!=y['normalized_fingerprint']]
        comparisons.append({'L':L,'routing_connected':connected,'first_message_change':min(different) if different else None,
            'first_retained_density_change':min(density_changes) if density_changes else None,
            'reassembly_times_base':[e['update'] for e in a['reference_reassemblies']],
            'reassembly_times_intervention':[e['update'] for e in b['reference_reassemblies']]})
    source=Path(__file__).read_bytes()
    result={'reviewed_main':'7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2','source_sha256':hashlib.sha256(source).hexdigest(),
        'local_Boolean_collision_truth_table_verified':8,
        'nonuniform_invariant_sector_checks':random_checks,
        'dependency_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in
            ('universe24/core/engine.py','universe24/core/tensor.py','universe24/core/lattice.py',
             'experiments/cosmology/recurrent_bursts.py','experiments/cosmology/PROTOCOL.md')},
        'declared_grid':'L in {3,5}; routing on/off; one-site initial memory intervention on/off; 160 updates; plus quiet control.',
        'interpretation':'New bounded toy with retained message-density record; not independent 48-channel reference dynamics, stagnation sensing or a complexity/Born law.',
        'cases':{k:{p:v for p,v in r.items() if p not in ('samples','message_hashes')} for k,r in cases.items()},
        'intervention_comparisons':comparisons}
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=Path('runs/complexity-research/03-reassembly'))
    main(parser.parse_args().out)
