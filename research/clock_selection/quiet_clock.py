"""Research-only initial Patch factory for exact passive-halo quarter-turn clocks.

No class or callback participates in runtime evolution. Prepare the frozen
validation with --prepare, obtain approval, then execute with --run.
"""
from __future__ import annotations
import argparse
from collections import Counter
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import time

from research.components import BoardSpec, Patch, TensorSpec, finalize, place, plain
from research.experiments.run import canonical, digest, recorded_states, run_experiment, source_hashes
from research.presenter.export import bundle
from research.presenter.build import build
from universe24.core.group_2o import DIRECTIONS
from universe24.core.state import Channel, State, channel as checked_channel
from universe24.observation.clicks import classify

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PROTOCOL=HERE/'quiet_clock_protocol.json'


def _int(value,label):
    if type(value) is not int:raise TypeError(label+' must be an exact integer')
    return value


def outgoing_recipients(tensor,source_channel):
    """Invert receiver input rows; do not identify incoming and outgoing ports."""
    if not isinstance(tensor,TensorSpec):raise TypeError('Expected the allowed fixed TensorSpec')
    _int(source_channel,'channel')
    if source_channel not in range(48):raise ValueError('Channel outside0..47')
    recipients=[]
    for d,delta in enumerate(DIRECTIONS):
        found=[h for h in range(48) if tensor.ports[d^1][h]==source_channel]
        if len(found)!=1:raise ValueError('Expected one outgoing recipient per spatial direction')
        h=found[0]
        recipients.append(((*delta,h),tensor.weights[d^1][h]))
    return tuple(recipients)


def QuietClock(*,channel=0,a=0,b=1,r=2,tensor=None,
               halo_remainders=None,halo_parity=None,background=(0,0,2)):
    """Return a complete336-triple initial Patch with an explicit isolated contract.

    a,b are the actual initial counters, not a runtime phase parameter.
    The center is nonzero and |a|+|b|<=2. Central r may be any0..5.
    Each supplied halo remainder must keep all signed cumulative prefixes in
    0..5. Otherwise choose the closest admissible value to background.r,
    optionally of halo_parity0/1, breaking ties upward. No input is injected.
    """
    for value,label in ((channel,'channel'),(a,'a'),(b,'b'),(r,'r')):_int(value,label)
    if channel not in range(48) or r not in range(6):raise ValueError('Invalid channel or central remainder')
    if not 0<abs(a)+abs(b)<=2:raise ValueError('A nonzero quiet clock requires0<|a|+|b|<=2')
    if halo_parity is not None and (type(halo_parity) is not int or halo_parity not in (0,1)):
        raise ValueError('Halo parity must be None,0 or1')
    tensor=TensorSpec() if tensor is None else tensor
    background=checked_channel(background)
    if background.a or background.b:raise ValueError('Background counters must be zero')
    outgoing=outgoing_recipients(tensor,channel)
    supplied=None if halo_remainders is None else tuple(halo_remainders)
    if supplied is not None and (len(supplied)!=6 or any(type(v) is not int for v in supplied)):
        raise ValueError('Six exact integer halo remainders are required')
    prefixes=(0,b,b-a,-a)
    cells={(*xyz,g):background for xyz in ((0,0,0),*DIRECTIONS) for g in range(48)}
    center=(0,0,0,channel);cells[center]=(a,b,r)
    requirements=[]
    for d,(address,weight) in enumerate(outgoing):
        signed=[weight*v for v in prefixes]
        lower,upper=-2*min(signed),5-2*max(signed)
        allowed=[v for v in range(lower,upper+1) if halo_parity is None or v%2==halo_parity]
        value=(min(allowed,key=lambda v:(abs(v-background.r),-v)) if supplied is None else supplied[d])
        if value not in allowed:raise ValueError('Halo remainder crosses a quotient threshold or requested parity')
        cells[address]=(0,0,value)
        requirements.append({'direction':d,'address':address,'weight':weight,
                             'remainder_interval':[lower,upper],'initial_remainder':value})
    contract={'format':'universe24-quiet-clock-contract-v1','prepared_only':True,
              'center':center,'counter_pair':[a,b],'center_remainder':r,
              'counter_L1':abs(a)+abs(b),'unit_counter_norm':a*a+b*b==1,
              'counter_period':4,'whole_isolated_state_period':4,'guarded_C_per_isolated_period':0,
              'protected_nodes':((0,0,0),*DIRECTIONS),'protected_triples':336,
              'outgoing_recipients':requirements,'tensor_fingerprint':tensor.fingerprint,
              'environment':'No additional input to any center/halo channel; every other counter remains zero. Shared active components need a new composition test.',
              'readout':'Complete center+halo quarter-turn state; phase is passive, never a runtime command.',
              'response_to_external_input':'Unspecified; isolated contract does not certify driven behavior.',
              'activation_by_signal_established':False}
    return Patch('quiet-clock',cells,tensor=tensor,background=background,
                 ports={'center':(center,),'center_node':tuple((0,0,0,g) for g in range(48)),
                        'outgoing_recipients':tuple(a for a,w in outgoing),'region':tuple(cells)},
                 sources={'clock':(center,)},evidence_domains=(contract,))


