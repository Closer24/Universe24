"""Frozen WRITE-to-PROBE study using initial data and unchanged Rule3 only."""
from __future__ import annotations

import argparse
from copy import deepcopy
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import platform
import subprocess
import time

from research.experiments.run import assemble, recorded_states, run_experiment
from research.presenter.export import bundle, state_sha256
from research.staged_blocks import interactions as base
from research.clock_selection.provenance import freeze_sources, verify_sources
from universe24 import State

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL = HERE / 'protocol_v1.json'


def geometries(p):
    f = p['family']
    for side, r, phase, delay, gap in itertools.product(p['board']['sides'], f['clock_remainders'],
            f['clock_phases'], f['writer_delays'], f['gaps']):
        yield {'id': f'write-probe-L{side}-r{r}-p{phase}-d{delay}-gap{gap}',
               'side': side, 'clock_remainder': r, 'phase': phase, 'writer_delay': delay,
               'gap': gap, 'stage': 'encounter', 'guide_target_channel': 0,
               'compensation_direction': None}


def observer_protocol(case, p):
    bp = json.loads(base.PROTOCOL.read_text())
    c, side = case['side']//2, case['side']
    bp['board'] = {'side': side, 'background': p['board']['background'], 'body_signs': p['board']['body_signs']}
    bp['steps'] = p['pristine']['steps'] if case['stage'] == 'pristine' else p['steps']
    bp['geometry'] = {'row_y': c, 'row_z': c, 'packet_x': c-16-case['writer_delay'],
                      'clock_x': c, 'clock_y': c+1, 'clock_z': c,
                      'forward_outlet_x': c+8, 'backward_outlet_x': c-8}
    bp['readouts']['eligible_hold_starts'] = []
    return bp


def case_spec(case, p):
    bp = observer_protocol(case, p)
    control = case['control']
    # The historical constructor's second control bit removes the clock;
    # here the clock is always present and the bits refer to writer/probe.
    old_case = {**case, 'control': control[0]+'1'}
    spec = base.case_spec(old_case, bp)
    c, side = case['side']//2, case['side']
    writer_x = c-16-case['writer_delay']
    probe_x = writer_x-case['gap']
    params = spec['components'][0]['params']
    if case['stage'] == 'pristine':
        params['cells'] = [[x,c,c,g,0,0,r] for x in range(side)
                           if x not in range(writer_x, writer_x+4)
                           for g,r in ((0,0),(14,4))]
        params['sources'] = {}
    params['cells'] = [row for row in params['cells']
                       if not (row[1:3] == [c,c] and row[3] in (0,14) and probe_x <= row[0] < probe_x+4)]
    params['sockets'] += [{'name': f'probe-{x}', 'addresses': [[x,c,c,g] for g in (0,14)],
                          'allowed_kinds': ['signal-source']} for x in range(probe_x,probe_x+4)]
    spec['components'][1]['name'] = 'writer'
    spec['components'].append({'name': 'probe', 'recipe': 'GuidedPacketSource',
                              'at': [probe_x,c,c], 'params': {'present': control[1]=='1'}})
    spec['id'] = case['id']+'-'+control
    spec['title'] = 'Clock-written conditional probe: '+spec['id']
    spec['question'] = p['question']
    spec['description'] = p['claim']
    spec['controls'] = deepcopy(case)
    spec['provenance'] = {'initial_only': True, 'protocol_sha256': base.digest(p),
                          'counter_only_masks': ['writer','probe'], 'clock_always_present': case['stage']!='pristine'}
    spec['budget'] = {'max_frames': spec['steps']+1, 'max_cells': p['budget']['max_cells_per_record'],
                      'max_bytes': 67108864, 'max_seconds': p['budget']['max_seconds_per_record']}
    return spec


def translated(state, displacement):
    return State(state.cube, state.background,
                 {((a[0]+displacement)%state.cube.side,*a[1:]):v for a,v in state.cells.items()})


