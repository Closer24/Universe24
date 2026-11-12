"""Independent integration review of the passive shared-metric geodesics.

These tests check the geodesic equation and spatial coordinate covariance,
not Einstein evolution of the metric or a retained Engine test particle.
"""
from __future__ import annotations

import copy
import unittest

import numpy as np

from .geodesics import build_geodesics, integrate_path


class IndependentGeodesicIntegrationReview(unittest.TestCase):
    def setUp(self):
        self.gamma0 = np.array([[2., .3, .1], [.3, 1.4, -.15], [.1, -.15, .9]])
        self.rate = np.array([[.3, .08, 0.], [.08, -.1, .04], [0., .04, .2]])
        self.p = np.array([.7, -.4, .3])

    def data(self, times, basis=None):
        basis = np.eye(3) if basis is None else basis
        inverse = np.linalg.inv(basis)
        return [{'time': t, 'homogeneous': True,
                 'gamma': (inverse.T @ (self.gamma0+t*self.rate) @ inverse).tolist()}
                for t in times]

    def test_full_christoffel_equation_not_only_tangent_normalization(self):
        # Independent 4D Christoffel construction for g00=-1, g0i=0.
        # Noncommuting gamma and gamma_dot exercise full matrix terms.
        h = 1e-5
        data = self.data([-h, 0., h])
        connection = np.zeros((4, 4, 4))
        connection[0, 1:, 1:] = self.rate/2
        connection[1:, 0, 1:] = np.linalg.solve(self.gamma0, self.rate)/2
        connection[1:, 1:, 0] = connection[1:, 0, 1:]
        for kind in ('null', 'timelike'):
            with self.subTest(kind=kind):
                points = integrate_path(data, self.p, kind=kind)['points']
                tangents = [np.r_[point['energy'],
                                  point['energy']*np.array(point['velocity'])]
                            for point in points]
                u = tangents[1]
                d_u_d_t = (tangents[2]-tangents[0])/(2*h)
                acceleration = u[0]*d_u_d_t
                curvature_term = np.einsum('abc,b,c->a', connection, u, u)
                np.testing.assert_allclose(acceleration+curvature_term, 0., atol=2e-10)

    def test_time_dependent_spatial_coordinate_covariance(self):
        # x'=A x is a constant spatial coordinate change, applied to a
        # time-dependent metric. It must not change proper or affine time.
        A = np.array([[1.2, .4, -.1], [0., .8, .2], [0., 0., 1.5]])
        transformed_p = np.linalg.solve(A.T, self.p)
        times = [0., .2, .5, 1.]
        for kind in ('null', 'timelike'):
            with self.subTest(kind=kind):
                original = integrate_path(self.data(times), self.p, kind=kind)
                transformed = integrate_path(self.data(times, A), transformed_p, kind=kind)
                for first, second in zip(original['points'], transformed['points']):
                    np.testing.assert_allclose(second['x'], A @ np.array(first['x']), atol=3e-15)
                    self.assertAlmostEqual(second['affine'], first['affine'], places=14)
                    self.assertAlmostEqual(second['energy'], first['energy'], places=14)

    def test_mixed_node_geometry_rejected_before_readout(self):
        data = self.data([0., 1.])
        for snapshot in data:
            snapshot['nodes'] = [{'gamma': snapshot['gamma']}]
        untouched = copy.deepcopy(data)
        build_geodesics(data)
        self.assertEqual(data, untouched)
        data[1]['nodes'].append({'gamma': self.gamma0.tolist()})
        with self.assertRaisesRegex(ValueError, 'share the declared homogeneous metric'):
            build_geodesics(data)

    def test_null_momentum_rescaling_changes_affine_scale_not_path(self):
        data = self.data([0., .2, 1.])
        first = integrate_path(data, self.p, kind='null')
        second = integrate_path(data, 7*self.p, kind='null')
        for u, v in zip(first['points'], second['points']):
            np.testing.assert_allclose(u['x'], v['x'], atol=3e-15)
            self.assertAlmostEqual(u['affine'], 7*v['affine'], places=14)
            self.assertAlmostEqual(7*u['energy'], v['energy'], places=14)


class SavedReportBoundaryReview(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import tempfile
        from pathlib import Path
        from .run import run
        cls.directory = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.directory.cleanup)
        cls.report = run(Path(cls.directory.name)/'one-run', steps=1)

    def test_complete_report_passes_without_mutation(self):
        from .board import validate_report
        report = copy.deepcopy(self.report)
        validate_report(report)
        self.assertEqual(report, self.report)

    def test_mixed_run_or_tensor_identity_rejected(self):
        from .board import validate_report
        for section, key in (('metadata', 'tensor_sha256'),
                             ('provenance', 'tensor_sha256'),
                             ('provenance', 'run_id'),
                             ('provenance', 'bundle_id'),
                             ('provenance', 'trace_sha256')):
            with self.subTest(section=section, key=key):
                report = copy.deepcopy(self.report)
                report[section][key] = '0'*64
                with self.assertRaises(ValueError):
                    validate_report(report)

    def test_stale_path_and_incomplete_snapshot_rejected(self):
        from .board import validate_report
        report = copy.deepcopy(self.report)
        report['geodesics']['paths'][0]['points'][-1]['x'][0] += .01
        with self.assertRaises(ValueError):
            validate_report(report)
        report = copy.deepcopy(self.report)
        report['snapshots'].pop()
        with self.assertRaises(ValueError):
            validate_report(report)

    def test_schema_or_physics_promotion_rejected(self):
        from .board import validate_report
        report = copy.deepcopy(self.report)
        report['schema'] = 'future-unverified-schema'
        with self.assertRaises(ValueError):
            validate_report(report)
        for gate in ('exact_discrete_Einstein_constraints', 'general_Einstein_convergence',
                     'Born_Bell_quantum_dynamics'):
            with self.subTest(gate=gate):
                report = copy.deepcopy(self.report)
                report['acceptance_gates'][gate] = 'passed'
                with self.assertRaises(ValueError):
                    validate_report(report)


if __name__ == '__main__':
    unittest.main()
