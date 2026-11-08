"""Registered route-to-clock composition using only initial data and Rule3."""
from __future__ import annotations
import argparse
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import shutil
import signal
import subprocess
import time
from universe24 import Coupling
from universe24.core.group_2o import DIRECTIONS
from universe24.observation.clicks import clicks
from research.staged_blocks.orbit import ShieldedOrbit
from research.experiments.run import assemble, run_experiment, recorded_states
from research.presenter.export import bundle

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
PROTOCOL=HERE/'route_clock_protocol.json';CP=Coupling((1,1,1))
PAIRS={'O':(4,0),'N':(2,2),'R':(0,4)}
PHASES=((0,1),(1,0),(0,-1),(-1,0))
class BudgetStop(RuntimeError):pass

def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'))
def write_json(path,value):
    path=Path(path)
    if path.exists():raise FileExistsError(path)
    temporary=path.with_name(path.name+'.partial')
    with temporary.open('x') as handle:handle.write(canonical(value)+'\n')
    temporary.replace(path)
def write_compressed(path,value):
    path=Path(path)
    if path.exists():raise FileExistsError(path)
    data=gzip.compress(canonical(value).encode(),mtime=0)
    temporary=path.with_name(path.name+'.partial');temporary.write_bytes(data);temporary.replace(path)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sides(case):return (case['isolated_direction'],) if case['isolated_direction'] else (-1,1)
def pattern(case,direction):return case['patterns'][0 if direction==-1 else 1]
def center(case,direction):
    c=case['side']//2
    return (c+8*direction,c+1,c)
def clock_cells(phase,enabled=True):
    cells=dict(ShieldedOrbit(channel=2,a=0,b=1,r=0,phase=phase,present=enabled,halo_remainders=(2,)*6).cells)
    cells[(0,-1,0,14)]=(0,0,0)
    return {a:tuple(v) for a,v in cells.items()}

def planned_pairs(p):
    for stage in ('bare','primary','clock_off'):
        for side in p['family']['sides']:
            phases=p['family']['clock_phases'] if stage=='primary' else [1]
            configs=[(0,list(patterns)) for patterns in p['family']['mixed_swaps']]
            if stage=='primary':configs += [(direction,[pat,pat]) for direction,pat in p['family']['isolated_configurations']]
            for phase,(isolated,patterns) in itertools.product(phases,configs):
                identity=f'route-clock-L{side}-{stage}-p{phase}-d{isolated}-'+''.join(patterns)
                yield [{'id':identity,'stage':stage,'side':side,'phase':phase,'isolated_direction':isolated,
                        'patterns':patterns,'source_present':present} for present in p['family']['source_controls']]

def spec(case,p):
    c=case['side']//2
    components=[{'name':'source','recipe':'SignalSource','at':[c,c,c],
                 'params':{'a':0,'b':1,'present':case['source_present']}}]
    for direction in sides(case):
        label='L' if direction==-1 else 'R'
        components.append({'name':label,'recipe':'PairedArm','at':[c,c,c],
                           'params':{'direction':direction,'length':8,
                                     'gate_pairs':[list(PAIRS[x]) for x in pattern(case,direction)]}})
        if case['stage']!='bare':
            cells=clock_cells(case['phase'],case['stage']=='primary')
            components.append({'name':label+'_clock','recipe':'Patch','at':list(center(case,direction)),
                'params':{'kind':'prepared-route-clock','cells':[[*a,*v] for a,v in sorted(cells.items())],
                          'ports':{'center':[[0,0,0,2]],'region':[list(a) for a in sorted(cells)]},
                          'sources':{'clock':[[0,0,0,2]]}}})
    view='L.outlet' if -1 in sides(case) else 'R.outlet'
    if case['stage']!='bare':view='L_clock.center' if -1 in sides(case) else 'R_clock.center'
    return {'format':'universe24-assembly-experiment-v1','id':case['id']+'-s'+str(int(case['source_present'])),
        'title':'Route and clock: '+case['id']+' source '+('on' if case['source_present'] else 'off'),
        'description':'Initial route and clock composition; all memory and click observations are passive.',
        'question':p['question'],'board':{**p['board'],'side':case['side']},'steps':p['steps'],'seed':None,
        'components':components,'detectors':[],'view':{'port':view},'controls':case,
        'provenance':{'initial_only':True,'protocol_sha256':hashlib.sha256(PROTOCOL.read_bytes()).hexdigest()},
        'budget':{'max_frames':p['steps']+1,'max_cells':p['budget']['max_cumulative_native_rows_per_record'],
                  'max_seconds':p['budget']['max_seconds_per_record'],'max_bytes':p['budget']['max_recorded_bytes']}}

