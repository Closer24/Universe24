"""Read-only clock/causality audit of main 7d238e8; no model updates."""
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import numpy as np
from universe24.algebra.integer_circuit import Circuit
from universe24.core import Engine
from universe24.layers.universe import UniverseProgram
from universe24.prepare.conformal_flrw import prepare as prepare_flrw
from universe24.observe.conformal_flrw import sample as sample_flrw
from universe24.observe.metric_clocks import rate_squared
from experiments.geometry.transported_probe_clock import run as probe_run

c=Circuit(); x=c.input('x'); p=c.compile({'square':x*x})
seed=p.prepare(3,{'x':np.full((3,3,3),2,dtype=object)})
clock_ids=[p.tensor.gear_index(f'clock.c{j}') for j in range(p.period)]
delayed=seed.copy(); pulse=lambda j:1 if j%p.period==0 else -1 if j%p.period==1 else 0
for j,g in enumerate(clock_ids):
    delayed.b[g,0]=pulse(j-2)
    delayed.a[g,0]=pulse(j-3)
e=Engine(p.tensor); a,b=seed,delayed; rows=[]
for t in range(p.period+p.ticks+1):
    rows.append({'microtick':t,'normal_node0':str(p.read(a,'square',0)),
                 'phase_delayed_node0':str(p.read(b,'square',0)),
                 'phase_delayed_node1':str(p.read(b,'square',1))})
    if t<p.period+p.ticks:a,b=e.step(a),e.step(b)
assert rows[2]['normal_node0']=='4' and rows[2]['phase_delayed_node0']=='0'
assert rows[4]['phase_delayed_node0']=='4'
assert rows[-1]['normal_node0']=='8'
assert e.rewind(a,p.period+p.ticks).same_as(seed)
assert e.rewind(b,p.period+p.ticks).same_as(delayed)
silent=seed.copy()
silent.a[clock_ids]=0; silent.b[clock_ids]=0
silent_final=e.run(silent,p.ticks)
assert p.read(silent_final,'square',0)==0
assert e.rewind(silent_final,p.ticks).same_as(silent)
clock_terms=[m for m in p.tensor.to_dict()['monomials'] if m[0].startswith('clock.')]
assert all(f[1]==[0,0,0] for m in clock_terms for f in m[2])
program=UniverseProgram(p,{'fields':['x'],'steps':0},causal_wave=True,probe_experiment=True)
terms=program.tensor.to_dict()['monomials']
cross=[m for m in terms if any(m[0].split('.')[0]!=f[0].split('.')[0] for f in m[2])]
assert not cross
flrw=[]
for A in (1,2):
    tensor, initial=prepare_flrw(L=3,q0=2,dust=(A,0,0),radiation=1)
    engine,state=Engine(tensor),initial
    frames=[]; kinds={0:0,1:0,2:0}
    for t in range(9):
        obs=sample_flrw(state)
        frames.append({'microtick':t,'q':int(state.b[tensor.gear_index('clock.q'),0]),
            'proper_time':str(obs['proper_time']),'scale_factor':str(obs['scale_factor']),
            'null_affine_parameter':str(obs['null_affine_parameter'])})
        if t<8:
            after=engine.step(state)
            ev=engine.clicks(state,after,t+1)
            for k in kinds:kinds[k]+=int(np.count_nonzero(ev.kind==k))
            state=after
    assert engine.rewind(state,8).same_as(initial)
    assert np.array_equal(state.r,initial.r)
    assert kinds[1]==kinds[2]==0
    flrw.append({'dust_A':A,'frames':frames,'classes':kinds,'rewind_exact':True})
assert [r['q'] for r in flrw[0]['frames']]==[r['q'] for r in flrw[1]['frames']]
probe=probe_run(macrosteps=12,L=5)
probe_compact=[{'curvature':c['curvature'],'x':c['x'],'y':c['y'],
    'exact_rewind':c['exact_rewind'],'assessment':c['assessment']} for c in probe['cases']]
report={'baseline':'7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2',
 'compiler_clock':{'G':p.tensor.G,'ticks':p.ticks,'period':p.period,'clock_channels':len(clock_ids),
 'uniform_initial_clock_a_b':bool(np.all(seed.a[clock_ids]==seed.a[clock_ids,:1]) and np.all(seed.b[clock_ids]==seed.b[clock_ids,:1])),
 'clock_terms_have_only_zero_spatial_offsets':True,'trajectory':rows,'both_complete_rewinds_exact':True,
 'zero_clock_output_at_horizon':str(p.read(silent_final,'square',0)),
 'zero_clock_rewind_exact':True,
 'interpretation':'Clock gears propagate around an internal gear ring at every spatial node; prepared phases match, but one node can be delayed independently. Repeated wraps reapply the finite arithmetic program; they are outside its declared horizon.'},
 'assembly':{'G':program.tensor.G,'monomials':len(terms),'cross_component_monomials':len(cross),
 'interpretation':'Exact ownership inspection of UniverseProgram constructors. Optional wave/communication/probe states cannot read ADM metric or drive ADM; they are isolated research components.'},
 'FLRW':flrw,'transported_probe':{'common_metric_validated':probe['common_metric_validated'],'cases':probe_compact},
 'coordinate_calibration_counterexample':{'tangent':[1,1,0,0],'norm_at_alpha1':str(rate_squared([[-1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],(1,0,0))),
 'proper_rate_squared_at_alpha2':str(rate_squared([[-4,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],(1,0,0))),
 'meaning':'A unit coordinate-speed signal is null in the first chart and timelike in the second. This is an illustrative metric identity, not a calibrated trajectory claim for computational microticks.'}}
files=['experiments/research/six_lens_clocks.py','universe24/algebra/integer_circuit.py','universe24/layers/universe.py','universe24/layers/causal_wave.py','universe24/layers/communication.py','universe24/prepare/conformal_flrw.py','universe24/observe/conformal_flrw.py','universe24/observe/metric_clocks.py','experiments/geometry/transported_probe_clock.py']
report['source_sha256']={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files}
out=ROOT/'runs/six-lens/01-clocks/report.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'compiler':report['compiler_clock'],'cross_component_monomials':len(cross),'FLRW_final':[x['frames'][-1] for x in flrw],'probe_common_metric_passes':probe['common_metric_validated']},indent=2))
