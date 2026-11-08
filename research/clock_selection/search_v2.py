"""New full-input source controls; V1 counter-only failures remain unchanged."""
from __future__ import annotations

import argparse
from copy import deepcopy
import gzip
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import time

from research.components import GuidedPacketSource
from research.experiments.run import assemble, recorded_states, run_experiment
from research.presenter.export import bundle, state_sha256
from research.clock_selection import search as old
from research.clock_selection.provenance import freeze_sources, verify_sources

base=old.base
ROOT=old.ROOT
HERE=Path(__file__).resolve().parent
PROTOCOL=HERE/'protocol_v2.json'


def geometries(p):
    for geometry in old.geometries(p):
        for present in p['family']['clock_present']:
            yield {**geometry,'id':geometry['id']+('-clock1' if present else '-clock0'), 'clock_present':present}


def input_footprints(case):
    c=case['side']//2
    origin=c-16-case['writer_delay']
    return {name:[(a[0]+x,a[1]+c,a[2]+c,a[3]) for a,_ in GuidedPacketSource().cells]
            for name,x in (('writer',origin),('probe',origin-case['gap']))}


def case_spec(case,p):
    spec=old.case_spec(case,p)
    c=case['side']//2
    params=spec['components'][0]['params']
    retained=[spec['components'][0]]
    for item,present in zip(spec['components'][1:],case['control']):
        if present=='1':
            retained.append(item)
        else:
            x=item['at'][0]
            params['cells'] += [[xx,c,c,g,0,0,r] for xx in range(x,x+4) for g,r in ((0,0),(14,4))]
            restored={(xx,c,c,g) for xx in range(x,x+4) for g in (0,14)}
            params['sockets']=[s for s in params['sockets'] if not any(tuple(a) in restored for a in s['addresses'])]
    if not case.get('clock_present',False):
        for row in params['cells']:
            if row[:4]==[c,c+1,c,2]:row[4:6]=[0,0]
    spec['components']=retained
    spec['title']='Full-input clock-conditioned probe: '+spec['id']
    spec['provenance']={'protocol_sha256':base.digest(p),'initial_only':True,
        'full_input_footprints':{name:[list(a) for a in addresses] for name,addresses in input_footprints(case).items()},
        'clock_present':case.get('clock_present',False),'clock_off_is_counter_only':True}
    return spec


def footprint_checks(case,p):
    states={m:assemble(case_spec({**case,'control':m},p)).initial for m in p['family']['controls']}
    addresses=set().union(*(s.cells for s in states.values()))
    footprints=input_footprints(case);c=case['side']//2
    tests=[]
    for index,name in enumerate(('writer','probe')):
        allowed=set(footprints[name])
        for other in ('0','1'):
            off=('0'+other) if index==0 else (other+'0')
            on=('1'+other) if index==0 else (other+'1')
            changed={a for a in addresses if states[off].at(a)!=states[on].at(a)}
            outside_ok=changed<=allowed
            absent_ok=all(tuple(states[off].at(a))==(0,0,0 if a[1:3]==(c,c) and a[3]==0 else
                         4 if a[1:3]==(c,c) and a[3]==14 else 2) for a in allowed)
            tests.append({'source':name,'other_present':other,'changed_addresses':len(changed),
                          'outside_declared_footprint_equal':outside_ok,'absent_footprint_pristine':absent_ok})
    return {'cases':tests,'passed':all(t['outside_declared_footprint_equal'] and t['absent_footprint_pristine'] for t in tests),
            'full_initial_remainders_identical':all(len({s.at(a).r for s in states.values()})==1 for a in addresses)}


