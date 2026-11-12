# Independent review: sourced Einstein subcase and complete-history boundaries

Reviewer 8 of the issue #58 construction. Baseline:
`f4f64e062f07b3ca119eccf655df746be206908b`.
The reviewed positive construction is a spatially flat, homogeneous,
isotropic, expanding **massless scalar plus positive pressureless dust**
solution. It has a genuine Einstein interpretation in that stated sector.
It is neither the old massive45 discrete trajectory nor a general spatial
Einstein model.

Reproduce the independent review with:

```bash
python -m validation.sourced_map.review
```

The source-hashed result is `runs/sourced-map/review.json`. Only the existing
Engine evolves retained state. No metric calculation, physical decoder,
reference integrator or review check feeds it.

## Independent derivation of all Einstein components

The review starts with the metric alone,

\[
g_{\mu\nu}=\operatorname{diag}(-1,a(\tau)^2,a(\tau)^2,a(\tau)^2),
\]

and computes its Christoffel symbols, Ricci tensor, scalar curvature and
Einstein tensor. It does not import a Friedmann equation or the production
frame right-hand side into that computation. With signature `-+++`,
`c=8*pi*G=1` and zero cosmological constant, it obtains

\[
G_{00}=3\dot a^2/a^2,\qquad
G_{ii}=-2a\ddot a-\dot a^2,
\]

with all twelve off-diagonal components zero. Substituting

\[
a=V^{1/3},\quad \dot V=U,\quad \dot U=3D/2,
\quad p=P/V,\quad \rho_d=D/V
\]

and independently specifying the massless-scalar/dust stress gives

\[
\rho=P^2/(2V^2)+D/V,\qquad p_{\rm pressure}=P^2/(2V^2).
\]

Every nontrivial residual is then controlled by the same exact invariant:

\[
G_{00}-T_{00}=\frac{Q}{3V^2},\qquad
\frac{G_{ii}-T_{ii}}{a^2}=\frac{Q}{3V^2},\qquad
Q=U^2-3DV-\tfrac32P^2.
\]

All off-diagonal residuals vanish identically. Thus `Q=0` is sufficient for
**all 16 Einstein components in this homogeneous isotropic sector**, rather
than merely for a scalar bookkeeping identity. The review separately verifies
massless Klein–Gordon, dust continuity and total stress conservation.

This does not establish a new cosmological solution. It establishes that the
new integer history map samples this known sourced Einstein solution exactly,
at the declared proper times, for its admitted initial-data chart. Analytic
interpolation by the exact volume flow is part of this restricted physical
interpretation; it is not a runtime callback.

## Actual Engine states satisfy the same equations

At `N=24` and `N=48`, the review runs the actual six-channel tensor for three
and six steps, respectively. Each step is checked against the separate scalar
Rule3 oracle, every immediate inverse, all retained carries, and the exact
Einstein residuals derived above. Both runs end at the same proper time
`1/8`, with

```text
V=355/256, U=51/16, P=2, D=1, Q=0.
```

The decoded scalar phase is also compared with an independent 80-digit
quadrature of `2/(1+3*t+3*t²/4)` over the proper-time interval. It agrees to
better than `1e-70`. This checks the scalar coordinate map against an integral
that does not use its stored velocity-anchor formula. Full rewinds pass.

The source response has the correct interpretation. Dust supplies the actual
volume acceleration in the tensor. Scalar momentum supplies a conserved
source term in the constrained integration constant; changing it while keeping
all `V,U,D` fixed generally moves the state off `Q=0`. Its absence from the constant
volume-acceleration term is therefore not evidence that scalar stress is
missing. It also does not establish a local spatial scalar–gravity interaction.

The complete history matters: `J=b_W-a_W+3D` carries the physical expansion
velocity. The integer invariant is `I=16N²Q`, not a constraint separately
imposed on each stored volume. The six channels retain 18 integers per node;
the scalar reference velocity, scalar offset and coordinate counter are
included in that count. All six legal carry values remain retained.

## Adversarial physical controls

