"""Exact inhomogeneous plane-dust control, not a general Einstein integrator.

Four prepared integer channels encode an analytic invariant solution family.
The Engine never evaluates ratios, roots, an Einstein RHS or an external solve.
All rational geometry/source expressions are passive and proved for this family.
"""
from fractions import Fraction as F
import gzip
import hashlib
import json
from math import isqrt
from pathlib import Path
import sys

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from universe24.core import Engine, State, Tensor

NAMES = ('plane.mass', 'plane.mode', 'plane.root_time', 'plane.proper_time')
ZERO = (0, 0, 0)


def build():
    terms = [(name, 6, ((name, ZERO, 'b'),)) for name in NAMES]
    terms.append((NAMES[3], 18, ((NAMES[2], ZERO, 'b'),),
                  {'designated_one_way': 'Prepared cubic proper-time identity Q=D^3; analytic dust control only.'}))
    return Tensor(NAMES, terms, strict_support=True)


def prepare(subdivision, L=4, *, amplitude_scale=1, base_numerator=None):
    if type(subdivision) is not int or subdivision < 1 or type(L) is not int or L < 3:
        raise ValueError('positive integer subdivision and integer L>=3 required')
    if type(amplitude_scale) is not int or amplitude_scale < 1:
        raise ValueError('positive exact amplitude scale required')
    if base_numerator is None:
        base_numerator = 2*amplitude_scale
    if type(base_numerator) is not int or base_numerator < 1:
        raise ValueError('positive exact base numerator required')
    # A(x)=2+x^2(1-x)^2 is C2-periodic; B(x)=1. The scale L^4 is
    # calibration only and independent of the microtime subdivision S.
    a = np.empty((4, L**3), dtype=object)
    b = np.empty_like(a)
    for node in range(L**3):
        x = node % L
        mass = base_numerator*L**4+amplitude_scale*x*x*(L-x)*(L-x)
        b[:, node] = (mass, amplitude_scale*L**4, 2*subdivision, (2*subdivision)**3)
        a[:, node] = (mass, amplitude_scale*L**4, 2*subdivision-1, (2*subdivision-1)**3)
    r = np.arange(4*L**3).reshape(4, L**3) % 6
    return State(L, a, b, r)


def read(state, subdivision, node=0, *, amplitude_scale=1):
    mass, mode, d, q = map(int, state.b[:, node])
    old_mass, old_mode, old_d, old_q = map(int, state.a[:, node])
    if (old_mass, old_mode, old_d, old_q) != (mass, mode, d-1, (d-1)**3):
        raise ValueError('prepared constant-profile and temporal-history relations failed')
    if q != d**3:
        raise ValueError('prepared proper-time invariant Q=D^3 failed')
    A, B, tau = F(mass, amplitude_scale*state.L**4), F(mode, amplitude_scale*state.L**4), F(d, subdivision)
    t = F(q, subdivision**3)
    if tau <= 0 or A*t+B <= 0:
        raise ValueError('outside positive-time, pre-shell-crossing chart')
    longitudinal = A*tau*tau+B/tau
    transverse = tau*tau
    density = 4*A/(3*t*(A*t+B))
    kx = -(2*A*t-B)/(3*t*(A*t+B))
    ky = -F(2, 3)/t
    volume = longitudinal*transverse**2
    hamiltonian = (kx+2*ky)**2-kx*kx-2*ky*ky-2*density
    return {'A': A, 'B': B, 'tau': tau, 'proper_time': t,
            'longitudinal': longitudinal, 'transverse': transverse,
            'rho': density, 'Kx': kx, 'Ky': ky, 'volume': volume,
            'rest_mass': density*volume, 'H': hamiltonian,
            'shear_difference': kx-ky}


