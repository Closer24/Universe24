# Inverse-square probe: what the outward field law does and does not derive

For exact path counting, size/translation controls and an equal-Euclidean-radius
counterexample, see [the emergence validation](EMERGENCE_VALIDATION.md).

This experiment asks whether Newton's inverse-square dependence follows from
the existing outward field transport. Every number below is a read-only
world/event audit of node state after the run, placed at host Euclidean
distance `r` from the source. This is not an operational observer measurement.
No detector is planted inside the
world; the held receivers in the second run only confirm that the in-world
flux coupling sees the same numbers as the host projection.

```sh
python examples/inverse-square/run_experiments.py --output artifacts/inverse-square
```

Four headless runs on a 41-cubed lattice, one link per tick, with a stationary
source that emits `8 * 3**12 = 4,251,528` units per tick so that the octant/axis
splitting stays exact for twelve links. The three octant-law runs are periodic
and use eighteen ticks, a steady state on every Manhattan shell up to radius 17
before any periodic return. The straight-ray run uses an open boundary, 4,096
golden-spiral headings at integer scale 24, 64 rays per tick, and measures the
host-read node value on every tick of one full 64-tick sweep of the heading
sequence after a first sweep has filled the domain.

## Observed outcomes on 2026-09-13

These tables were reported with the probe introduced in commit `ca51869`.
New reports identify the runtime and probe by SHA-256. Python 3.14, headless,
no visualization. `tests/test_inverse_square_experiments.py` checks selected
shell and receiver identities on a fast 15-cubed world, not every table entry.

### Moving stock is constant across reached Manhattan shells

| Manhattan radius R | Nodes on shell | Shell stock / emission | Mean node value x (4R^2 + 2) / emission |
| --- | --- | --- | --- |
| 1 | 6 | 1.0 | 1.0 |
| 2 | 18 | 1.0 | 1.0 |
| 5 | 102 | 1.0 | 1.0 |
| 10 | 402 | 1.0 | 1.0 |
| 17 | 1158 | 1.0 | 1.0 |

Every reached shell in the tested pre-wrap regime holds one tick of emission. The
shell has `4R^2 + 2` nodes, so the shell-averaged density is exactly
`emission / (4R^2 + 2)`: a shell-count identity,
for this steady source and one-hop transport before periodic return. This is a
consequence of conserved transport and shell growth. The probe sums resident
stock, not oriented surface flux; it does not establish a physical Gauss law.

### Pointwise, the field is not isotropic

| Direction | Steps k | R | Host r | Node value | value x r^2 / emission |
| --- | --- | --- | --- | --- | --- |
| axis | 1 | 1 | 1.00 | 708,588 | 0.167 |
| axis | 4 | 4 | 4.00 | 26,244 | 0.099 |
| axis | 8 | 8 | 8.00 | 324 | 0.005 |
| axis | 12 | 12 | 12.00 | 4 | 0.0001 |
| face diagonal | 3 | 6 | 4.24 | 29,160 | 0.123 |
| face diagonal | 9 | 18 | 12.73 | 136 | 0.005 |
| body diagonal | 1 | 3 | 1.73 | 118,098 | 0.083 |
| body diagonal | 3 | 9 | 5.20 | 45,360 | 0.288 |
| body diagonal | 6 | 18 | 10.39 | 23,530 | 0.598 |

Log-log slopes against host Euclidean `r`, using positive samples within requested steps 1 to 12. The finite causal support limits face-diagonal samples to 1..9 and body-diagonal samples to 1..6; these are finite-range fits:

| Ray | Slope |
| --- | --- |
| axis | -4.96 (exactly `emission / 6 / 3^(R-1)`, geometric) |
| face diagonal | -3.40 |
| body diagonal | -0.90 (close to `1/r`) |
| shell mean against R | -1.87 (tends to -2) |

Within the exact integer-splitting range, each octant population keeps its octant
label and forwards one third of itself along each of its three outward axes on
every link. On a shell this is a multinomial distribution: the stock
concentrates in a blob of width about `sqrt(R)` around the body diagonal, whose
continuum approximation has peak scaling like `1/R`, while axis nodes receive only the all-same-axis
path, `3^-R`. The mean over the shell is inverse square; the value at a given
host direction is not. Beyond exact splitting, integer allocation phases matter;
finite fitted slopes are not proofs of asymptotic scaling.

