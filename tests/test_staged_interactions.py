"""Exact contract checks for the prepared clock/carrier interaction study."""
import json
import gzip
import hashlib
from pathlib import Path
import unittest

from research.components import BoardSpec, GuidedPacketSource, GuideSegment, finalize, place
from research.experiments.run import assemble
from research.staged_blocks.interactions import (PROTOCOL, case_spec, clock_geometry,
                                                geometry_cases, reverse_same_guide, packet_matches)
from universe24 import State


class StagedInteractionTests(unittest.TestCase):
    def setUp(self):
        self.protocol = json.loads(PROTOCOL.read_text())

    def test_frozen_case_count_and_matched_control_remainders(self):
        geometries = list(geometry_cases(self.protocol))
        self.assertEqual(len(geometries), 84)
        self.assertEqual(len({c['id'] for c in geometries}), 84)
        for geometry in (geometries[0], geometries[23], geometries[-1]):
            boards = {mask: assemble(case_spec({**geometry, 'control': mask}, self.protocol))
                      for mask in ('00', '10', '01', '11')}
            addresses = set().union(*(b.initial.cells for b in boards.values()))
            for address in addresses:
                self.assertEqual(len({b.initial.at(address).r for b in boards.values()}), 1)
            center, channel, nodes = clock_geometry(self.protocol, geometry)
            self.assertEqual(len(nodes), 7)
            clock_changed = {a for a in addresses
                             if boards['11'].initial.at(a) != boards['10'].initial.at(a)}
            self.assertEqual(clock_changed, {(*center, channel)})
            for b in boards.values():
                self.assertTrue(all(w == 1 for row in b.engine.coupling.weights for w in row))

    def test_guide_embedded_clock_has_complete_four_cycle(self):
        geometries = list(geometry_cases(self.protocol))
        # Both signs, all four phases, and each compensation direction.
        selected = [g for g in geometries if g['clock_remainder'] == 2
                    and (g['stage'] == 'base' or g['phase'] == 0)]
        for geometry in selected:
            prepared = assemble(case_spec({**geometry, 'control': '01'}, self.protocol))
            states = list(prepared.engine.evolve(prepared.initial, 8))
            self.assertNotEqual(states[0], states[1])
            for t in range(5):
                self.assertEqual(states[t], states[t+4])
            for old, new in zip(states, states[1:]):
                self.assertEqual(prepared.engine.rewind(new), old)

    def test_reverse_packet_keeps_guide_and_complete_halo(self):
        side, x, y, z = 65, 24, 32, 32
        prepared = finalize(BoardSpec(side), [
            place(GuideSegment(start=0, stop=side-1, sockets=tuple(range(x, x+4)),
                               remainder_pair=(0, 4)), at=(0, y, z), name='guide'),
            place(GuidedPacketSource(), at=(x, y, z), name='packet')])
        for direction in (1, -1):
            initial = prepared.initial if direction == 1 else reverse_same_guide(prepared.initial)
            for t, state in enumerate(prepared.engine.evolve(initial, 8)):
                expected = State(initial.cube, initial.background,
                                 {((a[0]+direction*t) % side, *a[1:]): v
                                  for a, v in initial.cells.items()})
                self.assertEqual(state, expected)
                self.assertTrue(packet_matches(state, x+direction*t, y, z, direction))
        arbitrary = prepared.engine.advance(prepared.initial)
        self.assertEqual(prepared.engine.advance(reverse_same_guide(prepared.engine.advance(arbitrary))),
                         reverse_same_guide(arbitrary))

    def test_packaging_preserves_all_registered_complete_records(self):
        root = Path(__file__).resolve().parents[1]
        evidence = root/'research/staged_blocks/evidence/interactions/main'
        if not (evidence/'packaging.json').exists():
            self.skipTest('Published interaction evidence is not present')
        metadata = json.loads((evidence/'packaging.json').read_text())
        source = (evidence/metadata['executed_source_snapshot']).read_bytes()
        self.assertEqual(hashlib.sha256(source).hexdigest(), metadata['executed_source_sha256'])
        records = json.loads((evidence/'result.json').read_text())['cases']
        for record in records:
            raw = (evidence/record['record']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), record['record_gzip_sha256'])
            self.assertEqual(hashlib.sha256(gzip.decompress(raw)).hexdigest(), record['record_sha256'])
        self.assertEqual(len(records), 336)
        data = json.loads((evidence/'experiments.json').read_text())
        encoded = json.dumps(data, sort_keys=True, separators=(',', ':')).encode()
        self.assertEqual(hashlib.sha256(encoded).hexdigest(), metadata['semantic_sha256'])
        self.assertLessEqual(sum(p.stat().st_size for p in evidence.rglob('*') if p.is_file()), 20*1024*1024)

    def test_phase_reference_is_outside_both_initial_influence_cones(self):
        from research.staged_blocks import interactions_phase as phase
        protocol = json.loads(phase.PROTOCOL.read_text())
        self.assertEqual(len(list(phase.geometries(protocol))), 64)
        for side in (129, 161):
            case = {'id': 'test-phase', 'side': side, 'clock_remainder': 0, 'phase': 1,
                    'delay': 5, 'stage': 'phase', 'guide_target_channel': 0,
                    'compensation_direction': None, 'control': '11'}
            prepared = assemble(phase.case_spec(case, protocol))
            c = side//2
            reference = (c, c+24, c+24)
            reference_nodes = [tuple(a[:3]) for a in prepared.ports['reference.region']]
            for address, value in prepared.initial.cells.items():
                if (value.a or value.b) and address[:3] != reference:
                    self.assertGreater(min(phase.distance(address, p, side) for p in reference_nodes), 40)
            self.assertGreater(min(phase.distance(reference, a, side)
                                   for a in prepared.ports['apparatus.region']), 40)
            self.assertEqual(prepared.initial.at((*reference, 0)), (0, 1, 2))

    def test_phase_observer_orientation_and_common_rotation(self):
        from research.staged_blocks.interactions_phase import ALPHABET, COUNTER_CYCLE
        for reference_phase in range(4):
            z = COUNTER_CYCLE[reference_phase]
            for relative_phase in range(4):
                v = COUNTER_CYCLE[(reference_phase+relative_phase) % 4]
                observed = (v[0]*z[0]+v[1]*z[1], v[0]*z[1]-v[1]*z[0])
                self.assertEqual(observed, ALPHABET[relative_phase])
                v1, z1 = (v[1], -v[0]), (z[1], -z[0])
                self.assertEqual(observed, (v1[0]*z1[0]+v1[1]*z1[1], v1[0]*z1[1]-v1[1]*z1[0]))

    def test_signed_carrier_requires_its_complete_prepared_halo(self):
        from research.staged_blocks.interactions_signed import carrier_spec
        for method in ('same_seed', 'tensor_aware'):
            prepared = assemble(carrier_spec(method, (1, -1, 1), 1))
            actual = prepared.engine.advance(prepared.initial)
            expected = State(prepared.initial.cube, prepared.initial.background,
                             {((a[0]+1) % 129, *a[1:]): v for a, v in prepared.initial.cells.items()})
            self.assertEqual(actual == expected, method == 'tensor_aware')
            self.assertEqual(prepared.engine.rewind(actual), prepared.initial)

    def test_two_lane_bridge_pauses_full_node_but_not_full_region(self):
        from research.staged_blocks import pause_bridge as bridge
        protocol = json.loads(bridge.PROTOCOL.read_text())
        geometry = next(bridge.geometries(protocol))
        prepared = {mask: assemble(bridge.case_spec({**geometry, 'control': mask}, protocol))
                    for mask in ('00', '10', '01', '11')}
        addresses = set().union(*(b.initial.cells for b in prepared.values()))
        for address in addresses:
            self.assertEqual(len({b.initial.at(address).r for b in prepared.values()}), 1)
        joint = prepared['11']
        for mask, removed in (('01', 'lower'), ('10', 'upper')):
            changed = {a for a in addresses if joint.initial.at(a) != prepared[mask].initial.at(a)}
            self.assertEqual(changed, set(joint.sources['apparatus.'+removed]))
        states = list(joint.engine.evolve(joint.initial, 24))
        node = list(joint.ports['apparatus.center'])
        clock = joint.ports['apparatus.clock'][0]
        self.assertEqual(states[13].at(clock), (-1, 0, 0))
        self.assertEqual(states[14].at(clock), (0, 0, 4))
        self.assertEqual(states[24].at(clock), (0, 1, 0))
        for state in states[14:24]:
            self.assertEqual([state.at(a) for a in node], [states[14].at(a) for a in node])
            self.assertTrue(all(state.at(a)[:2] == (0, 0) for a in node))
        region = joint.ports['apparatus.region']
        self.assertTrue(any(state.at(a).a or state.at(a).b for state in states[14:24] for a in region))
        # Observe actual incoming signed terms independently of the study assessor.
        c = joint.engine.coupling
        actual = []
        for old in states[13:24]:
            terms = [c.weights[d][2]*old.at(old.cube.adjacent(clock, d, c.ports[d][2])).b
                     for d in range(6)]
            actual.append(terms)
        self.assertEqual([sum(terms) for terms in actual], [-1]+[0]*9+[1])
        self.assertEqual([i for i, terms in enumerate(actual) if sum(terms) == 0 and any(terms)], [2, 4, 6, 8])
        for old, new in zip(states, states[1:]):
            self.assertEqual(joint.engine.rewind(new), old)


if __name__ == '__main__':
    unittest.main()
