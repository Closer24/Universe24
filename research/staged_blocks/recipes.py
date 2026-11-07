"""Reusable initial-data recipes for a guide, clock interface and reference.

The recipe names never choose a runtime update. Only the reference Rule3 engine
evolves the returned board. D/X is a passive observer, not a physical comparator.

python -m research.staged_blocks.recipes --output NEW_DIRECTORY
python -m research.staged_blocks.recipes --verify-domain NEW_DIRECTORY
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import gzip
import hashlib
import json
from pathlib import Path
import time

from research.components import (BoardSpec, GuidedPacketSource, GuideSegment, Patch,
                                 Socket, TensorSpec, finalize, place, plain)
from research.components.spec import freeze, local_address
from research.experiments.run import assemble, recorded_states, run_experiment, source_hashes
from research.presenter.export import canonical, state_data, state_sha256, bundle, write_bundle
from universe24.observation import classify
from .composition import ComponentPreparation, RunContext, experiment_spec
from .orbit import ShieldedOrbit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TESTED_SIDES = (129, 161)
TESTED_DELAYS = (1, 2, 3, 5)
TESTED_REMAINDERS = (0, 4)
CONTROLS = ('00', '10', '01', '11')
EVIDENCE = ('research/staged_blocks/phase_protocol.json',
            'research/staged_blocks/evidence/interactions/phase_v1/result.json',
            'research/staged_blocks/evidence/independent_audit/phase.json')


def _integer(value, label):
    if type(value) is not int:
        raise ValueError(label + ' must be an exact integer')
    return value


def _tensor(tensor):
    tensor = TensorSpec() if tensor is None else tensor
    if not isinstance(tensor, TensorSpec) or tensor.body_signs != (1, 1, 1):
        raise ValueError('This interface recipe supports the fixed +++ body-013 tensor only')
    return tensor


def ClockGuideInterface(*, r=0, phase=0, present=True, tensor=None):
    """A full336-channel joint patch, with its guide one node in local -Y.

    The clock is the unit orbit R^phase(0,1) on ports[+Y][0]. Its guide-facing
    halo starts at remainder0 before phase rotation. The other guide channel14
    remains at remainder4; it must not be reset to a generic halo background.
    This explicitly defined joint patch replaces no other component's cells.
    """
    tensor = _tensor(tensor)
    _integer(r, 'r')
    _integer(phase, 'phase')
    if r not in TESTED_REMAINDERS or phase not in range(4):
        raise ValueError('Interface requires r in(0,4) and phase in0..3')
    if type(present) is not bool:
        raise ValueError('Clock presence must be Boolean initial data')
    g = tensor.ports[2][0]
    if tensor.ports[3][g] != 0:
        raise ValueError('The declared +Y/-Y guide interface is not reciprocal')
    orbit = ShieldedOrbit(channel=g, a=0, b=1, r=r, phase=phase, present=present,
                          tensor=tensor, halo_remainders=(2, 2, 2, 0, 2, 2))
    untouched = (0, -1, 0, 14)
    original = dict(orbit.cells)
    if tuple(original[untouched]) != (0, 0, 2):
        raise ValueError('Untouched guide channel unexpectedly belongs to the active halo')
    # Explicit joint initial definition: preserve the second channel of the guide.
    cells = {address: ((0, 0, 4) if address == untouched else value)
             for address, value in orbit.cells}
    ports = plain(orbit.ports)
    ports['guide_pair'] = [(0, -1, 0, g) for g in (0, 14)]
    ports['guide_contact'] = [(0, -1, 0, g) for g in range(48)]
    readouts = plain(orbit.readouts)
    for row in readouts:
        row['label'] = 'Prepared interface ' + row['label']
    contract = {'kind': 'clock-guide-interface-v1', 'tensor_fingerprint': tensor.fingerprint,
                'center_channel': g, 'phase': phase, 'center_remainder': r,
                'guide_pair': [0, 4], 'guide_direction': '-Y', 'protected_channels': 336,
                'untouched_guide_channel': 14, 'untouched_guide_remainder': 4,
                'present': present, 'unit_clock_prepared_initially': True,
                'scope': 'A reusable initial joint patch. Phase synchronization evidence is limited to the full registered assemblies.',
                'evidence': EVIDENCE, 'physical_comparator': False,
                'capture_or_approval_implemented': False}
    return Patch('clock-guide-interface', cells, tensor=tensor, ports=ports,
                 sources={'clock': ((0, 0, 0, g),)}, readouts=readouts,
                 evidence_domains=(contract,))


def InterfaceGuide(*, side, packet_start, interface_x, tensor=None):
    """Reuse GuideSegment with explicit packet and joint-interface sockets."""
    tensor = _tensor(tensor)
    for value, label in ((side, 'side'), (packet_start, 'packet_start'), (interface_x, 'interface_x')):
        _integer(value, label)
    if side < 5 or not 0 <= packet_start <= side-4 or not 0 <= interface_x < side:
        raise ValueError('Guide and packet slots must fit the declared board')
    packet_slots = tuple(range(packet_start, packet_start+4))
    if interface_x in packet_slots:
        raise ValueError('Packet core and clock interface cannot claim the same guide socket')
    guide = GuideSegment(start=0, stop=side-1, sockets=(*packet_slots, interface_x),
                         remainder_pair=(0, 4), tensor=tensor)
    sockets = tuple(Socket(socket.name, socket.addresses,
                           ('clock-guide-interface',) if socket.addresses[0][0] == interface_x else ('signal-source',))
                    for socket in guide.sockets)
    return Patch(guide.kind, guide.cells, tensor=tensor, ports=guide.ports,
                 sockets=sockets, evidence_domains=guide.evidence_domains)


@dataclass(frozen=True, slots=True)
class PhaseAssembly:
    board: BoardSpec
    placements: tuple
    metadata: object

    def prepare(self):
        """Finalize initial assignments once; return the existing PreparedBoard."""
        return finalize(self.board, self.placements)

    def experiment_spec(self, *, identifier=None, steps=40):
        _integer(steps, 'steps')
        if steps < 0:
            raise ValueError('Steps must be nonnegative')
        meta = plain(self.metadata)
        identifier = identifier or ('recipe-phase-L{side}-r{r}-p{phase}-d{delay}-{control}'.format(**meta))
        spec = experiment_spec(RunContext(self.board, seed=0),
            [ComponentPreparation(p, self.board.side, seed=0) for p in self.placements],
            identifier=identifier, steps=steps,
            title='Signal, clock interface, reference and guide: '+identifier,
            description=('Four initial-data pieces on one unchanged Rule3 board. The target clock is prepared; '
                         'D/X is a passive relative-phase observation. Finite synchronization is not '
                         'unconditional detection, an internal comparator, capture, approval or release.'),
            controls=meta, detectors=('interface.center_node', 'reference.center'),
            view={'port': 'interface.center'})
        spec['provenance'].update({'recipe': 'phase_assembly', 'randomness_used': False,
                                   'matches_validated_parameter_domain': meta['matches_validated_parameter_domain'] and steps == 40,
                                   'validated_hold_states': [32, 40], 'evidence': list(EVIDENCE)})
        return spec


def phase_assembly(*, side=129, r=0, phase=0, delay=1, control='11', tensor=None, exploratory=False):
    """Assemble four reusable pieces; parameterization does not enlarge evidence."""
    tensor = _tensor(tensor)
    for value, label in ((side, 'side'), (r, 'r'), (phase, 'phase'), (delay, 'delay')):
        _integer(value, label)
    if control not in CONTROLS or type(exploratory) is not bool or delay < 0:
        raise ValueError('Use a declared two-source control, Boolean exploratory flag and nonnegative delay')
    tested = side in TESTED_SIDES and r in TESTED_REMAINDERS and phase in range(4) and delay in TESTED_DELAYS
    if not tested and not exploratory:
        raise ValueError('Parameters are outside the validated finite domain; use exploratory=True for a new investigation')
    c, packet_x = side//2, side//2-16-delay
    if packet_x < 0 or c+25 >= side:
        raise ValueError('The packet or protected reference region does not fit without wrapping')
    target = ClockGuideInterface(r=r, phase=phase, present=control[1] == '1', tensor=tensor)
    guide = InterfaceGuide(side=side, packet_start=packet_x, interface_x=c, tensor=tensor)
    packet = GuidedPacketSource(present=control[0] == '1', tensor=tensor)
    reference = ShieldedOrbit(channel=0, a=0, b=1, r=2, phase=0, present=True,
                             tensor=tensor, halo_remainders=(2,)*6)
    placements = (
        place(guide, at=(0, c, c), name='guide'),
        place(packet, at=(packet_x, c, c), name='packet'),
        place(target, at=(c, c+1, c), name='interface'),
        place(reference, at=(c, c+24, c+24), name='reference'),
    )
    metadata = freeze({'side': side, 'r': r, 'phase': phase, 'delay': delay, 'control': control,
                       'seed': 0, 'randomness_used': False, 'time0': 0,
                       'matches_validated_parameter_domain': tested,
                       'exploratory_geometry': not tested, 'body_actions': (0,1,3),
                       'tensor_fingerprint': tensor.fingerprint,
                       'source_controls': {'packet': control[0] == '1', 'interface_clock': control[1] == '1',
                                           'reference_always_present': True},
                       'scope': 'Finite same-board relative-phase synchronization; no unconditional presence latch or implemented D/X comparator.'})
    result = PhaseAssembly(BoardSpec(side, tensor=tensor), placements, metadata)
    result.prepare()  # Fail conflicts before any spec or engine run is offered.
    return result


def relative_phase_observer(target_address, reference_address):
    """An immutable formula for reading existing counters, not another coupling."""
    target, reference = local_address(target_address), local_address(reference_address)
    if target == reference:
        raise ValueError('The target and reference must be distinct retained channels')
    return freeze({'kind': 'relative-phase-DX-v1', 'target': target, 'reference': reference,
                   'D': 'a_target*a_reference+b_target*b_reference',
                   'X': 'a_target*b_reference-b_target*a_reference',
                   'passive': True, 'physical_comparator_implemented': False,
                   'arithmetic_C_classes_retained': (0,1,2)})


def observe_relative_phase(observer, states):
    """Compute D/X after capture; no expected direction or state update is supplied."""
    observer, states = plain(observer), tuple(states)
    if observer.get('kind') != 'relative-phase-DX-v1' or observer.get('passive') is not True:
        raise ValueError('Expected a frozen passive relative-phase observer')
    if not states or any(s.cube != states[0].cube or s.background != states[0].background for s in states):
        raise ValueError('Relative-phase observations require retained states from one board')
    target, reference = tuple(observer['target']), tuple(observer['reference'])
    rows = []
    for t,state in enumerate(states):
        a,b,r = state.at(target)
        c,d,rr = state.at(reference)
        D, X, I, J = a*c+b*d, a*d-b*c, a*a+b*b, c*c+d*d
        assert D*D+X*X == I*J
        events = []
        if t:
            for label, address in (('target',target),('reference',reference)):
                event = classify(states[t-1].at(address),state.at(address))
                if event is not None:
                    events.append({'role':label,'kind':event[0],'ell':event[1]})
        rows.append({'step':t,'D':D,'X':X,'I_target':I,'I_reference':J,
                     'target_remainder':r,'reference_remainder':rr,
                     'arithmetic_events':events,'identity_equal':True})
    return {'observer':observer, 'trace':rows, 'scope':'Passive reading of same-board counters; not a physical comparison device'}


def verify_phase_preparations(output):
    """Compare all256 canonical initial-state byte strings; run no trajectories."""
    from . import interactions_phase as frozen
    output = Path(output)
    output.mkdir(parents=True,exist_ok=False)
    protocol = json.loads(frozen.PROTOCOL.read_text())
    recorded_result = json.loads((HERE/'evidence/interactions/phase_v1/result.json').read_text())
    recorded = {row['id']:row['initial_state_sha256'] for row in recorded_result['cases']}
    started, rows = time.process_time(), []
    for geometry in frozen.geometries(protocol):
        for mask in CONTROLS:
            case = {**geometry,'control':mask}
            recipe = phase_assembly(side=case['side'],r=case['clock_remainder'],phase=case['phase'],
                                    delay=case['delay'],control=mask)
            actual = recipe.prepare().initial
            expected = assemble(frozen.case_spec(case,protocol)).initial
            actual_bytes = canonical(state_data(actual)).encode('ascii')
            expected_bytes = canonical(state_data(expected)).encode('ascii')
            identity = case['id']+'-'+mask
            assert actual_bytes == expected_bytes, identity
            assert state_sha256(actual) == recorded[identity], identity
            rows.append({'id':identity,'canonical_initial_bytes_equal':True,
                         'recorded_initial_hash_equal':True,'state_sha256':state_sha256(actual)})
    if time.process_time()-started > 120:
        raise RuntimeError('Recipe preparation verification exceeded120CPU seconds')
    result = {'format':'universe24-recipe-preparation-equivalence-v1','status':'passed',
              'cases':len(rows),'new_trajectories_generated':0,'canonical_full_initial_states_byte_equal':True,
              'recipe_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'frozen_phase_protocol_sha256':hashlib.sha256(frozen.PROTOCOL.read_bytes()).hexdigest(),
              'registered_phase_result_sha256':hashlib.sha256((HERE/'evidence/interactions/phase_v1/result.json').read_bytes()).hexdigest(),
              'rows':rows,'cpu_seconds':time.process_time()-started}
    (output/'result.json').write_text(canonical(result)+'\n')
    return result


def run_demo(output, *, side=129, r=0, phase=0, delay=1):
    """Four matched native runs made from the reusable four-piece recipes."""
    output = Path(output)
    output.mkdir(parents=True,exist_ok=False)
    (output/'records').mkdir()
    started = time.process_time()
    recipes = [phase_assembly(side=side,r=r,phase=phase,delay=delay,control=mask) for mask in CONTROLS]
    specs = [recipe.experiment_spec() for recipe in recipes]
    prepared = recipes[0].prepare()
    observer = relative_phase_observer(prepared.ports['interface.center'][0],prepared.ports['reference.center'][0])
    protocol = {'format':'universe24-four-piece-phase-demo-v1','specs':specs,'observer':plain(observer),
                'interpretation':'Reproduction of an already validated finite preparation; no new behavioral scope',
                'source_controls':'Only packet and target-clock initial counters vary; reference and all remainders remain fixed.'}
    sources = source_hashes()
    for path in (Path(__file__), HERE/'orbit.py', HERE/'composition.py'):
        sources[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    (output/'protocol.json').write_text(canonical(protocol)+'\n')
    (output/'registration.json').write_text(canonical({'source_sha256':sources,
        'protocol_sha256':hashlib.sha256(canonical(protocol).encode()).hexdigest()})+'\n')
    experiments, rows = [], []
    for spec in specs:
        result = run_experiment(spec)
        phase_readout = observe_relative_phase(observer,recorded_states(result['experiment']))
        wrapper = {'spec':spec,'assembly':result['assembly'],'experiment':result['experiment'],
                   'observations':result['observations'],'relative_phase':phase_readout,
                   'assessment':{'initial_recipe_reproduction':True,'new_scope_claim':False,
                                 'full_rewind_equal':result['experiment']['provenance']['full_rewind_equal']}}
        path = output/'records'/(spec['id']+'.json.gz')
        path.write_bytes(gzip.compress(canonical(wrapper).encode(),mtime=0))
        rows.append({'id':spec['id'],'record':str(path.relative_to(output)),
                     'state_hashes':[frame['state_sha256'] for frame in result['experiment']['frames']]})
        experiments.append(result['experiment'])
    for name, expected in sources.items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest() != expected:
            raise RuntimeError('Recipe source changed during capture: '+name)
    write_bundle(output/'experiments.json',bundle(experiments,title='Signal, clock interface, reference and guide'))
    from research.presenter.build import build
    build(output/'experiments.json',output/'The_Presenter.html')
    report = {'format':'universe24-four-piece-phase-demo-result-v1','status':'completed','records':rows,
              'pieces':['guide','packet','interface','reference'],'source_sha256':sources,
              'same_board_DX_observer_passive':True,'physical_comparator_implemented':False,
              'new_scope_claim':False,'cpu_seconds':time.process_time()-started}
    if report['cpu_seconds'] > 120:
        raise RuntimeError('Recipe demonstration exceeded120CPU seconds')
    (output/'result.json').write_text(canonical(report)+'\n')
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--output', type=Path)
    mode.add_argument('--verify-domain', type=Path)
    args = parser.parse_args(argv)
    result = verify_phase_preparations(args.verify_domain) if args.verify_domain else run_demo(args.output)
    print(canonical({k:v for k,v in result.items() if k not in ('rows','records','source_sha256')}))


if __name__ == '__main__':
    main()
