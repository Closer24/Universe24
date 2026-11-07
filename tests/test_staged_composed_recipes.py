"""Data-only composition, controls and resource protection; no trajectories."""
import unittest

from research.components import BoardSpec, Patch, TensorSpec, finalize, place
from research.experiments.run import assemble
from research.staged_blocks.composed_recipes import effective_coupler, two_lane_pause
from research.staged_blocks.composition import validate_source_off


class ComposedRecipeTests(unittest.TestCase):
    def test_coupler_controls_are_exact_source_masks_within_each_family(self):
        for family in ('enable', 'aligned_suppress'):
            boards = {mask: effective_coupler(family=family, control=mask).prepare()
                      for mask in ('00', '10', '01', '11')}
            validate_source_off(boards['11'], boards['01'], ['packet.packet'])
            validate_source_off(boards['11'], boards['10'], ['interface.clock'])
            validate_source_off(boards['11'], boards['00'], ['packet.packet', 'interface.clock'])
        enabling = effective_coupler(family='enable').prepare()
        suppressing = effective_coupler(family='aligned_suppress').prepare()
        self.assertNotEqual(enabling.initial.at((68,68,68,0)).r,
                            suppressing.initial.at((68,68,68,0)).r)

    def test_pause_controls_keep_clock_and_shared_remainders(self):
        recipes = {mask: two_lane_pause(control=mask) for mask in ('00', '10', '01', '11')}
        boards = {mask: value.prepare() for mask, value in recipes.items()}
        validate_source_off(boards['11'], boards['01'], ['lower.train'])
        validate_source_off(boards['11'], boards['10'], ['upper.train'])
        validate_source_off(boards['11'], boards['00'], ['lower.train', 'upper.train'])
        clock = boards['11'].ports['bridge.clock'][0]
        self.assertEqual(len({board.initial.at(clock) for board in boards.values()}), 1)
        self.assertNotEqual(tuple(boards['00'].initial.at(clock))[:2], (0,0))
        self.assertEqual(len(boards['11'].ports['bridge.region']), 336)
        self.assertEqual([p.name for p in recipes['11'].placements], ['lower','upper','bridge'])

    def test_joint_region_and_guide_conflicts_never_overwrite(self):
        recipe = two_lane_pause()
        prepared = recipe.prepare()
        for address in ((64,65,64,47), (64,64,64,0), (64,66,64,6)):
            old = prepared.initial.at(address)
            patch = place(Patch('intruder', {address: (old.a+1, old.b, old.r)}),
                          at=(0,0,0), name='intruder')
            for placements in ((*recipe.placements, patch), (patch, *recipe.placements)):
                with self.assertRaisesRegex(ValueError, 'conflict'):
                    finalize(recipe.board, placements)
        wrong = BoardSpec(129, tensor=TensorSpec.from_signs((-1,1,1)))
        with self.assertRaises(ValueError):
            finalize(wrong, recipe.placements)

    def test_native_specs_and_metadata_are_data_only(self):
        for recipe in (effective_coupler(), two_lane_pause()):
            self.assertEqual(assemble(recipe.experiment_spec()).initial, recipe.prepare().initial)
            self.assertEqual(len(recipe.placements), 3)
            self.assertTrue(recipe.experiment_spec()['provenance']['matches_validated_parameter_domain'])
            self.assertFalse(recipe.experiment_spec(steps=41)['provenance']['matches_validated_parameter_domain'])
            with self.assertRaises(TypeError):
                recipe.metadata['control'] = '00'
            self.assertEqual(recipe.board.tensor.fingerprint, recipe.metadata['tensor_fingerprint'])

    def test_unvalidated_parameter_domains_are_rejected(self):
        for factory, kwargs in ((effective_coupler, {'side':129}),
                                (effective_coupler, {'delay':0}),
                                (effective_coupler, {'family':'approval'}),
                                (two_lane_pause, {'delay':4}),
                                (two_lane_pause, {'side':137})):
            with self.assertRaisesRegex(ValueError, 'finite domain'):
                factory(**kwargs)
        for factory in (effective_coupler, two_lane_pause):
            with self.assertRaises(ValueError):
                factory(control='111')
            with self.assertRaises(ValueError):
                factory(delay=True)
            with self.assertRaisesRegex(ValueError, r'fixed \+\+\+'):
                factory(tensor=TensorSpec.from_signs((-1,1,1)))


if __name__ == '__main__':
    unittest.main()
