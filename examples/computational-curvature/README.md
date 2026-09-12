# Computational-field curvature probe

This experiment asks one narrow question: does the existing Universe24 computation-field and local-cost machinery produce a curvature-like observable without inserting a gravity, geodesic or turning formula?

The probe deliberately separates three clocks that are easy to confuse:

1. **Global scheduler tick** — the coordinate-like time used to order events.
2. **Carrier local clock** — a stationary `local_clock` increments `clock_count` only when its own local cycle completes. Its `measured_cycle_cost` records the operation cost that sets that cycle's delay.
3. **Spatial-field clock** — configured spatial fields forward on the independent fixed `link_ticks` clock.

## Geometry

The default world is open and three-dimensional with shape `(25,17,7)`. The stationary mass source is at `(12,8,3)`. Two clock records sit at `(12,10,3)` and `(12,14,3)`, at Manhattan distances 2 and 6 from the source. A massless carrier probe travels in `+X` along `(y,z)=(12,4)`. A separate spatial wave travels in `+X` along `(y,z)=(12,2)`. Both pass the source at the same Manhattan impact distance 5. The detector plane is `x=21`.

The fields are:

- `mass`: stationary source inventory.
- `computation_field`: scalar outward field emitted by the mass source.
- `ray_token` and `direction`: a whole-record massless carrier probe.
- `clock_count`: completed local cycles of each stationary clock.
- `measured_cycle_cost`: the already-metered cost that drives each clock's local delay.
- `wave`: an independently transported local spatial field, streamed through `+X` with no turning rule.

No spatial coupling, force, geodesic correction or explicit trajectory rotation is configured. Therefore any lateral path change would have to arise from existing scheduling/transport behavior rather than a supplied gravity law.

## Measurements

`measure.py` runs five worlds and records an HTML playback for every run:

| Case | Mass | Normal local budget |
| --- | ---: | ---: |
| `control` | 0 | 32 |
| `weak_mass` | 64 | 32 |
| `strong_mass` | 512 | 32 |
| `strong_mass_tight_budget` | 512 | 16 |
| `strong_mass_loose_budget` | 512 | 64 |

For every tick it samples the computation-field value and spatial processing cost at the near clock, far clock and ray impact region. It records both local clock counters and their reported cycle cost, the carrier ray's sent/received positions, the spatial wave's resident/in-flight positions and both detector arrival times.

The independent readouts are:

- **Carrier coordinate delay:** detector arrival tick of `massless_ray` relative to the zero-mass control.
- **Spatial-wave coordinate delay:** detector arrival tick of `wave` relative to control.
- **Path bending:** maximum lateral displacement from each probe's original `(y,z)` line.
- **Clock-rate gradient:** local-clock cycles completed from tick 16 through tick 28, after both clock sites have had time to receive source influence.
- **Mass scaling:** whether increasing the configured source mass from 64 to 512 increases the carrier delay at unchanged computation budget.
- **Local causal link time:** every carrier `sent` event retains its explicit `arrival_tick - tick`; this distinguishes waiting at a node from slowing a link in transit.

## Acceptance rule

A full curvature-like signature is not declared merely because a carrier waits near an active field. For this probe it requires all of the following without adding a gravity-specific update:

1. positive carrier travel-time delay;
2. positive spatial-wave travel-time delay;
3. lateral carrier bending;
4. lateral spatial-wave bending;
5. a persistent near/far local-clock rate gradient after both sites are inside the established field; and
6. a stronger effect for the stronger mass source at fixed numerical budget.

A partial result is still useful evidence about the current simulator. In particular, a carrier delay with unchanged one-link transit is a local computation-delay effect; it is not by itself spacetime curvature. A spatial wave that ignores that delay demonstrates a clock-composition gap that must be resolved before identifying the result with gravitational light propagation.

## Run

```sh
python examples/computational-curvature/measure.py --output artifacts/computational-curvature
```

The output root contains `measurements.json` plus one directory per case. Each case contains the exact generated initialization, event stream, sampled measurements, final state and `run.html` playback. Measurement and rendering are read-only and never feed back into the simulation.
