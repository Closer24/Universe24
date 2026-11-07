# Staged building blocks: preparation, composition and evidence

All objects in this package prepare initial data or read completed recordings.
They add no evolution rule. The reference model remains one periodic cube,
48 channel triples per node, six spatial ports, fixed body actions `(0,1,3)`,
one globally selected sign triple, and the same scalar Rule3 at every update.
Every update reads the same complete preceding state.

## Reuse and interfaces

The package reuses `research.components` and `research.experiments.run`.
The older `research.building_blocks.preparation` contains specific initial
source/guide studies; it is evidence for those domains, not a second engine or
a general composition API. New catalog entries refer to the immutable generic
recipes instead of duplicating those older preparations.

```python
from research.components import BoardSpec, Receiver, place
from research.staged_blocks.composition import (
    RunContext, ComponentPreparation, compose_initial,
)

context = RunContext(BoardSpec(33), seed=0, time0=0)
memory = ComponentPreparation(
    place(Receiver(remainders=(4, 2)), at=(16, 16, 16), name="memory"),
    side=33, seed=0, time0=0,
)
prepared = compose_initial(context, [memory])
```

`compose_initial` delegates final assembly to the existing finalizer after
checking the side length, seed, time zero, background, complete tensor and
transformed channel resources. A seed is preparation provenance, not a runtime
random source. Components cannot introduce their own board or tensor. Different
channels at the same spatial node may coexist. An identical shared initial
triple is permitted unless a component explicitly reserves that channel.
Incompatible values produce an error naming the world address, owners and
triples; no writer wins silently. Spatial rotation transforms channel labels
as well as coordinates. Source identity, sockets and periodic alias checks
remain enforced by the existing finalizer.

`experiment_spec` converts those same patches into the native experiment JSON
and verifies equality of the reconstructed initial state. `source_off_state`
zeros only selected declared source counters. `validate_source_off` checks the
entire state, tensor, background and ports, including every retained remainder.
The default four-block control removes `carrier.packet`; it preserves the
already prepared clock. Its complete board therefore need not be stationary.

## Four-block demonstration and interaction investigation

```bash
python -m research.staged_blocks.composition --output /tmp/uni24-composition
```

The command writes `protocol.json` and `registration.json` before any evolution,
then complete native records, `result.json`, a generic experiment bundle and
`The_Presenter.html`. Every retained arithmetic C0, C1 and C2 remains visible.
The returned Python result also contains the unchanged native experiment
dictionaries for a combined Presenter. Existing output directories are rejected.

The default board is L33 with +++ coupling, 24 updates and seed 0. Four runs
contain four available preparations: a full periodic `(0,4)` guide, the exact
guided packet at X4..7, a separate prepared shielded clock, and a Receiver
initialized with remainder pair `(4,2)`. Source-on/off controls preserve the
same apparatus. All instances are exact initial triples; no block object runs
after finalization.

In the **isolated arrangement**, the carrier lane is at Y8,Z16, the clock at
`(16,24,16)` and the passive receiver at `(16,16,24)`. Acceptance checks exact
carrier translation, the complete clock-region four-cycle, and an unchanged
passive record. Passing establishes coexistence in this declared geometry.
It establishes neither signal capture nor a clock activated by light.

In the **connected arrangement**, the receiver moves to `(16,8,16)` and fills
a guide socket. The clock remains separate. The report distinguishes any
source-induced full48 receiver change from the stronger registered pending goal:
zero counters on all receiver channels through state 17, no receiver arithmetic
C through update 17, and exact target pair `(2,4)` with the other 46 remainders
equal to 2 at every state 9 through 17. Later events through the entire horizon
remain recorded. Interaction is useful evidence even when this pending goal
fails. A directly initialized Receiver is not a light-written memory.

`example_specs` also admits side>=33 and 24<=steps<=40 with the same declared
geometry rule. These are parameterized investigations, not automatic extensions
of the accepted evidence domain. The full periodic guide is apparatus, and
packet recurrence is visible if the run reaches it.

## Stage graph and fixed observations

`load_catalog()` reads `stages.json`. Its statuses distinguish a mathematical
claim (`proven`), a data recipe (`prepared`), finite accepted evidence
(`observed`), an investigation (`search`), and an unavailable capability
(`not_demonstrated`). Evidence and scope are required. `stage_report(id,
purpose="claim")` exposes unmet prerequisites; `require_stage` raises for a
blocked claim or deployment. An investigation is still runnable. A successful
run does not edit its own catalog status or promote downstream capabilities.

Quiet capture and orbit capture have distinct contracts. The quiet-memory
stage does not require a pre-existing clock. Orbit capture requires a separately
fixed full center-and-halo predicate and testing of the four arrival phases.
Either could eventually support waiting, but one cannot rescue the other's
failed predicate retrospectively. Evidence review must name the accepted
alternative and its domain before updating the catalog.

The pure `state_observer`, `orbit_observer` and `click_observer` builders freeze
data-only predicates. `observe_states` reads retained states without an engine
or mutation callback. Orbit observations check both membership and phase
advance; arithmetic observations retain all three C classes. Research code
must register these predicates before searching its validation family. Their
output never supplies an input to Rule3.

## Subsequent contracts

- **Approval/release:** a returned disturbance caused inside the board releases
  stored incoming information. Neither input alone may counterfeit release.
  Duplicate and late messages must be tested; a deadline must itself be
  represented by ordinary initial data and evolution.
- **One-to-two split:** a single incident pattern yields two predefined outgoing
  patterns at two spatial ports; the null control yields neither. This does
  not establish physical photon splitting or physical energy conservation.
- **Router:** two individually functional directions produce exactly one
  accepted outlet under an internally represented choice. Any symmetry-breaking
  preparation is explicit. No external comparison, tie chooser or deletion is
  allowed during evolution.
- **Finite acknowledgment:** a finite declared candidate family retains
  branch-specific obligations. Duplicate completion from A cannot settle B.
  All required completion information must reach the decision's causal past.
  Missing approval leaves the apparatus waiting within its specified horizon.

Every canceled or unselected candidate remains distinguishable in the complete
reversible state. Observed exclusivity is not full-state erasure. Exact entry
from a nonperiodic complete state into a global periodic attractor is impossible
for a bijective evolution; an incoming-capture construction needs continuing
external/history dynamics. None of these contracts proves quantum collapse,
entanglement, the Born rule or identification of a board disturbance with an
observed photon.
