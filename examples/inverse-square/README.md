# Inverse-square probe: what the outward field law does and does not derive

This experiment asks whether Newton's inverse-square dependence follows from
the existing outward field transport, measured the way an outside observer
would measure it. The observer is not the event space: every number below is a
read-only host sample of node state after the run, placed at the observer's
Euclidean distance `r` from the source. No detector is planted inside the
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

Runtime: this branch, commit after `2155c9d`. Python 3.14, headless, no
visualization. `tests/test_inverse_square_experiments.py` checks the same
statements on a fast 15-cubed world.

### Gauss holds exactly on Manhattan shells

| Manhattan radius R | Nodes on shell | Shell stock / emission | Mean node value x (4R^2 + 2) / emission |
| --- | --- | --- | --- |
| 1 | 6 | 1.0 | 1.0 |
| 2 | 18 | 1.0 | 1.0 |
| 5 | 102 | 1.0 | 1.0 |
| 10 | 402 | 1.0 | 1.0 |
| 17 | 1158 | 1.0 | 1.0 |

Every closed shell carries exactly one tick of emission, at every radius. The
shell has `4R^2 + 2` nodes, so the shell-averaged density is exactly
`emission / (4R^2 + 2)`: the inverse-square law in its integral (Gauss) form,
with the lattice factor 4 where the observer's sphere has 4 pi. This is a
consequence of conserved transport and three-dimensional shell growth alone.

### Pointwise, the field is not isotropic

| Direction | Steps k | R | Observer r | Node value | value x r^2 / emission |
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

Log-log slopes of node value against the observer's `r` over steps 1 to 12:

| Ray | Slope |
| --- | --- |
| axis | -4.96 (exactly `emission / 6 / 3^(R-1)`, geometric) |
| face diagonal | -3.40 |
| body diagonal | -0.90 (close to `1/r`) |
| shell mean against R | -1.87 (tends to -2) |

The reason is the transport law itself. Each octant population keeps its octant
label and forwards one third of itself along each of its three outward axes on
every link. On a shell this is a multinomial distribution: the stock
concentrates in a blob of width about `sqrt(R)` around the body diagonal, whose
peak falls like `1/R`, while the axis nodes receive only the single all-same-axis
path, `3^-R`. The mean over the shell is inverse square; the value at a given
observer direction is not.

### The in-world force probe agrees with the host reading

Held receivers gain momentum by the delivered scalar flux of `radiation`. After
eighteen ticks each receiver's momentum equals seventeen ticks of the host-read
flux at its node (axis, step 1: 12,045,996 = 17 x 708,588). The "force" seen by a
receiver therefore obeys the same anisotropic law: geometric decay on axes,
about `1/r` on body diagonals, inverse square only when averaged over a shell.

### Localizing attenuation screens instead of following a power law

With schema 2 and retention 2/3, the moving value along the body diagonal falls
by a fixed factor of about 0.2 per link (2/3 times the transverse spread), and
each removed fraction stays as a deposit at its node. Emission 76,527,504 over
eighteen ticks left 68,044,736 units at rest and zero dissipation. The moving
field is exponentially screened, like a Yukawa potential, and the deposits form
a static distribution around the source; neither is Newton's law.

### Straight rays restore the observer's inverse square in every direction

The [ray candidate](../../docs/SPATIAL_FIELDS.md#straight-ray-transport-isotropic-ray-field-v1)
gives each emitted share its own heading and integer accumulators, so it moves
along one lattice line and never spreads. Time-averaged over one sweep of the
heading sequence, the host-read value at the observer's distance `r`:

| Direction | Steps k | R | Observer r | Mean node value | value x r^2 / emission |
| --- | --- | --- | --- | --- | --- |
| axis | 2 | 2 | 2.00 | 110,025 | 0.104 |
| axis | 4 | 4 | 4.00 | 20,759 | 0.078 |
| axis | 8 | 8 | 8.00 | 5,190 | 0.078 |
| axis | 12 | 12 | 12.00 | 3,114 | 0.105 |
| face diagonal | 3 | 6 | 4.24 | 29,063 | 0.123 |
| face diagonal | 8 | 16 | 11.31 | 4,152 | 0.125 |
| body diagonal | 2 | 6 | 3.46 | 41,519 | 0.117 |
| body diagonal | 5 | 15 | 8.66 | 7,266 | 0.128 |

Log-log slopes against `r` over Manhattan radii 1 to 16: axis -2.25, face
diagonal -2.05, body diagonal -1.92. All three rays now follow `1/r^2`; the
octant law gave -4.96, -3.40 and -0.90 on the same three rays.

The observer's own test compares each node's share of the flux with the solid
angle the node subtends from the source (`rho = 1` is perfect isotropy),
node by node and in 72 detector patches of 6 polar by 12 azimuthal bins:

| R | Nodes on shell | CV of rho per node | CV of rho per patch | Patch min / max | Empty nodes |
| --- | --- | --- | --- | --- | --- |
| 4 | 66 | 0.107 | 0.064 | 0.90 / 1.16 | 0 |
| 8 | 258 | 0.111 | 0.071 | 0.89 / 1.25 | 0 |
| 12 | 578 | 0.182 | 0.072 | 0.87 / 1.26 | 0 |
| 16 | 1026 | 0.335 | 0.078 | 0.81 / 1.20 | 5 |

At detector resolution the flux is isotropic to within about 7 percent at every
radius, and `mean value x r^2 / emission` stays at 0.115 from R = 4 to 16. The
remaining node-level graininess grows with R because 4,096 lines cannot cover
every one of 1,026 nodes evenly; it is finite sampling of directions, not a
directional bias, and shrinks with more headings. Every Manhattan shell still
carries exactly one tick of emission, and 544,195,584 emitted units were fully
accounted as resident, in flight or escaped through the open boundary.

## Conclusion

Two ingredients derive the observer's inverse-square law from local rules.
Conserved transport through growing three-dimensional shells gives the integral
form, `emission / (4R^2 + 2)` per node on average, under both candidates. The
pointwise, direction-free `1/r^2` additionally needs straight lines: shares that
carry their own heading and phase, so that flux dilutes purely by geometry. The
octant law spreads each share into a blob and fails that test; the straight-ray
law passes it to within the resolution of its finite heading set. No
gravitational constant, mass coupling or attraction law is claimed; the field
is a flux, and a receiver's response to it remains a separately configured rule.
