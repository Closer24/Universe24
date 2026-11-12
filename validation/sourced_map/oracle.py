"""Independent proper-time oracle for the joined homogeneous sourced map.

The reference integrates the original five physical ODEs. It never advances
Engine state. Native comparisons read real macro boundaries at a declared
proper time; exact massless sampling is not called an infinite-order method.
"""
from __future__ import annotations

from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import mpmath as mp
import numpy as np
import sympy as sp

from universe24.core import Engine
from universe24.system.bundle import canonical_bytes

ROOT = Path(__file__).resolve().parents[2]
BASE_PIN = 'f4f64e062f07b3ca119eccf655df746be206908b'
PHYSICAL_FIELDS = ('B', 'k', 'p', 'phi', 'dust')
TIME = F(1, 8)
RESOLUTIONS = (24, 48, 96)
FIXTURES = (
    {'name': 'mixed_expanding', 'V': F(1), 'U': F(3), 'D': 1, 'P': 2},
    {'name': 'negative_scalar_charge', 'V': F(1), 'U': F(3), 'D': 1, 'P': -2},
    {'name': 'mixed_contracting', 'V': F(1), 'U': F(-3), 'D': 1, 'P': 2},
    {'name': 'pure_dust', 'V': F(1), 'U': F(3), 'D': 3, 'P': 0},
    {'name': 'stronger_scalar', 'V': F(1), 'U': F(27), 'D': 1, 'P': 22},
    {'name': 'stronger_dust', 'V': F(1), 'U': F(6), 'D': 10, 'P': 2},
)


def number(value):
    if isinstance(value, F):
        return mp.mpf(value.numerator)/value.denominator
    if isinstance(value, (int, np.integer)):
        return mp.mpf(int(value))
    if isinstance(value, str) and '/' in value:
        return number(F(value))
    return mp.mpf(value)


def text_number(value):
    return mp.nstr(value, 45)


def physical_constraint(y, mass_squared=0):
    B, k, p, phi, dust = y
    return 6*k*k-p*p-mass_squared*phi*phi-2*dust*dust


def independent_rhs(y, mass_squared=0):
    """FLRW/neutral scalar/dust, c=8*pi*G=1, lapse=1, B=1/a, k=-H.

    This implementation deliberately does not call the map, compiled tensor,
    continuum production RHS, or the massless analytic solution.
    """
    B, k, p, phi, dust = y
    return (k*B, 3*k*k-(mass_squared*phi*phi+dust*dust)/2,
            3*k*p-mass_squared*phi, p, 3*k*dust/2)


def symbolic_equations():
    B, k, p, phi, d, mu = sp.symbols('B k p phi d mu', real=True)
    fields = (B, k, p, phi, d)
    rhs = independent_rhs(fields, mu)
    C = physical_constraint(fields, mu)
    Cdot = sp.expand(sum(sp.diff(C, x)*v for x, v in zip(fields, rhs)))
    assert sp.expand(Cdot-6*k*C) == 0
    rho = (p*p+mu*phi*phi)/2+d*d
    pressure = (p*p-mu*phi*phi)/2
    rhodot = sp.expand(sum(sp.diff(rho, x)*v for x, v in zip(fields, rhs)))
    assert sp.expand(rhodot-3*k*(rho+pressure)) == 0
    assert sp.expand(rhs[1]-(p*p+d*d)/2-C/2) == 0
    V = B**-3
    U = -3*k*V
    P, D = p*V, d*d*V
    derivative = lambda z: sp.factor(sum(sp.diff(z, x)*v for x, v in zip(fields, rhs)))
    assert sp.simplify(derivative(V)-U) == 0
    assert sp.simplify(derivative(P).subs(mu, 0)) == 0
    assert sp.simplify(derivative(D)) == 0
    # This volume equation is exact even off the massless constraint surface;
    # imposing Q=0 selects the physical Einstein solution family initially.
    assert sp.simplify(derivative(U)-3*D/2-3*mu*phi*phi*V/2) == 0
    assert sp.simplify((U*U-sp.Rational(3,2)*P*P-3*D*V)-sp.Rational(3,2)*V*V*C).subs(mu, 0) == 0
    # Compare to the actual existing full continuum builder only after deriving
    # the independent equations; the numerical oracle below never calls it.
    from validation.completion import formulation
    source = {name: sp.Integer(0) for name in formulation.FIELDS}
    for j in range(3):
        source[f'B{j}{j}'], source[f'K{j}{j}'] = B, k
    source.update(phi=phi, Pi_phi=p, dust_amplitude=d)
    actual, constraints, _ = formulation.equations(source, lambda *_: sp.Integer(0), mass_squared=1)
    names = ('B00', 'K00', 'Pi_phi', 'phi', 'dust_amplitude')
    assert all(sp.simplify(actual[n]-r.subs(mu, 1)) == 0 for n, r in zip(names, rhs))
    assert sp.expand(constraints['H']-C.subs(mu, 1)) == 0
    return {'physical_field_order': list(PHYSICAL_FIELDS),
            'units': 'c=1, 8*pi*G=1, lapse=1, shift=0; tau is proper time of homogeneous normal observers',
            'B_equation': 'Bdot=k*B; a=1/B, H=-k',
            'k_equation': 'kdot=3*k^2-(mu*phi^2+dust^2)/2',
            'scalar_equations': 'phidot=p; pdot=3*k*p-mu*phi',
            'dust_equation': 'dustdot=3*k*dust/2',
            'constraint': 'C=6*k^2-p^2-mu*phi^2-2*dust^2; Cdot=6*k*C',
            'continuity_equation': 'rhodot=3*k*(rho+pressure)',
            'matches_existing_full_builder_at_mu1': True,
            'massless_invariants': 'V=B^(-3), U=-3*k*V, P=p*V, D=dust^2*V; Pdot=Ddot=0, Vdot=U',
            'massless_volume_equation': 'Udot=3*D/2, including the off-constraint massless extension',
            'massive_volume_equation': 'Udot=3*D/2+3*mu*phi^2*V/2',
            'constraint_equivalence_mu0': 'Q=U^2-3*P^2/2-3*D*V=(3/2)*V^2*C'}


