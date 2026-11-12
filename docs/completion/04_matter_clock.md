# Massive matter clock on the common corrected45 candidate

The monitor's different-tensor gap is closed for a **passive matter diagnostic**:
the clock audit now uses the explicitly massive corrected full45 law, its full
geometry and scalar stress, and the same complete weak seed as the other
completion audits. It does not establish an operational proper-time clock.

Run `python -m validation.completion.matter_clock` from the repository root.
Evidence is written to `runs/completion/04_matter_clock.json`.
The implementation is `validation/completion/matter_clock.py`; the shared law,
preparation, ownership and existing-runtime handoff are in `common45.py`.
The imported source baseline is PR50 commit
`62202fdccdd9a40d5dbbec104de6f97d9587a999`; this report describes new source on top
of that baseline, not a result already contained in PR50.

## 1. One explicit massive law and complete seed

Units are `c = 8 pi G = 1`, signature `-+++`, synchronous lapse one and shift
zero. The scalar parameter is `mass_squared = 1`, with charge coupling one and
zero cosmological constant. The common protocol has `dt = 1/64`, `dx = 1/4`.

| Object | Exact identity |
|---|---|
| Common tensor SHA256 | `6ea453fa77a5a9d74af5bd4fc626cfcdc8f92942b10c301d2d00814bf4d05ba0` |
| Complete seed SHA256 | `b53909631f3e14e3c09905275fe7b50a0dad2ecdec9ac431db2306127abd3b7c` |
| Retained allocation | 45 channels, 135 integers per node; zero added clock channels |
| Tensor | 889 monomials, degree two, strict single-face support |
| Grid | 27 sites, periodic `L = 3` |
| Physical initial data | `B = I`, `K = -I/10`, `phi = 1/5`, dust amplitude `1/10`; all other fields zero |
| Encoding | `D = 100`, old registers zero, carry `(gear + node) mod 6` |

The initial density is `rho = 3/100`; all constraints returned by the actual
builder vanish, including `H = 6/100 - 2 rho = 0`. The same retained `B` defines
`gamma_inverse = B.T B` for matter, metric and signal audits. No protected
triangular44 nondegeneracy result is imported.

Three actual Engine updates, including the independent scalar oracle, immediate
inverse and full rewind, pass. A matched rational rotation with cosine `3/5`
and sine `4/5` rotates all scalar/covariant-gradient pairs. The decoded `I`, `S`,
charge, source stress, geometry, dust and electromagnetic fields agree exactly
at every sample. Peak state sizes from the seed onward are `7, 22, 51, 110` bits.
This is global phase equivariance; it is not a proof of local lattice gauge
covariance.

Backreaction is checked on this tensor: removing the scalar from the same
geometric/dust preparation changes each first-step diagonal `K` by `-1/3200`
when the sourced result is subtracted from the scalar-free comparison in the
order `with_source - without_source`. Thus the clock carrier's stress is not
silently removed from the geometry. The scalar-removal comparison is
intentionally off the constraint surface; it is a causal source control.

## 2. Exact phase theorem and its domain

Let the real and imaginary scalar components be `x,y`, their covariant normal
derivatives `p_x,p_y`, and let `K = tr K_ab`. On the homogeneous sector with zero
covariant gradients and electromagnetic fields, the actual builder gives

\[
\dot x=p_x,\qquad \dot y=p_y,\qquad
\dot p_x=Kp_x-m^2x,\qquad \dot p_y=Kp_y-m^2y.
\]

Dots here mean continuum normal proper time, conditional on a nondegenerate
smooth solution in the stated gauge. They are not an identification of integer
Engine ticks with a measured proper time.

Define pointwise gauge-invariant quantities

\[
I=x^2+y^2,\quad S=xp_x+yp_y,\quad P^2=p_x^2+p_y^2,
\quad L=xp_y-yp_x.
\]

The code derives the following polynomial identities from the actual
mass-one equation builder, and separately verifies their arbitrary-mass form:

\[
\dot I=2S,\qquad \dot S=P^2+KS-m^2I,\qquad \dot L=KL.
\]

Set

\[
E=m^2I+P^2,\qquad Q=m^2I-P^2,\qquad R=-2mS.
\]

Direct multiplication gives

\[
Q^2+R^2=E^2-4m^2L^2,\qquad
Q\dot R-R\dot Q=2m(Q^2+R^2)+KER.
\]

Where `Q² + R² > 0`, a continuously unwrapped local phase
`theta = arg(Q+iR)/2` therefore obeys

\[
\boxed{\dot\theta=m+\frac{KER}{2(Q^2+R^2)}}.
\]

For the neutral radial sector, `L = 0` remains zero, and for `m > 0`, `E > 0`
this simplifies to

\[
\boxed{\dot\theta=m-\frac{KmS}{E}},\qquad
\theta_2-\theta_1=m(\tau_2-\tau_1)-\int_{\tau_1}^{\tau_2}\frac{KmS}{E}\,d\tau.
\]

Since `2m |S| <= E`, the sufficient bound `|K| < 2m` implies
`dot theta >= m - |K|/2 > 0`. This proves a monotone local phase under an
explicit domain condition. It also shows precisely why `theta/m` is generally
not elapsed proper time in the expanding sourced geometry. The initial common
slice has `|K| = 3/10`, but a global domain theorem does not follow from that
initial inequality.

