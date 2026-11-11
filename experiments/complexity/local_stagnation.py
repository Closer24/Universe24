"""Local Boolean no-change sensor and causal alarm transport at fixed six.

A deliberately restricted prototype, not a structural-complexity oracle.
python -m experiments.complexity.local_stagnation --out runs/complexity-research/01-stagnation
"""
import argparse
import hashlib
from itertools import product
import json
from pathlib import Path

import numpy as np
from universe24.core import Engine, State, Tensor

NAMES=('source.c','source.d','source.x','source.y','source.marker','sensor.alarm','message.x')
ROOT=Path(__file__).resolve().parents[2]
BASELINE='7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2'


def build(*, connected=True):
    """Fixed degree<=3 single-edge tensor; complete old-snapshot factors only."""
    terms=[]
    def f(name,field='b',offset=(0,0,0)):
        return (name,offset,field)
    def add(target,coefficient,*factors):
        terms.append((target,coefficient,factors,{'designated_one_way':
            'Declared local Boolean no-change sensor and one-way alarm; no reciprocal energy claim.'}))
    for name in ('source.c','source.d','source.marker'):
        add(name,6,f(name))
    for name,other in (('source.x','source.y'),('source.y','source.x')):
        add(name,6,f(name))
        add(name,6,f('source.c'),f(other))
        add(name,-6,f('source.c'),f(name))
    # S=1-a_x-b_x+2*a_x*b_x equals [a_x=b_x] on {0,1} only.
    add('sensor.alarm',3,f('source.marker'))
    add('sensor.alarm',-3,f('source.marker'),f('source.x','a'))
    add('sensor.alarm',-3,f('source.marker'),f('source.x'))
    add('sensor.alarm',6,f('source.marker'),f('source.x','a'),f('source.x'))
    for dx in (-1,1):
        add('message.x',3,f('message.x',offset=(dx,0,0)))
    if connected:
        add('message.x',3,f('sensor.alarm'))
    return Tensor(NAMES,terms,strict_support=True)


