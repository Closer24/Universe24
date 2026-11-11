"""Charged matter and PR39 square-dust independent exact checks.

Run: python -m experiments.geometry.team48.matter_charged_audit
This is not a discrete Einstein-constraint preservation certificate.
"""
import json
from pathlib import Path

import numpy as np
import sympy as s

from universe24.algebra import frame_matter as pr39
from universe24.core import Engine
from universe24.core.lattice import lattice
from . import geometry_triangular as triangular
from . import matter_charged as charged
from . import matter_dust_square as square
from .integer_sign_lift import compile_quadratic,prepare,physical_slices
from .matter_equations import epsilon

A = range(3)


def continuum_checks():
    v = {n:s.Symbol(n) for n in charged.FIELDS}
    ds = {(n,a):s.Symbol(f'd{a}_{n}') for n in v for a in A}
    rhs,_,diag = charged.equations(v,lambda n,a:ds[n,a])
    normal = {v[n]:s.Integer(int(n[1] == n[2])) for n in v if n.startswith('B')}
    normal.update({v[n]:s.Integer(0) for n in v if n.startswith('G') or (n.startswith('A') and len(n) == 2)})
    # A can be gauged to zero at this one point. The independently checked
    # Xi curl compatibility retains the nonzero electromagnetic curvature.
    spatial = {}
    for component,name in enumerate(('phi','chi')):
        other,sign = 1-component,(-1 if component == 0 else 1)
        for a in A:
            spatial[v[name],a] = v[f'Xi_{name}{a}']
            spatial[v[f'Pi_{name}'],a] = s.Symbol(f'gradPi_{name}{a}')
            for b in A:
                faraday = sum(epsilon(a,b,d)*v[f'M{d}'] for d in A)
                spatial[v[f'Xi_{name}{b}'],a] = s.Symbol(f'Hess_{name}{min(a,b)}{max(a,b)}')-faraday*sign*v[('phi','chi')[other]]/2
    for name in [*(f'E{a}' for a in A),*(f'M{a}' for a in A)]:
        for a in A:
            spatial[v[name],a] = s.Symbol(f'grad_{name}{a}')
    for a in A:
        spatial[v['rho_dust'],a] = s.Symbol(f'grad_dust{a}')

    def derivative(expr,a):
        return sum(s.diff(expr,value)*change for (value,b),change in spatial.items() if a == b)

    jets = {ds[n,a]:spatial.get((value,a),s.Integer(0)) for n,value in v.items() for a in A}
    temporal = {v[n]:s.expand(value.xreplace(normal).xreplace(jets)) for n,value in rhs.items() if not n.startswith(('B','K','G','A'))}

    def time_derivative(expr):
        return sum(s.diff(expr,value)*change for value,change in temporal.items())

    rho,j,stress = diag['rho'],diag['momentum'],diag['stress']
    K = [[v[f'K{min(a,b)}{max(a,b)}'] for b in A] for a in A]
    trace = sum(K[a][a] for a in A)
    energy = time_derivative(rho)+sum(derivative(j[a],a) for a in A)-trace*rho-sum(K[a][b]*stress[a][b] for a in A for b in A)
    gauss_e = sum(spatial[v[f'E{a}'],a] for a in A)
    gauss_m = sum(spatial[v[f'M{a}'],a] for a in A)
    momentum = [time_derivative(j[a])+sum(derivative(stress[a][b],b) for b in A)-trace*j[a]-sum(K[a][b]*j[b] for b in A)
                +v[f'E{a}']*(gauss_e-diag['electric_charge'])+v[f'M{a}']*gauss_m for a in A]
    charge = time_derivative(diag['electric_charge'])-trace*diag['electric_charge']+sum(derivative(diag['electric_current'][a],a) for a in A)
    assert s.expand(energy) == s.expand(charge) == 0
    assert all(s.expand(value) == 0 for value in momentum)
    conjugation = {value:-value for name,value in v.items() if name == 'chi' or name.startswith(('Pi_chi','Xi_chi','E','M','A'))}
    stress_components = [rho,*j,*(value for row in stress for value in row)]
    assert all(s.expand(value.xreplace(conjugation)-value) == 0 for value in stress_components)
    assert all(s.expand(value.xreplace(conjugation)+value) == 0 for value in [diag['electric_charge'],*diag['electric_current']])
    return {'combined_energy_identity':True,'combined_momentum_identity_given_covariant_curl_and_Gauss':True,
            'electric_charge_continuity':True,'charge_conjugation_preserves_stress_reverses_charge_and_current':True}


def pr39_comparison():
    v = {name:s.Symbol(name) for name in square.FIELDS}
    ds = {(name,a):s.Symbol(f'd{a}_{name}') for name in v for a in A}
    rhs,constraints,diag = square.equations(v,lambda name,a:ds[name,a])
    mapping = {'Pi':'Pi_phi',**{f'Q{a}':f'Psi_phi{a}' for a in A},**{f'W{a}':f'Psi_chi{a}' for a in A}}
    original = {name:v[mapping.get(name,name)] for name in pr39.FIELDS}
    old_rhs,old_constraints,old_diag = pr39.equations(original,lambda name,a:ds[mapping.get(name,name),a])
    assert all(s.expand(value-rhs[mapping.get(name,name)]) == 0 for name,value in old_rhs.items())
    assert all(s.expand(value-constraints[name]) == 0 for name,value in old_constraints.items() if name in constraints)
    assert s.expand(diag['rho']-old_diag['rho']) == 0
    assert all(s.expand(diag['momentum'][a]-old_diag['j'][a]) == 0 for a in A)
    assert all(s.expand(diag['stress'][a][b]-old_diag['S'][a][b]) == 0 for a in A for b in A)
    amplitude = v['dust_amplitude']
    trace = sum(v[f'K{a}{a}'] for a in A)
    assert s.expand(2*amplitude*rhs['dust_amplitude']-trace*amplitude**2) == 0
    return {'all_35_rhs_identical_under_field_renaming':True,'shared_constraints_and_stress_identical':True,
            'continuum_squared_dust_continuity':True,'pr39_head':'35344a1ba5c12c857404115e893911411ece7d35'}


