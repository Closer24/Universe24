"""Passive null-clock references and click-only controls for face-phase transport.

No reference metric is supplied to an Engine. Complete replay checks the
provenance of existing runs; the observation function reads clicks alone.
This audit does not turn lattice addresses or update counters into distances
or proper time, and does not claim a gravitational-wave detection.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
import json
import math
from pathlib import Path

from universe24.system.bundle import load_bundle
from universe24.system.runtime import verify_run
from validation.light_link_resonance import build_tensor, make_bundle, prepare

ROOT = Path(__file__).resolve().parents[1]


def tt_roundtrip(t0, *, epsilon=0.01, omega=math.pi/8, arm=1.0):
    """First-order TT result, c=1, equal transverse arms at z=0.

    h_xx=-h_yy=epsilon*cos(omega*(t-z)). The fixed-coordinate endpoint
    observers are freely falling in this gauge. Their proper time equals t.
    Integrate the metric perturbation on unperturbed outgoing/return paths.
    Terms of order epsilon**2 are not claimed.
    """
    if not all(math.isfinite(v) for v in (t0, epsilon, omega, arm)):
        raise ValueError('finite reference parameters required')
    if abs(epsilon) >= 0.1 or omega < 0 or arm <= 0:
        raise ValueError('weak amplitude, nonnegative frequency and positive arm required')
    integral = (2*arm*epsilon if omega == 0 else
                epsilon*(math.sin(omega*(t0+2*arm))-math.sin(omega*t0))/omega)
    return {'emission_coordinate_time': t0,
            'roundtrip_proper_time_x_first_order': 2*arm+integral/2,
            'roundtrip_proper_time_y_first_order': 2*arm-integral/2,
            'differential_proper_time_first_order': integral,
            'tidal_R0x0x_first_order': epsilon*omega**2*math.cos(omega*t0)/2,
            'tidal_R0y0y_first_order': -epsilon*omega**2*math.cos(omega*t0)/2}


def reference_panel():
    """Independent analytic and midpoint-integral agreement, never runtime input."""
    epsilon, omega, arm = 0.01, math.pi/8, 1.0
    samples = [tt_roundtrip(float(t), epsilon=epsilon, omega=omega, arm=arm)
               for t in range(0, 16, 2)]
    error = 0.0
    partitions = 4096
    width = 2*arm/partitions
    for sample in samples:
        t0 = sample['emission_coordinate_time']
        numeric = width*sum(epsilon*math.cos(omega*(t0+(k+0.5)*width))
                            for k in range(partitions))
        error = max(error, abs(numeric-sample['differential_proper_time_first_order']))
        assert abs(sample['roundtrip_proper_time_x_first_order']+
                   sample['roundtrip_proper_time_y_first_order']-4*arm) < 1e-12
    assert error < 1e-9
    assert any(s['differential_proper_time_first_order'] > 0 for s in samples)
    assert any(s['differential_proper_time_first_order'] < 0 for s in samples)
    assert tt_roundtrip(0.0, epsilon=0.0)['differential_proper_time_first_order'] == 0
    assert tt_roundtrip(0.0, omega=0.0)['differential_proper_time_first_order'] == 2*arm*epsilon
    return {'status': 'passed', 'role': 'passive independent target only',
            'approximation': 'first order in epsilon; no long-wavelength approximation',
            'c': 1, 'epsilon': epsilon, 'omega': omega, 'coordinate_arm': arm,
            'analytic_midpoint_max_error': error, 'samples': samples,
            'runtime_receives_reference': False}


def metric_ambiguity():
    """Six face norms fail to fix even a constant spatial metric's shear."""
    zero, one, half = Fraction(0), Fraction(1), Fraction(1, 2)
    diagonal = ((one, zero, zero), (zero, one, zero), (zero, zero, one))
    shear = ((one, half, zero), (half, one, zero), (zero, zero, one))

    def norm(metric, vector):
        return sum(metric[i][j]*vector[i]*vector[j] for i in range(3) for j in range(3))

    axes = [tuple(s if i == axis else 0 for i in range(3))
            for axis in range(3) for s in (-1, 1)]
    norms = [[norm(metric, v) for v in axes] for metric in (diagonal, shear)]
    assert norms[0] == norms[1] == [1]*6
    diagonal_norms = [norm(metric, (1, 1, 0)) for metric in (diagonal, shear)]
    assert diagonal_norms == [2, 3]
    return {'six_axis_squared_lengths': [[str(v) for v in row] for row in norms],
            'xy_diagonal_squared_lengths': [str(v) for v in diagonal_norms],
            'spatial_determinants': ['1', '3/4'],
            'xy_angle_cosines': ['0', '1/2'],
            'claim_six_face_lengths_determine_full_metric': 'failed',
            'scope': 'Both metrics are positive definite and flat; this proves missing shear data, not curvature.'}


