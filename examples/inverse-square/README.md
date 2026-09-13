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

Three headless runs on a periodic 41-cubed lattice, one link per tick, with a
stationary source that emits `8 * 3**12 = 4,251,528` units per tick so that the
octant/axis splitting stays exact for twelve links. Eighteen ticks reach a steady
state on every Manhattan shell up to radius 17 before any periodic return.

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

## Conclusion

The inverse-square law is derived here only in its integral form: conserved
transport through growing three-dimensional shells gives exactly
`emission / (4R^2 + 2)` per node on average. Newton's pointwise, direction-free
`1/r^2` needs one more ingredient that the current outward candidate lacks:
isotropy, meaning the shell stock must spread evenly over the observer's sphere
rather than concentrate near body diagonals. That is a new transport law with
its own model identity, not a parameter of this one, and it must still satisfy
the locality and fixed-cost rules. No gravitational constant, mass coupling or
attraction law is claimed.
