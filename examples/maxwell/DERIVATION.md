# Conditional vacuum Maxwell limit of local population scattering

This is an independent analysis of a proposed configuration on repository base
`fb083c159fe1f51612203962d9a7921683eb31c8`. It is not a new engine operation.
The configuration selects a local scattering hypothesis; locality, integer
arithmetic and conservation alone do not select this hypothesis uniquely.
The analysis below gives predictions before the corresponding simulator runs.
Measured acceptance belongs in the experiment report.

## Microscopic state and chosen rule

Let `n` range over the six unit travel directions, in the engine's order
`[+X, -X, +Y, -Y, +Z, -Z]`. A node owns one signed vector amplitude `a_n` for
each direction. Each amplitude is transverse to its own travel direction:
`dot(n, a_n) = 0`. Thus there are twelve independent scalar components, stored
in six ordinary vector fields. There are no geometric face or edge records.

Define two local moments for analysis:

\[
E=\sum_n a_n,\qquad B=\sum_n n\times a_n.
\]

These moments are interpretations of existing owned amplitudes, not additional
physical inventory. The letter `B` uses the same normalized amplitude scale as
`E`; conversion to SI electric and magnetic units has not been established.

The proposed local event uses this sequence:

1. Add the six local amplitudes and their direction cross products.
2. Remove the component parallel to the chosen outgoing direction.
3. Take half the difference between that transverse sum and the cross product
   of the direction with the second moment, then subtract the old amplitude.
4. Transfer each resulting amplitude through its own one-neighbor link.

In mathematical notation, let `T_n` remove the component parallel to `n`:

\[
T_n E=E-n(n\cdot E)=-n\times(n\times E),
\qquad
a'_n=\frac{T_nE-n\times B}{2}-a_n.
\]

Every right-hand side uses the same frozen local state. The entire scattering
proposal must pass its invariants before committing. Streaming then transfers
ownership without retaining a second copy. Incoming information has already
crossed its causal link; no step reads a neighbor's present state. All sums have
fixed size, and the same rule applies at every active node.

This selected cross-product mixing is additional microscopic structure. The
configuration contains no time derivative, spatial derivative, continuum force,
wave equation or Maxwell equation. Nevertheless, choosing the moment map and
this mixing specifically to obtain a Maxwell sector is a modeling choice. A
successful result would not prove that arbitrary conservative local rules must
produce electromagnetism.

## Exact local invariants

Treat the twelve transverse scalar amplitudes as one vector `a`, and let `M`
be the linear map taking it to the six components `(E, B)`. The six cardinal
directions satisfy

\[
MM^{\mathsf T}=4I,
\qquad
P=\frac14M^{\mathsf T}M,
\qquad
(Pa)_n=\frac{T_nE-n\times B}{4}.
\]

Consequently, `P` is an orthogonal projection and the collision is the reflection
`C = 2P - I`. It obeys

\[
C^2=I,\qquad C^{\mathsf T}C=I,\qquad MC=M.
\]

The local event therefore preserves the three components of each moment and
the nonnegative quadratic inventory

\[
Q=\sum_n a_n\cdot a_n.
\]

Exact integer evaluation and the transverse input constraint are part of this
statement. The implementation must reject an inexact division, failed invariant
or register overflow; the algebra does not permit rounding a failed proposal.

Periodic streaming permutes population owners, so the sum of `Q` over all
owners is also unchanged. At a snapshot, count retained and in-flight content
once each. The separate field names are not individually conserved: collision
can move amplitude between them. Their transformation ledgers must remain
consistent with the configured combined invariants.

`Q` is an exact microscopic quadratic invariant, not an established physical
energy. At a node,

\[
Q=\frac{|E|^2+|B|^2}{4}+|(I-P)a|^2.
\]

The last term describes six additional microscopic degrees of freedom. The
macroscopic electromagnetic energy proxy can exchange with that term during
streaming. An exact constant `Q` must not be reported as exact conservation of
the instantaneous collocated quantity `|E|^2 + |B|^2`.

## Long wavelength generator

