# Geometry and proper time of the same spinor law

This report concerns the selected `spinor_beta_mass1` candidate, not an additional
metric tensor. Its source authority is
`validation/unified_law/constrained_coordinates.py`; the coordinator's
`validation/unified_law/common.py` compiles and runs that source. This lane owns
`validation/unified_law/spatial_metric.py` and reads the resulting retained states
without feeding any data back into evolution.

Run `python -m validation.unified_law.spatial_metric`. Fresh evidence is
`runs/unified_law/05_spatial_metric.json`.

## One geometry coordinate with the original source equations

Let the isotropic inverse-frame entry be `B>0` and put `beta=log B`. The single
physical metric is

\[
 ds^2=-N^2dt^2+e^{-2\beta}(dx^2+dy^2+dz^2),\qquad
 \gamma^{ij}=e^{2\beta}\delta^{ij}.
\]

The selected source has lapse one and shift zero. The original frame equation
`dB/dtau=k B` becomes exactly `d beta/dtau=k`; no change to the Einstein source
equations is involved. The homogeneous equations for `k,phi,p,dust` contain no
`B`, so the exponential occurs only in the passive metric interpretation. There
is no runtime exponential, logarithm, clipping, inverse or state repair.

This distinction matters: the earlier `h K^2 B` modification changed the source
vector field and introduced a torsion defect. The present coordinate change
does neither in its declared homogeneous sector. It also does not replace the
projective integer time map or its bit cost.

The four spinors have the exact quadratic decoder

\[
 k=-\tfrac12(s_a^2+3s_b^2)-\tfrac1{12}(s_c^2+3s_e^2)\le0,
\]

with the scalar, scalar momentum and signed dust amplitude defined by the same
shared decoder. Its identity is
`6k^2-p^2-phi^2-2dust^2=0`. All four spinors, beta, denominator, old registers and
remainders remain retained. The physical decoder is many-to-one; no retained
state is discarded by calling different spinor states the same physical metric.

## Independent four-dimensional Einstein check

The audit constructs the metric and inverse explicitly, differentiates them,
builds every Christoffel coefficient, contracts the Ricci tensor, and forms the
four-dimensional Einstein tensor. For a homogeneous lapse, substitute

\[
 \partial_t\beta=Nk,\qquad
 \partial_t^2\beta=(\partial_tN)k+N^2\partial_\tau k.
\]

The independently obtained orthonormal components are

\[
 G_{\hat0\hat0}=3k^2,\qquad
 G_{\hati\hati}=2\partial_\tau k-3k^2,
\]

with all off-diagonal components zero. The same spinor-derived matter source is

\[
 \rho=\tfrac12(p^2+\phi^2)+d^2,\qquad
 P=\tfrac12(p^2-\phi^2).
\]

Differentiating the actual quadratic decoder along the actual cubic spinor RHS
gives, as polynomial identities,

\[
 3k^2=\rho,\quad 2\dot k-3k^2=P,\quad
 \dot\rho=3k(\rho+P),\quad \frac{d}{d\tau}d^2=3kd^2.
\]

Together with `beta_dot=k`, these prove the full continuum Einstein equations
for this homogeneous isotropic matter family. They do not assert that finite
integer time differences are exact continuum derivatives.

An independent negative control freezes beta while retaining the same nonzero
decoded scalar/dust fields. The algebraic constraint still vanishes, but the
actual frozen metric has `G00=0` and nonzero density. Its Einstein residual is
`-rho`. This prevents using an automatically vanishing algebraic constraint as
a substitute for a compatible geometric evolution.

## Domain theorem for the continuum and the actual integer trace

For every finite real beta, `det B=e^(3 beta)>0`,
`det gamma_inverse=e^(6 beta)>0`, and `det g=-e^(-6 beta)<0` in lapse one.
These statements do not depend on a numerical evaluation of the exponential;
overflow in a display cannot create or remove a metric singularity.

There is a stronger continuum future-domain result. On the exact constraint,

\[
 \dot k=\tfrac12(p^2+d^2)\ge0,
\]

while the decoder always gives `k<=0`. Thus `k0<=k(t)<=0` for `t>=0`.
The positive-definite weighted spinor norm `-k` stays bounded. The polynomial
spinor vector field therefore cannot have a finite future escape; its solution
extends to every finite future time. Integrating `beta_dot=k` gives

\[
 \beta_0+k_0t\le\beta(t)\le\beta_0.
\]

For the shared seed `sa=1,sb=sc=se=beta=0`, `k0=-1/2`, hence
`exp(-t/2)<=B(t)<=1`. This is future completeness of the coordinate ODE and a
finite-time metric lower bound, not a past-singularity or general-spacetime
theorem.

The actual degree-three projective recurrence also has an exact metric-domain
theorem. Write

\[
 D_{n+1}=C D_n^3-D_{n-1},\quad
 \epsilon_n=D_{n-1}/D_{n+1},\quad
 \beta_{n+1}=(1+\epsilon_n)(\beta_n+h k_n)-\epsilon_n\beta_{n-1}.
\]

The standard memory boundary is `D_old=0`, all old numerators zero,
`D0>=2`, `C>=2`. Positive increasing denominators give `0<=epsilon<=1/7`.
The first decoded step has `Delta beta1=h k0<=0`. Thereafter

\[
 \Delta\beta_{n+1}=\epsilon_n\Delta\beta_n+(1+\epsilon_n)h k_n\le0.
\]