def prepare(tensor=None, *, L=5, stagnant=True, payload=1, marker=True, residue=2):
    """One-hot current/previous source fields; no future trajectory injected.

    All unmarked nodes alternate. Only the central site's swap control is
    changed in the stagnation intervention; c+d and x+y remain one everywhere.
    """
    if L not in (3,5) or payload not in (0,1) or residue not in range(6):
        raise ValueError('L=3/5, Boolean payload, residue in 0..5 required')
    tensor=build() if tensor is None else tensor
    if tuple(tensor.names)!=NAMES:raise ValueError('unexpected tensor channels')
    a,b,r=(np.zeros((tensor.G,L**3),dtype=object) for _ in range(3))
    state=State(L,a,b,r); node=state.lattice.index(*(L//2,)*3)
    ids={name:tensor.gear_index(name) for name in NAMES}
    state.b[ids['source.c']]=1
    state.b[ids['source.c'],node]=0 if stagnant else 1
    state.b[ids['source.d']]=1-state.b[ids['source.c']]
    state.b[ids['source.x']]=payload
    state.b[ids['source.y']]=1-payload
    state.b[ids['source.marker'],node]=int(marker)
    state.a[:]=state.b
    c=state.b[ids['source.c']]
    x,y=state.b[ids['source.x']],state.b[ids['source.y']]
    state.a[ids['source.x']]=x+c*(y-x)
    state.a[ids['source.y']]=y+c*(x-y)
    state.r[:]=residue
    return state


def state_hash(state):
    return hashlib.sha256(json.dumps(state.to_dict(),sort_keys=True,separators=(',',':')).encode()).hexdigest()


def no_change(state,tensor):
    """Passive raw polynomial; caller must check its Boolean domain."""
    g=tensor.gear_index('source.x'); a,b=state.a[g],state.b[g]
    return 1-a-b+2*a*b


def observe(state,tensor,tick):
    ids={name:tensor.gear_index(name) for name in NAMES}
    c,d,x,y,m,alarm=(state.b[ids[name]] for name in NAMES[:6])
    ax,ay=state.a[ids['source.x']],state.a[ids['source.y']]
    bounded=all(np.all((v==0)|(v==1)) for v in (c,d,x,y,m,ax,ay,alarm,state.a[ids['sensor.alarm']]))
    invariant=bounded and np.all(c+d==1) and np.all(x+y==1) and np.all(ax+ay==1)
    invariant=bool(invariant and np.array_equal(ax,x+c*(y-x)) and np.array_equal(ay,y+c*(x-y))
        and all(np.array_equal(state.a[ids[name]],state.b[ids[name]])
                for name in ('source.c','source.d','source.marker')))
    center=state.lattice.index(*(state.L//2,)*3)
    msg=state.b[ids['message.x']]
    maxbits=max(abs(int(v)).bit_length() for array in (state.a,state.b,state.r) for v in array.flat)
    return {'microtick':tick,'state_sha256':state_hash(state),'Boolean_source_alarm_invariant':invariant,
        'source_amplitude_l1':int(np.sum(abs(x)+abs(y))),
        'control_amplitude_l1':int(np.sum(abs(c)+abs(d))),
        'center_source_current':[int(x[center]),int(y[center])],
        'center_source_previous':[int(ax[center]),int(ay[center])],
        'center_no_change':int(no_change(state,tensor)[center]),'center_alarm':int(alarm[center]),
        'message_b_nonzero':{str(i):int(msg[i]) for i in np.flatnonzero(msg)},
        'maximum_integer_bits':maxbits}


def execute(tensor,seed,*,steps,maxbits,out):
    out.mkdir(parents=True,exist_ok=True)
    (out/'tensor.json').write_text(json.dumps(tensor.to_dict(),indent=2)+'\n')
    (out/'seed.json').write_text(json.dumps(seed.to_dict())+'\n')
    engine,state=Engine(tensor),seed
    frames=[]; counts={0:0,1:0,2:0}; stop=None
    with (out/'full_trace.jsonl').open('w') as trace:
        for tick in range(steps+1):
            trace.write(json.dumps({'microtick':tick,'state':state.to_dict()})+'\n')
            frame=observe(state,tensor,tick);frames.append(frame)
            assert frame['Boolean_source_alarm_invariant']
            assert np.array_equal(state.r,seed.r)
            if frame['maximum_integer_bits']>maxbits:
                stop='full-step bit budget';break
            if tick==steps:break
            after=engine.step(state)
            assert engine.inverse_step(after).same_as(state)
            clicks=engine.clicks(state,after,tick+1)
            for kind in counts:counts[kind]+=int(np.count_nonzero(clicks.kind==kind))
            state=after
    assert engine.rewind(state,len(frames)-1).same_as(seed)
    return {'tensor_fingerprint':tensor.fingerprint,'initial_sha256':state_hash(seed),
        'final_sha256':state_hash(state),'completed_steps':len(frames)-1,'resource_stop':stop,
        'full_rewind_exact':True,'all_remainders_retained':True,'click_classes':counts,'frames':frames}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=Path('runs/complexity-research/01-stagnation'))
    parser.add_argument('--steps',type=int,default=40)
    parser.add_argument('--L',type=int,choices=(3,5),default=5)
    parser.add_argument('--maxbits',type=int,choices=(128,256),default=128)
    args=parser.parse_args(argv)
    if not 1<=args.steps<=160:raise ValueError('bounded protocol: 1..160 steps')
    args.out.mkdir(parents=True,exist_ok=True)
    declared=[('stagnant',True,1,True,True),('changing',False,1,True,True),
        ('stagnant_label_swap',True,0,True,True),('disconnected',True,1,True,False),
        ('unmarked',True,1,False,True)]
    protocol={'baseline':BASELINE,'declared_before_execution':True,'L':args.L,'steps':args.steps,
        'maxbits_checked_after_complete_step':args.maxbits,'cases':declared,
        'claim':'Local one-update equality sensor on a proved Boolean invariant sector; not arbitrary integer zero-test or structural-complexity stagnation.',
        'required_controls':['same source/control L1 amplitudes at each tick','local novelty intervention',
            'disconnected alarm-to-message law','unmarked detector','label-swapped stagnant payload','full rewind'],
        'ineligible_success_claims':['Born rule','Bell violation','growing structural complexity','recurrent cosmological bursts']}
    (args.out/'protocol.json').write_text(json.dumps(protocol,indent=2)+'\n')
    cases={}
    for label,stagnant,payload,marker,connected in declared:
        tensor=build(connected=connected)
        assert tensor.rank<=4 and not tensor.support_violations()
        seed=prepare(tensor,L=args.L,stagnant=stagnant,payload=payload,marker=marker)
        cases[label]=execute(tensor,seed,steps=args.steps,maxbits=args.maxbits,out=args.out/label)
    normal,novel=cases['stagnant']['frames'],cases['changing']['frames']
    matched_horizon=min(c['completed_steps'] for c in cases.values())
    assert all(a['source_amplitude_l1']==b['source_amplitude_l1'] and
        a['control_amplitude_l1']==b['control_amplitude_l1'] for a,b in zip(normal,novel))
    assert all(f['center_no_change']==1 for f in normal)
    assert all(f['center_no_change']==0 for f in novel)
    assert all(not f['message_b_nonzero'] for f in novel)
    for control in ('disconnected','unmarked'):
        assert all(not f['message_b_nonzero'] for f in cases[control]['frames'])
    matched=lambda rows:rows[:matched_horizon+1]
    assert [f['center_alarm'] for f in matched(normal)]==[f['center_alarm'] for f in matched(cases['disconnected']['frames'])]
    assert [f['message_b_nonzero'] for f in matched(normal)]==[f['message_b_nonzero'] for f in matched(cases['stagnant_label_swap']['frames'])]
    # Compare complete states, not only plotted messages; changed initial support is one node.
    traces={label:[State.from_dict(json.loads(line)['state']) for line in
        (args.out/label/'full_trace.jsonl').read_text().splitlines()] for label in ('stagnant','changing')}
    center=np.array((args.L//2,)*3)
    for tick,(a,b) in enumerate(zip(traces['stagnant'],traces['changing'])):
        changed=np.any((a.a!=b.a)|(a.b!=b.b)|(a.r!=b.r),axis=0)
        for node in np.flatnonzero(changed):
            delta=np.abs(np.array(a.lattice.coords(int(node)))-center)
            assert int(np.minimum(delta,args.L-delta).sum())<=tick
    first_by_node={}
    for frame in normal:
        for node in frame['message_b_nonzero']:first_by_node.setdefault(node,frame['microtick'])
    local_truth=[]
    for a,b in product((0,1),repeat=2):
        s=1-a-b+2*a*b;assert s==int(a==b);local_truth.append([a,b,s])
    # The polynomial is deliberately NOT a total zero-test outside its domain.
    outside=[{'a':a,'b':b,'polynomial':1-a-b+2*a*b,'actual_equal':a==b}
        for a,b in ((2,2),(2,1),(-1,-1))]
    for c,x,m,r in product((0,1),(0,1),(0,1),range(6)):
        tensor=build();seed=prepare(tensor,L=3,stagnant=not c,payload=x,marker=bool(m),residue=r)
        e,state=Engine(tensor),seed
        for t in range(12):
            state=e.step(state);assert observe(state,tensor,t+1)['Boolean_source_alarm_invariant']
        assert e.rewind(state,12).same_as(seed)
    report={'protocol':protocol,'tensor':{'channels':len(NAMES),'degree':build().rank-1,
        'single_edge_violations':len(build().support_violations()),'old_a_reads_only_source_x':True},
        'truth_table':local_truth,'outside_Boolean_domain':outside,'invariant_control_cases':48,
        'invariant_control_updates_each':12,'local_intervention_complete_state_cone_passed':True,
        'message_first_arrivals':first_by_node,'cases':cases,'matched_control_horizon':matched_horizon,
        'positive_result':'Local unchanged-vs-alternating input, at equal amplitude and time, controls a retained alarm and causally propagated messages.',
        'negative_result':'Period-two source has no growing structure but remains classified as changing. This is not a structural-complexity stagnation detector. Message growth does not certify structure.',
        'source_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in (
            'experiments/complexity/local_stagnation.py','universe24/core/engine.py',
            'universe24/core/tensor.py','universe24/core/lattice.py')}}
    (args.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'cases':len(cases),'steps':args.steps,'all_rewinds':all(c['full_rewind_exact'] for c in cases.values()),
        'first_message_arrivals':first_by_node,'invariant_controls':48,'classes':cases['stagnant']['click_classes']},indent=2))

if __name__=='__main__':main()