def initial_physical(fixture):
    V, U, P, D = (number(fixture[key]) for key in ('V', 'U', 'P', 'D'))
    return (V**(-mp.mpf(1)/3), -U/(3*V), P/V, mp.mpf(0), mp.sqrt(D/V))


def rk4(initial, time, steps, mass_squared=0):
    h = number(time)/steps
    y = tuple(number(x) for x in initial)
    for _ in range(steps):
        k1 = independent_rhs(y, mass_squared)
        k2 = independent_rhs(tuple(x+h*v/2 for x,v in zip(y,k1)), mass_squared)
        k3 = independent_rhs(tuple(x+h*v/2 for x,v in zip(y,k2)), mass_squared)
        k4 = independent_rhs(tuple(x+h*v for x,v in zip(y,k3)), mass_squared)
        y = tuple(x+h*(v1+2*v2+2*v3+v4)/6 for x,v1,v2,v3,v4 in zip(y,k1,k2,k3,k4))
    return y


def high_precision_reference(initial, time=TIME, mass_squared=0, dps=80):
    """80-decimal arithmetic plus time-step halving; no rigorous interval claim."""
    with mp.workdps(dps):
        levels = (256, 512, 1024)
        values = [rk4(initial, time, n, mass_squared) for n in levels]
        differences = [max(abs(a-b) for a,b in zip(left,right))
                       for left,right in zip(values, values[1:])]
        # Extrapolation is a passive high-accuracy reference, never native state.
        extrapolated = tuple(b+(b-a)/15 for a,b in zip(values[-2], values[-1]))
        return extrapolated, {'precision_decimal_digits': dps, 'method': 'independent RK4 with step halving and Richardson endpoint extrapolation',
                'proper_final_time': str(F(time)), 'steps': list(levels),
                'endpoint_step_differences': list(map(text_number, differences)),
                'observed_reference_difference_ratio': text_number(differences[0]/differences[1]) if differences[1] else None,
                'last_step_difference_over_15': text_number(differences[-1]/15),
                'error_estimate_kind': 'step-halving estimate, not a rigorous interval enclosure',
                'physical_endpoint': {n:text_number(v) for n,v in zip(PHYSICAL_FIELDS,extrapolated)},
                'endpoint_constraint': text_number(physical_constraint(extrapolated,mass_squared))}