def preflight(p):
    assert CP.ports[3][2]==0 and CP.weights[3][2]==1
    checks=[]
    for pair in planned_pairs(p):
        boards=[assemble(spec(case,p)) for case in pair]
        first,second=(board.initial for board in boards)
        addresses=set(first.cells)|set(second.cells)
        assert all(first.at(a).r==second.at(a).r for a in addresses)
        c=pair[0]['side']//2;source={(*[c]*3,g) for g in (0,14)}
        assert all(a in source or first.at(a)==second.at(a) for a in addresses)
        active=[a for a,v in second.cells.items() if v.a or v.b]
        margin=min(min(v,pair[0]['side']-1-v) for a in active for v in a[:3])
        assert margin>p['steps']
        case=pair[0]
        if case['stage']!='bare':
            regions=[]
            for direction in sides(case):
                o=center(case,direction);expected=clock_cells(case['phase'],case['stage']=='primary')
                assert all(tuple(first.at((*add(o,a[:3]),a[3])))==v for a,v in expected.items())
                assert tuple(first.at((o[0],o[1]-1,o[2],0)))==(0,0,4)
                assert tuple(first.at((o[0],o[1]-1,o[2],14)))==(0,0,0)
                regions.append({add(o,a[:3]) for a in expected})
            if len(regions)==2:assert not(regions[0]&regions[1])
        if case['stage']=='clock_off':
            for present in (False,True):
                x={**case,'phase':1,'source_present':present};y={**x,'phase':2}
                assert assemble(spec(x,p)).initial==assemble(spec(y,p)).initial
                on={**x,'stage':'primary'};a=assemble(spec(on,p)).initial;b=assemble(spec(x,p)).initial
                assert all(a.at(q).r==b.at(q).r for q in set(a.cells)|set(b.cells))
        checks.append({'id':case['id'],'source_remainders_match':True,'declared_counter_difference_only':True,
                       'complete_clock_contacts_compatible':True,'initial_active_boundary_margin':margin})
    assert len(checks)*2==p['family']['registered_cases']
    return {'status':'passed_initial_assembly_only','new_trajectories':0,'prepared_cases':len(checks)*2,'pairs':checks,
            'protocol_sha256':hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),'producer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

def six_terms(state,address):
    result=[]
    for direction in range(6):
        donor=state.cube.adjacent(address,direction,CP.ports[direction][address[3]])
        result.append({'source':list(donor),'term':CP.weights[direction][address[3]]*state.at(donor).b})
    return result

def external_terms(state,nodes):
    result=[]
    for a,v in state.cells.items():
        if not v.b or a[:3] in nodes:continue
        for direction in range(6):
            destination=state.cube.adjacent(a,direction,CP.ports[direction][a[3]])
            if destination[:3] in nodes:result.append({'source':list(a),'target':list(destination),'term':CP.weights[direction][a[3]]*v.b})
    return result