def observe(case, p, prepared, states):
    if case['stage'] == 'pristine':
        return {'complete_translation': all(s == translated(states[0],t) for t,s in enumerate(states))}
    data = base.observe(observer_protocol(case,p),case,prepared,states)
    c = case['side']//2
    probe_x = c-16-case['writer_delay']-case['gap']
    data['incoming'] = [{'step': case['gap']+k,
                         'origin_x': probe_x+case['gap']+k,
                         'match': base.packet_matches(states[case['gap']+k],probe_x+case['gap']+k,c,c,1)}
                        for k in p['incoming']['offsets']]
    T = 24+case['writer_delay']+case['gap']
    data['registered_output'] = [{'step': T+k, 'origin_x':c+8+k,
                                  'match':base.packet_matches(states[T+k],c+8+k,c,c,1)}
                                 for k in p['output']['offsets']]
    data['registered_C_window'] = [T-3,T+4]
    data['registered_output_C'] = [{k:e[k] for k in ('step','kind','ell')} for e in data['all_C']
                                  if e['address']==[c+8,c,c,0] and T-3 <= e['step'] <= T+4]
    data['expected_output_C'] = [{'step':T+dt,'kind':kind,'ell':ell} for dt,kind,ell in p['output']['C_expected']]
    active = [a for a,v in states[0].cells.items() if v.a or v.b]
    data['initial_active_boundary_margin'] = min(min(q,case['side']-1-q) for a in active for q in a[:3])
    start,end = p['hold']['start'],p['hold']['through']
    region = data['region_trace'][start:end+1]
    center = data['center_trace'][start:end+1]
    h = data['center_address'][3]
    terms = data['center_inputs'][start:end]
    data['hold'] = {'start':start,'through':end,
        'complete_region_period4': all(region[j]==region[j+4] for j in range(len(region)-4)),
        'center_unit_counter_norm': all(v[0]*v[0]+v[1]*v[1]==1 for v in center),
        'other_counter_pairs_zero': all(not(v[0] or v[1]) for frame in region for j,v in enumerate(frame) if j!=h),
        'every_external_term_zero': all(not row['nonzero_external_terms'] for row in data['boundary_inputs'][start:end]),
        'center_u_and_ell_zero': all(row['u']==0 and data['center_trace'][start+j+1][1]+center[j][0]==0
                                     for j,row in enumerate(terms))}
    return data


def assess_case(case,p,states,data):
    if case['stage']=='pristine':
        return {'pristine_translation':data['complete_translation']}
    exact = all(row['match'] for row in data['registered_output'])
    raw = data['registered_output_C']==data['expected_output_C']
    return {'incoming_contract': all(row['match']==(case['control'][1]=='1') for row in data['incoming']),
            'complete_hold': all(v for k,v in data['hold'].items() if k not in ('start','through')),
            'exact_output_carrier':exact,'exact_output_C_signature':raw,'carrier_plus_C':exact and raw,
            'strict_initial_causal_margin':data['initial_active_boundary_margin']>p['steps'],
            'no_active_boundary_contact':not data['active_boundary_hits']}


