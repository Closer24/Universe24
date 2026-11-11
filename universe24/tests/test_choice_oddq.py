"""The old matched-router amplitude equation has no fixed-six integer solution."""
import unittest
from universe24.layers.choice_oddq import near_matched_kappa,predicted_non_detection,build_odd_q_router
class RetiredMatchedRouterTests(unittest.TestCase):
    def test_integer_obstruction_is_reported(self):
        for amplitude in (1,2,100):
            self.assertGreater(16*amplitude**2,6)
            with self.assertRaises(NotImplementedError):near_matched_kappa(amplitude)
            with self.assertRaises(NotImplementedError):predicted_non_detection(amplitude)
        with self.assertRaises(NotImplementedError):build_odd_q_router(A=1,arm1=('a',),arm2=('b',))