def observe(case,p,prepared,states):
    if case['stage']=='pristine':return old.observe(case,p,prepared,states)
    data=base.observe(old.observer_protocol(case,p),case,prepared,states)
    c=case['side']//2;probe_x=c-16-case['writer_delay']-case['gap']
    data['incoming']=[{'step':case['gap']+k,'origin_x':probe_x+case['gap']+k,
        'match':base.packet_matches(states[case['gap']+k],probe_x+case['gap']+k,c,c,1)} for k in p['incoming']['offsets']]
    T=24+case['writer_delay']+case['gap']
    data['registered_output']=[{'step':T+k,'origin_x':c+8+k,
        'match':base.packet_matches(states[T+k],c+8+k,c,c,1)} for k in p['output']['offsets']]
    data['registered_C_window']=[T-3,T+4]
    data['registered_output_C']=[{k:e[k] for k in ('step','kind','ell')} for e in data['all_C']
        if e['address']==[c+8,c,c,0] and T-3<=e['step']<=T+4]
    data['expected_output_C']=[{'step':T+dt,'kind':kind,'ell':ell} for dt,kind,ell in p['output']['C_expected']]
    active=[a for a,v in states[0].cells.items() if v.a or v.b]
    data['initial_active_counter_count']=len(active)
    data['initial_active_boundary_margin']=min((min(q,case['side']-1-q) for a in active for q in a[:3]),default=None)
    start,end=p['hold']['start'],p['hold']['through'];region=data['region_trace'][start:end+1]
    center=data['center_trace'][start:end+1];h=data['center_address'][3]
    data['hold']={'start':start,'through':end,
        'complete_region_period4':all(region[j]==region[j+4] for j in range(len(region)-4)),
        'center_unit_counter_norm':all(v[0]*v[0]+v[1]*v[1]==1 for v in center),
        'other_counter_pairs_zero':all(not(v[0] or v[1]) for frame in region for j,v in enumerate(frame) if j!=h),
        'every_external_term_zero':all(not r['nonzero_external_terms'] for r in data['boundary_inputs'][start:end]),
        'center_u_and_ell_zero':all(row['u']==0 and data['center_trace'][start+j+1][1]+center[j][0]==0
            for j,row in enumerate(data['center_inputs'][start:end]))}
    c=case['side']//2; excluded={tuple(n) for n in data['region_nodes']}
    checks=[]
    for offset in p['near_incoming']['origin_offsets_from_clock']:
        x=c+offset;t=16+case['writer_delay']+case['gap']+offset
        expected={a:v for a,v in base._expected_packet(x,c,c,1).items() if a[:3] not in excluded}
        actual={a:v for a,v in states[t].cells.items() if x-1<=a[0]<=x+4 and abs(a[1]-c)<=1 and abs(a[2]-c)<=1
                and a[:3] not in excluded}
        checks.append({'step':t,'origin_x':x,'match':actual==expected})
    data['near_incoming']=checks
    return data


def assess_case(case,p,states,data):
    if case['stage']=='pristine':return {'pristine_translation':data['complete_translation']}
    exact=all(r['match'] for r in data['registered_output'])
    raw=data['registered_output_C']==data['expected_output_C']
    margin=data['initial_active_boundary_margin']
    return {'incoming_contract':all(r['match']==(case['control'][1]=='1') for r in data['incoming']),
        'near_incoming_contract':all(r['match']==(case['control'][1]=='1') for r in data['near_incoming']),
        'complete_hold':all(v for k,v in data['hold'].items() if k not in ('start','through')),
        'exact_output_carrier':exact,'exact_output_C_signature':raw,'carrier_plus_C':exact and raw,
        'strict_initial_causal_margin':margin is None or margin>p['steps'],
        'no_active_boundary_contact':not data['active_boundary_hits']}


def assess_group(rows,p,preparation_check):
    by={r['case']['control']:r for r in rows};case=rows[0]['case']
    start,end=p['hold']['start'],p['hold']['through']
    baseline=all(by['00']['states'][t]==by['00']['states'][t+4] for t in range(p['steps']-3))
    input_ok=all(r['assessment'][k] for r in rows for k in ('incoming_contract','near_incoming_contract',
                 'strict_initial_causal_margin','no_active_boundary_contact'))
    hold=all(r['assessment']['complete_hold'] for r in rows)
    changed=all(by['11']['observations']['region_trace'][t]!=by['01']['observations']['region_trace'][t]
                for t in range(start,end+1))
    no_leak=all(not by[m]['assessment']['exact_output_carrier'] for m in ('00','10'))
    joint=by['11']['assessment'];probe=by['01']['assessment']
    carrier_diff=joint['exact_output_carrier']!=probe['exact_output_carrier']
    raw_diff=joint['exact_output_C_signature']!=probe['exact_output_C_signature']
    gate=case['clock_present'] and preparation_check['passed'] and baseline and input_ok and hold and changed and no_leak and carrier_diff
    pred_joint=case['gap']%4==2;pred_probe=(case['phase']+case['writer_delay']+case['gap'])%4==2
    return {'geometry':{k:v for k,v in case.items() if k!='control'},'preparation_equivalence':preparation_check,
        'clock_only_complete_period4':baseline,'all_input_boundary_contracts':input_ok,'all_complete_holds':hold,
        'retained_full_region_differs':changed,'writer_only_and_null_output_absent':no_leak,
        'carrier_discriminator':gate,'enabling_gate':gate and joint['exact_output_carrier'],
        'suppressing_gate':gate and not joint['exact_output_carrier'],
        'carrier_and_C_discriminator':gate and joint['carrier_plus_C']!=probe['carrier_plus_C'],
        'raw_C_discriminator':gate and raw_diff,'raw_carrier_difference_without_eligibility':carrier_diff,
        'clock_off_comparison_only':not case['clock_present'],
        'predicted_joint_carrier':pred_joint if case['clock_present'] else None,
        'predicted_probe_only_carrier':pred_probe if case['clock_present'] else None,
        'carrier_prediction_matches':(joint['exact_output_carrier']==pred_joint and probe['exact_output_carrier']==pred_probe)
                                       if case['clock_present'] else None,
        'cases':{m:r['assessment'] for m,r in by.items()},
        'full_final_hashes':{m:state_sha256(r['states'][-1]) for m,r in by.items()},'claim_limit':p['claim']}


