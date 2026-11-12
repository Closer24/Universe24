# Independent integration review

The reviewed path is a 45-channel exact integer run through the existing
bundle/Engine/runtime, followed by passive reconstruction of its spatial metric
and homogeneous timelike/null geodesics. No retained probe, second metric or
quantum model is introduced by this display. This review supports that scoped
integration, not general Einstein or quantum acceptance.

## Independent equations and tests

For a spatially homogeneous metric `g00=-1`, `g0i=0`, `gij=gamma_ij(t)`, the
nonzero connection components are

- `Gamma^0_ij = dot(gamma)_ij / 2`;
- `Gamma^i_0j = Gamma^i_j0 = gamma^ik dot(gamma)_kj / 2`.

`test_full_christoffel_equation_not_only_tangent_normalization` independently
constructs these four-dimensional Christoffel symbols. On a non-diagonal,
anisotropic metric with noncommuting `gamma` and `dot(gamma)`, it checks
`du^mu/dlambda + Gamma^mu_ab u^a u^b = 0` for both timelike and null paths.
The finite-difference residual is below `2e-10` in the selected control. This
is stronger than checking tangent normalization alone, which any normalized
curve could satisfy.

Additional review controls establish:

1. A constant spatial change of coordinates `x'=A x` transforms an evolving
   metric and its paths covariantly and preserves proper/affine time.
2. Positive rescaling of null momentum changes affine normalization but leaves
   the spacetime path unchanged.
3. A forged heterogeneous node metric is rejected before path reconstruction;
   the unmodified homogeneous input remains unchanged by the observer.

Run:

```bash
python -m unittest validation.geodesic_board.test_geodesics \
  validation.geodesic_board.test_integration_review -v
```

All fourteen tests passed during this review: six author controls, four independent
geodesic controls and four independent report-boundary tests. The quadrature tests concern the interpolated metric readout;
they are not a spatial/time convergence test for Einstein evolution.

## Actual Engine checkpoint

The shared default builder has 45 retained channels and 889 monomials. The
reviewed tensor fingerprint is
`fbbf8f9b4128563e786ff0b57069fe18320698451c0ac9acb0c947c568cfc617`.
The default seed uses every carry class. Its first Engine update and exact
inverse were rerun independently. Both the passive full-frame diagnostic and
the separately derived homogeneous constraint return exactly `-7/1024` for
`dt=1/32`, starting from zero constraint. This confirms that the visible failure
is not hidden by the integration or a massless-law substitution.

## Review corrections and boundary

The initial board read the wrong key for exact replay status; the board author
corrected it to the saved report's execution gate. A `+y` null path was initially
drawn in an `x-t` section labeled `y=z=0`; the board author now excludes paths
leaving that section while preserving them in the underlying report.

The standalone JSON renderer now rejects unsupported schemas, mixed
run/bundle/tensor/trace identities, missing snapshots, stale geodesic paths and
unreviewed promotion of physical status. The four report-boundary tests exercise
these cases using a real one-step saved run. It remains a passive presentation
boundary: self-consistent JSON is not a new physics certification or proof of a
historical execution. Verification must use the saved full trace through
`python -m universe24 verify`. Reconstructing geodesics from a
metric does not establish that the metric solves Einstein's equations, that
actual retained matter follows those paths, or that arithmetic clicks satisfy
quantum measurement laws.

## Primary reference

F. H. Vincent, E. Gourgoulhon and J. Novak, *3+1 geodesic equation and images in
numerical spacetimes*, Class. Quantum Grav. 29, 245005 (2012),
[arXiv:1208.3927](https://arxiv.org/abs/1208.3927). This is the general numerical
spacetime geodesic framework; the elementary homogeneous connection above and
its independent executable controls were derived for this review.
