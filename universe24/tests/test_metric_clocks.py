from fractions import Fraction as F
import unittest
from universe24.observe.metric_clocks import rate_squared, clock_readout


class MetricClockTests(unittest.TestCase):
    def test_flat_motion_null_and_spacelike(self):
        metric = [[(-1 if i == 0 else 1) if i == j else 0 for j in range(4)] for i in range(4)]
        self.assertEqual(rate_squared(metric, (F(3, 5), 0, 0)), F(16, 25))
        self.assertEqual(rate_squared(metric, (1, 0, 0)), 0)
        self.assertLess(rate_squared(metric, (2, 0, 0)), 0)

    def test_shifted_chart_does_not_confuse_grid_clock_and_normal_clock(self):
        # Flat spacetime in a shifted chart; a stationary grid tangent may be
        # spacelike even though the hypersurface normal remains timelike.
        for shift in (F(1, 2), F(1), F(2)):
            metric = [[-1+shift*shift, shift, 0, 0], [shift, 1, 0, 0],
                      [0, 0, 1, 0], [0, 0, 0, 1]]
            result = clock_readout(metric, 1, (shift, 0, 0))
            self.assertEqual(result['normal_rate_squared'], 1)
            self.assertEqual(result['grid_rate_squared'], 1-shift*shift)
            self.assertEqual(result['normal_coordinate_velocity'], (-shift, 0, 0))
        self.assertEqual(result['grid_worldline'], 'spacelike')

    def test_nonunit_lapse_and_off_diagonal_metric(self):
        gamma = [[F(2), F(1, 3), F(0)], [F(1, 3), F(3), F(1, 7)], [F(0), F(1, 7), F(4)]]
        beta, alpha = (F(1, 5), F(-1, 6), F(1, 9)), F(7, 4)
        cov = [sum(gamma[i][j]*beta[j] for j in range(3)) for i in range(3)]
        metric = [[-alpha*alpha+sum(cov[i]*beta[i] for i in range(3)), *cov]]
        metric += [[cov[i], *gamma[i]] for i in range(3)]
        self.assertEqual(clock_readout(metric, alpha, beta)['normal_rate'], alpha)
        with self.assertRaises(ValueError):
            clock_readout(metric, alpha+1, beta)
