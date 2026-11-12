"""Exact spatial constraint-tangent diagnosis and fixed-domain refinement.

No Engine evolution, production-law change or hidden constraint projection.
Fraction calculations are independent validation, not retained runtime state.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import numpy as np

from validation.geometry.team48.numerical_sign_validation import (
    MATTER_FIELDS, as_array, matter_builder, momentum_seed, sampled)

ROOT = Path(__file__).resolve().parents[3]


def derivative(row, dx):
    return [(row[(i+1) % len(row)]-row[(i-1) % len(row)])/(2*dx)
            for i in range(len(row))]


def product_defect(row, dx):
    d = derivative(row, dx)
    d2 = derivative([v*v for v in row], dx)
    return [a-2*b*c for a,b,c in zip(d2,row,d)]


def predicted_momentum_tangent(k, q, dx):
    return [-3*a-F(1,2)*b for a,b in
            zip(product_defect(k,dx), product_defect(q,dx))]


def verify_existing_fixture():
    y, seed = momentum_seed()
    rhs, constraints, _ = sampled(MATTER_FIELDS, matter_builder, y, 5)
    f = as_array(rhs, MATTER_FIELDS, 125)
    _, plus, _ = sampled(MATTER_FIELDS, matter_builder, y+f, 5)
    _, minus, _ = sampled(MATTER_FIELDS, matter_builder, y-f, 5)
    # All constraint polynomials have degree <=2. Symmetric difference in
    # field space is their exact directional derivative, with no small epsilon.
    tangent = {name: F(1,2)*(plus[name]-minus[name]) for name in constraints}
    k, q = [F(10),F(14),F(18),F(14),F(10)], [F(2),F(4),F(0),F(-4),F(-2)]
    prediction = predicted_momentum_tangent(k,q,F(1))
    from universe24.core.lattice import lattice
    x = lattice(5).all_coords()[:,0]
    assert all(tangent['M0'][n] == prediction[int(x[n])] for n in range(125))
    peaks={name: str(max(abs(v) for v in np.broadcast_to(row,(125,))))
           for name,row in tangent.items()}
    assert peaks['H']=='0' and peaks['M0']=='21'
    assert all(value=='0' for name,value in peaks.items() if name!='M0')
    return {'seed': seed, 'constraint_tangent_peaks': peaks,
            'independent_M0_tangent_profile': list(map(str,prediction)),
            'formula': '-3*(D(k*k)-2*k*D(k))-(D(q*q)-2*q*D(q))/2',
            'all_125_nodes_match_independent_defect_formula':True}


def fixed_domain_refinement():
    rows=[]
    # C3 periodic continuation, exact rational data on the same physical torus.
    # Continuum phi=256*x^4*(1-x)^4, k=phi+10, Pi=2. We set q=D_h phi
    # and dust=k^2-(4+q^2)/2, so the stated discrete initial constraints vanish.
    for L in (8,16,32,64,128,256):
        dx=F(1,L)
        phi=[256*(i*dx)**4*(1-i*dx)**4 for i in range(L)]
        k=[v+10 for v in phi]
        q=derivative(phi,dx)
        dust=[kk*kk-F(1,2)*(4+qq*qq) for kk,qq in zip(k,q)]
        assert min(dust)>0
        dk=derivative(k,dx)
        # Independent discrete Hamiltonian/momentum/gradient constraints.
        assert all(2*kk*kk-2*(F(1,2)*(4+qq*qq)+dd)==0
                   for kk,qq,dd in zip(k,q,dust))
        assert all(-2*d+2*qq==0 for d,qq in zip(dk,q))
        residual=predicted_momentum_tangent(k,q,dx)
        peak=max(map(abs,residual))
        rows.append({'L':L,'dx':str(dx),'fixed_physical_domain':'[0,1) periodic',
                     'minimum_dust':str(min(dust)), 'initial_H_M_gradient_zero':True,
                     'max_abs_M0_dot':str(peak),
                     'max_abs_M0_dot_decimal':float(peak),
                     'max_abs_M0_dot_over_dx_squared':str(peak/(dx*dx))})
    for earlier,later in zip(rows,rows[1:]):
        assert F(later['max_abs_M0_dot'])<F(earlier['max_abs_M0_dot'])
        later['refinement_ratio']=float(F(earlier['max_abs_M0_dot'])/F(later['max_abs_M0_dot']))
    assert 3.8<rows[-1]['refinement_ratio']<4.2
    return rows


def audit(out):
    report={'scope':'spatial truncation diagnosis and exact rational validation; not integer Engine refinement',
            'existing_fixture':verify_existing_fixture(),
            'fixed_domain_refinement':fixed_domain_refinement(),
            'interpretation':['The previous nonzero tangent is exactly two centered product-rule defects.',
                'For this fixed smooth physical family, the defect decreases quadratically under spatial refinement.',
                'The test does not demonstrate fixed-time convergence, stability, integer coefficient realization, or general constraint preservation.',
                'No projection, revised current, changed constraint threshold, or runtime correction is introduced.'],
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    result=audit(ROOT/'runs/team48/constraint_repair/spatial.json')
    print(json.dumps(result,indent=2))
