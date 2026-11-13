"""Exact conserved-history and runtime audits for the shared Bianchi-I law."""
from __future__ import annotations

from fractions import Fraction as F
import gzip
from hashlib import sha256
import json
from pathlib import Path
import tempfile

import mpmath as mp
import numpy as np
import sympy as sp

from universe24.system.bundle import pad_state
from universe24.core import Engine, GearType, State, Tensor, exact_json
from universe24.core.lattice import ZERO
from universe24.system.decoder import decode_trace
from universe24.system.runtime import run_bundle, verify_run
from . import common as c


def jsonable(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, (tuple, list)):
        return [jsonable(v) for v in value]
    if isinstance(value, dict):
        return {k: jsonable(v) for k, v in value.items()}
    if isinstance(value, mp.mpf):
        return mp.nstr(value, 55)
    return value


def symbolic_audit():
    V, U, D, P, s1, s2, h = sp.symbols('V U D P s1 s2 h', real=True)
    S = (s1, s2, -s1-s2)
    constraint_residual = U**2-3*D*V-sp.Rational(3, 2)*(P**2+sum(s*s for s in S))
    Vp, Up = V+h*U+sp.Rational(3, 4)*D*h*h, U+sp.Rational(3, 2)*D*h
    assert sp.expand(constraint_residual.subs({V: Vp, U: Up}, simultaneous=True)-constraint_residual) == 0
    assert sp.expand(Vp-h*Up+sp.Rational(3, 4)*D*h*h-V) == 0
    H = [U/(3*V)+s/V for s in S]
    Hdot = [sp.diff(a, V)*U+sp.diff(a, U)*sp.Rational(3, 2)*D for a in H]
    rho, pressure = P**2/(2*V**2)+D/V, P**2/(2*V**2)
    G00 = sum(H[i]*H[j] for i in range(3) for j in range(i+1, 3))
    assert sp.factor(G00-rho-constraint_residual/(3*V**2)) == 0
    spatial = []
    for i in range(3):
        j, k = [a for a in range(3) if a != i]
        Gii = -(Hdot[j]+Hdot[k]+H[j]**2+H[k]**2+H[j]*H[k])
        residual = sp.factor(Gii-pressure)
        assert sp.factor(residual-constraint_residual/(3*V**2)) == 0
        spatial.append(str(residual))
    assert sp.simplify(sp.diff(rho, V)*U+sum(H)*(rho+pressure)) == 0
    assert sp.simplify(sp.diff(P/V, V)*U+sum(H)*P/V) == 0
    for s in S:
        assert sp.simplify(sp.diff(s/V, V)*U+sum(H)*s/V) == 0
    W, J, n = sp.symbols('W J n', integer=True)
    invariant = J**2-12*D*W-24*n*n*(P**2+sum(s*s for s in S))
    assert sp.expand(invariant.subs({W: W+J+3*D, J: J+6*D}, simultaneous=True)-invariant) == 0
    m = sp.symbols('m', integer=True, nonnegative=True)
    Wm, Jm = W+m*J+3*D*m*m, J+6*D*m
    assert sp.expand(Wm.subs(m, m+1)-Wm-Jm-3*D) == 0
    return {'status': 'passed', 'constraint': str(constraint_residual),
            'exact_flow': 'V+=h*U+3*D*h^2/4; U+=3*D*h/2',
            'complete_history_flow': 'W+=J+3D; J+=6D; J=bW-aW+3D',
            'integer_constraint': str(invariant),
            'Einstein_00_and_each_diagonal_residual': 'Q/(3V^2)',
            'continuity_and_shear_transport': 'exact identities',
            'closed_state_solution': 'W_m=W_0+m*J_0+3D*m^2; J_m=J_0+6D*m',
            'scope': 'orthogonal diagonal Bianchi I; massless scalar, comoving dust, Lambda=0'}


