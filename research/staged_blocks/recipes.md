# Assemble a signal, clock interface, reference and guide

These are four reusable **initial-data pieces**. Every runtime update still
comes from the unchanged Rule3 engine. The clock is prepared initially. The
finite validated behavior is synchronization to packet-arrival phase, measured
against a reference clock on the same board. An already aligned clock need not
change, so this is not an unconditional presence latch or a click per arrival.

```python
from research.components import TensorSpec, finalize
from research.experiments.run import run_experiment, recorded_states
from research.staged_blocks.recipes import (
    phase_assembly, relative_phase_observer, observe_relative_phase,
)

tensor = TensorSpec.from_signs((1, 1, 1))
assembly = phase_assembly(
    side=129, r=0, phase=0, delay=1, control="11", tensor=tensor,
)

# The ordinary immutable composer sees four pieces, not four runtime rules.
guide, packet, interface, reference = assembly.placements
prepared = finalize(assembly.board, (guide, packet, interface, reference))

# Freeze the passive observation before capture.
observer = relative_phase_observer(
    prepared.ports["interface.center"][0],
    prepared.ports["reference.center"][0],
)
recording = run_experiment(assembly.experiment_spec())
phase_data = observe_relative_phase(observer, recorded_states(recording["experiment"]))
```

Use `control="00"`, `"10"`, `"01"` or `"11"` for neither source, packet only,
target clock only or both. The reference is always present. These controls
remove only the designated initial counters; both full remainder fields and
all apparatus preparations remain identical. No source appears during a run.

For a complete four-control demonstration with the generic Presenter:

```bash
python -m research.staged_blocks.recipes --output /tmp/uni24-four-piece-phase
```

The output contains the frozen initial specs and passive observer, complete
native recordings, all arithmetic events, D/X traces and `The_Presenter.html`.
The Presenter displays recorded states and clocks; it does not perform the
comparison or choose an output. D/X values are computed by the research observer.

## What each piece owns

| Piece | Initial-state contract |
| --- | --- |
| `GuidedPacketSource` | Existing four-site packet and its complete retained halo |
| `InterfaceGuide` | Existing full periodic `(0,4)` guide, with explicit sockets for packet core and joint interface |
| `ClockGuideInterface` | Full 336-channel center/halo patch, unit clock at `ports[+Y][0]`, complete initial phase, and preserved untouched guide channel14 at remainder4 |
| Reference `ShieldedOrbit` | Existing isolated unit clock and full protected halo, placed beyond the registered influence range |

The joint interface is necessary because a generic clock halo has background
remainder2 on its unused channels, whereas guide channel14 must retain4.
`ClockGuideInterface` declares both requirements together. Its guide-facing
channel0 remainder also follows the initialized clock phase. The guide leaves
a socket for this patch, so composition does not overwrite a competing value.
Missing sockets, incompatible triples and conflicting protected channels fail
before evolution. Channel labels rotate with spatial placement through the
existing `place` API, but such alternate geometries require their own evidence.

`phase_assembly` returns an immutable `PhaseAssembly` with `board`, `placements`
and explicit evidence-domain metadata. Its `prepare()` delegates to the normal
finalizer; its `experiment_spec()` produces native data for the generic runner.
Seed 0 labels deterministic preparation provenance; no randomness is used.

## Scope and reconstruction

The validated family uses +++ coupling, unit clocks, center remainder0 or4,
all four initial phases, L129 or161, and delays1,2,3 or5. The full recordings
cover 40 updates, with the registered retained phase observation at states32–40.
Other board sizes or nonnegative delays require `exploratory=True`; this flag
marks a new investigation and confers no behavior guarantee. Other tensors,
amplitudes and center remainders are rejected by this interface API.

```bash
python -m research.staged_blocks.recipes --verify-domain /tmp/uni24-recipe-equality
```

This command compares the canonical complete initial-state bytes of all256
four-control preparations against the frozen phase-study producer and the
recorded initial-state hashes. It generates no trajectory. Splitting a study's
initial patch into four composable pieces must preserve every counter and
remainder, including untouched guide channels and reference halos.

The fixed observer reads

`D = a_target*a_reference + b_target*b_reference`

`X = a_target*b_reference - b_target*a_reference`.

