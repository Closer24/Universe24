"""Finite algebra checks for the reference routing, independently of Rule3."""
from collections import Counter
import unittest

from sympy.combinatorics import Permutation, PermutationGroup
from universe24.algebra.group_2o import DIRECTIONS, group, rotate
from universe24.algebra.coupling import Coupling


class CouplingAlgebraTests(unittest.TestCase):
    def test_double_cover_of_proper_cube_rotations(self):
        algebra = group()
        self.assertEqual(Counter(Counter(algebra.rotations).values()), {2: 24})
        for g in range(48):
            minus_g = algebra.multiplication[algebra.central][g]
            self.assertNotEqual(g, minus_g)
            self.assertEqual(algebra.rotations[g], algebra.rotations[minus_g])

    def test_ports_and_body_signs_are_covariant_and_reciprocal(self):
        algebra = group()
        for signs in ((1, 1, 1), (1, -1, 1)):
            c = Coupling(signs)
            for d, direction in enumerate(DIRECTIONS):
                self.assertEqual(sum(g == h for g, h in enumerate(c.ports[d])), 16)
                self.assertEqual(c.weights[d].count(-1), 0 if signs == (1, 1, 1) else 16)
                for g in range(48):
                    h = c.ports[d][g]
                    self.assertEqual(c.ports[d ^ 1][h], g)
                    self.assertEqual(c.weights[d ^ 1][h], c.weights[d][g])
                    for k in range(48):
                        rd = DIRECTIONS.index(rotate(algebra.rotations[k], direction))
                        kg = algebra.multiplication[k][g]
                        self.assertEqual(c.ports[rd][kg], algebra.multiplication[k][h])
                        self.assertEqual(c.weights[rd][kg], c.weights[d][g])

    def test_generated_group_is_not_2o_regular_action(self):
        plain = Coupling()
        ports = [Permutation(list(row)) for row in plain.ports]
        self.assertEqual([p.order() for p in ports], [8] * 6)
        self.assertEqual(PermutationGroup(ports).order(), 196608)
        signed = Coupling((1, -1, 1))
        lifted = [Permutation([
            signed.ports[d][i % 48] + 48 * ((i // 48) ^ (signed.weights[d][i % 48] < 0))
            for i in range(96)]) for d in range(6)]
        self.assertEqual([p.order() for p in lifted], [8] * 6)
        self.assertEqual(PermutationGroup(lifted).order(), 196608)
