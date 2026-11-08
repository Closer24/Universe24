# Mass-like families and fixed initial coefficients

Status: operational research proposal, not an executed experiment or a physical
mass identification. The baseline remains unchanged. The separate
[fixed-coefficient candidate](../fixed_ratio_candidate.md) specifies one possible
extension and its inverse; it is not an existing engine option. All tests below
would need their own frozen preparations, observations, budgets and acceptance
bounds before execution.

## What a mass claim must predict

Relativistic particle kinematics relates independently measured energy and
momentum through `E^2-c^2*|p|^2=m^2*c^4`; the velocity is `c^2*p/E`.
A massive particle admits a rest frame, whereas a nonzero-energy massless
particle in vacuum travels at c in this description. The same four-momentum
relations constrain collisions and transformations between inertial frames
[1, section 49.1–49.2]. These are connected physical predictions, not definitions
that can be established by naming a board counter “energy.”

A stationary periodic board pattern is therefore a candidate clock or object,
not an established massive particle. A directed moving packet is a candidate
carrier, not an established photon. A changed clock period, delay, signed
quotient gain or propagation speed in a prepared guide does not supply mass.
The present board studies have not independently calibrated physical energy,
momentum, inertial frames or a universal observed signal speed.

There is now a concrete algebraic starting point: the
[coherent-sector derivation](../coherent_wave_algebra.md) shows that equal
triples across all48 channels at each site form an invariant sector for +++.
Its large-amplitude linear comparison has
`cos(omega)=(cos(k_x)+cos(k_y)+cos(k_z))/3` in the baseline, with an explicit
finite-time RMS error bound for the integer trajectory. Its long-wavelength
branch is gapless with leading speed1/sqrt(3), below the microscopic causal
bound1. This is a controlled classical scalar-wave comparison, not a photon
identification. In particular, the scalar sector does not establish Maxwell's
transverse degrees of freedom. The bound does not control native threshold
click times, and it does not supply a moving detector or an internal record.
The separate [internal-channel derivation](../internal_gap_algebra.md) also
exhibits a baseline k=0 eigenvalue2, giving `cos(omega)=1/3` in the full-channel
comparison. It constructs exact integer preparations following that internal
oscillation for any predeclared finite duration, at the cost of initial
amplitudes growing exponentially with the duration. Thus a frequency gap does
not require changed primitive coefficients. This global internal mode is not a
localized rest particle, and its nonzero-wave-vector dispersion remains to be
derived. Uniform candidate ratios below1 provide another comparison frequency
gap; those variants have not been implemented or run. These algebraic
statements make M1 below more concrete while leaving the remaining physical
gates open.

There is a useful methodological precedent: D'Ariano and Perinotti derive a
Dirac limit and dispersion relations for a particular quantum cellular
automaton, under unitarity, locality, homogeneity and discrete isotropy, in a
specified small-wave-vector and small-mass regime [2]. Their model has quantum
amplitudes and a different evolution law. Its derivation illustrates the kind
of controlled effective limit to seek; it does not establish that the same
result holds for reversible integer Rule3.

## Separate the three coefficient interpretations

| Interpretation | Mathematical meaning | Necessary operational distinction |
| --- | --- | --- |
| Uniform initialized ratio | One fixed p/q everywhere in a separately specified candidate | Compare complete behavior families across candidate values; a different primitive gain is not a measured mass. |
| Site/channel-fixed ratio field | Each lattice address and channel pair has immutable p_i/q_i | A moving pattern traverses a prepared medium. Test translation and direction dependence; the coefficient map belongs to the full experiment identity. |
| Ratio carried by a moving object | A property follows the identified object through different lattice addresses | This does not follow from a fixed address field. It requires an explicit admissible transport rule in a separate candidate, or a derived state-dependent effective response under the unchanged rule. |

In the current proposal, coefficients belong to the entire channel update,
including the a/b pair and remainder domain. Giving a and b unrelated ratios
is another proposal, not a choice already covered by its proof.

Generic heterogeneous coefficient fields select locations; channel dependence
can also select directions. A uniform choice avoids that particular spatial
inhomogeneity but does not prove Lorentz covariance. Even a homogeneous lattice
provides a microscopic rest frame. Observed approximate frame independence
would have to be demonstrated with moving emitters, receivers and clocks, not
by changing camera coordinates. Distinguish a physical medium with a preferred
rest frame from an effective vacuum law, and quantify the scale on which any
preferred-frame effect becomes small.

## A staged operational test

The following gates are proposals. Failure at an earlier gate limits the name
of the later result; it must not be repaired by changing the observer afterward.

