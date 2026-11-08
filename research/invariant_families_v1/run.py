"""Native verification of independently encoded invariant families; no model changes."""
from __future__ import annotations
import argparse
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import signal
import subprocess
import time
from universe24 import Coupling, Cube, State, Channel, Engine
from universe24.observation.clicks import clicks
from research.reference.algebra import algebra as reference_algebra, coupling as reference_coupling, DIRECTIONS
from research.presenter.export import capture, bundle
from research.experiments.run import recorded_states

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];PROTOCOL=HERE/'protocol.json'
CP=Coupling((1,1,1));ENGINE=Engine(CP)
class BudgetStop(RuntimeError):pass

def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'))
def write_json(path,value):
    path=Path(path)
    if path.exists():raise FileExistsError(path)
    temporary=path.with_name(path.name+'.partial');temporary.write_text(canonical(value)+'\n');temporary.replace(path)
def write_compressed(path,value):
    path=Path(path)
    if path.exists():raise FileExistsError(path)
    temporary=path.with_name(path.name+'.partial');temporary.write_bytes(gzip.compress(canonical(value).encode(),mtime=0));temporary.replace(path)
def J(value):
    a,b,r=value;return (-a,-b,4-r+2*(r%2))
def encode(value,sign):return tuple(value) if sign==1 else J(value) if sign==-1 else (0,0,2)
def addresses(side):return [(*xyz,g) for xyz in itertools.product(range(side),repeat=3) for g in range(48)]
def pattern(case,p):return next(item for item in p['family']['patterns'] if item['id']==case['pattern'])
def value_at(address,item):
    if item['id']=='uniform':return 1
    if 'x_period' in item:return item['x_period'][address[0]%len(item['x_period'])]
    return item['channel_vector'][address[3]]
def cases(p):
    for item,r,(a,b) in itertools.product(p['family']['patterns'],p['family']['remainders'],p['family']['counter_seeds']):
        yield {'id':f'{item["id"]}-L{item["side"]}-r{r}-a{a}-b{b}','pattern':item['id'],'side':item['side'],'lambda':item['lambda'],'a':a,'b':b,'r':r,'steps':p['family']['steps']}
def scalar_trace(case):
    result=[(case['a'],case['b'],case['r'])]
    for _ in range(case['steps']):
        a,b,r=result[-1];ell,rem=divmod(2*case['lambda']*b+r,6);result.append((b,ell-a,rem))
    return result
def initial(case,p):
    item=pattern(case,p);value=(case['a'],case['b'],case['r'])
    return State(Cube(case['side']),cells={address:Channel(*encode(value,value_at(address,item))) for address in addresses(case['side'])})
def donor(address,d,side,ports):
    return (*tuple((address[j]+DIRECTIONS[d][j])%side for j in range(3)),ports[d][address[3]])

def preflight(p):
    reference=reference_coupling((1,1,1));rotations=reference_algebra().rotations
    assert CP.fingerprint==p['baseline']['tensor_fingerprint']
    assert CP.ports==reference.ports and CP.weights==reference.weights
    internal=next(item for item in p['family']['patterns'] if item['id']=='internal_yy')
    vector=[rotation[1][1] for rotation in rotations];assert vector==internal['channel_vector']
    assert (vector.count(1),vector.count(-1),vector.count(0))==(8,8,32)
    eigenchecks=[]
    for item in p['family']['patterns']:
        aa=addresses(item['side']);hist={str(v):sum(value_at(a,item)==v for a in aa) for v in (-1,0,1)}
        for address in aa:
            actual=sum(reference.weights[d][address[3]]*value_at(donor(address,d,item['side'],reference.ports),item) for d in range(6))
            assert actual==item['lambda']*value_at(address,item)
        eigenchecks.append({'pattern':item['id'],'addresses_checked':len(aa),'lambda':item['lambda'],'ternary_counts':hist,'independent_operator_eigenidentity':True})
    registered=[]
    for case in cases(p):
        trace=scalar_trace(case)
        for old,new in zip(trace,trace[1:]):
            for sign in (-1,0,1):
                a,b,r=encode(old,sign);u=case['lambda']*old[1]*sign;ell,rem=divmod(2*u+r,6)
                assert (b,ell-a,rem)==encode(new,sign)
        registered.append({'case':case,'scalar_oracle_states':[list(row) for row in trace]})
    for r in range(6):
        for u in range(-8,9):
            ell,rem=divmod(2*u+r,6);other,new_rem=divmod(-2*u+J((0,0,r))[2],6)
            assert other==-ell and new_rem==J((0,0,rem))[2]
    core_changes=subprocess.check_output(['git','diff','--name-only',p['baseline']['core_baseline_commit'],'--','universe24'],cwd=ROOT,text=True).strip()
    assert not core_changes,'Fixed core baseline changed'
    return {'status':'passed_independent_algebra_and_initial_encoding','new_native_trajectories':0,'registered_cases':len(registered),
        'patterns':eigenchecks,'cases':registered,'native_tensor_equals_independent_operator':True,'core_matches_fixed_baseline':True,
        'independent_ports':[list(row) for row in reference.ports],'independent_weights':[list(row) for row in reference.weights],
        'protocol_sha256':hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),'producer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

