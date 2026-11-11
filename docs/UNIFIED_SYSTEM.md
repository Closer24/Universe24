# One Universe24 system with explicit channel ownership

> Historical research/reference document. The current supported interface and acceptance status are defined in [ONE_SYSTEM.md](ONE_SYSTEM.md). Commands and default-model descriptions below refer to the earlier construction; see [the 0.6 migration](MIGRATION_0_6.md). No general ≤48-channel physical model is accepted.


The default run constructs **one fixed tensor, one complete seed and one
Rule3 Engine**. It includes the Einstein physical component and the local
communication control. The transported-probe experiment can be included in the
same tensor explicitly. All state is retained and rewound together.

The physical metric has one authority: the evolved ADM metric. Complex scalar
matter and dark dust source it inside the Einstein component. The communication
receiver and the probe's independent test coframe are computational research
components, not extra matter species or alternative metrics for that board.
Placing components in one tensor does not by itself physically couple them.

## How many channels are needed?

There are **21 physical fields per event** in the current default model:

| Property | Independent fields |
| --- | ---: |
| Spatial metric | 6 |
| Extrinsic curvature | 6 |
| Lapse and shift | 4 |
| Complex scalar and its two momenta | 4 |
| Dark dust density | 1 |

Opposite scalar charge uses the same complex field, so it does not require a
duplicate universe or a second metric. Stress, current, constraints and the
four-dimensional metric are derived readouts with explicit arithmetic
dependencies. They are not additional independent evolution variables.

A physical field is not the same thing as an integer gear. A rational field
uses integer numerator/denominator expressions, and evaluation needs temporary
arithmetic and clock gears. With the default one-step Euler construction:

| Allocated range, inclusive | Owner / use | Channels |
| --- | --- | ---: |
| 0–98 | `einstein.clock`: finite computation clock | 99 |
| 99–4770 | `einstein.arithmetic`: inputs, retained work and outputs | 4,672 |
| 4771–4818 | `communication.ref`: reference receivers | 48 |
| 4819–4824 | `communication.comm`: six directed lanes | 6 |
| 4825–4850, when selected | `probe_experiment`: separate coframe, marker and clocks | 26 |

The default therefore has **4,825 channels per node**, or **14,475 retained
integers** counting `(a,b,r)`. On the 3×3×3 lattice this is 390,825 retained
integer entries per complete snapshot. These are counts, not a byte-memory
bound: integers grow. The optional probe needs odd `L >= 5`.

The counts depend on equations, integrator and requested horizon. They are
computed rather than hardcoded reservations. Two default Euler physical steps
require 11,111 Einstein channels plus 54 communication channels. Increasing
the horizon retains more work and larger integers. Neither 21 nor 4,825 is a
universal fixed channel budget for all matter theories.

## Why properties cannot overwrite one another

`core/channels.py` allocates a disjoint interval to every component, validates
unique namespaces and rewrites **every target and input factor** into that
owner's namespace. Duplicate owners, unknown names, incomplete/mismatched
seeds and exceeded budgets fail before evolution. No channel is released or
recycled while the compiled history is valid. Seed assembly copies all three
retained arrays and requires every owner exactly once.

Only the owning component's equations target its gears. The assembly API adds
no implicit cross-component reads or writes. `read_port` exposes a read-only
symbolic address; it does not create a new writer. Intended interactions must
be constructed and tested inside the owning coupled equation component, as
matter/geometry already are in ADM. The one-way communication receiver is
explicit inside its component and keeps its nonreciprocity designations.

Logical field readouts use `(physical step, property, numerator/denominator)`
keys. Two readouts may share an identical retained arithmetic subexpression.
That is safe read sharing: neither readout writes the common register, and
past snapshots are never reused as mutable slots for future properties.
`channels.json` lists every channel, owner and label, plus each physical
field's exact expression and readiness microtick. The board summarizes the
allocation and retains its per-field provenance display.

Computational clocks and workspace have audit labels. In the assembled run,
communication and probe gears also have audit labels. Labels affect only
observation, never Rule3. Standalone research runs retain their original labels
so historical evidence remains replayable.

