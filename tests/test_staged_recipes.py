"""Reusable data recipes reproduce the frozen phase preparations exactly."""
from copy import deepcopy
import gzip
import json
from pathlib import Path
import tempfile
import unittest

from research.components import BoardSpec, GuideSegment, Patch, TensorSpec, finalize, place
from research.experiments.run import assemble, recorded_states
from research.staged_blocks.recipes import (ClockGuideInterface, InterfaceGuide,
    phase_assembly, relative_phase_observer, observe_relative_phase, verify_phase_preparations)
from research.staged_blocks.composition import validate_source_off

ROOT = Path(__file__).resolve().parents[1]


class StagedRecipeTests(unittest.TestCase):
    def test_all256_frozen_initial_states_equal_canonical_bytes_and_recorded_hashes(self):
        with tempfile.TemporaryDirectory() as folder:
            result = verify_phase_preparations(Path(folder)/'equivalence')
            self.assertEqual(result['cases'],256)
            self.assertTrue(result['canonical_full_initial_states_byte_equal'])
            self.assertEqual(result['new_trajectories_generated'],0)
            self.assertTrue(all(row['recorded_initial_hash_equal'] for row in result['rows']))

    def test_interface_protects336_channels_and_preserves_other_guide_channel(self):
        tensor = TensorSpec()
        for phase in range(4):
            patch = ClockGuideInterface(r=4, phase=phase, tensor=tensor)
            cells = dict(patch.cells)
            self.assertEqual(len(cells),336)
            self.assertEqual(tuple(cells[(0,-1,0,14)]),(0,0,4))
            self.assertEqual(cells[(0,-1,0,0)].r,2 if phase in (1,2) else 0)
            self.assertEqual(patch.tensor.fingerprint,tensor.fingerprint)
            off = ClockGuideInterface(r=4,phase=phase,present=False,tensor=tensor)
            self.assertTrue(all(cells[a].r==v.r for a,v in off.cells))
            changed = {a for a,v in off.cells if cells[a]!=v}
            self.assertEqual(changed,set(patch.sources['clock']))

    def test_guide_uses_explicit_compatible_interface_socket(self):
        assembly = phase_assembly(phase=1)
        guide, packet, interface, reference = assembly.placements
        with self.assertRaisesRegex(ValueError,'socket'):
            finalize(assembly.board,[guide,packet,reference])
        prepared = finalize(assembly.board,assembly.placements)
        self.assertEqual(prepared.initial.at((64,64,64,14)).r,4)
        self.assertEqual(prepared.initial.at((64,64,64,0)).r,2)
        with self.assertRaisesRegex(ValueError,'same guide socket'):
            InterfaceGuide(side=129,packet_start=62,interface_x=64)

    def test_unreserved_guide_and_wrong_protected_channel_do_not_overwrite(self):
        board = BoardSpec(129)
        interface = place(ClockGuideInterface(phase=1),at=(64,65,64),name='interface')
        wrong_guide = place(GuideSegment(start=0,stop=128,remainder_pair=(0,4)),
                            at=(0,64,64),name='wrong-guide')
        for order in ([interface,wrong_guide],[wrong_guide,interface]):
            with self.assertRaisesRegex(ValueError,'conflict'):
                finalize(board,order)
        bad = place(Patch('bad', {(0,0,0,14):(0,0,2)}),at=(64,64,64),name='bad')
        with self.assertRaisesRegex(ValueError,'conflict'):
            finalize(board,[interface,bad])
        # Full protected background channels are resources too, not absent cells.
        active = place(Patch('active', {(0,0,0,47):(1,0,2)}),at=(64,65,64),name='active')
        with self.assertRaisesRegex(ValueError,'conflict'):
            finalize(board,[interface,active])

    def test_control_removes_only_declared_counter_sources_reference_unchanged(self):
        prepared = {mask:phase_assembly(control=mask,phase=2).prepare() for mask in ('00','10','01','11')}
        validate_source_off(prepared['11'],prepared['01'],['packet.packet'])
        validate_source_off(prepared['11'],prepared['10'],['interface.clock'])
        validate_source_off(prepared['11'],prepared['00'],['packet.packet','interface.clock'])
        reference = prepared['11'].ports['reference.center'][0]
        for board in prepared.values():
            self.assertEqual(tuple(board.initial.at(reference)),(0,1,2))

    def test_parameter_domain_is_explicit_and_no_new_tensor_is_implied(self):
        for kwargs in ({'side':65},{'delay':0},{'r':2}):
            with self.assertRaisesRegex(ValueError,'finite domain'):
                phase_assembly(**kwargs)
        exploratory = phase_assembly(side=65,delay=0,exploratory=True)
        self.assertFalse(exploratory.metadata['matches_validated_parameter_domain'])
        self.assertTrue(exploratory.metadata['exploratory_geometry'])
        with self.assertRaisesRegex(ValueError,r'fixed \+\+\+'):
            ClockGuideInterface(tensor=TensorSpec.from_signs((-1,1,1)))
        for kwargs in ({'phase':True},{'r':2},{'present':1}):
            with self.assertRaises(ValueError):
                ClockGuideInterface(**kwargs)
        with self.assertRaisesRegex(ValueError,'does not fit'):
            phase_assembly(side=33,exploratory=True)

    def test_native_four_piece_spec_roundtrips_and_extended_horizon_is_not_validated(self):
        assembly = phase_assembly(side=161,r=4,phase=3,delay=5)
        spec = assembly.experiment_spec()
        self.assertEqual(len(spec['components']),4)
        self.assertEqual([c['name'] for c in spec['components']],['guide','packet','interface','reference'])
        self.assertEqual(assemble(spec).initial,assembly.prepare().initial)
        self.assertTrue(spec['provenance']['matches_validated_parameter_domain'])
        self.assertFalse(assembly.experiment_spec(steps=80)['provenance']['matches_validated_parameter_domain'])

    def test_passive_same_board_DX_matches_frozen_readout_and_all_C_remain(self):
        filename = ROOT/'research/staged_blocks/evidence/interactions/phase_v1/records/phase-L129-r0-p0-d1-11.json.gz'
        record = json.loads(gzip.decompress(filename.read_bytes()))
        states = recorded_states(record['experiment'])
        prepared = phase_assembly(side=129,r=0,phase=0,delay=1).prepare()
        observer = relative_phase_observer(prepared.ports['interface.center'][0],prepared.ports['reference.center'][0])
        old_hashes = [frame['state_sha256'] for frame in record['experiment']['frames']]
        result = observe_relative_phase(observer,states)
        expected = record['observations']['phase_trace']
        self.assertEqual([(r['D'],r['X']) for r in result['trace']],[(r['D'],r['X']) for r in expected])
        self.assertEqual(old_hashes,[frame['state_sha256'] for frame in record['experiment']['frames']])
        self.assertTrue(all(row['identity_equal'] for row in result['trace']))
        self.assertFalse(observer['physical_comparator_implemented'])
        self.assertEqual(tuple(observer['arithmetic_C_classes_retained']),(0,1,2))
        with self.assertRaises(TypeError):
            observer['target']=(0,0,0,0)


if __name__ == '__main__':
    unittest.main()
