"""Exact local TT carrier readout and a declared one-way diagonal test probe."""
from pathlib import Path
import json
import numpy as np
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))

from universe24.core import Engine,Tensor
from universe24.core.tensor import GearType
from universe24.core.reciprocity import check_reciprocity
from experiments.geometry.linear_spin2_check import build,phase_seed,constraints
from universe24.core.lattice import lattice


def run(steps=84):
    if type(steps) is not int or steps < 4:
        raise ValueError("at least four updates are required for the declared probe comparison")
    M=7;P=4096;R=M*P;Q=4*R;D=6*Q;w=2*R;L=7
    Hp=np.array([120,-96,24,-24,-16,48,-56],dtype=object)
    p=np.array([3,-2,-1,0,0,0,0],dtype=object)
    assert np.array_equal(np.roll(Hp,-2)+np.roll(Hp,2)-2*Hp,-8*M*p)
    base=build(Q)
    gears=[GearType('metric.'+name,'audit') for name in base.names]
    gears += [GearType('phase.c','audit'),GearType('phase.s','audit')]
    gears += [GearType('probe.X'),GearType('probe.Y'),GearType('rest.clock')]
    terms=[]
    for m in base.monomials:
     terms.append(('metric.'+base.names[m.target],m.coeff,tuple(('metric.'+base.names[f.gear],f.offset,f.field) for f in m.factors)))
    zero=(0,0,0)
    why={'designated_one_way':'Prescribed evolving TT test background: probes read the metric and its internal phase registers; their reciprocal backreaction is deliberately omitted, not an Einstein source model.'}
    for probe in ['probe.X','probe.Y']:
     terms.append((probe,D-6*w,((probe,zero,'b'),)))
     for axis in range(3):
      for sign in [-1,1]:
       off=tuple(sign if k==axis else 0 for k in range(3))
       terms.append((probe,w,((probe,off,'b'),)))
       sigma=[1,-1,0][axis]
       if not sigma:continue
       for metric_site in [zero,off]:
        for phase,field in [('phase.c','metric.E00'),('phase.s','metric.B01')]:
         for probe_site,polarity in [(off,-1),(zero,1)]:
          terms.append((probe,sigma*polarity,((phase,metric_site,'b'),(field,metric_site,'b'),(probe,probe_site,'b')),why))
    terms.append(('rest.clock',D//2,(('rest.clock',zero,'b'),)))
    T=Tensor(gears,terms,strict_support=True,Q=Q);engine=Engine(T,Q)
    reciprocity=check_reciprocity(T);assert reciprocity.ok
    lat=lattice(L);coords=np.array([lat.coords(i) for i in range(lat.N)]);z=coords[:,2]
    def prepare(wave):
     E=np.zeros((3,3,lat.N),dtype=object);B=E.copy()
     if wave:
      E[0,0]=Hp[z];E[1,1]=-Hp[z]
      B[0,1]=Hp[(z+1)%L];B[1,0]=B[0,1]
     core=phase_seed(E,B,Q,L)
     s=engine.vacuum(L,[D//2-1]*T.G)
     for field in ['a','b','r']:getattr(s,field)[:18]=getattr(core,field)
     s.b[T.gear_index('phase.c')]=1;s.a[T.gear_index('phase.s')]=-1
     amp=1<<18
     for name,axis in [('probe.X',0),('probe.Y',1)]:
      s.b[T.gear_index(name)]=(coords[:,axis]==0)*amp
      s.a[T.gear_index(name)]=s.b[T.gear_index(name)]
     s.b[T.gear_index('rest.clock')]=1
     return s
    
    def metric(s):
     return s.b[T.gear_index('phase.c')]*s.b[T.gear_index('metric.E00')]+s.b[T.gear_index('phase.s')]*s.b[T.gear_index('metric.B01')]
    def detnode(x,y,z):return x*L*L+y*L+z
    nodes={'probe.X':detnode(2,0,0),'probe.Y':detnode(0,2,0),'rest.clock':0}
    def one_case(wave):
     seed=prepare(wave);s=seed;records=0;phase_records=0;series={k:[] for k in nodes};first={k:None for k in nodes};peak=0
     for step in range(1,steps+1):
      after=engine.step(s)
      expected=Hp[(z+step)%L] if wave else np.zeros(lat.N,dtype=object)
      assert np.array_equal(metric(after),expected)
      assert np.array_equal(after.r[:20],seed.r[:20])
      for field in [after.a,after.b]:
       for start in [0,9]:assert not any(constraints(field[start:start+9].reshape(3,3,-1),lat).values())
      log=engine.clicks(s,after,step)
      phase_records+=sum(int(g) in [18,19] for g in log.gear)
      official=log.select('official');records+=len(official)
      rowmap={(int(g),int(n)):int(q) for g,n,q in zip(official.gear,official.node,official.quotient)}
      for name,node in nodes.items():
       value=rowmap.get((T.gear_index(name),node),0);series[name].append(value)
       if value and first[name] is None:first[name]=step
      peak=max(peak,after.max_abs());s=after
     assert phase_records==0
     assert engine.rewind(s,steps).same_as(seed)
     return {'wave':wave,'steps':steps,'official_records':records,'phase_register_records':phase_records,'detector_signed_official_quotients':series,'first_detector_event':first,'peak_counter':peak,'all_microstep_metric_shift_identities':True,'all_raw_metric_a_b_TT_constraints':True,'metric_and_phase_remainders_constant':True,'exact_rewind':True}
    flat=one_case(False);wave=one_case(True)
    assert flat['detector_signed_official_quotients']['probe.X']==flat['detector_signed_official_quotients']['probe.Y']
    assert flat['detector_signed_official_quotients']['rest.clock']==wave['detector_signed_official_quotients']['rest.clock']
    differences={}
    for name in ['probe.X','probe.Y']:
     a=flat['detector_signed_official_quotients'][name];b=wave['detector_signed_official_quotients'][name]
     differences[name]={'changed_samples':sum(x!=y for x,y in zip(a,b)),'first_change':next(i+1 for i,(x,y) in enumerate(zip(a,b)) if x!=y),'maximum_absolute_quotient_change':max(abs(x-y) for x,y in zip(a,b))}
    x,y=[wave['detector_signed_official_quotients'][name] for name in ['probe.X','probe.Y']]
    assert any(a!=b for a,b in zip(x,y))
    result={'scope':'Local phase-register decoding of an exact TT metric profile plus a metric-shaped one-way scalar test response; not a common Einstein geometry',
     'Q':Q,'D':D,'L':L,'M':M,'P':P,'metric_denominator':R,'probe_amplitude':1<<18,'w':w,'probe_flat_speed_squared':'1/6','metric_pattern_speed_squared':1,
     'rank':T.rank,'gears':T.G,'strict_support':True,'monomials':len(T.monomials),'designated_one_way_terms':len(reciprocity.designated),'remaining_reciprocity':reciprocity.ok,'tensor_fingerprint':T.fingerprint,
     'integer_metric_profile':list(map(int,Hp)),'curvature_profile':list(map(int,p)),'exact_reconstruction_identity':'delta_z^2 Hp = -8 M p','metric_bound':{'maximum_abs_h':float(max(abs(v) for v in Hp)/R),'spatial_metric_positive_every_step':bool(max(abs(v) for v in Hp)<R)},
     'phase_preparation':'Uniform c: a=0,b=1; s: a=-1,b=0; both u=0. They are unobserved internal phase registers, not click clocks.',
     'metric_observable':'F=c*metric.E00+s*metric.B01; hxx=F/(M P); hyy=-hxx; h0mu=hzz=hxy=0',
     'probe_input':'D chi + w sum_neighbors(chi_y-chi_x) - [w/(2 M P)] sum_{x/y neighbors} sigma_axis (F_x+F_y)(chi_y-chi_x)',
     'detectors':{k:dict(zip(['x','y','z'],lat.coords(v))) for k,v in nodes.items()},'flat':flat,'wave':wave,'wave_vs_flat':differences,
     'flat_X_Y_streams_identical':True,'wave_X_Y_streams_differ':True,'rest_clock_streams_identical':True,
     'limitations':['The two phase registers have zero quotient and no official records. Metric decoding is a local board polynomial, not an official-only reconstruction.','Probe couplings are fixed but explicitly one-way; reciprocal stress/backreaction and Einstein constraints are absent.','Only plus polarization diagonal link response is built; cross-polarization cross-axis gradient products violate strict single-edge support.','The probe speed squared is1/6 while the exact metric pattern speed squared is1; no common Einstein characteristic metric is established.','Measured differences are raw official quotient changes, not a calibrated geodesic or travel-time fit.','The metric profile is bounded by proof; the responding probe is checked only for the stated finite horizon.']}
    return result

if __name__ == "__main__":
    import argparse
    import hashlib
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--steps",type=int,default=84)
    parser.add_argument("--out",type=Path,default=Path("runs/geometry/phase_metric_probe.json"))
    args=parser.parse_args()
    result=run(args.steps)
    result["implementation_sha256"]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ("flat","wave")},indent=2))
