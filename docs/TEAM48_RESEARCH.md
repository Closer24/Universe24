# Compact sourced geometry within a 48-channel budget

Status: research construction, not a replacement for the default ADM event
board. Seven AI reviewers (one integrator and six specialists) developed and
cross-checked the algebra, integer encoding, geometry, sources, constraints,
numerics and invariant subflows. Their shared discussion is
[issue #17](https://github.com/Closer24/Universe24/issues/17).

The useful result is an actual fixed-six **41-channel charged scalar,
Maxwell and nonnegative normal-dust candidate**, with one geometric frame,
and a separately tested **44-channel positive-frame variant**.
The main unsolved problem is a stable, refinable integer evolution with
controlled Einstein and matter-constraint errors. The channel count alone
does not settle that problem. Discretization error is allowed; a controlled
refinement family is still required to distinguish it from an encoding or
stability failure.

## Git review and reuse

The investigation started on main `7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2`.
A fresh remote review found [PR #39](https://github.com/Closer24/Universe24/pull/39)
at `35344a1ba5c12c857404115e893911411ece7d35`. Its signed dust amplitude
`d`, density `rho_d=d*d`, and equation `dot(d)=tr(K)*d/2` solve the negative
density encoding problem without clipping or an additional field. All 35
continuum RHS components and the shared source/constraints agree with our
adapter after explicit field renaming. The 14 new upstream tests, 10 existing
Frame48 tests and two fixed-six guards passed in an isolated review checkout.

The **70-to-36 compression is exact for physical trajectories**, including
both time slices, all four phase sectors, arbitrary retained remainders and
large integers. The 70- and 36-channel complete storage arrays differ; each
has its own exact inverse. This is not a claim of byte-identical state.
The 20-field triangular gauge is a further representation change, not an
arbitrary-field identity with the Fermi-frame trajectory.

PR #38 supplies independent physics-gap audits, not a smaller Einstein
solver. The other remote branches inspected were already ancestors of main.
No complexity/detector experiment is silently added to gravitational stress.

## Actual allocation

`python -m experiments.geometry.team48.candidate` constructs the tensors and
writes named addresses to `runs/team48/candidate/channels.json`.

| Retained content | Scalar/dust | Independent Maxwell | Charged scalar/Maxwell |
| --- | ---: | ---: | ---: |
| Upper-triangular inverse triad | 6 | 6 | 6 |
| Symmetric extrinsic curvature | 6 | 6 | 6 |
| Spatial frame connection | 8 | 8 | 8 |
| Two real scalar fields, momenta and gradients | 10 | 10 | 10 |
| Signed dust amplitude | 1 | 1 | 1 |
| Electric and magnetic fields | 0 | 6 | 6 |
| Spatial electromagnetic potential | 0 | 0 | 3 |
| Computational sign phase | 1 | 1 | 1 |
| **Actual channels** | **32** | **38** | **41** |
| Unallocated capacity below 48 | 16 | 10 | 7 |
| Monomials at mass=Lambda=0, dt=dx=1 | 322 | 432 | 465 |

There is no padding or channel aliasing. Each channel retains `(a,b,r)`, so
41 channels mean 123 integer entries per node, not 41 bits. Integer bit
lengths and exported history can grow. The communication/reference block is
not included in these counts. The default one-step system still has 4,825
channels; the original 48-channel reference is a different construction.

## Why a single sign channel removes the second bank

For a quadratic local field equation `dot(y)=f2(y)+f1(y)+f0`, the leapfrog is

`y[n+1]=y[n-1]+2*h*f(y[n])`.

Use signs `s=(1,1,-1,-1,...)`, encode `z[n]=s[n]*y[n]`, and retain
`a_clock=s[n]`, `b_clock=s[n+1]`, with `u_clock=0`. For a physical field set

`u_z=6*h*b_clock*(f2(z)+a_clock*f1(z)+f0)`.

The unchanged Rule3 gives exactly the encoded leapfrog. Quadratic terms have
three inputs including the phase; linear terms have two phase inputs and
one field. The only old-a dependency is the phase, so staged inversion is
acyclic. All fields and neighbors share a prepared phase. Nonuniform phase
preparation is rejected; this is not autonomous asynchronous scheduling.
The sign channel is computational and is not an operational proper clock.

Every coefficient of `2*h*f` must be integral. The compiler rejects unsupported
fractions; it does not round them or change the Engine divisor. Thus this
encoding preserves the numerical integrator's failures as well as its successes.

## The compiled 44-channel positive-frame variant

`build('charged_positive')` replaces each diagonal B component with two
amplitudes, `B_aa=p_a²+q_a²`, both obeying `dot p=K_aa*p/2` and
`dot q=K_aa*q/2`. It uses **23 geometry + 10 scalar + 1 dust + 6 Maxwell +
3 potential + 1 phase = 44 channels**, or 132 retained integer entries per
node. Four channel slots remain unallocated. The actual tensor has 585
monomials at mass_squared=0, or 593 at mass_squared=1; dt=dx=coupling=1.

This cubic field system needs a different sign encoding. Each field has
phase offset delta=0 or 1, selecting clock.a or clock.b. For every cubic
monomial, `delta_target+sum(delta_inputs)=1 mod 2` cancels the phase factors;
quadratic terms retain one phase factor. The compiler checks every term and
rejects incompatible cubic laws. K/Gamma, Pi/Xi and E/M use opposite offsets.
This preserves maximum input degree three and strict single-face support.

The discrete pair area `W=p_now*q_previous-q_now*p_previous` flips sign
exactly under the common two-level recurrence. Nonzero W therefore prevents
both amplitudes vanishing. All three positive diagonals imply `det(B)>0`.
This is an exact prepared-domain invariant, not a post-step repair. All four
phase sectors, arbitrary nonzero carries, independent scalar/RHS oracles,
complete rewind and trace replay were checked in the actual Engine.

**The physical limitation is essential:** exact continuum auxiliary histories
keep q/p constant, so two such slices have W=0. The protecting W!=0 seed
therefore introduces a computational temporal mode. In a contracting
constant-K control it can eventually grow instead of following the intended
decay. A separate fixed-time refinement control can suppress it, but no
compatible integer refinement family for the full sourced candidate exists
yet. This variant changes the discrete physical map; it is not the same
trajectory as the 41-channel B-variable update.

The independent L=4 squared-dust fixture starts with nonzero momentum and all
literal constraints zero on each slice. Its first integer update has H=2624,
M0=144 and torsion=4 while det(B) stays positive. Smaller joint steps 1/2,
1/4 and 1/8 fail raw integer coefficient checks. These are open physical
gates, not discarded outcomes. Constraints difference the **reconstructed
diagonal**: substituting `2*p*D(p)+2*q*D(q)` for `D(p²+q²)` would hide a
discrete product-rule defect. A regression exposes that incorrect substitution.

## Geometry and matter are genuinely coupled

The triangular gauge uses `Omega_ab=sign(b-a)*K_ab`. It preserves the three
zero lower-triangular B components without division. One connection relation
`Gamma_021=Gamma_012` is invariant, leaving eight components. Four independent
general-spatial coordinate-jet oracles compare frame Ricci and connection
evolution with a metric/Christoffel construction. The rotation is also applied
to matter vectors, including covariant scalar gradients and the potential.

There is one contravariant spatial metric `gamma_inverse=B.T*B`. The existing
nondegeneracy gate still matters for its inverse. Generic covariant metric
ratios in the frame experiments remain diagnostic oracles, not a new general
rational readout theorem. Synchronous gauge has lapse one and shift zero and
is only a local chart before normal-congruence caustics.

In the charged model, store `Xi_a=D_a Phi` rather than ordinary scalar
gradients. With `J(phi,chi)=(-chi,phi)`,
`D_mu Phi=partial_mu Phi-g*A_mu*J(Phi)` and temporal potential zero, all source
and evolution terms remain quadratic before the sign encoding. The three
stored `A0,A1,A2` names are spatial frame components. They are not a retained
time potential. Maxwell's equations use the scalar current, and their stress
and Poynting momentum source the same geometry.

Independent audits verify combined continuum energy and momentum balance,
electric-charge continuity, local spatial U(1) gauge covariance, and charge
conjugation. Actual integer runs verify current-to-electric-field response,
the conjugate trajectory and complete inversion. Normal dust is neutral,
comoving and single-stream; it is not a tilted fluid or collisionless dark
matter solver. Charged classical scalar matter is not Dirac matter, quantum
antiparticles, a Born rule or annihilation physics.

## What the physical tests actually show

| Check | Finding | Limit |
| --- | --- | --- |
| Exact #39 compression | Same 35 fields on both slices, 70 to 36 channels | Does not improve its physical integrator |
| Sourced continuum identities | Correct stress, flux, gauge and geometric equations | Continuum product identities need not hold for centered differences |
| Charged constrained initial slice | Every reported constraint initially zero; rho=5 and current_y=-4 | Repeated starting slices are explicitly not an exact temporal history |
| Next integer charged step | Electric field responds; H becomes -314 at dt=1 | Coarse-step failure, not a proof of nonconvergence |
| Earlier raw-density 32/38 runs | Nonzero momentum and all initial sampled constraints zero; subsequent drift | They use raw rho, not the later square encoding; histories are not relabeled |
| Formal time refinement | Same-seed first-step H decreases as 156086*h^2; momentum error also decreases | Exact Fraction reference, not an accessible integer refinement family |
| Spatial constraint tangent | At fixed dx=1, initial semidiscrete momentum-constraint derivative has peak 21 | Time refinement alone cannot make that discrete constraint surface invariant |
| Exact Milne initial time pair | Old leapfrog reaches B00=0 at t=2 while H/M remain zero | Shows why constraints and metric validity need separate checks |
| Floating Milne refinement | Smaller steps remove that degeneracy and converge on a fixed interval | Raw integer coefficients/seeds do not realize the fine family |

Preservation of H/M is not generic conservation of a scalar matter energy.
The relevant continuum local balance includes energy flux, stress and work
by the geometry. All supplied matter terms are included in this balance.

## Constructive controls and remaining arithmetic work

- A seven-channel linearized sourced translation preserves H, M and its
  gradient constraint for 20 actual Engine updates. Freezing the source
  evolution breaks them. Its periodic density is a signed zero-mean
  perturbation, not positive nonlinear matter.
- A three-channel projective Milne sector uses `u=6*b`, prepared
  `D[n]=2*S+n`, `P=C=1`, and passive `B00=C*S/D`, `K00=-P*S/D`. With
  `t=D/(P*S)`, the same tensor supports S=1,2,4,16,64,256. The exact frame
  equations and an independent four-dimensional Ricci calculation pass.
  This proves this restricted readout, not arbitrary dynamic ratios.
- A six-channel Lorentz null rotation preserves a mass shell and supports
  weighted refinement. It is a kinematic control, not sourced gravity.
- The one-channel `u=10*b` divider has exact coordinates
  `e=r/2`, `z=(3*a-b-e)/2`, `w=(3*b-a+e)/2`, with
  `z_next=floor(z/3)` and `w_next=3*w-e`. Discarded digits remain in the
  reversible state. The tensor cannot directly read r; autonomous quotient
  handoff into a reusable field update is still missing.
- Naive damping added to leapfrog has an unstable root for every positive
  damping rate. Adding four Z4 fields alone does not fix this integrator.

These are constructive pieces, not a claim that no solution can exist.
The next acceptance experiment needs the same physical initial problem at
increasing integer resolution, a fixed physical interval, independently
measured H/M and matter constraints, a valid metric and a decreasing error.
A compatible spatial flux law and suppression of the leapfrog computational
mode must be included, rather than inferred from exact reversibility.

## Reproduction and source boundaries

The shared runner, `python -m experiments.geometry.team48.run_audits`, executes
the isolated checks and saves fresh reports under `runs/team48`. The lightweight
regressions are `python -m unittest universe24.tests.test_team48 -v`.
Each earlier frame/FLRW report retains its original source pin. New source
and artifact hashes accompany the aggregate evidence; raw traces remain
available from the reproducible runner and CI artifact.

The detailed derivations and primary-source ledgers are in
[geometry notes](../experiments/geometry/team48/geometry_notes.md),
[matter report](../experiments/geometry/team48/matter_report.md),
[integer proof](../experiments/geometry/team48/integer_RESEARCH.md),
[constraint findings](../experiments/geometry/team48/constraints_findings.md),
and [variational routes](../experiments/geometry/team48/variational_routes.md).
The external literature supplies formulations and methods; the compact
encoding, squared-dust comparison and actual Engine gates are checked here.
No external hyperbolicity, stability or full-GR theorem is inherited.
