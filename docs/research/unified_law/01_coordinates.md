# A cubic constrained coordinate law for the shared homogeneous candidate

The seven-agent search selects one common candidate: four real auxiliary
spinor coordinates and one logarithmic frame coordinate. Its physical decoder
obeys the homogeneous Hamiltonian constraint identically, and its cubic
continuum drift pushes forward to the actual massive Einstein–scalar–dust
equations. This removes the specific independently-null-history obstruction
by changing the complete physical interpretation. It does not make an arbitrary
integer update solve Einstein evolution.

Source: `validation/unified_law/constrained_coordinates.py`.
Reproduce: `python -m validation.unified_law.constrained_coordinates`.
Fresh evidence: `runs/unified_law/01_coordinates.json`.
The shared Engine compiler, finite-time refinement and cost checks are separate
packages consuming this exact source, not separately defined candidate formulas.

## 1. Actual physical target

Use the existing corrected full-frame source restricted to homogeneous,
isotropic, neutral radial scalar and comoving dust data, mass squared one,
zero cosmological constant, synchronous proper time and zero shift:

\[
\dot k=3k^2-\frac12(\phi^2+d^2),\qquad
\dot p=3kp-\phi,\qquad \dot\phi=p,\qquad
\dot d=\frac32kd,\qquad \dot B=kB.
\]

Here K is k times the identity, p is the scalar normal momentum, d is the
signed dust amplitude, and the inverse spatial metric is B squared times the
identity. The scalar and dust density is
\(\rho=(p^2+\phi^2)/2+d^2\). Its sole nontrivial homogeneous constraint is

\[
C=6k^2-p^2-\phi^2-2d^2=0,\qquad \dot C=6kC.
\]

The executable compares the coordinate construction with the actual imported
full44 source: every diagonal K equation, every B equation, both scalar
equations and the dust equation agree; all 33 declared constraints vanish;
every omitted field velocity vanishes. Thus the target is the existing sourced
Einstein sector, not a different ODE chosen just to preserve a quadratic form.

## 2. One quadratic physical decoder

Let the four real coordinates be a,b,c,e. Define

\[
\sigma=\frac{a^2+3b^2}{2},\qquad
\tau=c^2+3e^2,\qquad
p=ac+3be,\qquad y=bc-ae,
\]

and decode

\[
\boxed{
k=-\sigma-\tau/12,\quad
\phi=2\sigma-\tau/6-y,\quad
d=\sigma-\tau/12+y.}
\]

All coefficients are rational. The algebraic identities

\[
C=2\sigma\tau-p^2-3y^2=0
\]

hold for every real coordinate value. In particular they hold for every exact
rational readout of any retained integer state, without projecting it or
discarding a remainder or old register. Also k is nonpositive, and it vanishes
only when all four coordinates vanish.

The construction is a Hermitian rank-one factorization. With
\(\omega=i\sqrt3\) and \(\psi=(a+\omega b,c+\omega e)^T\),

\[
\psi\psi^\dagger=
\begin{pmatrix}2\sigma&p+\omega y\\p-\omega y&\tau\end{pmatrix},
\]

whose determinant is zero. The complex notation is only a proof device: the
implemented source uses four real polynomials and exact rational coefficients.
These are auxiliary coordinates on the constraint cone, not physical fermions,
quantum spin or a new spacetime metric.

Every real point on the expanding nonzero cone is represented. In fact
\(\sigma=(-3k+\phi+d)/6\ge0\) and
\(\tau=-6k-2\phi-2d\ge0\), so its rank-one Hermitian matrix is positive
semidefinite and has a spinor factor. The factor is not unique: a common complex
unit phase leaves the physical data invariant. All coordinates and their
retained histories/carries must nevertheless remain in the integer state;
many-to-one physical observation is not a state compression.

An arbitrary *rational* physical datum need not admit a rational spinor factor.
The new candidate therefore declares its own exactly representable initial
data. For a=1 and b=c=e=0 it has
\((k,p,\phi,d)=(-1/2,0,1,1/2)\). It is not the earlier full45 weak seed.
Rational coordinate data are dense in the real coordinate space, but that
observation alone is not a prepared-initial-data convergence theorem.

## 3. Exact cubic lift in the same proper time

Set \(u=d-\phi\), \(v=d+2\phi\), using the quadratic decoder above. The
shared coordinate drift is

\[
\begin{aligned}
\dot a&=\tfrac32ak+\tfrac14av+\tfrac12b+\tfrac16c-\tfrac14eu,\\
\dot b&=-\tfrac16a+\tfrac32bk+\tfrac14bv+\tfrac1{12}cu+\tfrac16e,\\
\dot c&=-a+\tfrac32bu+\tfrac32ck-\tfrac14cv-\tfrac12e,\\
\dot e&=-\tfrac12au-b+\tfrac16c+\tfrac32ek-\tfrac14ev.
\end{aligned}
\]

There are twelve expanded monomials in each of these equations, of degrees
one or three. The equation for beta below has four quadratic monomials. No
division by a state variable, square root, norm or time-dependent lapse enters
this drift. All dots denote the same synchronous proper-time coordinate as the
physical target. There is no time reparametrization to undo in the clock audit.

Let P denote the quadratic physical decoder and G the four-component drift.
Exact symbolic multiplication verifies

\[
\boxed{D P(\psi)\,G(\psi)=F(P(\psi)).}
\]

This equality holds identically, not just along sampled trajectories or after
imposing a separate constraint. By the chain rule, every regular solution of
the coordinate ODE decodes to the stated Einstein source equations.

The derivation is constructive. For \(z=(k,p,\phi,d)^T\) and
\(J=\operatorname{diag}(6,-1,-1,-2)\), write