def observe(case,states,p,deadline_cpu=None):
    c=case['side']//2;start,end=p['readouts']['hold_states'];routes={};clocks={}
    events=[];event_map={};counts={str(k):0 for k in range(3)}
    for t,(old,new) in enumerate(zip(states,states[1:]),1):
        if deadline_cpu is not None and time.process_time()>deadline_cpu:raise BudgetStop('Passive observation CPU limit exceeded; native checkpoint retained')
        for event in clicks(old,new,t):
            terms=six_terms(old,event.address)
            row={'step':t,'address':list(event.address),'kind':event.kind,'ell':event.quotient,'six_terms':terms,'u':sum(x['term'] for x in terms)}
            events.append(row);event_map[t,event.address]=row;counts[str(event.kind)]+=1
    for direction in sides(case):
        if deadline_cpu is not None and time.process_time()>deadline_cpu:raise BudgetStop('Passive observation CPU limit exceeded; native checkpoint retained')
        key=str(direction)
        routes[key]={name:[[list(state.at((c+distance*direction,c,c,g))) for g in range(48)] for state in states]
                     for name,distance in (('upstream',6),('outlet',8))}
        if case['stage']=='bare':continue
        o=center(case,direction);local=sorted(clock_cells(0));addresses=[(*add(o,a[:3]),a[3]) for a in local];nodes={a[:3] for a in addresses}
        trace=[[list(state.at(a)) for a in addresses] for state in states];center_address=(*o,2)
        center_trace=[list(state.at(center_address)) for state in states]
        inputs=[];boundary=[]
        for t,(old,new) in enumerate(zip(states,states[1:]),1):
            terms=six_terms(old,center_address)
            inputs.append({'update':t,'six_terms':terms,'u':sum(x['term'] for x in terms),'ell':new.at(center_address).b+old.at(center_address).a,
                           'contact_term':terms[3]['term']})
            boundary.append({'update':t,'terms':external_terms(old,nodes)})
        other_zero=all(not(value[0] or value[1]) for frame in trace[start:end+1] for a,value in zip(addresses,frame) if a!=center_address)
        quiet={'full_region_period4':all(trace[t]==trace[t+4] for t in range(start,end-3)),
               'only_center_counter_activity':other_zero,
               'constant_center_remainder':len({row[2] for row in center_trace[start:end+1]})==1,
               'exact_quarter_turn':all(center_trace[t+1][:2]==[center_trace[t][1],-center_trace[t][0]] for t in range(start,end)),
               'zero_center_input_and_quotient':all(inputs[t]['u']==inputs[t]['ell']==0 for t in range(start,end)),
               'zero_individual_external_terms':all(not boundary[t]['terms'] for t in range(start,end))}
        quiet_common=all(quiet.values());hold=center_trace[start:end+1]
        unit=all(a*a+b*b==1 for a,b,r in hold)
        broad=all(0<abs(a)+abs(b)<=2 for a,b,r in hold)
        amplitude='unit' if unit else 'axis_two' if all((a==0) != (b==0) and max(abs(a),abs(b))==2 for a,b,r in hold) else 'diagonal' if all(abs(a)==abs(b)==1 for a,b,r in hold) else None
        null_canonical=all(all(tuple(state.at((*add(o,a[:3]),a[3])))==v for a,v in clock_cells((case['phase']+t)%4,True).items()) for t,state in enumerate(states))
        first_active=next((t for t,row in enumerate(center_trace) if row[0] or row[1]),None)
        first_activation=None
        if not(center_trace[0][0] or center_trace[0][1]) and first_active is not None:
            t=first_active;row=inputs[t-1];event=event_map.get((t,center_address))
            first_activation={'update':t,'before':center_trace[t-1],'after':center_trace[t],**row,'native_C':event,
                'zero_to_counter_guard_consistent':bool(center_trace[t][0]==0 and center_trace[t][1]==row['ell'] and row['ell']!=0 and row['u']!=0 and event is not None)}
        clocks[key]={'region_addresses':[list(a) for a in addresses],'region_trace':trace,'center_trace':center_trace,
            'center_inputs':inputs,'external_inputs':boundary,'quiet_predicates':quiet,'quiet_common':quiet_common,
            'unit_center':unit,'bounded_nonzero_center':broad,'amplitude_class':amplitude,'retained_center_remainder':hold[0][2] if quiet['constant_center_remainder'] else None,
            'primary_unit_r0_quiet':quiet_common and unit and all(row[2]==0 for row in hold),
            'secondary_even_quiet':quiet_common and broad and all(row[2] in (0,2,4) for row in hold),
            'complete_canonical_null_orbit':null_canonical,'all_region_counters_zero':all(not(v[0] or v[1]) for frame in trace for v in frame),
            'first_activation':first_activation}
    return {'routes':routes,'clocks':clocks,'all_C':events,'C_counts':counts,'whole_board_stationary':all(state==states[0] for state in states),
            'active_boundary_hit':any(any(v in (0,case['side']-1) for v in a[:3]) for state in states for a,x in state.cells.items() if x.a or x.b),
            'max_sparse_channels':max(len(state.cells) for state in states)}

