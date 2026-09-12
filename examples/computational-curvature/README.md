# Computation-field timing and mixing probe

This version replaces the earlier fixed-direction *bending test*. A carrier
with a constant +X direction and a field streamed only through +X cannot bend
by changing its waiting time. That earlier arrangement remains a useful timing
control, not evidence that a scalar delay cannot bend a genuine wavefront.

## One law, configurable clocks

[configuration.json](configuration.json) is an **experiment settings file**, not
an engine initialization. [configuration.py](configuration.py) composes the
existing [six-mode local reflection candidate](../maxwell/configuration.py), a
source, local clocks and the ordinary field/control definitions into validated
engine JSON. There is no second simulator and no gravitational turning formula.

The settings explicitly contain the control-field definition and its local rule:
for each axis, add source-field receipts from the two opposite travel channels.
The resulting unsigned vector `axis_delay_control` can add the same coefficient
to both signs of that axis. This is one supplied local hypothesis. It is not a
spatial derivative, a global mass scan or a derived gravity law. Its effect on
timing follows [directional delay](../../docs/DIRECTIONAL_DELAY.md).

Six signed three-vector amplitude fields provide the wave modes. `mass` is the
stationary source inventory, not calibrated SI mass; `computation_field` is its
outward transported scalar stock. `clock_count` and `measured_cycle_cost` belong
to the held clock records. A control value is not the same quantity as the
operation count: state values and execution costs are measured separately.

The default world is 9 by 9 by 9, open, with eight scheduler ticks. It contains
three initially +X mode seeds at `(2,3,4)`, `(2,4,4)` and `(2,5,4)`, source
`(4,4,2)`, clocks `(4,4,3)` and `(4,7,3)`, and reception probe `(6,4,4)`.
All placements come from the settings and must be in bounds. The shared wave
candidate retains its fixed amplitude scale and eighteen-tick exact-arithmetic
limit. Do not extend a run beyond that law's tested arithmetic contract.

## Run

```sh
python examples/computational-curvature/configuration.py --output artifacts/directional-input.json
python -m event_universe --init artifacts/directional-input.json --output artifacts/directional-run
python examples/computational-curvature/measure.py --output artifacts/directional-comparison
```

Use fresh output paths. Normal runs are headless. An explicit `--visualize` on
the runner or comparison adds playback through the existing HTML generator;
no new renderer or GIF is supplied. To restore the old scheduler, omit the
`directional_delay` object or use unit weights, no control-field references and
`spatial_mode: "fixed"`. Equal weights with `cost` select isotropic **new spatial
waiting**, not the old field bypass. Nonuniform constant coefficients can also
be tested without any control fields.

The comparison includes fixed-clock control; isotropic cost timing with zero
and nonzero source strength; field-controlled directional timing with zero and
nonzero source strength; and a mixing-disabled negative control. Zero strength
retains the same source record and rule overhead but injects no source stock.
Mixing cases use the identical wave/control laws and initial mode seeds. Only
explicit source strength and timing selection differ.

## What is measured, and where

The ordinary runner preserves the exact generated initialization, runtime hash,
event journal, final state, local observations and declared accounting. Inputs
are stored separately from run output. The comparison's `measurements.json`
contains read-only summaries:

- **Audit arrival tick:** first completed nonzero wave reception at the selected
  probe node. Global timestamps are audit coordinates, not the observer's clock.
- **Local observer clock:** the completed carrier-transaction counter attached
  to the first wave receipt. It is not proper time or a material optical detector.
- **Transverse reception:** whether nonzero mode content actually arrived outside
  the initial beam lines. With mixing disabled, no transverse receipt should
  appear. Mixing itself must not be mislabeled gravitational deflection.
- **Accounting and squared amplitude:** linear declared balances at every tick,
  plus independently summed wave-mode squares over final resident, waiting,
  in-flight and escaped owners. This finite readout is not a universal energy law.

If a detector has not received the wave before the stop tick, its arrival and
mass-induced arrival difference remain `null` with `not_observed_within_window`.
A censored result is neither zero delay nor a failed mass-scaling law. The code
does not classify full curvature from these incomplete observables.

## Independent expectations and limits

A single incoming mode with amplitude `(0,4,0)` along +X must, under the selected
mixing rule, produce four transverse outputs: -2X through +Y, +2X through -Y,
and +2Y through each of +Z and -Z. Without mixing, that identical input travels
only +X. These values are checked independently, not read from a recorded movie.
This repairs the locked-direction defect without directing the wave toward a
known source coordinate.

A low-resolution single-mode pulse is not automatically a geometrical-optics
beam. Proper time, radar distances, convergence, representation-independent
clocks and a quantitative gravitational bending/time-delay law remain separate
acceptance work. In particular, the new spatial timing commits a prepared field
batch before its outputs wait; it is not a claim that every internal process now
shares one relativistic clock. See the timing contract for exact ownership.
