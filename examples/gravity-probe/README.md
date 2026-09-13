# Gravity probe: mass-proportional attraction toward a straight-ray source

This experiment composes existing rules only; it adds no engine law. Two
variants are run: an `exchange` coupling that moves momentum without any
energy, and a closed variant on signed quanta in which the pulled body pays for
its pull. In the first, a stationary source emits the [straight-ray field](../../docs/SPATIAL_FIELDS.md#straight-ray-transport-isotropic-ray-field-v1)
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

The closed variant keeps the world and the sweep but replaces the exchange with
[signed quanta](../../docs/SPATIAL_FIELDS.md#funded-emission-and-absorption).
The source emits `-1,048,576` quanta per tick, funded, over 4,096 mirrored
headings (2,048 golden-spiral headings and their exact negatives, so each
sweep's recoil is zero): it is credited with what it emits and every ray's
momentum, `amount x heading`, points back at it. A body absorbs the share
`mass / 256` of every ray that crosses its Node, pays that share from its own
`quanta` stock of `65,536 x mass`, and gains the share's momentum toward the
source. One mass per world, because bodies on one line shadow each other by
their share. A short world with the event audit on checks that every event is
closed.

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

### A moving body in the sparse field: discrete kicks, the same path for every mass

A body of mass 1 or 2 starts eight links out on the axis with zero momentum and
moves along its momentum at `min(1, |p| / (64 m))` hops per tick. With 64 rays
per tick spread over 4,096 headings, a single Node is hit only now and then, so
the fall is a sequence of discrete kicks rather than a smooth curve:

| Tick | Offset, mass 1 | Momentum, mass 1 | Offset, mass 2 | Momentum, mass 2 |
| --- | --- | --- | --- | --- |
| 32 | 8 | 0 | 8 | 0 |
| 40 | 8 | -8 | 8 | -16 |
| 48 | 6 | -20 | 6 | -40 |
| 64 | 1 | -20 | 1 | -40 |
| 66 | 0 | -20 | 0 | -40 |
| 96 | -9 | -20 | -9 | -40 |
| 112 | -14 | -16 | -14 | -32 |
| 139 | left the open boundary | | left the open boundary | |

Both masses occupy the same Node on every tick, with the mass-2 momentum exactly
twice the mass-1 momentum: the rule is mass independent by construction. Past the
source the body received a single outward kick and left through the open
boundary at 0.3 hops per tick; the inbound kicks it collected were too few to be
undone by the equally sparse outbound field. The small-world test in
`tests/test_gravity_probe.py`, where six axis rays hit every axis Node on every
tick, shows the dense-field limit: the body falls through the source, turns
between five and seven links past it with zero momentum, and comes back, a bound
oscillation with combined momentum still zero. An earlier configuration with
rate scale 8 let the body reach one hop per tick, where a ray moving the same
way can never catch it; that is why the scale is 64 here.

## Conclusion

Three statements follow from configuration on top of the straight-ray field:
momentum moves toward the source, its rate falls as `1/r^2` in every host
direction to within the finite direction sampling, and the acceleration does not
depend on the body's mass. The coupling constant is the configured `1 / D` and
the emission per tick stands in for the source mass. The reaction never reaches
the source, so this is attraction toward a fixed source, not a two-body law; a
smooth orbit in the sparse field needs more rays per tick or a slower body. No
physical constant, unit or mass is identified.