def bare_key(case):return (case['side'],tuple(case['patterns']))
def assess_pair(rows,bare_bank,p):
    by={row['case']['source_present']:row for row in rows};off,on=by[False],by[True];case=on['case'];start,end=p['readouts']['hold_states']
    lo,hi=p['readouts']['route_window'];u0,u1=p['readouts']['upstream_window'];t0,t1=p['readouts']['contact_input_updates']
    result={'case':{k:v for k,v in case.items() if k!='source_present'},'stage':case['stage'],'clocks':{}}
    if case['stage']=='bare':
        checks={}
        for direction in sides(case):
            key=str(direction);a=on['observations']['routes'][key]['outlet'];b=off['observations']['routes'][key]['outlet']
            excited=any(any(v[:2]!=w[:2] and (v[0] or v[1]) for v,w in zip(a[t],b[t])) for t in range(lo,hi+1))
            equal=all(a[t]==b[t] for t in range(lo,hi+1))
            checks[key]={'pattern':pattern(case,direction),'source_caused_counter_output':excited,'entire_outlet_matches_null':equal}
        result.update({'bare_valid':all(v['source_caused_counter_output'] if v['pattern']=='OR' else v['entire_outlet_matches_null'] for v in checks.values()) and off['observations']['whole_board_stationary'],
                       'outlets':checks,'null_stationary':off['observations']['whole_board_stationary']})
        return result
    bare=bare_bank.get(bare_key(case));early={};nulls={};deliveries={}
    for direction in sides(case):
        key=str(direction);a=on['observations']['clocks'][key];b=off['observations']['clocks'][key]
        nulls[key]=b['complete_canonical_null_orbit'] if case['stage']=='primary' else off['observations']['whole_board_stationary'] and b['all_region_counters_zero']
        upstream_on=on['observations']['routes'][key]['upstream'];upstream_off=off['observations']['routes'][key]['upstream']
        upstream_arrival=next((t for t in range(lo,hi+1) if any(v[:2]!=w[:2] and (v[0] or v[1]) for v,w in zip(upstream_on[t],upstream_off[t]))),None)
        first_contact=next((t+1 for t in range(t0-1,t1) if a['center_inputs'][t]['contact_term']!=0 and a['center_inputs'][t]['contact_term']!=b['center_inputs'][t]['contact_term']),None)
        first_center=next((t for t in range(len(a['center_trace'])) if a['center_trace'][t]!=b['center_trace'][t]),None)
        first_region=next((t for t in range(len(a['region_trace'])) if a['region_trace'][t]!=b['region_trace'][t]),None)
        delivery=upstream_arrival is not None and first_contact is not None and first_center is not None and first_contact<=first_center
        deliveries[key]=delivery
        early[key]=True if case['isolated_direction'] else all(
            row['observations']['routes'][key]['upstream'][u0:u1+1]==bare['rows'][present]['observations']['routes'][key]['upstream'][u0:u1+1]
            for present,row in by.items())
        changed=all(a['center_trace'][t][:2]!=b['center_trace'][t][:2] for t in range(start,end+1))
        relative=[]
        for t in range(start,end+1):
            aa=tuple(a['center_trace'][t][:2]);bb=tuple(b['center_trace'][t][:2])
            relative.append((PHASES.index(aa)-PHASES.index(bb))%4 if aa in PHASES and bb in PHASES else None)
        fixed_changed=len(set(relative))==1 and relative[0] in (1,2,3)
        result['clocks'][key]={'pattern':pattern(case,direction),'null_valid':nulls[key],'early_upstream_matches_bare':early[key],
            'first_upstream_counter_arrival':upstream_arrival,'first_source_caused_contact_input':first_contact,
            'first_center_departure':first_center,'first_region_departure':first_region,'delivery_valid':delivery,
            'quiet_predicates':a['quiet_predicates'],'unit_r0_quiet':a['primary_unit_r0_quiet'],
            'retained_changed_phase':bool(a['primary_unit_r0_quiet'] and changed and fixed_changed),
            'relative_phase_during_hold':relative,'full_hold_matches_null':a['region_trace'][start:end+1]==b['region_trace'][start:end+1],
            'secondary_even_quiet':a['secondary_even_quiet'],'amplitude_class':a['amplitude_class'],
            'retained_remainder':a['retained_center_remainder'],'first_activation':a['first_activation']}
    bare_valid=True if case['isolated_direction'] else bare['assessment']['bare_valid']
    winner_keys=[str(d) for d in sides(case) if case['isolated_direction'] or pattern(case,d)=='OR']
    loser_keys=[str(d) for d in sides(case) if not case['isolated_direction'] and pattern(case,d)=='NO']
    eligible=bare_valid and all(early.values()) and all(nulls.values()) and all(deliveries[k] for k in winner_keys)
    loser_retained=all(result['clocks'][k]['full_hold_matches_null'] for k in loser_keys)
    primary=case['stage']=='primary' and eligible and loser_retained and all(result['clocks'][k]['retained_changed_phase'] for k in winner_keys)
    activation=case['stage']=='clock_off' and eligible and loser_retained and all(result['clocks'][k]['secondary_even_quiet'] and result['clocks'][k]['first_activation'] and result['clocks'][k]['first_activation']['zero_to_counter_guard_consistent'] for k in winner_keys)
    result.update({'eligible':bool(eligible),'bare_route_valid':bare_valid,'loser_retained':loser_retained,
                   'primary_phase_memory_pass':bool(primary),'secondary_activation_pass':bool(activation),
                   'secondary_unit_activation_pass':bool(activation and all(result['clocks'][k]['amplitude_class']=='unit' for k in winner_keys))})
    return result