def symbolic_oracle():
    """All Einstein components from coordinate metric, no production RHS."""
    tau, x, y, z = sp.symbols('tau x y z', positive=True)
    A, B = sp.Function('A')(x), sp.Function('B')(x)
    coordinates = (tau, x, y, z)
    metric = sp.diag(-9*tau**4, (A*tau**2+B/tau)**2, tau**4, tau**4)
    inverse = metric.inv()
    gamma = [[[sp.cancel(sum(inverse[a, d]*(
        sp.diff(metric[d, c], coordinates[b])+sp.diff(metric[d, b], coordinates[c])
        -sp.diff(metric[b, c], coordinates[d]))/2 for d in range(4)))
        for c in range(4)] for b in range(4)] for a in range(4)]
    def riemann(a, b, c, d):
        return sp.cancel(sp.diff(gamma[a][b][d], coordinates[c])
                         -sp.diff(gamma[a][b][c], coordinates[d])
                         +sum(gamma[a][e][c]*gamma[e][b][d]
                              -gamma[a][e][d]*gamma[e][b][c] for e in range(4)))
    ricci = sp.Matrix(4, 4, lambda b, d: sp.cancel(sum(riemann(a, b, a, d) for a in range(4))))
    scalar = sp.cancel(sum(inverse[a, b]*ricci[a, b] for a in range(4) for b in range(4)))
    einstein = (ricci-metric*scalar/2).applyfunc(sp.cancel)
    rho = 4*A/(3*tau**3*(A*tau**3+B))
    stress = sp.zeros(4)
    stress[0, 0] = rho*9*tau**4
    assert (einstein-stress).applyfunc(sp.cancel) == sp.zeros(4)
    # T^{ab}=rho u^a u^b, u^tau=1/(3 tau^2). All four divergences.
    contravariant_stress = sp.zeros(4)
    contravariant_stress[0, 0] = rho/(9*tau**4)
    divergence = []
    for b in range(4):
        value = sum(sp.diff(contravariant_stress[a, b], coordinates[a])
                    +sum(gamma[a][a][c]*contravariant_stress[c, b]
                         +gamma[b][a][c]*contravariant_stress[a, c] for c in range(4))
                    for a in range(4))
        divergence.append(sp.cancel(value))
    assert divergence == [0]*4
    volume = (A*tau**2+B/tau)*tau**4
    assert sp.cancel(rho*volume-4*A/3) == 0
    # A nonzero Weyl component demonstrates non-FLRW tidal curvature.
    a, b, c, d = 0, 2, 0, 2
    covariant_riemann = metric[a, a]*riemann(a, b, c, d)
    weyl = sp.cancel(covariant_riemann-(metric[a, c]*ricci[d, b]
                    -metric[a, d]*ricci[c, b]-metric[b, c]*ricci[d, a]
                    +metric[b, d]*ricci[c, a])/2
                    +scalar*(metric[a, c]*metric[d, b]-metric[a, d]*metric[c, b])/6)
    assert weyl != 0
    assert sp.cancel(weyl.subs(B, 0)) == 0
    assert sp.cancel(sp.diff(rho, x)) != 0
    # A transverse profile is not another valid dust solution: evaluate its
    # mixed Einstein component independently rather than assuming closure.
    transverse_metric = sp.diag(-9*tau**4, (2*tau**2+(1+y*y)/tau)**2, tau**4, tau**4)
    transverse_inverse = transverse_metric.inv()
    transverse_gamma = [[[sp.cancel(sum(transverse_inverse[a, e]*(
        sp.diff(transverse_metric[e, c], coordinates[b])
        +sp.diff(transverse_metric[e, b], coordinates[c])
        -sp.diff(transverse_metric[b, c], coordinates[e]))/2 for e in range(4)))
        for c in range(4)] for b in range(4)] for a in range(4)]
    mixed_einstein = sp.cancel(sum(
        sp.diff(transverse_gamma[a][0][2], coordinates[a])
        -sp.diff(transverse_gamma[a][0][a], y)
        +sum(transverse_gamma[a][a][c]*transverse_gamma[c][0][2]
             -transverse_gamma[a][2][c]*transverse_gamma[c][0][a] for c in range(4))
        for a in range(4)))
    assert mixed_einstein != 0
    return {'all_16_Einstein_components_exact': True,
            'all_4_stress_divergences_zero': True,
            'conserved_rest_mass_density': str(sp.cancel(rho*volume)),
            'Weyl_tau_y_tau_y': str(weyl),
            'density_gradient': str(sp.cancel(sp.diff(rho, x))),
            'arbitrary_smooth_longitudinal_profiles': True,
            'transverse_profile_negative_G_tau_y': str(mixed_einstein),
            'sources': ['https://doi.org/10.1103/PhysRevD.26.3315',
                        'https://doi.org/10.1140/epjc/s10052-021-09154-0']}