def exact_massless(fixture, time):
    """Independent integral in proper time, including pure dust and scalar branches."""
    t = number(time)
    v0,u0,P,D = (number(fixture[key]) for key in ('V','U','P','D'))
    v = v0+u0*t+3*D*t*t/4
    u = u0+3*D*t/2
    if v <= 0:
        raise ValueError('outside positive-volume proper-time chart')
    if not P:
        phi = mp.mpf(0)
    elif not D:
        if not u0:
            raise ValueError('nonzero scalar charge with zero vacuum volume velocity')
        phi = P/u0*mp.log(v/v0)
    else:
        # Integral P dt/(v0+u0*t+3D*t²/4), independently parameterized
        # by the quadratic discriminant, not the compiler's stored Uref.
        disc = u0*u0-3*D*v0
        if disc <= 0:
            raise ValueError('this constrained nonzero-P branch has positive discriminant')
        root = mp.sqrt(disc)
        ratio = ((u-root)/(u+root))*((u0+root)/(u0-root))
        phi = P/root*mp.log(abs(ratio))
    return (v**(-mp.mpf(1)/3), -u/(3*v), P/v, phi, mp.sqrt(D/v))


def independent_readout(conserved):
    """Decode observed retained coordinates, not an expected trajectory or projection."""
    V,U,P,D,Uref,offset = (number(conserved[k]) for k in ('V','U','P','D','Uref','phi_ref'))
    if V <= 0 or D < 0:
        raise ValueError('positive V and nonnegative dust D required')
    if P == 0:
        phi = offset
    elif D > 0:
        root = mp.sqrt(mp.mpf(3)/2)*abs(P)
        phi = offset+P/root*mp.log(abs((U-root)*(Uref+root)/((U+root)*(Uref-root))))
    else:
        raise ValueError('native exact rational nonzero pure-scalar branch is unsupported')
    return (V**(-mp.mpf(1)/3), -U/(3*V), P/V, phi, mp.sqrt(D/V))


def raw_conserved(program, state, N):
    ids = {name: program.tensor.gear_index(name) for name in program.tensor.names}
    # Direct register arithmetic is independent of native.read_conserved.
    W = ids['volume']
    D,P = int(state.b[ids['dust_charge'],0]), int(state.b[ids['scalar_charge'],0])
    V = F(int(state.b[W,0]),4*N*N)
    U = F(int(state.b[W,0])-int(state.a[W,0])+3*D,4*N)
    return {'V':V,'U':U,'D':F(D),'P':F(P),
            'Uref':F(int(state.b[ids['reference_velocity'],0]),4*N),
            'phi_ref':F(int(state.b[ids['scalar_offset'],0])),
            'tau':F(int(state.b[ids['proper_tick'],0]),N),
            'invariant':F((int(state.b[W,0])-int(state.a[W,0])+3*D)**2
                          -12*D*int(state.b[W,0])-24*N*N*P*P)}


