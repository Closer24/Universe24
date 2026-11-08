"""New initial-state region/exterior crosses; no runtime state intervention."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import time

from research.experiments.run import assemble, recorded_states, run_experiment
from research.presenter.export import bundle, state_sha256
from research.clock_selection import search_v2 as parent
from research.clock_selection.provenance import freeze_sources, verify_sources
from universe24 import State

ROOT = parent.ROOT
HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / 'protocol_mediation.json'
base = parent.base


def load_parent(study, side, gap, mask):
    name = f'write-probe-L{side}-r0-p0-d2-gap{gap}-clock1-{mask}.json.gz'
    path = Path(study) / 'records' / name
    compressed = path.read_bytes()
    raw = gzip.decompress(compressed)
    record = json.loads(raw)
    return record, recorded_states(record['experiment']), {
        'record': str(path.relative_to(ROOT)),
        'record_gzip_sha256': hashlib.sha256(compressed).hexdigest(),
        'record_sha256': hashlib.sha256(raw).hexdigest(),
    }


def region_addresses(side):
    c = side // 2
    center = (c, c + 1, c)
    nodes = [center]
    for delta in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
        nodes.append(tuple(x+d for x,d in zip(center, delta)))
    return tuple((*n,g) for n in nodes for g in range(48))


def cross_initial(exterior, region_source, region):
    """Select complete triples from two source states before finalization."""
    if exterior.cube != region_source.cube or exterior.background != region_source.background:
        raise ValueError('Source boards differ')
    region = set(region)
    cells = {a:v for a,v in exterior.cells.items() if a not in region}
    cells.update({a:region_source.at(a) for a in region})
    return State(exterior.cube, exterior.background, cells)


def make_spec(case, p, initial, source_metadata):
    c = case['side']//2
    return {'format': 'universe24-assembly-experiment-v1', 'id': case['id'],
        'title': 'Clock-region mediation: '+case['id'],
        'description': p['claim'], 'question': p['question'],
        'board': {'side': case['side'], 'background': p['board']['background'], 'body_signs': p['board']['body_signs']},
        'components': [{'name': 'complete_initial_preparation', 'recipe': 'Patch', 'at': [0,0,0],
            'params': {'kind': 'offline-clock-region-cross',
                       'cells': [[*a,*v] for a,v in sorted(initial.cells.items())]}}],
        'steps': p['steps'], 'view': {'position': [c,c+1,c], 'channel': 2},
        'controls': case, 'provenance': {'initial_only': True, 'source_records': source_metadata,
            'anchor': p['parent']['anchor'], 'region_triples': len(region_addresses(case['side'])),
            'protocol_canonical_sha256': base.digest(p)},
        'budget': {'max_frames': p['steps']+1, 'max_cells': p['budget']['max_cells_per_record'],
                   'max_bytes': 67108864, 'max_seconds': p['budget']['max_seconds_per_record']}}


def observe(case, p, prepared, states, parent_protocol):
    vp = dict(parent_protocol, steps=p['steps'])
    vc = {'side': case['side'], 'clock_remainder': 0, 'phase': 0, 'writer_delay': 2,
          'gap': case['gap'], 'stage': 'encounter', 'guide_target_channel': 0,
          'compensation_direction': None, 'control': '11', 'clock_present': True}
    data = base.observe(parent.old.observer_protocol(vc, vp), vc, prepared, states)
    c = case['side']//2
    anchor = p['parent']['anchor']
    probe_x = c-18-case['gap']
    data['incoming'] = [{'step': case['gap']+k-anchor,
        'match': base.packet_matches(states[case['gap']+k-anchor], probe_x+case['gap']+k, c,c,1)}
        for k in p['incoming']['offsets']]
    excluded = {tuple(n) for n in data['region_nodes']}
    data['near_incoming'] = []
    for offset in p['near_incoming']['origin_offsets_from_clock']:
        x = c+offset
        t = 18+case['gap']+offset-anchor
        expected = {a:v for a,v in base._expected_packet(x,c,c,1).items() if a[:3] not in excluded}
        actual = {a:v for a,v in states[t].cells.items()
            if x-1<=a[0]<=x+4 and abs(a[1]-c)<=1 and abs(a[2]-c)<=1 and a[:3] not in excluded}
        data['near_incoming'].append({'step':t,'origin_x':x,'match':actual==expected})
    T = 26+case['gap']-anchor
    data['registered_output'] = [{'step':T+k,'origin_x':c+8+k,
        'match':base.packet_matches(states[T+k],c+8+k,c,c,1)} for k in p['output']['offsets']]
    data['registered_C_window'] = [T-3,T+4]
    data['registered_output_C'] = [{k:e[k] for k in ('step','kind','ell')} for e in data['all_C']
        if e['address']==[c+8,c,c,0] and T-3<=e['step']<=T+4]
    data['expected_output_C'] = [{'step':T+dt,'kind':kind,'ell':ell} for dt,kind,ell in p['output']['C_expected']]
    region = data['region_trace'][:5]
    center = data['center_trace'][:5]
    data['initial_hold'] = {
        'complete_region_period4':region[0]==region[4],
        'center_unit_counter_norm':all(v[0]*v[0]+v[1]*v[1]==1 for v in center),
        'other_counter_pairs_zero':all(not(v[0] or v[1]) for frame in region for j,v in enumerate(frame) if j!=2),
        'every_external_term_zero':all(not row['nonzero_external_terms'] for row in data['boundary_inputs'][:4])}
    active = [a for a,v in states[0].cells.items() if v.a or v.b]
    data['initial_active_boundary_margin'] = min((min(q,case['side']-1-q) for a in active for q in a[:3]), default=None)
    return data


def assess(case, p, states, data, split, native):
    predicted = case['gap']==(38 if case['region_source']=='11' else 36)
    carrier = all(x['match'] for x in data['registered_output'])
    raw = data['registered_output_C']==data['expected_output_C']
    margin = data['initial_active_boundary_margin']
    return {'split_equivalence': all(split.values()), 'incoming_contract':all(x['match'] for x in data['incoming']),
        'near_incoming_contract':all(x['match'] for x in data['near_incoming']),
        'initial_hold':all(data['initial_hold'].values()),
        'strict_initial_causal_margin':margin is None or margin>p['steps'],
        'no_active_boundary_contact':not data['active_boundary_hits'],
        'native_suffix_equal':native, 'predicted_output':predicted,
        'exact_output_carrier':carrier, 'exact_output_C_signature':raw,
        'carrier_follows_region':carrier==predicted, 'C_follows_region':raw==predicted}


def assess_group(rows):
    required = ('split_equivalence','incoming_contract','near_incoming_contract','initial_hold',
                'strict_initial_causal_margin','no_active_boundary_contact')
    complete = len(rows)==4 and {(r['case']['exterior_source'],r['case']['region_source']) for r in rows}==set(itertools.product(('01','11'),repeat=2))
    eligible = complete and all(r['assessment'][key] for r in rows for key in required)
    native = all(r['assessment']['native_suffix_equal'] is True for r in rows
                 if r['case']['exterior_source']==r['case']['region_source'])
    carrier = all(r['assessment']['carrier_follows_region'] for r in rows)
    raw = all(r['assessment']['C_follows_region'] for r in rows)
    inverse = all(r['experiment']['provenance']['full_rewind_equal'] for r in rows)
    return {'side':rows[0]['case']['side'], 'gap':rows[0]['case']['gap'],
        'complete_control_group':complete, 'eligible':eligible, 'native_suffix_controls_pass':native, 'all_full_state_inverses':inverse,
        'carrier_follows_region_all_exteriors':carrier, 'C_follows_region_all_exteriors':raw,
        'accepted_clock_region_mediation':eligible and native and inverse and carrier and raw,
        'cases':{r['case']['exterior_source']+'/'+r['case']['region_source']:r['assessment'] for r in rows}}


def run(output, study, parent_audit, protocol_path=PROTOCOL):
    raw_protocol = Path(protocol_path).read_bytes()
    p = json.loads(raw_protocol)
    study = Path(study).resolve()
    if hashlib.sha256((study/'protocol.json').read_bytes()).hexdigest()!=p['parent']['protocol_sha256']:
        raise ValueError('Parent protocol differs')
    audit_raw = Path(parent_audit).read_bytes()
    audit = json.loads(audit_raw)
    if not audit.get('passed') or audit.get('protocol_sha256')!=p['parent']['protocol_sha256']:
        raise ValueError('A passing independent certificate for the exact parent protocol is required')
    parent_protocol = json.loads((study/'protocol.json').read_text())
    parent_ledger = {r['id']:r for r in json.loads((study/'result.json').read_text())['cases']}
    output = Path(output)
    output.mkdir(parents=True,exist_ok=False)
    (output/'records').mkdir()
    (output/'protocol.json').write_bytes(raw_protocol)
    (output/'parent_independent_audit.json').write_bytes(audit_raw)
    source_paths = set(json.loads((study/'registration.json').read_text())['source_sha256'])
    source_paths.update(str(x.relative_to(ROOT)) for x in (Path(__file__),Path(protocol_path)))
    freeze_sources(output/'source_provenance',source_paths,metadata={'protocol_sha256':hashlib.sha256(raw_protocol).hexdigest(),
        'parent_study':str(study.relative_to(ROOT)),'anchor':40,'budget':p['budget'],'seed':None})
    cases = [{'id':f'mediation-L{L}-gap{gap}-E{E}-R{R}', 'side':L, 'gap':gap,
              'exterior_source':E,'region_source':R}
             for L,gap,E,R in itertools.product(p['board']['sides'],p['family']['gaps'],
                 p['family']['exterior_sources'],p['family']['region_sources'])]
    base.write_json(output/'registration.json',{'format':'universe24-clock-region-mediation-registration-v1',
        'cases':cases,'registered_before_capture':True,'protocol_sha256':hashlib.sha256(raw_protocol).hexdigest(),
        'parent_audit_sha256':hashlib.sha256(audit_raw).hexdigest(),'seed':None})
    cpu_start,wall_start = time.process_time(),time.monotonic()
    ledger=[];groups=[];examples=[];reason=None
    for L,gap in itertools.product(p['board']['sides'],p['family']['gaps']):
        if time.process_time()-cpu_start>=p['budget']['max_cpu_seconds'] or time.monotonic()-wall_start>=p['budget']['max_wall_seconds']:
            reason='time_budget';break
        if sum(f.stat().st_size for f in output.rglob('*') if f.is_file())>=p['budget']['max_recorded_bytes']:
            reason='data_budget';break
        originals={m:load_parent(study,L,gap,m) for m in ('01','11')}
        for record,_,metadata in originals.values():
            if record['protocol_sha256']!=p['parent']['protocol_sha256']:
                raise ValueError('Source record belongs to another protocol')
            expected=parent_ledger[record['spec']['id']]
            if any(expected[k]!=metadata[k] for k in ('record_sha256','record_gzip_sha256')):
                raise ValueError('Source record differs from the parent result ledger')
        anchors={m:v[1][40] for m,v in originals.items()}
        region=region_addresses(L);region_set=set(region)
        rows=[]
        for case in (x for x in cases if x['side']==L and x['gap']==gap):
            E,R=case['exterior_source'],case['region_source']
            initial=cross_initial(anchors[E],anchors[R],region)
            addresses=initial.cells.keys()|anchors[E].cells.keys()
            split={'region_equal_source':all(initial.at(a)==anchors[R].at(a) for a in region),
                   'outside_equal_source':all(initial.at(a)==anchors[E].at(a) for a in addresses if a not in region_set)}
            source_metadata={m:{**v[2],'anchor_state_sha256':state_sha256(anchors[m])} for m,v in originals.items()}
            spec=make_spec(case,p,initial,source_metadata)
            prepared=assemble(spec)
            split['finalized_initial_equal']=prepared.initial==initial
            record=run_experiment(spec)
            states=recorded_states(record['experiment'])
            data=observe(case,p,prepared,states,parent_protocol)
            native=all(a==b for a,b in zip(states,originals[E][1][40:89])) if E==R else None
            assessment=assess(case,p,states,data,split,native)
            rows.append({'case':case,'spec':spec,'assembly':record['assembly'],'experiment':record['experiment'],
                'source_records':source_metadata,'split_checks':split,'observations':data,'assessment':assessment})
        group=assess_group(rows);groups.append(group)
        for row in rows:
            wrapper={'format':'universe24-clock-region-mediation-record-v1',**row,'group_assessment':group,
                     'protocol_sha256':hashlib.sha256(raw_protocol).hexdigest()}
            raw=base.canonical(wrapper).encode();compressed=gzip.compress(raw,mtime=0)
            relative='records/'+row['case']['id']+'.json.gz'
            (output/relative).write_bytes(compressed)
            ledger.append({'id':row['case']['id'],'case':row['case'],'record':relative,
                'record_sha256':hashlib.sha256(raw).hexdigest(),'record_gzip_sha256':hashlib.sha256(compressed).hexdigest(),
                'frames':len(row['experiment']['frames']),'full_state_inverse':row['experiment']['provenance']['full_rewind_equal'],
                'assessment':row['assessment']})
            if L==337:examples.append(row['experiment'])
        print(base.canonical({'completed':len(ledger),'registered':len(cases),'side':L,'gap':gap,'mediation':group['accepted_clock_region_mediation']}),flush=True)
    verification=verify_sources(output/'source_provenance')
    base.write_json(output/'source_verification.json',verification)
    if not verification['archive_verified'] or not verification['live_sources_unchanged']:
        raise RuntimeError('Source identity changed')
    result={'format':'universe24-clock-region-mediation-result-v1','status':'completed' if reason is None else 'budget_stopped',
        'stop_reason':reason,'registered_cases':len(cases),'completed_cases':len(ledger),'not_run_cases':cases[len(ledger):],
        'cases':ledger,'groups':groups,'accepted_groups':sum(g['accepted_clock_region_mediation'] for g in groups),
        'all_full_state_inverses':all(r['full_state_inverse'] for r in ledger),'source_hashes_unchanged':True,
        'cpu_seconds':time.process_time()-cpu_start,'wall_seconds':time.monotonic()-wall_start,'claim':p['claim']}
    base.write_json(output/'result.json',result)
    selections=[]
    for i in range(0,len(examples),4):
        subset=examples[i:i+4];filename=f'experiments-{i//4+1:03d}.json'
        (output/filename).write_text(base.canonical(bundle(subset,title='The Presenter: clock-region mediation'))+'\n')
        selections.append({'bundle':filename,'ids':[e['id'] for e in subset]})
    base.write_json(output/'presenter_selection.json',{'complete_experiments':len(examples),'pages':selections})
    receipt={'bytes':sum(f.stat().st_size for f in output.rglob('*') if f.is_file()),
        'cpu_overrun':max(0,result['cpu_seconds']-p['budget']['max_cpu_seconds']),
        'wall_overrun':max(0,result['wall_seconds']-p['budget']['max_wall_seconds'])}
    receipt['byte_overrun']=max(0,receipt['bytes']-p['budget']['max_recorded_bytes'])
    base.write_json(output/'budget_receipt.json',receipt)
    print(base.canonical({k:result[k] for k in ('completed_cases','accepted_groups','cpu_seconds')}),flush=True)
    return result


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path)
    parser.add_argument('--study',type=Path,default=ROOT/'research/clock_selection/evidence/write_probe_v2')
    parser.add_argument('--parent-audit',required=True,type=Path)
    args=parser.parse_args(argv)
    run(args.output,args.study,args.parent_audit)


if __name__=='__main__':main()
