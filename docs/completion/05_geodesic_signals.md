# Same-metric signals, conditional geodesics and proper time

The actual massive corrected full45 equations have the same scalar/Maxwell
characteristic cone determined by their retained frame. This is now proved
algebraically and tested on the same three-step Engine run as the clock workstream.
It does **not** yet establish a localized material trajectory, a measured
proper-time clock, or an Einstein continuum limit.

Baseline: PR50 `62202fdccdd9a40d5dbbec104de6f97d9587a999`.
Reproduce with `python -m validation.completion.geodesic_signals`.
Evidence: `runs/completion/05_geodesic_signals.json`, including source hashes.
Verified issue discussion: [same-metric result in #41](https://github.com/Closer24/Universe24/issues/41#issuecomment-6810847664)
and [allocation/acceptance crosslink in #40](https://github.com/Closer24/Universe24/issues/40#issuecomment-6810850747).
The script imports `formulation.equations` and `common45.build45/weak_seed`;
it does not duplicate a second physical law or call a trajectory solver in the Engine.

## 1. What was run

The shared law uses mass squared 1, coupling 1, physical step 1/64 and spatial
step 1/4. The exact initial slice has B=I, K diagonal -1/10, phi=1/5,
dust amplitude 1/10 and all other fields zero. All initial constraints vanish.
Previous registers are zero, the common denominator is 100, and all six legal
remainders are represented across 45 channels and 27 nodes.

- Tensor SHA256: `6ea453fa77a5a9d74af5bd4fc626cfcdc8f92942b10c301d2d00814bf4d05ba0`.
- Complete seed SHA256: `b53909631f3e14e3c09905275fe7b50a0dad2ecdec9ac431db2306127abd3b7c`.
- Retained state: 45 channels, 135 integers/node, zero added probe channels.
- Three actual Engine updates and complete rewind pass.
- Maximum integer lengths, including the initial slice: 7, 22, 51, 110 bits.

The common bundle audit checks all carries and the independent scalar oracle.
This script checks the characteristic/metric identities at its four snapshots.
Hashing before and after each passive read verifies that the read changes no state.
The actual seed is homogeneous and has no moving packet; the covector used in
the passive diagnostic is a test argument, not a retained excitation.

## 2. Derivation from the actual equations

The synchronous convention is

$$ds^2=-dt^2+\gamma_{ij}dx^i dx^j,\qquad
\gamma^{-1}=B^T B.$$

For a coordinate covector n let w=Bn and sigma=w dot w. The derivative part of
each real scalar component, ordered as (Pi,Xi_0,Xi_1,Xi_2), is exactly

$$A_{KG}(n)=\begin{pmatrix}0&w^T\\w&0_{3\times3}\end{pmatrix}.$$

The Maxwell block, ordered as (E,M), is exactly

$$A_{EM}(n)=\begin{pmatrix}0&C(w)\\-C(w)&0\end{pmatrix},
\qquad C(w)v=w\times v.$$

These equalities are extracted by differentiating the actual shared equation
builder with respect to derivative jets. Background values, frame entries and
n are symbolic. They are not fitted to numerical trajectories. The script
proves A cubed = sigma A and the trace identities for both blocks. Therefore
the propagating speeds are plus/minus sqrt(sigma), one scalar polarization per
real component and two Maxwell polarizations. The additional zero eigenvalues
are first-order reduction/longitudinal variables. The characteristic relation is

$$-\omega^2+n^T\gamma^{-1}n=0.$$

Mass, charge, potentials, K, connection and nonzero source fields enter only
lower-order terms in these matter blocks. **Massive Klein–Gordon PDE
characteristics are null.** Timelike massive trajectories require a different
mass-shell/semiclassical argument; they do not follow by relabeling a principal
eigenvalue.

An independent full, nonorthogonal frame with oblique n=(1,2,-1) gives
sigma=16381/900. A fixed Euclidean decoder gives 6 and fails both matrix
identities. On the actual expanding run, the same incorrect Euclidean metric
passes only at the initial B=I and fails at every evolved snapshot. All sampled
determinants are positive, but these samples are not a metric-domain theorem.

## 3. The precise massive limit and its source

Use signature (-+++), and write a controlled semiclassical equation

$$[\epsilon^2 D_\mu D^\mu-m^2]\psi=0,\quad
D_\mu=\nabla_\mu-iq A_\mu/\epsilon,\quad
\psi=R e^{iS/\epsilon},\quad k_\mu=\partial_\mu S-qA_\mu.$$

Direct substitution, separating real and imaginary parts, gives

$$k_\mu k^\mu+m^2=\epsilon^2\frac{\Box R}{R},\qquad
\nabla_\mu(R^2k^\mu)=0.$$

This holds locally where R is nonzero. If the amplitude correction is
controlled and negligible, k squared = -m squared. With F=dA,

$$\nabla_\nu k_\mu-\nabla_\mu k_\nu=qF_{\mu\nu},\qquad
k^\nu\nabla_\nu k_\mu=qF_{\mu\nu}k^\nu.$$

Consequently u=k/m is a unit timelike tangent and

$$u^\nu\nabla_\nu u^\mu=\frac qm F^\mu{}_{\nu}u^\nu.$$

Only in a force-free case does this give a geodesic. At finite epsilon the
gradient of the amplitude correction supplies another term, and k/m need not
be unit. A generic finite-width massive field must not be identified with an
exact point particle.

The code verifies the stress and current algebra **using the shared builder at
its actual mass and coupling, both 1**. At a constant-amplitude phase point,
phi=R, chi=0, Pi_chi=-R omega and Xi_chi=R k_spatial. On the local mass shell,

$$\rho=R^2\omega^2,\qquad j_a=R^2\omega k_a,\qquad
S_{ab}=R^2 k_a k_b.$$

Thus these particular field stresses agree with the leading single-stream
form T=R squared k tensor k; no separate particle stress is appended. The
current has the corresponding q R squared k form. This is a local source
identity, not a globally prepared plane-wave solution of all constraints:
nonzero charged density requires its Maxwell/geometry constraints to be solved.

The epsilon-family above is a continuum reference, not an implemented family
of immutable tensors. Holding the code's mass=1 fixed while merely narrowing
a packet does not establish the required timelike limit. In particular,
Geroch–Weatherall's tracking notion makes packets arbitrarily localized and
long-lived; their fixed-mass Klein–Gordon family cannot track timelike curves,
whereas allowing the mass parameter to increase admits them [2, §4]. This does
not prohibit useful finite packets; it specifies the missing limiting argument.

## 4. Proper time and observable phase

For the positive-energy local branch,

$$\omega^2=m^2+n^T\gamma^{-1}n,\qquad
v^i=\gamma^{ij}n_j/\omega,\qquad
\frac{d\tau}{dt}=\sqrt{1-\gamma_{ij}v^iv^j}=\frac m\omega.$$

The covariant phase accumulated along that ray satisfies

$$dS-qA_\mu dx^\mu=k_\mu dx^\mu=-m\,d\tau.$$

These equations use one metric throughout. The script checks their algebra,
including the gauge transformation S to S+q lambda, A to A+d lambda.
Bare phase fails that invariance test. A charged phase difference requires an
actual reference/transport comparison to become an operational reading.
Neither a hidden-state ratio nor an integrated oracle phase is a retained clock.

The already retained components support the exact identity

$$I(\Pi_\phi^2+\Pi_\chi^2)=S_0^2+J_0^2,\quad
I=\phi^2+\chi^2,\quad S_0=\phi\Pi_\phi+\chi\Pi_\chi,
\quad J_0=\phi\Pi_\chi-\chi\Pi_\phi.$$

The same decomposition holds spatially with gauge-covariant Xi. Where I is
nonzero, J_mu/I gives the covariant phase gradient. This consumes no retained
channel but supplies no material reference or detector. A circular internal
oscillation has constant I; intensity alone cannot read its phase. See the
companion clock audit for the homogeneous radial oscillator and expansion bias.

## 5. Independent geodesic and moving-time controls

For arbitrary positive a(t), the script builds Christoffel symbols directly
from diag(-1,a squared,a squared,a squared). For constant spatial covector p,

$$u^t=\sqrt{1+|p|^2/a^2},\qquad u^i=p_i/a^2$$

has exact unit normalization and zero geodesic residual. The null tangent
replaces u^t by |p|/a. Both residuals vanish symbolically. The held-out choice
a(t)=1+t squared/50 has nonzero curvature, so this is not just a Cartesian
flat-space control. The reference metric is deliberately independent of an
Einstein-source solution and is never asserted to equal the Engine history.

A separate Milne control uses ds squared = -dt squared + t squared dx squared
in one spatial dimension. Its exact moving solution has

$$\tau(t)=\sqrt{t^2+P^2}+\text{constant},\qquad
x(t)=\log\frac{t}{\sqrt{t^2+P^2}+P}+\text{constant}.$$

For P=4, t from 3 to 8, coordinate time is 5 and proper time is
4 sqrt(5)-5 = 3.9442719099991588. Derivatives, normalization and the general
geodesic formulas agree. This example is a nonconstant coordinate metric on
flat spacetime; it is a moving-clock oracle, not a simulated clock.

A constant electric field supplies a negative control: k^t=E+q F x and
k^x=sqrt((E+q F x) squared-m squared) have nonzero
k^nu partial_nu k^x = q F (E+q F x), but zero Lorentz-force residual. Calling this motion a geodesic
would fail the test. The variables in this oracle are not added to any lattice.

## 6. Evidence boundary and next falsifying experiment

| Requirement | Status | Evidence or remaining work |
|---|---|---|
| Common scalar/Maxwell metric and null cone | passed | Exact arbitrary-background builder identities |
| Wrong-metric discrimination | passed | Nonorthogonal oblique control and evolving snapshots |
| Conditional mass-shell stress and proper-phase algebra | passed | Actual source expressions, independent normalization/gauge controls |
| Independent curved/synchronous geodesic formulas | passed | Exact symbolic Christoffel residuals |
| Same-tensor three-step passive diagnostic and rewind | passed | Common tensor/seed hashes above |
| Engine-propagated localized massive/light packet | not_tested | Homogeneous seed contains no packet |
| Full moving material-clock period and relative redshift | not_tested | No retained clock reference, propagation or receiver |
| Stable continuum packet limit and finite-width errors | blocked | Time-map growth/instability and nonlinear constraint/domain gates remain |

A next physical test must prepare a constrained packet of the existing fields,
predeclare its width, wavelength, curvature and backreaction scales, and measure
its energy/current transport on the common Engine history with held-out
refinement. Charged tests must compare to Lorentz motion. A clock additionally
needs a retained reference/record and fixed calibration; the three unallocated
channels must cover all apparatus/arithmetic/memory together. An independent
eight-register position/momentum bank would exceed the contract and would
demonstrate an imported particle, not matter emerging from this law.

Finite-wavelength Maxwell energy flux can deviate from the leading eikonal
direction [3]. A correct principal cone alone therefore cannot certify an exact
ray at finite wavelength. Equally, analytic geodesics do not prove that this
candidate satisfies Einstein's equations.

## Primary literature read

1. S. R. Dolan, *Geometrical optics for scalar, electromagnetic and gravitational
   waves on curved spacetime*, [arXiv:1806.08617v1](https://arxiv.org/pdf/1806.08617v1),
   §§3.1–3.2: common null principal propagation, transport and its asymptotic regime.
2. R. Geroch and J. O. Weatherall, *The Motion of Small Bodies in Space-time*,
   [arXiv:1707.04222v2](https://arxiv.org/pdf/1707.04222v2), §4, especially pp.20–23:
   wave-packet tracking, fixed versus increasing KG mass, and charged motion.
3. S. R. Dolan, *Higher-order geometrical optics for electromagnetic waves on a
   curved spacetime*, [arXiv:1801.02273v3](https://arxiv.org/pdf/1801.02273v3),
   abstract and introduction: polarization-dependent subleading stress/energy flow.

The matrix, source, phase and oracle calculations above are this audit's own
derivations and exact checks. The papers do not certify the Universe24 tensor.
