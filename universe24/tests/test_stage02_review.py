"""Fixed-divisor contract, field-sign justification, and reference mirror checks."""
import unittest
import numpy as np

from universe24.core import Engine, GearType, State, Tensor, build, check_reciprocity, reference_block
from universe24.core.lattice import ZERO
from universe24.core.reversors import GearwiseMap, is_fixed, remainder_map, reversor_check
from universe24.core.tensor import FORMAT
from universe24.tests import randgen
from universe24.tests.l0_oracle import time_reverse, Channel, Cube, RefState


class T14FixedDivisorAndSigns(unittest.TestCase):
    def test_fixed_divisor_is_not_a_constructor_option(self):
        tensor = build(reference_block())
        engine = Engine(tensor)
        self.assertEqual(engine.D, 6)
        with self.assertRaises(TypeError):
            Engine(tensor, 7)
        with self.assertRaises(TypeError):
            Tensor(["g"], [], Q=7)
        for value in (-1, 6, 42):
            with self.subTest(remainder=value), self.assertRaises(ValueError):
                engine.vacuum(3, [value]*48)
        self.assertEqual(Tensor.from_dict(tensor.to_dict()), tensor)

    def test_field_signs_need_justification(self):
        with self.assertRaises(ValueError):
            GearType("p", sign=-1)
        with self.assertRaises(ValueError):
            Tensor([{"name":"p", "sign":-1}], [])
        with self.assertRaises(ValueError):
            Tensor.from_dict({"format":FORMAT, "gears":[{"name":"p", "sign":-1}], "monomials":[]})
        gears = [GearType("a0"), GearType("a1", sign=-1, sign_why="time-like test component")]
        terms = [("a0",4,(("a1",ZERO,"b"),)), ("a1",-4,(("a0",ZERO,"b"),))]
        tensor = Tensor(gears, terms)
        report = check_reciprocity(tensor)
        self.assertTrue(report.ok)
        self.assertEqual(report.negative_sign_gears, [("a1","time-like test component")])
        self.assertEqual(Tensor.from_dict(tensor.to_dict()), tensor)


class T15ReferenceMirror(unittest.TestCase):
    def test_six_remainder_map(self):
        r = np.arange(6, dtype=object)
        rho = remainder_map("rhoL0", r)
        self.assertTrue(np.all((0 <= rho) & (rho < 6)))
        np.testing.assert_array_equal(remainder_map("rhoL0",rho),r)
        expected = [time_reverse(RefState(Cube(3),Channel(0,0,k))).background.r for k in range(6)]
        self.assertEqual(list(map(int,rho)),expected)
        np.testing.assert_array_equal(rho,remainder_map("Mp",r))
        self.assertEqual(int(rho[2]),2)
        with self.assertRaises(ValueError):
            remainder_map("rhoL0",r,42)

    def test_joint_reference_and_integer_nonlinear_reversor(self):
        # At divisor six every input numerator 2u is even. No extra scale
        # lattice is needed. Both even/odd carry sectors are exercised.
        reference = reference_block()
        names = [g.name for g in reference.gears] + ["new"]
        terms = list(reference.terms) + [
            ("new",3,(("new",ZERO,"b"),)),
            ("new",1,(("R00",ZERO,"b"),("new",ZERO,"b"))),
            ("R00",-1,(("new",ZERO,"b"),("R01",ZERO,"b"))),
        ]
        tensor = Tensor(names,terms)
        engine = Engine(tensor)
        mirror = GearwiseMap(tensor,default="rhoL0")
        seed = engine.vacuum(3,[2]*tensor.G)
        self.assertTrue(is_fixed(mirror,seed))
        states = [randgen.random_state(1500+k,tensor.G,3,6,-2,2) for k in range(3)]
        result = reversor_check(mirror,engine,states,4)
        self.assertTrue(result["ok"])
        self.assertEqual(result["identity"],3)


if __name__ == "__main__":
    unittest.main()