| Gate | Frozen observable and comparison | Permitted conclusion if passed |
| --- | --- | --- |
| M0: identity and transport | Complete template or declared finite-error identity, background and halo; isolated motion over new distances and orientations; zero-input and no-wrap controls | An identified mobile board object in the declared environment. |
| M1: dispersion | Fixed spatial/temporal readout for a family of wavelengths, phases and valid amplitudes; measure omega(k), packet velocity and dispersion with errors | A finite effective propagation law, possibly a gapless or gapped branch. |
| M2: rest and inertia | An identifiable rest preparation and moving relatives; compare full-state trajectories after matched, internally realized probe encounters against free controls | A reproducible response family. “Inertia” additionally needs an independently calibrated transferred momentum. |
| M3: common kinematics | Independently defined energy and momentum, conserved balance including radiation, and common coefficients predicting held-out collisions and motion | A mass-like parameter only within the tested effective kinematic law. |
| M4: moving-apparatus records | The same source, clock and detector definitions in several moving preparations; common transformation predicts clock ratios, crossings and collision records | A tested approximate frame relation over its measured range, not exact Lorentz symmetry. |

For M1, preregister competing effective models such as
`omega^2 = c_eff^2*|k|^2` and
`omega^2 = omega_0^2+c_eff^2*|k|^2`, together with allowed higher-order lattice
corrections and an error bound. A nonzero fitted omega_0 is initially a
**frequency gap**, not mass. Interpreting it as `m*c^2/hbar` needs a justified
energy/frequency and momentum/wave-vector correspondence. Rule3 is nonlinear
and integer-valued; a smooth mode family, superposition regime or linearized
dispersion relation must first be shown to exist in the declared preparation
domain. A Fourier peak from one periodic clock is insufficient.

Use at least three distinct nonzero wave-vector magnitudes for discovery and
two new magnitudes for validation, plus the independently defined rest/long-wave
case where available. Include reversed directions and inequivalent lattice
orientations, multiple initial phases, valid amplitudes, two new board sizes
and a longer non-wrapping horizon. Freeze the branch-identification and alias
convention: discrete sampling identifies frequency modulo 2*pi per update and
wave vector modulo lattice reciprocal vectors. Compare measured packet motion
with the derivative of the same fitted branch where that derivative is defined.
Do not reselect peaks, unwrap phases differently, or refit mass for each run.
These counts are a minimum protocol design, not a guarantee of identifiability.

For M2, use initially prepared colliding probes, retain outgoing probes and
radiation, and compare several strengths and timings. Counter magnitude,
`a^2+b^2`, and an activity centroid have no automatic energy, momentum or
position interpretation. Lost object identity is a failed tracking case.
The relative response of two objects to the same uncalibrated probe is useful
discrimination, but alone is not an inertial-mass ratio.

## Connection to complexity and internal evolution

An internal response parameter can affect transport, interaction and storage
without optimizing anything. The cooperation proxy and property-reversal
controls in [the operational protocol](../physics.md) remain separate tests.
A mass-like dispersion law would neither prove preferred-complexity selection
nor supply an evolutionary mechanism. Conversely, a route that requires more
cooperating sources would not establish mass, energy or gravity.

An evolutionary claim needs a registered population/lineage identity, internally
produced heritable variation, differential persistence or reproduction, and
resource accounting under the same autonomous dynamics. Long trajectories,
periodic retries and a successful prepared gate do not by themselves meet those
requirements. All canceled visible alternatives must retain their information
in the full reversible state. No fitness score or acceptance rule may be an
external instruction to the board.

## Sources and reading scope

Checked 2026-11-08. Equations and physical context are sourced below; the M0–M4
gates and Universe24 tests are our proposed protocol, not claims from these
papers.

1. Particle Data Group, *Kinematics*, 2025 Review of Particle Physics,
   sections 49.1–49.2. Official full PDF inspected, including four-momentum,
   velocity and center-of-mass relations:
   <https://pdg.lbl.gov/2025/reviews/rpp2025-rev-kinematics.pdf>.
2. G. M. D'Ariano and P. Perinotti, *Derivation of the Dirac equation from
   principles of information processing*, Physical Review A **90**, 062106
   (2014). Abstract and author-hosted published PDF inspected; its quantum
   assumptions and limited continuum regime are essential:
   <https://arxiv.org/abs/1306.1934>,
   <https://doi.org/10.1103/PhysRevA.90.062106>,
   <https://wordpress.qubit.it/wp-content/uploads/publications-dariano/1306.1934.pdf>.
