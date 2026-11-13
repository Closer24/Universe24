"""Bind the sourced six-channel audit to the existing saved-run runtime.

This module is a source-only validation client, not an alternate execution
interface. The generic runtime retains its mechanical acceptance gates; the
restricted physical diagnostics below consume its verified complete trace.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction as F
import gzip
from hashlib import sha256
import json
from pathlib import Path
import tempfile

import mpmath as mp

from universe24.core import Engine, State, exact_json
from universe24.system.bundle import canonical_bytes, create_bundle, load_bundle
from universe24.system.decoder import default_protocol, decode_trace
from universe24.system.runtime import run_bundle, verify_run
from .native import build_native, prepare_native, read_conserved, scalar_step
from .physical_map import exact_readout, physical_decode, validate_domain


ROOT = Path(__file__).resolve().parents[2]
MODEL_ID = 'sourced-massless-flrw-volume-audit'
MODEL_DOMAIN = ('Spatially flat homogeneous isotropic expanding FLRW; mass_squared=0; '
                'D>0, P!=0, V>0 and U>sqrt(3P^2/2); exact constraint; '
                'complete compatible history; no spatial modes or operational apparatus.')


def model_metadata(N):
    """Exact, static interpretation bound into the ordinary bundle hash."""
    program = build_native(N)
    return {'id': MODEL_ID, 'version': '1', 'domain': MODEL_DOMAIN,
            'N': N, 'proper_time_step': str(program.h), 'mass_squared': 0,
            'physical_units': 'c=8*pi*G=1; unit lapse; proper time tau',
            'coordinates': {'V': 'b_volume/(4*N^2)',
                            'U': '(b_volume-a_volume+3*b_dust_charge)/(4*N)',
                            'D': 'b_dust_charge', 'P': 'b_scalar_charge',
                            'Uref': 'b_reference_velocity/(4*N)',
                            'phi_ref': 'b_scalar_offset', 'tau': 'b_proper_tick/N'},
            'metric': 'ds^2=-d_tau^2+V^(2/3)*(dx^2+dy^2+dz^2)',
            'root_branches': 'B=V^(-1/3)>0; d=sqrt(D/V)>0',
            'scalar_phase': 'retained Uref and phi_ref anchor the present-state logarithmic coordinate',
            'observation_input': 'full retained state diagnostic',
            'canonical_click_role': 'unchanged arithmetic protocol; no physical detector claim'}


def channel_manifest(program):
    purposes = ('scaled physical volume, both histories encode expansion velocity',
                'comoving dust density, frozen complete history',
                'signed comoving scalar momentum, frozen complete history',
                'retained scalar-phase reference velocity, frozen complete history',
                'retained scalar integration offset, frozen complete history',
                'proper-time coordinate counter, not a material clock')
    return [{'index': i, 'name': gear.name, 'label': gear.label,
             'owner': 'validation.sourced_map', 'purpose': purposes[i]+'; all carries retained'}
            for i, gear in enumerate(program.tensor.gears)]


def make_bundle(program, seed):
    """Declare a physical research preparation without altering any register."""
    validate_domain(read_conserved(program, seed))
    return create_bundle(program.tensor, seed, channels=channel_manifest(program),
                         protocol=default_protocol(), model=model_metadata(program.N))


def _check_interpretation(bundle):
    model = bundle.model
    if type(model.get('N')) is not int:
        raise ValueError('saved source interpretation needs exact integer N')
    program = build_native(model['N'])
    expected = make_bundle(program, prepare_native(program))
    if bundle.tensor.fingerprint != expected.tensor.fingerprint:
        raise ValueError('saved tensor is not the declared sourced volume law')
    if model != model_metadata(program.N):
        raise ValueError('saved mass, physical-time calibration or coordinate declaration differs')
    if bundle.protocol != default_protocol() or list(bundle.channels) != list(expected.channels):
        raise ValueError('saved observation protocol or channel ownership differs')
    validate_domain(read_conserved(program, bundle.seed))
    return program


def _records(path):
    with gzip.open(path, 'rt', encoding='utf-8') as stream:
        return [exact_json.loads(line) for line in stream]


def _digest(value):
    return sha256(canonical_bytes(value)).hexdigest()


def _exact_strings(value):
    return {key: str(number) for key, number in value.items()}


@dataclass(frozen=True)
class RunObservation:
    N: int
    run_id: str
    bundle_id: str
    tensor_sha256: str
    seed_sha256: str
    model_sha256: str
    trace_sha256: str
    steps: int
    initial_physical_coordinates: tuple
    final_time: F
    final_rational_fields: tuple
    final_physical_fields: tuple


def _preparation_key(values):
    return tuple((name, F(values[name])) for name in ('V','U','D','P','Uref','phi_ref','tau'))


def inspect_run(path):
    """Replay saved inputs, then derive scoped diagnostics from saved states.

    The independent scalar recurrence and generic canonical decoder both read
    the verified records. No cached target trajectory supplies a state.
    """
    path = Path(path)
    report = verify_run(path)
    bundle = load_bundle(path/'bundle')
    program = _check_interpretation(bundle)
    records = _records(path/'full_trace.jsonl.gz')
    saved_clicks = _records(path/'clicks.jsonl.gz')
    reconstructed = decode_trace(records, bundle.tensor, run_id=report['run_id'],
                                 expected_steps=report['steps'], initial_state=bundle.seed)
    if saved_clicks != reconstructed:
        raise AssertionError('passive canonical click stream differs')
    if not records:
        raise ValueError('physical audit requires a nonempty saved trajectory')
    seed = bundle.seed
    previous, engine = seed, Engine(bundle.tensor)
    initial = read_conserved(program, seed)
    physical_rows = []
    scalar_comparisons = 0
    for index, record in enumerate(records, 1):
        before, after = (State.from_dict(record[key]) for key in ('before','after'))
        if not before.same_as(previous) or not after.same_as(scalar_step(before)):
            raise AssertionError('saved state does not match independent scalar recurrence')
        if not engine.inverse_step(after).same_as(before):
            raise AssertionError('saved complete-state inverse failed')
        values = read_conserved(program, after)
        rational = exact_readout(values)
        physical = physical_decode(values, precision=80)
        if values['tau'] != initial['tau']+F(index, program.N) or values['invariant'] != 0:
            raise AssertionError('saved physical-time/constraint identity failed')
        if rational['constraint'] != 0:
            raise AssertionError('saved physical constraint is not exactly zero')
        with mp.workdps(80):
            physical_rows.append({'step': index, 'conserved': _exact_strings(values),
                                  'rational': _exact_strings(rational),
                                  'physical': {key: mp.nstr(value, 70) for key,value in physical.items()}})
        scalar_comparisons += 3*after.G*after.N
        previous = after
    if not engine.rewind(previous, len(records)).same_as(seed):
        raise AssertionError('saved complete trajectory failed full rewind')
    if any(report['acceptance_gates'][key]['status'] != 'not_tested' for key in 'CDEF'):
        raise AssertionError('generic runtime promoted a physical acceptance gate')
    observation = RunObservation(
        N=program.N, run_id=report['run_id'], bundle_id=report['bundle_id'],
        tensor_sha256=bundle.tensor.fingerprint, seed_sha256=_digest(seed.to_dict()),
        model_sha256=_digest(bundle.model), trace_sha256=report['files']['full_trace.jsonl.gz'],
        steps=len(records), initial_physical_coordinates=_preparation_key(initial),
        final_time=F(physical_rows[-1]['conserved']['tau']),
        final_rational_fields=tuple(sorted(physical_rows[-1]['rational'].items())),
        final_physical_fields=tuple(sorted(physical_rows[-1]['physical'].items())))
    result = {'path': str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
              'N': program.N, 'steps': len(records), 'run_id': report['run_id'],
              'bundle_id': report['bundle_id'], 'tensor_sha256': bundle.tensor.fingerprint,
              'seed_sha256': observation.seed_sha256, 'model_sha256': observation.model_sha256,
              'trace_sha256': observation.trace_sha256,
              'final_proper_time': str(observation.final_time),
              'saved_physical_rows': physical_rows,
              'independent_scalar_integer_comparisons': scalar_comparisons,
              'canonical_click_count': len(saved_clicks), 'canonical_click_parity': 'passed',
              'complete_inverse_and_rewind': 'passed',
              'maximum_retained_bits_by_step': report['maximum_integer_bits_by_step'],
              'generic_physical_gates': {key: report['acceptance_gates'][key]['status'] for key in 'CDEF'},
              'restricted_exact_constraint': 'zero at every saved physical step',
              'observation_role': 'full-state diagnostic; not arithmetic clicks or operational clock records'}
    return observation, result


def require_same_run(left, right):
    """Scoped comparison of locally created receipts, not authentication."""
    if type(left) is not RunObservation or type(right) is not RunObservation:
        raise TypeError('RunObservation receipts required')
    fields = ('N','run_id','bundle_id','tensor_sha256','seed_sha256','model_sha256',
              'trace_sha256','steps','final_time')
    if any(getattr(left,key) != getattr(right,key) for key in fields):
        raise ValueError('observations do not come from the same complete run and interpretation')
    return True


def compare_resolution(left, right):
    """Explicit physical-resolution comparison; never a same-run join."""
    if type(left) is not RunObservation or type(right) is not RunObservation:
        raise TypeError('RunObservation receipts required')
    if left.N == right.N:
        raise ValueError('resolution comparison requires distinct declared resolutions')
    if left.tensor_sha256 != right.tensor_sha256:
        raise ValueError('resolution comparison changed the immutable tensor')
    if left.initial_physical_coordinates != right.initial_physical_coordinates:
        raise ValueError('different physical preparation or retained phase anchor')
    if left.final_time != right.final_time:
        raise ValueError('different final proper-time intervals')
    if left.final_rational_fields != right.final_rational_fields:
        raise ValueError('exact rational physical endpoints differ')
    if left.final_physical_fields != right.final_physical_fields:
        raise ValueError('same-precision root/log diagnostics differ')
    return {'kind': 'explicit_resolution_comparison', 'same_run': False,
            'N_values': [left.N,right.N], 'final_proper_time': str(left.final_time),
            'same_exact_rational_endpoint': True, 'same_root_log_diagnostics': True}


def run_audit(out=None):
    """Run the native bundle using existing runtime functions, then inspect."""
    if out is None:
        parent = ROOT/'runs/sourced-map/runtime'
        parent.mkdir(parents=True, exist_ok=True)
        out = Path(tempfile.mkdtemp(prefix='runtime-', dir=parent))
    else:
        out = Path(out)
        if out.exists():
            raise ValueError('sourced runtime audit requires a fresh output directory')
        out.mkdir(parents=True)
    observations, runs = [], []
    for N in (24,48,96):
        program = build_native(N)
        bundle = make_bundle(program, prepare_native(program))
        directory = out/f'N{N}'
        run_bundle(bundle, directory, N//8)
        receipt, evidence = inspect_run(directory)
        observations.append(receipt); runs.append(evidence)
    joins = [compare_resolution(observations[0], other) for other in observations[1:]]
    require_same_run(observations[0], inspect_run(out/'N24')[0])
    negative = {}
    def reject(name, callback):
        try:
            callback()
        except (TypeError,ValueError) as error:
            negative[name] = {'status': 'rejected', 'reason': str(error)}
        else:
            raise AssertionError(f'invalid observation accepted: {name}')
    reject('same_tensor_different_resolution_is_not_same_run',
           lambda: require_same_run(observations[0],observations[1]))
    reject('same_resolution_is_not_a_resolution_comparison',
           lambda: compare_resolution(observations[0],observations[0]))
    reject('different_physical_final_time',
           lambda: compare_resolution(observations[0],replace(observations[1],final_time=F(1,4))))
    reject('altered_physical_preparation',
           lambda: compare_resolution(observations[0],replace(observations[1],initial_physical_coordinates=())))
    program = build_native(24)
    seed = prepare_native(program)
    changed = seed.copy(); changed.r[0,0] = (int(changed.r[0,0])+1)%6
    changed_bundle = make_bundle(program,changed)
    run_bundle(changed_bundle,out/'changed-carry',3)
    carry_observation, carry_run = inspect_run(out/'changed-carry')
    if carry_observation.final_rational_fields != observations[0].final_rational_fields:
        raise AssertionError('carry-transparent fixture unexpectedly changed physical readouts')
    reject('same_physical_fields_different_complete_seed',
           lambda: require_same_run(observations[0],carry_observation))
    runs.append(carry_run)
    # Coordinate-time origin is a label: shift both retained counter slices,
    # leave the actual geometry/sources untouched and retain the same lapse.
    shifted = seed.copy(); shifted.a[5] += 10; shifted.b[5] += 10
    shifted_bundle = make_bundle(program,shifted)
    run_bundle(shifted_bundle,out/'shifted-time-origin',3)
    shifted_observation, shifted_run = inspect_run(out/'shifted-time-origin')
    if shifted_observation.final_time != observations[0].final_time+F(10,24):
        raise AssertionError('saved physical reader lost the coordinate-time origin')
    if shifted_observation.final_rational_fields != observations[0].final_rational_fields:
        raise AssertionError('changing only the coordinate origin changed physical fields')
    shifted_fields = dict(shifted_observation.final_physical_fields)
    original_fields = dict(observations[0].final_physical_fields)
    if any(shifted_fields[key] != original_fields[key] for key in ('B','k','p','phi','d')):
        raise AssertionError('passive fields depend on the coordinate counter origin')
    runs.append(shifted_run)
    valid_bundle = make_bundle(program,seed)
    def relabel(**changes):
        return create_bundle(valid_bundle.tensor,valid_bundle.seed,channels=valid_bundle.channels,
                             protocol=valid_bundle.protocol,model=dict(valid_bundle.model,**changes))
    reject('massive_model_relabel',lambda: _check_interpretation(relabel(mass_squared=1)))
    reject('changed_time_calibration',lambda: _check_interpretation(relabel(proper_time_step='1/48')))
    reject('hidden_state_as_click_only_claim',lambda: _check_interpretation(relabel(observation_input='canonical clicks only')))
    off = seed.copy(); off.a[0] += 1; off.b[0] += 1
    reject('off_constraint_preparation_is_not_projected',lambda: make_bundle(program,off))
    files = ['validation/sourced_map/runtime.py','validation/sourced_map/native.py',
             'validation/sourced_map/physical_map.py','universe24/system/bundle.py',
             'universe24/system/decoder.py','universe24/system/runtime.py']
    return {'schema':'universe24/sourced-map/runtime/1',
            'status':'saved-native-runtime-and-scoped-physical-diagnostics-passed',
            'channels':48,'active_channels':6,'retained_integers_per_node':144,
            'runs':runs,'explicit_resolution_comparisons':joins,
            'negative_controls':negative,
            'source_sha256':{name:sha256((ROOT/name).read_bytes()).hexdigest() for name in files},
            'limitations':['Restricted massless expanding homogeneous scalar+dust chart only.',
                           'Physical diagnostics consume saved complete states, not arithmetic clicks.',
                           'Coordinate counter is not an independent material clock.',
                           'Receipt equality is a compatibility check, not an authenticated semantic proof.',
                           'Generic runtime physical gates C/D/E/F remain not_tested.']}


def main():
    result = run_audit()
    path = ROOT/'runs/sourced-map/runtime.json'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'runs':len(result['runs']),
                      'comparisons':len(result['explicit_resolution_comparisons']),
                      'negative_controls':len(result['negative_controls']),
                      'out':str(path)},indent=2))


if __name__ == '__main__':
    main()
