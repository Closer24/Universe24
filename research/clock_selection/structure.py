"""Frozen initial-data structure family and passive full-state observations."""
from __future__ import annotations
import argparse,gzip,hashlib,itertools,json,subprocess,time
from functools import lru_cache
from collections import Counter
from pathlib import Path
from universe24 import Coupling
from universe24.core.group_2o import DIRECTIONS
from universe24.observation.clicks import clicks
from research.components.recipes import GuidedPacketSource
from research.experiments.run import recorded_states,run_experiment
from research.presenter.export import bundle
from research.staged_blocks import interactions as shared
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];PROTOCOL=HERE/'structure_protocol_v1.json'
CP=Coupling((1,1,1));PAIR=((-1,-1,0),(-1,0,4),(0,1,4),(1,1,0),(1,-1,2));PH=(2,0,0,2,4)
SINGLE=((-1,-1,0),(-1,1,0),(1,1,0),(1,-1,0));SH=(2,0,2,4)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
@lru_cache(None)
def template(kind,phase):
    centers=((0,0,0),(0,0,1)) if kind=='pair' else ((0,0,0),)
    cycle,halo=(PAIR,PH) if kind=='pair' else (SINGLE,SH)
    a,b,r=cycle[phase];rh=halo[phase];nodes=set(centers)
    for o in centers:nodes.update(add(o,d) for d in DIRECTIONS)
    cells={(*o,g):(0,0,2) for o in nodes for g in range(48)}
    for o in centers:
        cells[(*o,2)]=(a,b,r);cells[(*o,24)]=(-a,-b,4-r)
        for d,delta in enumerate(DIRECTIONS):
            q=add(o,delta)
            if q in centers:continue
            cells[(*q,CP.ports[d][2])]=(0,0,rh);cells[(*q,CP.ports[d][24])]=(0,0,4-rh)
    return tuple(sorted(cells.items()))
def spec(case,p):
    L=case['side'];c=L//2;x0=c-16-case['delay'];origin=(c,c+1,c);cells={};owners={}
    def put(a,v,owner):
        v=tuple(v)
        if a in cells and cells[a]!=v:raise ValueError(f'Initial conflict {a}: {owners[a]} / {owner}')
        cells[a]=v;owners[a]=owner
    for x in range(L):
        if x not in range(x0,x0+4):
            put((x,c,c,0),(0,0,0),'guide');put((x,c,c,14),(0,0,4),'guide')
    sources={'packet':[],'cluster':[]}
    for a,v in GuidedPacketSource().cells:
        q=(a[0]+x0,a[1]+c,a[2]+c,a[3]);v=tuple(v)
        if v[0] or v[1]:
            sources['packet'].append(q)
            if case['control'][0]=='0':v=(0,0,v[2])
        put(q,v,'packet')
    if case['kind']=='encounter':
        for a,v in template('pair',case['phase']):
            q=(*add(a[:3],origin),a[3])
            if v[0] or v[1]:
                sources['cluster'].append(q)
                if case['control'][1]=='0':v=(0,0,v[2])
            put(q,v,'cluster')
    region=[[*add(a[:3],origin),a[3]] for a,v in template('pair',0)]
    return {'format':'universe24-assembly-experiment-v1','id':case['id']+'-'+case['control'],
        'title':'Signal and paired-clock cluster: '+case['id']+'-'+case['control'],
        'description':'Initial-data-only structure experiment; passive complete-state readouts do not implement physical forces.',
        'question':p['question'],'board':{**p['board'],'side':L},'steps':p['steps'],'seed':None,
        'components':[{'name':'prepared','recipe':'Patch','at':[0,0,0],
        'params':{'kind':'joint-signal-cluster','cells':[[*a,*v] for a,v in sorted(cells.items())],
        'ports':{'cluster':region,'center':[[*origin,2]]},'sources':{k:v for k,v in sources.items() if v}}}],
        'detectors':[],'view':{'port':'prepared.center'},'controls':case,
        'provenance':{'initial_only':True,'protocol_sha256':hashlib.sha256(PROTOCOL.read_bytes()).hexdigest()},
        'budget':{'max_frames':p['steps']+1,'max_cells':p['budget']['max_sparse_channels']*(p['steps']+1),
                  'max_seconds':p['budget']['max_seconds_per_record'],'max_bytes':67108864}}
