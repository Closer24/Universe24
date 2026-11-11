"""Separate continuum leapfrog convergence from raw-integer accessibility.

A scalar floating reference follows exact Milne data B00=1/t,K00=-1/t.
This is deliberately NOT an Engine trajectory or an integer resolution
hierarchy. The actual compiled h=dx=1/2 case is checked separately against it.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from universe24.layers.frame48 import compile_frame48
from universe24.algebra.frame_equations import FIELDS,equations
from experiments.geometry.team48.integer_sign_lift import compile_quadratic
from experiments.geometry.team48.numerical_milne import run as actual_milne


def run(out):
    out=Path(out); out.mkdir(parents=True,exist_ok=True)
    actual=actual_milne(out)
    rows=[]
    for denominator in (2,4,8,16,32,64,128,256):
        step=F(1,denominator)
        previous,current=float(1/(1-step)),1.0
        peak_error=0.0;minimum=current
        # Fixed physical interval [1,2], exact time-consistent starting pair.
        for n in range(1,denominator+1):
            previous,current=current,previous-2*float(step)*current*current
            minimum=min(minimum,current)
            peak_error=max(peak_error,abs(current-1/(1+n*float(step))))
        accessibility={}
        for label,builder in [('old48',lambda:compile_frame48(dt=step,dx=step)),
                              ('sign25',lambda:compile_quadratic(FIELDS,equations,dt=step,dx=step))]:
            try:
                builder()
                accessibility[label]={'compiles':True}
            except ValueError as exc:
                accessibility[label]={'compiles':False,'reason':str(exc)}
        rows.append({'h_and_dx':str(step),'reference_kind':'floating scalar leapfrog; not Engine',
                     'exact_previous_B00':str(1/(1-step)),
                     'previous_value_is_raw_integer':(1/(1-step)).denominator==1,
                     'B00_at_t2':current,'exact_B00_at_t2':0.5,
                     'endpoint_absolute_error':abs(current-0.5),
                     'peak_B00_error':peak_error,'minimum_B00_over_interval':minimum,
                     'raw_integer_compile':accessibility})
    assert rows[0]['B00_at_t2']==0.0
    assert actual['samples'][2]['B00']==0
    assert all(row['minimum_B00_over_interval']>0 for row in rows[1:])
    assert all(rows[i+1]['peak_B00_error']<rows[i]['peak_B00_error'] for i in range(len(rows)-1))
    assert all(not row['raw_integer_compile']['sign25']['compiles'] for row in rows[1:])
    for i in range(1,len(rows)):
        rows[i]['peak_error_reduction_from_previous']=rows[i-1]['peak_B00_error']/rows[i]['peak_B00_error']
    report={'scope':'Continuum time-refinement control contrasted with the accessible raw-integer sector',
            'same_physical_problem':'Exact Milne slices at1-h and1; evolve to2, ds²=-dt²+t²dx²+dy²+dz²',
            'joint_refinement_is_formal_for_homogeneous_solution':'dx=h; spatial derivatives vanish',
            'actual_engine_only_at_h':'1/2', 'samples':rows,
            'conclusion':'Smaller steps remove the coarse Milne degeneracy and approach the continuum. The current raw-field integer compilers and initial-data encoding cannot realize this family; no convergent integer Einstein hierarchy is demonstrated.',
            'source_sha256':{str(Path(__file__).relative_to(ROOT)):hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}}
    (out/'milne_refinement_report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    result=run(ROOT/'runs/team48/numerical')
    print(json.dumps([{'h':r['h_and_dx'],'error':r['endpoint_absolute_error'],
                       'minimum_B':r['minimum_B00_over_interval'],
                       'integer_sign25_compiles':r['raw_integer_compile']['sign25']['compiles']} for r in result['samples']],indent=2))
