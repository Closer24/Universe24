"""Passive geodesics of the homogeneous metric reconstructed from one run.

No Engine, seed mutation or retained probe lives here. Floating arithmetic is
confined to this declared observation layer. The metric is piecewise linear in
time, with lapse one and shift zero; spatial homogeneity is required, not guessed.
"""
from __future__ import annotations

import math
from typing import Sequence

import numpy as np


def _metric(value):
    gamma = np.asarray(value, dtype=float)
    if gamma.shape != (3, 3) or not np.all(np.isfinite(gamma)):
        raise ValueError('The spatial metric must be a finite 3 by 3 matrix')
    if not np.allclose(gamma, gamma.T, rtol=0, atol=1e-12):
        raise ValueError('The spatial metric must be symmetric')
    try:
        np.linalg.cholesky(gamma)
    except np.linalg.LinAlgError as error:
        raise ValueError('The spatial metric must be positive definite') from error
    return gamma


def _snapshots(snapshots):
    if len(snapshots) < 2:
        raise ValueError('At least two saved metric snapshots are required')
    result = []
    for item in snapshots:
        if item.get('homogeneous') is not True:
            raise ValueError('This geodesic readout requires declared spatial homogeneity')
        t = float(item['time'])
        if not math.isfinite(t) or (result and t <= result[-1][0]):
            raise ValueError('Snapshot times must be finite and strictly increasing')
        gamma = _metric(item['gamma'])
        for node in item.get('nodes', []):
            if not np.array_equal(_metric(node['gamma']), gamma):
                raise ValueError('The nodes do not share the declared homogeneous metric')
        result.append((t, gamma))
    return result


def _tangent(gamma, momentum, epsilon):
    raised = np.linalg.solve(gamma, momentum)
    energy = math.sqrt(epsilon + float(momentum @ raised))
    velocity = raised / energy
    # u^mu = (E, gamma^-1 p); null affine scale is set by supplied p_i.
    norm_error = abs(-energy*energy + float(raised @ gamma @ raised) + epsilon)
    return velocity, 1.0/energy, energy, norm_error


def integrate_path(snapshots: Sequence[dict], momentum=(1., 0., 0.), *,
                   kind='timelike', substeps=32, initial_position=(0., 0., 0.)):
    """Integrate Killing-momentum geodesics of the interpolated saved metric.

    p_i = gamma_ij dx^j/dlambda is constant by translation symmetry.
    E = dt/dlambda = sqrt(epsilon + gamma^ij p_i p_j), epsilon in {0,1}.
    Thus dx^i/dt = gamma^ij p_j / E and dlambda/dt = 1/E. For a unit
    timelike tangent lambda is proper time; for null paths it is affine time.
    Composite midpoint integration has second order *readout* accuracy.
    """
    data = _snapshots(snapshots)
    if kind not in ('timelike', 'null'):
        raise ValueError('kind must be timelike or null')
    if type(substeps) is not int or substeps < 1:
        raise ValueError('substeps must be a positive integer')
    p = np.asarray(momentum, dtype=float)
    x = np.asarray(initial_position, dtype=float).copy()
    if p.shape != (3,) or x.shape != (3,) or not np.all(np.isfinite(p)) or not np.all(np.isfinite(x)):
        raise ValueError('Momentum and position must be finite three-vectors')
    if kind == 'null' and not np.any(p):
        raise ValueError('A null path requires nonzero covariant momentum')
    epsilon, affine = int(kind == 'timelike'), 0.0
    points = []

    def append(t, gamma):
        velocity, _, energy, norm_error = _tangent(gamma, p, epsilon)
        points.append({'t': float(t), 'x': x.tolist(),
                       'tau': affine if epsilon else None, 'affine': affine,
                       'energy': energy, 'velocity': velocity.tolist(),
                       'normalization_error': norm_error})

    append(*data[0])
    for (t0, g0), (t1, g1) in zip(data, data[1:]):
        step = (t1-t0)/substeps
        for j in range(substeps):
            weight = (j+0.5)/substeps
            gamma = (1-weight)*g0 + weight*g1
            velocity, rate, _, _ = _tangent(gamma, p, epsilon)
            x += step*velocity
            affine += step*rate
        append(t1, g1)
    return {'kind': kind, 'covariant_momentum': p.tolist(), 'points': points,
            'max_normalization_error': max(p['normalization_error'] for p in points)}


def build_geodesics(snapshots, *, substeps=32):
    definitions = (
        ('null_plus_x', 'Light +x', 'null', (1, 0, 0)),
        ('null_minus_x', 'Light -x', 'null', (-1, 0, 0)),
        ('null_plus_y', 'Light +y', 'null', (0, 1, 0)),
        ('massive_x', 'Freely falling massive probe', 'timelike', (1, 0, 0)),
        ('comoving', 'Comoving proper time', 'timelike', (0, 0, 0)),
    )
    paths = []
    refinements = []
    for identity, name, kind, momentum in definitions:
        path = integrate_path(snapshots, momentum, kind=kind, substeps=substeps)
        path.update(id=identity, name=name)
        paths.append(path)
        fine = integrate_path(snapshots, momentum, kind=kind, substeps=2*substeps)
        coarse = integrate_path(snapshots, momentum, kind=kind, substeps=max(1, substeps//2))
        difference = lambda a, b: float(np.linalg.norm(np.array(a['points'][-1]['x'])-np.array(b['points'][-1]['x'])))
        refinements.append({'id': identity, 'coarse_to_medium_endpoint': difference(coarse, path),
                            'medium_to_fine_endpoint': difference(path, fine),
                            'fine_affine_difference': abs(path['points'][-1]['affine']-fine['points'][-1]['affine'])})
    return {'schema': 'universe24.passive-homogeneous-geodesics.v1',
            'metric_authority': 'saved run gamma; lapse=1; shift=0',
            'method': 'translation Killing momenta; piecewise-linear gamma; composite midpoint quadrature',
            'scope': 'Passive test-particle trajectories of the reconstructed metric; not retained Engine apparatus or proof of Einstein convergence.',
            'substeps_per_saved_interval': substeps,
            'paths': paths, 'quadrature_refinement': refinements,
            'normalization_max_error': max(p['max_normalization_error'] for p in paths),
            'retained_probe_channels': 0,
            'retained_probe_dynamics': 'not_implemented'}
