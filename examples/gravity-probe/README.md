# Gravity probe: mass-proportional attraction toward a straight-ray source

This experiment composes existing rules only; it adds no engine law. A
stationary source emits the [straight-ray field](../../docs/SPATIAL_FIELDS.md#straight-ray-transport-isotropic-ray-field-v1)
`radiation`. A test body of mass `m` responds through an `exchange` coupling
whose amount is `m x flux(radiation) / D` with `D = 16`. The delivered flux
points away from the source, so the body's momentum moves toward it by `m`
times the flux, with the equal-and-opposite reaction landing in the local
`momentum` field at the body's Node. Every number below is a read-only
world/event audit at host Euclidean distance `r`; no operational observer is
modeled.

```sh
python examples/gravity-probe/run_experiments.py --output artifacts/gravity-probe
```

41-cubed open world, emission 4,096 units per tick over 4,096 golden-spiral
headings at scale 24, 64 rays per tick. Held bodies of mass 1, 2 and 4 sit at
the same Nodes along the axis, a face diagonal and a body diagonal. After one
64-tick sweep fills the domain, momentum gained over the next full sweep is
divided by the tick count and the mass: the host's "acceleration".

## Observed outcomes on 2026-09-13

Runtime source SHA-256 `53710d462fd4...` (full value in `summary.json`), Python
3.14, headless, no visualization. `tests/test_gravity_probe.py` checks the same
statements with six axis rays on a 15-cubed world.

### Attraction, inverse square, and the same acceleration for every mass

| Direction | Host r | Momentum gained by mass 1 over 64 ticks | Radial momentum per tick | a x r^2 x D / emission |
| --- | --- | --- | --- | --- |
| axis | 2.00 | (-424, 0, 0) | -6.63 | 0.104 |
| axis | 4.00 | (-80, 0, 0) | -1.25 | 0.078 |
| axis | 8.00 | (-20, 0, 0) | -0.31 | 0.078 |
| axis | 12.00 | (-12, 0, 0) | -0.19 | 0.105 |
| face diagonal | 2.83 | (-112, -128, 0) | -2.65 | 0.083 |
| face diagonal | 8.49 | (-12, -16, 0) | -0.31 | 0.087 |
| body diagonal | 3.46 | (-44, -56, -60) | -1.44 | 0.068 |
| body diagonal | 8.66 | (-8, -8, -12) | -0.25 | 0.074 |

Every gained momentum points toward the source. Log-log slopes of the mass-1
acceleration against host `r` over positive samples: axis -2.03, face diagonal
-1.94, body diagonal -1.92. The product `a x r^2 x D / emission` stays between
0.06 and 0.11 in every direction; the residual scatter is the finite direction
sampling already seen in the inverse-square probe. At every Node the three
masses report the same acceleration to the printed precision, because the rule
scales the momentum change by `m` and the carried integer remainder differs by at
most one unit per tick. Combined carrier plus local-field momentum is exactly
zero at the end of every run.

In these units the coupling constant is the configured `1 / D`: a body's
acceleration is about `0.08 x emission / (D x r^2)`, where the emission per tick
plays the role of the source mass. Nothing identifies `D` or the emission with
physical quantities.
