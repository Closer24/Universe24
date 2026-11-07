"""Independent adversarial audits of the component preparation boundary.

The oracle uses a separate exact-matrix construction and gathers old-state
neighbors. A successful software composition is not a scientific performance
certificate for a connected apparatus.
"""
import itertools
import copy
import json
from pathlib import Path
import tempfile
import unittest

from research.component_review.audit import (
    Snapshot, advance, audit_checkpoints, coupling_fingerprint,
    from_checkpoint, from_state, net_inputs, rewind, transition_events,
)
from research.reference import evolution as dense_reference
from research.reference.algebra import algebra as matrix_algebra
from research.components import (
    BoardSpec, TensorSpec, Patch, Socket, SignalSource, GuideSegment,
    Receiver, PairedArm, GuidedPacketSource, place, finalize,
)
from research.component_review.review_packet import declared_packet
from universe24 import Channel, Coupling, Cube, Engine, State
from universe24.experiments.config import checkpoint_data
from research.experiments.run import assemble, run_experiment, recorded_states

ROOT = Path(__file__).resolve().parents[1]


def assembled_legacy_case(result):
    """Reassemble published cases through the new primitive recipe boundary."""
    case = result['preparation']
    origin = (case['side']//2,)*3
    tensor = TensorSpec.from_signs(case.get('body_signs', (1, 1, 1)))
    placements = []
    if 'variants' in case:
        for sign, variant in zip((-1, 1), case['variants']):
            if case.get('isolated_side') is not None and case['isolated_side'] != sign:
                continue
            placements.append(place(PairedArm(variant=variant, direction=sign, tensor=tensor),
                                    at=origin, name=f'arm-{sign}'))
        placements.append(place(SignalSource(present=case['source_present'], tensor=tensor),
                                at=origin, name='source'))
    else:
        offsets = case['source_offsets']
        if case.get('guide_mode', 'full_segment') == 'between_sources':
            start, stop = min(offsets), max(offsets)
        else:
            start, stop = -case['extent'], case['extent']
        socket_positions = tuple(offsets)+((0,) if start <= 0 <= stop else ())
        placements.append(place(GuideSegment(start=start, stop=stop, sockets=socket_positions,
                                             tensor=tensor), at=origin, name='guide'))
        placements.append(place(Receiver(remainders=case['target_remainders'], tensor=tensor),
                                at=origin, name='receiver'))
        for index, (offset, counters, present) in enumerate(zip(
                offsets, case['source_ab'], result['source_mask'])):
            position = (origin[0]+offset, origin[1], origin[2])
            placements.append(place(SignalSource(a=counters[0], b=counters[1],
                                                 present=present, tensor=tensor),
                                    at=position, name=f'source-{index}'))
    return finalize(BoardSpec(case['side'], tensor=tensor), placements)


def audit_legacy_migration():
    reports = []
    for study in ('toggle_confirmation', 'counter_memory', 'paired_blocker'):
        for folder in sorted((ROOT/'research/signal_clocks/evidence'/study/'cases').iterdir()):
            if not folder.is_dir():
                continue
            result = json.loads((folder/'result.json').read_text())
            prepared = assembled_legacy_case(result)
            checkpoints = [json.loads(line) for line in (folder/'states.jsonl').read_text().splitlines()]
            actual = list(prepared.engine.evolve(prepared.initial, result['preparation']['steps']))
            assert len(actual) == len(checkpoints)
            for step, (state, record) in enumerate(zip(actual, checkpoints)):
                assert from_state(state) == from_checkpoint(record), (str(folder), step)
                assert record['coupling_fingerprint'] == prepared.engine.coupling.fingerprint
            reports.append({'case': folder.name, 'frames': len(actual), 'all_registers_equal': True})
    assert len(reports) == 44 and sum(r['frames'] for r in reports) == 1868
    return reports


class ComponentBoundaryTests(unittest.TestCase):
    def test_explicit_background_is_not_lost_before_collision_check(self):
        quiet = Patch('quiet', { (0, 0, 0, 0): (0, 0, 2) })
        wire = Patch('wire', { (0, 0, 0, 0): (0, 0, 4) })
        board = BoardSpec(11)
        q = place(quiet, at=(5, 5, 5), name='quiet')
        prepared = finalize(board, [q])
        self.assertNotIn((5, 5, 5, 0), prepared.initial.cells)
        self.assertIn((5, 5, 5, 0, 0, 0, 2), prepared.manifest['raw_assignments'])
        with self.assertRaisesRegex(ValueError, 'Initial-state conflict'):
            finalize(board, [q, place(wire, at=(5, 5, 5), name='wire')])

    def test_socket_requires_declared_filler_and_preserves_background_filler(self):
        board = BoardSpec(11)
        guide = place(GuideSegment(start=-1, stop=1, sockets=(0,)),
                      at=(5, 5, 5), name='guide')
        with self.assertRaisesRegex(ValueError, 'socket'):
            finalize(board, [guide])
        foreign = Patch('foreign', { (0, 0, 0, g): (0, 0, 2) for g in (0, 14) })
        with self.assertRaisesRegex(ValueError, 'socket'):
            finalize(board, [guide, place(foreign, at=(5, 5, 5), name='foreign')])
        prepared = finalize(board, [guide, place(SignalSource(present=False),
                                                at=(5, 5, 5), name='source')])
        for g in (0, 14):
            self.assertEqual(prepared.initial.at((5, 5, 5, g)), Channel(0, 0, 2))
        self.assertEqual(len(prepared.manifest['raw_assignments']), 6)

    def test_identical_writes_keep_owners_but_independent_source_aliases_fail(self):
        board = BoardSpec(11)
        at = (5, 5, 5)
        prepared = finalize(board, [place(Receiver(), at=at, name='a'),
                                   place(Receiver(), at=at, name='b')])
        self.assertTrue(all(len(row['owners']) == 2
                            for row in prepared.manifest['assignment_owners']))
        self.assertFalse(prepared.manifest['behavior_verified_by_assembly'])
        for present in (True, False):
            with self.assertRaisesRegex(ValueError, 'Independent sources alias'):
                finalize(board, [place(SignalSource(present=present), at=at, name='a'),
                                 place(SignalSource(present=present), at=at, name='b')])

    def test_exact_global_tensor_and_background_contracts(self):
        board = BoardSpec(11)
        wrong = SignalSource(tensor=TensorSpec.from_signs((1, -1, 1)))
        with self.assertRaisesRegex(ValueError, 'Tensor conflict'):
            finalize(board, [place(wrong, at=(5, 5, 5), name='source')])
        wrong_background = Patch('other', {}, background=Channel(0, 0, 4))
        with self.assertRaisesRegex(ValueError, 'Background conflict'):
            finalize(board, [place(wrong_background, at=(5, 5, 5), name='other')])
        spec = TensorSpec()
        weights = [list(row) for row in spec.weights]
        weights[0][0] *= -1
        with self.assertRaisesRegex(ValueError, 'weights'):
            TensorSpec(weights=weights, fingerprint=spec.fingerprint)
        ports = [list(row) for row in spec.ports]
        ports[0][0], ports[0][1] = ports[0][1], ports[0][0]
        with self.assertRaisesRegex(ValueError, 'ports'):
            TensorSpec(ports=ports, fingerprint=spec.fingerprint)
        with self.assertRaisesRegex(ValueError, 'fingerprint'):
            TensorSpec(fingerprint='0'*64)

    def test_all_2o_lifts_transform_states_ports_sources_and_readouts(self):
        algebra = matrix_algebra()
        origin = (6, 6, 6)
        addresses = ((-1, 1, 0, 0), (0, 0, 0, 14), (1, 0, -1, 37))
        values = ((2, -3, 1), (-4, 8, 5), (0, 1, 2))
        tensor = TensorSpec.from_signs((1, -1, 1))
        patch = Patch('probe', dict(zip(addresses, values)), tensor=tensor,
                      ports={'input': addresses}, sources={'source': addresses[:1]},
                      readouts=({'id': 'record', 'label': 'Record', 'kind': 'all_equal',
                                 'clauses': [{'address': addresses[1], 'component': 'r', 'equals': '5'}]},))
        for orientation in range(48):
            rotation = algebra.rotations[orientation]
            def moved(address):
                xyz = tuple(sum(rotation[i][j]*address[j] for j in range(3))
                            + origin[i] for i in range(3))
                return (*xyz, algebra.multiplication[orientation][address[3]])
            expected_addresses = tuple(moved(a) for a in addresses)
            prepared = finalize(BoardSpec(13, tensor=tensor), [
                place(patch, at=origin, name='probe', orientation=orientation)])
            expected = Snapshot(13, (0, 0, 2), dict(zip(expected_addresses, values)))
            self.assertEqual(from_state(prepared.initial), expected)
            self.assertEqual(prepared.ports['probe.input'], expected_addresses)
            self.assertEqual(prepared.sources['probe.source'], expected_addresses[:1])
            self.assertEqual(prepared.readouts[0]['clauses'][0]['address'], expected_addresses[1])
            self.assertEqual(from_state(prepared.engine.advance(prepared.initial)),
                             advance(expected, (1, -1, 1)))

    def test_socket_addresses_transform_with_the_same_lift(self):
        for orientation in (0, 1, 14, 37):
            guide = GuideSegment(start=-1, stop=1, sockets=(0,))
            prepared = finalize(BoardSpec(11), [
                place(guide, at=(5, 5, 5), name='guide', orientation=orientation),
                place(Receiver(), at=(5, 5, 5), name='receiver', orientation=orientation)])
            self.assertEqual(prepared.manifest['sockets'][0]['addresses'],
                             prepared.ports['receiver.memory'])

    def test_wrapping_is_explicit_and_never_aliases_two_local_addresses(self):
        patch = Patch('edge', {(-1, 0, 0, 0): (1, 2, 3)})
        with self.assertRaisesRegex(ValueError, 'outside'):
            finalize(BoardSpec(11), [place(patch, at=(0, 5, 5), name='edge')])
        prepared = finalize(BoardSpec(11), [place(patch, at=(0, 5, 5), name='edge', wrap=True)])
        self.assertEqual(prepared.initial.at((10, 5, 5, 0)), Channel(1, 2, 3))
        alias = Patch('alias', {(0, 0, 0, 0): (1, 2, 3), (11, 0, 0, 0): (1, 2, 3)})
        with self.assertRaisesRegex(ValueError, 'wraps distinct'):
            finalize(BoardSpec(11), [place(alias, at=(0, 5, 5), name='alias', wrap=True)])

    def test_raw_duplicate_and_mutation_or_callback_metadata_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate address'):
            Patch('dup', [((0, 0, 0, 0), (0, 0, 2)), ((0, 0, 0, 0), (0, 0, 2))])
        with self.assertRaisesRegex(TypeError, 'only data'):
            Patch('callback', {}, evidence_domains=(lambda state: state,))
        prepared = finalize(BoardSpec(11), [place(Receiver(), at=(5, 5, 5), name='r')])
        with self.assertRaises(TypeError):
            prepared.manifest['tensor']['weights'][0][0] = -1
        with self.assertRaises(TypeError):
            prepared.initial.cells[(5, 5, 5, 0)] = Channel(0, 0, 0)

    def test_all_44_historical_experiments_reassemble_all_1868_full_states(self):
        reports = audit_legacy_migration()
        self.assertEqual(len(reports), 44)
        self.assertEqual(sum(row['frames'] for row in reports), 1868)


class GenericRunnerReviewTests(unittest.TestCase):
    @staticmethod
    def spec():
        return {'format': 'universe24-assembly-experiment-v1', 'id': 'review-source',
                'board': {'side': 13, 'body_signs': [1, -1, 1]}, 'steps': 3,
                'components': [{'name': 'source', 'recipe': 'SignalSource',
                                'params': {'a': '-9', 'b': str(10**70+1)},
                                'at': [6, 6, 6]}],
                'detectors': ['source.signal'],
                'readouts': [{'id': 'r2', 'label': 'Remainder two', 'kind': 'all_equal',
                              'clauses': [{'port': 'source.signal', 'index': 0,
                                           'component': 'r', 'equals': '2'}]}],
                'budget': {'max_frames': 8, 'max_cells': 20000, 'max_seconds': 30}}

    def test_observers_do_not_change_frames_and_report_exact_arithmetic(self):
        spec = self.spec()
        original = copy.deepcopy(spec)
        result = run_experiment(spec)
        self.assertEqual(spec, original)
        unobserved = copy.deepcopy(spec)
        unobserved.update({'detectors': [], 'readouts': []})
        passive_control = run_experiment(unobserved)
        self.assertEqual(result['experiment']['frames'], passive_control['experiment']['frames'])
        states = [from_state(state) for state in recorded_states(result['experiment'])]
        addresses = ((6, 6, 6, 0), (6, 6, 6, 14))
        self.assertEqual(states[0].at(addresses[0]), (-9, 10**70+1, 2))
        observed = result['observations']['source.signal']
        events, rtimes = [], []
        for step, state in enumerate(states):
            row = observed['trace'][step]
            self.assertEqual([int(v) for v in row['next_input']], net_inputs(state, addresses, (1, -1, 1)))
            self.assertEqual(row['memory'], [state.at(a)[2] for a in addresses])
            self.assertEqual([int(v) for v in row['magnitude']],
                             [state.at(a)[0]**2+state.at(a)[1]**2 for a in addresses])
            if step:
                self.assertEqual(advance(states[step-1], (1, -1, 1)), state)
                self.assertEqual(rewind(state, (1, -1, 1)), states[step-1])
                derived = transition_events(states[step-1], state, addresses)
                if derived['remainder']:
                    rtimes.append(step)
                events.extend({'step': step, 'address': list(event['address']),
                               'kind': event['kind'], 'quotient': str(event['quotient'])}
                              for event in derived['arithmetic'])
        self.assertEqual(events, observed['arithmetic_events'])
        self.assertEqual(rtimes, observed['record_event_times'])
        self.assertFalse(result['physical_light_established'])

    def test_json_boundary_rejects_runtime_and_conflicting_tensor_controls(self):
        invalid = self.spec()
        invalid['on_click'] = 'erase-other-path'
        with self.assertRaises(ValueError):
            assemble(invalid)
        invalid = self.spec()
        invalid['components'][0]['params']['tensor'] = {'body_signs': [-1, 1, 1]}
        with self.assertRaisesRegex(ValueError, 'separate tensor'):
            assemble(invalid)
        invalid = self.spec()
        invalid['board']['tensor'] = TensorSpec.from_signs((1, -1, 1)).data()
        with self.assertRaisesRegex(ValueError, 'two tensor definitions'):
            assemble(invalid)
        invalid = self.spec()
        invalid['components'][0]['recipe'] = 'external_selector'
        with self.assertRaisesRegex(ValueError, 'Unknown'):
            assemble(invalid)
        invalid = self.spec()
        invalid['detectors'] = ['missing.port']
        with self.assertRaisesRegex(ValueError, 'Detectors'):
            run_experiment(invalid)

    def test_raw_patch_json_keeps_explicit_background_and_rejects_duplicate_rows(self):
        spec = {'format': 'universe24-assembly-experiment-v1', 'id': 'raw',
                'board': {'side': 7}, 'steps': 0,
                'components': [{'name': 'quiet', 'recipe': 'Patch', 'at': [3, 3, 3],
                                'params': {'kind': 'quiet', 'cells': [[0, 0, 0, 0, '0', '0', 2]]}}]}
        prepared = assemble(spec)
        self.assertEqual(len(prepared.initial.cells), 0)
        self.assertEqual(len(prepared.manifest['raw_assignments']), 1)
        spec['components'][0]['params']['cells'] *= 2
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            assemble(spec)


class ComponentExtensionReviewTests(unittest.TestCase):
    def test_guided_packet_recipe_preserves_all_six_frozen_complete_trajectories(self):
        evidence = ROOT/'research/component_studies/confirmation_packet_evidence_v1/cases'
        for side in (5, 17, 31):
            origin = (0, side//2, side//2)
            for present in (True, False):
                prepared = finalize(BoardSpec(side), [
                    place(GuideSegment(start=0, stop=side-1, sockets=(0, 1, 2, 3),
                                       remainder_pair=(0, 4)), at=origin, name='guide'),
                    place(GuidedPacketSource(present=present), at=origin, name='packet')])
                self.assertEqual(from_state(prepared.initial), declared_packet(side, present))
                folder = evidence/f'guided-packet-L{side}-s{int(present)}'
                frozen = [from_checkpoint(json.loads(line)) for line in
                          (folder/'states.jsonl').read_text().splitlines()]
                actual = [from_state(s) for s in prepared.engine.evolve(prepared.initial, side)]
                self.assertEqual(actual, frozen)

    def test_arm_length_changes_geometry_and_port_with_fixed_gate_sites(self):
        for length, direction in itertools.product((3, 6, 8), (-1, 1)):
            patch = PairedArm(length=length, direction=direction,
                              gate_pairs=((2, 4), (0, 2)))
            expected = {}
            for j in range(1, length+1):
                pair = {2: (2, 4), 3: (0, 2)}.get(j, (4, 0))
                for g, r in zip((0, 14), pair):
                    expected[(direction*j, 0, 0, g)] = Channel(0, 0, r)
            self.assertEqual(dict(patch.cells), expected)
            self.assertEqual(patch.ports['outlet'],
                             tuple((direction*length, 0, 0, g) for g in range(48)))
            self.assertEqual(patch.ports['memory-2'],
                             tuple((direction*2, 0, 0, g) for g in (0, 14)))
            self.assertEqual(patch.ports['memory-3'],
                             tuple((direction*3, 0, 0, g) for g in (0, 14)))
        for length in (2, True, 3.0, '8'):
            with self.assertRaises(ValueError):
                PairedArm(length=length)
        with self.assertRaises(ValueError):
            GuidedPacketSource(present=1)

    def test_packet_recipe_generic_json_source_control_keeps_all_remainders(self):
        def spec(present):
            return {'format': 'universe24-assembly-experiment-v1', 'id': 'packet',
                    'board': {'side': 5}, 'steps': 1,
                    'components': [
                        {'name': 'guide', 'recipe': 'GuideSegment', 'at': [0, 2, 2],
                         'params': {'start': 0, 'stop': 4, 'sockets': [0, 1, 2, 3],
                                    'remainder_pair': [0, 4]}},
                        {'name': 'packet', 'recipe': 'GuidedPacketSource',
                         'at': [0, 2, 2], 'params': {'present': present}}]}
        on, off = (assemble(spec(p)) for p in (True, False))
        addresses = on.initial.cells.keys() | off.initial.cells.keys()
        self.assertTrue(all(on.initial.at(a).r == off.initial.at(a).r for a in addresses))
        self.assertTrue(all(value.a == value.b == 0 for value in off.initial.cells.values()))
        self.assertEqual(off.engine.advance(off.initial), off.initial)


class IndependentOracleTests(unittest.TestCase):
    def test_sparse_gather_matches_separate_dense_old_snapshot(self):
        initial = Snapshot(3, (0, 0, 2), {
            (0, 0, 0, 0): (-(10**35), 10**37+1, 5),
            (2, 0, 0, 14): (3, -8, 0),
            (1, 2, 1, 37): (-5, 13, 1),
            (0, 1, 2, 9): (0, 0, 4),
        })
        for signs in itertools.product((-1, 1), repeat=3):
            dense = dense_reference.flatten(initial.cells, initial.side, initial.background)
            reference = dense_reference.advance(dense, initial.side, signs)
            actual = advance(initial, signs)
            self.assertEqual(dense_reference.flatten(actual.cells, actual.side,
                                                    actual.background), reference)
            self.assertEqual(rewind(actual, signs), initial)

    def test_c_is_distinct_from_remainder_change_and_local_rotation(self):
        address = (2, 2, 2, 0)
        before = Snapshot(5, (0, 0, 2), {address: (0, 0, 0)})
        after = Snapshot(5, (0, 0, 2), {address: (0, 0, 2)})
        self.assertEqual(transition_events(before, after, [address]),
                         {"arithmetic": [], "remainder": [address]})
        before = Snapshot(5, (0, 0, 2), {address: (0, 1, 2)})
        after = Snapshot(5, (0, 0, 2), {address: (1, 0, 2)})
        self.assertEqual(transition_events(before, after, [address]),
                         {"arithmetic": [], "remainder": []})

    def test_full_checkpoint_audit_rejects_hidden_register_and_fingerprint_tampering(self):
        engine = Engine(Coupling((1, -1, 1)))
        initial = State(Cube(7), cells={(3, 3, 3, 0): Channel(0, 1, 2)})
        states = list(engine.evolve(initial, 3))
        records = [checkpoint_data(state, engine, step)
                   for step, state in enumerate(states)]
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/"states.jsonl"
            def save(rows):
                path.write_text("".join(json.dumps(row)+"\n" for row in rows))
            save(records)
            report = audit_checkpoints(path, expected_initial=from_state(initial))
            self.assertEqual(report["transitions"], 3)
            changed = json.loads(json.dumps(records))
            changed[2]["experiment"]["seed_changes"].append({
                "position": [1, 1, 1], "channel": 47, "state": [0, 0, 5]})
            save(changed)
            with self.assertRaisesRegex(AssertionError, "forward mismatch"):
                audit_checkpoints(path)
            changed = json.loads(json.dumps(records))
            changed[1]["coupling_fingerprint"] = "0"*64
            save(changed)
            with self.assertRaisesRegex(AssertionError, "fingerprint"):
                audit_checkpoints(path)

    def test_exact_matrix_fingerprint_matches_all_registered_sign_tensors(self):
        for signs in itertools.product((-1, 1), repeat=3):
            self.assertEqual(coupling_fingerprint(signs), Coupling(signs).fingerprint)

    def test_duplicate_checkpoint_address_rejected_even_with_identical_triples(self):
        engine = Engine()
        state = State(Cube(5), cells={(2, 2, 2, 0): Channel(0, 1, 2)})
        record = checkpoint_data(state, engine, 0)
        record["experiment"]["seed_changes"] *= 2
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            from_checkpoint(record)


if __name__ == "__main__":
    unittest.main()