def matches(s,o,kind,q):
    cycle=PAIR if kind=='pair' else SINGLE
    if tuple(s.at((*o,2)))!=cycle[q]:return False
    if kind=='pair' and tuple(s.at((*add(o,(0,0,1)),2)))!=cycle[q]:return False
    return all(tuple(s.at((*add(a[:3],o),a[3])))==v for a,v in template(kind,q))
def external(s,nodes):
    result=[]
    for a,v in s.cells.items():
        if not v.b or a[:3] in nodes:continue
        for d in range(6):
            target=s.cube.adjacent(a,d,CP.ports[d][a[3]])
            if target[:3] in nodes:result.append({'source':list(a),'target':list(target),'term':v.b})
    return result
def observe(case,states,p):
    c=case['side']//2;o=(c,c+1,c);start,end=p['readouts']['hold_states'];core={o,add(o,(0,0,1))}
    region=[(*add(a[:3],o),a[3]) for a,v in template('pair',0)];nodes={a[:3] for a in region};skin=nodes-core
    trace=[[list(s.at(a)) for a in region] for s in states]
    boundary=[{'update':t+1,'terms':external(s,nodes)} for t,s in enumerate(states[:-1])]
    periods=[q for q in p['readouts']['periods'] if all(trace[t]==trace[t+q] for t in range(start,end-q+1))]
    origins=[add(o,d) for d in itertools.product(range(-4,5),repeat=3)]
    objects=[{'state':t,'matches':[{'origin':list(a),'phase':q} for a in origins for q in range(5) if matches(s,a,'pair',q)]} for t,s in enumerate(states)]
    unique=all(len(v['matches'])==1 for v in objects)
    continuous=bool(unique and all(objects[t+1]['matches'][0]['phase']==(objects[t]['matches'][0]['phase']+1)%5 and sum(abs(a-b) for a,b in zip(objects[t+1]['matches'][0]['origin'],objects[t]['matches'][0]['origin']))<=1 for t in range(len(objects)-1)))
    products=[]
    for a in origins:
        for q in range(4):
            if not all(matches(states[t],a,'single',(q+t-start)%4) for t in range(start,end+1)):continue
            n={add(b[:3],a) for b,v in template('single',0)}
            if all(not external(states[t],n) for t in range(start,end)):products.append({'origin':list(a),'phase_at_start':q})
    product_pairs=[[a,b] for a,b in itertools.combinations(products,2) if sum(abs(x-y) for x,y in zip(a['origin'],b['origin']))>=3]
    incoming=[{'step':t,'matches':shared.packet_matches(states[t],c-16-case['delay']+t,c,c,1)} for t in range(case['delay']+4,case['delay']+8)]
    events=[];counts={r:{str(k):0 for k in range(3)} for r in ('core','skin','exterior')}
    for t,(old,new) in enumerate(zip(states,states[1:]),1):
        for e in clicks(old,new,t):
            r='core' if e.address[:3] in core else 'skin' if e.address[:3] in skin else 'exterior'
            terms=[]
            for d in range(6):
                a=old.cube.adjacent(e.address,d,CP.ports[d][e.address[3]])
                terms.append({'source':list(a),'term':CP.weights[d][e.address[3]]*old.at(a).b})
            events.append({'step':t,'address':list(e.address),'kind':e.kind,'ell':e.quotient,'region':r,'six_terms':terms,'u':sum(v['term'] for v in terms)})
            counts[r][str(e.kind)]+=1
    # Raw-class coexistence diagnostics: no type is assigned selection semantics.
    coexist=[]
    event_counts=Counter((e['step'],e['kind']) for e in events)
    for lag in range(5):
        pairs=[]
        for a in range(3):
            for b in range(3):
                count=sum(event_counts[t,a]*event_counts[t+lag,b]-(event_counts[t,a] if lag==0 and a==b else 0) for t in range(1,len(states)))
                pairs.append([a,b,count])
        coexist.append({'lag':lag,'ordered_distinct_event_pairs':pairs})
    margin=min((min(v,case['side']-1-v) for a,x in states[0].cells.items() if x.a or x.b for v in a[:3]),default=case['side'])
    return {'region_addresses':[list(a) for a in region],'core_nodes':[list(a) for a in sorted(core)],'skin_nodes':[list(a) for a in sorted(skin)],
       'region_trace':trace,'boundary_inputs':boundary,'hold_periods':periods,
       'hold_nonzero':any(v[0] or v[1] for frame in trace[start:end+1] for v in frame),
       'hold_individually_isolated':all(not boundary[t]['terms'] for t in range(start,end)),
       'incoming':incoming,'incoming_valid':all(v['matches'] for v in incoming),
       'canonical_object_trace':objects,'unique_continuous_object':continuous,
       'moving_composite':bool(continuous and any(v['matches'][0]['origin']!=objects[0]['matches'][0]['origin'] for v in objects)),
       'isolated_product_templates':products,'separated_product_pairs':product_pairs,
       'separated_products_without_parent':bool(product_pairs and all(not v['matches'] for v in objects[start:end+1])),
       'all_C':events,'C_counts':counts,'C_class_lag_coexistence':coexist,'initial_active_boundary_margin':margin,
       'active_boundary_hit':any(any(v in (0,case['side']-1) for v in a[:3]) for s in states for a,x in s.cells.items() if x.a or x.b)}
