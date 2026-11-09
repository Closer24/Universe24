#!/usr/bin/env python3
"""Worker 3: independent Einstein PPN, causal graph, finite-lattice tensor gates."""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
from universe24.core.coupling import Coupling
from universe24.core.group_2o import DIRECTIONS, group

ROOT=Path(__file__).resolve().parent;OUT=ROOT/'results';OUT.mkdir(exist_ok=True)

def scalar_spectrum():
    rows=[]
    for q in (0.04,0.08,0.16,0.32,0.64):
        ka=(q,0.,0.); kd=(q/math.sqrt(3),)*3
        lamA=6-2*sum(math.cos(k) for k in ka)
        lamD=6-2*sum(math.cos(k) for k in kd)
        rows.append({'abs_k':q,'L_axis':lamA,'L_diagonal':lamD,'axis_minus_diagonal':lamA-lamD,
                     'difference_over_q4':(lamA-lamD)/q**4})
    return {'exact_symbol':'Lsc(k)=6-2[cos(kx)+cos(ky)+cos(kz)]',
            'quartic_expansion':'Lsc(k)=|k|^2-(kx^4+ky^4+kz^4)/12+O(k^6)',
            'axis_minus_equal_length_body_diagonal_coefficient':'-1/18 at order |k|^4',
            'samples':rows,'interpretation':'cubic anisotropy at finite k, isotropy possible only as long-wavelength limit'}

def causal_graph():
    # Every evolving address sees its old local state and six spatial neighbors;
    # minimal spatial causal graph distance from all 48 source labels to any target
    # site equals Manhattan norm (for sites below torus wrap radius).
    c=Coupling();L=23;start=(11,11,11)
    cover={(start[0],start[1],start[2],g) for g in range(48)}
    visited=set(cover)
    steps={start:0}
    for t in range(1,7):
        nxt=set()
        for x,y,z,g in cover:
            for k,(dx,dy,dz) in enumerate(DIRECTIONS):
                nxt.add(((x+dx)%L,(y+dy)%L,(z+dz)%L,c.ports[k][g]))
        cover=nxt-visited
        visited|=cover
        for x,y,z,g in cover:steps.setdefault((x,y,z),t)
    samples=[]
    for disp in ((1,0,0),(1,1,0),(1,1,1),(2,0,0),(2,2,0),(2,2,2),(3,0,0),(3,1,2)):
        target=tuple(start[i]+disp[i] for i in range(3))
        assert steps[target]==sum(disp)
        samples.append({'displacement':disp,'euclidean_length':math.sqrt(sum(x*x for x in disp)),
                        'minimum_graph_update_count':steps[target],
                        'maximum_graph_euclidean_speed_per_update':round(math.sqrt(sum(x*x for x in disp))/steps[target],8)})
    return {'samples':samples,'claim':'minimal possible spatial edge count, not photon speed; local state can also persist at sites',
            'graph_exact_isotropic_lorentz':False,'low_energy_isotropic_limit_not_excluded':True}

def redshift_vs_schwarzschild():
    observed={1:0.8,3:1.,4:1.,5:1.,6:1.}
    # Calibrate in a chart as if far clock at infinity; EXPLICITLY unphysical normalization assumption.
    q=(1-observed[1])/(1+observed[1]);r=[]
    for d,Nobs in observed.items():
        sch=(1-q/d)/(1+q/d)
        r.append({'r_lattice':d,'observed_recurrence_ratio_to_far':Nobs,
                  'schwarzschild_isotropic_N_if_assume_r1_infinity_normalization':sch,
                  'absolute_discrepancy':abs(Nobs-sch)})
    # More defensible calibration with finite reference r=6: find q such that N(1)/N(6)=0.8.
    def normal_N(rad,s):return (1-s/rad)/(1+s/rad)
    lo,hi=0.,.99
    for _ in range(100):
        mid=(lo+hi)/2
        val=normal_N(1,mid)/normal_N(6,mid)
        if val>0.8:lo=mid
        else:hi=mid
    qfinite=(lo+hi)/2
    fit=[{'r':d,'observed':observed[d],
          'predicted_N_over_N6':normal_N(d,qfinite)/normal_N(6,qfinite),
          'absolute_difference':abs(observed[d]-normal_N(d,qfinite)/normal_N(6,qfinite))} for d in observed]
    return {'comparison_is_hypothetical_only':True,'reason':'recurrence periods are not operational proper times and lattice distance not calibrated isotropic radius',
            'observed_clock_ratios':observed,'fitted_schwarzschild_q_at_r1_r6':qfinite,
            'same_mass_parameter_predicts_unperturbed_r3_clock_incorrectly':fit,
            'pinned_finite_radius_reference':6,
            'strong_field_q_for_infinity_normalization':q,
            'infinity_normalization_samples':r}

