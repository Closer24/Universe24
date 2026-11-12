"""Cross-layer regressions for the saved massive law and board evidence."""
from fractions import Fraction as F
import tempfile
import unittest
from pathlib import Path

from universe24.system.runtime import verify_run
from .run import build_program, prepare_seed, run


class MassiveRunTests(unittest.TestCase):
    def test_same_massive_law_replays_and_exposes_constraint_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)/'evidence'
            result = run(out, steps=1)
            self.assertEqual(result['metadata']['tensor_sha256'],
                             'fbbf8f9b4128563e786ff0b57069fe18320698451c0ac9acb0c947c568cfc617')
            self.assertEqual(result['metadata']['channels'], 45)
            self.assertEqual(result['metadata']['terms'], 889)
            self.assertEqual(result['runtime_validation'], verify_run(out/'runtime'))
            self.assertEqual(result['independent_first_step_control']['observed_H'], '-7/1024')
            self.assertEqual(result['acceptance_gates']['exact_discrete_Einstein_constraints'], 'failed')
            self.assertTrue((out/'board.html').is_file())
            self.assertTrue(result['geodesics'])
            with self.assertRaises(ValueError):
                run(out, steps=1)

    def test_exact_inputs_and_bounded_horizon(self):
        for value in (0, -1):
            with self.assertRaises(ValueError):
                build_program(dt=value)
            with self.assertRaises(ValueError):
                build_program(dx=value)
        for value in (0.1, True):
            with self.assertRaises(TypeError):
                build_program(dt=value)
        for value in (-1, 1.0, True):
            with self.assertRaises(ValueError):
                build_program(mass_squared=value)
        with tempfile.TemporaryDirectory() as directory:
            for steps in (0, 9, True):
                with self.assertRaises(ValueError):
                    run(Path(directory)/'unused', steps=steps)

    def test_seed_retains_every_remainder_and_denominator_is_explicit(self):
        program = build_program()
        seed = prepare_seed(program)
        self.assertEqual(set(int(v) for v in seed.r.flat), set(range(6)))
        self.assertEqual(seed.G*3, 135)
        self.assertTrue(all(int(v) == 32 for v in seed.b[0]))
        with self.assertRaises(ValueError):
            prepare_seed(program, denominator=1)
        self.assertFalse(program.tensor.support_violations())
        self.assertFalse(any(f.field == 'a' for term in program.tensor.monomials for f in term.factors))


if __name__ == '__main__':
    unittest.main()
