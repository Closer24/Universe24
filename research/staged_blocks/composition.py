"""Strict initial composition and honest four-block recordings; no runtime gates."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import gzip
import hashlib
import json
from pathlib import Path
import time

from research.components import (BoardSpec, GuidedPacketSource, GuideSegment,
                                 Receiver, TensorSpec, place, finalize, plain)
from research.components.compose import PreparedBoard
from research.components.spec import Placement, freeze, local_address
from research.experiments.run import (FORMAT, assemble, canonical, digest,
                                      recorded_states, run_experiment, source_hashes)
from research.presenter.export import bundle, write_bundle
from universe24 import State
from universe24.core.group_2o import group, rotate
from universe24.observation import clicks
from .contracts import load_catalog, stage_report

HERE = Path(__file__).resolve().parent


@dataclass(frozen=True, slots=True)
class RunContext:
    board: BoardSpec
    seed: int = 0
    time0: int = 0

    def __post_init__(self):
        if not isinstance(self.board, BoardSpec):
            raise TypeError('RunContext needs an existing BoardSpec')
        if type(self.seed) is not int:
            raise ValueError('The preparation seed must be an exact integer')
        if type(self.time0) is not int or self.time0 != 0:
            raise ValueError('Components may only be assembled at time0=0')


@dataclass(frozen=True, slots=True)
class ComponentPreparation:
    placement: Placement
    side: int
    seed: int = 0
    time0: int = 0
    reserved_channels: tuple = ()

    def __post_init__(self):
        if not isinstance(self.placement, Placement):
            raise TypeError('A component must wrap an existing immutable Placement')
        for key in ('side', 'seed', 'time0'):
            if type(getattr(self, key)) is not int:
                raise ValueError(f'{key} must be an exact integer')
        reserved = tuple(local_address(a) for a in self.reserved_channels)
        if len(set(reserved)) != len(reserved):
            raise ValueError('Reserved channels must be distinct')
        assigned = {a for a, _ in self.placement.patch.cells}
        if any(a not in assigned for a in reserved):
            raise ValueError('Every reserved channel needs an explicit initial triple')
        object.__setattr__(self, 'reserved_channels', reserved)


def _world_address(placement, address, cube):
    algebra = group()
    xyz = rotate(algebra.rotations[placement.orientation], address[:3])
    xyz = tuple(x + offset for x, offset in zip(xyz, placement.at))
    if placement.wrap:
        xyz = tuple(x % cube.side for x in xyz)
    return cube.validate_address((*xyz, algebra.multiplication[placement.orientation][address[3]]))


def compose_initial(context, components):
    """Check shared preparation context, then delegate to the existing finalizer."""
    if not isinstance(context, RunContext):
        raise TypeError('Expected a RunContext')
    components = tuple(components)
    if any(not isinstance(item, ComponentPreparation) for item in components):
        raise TypeError('Only data-only ComponentPreparation values are accepted')
    names = [item.placement.name for item in components]
    if len(set(names)) != len(names):
        raise ValueError('Component names must be unique')
    from universe24 import Cube
    cube = Cube(context.board.side)
    owners, reservations = {}, {}
    for item in sorted(components, key=lambda component: component.placement.name):
        p = item.placement
        for field, expected in (('side', context.board.side), ('seed', context.seed), ('time0', context.time0)):
            actual = getattr(item, field)
            if actual != expected:
                raise ValueError(f'Context conflict for {p.name}: {field}={actual}, expected {expected}')
        if p.patch.tensor != context.board.tensor:
            raise ValueError(f'Tensor conflict for {p.name}: signs={p.patch.tensor.body_signs}, '
                             f'fingerprint={p.patch.tensor.fingerprint}; expected signs={context.board.tensor.body_signs}, '
                             f'fingerprint={context.board.tensor.fingerprint}; body actions remain (0,1,3)')
        if p.patch.background != context.board.background:
            raise ValueError(f'Background conflict for {p.name}: {tuple(p.patch.background)}, '
                             f'expected {tuple(context.board.background)}')
        transformed = {}
        for address, value in p.patch.cells:
            target = _world_address(p, address, cube)
            if target in transformed:
                raise ValueError(f'Placement {p.name} aliases local channels at {target}')
            transformed[target] = value
            if target in owners and owners[target][1] != value:
                previous, old = owners[target]
                raise ValueError(f'Initial-state conflict at {target}: {previous}={tuple(old)}; '
                                 f'{p.name}={tuple(value)}; neither overwrite nor addition is allowed')
            if target in reservations and reservations[target] != p.name:
                previous, old = owners[target]
                raise ValueError(f'Channel resource conflict at {target}: reserved by {reservations[target]}, '
                                 f'{previous}={tuple(old)}; also assigned by {p.name}={tuple(value)}')
            owners.setdefault(target, (p.name, value))
        for address in item.reserved_channels:
            target = _world_address(p, address, cube)
            if target in owners and owners[target][0] != p.name:
                previous, value = owners[target]
                raise ValueError(f'Channel resource conflict at {target}: {p.name} reserves '
                                 f'{tuple(transformed[target])}; {previous} already assigns {tuple(value)}')
            reservations[target] = p.name
    prepared = finalize(context.board, [item.placement for item in components])
    manifest = plain(prepared.manifest)
    manifest['staged_context'] = {'side': context.board.side, 'seed': context.seed,
                                  'time0': context.time0, 'preparation_only': True}
    manifest['reserved_channels'] = [{'address': list(a), 'owner': owner}
                                     for a, owner in sorted(reservations.items())]
    return PreparedBoard(prepared.engine, prepared.initial, prepared.ports, prepared.sources,
                         prepared.readouts, freeze(manifest))


def _source_addresses(prepared, source_names):
    names = tuple(prepared.sources) if source_names is None else tuple(source_names)
    if len(set(names)) != len(names) or any(name not in prepared.sources for name in names):
        raise ValueError('Source names must be distinct declared source ports')
    return {address for name in names for address in prepared.sources[name]}


def source_off_state(prepared, source_names=None):
    """Zero designated initial source counters only, preserving every remainder."""
    addresses = _source_addresses(prepared, source_names)
    cells = dict(prepared.initial.cells)
    for address in addresses:
        cells[address] = (0, 0, prepared.initial.at(address).r)
    return State(prepared.initial.cube, prepared.initial.background, cells)


def validate_source_off(on, off, source_names=None):
    source_names = None if source_names is None else tuple(source_names)
    if (on.initial.cube != off.initial.cube or on.initial.background != off.initial.background
            or on.engine.coupling != off.engine.coupling or on.ports != off.ports or on.sources != off.sources
            or on.manifest.get('staged_context') != off.manifest.get('staged_context')):
        raise ValueError('Source-off context conflict: board, background, tensor and ports must agree')
    expected = source_off_state(on, source_names)
    for address in sorted(expected.cells.keys() | off.initial.cells.keys()):
        before, after = expected.at(address), off.initial.at(address)
        if before != after:
            raise ValueError(f'Source-off conflict at {address}: expected {tuple(before)}, got {tuple(after)}; '
                             'only designated initial source counters may change')
    return {'matched_source_off': True, 'source_ports': list(on.sources) if source_names is None else list(source_names),
            'all_remainders_preserved': True, 'apparatus_preserved': True}


def _patch_params(patch):
    return {'kind': patch.kind, 'cells': [[*a, *v] for a, v in patch.cells],
            'background': list(patch.background), 'ports': plain(patch.ports),
            'sources': plain(patch.sources), 'readouts': plain(patch.readouts),
            'evidence_domains': plain(patch.evidence_domains),
            'sockets': [{'name': s.name, 'addresses': plain(s.addresses),
                         'allowed_kinds': list(s.allowed_kinds)} for s in patch.sockets]}


def experiment_spec(context, components, *, identifier, steps, title, description,
                    controls=None, detectors=(), view=None):
    """Compile existing patches to the existing native experiment format."""
    components = tuple(components)
    checked = compose_initial(context, components)
    spec = {'format': FORMAT, 'id': identifier, 'title': title, 'description': description,
            'board': {'side': context.board.side, 'background': list(context.board.background),
                      'tensor': context.board.tensor.data()}, 'steps': steps, 'seed': context.seed,
            'components': [{'name': item.placement.name, 'recipe': 'Patch',
                            'params': _patch_params(item.placement.patch), 'at': list(item.placement.at),
                            'orientation': item.placement.orientation, 'wrap': item.placement.wrap}
                           for item in components], 'detectors': list(detectors),
            'controls': controls or {}, 'provenance': {'time0': 0, 'initial_data_only': True},
            'budget': {'max_frames': steps + 1, 'max_cells': 500000,
                       'max_bytes': 67108864, 'max_seconds': 30}}
    if view is not None:
        spec['view'] = view
    if assemble(spec).initial != checked.initial:
        raise AssertionError('Native serialization changed the composed initial state')
    return spec


def example_specs(*, side=33, steps=24, seed=0):
    """Four native runs: isolated/connected four-block assemblies, each on/off."""
    from .orbit import ShieldedOrbit
    if type(side) is not int or side < 33 or type(steps) is not int or not 24 <= steps <= 40:
        raise ValueError('Registered demo domain is side>=33 and 24<=steps<=40')
    tensor = TensorSpec.from_signs((1, 1, 1))
    context = RunContext(BoardSpec(side, tensor=tensor), seed)
    mid, lane, far = side // 2, side // 4, 3 * side // 4
    specs = []
    for arrangement in ('isolated', 'connected'):
        receiver = (16, mid, far) if arrangement == 'isolated' else (16, lane, mid)
        sockets = [4, 5, 6, 7] + ([16] if arrangement == 'connected' else [])
        for present in (True, False):
            patches = [
                place(GuideSegment(start=0, stop=side-1, sockets=sockets, remainder_pair=(0, 4), tensor=tensor),
                      at=(0, lane, mid), name='guide'),
                place(GuidedPacketSource(present=present, tensor=tensor), at=(4, lane, mid), name='carrier'),
                place(ShieldedOrbit(tensor=tensor), at=(mid, far, mid), name='clock'),
                place(Receiver(remainders=(4, 2), tensor=tensor), at=receiver, name='memory')]
            components = [ComponentPreparation(p, side, seed) for p in patches]
            identifier = f'four-blocks-{arrangement}-' + ('on' if present else 'off')
            specs.append(experiment_spec(context, components, identifier=identifier, steps=steps,
                title=f'Four blocks: {arrangement}, carrier ' + ('present' if present else 'absent'),
                description=('Carrier, periodic guide, prepared local clock and initially prepared passive memory. '
                             + ('The separated regions test coexistence only.' if arrangement == 'isolated' else
                                'The memory intersects the carrier lane. Actual interaction and strict pending-memory acceptance are separate observations.')
                             + ' The clock is prepared directly, not written by light. Source-off preserves the clock and every remainder.'),
                controls={'arrangement': arrangement, 'carrier_present': present, 'source_off_ports': ['carrier.packet'],
                          'receiver': list(receiver), 'carrier_lane': [lane, mid], 'source_x': 4,
                          'prepared_orbit_not_capture': True},
                detectors=('memory.node', 'clock.center', 'carrier.front'), view={'port': 'memory.memory'}))
    return specs


def _project(state, addresses):
    return tuple(tuple(state.at(tuple(a))) for a in addresses)


def _assess(spec, prepared, states):
    clock = prepared.ports['clock.region']
    receiver = prepared.ports['memory.node']
    clock_trace = [_project(state, clock) for state in states]
    receiver_trace = [_project(state, receiver) for state in states]
    event_rows = [{'step': t, 'address': list(event.address), 'kind': event.kind,
                   'quotient': str(event.quotient)}
                  for t, (before, after) in enumerate(zip(states, states[1:]), start=1)
                  for event in clicks(before, after, t)]
    target = [(0, 0, 2)] * 48
    target[0], target[14] = (0, 0, 2), (0, 0, 4)
    first_write, last_wait = 9, 17
    receiver_addresses = set(receiver)
    receiver_events = [row for row in event_rows if tuple(row['address']) in receiver_addresses]
    quiet = all(a == b == 0 for row in receiver_trace[:last_wait+1] for a, b, r in row)
    pending = (all(row == tuple(target) for row in receiver_trace[first_write:last_wait+1]) and quiet
               and not any(row['step'] <= last_wait for row in receiver_events))
    return {'prepared_clock_full_region_period4': all(row == clock_trace[t % 4] for t, row in enumerate(clock_trace)),
            'clock_initial_state_repeats_at4': clock_trace[4] == clock_trace[0],
            'receiver_stays_at_initial_record': all(row == receiver_trace[0] for row in receiver_trace),
            'first_receiver_change': next((t for t, row in enumerate(receiver_trace) if row != receiver_trace[0]), None),
            'strict_zero_counter_pending_goal': pending,
            'pending_write_state': first_write, 'pending_last_required_state': last_wait,
            'all_arithmetic_events': event_rows, 'arithmetic_classes_retained': [0, 1, 2],
            'receiver_arithmetic_events': receiver_events, 'signal_capture_proven': False,
            'approval_release_demonstrated': False, 'physical_photon_claim': False}


def _carrier_translation(spec, prepared, states):
    """Compare the isolated carrier lane with its exact translated preparation."""
    lane, z = spec['controls']['carrier_lane']
    side = spec['board']['side']
    rows = ((lane, z), (lane-1, z), (lane+1, z), (lane, z-1), (lane, z+1))
    region = [(x, y, zz, g) for x in range(side) for y, zz in rows for g in range(48)]
    initial = states[0]
    for t, state in enumerate(states):
        shift = t if spec['controls']['carrier_present'] else 0
        for x, y, zz, g in region:
            if state.at((x, y, zz, g)) != initial.at(((x-shift) % side, y, zz, g)):
                return False
    return True


def run(output, *, side=33, steps=24, seed=0, presenter=True):
    """Record real Rule3 runs, keeping negative interaction results publishable."""
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    (output / 'records').mkdir()
    started = time.process_time()
    specs = example_specs(side=side, steps=steps, seed=seed)
    catalog = load_catalog()
    protocol = {'format': 'universe24-staged-composition-protocol-v1', 'side': side, 'steps': steps, 'seed': seed,
                'time0': 0, 'fixed_body_actions': [0, 1, 3], 'fixed_body_signs': [1, 1, 1],
                'cases': specs, 'catalog_sha256': digest(catalog),
                'isolated_acceptance': 'Carrier translates, complete prepared clock retains period4, passive receiver stays unchanged; coexistence only.',
                'connected_observation': 'Actual receiver difference from matched source-off; independently report strict target24 at states9..17, all48 counterszero and no receiver C through17.',
                'source_off': 'Zero only carrier.packet initial counters; preserve every remainder and the prepared clock.',
                'resource_budget_cpu_seconds': 120, 'maximum_output_bytes': 268435456,
                'no_status_promotion': True, 'no_runtime_controller': True}
    protocol_hash = digest(protocol)
    (output / 'protocol.json').write_text(canonical(protocol) + '\n')
    sources = source_hashes()
    root = HERE.parents[1]
    for name in ('contracts.py', 'composition.py', 'stages.json', 'protocol.md', 'orbit.py'):
        path = HERE / name
        sources[str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
    (output / 'registration.json').write_text(canonical({'protocol_sha256': protocol_hash, 'source_sha256': sources}) + '\n')
    entries, preparations, full_states = [], {}, {}
    for spec in specs:
        if time.process_time() - started > 120:
            raise RuntimeError('Registered composition CPU budget exceeded')
        result = run_experiment(spec)
        prepared = assemble(spec)
        states = recorded_states(result['experiment'])
        assessment = _assess(spec, prepared, states)
        if spec['controls']['arrangement'] == 'isolated':
            assessment['carrier_translation_or_stationary_off_control'] = _carrier_translation(spec, prepared, states)
        if not result['experiment']['provenance']['full_rewind_equal']:
            raise AssertionError('Full-state rewind failed')
        entries.append({'spec': spec, 'assembly': result['assembly'], 'experiment': result['experiment'],
                        'observations': result['observations'], 'assessment': assessment,
                        'protocol_sha256': protocol_hash, 'source_sha256': sources})
        preparations[spec['id']], full_states[spec['id']] = prepared, states
    checks = {}
    for arrangement in ('isolated', 'connected'):
        name = 'four-blocks-' + arrangement
        on, off = preparations[name+'-on'], preparations[name+'-off']
        checks[arrangement] = validate_source_off(on, off, ['carrier.packet'])
        on_states, off_states = full_states[name+'-on'], full_states[name+'-off']
        region = on.ports['memory.node']
        changed = [t for t, (a, b) in enumerate(zip(on_states, off_states)) if _project(a, region) != _project(b, region)]
        checks[arrangement]['receiver_differs_from_source_off_at'] = changed
        checks[arrangement]['prepared_clock_unchanged_by_source_control'] = all(
            _project(a, on.ports['clock.region']) == _project(b, off.ports['clock.region'])
            for a, b in zip(on_states, off_states))
    records = []
    for entry in entries:
        filename = entry['spec']['id'] + '.json.gz'
        path = output / 'records' / filename
        path.write_bytes(gzip.compress(canonical(entry).encode('ascii'), mtime=0))
        records.append(str(path.relative_to(output)))
    for name, expected in sources.items():
        if hashlib.sha256((root / name).read_bytes()).hexdigest() != expected:
            raise RuntimeError('Composition source changed during recording: ' + name)
    isolated = [entry['assessment'] for entry in entries if entry['spec']['controls']['arrangement'] == 'isolated']
    isolated_pass = all(row['prepared_clock_full_region_period4'] and row['receiver_stays_at_initial_record']
                        and row['carrier_translation_or_stationary_off_control'] for row in isolated)
    connected = next(entry['assessment'] for entry in entries if entry['spec']['id'] == 'four-blocks-connected-on')
    report = {'format': 'universe24-staged-composition-result-v1', 'status': 'completed',
              'protocol_sha256': protocol_hash, 'source_sha256': sources, 'records': records,
              'checks': checks, 'isolated_coexistence_passed': isolated_pass,
              'connected_interaction_observed': bool(checks['connected']['receiver_differs_from_source_off_at']),
              'connected_strict_pending_goal_passed': connected['strict_zero_counter_pending_goal'],
              'prepared_orbit_not_signal_written': True, 'new_capture_or_approval_claim': False,
              'contract_reports': [stage_report(row['id'], purpose='claim', catalog=catalog) for row in catalog['stages']],
              'cpu_seconds': time.process_time()-started}
    if report['cpu_seconds'] > 120:
        raise RuntimeError('Registered composition CPU budget exceeded')
    (output / 'result.json').write_text(canonical(report) + '\n')
    experiments = [entry['experiment'] for entry in entries]
    write_bundle(output / 'experiments.json', bundle(experiments, title='Four building blocks: coexistence and interaction'))
    if presenter:
        from research.presenter.build import build
        build(output / 'experiments.json', output / 'The_Presenter.html')
    if sum(path.stat().st_size for path in output.rglob('*') if path.is_file()) > protocol['maximum_output_bytes']:
        raise RuntimeError('Registered composition output budget exceeded')
    return {**report, 'experiments': experiments}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args(argv)
    report = run(args.output)
    print(canonical({key: value for key, value in report.items() if key not in {'experiments', 'source_sha256', 'contract_reports'}}))


if __name__ == '__main__':
    main()
