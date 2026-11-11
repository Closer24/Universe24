# A repeating sourced geometric step within the 48-channel budget

This optional construction uses **eight actual channels**, with no empty
padding, clock bank, unrolled future or external evolution callback. It runs
the unchanged fixed-six Engine. It covers the expanding, homogeneous,
isotropic, spatially flat FLRW sector with noninteracting dust and radiation,
zero cosmological constant and a prepared big-bang origin. It is not a
general 48-channel Einstein solver or an equivalent replacement for ADM.

```sh
python experiments/geometry/compact_flrw.py --out runs/compact-flrw
python -m unittest universe24.tests.test_conformal_flrw universe24.tests.test_metric_clocks -v
```

## Geometry, sources and one shared clock interpretation

Use signature `-+++` and units `c=8πG=1`. Let three nonnegative integers
`A_m, A_anti, A_dark` label conserved comoving dust coefficients, let
`A=A_m+A_anti+A_dark`, and let nonnegative integer `B` label radiation.
For conformal time `η>0`,

```text
a(η) = A η² + B η
g = a² diag(-1, 1, 1, 1)
ρ_i = 12 A_i / a³             (three pressureless dust species)
ρ_rad = 3 B² / a⁴,  p_rad = ρ_rad/3
```

At least one source must be nonzero. Matter and antimatter here are labels of
two pressureless fluids with the same positive gravitational coupling. They
are not the default model's complex scalar, do not carry a retained U(1)
charge, and do not interact or annihilate. Radiation is an isotropic fluid;
its pressure enters the spatial Einstein equations. This includes no
anisotropic stress or arbitrary streaming matter.

The conformal Friedmann equations become

```text
(a')² = 4 A a + B²,       a'' = 2 A.
```

Radiation enters the first constraint and the initial conformal velocity;
its absence from `a''` is specific to this time coordinate and equation of
state. The full metric calculation gives

```text
G_ηη = 3(a'/a)² = ρ a²
G_ii = (a'/a)² - 2a''/a = p a²
G_μν = T_μν = 0 for μ != ν.
```

The source continuity equation also vanishes. A comoving observer is
geodesic, with proper time `τ=Aη³/3+Bη²/2`. An axial null test path is
`x=η-η0`, with affine parameter
`λ=A²η⁵/5+ABη⁴/2+B²η³/3`. It obeys `dλ/dη=a²`; its proper time is zero.
The null counter does not represent photon energy or move a packet across
board nodes. The affine normalization is chosen once by this formula.

The test independently constructs Christoffels, Ricci and Einstein tensors
from this four-metric using SymPy and checks both geodesic equations, their
norms and the source conservation equation. SymPy never supplies Engine
updates. The derivation follows standard FLRW equations; see
[Tong, Cosmology, sections 1.2–1.3](https://www.damtp.cam.ac.uk/user/tong/cosmo/cosmohtml/S1.html).
The compact integer encoding below is this repository's construction.

## Eight retained channels

Fix a positive integer resolution `Q` at tensor construction (`subdivision` in
the API and `--subdivision` on the CLI). It specifies
`Δη=1/Q` and passive readout units; it never changes the Engine divisor.

| Channel | Prepared integer value | Physical readout |
| --- | --- | --- |
| `clock.q` | `q` | `η=q/Q` |
| `geometry.s` | `Aq²+BQq` | `a=s/Q²` |
| `clock.c6` | `2Aq³+3BQq²` | `τ=c6/(6Q³)` |
| `light.l30` | `6A²q⁵+15ABQq⁴+10B²Q²q³` | `λ=l30/(30Q⁵)` |
| `dust.matter` | `A_m` | conserved dust coefficient |
| `dust.antimatter` | `A_anti` | conserved dust coefficient |
| `dust.dark` | `A_dark` | conserved dust coefficient |
| `radiation.b` | `B` | conserved radiation amplitude |

Each channel retains `(a,b,r)` as usual: 24 integer entries per node. There
are no additional retained arrays hidden in the observer. Bit lengths grow;
eight channels are not a fixed byte-memory bound. Conservation coefficients
stay constant while their physical densities dilute with the evolving metric.

## The fixed local step

All values on the right are from the same old `b` snapshot. Expand `A` into
the sum of its three retained channels:

```text
u_q   = 6q
u_Ai  = 6Ai;                   u_B = 6B
u_s   = 6s + 6A
u_c6  = 6c6 + 36Aq + 18BQ
u_l30 = 6l30 + 360Asq + 180BQs + 180A²q + 90ABQ
```

These are fixed integer polynomials of degree at most three, entirely onsite.
All inputs are multiples of three, so all valid remainders stay fixed and
`b_next=2u/6-a_old`. Preparing both histories at `q0-1` and `q0` proves by
induction that the polynomial identities in the table hold at every step.
They follow from the centered second differences of powers up to five. In
particular, `s_next-2s+s_previous=2A` is exactly the sampled acceleration
equation. No future values are seeded, stored in a table or injected during
evolution. The observer rejects nonhomogeneous or off-invariant histories;
the Engine still evolves such states reversibly without a GR interpretation.

This is a new symmetry-reduced model. It is not full-state equivalent to an
ADM run, the old 48-channel reference, or either pp-wave construction.
One-way designations describe the reduced recurrence; no generic reciprocal
potential for arbitrary off-sector channel states is claimed.

## What refinement establishes

The experiment advances actual integer states and replays every serialized
complete snapshot. Tests include pure matter, pure antimatter, pure dark dust,
pure radiation, mixed sources, 80-bit source coefficients, negative controls
that disconnect the metric/clock source terms, and exact inverse evolution.
Doubling `Q` while matching the physical endpoint produces identical rational
samples in this polynomial family, without allocating more channels. This
exact sampling result is not a convergence result for general inhomogeneous GR.

The default evidence run has 64 updates at `Q=16`, from `η=2` to `η=6`.
Fresh full traces and all samples are under `runs/compact-flrw`; a compact
source-hashed record is in [evidence/compact_flrw.json](evidence/compact_flrw.json).

## What clocks mean on the general ADM board

The default board now reads clock rates from its own ADM four-metric:

```text
(dτ/dt)² = -g_μν (1,v)^μ (1,v)^ν
         = α² - γ_ij (v^i+β^i)(v^j+β^j).
```

For normal observers `v=-β`, the rate is `α`. For a fixed grid observer `v=0`,
the squared rate is `-g_tt`; a nonpositive result is not a ticking timelike
observer. These exact contractions are passive and allocate no channels.
Only the displayed square root uses floating point. Rates are instantaneous,
not accumulated worldline integrals, geodesic solutions or redshift estimates.

In the default geodesic chart `α=1, β=0`, all normal clocks have unit rate
despite varying matter and curvature. Gravity also changes spatial distances,
relative motion and the comparison of clocks along different worldlines.
Reading `g_tt` alone does not determine the full Einstein geometry.

The general coupled model still sources one metric with the full classical
scalar and dark-dust stress tensor, including energy, momentum and stress.
Charge conjugation reverses the scalar charge without reversing its energy.
A cosmological constant, when selected through the API, enters `G+Λg=T`.
Gravitational radiation is encoded in the geometry; it is not another local
matter density to add to `T`. Electromagnetic/Dirac/quantum sectors and a
general repeating 48-channel update remain unimplemented.