def native_refinement(fixture, reference):
    from validation.sourced_map import native
    from validation.sourced_map.physical_map import physical_decode
    if fixture['P'] == 0 or fixture['U'] <= 0:
        rejected = {}
        program = native.build_native(RESOLUTIONS[0])
        try:
            native.prepare_native(program,L=3,V=fixture['V'],U=fixture['U'],D=fixture['D'],P=fixture['P'])
        except ValueError as error:
            rejected['native_preparation'] = str(error)
        else:
            raise AssertionError('An out-of-chart fixture entered native preparation')
        conserved = {key:fixture[key] for key in ('V','U','D','P')}
        conserved.update(Uref=fixture['U'],phi_ref=F(0),tau=F(0))
        try:
            physical_decode(conserved,mass_squared=0,precision=80)
        except ValueError as error:
            rejected['selected_physical_decoder'] = str(error)
        else:
            raise AssertionError('An out-of-chart fixture entered selected readout')
        return {'fixture':fixture['name'],'status':'blocked: outside selected expanding mixed native chart',
                'actual_rejections':rejected,'resolutions':[],
                'scope':'Independent analytic/numerical continuum control only; no native physical success claimed'}
    rows = []
    resolutions = (48,96,192) if fixture['name'] == 'stronger_scalar' else RESOLUTIONS
    coarse_rejection = None
    if fixture['name'] == 'stronger_scalar':
        try:
            native.prepare_native(native.build_native(24),L=3,V=fixture['V'],U=fixture['U'],D=fixture['D'],P=fixture['P'])
        except ValueError as error:
            coarse_rejection = str(error)
        else:
            raise AssertionError('Strong-source history crossing the chart boundary was accepted')
    for N in resolutions:
        steps = int(TIME*N)
        assert steps >= 3 and F(steps,N) == TIME
        program = native.build_native(N)
        seed = native.prepare_native(program,L=3,V=fixture['V'],U=fixture['U'],D=fixture['D'],P=fixture['P'])
        state, engine = seed, Engine(program.tensor)
        samples, max_error, max_constraint = [], mp.mpf(0), mp.mpf(0)
        nontrivial_volume_updates = 0
        for n in range(steps+1):
            retained = raw_conserved(program,state,N)
            public = native.read_conserved(program,state)
            assert all(F(public[k]) == v for k,v in retained.items())
            assert retained['tau'] == F(n,N)
            assert retained['invariant'] == 0
            t = F(n,N)
            expected_v = fixture['V']+fixture['U']*t+F(3,4)*fixture['D']*t*t
            expected_u = fixture['U']+F(3,2)*fixture['D']*t
            assert retained['V'] == expected_v and retained['U'] == expected_u
            values = independent_readout(retained)
            selected = physical_decode(retained,mass_squared=0,precision=80)
            assert max(abs(v-selected['d' if name == 'dust' else name])
                       for name,v in zip(PHYSICAL_FIELDS,values)) < mp.mpf('1e-65')
            expected = exact_massless(fixture,t)
            discrepancy = max(abs(a-b) for a,b in zip(values,expected))
            max_error = max(max_error,discrepancy)
            max_constraint = max(max_constraint,abs(physical_constraint(values)))
            samples.append({'macro':n,'proper_time':str(t),
                            'exact_conserved':{k:str(v) for k,v in retained.items()},
                            'physical':{k:text_number(v) for k,v in zip(PHYSICAL_FIELDS,values)}})
            if n < steps:
                before = state
                state = engine.step(before)
                assert engine.inverse_step(state).same_as(before)
                nontrivial_volume_updates += int(int(state.b[0,0]) != int(before.b[0,0]))
        assert nontrivial_volume_updates >= 3
        assert max_error < mp.mpf('1e-65') and max_constraint < mp.mpf('1e-65')
        endpoint = independent_readout(raw_conserved(program,state,N))
        ode_error = max(abs(a-b) for a,b in zip(endpoint,reference))
        assert ode_error < mp.mpf('1e-12')
        final_hash = hashlib.sha256(canonical_bytes(state.to_dict())).hexdigest()
        assert engine.rewind(state,steps).same_as(seed)
        rows.append({'N':N,'h':str(F(1,N)),'macro_updates':steps,
                     'nontrivial_volume_updates':nontrivial_volume_updates,'proper_final_time':str(TIME),
                     'tensor_sha256':program.tensor.fingerprint,
                     'seed_sha256':hashlib.sha256(canonical_bytes(seed.to_dict())).hexdigest(),
                     'final_sha256':final_hash,'full_rewind':True,
                     'maximum_physical_readout_vs_exact_solution':text_number(max_error),
                     'maximum_readout_constraint':text_number(max_constraint),
                     'endpoint_vs_independent_ODE':text_number(ode_error),
                     'samples':samples})
    return {'fixture':fixture['name'],'resolutions':rows,
            'N24_past_slice_rejection':coarse_rejection,
            'comparison_kind':'exact sampling of a restricted integrable massless continuum sector; remaining physical readout discrepancy is roundoff',
            'convergence_order':'not_applicable: exact endpoint agreement is not infinite numerical order'}


def time_and_model_controls(main_fixture, reference):
    at_half = exact_massless(main_fixture,TIME/2)
    at_time = exact_massless(main_fixture,TIME)
    time_relabel_error = max(abs(a-b) for a,b in zip(at_half,at_time))
    frozen_B = list(at_time)
    frozen_B[0] = mp.mpf(1)
    # Constraint equality ignores B; it cannot validate spatial geometry/time.
    assert abs(physical_constraint(frozen_B)) < mp.mpf('1e-65')
    B_error = abs(frozen_B[0]-at_time[0])
    massive, massive_report = high_precision_reference(initial_physical(main_fixture),mass_squared=1)
    wrong_mass_error = max(abs(a-b) for a,b in zip(at_time,massive))
    massive_constraint = physical_constraint(at_time,1)
    # The actual massless trajectory violates massive KG by +phi in pdot.
    KG_residual = at_time[3]
    assert time_relabel_error > mp.mpf('0.05') and B_error > mp.mpf('0.05')
    assert wrong_mass_error > mp.mpf('1e-4') and abs(massive_constraint) > mp.mpf('1e-3')
    assert abs(KG_residual) > mp.mpf('0.1')
    return {'time_relabel_half_speed_rejected':True,'half_time_declared_as_full_time_error':text_number(time_relabel_error),
            'frozen_B_can_pass_C_but_fails_geometry':True,'frozen_B_endpoint_error':text_number(B_error),
            'massive_mu1_same_initial_constraint_zero':True,'massive_reference':massive_report,
            'massless_candidate_vs_massive_endpoint_error':text_number(wrong_mass_error),
            'massive_constraint_on_actual_massless_endpoint':text_number(massive_constraint),
            'massive_KG_pdot_residual_on_actual_massless_endpoint':text_number(KG_residual),
            'massive_extension':'failed if this massless law is relabelled mu=1',
            'post_step_constraint_projection':'not_used; exact Q is read before all physical reconstruction'}


