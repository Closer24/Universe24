"""Prospective signal-started quiet clocks; preparation and passive readout only."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
import signal
from pathlib import Path
import time

from research.components import BoardSpec, TensorSpec, Patch, GuidedPacketSource, place, finalize, plain
from research.experiments.run import assemble, recorded_states, run_experiment
from research.presenter.export import bundle, state_sha256
from research.clock_selection.provenance import freeze_sources, verify_sources
from research.staged_blocks import interactions as base
from universe24 import Channel
from universe24.core.group_2o import DIRECTIONS

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];PROTOCOL=HERE/'protocol_activation.json'


def cases(p):
    for side,rc,rh,present in itertools.product(p['board']['sides'],p['family']['center_remainders'],
            p['family']['other_halo_remainders'],p['family']['source_present']):
        yield {'id':f'activation-L{side}-rc{rc}-rh{rh}-s{int(present)}','side':side,
               'center_remainder':rc,'halo_remainder':rh,'source_present':present}


def geometry(side):
    c=side//2;center=(c,c+1,c)
    nodes=(center,*(tuple(center[j]+d[j] for j in range(3)) for d in DIRECTIONS))
    return c,center,tuple((*n,g) for n in nodes for g in range(48))


def prepare(case):
    side=case['side'];c,center,region=geometry(side);tensor=TensorSpec();source_x=c-18
    cells={a:(0,0,2) for a in region};cells[(*center,2)]=(0,0,case['center_remainder'])
    for d,delta in enumerate(DIRECTIONS):
        a=tuple(center[j]+delta[j] for j in range(3))+(tensor.ports[d][2],)
        cells[a]=(0,0,0 if d==3 else case['halo_remainder'])
    cells[(c,c,c,14)]=(0,0,4)
    guide={(x,c,c,g):(0,0,r) for x in range(side) if x!=c and not(case['source_present'] and source_x<=x<source_x+4)
           for g,r in ((0,0),(14,4))}
    pieces=[place(Patch('resting-remainder-apparatus',cells,tensor=tensor),name='apparatus',at=(0,0,0)),
            place(Patch('pristine-guide',guide,tensor=tensor),name='guide',at=(0,0,0))]
    if case['source_present']:
        pieces.append(place(GuidedPacketSource(tensor=tensor),name='source',at=(source_x,c,c)))
    return finalize(BoardSpec(side,tensor=tensor),pieces)


def source_footprint(case):
    c=case['side']//2
    return {tuple(a[j]+(c-18,c,c)[j] for j in range(3))+(a[3],) for a,_ in GuidedPacketSource().cells}


def preparation_check(case):
    on=prepare({**case,'source_present':True}).initial;off=prepare({**case,'source_present':False}).initial
    c,_,region=geometry(case['side']);allowed=source_footprint(case);addresses=on.cells.keys()|off.cells.keys()
    changed={a for a in addresses if on.at(a)!=off.at(a)}
    expected=lambda a:Channel(0,0,0 if a[1:3]==(c,c) and a[3]==0 else 4 if a[1:3]==(c,c) and a[3]==14 else 2)
    return {'outside_source_footprint_equal':changed<=allowed,'changed_addresses':len(changed),
        'source_absent_pristine':all(off.at(a)==expected(a) for a in allowed),
        'all336_initial_counter_pairs_zero':all(not(on.at(a).a or on.at(a).b or off.at(a).a or off.at(a).b) for a in region)}


def case_spec(case,p):
    prepared=prepare(case);c,center,_=geometry(case['side'])
    return {'format':'universe24-assembly-experiment-v1','id':case['id'],'title':'Signal-started clock: '+case['id'],
        'description':p['claim'],'question':p['question'],
        'board':{'side':case['side'],'body_signs':p['board']['body_signs'],'background':p['board']['background']},
        'components':[{'name':'complete_preparation','recipe':'Patch','at':[0,0,0],
            'params':{'kind':'resting-clock-input','cells':[[*a,*v] for a,v in sorted(prepared.initial.cells.items())]}}],
        'steps':p['steps'],'controls':case,'seed':None,'view':{'position':list(center),'channel':2},
        'provenance':{'initial_only':True,'component_manifest':plain(prepared.manifest),'protocol_canonical_sha256':base.digest(p)},
        'budget':{'max_frames':p['steps']+1,'max_cells':p['budget']['max_cells_per_record'],
            'max_bytes':p['budget']['max_bytes_per_record'],'max_seconds':p['budget']['max_seconds_per_record']}}


def observe(case,p,prepared,states):
    c,center,region=geometry(case['side']);bp=json.loads(base.PROTOCOL.read_text())
    bp['board']={'side':case['side'],'body_signs':p['board']['body_signs'],'background':p['board']['background']}
    bp['steps']=p['steps'];bp['readouts']['eligible_hold_starts']=[]
    bp['geometry']={'clock_x':c,'clock_y':c+1,'clock_z':c,'packet_x':c-18,'row_y':c,'row_z':c,
                    'forward_outlet_x':c+8,'backward_outlet_x':c-8}
    data=base.observe(bp,{'guide_target_channel':0},prepared,states)
    data['incoming']=[{'step':t,'match':base.packet_matches(states[t],c-18+t,c,c,1)} for t in p['incoming']['times']]
    ctr=data['center_trace'];first=next((t for t,v in enumerate(ctr) if v[0] or v[1]),None)
    native=next((e for e in data['center_C'] if e['step']==first),None)
    data['first_center_activation']=None if first is None else {'step':first,'before':ctr[first-1] if first else None,
        'after':ctr[first],'input':data['center_inputs'][first-1] if first else None,'native_C':native}
    data['first_other_region_counter_activity']=next((t for t,frame in enumerate(data['region_trace'])
        if any(v[0] or v[1] for index,v in enumerate(frame) if index!=2)),None)
    start,end=p['hold']['start'],p['hold']['through'];frames=data['region_trace'][start:end+1];central=ctr[start:end+1]
    data['hold']={'full336_lag4':all(frames[k]==frames[k+4] for k in range(len(frames)-4)),
        'only_center_counters_nonzero':all(not(v[0] or v[1]) for frame in frames for index,v in enumerate(frame) if index!=2),
        'center_small_nonzero':all(0<abs(v[0])+abs(v[1])<=2 for v in central),
        'constant_even_remainder':len({v[2] for v in central})==1 and all(v[2]%2==0 for v in central),
        'quarter_turn_each_update':all(after[:2]==[before[1],-before[0]] for before,after in zip(central,central[1:])),
        'every_external_term_zero':all(not row['nonzero_external_terms'] for row in data['boundary_inputs'][start:end]),
        'no_center_C':not any(start<e['step']<=end for e in data['center_C'])}
    a,b,r=central[0];data['hold_class']='unit' if abs(a)+abs(b)==1 else 'axis2' if sorted((abs(a),abs(b)))==[0,2] else 'diagonal' if abs(a)==abs(b)==1 else None
    data['hold_center_initial']=[a,b,r]
    active=[a for a,v in states[0].cells.items() if v.a or v.b]
    data['initial_active_boundary_margin']=min((min(q,case['side']-1-q) for a in active for q in a[:3]),default=None)
    return data


def assess(case,p,states,data):
    act=data['first_center_activation'];margin=data['initial_active_boundary_margin']
    native=bool(act and act['step']>0 and act['before'][:2]==[0,0] and act['input']['u']!=0 and
                act['native_C'] is not None and act['native_C']['ell']!=0)
    return {'incoming_contract':all(v['match']==case['source_present'] for v in data['incoming']),
        'initial_region_at_rest':all(not(v[0] or v[1]) for v in data['region_trace'][0]),
        'whole_board_stationary':all(s==states[0] for s in states),
        'native_contact_activation':native,'quiet_clock_hold':all(data['hold'].values()),'clock_class':data['hold_class'],
        'strict_initial_causal_margin':margin is None or margin>p['steps'],
        'no_active_boundary_contact':not data['active_boundary_hits']}


def assess_pair(rows,check,case=None):
    by={r['case']['source_present']:r for r in rows};complete=len(rows)==2 and set(by)=={False,True}
    valid=all(check[k] for k in ('outside_source_footprint_equal','source_absent_pristine','all336_initial_counter_pairs_zero'))
    common=complete and valid and all(r['assessment'][k] for r in rows for k in ('incoming_contract','initial_region_at_rest',
        'strict_initial_causal_margin','no_active_boundary_contact')) and all(r['experiment']['provenance']['full_rewind_equal'] for r in rows)
    accepted=common and by[False]['assessment']['whole_board_stationary'] and by[True]['assessment']['native_contact_activation'] and by[True]['assessment']['quiet_clock_hold']
    case=rows[0]['case'] if rows else (case or {})
    return {'geometry':{k:v for k,v in case.items() if k not in ('source_present','id')},'complete_pair':complete,
        'initial_preparation_checks':check,'common_eligible':common,'accepted_signal_started_clock':accepted,
        'clock_class':by[True]['assessment']['clock_class'] if accepted else None,
        'cases':{str(int(k)):r['assessment'] for k,r in by.items()}}


def run(output,protocol_path=PROTOCOL):
    wall_start=time.monotonic();raw_protocol=Path(protocol_path).read_bytes();p=json.loads(raw_protocol)
    output=Path(output);output.mkdir(parents=True,exist_ok=False);(output/'records').mkdir();(output/'native_captures').mkdir();(output/'protocol.json').write_bytes(raw_protocol)
    def captured_unobserved():
        captured={f.name[:-8] for f in (output/'native_captures').glob('*.json.gz')}
        observed={f.name[:-8] for f in (output/'records').glob('*.json.gz')}
        return sorted(captured-observed)
    def cpu_interrupt(signum,frame):
        base.write_json(output/'cpu_interruption.json',{'status':'inconclusive_cpu_interruption',
            'signal':signum,'cpu_absolute':time.process_time(),'captured_but_unobserved_ids':captured_unobserved(),
            'native_checkpoints_preserved':True,'scientific_acceptance':'No incomplete pair is accepted.'})
        raise SystemExit(124)
    signal.signal(signal.SIGXCPU,cpu_interrupt)
    sources=[Path(__file__),Path(protocol_path),HERE/'activation_budget.py',HERE/'provenance.py',HERE/'__init__.py',
        Path(base.__file__),base.PROTOCOL,ROOT/'research/staged_blocks/__init__.py',ROOT/'research/experiments/run.py',
        ROOT/'research/experiments/__init__.py',*sorted((ROOT/'universe24').rglob('*.py')),
        *sorted((ROOT/'research/components').glob('*.py')),*sorted((ROOT/'research/presenter').glob('*.py'))]
    freeze_sources(output/'source_provenance',[str(x.relative_to(ROOT)) for x in sources],metadata={'protocol_sha256':hashlib.sha256(raw_protocol).hexdigest(),'seed':None,'budget':p['budget']})
    domain=list(cases(p));checks={c['id']:preparation_check(c) for c in domain}
    if not all(all(x[k] for k in ('outside_source_footprint_equal','source_absent_pristine','all336_initial_counter_pairs_zero')) for x in checks.values()):raise ValueError('Preparation check failed')
    base.write_json(output/'registration.json',{'protocol_sha256':hashlib.sha256(raw_protocol).hexdigest(),'cases':domain,'registered_before_capture':True,'seed':None})
    base.write_json(output/'preparation_equivalence.json',checks)
    ledger=[];failed=[];pairs=[];examples=[];rows=[];stop=None
    for case in domain:
        if time.process_time()>=p['budget']['stop_new_captures_at_cpu_seconds'] or time.monotonic()-wall_start>=p['budget']['max_wall_seconds']-35:
            stop='global_capture_cutoff';break
        if sum(f.stat().st_size for f in output.rglob('*') if f.is_file())>=p['budget']['max_recorded_bytes']-1048576:
            stop='data_budget';break
        spec=case_spec(case,p);base.write_json(output/'inflight_spec.json',spec)
        base.write_json(output/'progress.json',{'case':case['id'],'complete_records':len(ledger),'failed_records':len(failed),'cpu_absolute':time.process_time(),'status':'capture_started'})
        try:
            prepared=assemble(spec);record=run_experiment(spec)
            native_relative='native_captures/'+case['id']+'.json.gz'
            native_bytes=gzip.compress(base.canonical(record).encode(),mtime=0)
            temporary=output/(native_relative+'.tmp');temporary.write_bytes(native_bytes);temporary.replace(output/native_relative)
            base.write_json(output/'progress.json',{'case':case['id'],'complete_records':len(ledger),'failed_records':len(failed),'cpu_absolute':time.process_time(),'status':'native_saved_observation_pending'})
            states=recorded_states(record['experiment']);obs=observe(case,p,prepared,states)
            row={'case':case,'spec':spec,'assembly':record['assembly'],'experiment':record['experiment'],'observations':obs,'assessment':assess(case,p,states,obs),
                 'protocol_sha256':hashlib.sha256(raw_protocol).hexdigest()}
            raw=base.canonical(row).encode();compressed=gzip.compress(raw,mtime=0);relative='records/'+case['id']+'.json.gz'
            temporary=output/(relative+'.tmp');temporary.write_bytes(compressed);temporary.replace(output/relative)
            ledger.append({'id':case['id'],'case':case,'record':relative,'record_sha256':hashlib.sha256(raw).hexdigest(),
                'native_capture':native_relative,'native_capture_sha256':hashlib.sha256(native_bytes).hexdigest(),
                'record_gzip_sha256':hashlib.sha256(compressed).hexdigest(),'frames':len(states),'full_state_inverse':record['experiment']['provenance']['full_rewind_equal'],
                'initial_state_sha256':state_sha256(states[0]),'final_state_sha256':state_sha256(states[-1]),'assessment':row['assessment']})
            rows.append(row)
            if case['side']==225:examples.append(record['experiment'])
        except Exception as exc:
            failure={'case':case,'exception_type':type(exc).__name__,'message':str(exc),'spec':spec,'status':'inconclusive_record_failure'}
            failed.append(failure);base.write_json(output/('failure-'+case['id']+'.json'),failure)
        base.write_json(output/'completed_records_checkpoint.json',ledger)
        base.write_json(output/'progress.json',{'case':case['id'],'complete_records':len(ledger),'failed_records':len(failed),'cpu_absolute':time.process_time(),'status':'case_finished'})
        if case['source_present']:
            pair=assess_pair(rows,checks[case['id']],case);pairs.append(pair);rows=[]
            print(base.canonical({'case':case['id'],'completed':len(ledger),'failed':len(failed),'accepted':pair['accepted_signal_started_clock'],'cpu_absolute':time.process_time()}),flush=True)
    if rows:pairs.append(assess_pair(rows,checks[rows[0]['case']['id']]))
    verification=verify_sources(output/'source_provenance');base.write_json(output/'source_verification.json',verification)
    if not verification['archive_verified'] or not verification['live_sources_unchanged']:raise RuntimeError('Source identity changed')
    selections=[];unexported=[]
    for i in range(0,len(examples),2):
        subset=examples[i:i+2];name=f'experiments-{i//2+1:03d}.json'
        if time.process_time()>=165:
            unexported.extend(e['id'] for e in examples[i:]);break
        raw=(base.canonical(bundle(subset,title='The Presenter: signal-started clock tests'))+'\n').encode()
        if sum(f.stat().st_size for f in output.rglob('*') if f.is_file())+len(raw)+1048576>=p['budget']['max_recorded_bytes']:
            unexported.extend(e['id'] for e in examples[i:]);break
        (output/name).write_bytes(raw);selections.append({'bundle':name,'ids':[e['id'] for e in subset]})
    base.write_json(output/'presenter_selection.json',{'selected_completed_experiments':len(examples),'pages':selections,'unexported':unexported})
    accepted=[g for g in pairs if g['accepted_signal_started_clock']]
    replicated=[]
    for rc,rh in itertools.product(p['family']['center_remainders'],p['family']['other_halo_remainders']):
        matching=[g for g in pairs if g['geometry'].get('center_remainder')==rc and g['geometry'].get('halo_remainder')==rh]
        ok=len(matching)==2 and all(g['accepted_signal_started_clock'] for g in matching) and len({g['clock_class'] for g in matching})==1
        replicated.append({'center_remainder':rc,'halo_remainder':rh,'accepted_on_both_sizes':ok,'class':matching[0]['clock_class'] if ok else None})
    done={x['id'] for x in ledger}|{x['case']['id'] for x in failed}
    result={'status':'completed' if not stop and not failed else 'inconclusive','stop_reason':stop,'registered_cases':len(domain),
        'completed_cases':len(ledger),'failed_cases':failed,'not_run_cases':[c for c in domain if c['id'] not in done],
        'captured_but_unobserved_ids':captured_unobserved(),
        'cases':ledger,'pairs':pairs,'replicated_geometries':replicated,'accepted_pairs':len(accepted),
        'classes':{kind:sum(g['clock_class']==kind for g in accepted) for kind in ('unit','axis2','diagonal')},
        'all_full_state_inverses':all(x['full_state_inverse'] for x in ledger),'source_hashes_unchanged':True,
        'cpu_seconds_through_export':time.process_time(),'wall_seconds_through_export':time.monotonic()-wall_start,'claim':p['claim']}
    base.write_json(output/'result.json',result)
    print(base.canonical({k:result[k] for k in ('status','completed_cases','accepted_pairs','classes','cpu_seconds_through_export')}),flush=True)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True,type=Path);args=parser.parse_args();run(args.output)


if __name__=='__main__':main()
