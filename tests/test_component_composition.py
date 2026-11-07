"""Reusable assembly contracts, checked against actual unchanged Rule3 states."""
from copy import deepcopy
from itertools import product
import unittest

from universe24 import Channel, State
from universe24.core.group_2o import group, rotate
from research.components import (BoardSpec, TensorSpec, Patch, SignalSource,
                                 GuideSegment, Receiver, PairedArm, place, finalize)
from research.experiments.run import assemble, run_experiment
from research.experiments.interfaces import signal_case_spec, paired_case_spec


class ComponentCompositionTests(unittest.TestCase):
    def test_all_eight_tensors_and_all_48_lifts_commute_with_complete_evolution(self):
        algebra = group()
        center = (8,8,8)
        raw = {(0,0,0,0):(1,-2,1), (1,-2,0,3):(0,3,4), (-1,0,2,47):(-1,0,5)}
        for signs in product((-1,1), repeat=3):
            tensor = TensorSpec.from_signs(signs)
            board = BoardSpec(17, tensor=tensor)
            patch = Patch('asymmetric', raw, tensor=tensor, ports={'probe': tuple(raw)})
            original = finalize(board, [place(patch, at=center, name='p')])
            states = list(original.engine.evolve(original.initial, 2))
            for lift in range(48):
                moved = finalize(board, [place(patch, at=center, name='p', orientation=lift)])
                actual = list(moved.engine.evolve(moved.initial, 2))
                for before, after in zip(states, actual):
                    cells = {}
                    for address, value in before.cells.items():
                        xyz = rotate(algebra.rotations[lift], tuple(address[i]-center[i] for i in range(3)))
                        target = (*tuple(xyz[i]+center[i] for i in range(3)), algebra.multiplication[lift][address[3]])
                        cells[target] = value
                    self.assertEqual(after, State(before.cube, before.background, cells))
                self.assertEqual(moved.engine.coupling.fingerprint, tensor.fingerprint)

    def test_conflicting_background_claim_is_not_pruned_before_validation(self):
        board = BoardSpec(11)
        blank = Patch('explicit-empty', {(0,0,0,0):(0,0,2)})
        active = Patch('active', {(0,0,0,0):(0,1,2)})
        placements = [place(blank, at=(5,5,5), name='a'), place(active, at=(5,5,5), name='b')]
        for ordered in (placements, placements[::-1]):
            with self.assertRaisesRegex(ValueError, 'conflict'):
                finalize(board, ordered)

    def test_sockets_source_identity_and_shared_assignments(self):
        board = BoardSpec(21)
        guide = place(GuideSegment(start=-3, stop=3, sockets=(0,)), at=(10,10,10), name='guide')
        with self.assertRaisesRegex(ValueError, 'socket'):
            finalize(board, [guide])
        source = place(SignalSource(present=False), at=(10,10,10), name='source')
        prepared = finalize(board, [guide, source])
        self.assertTrue(any(row[:4] == (10,10,10,0) for row in prepared.manifest['raw_assignments']))
        with self.assertRaisesRegex(ValueError, 'sources alias'):
            finalize(board, [source, place(SignalSource(present=False), at=(10,10,10), name='second')])
        one = place(Receiver(), at=(10,10,10), name='one')
        two = place(Receiver(), at=(10,10,10), name='two')
        a, b = finalize(board,[one,two]), finalize(board,[two,one])
        self.assertEqual(a.initial,b.initial)
        self.assertEqual(a.manifest,b.manifest)
        self.assertEqual(len(a.manifest['assignment_owners'][0]['owners']),2)

    def test_json_counter_memory_sources_are_initial_data_and_observers_are_passive(self):
        case = {'id':'counter-test','side':101,'extent':20,'steps':24,
                'source_offsets':[-8,16], 'source_ab':[[0,1],[0,1]],
                'target_remainders':[4,0], 'guide_mode':'between_sources'}
        spec = signal_case_spec(case)
        before = deepcopy(spec)
        original = run_experiment(spec)
        variant = deepcopy(spec)
        variant['detectors'] = []
        variant['readouts'] = []
        variant['view'] = {'port':'source-2.signal','index':1}
        observed = run_experiment(variant)
        self.assertEqual(spec,before)
        self.assertEqual(original['experiment']['frames'],observed['experiment']['frames'])
        self.assertTrue(original['experiment']['provenance']['full_rewind_equal'])
        self.assertEqual(original['observations']['receiver.memory']['record_event_times'],[8,18])

    def test_no_source_control_keeps_the_apparatus_and_full_tensor(self):
        case = {'id':'arms','side':101,'steps':0,'variants':['O','N'],'source_present':True}
        on = assemble(paired_case_spec(case))
        case['source_present'] = False
        off = assemble(paired_case_spec(case))
        changed = {a for a in on.initial.cells.keys() | off.initial.cells.keys() if on.initial.at(a)!=off.initial.at(a)}
        self.assertEqual(changed,set(on.sources['source.signal']))
        self.assertTrue(all(on.initial.at(a).r==off.initial.at(a).r for a in changed))
        self.assertEqual(on.engine.coupling,off.engine.coupling)
        self.assertEqual(on.ports,off.ports)

    def test_runtime_controls_and_invalid_lifts_are_rejected(self):
        for orientation in (True,-1,48,(1,0,0)):
            with self.assertRaises((ValueError,TypeError)):
                place(Receiver(),at=(5,5,5),name='receiver',orientation=orientation)
        spec = paired_case_spec({'id':'invalid','side':101,'steps':1,'variants':['O','N']})
        spec['runtime_gate'] = {'at_step':1,'source_on':True}
        with self.assertRaisesRegex(ValueError,'experiment fields'):
            run_experiment(spec)
        with self.assertRaisesRegex(ValueError,'Tensor conflict'):
            finalize(BoardSpec(11),[place(Receiver(tensor=TensorSpec.from_signs((-1,1,1))),at=(5,5,5),name='receiver')])


if __name__ == '__main__':
    unittest.main()