def scalar_step(state):
    """Independent fixed-six scalar oracle; does not call Engine.step."""
    a, b, r = (np.empty_like(state.a) for _ in range(3))
    for node in range(state.L**3):
        for gear in range(4):
            u = 6*int(state.b[gear, node])
            if gear == 3:
                u += 18*int(state.b[2, node])
            ell, carry = divmod(2*u+int(state.r[gear, node]), 6)
            a[gear, node] = state.b[gear, node]
            b[gear, node] = ell-int(state.a[gear, node])
            r[gear, node] = carry
    return State(state.L, a, b, r)


def run(out):
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    raw = out.parent/'repair_plane_dust_raw'
    raw.mkdir(exist_ok=True)
    tensor, rows = build(), []
    (raw/'tensor.json').write_text(json.dumps(tensor.to_dict(), indent=2)+'\n')
    engine = Engine(tensor)
    for subdivision in (1, 2, 4, 8, 16, 32, 64):
        seed = prepare(subdivision)
        state = seed
        snapshots = [seed.to_dict()]
        largest = 0
        for tick in range(subdivision+1):
            for node in range(state.L):
                q = read(state, subdivision, node)
                assert q['H'] == 0 and q['rho'] > 0 and q['volume'] > 0
                assert q['rest_mass'] == 4*q['A']/3
                assert q['proper_time'] == F(2*subdivision+tick, subdivision)**3
                assert q['shear_difference'] != 0
            if tick < subdivision:
                before = state
                state = engine.step(state)
                snapshots.append(state.to_dict())
                assert state.same_as(scalar_step(before))
                assert engine.inverse_step(state).same_as(before)
                assert np.array_equal(state.r, seed.r)
                largest = max(largest, max(abs(int(v)).bit_length() for v in state.b.flat))
        assert engine.rewind(state, subdivision).same_as(seed)
        trace_path = raw/f'time_{subdivision}.json.gz'
        with gzip.open(trace_path, 'wt') as stream:
            json.dump({'subdivision': subdivision, 'amplitude_scale': 1,
                       'complete_snapshots': snapshots}, stream)
        with gzip.open(trace_path, 'rt') as stream:
            loaded = json.load(stream)['complete_snapshots']
        replay = State.from_dict(loaded[0])
        assert replay.same_as(seed)
        for expected in loaded[1:]:
            replay = engine.step(replay)
            assert replay.same_as(State.from_dict(expected))
        assert replay.same_as(state)
        endpoint = read(state, subdivision, node=1)
        rows.append({'subdivision': subdivision, 'updates': subdivision,
                     'root_time_interval': '[2,3]', 'proper_time_interval': '[8,27]',
                     'max_integer_bit_length': largest, 'all_sampled_H_zero': True,
                     'M_xyz_zero_analytic': True, 'positive_density_metric': True,
                     'mass_conserved': True, 'exact_rewind': True,
                     'serialized_full_state_replay': True,
                     'endpoint': {k: str(endpoint[k]) for k in ('rho', 'Kx', 'Ky', 'volume')}})
    assert all(row['endpoint'] == rows[0]['endpoint'] for row in rows)

    # Independent spatial resolution at fixed final t=27. Spatial evolution
    # is silent in this exact family: this assesses sampling/differentiation,
    # not a generic spatial-curvature stencil's convergence.
    spatial = []
    x, t = sp.symbols('x t')
    A = 2+x*x*(1-x)*(1-x)
    exact_gradient = sp.diff(4*A/(3*t*(A*t+1)), x).subs({x: sp.Rational(1, 4), t: 27})
    exact_gradient = F(int(exact_gradient.p), int(exact_gradient.q))
    for L in (4, 8, 16, 32):
        s = prepare(1, L=L)
        s = engine.step(s)
        i = L//4
        left, right = read(s, 1, (i-1) % L), read(s, 1, (i+1) % L)
        gradient = (right['rho']-left['rho'])*F(L, 2)
        error = abs(gradient-exact_gradient)
        spatial.append({'L': L, 'dx': str(F(1, L)), 'gradient_error': str(error),
                        'common_point_density': str(read(s, 1, i)['rho'])})
    assert all(F(spatial[i+1]['gradient_error']) < F(spatial[i]['gradient_error']) for i in range(3))
    assert all(q['common_point_density'] == spatial[0]['common_point_density'] for q in spatial)

    # Quantization is refined independently of space and time. The target
    # A=sqrt(2)+x^2(1-x)^2 is approximated only in seed preparation.
    quantization = []
    target_A = sp.sqrt(2)+sp.Rational(9, 256)
    target_density = 4*target_A/(81*(27*target_A+1))
    previous_error = None
    for amplitude_scale in (1, 4, 16, 64, 256):
        numerator = isqrt(2*amplitude_scale*amplitude_scale)
        seed = prepare(8, amplitude_scale=amplitude_scale, base_numerator=numerator)
        state = seed
        for _ in range(8):
            state = engine.step(state)
        observed = read(state, 8, 1, amplitude_scale=amplitude_scale)
        error = sp.simplify(target_density-sp.Rational(observed['rho'].numerator, observed['rho'].denominator))
        assert error > 0
        if previous_error is not None:
            assert sp.simplify(previous_error-error) > 0
        assert observed['H'] == 0 and engine.rewind(state, 8).same_as(seed)
        quantization.append({'amplitude_scale': amplitude_scale,
                             'base': str(F(numerator, amplitude_scale)),
                             'density_error_to_sqrt2_profile': str(error),
                             'density_error_decimal_diagnostic': str(error.evalf(12)),
                             'H_exact_zero': True, 'exact_rewind': True})
        previous_error = error

    # Full arithmetic inversion does not imply this restricted physical chart.
    bad = prepare(4)
    bad.a[3, :] += 1
    after = engine.step(bad)
    try:
        read(after, 4)
    except ValueError:
        invalid_history_rejected = True
    else:
        invalid_history_rejected = False
    assert invalid_history_rejected and engine.inverse_step(after).same_as(bad)
    shell = prepare(1)
    shell.b[1, :] = shell.a[1, :] = -16*shell.L**4
    try:
        read(shell, 1, 0)
    except ValueError:
        shell_crossing_rejected = True
    else:
        shell_crossing_rejected = False
    assert shell_crossing_rejected
    report = {'scope': 'exact analytic invariant plane-dust sector, not generic 44-channel repair',
              'channels': tensor.G, 'retained_integer_entries_per_node': 3*tensor.G,
              'monomials': len(tensor), 'degree': tensor.rank-1,
              'tensor_fingerprint': tensor.fingerprint, 'strict_support': not tensor.support_violations(),
              'same_tensor_every_resolution': True, 'spatial_exchange_terms': 0,
              'symbolic_oracle': symbolic_oracle(), 'time_refinement': rows,
              'spatial_sampling': spatial, 'independent_seed_quantization': quantization,
              'negative_controls': {'bad_temporal_history_rejected': invalid_history_rejected,
                                    'bad_history_still_rewinds': True,
                                    'shell_crossing_chart_rejected': shell_crossing_rejected},
              'limitations': ['No generic spatial gravitational coupling; exact silent plane-dust family only.',
                              'M_i=0, pressure=0; no tilted matter, Maxwell/scalar fields, apparatus or detector.',
                              'Readout is an analytic solution parameterization, not an Einstein RHS solver.',
                              'No assertion that analytic prepared families satisfy the full issue40 model acceptance.',
                              'The spatial check refines sampled density and its gradient, not an arbitrary curvature stencil.',
                              'Positive chart requires tau>0 and A*t+B>0; shell crossings remain physical boundaries.',
                              'Proper-time register is geometric accounting, not an independently ticking material clock.'],
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    report['raw_evidence_sha256'] = {
        str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(raw.iterdir())}
    out.write_text(json.dumps(report, indent=2)+'\n')
    return report


if __name__ == '__main__':
    result = run(ROOT/'runs/team48/variational/repair_plane_dust.json')
    print(json.dumps(result, indent=2))