def observe(case,states,p,deadline):
    item=pattern(case,p);aa=addresses(case['side']);vv=[value_at(a,item) for a in aa];trace=scalar_trace(case)
    mismatch_count=0;counterexamples=[];input_mismatch_count=0;input_examples=[];event_mismatch_count=0;event_examples=[]
    all_inputs=[];all_events=[];counts={str(k):0 for k in range(3)};checks=[]
    for t,state in enumerate(states):
        if time.process_time()>deadline:raise BudgetStop('Passive observation budget exceeded; complete native checkpoint retained')
        for address,sign in zip(aa,vv):
            expected=encode(trace[t],sign);actual=tuple(state.at(address))
            if actual!=expected:
                mismatch_count+=1
                if len(counterexamples)<16:counterexamples.append({'state':t,'address':list(address),'actual':list(actual),'expected':list(expected)})
    for t,(old,new) in enumerate(zip(states,states[1:]),1):
        if time.process_time()>deadline:raise BudgetStop('Passive observation budget exceeded; complete native checkpoint retained')
        sums=ENGINE.input_sums(old);input_values=[sums.get(address,0) for address in aa];all_inputs.append(input_values)
        expected_events=[]
        for address,sign,u in zip(aa,vv,input_values):
            expected_u=case['lambda']*trace[t-1][1]*sign
            if u!=expected_u:
                input_mismatch_count+=1
                if len(input_examples)<16:input_examples.append({'update':t,'address':list(address),'actual':u,'expected':expected_u})
            before,after=encode(trace[t-1],sign),encode(trace[t],sign);ell=after[1]+before[0]
            if ell and before!=after:expected_events.append((address,expected_u%3,ell))
        actual_events=sorted((event.address,event.kind,event.quotient) for event in clicks(old,new,t));expected_events.sort()
        if actual_events!=expected_events:
            event_mismatch_count+=1
            if len(event_examples)<16:event_examples.append({'update':t,'actual_count':len(actual_events),'expected_count':len(expected_events),
                'unexpected':[list(x) for x in actual_events if x not in set(expected_events)][:16],
                'missing':[list(x) for x in expected_events if x not in set(actual_events)][:16]})
        for address,kind,ell in actual_events:
            terms=[CP.weights[d][address[3]]*old.at(donor(address,d,case['side'],CP.ports)).b for d in range(6)]
            assert sum(terms)==sums.get(address,0)
            all_events.append({'step':t,'address':list(address),'kind':kind,'ell':ell,'u':sum(terms),'six_signed_donor_values':terms});counts[str(kind)]+=1
        checks.append({'update':t,'complete_event_list_matches':actual_events==expected_events,'actual_count':len(actual_events),'expected_count':len(expected_events)})
    returns=[t for t in range(1,len(states)) if states[t]==states[0]];first=returns[0] if returns else None
    lag=first is not None and all(states[t]==states[t+first] for t in range(len(states)-first))
    zero_fixed=all(tuple(state.at(address))==(0,0,2) for state in states for address,sign in zip(aa,vv) if sign==0)
    return {'scalar_trace':[list(row) for row in trace],'full_state_mismatch_count':mismatch_count,'full_state_counterexamples_first16':counterexamples,
        'input_sum_mismatch_count':input_mismatch_count,'input_counterexamples_first16':input_examples,
        'event_mismatch_updates':event_mismatch_count,'event_counterexamples_first16':event_examples,'event_checks':checks,
        'all_native_input_sums':all_inputs,'input_address_order':'lexicographic x,y,z,g; all48 channels at every site',
        'all_C':all_events,'C_counts':counts,'zero_pattern_channels_remain_fixed':zero_fixed,
        'first_complete_state_return_within_H':first,'registered_lag_matches_entire_available_window':lag,
        'all_observed_returns_within_H':returns,'max_sparse_channels':max(len(state.cells) for state in states),
        'all_registered_oracles_pass':mismatch_count==input_mismatch_count==event_mismatch_count==0 and zero_fixed}

def source_hashes():
    paths=[Path(__file__),PROTOCOL,HERE/'__init__.py',HERE/'budget.py',ROOT/'research/reference/algebra.py',ROOT/'research/reference/__init__.py']
    for directory in ('universe24','research/presenter','research/experiments','research/components'):paths.extend((ROOT/directory).rglob('*.py'))
    return {str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(set(paths))}

