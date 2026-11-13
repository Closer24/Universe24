"""Independent reread of the lossless saved traces and click records."""
import gzip
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from universe24.core import Engine, State, Tensor
from universe24.system.decoder import make_transition, decode_transition

parser=argparse.ArgumentParser()
parser.add_argument('--base',type=Path,default=Path('runs/light-packet-clicks-v2'))
base=parser.parse_args().base
reports={}
for name in ('flat','fast','step'):
    folder=base/name
    law=Tensor.from_dict(json.loads((folder/'tensor.json').read_text()),strict_support=True)
    setup=json.loads((folder/'protocol.json').read_text()); L=setup['L']
    engine=Engine(law)
    with gzip.open(folder/'full_trace_planes.jsonl.gz','rt') as f:
        traces=[json.loads(line) for line in f]
    with gzip.open(folder/'canonical_click_planes.jsonl.gz','rt') as f:
        clicks=[json.loads(line) for line in f]
    def state(record):
        return State(L,*[np.repeat(np.asarray(record[b],dtype=object),L*L,axis=1) for b in ('a','b','r')])
    before=state(traces[0]);seed=before.copy(); total=0
    for tick,(record,savedclicks) in enumerate(zip(traces[1:],clicks),1):
        after=state(record)
        assert engine.step(before).same_as(after)
        assert engine.inverse_step(after).same_as(before)
        old=[np.asarray(traces[tick-1][b],dtype=object) for b in ('a','b','r')]
        new=[np.asarray(record[b],dtype=object) for b in ('a','b','r')]
        expected=[]
        for x in range(L):
            for g in range(18):
                v=int(new[1][g,x]+old[0][g,x])
                changed=any(old[j][g,x]!=new[j][g,x] for j in range(3))
                if v and changed:
                    d=int((new[2][g,x]-old[2][g,x])%6)
                    kind=0 if d in (0,3) else 1 if d in (1,2) else 2
                    expected.append([x,g,kind,v])
        assert expected==savedclicks['rows']
        assert savedclicks['multiplicity']==L*L
        total+=len(expected)*L*L
        if tick==1:
            canonical=decode_transition(make_transition(law,before,after,run_id='d'*64,step=1),law)
            assert len(canonical)==len(expected)*L*L
            line=[(d['xyz'][0],d['channel'],int(d['kind'][1]),d['quotient'])
                  for d in canonical if d['xyz'][1:]==[0,0]]
            assert line==[tuple(v) for v in expected]
        before=after
    assert engine.rewind(before,len(clicks)).same_as(seed)
    assert total==json.loads((folder/'summary.json').read_text())['clicks']
    reports[name]={'full_array_forward_replay':'passed','full_array_inverse_and_rewind':'passed',
                   'all_saved_click_rows_independent_scalar_check':'passed',
                   'canonical_full_cube_decoder_step_1':'passed','clicks':total,
                   'trace_sha256':hashlib.sha256((folder/'full_trace_planes.jsonl.gz').read_bytes()).hexdigest()}
    print(name, reports[name],flush=True)
obs=[json.loads((base/n/'observations.json').read_text()) for n in reports]
same=obs[0]['clicks_per_node_per_tick']==obs[1]['clicks_per_node_per_tick']==obs[2]['clicks_per_node_per_tick']
assert same
reports['comparison']={'all_three_raw_click_maps_identical':same,
                       'all_three_first_click_maps_identical':all(o['summary']['first_click_ticks']==obs[0]['summary']['first_click_ticks'] for o in obs),
                       'quotient_magnitudes_differ':obs[0]['absolute_quotient_per_node_per_tick']!=obs[1]['absolute_quotient_per_node_per_tick'],
                       'x30_first_click_time':obs[0]['summary']['first_click_ticks'][30]/3,
                       'x30_earliest_flat_target_cone_time_from_complete_initial_support':12,
                       'x30_energy_fraction_at_first_click':obs[0]['energy'][7][30]/sum(obs[0]['energy'][7])}
(base/'post_validation.json').write_text(json.dumps(reports,indent=2))
print(json.dumps(reports['comparison'],indent=2),flush=True)
