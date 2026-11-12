# Conserved charges give an exact native anisotropic sector

The selected candidate is an eight-channel, homogeneous diagonal Bianchi-I
model with a massless scalar and comoving dust. It extends the exact native
volume-history construction of [PR59](https://github.com/Closer24/Universe24/pull/59),
pin `228f581d02971435c0cd70548ff56267378ffc31`. It is a new explicitly declared
physical chart and tensor, not an equivalence claim for the massive spinor
candidate of PR60. There are no spatial gradients in this law.

The useful simplification is the conservation of scalar momentum, dust mass
and two independent shear charges. Their effects survive in a common Einstein
constraint while the volume acceleration becomes constant. This permits an
exact polynomial flow and a complete integer history encoding, without a
growing projective denominator.

## One continuum system

Use units `c=8*pi*G=1`, synchronous proper time, zero cosmological constant and
metric

\[
ds^2=-dt^2+\sum_{i=1}^3 a_i(t)^2 dx_i^2,\qquad V=a_1a_2a_3.
\]

Define the directional Hubble rates and conserved charges by

\[
H_i=\frac{\dot a_i}{a_i}=\frac{U}{3V}+\frac{S_i}{V},\qquad
\sum_i S_i=0,\quad P=V\dot\phi,\quad D=V\rho_d.
\]

The shared source has

\[
\rho=\frac{P^2}{2V^2}+\frac{D}{V},\qquad
\mathcal P=\frac{P^2}{2V^2}.
\]

The volume and charges obey

\[
\dot V=U,\quad\dot U=\frac32D,\quad
\dot D=\dot P=\dot S_i=0.
\]

The first integral is

\[
Q=U^2-3DV-\frac32\left(P^2+\sum_iS_i^2\right).
\]

Direct substitution into the Bianchi-I Einstein equations gives

\[
G_{00}-\rho=\frac{Q}{3V^2},\qquad
\frac{G_{ii}}{a_i^2}-\mathcal P=\frac{Q}{3V^2}.
\]

The off-diagonal components vanish for this diagonal homogeneous metric. The
independent metric audit reconstructs them from the full connection and Ricci
tensor. Scalar, dust and shear continuity follow separately:

\[
\ddot\phi+\frac{U}{V}\dot\phi=0,\quad
\dot\rho_d+\frac{U}{V}\rho_d=0,\quad
\dot\sigma_i+\frac{U}{V}\sigma_i=0,
\quad\sigma_i=S_i/V.
\]

Thus the tensor/source interpretation is more than a scalar constraint. No
massive scalar potential is present: adding one makes `P` nonconstant and
invalidates this exact flow.

## Exact flow and complete fixed-six realization

For any time increment `h`, the exact reduced flow is

\[
V_+=V+hU+\frac34Dh^2,\qquad U_+=U+\frac32Dh.
\]

Expansion verifies `Q_+=Q`; replacing `h` by `-h` is its inverse. Let `h=1/N`
and encode

\[
W=4N^2V,\qquad J=4NU=b_W-a_W+3D.
\]

The tensor contains nine linear monomials. Every channel has `u=6b`; the
volume additionally has `u_W+=18b_D`. In the unchanged Engine this gives

\[
a_+=b,\quad b_{W,+}=2b_W-a_W+6D,\quad r_+=r,
\]

because `2u` is divisible by six. Equivalently,

\[
W_+=W+J+3D,\quad J_+=J+6D.
\]

The exact integer invariant is

\[
\mathcal I=J^2-12DW-24N^2\left(P^2+\sum_iS_i^2\right)
          =16N^2Q.
\]

Both volume histories participate in momentum. Constants have prepared
`a=b`; the proper-time coordinate has `b-a=1`. Every channel retains its own
`a,b,r`, including nonzero remainders. No information is reset or discarded.

| Index | Channel | Role |
|---:|---|---|
| 0 | volume | Current volume and complete-history velocity |
| 1 | dust_charge | Conserved comoving dust mass `D` |
| 2 | scalar_charge | Conserved signed scalar momentum `P` |
| 3 | reference_velocity | Retained `4N Uref` integration anchor |
| 4 | scalar_offset | Retained scalar offset |
| 5 | proper_tick | Calibrated proper-time coordinate |
| 6 | shear1 | Conserved `S1` |
| 7 | shear2 | Conserved `S2`; `S3=-S1-S2` |

Total: **8 channels, 24 retained integers per node**, no scheduler or workspace,
degree one, no old-`a` tensor reads, strict onsite support. The single tensor is
identical at all three declared resolutions; only prepared scales and static
physical units differ.

## Metric and scalar readout from retained anchors

Let `K_flow=U²-3DV>0`, `q=sqrt(K_flow)`, and retain `Uref>q`. Define

\[
I=\frac1q\log\left[
\frac{(U-q)(U_{\rm ref}+q)}{(U+q)(U_{\rm ref}-q)}\right],\qquad
a_i=V^{1/3}\exp(S_i I),\qquad\phi=\phi_{\rm ref}+PI.
\]

Here `I_dot=1/V`. These are passive diagnostics of actual present volume,
complete-history velocity and retained charges/anchors. Elapsed tick count and
a cached reference trajectory do not generate metric or matter values. The
chart fixes the anisotropy factors to one at the retained reference; it does
not allocate arbitrary independent initial torus-shape moduli.

Off-constraint inputs use their actual `K_flow`, not the desired source value
`3(P²+ΣS²)/2`. They therefore remain off constraint. Preparation and readout do
not project them. A declared physical research bundle rejects a nonzero `Q`
without changing state.

The diagnostic uses exact rational differences before conversion and a
positive `log1p` ratio. If the anchor is in the future, current and reference
velocities are swapped and the logarithm is negated. Independent review found
that using a negative `log1p` argument could otherwise round to `-1` near the
branch and produce a spurious infinite metric. The corrected valid-domain
fixture uses `N=10^160, V=1, U=10^80, Uref=10^80+1`; its finite result agrees
with a separate 320-digit direct logarithm to better than `1e-55` relative
error. This changes neither tensor nor default seed.

## Executed common preparation

The selected nonzero-anisotropy seed is

\[
V_0=7/3,\quad U_0=4,\quad D=1,\quad P=2,\quad
(S_1,S_2,S_3)=(1,-1,0),\quad I_0=\phi_0=t_0=0.
\]

It has `K=9`, `Q=0`, and initial directional rates `(1,1/7,4/7)`.
For `N=24`, `W0=5376`, `J0=384`, `a_W=4995`; the full cube has 27 nodes,
and carries are `(channel+node) mod 6`.

Tensor SHA256:
`a51595cb6b4facd289fc40334527dc9ad4126c4f3244f70f8d5fcba53585231b`.

Complete `N24` seed SHA256:
`d1fcbb9266b7c9cb06ce10a33e900068ade4f83a01f7507c3f894efff103e1cc`.

| N | Actual updates to T=1/8 | Exact final V | Exact final U | Peak retained bits |
|---:|---:|---|---|---:|
| 24 | 3 | 2185/768 | 67/16 | 13 |
| 48 | 6 | 2185/768 | 67/16 | 15 |
| 96 | 12 | 2185/768 | 67/16 | 17 |

All exact rational physical fields agree at the common endpoint. Unlike a
convergent approximate integrator, the declared reduced flow is sampled
exactly; the root/log/exp diagnostic is evaluated at stated finite precision.

Thirteen native audit cases include all six uniform carry classes, mixed
carries, signed scalar/shear changes, a changed dust density, a different
anisotropy and the isotropic restriction. Three ordinary saved runtime runs
match the independent scalar recurrence register for register, reconstruct
the canonical click stream, verify replay and retain the runtime's untested
general physical acceptance gates. The canonical clicks are arithmetic
observations; they are not relabelled as autonomous material clock records.

## Long-time domain and cost

The complete state has closed polynomial formulas

\[
W_m=W_0+mJ_0+3Dm^2,\qquad J_m=J_0+6Dm.
\]

For a radius `M` including the old history,

\[
|W_m|\le |W_0|+M|J_0|+3|D|M^2.
\]

Other nonconstant retained data are the linear proper-time counter. For fixed
physical preparation, per-register bit length is
`O(log N + log(1+number_of_steps))`. This is a retained-integer size theorem,
not a claim that transcendental output has exact finite representation.

An actual **4,096-step** Engine run at `N24` reaches `T=512/3`,
`V=67591/3`, `U=260`, `Q=0`, with **26 peak bits**. Its 2,654,208 independent
scalar-register comparisons, every single-step inverse and full rewind pass.
The analytic bound is also 26 bits. At positive dust, volume and initial
expansion, `V(t)>0` for all future proper times. Positive scale factors follow
from the declared exponential chart; this does not extend the physical
interpretation through a past zero-volume singularity.

## Failure controls and boundary

Moving both volume histories by one leaves `I=-12` at every tested step;
the algorithm does not repair it. Changing a shear charge without compatible
initial expansion fails the sourced constraint. Removing the dust-to-volume
reaction also fails the constraint despite preserving arithmetic rewind.
Nonhomogeneous histories, nonfrozen charge histories, invalid carries and
inexact parameters are rejected by the declared interpretation checks.

This closes an exact, efficient **anisotropic homogeneous massless** sector.
It does not close massive-field dynamics, spatial Einstein constraints,
transported retained matter, an autonomous operational detector or uniqueness
of the physical law. The other five audits retain those distinctions.

Reproduce with `python -m validation.conservation_closure.native`.
Fresh evidence is `runs/conservation_closure/native.json` and its referenced
ordinary-runtime trace directories.

## Primary readings

- Capozziello, Marmo, Rubano and Scudellaro, [Noether symmetries in Bianchi
  universes](https://arxiv.org/pdf/gr-qc/9606050), §§2–3, equations (5)–(13).
  Read for the volume/traceless-anisotropy decomposition and cyclic scalar and
  anisotropy coordinates. Their discussed system omits ordinary matter; the
  dust source, normalization and native discrete embedding above are derived
  and checked here.
- Russell, Kılınç and Pashaev, [Bianchi I model: an alternative way to model the
  present-day Universe](https://doi.org/10.1093/mnras/stu932), §2, equations
  (5), (6), (10). Read for the directional Einstein equations and volume
  acceleration identity. The present report uses its own explicitly stated
  signature, units and massless-scalar-plus-dust source.