An unwrapped phase uses a branch/winding history in the passive analysis. No
such winding counter or autonomous detector has been allocated to the retained
system. The formulas introduce no runtime division, inverse trigonometry,
projection or observer feedback.

## 3. An actual sampled oscillation, on a separately identified coarse protocol

The fine common protocol is impractical for a full massive cycle under the
current projective representation. To test more than three early samples, the
audit additionally executes **14 full Engine updates** of the same massive
equation family at `dt = 1/4`, `dx = 1/4`, on the same complete seed. Its tensor
SHA256 is
`5383a9d4354b2ac3bc64692e4075986d53998e0852fe9381237ce72cd795105b`.
This is an explicit different immutable tensor, not extra evidence silently
assigned to the `dt = 1/64` law.

Every update passes the literal scalar oracle, all-six-carry check and inverse;
full 14-step rewind also passes. The intensity has an actual sampled minimum
at tick 7 and a sampled maximum at tick 13. The sampled `S` signs change over
coordinate intervals `[1.5, 1.75]` and `[3.0, 3.25]`. These intervals describe
sample signs; they are not a theorem about a continuous interpolating solution.

| Diagnostic | Value |
|---|---:|
| Initial intensity | 0.04 |
| Sampled minimum, tick 7 | 0.00007444143761233207 |
| Following sampled maximum, tick 13 | 0.03994999858229903 |
| Largest retained integer, tick 14 | 174,385 bits |
| `det B` at tick 14 | 0.4090121901951048 |
| `tr K` at tick 14 | -0.2228109228442173 |
| Hamiltonian constraint at tick 14 | -0.017676989825824132 |
| Passive radial phase minus coordinate time, tick 14 | -0.03236283069935997 |

All sampled determinants are positive and all sampled `|tr K| < 2m`. The
Hamiltonian constraint drifts, and the next sampled intensity peak is not an
exact recurrence of the initial peak. Therefore the result is one resolved
sampled oscillation, not an exact period, a convergence result, a reconstructed
ideal proper-time clock or a nonlinear Einstein solution.

The cost obstruction is quantitative. With quadratic projective denominator
recurrence and the declared preparation, `D_n >= D_0^(2^n)`. A flat intensity
period `pi/m` at the fine `dt = 1/64` would need at least 202 updates. The lower
bound already rules out that straightforward long run with this encoding.
The separate native potential-shear work does not yet supply a replacement
shared-metric massive oscillator.

## 4. Negative controls and operational boundary

The mass-one tensor evolves a flat zero-source preparation with stationary
physical fields for three steps, with exact oracle and rewind. Removing the
mass in a separately fingerprinted control tensor leaves the homogeneous
zero-momentum scalar stationary: `I` is constant and `S = 0`. Holding the
massive geometric seed fixed for this massless control makes it off-constraint;
this is an algebraic no-oscillator test, not a second accepted universe.

In flat continuum Klein–Gordon theory, `x=A cos(m tau)`, `y=B sin(m tau)` gives

\[
I=\frac{A^2+B^2}{2}+\frac{A^2-B^2}{2}\cos(2m\tau).
\]

For `|A| != |B|`, its intensity period is `pi/m`. For a circular solution
`A = B`, intensity is constant and `Q = R = 0`: the proposed intensity phase is
undefined. A nonzero homogeneous charged circle has nonzero charge and violates
the periodic Gauss constraint without compensating data. It is only a
flat-field negative control here, not admissible full45 initial data.

The common three-step run emits 810 arithmetic Engine clicks, all of carry kind
`C0`. These are not calibrated material ticks. No retained receiver, memory,
moving detector, redshift measurement or click-only proper-time readout is
proved. The three unallocated channels must not be allocated simultaneously to
arithmetic work, apparatus and memory by different proposals.

## 5. Primary papers read and the narrow conclusions used

- [Roura, *Gravitational redshift in quantum-clock interferometry*](https://arxiv.org/pdf/1810.06744), sections II–III, equations (2), (6)–(10): proper-time phase and an operational clock initialization/readout are distinct ingredients. A scalar phase formula alone does not reproduce the preparation, internal levels and readout apparatus of that model.
- [Cembranos, Maroto and Núñez Jareño, *Cosmological perturbations in coherent oscillating scalar field models*](https://arxiv.org/pdf/1509.08819), equations (2)–(4), (26)–(29): expansion changes the massive scalar equation; the familiar oscillatory proper-time dependence is an adiabatic result with a specified small parameter. The exact phase identities above are derived independently for this candidate.
- [Brown and Kuchař, *Dust as a Standard of Space and Time in Canonical Quantum Gravity*](https://arxiv.org/pdf/gr-qc/9409001), section II: material reference fields have their own action, stress and constraints. The present one-amplitude normal dust is not silently promoted to that complete reference system.

Passed gates are same-law massive sourcing, exact short covariance, mechanics,
the conditional phase identities and one coarse sampled oscillation. Failed
gates include exact recurrence at the sampled peak, sampled Hamiltonian
constraint preservation and a universal identification of phase divided by
mass with proper time. Fine-cycle calibration, moving clocks, an autonomous
retained apparatus and physical acceptance remain unproved.
