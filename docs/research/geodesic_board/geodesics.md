# Geodesics from the same saved metric

The event board's paths are passive test-particle geodesics of the spatial metric
reconstructed from the massive corrected45 run. They are not a second evolution
law or extra retained particle channels. No path enters the Engine, changes its
seed, repairs a constraint, or supplies its metric from an analytic background.

## Domain and derivation

The first connected case is spatially homogeneous, lapse one, shift zero:

\[
 ds^2=-dt^2+\gamma_{ij}(t)dx^i dx^j.
\]

Every node's saved metric must agree. The reader rejects nonpositive, asymmetric,
nonfinite, unordered or inhomogeneous inputs. Between saved times, it uses a
convex linear interpolation of positive spatial metrics. This interpolation is
part of the readout specification; it is not claimed to satisfy the retained
extrinsic curvature equations exactly.

Spatial translation symmetry gives constant covariant momenta
\(p_i=\gamma_{ij}dx^j/d\lambda\). With \(\epsilon=1\) for a timelike path
parameterized by proper time and \(\epsilon=0\) for a null path,

\[
 E=\frac{dt}{d\lambda}=\sqrt{\epsilon+\gamma^{ij}p_i p_j},\qquad
 \frac{dx^i}{dt}=\frac{\gamma^{ij}p_j}{E},\qquad
 \frac{d\lambda}{dt}=\frac1E.
\]

The normalization is \(g_{\mu\nu}u^\mu u^\nu=-\epsilon\).
For a null path, the supplied nonzero \(p_i\) fixes the arbitrary affine scale;
`tau` is therefore null rather than mislabeled proper time. The comoving timelike
path has \(\tau=t-t_0\). General anisotropic homogeneous matrices, including
off-diagonal terms, are supported; a spatially varying metric is deliberately
outside this reader's domain.

The formulas follow directly by applying the translation Killing integrals and
normalization to the geodesic equation. Relevant primary context:
F. H. Vincent, E. Gourgoulhon and J. Novak, [3+1 geodesic equation and images in
numerical spacetimes](https://arxiv.org/abs/1208.3927), *Class. Quantum Grav.*
29 (2012) 245005. That paper describes passive null/timelike ray tracing in a
numerical spacetime; it is not a validation theorem for the Universe24 law.

## Implementation and evidence

`validation/geodesic_board/geodesics.py` integrates these rates using composite
midpoint quadrature on every saved interval. No floating-point arithmetic enters
fundamental state evolution. `build_geodesics` produces opposed x-directed light
paths, a y-directed light path, a moving massive path, and a comoving path. Every
point records time, position, energy, affine parameter, appropriate proper time,
and tangent-normalization error. The report compares 16/32/64 quadrature
substeps per saved interval by default.

Six independent analytic/domain controls are executable:

```bash
python -m unittest validation.geodesic_board.test_geodesics -v
```

- Flat light speed, massive speed and time dilation.
- Off-diagonal constant metric obtained from a declared linear coordinate change
  of Minkowski spacetime, checked in independent Cartesian coordinates.
- Expanding \(\gamma=(1+2Ht)I\): analytic null displacement and redshift;
  halving the quadrature step reduces position error by approximately four.
- The same expanding metric: analytic massive displacement and proper time.
- Readout passivity and comoving proper time.
- Rejection of unsupported metric domains, zero-momentum null paths and
  contradictory spatial homogeneity.

The expanding control is an analytic *geodesic oracle*; it is not substituted
for the board run's geometry. The board's source is the retained metric. A
reported convergence of these quadratures is solely a convergence of readout on
a fixed interpolated metric. It does not establish continuum convergence of the
Engine, exact Einstein constraint propagation, in-Engine free fall, operational
clock dynamics, or a quantum detector. Those acceptance gates remain separate.