def planned(p):
    for si,signs in enumerate(p['signs_order']):
        for oi,(a,b) in enumerate(p['orbits']):
            for parity in p['parities']:
                yield {'id':f'quiet-s{si}-o{oi}-p{parity}','sign_index':si,'orbit_index':oi,
                       'signs':signs,'channel':p['representative_channels_by_sign_and_orbit'][si][oi],
                       'a':a,'b':b,'r':2+parity,'parity':parity,'side':5 if si%2==0 else 7}


def clock_for(case):
    return QuietClock(channel=case['channel'],a=case['a'],b=case['b'],r=case['r'],
                      halo_parity=case['parity'],tensor=TensorSpec.from_signs(case['signs']))


def spec_for(case,protocol_sha):
    patch=clock_for(case);c=case['side']//2
    return {'format':'universe24-assembly-experiment-v1','id':case['id'],
            'title':f"Prepared quiet clock {case['a']},{case['b']}; signs{case['signs']}; parity{case['parity']}",
            'description':'A full isolated counter/halo orbit. Initial preparation only; no signal activation is claimed.',
            'board':{'side':case['side'],'body_signs':case['signs'],'background':[0,0,2]},
            'components':[{'name':'clock','recipe':'Patch','at':[c,c,c],
                'params':{'kind':patch.kind,'cells':[[*a,*v] for a,v in patch.cells],
                          'ports':plain(patch.ports),'sources':plain(patch.sources),
                          'evidence_domains':plain(patch.evidence_domains)}}],
            'steps':8,'detectors':[],'seed':None,'controls':case,'view':{'port':'clock.center'},
            'provenance':{'protocol_sha256':protocol_sha,'initial_only':True},
            'budget':{'max_frames':9,'max_cells':10000,'max_bytes':2097152,'max_seconds':10}}


def file_sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(path,value):Path(path).write_text(canonical(value)+'\n')


