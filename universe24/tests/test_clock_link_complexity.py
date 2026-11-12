"""Falsifying controls for the passive clock-link organization protocol."""
import unittest

from validation.clock_links.complexity_audit import (
    burst_growth, control_audit, cube_adjacency, persistent_organization,
    phase_motifs, phase_relation, trajectory_scores,
)


class ClockLinkComplexityTests(unittest.TestCase):
    def test_relation_preserves_signed_interference_distinction(self):
        self.assertEqual(phase_relation((1, 0), (2, 0)), (1, 0))
        self.assertEqual(phase_relation((1, 0), (-2, 0)), (-1, 0))
        self.assertEqual(phase_relation((1, 0), (0, 2)), (0, 1))
        self.assertEqual(phase_relation((0, 2), (1, 0)), (0, -1))
        self.assertEqual(phase_relation((0, 0), (1, 0)), (2, 2))

    def test_exact_large_integer_amplitude_and_common_phase(self):
        left, right = (2, -3), (-7, 11)
        expected = phase_relation(left, right)
        self.assertEqual(phase_relation(tuple(v*(10**150+1) for v in left),
                                        tuple(v*(10**130+7) for v in right)), expected)
        multiply = lambda p: (3*p[0]+5*p[1], -5*p[0]+3*p[1])
        self.assertEqual(phase_relation(multiply(left), multiply(right)), expected)

    def test_no_source_uniform_and_single_site_novelty_do_not_pass(self):
        adjacent = cube_adjacency(3)
        for vectors in [[(0, 0)]*27, [(1, 0)]*27]:
            motifs = phase_motifs(vectors, adjacent)
            self.assertEqual(persistent_organization(motifs, motifs)["score"], 0)
        motif = (((1, 0),)*5 + ((0, 1),))
        self.assertEqual(persistent_organization([motif], [motif])["score"], 0)
        self.assertEqual(persistent_organization([motif, motif], [motif, motif])["score"], 1)

    def test_seed_is_not_credited_without_two_checkpoints(self):
        adjacent = cube_adjacency(3)
        trajectory = [[(1, 0)]*27]
        self.assertEqual(trajectory_scores(trajectory, adjacent)[0]["score"], 0)

    def test_periodic_bursts_cannot_pass_strict_growth(self):
        result = control_audit()
        self.assertTrue(all(result["checks"].values()))
        self.assertEqual(len(result["periodic_growth_control"]["burst_steps"]), 4)
        self.assertEqual(result["periodic_growth_control"]["status"], "failed")

    def test_burst_window_requires_interior_maxima_and_full_sequence(self):
        scores = [{"score": i} for i in range(13)]
        self.assertTrue(burst_growth(scores, [0, 1, 0]*4)["strict_growth"])
        self.assertEqual(burst_growth(scores, [1]*12)["status"], "blocked")
        self.assertEqual(burst_growth(scores[:4], [9, 8, 7])["burst_steps"], [])
        with self.assertRaises(ValueError):
            burst_growth(scores, [0])

    def test_frozen_random_limitation_is_preserved(self):
        random_controls = control_audit()["random_controls"]
        self.assertTrue(any(c["frozen_random_score"] > 0 for c in random_controls))

    def test_reject_noninteger_and_incomplete_geometry(self):
        with self.assertRaises(ValueError):
            phase_relation((1.0, 0), (1, 0))
        with self.assertRaises(ValueError):
            phase_motifs([(1, 0)], [(0,)])


if __name__ == "__main__":
    unittest.main()