def audit_case(N=24, **preparation):
    data = c.trace(N, **preparation)
    initial, final = data['readouts'][0], data['readouts'][-1]
    assert initial['Q'] == final['Q'] == 0
    T = final['tau']-initial['tau']
    assert T == F(1, 8)
    assert final['V'] == initial['V']+T*initial['U']+F(3, 4)*initial['D']*T*T
    assert final['U'] == initial['U']+F(3, 2)*initial['D']*T
    for physical in data['physical']:
        with mp.workdps(60):
            assert all(a > 0 for a in physical['a'])
            assert abs(mp.fprod(physical['a'])-c._mp(physical['V'])) < mp.mpf('1e-55')
    return {**c.identity(data['program'], data['seed']), 'steps': len(data['states'])-1,
            'initial': jsonable(initial), 'final': jsonable(final),
            'readouts': jsonable(data['readouts']), 'metric_endpoint': jsonable(data['physical'][-1]),
            'maximum_retained_bits': max(data['bits']), 'bits': data['bits'],
            'complete_trace_sha256': sha256(b''.join(c.canonical_bytes(s.to_dict()) for s in data['states'])).hexdigest(),
            'scalar_integer_comparisons': 3*8*data['seed'].N*(len(data['states'])-1),
            'all_inverse_and_rewind': True, 'all_carries_retained': True,
            'exact_constraint_and_charges': True, 'actual_steps_match_exact_physical_flow': True}


