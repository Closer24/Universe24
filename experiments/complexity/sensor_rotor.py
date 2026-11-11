"""Boolean no-change sensor coupled to a reversible retained-memory rotor.

Declared integration experiment; no physical cosmology or complexity claim.
"""
import argparse
from collections import Counter, deque
import gzip
import hashlib
from itertools import product
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from universe24.core import Engine, State, Tensor
from experiments.complexity import local_stagnation as sensor
from experiments.complexity import reassembly_feedback as rotor
from experiments.cosmology.recurrent_bursts import structural_snapshot, ReassemblyTracker, progressive_reassemblies

OFFSET = len(sensor.NAMES)
NAMES = sensor.NAMES + rotor.NAMES


def build(*, connected=True):
    # The former scalar message wire is retained but undriven and remains zero.
    data = sensor.build(connected=False).to_dict()
    other = rotor.build(connected=True).to_dict()
    data['gears'].extend(other['gears'])
    data['monomials'].extend(other['monomials'])
    data['designated_one_way'].extend(other.get('designated_one_way', []))
    if connected:
        for axis in rotor.AXES:
            for target_bank, source_bank, field, sign in (
                    ('X', 'Y', 'b', 1), ('Y', 'X', 'a', -1)):
                p = f'comm.plus.{axis}.{source_bank}'
                n = f'comm.minus.{axis}.{source_bank}'
                m = f'memory.{axis}.{source_bank}'
                for kind, outsign in (('comm.plus', 1), ('comm.minus', -1)):
                    target = f'{kind}.{axis}.{target_bank}'
                    for coefficient, extras in ((3, (n,)), (-3, (p,)), (-6, (m,n)), (6, (m,p))):
                        factors = [['sensor.alarm', [0,0,0], field]] + [[g,[0,0,0],'b'] for g in extras]
                        data['monomials'].append([target, sign*outsign*coefficient, factors])
                        data['designated_one_way'].append([target, factors,
                            'Declared Boolean alarm controls a reversible local rotor; sensor receives no feedback.'])
    return Tensor.from_dict(data, strict_support=True)


def map_rotor(values, lattice, alarm, *, inverse=False, connected=True):
    """Independent Boolean specification using explicit conditional swaps/XOR."""
    result = np.empty_like(values)
    def g(kind, axis, bank):
        return rotor.NAMES.index(f'{kind}.{axis}.{bank}')
    for axis_id, axis in enumerate(rotor.AXES):
        source, target = ('X','Y') if inverse else ('Y','X')
        p,n,m,density = (values[g(k,axis,source)] for k in rotor.KINDS)
        h = np.logical_xor(m.astype(bool), alarm.astype(bool)) if connected else m.astype(bool)
        selector = np.logical_not(h) if inverse else h
        pp, nn = np.where(selector, n, p), np.where(selector, p, n)
        mm = np.logical_xor(m.astype(bool), np.logical_xor(p.astype(bool),n.astype(bool))).astype(int)
        for kind, value in zip(rotor.KINDS, (pp,nn,mm,density)):
            result[g(kind,axis,target)] = value
        source, target = ('Y','X') if inverse else ('X','Y')
        p,n,m,density = (values[g(k,axis,source)] for k in rotor.KINDS)
        e = tuple(int(k==axis_id)*(1 if inverse else -1) for k in range(3))
        pp = p[lattice.shift_index(e)]
        nn = n[lattice.shift_index(tuple(-v for v in e))]
        for kind,value in zip(rotor.KINDS,(pp,nn,m,density+pp+nn-p-n)):
            result[g(kind,axis,target)] = value
    return result


def prepare(*, L, stagnant, connected, memory_intervention):
    tensor = build(connected=connected)
    source = sensor.prepare(sensor.build(connected=False), L=L, stagnant=stagnant)
    _, spinning = rotor.prepare(L=L, connected=True, memory_intervention=memory_intervention)
    # Fixed geometry chosen before running: packet center is one edge left of
    # the marked sensor, so it encounters a singly occupied link, not only a
    # simultaneous p=n focus. Shift the prepared memory intervention with it.
    spinning.b = spinning.b[:, spinning.lattice.shift_index((1,0,0))].copy()
    alarm = source.a[sensor.NAMES.index('sensor.alarm')]
    spinning.a = map_rotor(spinning.b, spinning.lattice, alarm, inverse=True, connected=connected)
    seed = State(L, *[np.concatenate([getattr(source,f),getattr(spinning,f)]) for f in ('a','b','r')])
    return tensor, seed


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def domain(state, tensor, *, connected):
    source = State(state.L, *(getattr(state,f)[:OFFSET].copy() for f in ('a','b','r')))
    source_info = sensor.observe(source, sensor.build(connected=False), 0)
    assert source_info['Boolean_source_alarm_invariant']
    assert not np.any(source.b[-1]) and not np.any(source.a[-1])
    fields = state.b[OFFSET:]
    for axis in rotor.AXES:
        for bank in ('X','Y'):
            ids = [rotor.NAMES.index(f'{kind}.{axis}.{bank}') for kind in rotor.KINDS]
            p,n,m,r = fields[ids]
            assert all(np.all((v==0)|(v==1)) for v in (p,n,m))
            assert np.array_equal(r,p+n)
    previous_alarm = state.a[tensor.gear_index('sensor.alarm')]
    assert np.array_equal(state.a[OFFSET:], map_rotor(fields,state.lattice,previous_alarm,
                                                    inverse=True,connected=connected))
    return source_info


