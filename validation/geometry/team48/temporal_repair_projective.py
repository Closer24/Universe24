"""Independent temporal/positivity test of the projective 44-channel proposal.

Fundamental trajectories use the unchanged integer Engine. Floating evaluation
is confined to independent exact-solution comparisons in this diagnostic.
The mixed scalar/dust reference is homogeneous, not a spatial convergence test.
"""
from fractions import Fraction as F
from functools import partial
import hashlib
import json
import math
from pathlib import Path

import numpy as np

from universe24.core import Engine
from . import geometry_positive_pairs as positive
from . import matter_charged as charged
from . import matter_dust_square as square
from . import refinement_integer_projective as projective

ROOT = Path(__file__).resolve().parents[3]
NAMES = positive.replace_fields(square.FIELDS_CHARGED)
SOURCE = partial(square.equations, base_equations=charged.equations,
                 mass_squared=0, cosmological=0, coupling=1)
BUILDER = partial(positive.equations, fermi_equations=SOURCE)


def reference(time):
    """Independent flat FLRW with comoving dust M=1 and scalar momentum P=2.

    v=a^3, v(0)=1, v'(0)=3, v''=3/2. Friedmann and scalar/dust conservation
    give v=1+3t+3t²/4. Units c=8piG=1; K=-H, normal lapse=1.
    """
    t = float(time)
    v, speed = 1+3*t+0.75*t*t, 3+1.5*t
    discriminant = math.sqrt(6)
    ratio = ((1.5*t+3-discriminant)/(1.5*t+3+discriminant)
             *(3+discriminant)/(3-discriminant))
    return {'B': v**(-1/3), 'K': -speed/(3*v), 'Pi_phi': 2/v,
            'dust_amplitude': 1/math.sqrt(v), 'phi': 2/discriminant*math.log(ratio)}


def prepared(program, denominator, *, protected=True):
    current = np.zeros((len(NAMES), 27), dtype=object)
    fields = dict(zip(NAMES, current))
    for axis in range(3):
        fields[f'diag_p{axis}'][:] = 1
        fields[f'K{axis}{axis}'][:] = -1
    fields['Pi_phi'][:] = 2
    fields['dust_amplitude'][:] = 1
    remainder = np.array([int(i % 6) for i in range(44*27)], dtype=object).reshape(44,27)
    seed = projective.prepare(program, current, L=3, denominator=denominator,
                              remainders=remainder)
    # This is initial retained memory, never a post-step injection. D_old=0
    # is a memory boundary. We DO NOT interpret it as an earlier metric.
    if protected:
        for axis in range(3):
            seed.a[1+NAMES.index(f'diag_q{axis}'), :] = 1
    return seed


def integer_oracle(program, old, now):
    """Independent reduced homogeneous equations, not production RHS/step."""
    c, h = program.multiplier, program.dt
    d = int(now[0]); p = dict(zip(NAMES, map(int, now[1:])))
    f = {name: 0 for name in NAMES}
    k, dust, pi = p['K00'], p['dust_amplitude'], p['Pi_phi']
    assert p['K11'] == k == p['K22']
    for axis in range(3):
        f[f'K{axis}{axis}'] = 3*k*k-F(1,2)*dust*dust
        f[f'diag_p{axis}'] = F(1,2)*k*p[f'diag_p{axis}']
        f[f'diag_q{axis}'] = F(1,2)*k*p[f'diag_q{axis}']
    f['Pi_phi'] = 3*k*pi
    f['dust_amplitude'] = F(3,2)*k*dust
    result = [c*d**3-int(old[0])]
    for index, name in enumerate(NAMES):
        # Nonzero nonlinear f is degree2, phi_dot=Pi is degree1.
        increment = c*h*d*f[name]
        if name == 'phi': increment = c*h*d*d*pi
        assert F(increment).denominator == 1
        result.append(c*d*d*p[name]+int(increment)-int(old[index+1]))
    return np.array(result, dtype=object)


