"""Independent analytic controls for passive geodesic readout."""
import copy
import math
import unittest

import numpy as np

from .geodesics import build_geodesics, integrate_path


def snapshots(g0, g1, duration=1):
    return [{'time': 0., 'gamma': g0, 'homogeneous': True},
            {'time': duration, 'gamma': g1, 'homogeneous': True}]


class GeodesicReadoutTests(unittest.TestCase):
    def test_minkowski_massive_and_null(self):
        data = snapshots(np.eye(3), np.eye(3), 2.)
        massive = integrate_path(data, (3, 0, 0), substeps=7)['points'][-1]
        np.testing.assert_allclose(massive['x'], [6/math.sqrt(10), 0, 0], atol=1e-14)
        self.assertAlmostEqual(massive['tau'], 2/math.sqrt(10), places=14)
        light = integrate_path(data, (3, 0, 0), kind='null', substeps=7)['points'][-1]
        np.testing.assert_allclose(light['x'], [2, 0, 0], atol=1e-14)
        self.assertIsNone(light['tau'])
        self.assertAlmostEqual(light['affine'], 2/3, places=14)

    def test_off_diagonal_coordinate_flat_metric(self):
        # x = A X is an independently declared linear change of Minkowski coordinates.
        A = np.array([[2., 1., 0.], [0., 3., 0.], [0., 0., .5]])
        inverse = np.linalg.inv(A)
        gamma = inverse.T @ inverse
        p = np.array([1., 2., -1.])
        physical_p = A.T @ p
        expected_x = A @ physical_p/math.sqrt(1+physical_p @ physical_p)
        final = integrate_path(snapshots(gamma, gamma), p)['points'][-1]
        np.testing.assert_allclose(final['x'], expected_x, atol=2e-14)
        self.assertLess(final['normalization_error'], 2e-14)

    def test_expanding_metric_null_analytic_refinement(self):
        # ds²=-dt²+(1+2Ht)dx², exact x=(sqrt(1+2HT)-1)/H.
        h, duration = .5, 2.
        data = snapshots(np.eye(3), (1+2*h*duration)*np.eye(3), duration)
        exact = (math.sqrt(1+2*h*duration)-1)/h
        errors = [abs(integrate_path(data, kind='null', substeps=n)['points'][-1]['x'][0]-exact)
                  for n in (4, 8, 16)]
        self.assertGreater(errors[0]/errors[1], 3.8)
        self.assertGreater(errors[1]/errors[2], 3.9)
        final = integrate_path(data, kind='null')['points'][-1]
        self.assertAlmostEqual(final['energy'], 1/math.sqrt(3), places=14)

    def test_expanding_metric_massive_analytic(self):
        h, duration, p = .5, 2., .75
        g = 1+2*h*duration
        data = snapshots(np.eye(3), g*np.eye(3), duration)
        exact_x = p/h*(math.asinh(math.sqrt(g)/p)-math.asinh(1/p))
        primitive = lambda z: math.sqrt(z*(z+p*p))-p*p*math.asinh(math.sqrt(z)/p)
        exact_tau = (primitive(g)-primitive(1))/(2*h)
        final = integrate_path(data, (p, 0, 0), substeps=4096)['points'][-1]
        self.assertAlmostEqual(final['x'][0], exact_x, places=7)
        self.assertAlmostEqual(final['tau'], exact_tau, places=7)

    def test_no_mutation_and_same_metric(self):
        data = snapshots(np.eye(3).tolist(), (2*np.eye(3)).tolist())
        before = copy.deepcopy(data)
        report = build_geodesics(data)
        self.assertEqual(data, before)
        self.assertEqual(report['retained_probe_channels'], 0)
        self.assertEqual(len(report['paths']), 5)
        resting = report['paths'][-1]['points'][-1]
        self.assertEqual(resting['x'], [0., 0., 0.])
        self.assertEqual(resting['tau'], 1.)

    def test_reject_unsupported_domains(self):
        data = snapshots(np.eye(3), np.eye(3))
        for bad in (np.diag([1, 1, 0]), np.diag([1, 1, -1]), [[1, 1, 0], [0, 1, 0], [0, 0, 1]]):
            with self.assertRaises(ValueError):
                integrate_path(snapshots(np.eye(3), bad))
        with self.assertRaises(ValueError):
            integrate_path(data, (0, 0, 0), kind='null')
        with self.assertRaises(ValueError):
            integrate_path([{**data[0], 'homogeneous': False}, data[1]])
        with self.assertRaises(ValueError):
            integrate_path([{**data[0], 'nodes': [{'gamma': 2*np.eye(3)}]}, data[1]])
        with self.assertRaises(ValueError):
            integrate_path([data[0], {**data[1], 'time': 0}])


if __name__ == '__main__':
    unittest.main()