- Moving both stored volume histories by one leaves the native integer
  constraint at `I=-12` for all four tested states. It is not projected back
  to zero. The physical decoder rejects each state because its exact Einstein
  constraint is nonzero.
- Deleting the actual `18D` volume input, with the same complete source seed,
  gives `I=-3420` after one step. The altered mechanical law still rewinds.
  Thus the positive Einstein result depends on the actual source coupling.
- Rewinding the positive seed by 96 ticks at `N=24` reaches proper time `-4`
  with `V=1,U=-3` and preserved `I=0`; running forward returns the entire seed.
  Both volume endpoints are positive, but the intervening volume minimum is
  `-2`. The interval crosses two zero-volume singularities. The whole-interval
  validator and expanding-chart decoder reject its physical continuation.
  Mechanical invertibility is not a cosmological bounce proof.
- Relabelling the decoder or saved model as massive is rejected. For nonzero
  mass, `Pdot=-mu*phi*V`; the present frozen `P` law cannot satisfy that equation.
- Changing only the coordinate counter does not change `B,k,p,phi,d`. The
  physical fields are read from the current retained geometry/source coordinates,
  not reconstructed from a precomputed trajectory indexed by ticks.
- A changed carry seed has a different bundle identity even though this
  carry-transparent law gives the same physical readout. Physical equivalence
  does not erase complete-state provenance.

## Review findings corrected before final validation

The initial passive logarithm evaluation subtracted
`U-sqrt(3P²/2)` directly. Valid arbitrarily large integer data can lie extremely
close to that branch root. The reviewer constructed the Pell family
`x²-6y²=1`, with `V=1/3,U=Uref=x,D=1,P=2y`. A 90-digit `x` passed the exact
domain check but raised `ZeroDivisionError` at the requested 80-digit display
precision.

The decoder now evaluates the anchored logarithm using exact rational branch
products and velocity differences, followed by a stable `log1p` expression.
The review verifies both the zero-phase anchor and a **nonzero actual Engine
step** from this near-root family, at `N=24x`. The step still inverts exactly;
the 80-digit scalar phase agrees with an independently evaluated 400-digit
direct logarithm to better than `1e-70`. This repair changes passive numerical
evaluation only, not any retained state or symbolic physical identity.

The runtime audit also initially assumed the counter started at zero even
though its bundle constructor accepted a shifted coordinate origin. It now
checks `tau=initial_tau+step/N`. Its separate saved-run audit includes an
origin shift of ten ticks, with unchanged physical fields. The resolution
comparison now rejects equal `N`, so it cannot label an identical run as a
different-resolution comparison. These fixes were reviewed at the source
boundary; their saved-run execution belongs to the runtime work package.

## Original failures remain failures

The reviewer independently expands the original massive constrained seed's
Euler update and recovers `C_after=-7h²`. The existing five-channel reduced
history audit is rerun: its first-step constraint is zero, but its second-step
constraint is exactly nonzero. Those results remain attached to their original
laws. The positive six-channel massless construction changes physical
coordinates and the discrete evolution; it does not relabel those failed
trajectories as successes.

The massive alternatives retain their separate status. Exact invertibility of
Kahan or a rational symmetric splitting does not imply exact Einstein
constraint preservation. The implicit-midpoint quadratic-invariant identity
does not provide a permitted exact rational Engine update when its selected
solution requires an irreducible algebraic root. None is promoted by the
restricted massless result.

## Accepted scope

No remaining blocking mathematical error was found in the declared positive
construction. Its supported physical statement is exact sampling of the
spatially flat, homogeneous, isotropic, expanding massless-scalar plus positive-
dust Einstein solution on its valid complete-history and representability
domain. The roots and logarithm are passive analytical readouts, evaluated
numerically for display. They are not fundamental integer operations.

Spatial gradients, anisotropy, the massive scalar, general Einstein dynamics,
operational material clocks and detector records remain unestablished. The
generic runtime's physical gates remain unpromoted. These limits are part of
the result, not consequences erased by the successful restricted proof.