## Pending work integrated

| Source | Incorporated behavior | Integration decision |
| --- | --- | --- |
| PR #27 / main | Nonlinear ADM, complex scalar, dark dust, constraints and event geometry | The single physical metric and source |
| PR #29, `90d8638` | Six message lanes, 48-channel receiver, preparation, passive edge logs and tests | Default companion component; standalone control retained |
| PR #30, `da66a78` | C2/cone audit, burst controls, exact readout bounds, figures and scheduler review | Passive research tools and negative results retained |
| PR #31, `37543d9` | 26-channel transported probe and candidate clocks | Explicit experiment; failed general common-metric gate stays false |
| PR #33, `d8e297b` | Nine-channel local arrival, C2 memory and response | Optional computational probe; no stress-energy or metric-null cone |
| PR #34, `d01e419` | Two-channel null-profile geometry and inverse certificates | Standalone restricted pp-wave sector; no generic matter or proper clock |

PR #33 and #34 were reviewed together and merged after 23 combined focused
checks and successful upstream CI. Neither supplies a general 48-channel
Einstein replacement. The new [eight-channel FLRW clock sector](COMPACT_FLRW_CLOCKS.md)
demonstrates indefinite-horizon prepared evolution with dust and radiation,
using eight actual channels and no padding. It is not added to the default
physical owner and must not overwrite the ADM metric.

The board's new proper-clock rates are passive contractions of the existing
four-metric. They allocate zero additional channels and add no second clock
law to the Engine. The normal rate equals the lapse; a fixed-grid clock has
squared rate `-g_tt` only when its tangent is timelike. Unit normal clock rate
does not imply flat spacetime. See the clock note for coordinate and observer
conventions.

The old PR #29 CLI is available as
`python -m universe24.demos.communication.run_communication`. The default
`reference_system()` remains the explicit 48-channel control;
`reference_system(communication=True)` constructs the 54-channel control.
No retired ONE module or variable-divisor API is restored.

PR #30's review patch applies only to the historical pinned source it reviewed.
Current ADM is already installed and fixed-six. That patch must not be applied
to the present package. Its finding about independent compiler clocks remains
relevant: adding message lanes does not make the ADM compiler message-driven,
asynchronous, or valid past its precompiled horizon.

The existing Palatini, pp-wave geodesic/proper-time and independent full-GR
checks remain under `experiments/geometry/`. They are comparison cases and
audits, not additional simultaneous physical metrics. Earlier variable-divisor
models remain in the historical archive, with their original provenance.

## Reproduce and inspect

```bash
# Allocation only: no Engine evolution
python -m universe24 --plan --out runs/channel-plan

# Default: Einstein and local communication in one Engine, exact full rewind
python -m universe24 --out runs/unified

# Explicit physical-only control
python -m universe24 --no-communication --out runs/einstein-control

# Include the independently labelled probe experiment
python -m universe24 --probe-experiment --L 5 --out runs/unified-with-probe

# Reject excessive allocation instead of dropping or overwriting properties
python -m universe24 --plan --max-channels 5000 --out runs/budgeted-plan

# Original communication and probe research controls
python -m universe24.demos.communication.run_communication --L 5 --tmax 20 --out runs/messages --rewind
python experiments/geometry/transported_probe_clock.py --replay runs/transported-probe/checked.json
python -m unittest universe24.tests.test_channels universe24.tests.test_communication universe24.tests.test_transported_probe -v
```

`component_events.jsonl.gz` records passive message edges and each component's
C0/C1/C2 counts. These are not physical particle counts. C2 does not establish
structural growth or an Einstein light cone. `full_trace.jsonl.gz` now uses
version 2 with explicit **both b and r deltas**, because the reference receivers
can change remainders. Version-1 traces remain readable. Rewind and trace replay
cover every owner, including clocks, messages and computational workspace.

See [unification evidence](evidence/universe24_unification.json) for measured
validation. Classical-scalar matter, single-stream dust, discretization and
finite-horizon limits in [INTEGER_ADM.md](INTEGER_ADM.md) still apply.
