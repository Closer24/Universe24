"""Prospective conditional-carrier to terminal-clock composition."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import shutil
import signal
import subprocess
import time
from research.clock_selection import search_v2 as v2
from research.clock_selection import route_clock as helper
from research.staged_blocks.recipes import ClockGuideInterface
from research.experiments.run import assemble, run_experiment, recorded_states
from research.presenter.export import bundle
from universe24.observation.clicks import clicks

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
PROTOCOL=HERE/'carrier_memory_protocol.json'; PHASES=helper.PHASES
BudgetStop=helper.BudgetStop; write_json=helper.write_json; write_compressed=helper.write_compressed

def groups(p):
    for side,phase in itertools.product(p['family']['sides'],p['family']['receiver_phases']):
        yield [{'id':f'carrier-memory-L{side}-p{phase}-{mask}','side':side,'receiver_phase':phase,'control':mask,
                'clock_remainder':0,'phase':0,'writer_delay':2,'gap':38,'stage':'encounter',
                'guide_target_channel':0,'compensation_direction':None,'clock_present':True}
               for mask in p['family']['controls']]

def interface_cells(phase):return {a:tuple(v) for a,v in ClockGuideInterface(r=0,phase=phase).cells}

def spec(case,p):
    old=json.loads(v2.PROTOCOL.read_text());old['steps']=p['steps'];old['question']=p['question'];old['claim']=p['claim']
    old['budget']['max_cells_per_record']=p['budget']['max_cumulative_native_rows_per_record']
    old['budget']['max_seconds_per_record']=p['budget']['max_seconds_per_record']
    result=v2.case_spec(case,old);c=case['side']//2;contact={(c+20,c,c,g) for g in (0,14)}
    apparatus=result['components'][0]['params']; removed={tuple(row[:4]) for row in apparatus['cells'] if tuple(row[:4]) in contact}
    assert removed==contact
    apparatus['cells']=[row for row in apparatus['cells'] if tuple(row[:4]) not in contact]
    apparatus['sockets'].append({'name':'downstream-interface','addresses':[list(a) for a in sorted(contact)],'allowed_kinds':['clock-guide-interface']})
    cells=interface_cells(case['receiver_phase'])
    result['components'].append({'name':'receiver','recipe':'Patch','at':[c+20,c+1,c],
        'params':{'kind':'clock-guide-interface','cells':[[*a,*v] for a,v in sorted(cells.items())],
                  'ports':{'center':[[0,0,0,2]],'region':[list(a) for a in sorted(cells)]},'sources':{'clock':[[0,0,0,2]]}}})
    result['id']=case['id'];result['title']='Conditional carrier and downstream clock: '+case['id']
    result['view']={'port':'receiver.center'};result['provenance']={'initial_only':True,'protocol_sha256':hashlib.sha256(PROTOCOL.read_bytes()).hexdigest()}
    result['budget']['max_bytes']=p['budget']['max_recorded_bytes'];return result

def preflight(p):
    output=[]
    for family in groups(p):
        prepared={case['control']:assemble(spec(case,p)) for case in family};case=family[0];c=case['side']//2
        states={m:b.initial for m,b in prepared.items()};addresses=set().union(*(s.cells for s in states.values()))
        footprints=v2.input_footprints(case);checks=[]
        for i,name in enumerate(('writer','probe')):
            for other in '01':
                off='0'+other if i==0 else other+'0';on='1'+other if i==0 else other+'1'
                allowed=set(footprints[name]);changed={a for a in addresses if states[off].at(a)!=states[on].at(a)}
                pristine=all(tuple(states[off].at(a))==(0,0,0 if a[1:3]==(c,c) and a[3]==0 else 4 if a[1:3]==(c,c) and a[3]==14 else 2) for a in allowed)
                assert changed<=allowed and pristine
                checks.append({'source':name,'other':other,'changed_addresses':len(changed),'outside_footprint_equal':True,'absent_footprint_pristine':True})
        margins=[]
        for mask,state in states.items():
            for dx,phase in ((0,0),(20,case['receiver_phase'])):
                o=(c+dx,c+1,c)
                assert all(tuple(state.at((*helper.add(o,a[:3]),a[3])))==value for a,value in interface_cells(phase).items())
            active=[a for a,v in state.cells.items() if v.a or v.b]
            margin=min(min(q,case['side']-1-q) for a in active for q in a[:3]);assert margin>p['steps'];margins.append(margin)
        output.append({'side':case['side'],'receiver_phase':case['receiver_phase'],'footprint_checks':checks,
                       'complete_interfaces_compatible':True,'initial_active_margins':margins})
    return {'status':'passed_initial_assembly_only','new_trajectories':0,'cases':sum(len(x) for x in groups(p)),'groups':output,
            'protocol_sha256':hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

def quiet(trace,centers,inputs,boundary,addresses,center_address,hold):
    lo,hi=hold
    predicates={'full336_period4':all(trace[t]==trace[t+4] for t in range(lo,hi-3)),
        'only_center_counters':all(not(v[0] or v[1]) for frame in trace[lo:hi+1] for a,v in zip(addresses,frame) if a!=center_address),
        'unit_center_r0':all(a*a+b*b==1 and r==0 for a,b,r in centers[lo:hi+1]),
        'exact_quarter_turn':all(centers[t+1][:2]==[centers[t][1],-centers[t][0]] for t in range(lo,hi)),
        'zero_center_input_quotient':all(row['u']==row['ell']==0 for row in inputs[lo:hi]),
        'zero_individual_external_terms':all(not row['terms'] for row in boundary[lo:hi])}
    return {'states':hold,'predicates':predicates,'passed':all(predicates.values())}

def observe(case,states,p,deadline):
    c=case['side']//2;events=[];counts={str(k):0 for k in range(3)}
    for t,(old,new) in enumerate(zip(states,states[1:]),1):
        if time.process_time()>deadline:raise BudgetStop('Passive observer budget reached; native checkpoint retained')
        for event in clicks(old,new,t):
            terms=helper.six_terms(old,event.address)
            events.append({'step':t,'address':list(event.address),'kind':event.kind,'ell':event.quotient,'six_terms':terms,'u':sum(x['term'] for x in terms)})
            counts[str(event.kind)]+=1
    clocks={}
    for name,dx,phase in (('controller',0,0),('receiver',20,case['receiver_phase'])):
        o=(c+dx,c+1,c);addresses=[(*helper.add(o,a[:3]),a[3]) for a in sorted(interface_cells(0))];nodes={a[:3] for a in addresses};ca=(*o,2)
        trace=[[list(state.at(a)) for a in addresses] for state in states];centers=[list(state.at(ca)) for state in states]
        inputs=[];boundary=[]
        for t,(old,new) in enumerate(zip(states,states[1:]),1):
            terms=helper.six_terms(old,ca);inputs.append({'update':t,'six_terms':terms,'u':sum(x['term'] for x in terms),'ell':new.at(ca).b+old.at(ca).a})
            boundary.append({'update':t,'terms':helper.external_terms(old,nodes)})
        canonical=all(all(tuple(state.at((*helper.add(o,a[:3]),a[3])))==v for a,v in interface_cells((phase+t)%4).items()) for t,state in enumerate(states))
        windows={'controller_hold':p['readouts']['controller_hold']} if name=='controller' else {'pre_late':p['readouts']['receiver_pre_late_hold'],'terminal':p['readouts']['receiver_terminal_hold']}
        clocks[name]={'region_addresses':[list(a) for a in addresses],'region_trace':trace,'center_trace':centers,'center_inputs':inputs,'external_inputs':boundary,
            'complete_canonical_orbit':canonical,'holds':{label:quiet(trace,centers,inputs,boundary,addresses,ca,hold) for label,hold in windows.items()}}
    incoming={}
    for name,start,delay,bit in (('writer',c-18,0,0),('probe',c-56,38,1)):
        matches=[{'time':delay+k,'origin':start+delay+k,'match':v2.base.packet_matches(states[delay+k],start+delay+k,c,c,1)} for k in p['input']['source_packet_offsets']]
        incoming[name]={'frames':matches,'expected_present':case['control'][bit]=='1','passed':all(row['match']==(case['control'][bit]=='1') for row in matches)}
    epochs={}
    for name,ep in p['epochs'].items():
        frames=[{'time':t,'origin':c+x,'match':v2.base.packet_matches(states[t],c+x,c,c,1)} for t,x in zip(ep['carrier_times'],ep['carrier_origin_offsets'])]
        lo,hi=ep['C_window'];raw=[{k:e[k] for k in ('step','kind','ell')} for e in events if e['address']==[c+12,c,c,0] and lo<=e['step']<=hi]
        expected=[dict(zip(('step','kind','ell'),row)) for row in ep['C_expected']]
        present=case['control'][0]=='1' if name=='early' else case['control']=='11'
        exact=all(row['match'] for row in frames);signature=raw==expected
        epochs[name]={'carrier_frames':frames,'raw_C':raw,'expected_C':expected,'exact_carrier':exact,'exact_C_signature':signature,'carrier_plus_C':exact and signature,
                      'predicted_present':present,'truth_table_pass':all(row['match']==present for row in frames) and ((raw==expected) if present else raw==[])}
    return {'clocks':clocks,'incoming':incoming,'epochs':epochs,'all_C':events,'C_counts':counts,
        'whole_board_period4':all(states[t]==states[t+4] for t in range(len(states)-4)),
        'active_boundary_hit':any(any(q in (0,case['side']-1) for q in a[:3]) for state in states for a,v in state.cells.items() if v.a or v.b),
        'max_sparse_channels':max(len(s.cells) for s in states)}

def assess(rows,p):
    by={row['case']['control']:row['observations'] for row in rows};case=rows[0]['case'];lo,hi=p['readouts']['receiver_terminal_hold']
    eligible=all(v['incoming'][name]['passed'] for v in by.values() for name in ('writer','probe')) and all(not v['active_boundary_hit'] for v in by.values())
    null=by['00']['whole_board_period4'] and all(v['complete_canonical_orbit'] for v in by['00']['clocks'].values())
    gates=all(v['epochs'][name]['truth_table_pass'] for v in by.values() for name in ('early','late'))
    terminal=all(v['clocks']['receiver']['holds']['terminal']['passed'] for v in by.values());comparisons={}
    joint=by['11']['clocks']['receiver']
    for mask in ('00','10','01'):
        other=by[mask]['clocks']['receiver'];rel=[]
        for t in range(lo,hi+1):
            a=tuple(joint['center_trace'][t][:2]);b=tuple(other['center_trace'][t][:2]);rel.append((PHASES.index(a)-PHASES.index(b))%4 if a in PHASES and b in PHASES else None)
        different=all(joint['region_trace'][t]!=other['region_trace'][t] for t in range(lo,hi+1))
        comparisons[mask]={'full336_differs_every_state':different,'relative_center_phases':rel,'fixed_nonzero_phase':len(set(rel))==1 and rel[0] in (1,2,3)}
    departures={}
    for mask in by:
        a=by[mask]['clocks']['receiver'];b=by['00']['clocks']['receiver']
        departures[mask]={name:next((t for t,(x,y) in enumerate(zip(a[key],b[key])) if x!=y),None) for name,key in (('first_center','center_trace'),('first_region','region_trace'))}
    strong=eligible and null and gates and terminal and all(v['full336_differs_every_state'] and v['fixed_nonzero_phase'] for v in comparisons.values())
    return {'side':case['side'],'receiver_phase':case['receiver_phase'],'source_inputs_and_boundary_valid':eligible,'canonical_null_valid':null,
        'early_and_late_truth_tables_valid':gates,'all_terminal_receivers_quiet':terminal,'comparisons_11_against':comparisons,'departures_from_null':departures,
        'primary_terminal_record':strong,'weaker_writer_armed_record':bool(eligible and null and gates and terminal and comparisons['10']['full336_differs_every_state'] and comparisons['10']['fixed_nonzero_phase']),
        'cases':{m:{'incoming':v['incoming'],'epochs':v['epochs'],'holds':{k:x['holds'] for k,x in v['clocks'].items()},'C_counts':v['C_counts']} for m,v in by.items()}}

def source_hashes():
    paths=[Path(__file__),PROTOCOL,HERE/'carrier_memory_budget.py',Path(v2.__file__),v2.PROTOCOL,Path(v2.old.__file__),v2.old.PROTOCOL,Path(v2.base.__file__),v2.base.PROTOCOL,Path(helper.__file__)]
    for directory in ('universe24','research/components','research/experiments','research/presenter','research/staged_blocks'):
        paths.extend((ROOT/directory).glob('*.py') if directory=='research/staged_blocks' else (ROOT/directory).rglob('*.py'))
    return {str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(set(paths))}

def run(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=False);(output/'records').mkdir();(output/'native').mkdir();p=json.loads(PROTOCOL.read_text())
    frozen=source_hashes();wall=time.monotonic();ledger=[];native=[];assessments=[];examples=[];failure=None
    shutil.copyfile(PROTOCOL,output/'protocol.json');shutil.copyfile(Path(__file__),output/'executed_carrier_memory.py')
    for relative in frozen:
        target=output/'executed_sources'/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((ROOT/relative).read_bytes())
    write_json(output/'registration.json',{'source_sha256':frozen,'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'registered_before_capture':True,'preflight':preflight(p)})
    try:
        for family in groups(p):
            rows=[]
            for case in family:
                if time.process_time()>p['budget']['max_cpu_seconds']-p['budget']['reserve_cpu_seconds_before_case'] or time.monotonic()-wall>p['budget']['max_wall_seconds']-60:raise BudgetStop('Insufficient whole-process reserve before next case')
                sp=spec(case,p);cap=run_experiment(sp)
                np=output/'native'/(case['id']+'.json.gz');write_compressed(np,{'case':case,'spec':sp,'assembly':cap['assembly'],'experiment':cap['experiment']})
                native.append({'id':case['id'],'record':str(np.relative_to(output)),'sha256':hashlib.sha256(np.read_bytes()).hexdigest()})
                states=recorded_states(cap['experiment'])
                if any(len(s.cells)>p['budget']['max_sparse_channels_per_state'] for s in states):raise RuntimeError('Per-state sparse cap exceeded')
                row={'case':case,'spec':sp,'assembly':cap['assembly'],'experiment':cap['experiment'],'observations':observe(case,states,p,time.process_time()+p['budget']['max_observer_cpu_seconds_per_record'])}
                rp=output/'records'/(case['id']+'.json.gz');write_compressed(rp,row)
                ledger.append({'id':case['id'],'record':str(rp.relative_to(output)),'sha256':hashlib.sha256(rp.read_bytes()).hexdigest(),'full_rewind_equal':cap['experiment']['provenance']['full_rewind_equal']})
                if case['side']==393 and case['receiver_phase']==2:examples.append(cap['experiment'])
                rows.append({'case':case,'observations':{k:v for k,v in row['observations'].items() if k!='all_C'}})
                if sum(q.stat().st_size for q in output.rglob('*') if q.is_file())>p['budget']['max_recorded_bytes']-16000000:raise BudgetStop('Evidence byte reserve reached')
            assessments.append(assess(rows,p));print(f'{len(ledger)}/32 '+family[0]['id'],flush=True)
    except Exception as error:
        failure={'type':type(error).__name__,'message':str(error),'case':locals().get('case')};write_json(output/'failure.json',failure)
    assert frozen==source_hashes(),'Frozen sources changed'
    if examples and time.process_time()<p['budget']['child_cpu_soft_limit']-10:write_json(output/'experiments.json',bundle(examples,title='The Presenter: conditional carrier and terminal clock'))
    family_pass={str(phase):len([g for g in assessments if g['receiver_phase']==phase])==2 and all(g['primary_terminal_record'] for g in assessments if g['receiver_phase']==phase) for phase in p['family']['receiver_phases']}
    result={'status':'completed' if len(ledger)==32 and failure is None else 'inconclusive','failure':failure,'completed_cases':len(ledger),'cases':ledger,'groups':assessments,
        'primary_family_by_phase':family_pass,'primary_family_pass':any(family_pass.values()),'all_full_rewinds':all(x['full_rewind_equal'] for x in ledger),'sources_unchanged':True,
        'native_checkpoints':native,'not_run_cases':[c['id'] for f in groups(p) for c in f if c['id'] not in {r['id'] for r in native}],
        'captured_not_observed':[r['id'] for r in native if r['id'] not in {x['id'] for x in ledger}],
        'child_cpu_seconds_at_result':time.process_time(),'wall_seconds_from_run_entry':time.monotonic()-wall,'scope':p['claim']}
    write_json(output/'result.json',result);return result

def main():
    parser=argparse.ArgumentParser(description=__doc__);modes=parser.add_mutually_exclusive_group(required=True);modes.add_argument('--preflight-output',type=Path);modes.add_argument('--output',type=Path);args=parser.parse_args()
    if args.output:
        def exhausted(signum,frame):raise BudgetStop('Child CPU soft limit reached; native checkpoints retained')
        signal.signal(signal.SIGXCPU,exhausted);run(args.output)
    else:
        args.preflight_output.parent.mkdir(parents=True,exist_ok=True);write_json(args.preflight_output,preflight(json.loads(PROTOCOL.read_text())))
if __name__=='__main__':main()
