"""Three-channel native massive packet/phase control, not a GR runtime model.

Run ``python -m validation.generic_structure.packet_clock``. Only Engine.step
advances retained data. FFTs, complex eigenvectors and floats prepare two slices
or passively measure them; none enters the immutable integer update tensor.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp

from universe24.core import Engine, GearType, State, Tensor
from universe24.core.lattice import ZERO, lattice
from universe24.system.bundle import canonical_bytes
from validation.completion.time_stability import prepare_native, decoded

ROOT = Path(__file__).resolve().parents[2]
BASE_PIN = '8c53e69f4b466dcbd2da7dab7e3c365bd9731766'


def build(mass=1, axis=0):
    """Extend the existing native chiral stencil by an on-site skew mass.

    mass is an integer coefficient, not a physical mass under mesh refinement.
    The two retained real fields are a classical 1+1 first-order KG factorization;
    they are not an inferred quantum spinor or a new clock bank.
    """
    if type(mass) is not int or type(axis) is not int or axis not in range(3):
        raise ValueError('integer mass coefficient and axis 0, 1 or 2 required')
    names = ('wave.sign', 'wave.plus', 'wave.minus')
    phase = ((names[0], ZERO, 'a'), (names[0], ZERO, 'b'))
    mark = {'designated_one_way': 'Counted computational sign, not physical apparatus or Einstein sourcing.'}
    terms = []
    for i, chirality in ((1, 1), (2, -1)):
        for direction in (-1, 1):
            offset = tuple(direction if j == axis else 0 for j in range(3))
            terms.append((names[i], chirality*direction,
                          (*phase, (names[i], offset, 'b')), mark))
        if mass:
            terms.append((names[i], chirality*mass,
                          (*phase, (names[3-i], ZERO, 'b')), mark))
    return Tensor([GearType(n, label='audit') for n in names], terms, strict_support=True)


def scalar_step(state, mass, axis):
    """Independent scalar coordinates; no production tensor evaluator or shifts."""
    arrays = [np.empty((3, state.N), dtype=object) for _ in range(3)]
    aa, bb, rr = arrays
    L = state.L
    for xyz in np.ndindex((L, L, L)):
        node = (xyz[0]*L+xyz[1])*L+xyz[2]
        neighbors = []
        for direction in (1, -1):
            pos = list(xyz)
            pos[axis] = (pos[axis]+direction) % L
            neighbors.append((pos[0]*L+pos[1])*L+pos[2])
        factor = int(state.a[0, node])*int(state.b[0, node])
        for g in range(3):
            u = 0 if g == 0 else factor*(1 if g == 1 else -1)*(
                int(state.b[g, neighbors[0]])-int(state.b[g, neighbors[1]])
                +mass*int(state.b[3-g, node]))
            ell, rem = divmod(2*u+int(state.r[g, node]), 6)
            aa[g, node], bb[g, node], rr[g, node] = int(state.b[g, node]), ell-int(state.a[g, node]), rem
    return State(L, aa, bb, rr)


def spectrum(k, mass=1):
    """Positive-frequency physical branch, radians per Engine tick."""
    H = np.array([[-math.sin(k)/3, 1j*mass/6], [-1j*mass/6, math.sin(k)/3]])
    eigenvalues, eigenvectors = np.linalg.eigh(H)
    a, vec = float(eigenvalues[1]), eigenvectors[:, 1]
    if not 0 < a < 1:
        raise ValueError('strict stable nonzero physical-branch frequency required')
    omega = math.asin(a)
    vg = math.sin(k)*math.cos(k)/(9*a*math.sqrt(1-a*a))
    return omega, vg, vec


def analytic_derivation():
    s, m = sp.symbols('s m', real=True)
    B = sp.Matrix([[-s/3, sp.I*m/6], [-sp.I*m/6, s/3]])
    I, Z = sp.eye(2), sp.zeros(2)
    M = (-2*sp.I*B).row_join(I).col_join(I.row_join(Z))
    H = I.row_join(sp.I*B).col_join((-sp.I*B).row_join(I))
    assert sp.simplify(M.conjugate().T*H*M-H) == sp.zeros(4)
    assert sp.simplify(B*B-(4*s*s+m*m)/36*I) == Z
    rmax = math.sqrt(5)/6
    return {'exact_symbolic_symmetrizer': True,
            'spectral_theorem_scope': 'Ideal recurrence without carry forcing; actual Engine is compared against it with a deterministic error bound.',
            'decoded_recurrence': 'Y[n+1]=Y[n-1]+(sigma3*Delta_axis+mu*J)*Y[n]/3+eta[n]',
            'J': [[0, 1], [-1, 0]],
            'exact_carry': 'eta=s_b*(r-r_next)/(6*S), |eta|<=2/(3*S)',
            'dispersion': 'sin(omega)^2=(4*sin(k)^2+mu^2)/36',
            'group_velocity_nodes_per_tick': 'sin(k)*cos(k)/(9*sin(omega)*cos(omega))',
            'phase_rate_along_packet_center': 'omega-k*v_group',
            'rest_angular_frequency': 'asin(abs(mu)/6)',
            'stability_domain': 'sqrt(4+mu^2)<6',
            'mu1_uniform_pair_power_bound': math.sqrt((1+rmax)/(1-rmax)),
            'principal_continuum_limit': 'Y_t=sigma3*Y_x+m*J*Y; each component solves Y_tt=Y_xx-m^2*Y',
            'units': 'dx=1, dt=1/3 gives continuum c=1 and m=mu/2; frequencies above use Engine ticks',
            'refinement_obstruction': 'At dt=dx/3, fixed physical m requires mu=2*m*dx. Nonzero integer mu cannot tend to zero with dx. No fixed-mass refinement claim.'}


def mechanics():
    rng = np.random.default_rng(44042026)
    rows = []
    for axis in range(3):
        seed = prepare_native(rng.integers(-100, 101, (2, 27)).astype(object),
                              rng.integers(-100, 101, (2, 27)).astype(object), L=3)
        tensor, state = build(axis=axis), seed
        engine, changed, trace = Engine(tensor), 0, hashlib.sha256()
        for _ in range(24):
            old = state
            state = engine.step(old)
            assert state.same_as(scalar_step(old, 1, axis))
            assert engine.inverse_step(state).same_as(old)
            assert np.all((state.r-old.r) % 2 == 0)
            changed += int(np.count_nonzero(state.r != old.r))
            trace.update(canonical_bytes(state.to_dict()))
        assert changed and engine.rewind(state, 24).same_as(seed)
        rows.append({'axis': axis, 'changed_remainder_entries': changed,
                     'tensor_sha256': tensor.fingerprint, 'trace_sha256': trace.hexdigest(),
                     'scalar_register_comparisons': 24*27*3*3, 'full_rewind': True})
    return {'channels': 3, 'retained_integers_per_node': 9, 'additional_clock_fields': 0,
            'degree': 3, 'all_six_initial_remainders': True, 'cases': rows}


def profile_seed(profile_prev, profile_now, *, L, axis, scale):
    coords = lattice(L).all_coords()[:, axis]
    old = np.rint(scale*np.asarray(profile_prev)[:, coords]).astype(np.int64).astype(object)
    now = np.rint(scale*np.asarray(profile_now)[:, coords]).astype(np.int64).astype(object)
    return prepare_native(old, now, L=L)


def reduce_profile(state, scale, axis):
    """Passive transverse average; all transverse carry differences remain retained."""
    _, now = decoded(state)
    arr = np.asarray(now, dtype=float).reshape(2, state.L, state.L, state.L)/scale
    return arr.mean(axis=tuple(j+1 for j in range(3) if j != axis))


def run_packet(*, L=32, carrier=4, axis=0, steps=64, scale=2**24):
    """Finite band initial packet; only two initial slices are ever prepared."""
    x = np.arange(L)
    # No zero/Nyquist components; conjugate completion makes two real fields.
    modes = np.arange(abs(carrier)-3, abs(carrier)+4)*(1 if carrier > 0 else -1)
    weights = np.exp(-0.5*((np.abs(modes)-abs(carrier))/0.7)**2)
    vectors, omegas, velocities = [], [], []
    for mode in modes:
        w, v, vec = spectrum(2*math.pi*mode/L)
        omegas.append(w)
        velocities.append(v)
        vectors.append(vec)
    ks, omegas, vectors = 2*math.pi*modes/L, np.array(omegas), np.array(vectors)
    def ideal(n):
        z = np.exp(1j*(ks[:, None]*(x-L/4)[None, :]-omegas[:, None]*n))
        return np.einsum('j,ja,jx->ax', weights, vectors, z).real
    seed = profile_seed(ideal(-1), ideal(0), L=L, axis=axis, scale=scale)
    tensor, state = build(axis=axis), seed
    engine = Engine(tensor)
    centers, ideal_centers, phases, changed = [], [], [], 0
    mask = modes % L
    center_index = list(modes).index(carrier)
    def measure(profile):
        fourier = np.fft.fft(profile, axis=1)/L
        analytic = np.zeros_like(fourier)
        analytic[:, mask] = 2*fourier[:, mask]
        field = np.fft.ifft(analytic, axis=1)*L
        density = np.sum(abs(field)**2, axis=0)
        circular = np.sum(density*np.exp(2j*math.pi*x/L))/np.sum(density)
        center = np.angle(circular)*L/(2*math.pi)
        amplitude = np.vdot(vectors[center_index], fourier[:, carrier % L])
        return center, np.angle(amplitude), float(abs(circular)), float(np.sum(density))
    peaks, maxbits = [], 0
    for n in range(steps+1):
        profile = reduce_profile(state, scale, axis)
        center, phase, localized, _ = measure(profile)
        centers.append(center)
        ideal_centers.append(measure(ideal(n))[0])
        phases.append(phase)
        peaks.append(localized)
        maxbits = max(maxbits, state.max_abs().bit_length())
        if n < steps:
            old = state
            state = engine.step(old)
            changed += int(np.count_nonzero(state.r != old.r))
    centers = np.unwrap(np.array(centers)*2*math.pi/L)*L/(2*math.pi)
    ideal_centers = np.unwrap(np.array(ideal_centers)*2*math.pi/L)*L/(2*math.pi)
    omega_fit = -float(np.polyfit(np.arange(steps+1), np.unwrap(phases), 1)[0])
    group_fit = float(np.polyfit(np.arange(steps+1), centers, 1)[0])
    ideal_fit = float(np.polyfit(np.arange(steps+1), ideal_centers, 1)[0])
    predicted_weighted_vg = float(np.dot(weights*weights, velocities)/np.dot(weights, weights))
    final_error = float(np.sqrt(np.mean((reduce_profile(state, scale, axis)-ideal(steps))**2)))
    power_bound = math.sqrt((1+math.sqrt(5)/6)/(1-math.sqrt(5)/6))
    error_bound = power_bound*(math.sqrt(2)/(2*scale)+2*steps/(3*scale))
    assert final_error < error_bound
    assert abs(omega_fit-omegas[center_index]) < 2e-6
    assert np.max(abs(centers-ideal_centers)) < 2e-4
    assert abs(group_fit-predicted_weighted_vg) < 0.02
    assert min(peaks) > 0.5 and changed > 0
    final_hash = hashlib.sha256(canonical_bytes(state.to_dict())).hexdigest()
    assert engine.rewind(state, steps).same_as(seed)
    rest = math.asin(1/6)
    k0, w0, vg0 = float(ks[center_index]), float(omegas[center_index]), float(velocities[center_index])
    return {'L': L, 'axis': axis, 'carrier_mode': carrier, 'steps': steps, 'amplitude_scale': scale,
            'tensor_sha256': tensor.fingerprint, 'complete_seed_sha256': hashlib.sha256(canonical_bytes(seed.to_dict())).hexdigest(),
            'complete_final_sha256': final_hash, 'full_rewind': True,
            'changed_remainder_entries': changed, 'max_retained_bits': maxbits,
            'packet_is_localized_along_one_axis_only': True,
            'envelope_circular_concentration_minimum': min(peaks),
            'measured_displacement_nodes': float(centers[-1]-centers[0]),
            'measured_group_velocity': group_fit, 'ideal_finite_band_centroid_velocity': ideal_fit,
            'spectrum_weighted_group_prediction': predicted_weighted_vg,
            'central_mode_omega_prediction': w0, 'central_mode_omega_measured': omega_fit,
            'final_field_rms_error': final_error, 'deterministic_error_bound': error_bound,
            'central_ray_phase_rate': w0-k0*vg0,
            'central_ray_phase_over_rest_rate': (w0-k0*vg0)/rest,
            'continuum_SR_rate_at_same_group_speed': math.sqrt(max(0, 1-9*vg0*vg0)),
            'proper_clock_from_packet': 'not_established: FFT phase is a passive field diagnostic, not an independently ticking retained apparatus',
            'same_law_as_common45': False}


def spectral_controls():
    rows = []
    for L, mode, axis in ((16, 0, 0), (32, 1, 0), (16, 2, 1), (16, -3, 2), (16, 4, 0), (16, 8, 2)):
        scale, steps = 2**20, 80
        k = 2*math.pi*mode/L
        omega, vg, vec = spectrum(k)
        x = np.arange(L)
        initial = (vec[:, None]*np.exp(1j*k*x)).real
        previous = (vec[:, None]*np.exp(1j*(k*x+omega))).real
        seed = profile_seed(previous, initial, L=L, axis=axis, scale=scale)
        state, engine = seed, Engine(build(axis=axis))
        phases = []
        rest_crossings, old_q = [], float(initial[0, 0])
        for n in range(steps+1):
            profile = reduce_profile(state, scale, axis)
            # k=0's real rotating pair has one signed temporal quadrature.
            amplitude = np.vdot(vec, np.fft.fft(profile, axis=1)[:, mode % L]/L)
            phases.append(float(np.angle(amplitude)))
            if mode == 0 and n and old_q <= 0 < profile[0, 0]:
                rest_crossings.append(n)
            old_q = profile[0, 0]
            if n < steps:
                state = engine.step(state)
        measured = -float(np.polyfit(np.arange(steps+1), np.unwrap(phases), 1)[0])
        assert abs(measured-omega) < 2e-6
        assert engine.rewind(state, steps).same_as(seed)
        rows.append({'L': L, 'mode': mode, 'axis': axis, 'omega_predicted': omega,
                     'omega_measured': measured, 'group_velocity_predicted': vg,
                     'ray_phase_rate_over_rest': (omega-k*vg)/math.asin(1/6),
                     'continuum_SR_rate_at_group_speed': math.sqrt(max(0, 1-9*vg*vg)),
                     'full_rewind': True, 'rest_upward_crossings': rest_crossings,
                     'tensor_sha256': engine.tensor.fingerprint})
    # A massless spatially constant field has no intrinsic phase clock.
    L = 3
    ones = np.ones((2, 27), dtype=object)*12345
    seed, tensor = prepare_native(ones, ones, L=L), build(mass=0)
    state, engine = seed, Engine(tensor)
    for _ in range(24):
        state = engine.step(state)
        assert np.array_equal(decoded(state)[1], ones)
    assert engine.rewind(state, 24).same_as(seed)
    # Same algorithm but outside its massive CFL margin: mu=7 amplifies rest.
    seed = prepare_native(np.zeros((2, 27), dtype=object), ones, L=3)
    state, engine = seed, Engine(build(mass=7))
    for _ in range(24):
        state = engine.step(state)
    amplification = float(np.max(abs(decoded(state)[1]))/12345)
    assert amplification > 100 and engine.rewind(state, 24).same_as(seed)
    assert rows[4]['ray_phase_rate_over_rest'] > 2 and abs(rows[4]['continuum_SR_rate_at_group_speed']-1) < 1e-14
    assert abs(rows[5]['omega_measured']-rows[0]['omega_measured']) < 2e-6
    return {'spectral_cases': rows, 'massless_uniform_no_clock': True,
            'zero_group_speed_high_k_is_not_rest_clock': True,
            'Nyquist_rest_gap_doubling_observed': True,
            'unstable_mu7_still_rewinds': True, 'unstable_mu7_amplification_24_ticks': amplification,
            'Nyquist_zero_derivative_warning': 'k=pi and k=0 share the same gap; central differences have doubling.',
            'continuum_clock_identity_exact_at_finite_lattice_spacing': False}


def main():
    from validation.completion.common45 import build45
    common_fingerprint = build45().tensor.fingerprint
    assert common_fingerprint != build().fingerprint
    report = {'schema': 'universe24/native-packet-clock/1', 'baseline_pin': BASE_PIN,
              'common45_tensor_sha256': common_fingerprint,
              'scope': 'Source-only fixed-flat one-direction massive linear field primitive; no GR, stress source, detector or proper-clock acceptance.',
              'derivation': analytic_derivation(), 'mechanics': mechanics(),
              'spectral_controls': spectral_controls(),
              'packets': [run_packet(), run_packet(carrier=-4, axis=1)],
              'gates': {'flat_localized_wave_packet': 'passed', 'same_field_spectral_gap_and_phase': 'passed',
                        'exact_carry_mechanics_and_replay': 'passed', 'continuum_SR_clock_exact_at_fixed_spacing': 'failed',
                        'fixed_physical_mass_refinement': 'blocked', 'common45_curved_packet': 'not_tested',
                        'operational_clock_apparatus': 'not_tested', 'Einstein_source_and_backreaction': 'not_tested'}}
    report['source_sha256'] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in (Path(__file__), ROOT/'validation/completion/time_stability.py',
                  ROOT/'universe24/core/engine.py', ROOT/'universe24/core/tensor.py')}
    output = ROOT/'runs/generic-structure/packet_clock.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
