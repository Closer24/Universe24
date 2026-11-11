# Independent fixed-domain projective validation

The new projective compiler has been exercised in the **actual fixed-six
Engine**, with 41 total channels, 506 degree-two monomials, nonzero retained
remainders, strict single-face support, and exact complete rewind. This
removes the previous raw-coefficient obstruction for this tested smooth
inhomogeneous Einstein–scalar–dust family. It does **not** establish general
constraint preservation or a long-time stable Einstein solver.

Run:

```bash
python -m validation.geometry.team48.validation_repair_projective
```

Fresh data, source hashes, tensor hashes, binary complete-seed/final hashes,
and every positive and negative group are written to
`runs/team48/validation_repair/projective_validation.json`.

## Problem and independent oracle

The physical domain is the periodic interval `[0,1)` with transverse
homogeneity; the actual Engine nevertheless runs all `n^3` nodes. Final
physical time is always `1/16`. Initial data are

`B=I`, `K=diag(0,k,k)`, `phi=sin(2*pi*x)/16`, `Pi_phi=2`,
`Xi_phi0=D_dx(phi)`, `k=2+phi`, and
`rho_d=k^2-(4+Xi_phi0^2)/2>0`.

These satisfy the flat-slice Hamiltonian and momentum constraints. The
finite-difference version satisfies momentum and scalar-gradient constraints
exactly after quantizing `phi`. All retained seed numerators are integers.
The common denominator is `Q=2^24`; `phi` is prepared by exact rational Taylor
arithmetic, and the dust amplitude by an integer square root. The latter
introduces a disclosed positive initial Hamiltonian residual no greater than
`3.08e-7` in these runs. No square root, rounding or correction occurs during
evolution. The denominator itself is a counted, dynamically retained channel.

The geometric observer reconstructs

`ds3^2=b^-2 dx^2+c^-2(dy^2+dz^2)`, `C=1/c`,
`R=-4 C''/C-2(C'/C)^2`, with prime denoting `b*d/dx`.

It computes literal metric Hamiltonian/momentum constraints without calling
the production connection, curvature, stress or constraint routines. A
separate planar Einstein/matter RHS verifies the first exact Euler readout
and the subsequent physical trajectory. Floating arithmetic is restricted
to these passive diagnostics and the independent reference, never the seed
or Engine.

## Results and retained failures

The additional four/six/eight-update family gives:

| Spatial nodes | Step | H infinity norm | M infinity norm | Scalar gradient defect | Connection/metric defect | Field error vs independent RK4 |
|---:|---:|---:|---:|---:|---:|---:|
| 8 | 1/64 | 0.0881762 | 0.00512618 | 1.02866e-5 | 0.000849974 | 0.0817920 |
| 12 | 1/96 | 0.0678572 | 0.00327291 | 1.02096e-5 | 0.000625571 | 0.0492867 |
| 16 | 1/128 | 0.0533736 | 0.00230916 | 9.00453e-6 | 0.000488608 | 0.0347661 |

The independent RK4 reference uses 384 spatial nodes and 1024 updates; its
nested comparison with 192 nodes and 512 updates differs by `2.27e-5` in the
maximum field norm, substantially below these coarse-run errors. This is a
reference consistency check, not an exact continuum solution or stability
theorem.

The acceptance rule was strict decrease of **all four unscaled** final
constraint/compatibility residuals. Results that fail it remain in the JSON:

| Refinement group | Result |
|---|---|
| Time only, n=8, h=1/32,1/64,1/128 | All four decline; momentum approaches a spatial-error floor |
| Space only, h=1/128, n=4,8,16 | All-four gate fails |
| Original joint n=4,8,16 with 2,4,8 updates | All-four gate fails |
| Better resolved joint n=8,12,16 with 2,4,8 updates | H/M/connection decline; gradient gate fails |
| Additional joint n=8,12,16 with 4,6,8 updates | All four decline; independently measured field error also declines |

The last group was an **explicit protocol extension after observing earlier
failures**, motivated by the first Euler step's exactly zero gradient defect
and the two-update run's possible temporal underresolution. It is not an
independent preregistered confirmation, and no prior row was discarded.

The separate seed-quantization study holds n=8, h=1/64, T=1/16 fixed:

| Q | Initial H infinity norm | Final H infinity norm |
|---:|---:|---:|
| 16 | 0.3125 | 0.562660 |
| 256 | 0.0162659 | 0.0866099 |
| 4096 | 0.000701904 | 0.0870188 |
| 16777216 | 3.07853e-7 | 0.0881762 |

Increasing integer precision suppresses initial quantization error; it does
not remove the fixed time/space discretization error. Final H is consequently
not monotone in Q and is not presented as such.

Metric diagonals and dust density stay positive in every tested trajectory.
No general nondegeneracy theorem follows. The charged/Maxwell fields are
present in the 41-channel law but zero in this neutral real-scalar fixture;
this report does not validate their active dynamics or physical apparatus.

The largest retained integer reaches **8186 bits after eight updates**.
Its growth is exponential in the number of updates, an important practical
limitation rather than an omitted state cost. There is no bounded-memory or
long-time claim.

## Primary sources and scope

- Gourgoulhon, *3+1 Formalism and Bases of Numerical Relativity*,
  [gr-qc/0703035](https://arxiv.org/abs/gr-qc/0703035), especially the constraint
  projections and propagation in section 10.3. The ADM constraints used here
  follow those definitions with `8*pi*G=1` and the repository sign convention.
- Alcubierre et al., *Toward standard testbeds for numerical relativity*,
  [gr-qc/0305023](https://arxiv.org/abs/gr-qc/0305023), motivates controlled
  periodic tests that separate discretization, initial-data and formulation
  effects. It does not validate this new projective encoding.

The independent reviewer also reran the previous 44-channel first-step
counterexample and retained `H=2624`, `M0=144`; the new encoding changes the
integrator and does not retroactively repair or relabel that trajectory.
The separately proposed five-channel pp-wave control was cross-checked for
its exact transport/rewind and symbolic Einstein/null-stress identities; its
restricted matter family and transverse chart seams remain essential limits.
