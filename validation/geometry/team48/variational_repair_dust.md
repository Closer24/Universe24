# A new exact inhomogeneous sourced control

This continuation adds one **analytic invariant-family control**, not another
supported runtime and not a repair of the general 44-channel frame update.
It demonstrates that the fixed-six law admits an integer, refinable,
inhomogeneous dust geometry with nonzero tidal curvature. It does not solve the
general constraint-propagation problem in issue #40.

## Geometry and independently checked field equations

In units `8 pi G = 1`, take smooth longitudinal profiles `A(x),B(x)` and

```
ds^2 = -dt^2 + [A(x)t^(2/3)+B(x)t^(-1/3)]^2 dx^2
              + t^(4/3)(dy^2+dz^2),
rho = 4 A / [3 t (A t+B)],    u = partial_t.
```

This is a plane-symmetric dust sector related to Szekeres class II. The script
does not trust that identification: it constructs Christoffel symbols, Ricci,
scalar curvature and all 16 Einstein components directly from the coordinate
metric. It checks `G_ab=rho u_a u_b` and all four components of `nabla_a T^ab=0`
symbolically, allowing arbitrary differentiable `A(x),B(x)`. It never calls
the production frame RHS for these expectations.

Let `tau=t^(1/3)`. The metric and source become rational:

```
g_tau,tau = -9 tau^4,
a_x = A tau^2 + B/tau,   a_y=a_z=tau^2,
K_x = -(2 A t-B)/[3t(At+B)],  K_y=K_z=-2/(3t).
```

The Hamiltonian constraint `tr(K)^2-tr(K^2)-2rho=0` is exact; momentum vanishes
in this comoving slicing. `rho sqrt(gamma)=4A/3` is conserved coordinate rest
mass. The independent Weyl component is
`C_tau,y,tau,y = 2 tau^2 B/(tau^3 A+B)`, nonzero for the tested `B=1`.
The density varies in x when `B A'-A B' != 0`. Thus the control has matter,
inhomogeneity, anisotropic expansion and nonzero tidal curvature, not just a
coordinate transform of vacuum or uniform FLRW.

The valid expanding chart is `tau>0`, `At+B>0`; positive `A` gives positive
density. The construction does not remove physical shell crossings outside
that domain. It has zero spatial exchange terms because this particular
Einstein sector is silent: each longitudinal worldline evolves independently.
It cannot be used as evidence of generic neighbor-coupled gravity.

## Four exact retained channels

Each node retains `(M,N,D,Q)`, each with its complete `(a,b,r)`. With static
positive integer calibrations `S` (time) and `C` (amplitude), decode

```
A=M/(C L^4),  B=N/(C L^4),  tau=D/S,  t=Q/S^3.
```

Every channel has `u=6b`; Q additionally has `+18 D`. The five monomials are
linear, onsite, and read only old b. The divisor remains exactly six. Hence
arbitrary valid carries remain unchanged and

```
M_next=2M-M_previous,  N_next=2N-N_previous,
D_next=2D-D_previous,
Q_next=2Q-Q_previous+6D.
```

Prepare M,N equal on both slices, D_previous=D-1, Q=D^3 and
Q_previous=(D-1)^3. Induction gives constant M,N, D advancing by one, and
Q=D^3 because `(D+1)^3-2D^3+(D-1)^3=6D`. This proves the rational observer's
meaning on this prepared family. It is not an arbitrary division primitive.

The retained Q is proper-time accounting derived from this geometry. It is
not an independent material oscillator or a click-only operational clock.
The physical time increment is `[(D+1)^3-D^3]/S^3`; uniform microticks are
uniform in coordinate tau, with lapse `3tau^2`, not uniform in proper time.

This is an analytic solution parameterization, with four parameters/counters
per node and no future answer table. Nevertheless, it is not a generic
Einstein initial-value algorithm; issue #40 must not accept it merely because
it satisfies a restricted exact solution family.

## Actual evidence

Run from the repository root:

```
python -m validation.geometry.team48.variational_repair_dust
```

The same immutable tensor is run at `S=1,2,4,8,16,32,64`, over fixed
`tau in [2,3]`, hence fixed proper time `t in [8,27]`. Both starting slices
lie inside the positive-time chart. All sampled Hamiltonian constraints are
exactly zero, density and volume stay positive, the independent scalar
fixed-six oracle agrees, and every complete state rewinds. Final observables
are identical rational numbers at every time resolution. Bit growth is
reported rather than hidden. Complete raw time-family snapshots and the
tensor are exported under `runs/team48/variational/repair_plane_dust_raw/`.

Spatial sampling separately uses `L=4,8,16,32` for the fixed C2-periodic profile
`A=2+x^2(1-x)^2`, `B=1`. At a common physical point, density is identical;
centered reconstruction of its gradient converges. This does **not** test a
general spatial-curvature stencil, since the sector has no such evolution.

Seed quantization is refined independently: replace the constant 2 by
`floor(C sqrt(2))/C`, with `C=1,4,16,64,256`, computed by integer square root
of `2C^2` during preparation. At fixed spatial/time resolution the density
converges to the independently evaluated irrational-profile target while
the Hamiltonian constraint stays exactly zero for each rational seed.
Only observer diagnostics use a decimal rendering; all fundamental state,
input evaluation and Engine arithmetic are integers.

Negative controls include: a mismatched previous Q slice remains exactly
reversible but fails the proved physical readout; the shell-crossing chart
fails explicitly; and extending `B` into the transverse coordinate,
`A=2,B=1+y^2`, produces nonzero `G_tau,y`. The last result directly falsifies
an unconstrained three-dimensional-profile generalization of this ansatz.

## Literature route and boundary

Primary sources read during this continuation:

- [Goode and Wainwright, 1982](https://doi.org/10.1103/PhysRevD.26.3315):
  Szekeres classes and their relation to FLRW. This supplies family context,
  not a theorem about this integer encoding.
- [Najera and Sussman, 2021](https://doi.org/10.1140/epjc/s10052-021-09154-0),
  section 2: Szekeres-II form and valid-domain issues. Its non-comoving model
  is broader than the comoving exact control here.
- [Kur and Glasser, 2022](https://arxiv.org/html/2202.02486v2), sections III–IV:
  the Palatini lattice uses group-valued edge holonomies and face products.
  Lorentz-gauge/symplectic preservation is not an off-the-shelf explicit
  integer update obeying our single-face monomial and channel rules.
- [Bahr and Dittrich, 2009](https://arxiv.org/abs/0909.5688): restoring the
  broken diffeomorphism symmetry motivates perfect discretizations. No
  finite 48-channel general construction is supplied by citing that program.

The constructive lesson is limited but useful: exact invariant variables and
nonlinear time coordinates can eliminate a step/denominator obstruction in
a sourced inhomogeneous sector. A generic extension must still implement
spatial transport, nonzero matter momentum, general gravitational degrees
of freedom, scalar/Maxwell couplings and independent apparatus within the
same cap. None follows from the four-channel count.
