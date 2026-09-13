# Inverse-square probe: what the outward field law does and does not derive

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

Three headless runs on a periodic 41-cubed lattice, one link per tick, with a
stationary source that emits `8 * 3**12 = 4,251,528` units per tick so that the
octant/axis splitting stays exact for twelve links. Eighteen ticks reach a steady
state on every Manhattan shell up to radius 17 before any periodic return.

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

## Conclusion

For this tested transport regime, conserved moving stock distributed across
growing Manhattan shells gives exactly
`emission / (4R^2 + 2)` per node on average. Newton's pointwise, direction-free
`1/r^2` requires additional physical mechanisms and evidence. The present law
is anisotropic and concentrates stock near body diagonals. A different transport
candidate would need angular tests over host-defined spheres and
its own model identity, not a parameter of this one, and it must still satisfy
the locality and fixed-cost rules. No gravitational constant, mass coupling or
attraction law is claimed.