def run(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=False);(output/'native').mkdir();(output/'records').mkdir()
    p=json.loads(PROTOCOL.read_text());frozen=source_hashes();wall=time.monotonic();ledger=[];native=[];examples=[];failure=None
    (output/'protocol.json').write_bytes(PROTOCOL.read_bytes())
    for relative in frozen:
        target=output/'executed_sources'/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((ROOT/relative).read_bytes())
    registration={'source_sha256':frozen,'checkout_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'checkout_tree':subprocess.check_output(['git','rev-parse','HEAD^{tree}'],cwd=ROOT,text=True).strip(),
        'baseline':p['baseline'],'registered_before_first_native_step':True,'preflight':preflight(p)}
    write_json(output/'registration.json',registration)
    try:
        for case in cases(p):
            if time.process_time()>p['budget']['max_cpu_seconds']-p['budget']['reserve_cpu_seconds_before_case'] or time.monotonic()-wall>p['budget']['max_wall_seconds']-30:raise BudgetStop('Insufficient whole-process reserve before next case')
            experiment=capture(ENGINE,initial(case,p),case['steps'],id=case['id'],title='Invariant family: '+case['id'],
                description=p['scope'],view={'position':[0,0,0],'channel':0},max_frames=case['steps']+1,
                max_cells=p['budget']['max_cumulative_native_rows_per_record'],max_bytes=p['budget']['max_recorded_bytes'],max_seconds=p['budget']['max_seconds_per_record'])
            experiment['provenance']['invariant_case']=case;experiment['provenance']['protocol_sha256']=registration['preflight']['protocol_sha256']
            native_path=output/'native'/(case['id']+'.json.gz');write_compressed(native_path,{'case':case,'experiment':experiment})
            native.append({'id':case['id'],'record':str(native_path.relative_to(output)),'sha256':hashlib.sha256(native_path.read_bytes()).hexdigest()})
            states=recorded_states(experiment)
            if any(len(state.cells)>p['budget']['max_sparse_channels_per_state'] for state in states):raise BudgetStop('Per-state sparse channel cap exceeded')
            observations=observe(case,states,p,time.process_time()+p['budget']['max_observer_cpu_seconds_per_record'])
            row={'case':case,'experiment':experiment,'observations':observations};path=output/'records'/(case['id']+'.json.gz');write_compressed(path,row)
            ledger.append({'id':case['id'],'case':case,'record':str(path.relative_to(output)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                'full_rewind_equal':experiment['provenance']['full_rewind_equal'],'all_registered_oracles_pass':observations['all_registered_oracles_pass'],
                'first_complete_state_return_within_H':observations['first_complete_state_return_within_H'],'C_counts':observations['C_counts']})
            if (case['a'],case['b'])==(0,1) and (case['r']==2 or (case['pattern']=='internal_yy' and case['r']==1)):examples.append(experiment)
            if sum(path.stat().st_size for path in output.rglob('*') if path.is_file())>p['budget']['max_recorded_bytes']-8000000:raise BudgetStop('Recorded evidence byte reserve reached')
            print(f'{len(ledger)}/48 '+case['id'],flush=True)
    except Exception as error:
        failure={'type':type(error).__name__,'message':str(error),'case':locals().get('case')};write_json(output/'failure.json',failure)
    assert frozen==source_hashes(),'Frozen source changed'
    if examples and time.process_time()<p['budget']['child_cpu_soft_limit']-8:write_json(output/'experiments.json',bundle(examples,title='The Presenter: exact invariant families'))
    result={'status':'completed' if len(ledger)==48 and failure is None else 'inconclusive','failure':failure,'completed_cases':len(ledger),'cases':ledger,
        'all_full_rewinds':all(row['full_rewind_equal'] for row in ledger),'all_registered_oracles_pass':len(ledger)==48 and all(row['all_registered_oracles_pass'] for row in ledger),
        'native_checkpoints':native,'not_run_cases':[case['id'] for case in cases(p) if case['id'] not in {row['id'] for row in native}],
        'captured_not_observed':[row['id'] for row in native if row['id'] not in {case['id'] for case in ledger}],
        'child_cpu_seconds_at_result':time.process_time(),'wall_seconds_from_run_entry':time.monotonic()-wall,'scope':p['scope'],'sources_unchanged':True}
    write_json(output/'result.json',result);return result

def main():
    parser=argparse.ArgumentParser(description=__doc__);mode=parser.add_mutually_exclusive_group(required=True);mode.add_argument('--preflight-output',type=Path);mode.add_argument('--output',type=Path);args=parser.parse_args()
    if args.output:
        def exhausted(signum,frame):raise BudgetStop('Child CPU soft limit reached; complete earlier native checkpoints retained')
        signal.signal(signal.SIGXCPU,exhausted);run(args.output)
    else:
        args.preflight_output.parent.mkdir(parents=True,exist_ok=True);write_json(args.preflight_output,preflight(json.loads(PROTOCOL.read_text())))
if __name__=='__main__':main()