This subsection is host-side mathematical analysis, not simulation evolution.
Use a Fourier convention with spatial phase `exp(i k dot x)`. Streaming has
the diagonal symbol

\[
D(k)_{nn}=\exp(-i k\cdot n),\qquad U(k)=D(k)C.
\]

At zero wave number, the six moment degrees of freedom have eigenvalue `+1`;
the six complementary degrees have eigenvalue `-1`. The latter alternate on
the microscopic time scale and are not additional vacuum photon polarizations.

For small `k`, write `D(k) = I - iN(k) + O(|k|^2)`, where `N` multiplies each
population by `k dot n`. Projecting the first-order generator onto the `+1`
sector gives

\[
\frac14MN(k)M^{\mathsf T}(E,B)
=\left(-\frac12 k\times B,\ \frac12 k\times E\right).
\]

It follows, conditional on this scattering law and a long wavelength,
low-frequency sector, that the leading effective evolution is

\[
\partial_t E=\frac12\nabla\times B,
\qquad
\partial_t B=-\frac12\nabla\times E.
\]

This is the normalized source-free Maxwell evolution with two transverse
polarizations and leading frequencies `omega = +/- |k| / 2`. The two
longitudinal moment modes are stationary at this order. On divergence-free
initial data, the leading equations preserve zero electric and magnetic
divergence. This is not yet an exact finite-grid Gauss theorem.

The predicted wave speed is **one half link per field tick**. The engine's
causal link speed remains **one link per tick**. No relabeling of time may erase
this distinction. Small-scale precursor or kinetic behavior can occupy the
larger causal cone even while the low-frequency wave travels more slowly.

## Independent finite-grid forecasts

The following numbers come from the twelve-dimensional matrix `D(k)C`, before
engine runs. They describe real-valued linear analysis; actual runs must still
establish exact integer execution and correct scheduling.

| Mode indices | Period in active directions | Positive low-frequency `omega` | Phase speed `omega / |k|` | Error relative to `1/2` |
| --- | --- | --- | --- | --- |
| `(1, 0, 0)` | 9 | 0.3490658503988659 | 0.5 | 0 |
| `(1, 0, 0)` | 15 | 0.2094395102393195 | 0.5 | 0 |
| `(1, 2, 0)` | 9 | 0.7672154454689077 | 0.4914676951343031 | -1.7064609731% |
| `(1, 2, 0)` | 15 | 0.4655332934913530 | 0.4970237415311709 | -0.5952516938% |

Here `k_j = 2 pi mode_j / period_j`. Axial dispersion is exactly
`omega = |k| / 2` in the low-frequency branch; the coordinate-permuted cases and
both transverse polarizations have the same prediction. Oblique modes have
finite lattice dispersion. Increasing the period from 9 to 15 makes their
error smaller without changing any microscopic rule or unit.

Thin periodic transverse directions are sufficient for a spatially uniform
plane mode: `9 x 3 x 3` and `15 x 3 x 3` retain the same three-dimensional
six-link rule. The asymmetric oblique examples need `9 x 9 x 3` and
`15 x 15 x 3`. A localized pulse still requires all three dimensions to vary.
These are small-domain mode tests, not an extrapolation to an unlimited universe.

## Frequency measurement without assuming the answer

Prepare an electric-only standing mode with `B = 0` and initialize populations
in the moment subspace using `P`. Read the electric Fourier amplitude along the
initial polarization from the recorded engine states. Use only the same physical
phase of each completed field interval.

For sixteen field steps, take nine even-time samples `x_n` at times
`0, 2, ..., 16`. Define `y_n = x_(n+1) - x_n` to remove a static offset. The
kinetic branch near `pi` folds onto the same oscillatory branch at these sample
times. Fit the one coefficient `q` by the fixed least-squares recurrence

\[
q=\frac{\sum_{n=1}^{6}y_n(y_{n-1}+y_{n+1})}
        {2\sum_{n=1}^{6}y_n^2},
\qquad
\omega=\frac12\arccos q.
\]

Report the recurrence residual as well as the frequency. A zero denominator
means that this estimator has no frequency evidence; it is not a zero-frequency
measurement. A coefficient outside the real cosine range is a failed fit, not
permission to force it onto a desired answer. The chosen modes have
`0 < omega < pi/2`, so this sampling does not identify a different low branch.