It checks `D²+X²=I_target*I_reference` and retains every target/reference
arithmetic event, while the complete native recording retains the full board.
Under zero quotients both clocks rotate together and D/X remains constant.
The calculation is passive analysis across two recorded locations; it is not
an implemented physical comparator, approval signal or release mechanism.

Evidence: [frozen phase protocol](phase_protocol.json),
[complete result](evidence/interactions/phase_v1/result.json), and
[independent audit](evidence/independent_audit/phase.json).

## Reuse the effective coupler

The separate data-only [composed recipes](composed_recipes.py) expose the audited
transmission apparatus as three ordinary pieces. This preparation needs no
reference clock and adds no runtime switch.

```python
from research.components import TensorSpec, finalize
from research.staged_blocks.composed_recipes import effective_coupler

recipe = effective_coupler(side=137, delay=4, family="enable", control="11",
                           tensor=TensorSpec.from_signs((1, 1, 1)))
guide, packet, interface = recipe.placements
prepared = finalize(recipe.board, (guide, packet, interface))
spec = recipe.experiment_spec()  # Native data for the existing generic runner.
```

Its named ports include `guide.incoming`, `guide.forward`, `guide.backward`,
`interface.center` and the complete protected `interface.region`. Sources are
`packet.packet` and `interface.clock`. Control bits remove only those initial
counters; every initial remainder is retained within each family.

The finite domain is +++, L137/193, delays4/5/8/9, 40 updates. `family="enable"`
initializes phase `(2-delay)%4`; the complete outgoing carrier occurs in11.
`family="aligned_suppress"` initializes phase `(-delay)%4`; it occurs in10.
These families have different phase-dependent halo preparations. They are not
two settings applied during evolution. The forward criterion compares all48
channels throughout the full carrier template, including its halo, at
states24+delay through27+delay. Absence of that carrier is not absence of every
disturbance or loss of full-state information.

## Reuse the driven pause

```python
from research.components import finalize
from research.staged_blocks.composed_recipes import two_lane_pause

recipe = two_lane_pause(side=129, delay=0, control="11")
lower, upper, bridge = recipe.placements
prepared = finalize(recipe.board, (lower, upper, bridge))
spec = recipe.experiment_spec()
```

The three pieces are lower train/guide, upper train/guide, and clock/shared
halo. Their initial values are **solved jointly** using the frozen pure
preparation helper, then partitioned into immutable patches. Transverse
contributions are summed once before checking the valid remainder range.
Full clock-region resources are explicitly protected. Where a lane and the
protected region share an address, both declare the same triple; incompatible
triples fail composition. Adding independently prepared halo states would not
be equivalent to this construction.

Named ports include `lower.incoming`, `upper.incoming`, `bridge.clock`,
`bridge.center` and `bridge.region`. Sources `lower.train` and `upper.train`
follow the two control bits. `bridge.clock` is always present, and all four
controls retain the full common remainder field, including inactive-source
footprints. The domain is +++, L129/161, delays0/1/2/3 and40 updates.

For11, put `T=14+delay`. The full48-channel center is unchanged with zero
counters at statesT throughT+9; the designated channel is `(0,0,4)`. It restarts
at stateT+10 as `(0,1,0)`. Individual incoming terms cancel during part of the
pause. All other controls fail the complete two-train predicate. This is driven
waiting supplied by prearranged trains: autonomous336-region memory failed in
all eight geometries, and no independent approval computation is implemented.

Both constructors reject parameters outside their audited finite domains.
Their immutable metadata exposes tensor fingerprints, assigned resources,
source masks and evidence. Native specs can be passed to the existing
`run_experiment` and Presenter export pipeline; no constructor evolves a state.
Other placements or assemblies require new evidence before inheriting a claim.

```bash
python -m research.staged_blocks.composed_recipes --verify-domain /tmp/uni24-composed-equality
```

This read-only check compares complete initial-state bytes against all64
transmission and32 pause-apparatus recordings. The
[equality certificate](evidence/composed_recipe_equivalence/result.json)
reports96 matches and zero new trajectories. The six pristine train checks
remain separate evidence, not additional apparatus cases. See the independent
[transmission](evidence/independent_audit/transmission.json) and
[pause](evidence/independent_audit/bridge.json) audits for behavior and limits.
