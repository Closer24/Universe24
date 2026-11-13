"""48-channel light, internal restoring motion, and optical coupling controls.

Every saved candidate obeys the current regular 2O admission contract. These
are separate research laws: no general Einstein/source acceptance is implied.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import gzip
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
from universe24.algebra.group_2o import group
from universe24.core import Engine, State, Tensor, exact_json
from universe24.core.lattice import ZERO
from universe24.core.symmetry import CONTRACT, require_equivariant
from universe24.light import light_tensor, make_light_bundle, electromagnetic_fields, orientations
from universe24.system.bundle import create_bundle
from universe24.system.decoder import default_protocol
from universe24.system.runtime import run_bundle, verify_run
from validation.system_smoke import scalar_step
from validation.light_runtime import inspect as inspect_installed_light

ROOT = Path(__file__).resolve().parents[1]
PARTNER = tuple(group().multiplication[group().central])
PAIRS = tuple((g, h) for g, h in enumerate(PARTNER) if g < h)


def build_tensor(*, gradient=3, spring=3, optical=0, backreaction=False, phase_gate=False):
    """Fixed integer force, with an optional full gradient of edge energy.

    p=b_g+b_-g, q=b_g-b_-g. E_edge=optical*q(x)^2*Delta(p)^2/2.
    The probe keeps only the p-force; the reciprocal law also keeps q-force.
    phase_gate is a separate matched-history move/hold law, not a force
    derived from that energy. Its exact prepared sector is homogeneous in q.
    """
    if gradient not in (1, 3) or spring not in (0, 3) or optical not in (0, 1):
        raise ValueError('this audit declares only the finite parameter panel')
    terms = []
    frames = orientations()
    for g in range(48):
        h = PARTNER[g]
        direction = frames[g][0]
        if phase_gate:
            if (gradient,spring,optical,backreaction) != (3,3,0,False):
                raise ValueError('the matched-phase law is one distinct fixed tensor')
            terms.extend([(g,3,[(h,ZERO,'b')]),(g,3,[(g,direction,'b')])])
            for sign in (-1,1):
                at=tuple(sign*v for v in direction)
                for left,right in itertools.product((g,h),repeat=2):
                    coefficient=-3*sign*(1 if left==g else -1)*(1 if right==g else -1)
                    terms.append((g,coefficient,[(left,ZERO,'b'),(right,ZERO,'b'),(g,at,'b')]))
            continue
        terms.append((g, 6-2*gradient-spring, [(g, ZERO, 'b')]))
        terms.append((g, spring, [(h, ZERO, 'b')]))
        for sign in (-1, 1):
            terms.append((g, gradient, [(g, tuple(sign*v for v in direction), 'b')]))

    def product(target, target_at, coefficient, forms):
        for choices in itertools.product(*forms):
            c = coefficient
            factors = []
            for gear, at, weight in choices:
                c *= weight
                factors.append((gear, tuple(at[k]-target_at[k] for k in range(3)), 'b'))
            terms.append((target, c, factors))

    if optical:
        for g, h in PAIRS:
            direction = frames[g][0]
            q = [(g, ZERO, 1), (h, ZERO, -1)]
            delta_p = [(g, direction, 1), (h, direction, 1), (g, ZERO, -1), (h, ZERO, -1)]
            for target in (g, h):
                product(target, ZERO, optical, [q, q, delta_p])
                product(target, direction, -optical, [q, q, delta_p])
            if backreaction:
                product(g, ZERO, -optical, [q, delta_p, delta_p])
                product(h, ZERO, optical, [q, delta_p, delta_p])
    tensor = Tensor(light_tensor().gears, terms, strict_support=True)
    require_equivariant(tensor)
    return tensor


def prepare(*, L=4, precision=1, bias=None, amplitude=1, textured=False,
            axis=0,sign=1,polarization=1,paused_history=False):
    """All 48 channels explicit. Uniform central contrast is EM-invisible.

    Pair sums start with a unit slope and pair differences with (old,current)
    =(0,1). This keeps integer parity compatible with the four-cycle contrast.
    """
    if bias is None:
        bias = 8*precision
    original = make_light_bundle(L=L, axis=axis, sign=sign, polarization=polarization, center=1, order=2,
                                 amplitude=amplitude*precision)
    carrier = original.model['preparation']['carrier']
    g, h = min(carrier, PARTNER[carrier]), max(carrier, PARTNER[carrier])
    seed = State(L, np.full((48,L**3), bias, dtype=object),
                 np.full((48,L**3), bias, dtype=object), np.ones((48,L**3), dtype=int))
    pattern = 1-2*(seed.lattice.all_coords()[:,0] % 2) if textured else np.ones(seed.N, dtype=int)
    for left, right in PAIRS:
        seed.b[left] += (1+pattern)//2
        seed.b[right] += (1-pattern)//2
    for channel in (g,h):
        seed.a[channel] += original.seed.b[carrier] if paused_history else original.seed.a[carrier]
        seed.b[channel] += original.seed.b[carrier]
    metadata = {'L': L, 'precision': precision, 'bias': bias, 'amplitude': amplitude,
                'carrier_pair': [g,h], 'textured': textured, 'axis':axis, 'sign':sign,
                'polarization':polarization,'paused_history':paused_history}
    return seed, metadata


def force_oracle(state, *, gradient, spring, optical, backreaction, phase_gate=False):
    """Independent vector force from p,q and an edge-energy derivative."""
    b = state.b.astype(object)
    u = (6-2*gradient)*b.copy()
    for g,(direction,_,_) in enumerate(orientations()):
        plus, minus = state.lattice.shift_index(direction), state.lattice.shift_index(tuple(-v for v in direction))
        if phase_gate:
            q=b[g]-b[PARTNER[g]]
            u[g]=3*(b[PARTNER[g]]+b[g,plus]+q*q*(b[g,minus]-b[g,plus]))
            continue
        u[g] += gradient*(b[g,plus]+b[g,minus]) + spring*(b[PARTNER[g]]-b[g])
    if optical:
        for g,h in PAIRS:
            direction = orientations()[g][0]
            plus, minus = state.lattice.shift_index(direction), state.lattice.shift_index(tuple(-v for v in direction))
            p, q = b[g]+b[h], b[g]-b[h]
            dp = p[plus]-p
            flux = optical*q*q*dp
            u[g] += flux-flux[minus]
            u[h] += flux-flux[minus]
            if backreaction:
                source = optical*q*dp*dp
                u[g] -= source
                u[h] += source
    numerator = 2*u+state.r
    ell, remainder = numerator//6, numerator%6
    return State(state.L, state.b, ell-state.a, remainder)


def read_states(path, seed):
    yield 0, seed
    with gzip.open(Path(path)/'full_trace.jsonl.gz','rt') as stream:
        for tick,line in enumerate(stream,1):
            yield tick, State.from_dict(exact_json.loads(line)['after'])


def mode_norm4(field):
    """Exact |DFT(k=pi/2)|^2 on the x line, without floating arithmetic."""
    values = [int(v) for v in field.reshape(4,4,4)[:,0,0]]
    return (values[0]-values[2])**2 + (values[3]-values[1])**2


def observe(path, bundle, parameters, metadata, *, verify=True):
    saved = verify_run(path) if verify else json.loads((Path(path)/'validation.json').read_text())
    engine = Engine(bundle.tensor)
    seed = bundle.seed
    g,h = metadata['carrier_pair']
    initial_e,initial_b = electromagnetic_fields(seed)
    modal_reference=seed.L==4 and metadata['axis']==0 and metadata['polarization']==1
    initial_mode = mode_norm4(initial_e[1]) if modal_reference else None
    initial_energy=sum(int(v)**2 for fields in (initial_e,initial_b) for v in fields.flat)
    previous = None
    samples = []
    first_negative = None
    largest_field = 0
    for tick,state in read_states(path, seed):
        if previous is not None:
            if not state.same_as(force_oracle(previous, **parameters)):
                raise AssertionError('edge force oracle mismatch')
            if tick <= 2 and not state.same_as(scalar_step(bundle.tensor, previous)):
                raise AssertionError('scalar monomial oracle mismatch')
            if not engine.inverse_step(state).same_as(previous):
                raise AssertionError('complete step inverse mismatch')
        for bank in ('a','b','r'):
            values = getattr(state,bank)
            bad = np.argwhere(values < 1)
            if len(bad) and first_negative is None:
                channel,node = map(int,bad[0])
                first_negative = {'tick':tick,'bank':bank,'channel':channel,'node':node,'value':str(values[channel,node])}
        q = state.b[g].astype(object)-state.b[h].astype(object)
        qa = state.a[g].astype(object)-state.a[h].astype(object)
        e,b = electromagnetic_fields(state)
        expected_e = np.roll(initial_e.reshape(3,seed.L,seed.L,seed.L),metadata['sign']*tick,axis=metadata['axis']+1).reshape(3,-1)
        expected_b = np.roll(initial_b.reshape(3,seed.L,seed.L,seed.L),metadata['sign']*tick,axis=metadata['axis']+1).reshape(3,-1)
        exact_shift = np.array_equal(e,expected_e) and np.array_equal(b,expected_b)
        hops=(tick+1)//2
        delayed_e=np.roll(initial_e.reshape(3,seed.L,seed.L,seed.L),metadata['sign']*hops,axis=metadata['axis']+1).reshape(3,-1)
        delayed_b=np.roll(initial_b.reshape(3,seed.L,seed.L,seed.L),metadata['sign']*hops,axis=metadata['axis']+1).reshape(3,-1)
        exact_delayed=np.array_equal(e,delayed_e) and np.array_equal(b,delayed_b)
        largest_field = max(largest_field,max(abs(int(v)) for v in e.flat))
        norm = mode_norm4(e[1]) if modal_reference else None
        energy=sum(int(v)**2 for fields in (e,b) for v in fields.flat)
        samples.append({'tick':tick,'central_contrast_at_origin':str(q[0]),
                        'contrast_homogeneous':bool(np.all(q==q[0])),
                        'oscillator_ledger_at_origin':str(int(q[0])**2+int(qa[0])**2),
                        'proposed_speed_squared_at_origin':None if parameters.get('phase_gate') else str(Fraction(parameters['gradient'],3)+Fraction(2*parameters['optical'],3)*int(q[0])**2),
                        'exact_installed_light_translation':bool(exact_shift),
                        'exact_alternating_move_hold':bool(exact_delayed),
                        'plane_field_energy_conserved':energy==initial_energy,
                        'maxwell_characteristic_mode_norm_ratio':str(Fraction(norm,initial_mode)) if initial_mode else None})
        previous=state
    if not engine.rewind(previous, saved['steps']).same_as(seed):
        raise AssertionError('full rewind mismatch')
    return {'run_id':saved['run_id'],'tensor_hash':bundle.tensor.fingerprint,
            'model_contract':saved['model_contract'],'channels':48,'degree':bundle.tensor.rank-1,
            'terms':len(bundle.tensor.monomials),'steps':saved['steps'],
            'maximum_integer_bits':max(saved['maximum_integer_bits_by_step']),
            'force_oracle_all_steps':'passed','scalar_oracle_first_two_steps':'passed',
            'full_replay_and_inverse':'passed','strict_naturals':'passed' if first_negative is None else 'failed',
            'first_nonpositive':first_negative,'max_field_amplitude':str(largest_field),
            'all_steps_exact_light_translation':all(s['exact_installed_light_translation'] for s in samples),
            'all_steps_exact_alternating_move_hold':all(s['exact_alternating_move_hold'] for s in samples),
            'all_steps_plane_field_energy_conserved':all(s['plane_field_energy_conserved'] for s in samples),
            'samples':samples}


def make_bundle(tensor,seed,parameters,metadata):
    return create_bundle(tensor,seed,
        channels=[{'index':g,'name':gear.name,'label':gear.label,'owner':'regular-48-resonance-audit',
                   'purpose':'complete regular amplitude; central-pair sum and contrast are passive readouts'}
                  for g,gear in enumerate(tensor.gears)],protocol=default_protocol(),
        model={'id':'light-link-resonance-control','version':'1','role':'research','symmetry':CONTRACT,
               'domain':'declared plane-profile / central-contrast research cases; no general Einstein acceptance',
               'parameters':parameters,'preparation':metadata,
               'scope':'oscillator, probe-only or variational negative control; no scalar link-length claim'})


def source_hashes():
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
            for name in ('universe24','validation') for p in sorted((ROOT/name).rglob('*.py'))
            if 'tests' not in p.parts}


def run(out):
    out=Path(out)
    out.mkdir(parents=True,exist_ok=False)
    sources=source_hashes()
    baseline=[]
    for axis,sign in itertools.product(range(3),(-1,1)):
        for polarization in range(3):
            if polarization==axis:
                continue
            bundle=make_light_bundle(L=5,axis=axis,sign=sign,polarization=polarization,center=2,order=2)
            destination=out/f'light-{axis}-{sign}-{polarization}'
            run_bundle(bundle,destination,8)
            baseline.append(inspect_installed_light(destination))
    cases={}
    specs=[('spring-dark',dict(gradient=3,spring=3,optical=0,backreaction=False),dict(precision=1),16),
           ('spring-textured',dict(gradient=3,spring=3,optical=0,backreaction=False),dict(precision=1,amplitude=0,textured=True),10),
           ('optical-probe',dict(gradient=1,spring=3,optical=1,backreaction=False),dict(precision=3**13),12),
           ('reciprocal-small',dict(gradient=1,spring=3,optical=1,backreaction=True),dict(precision=1),4),
           ('reciprocal-large',dict(gradient=1,spring=3,optical=1,backreaction=True),dict(precision=3**5),3)]
    phase_parameters=dict(gradient=3,spring=3,optical=0,backreaction=False,phase_gate=True)
    for axis,sign in itertools.product(range(3),(-1,1)):
        for polarization in range(3):
            if polarization!=axis:
                specs.append((f'phase-{axis}-{sign}-{polarization}',phase_parameters,
                              dict(axis=axis,sign=sign,polarization=polarization,paused_history=True),64))
    specs.extend([('phase-textured',phase_parameters,dict(textured=True,paused_history=True),4),
                  ('phase-wrong-history',phase_parameters,dict(paused_history=False),4)])
    for name,parameters,preparation,steps in specs:
        tensor=build_tensor(**parameters)
        seed,metadata=prepare(**preparation)
        bundle=make_bundle(tensor,seed,parameters,metadata)
        run_bundle(bundle,out/name,steps)
        cases[name]=observe(out/name,bundle,parameters,metadata)
        print(f'{name}: {steps} steps, natural={cases[name]["strict_naturals"]}, bits={cases[name]["maximum_integer_bits"]}',flush=True)
    if not cases['spring-dark']['all_steps_exact_light_translation']:
        raise AssertionError('dark-oscillator negative control changed')
    if cases['optical-probe']['samples'][-1]['maxwell_characteristic_mode_norm_ratio'] != '65':
        raise AssertionError('predeclared optical parametric-growth control changed')
    if not all(s['central_contrast_at_origin']==str((1,0,-1,0)[s['tick']%4]) and s['oscillator_ledger_at_origin']=='1'
               for s in cases['spring-dark']['samples']):
        raise AssertionError('restoring cycle changed')
    phase_cases={k:v for k,v in cases.items() if k.startswith('phase-') and k not in ('phase-textured','phase-wrong-history')}
    if len({v['tensor_hash'] for v in phase_cases.values()})!=1 or not all(
            v['all_steps_exact_alternating_move_hold'] and v['all_steps_plane_field_energy_conserved'] and v['strict_naturals']=='passed'
            for v in phase_cases.values()):
        raise AssertionError('matched-phase prepared transport failed')
    if cases['phase-wrong-history']['all_steps_exact_alternating_move_hold']:
        raise AssertionError('mismatched history unexpectedly accepted')
    if any(cases[k]['first_nonpositive'] is None for k in ('reciprocal-small','reciprocal-large','spring-textured','phase-textured')):
        raise AssertionError('registered instability control changed')
    # These gates intentionally remain failures, not relabeled successes.
    result={'schema':'universe24/light-link-resonance/1','git_base':'3285c11fcde949774f9db5f80fecd696dbbd0039',
            'installed_light':baseline,'candidates':cases,'source_hashes':sources,
            'gates':{'installed_axis_light':'passed','all_candidates_current_48_2o_contract':'passed',
                     'internal_restoring_cycle':'passed','spring_alone_changes_light':'failed',
                     'naive_coefficient_preserves_time_reparametrized_maxwell':'failed',
                     'full_coupling_preserves_declared_natural_domain':'failed',
                     'matched_phase_axis_transport':'passed',
                     'matched_phase_plane_energy_and_naturals':'passed',
                     'matched_phase_spatial_clock_domain':'failed',
                     'matched_phase_physical_link_stretch':'not_tested',
                     'einstein_geometry_and_source':'not_tested','accepted_dynamic_light_geometry':'blocked'},
            'scope':'One current Engine, explicitly separate tensors and negative controls; no joining of distinct-law successes.'}
    if sources!=source_hashes():
        raise AssertionError('sources changed during audit')
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    result=run(parser.parse_args().out)
    print(json.dumps({'gates':result['gates'],'cases':len(result['installed_light'])+len(result['candidates'])},indent=2))