def charged_builder(fields,partial):
    return triangular.equations(fields,partial,fermi_equations=square.equations,
                                base_equations=charged.equations,mass_squared=0)


def engine_checks():
    names = tuple(triangular.FIELDS)+tuple(name for name in square.FIELDS_CHARGED if name not in charged.neutral.GEOMETRY_FIELDS)
    program = compile_quadratic(names,charged_builder)
    lat = lattice(3)
    initial = np.zeros((len(names),lat.N),dtype=object)
    for a in A:
        initial[names.index(f'B{a}{a}')] = 1
    # This algebraic interaction fixture is explicitly not constrained GR data.
    # It has nonzero charge and current, and conjugate matter has the same T.
    settings = {'phi':2,'chi':1,'Pi_phi':1,'Pi_chi':3,
                'Xi_phi0':1,'Xi_chi0':2,'E0':1,'M1':2,'A2':1,
                'dust_amplitude':1,'K00':-2}
    for name,value in settings.items():
        initial[names.index(name)] = value
    conjugate = initial.copy()
    signs = np.array([-1 if name == 'chi' or name.startswith(('Pi_chi','Xi_chi','E','M','A')) else 1 for name in names],dtype=object)
    conjugate *= signs[:,None]
    state = prepare(program,initial,initial,L=3)
    conjugate_state = prepare(program,conjugate,conjugate,L=3)
    engine = Engine(program.tensor)
    evolved = engine.step(state)
    evolved_conjugate = engine.step(conjugate_state)
    _,physical = physical_slices(program,evolved)
    _,conjugated_physical = physical_slices(program,evolved_conjugate)
    np.testing.assert_array_equal(conjugated_physical,signs[:,None]*physical)
    assert engine.inverse_step(evolved).same_as(state)
    assert all(value == -1 for value in physical[names.index('dust_amplitude')])
    fields = dict(zip(names,initial))
    rhs,constraints,diag = charged_builder(fields,lambda name,a:np.zeros(lat.N,dtype=object))
    np.testing.assert_array_equal(physical,initial+2*np.array([rhs[name] for name in names],dtype=object))
    assert int(diag['electric_charge'][0]) == -5
    assert int(diag['electric_current'][0][0]) == 3
    # E0 evolves with an explicit -current contribution relative to deleting it.
    assert int(physical[names.index('E0'),0]-initial[names.index('E0'),0]) == -6
    constrained = np.zeros_like(initial)
    for a in A:
        constrained[names.index(f'B{a}{a}')] = 1
    for name,value in {'K00':1,'K11':1,'K22':2,'phi':2,'A1':1,
                       'Xi_chi1':-2,'E1':2,'dust_amplitude':1}.items():
        constrained[names.index(name)] = value
    _,initial_constraints,initial_diagnostic = charged_builder(
        dict(zip(names,constrained)),lambda name,a:np.zeros(lat.N,dtype=object))
    assert all(all(value == 0 for value in np.asarray(row,dtype=object).flat)
               for row in initial_constraints.values())
    constrained_state = prepare(program,constrained,constrained,L=3)
    constrained_after = engine.step(constrained_state)
    _,constrained_physical = physical_slices(program,constrained_after)
    _,after_constraints,_ = charged_builder(dict(zip(names,constrained_physical)),
                                            lambda name,a:np.zeros(lat.N,dtype=object))
    assert int(initial_diagnostic['electric_current'][1][0]) == -4
    assert int(after_constraints['H'][0]) == -314
    assert engine.inverse_step(constrained_after).same_as(constrained_state)
    return {'physical_fields':len(names),'channels':program.tensor.G,'integer_engine_matches_complete_rhs':True,
            'integer_engine_charge_conjugation_commutes':True,'integer_engine_exact_inverse':True,
            'nonzero_initial_electric_charge':-5,'nonzero_initial_electric_current_x':3,
            'electric_field_current_contribution_after_one_step':-6,
            'signed_dust_crosses_plus_one_to_minus_one':True,'dust_density_stays_one':True,
            'fixture_is_constrained_Einstein_data':False,
            'initial_H':str(constraints['H'][0]),'initial_Gauss_E':str(constraints['Gauss_E'][0]),
            'additional_constrained_current_fixture':{
                'initial_all_reported_constraints_zero':True,'initial_density':str(initial_diagnostic['rho'][0]),
                'initial_electric_current_y':-4,'after_one_step_H':str(after_constraints['H'][0]),
                'after_one_step_electric_y':str(constrained_physical[names.index('E1'),0]),
                'exact_inverse':True,'previous_slice_repeated_not_a_verified_history':True}}


def audit():
    report = {'continuum':continuum_checks(),'PR39_comparison':pr39_comparison(),'actual_engine':engine_checks(),
              'discrete_constraint_preservation_claimed':False,'arbitrary_integer_refinement_claimed':False,
              'Dirac_or_annihilation_model_claimed':False}
    folder = Path('runs/team48/matter')
    folder.mkdir(parents=True,exist_ok=True)
    (folder/'charged_square_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__ == '__main__':
    print(json.dumps(audit(),indent=2))
