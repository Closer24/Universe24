# Researcher 5: a material clock port without another clock bank

Date: 2026-11-11. Inspected local integration commit: `613ea1b`.
Baseline: PR #47 (`621fc1f55800e50e1db5f6a30ce24bb83716a49a` remotely),
the projective 41/44 proposal, and issues [40](https://github.com/Closer24/Universe24/issues/40)
and [41](https://github.com/Closer24/Universe24/issues/41).

## Recommendation and boundary

Use **an observable of the already gravitating massive scalar** as the first
clock candidate. Do not spend the remaining four slots on an uncoupled rotor,
and do not identify the projective denominator, phase scheduler, or the charged
scalar's absolute phase with proper time. The two local scalar invariants

\[
 I=\phi^2+\chi^2,\qquad S=\phi\Pi_\phi+\chi\Pi_\chi
\]

provide an amplitude and an orientation for a potential tick. They use no new
retained channel. In the normal-frame continuum equations, \(n(I)=2S\).
This follows directly from the existing scalar equations, including the
cancellation of a temporal gauge rotation; it is not a claim that a finite
difference satisfies a continuum product rule.

The minimal near-term experiment is a weak, localized, oscillating scalar packet
in the same metric, with its contribution to stress kept once. The tick candidate
is a negative-to-nonnegative crossing of S, with a predeclared amplitude/domain
condition. A broad homogeneous oscillation is a calibration control, not a
localized moving apparatus. Existing Maxwell variables supply the prospective
signal field. No accepted operational detector or proper-clock implementation
is supplied by this report.

## Original papers read and what transfers

The following readings use the original papers' equations and relevant sections,
not only search abstracts. These are continuum results; none supplies the
required fixed-six integer compiler.

1. **Brown and Kuchař, “Dust as a Standard of Space and Time in Canonical Quantum
   Gravity” (1995)**, [original PDF](https://arxiv.org/pdf/gr-qc/9409001),
   Section II, equations (2.1)–(2.10), and Section IV.
   They introduce eight scalar variables \(T,Z^k,W_k,M\), with
   \(U_\mu=-\partial_\mu T+W_k\partial_\mu Z^k\).
   Their action imposes \(U^\mu U_\mu=-1\); along the dust flow,
   \(U^\mu\partial_\mu T=1\). Thus T can be physical reference time in
   its valid dust chart. This does **not** turn our one signed density amplitude
   into a clock: its present normal-comoving equations retain neither T nor the
   general velocity/reference-label variables. An eight-scalar continuum count
   is also not an eight-channel integer implementation proof. Caustics and
   chart validity remain relevant.

2. **Roura, “Gravitational Redshift in Quantum-Clock Interferometry” (2020)**,
   [original PDF](https://arxiv.org/pdf/1810.06744), Sections II–III,
   equations (2), (7)–(11).
   Two internal energies give relative phase
   \(\Delta E\,\Delta\tau/\hbar\); initialization and readout involve
   explicit radiation interactions. The freely falling wave-packet treatment
   assumes small packet size relative to curvature scales and small internal
   momenta in its comoving frame. This motivates distinguishing evolving
   material state, actual readout, and metric-predicted proper time. The paper's
   atomic states, pulses and quantum measurement are not already present in
   the classical scalar/Maxwell model.

3. **Zych, Costa, Pikovski and Brukner, “Quantum interferometric visibility as a
   witness of general relativistic proper time” (2011)**,
   [original PDF](https://arxiv.org/pdf/1105.4531), introductory distinction,
   massive-clock model and equations (10)–(13).
   Their clock has evolving internal degrees of freedom; an overall matter-wave
   phase alone does not establish an operational clock. The visibility prediction
   is a quantum result for their apparatus. We use the distinction to reject a
   phase-label shortcut, without importing their probabilities or claiming a
   Born derivation.

4. **Dolan, “Geometrical optics for scalar, electromagnetic and gravitational
   waves on curved spacetime” (2018)**,
   [original PDF](https://arxiv.org/pdf/1806.08617), Section 3,
   equations (16)–(25).
   At leading short-wavelength order, scalar/Maxwell phases define null
   geodesics, flux is transported and polarization is parallel transported.
   The measured frequency depends on the observer, \(-\omega u^a\nabla_a\Psi\).
   Wavelength and inverse frequency must be small relative to background scales;
   discarded amplitude terms limit exactness. Existing Maxwell fields are
   therefore a candidate shared-metric signal, but nearest-neighbor message
   speed and a finite lattice dispersion relation cannot simply be called light.

## Algebraic proposal and two required negative controls

For the continuum homogeneous flat, free massive scalar calibration,

\[
 \phi=A\cos(m\tau),\quad\chi=B\sin(m\tau),\quad
 I={A^2+B^2\over2}+{A^2-B^2\over2}\cos(2m\tau).
\]

When \(A\ne B\), I has a repeatable feature every \(\pi/m\) proper-time units.
An oriented minimum of I is a possible tick without evaluating `atan2`,
unwrapping a phase, or retaining a new counter. When \(A=B\), I is constant:
**phase rotation alone is a no-clock control**. When m=0 the massive periodic
mechanism is absent. These are continuum calibration identities, not a proof
of an indefinitely accurate discrete clock.

The circular/elliptical charged homogeneous case has nonzero scalar charge
unless one component vanishes. With zero electric divergence, it violates
Gauss on a periodic board. It is therefore a neutral-scalar algebra control
(`coupling=0`), not valid charged periodic initial data. The actual coupled audit
below uses a linearly polarized, charge-zero field instead.

Under a local U(1) rotation, the scalar and its covariant momenta rotate
together. I and S are invariant, whereas an absolute component-phase crossing
is not. In projective representation,

\[
 I={P_\phi^2+P_\chi^2\over D^2},\qquad
 S={P_\phi P_{\Pi_\phi}+P_\chi P_{\Pi_\chi}\over D^2}.
\]

On the proved positive-D domain, the sign of S needs only the numerator.
This is an onsite, degree-two passive diagnostic. The tick rule uses the two
adjacent saved transitions; its record does not feed evolution. A passive
event count is not additional retained state. If a counter/receiver affects
later dynamics, it must be compiled and charged to the 48-channel allocation.

The present charged lattice equations have not been proved to possess exact
arbitrary **spatially varying** gauge covariance. The check below establishes
only constant rational rotation equivariance. Gauge-invariant definitions
remain necessary even before local discrete gauge symmetry is repaired.

Expansion, gradients, electromagnetic work and self-gravity disturb the ideal
oscillator. For example, a homogeneous scalar on FLRW satisfies
\(\ddot\phi+3H\dot\phi+m^2\phi=0\), giving

\[
 \ddot I=2(\Pi_\phi^2+\Pi_\chi^2)-2m^2I-6HS.
\]

Consequently even gauge-invariant amplitude minima are not automatically
universal clocks. The prospective proper-clock regime must have envelope,
curvature, acceleration and interaction scales well separated from \(m^{-1}\),
and finite-size errors must be measured. In the current synchronous chart,
normal stationary trajectories have lapse one: observing identical local rates
there cannot demonstrate gravitational redshift.

## Allocation and coupling

| Candidate | Extra retained channels | Total over protected44 | Status |
|---|---:|---:|---|
| I/S from existing massive scalar, existing Maxwell signal | 0 | 44 | Algebraic/readout candidate; no new apparatus dynamics |
| Independent real scalar in the current first-order representation: q, p, three gradients | 5 | 49 | Over budget; 41+5=46 is only an unprotected alternative allocation |
| Onsite q,p oscillator without gradients or transported carrier | 2 | 46 | Does not establish moving/3D matter apparatus |
| General Brown–Kuchař reference dust | Not compiled | Unknown | Cannot be inserted by renaming the existing density amplitude |

The five-field count is for the supplied first-order representation, not a
universal lower bound for all encodings. Reusing the complex field for source
and clock means a single owner with a clock readout, not two superposed owners.
The scalar kinetic, gradient and mass terms already contribute to rho, momentum
and stress; do not add the same clock energy a second time. A probe limit must
scale its actual amplitude and compare decreasing backreaction, not suppress
its source term by a runtime switch.

An explicit future detector interaction, for example a neutral readout field q
with \(V_{int}=g_d qI\), has reciprocal scalar forces proportional to q phi and
q chi and receiver force proportional to I. These are degree-two forces; the
interaction energy is cubic and must also enter the shared stress tensor.
That is a concrete port hypothesis, **not implemented**, and a full 3D q field
costs the five fields above. A bare source-driven q,p with no reciprocal force
would fail the energy/backreaction requirement. Binding, localization and record
formation remain additional work, not free consequences of this interaction.

## Fresh exact Engine evidence

Reproduce from this checkout:

```bash
PYTHONPATH=. python validation/research_eight/05_clock_port_audit.py
```

The audit creates the **existing** massive protected44 tensor, with no runtime
modification: 44 channels, 132 retained integers/node, 637 monomials,
`mass_squared=1`, `dt=1/64`, 27 sites. Tensor fingerprint:
`dca4eee3ac204b368af811e73291bf0e441869f469263d0124d018431e4788ef`.

It compares a homogeneous scalar/dust preparation and its constant rational
U(1) rotation `(cos,sin)=(3/5,4/5)` through three real Engine updates. Both have
B=I, K=-I, phi=2, scalar momenta zero and signed dust amplitude 1 initially,
with the protected old-q memory. These current continuum fields have rho=3 and
vanishing homogeneous initial H/M constraints. The audit does not certify
later constraints.

Passed: complete rational rotation equivariance, identical geometry/dust/Maxwell
readouts, zero scalar charge, all six retained remainder classes, exact scalar
oracle agreement, per-step inversion and full rewind. Maximum retained bits
at seed and subsequent updates: **8, 28, 89, 272**. Strict face-support
violations: zero. Independent symbolic checks verify I/S invariance, the radial
derivative identity, the elliptical intensity formula and constant-intensity
circular negative control. Output: `runs/research_eight/05_clock_port.json`.

Not tested: a complete tick period in the coupled Engine, moving packet
transport, arbitrary local lattice gauge covariance, redshift, null-signal
propagation, click-only readout and general Einstein acceptance. The original
projective bit-growth problem remains. This is a verified invariant port and
negative-control package, not a successful physical clock experiment.

## First acceptance sequence

1. **Flat calibration:** one massive real/charge-zero packet, one fixed tick rule
   and frequency calibration. Hold out amplitude, initial phase and orientation;
   retain zero-source, massless and circular no-clock controls. Refine time and
   space enough to resolve actual periods; report dispersion and missed ticks.
2. **Moving control:** transport the localized field across actual face links
   in axial and off-axis directions. Compare tick ratios with independently
   integrated metric proper time, using the same calibration. Counting events at
   a fixed Eulerian node is not the moving packet's clock reading.
3. **Geometry control:** nontrivial lapse/shift or transformed-flat tests plus
   weak inhomogeneous sources. A common metric must predict both the packet
   path and tick rate. No per-trajectory fit. Reconstruct curvature independently.
4. **Signal/readout:** a Maxwell pulse and a retained reciprocal receiver
   interaction. Expose all no-detection windows. The current arithmetic click
   stream does not contain I/S by definition; state-diagnostic minima cannot be
   relabeled click-only measurements. An actual record-to-tick protocol must
   pass the existing decoder boundary and avoid hidden trajectory reads.
5. **Backreaction:** vary clock/source amplitudes, compare rho/j/S and metric
   response, and check the same independent Einstein/matter balances. Only
   after that test another mechanism without changing calibration rules.

The strongest next step is reuse of the massive scalar with a gauge-invariant
tick candidate, accompanied by the explicit no-clock controls above. It keeps
the 44-channel budget while exposing precisely what still needs a material
implementation and convergence evidence.