The inequality follows by induction because every decoded `k_n<=0`, including
off-trajectory integer spinor values. Thus beta is nonincreasing at every actual
tick. In particular `0<B_n<=B0` for every finite tick. This result uses the
retained old slice rather than dropping it.

If `|k_n|<=Kmax` on an interval, the same recurrence gives

\[
 -\tfrac43hK_{\max}\le\Delta\beta_n\le0,
\quad \beta_0-\tfrac43TK_{\max}\le\beta_n\le\beta_0,
\]

because `(1+1/7)/(1-1/7)=4/3`. Therefore

\[
 \lambda_{\min}(\gamma_n^{-1})\ge
 \exp(2\beta_0-\tfrac83 T K_{\max}).
\]

The trace audit verifies that inequality exactly using rational beta and k.
A finite observed `Kmax` is a certificate for that trace, not a proof that the
native map has the continuum's global curvature bound. Discrete global stability
and efficient storage remain separate obligations.

## Actual common-state evidence

The default identity is the same as the runtime/clock candidate:

| Object | Identity |
|---|---|
| Tensor | `8d5f0fad5d094908afd4e78d05e60710b96c95943bb7aa791e5b753ff33e9df9` |
| Complete seed | `61b79e0831d775508ab04086aa4f4009d89bb6df95e2357e4ee7e5ff2777097f` |
| Allocation | 6 channels, 18 retained integers per node |
| Terms | 58 monomials, degree 3, coefficient multiplier 3456 |
| Preparation | 27 nodes, D=4, all old registers zero, all six carry classes |

The same source and complete seed were run at fixed physical time `T=1/8`:

| h | Ticks | Peak retained bits | Metric/history checks |
|---:|---:|---:|---|
| 1/24 | 3 | 207 | passed |
| 1/32 | 4 | 649 | passed |
| 1/48 | 6 | 6101 | passed |

Each shared trace includes the independent scalar oracle, every microstep
inverse and full rewind. This lane checks all snapshot constraints, the exact
beta/history recurrence, monotonicity and the quantitative metric bound.
The maximum observed `|k|` is exactly `1/2` in these runs, giving the certified
lower bound `beta>=-1/12`; their actual final beta values are near `-0.062`.
The three timestep choices have different tensor fingerprints; they are a
declared refinement family, not three allegedly identical laws. This table
establishes domain certificates; the coordinator's independent trajectory
comparison supplies the separate convergence evidence.

A forged beta numerator in an otherwise unchanged first output still has zero
algebraic matter constraint. The metric recurrence rejects it. This is a passive
corruption control; no running state is changed or repaired.

## Proper-time and geodesic interpretation

For the same homogeneous metric, `u=(1/N,0,0,0)` has unit timelike norm and
zero covariant acceleration. Comoving dust curves are geodesics and
`d tau_comoving=N dt`. In the chosen candidate `N=1`; the continuum parameter
is the synchronous dust proper time. This does not turn a retained arithmetic
scheduler or a passive graph label into an operational clock detector.

For a freely falling reference body of rest mass m and conserved spatial
covector `p_i`, the same metric gives

\[
 E=\sqrt{m^2+e^{2\beta}|p|^2},\qquad
 \frac{dx^i}{dt}=\frac{N e^{2\beta}p_i}{E},\qquad
 \frac{d\tau_{\rm body}}{dt}=\frac{Nm}{E}.
\]

The audit verifies both the mass shell and proper-time contraction exactly.
At beta=0, N=1, m=4 and spatial momentum magnitude 3, the rate is `4/5`, not
one. A null reference signal has coordinate speed `N exp(beta)`.
Because `B(t)<=B0` for the exact future solution, any timelike geodesic with
finite conserved momentum has proper-time rate bounded below by a positive
constant, and a nontrivial null geodesic has affine rate
`d lambda/dt=1/(B|p|)>=1/(B0|p|)`. Thus this exact future homogeneous geometry
also has complete future timelike and null reference geodesics. These are
continuum consequences of the shared solution, not retained moving particles.

No additional packet, trajectory or endpoint detector channels are allocated
by this module. Restoring spatial scalar gradients would make the frame factor
`exp(beta)` enter the evolution itself. Such an extension needs its own legal
polynomial encoding, momentum/curvature constraints and source ledger; the
homogeneous six-channel proof cannot simply be relabeled as a spatial model.

## Primary sources and scope

- Husain and Pawlowski, [Dust reference frame in quantum cosmology,
  arXiv:1108.1147](https://arxiv.org/pdf/1108.1147), §2: dust time and the
  physical Hamiltonian for homogeneous gravity plus other matter.
- Husain and Saeed, [Cosmological perturbation theory with matter time,
  arXiv:2007.06609](https://arxiv.org/pdf/2007.06609), §II, equations (11)–(16):
  dust-time gauge, lapse choice and the still-present spatial constraint.
- Brown and Kuchar, [Dust as a Standard of Space and Time,
  gr-qc/9409001](https://arxiv.org/pdf/gr-qc/9409001), equation (2.10) and
  Appendix D: material proper time and the particle mass-shell relation.

These references establish the interpretation of dust time and geometric
measurements. The spinor pushforward, exact beta/history inequality, numerical
fingerprints and corruption controls are explicitly derived and tested here.
General inhomogeneous Einstein evolution, operational clock calibration and
efficient long-time integer evolution remain unestablished.
