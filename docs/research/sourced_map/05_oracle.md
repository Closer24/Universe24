# Independent physical time and source oracle

Baseline: `f4f64e062f07b3ca119eccf655df746be206908b`.
Run `python -m validation.sourced_map.oracle`.
Evidence: `runs/sourced-map/oracle.json`.

The joined six-channel native map passes an independent test of the five
physical homogeneous massless-scalar/dust equations at a fixed **proper**
time. This is an exact sampling result for the selected integrable sector,
not a test of general Einstein dynamics or an arbitrarily high numerical
convergence order.

The oracle reads actual Engine states. It independently reconstructs the
conserved coordinates from retained integers, compares that reconstruction
with `native.read_conserved`, checks the selected physical decoder against
an independent readout, and compares all five fields against a separate
high-precision integration of the original ODEs. Neither the reference
integrator nor the analytic solution feeds the Engine.

## 1. Physical equations and time convention

Use `c=1`, `8*pi*G=1`, unit lapse and zero shift. Let `a` be the spatial
FLRW scale factor, `B=1/a`, `H=a_dot/a=-k`, and let `tau` denote proper time
of comoving normal observers. `p=phi_dot` is the real scalar momentum and
`d^2` is the dust density. The selected decoder takes the positive dust
amplitude branch. With scalar mass squared `mu`,

\[
\begin{aligned}
\dot B&=kB,\\
\dot k&=3k^2-\tfrac12(\mu\phi^2+d^2),\\
\dot p&=3kp-\mu\phi,\\
\dot\phi&=p,\\
\dot d&=\tfrac32kd.
\end{aligned}
\]

These follow from homogeneous scalar/dust conservation and the FLRW Einstein
equations in the repository's sign convention. The exact constraint and
continuity identities are

\[
C=6k^2-p^2-\mu\phi^2-2d^2,\quad \dot C=6kC,
\]

\[
\rho=\tfrac12(p^2+\mu\phi^2)+d^2,\quad
\mathcal P=\tfrac12(p^2-\mu\phi^2),\quad
\dot\rho=3k(\rho+\mathcal P).
\]

The oracle derives these expressions independently and then symbolically
compares them with the actual existing `completion.formulation.equations`
builder at `mu=1`. The numerical reference calls only its independently
written five-component RHS. The projective denominator `D` in the older
six-channel sector is not a sixth physical field or a proper clock; the new
native dust variable called `D` below instead means comoving dust density.

For the massless system define

\[
V=B^{-3},\quad U=-3kV,\quad P=pV,\quad D=d^2V.
\]

Here `P` is a conserved scalar momentum, not a demonstrated electromagnetic
or quantum charge. Direct differentiation gives

\[
\dot V=U,\quad\dot P=\dot D=0,\quad\dot U=\tfrac32D.
\]

The last equation also holds for this massless off-constraint extension.
For the massive source equations it becomes
\(\dot U=3D/2+3\mu\phi^2V/2\); dropping that second term would change the
physical model. The native constraint is

\[
Q=U^2-\tfrac32P^2-3DV=\tfrac32V^2C.
\]

Thus preparing `Q=0` selects the physical solutions without a runtime
constraint projection. The original `B_dot=kB` is checked throughout; the
constraint by itself cannot check `B` because it does not contain `B`.

## 2. Independent exact and numerical references

The independently derived massless solution is

\[
V(\tau)=V_0+U_0\tau+\tfrac34D\tau^2,\qquad
U(\tau)=U_0+\tfrac32D\tau,
\]

\[
B=V^{-1/3},\quad k=-U/(3V),\quad p=P/V,\quad d=\sqrt{D/V},
\quad \phi=\phi_0+P\int_0^\tau\frac{ds}{V(s)}.
\]

The scalar integral is evaluated independently using the discriminant of
the quadratic in proper time. The production decoder instead uses the
present retained `U` and retained scalar anchor. These two calculations
agree at the observed states. The oracle also checks the constant-phi pure
dust branch and logarithmic pure scalar branch as independent continuum
controls; those branches are not accepted by the selected native chart.

The numerical reference uses 80-decimal arithmetic and an independent RK4
integrator with 256, 512 and 1,024 time intervals, followed by Richardson
endpoint extrapolation. Step-halving differences decrease by approximately
16. This is an empirical truncation-error estimate, not an interval enclosure
or a statement that all 80 digits are accurate. Against the separately
derived exact solution, the reference endpoint errors range from about
`6.25e-22` for pure dust to `7.08e-15` for the stronger-scalar fixture.

All references end at the same declared proper time `tau=1/8`. No coordinate
time is subsequently renamed to force agreement.

## 3. Actual native fixed-time comparisons

The main initial state is

