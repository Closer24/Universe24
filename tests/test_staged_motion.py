"""Exact translation semantics and immutable observer tests."""
import unittest

from universe24 import Coupling, Cube, Engine, State
from research.component_review import audit as independent
from research.staged_blocks import motion


class MotionTests(unittest.TestCase):
    def test_translation_group_law_with_wrapping_and_all_components(self):
        state = State(Cube(5), cells={(0,4,2,47):(-10**80,10**90,5), (4,0,1,0):(0,0,0)})
        first = motion.translate_state(state,(7,-3,2))
        self.assertEqual(motion.translate_state(first,(-7,3,-2)), state)
        self.assertEqual(motion.translate_state(first,(1,3,-5)), motion.translate_state(state,(8,0,-3)))
        self.assertEqual(first.at((2,1,4,47)), state.at((0,4,2,47)))

    def test_signed_covariance_matches_independent_matrix_oracle(self):
        state = State(Cube(5),cells={(0,4,2,47):(-10**80,10**90,5),(4,0,1,0):(0,2,0),(1,2,0,14):(3,-1,4)})
        engine = Engine(Coupling((1,-1,1)))
        q = (-1,2,0)
        moved = motion.translate_state(state,q)
        actual = engine.advance(moved)
        oracle = independent.advance(independent.from_state(moved),(1,-1,1))
        self.assertEqual(independent.from_state(actual),oracle)
        self.assertEqual(actual,motion.translate_state(engine.advance(state),q))
        self.assertEqual(engine.rewind(actual),moved)

    def test_vacuum_and_shift_alias_cannot_count_as_motion(self):
        vacuum = State(Cube(5))
        raw = motion.relative_periodicity([vacuum]*5,1,(1,0,0))
        self.assertTrue(raw["all_complete_comparisons_equal"])
        self.assertTrue(raw["initial_translation_invariant"])
        self.assertFalse(raw["nontrivial_relative_periodicity"])
        defect = State(Cube(5),cells={(2,2,2,8):(0,0,4)})
        alias = motion.relative_periodicity([defect]*5,4,(5,0,0))
        self.assertTrue(alias["shift_aliases_identity"])
        self.assertFalse(alias["nontrivial_relative_periodicity"])
        self.assertFalse(motion.relative_periodicity([defect]*5,4,(1,0,0))["nontrivial_relative_periodicity"])

    def test_periodic_fixed_location_is_not_a_traveling_pattern(self):
        triples = [(1,0,2),(0,-1,2),(-1,0,2),(0,1,2),(1,0,2)]
        states = [State(Cube(5),cells={(2,2,2,8):v}) for v in triples]
        self.assertTrue(motion.relative_periodicity(states,4,(0,0,0))["all_complete_comparisons_equal"])
        for q in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
            self.assertFalse(motion.relative_periodicity(states,4,q)["nontrivial_relative_periodicity"])

    def test_observer_samples_native_addresses_without_mutation(self):
        states = [State(Cube(5),cells={(t,2,2,8):(t+1,-t,t%6)}) for t in range(5)]
        original = [motion.state_sha256(s) for s in states]
        result = motion.sample_moving_observer(states,(0,2,2),(2,0,0),period=2)
        self.assertEqual([s["native_step"] for s in result["samples"]],[0,2,4])
        self.assertEqual([s["native_position"] for s in result["samples"]],[[0,2,2],[2,2,2],[4,2,2]])
        self.assertEqual(result["samples"][1]["full_48_channel_node"][8],["3","-2","2"])
        self.assertFalse(result["is_native_engine_trajectory"])
        self.assertNotIn("frames",result)
        self.assertEqual(original,[motion.state_sha256(s) for s in states])


if __name__ == "__main__":
    unittest.main()