def assess(rows,p):
    by={r['case']['control']:r for r in rows};start,end=p['readouts']['hold_states']
    initial={m:recorded_states(r['experiment'])[0] for m,r in by.items()};addresses=set().union(*(s.cells for s in initial.values()))
    remainder=all(len({s.at(a).r for s in initial.values()})==1 for a in addresses)
    masks=all(initial['11'].at(a)[j]==initial['10'].at(a)[j]+initial['01'].at(a)[j]-initial['00'].at(a)[j] for a in addresses for j in (0,1))
    validity={m:(r['observations']['incoming_valid'] if m[0]=='1' else not any(v['matches'] for v in r['observations']['incoming'])) for m,r in by.items()}
    eligible=remainder and masks and all(validity.values());clock=by['01']['observations'];on=by['11']['observations'];packet=by['10']['observations'];null=by['00']['observations']
    def retained(o):return bool(o['hold_periods'] and o['hold_nonzero'] and o['hold_individually_isolated'])
    return {'geometry':{k:v for k,v in rows[0]['case'].items() if k!='control'},'matched_remainders':remainder,'counter_masks_commute':masks,
      'incoming_controls':validity,'eligible_source_comparison':eligible,
      'clock_only_period5':all(clock['region_trace'][t]==clock['region_trace'][t+5] for t in range(p['steps']-4)),
      'clock_only_complete_template':all(len(v['matches'])==1 and v['matches'][0]['phase']==(by['01']['case']['phase']+v['state'])%5 for v in clock['canonical_object_trace']),
      'signal_created_recurrent_region':bool(eligible and retained(packet) and not any(v[0] or v[1] for f in null['region_trace'] for v in f)),
      'signal_reconfigured_recurrent_region':bool(eligible and retained(on) and on['region_trace'][start:end+1]!=clock['region_trace'][start:end+1]),
      'joint_canonical_cluster_retained_in_hold':all(v['matches'] for v in on['canonical_object_trace'][start:end+1]),
      'source_induced_separated_clock_products':bool(eligible and on['separated_products_without_parent'] and not clock['separated_products_without_parent']),
      'motion_attraction_repulsion':'not_tested_no_two_initial_moving_objects','physical_binding_or_dissociation_established':False}