\[
(B,k,p,\phi,d)=(1,-1,2,0,1),\qquad
(V,U,P,D)=(1,3,2,1).
\]

The oracle executes the actual Engine at `N=24,48,96`, with `h=1/N`, for
3, 6 and 12 nontrivial macro updates. Every observed time equals `n/N` from
the retained counter. Direct integer reads give exactly

\[
V(1/8)=355/256,\qquad U(1/8)=51/16.
\]

The physical endpoint is

| Field | Value at proper time 1/8 |
|---|---:|
| B | 0.89674824916111762018 |
| k | -0.76619718309859154930 |
| p | 1.44225352112676056338 |
| phi | 0.21170443766110203839 |
| positive dust amplitude | 0.84919182789484042567 |

All three resolutions have exactly the same rational endpoint invariants.
The largest physical readout disagreement with the analytic solution is
about `1.32e-81`, at the scale of 80-digit evaluation roundoff. The numerical
ODE reference differs by about `5.77e-20`, dominated by its own residual
truncation error. This is **exact sampling of this restricted flow**; the
report explicitly does not assign an infinite convergence order.

At every macro boundary the exact integer invariant is checked before
physical reconstruction, and every step inverts. Full rewind restores all
retained fields, histories and remainders. The report records each observed
macro state, physical readouts, tensor and complete seed/final-state hashes.

## 4. Held-out source response, with the same immutable tensor

All native source cases and resolutions use the same actual tensor
fingerprint. They change complete preparation and the static unit calibration.
There are 12 accepted native runs, each with at least three nontrivial volume
updates.

| Fixture at V=1 | P | D | U | Resolutions N | Updates to tau=1/8 |
|---|---:|---:|---:|---|---|
| Main mixed source | 2 | 1 | 3 | 24, 48, 96 | 3, 6, 12 |
| Opposite scalar momentum | -2 | 1 | 3 | 24, 48, 96 | 3, 6, 12 |
| Stronger scalar source | 22 | 1 | 27 | 48, 96, 192 | 6, 12, 24 |
| Stronger dust source | 2 | 10 | 6 | 24, 48, 96 | 3, 6, 12 |

All initial source constraints vanish exactly. Compared with the main case,
the stronger scalar gives endpoint `Delta B=-0.2858717709`,
`Delta k=-1.2996977412`; stronger dust gives `Delta B=-0.0846585105`,
`Delta k=-0.6396605575`. Each geometry is independently checked against the
original ODEs. Scalar sourcing enters the constraint-compatible initial
volume velocity even though the massless volume acceleration explicitly
contains only dust. The comparison changes the geometry preparation as
required by the constraint; it is not a claim that arbitrary source changes
at fixed initial geometry remain physical data.

Changing `P` to `-P` gives the same geometry and dust, opposite scalar
momentum and opposite scalar displacement. Its physical endpoint also agrees
with the independent ODE.

The stronger-scalar seed is correctly rejected at `N=24`: its retained past
slice lies outside the positive-volume expanding chart. That rejection is
preserved in the evidence. `N=48,96,192` keep both retained slices inside the
chart and still finish at proper time `1/8`; this is not a time relabel.

## 5. Controls that prohibit overclaiming

- **Wrong elapsed time:** substituting the exact solution at `tau=1/16`
  while claiming `tau=1/8` creates a maximum field error about `0.237812`.
- **Constraint-only false success:** freezing `B=1` while keeping the other
  exact endpoint fields still gives `C=0` but misses the true geometry by
  `0.103252` and fails `B_dot=kB`.
- **Massive relabel:** the same initial physical data have `C=0` also at
  `mu=1`, since `phi0=0`. Nevertheless, the independently integrated massive
  endpoint differs from the actual massless endpoint by about `0.0127081`.
  On the massless endpoint the massive constraint is `-0.04481877` and the
  massive scalar momentum equation has residual `+phi=0.21170444`.
- **Pure dust and contraction:** independent analytic and numerical ODE
  controls agree, but actual native preparation and the selected physical
  decoder both reject those branches. No native physical success is claimed
  for them.
- **Pure scalar:** its separate analytic logarithmic solution validates the
  reference ODE. Nonzero rational `P,U` cannot satisfy the native pure-scalar
  condition `U^2=3P^2/2`; the selected chart also requires positive dust.
  This remains outside the accepted native encoding.

Roots and logarithms are passive evaluations of declared physical coordinates,
not fundamental Engine arithmetic. They do not supply an independently ticking
clock or detector. The result establishes the particular homogeneous,
expanding, massless scalar-plus-dust sector and its proper-time sampling;
massive scalar evolution, spatially varying geometry, packet geodesics,
operational clocks and general Einstein acceptance remain separate tasks.