def assess_group(rows,p):
    by = {r['case']['control']:r for r in rows}
    case=rows[0]['case']; start,end=p['hold']['start'],p['hold']['through']
    addresses=set().union(*(r['states'][0].cells for r in rows))
    matched=all(len({r['states'][0].at(a).r for r in rows})==1 for a in addresses)
    baseline=all(by['00']['states'][t]==by['00']['states'][t+4] for t in range(p['steps']-3))
    checks=all(r['assessment'][key] for r in rows for key in ('incoming_contract','complete_hold',
               'strict_initial_causal_margin','no_active_boundary_contact'))
    changed=all(by['11']['observations']['region_trace'][t]!=by['01']['observations']['region_trace'][t]
                for t in range(start,end+1))
    no_writer_leak=all(not by[m]['assessment']['exact_output_carrier'] for m in ('00','10'))
    carrier_diff=by['11']['assessment']['exact_output_carrier']!=by['01']['assessment']['exact_output_carrier']
    combined_diff=by['11']['assessment']['carrier_plus_C']!=by['01']['assessment']['carrier_plus_C']
    raw_diff=by['11']['assessment']['exact_output_C_signature']!=by['01']['assessment']['exact_output_C_signature']
    gate=matched and baseline and checks and changed and no_writer_leak and carrier_diff
    pred_joint=case['gap']%4==2
    pred_probe=(case['phase']+case['writer_delay']+case['gap'])%4==2
    return {'geometry':{k:v for k,v in case.items() if k!='control'},'matched_initial_remainders':matched,
            'clock_only_complete_period4':baseline,'all_input_hold_boundary_contracts':checks,
            'retained_full_region_differs':changed,'writer_only_and_null_output_absent':no_writer_leak,
            'carrier_discriminator':gate,'carrier_and_C_discriminator':gate and combined_diff,
            'raw_C_discriminator':gate and raw_diff,
            'direction':'enabled' if by['11']['assessment']['exact_output_carrier'] else 'suppressed',
            'predicted_joint_carrier':pred_joint,'predicted_probe_only_carrier':pred_probe,
            'carrier_prediction_matches':by['11']['assessment']['exact_output_carrier']==pred_joint and
                                         by['01']['assessment']['exact_output_carrier']==pred_probe,
            'cases':{m:r['assessment'] for m,r in by.items()},
            'full_final_hashes':{m:state_sha256(r['states'][-1]) for m,r in by.items()},
            'claim_limit':p['claim']}