def click_signature(click_path, *, address, horizon):
    """Read local click data only; no seed, hidden trace or reconstructed field.

    Address and horizon are declared observation settings, not spatial units
    or proper time. The histogram deliberately coarse-grains channel identity.
    Complete channel-labelled records remain in the input stream.
    """
    counters = {tick: Counter() for tick in range(1, horizon+1)}
    with gzip.open(click_path, 'rt') as stream:
        for line in stream:
            event = json.loads(line)
            if event['xyz'] == list(address):
                if not 1 <= event['step'] <= horizon:
                    raise ValueError('click falls outside declared observation horizon')
                counters[event['step']][(event['quotient'], event['kind'], event['sign'])] += 1
    return [{'update_index': tick, 'arithmetic_event_count': sum(counter.values()),
             'histogram': [[q, kind, sign, count]
                           for (q, kind, sign), count in sorted(counter.items())]}
            for tick, counter in counters.items()]


def verified_phase_fixture(directory, axis):
    """Auditor provenance check, separate from the click-only observation."""
    report = verify_run(directory)
    bundle = load_bundle(Path(directory)/'bundle')
    model = bundle.model
    p, metadata = model['parameters'], model['preparation']
    if not p.get('phase_gate') or metadata['axis'] != axis or metadata['sign'] != 1:
        raise ValueError('the registered positive-axis matched-phase fixture is required')
    if metadata['textured'] or not metadata['paused_history'] or metadata['L'] != 4:
        raise ValueError('the registered homogeneous matched predecessor at L=4 is required')
    fields = ('L', 'precision', 'bias', 'amplitude', 'textured', 'axis', 'sign',
              'polarization', 'paused_history')
    seed, expected_metadata = prepare(**{k: metadata[k] for k in fields})
    expected = make_bundle(build_tensor(**p), seed, p, expected_metadata)
    if expected.bundle_id != bundle.bundle_id:
        raise ValueError('declared fixture differs from its complete prepared bundle')
    return report


def source_hashes():
    names = ('validation/geodesic_link_audit.py', 'validation/light_link_resonance.py',
             'universe24/light.py', 'universe24/system/runtime.py',
             'universe24/system/decoder.py', 'universe24/core/engine.py')
    return {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names}


def run(run_root, out):
    """Inspect existing canonical runs and save a fresh passive audit report."""
    run_root, out = Path(run_root), Path(out)
    out.mkdir(parents=True, exist_ok=False)
    sources = source_hashes()
    paths = (run_root/'phase-0-1-1', run_root/'phase-1-1-0')
    reports = [verified_phase_fixture(path, axis) for axis, path in enumerate(paths)]
    if reports[0]['steps'] != reports[1]['steps'] or reports[0]['tensor_hash'] != reports[1]['tensor_hash']:
        raise ValueError('comparison requires a common tensor and observation horizon')
    signatures = [click_signature(path/'clicks.jsonl.gz', address=address,
                                  horizon=reports[0]['steps'])
                  for path, address in zip(paths, ((3, 0, 0), (0, 3, 0)))]
    equal = signatures[0] == signatures[1]
    if not equal:
        raise AssertionError('registered homogeneous directional click control changed')
    result = {
        'schema': 'universe24/geodesic-link-audit/1',
        'source_hashes': sources,
        'inputs': [{'run_id': report['run_id'], 'tensor_hash': report['tensor_hash'],
                    'steps': report['steps'], 'channels': report['channels_per_node'],
                    'click_file_sha256': report['files']['clicks.jsonl.gz']}
                   for report in reports],
        'passive_tt_reference': reference_panel(),
        'six_face_metric_counterexample': metric_ambiguity(),
        'click_only_control': {'addresses': [[3, 0, 0], [0, 3, 0]],
                               'same_local_histograms_on_xy': equal,
                               'x': signatures[0], 'y': signatures[1],
                               'proper_time_assignment': None,
                               'emission_reflection_return_assignment': None,
                               'scope': 'Local quotient/class/sign histograms only; not a claim that all channel-labelled records coincide.'},
        'time_chart_control': {
            'smooth_positive_lapse': 'ds^2=-N(t)^2 dt^2+dx^2+dy^2+dz^2; tau=int N dt makes this flat',
            'phase_transport_count': 'ceil(t/2)',
            'microscopic_lorentzian_time_coordinate': 'not_established',
            'reason': 'The move/hold transport count has plateaus; it is not an invertible time coordinate or a material clock.'},
        'gates': {'independent_tt_null_roundtrip_reference': 'passed',
                  'current_bundle_replay_and_admission': 'passed',
                  'homogeneous_equal_axis_click_control': 'passed',
                  'six_axis_norms_determine_full_spatial_metric': 'failed',
                  'homogeneous_scalar_gate_identifies_plus_polarized_gravity': 'failed',
                  'source_coupled_einstein_equations': 'not_tested',
                  'retained_clock_and_reflection_proper_time_measurement': 'not_tested',
                  'general_gw_response_of_other_preparations': 'not_tested',
                  'physical_event_geometry_acceptance': 'blocked'},
        'scope': 'No external metric drives evolution. The reference is a future target, not a calibrated numerical comparison to these arithmetic clicks.'}
    if sources != source_hashes():
        raise AssertionError('audit source changed during collection')
    (out/'geodesics.json').write_text(json.dumps(result, indent=2)+'\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runs', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = run(args.runs, args.out)
    print(json.dumps({'gates': result['gates']}, indent=2))
