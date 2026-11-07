"""Deliberately incorrect executors, confined to tests, must be detected.

No production file or running automaton is patched. These are four specific
fault models, not a claim of exhaustive mutation coverage.
"""
import random
import unittest
from research.reference import advance, coupling, forward
from research.reference.evolution import neighbor_indices
from research.reproducibility.bundle import first_difference


def corrupted_step(state, side, fault):
    neighbors = neighbor_indices(side)
    weights = coupling((1, -1, 1)).weights
    source = list(state)
    result = []
    for i, adjacent in enumerate(neighbors):
        g = i % 48
        total = 0
        for d in range(6):
            swap = fault == 'paired_swap' or (fault == 'wrong_direction' and d == 0)
            sender = adjacent[d ^ 1] if swap else adjacent[d]
            weight = weights[d][g] * (-1 if fault == 'wrong_sign' and d == 0 else 1)
            total += weight * source[sender][1]
        value = forward(source[i], total)
        if fault == 'lost_remainder':
            value = value[:2] + (2,)
        result.append(value)
        if fault == 'in_place':
            source[i] = value
    return tuple(result)


class FaultDetectionTests(unittest.TestCase):
    def test_four_fault_classes_are_detected_by_complete_state_comparison(self):
        rng = random.Random(24004)
        state = tuple((rng.randrange(-3,4), rng.randrange(-3,4), rng.randrange(6))
                      for _ in range(48*3**3))
        expected = advance(state, 3, (1,-1,1))
        self.assertEqual(corrupted_step(state,3,'none'), expected)
        # Swapping BOTH opposite inputs with equal weights only reorders a sum.
        # This equivalent transformation is a negative control, not a fault.
        self.assertEqual(corrupted_step(state,3,'paired_swap'), expected)
        for fault in ('wrong_direction','wrong_sign','lost_remainder','in_place'):
            with self.subTest(fault=fault):
                actual = corrupted_step(state,3,fault)
                difference = first_difference([list(x) for x in expected], [list(x) for x in actual])
                self.assertIsNotNone(difference, f'Fault escaped: {fault}')
                self.assertNotEqual(difference['expected'], difference['actual'])
        self.assertEqual(advance(state,3,(1,-1,1)),expected)


if __name__ == '__main__':
    unittest.main()