def preflight(p):
    # Exact4x4 construction is independent of production group/coupling generation.
    from research.reference.algebra import coupling as matrix_coupling
    checks=[];orientations=[]
    for signs in p['signs_order']:
        tensor=TensorSpec.from_signs(signs);oracle=matrix_coupling(tuple(signs))
        for g in range(48):
            patch=QuietClock(channel=g,a=1,b=1,r=2+(g%2),halo_parity=g%2,tensor=tensor)
            actual=outgoing_recipients(tensor,g);expected=[]
            for d,delta in enumerate(DIRECTIONS):
                hs=[h for h in range(48) if oracle.ports[d^1][h]==g]
                assert len(hs)==1
                expected.append(((*delta,hs[0]),oracle.weights[d^1][hs[0]]))
            assert actual==tuple(expected) and len(patch.cells)==336
            cells=dict(patch.cells)
            for address,weight in expected:
                assert cells[address]==(0,0,2+(g%2))
            checks.append({'signs':signs,'channel':g,'outgoing':[[list(a),w] for a,w in actual]})
            # Compare all48 proper orientation placements to direct channel construction.
            base=QuietClock(channel=0,a=1,b=1,r=2+(g%2),halo_parity=g%2,tensor=tensor)
            board=BoardSpec(5,tensor=tensor)
            rotated=finalize(board,[place(base,at=(2,2,2),name='clock',orientation=g)])
            direct=finalize(board,[place(patch,at=(2,2,2),name='clock')])
            assert rotated.initial==direct.initial
            orientations.append({'signs':signs,'orientation':g,'complete_state_equal':True})
    return {'matrix_recipient_checks':checks,'orientation_checks':orientations,
            'matrix_recipient_cases':len(checks),'full_orientation_cases':len(orientations),
            'native_evolution_steps':0,'all_passed':True}