def run(output,protocol_path=PROTOCOL):
    raw_protocol=Path(protocol_path).read_bytes();p=json.loads(raw_protocol)
    output=Path(output);output.mkdir(parents=True,exist_ok=False);(output/'records').mkdir()
    (output/'protocol.json').write_bytes(raw_protocol)
    source_paths=[Path(__file__),Path(protocol_path),Path(old.__file__),old.PROTOCOL,Path(base.__file__),base.PROTOCOL,
        HERE/'provenance.py',HERE/'__init__.py',*sorted((ROOT/'universe24').rglob('*.py')),
        *sorted((ROOT/'research/components').glob('*.py')),ROOT/'research/experiments/__init__.py',
        ROOT/'research/experiments/run.py',ROOT/'research/staged_blocks/__init__.py',*sorted((ROOT/'research/presenter').glob('*.py'))]
    source_hashes={str(s.relative_to(ROOT)):hashlib.sha256(s.read_bytes()).hexdigest() for s in source_paths}
    freeze_sources(output/'source_provenance',source_hashes.keys(),metadata={'protocol_sha256':hashlib.sha256(raw_protocol).hexdigest(),
        'seed':None,'board':p['board'],'family':p['family'],'budget':p['budget']})
    groups=list(geometries(p))
    preparation_checks={g['id']:footprint_checks(g,p) for g in groups}
    if not all(v['passed'] for v in preparation_checks.values()):raise ValueError('Full-input preparation contract failed before capture')
    # Independent clock bit has exactly one allowed changed counter address.
    clock_checks=[]
    for g in groups:
        if not g['clock_present']:continue
        for mask in p['family']['controls']:
            on=assemble(case_spec({**g,'control':mask},p)).initial
            off=assemble(case_spec({**g,'control':mask,'clock_present':False},p)).initial
            changed={a for a in on.cells.keys()|off.cells.keys() if on.at(a)!=off.at(a)}
            center=(g['side']//2,g['side']//2+1,g['side']//2,2)
            ok=changed<={center} and on.at(center).r==off.at(center).r
            clock_checks.append({'case':g['id']+'-'+mask,'passed':ok})
    if not all(c['passed'] for c in clock_checks):raise ValueError('Clock-only counter mask failed before capture')
    base.write_json(output/'preparation_equivalence.json',{'groups':preparation_checks,'clock_masks':clock_checks,'no_evolution':True})
    pristine=[{'id':f'full-input-pristine-gap{gap}','side':p['pristine']['side'],'clock_remainder':0,'phase':0,
        'writer_delay':p['pristine']['writer_delay'],'gap':gap,'stage':'pristine','guide_target_channel':0,
        'compensation_direction':None,'control':'11','clock_present':False} for gap in p['pristine']['gaps']]
    batches=[[c] for c in pristine]+[[{**g,'control':m} for m in p['family']['controls']] for g in groups]
    cases=[c for batch in batches for c in batch]
    registration={'format':'universe24-clock-selection-registration-v2','base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'protocol_sha256':hashlib.sha256(raw_protocol).hexdigest(),'protocol_canonical_sha256':base.digest(p),
        'source_sha256':source_hashes,'registered_before_capture':True,'cases':cases,'seed':None,'python':platform.python_version()}
    base.write_json(output/'registration.json',registration)
    started_cpu,started_wall=time.process_time(),time.monotonic();ledger=[];assessments=[];examples=[];reason=None
    for batch in batches:
        if time.process_time()-started_cpu>=p['budget']['max_cpu_seconds'] or time.monotonic()-started_wall>=p['budget']['max_wall_seconds']:
            reason='time_budget';break
        if sum(f.stat().st_size for f in output.rglob('*') if f.is_file())>=p['budget']['max_recorded_bytes']:
            reason='data_budget';break
        rows=[]
        for case in batch:
            spec=case_spec(case,p);prepared=assemble(spec);record=run_experiment(spec)
            states=recorded_states(record['experiment']);obs=observe(case,p,prepared,states)
            rows.append({'case':case,'spec':spec,'assembly':record['assembly'],'experiment':record['experiment'],
                         'states':states,'observations':obs,'assessment':assess_case(case,p,states,obs)})
        group=assess_group(rows,p,preparation_checks[batch[0]['id']]) if len(rows)==4 else None
        for row in rows:
            wrapper={k:v for k,v in row.items() if k!='states'}
            wrapper.update({'format':'universe24-clock-selection-record-v2','protocol_sha256':registration['protocol_sha256'],'group_assessment':group})
            raw=base.canonical(wrapper).encode();compressed=gzip.compress(raw,mtime=0)
            relative='records/'+row['spec']['id']+'.json.gz';(output/relative).write_bytes(compressed)
            ledger.append({'id':row['spec']['id'],'case':row['case'],'record':relative,
                'record_sha256':hashlib.sha256(raw).hexdigest(),'record_gzip_sha256':hashlib.sha256(compressed).hexdigest(),
                'initial_state_sha256':state_sha256(row['states'][0]),'final_state_sha256':state_sha256(row['states'][-1]),
                'frames':len(row['states']),'transitions':len(row['states'])-1,
                'full_state_inverse':row['experiment']['provenance']['full_rewind_equal'],'assessment':row['assessment']})
            c=row['case']
            if c['stage']=='encounter' and c['side']==337 and c['clock_present'] and c['phase']==0 and c['gap'] in (36,38):
                examples.append(row['experiment'])
        if group:assessments.append(group)
        print(base.canonical({'completed':len(ledger),'registered':len(cases),'case':batch[0]['id'],
            'gate':group['carrier_discriminator'] if group else None}),flush=True)
    verification=verify_sources(output/'source_provenance');base.write_json(output/'source_verification.json',verification)
    if not verification['archive_verified'] or not verification['live_sources_unchanged']:raise RuntimeError('Source identity changed')
    result={'format':'universe24-clock-selection-result-v2','status':'completed' if reason is None else 'budget_stopped',
        'stop_reason':reason,'registered_cases':len(cases),'completed_cases':len(ledger),'cases':ledger,'groups':assessments,
        'not_run_cases':cases[len(ledger):],'all_full_state_inverses':all(r['full_state_inverse'] for r in ledger),
        'pristine_passes':sum(r['assessment'].get('pristine_translation',False) for r in ledger),
        'carrier_discriminator_groups':sum(g['carrier_discriminator'] for g in assessments),
        'enabling_groups':sum(g['enabling_gate'] for g in assessments),'suppressing_groups':sum(g['suppressing_gate'] for g in assessments),
        'raw_C_discriminator_groups':sum(g['raw_C_discriminator'] for g in assessments),
        'cpu_seconds':time.process_time()-started_cpu,'wall_seconds':time.monotonic()-started_wall,
        'source_hashes_unchanged':True,'claim':p['claim']}
    base.write_json(output/'result.json',result)
    selections=[]
    for i in range(0,len(examples),4):
        filename=f'experiments-{i//4+1:03d}.json'
        subset=examples[i:i+4]
        (output/filename).write_text(base.canonical(bundle(subset,title='The Presenter: full-input clock-written probe'))+'\n')
        selections.append({'bundle':filename,'ids':[e['id'] for e in subset]})
    base.write_json(output/'presenter_selection.json',{'complete_experiments':len(examples),'pages':selections,
                    'selection':'Frozen protocol selection, partitioned into complete groups of four for unchanged Presenter limits.'})
    receipt={'bytes':sum(f.stat().st_size for f in output.rglob('*') if f.is_file()),
        'cpu_overrun':max(0,result['cpu_seconds']-p['budget']['max_cpu_seconds']),
        'wall_overrun':max(0,result['wall_seconds']-p['budget']['max_wall_seconds'])}
    receipt['byte_overrun']=max(0,receipt['bytes']-p['budget']['max_recorded_bytes'])
    base.write_json(output/'budget_receipt.json',receipt)
    print(base.canonical({k:result[k] for k in ('completed_cases','carrier_discriminator_groups','enabling_groups',
                                             'suppressing_groups','raw_C_discriminator_groups','cpu_seconds')}),flush=True)
    return result


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True,type=Path)
    parser.add_argument('--protocol',default=PROTOCOL,type=Path);args=parser.parse_args(argv)
    return run(args.output,args.protocol)


if __name__=='__main__':main()
