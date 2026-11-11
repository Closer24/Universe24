"""Exact local matter balances for the retained two-time scalar state.

This is a seven-channel, one-dimensional flat test-field control, NOT the
coupled 41/44-channel Einstein law. No production files are modified.
Time-polarized densities and symmetric face fluxes repair the naive
point-density conservation test without projecting or changing evolution.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import numpy as np

from universe24.core import Engine, GearType, Tensor
from universe24.core.lattice import lattice
from .integer_sign_lift import SignProgram, compile_quadratic, prepare, physical_slices

ROOT = Path(__file__).resolve().parents[3]
FIELDS = ('phi', 'chi', 'P_phi', 'P_chi', 'X_phi', 'X_chi')


def equations(y, derivative):
    return {**{s: y['P_'+s] for s in ('phi', 'chi')},
            **{'P_'+s: derivative('X_'+s, 0) for s in ('phi', 'chi')},
            **{'X_'+s: derivative('P_'+s, 0) for s in ('phi', 'chi')}}


def shifted(row, lat, sign=1):
    return row[lat.shift_index((sign, 0, 0))]


def difference(row, lat):
    return F(1,2)*(shifted(row, lat)-shifted(row, lat, -1))


def densities(previous, current):
    """Twice the time-polarized charge, energy and x-momentum; all integers."""
    p, c = dict(zip(FIELDS, previous)), dict(zip(FIELDS, current))
    charge = (c['phi']*p['P_chi']+p['phi']*c['P_chi']
              -c['chi']*p['P_phi']-p['chi']*c['P_phi'])
    energy = sum(c['P_'+s]*p['P_'+s]+c['X_'+s]*p['X_'+s] for s in ('phi', 'chi'))
    momentum = -sum(c['P_'+s]*p['X_'+s]+p['P_'+s]*c['X_'+s] for s in ('phi', 'chi'))
    return {'charge': charge, 'energy': energy, 'momentum': momentum}


def fluxes(current, lat):
    """One-face quadratic fluxes; difference of outgoing/incoming faces."""
    c = dict(zip(FIELDS, current))
    q = {n: shifted(v, lat) for n, v in c.items()}
    charge = (c['phi']*q['X_chi']+q['phi']*c['X_chi']
              -c['chi']*q['X_phi']-q['chi']*c['X_phi'])
    energy = sum(c['P_'+s]*q['X_'+s]+q['P_'+s]*c['X_'+s] for s in ('phi', 'chi'))
    momentum = -sum(c['P_'+s]*q['P_'+s]+c['X_'+s]*q['X_'+s] for s in ('phi', 'chi'))
    return {'charge': charge, 'energy': energy, 'momentum': momentum}


def local_residuals(previous, current, following, lat):
    before, after, flux = densities(previous, current), densities(current, following), fluxes(current, lat)
    return {name: after[name]-before[name]-flux[name]+shifted(flux[name], lat, -1)
            for name in before}


def peak(row):
    return int(max(abs(v) for v in row))


def raw_point_densities(current):
    c = dict(zip(FIELDS, current))
    return {'charge': 2*(c['phi']*c['P_chi']-c['chi']*c['P_phi']),
            'energy': sum(c['P_'+s]**2+c['X_'+s]**2 for s in ('phi', 'chi')),
            'momentum': -2*sum(c['P_'+s]*c['X_'+s] for s in ('phi', 'chi'))}


def direct_next(previous, current, lat):
    """Independent six-field recurrence; never calls the tensor evaluator."""
    c = dict(zip(FIELDS, current))
    delta = [2*c['P_phi'], 2*c['P_chi'],
             shifted(c['X_phi'], lat)-shifted(c['X_phi'], lat, -1),
             shifted(c['X_chi'], lat)-shifted(c['X_chi'], lat, -1),
             shifted(c['P_phi'], lat)-shifted(c['P_phi'], lat, -1),
             shifted(c['P_chi'], lat)-shifted(c['P_chi'], lat, -1)]
    return previous+np.asarray(delta, dtype=object)


def prepared_pair(L, *, extra_scale=1):
    """Exact sampled periodic C2 bump, right+left-moving, no float seeds.

    Physical dx=dt=1/L, field scale A=2*L^6*extra_scale,
    phi=Phi/A, pi=P/(dt*A), spatial_gradient=X/(dt*A).
    Seed data use analytic d'Alembert histories on grid. P,X are centered
    derivatives (second-order approximations to physical derivatives).
    """
    lat = lattice(L)
    x = lat.all_coords()[:, 0]
    def bump(offset):
        j = (x+offset) % L
        return np.asarray([2*int(v)**3*(L-int(v))**3*extra_scale for v in j], dtype=object)
    right = [bump(0), 2*bump(L//4)]
    left = [bump(L//2), -bump(3*L//4)]
    def values(tick):
        rr = [v[lat.shift_index((-tick % L, 0, 0))] for v in right]
        ll = [v[lat.shift_index((tick % L, 0, 0))] for v in left]
        fields = rr[0]+ll[0], rr[1]+ll[1]
        momenta = [-difference(r, lat)+difference(l, lat) for r,l in zip(rr,ll)]
        gradients = [difference(v, lat) for v in fields]
        rows = [*fields, *momenta, *gradients]
        assert all(F(v).denominator == 1 for row in rows for v in row)
        return np.asarray([[int(v) for v in row] for row in rows], dtype=object)
    return values(-1), values(0), values, 2*L**6*extra_scale


def random_pair(L=5):
    lat = lattice(L)
    rng = np.random.default_rng(29131)
    slices = []
    for _ in range(2):
        fields = 2*rng.integers(-7,8,(2,lat.N)).astype(object)
        pi = rng.integers(-7,8,(2,lat.N)).astype(object)
        grad = np.asarray([difference(row, lat) for row in fields], dtype=object)
        slices.append(np.asarray([[int(v) for v in row] for row in [*fields,*pi,*grad]], dtype=object))
    return slices


def analytic_derivative_error(current, L, tick, scale):
    """Independent continuum derivatives of x^3(1-x)^3 on the circle."""
    def derivative(j):
        x = F(j % L,L)
        return 3*x*x*(1-x)*(1-x)*(1-2*x)
    errors = []
    for j in range(L):
        right = derivative(j-tick), 2*derivative(j-tick+L//4)
        left = derivative(j+tick+L//2), -derivative(j+tick+3*L//4)
        exact = (-right[0]+left[0],-right[1]+left[1],
                 right[0]+left[0],right[1]+left[1])
        errors.extend(abs(F(int(current[i+2,j*L*L])*L,scale)-v)
                      for i,v in enumerate(exact))
    return max(errors)


def gauge_transport_control():
    """Exact Fraction stencil comparison, deliberately NOT an Engine law.

    A continuum pure gauge has theta(x)=2 atan(x), Phi=(cos theta,sin theta),
    A=theta'=2/(1+x^2). At x=0 its additive centered lattice derivative
    violates Xi=0. Parallel-transported endpoint values satisfy Xi=0 exactly.
    """
    rows=[]
    def rotation(x):
        c,s=(1-x*x)/(1+x*x),2*x/(1+x*x)
        return ((c,-s),(s,c))
    def apply(m,v):
        return tuple(sum(m[i][j]*v[j] for j in range(2)) for i in range(2))
    for denominator in (1,2,4,8,16):
        h=F(1,denominator)
        rp,rm=rotation(h),rotation(-h)
        vp,vm=apply(rp,(1,0)),apply(rm,(1,0))
        additive=((vp[0]-vm[0])/(2*h),(vp[1]-vm[1])/(2*h)-2)
        up=tuple(zip(*rp));um=tuple(zip(*rm))
        tp,tm=apply(up,vp),apply(um,vm)
        transported=tuple((tp[i]-tm[i])/(2*h) for i in range(2))
        assert additive==(0,-2*h*h/(1+h*h)) and transported==(0,0)
        rows.append({'dx':str(h),'additive_covariant_gradient_defect':list(map(str,additive)),
                     'parallel_transport_covariant_gradient_defect':list(map(str,transported)),
                     'arithmetic':'Exact Fraction diagnostic, no Engine evolution'})
    return rows


def gauss_program(*, wrong_nodal_current=False):
    """Add one retained face accumulator with a prepared first-order history.

    Its actual physical recurrence is E_next=E_previous+J_now+J_previous.
    Preparing E_now-E_previous=J_previous proves E_next-E_now=J_now for
    every update. It is a one-way source control, not full scalar QED.
    """
    scalar=compile_quadratic(FIELDS,equations)
    terms=[]
    for m in scalar.tensor.monomials:
        terms.append((scalar.tensor.names[m.target],m.coeff,
                      tuple((scalar.tensor.names[f.gear],f.offset,f.field) for f in m.factors),
                      {'designated_one_way':scalar.tensor.is_designated(m)}))
    zero=(0,0,0);plus=(1,0,0)
    if wrong_nodal_current:
        flux_terms=((2,'phi',zero,'X_chi',zero),(-2,'chi',zero,'X_phi',zero))
    else:
        flux_terms=((1,'phi',zero,'X_chi',plus),(1,'phi',plus,'X_chi',zero),
                    (-1,'chi',zero,'X_phi',plus),(-1,'chi',plus,'X_phi',zero))
    for clock_slice in ('a','b'):
        for coefficient,left,lo,right,ro in flux_terms:
            terms.append(('field.E_face',3*coefficient,
                          (('phase.sign',zero,'b'),('field.'+left,lo,clock_slice),
                           ('field.'+right,ro,clock_slice)),
                          {'designated_one_way':'One-way current-to-Gauss accumulator control; no Lorentz-force or stress backreaction.'}))
    tensor=Tensor([*scalar.tensor.gears,GearType('field.E_face',label='audit',link=0)],terms,strict_support=True)
    return SignProgram(tensor,FIELDS+('E_face',),F(1),F(1))


def gauss_audit():
    L=5;lat=lattice(L)
    _,now=random_pair(L)
    now[2:4]=0
    prev=now.copy()
    rows=[]
    for wrong in (False,True):
        program=gauss_program(wrong_nodal_current=wrong)
        current_flux=fluxes(now,lat)['charge']
        if wrong:
            c=dict(zip(FIELDS,now))
            current_flux=2*(c['phi']*c['X_chi']-c['chi']*c['X_phi'])
        old=np.concatenate((prev,(-current_flux)[None,:]))
        current=np.concatenate((now,np.zeros((1,lat.N),dtype=object)))
        seed=prepare(program,old,current,L=L,remainders=np.arange(8*lat.N).reshape(8,lat.N)%6)
        state=seed;engine=Engine(program.tensor)
        gauss_peak=0;increment_peak=0
        for _ in range(12):
            old,current=physical_slices(program,state)
            before=state
            state=engine.step(state)
            _,nxt=physical_slices(program,state)
            assert engine.inverse_step(state).same_as(before)
            assert np.array_equal(state.r,seed.r)
            charge=densities(current[:6],nxt[:6])['charge']
            divergence=nxt[-1]-shifted(nxt[-1],lat,-1)
            gauss_peak=max(gauss_peak,peak(divergence-charge))
            chosen_flux=fluxes(current[:6],lat)['charge']
            if wrong:
                c=dict(zip(FIELDS,current[:6]))
                chosen_flux=2*(c['phi']*c['X_chi']-c['chi']*c['X_phi'])
            increment_peak=max(increment_peak,peak(nxt[-1]-current[-1]-chosen_flux))
        assert increment_peak==0
        assert engine.rewind(state,12).same_as(seed)
        assert (gauss_peak>0) if wrong else gauss_peak==0
        rows.append({'current':'wrong_same_node' if wrong else 'compatible_face',
                     'channels':program.tensor.G,'monomials':len(program.tensor),
                     'strict_single_face_support':not program.tensor.support_violations(),
                     'tensor_sha256':program.tensor.fingerprint,'updates':12,
                     'Gauss_residual_peak':gauss_peak,'first_order_E_increment_residual_peak':increment_peak,
                     'full_rewind':True,'scalar_E_energy_exchange_included':False,
                     'scope':'One-way scalar-current-to-face accumulator control, not coupled Maxwell-Klein-Gordon'})
    return rows


def audit(out):
    program = compile_quadratic(FIELDS, equations)
    engine = Engine(program.tensor)
    cases = []
    for label, L, steps, pair in [('arbitrary_valid_gradients', 5, 8, random_pair(5)),
                                 ('100_bit_seed', 5, 4, [x*(2**100+1) for x in random_pair(5)])]:
        lat = lattice(L)
        seed = prepare(program,*pair,L=L,remainders=np.arange(7*lat.N).reshape(7,lat.N)%6)
        state = seed
        naive_peak = dict.fromkeys(('charge','energy','momentum'),0)
        exact_peak = dict(naive_peak)
        initial_totals = {n:int(sum(v)) for n,v in densities(*pair).items()}
        for _ in range(steps):
            old, now = physical_slices(program,state)
            expected = direct_next(old,now,lat)
            following = engine.step(state)
            p, nxt = physical_slices(program,following)
            assert np.array_equal(p,now) and np.array_equal(nxt,expected)
            assert engine.inverse_step(following).same_as(state)
            assert np.array_equal(following.r,seed.r)
            residual = local_residuals(old,now,nxt,lat)
            point_before, point_after = raw_point_densities(now),raw_point_densities(nxt)
            flux = fluxes(now,lat)
            for name in residual:
                exact_peak[name] = max(exact_peak[name],peak(residual[name]))
                naive_peak[name] = max(naive_peak[name],peak(point_after[name]-point_before[name]-flux[name]+shifted(flux[name],lat,-1)))
                assert int(sum(densities(now,nxt)[name])) == initial_totals[name]
            for s in ('phi','chi'):
                assert not any(nxt[FIELDS.index('X_'+s)]-difference(nxt[FIELDS.index(s)],lat))
            state = following
        assert not any(exact_peak.values()) and all(naive_peak.values())
        assert engine.rewind(state,steps).same_as(seed)
        cases.append({'case':label,'L':L,'steps':steps,'exact_local_balance_residuals':exact_peak,
                      'wrong_same_time_density_residuals':naive_peak,'global_polarized_totals':initial_totals,
                      'all_gradient_constraints_zero':True,'full_rewind':True})

    refinements=[]
    for L in (8,16,24):
        old, now, expected, scale = prepared_pair(L)
        seed=prepare(program,old,now,L=L,remainders=np.arange(7*L**3).reshape(7,L**3)%6)
        state=seed
        for tick in range(1,L//4+1):
            previous=state
            state=engine.step(state)
            a,b=physical_slices(program,state)
            assert np.array_equal(a,expected(tick-1)) and np.array_equal(b,expected(tick))
            assert engine.inverse_step(state).same_as(previous)
            assert all(not any(v) for v in local_residuals(*physical_slices(program,previous),b,lattice(L)).values())
        assert engine.rewind(state,L//4).same_as(seed)
        derivative_error=analytic_derivative_error(b,L,L//4,scale)
        # |f'''|<=6 for the periodic C2 bump; the largest component has
        # total profile weight 3, hence central-derivative error<=3*dx^2.
        assert derivative_error<=F(3,L*L)
        refinements.append({'L':L,'physical_dt':str(F(1,L)),'physical_dx':str(F(1,L)),
                            'field_scale':scale,'fixed_physical_final_time':'1/4',
                            'steps':L//4,'same_immutable_tensor':True,
                            'exact_grid_dAlembert_field_error':'0',
                            'physical_momentum_gradient_max_error':str(derivative_error),
                            'derivative_error_over_dx_squared':str(derivative_error*L*L),
                            'proved_derivative_error_bound':str(F(3,L*L)),
                            'exact_local_balance_residuals':{'charge':0,'energy':0,'momentum':0},
                            'seed_and_evolution_are_integers':True,'full_rewind':True})
    assert all(F(refinements[i+1]['physical_momentum_gradient_max_error'])
               <F(refinements[i]['physical_momentum_gradient_max_error']) for i in range(2))

    lat=lattice(5)
    old,now=random_pair(5)
    bad=now.copy();bad[FIELDS.index('X_chi'),0]+=2
    nxt=direct_next(old,bad,lat)
    defects={name:peak(v) for name,v in local_residuals(old,bad,nxt,lat).items()}
    assert defects['charge']>0 and defects['energy']==defects['momentum']==0
    # Exact compact U(1) transports cannot be naively substituted by a
    # nontrivial pair of unscaled integers; the smallest rational example
    # already needs a denominator. This is not a general no-go theorem.
    rational_link={'cos':'3/5','sin':'4/5','unit_norm':True,
                   'direct_unit_seed_next_is_integer':False}
    report={'scope':'1D flat massless complex scalar test-field primitive; no dynamic geometry or Maxwell field',
            'channels':program.tensor.G,'retained_integer_entries':3*program.tensor.G,
            'monomials':len(program.tensor),'rank':program.tensor.rank,
            'strict_single_face_support':not program.tensor.support_violations(),
            'tensor_sha256':program.tensor.fingerprint,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'cases':cases,'fixed_domain_refinement':refinements,
            'pure_gauge_spatial_control':gauge_transport_control(),
            'actual_Engine_Gauss_controls':gauss_audit(),
            'broken_gradient_control_residuals':defects,'naive_rational_link_obstruction':rational_link,
            'result':'Existing retained a,b slices support exact local time-polarized charge, energy and momentum balances with face fluxes. A same-time continuum density is the wrong exact discrete conservation diagnostic.',
            'limitations':['This primitive is not added to the 44-channel geometry candidate.',
                           'No Einstein constraint, dynamically curved geometry or physical detector is validated.',
                           'Energy is a time-polarized discrete invariant, not positive on arbitrary two-time data.',
                           'Charge balance requires both scalar gradient constraints; energy/momentum identities do not.',
                           'Fixed-domain runs use a prepared 1D traveling-wave sector and do not prove 3D CFL stability.',
                           'Local U(1) gauge invariance with dynamical compact link transport remains unimplemented.']}
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    r=audit(ROOT/'runs/team48/matter/repair_flux.json')
    print(json.dumps(r,indent=2))