def source_hashes():
    paths=[Path(__file__),PROTOCOL,HERE/'route_clock_budget.py',ROOT/'research/staged_blocks/orbit.py']
    for directory in ('universe24','research/components','research/experiments','research/presenter'):paths.extend((ROOT/directory).rglob('*.py'))
    return {str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(set(paths))}

def run(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=False);(output/'records').mkdir();(output/'native').mkdir();p=json.loads(PROTOCOL.read_text())
    frozen=source_hashes();wall=time.monotonic();ledger=[];native_ledger=[];groups=[];bare_bank={};examples=[];failure=None
    shutil.copyfile(PROTOCOL,output/'protocol.json');shutil.copyfile(Path(__file__),output/'executed_route_clock.py')
    write_json(output/'registration.json',{'source_sha256':frozen,'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'registered_before_capture':True,'preflight':preflight(p)})
    try:
        for pair in planned_pairs(p):
            if time.process_time()>p['budget']['max_cpu_seconds']-p['budget']['reserve_cpu_seconds_before_case'] or time.monotonic()-wall>p['budget']['max_wall_seconds']-60:
                failure={'type':'budget_stop_before_pair','case':pair[0]};break
            rows=[]
            for case in pair:
                if time.process_time()>p['budget']['max_cpu_seconds']-p['budget']['reserve_cpu_seconds_before_case'] or time.monotonic()-wall>p['budget']['max_wall_seconds']-60:
                    raise BudgetStop('Insufficient whole-process budget before next case')
                sp=spec(case,p);cap=run_experiment(sp);states=recorded_states(cap['experiment'])
                native_path=output/'native'/(sp['id']+'.json.gz')
                write_compressed(native_path,{'case':case,'spec':sp,'assembly':cap['assembly'],'experiment':cap['experiment']})
                native_ledger.append({'id':sp['id'],'record':str(native_path.relative_to(output)),'sha256':hashlib.sha256(native_path.read_bytes()).hexdigest()})
                if any(len(state.cells)>p['budget']['max_sparse_channels_per_state'] for state in states):raise RuntimeError('Per-state sparse channel cap exceeded')
                row={'case':case,'spec':sp,'assembly':cap['assembly'],'experiment':cap['experiment'],
                     'observations':observe(case,states,p,time.process_time()+p['budget']['max_observer_cpu_seconds_per_record'])}
                path=output/'records'/(sp['id']+'.json.gz');write_compressed(path,row)
                ledger.append({'id':sp['id'],'record':str(path.relative_to(output)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'full_rewind_equal':cap['experiment']['provenance']['full_rewind_equal']})
                if case['side']==289 and not case['isolated_direction'] and ((case['stage']=='primary' and case['phase']==1) or case['stage']=='clock_off'):examples.append(cap['experiment'])
                compact={'case':case,'observations':{key:value for key,value in row['observations'].items() if key!='all_C'}}
                rows.append(compact)
                if sum(path.stat().st_size for path in output.rglob('*') if path.is_file())>p['budget']['max_recorded_bytes']-12000000:raise RuntimeError('Recorded evidence budget reached')
            assessment=assess_pair(rows,bare_bank,p);groups.append(assessment)
            if pair[0]['stage']=='bare':bare_bank[bare_key(pair[0])]={'rows':{row['case']['source_present']:row for row in rows},'assessment':assessment}
            print(f'{len(ledger)}/64 {pair[0]["id"]}',flush=True)
    except Exception as error:
        failure={'type':type(error).__name__,'message':str(error),'case':locals().get('case')};write_json(output/'failure.json',failure)
    assert frozen==source_hashes(),'Frozen sources changed'
    if examples and time.process_time()<p['budget']['child_cpu_soft_limit']-10:write_json(output/'experiments.json',bundle(examples,title='The Presenter: routes and clock memory'))
    primary={str(phase):len([g for g in groups if g['stage']=='primary' and g['case']['phase']==phase])==12 and all(g['primary_phase_memory_pass'] for g in groups if g['stage']=='primary' and g['case']['phase']==phase) for phase in p['family']['clock_phases']}
    secondary=[g for g in groups if g['stage']=='clock_off']
    result={'status':'completed' if len(ledger)==64 and failure is None else 'inconclusive','failure':failure,'completed_cases':len(ledger),'cases':ledger,'pairs':groups,
        'primary_family_by_phase':primary,'primary_family_pass':any(primary.values()),
        'secondary_family_pass':len(secondary)==4 and all(g['secondary_activation_pass'] for g in secondary),
        'secondary_unit_family_pass':len(secondary)==4 and all(g['secondary_unit_activation_pass'] for g in secondary),
        'all_full_rewinds':all(row['full_rewind_equal'] for row in ledger),'sources_unchanged':True,'cpu_seconds_at_result':time.process_time(),'wall_seconds_from_run_entry':time.monotonic()-wall,
        'timing_scope':'Inner CPU is entire child-process CPU so far; authoritative whole-workflow timing including startup and final export/hashing is in outer_budget.json.',
        'native_checkpoints':native_ledger,
        'not_run_cases':[case['id']+'-s'+str(int(case['source_present'])) for pair in planned_pairs(p) for case in pair if case['id']+'-s'+str(int(case['source_present'])) not in {row['id'] for row in native_ledger}],
        'captured_not_observed':[row['id'] for row in native_ledger if row['id'] not in {item['id'] for item in ledger}],
        'scope':'Finite prepared route-to-clock memory and activation criteria; no autonomous selection or physical-light claim.'}
    result['inner_budget_so_far_passed']=result['cpu_seconds_at_result']<=p['budget']['max_cpu_seconds'] and result['wall_seconds_from_run_entry']<=p['budget']['max_wall_seconds'] and sum(path.stat().st_size for path in output.rglob('*') if path.is_file())<=p['budget']['max_recorded_bytes']
    write_json(output/'result.json',result);return result

def main():
    parser=argparse.ArgumentParser(description=__doc__);modes=parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--preflight-output',type=Path);modes.add_argument('--output',type=Path);args=parser.parse_args()
    if args.output:
        def exhausted(signum,frame):raise BudgetStop('Child CPU soft limit reached; earlier native checkpoints retained')
        signal.signal(signal.SIGXCPU,exhausted)
        run(args.output)
    else:
        args.preflight_output.parent.mkdir(parents=True,exist_ok=True);write_json(args.preflight_output,preflight(json.loads(PROTOCOL.read_text())))

if __name__=='__main__':main()