Prespecified checks for a clean linear mode are a normalized recurrence residual
below `1e-8`, frequency within `1e-8` of the independent matrix forecast,
matching axial polarizations/axis permutations, and smaller oblique speed error
for period 15 than period 9. The Fourier analysis and trigonometry are read-only
host diagnostics. None of their values enters a node update.

The matrix comparison checks implementation. The comparison against the
continuum speed, transverse behavior, conservation and convergence checks the
physical interpretation. Neither alone establishes complete electromagnetism.

## Gauss counterexample to an exact finite-grid claim

A continuum-transverse polarization at oblique `k` need not be transverse to the
centered-grid derivative, whose Fourier direction is `sin(k)` componentwise.
Starting with such data and observing nonzero centered divergence would not
demonstrate that evolution created it. Initial divergence must be measured.

A stronger control starts from an integer scalar potential `phi` and prepares
the initial moment

\[
E=(\delta_y\phi,-\delta_x\phi,0),\qquad B=0,
\]

where each `delta` is the difference of values one node forward and one node
backward. These commuting integer differences make the initial centered
divergence exactly zero. They are initial preparation and diagnostic operators,
not physical nonlocal reads in the update rule.

For a `(1, 2, 0)` mode on period 9, the proposed rule is predicted to produce
nonzero centered electric divergence **after the first field step**. In the
unrounded Fourier analysis, its magnitude normalized by
`|sin(k)| |E_initial|` at steps `0, 1, 2, 3, 4` is approximately
`0, 0.135572659, 0.143748691, 0.161782867, 0.297950045`.
For period 15 it is approximately
`0, 0.051468565, 0.021479064, 0.052940831, 0.068603213`.
Magnetic divergence stays zero in this particular planar polarization by
symmetry; that is not a general magnetic Gauss proof.

Thus the candidate can have a Maxwell long wavelength generator while failing
an exact collocated centered Gauss constraint. The finite-wave-number static
sector instead involves the direction `tan(k_j / 2)` and additional population
information. A modified discrete charge/divergence definition would need its own
local ownership contract and independent proof. Do not silently switch the
measured operator after a failed test.

## Integer lifetime and remaining scope

The collision contains exact halves. If every initial population component is
a multiple of `2^T`, at least `T` scattering phases have an integer divisibility
budget under this linear rule. Initial preparation with `P` contains quarters
and needs an additional factor of four in the supplied moment amplitude.
These are fixed initial conditions; the simulator must not scale amplitudes up
as a run progresses. Payload and intermediate invariant registers must fit their
existing bounds throughout.

This finite experiment is not a closed rule for arbitrary integer seeds for
unlimited time. A smallest-amplitude counterexample should fail visibly on an
inexact half. Preserving both exact quadratic invariants and unrestricted
quantized mixing may require a different integer scattering law; adding a
generic remainder does not by itself prove the quadratic invariant.

Required controls include disabled scattering, both polarizations, coordinate
rotations, an axial longitudinal seed, an electric-only seed, the oblique
divergence counterexample, and the exact-division boundary. Report failed
physical conditions as failures even when the software correctly detects them.

No charge/current source, continuity-compatible Gauss law, Lorentz force,
material constitutive law, quantum photon, full Lorentz symmetry or derivation
of the physical speed of light is established by this candidate.

## Related primary work

[Simons, Bridges and Cuhaci, 1999](https://people.csail.mit.edu/nhm/EMLGA.pdf)
studied a different polarized integer lattice-gas automaton and compared cavity
mode frequencies. Their paper explicitly distinguished numerical evidence from
an unproved macroscopic-limit derivation. It provides context for the evidence
standard, not verification of this specific reflection.

[Mendoza and Munoz, 2008](https://arxiv.org/abs/0806.2678) derived a Maxwell
continuum limit for a different three-dimensional lattice-Boltzmann model with
auxiliary vectors and selected collision equilibria. That construction is not
the six-population configuration analyzed here, and its results are not imported
as proof for this model.
