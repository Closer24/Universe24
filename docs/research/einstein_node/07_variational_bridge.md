# 7. A constructive bridge: the same matter phase can encode motion and time

Status: continuum derivation and proposed falsifying experiment; **not an
executed Universe24 packet/clock result**. Inspected main `4c494c1188f70eb8a677bf59765cc6e8571c6b88`
and PR #50 `62202fdccdd9a40d5dbbec104de6f97d9587a999`. No Engine, tensor,
allocation, protocol, or supported runtime was changed by this review.

## What can unify naturally

Assume a single smooth Lorentz metric, signature (-+++), and a neutral massive
scalar obeying `(hbar^2 Box_g - m^2) Phi = 0`, with c=1. Substitute
`Phi=A exp(i S/hbar)`. Direct differentiation gives

\[
-A\big(g^{\mu\nu}\partial_\mu S\partial_\nu S+m^2\big)
+i\hbar\big(2\nabla A\cdot\nabla S+A\Box S\big)
+\hbar^2\Box A=0.
\]

For a controlled single-branch semiclassical approximation, with slowly varying
nonzero amplitude, the leading phase therefore satisfies

\[
p_\mu=\partial_\mu S,\qquad p^\mu p_\mu=-m^2.
\]

Metric compatibility and the symmetry of the scalar Hessian give
`p^nu nabla_nu p_mu = (1/2) nabla_mu(p^2)=0`. Thus `u=p/m` is the tangent
of a timelike geodesic. Along it,

\[
\frac{dS}{d\tau}=p_\mu u^\mu=-m.
\]

This connects **matter propagation, proper-time phase, and the same metric**
without appending a particle-trajectory register. It remains conditional on
the matter equation and asymptotic regime. Phase is not an operational clock
record until a physical comparison/measurement mechanism is supplied.

For a massless scalar or source-free Maxwell wave, geometric optics instead
gives `k=dS`, `k^2=0`, `k^nu nabla_nu k_mu=0`, and amplitude-flux conservation.
The same principal kinetic metric then supplies null rays. This relation is
derived from wave dynamics, not a greedy path choice or load equalization.

### The limit matters

At **fixed mass**, taking arbitrarily high frequency makes the mass lower
order: the principal characteristics are null. A proof that the massive
Klein–Gordon principal cone is null is consequently not a proof of timelike
packet motion. The timelike result keeps mass in the leading Hamilton–Jacobi
balance, for example in the semiclassical scaling above, or in a slowly varying
background with `m L >> 1` and suitable resolved packets. It also requires
control of packet spread, amplitude gradients, caustics, and gravitational
backreaction. An arbitrary real oscillation in an expanding background is not
an ideal phase clock.

For charged matter `p=dS-q A`; differentiation yields the Lorentz force,
not a geodesic whenever the electromagnetic field contributes at leading
order. A charged phase is gauge dependent; any proposed clock comparison must
use an appropriate gauge-invariant relative phase or a neutral sector.

## Where the present candidate offers a port

At the PR #50 pin, `validation/geometry/team48/matter_charged.py` already
retains `(phi, chi)`, their two Pi fields, six covariant Xi gradients, Maxwell
fields and the shared frame. `equations()` constructs directional derivatives
with `B[a][i]` and uses reciprocal scalar current in the Maxwell equation.
`validation/research_eight/05_clock_port_audit.py` explicitly distinguishes its
three-step phase-equivariance check from moving-clock/redshift acceptance.
Those are useful existing fields, not yet a transported clock demonstration.

There is a separate obligation: derive or validate the metric's Einstein
equation and its constraint propagation. Minimally coupled fields follow the
metric in the stated limit even when that metric does **not** satisfy Einstein's
equations. Likewise, a reciprocal edge force does not itself imply a covariant
stress tensor, a discrete Bianchi identity, or gravitational dynamics.

## Minimal next experiment, with no additional retained channels

Use one pinned massive common-frame law, complete seed, runtime and metric
readout for all runs. The following is a proposal and is **not_tested**.

1. First establish a resolved narrow-band scalar packet in the flat limit;
   compare its measured group velocity with `p/sqrt(m^2+p^2)` in several
   directions. Use existing scalar/Pi/Xi channels and prepare their gradient
   relations consistently. Read the center/phase passively from saved fields;
   no trajectory callback advances the packet.
2. Move to a slowly varying vacuum Kasner background, whose synchronous
   rest-clock rates are all one while its directional metric and tidal field
   are nontrivial. At a reference time, `B=I` and
   `K=diag(1/3,-2/3,-2/3)/t0` give an exact homogeneous vacuum-constraint
   control. Use `m t0 >> 1`, an oblique packet, and at least two boosts and
   widths. A packet added with amplitude epsilon perturbs the Einstein
   constraints at order epsilon squared: either solve that initial constraint
   correction during preparation or quantify this as a test-field error and
   demonstrate its controlled vanishing.
3. Compare actual packet transport with an independently integrated geodesic
   in **that run's decoded metric**, and compare accumulated phase with
   `-m tau/hbar`. Independently compare the metric with the analytic Kasner
   background as epsilon tends to zero. Keep these two error sources separate.
4. Use the already retained Maxwell fields in a separate preparation of the
   same law to check a localized, transverse null packet. Include an oblique
   direction and reject a fixed Euclidean-cone oracle. Do not equate a
   principal-symbol calculation with this finite-packet experiment.
5. Predeclare a fixed endpoint, resolution ladder, error norms, admissible
   gradient/Gauss/Einstein defects and tolerances. Refine time, space and
   integer preparation independently before claiming a joint limit. Track
   packet width and field tails, phase failures, source stress, all carries,
   inverse/replay and integer bit cost. Calibration is fixed in flat space.

The present projective representation's exponential bit growth may block the
required resolved duration. Record that as **blocked**, not a successful
geodesic limit. This experiment also supplies no click-only detector or Born
claim; it isolates the next same-field motion/phase gate without consuming
the three unallocated slots.

## Primary-source ledger

- Sam R. Dolan, *Geometrical optics for scalar, electromagnetic and gravitational
  waves on curved spacetime* (2018), [arXiv:1806.08617](https://arxiv.org/pdf/1806.08617),
  sections 2 and 3, especially equations 16–20 and the Maxwell construction.
  Inspected the text: shared principal part, null eikonal/geodesic equation,
  short-wavelength conditions, amplitude flux. This is the source for the
  null-wave bridge; it does not prove the integer scheme's limit.
- Hikaru Yumisaki, *Several solutions of the Klein–Gordon equation in
  Kerr–Newman spacetime and the BSW effect*, PTEP 2017 063B04,
  [original article](https://academic.oup.com/ptep/article/2017/6/063B04/3904555),
  [author preprint](https://arxiv.org/abs/1606.09626), section 3.1,
  equations 51–54. Inspected article text: charged KG to Hamilton–Jacobi
  limit. The neutral timelike-geodesic and proper-phase identities above
  are directly derived here; no black-hole-specific result is imported.

The proposed use of existing fields, Kasner protocol and separation of error
budgets are this review's recommendations, not results claimed by these papers.
