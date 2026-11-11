"""Exact code counterexamples for the named optional Einstein metric."""
from pathlib import Path
import sys,json,argparse
import numpy as np
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--out',type=Path,default=Path('runs/geometry/metric_obstruction_check.json'))
args=parser.parse_args()
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from universe24.core import Engine,compose
from universe24.layers.one import one_system
from universe24.layers.einstein import einstein_system
from universe24.observe.einstein import conservation_defect
from universe24.prepare.one import one_seed
from universe24.observe.readout import official_clicks
base=one_system();system=einstein_system(base,on=True);tensor=compose(*system.blocks)
engine=Engine(tensor,system.Q)
blind={}
for name in ('h0x','h0y','h0z','hxy','hxz','hyz'):
 g=tensor.gear_index('metric.'+name)
 readers=[m for m in tensor.monomials if m.target!=g and any(f.gear==g for f in m.factors)]
 blind[name]={'external_reading_monomials':len(readers),
              'own_target_monomials':sum(m.target==g for m in tensor.monomials)}
assert all(row['external_reading_monomials']==0 for row in blind.values())
initial,_=one_seed(system,tensor,4)
other=initial.copy();g=tensor.gear_index('metric.hxy')
pattern=np.array([(-1)**(n%4) for n in range(4**3)])
other.a[g]=system.info['P']//4*pattern;other.b[g]=other.a[g]
s,v=initial,other
records=0
for step in range(1,21):
 n,w=engine.step(s),engine.step(v)
 log=official_clicks(engine,s,n,step);twin=official_clicks(engine,v,w,step)
 assert log.rows()==twin.rows()
 keep=[i for i in range(tensor.G) if i!=g]
 assert np.array_equal(n.a[keep],w.a[keep])
 assert np.array_equal(n.b[keep],w.b[keep])
 assert np.array_equal(n.r[keep],w.r[keep])
 records+=len(log);s,v=n,w
assert engine.rewind(s,20).same_as(initial)
assert engine.rewind(v,20).same_as(other)
# A separate uniform scalar/reference preparation exposes the declared-source defect.
probe=engine.vacuum(3,[3*system.Q-1]*tensor.G)
probe.b[tensor.gear_index('ref.R00')]=32
after=engine.step(probe)
defect=conservation_defect(engine,probe,after)
assert defect['0']>0
result={'scope':'Named optional Einstein tensor, not all possible encodings or prepared sectors',
 'Q':system.Q,'P':system.info['P'],'tensor_fingerprint':tensor.fingerprint,
 'dynamics_fingerprint':tensor.dynamics_fingerprint,
 'blind_components':blind,
 'official_counterfactual':{'changed_initial_field':'metric.hxy alternating along z',
 'amplitude':system.info['P']//4,'steps':20,'official_records_each':records,
 'official_streams_identical':True,'all_other_state_registers_identical':True,
 'both_exact_rewind':True},
 'source_counterexample':{'preparation':'uniform ref.R00 b=32; a=0; all other counters0; r=3Q-1',
                         'declared_source_divergence':defect,
                         'limitation':'This is the implemented source diagnostic, not an independently derived physical stress tensor.'}}
args.out.parent.mkdir(parents=True,exist_ok=True)
args.out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
