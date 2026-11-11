"""Exact rational first-update truncation control, never an Engine trajectory.

The same spatial constrained slice is used at every h with a first-order
backward temporal initialization y_prev=y-h*f(y). The first leapfrog output
is y+h*f(y). This local one-update check says nothing by itself about a fixed
physical-time or joint spatial/time convergence theorem.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from experiments.geometry.team48.numerical_sign_validation import momentum_seed,sampled,as_array,matter_builder,numerical_summary,MATTER_FIELDS
from experiments.geometry.team48.integer_sign_lift import compile_quadratic


def run(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    current,seed_report=momentum_seed()
    rhs,_,_=sampled(MATTER_FIELDS,matter_builder,current,5)
    derivative=as_array(rhs,MATTER_FIELDS,125)
    _,plus_constraints,_=sampled(MATTER_FIELDS,matter_builder,current+derivative,5)
    _,minus_constraints,_=sampled(MATTER_FIELDS,matter_builder,current-derivative,5)
    # Every constraint is degree<=2: this symmetric directional derivative
    # is exact, not a finite-difference approximation in field space.
    tangent={name:str(max(abs(v) for v in np.broadcast_to(
        F(1,2)*(plus_constraints[name]-minus_constraints[name]),(125,))))
        for name in plus_constraints}
    assert tangent['H']=='0' and tangent['M0']=='21'
    rows=[]
    for denominator in (1,2,4,8,16,32,64,128):
        h=F(1,denominator)
        previous=current-h*derivative
        following=previous+2*h*derivative
        check=numerical_summary(following,5)
        try:
            compile_quadratic(MATTER_FIELDS,matter_builder,dt=h,dx=1)
            compiles=True;reason=None
        except ValueError as exc:
            compiles=False;reason=str(exc)
        rows.append({'h':str(h),'arithmetic':'Exact Fraction reference; not Engine',
                     'raw_integer_compiles':compiles,'compile_reason':reason,
                     'previous_and_next_all_raw_integers':all(F(v).denominator==1 for v in previous.flat)
                                                        and all(F(v).denominator==1 for v in following.flat),
                     'H_peak':check['peak_constraints']['H'],'M0_peak':check['peak_constraints']['M0'],
                     'H_peak_divided_by_h_squared':str(F(check['peak_constraints']['H'])/(h*h)),
                     'M0_peak_divided_by_h_squared':str(F(check['peak_constraints']['M0'])/(h*h)),
                     'singular_nodes':check['singular_nodes']})
    assert all(F(rows[i+1]['H_peak'])<F(rows[i]['H_peak']) for i in range(len(rows)-1))
    assert all(F(rows[i+1]['M0_peak'])<F(rows[i]['M0_peak']) for i in range(len(rows)-1))
    report={'scope':'Exact rational same-spatial-seed first-update control, not a fixed-time or integer-refinement convergence claim',
            'initial_slice':seed_report,'dx':1,'temporal_initialization':'previous=current-h*rhs(current)',
            'initial_constraint_time_derivative_peaks':tangent,
            'semidiscrete_momentum_constraint_has_nonzero_time_derivative':True,
            'samples':rows,'conclusion':'Smaller formal time steps reduce this seeded first-update constraint error. The exact semidiscrete momentum-constraint derivative is already nonzero (peak21) at fixed dx1, so time refinement alone does not make the constraint surface invariant. The raw integer compiler does not implement these smaller-step trajectories.',
            'source_sha256':{str(Path(__file__).relative_to(ROOT)):hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}}
    (out/'sourced_refinement_report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    result=run(ROOT/'runs/team48/numerical')
    print(json.dumps(result['samples'],indent=2))