def main():
    with mp.workdps(80):
        equations = symbolic_equations()
        results = []
        for fixture in FIXTURES:
            initial = initial_physical(fixture)
            assert abs(physical_constraint(initial)) < mp.mpf('1e-65')
            reference, ref_report = high_precision_reference(initial)
            exact = exact_massless(fixture,TIME)
            ref_report['error_against_independent_analytic_solution'] = text_number(max(abs(a-b) for a,b in zip(reference,exact)))
            assert max(abs(a-b) for a,b in zip(reference,exact)) < mp.mpf('1e-12')
            results.append({'parameters':{k:str(v) for k,v in fixture.items()},
                            'reference':ref_report,'native':native_refinement(fixture,reference)})
        # Pure scalar validates the independent oracle, but is not encoded by
        # rational P,U with exact Q=0 in this native representation.
        pure_scalar = {'V':mp.mpf(1),'U':mp.mpf(3),'P':mp.sqrt(6),'D':mp.mpf(0)}
        scalar_reference, scalar_report = high_precision_reference(initial_physical(pure_scalar))
        scalar_exact = exact_massless(pure_scalar,TIME)
        scalar_error = max(abs(a-b) for a,b in zip(scalar_reference,scalar_exact))
        assert scalar_error < mp.mpf('1e-12')
        controls = time_and_model_controls(FIXTURES[0],results[0]['reference'])
        geometries = {f['name']:exact_massless(f,TIME) for f in FIXTURES}
        base = geometries['mixed_expanding']
        changes = {}
        for name in ('stronger_scalar','stronger_dust'):
            value = geometries[name]
            changes[name] = {'B_difference':text_number(value[0]-base[0]),
                             'k_difference':text_number(value[1]-base[1]),
                             'constraint_consistent_source_change':True}
            assert value[0] != base[0] and value[1] != base[1]
        negative = geometries['negative_scalar_charge']
        assert all(abs(negative[i]-base[i]) < mp.mpf('1e-65') for i in (0,1,4))
        assert abs(negative[3]+base[3]) < mp.mpf('1e-65')
        report = {'schema':'universe24/sourced-map/independent-oracle/1','baseline_pin':BASE_PIN,
                  'equations':equations,'fixtures':results,
                  'source_response':changes,
                  'negative_scalar_charge_same_geometry_opposite_phi':True,
                  'pure_scalar_reference_control':{'reference':scalar_report,'analytic_error':text_number(scalar_error),
                    'native_status':'blocked for nonzero rational P,U: U^2=3P^2/2 has no nonzero rational solution'},
                  'negative_controls':controls,
                  'status':'exact restricted sourced massless proper-time sampling passed; massive and general Einstein claims remain unestablished'}
        all_runs = [row for result in results for row in result['native']['resolutions']]
        assert len({row['tensor_sha256'] for row in all_runs}) == 1
        report['same_immutable_tensor_across_all_native_sources_and_resolutions'] = True
        paths = (Path(__file__),ROOT/'validation/sourced_map/native.py',
                 ROOT/'validation/sourced_map/physical_map.py',
                 ROOT/'validation/completion/constraint_closure.py',ROOT/'validation/completion/formulation.py',
                 ROOT/'validation/generic_structure/symmetry_sector.py',ROOT/'universe24/core/engine.py')
        report['source_sha256'] = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        output = ROOT/'runs/sourced-map/oracle.json'
        output.parent.mkdir(parents=True,exist_ok=True)
        output.write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({'output':str(output),'fixtures':len(results),'native_runs':sum(len(r['native']['resolutions']) for r in results),
                          'proper_final_time':str(TIME),'all_actual_macro_counts':sorted({row['macro_updates'] for row in all_runs}),
                          'physical_time_semantics':'passed','massive_relabel_control':'failed as required'}))


if __name__ == '__main__':
    main()