def run(output,protocol_path=PROTOCOL):
    raw_protocol=Path(protocol_path).read_bytes(); p=json.loads(raw_protocol)
    output=Path(output);output.mkdir(parents=True,exist_ok=False);(output/'records').mkdir()
    (output/'protocol.json').write_bytes(raw_protocol)
    (output/'executed_search.py').write_bytes(Path(__file__).read_bytes())
    sources=[Path(__file__),Path(protocol_path),Path(base.__file__),base.PROTOCOL,
             HERE/'provenance.py',HERE/'__init__.py',
             *sorted((ROOT/'universe24').rglob('*.py')),*sorted((ROOT/'research/components').glob('*.py')),
             ROOT/'research/experiments/__init__.py',ROOT/'research/experiments/run.py',
             ROOT/'research/staged_blocks/__init__.py',*sorted((ROOT/'research/presenter').glob('*.py'))]
    hashes={str(s.relative_to(ROOT)):hashlib.sha256(s.read_bytes()).hexdigest() for s in sources}
    freeze_sources(output/'source_provenance',hashes.keys(),metadata={'protocol_sha256':hashlib.sha256(raw_protocol).hexdigest(),
                   'seed':None,'board':p['board'],'family':p['family'],'budget':p['budget']})
    groups=list(geometries(p))
    pristine=[{'id':f'write-probe-pristine-L{p["board"]["sides"][0]}-gap{gap}',
               'side':p['board']['sides'][0],'clock_remainder':0,'phase':0,'writer_delay':1,
               'gap':gap,'stage':'pristine','guide_target_channel':0,'compensation_direction':None,'control':'11'}
              for gap in p['pristine']['gaps']]
    batches=[[c] for c in pristine]+[[{**g,'control':m} for m in p['family']['controls']] for g in groups]
    cases=[c for batch in batches for c in batch]
    reg={'format':'universe24-clock-selection-registration-v1','base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
         'protocol_sha256':hashlib.sha256(raw_protocol).hexdigest(),'protocol_canonical_sha256':base.digest(p),
         'source_sha256':hashes,'registered_before_capture':True,'cases':cases,'seed':None,
         'python':platform.python_version(),'platform':platform.platform()}
    base.write_json(output/'registration.json',reg)
    started_cpu,started_wall=time.process_time(),time.monotonic()
    ledger,assessments,examples=[],[],[];reason=None
    for batch in batches:
        if time.process_time()-started_cpu>=p['budget']['max_cpu_seconds'] or time.monotonic()-started_wall>=p['budget']['max_wall_seconds']:
            reason='time_budget';break
        if sum(f.stat().st_size for f in output.rglob('*') if f.is_file())>=p['budget']['max_recorded_bytes']:
            reason='data_budget';break
        rows=[]
        for case in batch:
            spec=case_spec(case,p);prepared=assemble(spec);record=run_experiment(spec)
            states=recorded_states(record['experiment']);obs=observe(case,p,prepared,states)
            row={'case':case,'spec':spec,'assembly':record['assembly'],'experiment':record['experiment'],
                 'states':states,'observations':obs,'assessment':assess_case(case,p,states,obs)}
            rows.append(row)
        group=assess_group(rows,p) if len(rows)==4 else None
        for row in rows:
            wrapper={k:v for k,v in row.items() if k!='states'}
            wrapper.update({'format':'universe24-clock-selection-record-v1','protocol_sha256':reg['protocol_sha256'],'group_assessment':group})
            raw=base.canonical(wrapper).encode(); compressed=gzip.compress(raw,mtime=0)
            relative='records/'+row['spec']['id']+'.json.gz';(output/relative).write_bytes(compressed)
            ledger.append({'id':row['spec']['id'],'case':row['case'],'record':relative,
                'record_sha256':hashlib.sha256(raw).hexdigest(),'record_gzip_sha256':hashlib.sha256(compressed).hexdigest(),
                'initial_state_sha256':state_sha256(row['states'][0]),'final_state_sha256':state_sha256(row['states'][-1]),
                'frames':len(row['states']),'transitions':len(row['states'])-1,
                'full_state_inverse':row['experiment']['provenance']['full_rewind_equal'],'assessment':row['assessment']})
            if row['case']['stage']=='encounter' and (row['case']['gap'],row['case']['phase']) in ((34,0),(32,1)):
                examples.append(row['experiment'])
        if group:assessments.append(group)
        print(base.canonical({'completed':len(ledger),'registered':len(cases),'case':batch[0]['id'],
                            'gate':group['carrier_discriminator'] if group else None}),flush=True)
    unchanged=all(hashlib.sha256((ROOT/s).read_bytes()).hexdigest()==sha for s,sha in hashes.items())
    if not unchanged:raise RuntimeError('Execution source changed during capture')
    base.write_json(output/'source_verification.json',verify_sources(output/'source_provenance'))
    result={'format':'universe24-clock-selection-result-v1','status':'completed' if reason is None else 'budget_stopped',
            'stop_reason':reason,'registered_cases':len(cases),'completed_cases':len(ledger),'cases':ledger,'groups':assessments,
            'not_run_cases':cases[len(ledger):],'all_full_state_inverses':all(r['full_state_inverse'] for r in ledger),
            'pristine_passes':sum(r['assessment'].get('pristine_translation',False) for r in ledger),
            'carrier_discriminator_groups':sum(g['carrier_discriminator'] for g in assessments),
            'carrier_and_C_discriminator_groups':sum(g['carrier_and_C_discriminator'] for g in assessments),
            'raw_C_discriminator_groups':sum(g['raw_C_discriminator'] for g in assessments),
            'predictions_matched':sum(g['carrier_prediction_matches'] for g in assessments),
            'cpu_seconds':time.process_time()-started_cpu,'wall_seconds':time.monotonic()-started_wall,
            'source_hashes_unchanged':unchanged,'claim':p['claim']}
    base.write_json(output/'result.json',result)
    (output/'experiments.json').write_text(base.canonical(bundle(examples,title='The Presenter: clock-written conditional probe'))+'\n')
    receipt={'bytes':sum(f.stat().st_size for f in output.rglob('*') if f.is_file()),
             'cpu_overrun':max(0,result['cpu_seconds']-p['budget']['max_cpu_seconds']),
             'wall_overrun':max(0,result['wall_seconds']-p['budget']['max_wall_seconds'])}
    receipt['byte_overrun']=max(0,receipt['bytes']-p['budget']['max_recorded_bytes'])
    base.write_json(output/'budget_receipt.json',receipt)
    print(base.canonical({k:result[k] for k in ('completed_cases','carrier_discriminator_groups',
        'raw_C_discriminator_groups','predictions_matched','cpu_seconds')}),flush=True)
    return result


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--protocol',type=Path,default=PROTOCOL)
    args=ap.parse_args(argv);return run(args.output,args.protocol)


if __name__=='__main__':main()