def prepare(output):
    output.mkdir(parents=True,exist_ok=False)
    start=time.process_time();p=json.loads(PROTOCOL.read_text());raw=PROTOCOL.read_bytes()
    specs=[spec_for(c,file_sha(PROTOCOL)) for c in planned(p)]
    receipt=preflight(p)
    write(output/'preflight.json',receipt);write(output/'specs.json',specs)
    (output/'protocol.json').write_bytes(raw);(output/'producer.py').write_bytes(Path(__file__).read_bytes())
    sources=source_hashes()
    for name in ('research/reference/algebra.py','research/reference/evolution.py'):
        sources[name]=file_sha(ROOT/name)
    for relative,expected in sources.items():
        dst=output/'source'/relative;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes((ROOT/relative).read_bytes())
        assert file_sha(dst)==expected
    registration={'protocol_sha256':file_sha(PROTOCOL),'producer_sha256':file_sha(__file__),
                  'specs_sha256':file_sha(output/'specs.json'),'source_sha256':sources,
                  'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                  'native_cases':len(specs),'native_steps':0,'preflight_cpu_seconds':time.process_time()-start}
    write(output/'registration.json',registration)
    print(canonical({k:v for k,v in registration.items() if k!='source_sha256'}))


def expected_state(initial,case,t):
    c=case['side']//2;g=case['channel'];a,b=case['a'],case['b'];phase=t%4
    aa,bb=((a,b),(b,-a),(-a,-b),(-b,a))[phase]
    cells=dict(initial.cells);center=(c,c,c,g);cells[center]=Channel(aa,bb,case['r'])
    prefix=(0,b,b-a,-a)[phase]
    for address,weight in outgoing_recipients(TensorSpec.from_signs(case['signs']),g):
        target=tuple(address[j]+c for j in range(3))+(address[3],)
        cells[target]=Channel(0,0,initial.at(target).r+2*weight*prefix)
    return State(initial.cube,initial.background,cells)


def analyze(case,experiment):
    states=recorded_states(experiment);initial=states[0];events=[];center=(*([case['side']//2]*3),case['channel'])
    for t,(old,new) in enumerate(zip(states,states[1:]),1):
        for address in sorted(old.cells.keys()|new.cells.keys()):
            event=classify(old.at(address),new.at(address))
            if event is not None:events.append({'step':t,'address':list(address),'kind':event[0],'ell':str(event[1])})
    checks={'full_analytic_state':all(s==expected_state(initial,case,t) for t,s in enumerate(states)),
            'minimal_period4':states[4]==initial and all(states[t]!=initial for t in (1,2,3)),
            'no_guarded_C':not events,
            'only_center_counters':all(not(v.a or v.b) or a==center for s in states for a,v in s.cells.items()),
            'full_inverse':experiment['provenance']['full_rewind_equal'],
            'no_nonbackground_boundary_contact':all(all(0<v<case['side']-1 for v in a[:3]) for s in states for a in s.cells)}
    return {'case':case,'checks':checks,'all_checks':all(checks.values()),'all_world_C':events,
            'center_trace':[list(s.at(center)) for s in states]}


def run(output):
    reg=json.loads((output/'registration.json').read_text());p=json.loads((output/'protocol.json').read_text())
    assert file_sha(__file__)==reg['producer_sha256'] and file_sha(PROTOCOL)==reg['protocol_sha256']
    assert file_sha(output/'specs.json')==reg['specs_sha256']
    assert all(file_sha(ROOT/name)==sha for name,sha in reg['source_sha256'].items())
    if (output/'run_started.json').exists():raise FileExistsError('Registered run already started')
    write(output/'run_started.json',{'registered_before_capture':True})
    (output/'records').mkdir();cpu,wall=time.process_time(),time.monotonic();rows=[];selected=[];pairs={};errors=[]
    try:
        for spec in json.loads((output/'specs.json').read_text()):
            if time.process_time()-cpu+reg['preflight_cpu_seconds']>60:raise TimeoutError('CPU budget')
            if time.monotonic()-wall>180:raise TimeoutError('Wall budget')
            result=run_experiment(spec);case=spec['controls'];report=analyze(case,result['experiment'])
            record={'case':case,'spec':spec,'assembly':result['assembly'],'experiment':result['experiment'],'analysis':report}
            data=gzip.compress((canonical(record)+'\n').encode(),mtime=0);path='records/'+case['id']+'.json.gz';(output/path).write_bytes(data)
            rows.append({'id':case['id'],'record':path,'record_sha256':hashlib.sha256(data).hexdigest(),**report})
            pairs[(case['sign_index'],case['orbit_index'],case['parity'])]=recorded_states(result['experiment'])
            if case['id'] in p['presenter_ids']:selected.append(result['experiment'])
            if sum(f.stat().st_size for f in output.rglob('*') if f.is_file())>16777216:raise MemoryError('Output budget')
        write(output/'presenter_experiments.json',bundle(selected,title='Prepared quiet clock building blocks'))
        build(output/'presenter_experiments.json',output/'The_Presenter.html')
    except Exception as exc:errors.append({'type':type(exc).__name__,'message':str(exc)})
    parity=[]
    for si,oi in itertools.product(range(8),range(3)):
        if (si,oi,0) not in pairs or (si,oi,1) not in pairs:continue
        equal=True;residue=True
        for s0,s1 in zip(pairs[si,oi,0],pairs[si,oi,1]):
            addresses=s0.cells.keys()|s1.cells.keys()
            equal &= all(s0.at(a)[:2]==s1.at(a)[:2] for a in addresses)
            changed=[s1.at(a).r-s0.at(a).r for a in addresses if s1.at(a).r!=s0.at(a).r]
            residue &= len(changed)==7 and set(changed)=={1}
        parity.append({'sign_index':si,'orbit_index':oi,'same_counter_trace':equal,'seven_remainders_offset1':residue})
    sources_ok=all(file_sha(ROOT/name)==sha for name,sha in reg['source_sha256'].items()) and file_sha(__file__)==reg['producer_sha256']
    result={'status':'completed' if len(rows)==48 and not errors else 'inconclusive','completed_cases':len(rows),'registered_cases':48,
            'cases':rows,'all_case_checks':len(rows)==48 and all(r['all_checks'] for r in rows),
            'parity_comparisons':parity,'all_parity_checks':len(parity)==24 and all(r['same_counter_trace'] and r['seven_remainders_offset1'] for r in parity),
            'errors':errors,'source_unchanged':sources_ok,'cpu_seconds':time.process_time()-cpu,
            'preflight_cpu_seconds':reg['preflight_cpu_seconds'],'wall_seconds':time.monotonic()-wall,'claim_limits':p['claim_limits']}
    write(output/'result.json',result);print(canonical({k:v for k,v in result.items() if k not in ('cases','parity_comparisons','claim_limits')}))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);action=parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--prepare',action='store_true');action.add_argument('--run',action='store_true')
    parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    (prepare if args.prepare else run)(args.output)