### The in-world force probe agrees with the host reading

Held receivers gain momentum by the delivered scalar flux of `radiation`. After
eighteen ticks the axis receiver at step 1 has seventeen response cycles
(12,045,996 = 17 x 708,588). More distant receivers have fewer response cycles
because their input arrives later; their final momentum is accumulated response.
The selected receiver responses are direction dependent. The shell-stock
average above is a separate scalar measurement; it is not a vector force average.

### Localizing attenuation screens instead of following a power law

With schema 2 and retention 2/3, the moving value along the body diagonal falls
between consecutive diagonal samples (three Links apart), and
each removed fraction stays as a deposit at its node. Emission 76,527,504 over
eighteen ticks left 68,044,736 units at rest and zero dissipation. The moving
stock attenuates under the configured per-hop rule. Deposits remain at their
Nodes but continue accumulating during emission; neither is Newton's law.

### Straight rays give an inverse square in every host direction

The [ray candidate](../../docs/SPATIAL_FIELDS.md#straight-ray-transport-isotropic-ray-field-v1)
gives each emitted share its own heading and integer accumulators, so it moves
along one lattice line and never spreads. Time-averaged over one sweep of the
heading sequence, the host-read value at host Euclidean distance `r`:

| Direction | Steps k | R | Host r | Mean node value | value x r^2 / emission |
| --- | --- | --- | --- | --- | --- |
| axis | 2 | 2 | 2.00 | 110,025 | 0.104 |
| axis | 4 | 4 | 4.00 | 20,759 | 0.078 |
| axis | 8 | 8 | 8.00 | 5,190 | 0.078 |
| axis | 12 | 12 | 12.00 | 3,114 | 0.105 |
| face diagonal | 3 | 6 | 4.24 | 29,063 | 0.123 |
| face diagonal | 8 | 16 | 11.31 | 4,152 | 0.125 |
| body diagonal | 2 | 6 | 3.46 | 41,519 | 0.117 |
| body diagonal | 5 | 15 | 8.66 | 7,266 | 0.128 |

Log-log slopes against host `r` over positive samples within Manhattan radii 1
to 16: axis -2.25, face diagonal -2.05, body diagonal -1.92. All three rays are
close to `1/r^2` within this finite range; the octant law gave -4.96, -3.40 and
-0.90 on the same three rays.

The angular test compares each node's share of the time-averaged stock with the
solid angle the node subtends from the source (`rho = 1` is perfect isotropy),
node by node and in 72 detector patches of 6 polar by 12 azimuthal bins:

| R | Nodes on shell | CV of rho per node | CV of rho per patch | Patch min / max | Empty nodes |
| --- | --- | --- | --- | --- | --- |
| 4 | 66 | 0.107 | 0.064 | 0.90 / 1.16 | 0 |
| 8 | 258 | 0.111 | 0.071 | 0.89 / 1.25 | 0 |
| 12 | 578 | 0.182 | 0.072 | 0.87 / 1.26 | 0 |
| 16 | 1026 | 0.335 | 0.078 | 0.81 / 1.20 | 5 |

At patch resolution the stock is isotropic to within about 7 percent at every
tested radius, and `mean value x r^2 / emission` stays at 0.115 from R = 4 to 16. The
remaining node-level graininess grows with R because 4,096 lines cannot cover
every one of 1,026 nodes evenly; it is finite sampling of directions, not a
directional bias, and shrinks with more headings. Every Manhattan shell still
carries exactly one tick of emission, and 544,195,584 emitted units were fully
accounted as resident, in flight or escaped through the open boundary.

## Conclusion

For this tested transport regime, conserved moving stock distributed across
growing Manhattan shells gives exactly `emission / (4R^2 + 2)` per node on
average under both candidates; this is a shell-count identity, not a physical
Gauss law. The octant law is anisotropic and concentrates stock near body
diagonals. The straight-ray candidate, with its own model identity, adds the
one mechanism the pointwise direction-free `1/r^2` needs: shares that carry
their own heading and phase and dilute purely by line geometry. Its angular
test over host-defined spheres passes to within the resolution of its finite
heading set. Finite fitted slopes are not proofs of asymptotic scaling. No
gravitational constant, mass coupling or attraction law is claimed; the field is
a transported stock, and a receiver's response to it remains a separately
configured rule.
