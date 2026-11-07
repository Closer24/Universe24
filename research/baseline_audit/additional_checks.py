"""Independent bounded baseline checks; no runtime state intervention."""
from itertools import product
import hashlib,json,pathlib,random
from universe24.core import Channel,Coupling,Cube,Engine,State,VACUUM
from universe24.core.group_2o import DIRECTIONS
from universe24.experiments import load

root=pathlib.Path(__file__).resolve().parents[2]
out=pathlib.Path(__file__).resolve().parent
rng=random.Random(20261107)
results={'rng_seed':20261107,'node_equivalence':[],'clocks':[]}
for signs in product((-1,1), repeat=3):
 for rem in range(6):
  cube=Cube(3);engine=Engine(Coupling(signs))
  cells={(rng.randrange(3),rng.randrange(3),rng.randrange(3),rng.randrange(48)):
         Channel(rng.randrange(-11,12),rng.randrange(-11,12),rng.randrange(6)) for _ in range(40)}
  state=State(cube,Channel(0,0,rem),cells);after=engine.advance(state)
  for x,y,z in product(range(3),repeat=3):
   neighbors=tuple(state.node(((x+dx)%3,(y+dy)%3,(z+dz)%3)) for dx,dy,dz in DIRECTIONS)
   assert engine.update_node(state.node((x,y,z)),neighbors)==after.node((x,y,z))
  assert engine.rewind(after)==state
  results['node_equivalence'].append({'signs':signs,'background_remainder':rem,'L':3,'nodes_compared':27,'pass':True})
for side in (5,7,11):
 for signs in ((1,1,1),(1,-1,1)):
  for count in (1,2):
   engine=Engine(Coupling(signs));mid=side//2
   cells={}
   for offset in range(count):
    cells[(mid+offset,mid,mid,0)]=Channel(-1,-1,0)
    cells[(mid+offset,mid,mid,14)]=Channel(1,1,4)
   state=State(Cube(side),cells=cells);initial=state;period=None
   for t in range(1,21):
    state=engine.advance(state)
    if state==initial: period=t;break
   results['clocks'].append({'L':side,'signs':signs,'adjacent_clock_pairs':count,'first_full_state_return_up_to_20':period})
ref_original=json.loads((root/'research/reflection_audit_results.json').read_text())
ref_new=json.loads((out/'reflection_audit_results.json').read_text())
results['reflection_result_matches_committed_json']=ref_original==ref_new
assert results['reflection_result_matches_committed_json']
(out/'additional_results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'node_equivalence_runs':len(results['node_equivalence']),'clocks':results['clocks'],'reflection_result_matches_committed_json':True},indent=2))
