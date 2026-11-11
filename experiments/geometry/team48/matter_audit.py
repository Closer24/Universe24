"""Independent continuum/source audits for the research matter candidate.

Run from the repository root: python -m experiments.geometry.team48.matter_audit
No successful symbolic identity is a discrete conservation claim.
"""
import json
from pathlib import Path

import sympy as s

from .matter_equations import FIELDS_WITH_MAXWELL, equations, epsilon

A = range(3)


def audit():
    result = {}
    fields = {name: s.Symbol(name) for name in FIELDS_WITH_MAXWELL}
    derivatives = {(name, a): s.Symbol(f'd{a}_{name}') for name in fields for a in A}
    rhs, constraints, diagnostic = equations(fields, lambda name, a: derivatives[name, a], maxwell=True)
    all_symbols = tuple(fields.values()) + tuple(derivatives.values())
    result['full_physical_fields'] = len(fields)
    result['max_rhs_degree'] = max(s.Poly(s.expand(v), *all_symbols).total_degree() for v in rhs.values())
    assert result['full_physical_fields'] == 41 and result['max_rhs_degree'] == 2

    # Independent projections of covariant canonical scalar and Maxwell T.
    eta = s.diag(-1, 1, 1, 1)
    tensor = s.zeros(4)
    potential = sum(fields[name]**2 for name in ('phi', 'chi'))/2
    for name in ('phi', 'chi'):
        d = s.Matrix([fields[f'Pi_{name}'], *(fields[f'Psi_{name}{a}'] for a in A)])
        tensor += d*d.T - eta*(d.dot(eta*d)/2)
    tensor -= eta*potential
    tensor[0, 0] += fields['rho_dust']
    faraday = s.zeros(4)
    for a in A:
        faraday[0,a+1] = -fields[f'E{a}']
        faraday[a+1,0] = fields[f'E{a}']
        for b in A:
            faraday[a+1,b+1] = sum(epsilon(a,b,c)*fields[f'M{c}'] for c in A)
    invariant = sum(faraday[u,v]*(eta*faraday*eta)[u,v] for u in range(4) for v in range(4))
    tensor += faraday*eta*faraday.T - eta*invariant/4
    stress_residuals = [tensor[0,0]-diagnostic['rho']]
    stress_residuals += [-tensor[0,a+1]-diagnostic['momentum'][a] for a in A]
    stress_residuals += [tensor[a+1,b+1]-diagnostic['stress'][a][b] for a in A for b in A]
    assert all(s.expand(v) == 0 for v in stress_residuals)
    result['independent_covariant_stress_projection'] = True

    conjugation = {v: -v for name,v in fields.items() if name == 'chi' or name.startswith('Pi_chi') or name.startswith('Psi_chi')}
    invariant_components = [diagnostic['rho'], *diagnostic['momentum'], *(v for row in diagnostic['stress'] for v in row)]
    assert all(s.expand(v.xreplace(conjugation)-v) == 0 for v in invariant_components)
    assert s.expand(diagnostic['charge'].xreplace(conjugation)+diagnostic['charge']) == 0
    result['global_U1_conjugation_preserves_stress_reverses_charge'] = True

    # At any point choose an orthonormal spatial frame with Gamma=0. Its time
    # derivative remains Fermi, so arbitrary symmetric K must be retained.
    normal_frame = {v: s.Integer(int(name[1] == name[2])) for name,v in fields.items() if name.startswith('B')}
    normal_frame.update({v: s.Integer(0) for name,v in fields.items() if name.startswith('G')})
    spatial = {}
    for name in ('phi','chi'):
        for a in A:
            spatial[fields[name],a] = fields[f'Psi_{name}{a}']
            spatial[fields[f'Pi_{name}'],a] = s.Symbol(f'gradPi_{name}{a}')
            for b in A:
                spatial[fields[f'Psi_{name}{b}'],a] = s.Symbol(f'Hess_{name}{min(a,b)}{max(a,b)}')
    for name in [*(f'E{a}' for a in A), *(f'M{a}' for a in A)]:
        for a in A:
            spatial[fields[name],a] = s.Symbol(f'grad_{name}{a}')
    for a in A:
        spatial[fields['rho_dust'],a] = s.Symbol(f'grad_dust{a}')
    def derivative(expr,a):
        return sum(s.diff(expr,v)*dv for (v,direction),dv in spatial.items() if direction == a)
    jet_values = {derivatives[name,a]: spatial.get((value,a),s.Integer(0)) for name,value in fields.items() for a in A}
    temporal = {fields[name]: s.expand(value.xreplace(normal_frame).xreplace(jet_values)) for name,value in rhs.items() if not name.startswith(('B','K','G'))}
    def time_derivative(expr):
        return sum(s.diff(expr,v)*dv for v,dv in temporal.items())
    rho,j,stress = diagnostic['rho'],diagnostic['momentum'],diagnostic['stress']
    K = [[fields[f'K{min(a,b)}{max(a,b)}'] for b in A] for a in A]
    trace = sum(K[a][a] for a in A)
    energy = time_derivative(rho)+sum(derivative(j[a],a) for a in A)-trace*rho-sum(K[a][b]*stress[a][b] for a in A for b in A)
    assert s.expand(energy) == 0
    gauss_e = sum(spatial[fields[f'E{a}'],a] for a in A)
    gauss_m = sum(spatial[fields[f'M{a}'],a] for a in A)
    momentum = [time_derivative(j[a])+sum(derivative(stress[a][b],b) for b in A)-trace*j[a]-sum(K[a][b]*j[b] for b in A)
                + fields[f'E{a}']*gauss_e+fields[f'M{a}']*gauss_m for a in A]
    assert all(s.expand(v) == 0 for v in momentum)
    charge = diagnostic['charge']
    charge_flux = [fields['chi']*fields[f'Psi_phi{a}']-fields['phi']*fields[f'Psi_chi{a}'] for a in A]
    charge_residual = time_derivative(charge)-trace*charge+sum(derivative(charge_flux[a],a) for a in A)
    assert s.expand(charge_residual) == 0
    result['continuum_energy_identity'] = True
    result['continuum_momentum_identity_given_scalar_curl_and_Maxwell_Gauss'] = True
    result['continuum_global_U1_charge_identity'] = True

    # Two exact sourced Einstein solutions, independently substituted in every
    # evolution component and every returned constraint, with zero spatial jets.
    t = s.Symbol('t', positive=True)
    solutions = {}
    for model,power in [('normal_dust',s.Rational(2,3)),('massless_scalar',s.Rational(1,3))]:
        values = {name:s.Integer(0) for name in fields}
        for a in A:
            values[f'B{a}{a}'] = t**(-power)
            values[f'K{a}{a}'] = -power/t
        if model == 'normal_dust':
            values['rho_dust'] = s.Rational(4,3)/t**2
        else:
            values['phi'] = s.sqrt(s.Rational(2,3))*s.log(t)
            values['Pi_phi'] = s.sqrt(s.Rational(2,3))/t
        solution_rhs, solution_constraints, _ = equations(values,lambda name,a:s.Integer(0),mass_squared=0,maxwell=True)
        assert all(s.simplify(solution_rhs[name]-s.diff(values[name],t)) == 0 for name in fields)
        assert all(s.simplify(value) == 0 for value in solution_constraints.values())
        solutions[model] = {'all_evolution_residuals_zero':True,'all_constraint_residuals_zero':True}
    result['exact_flat_FLRW_solutions'] = solutions
    result['discrete_constraint_preservation_claimed'] = False
    result['general_tilted_dust_claimed'] = False
    result['electromagnetically_gauged_scalar_claimed'] = False
    return result


if __name__ == '__main__':
    report = audit()
    folder = Path('runs/team48/matter')
    folder.mkdir(parents=True,exist_ok=True)
    (folder/'symbolic_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