\[
F(z)=3kz+A(z)z,\qquad
A=\begin{pmatrix}
0&0&-\phi/2&-d/2\\
0&0&-1&0\\
-3\phi&1&0&0\\
-3d/2&0&0&0
\end{pmatrix}.
\]

Direct multiplication gives \(A^TJ+JA=0\). Under the Hermitian
factorization this linear action lifts to a complex-linear action on psi;
the dilation contributes 3k/2 times psi. Substitution yields the four displayed
real equations. Thus quadratic physical coefficients become cubic coordinate
terms without multiplying them by extra phase registers.

The source also verifies phase equivariance. The infinitesimal common-phase
generator is \((-3b,a,-3e,c)\); it annihilates every physical decoder and
commutes with G. A rational period-six phase
\((a,b)\mapsto((a-3b)/2,(a+b)/2)\), and likewise for c,e, is checked
independently. This is coordinate gauge freedom, not an operational material
clock and not permission to erase its retained values.

## 4. One nondegenerate metric coordinate

Append beta with

\[
\dot\beta=k,\qquad B=\exp(\beta),\qquad
ds^2=-dt^2+\exp(-2\beta)(dx^2+dy^2+dz^2).
\]

For every finite real beta the spatial metric is nondegenerate. Exponentiation
is a passive physical interpretation only; the homogeneous drift never needs
B on its right-hand side, and beta's actual source is the same decoded k.
The continuum chain rule gives \(\dot B=kB\). The metric researcher checks
the same construction directly against four-dimensional curvature/source
identities and the actual common Engine trace.

The five continuum coordinates are **not** a complete retained-channel count:
the selected projective realization adds its denominator, and any native
compiler must count all clocks/workspace. No direct finite-step metric/Einstein
convergence claim follows merely from exponentiating beta.

There is also a uniform finite-physical-time continuum theorem, not only a
pointwise positivity observation. Substituting C=0 into the k equation gives

\[
\dot k=\frac{p^2+d^2}{2}\ge0,\qquad
-k=\frac{a^2}{2}+\frac{3b^2}{2}+\frac{c^2}{12}+\frac{e^2}{4}\ge0.
\]

Therefore k starts negative and remains between its initial value and zero,
and the weighted spinor norm is nonincreasing. The polynomial four-coordinate
vector field stays in a compact set on every future interval and hence has a
global future solution. Beta cannot diverge in finite time because its
derivative k is bounded. Explicitly, for 0<=t<=T,

\[
\beta_0+k_0 t\le\beta(t)\le\beta_0,\qquad
e^{\beta_0+k_0T}\le B(t)\le e^{\beta_0}.
\]

These are continuum results for the selected expanding branch. The discrete
projective Euler/memory map still needs its own bounded-error proof; the
nonincreasing-norm conclusion is not automatically inherited by it.

## 5. Invariants, acceptance and a falsifying control

The same vector field exactly gives
\(\dot\rho=3k(\rho+P)\), with scalar pressure
\(P=(p^2-\phi^2)/2\), and

\[
\frac{d}{dt}\bigl(d^2 e^{-3\beta}\bigr)=0.
\]

These are useful independent source/volume targets for the actual discrete
trajectory. Exact C=0 does not imply that they hold at finite Engine ticks.

For the exactly representable initial seed above, |3k0|=3/2<2. The global
bound proves that this inequality remains true in the continuum. The scalar
pair obeys a linear homogeneous second-order equation with continuous bounded
coefficients and cannot become simultaneously zero at finite time from its
nonzero initial value. Consequently the neutral phase
\(\theta=\operatorname{atan2}(-p,\phi)\) has
\(\dot\theta=1-3k\phi p/(\phi^2+p^2)\ge1/4\) at every finite future
time. This proves a monotone material phase for this continuum sector, not
an operational detector or equality of phase with elapsed proper time.

The audit deliberately sets only the c-coordinate drift to zero. The same
decoder still makes C identically zero, yet the decoded scalar equation
\(\dot\phi=p\) fails by a nonzero polynomial. Thus a candidate cannot pass
just by reporting its exact constraint residual: it must pass independent
equation and fixed-time trajectory checks too. The native scheduler and common
compiler retain that obligation.

Executed local evidence: exact all-coordinate polynomial identities; actual
full44 source comparison; all 33 constraints; phase equivariance; 625 signed
rational decoder controls; and the wrong-drift rejection. No production Engine,
runtime, default model or physical-acceptance status is changed by this module.
Spatial modes, anisotropy, Maxwell fields, charged scalar phase and autonomous
detectors are outside this homogeneous candidate.

## 6. Primary reading and source-specific derivation

- Larsson and Larsson, [The Lorentz group and the Kronecker product of matrices,
  arXiv:2110.15118v2](https://arxiv.org/pdf/2110.15118), sections 1 and 3:
  Hermitian matrices relate real Lorentz actions to two-component complex
  transformations. This motivates the algebraic lift; the rational decoder
  and cubic sourced vector field above are derived here, not taken from that paper.
- Husain and Pawlowski, [Dust reference frame in quantum cosmology,
  arXiv:1108.1147](https://arxiv.org/pdf/1108.1147), section 2:
  a timelike dust reference permits a proper-time Hamiltonian description.
  The present coordinate construction does not import their quantum model or
  add a retained operational dust clock.
- Alho, Uggla and Wainwright, [Dynamical systems in perturbative scalar field
  cosmology, arXiv:2006.00800v2](https://arxiv.org/pdf/2006.00800), introduction:
  selecting regular state-space variables can simplify cosmological dynamics.
  Their potential and perturbation model differ from this mass-one sector.

Initial shared-candidate coordination:
[issue40 comment](https://github.com/Closer24/Universe24/issues/40#issuecomment-6811668593).
