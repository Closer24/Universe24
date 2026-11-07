"""Exact ansatz checks; these never inject input into a running board."""
import unittest

from research.staged_blocks.pulse_words import check_translation, profile, train_cumulative, verify


class PulseWordTests(unittest.TestCase):
    def test_known_packet_and_adjacent_lobes(self):
        self.assertTrue(check_translation([1,1]))
        self.assertTrue(check_translation([1]))
        row,_ = profile([1,1])
        self.assertEqual([row(i) for i in range(4)],
                         [(1,0,4),(0,1,4),(-1,0,4),(0,-1,4)])

    def test_stretching_is_not_superposition(self):
        for distance in range(3,17):
            with self.assertRaises(ValueError):
                profile([1]*distance)
        with self.assertRaises(ValueError):
            profile(train_cumulative((0,2)))
        self.assertTrue(check_translation(train_cumulative((0,4,8))))

    def test_bounded_word_certificate(self):
        result=verify()
        self.assertEqual(result['admissible_isolated_pair_distances'],[1,2])
        self.assertEqual(result['conditional_C_updates'],[1,11])
        self.assertFalse(result['autonomous_two_lane_mechanism_established'])


if __name__=='__main__':
    unittest.main()