def zero_momentum_internal_spectrum():
    """Exact 48x48 characteristic polynomial, not a physical graviton spectrum."""
    import sympy as sp
    C=Coupling();A=sp.zeros(48)
    for d in range(6):A+=sp.Matrix(C.matrix(d))
    lam=sp.symbols('lam')
    factored=sp.factor(A.charpoly(lam).as_expr())
    target=(lam**8*(lam-6)*(lam-4)**8*(lam-2)**14*(lam+2)*(lam**2-4*lam-2)**8)
    assert sp.expand(factored-target)==0
    # The scalar constant is the unique top eigendirection.
    assert A*sp.ones(48,1)==6*sp.ones(48,1)
    # The traceless symmetric all-channel orbit has no overlap with uniform scalar.
    R=group().rotations
    diag=[]
    for i in range(3):
        diag.append([sum(R[g][i][j]*v[j] for j in range(3))**2-2 for g in range(48) for v in [(1,1,2)]])
    assert all(sum(v)==0 for v in diag)
    return {'all48_exact_characteristic_polynomial':str(factored),
            'internal_zero_momentum_eigenvalues':{'6':1,'-2':1,'2':14,'0':8,'4':8,'2+sqrt(6)':8,'2-sqrt(6)':8},
            'unique_lambda6_multiplicity':1,
            'nearest_nontrivial_lambda':'2+sqrt(6)',
            'spectral_gap_to_6':float(4-sp.sqrt(6)),
            'frozen_remainder_comparison_only_min_internal_frequency_radians_per_update':math.acos((2+math.sqrt(6))/6),
            'traceless_diagonal_spin2_readouts_orthogonal_to_uniform':True,
            'claim':'No gapless nonuniform internal/tensor mode in this homogeneous frozen-remainder comparison at zero momentum; does not exclude nonperturbative emergent spin-2 geometry.'}

def schwarzschild_isotropic_target():
    """Exact external Schwarzschild clock/null relation in isotropic radius, purely GR target."""
    import sympy as sp
    N=sp.symbols('N',positive=True)
    q=(1-N)/(1+N)
    H=(1+q)**2
    v=sp.factor(N/H)
    assert sp.simplify(v-N*(1+N)**2/4)==0
    n=sp.Rational(4,5)
    return {'model_fit':False,'premise':'Schwarzschild exterior isotropic coordinate with N(infinity)=1, not measured in the automaton',
            'N':'(1-q)/(1+q)','q':'GM/(2c^2 rho)','H':'(1+q)^2',
            'exact_physical_coordinate_null_speed_from_lapse':'v_null/c=N*(1+N)^2/4',
            'illustrative_at_N_four_fifths':{'H':str(H.subs(N,n)),'v_null_over_c':str(v.subs(N,n)),
                                            'warning':'N=4/5 is a recurrence-rate analogy only, not an operational GR lapse'}}

def ppn_crosscheck():
    # N~1-U, H~1+gamma U, so physical-null coordinate speed N/H~1-(1+gamma)U
    strengths=[1e-4,2e-4,5e-4,1e-3]
    rows=[]
    for U in strengths:
        N=1-U;H=1+U
        alpha=math.log(N/H)/math.log(N)
        rows.append({'U_over_c2':U,'N':N,'H_gamma1':H,'physical_null_speed_over_c_gamma1':N/H,'finite_log_slope':alpha})
    return {'weak_field_GR_requires_gamma':1,'alpha_limit':2,
            'without_spatial_metric_H_or_physical_null_cone_gamma_is_unidentifiable':True,
            'baseline_tests':rows,
            'flat_space_nonconstant_lapse_counterexample':'Rindler: ds^2=-(1+g*x)^2dt^2+dx^2+dy^2+dz^2 has nonconstant rate N but zero Riemann curvature where N>0',
            'conformal_static_vacuum_gate':'if g=N^2 eta and Einstein Gmunu=0,Lambda=0 then 3*|grad ln N|^2 = sum_i Gii +2 G00 =0, hence N constant'}

def run():
    report={'worker':'C_Einstein_operational_and_dispersion','status':'PASS',
            'einstein_metric':ppn_crosscheck(),
            'exact_schwarzschild_target':schwarzschild_isotropic_target(),
            'cubic_dispersion':scalar_spectrum(),
            'full48_internal_spectrum':zero_momentum_internal_spectrum(),
            'microscopic_causal_graph':causal_graph(),
            'clock_distance_comparison':redshift_vs_schwarzschild(),
            'science_scope':'A fitted recurrence-rate snapshot does not determine physical N; tests are necessary conditions and conditional counterexamples, not extraction of GR parameters.'}
    path=OUT/'worker3_einstein.json';path.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'worker':report['worker'],'status':report['status'],'qfit':report['clock_distance_comparison']['fitted_schwarzschild_q_at_r1_r6'],'path':str(path)}),flush=True)
    return report

if __name__=='__main__':run()
