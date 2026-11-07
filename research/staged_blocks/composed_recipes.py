"""Reusable initial data for audited transmission and driven waiting.

No forward evolution, injected input word, runtime switch or observer feedback
exists here. Shared train halos are solved jointly before immutable patches are
created. Run --verify-domain NEW_DIRECTORY to compare recorded initial bytes.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import gzip
import hashlib
import json
from pathlib import Path
import time

from research.components import BoardSpec, GuidedPacketSource, Patch, TensorSpec, finalize, place, plain
from research.components.spec import freeze
from research.presenter.export import canonical, state_data
from .composition import ComponentPreparation, RunContext, experiment_spec
from .recipes import ClockGuideInterface, InterfaceGuide

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CONTROLS = ('00', '10', '01', '11')
TRANSMISSION_EVIDENCE = ('research/staged_blocks/transmission_protocol.json',
    'research/staged_blocks/evidence/transmission_v1/result.json',
    'research/staged_blocks/evidence/independent_audit/transmission.json')
PAUSE_EVIDENCE = ('research/staged_blocks/pause_bridge_protocol.json',
    'research/staged_blocks/evidence/pause_bridge_v1/result.json',
    'research/staged_blocks/evidence/independent_audit/bridge.json')


def _context(side, delay, control, tensor):
    if type(side) is not int or type(delay) is not int:
        raise ValueError('Board side and delay must be exact integers')
    if control not in CONTROLS:
        raise ValueError('Control must be one of 00, 10, 01, 11')
    tensor = TensorSpec() if tensor is None else tensor
    if not isinstance(tensor, TensorSpec) or tensor.body_signs != (1, 1, 1):
        raise ValueError('These recipes require the fixed +++ body-013 tensor')
    return tensor


def _resources(patch, role):
    return {'role': role, 'assigned_channels': len(patch.cells),
            'tensor_fingerprint': patch.tensor.fingerprint,
            'background': list(patch.background), 'initial_only': True,
            'ports': plain(patch.ports), 'sources': plain(patch.sources)}


@dataclass(frozen=True, slots=True)
class ComposedRecipe:
    board: BoardSpec
    placements: tuple
    metadata: object

    def prepare(self):
        """Check all resource collisions through the existing immutable composer."""
        return finalize(self.board, self.placements)

    def experiment_spec(self, *, identifier=None, steps=40):
        """Return native experiment data; do not execute an experiment."""
        if type(steps) is not int or steps < 0:
            raise ValueError('Steps must be a nonnegative exact integer')
        meta = plain(self.metadata)
        identifier = identifier or meta['id']
        spec = experiment_spec(RunContext(self.board, seed=0),
            [ComponentPreparation(p, self.board.side, seed=0) for p in self.placements],
            identifier=identifier, steps=steps, title=meta['title'],
            description=meta['scope'], controls=meta,
            detectors=(meta['center_port'],), view={'port': meta['clock_port']})
        spec['provenance'].update({'recipe': meta['recipe'], 'initial_only': True,
            'randomness_used': False, 'evidence': meta['evidence'],
            'matches_validated_parameter_domain': steps == 40,
            'physical_comparator_or_approval': False})
        return spec


def effective_coupler(*, side=137, delay=4, family='enable', control='11', tensor=None):
    """Three pieces: guide, carrier, prepared clock interface. Initial masks only.

    The two families have distinct phase-dependent halo preparations. Within
    each family the four controls preserve exactly the same remainder field.
    """
    tensor = _context(side, delay, control, tensor)
    if side not in (137, 193) or delay not in (4, 5, 8, 9) or family not in ('enable', 'aligned_suppress'):
        raise ValueError('Parameters are outside the audited effective-coupler finite domain')
    c, source_x = side//2, side//2-16-delay
    phase = ((2 if family == 'enable' else 0)-delay) % 4
    guide = InterfaceGuide(side=side, packet_start=source_x, interface_x=c, tensor=tensor)
    ports = plain(guide.ports)
    ports.update({'incoming': [(c-8, 0, 0, g) for g in range(48)],
                  'forward': [(c+8, 0, 0, g) for g in range(48)],
                  'backward': [(c-8, 0, 0, g) for g in range(48)]})
    guide = Patch(guide.kind, guide.cells, tensor=tensor, ports=ports,
                  sockets=guide.sockets, evidence_domains=guide.evidence_domains)
    packet = GuidedPacketSource(present=control[0] == '1', tensor=tensor)
    interface = ClockGuideInterface(r=0, phase=phase, present=control[1] == '1', tensor=tensor)
    placements = (place(guide, at=(0, c, c), name='guide'),
                  place(packet, at=(source_x, c, c), name='packet'),
                  place(interface, at=(c, c+1, c), name='interface'))
    meta = {'id': f'coupler-{family}-L{side}-d{delay}-{control}',
            'title': 'Prepared state-dependent guided-carrier transmission',
            'recipe': 'effective_coupler', 'side': side, 'delay': delay,
            'phase': phase, 'family': family, 'control': control, 'time0': 0, 'seed': 0,
            'matches_validated_parameter_domain': True, 'tensor_fingerprint': tensor.fingerprint,
            'clock_port': 'interface.center', 'center_port': 'interface.center_node',
            'source_masks': {'packet.packet': control[0] == '1', 'interface.clock': control[1] == '1'},
            'resources': [_resources(p.patch, p.name) for p in placements],
            'evidence': TRANSMISSION_EVIDENCE,
            'expected_complete_forward_carrier': control == ('11' if family == 'enable' else '10'),
            'forward_match_states': [24+delay, 27+delay], 'validated_horizon': 40,
            'scope': 'Observed exact-template guided-carrier transmission controlled by a prepared clock. '
                     'An absent template is not all-output silence or erased information. '
                     'No incoming-written controller, autonomous capture, approval, splitter or release.'}
    result = ComposedRecipe(BoardSpec(side, tensor=tensor), placements, freeze(meta))
    result.prepare()
    return result


def two_lane_pause(*, side=129, delay=0, control='11', tensor=None):
    """Jointly solve two trains and their shared halo; return three data pieces.

    The clock is always initially present. Bits mask only lower/upper source
    counters. Shared halo values are constructed once, never merged by override.
    """
    tensor = _context(side, delay, control, tensor)
    if side not in (129, 161) or delay not in (0, 1, 2, 3):
        raise ValueError('Parameters are outside the audited driven-pause finite domain')
    # This frozen helper constructs initial cells only; no study runner/observer
    # is called. It validates every shared remainder and clock-halo replacement.
    from .pause_bridge import initial_cells
    c = side//2
    case = {'side': side, 'delay': delay, 'control': control,
            'phase': (2-delay) % 4, 'stage': 'encounter'}
    cells, ports, sources, joint = initial_cells(case)
    row_addresses = {
        'lower': {(x, c, c, g) for x in range(side) for g in (0, 14)},
        'upper': {(x, c+2, c, g) for x in range(side) for g in (6, 36)}}
    if row_addresses['lower'] & row_addresses['upper']:
        raise ValueError('Distinct lane rows overlap')
    lanes = []
    for name in ('lower', 'upper'):
        addresses = row_addresses[name]
        patch = Patch('joint-train-lane', {a: cells[a] for a in addresses}, tensor=tensor,
            ports={'incoming': ports[name+'_incoming'], 'row': sorted(addresses)},
            sources={'train': sources[name]},
            evidence_domains=({'kind': 'joint-pause-lane-v1', 'lane': name,
                'shared_halo_required': True, 'tensor_fingerprint': tensor.fingerprint,
                'evidence': PAUSE_EVIDENCE},))
        lanes.append(place(patch, at=(0, 0, 0), name=name))
    row_union = row_addresses['lower'] | row_addresses['upper']
    shared = {a: v for a, v in cells.items() if a not in row_union}
    # Explicitly reserve the full clock region, including background channels.
    # Where the region meets a lane, both declarations have the identical value.
    for row in ports['region']:
        address = tuple(row)
        value = cells.get(address, (0, 0, 2))
        if address in shared and tuple(shared[address]) != tuple(value):
            raise ValueError(f'Joint resource conflict at {address}: {shared[address]} != {value}')
        shared[address] = value
    bridge = Patch('joint-two-lane-clock', shared, tensor=tensor,
        ports=ports, sources={'clock': sources['clock']},
        evidence_domains=({'kind': 'joint-pause-interface-v1',
            'tensor_fingerprint': tensor.fingerprint, 'joint_preparation': joint,
            'protected_clock_region_channels': 336, 'evidence': PAUSE_EVIDENCE},))
    placements = (*lanes, place(bridge, at=(0, 0, 0), name='bridge'))
    T = 14+delay
    meta = {'id': f'driven-pause-L{side}-d{delay}-{control}',
            'title': 'Two prepared trains drive a local pause and restart',
            'recipe': 'two_lane_pause', **case, 'time0': 0, 'seed': 0,
            'matches_validated_parameter_domain': True, 'tensor_fingerprint': tensor.fingerprint,
            'clock_port': 'bridge.clock', 'center_port': 'bridge.center',
            'source_masks': {'lower.train': control[0] == '1', 'upper.train': control[1] == '1',
                             'bridge.clock': True},
            'resources': [_resources(p.patch, p.name) for p in placements],
            'joint_preparation': joint, 'evidence': PAUSE_EVIDENCE,
            'driven_pause_expected': control == '11', 'pause_states': [T, T+9],
            'restart_state': T+10, 'validated_horizon': 40,
            'scope': 'Observed driven center waiting from two prearranged packet trains. '
                     'The full48 center is constant while incoming terms can cancel; '
                     'autonomous336-region memory failed. No independently generated approval, '
                     'incoming capture or quantum-collapse claim.'}
    result = ComposedRecipe(BoardSpec(side, tensor=tensor), placements, freeze(meta))
    result.prepare()
    return result


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify_preparations(output):
    """Compare all64+32 complete initial bytes directly to frozen recordings."""
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    inputs = [(kind, p) for kind, folder, pattern in
              (('effective_coupler', 'transmission_v1', '*.json.gz'),
               ('driven_pause', 'pause_bridge_v1', 'bridge-L*.json.gz'))
              for p in sorted((HERE/'evidence'/folder/'records').glob(pattern))]
    if [sum(k == name for k, _ in inputs) for name in ('effective_coupler', 'driven_pause')] != [64, 32]:
        raise ValueError('Expected exactly64 transmission and32 apparatus recordings')
    dependencies = [Path(__file__), HERE/'recipes.py', HERE/'orbit.py', HERE/'pause_bridge.py',
                    HERE/'pulse_words.py', HERE/'composition.py',
                    *sorted((ROOT/'research/components').glob('*.py'))]
    protocols = [HERE/'transmission_protocol.json', HERE/'pause_bridge_protocol.json']
    results = [HERE/'evidence'/f/'result.json' for f in ('transmission_v1', 'pause_bridge_v1')]
    registration = {'format': 'universe24-composed-recipe-equivalence-v1',
        'scope': 'Initial preparation equality only; no new trajectories or enlarged behavior domain',
        'counts': {'effective_coupler': 64, 'driven_pause': 32}, 'max_cpu_seconds': 120,
        'source_sha256': {str(p.relative_to(ROOT)): _sha(p) for p in dependencies},
        'frozen_protocol_sha256': {str(p.relative_to(ROOT)): _sha(p) for p in protocols},
        'frozen_result_sha256': {str(p.relative_to(ROOT)): _sha(p) for p in results},
        'record_gzip_sha256': {str(p.relative_to(ROOT)): _sha(p) for _, p in inputs}}
    (output/'protocol.json').write_text(canonical(registration)+'\n')
    started, rows = time.process_time(), []
    for kind, path in inputs:
        if time.process_time()-started > 120:
            raise RuntimeError('Initial-data verification exceeded120CPU seconds')
        record = json.loads(gzip.decompress(path.read_bytes()))
        case = record['spec']['controls']
        kwargs = {key: case[key] for key in ('side', 'delay', 'control')}
        recipe = (effective_coupler(family=case['family'], **kwargs) if kind == 'effective_coupler'
                  else two_lane_pause(**kwargs))
        actual = canonical(state_data(recipe.prepare().initial)).encode('ascii')
        experiment, frame = record['experiment'], record['experiment']['frames'][0]
        expected = canonical({'side': experiment['side'], 'background': experiment['background'],
                              'cells': frame['cells']}).encode('ascii')
        if actual != expected:
            raise AssertionError('Complete initial state differs: '+path.name)
        digest = hashlib.sha256(actual).hexdigest()
        if digest != frame['state_sha256']:
            raise AssertionError('Recorded initial hash differs: '+path.name)
        rows.append({'id': record['spec']['id'], 'kind': kind,
                     'record': str(path.relative_to(ROOT)), 'canonical_initial_bytes_equal': True,
                     'recorded_initial_hash_equal': True, 'state_sha256': digest})
    if any(_sha(ROOT/p) != sha for p, sha in registration['source_sha256'].items()):
        raise RuntimeError('Preparation source changed during equality check')
    result = {'format': registration['format'], 'status': 'passed', 'cases': len(rows),
              'counts': registration['counts'], 'new_trajectories_generated': 0,
              'canonical_full_initial_states_byte_equal': True,
              'protocol_sha256': _sha(output/'protocol.json'), 'rows': rows,
              'cpu_seconds': time.process_time()-started}
    (output/'result.json').write_text(canonical(result)+'\n')
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-domain', required=True, type=Path)
    args = parser.parse_args(argv)
    result = verify_preparations(args.verify_domain)
    print(canonical({k: v for k, v in result.items() if k != 'rows'}))


if __name__ == '__main__':
    main()
