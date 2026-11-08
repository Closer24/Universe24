"""Frozen orthogonal-input experiments with complete passive outlet readouts."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
from functools import lru_cache
from pathlib import Path
import time

from research.components import BoardSpec, Patch, TensorSpec, finalize, place, plain
from research.staged_blocks.orbit import ShieldedOrbit
from research.clock_selection.orthogonal_preflight import packet
from research.clock_selection import search as previous
from research.clock_selection.provenance import freeze_sources, verify_sources
from research.experiments.run import assemble, recorded_states, run_experiment
from research.presenter.export import bundle, state_sha256
from universe24 import Channel, State

ROOT = previous.ROOT
HERE = Path(__file__).resolve().parent
PROTOCOL = HERE/'protocol_two_outlet.json'
base = previous.base
AXES = {'X':(0,0,14), 'Y':(1,15,39)}


@lru_cache(maxsize=1)
def tensor():
    return TensorSpec()


def geometries(p):
    for side,gap in itertools.product(p['pristine_crossed'].get('sides',[p['pristine_crossed']['side']]),p['pristine_crossed']['gaps']):
        if side!=p['pristine_crossed']['side'] and gap not in p['pristine_crossed'].get('holdout_gaps',[]):continue
        yield {'id':f'orthogonal-L{side}-bare-gap{gap}','side':side,'gap':gap,'phase':0,'clock_mode':'bare','stage':'crossed'}
    f=p['family']
    for side,phases,modes in ((f['primary_side'],f['phases'],f['clock_modes']),
                             (f['holdout_side'],f['holdout_phases'],f['holdout_clock_modes'])):
        for phase,gap,mode in itertools.product(phases,f['gaps'],modes):
            yield {'id':f'orthogonal-L{side}-p{phase}-{mode}-gap{gap}','side':side,'gap':gap,'phase':phase,
                   'clock_mode':mode,'stage':'encounter'}


def origins(case):
    c=case['side']//2
    return {'X':(c-19,c-1,c), 'Y':(c+1,c-19-case['gap'],c)}


def source_footprints(case):
    fixed_tensor=tensor()
    return {name:[tuple(a[j]+origin[j] for j in range(3))+(a[3],)
                  for a,_ in packet(*AXES[name],True,fixed_tensor).cells]
            for name,origin in origins(case).items()}


def prepare(case,p):
    fixed_tensor=tensor();side=case['side'];c=side//2;pieces=[]
    isolated=case['stage']=='isolated'
    names=(case['axis'],) if isolated else ('X','Y')
    source_positions=origins(case)
    for name in names:
        axis,primary,companion=AXES[name]
        present=case.get('control','11')['XY'.index(name)]=='1'
        origin=source_positions[name]
        start=origin[axis]
        cells={}
        for i in range(side):
            if present and start<=i<start+4:continue
            if not isolated and case['clock_mode']!='bare' and i==c:continue
            xyz=list(origin);xyz[axis]=i
            for g,r in ((primary,0),(companion,4)):cells[(*xyz,g)]=(0,0,r)
        pieces.append(place(Patch(name+'-guide',cells,tensor=fixed_tensor),name=name+'_guide',at=(0,0,0)))
        if present:pieces.append(place(packet(axis,primary,companion,True,fixed_tensor),name=name+'_source',at=origin))
    if not isolated and case['clock_mode']!='bare':
        orbit=ShieldedOrbit(channel=2,a=0,b=1,r=0,phase=case['phase'],tensor=fixed_tensor,
                            halo_remainders=(0,2,2,0,2,2))
        cells=dict(orbit.cells)
        for address in ((0,-1,0,14),(1,0,0,39)):
            if cells[address]!=(0,0,2):raise ValueError('Companion guide conflicts with active clock halo')
            cells[address]=(0,0,4)
        if case['clock_mode']=='counter_off':cells[(0,0,0,2)]=(0,0,cells[(0,0,0,2)][2])
        pieces.append(place(Patch('crossed-clock-interface',cells,tensor=fixed_tensor),name='clock_interface',at=(c,c,c)))
    return finalize(BoardSpec(side,tensor=fixed_tensor),pieces)


def case_spec(case,p):
    prepared=prepare(case,p);c=case['side']//2
    steps=p['pristine_isolated']['steps'] if case['stage']=='isolated' else p['steps']
    return {'format':'universe24-assembly-experiment-v1','id':case['id']+'-'+case['control'],
        'title':'Orthogonal inputs: '+case['id']+'-'+case['control'],'description':p['claim'],'question':p['question'],
        'board':{'side':case['side'],'body_signs':p['board']['body_signs'],'background':p['board']['background']},
        'components':[{'name':'complete_preparation','recipe':'Patch','at':[0,0,0],
            'params':{'kind':'orthogonal-complete-preparation','cells':[[*a,*v] for a,v in sorted(prepared.initial.cells.items())]}}],
        'steps':steps,'controls':case,'seed':None,'view':{'position':[c,c,c],'channel':2},
        'provenance':{'initial_only':True,'component_manifest':plain(prepared.manifest),
                      'protocol_canonical_sha256':base.digest(p)},
        'budget':{'max_frames':steps+1,'max_cells':p['budget']['max_cells_per_record'],
                  'max_bytes':67108864,'max_seconds':p['budget']['max_seconds_per_record']}}


@lru_cache(maxsize=4096)
def template(axis_name, origin):
    axis,primary,companion=AXES[axis_name]
    cells={}
    for i in range(-1,5):
        xyz=list(origin);xyz[axis]+=i
        for g,r in ((primary,0),(companion,4)):cells[(*xyz,g)]=Channel(0,0,r)
    for a,v in packet(axis,primary,companion,True,tensor()).cells:
        cells[tuple(a[j]+origin[j] for j in range(3))+(a[3],)]=Channel(*v)
    return {a:v for a,v in cells.items() if v!=Channel(0,0,2)}


def matches(state, axis_name, origin):
    axis=AXES[axis_name][0]
    actual={a:v for a,v in state.cells.items() if all(origin[j]+(-1 if j==axis else -1)<=a[j]<=origin[j]+(4 if j==axis else 1) for j in range(3))}
    return actual==template(axis_name,tuple(origin))


def translate(state,axis,n):
    cells={}
    for a,v in state.cells.items():
        aa=list(a);aa[axis]=(aa[axis]+n)%state.cube.side;cells[tuple(aa)]=v
    return State(state.cube,state.background,cells)


def footprint_checks(case,p):
    states={mask:prepare({**case,'control':mask},p).initial for mask in p['family']['controls']}
    addresses=set().union(*(s.cells for s in states.values()));footprints=source_footprints(case);tests=[]
    for index,name in enumerate(('X','Y')):
        axis,primary,companion=AXES[name];origin=origins(case)[name];allowed=set(footprints[name])
        for other in ('0','1'):
            off=('0'+other) if index==0 else (other+'0');on=('1'+other) if index==0 else (other+'1')
            changed={a for a in addresses if states[off].at(a)!=states[on].at(a)}
            def pristine(a):
                same_row=all(a[j]==origin[j] for j in range(3) if j!=axis)
                r=0 if same_row and a[3]==primary else 4 if same_row and a[3]==companion else 2
                return Channel(0,0,r)
            tests.append({'source':name,'other_present':other,'changed_addresses':len(changed),
                'outside_equal':changed<=allowed,'absent_footprint_pristine':all(states[off].at(a)==pristine(a) for a in allowed)})
    return {'checks':tests,'passed':all(t['outside_equal'] and t['absent_footprint_pristine'] for t in tests)}


def observer_protocol(case,p):
    bp=json.loads(base.PROTOCOL.read_text());c=case['side']//2
    bp['board']={'side':case['side'],'body_signs':p['board']['body_signs'],'background':p['board']['background']}
    bp['steps']=p['steps'];bp['readouts']['eligible_hold_starts']=[]
    bp['geometry']={'clock_x':c,'clock_y':c,'clock_z':c,'packet_x':c-19,'row_y':c-1,'row_z':c,
                    'forward_outlet_x':c+8,'backward_outlet_x':c-8}
    return bp


def observe(case,p,prepared,states):
    if case['stage']=='isolated':
        return {'complete_translation':all(s==translate(states[0],AXES[case['axis']][0],t) for t,s in enumerate(states))}
    data=base.observe(observer_protocol(case,p),{'guide_target_channel':0},prepared,states)
    c=case['side']//2
    inputs={}
    for name,origin in origins(case).items():
        axis=AXES[name][0];gap=0 if name=='X' else case['gap']
        samples=[]
        for label,times in (('early',[gap+k for k in p['incoming']['early_offsets']]),
                            ('near',[19+gap+k for k in p['incoming']['near_origin_offsets']])):
            for t in times:
                at=list(origin);at[axis]+=t
                samples.append({'kind':label,'step':t,'origin':at,'match':matches(states[t],name,at)})
        inputs[name]=samples
    data['incoming']=inputs
    outlets={'X':(c+8,c-1,c),'Y':(c+1,c+8,c)}
    natural={'writer':27,'probe':27+case['gap']}
    outputs={}
    for epoch,T in natural.items():
        row=[]
        for name,origin in outlets.items():
            axis,primary,_=AXES[name];address=[*origin,primary]
            for latency in p['outputs']['latency_offsets']:
                t=T+latency;frames=[]
                for k in p['outputs']['carrier_offsets']:
                    at=list(origin);at[axis]+=k
                    frames.append({'step':t+k,'origin':at,'match':matches(states[t+k],name,at)})
                observed=[{key:e[key] for key in ('step','kind','ell')} for e in data['all_C']
                    if e['address']==address and t-3<=e['step']<=t+4]
                expected=[{'step':t+dt,'kind':kind,'ell':ell} for dt,kind,ell in p['outputs']['C_expected']]
                row.append({'port':name,'origin_step':t,'latency':latency,'carrier_states':frames,
                    'exact_carrier':all(f['match'] for f in frames),'C_events':observed,
                    'expected_C':expected,'exact_C':observed==expected})
        outputs[epoch]=row
    data['outputs']=outputs
    start,end=p['hold']['start'],p['hold']['through'];region=data['region_trace'][start:end+1];center=data['center_trace'][start:end+1]
    data['hold']={'complete_region_period4':all(region[k]==region[k+4] for k in range(len(region)-4)),
        'center_unit_counter_norm':all(v[0]*v[0]+v[1]*v[1]==1 for v in center),
        'other_counter_pairs_zero':all(not(v[0] or v[1]) for frame in region for j,v in enumerate(frame) if j!=2),
        'every_external_term_zero':all(not row['nonzero_external_terms'] for row in data['boundary_inputs'][start:end])}
    active=[a for a,v in states[0].cells.items() if v.a or v.b]
    data['initial_active_boundary_margin']=min((min(q,case['side']-1-q) for a in active for q in a[:3]),default=None)
    return data


def candidates(data,epoch):
    return [{'port':x['port'],'origin_step':x['origin_step'],'exact_C':x['exact_C']}
            for x in data['outputs'][epoch] if x['exact_carrier']]


def assess_case(case,p,states,data):
    if case['stage']=='isolated':return {'pristine_translation':data['complete_translation']}
    margin=data['initial_active_boundary_margin']
    union={(x['port'],x['origin_step']):x for epoch in ('writer','probe') for x in candidates(data,epoch)}
    return {'input_contracts':{name:all(x['match']==(case['control'][i]=='1') for x in data['incoming'][name]) for i,name in enumerate(('X','Y'))},
        'complete_hold':all(data['hold'].values()),'strict_initial_causal_margin':margin is None or margin>p['steps'],
        'no_active_boundary_contact':not data['active_boundary_hits'],
        'writer_candidates':candidates(data,'writer'),'probe_candidates':candidates(data,'probe'),
        'unique_carrier_candidates':[union[key] for key in sorted(union)],
        'natural_X':next(x for x in data['outputs']['writer'] if x['port']=='X' and x['latency']==0)['exact_carrier'],
        'natural_Y':next(x for x in data['outputs']['probe'] if x['port']=='Y' and x['latency']==0)['exact_carrier'],
        'natural_X_C':next(x for x in data['outputs']['writer'] if x['port']=='X' and x['latency']==0)['exact_C'],
        'natural_Y_C':next(x for x in data['outputs']['probe'] if x['port']=='Y' and x['latency']==0)['exact_C']}


def candidate_key(values):
    return [(x['port'],x['origin_step']) for x in values]


def assess_group(rows,p,preparation_check,calibration):
    by={r['case']['control']:r for r in rows};case=rows[0]['case']
    complete=len(rows)==4 and set(by)==set(p['family']['controls'])
    baseline=all(by['00']['states'][t]==by['00']['states'][t+4] for t in range(p['steps']-3))
    inputs=all(all(r['assessment']['input_contracts'].values()) for r in rows)
    safe=all(r['assessment']['strict_initial_causal_margin'] and r['assessment']['no_active_boundary_contact'] and
             r['experiment']['provenance']['full_rewind_equal'] for r in rows)
    null=not by['00']['assessment']['writer_candidates'] and not by['00']['assessment']['probe_candidates']
    common=complete and preparation_check['passed'] and baseline and inputs and safe and null
    assessments={m:r['assessment'] for m,r in by.items()};joint=assessments['11'];single=assessments['01']
    crossed=all(by[m]['assessment'][k] for m,keys in (('10',('natural_X','natural_X_C')),('01',('natural_Y','natural_Y_C')),
        ('11',('natural_X','natural_X_C','natural_Y','natural_Y_C'))) for k in keys)
    single_ok=all(assessments[m][k] for m,keys in (('10',('natural_X','natural_X_C')),('01',('natural_Y','natural_Y_C'))) for k in keys)
    both_native=calibration is not None and calibration['crossed_natural_calibration']
    jc=joint['probe_candidates'];pc=single['probe_candidates']
    one=case['gap']==0 and len(joint['unique_carrier_candidates'])==1 and joint['unique_carrier_candidates'][0]['exact_C']
    exclusive=case['clock_mode']=='on' and common and single_ok and both_native and one
    start,end=p['hold']['start'],p['hold']['through']
    hold=all(r['assessment']['complete_hold'] for r in rows)
    changed=all(by['11']['observations']['region_trace'][t]!=by['01']['observations']['region_trace'][t] for t in range(start,end+1))
    no_leak=not assessments['00']['probe_candidates'] and not assessments['10']['probe_candidates']
    differs=candidate_key(jc)!=candidate_key(pc)
    history=case['gap'] in p['hold']['applies_to_gaps'] and case['clock_mode']=='on' and common and hold and changed and no_leak and differs
    allC=all(x['exact_C'] for x in jc+pc)
    redirected=history and single['natural_Y'] and single['natural_Y_C'] and len(jc)==1 and jc[0]['port']=='X' and jc[0]['exact_C']
    category='no_exact_output' if not jc else 'one_registered_outlet' if len(jc)==1 else 'multiple_candidates'
    if any(not x['exact_C'] for x in jc):category='carrier_with_unmatched_C'
    if history:
        if not pc and jc:direction='enabled'
        elif pc and not jc:direction='suppressed'
        elif {x['port'] for x in pc}!={x['port'] for x in jc}:direction='changed_ports'
        else:direction='changed_latency_or_count'
    else:direction=None
    return {'geometry':{k:v for k,v in case.items() if k!='control'},'complete_control_group':complete,
        'preparation_equivalence':preparation_check,'null_period_divides4':baseline,'both_input_contracts':inputs,
        'safe_and_reversible':safe,'null_output_absent':null,'common_eligible':common,
        'crossed_natural_calibration':case['clock_mode']=='bare' and common and crossed,
        'calibration_geometry':calibration['geometry']['id'] if calibration else None,
        'independent_single_continuations':single_ok,'simultaneous_exclusivity':exclusive,
        'all_complete_holds':hold,'retained_region_differs':changed,'no_late_writer_only_carrier':no_leak,
        'history_discriminator':history,'history_carrier_C_discriminator':history and allC,
        'history_change':direction,'redirected_output_candidate':redirected,'joint_late_category':category,
        'cases':assessments,'clock_off_comparison_only':case['clock_mode']=='counter_off','claim_limit':p['claim']}


def run(output,protocol_path=PROTOCOL,previous_attempt=None):
    raw_protocol=Path(protocol_path).read_bytes();p=json.loads(raw_protocol)
    output=Path(output);output.mkdir(parents=True,exist_ok=False);(output/'records').mkdir();(output/'protocol.json').write_bytes(raw_protocol)
    source_files=[Path(__file__),Path(protocol_path),Path(previous.__file__),previous.PROTOCOL,
        Path(base.__file__),base.PROTOCOL,HERE/'orthogonal_preflight.py',HERE/'provenance.py',HERE/'__init__.py',
        ROOT/'research/staged_blocks/orbit.py',ROOT/'research/staged_blocks/__init__.py',
        ROOT/'research/experiments/run.py',ROOT/'research/experiments/__init__.py',
        *sorted((ROOT/'universe24').rglob('*.py')),*sorted((ROOT/'research/components').glob('*.py')),
        *sorted((ROOT/'research/presenter').glob('*.py'))]
    source_paths={str(x.relative_to(ROOT)) for x in source_files}
    freeze_sources(output/'source_provenance',source_paths,metadata={'protocol_sha256':hashlib.sha256(raw_protocol).hexdigest(),
        'family':p['family'],'board':p['board'],'budget':p['budget'],'seed':None})
    geo=list(geometries(p));checks={g['id']:footprint_checks(g,p) for g in geo}
    if not all(x['passed'] for x in checks.values()):raise ValueError('Initial footprint equivalence failed')
    clock_checks=[]
    for g in geo:
        if g['clock_mode']!='on' or g['side']!=p['family']['primary_side']:continue
        c=g['side']//2
        for mask in p['family']['controls']:
            on=prepare({**g,'control':mask},p).initial;off=prepare({**g,'control':mask,'clock_mode':'counter_off'},p).initial
            addresses=on.cells.keys()|off.cells.keys();changed={a for a in addresses if on.at(a)!=off.at(a)}
            clock_checks.append({'id':g['id']+'-'+mask,'passed':changed<={(c,c,c,2)} and on.at((c,c,c,2)).r==off.at((c,c,c,2)).r})
    if not all(x['passed'] for x in clock_checks):raise ValueError('Counter-only clock mask failed')
    base.write_json(output/'preparation_equivalence.json',{'groups':checks,'clock_masks':clock_checks,'trajectories':0})
    isolated=[{'id':f'orthogonal-isolated-{x["axis"]}-gap{x["gap"]}','side':p['pristine_isolated']['side'],
        'axis':x['axis'],'gap':x['gap'],'phase':0,'clock_mode':'bare','stage':'isolated','control':'10' if x['axis']=='X' else '01'} for x in p['pristine_isolated']['cases']]
    batches=[[c] for c in isolated]+[[{**g,'control':m} for m in p['family']['controls']] for g in geo]
    all_cases=[c for b in batches for c in b]
    if len(all_cases)!=p['budget']['registered_cases']:raise ValueError('Registered case count differs')
    base.write_json(output/'registration.json',{'format':'universe24-orthogonal-two-outlet-registration-v1',
        'protocol_sha256':hashlib.sha256(raw_protocol).hexdigest(),'cases':all_cases,'seed':None,'registered_before_capture':True})
    started_cpu,started_wall=time.process_time(),time.monotonic();ledger=[];groups=[];examples=[];calibrations={};reason=None
    failures=[];overlap=[]
    previous_attempt=Path(previous_attempt) if previous_attempt is not None else None
    if previous_attempt is not None:
        receipt=previous_attempt/'interruption_receipt.json'
        if not receipt.exists():raise ValueError('A preserved interruption receipt is required for retry')
        (output/'previous_interruption_receipt.json').write_bytes(receipt.read_bytes())

    def progress(status,case=None):
        row={'status':status,'case':case,'completed_cases':len(ledger),'registered_cases':len(all_cases),
             'cpu_seconds':time.process_time()-started_cpu,'wall_seconds':time.monotonic()-started_wall}
        base.write_json(output/'progress.json',row)
        with (output/'progress.jsonl').open('a') as stream:stream.write(base.canonical(row)+'\n')
        base.write_json(output/'completed_records_checkpoint.json',ledger)

    def save_record(row,group):
        wrapper={k:v for k,v in row.items() if k!='states'}
        wrapper.update({'format':'universe24-orthogonal-two-outlet-record-v1','group_assessment':group,
                        'protocol_sha256':hashlib.sha256(raw_protocol).hexdigest()})
        raw=base.canonical(wrapper).encode();compressed=gzip.compress(raw,mtime=0)
        relative='records/'+row['spec']['id']+'.json.gz';(output/relative).write_bytes(compressed)
        return {'id':row['spec']['id'],'case':row['case'],'record':relative,
            'record_sha256':hashlib.sha256(raw).hexdigest(),'record_gzip_sha256':hashlib.sha256(compressed).hexdigest(),
            'initial_state_sha256':state_sha256(row['states'][0]),'final_state_sha256':state_sha256(row['states'][-1]),
            'frames':len(row['states']),'full_state_inverse':row['experiment']['provenance']['full_rewind_equal'],'assessment':row['assessment']}

    for batch in batches:
        rows=[]
        for case in batch:
            if time.process_time()-started_cpu>=p['budget']['max_cpu_seconds'] or time.monotonic()-started_wall>=p['budget']['max_wall_seconds']:
                reason='time_budget';break
            if sum(f.stat().st_size for f in output.rglob('*') if f.is_file())>=p['budget']['max_recorded_bytes']:
                reason='data_budget';break
            spec=case_spec(case,p);prepared=assemble(spec)
            base.write_json(output/'inflight_spec.json',spec);progress('capture_started',spec['id'])
            try:
                record=run_experiment(spec)
                (output/'pending_native_capture.json.gz').write_bytes(gzip.compress(base.canonical(record).encode(),mtime=0))
                progress('capture_completed_observation_pending',spec['id'])
                states=recorded_states(record['experiment']);obs=observe(case,p,prepared,states)
                row={'case':case,'spec':spec,'assembly':record['assembly'],'experiment':record['experiment'],
                    'states':states,'observations':obs,'assessment':assess_case(case,p,states,obs)}
                if previous_attempt is not None:
                    prior=previous_attempt/'records'/(spec['id']+'.json.gz')
                    if prior.exists():
                        old=json.loads(gzip.decompress(prior.read_bytes()))
                        check={'id':spec['id'],'full_frames_equal':old['experiment']['frames']==row['experiment']['frames'],
                               'spec_equal':old['spec']==spec,'assessment_equal':old['assessment']==row['assessment']}
                        overlap.append(check);base.write_json(output/'retry_overlap.json',overlap)
                        if not all(v for k,v in check.items() if k!='id'):raise ValueError('Retry overlap differs from interrupted evidence')
                rows.append(row);ledger.append(save_record(row,None))
                (output/'pending_native_capture.json.gz').unlink()
                progress('record_saved',spec['id'])
            except Exception as exc:
                reason='record_failure'
                failures.append({'case':case,'id':spec['id'],'exception_type':type(exc).__name__,'message':str(exc),
                    'cpu_seconds':time.process_time()-started_cpu,'wall_seconds':time.monotonic()-started_wall})
                base.write_json(output/'failures.json',failures);progress('record_failed',spec['id']);break
            rc=row['case']
            if rc['side']==p['family']['primary_side'] and ((rc['clock_mode']=='on' and rc['phase']==3) or
               (rc['clock_mode']=='bare' and rc['stage']=='crossed' and rc['gap']==0)):examples.append(row['experiment'])
        case=batch[0]
        group=assess_group(rows,p,checks[case['id']],calibrations.get((case['side'],case['gap']))) if len(rows)==4 else None
        if group:
            groups.append(group)
            if case['clock_mode']=='bare':calibrations[(case['side'],case['gap'])]=group
            for index,row in enumerate(rows):ledger[-len(rows)+index]=save_record(row,group)
        progress('group_completed' if group else 'single_or_incomplete_group',case['id'])
        print(base.canonical({'completed':len(ledger),'registered':len(all_cases),'case':case['id'],
            'exclusive':group['simultaneous_exclusivity'] if group else None,
            'history':group['history_carrier_C_discriminator'] if group else None,'stop_reason':reason}),flush=True)
        if reason is not None:break
    verification=verify_sources(output/'source_provenance');base.write_json(output/'source_verification.json',verification)
    if not verification['archive_verified'] or not verification['live_sources_unchanged']:raise RuntimeError('Source identity changed')
    result={'format':'universe24-orthogonal-two-outlet-result-v1','status':'completed' if reason is None else ('inconclusive' if reason=='record_failure' else 'budget_stopped'),
        'stop_reason':reason,'failures':failures,'retry_overlap':overlap,'registered_cases':len(all_cases),'completed_cases':len(ledger),'not_run_cases':all_cases[len(ledger):],
        'cases':ledger,'groups':groups,'all_full_state_inverses':all(x['full_state_inverse'] for x in ledger),
        'isolated_translation_passes':sum(x['assessment'].get('pristine_translation',False) for x in ledger),
        'crossed_calibrations':sum(g['crossed_natural_calibration'] for g in groups),
        'simultaneous_exclusivity_groups':sum(g['simultaneous_exclusivity'] for g in groups),
        'history_discriminator_groups':sum(g['history_discriminator'] for g in groups),
        'history_carrier_C_groups':sum(g['history_carrier_C_discriminator'] for g in groups),
        'redirected_output_groups':sum(g['redirected_output_candidate'] for g in groups),
        'cpu_seconds':time.process_time()-started_cpu,'wall_seconds':time.monotonic()-started_wall,
        'source_hashes_unchanged':True,'claim':p['claim']}
    base.write_json(output/'result.json',result)
    selections=[]
    for i in range(0,len(examples),2):
        subset=examples[i:i+2];name=f'experiments-{i//2+1:03d}.json'
        (output/name).write_text(base.canonical(bundle(subset,title='The Presenter: orthogonal inputs and two outlets'))+'\n')
        selections.append({'bundle':name,'ids':[e['id'] for e in subset]})
    base.write_json(output/'presenter_selection.json',{'complete_experiments':len(examples),'pages':selections})
    receipt={'bytes':sum(f.stat().st_size for f in output.rglob('*') if f.is_file()),
        'cpu_overrun':max(0,result['cpu_seconds']-p['budget']['max_cpu_seconds']),
        'wall_overrun':max(0,result['wall_seconds']-p['budget']['max_wall_seconds'])}
    receipt['byte_overrun']=max(0,receipt['bytes']-p['budget']['max_recorded_bytes']);base.write_json(output/'budget_receipt.json',receipt)
    print(base.canonical({k:result[k] for k in ('completed_cases','simultaneous_exclusivity_groups','history_discriminator_groups','redirected_output_groups','cpu_seconds')}),flush=True)
    return result


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True,type=Path)
    parser.add_argument('--previous-attempt',type=Path)
    args=parser.parse_args(argv);run(args.output,previous_attempt=args.previous_attempt)


if __name__=='__main__':main()