def integer_digest(values):
    digest = hashlib.sha256()
    for value in values:
        value = int(value)
        payload = abs(value).to_bytes(max(1,(abs(value).bit_length()+7)//8),'big')
        digest.update(bytes([value < 0]))
        digest.update(len(payload).to_bytes(8,'big'))
        digest.update(payload)
    return digest.hexdigest()


def fraction_certificate(value):
    return {'numerator_bits':abs(value.numerator).bit_length(),
            'denominator_bits':value.denominator.bit_length(),
            'signed_integer_pair_sha256':integer_digest((value.numerator,value.denominator))}


def diagnostics(state):
    d = int(state.b[0,0]); values = dict(zip(NAMES, map(int, state.b[1:,0])))
    k, pi, dust = (F(values[name], d) for name in ('K00','Pi_phi','dust_amplitude'))
    p, q = (F(values[name],d) for name in ('diag_p0','diag_q0'))
    B = p*p+q*q
    H = 6*k*k-pi*pi-2*dust*dust
    return {'B':float(B), 'K':float(k), 'Pi_phi':float(pi),
            'dust_amplitude':float(dust), 'phi':float(F(values['phi'],d)),
            'abs_H':float(abs(H)), 'det_B':float(B**3),
            'physical_q':float(q), 'physical_q_squared':float(q*q),
            'q_exact_fraction_certificate':fraction_certificate(q),
            'H_exact_fraction_certificate':fraction_certificate(H),
            'nonq_retained_state_sha256':integer_digest(
                int(bank[index,0]) for bank in (state.a,state.b,state.r)
                for index in range(44) if index == 0 or not NAMES[index-1].startswith('diag_q')),
            'denominator_bits':d.bit_length(),
            'maximum_retained_bits':max(abs(int(v)).bit_length() for v in state.b[:,0]),
            'Wronskians': [int(state.b[1+NAMES.index(f'diag_p{axis}'),0])
                           *int(state.a[1+NAMES.index(f'diag_q{axis}'),0])
                           -int(state.b[1+NAMES.index(f'diag_q{axis}'),0])
                           *int(state.a[1+NAMES.index(f'diag_p{axis}'),0])
                           for axis in range(3)]}


def execute(count, *, protected=True):
    final_time = F(1,4); h = final_time/count
    program = projective.compile_projective(NAMES, BUILDER, dt=h, dx=1, degree=3)
    assert program.tensor.G == 44 and not program.tensor.support_violations()
    assert not any(f.field == 'a' for term in program.tensor.monomials for f in term.factors)
    denominator = h.denominator**2
    seed = prepared(program, denominator, protected=protected)
    state = seed
    engine = Engine(program.tensor)
    oracle_old, oracle_now = seed.a[:,0].copy(), seed.b[:,0].copy()
    rows = []
    for tick in range(count+1):
        observed = diagnostics(state)
        target = reference(tick*h)
        errors = {name:abs(observed[name]-target[name]) for name in target}
        assert observed['det_B'] > 0
        if protected: assert observed['Wronskians'] == [denominator]*3
        else: assert observed['Wronskians'] == [0]*3
        rows.append({'tick':tick,'proper_time':str(tick*h),**observed,
                     'maximum_field_error':max(errors.values()),'field_errors':errors})
        if tick == count: break
        oracle_next = integer_oracle(program, oracle_old, oracle_now)
        before = state
        state = engine.step(state)
        assert np.array_equal(state.a, np.repeat(oracle_now[:,None],27,axis=1))
        assert np.array_equal(state.b, np.repeat(oracle_next[:,None],27,axis=1))
        assert np.array_equal(state.r, seed.r)
        assert engine.inverse_step(state).same_as(before)
        oracle_old, oracle_now = oracle_now, oracle_next
    assert engine.rewind(state,count).same_as(seed)
    return {'steps':count,'h':str(h),'fixed_final_proper_time':str(final_time),
            'channels':program.tensor.G,'retained_integers_per_node':132,
            'monomials':len(program.tensor.monomials),'degree':program.tensor.rank-1,
            'tensor_fingerprint':program.tensor.fingerprint,'multiplier':program.multiplier,
            'initial_denominator':denominator,'protected':protected,
            'integer_scalar_oracle_all_complete_states':True,
            'all_nonzero_remainders_preserved':True,'complete_rewind':True,
            'peak_abs_H':max(r['abs_H'] for r in rows),
            'peak_field_error':max(r['maximum_field_error'] for r in rows),
            'final':rows[-1],'samples':rows}


def spatial_invariant_control():
    """Off-constraint heterogeneous source control for the algebraic W theorem."""
    program=projective.compile_projective(NAMES,BUILDER,dt=F(1,4),dx=1,degree=3)
    current=np.array([F(((i*11+j*7)%9)-4,8) for i in range(len(NAMES))
                      for j in range(27)],dtype=object).reshape(len(NAMES),27)
    for axis in range(3):
        current[NAMES.index(f'diag_p{axis}'),:]=1
        current[NAMES.index(f'diag_q{axis}'),:]=0
    seed=projective.prepare(program,current,L=3,denominator=8,
                           remainders=np.array([int(i%6) for i in range(44*27)],dtype=object).reshape(44,27))
    for axis in range(3): seed.a[1+NAMES.index(f'diag_q{axis}'),:]=1
    state=seed;engine=Engine(program.tensor)
    for tick in range(4):
        assert all(int(d)>0 for d in state.b[0,:])
        for axis in range(3):
            p,q=1+NAMES.index(f'diag_p{axis}'),1+NAMES.index(f'diag_q{axis}')
            W=state.b[p]*state.a[q]-state.b[q]*state.a[p]
            assert all(int(value)==8 for value in W)
            assert all(int(pv)**2+int(qv)**2>0 for pv,qv in zip(state.b[p],state.b[q]))
        if tick<3:
            before=state;state=engine.step(state)
            assert engine.inverse_step(state).same_as(before)
            assert np.array_equal(state.r,seed.r)
    assert engine.rewind(state,3).same_as(seed)
    return {'scope':'Heterogeneous charged/scalar/Maxwell/dust off-constraint seed; algebraic positivity only',
            'nodes':27,'updates':3,'all_81_Wronskians_exactly_8':True,
            'all_three_frame_diagonals_positive_at_every_node_and_tick':True,
            'complete_rewind':True,'initial_constraints_satisfied':False,
            'maximum_retained_bits':max(abs(int(v)).bit_length() for v in state.b.flat)}


def audit(out):
    runs = [execute(count) for count in (2,4,8)]
    # A separate unprotected seed is allowed to approach the same physical
    # solution. Protection is an exact domain invariant, not a new source.
    unprotected = execute(4, protected=False)
    assert all(b['peak_abs_H']<a['peak_abs_H'] for a,b in zip(runs,runs[1:]))
    assert all(b['peak_field_error']<a['peak_field_error'] for a,b in zip(runs,runs[1:]))
    fields = ('B','K','Pi_phi','dust_amplitude','phi')
    effect = max(abs(runs[1]['final'][name]-unprotected['final'][name]) for name in fields)
    assert runs[1]['final']['nonq_retained_state_sha256'] == unprotected['final']['nonq_retained_state_sha256']
    # Every other retained component is identical in this homogeneous control.
    # The EXACT positive metric difference is q^2; float subtraction rounds it away.
    exact_metric_effect_float = runs[1]['final']['physical_q_squared']
    assert exact_metric_effect_float > 0
    assert all(abs(b['final']['physical_q'])<abs(a['final']['physical_q']) for a,b in zip(runs,runs[1:]))
    report = {'scope':'Actual fixed-six cubic44 homogeneous scalar+dust temporal refinement and invariant positive frame; not spatial/general-Einstein convergence',
              'seed':'K00=K11=K22=-1, Pi_phi=2, dust_amplitude=1, B=I; rho=3, H=0, all momenta/gradients/Maxwell fields zero',
              'physical_metric_authority':'B_aa=(Pp_a²+Pq_a²)/D²; gamma_inverse=B.T*B; lapse1/shift0',
              'history':'D_old=0 and P_old=0 except each q_old=1. This is declared retained memory, not an earlier physical slice.',
              'identity':'W_n=Pp_n*Pq_(n-1)-Pq_n*Pp_(n-1)=D_initial exactly; uniform D>0 implies each B_aa>0.',
              'new_method':'Homogenized Euler plus reversible old-numerator memory, not the previous sign-lift leapfrog.',
              'fixed_time_runs':runs,'unprotected_4step_control':unprotected,
              'heterogeneous_invariant_control':spatial_invariant_control(),
              'protection_max_field_effect_at_4steps_float64_subtraction':effect,
              'protection_B_effect_exact_expression':'q_protected^2; every other retained component is identical',
              'protection_B_effect_at_4steps_from_exact_fraction_float64':exact_metric_effect_float,
              'float64_rounding_note':'Direct float64 subtraction rounds this positive B difference to zero; no exact equality is claimed.',
              'limitations':['Only homogeneous flat scalar+dust FLRW is independently compared here; charged current and spatial flux are zero.',
                             'Hamiltonian residual decreases but is not zero after updates; no exact constraint preservation claimed.',
                             'Cubic denominator bit length grows like 3^N; computational cost is a major unresolved issue.',
                             'Apparatus/clocks/click-only readout are absent; four channel slots remain unallocated.',
                             'Finite refinement evidence does not prove global stability, bounded integers or general Einstein convergence.'],
              'primary_sources':[{'title':'Initializing and stabilizing variational multistep algorithms for modeling dynamical systems','authors':'Ellison, Burby, Finn, Qin, Tang','url':'https://arxiv.org/abs/1403.0890','use':'Motivation for explicit principal/parasitic-mode control; no inherited stability theorem. Runtime resets from the paper are not used.'}],
              'source_sha256':{str(Path(__file__).relative_to(ROOT)):hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}}
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    result=audit(ROOT/'runs/team48/temporal_repair/projective44.json')
    print(json.dumps([{'steps':r['steps'],'peak_H':r['peak_abs_H'],
                       'error':r['peak_field_error'],'bits':r['final']['maximum_retained_bits']}
                      for r in result['fixed_time_runs']],indent=2))