def hashes():
    files=[Path(__file__),PROTOCOL,Path(shared.__file__)]
    for directory in ('universe24','research/components','research/experiments','research/presenter'):files.extend((ROOT/directory).rglob('*.py'))
    return {str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(set(files))}
def run(output):
    output=Path(output);raw=PROTOCOL.read_bytes();p=json.loads(raw);source=hashes();output.mkdir(parents=True,exist_ok=False);(output/'records').mkdir();(output/'protocol.json').write_bytes(raw)
    shared.write_json(output/'registration.json',{'protocol_sha256':hashlib.sha256(raw).hexdigest(),'source_sha256':source,'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'registered_before_capture':True})
    planned=[]
    for side,delay in itertools.product(p['family']['sides'],p['family']['delays']):planned.append([{'id':f'pristine-L{side}-d{delay}','side':side,'phase':1,'delay':delay,'kind':'pristine','control':'10'}])
    for side,phase,delay in itertools.product(p['family']['sides'],p['family']['cluster_phases'],p['family']['delays']):planned.append([{'id':f'cluster-L{side}-p{phase}-d{delay}','side':side,'phase':phase,'delay':delay,'kind':'encounter','control':m} for m in p['family']['controls']])
    cpu,wall=time.process_time(),time.monotonic();ledger=[];groups=[];examples=[];stop=None
    for planned_group in planned:
        if time.process_time()-cpu>p['budget']['max_cpu_seconds']-20 or time.monotonic()-wall>p['budget']['max_wall_seconds']-30:stop='budget_before_group';break
        rows=[]
        for case in planned_group:
            sp=spec(case,p);cap=run_experiment(sp);states=recorded_states(cap['experiment'])
            if any(len(state.cells)>p['budget']['max_sparse_channels'] for state in states):raise RuntimeError('Registered per-state sparse-channel cap exceeded')
            rows.append({'case':case,'spec':sp,'assembly':cap['assembly'],'experiment':cap['experiment'],'observations':observe(case,states,p)})
        group=assess(rows,p) if len(rows)==4 else {'pristine':True,'incoming_valid':rows[0]['observations']['incoming_valid']};groups.append(group)
        for row in rows:
            row['assessment']=group;identity=row['spec']['id'];path=output/'records'/(identity+'.json.gz');path.write_bytes(gzip.compress(shared.canonical(row).encode(),mtime=0))
            ledger.append({'id':identity,'record':str(path.relative_to(output)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'full_rewind_equal':row['experiment']['provenance']['full_rewind_equal']})
            if row['case']['kind']=='encounter' and row['case']['side']==161 and row['case']['delay']==4:examples.append(row['experiment'])
        print(f'{len(ledger)}/36 {planned_group[0]["id"]}',flush=True)
        if sum(f.stat().st_size for f in output.rglob('*') if f.is_file())>p['budget']['max_recorded_bytes']-20000000:stop='evidence_budget';break
    if source!=hashes() or raw!=PROTOCOL.read_bytes():raise RuntimeError('Frozen source changed')
    (output/'experiments.json').write_text(shared.canonical(bundle(examples,title='The Presenter: signal and clock structures'))+'\n')
    result={'status':'completed' if len(ledger)==36 and stop is None else 'budget_stopped','stop_reason':stop,'registered_cases':36,'completed_cases':len(ledger),'groups':groups,'cases':ledger,'all_full_rewinds':all(c['full_rewind_equal'] for c in ledger),'cpu_seconds':time.process_time()-cpu,'wall_seconds':time.monotonic()-wall,'sources_unchanged':True,'scope':'Finite structures; no physical attraction, repulsion or chemical binding established.'}
    result['budget_passed']=result['cpu_seconds']<=p['budget']['max_cpu_seconds'] and result['wall_seconds']<=p['budget']['max_wall_seconds'] and sum(f.stat().st_size for f in output.rglob('*') if f.is_file())<=p['budget']['max_recorded_bytes']
    shared.write_json(output/'result.json',result);return result
def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',required=True,type=Path);return run(ap.parse_args(argv).output)
if __name__=='__main__':main()