def execute(path, *, L, stagnant, connected, memory_intervention, steps=80):
    path.mkdir(parents=True,exist_ok=True)
    tensor, seed = prepare(L=L,stagnant=stagnant,connected=connected,memory_intervention=memory_intervention)
    (path/'tensor.json').write_text(tensor.to_json()+'\n')
    (path/'seed.json').write_text(json.dumps(seed.to_dict())+'\n')
    state = seed
    engine = Engine(tensor)
    refs = [i for i,n in enumerate(NAMES) if n.startswith('ref.density.')]
    comm = [i for i,n in enumerate(NAMES) if n.startswith('comm.')]
    history, tracker, frames, classes, returns = deque(maxlen=2), ReassemblyTracker(), [], Counter(), []
    center = seed.lattice.index(*(L//2,)*3)
    initial_mass = int(sum(seed.b[comm].flat))
    with gzip.open(path/'full_trace.jsonl.gz','wt') as trace:
        for tick in range(steps+1):
            trace.write(json.dumps({'microtick':tick,'state':state.to_dict()})+'\n')
            source_info = domain(state,tensor,connected=connected)
            obs, signature = structural_snapshot(state,refs,tuple(history))
            history.append(signature)
            obs.update(update=tick)
            tracker.observe(obs)
            assert int(sum(state.b[comm].flat)) == initial_mass
            assert np.array_equal(state.r,seed.r)
            obs.update(alarm=int(state.b[tensor.gear_index('sensor.alarm'),center]),
                source_l1=source_info['source_amplitude_l1'],
                control_l1=source_info['control_amplitude_l1'],
                source_sha256=digest([getattr(state,f)[:OFFSET].tolist() for f in ('a','b','r')]),
                rotor_sha256=digest([getattr(state,f)[OFFSET:].tolist() for f in ('a','b','r')]),
                message_sha256=digest(state.b[comm].tolist()),
                maximum_bits=max(state.max_abs().bit_length(), int(state.r.max()).bit_length()))
            frames.append(obs)
            if tick and state.same_as(seed): returns.append(tick)
            assert obs['maximum_bits'] <= 128
            if tick == steps: break
            after = engine.step(state)
            expected = map_rotor(state.b[OFFSET:],state.lattice,
                state.b[tensor.gear_index('sensor.alarm')],connected=connected)
            assert np.array_equal(after.b[OFFSET:],expected)
            assert engine.inverse_step(after).same_as(state)
            classes.update(map(int,engine.clicks(state,after,tick+1).kind))
            state = after
    assert engine.rewind(state,steps).same_as(seed)
    (path/'final.json').write_text(json.dumps(state.to_dict())+'\n')
    result = {'parameters':dict(L=L,stagnant=stagnant,connected=connected,
                memory_intervention=memory_intervention,steps=steps),
        'gears':tensor.G,'terms':len(tensor),'degree':tensor.rank-1,
        'support_violations':len(tensor.support_violations()),
        'old_a_graph_accepted':True,'tensor_fingerprint':tensor.fingerprint,
        'exact_rewind':True,'prepared_domain_verified_every_step':True,
        'every_rotor_step_matches_independent_Boolean_map':True,
        'message_occupancy':initial_mass,'click_classes':{str(k):classes[k] for k in range(3)},
        'maxbits':max(f['maximum_bits'] for f in frames),'full_state_returns':returns,
        'density_reassemblies':tracker.events,'growing_structural_proxies':progressive_reassemblies(tracker.events),
        'independent_reference_board':False,'full_goal_demonstrated':False,
        'frames':frames,'seed_sha256':digest(seed.to_dict()),'final_sha256':digest(state.to_dict()),
        'trace_sha256':hashlib.sha256((path/'full_trace.jsonl.gz').read_bytes()).hexdigest()}
    (path/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=ROOT/'runs/complexity-research/07-sensor-rotor')
    args=parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    grid=list(product((3,5),(True,False),(True,False),(False,True)))
    protocol={'baseline':'7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2',
        'declared_before_execution':True,'grid_keys':['L','stagnant','connected','memory_intervention'],
        'grid':grid,'updates':80,'maxbits':128,
        'fixed_geometry':'Sensor at cube center; rotor packet origin shifted one negative-x edge. Optional memory intervention at sensor node.',
        'claim':'Equal-amplitude local input history affects retained alarm and Boolean scattering under matched disconnection. No structural-stagnation/cosmology/Born claim.'}
    (args.out/'protocol.json').write_text(json.dumps(protocol,indent=2)+'\n')
    truth=[]
    for p,n,m,s in product((0,1),repeat=4):
        h=m+s-2*m*s
        pp,nn=p+h*(n-p),n+h*(p-n)
        mm=m+p+n-2*p*n-2*m*p-2*m*n+4*m*p*n
        hh=mm+s-2*mm*s
        old=(pp+(1-hh)*(nn-pp),nn+(1-hh)*(pp-nn),
             mm+pp+nn-2*pp*nn-2*mm*pp-2*mm*nn+4*mm*pp*nn)
        assert old==(p,n,m)
        truth.append([p,n,m,s,pp,nn,mm])
    cases={}
    for L,stagnant,connected,intervention in grid:
        label=f'L{L}-static{int(stagnant)}-connected{int(connected)}-memory{int(intervention)}'
        cases[label]=execute(args.out/label,L=L,stagnant=stagnant,connected=connected,memory_intervention=intervention)
    comparisons=[]
    cone_checks=0
    for L,connected,intervention in product((3,5),(True,False),(False,True)):
        a,b=(cases[f'L{L}-static{s}-connected{int(connected)}-memory{int(intervention)}'] for s in (1,0))
        different=[i for i,(x,y) in enumerate(zip(a['frames'],b['frames'])) if x['message_sha256']!=y['message_sha256']]
        density=[i for i,(x,y) in enumerate(zip(a['frames'],b['frames'])) if x['normalized_fingerprint']!=y['normalized_fingerprint']]
        assert all(x['source_l1']==y['source_l1'] and x['control_l1']==y['control_l1'] for x,y in zip(a['frames'],b['frames']))
        if not connected: assert not different and not density
        names=[f'L{L}-static{s}-connected{int(connected)}-memory{int(intervention)}' for s in (1,0)]
        with gzip.open(args.out/names[0]/'full_trace.jsonl.gz','rt') as first, gzip.open(args.out/names[1]/'full_trace.jsonl.gz','rt') as second:
            center=np.array((L//2,)*3)
            for tick,(left,right) in enumerate(zip(first,second)):
                sa,sb=(State.from_dict(json.loads(line)['state']) for line in (left,right))
                changed=np.any((sa.a!=sb.a)|(sa.b!=sb.b)|(sa.r!=sb.r),axis=0)
                for node in np.flatnonzero(changed):
                    delta=np.abs(np.array(sa.lattice.coords(int(node)))-center)
                    assert int(np.minimum(delta,L-delta).sum()) <= tick
                cone_checks+=1
        comparisons.append({'L':L,'connected':connected,'memory_intervention':intervention,
            'first_message_difference':min(different) if different else None,
            'first_density_difference':min(density) if density else None,
            'static_reassemblies':[x['update'] for x in a['density_reassemblies']],
            'alternating_reassemblies':[x['update'] for x in b['density_reassemblies']]})
    for L,stagnant,intervention in product((3,5),(True,False),(False,True)):
        a,b=(cases[f'L{L}-static{int(stagnant)}-connected{c}-memory{int(intervention)}'] for c in (1,0))
        assert all(x['source_sha256']==y['source_sha256'] for x,y in zip(a['frames'],b['frames']))
    memory_comparisons=[]
    for L,stagnant,connected in product((3,5),(True,False),(True,False)):
        a,b=(cases[f'L{L}-static{int(stagnant)}-connected{int(connected)}-memory{m}'] for m in (0,1))
        assert all(x['source_sha256']==y['source_sha256'] for x,y in zip(a['frames'],b['frames']))
        changes=[i for i,(x,y) in enumerate(zip(a['frames'],b['frames'])) if x['message_sha256']!=y['message_sha256']]
        memory_comparisons.append({'L':L,'stagnant':stagnant,'connected':connected,
            'first_message_difference':min(changes) if changes else None,
            'base_episodes':[x['update'] for x in a['density_reassemblies']],
            'memory_intervention_episodes':[x['update'] for x in b['density_reassemblies']]})
    files=['experiments/complexity/sensor_rotor.py','experiments/complexity/local_stagnation.py',
        'experiments/complexity/reassembly_feedback.py','experiments/cosmology/recurrent_bursts.py',
        'universe24/core/engine.py','universe24/core/tensor.py']
    result={'protocol':protocol,'local_Boolean_inverse_cases':truth,'cases':cases,
        'source_history_comparisons':comparisons,'source_independent_of_rotor_connection':True,
        'memory_intervention_comparisons':memory_comparisons,
        'complete_state_cone_comparisons':cone_checks,
        'all_exact_rewinds':True,'original_goal_demonstrated':False,
        'source_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in files}}
    (args.out/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'cases':len(cases),'comparisons':comparisons,'all_rewinds':True},indent=2))


if __name__=='__main__':main()