def runtime_case(N):
    data = c.trace(N)
    bundle = c.make_bundle(data['program'], data['seed'])
    parent = c.ROOT/'runs/conservation_closure/runtime'
    parent.mkdir(parents=True, exist_ok=True)
    out = Path(tempfile.mkdtemp(prefix=f'N{N}-', dir=parent))/'run'
    report = run_bundle(bundle, out, N//8)
    assert verify_run(out) == report
    with gzip.open(out/'full_trace.jsonl.gz', 'rt') as stream:
        records = [exact_json.loads(line) for line in stream]
    with gzip.open(out/'clicks.jsonl.gz', 'rt') as stream:
        clicks = [exact_json.loads(line) for line in stream]
    assert len(records) == N//8
    for n, row in enumerate(records):
        before, after = (State.from_dict(row[key]) for key in ('before', 'after'))
        assert before.same_as(pad_state(data['states'][n]))
        assert after.same_as(pad_state(data['states'][n+1]))
        assert after.same_as(c.scalar_step(before))
        assert c.read_conserved(data['program'], after)['Q'] == 0
    assert clicks == decode_trace(records, bundle.tensor, run_id=report['run_id'],
                                  expected_steps=N//8, initial_state=bundle.seed)
    assert all(report['acceptance_gates'][key]['status'] == 'not_tested' for key in 'CDEF')
    return {**c.identity(data['program'], data['seed']),
            'path': str(out.relative_to(c.ROOT)), 'bundle_id': bundle.bundle_id,
            'tensor_sha256': bundle.tensor.fingerprint,
            'seed_sha256': sha256(c.canonical_bytes(bundle.seed.to_dict())).hexdigest(),
            'channels': 48, 'active_channels': 8, 'retained_integers_per_node': 144,
            'run_id': report['run_id'], 'steps': N//8,
            'trace_sha256': report['files']['full_trace.jsonl.gz'],
            'saved_complete_states_equal_independent_oracle': True,
            'canonical_click_reconstruction_equal': True, 'click_records': len(clicks),
            'runtime_replay_and_inverse': True, 'physical_gates_unchanged': True,
            'maximum_retained_bits_by_step': report['maximum_integer_bits_by_step']}


def negative_controls():
    program, results = c.build(), {}
    def rejected(name, f):
        try:
            f()
        except (ValueError, TypeError) as error:
            results[name] = {'status': 'rejected', 'reason': str(error)}
        else:
            raise AssertionError(f'{name} unexpectedly accepted')
    rejected('float_N', lambda: c.build(24.0))
    rejected('boolean_N', lambda: c.build(True))
    rejected('float_shear', lambda: c.prepare(program, S=(1.0, -1, 0)))
    rejected('nonzero_trace_shear', lambda: c.prepare(program, S=(1, 1, 1)))
    rejected('nonintegral_static_scaling', lambda: c.prepare(program, V=F(1, 7)))
    rejected('zero_dust_undeclared_chart', lambda: c.prepare(program, D=0))
    rejected('invalid_carry', lambda: c.prepare(program, remainders=[[6]*27 for _ in range(8)]))
    rejected('past_slice_singularity', lambda: c.prepare(c.build(1), V=3, U=4))
    seed = c.prepare(program)
    spatial = seed.copy(); spatial.b[6, 1] += 1
    rejected('inhomogeneous_physical_claim', lambda: c.read_conserved(program, spatial))
    wrong_history = seed.copy(); wrong_history.a[6] += 1
    rejected('nonfrozen_shear_history', lambda: c.read_conserved(program, wrong_history))
    off = seed.copy(); off.a[0] += 1; off.b[0] += 1
    engine = Engine(program.tensor)
    defects = [c.read_conserved(program, off)['invariant']]
    for _ in range(3):
        off = engine.step(off); defects.append(c.read_conserved(program, off)['invariant'])
    assert defects == [-12]*4
    rejected('off_constraint_bundle', lambda: c.make_bundle(program, off))
    results['constraint_is_not_projected'] = {'status': 'preserved_nonzero_defect', 'invariants': defects}
    # Scalar/shear charges enter the physical constraint rather than the volume
    # acceleration. Altering them without the compatible momentum is observable.
    shear = seed.copy(); shear.a[6] += 1; shear.b[6] += 1
    shear_defect = c.read_conserved(program, shear)['Q']
    assert shear_defect != 0
    assert c.read_conserved(program, engine.step(shear))['Q'] == shear_defect
    results['incompatible_shear_intervention'] = {'status': 'physical_constraint_failed', 'Q': str(shear_defect)}
    broken = Tensor([GearType(name, label='audit') for name in c.NAMES],
                    [(name, 6, ((name, ZERO, 'b'),)) for name in c.NAMES], strict_support=True)
    broken_engine, state, defects = Engine(broken), seed, []
    for _ in range(3):
        before = state; state = broken_engine.step(state)
        assert state.same_as(c.scalar_step(before, source_coupling=False))
        defects.append(c.read_conserved(program, state)['invariant'])
    assert all(v != 0 for v in defects)
    assert broken_engine.rewind(state, 3).same_as(seed)
    results['removed_dust_reaction'] = {'status': 'physical_constraint_failed',
                                      'invariants': defects, 'rewind_still_passes': True}
    # The full declared log chart admits an anchor in the future. At a very
    # near-root state log1p(negative ratio) used to round to log(0); orienting
    # the ratio positively must keep both time directions finite.
    huge = c.build(10**160)
    near = c.prepare(huge, V=1, U=10**80)
    near.a[3, :] = near.b[3, :] = 4*huge.N*(10**80+1)
    backward = c.physical(huge, near, dps=60)
    assert backward['I'] < 0 and mp.isfinite(backward['I'])
    assert all(a > 0 and mp.isfinite(a) for a in backward['a'])
    with mp.workdps(320):
        U, Ur, K = (c._mp(backward[k]) for k in ('U', 'Uref', 'K_flow'))
        q = mp.sqrt(K)
        reference = mp.log(((U-q)/(U+q))/((Ur-q)/(Ur+q)))/q
        relative = abs((backward['I']-reference)/reference)
        assert relative < mp.mpf('1e-55')
    results['near_root_future_anchor'] = {'status': 'finite_and_high_precision_reference_passed',
                                        'I': mp.nstr(backward['I'], 55),
                                        'relative_error': mp.nstr(relative, 8),
                                        'Q_remains_nonzero': str(backward['Q'])}
    return results


def long_run(steps=4096):
    """Actual Engine trajectory; the polynomial is used only as an oracle."""
    program = c.build()
    seed, engine = c.prepare(program), Engine(program.tensor)
    start = c.read_conserved(program, seed)
    state, peak, compared = seed, c.complete_bits(seed), 0
    for n in range(1, steps+1):
        before = state; state = engine.step(state)
        assert state.same_as(c.scalar_step(before))
        assert engine.inverse_step(state).same_as(before)
        W = start['W']+n*start['J']+3*start['D']*n*n
        J = start['J']+6*start['D']*n
        assert all(int(v) == W for v in state.b[0])
        assert int(state.b[0, 0])-int(state.a[0, 0])+3*start['D'] == J
        assert J*J-12*start['D']*W-24*program.N**2*(start['P']**2+sum(s*s for s in start['S'])) == 0
        peak = max(peak, c.complete_bits(state)); compared += 3*8*state.N
    assert engine.rewind(state, steps).same_as(seed)
    radius = steps+1  # also includes the old history at either endpoint.
    bound = abs(start['W'])+radius*abs(start['J'])+3*abs(start['D'])*radius*radius
    bound = max(bound, radius+abs(int(seed.b[5, 0])),
                *(abs(int(v)) for ar in (seed.a, seed.b, seed.r) for v in ar.flat))
    assert peak <= bound.bit_length()
    final = c.read_conserved(program, state)
    return {'steps': steps, 'time': str(final['tau']), 'scalar_integer_comparisons': compared,
            'final_V': str(final['V']), 'final_U': str(final['U']), 'final_Q': str(final['Q']),
            'maximum_retained_bits': peak, 'proved_bit_bound': bound.bit_length(),
            'absolute_integer_bound': bound, 'all_step_oracles_and_inverses_and_full_rewind': True,
            'bit_complexity': 'O(log N + log(1+steps)) for fixed physical preparation',
            'whole_future_metric_domain': 'V0>0,U0>0,D>0 imply V(t)>0 for all t>=0; exponentials positive'}


def main():
    cases = [audit_case(N) for N in (24, 48, 96)]
    cases += [audit_case(24, remainders=[[r]*27 for _ in range(8)]) for r in range(6)]
    cases += [audit_case(24, P=-2, S=(-1, 1, 0)),
              audit_case(24, V=F(7, 6), D=2),
              audit_case(24, V=7, U=6, S=(1, 1, -2)),
              audit_case(24, V=1, U=3, S=(0, 0, 0))]
    assert len({case['tensor_sha256'] for case in cases}) == 1
    # Physical fields agree across resolutions; scaled W/J are different.
    for i in (1, 2):
        for key in ('V', 'U', 'D', 'P', 'S', 'Q', 'tau', 'H', 'rho', 'pressure'):
            assert cases[i]['final'][key] == cases[0]['final'][key]
    runtime = [runtime_case(N) for N in (24, 48, 96)]
    for case, receipt in zip(cases[:3], runtime):
        assert all(case[key] == receipt[key] for key in ('tensor_sha256', 'seed_sha256', 'N'))
    paths = (Path(c.__file__), Path(__file__), c.ROOT/'universe24/core/engine.py',
             c.ROOT/'universe24/core/tensor.py')
    tensor = c.native_tensor()
    report = {'schema': 'universe24/conservation-closure/native/1',
              'predecessor': c.PREDECESSOR, 'status': 'exact_native_anisotropic_massless_dust_sector_passed',
              'allocation': {'channels': 8, 'retained_integer_entries_per_node': 24,
                             'terms': len(tensor), 'degree': tensor.rank-1,
                             'workspace': 0, 'scheduler': 0, 'anchor_channels': 2,
                             'proper_time_coordinate_channels': 1,
                             'strict_face_support': not tensor.support_violations()},
              'symbolic': symbolic_audit(), 'cases': cases, 'runtime': runtime,
              'negative_controls': negative_controls(), 'long_run': long_run(),
              'source_sha256': {str(p.relative_to(c.ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
              'limits': ['known restricted Bianchi-I solution, not general spatial Einstein evolution',
                         'massless scalar only; no massive-potential invariant claim',
                         'proper_tick is a calibrated coordinate, not a material detector',
                         'root/log/exp readouts are passive full-state diagnostics',
                         'finite dimensional exact chart, not a uniqueness theorem for nature']}
    out = c.ROOT/'runs/conservation_closure/native.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'status': report['status'], 'allocation': report['allocation'],
                      'cases': len(cases), 'runtime_cases': len(runtime),
                      'long_run': report['long_run'], 'out': str(out)}))


if __name__ == '__main__':
    main()
