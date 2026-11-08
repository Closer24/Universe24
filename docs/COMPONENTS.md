# Composing experiments from initial-state building blocks

The component library builds **one complete initial board**. The unchanged
Universe24 engine then applies Rule3 to every channel from the same previous
snapshot. Components do not survive as runtime objects with their own rules.

Code is separated by responsibility:

| Location | Responsibility |
| --- | --- |
| `universe24/` | Existing state, fixed coupling and sole Rule3 evolution |
| `research/components/` | Immutable initial patterns, placement and strict assembly |
| `research/experiments/` | Data-defined experiments, controls, complete recordings and passive observations |
| `research/component_studies/` | Separately declared scientific hypotheses, search budgets and acceptance criteria |
| `research/presenter/` | The same generic, read-only clocks-and-gears display |

## Run the composed examples

From the repository root:

```bash
python -m research.experiments.run \
  --spec research/experiments/examples/assembled_demo.json \
  --output runs/my-assembled-demo
```

Use a new output directory. The command records six experiments and creates
`runs/my-assembled-demo/The_Presenter.html`. Four cases combine two initially
prepared signal sources, a guide and a clock/memory receiver; the four source
controls are both, neither, first only and second only. Two cases combine a
source with open-left and neutral-right arms, with and without the source.

Open the HTML in a browser that executes its scripts, select an experiment,
press **Play**, and drag the cube to rotate it. **Look inside** shows all 48
channels of a node. **Focus retained state** makes a small apparatus readable
inside a large board. Exact counters and declared phase/memory readouts are
available behind the clocks. A normalized clock hand shows direction, so the
exact counters or phase predicates are needed to distinguish magnitudes.

A file-preview host may not run JavaScript. The Presenter reports startup
status and includes a static experiment inventory, but that static inventory
cannot play or rotate. See [opening instructions](PRESENTER_DELIVERY.md).

The smaller `examples/signal_memory.json` and `examples/paired_transfer.json`
use the same generic command. All paths in this paragraph are relative to
`research/experiments/`.

## Prepare a board in Python

For the newer period-five/period-six clocks, complete even packet, cooperative
pair and scoped scatterer/register assemblies, see
[Local building blocks: API, algebra and replay](LOCAL_BUILDING_BLOCKS.md).
They use this same composer and generic JSON runner. Their factories prepare
data only; a valid overlap contract does not establish functional composition.

```python
from research.components import (
    BoardSpec, SignalSource, GuideSegment, Receiver, place, finalize,
)

origin = (110, 110, 110)
prepared = finalize(BoardSpec(side=221), [
    place(GuideSegment(start=-20, stop=28, sockets=(-20, 0, 28)),
          at=origin, name="guide"),
    place(Receiver(), at=origin, name="receiver"),
    place(SignalSource(), at=(90, 110, 110), name="first"),
    place(SignalSource(), at=(138, 110, 110), name="second"),
])

states = list(prepared.engine.evolve(prepared.initial, 48))
receiver_addresses = prepared.ports["receiver.memory"]
```

This reproduces the retained counter-memory 20/28 preparation exactly. Both
signals exist at step zero; their later arrivals result from the closed-board
evolution. The JSON experiment runner adds full-state recording, inverse
audits, provenance and Presenter export around this same assembly boundary.

## Available recipes and their scope

| Recipe | Initial data | Named locations |
| --- | --- | --- |
| `SignalSource(a=0, b=1, present=True)` | Opposite counter pairs in channels 0 and 14, both with remainder 2 | `signal` |
| `GuideSegment(start, stop, sockets=...)` | Inclusive local x-segment, normally remainder pair `(4,0)`, with explicit unassigned sockets | `start`, `end` |
| `Receiver(remainders=(4,0), counters=((0,0),(0,0)))` | Two local channel triples; clock and memory are roles read from these same counters | `memory` pair; complete 48-channel `node` |
| `PairedArm(variant="O", direction=1, length=6)` | An initial arm of explicit length; sites 2 and 3 use O=`(4,0)`, N=`(2,2)` or R=`(0,4)` | `inlet`, all-48-channel `outlet`, `memory-2`, `memory-3` |
| `GuidedPacketSource(present=True)` | Four-site opposite-counter pattern and its complete transverse remainder halo; pair with a periodic `(0,4)` guide | `packet`, `front` |
| `Patch(kind, cells, ...)` | Arbitrary explicit initial assignments, including assignments equal to background | Declared ports, sources, sockets and readouts |

`PairedArm(gate_pairs=(pair_at_2, pair_at_3))` permits a separately specified
initial pair at each of the two memory sites. It supplies no dynamic gate.
All recipe parameters are initial data. An admissible recipe outside its
declared evidence domain has **unverified behavior**.

The exact generic reconstruction covers the 12 retained toggle runs, eight
counter-memory runs and 24 paired-transfer runs: all 1,868 complete states,
1,824 inverses, C/R events and detector input terms match their historical
records. The old preparations and evidence were left unchanged. The evidence
is in `research/experiments/evidence/assembly_v1/compatibility/report.json`.

These finite results do not establish arbitrary component reuse. A source
recipe is a candidate for signal preparation; physical light has not been
derived. An initialized oscillator can change its counters without another
arrival. A counted signal-triggered detector event and a board update are
different observables; the library does not force a clock to wait by pausing it.

## Guided propagation and connected examples

The same runner accepts `research/experiments/examples/guided_packet.json`.
Its assembly combines `GuidedPacketSource()` at `(0,L//2,L//2)` with
`GuideSegment(start=0,stop=L-1,sockets=(0,1,2,3),remainder_pair=(0,4))` at the same origin.
The source includes its complete remainder halo; no channels are discarded.
The six on/off controls at L=5,17,31 reproduce the audited whole-state packet
translation exactly. This domain requires a prepared periodic guide and the
`(+,+,+)` tensor; it is not a free-vacuum wave or a quiet waiting latch.

`research/experiments/examples/selected_examples.json` runs 24 selected
examples through the identical API: source/guide/clock/memory controls,
guided packets, matched-arrival OR/NO competition and its spatial swap,
a failed strict-waiting preparation, and actual routes driving receivers.
The receiver example has repeated clicks and loses the candidate record;
it is explicitly not a successful one-click memory. Existing immutable
portable records of all 1,234 new study runs, including every failed case,
are available in the complete replay collection described below.

The shorter `assembled_demo.json` remains useful as a six-case introduction.
A valid placement with another arm length, sign or orientation does not
inherit a behavioral guarantee. See [the result ledger](COMPONENT_RESULTS.md),
[waiting and packet scope](CONFIRMATION_BLOCK.md), and
[path selection scope](PATH_SELECTION_BLOCK.md).

## One tensor, explicit sockets and placement

`TensorSpec.from_signs((sx,sy,sz))` describes one of the eight existing fixed
body-013 tensors. It retains and validates the complete ports, weights and
fingerprint. `BoardSpec(..., tensor=...)` chooses that single tensor before
the run. Every patch must agree with it and with the board background. The
proposed 4096-tensor family is not implemented here.

`place(patch, at=..., name=..., orientation=0, wrap=False)` applies translation
and an explicit proper `2O` lift. Spatial coordinates rotate together with
channel labels. Ports, source addresses, socket addresses and local readout
clauses transform with the state. The two lifts of one spatial rotation remain
distinct channel transformations. Out-of-board placement is rejected unless
wrapping is explicitly requested; wrapping that aliases two different local
addresses is rejected.

Ports are names for existing addresses. They add no links to the lattice.
Guide sockets exclude source/receiver assignments from the guide and require
compatible fillers at finalization. They replace the old preparation's
implicit order of overwrites. An unfilled socket is an error.

The finalizer rejects conflicting triples, backgrounds, tensors, duplicate
placement names and independent sources sharing an address. Identical shared
assignments are permitted, with all owners recorded. It never adds counter
values or chooses a last writer. Explicit background triples remain in the
raw assembly manifest until conflicts have been checked; only the final
complete `State` uses the engine's ordinary sparse representation.

A valid preparation is not proof that its components still function together.
Source timing, phase, interference and reflected disturbances must be tested
with the complete composed state and controls.

## Data-defined recording and observations

An experiment has format `universe24-assembly-experiment-v1`, with an `id`,
`board`, `components` list and `steps`. A component specifies its `name`,
`recipe`, `params`, `at`, and optional `orientation` and `wrap`. A study uses
format `universe24-component-study-v1` and an `experiments` list.

`research.experiments.run.run_experiment(spec, output=None)` finalizes once,
records every state through the existing `capture` routine, audits exact
inversion and complete rewind, then computes fixed passive observations. Its
result contains `experiment`, `assembly` and `observations`. Counter-valued
observations use exact decimal strings, including arithmetic quotients.

`detectors` is a list of qualified port names, such as `receiver.memory`.
Each observer reports every retained triple, remainder change, original
arithmetic C event, counter magnitude and six signed input terms. No event is
suppressed to improve a scientific result. Existing C classification remains
`ell != 0` and a changed full triple; a remainder change is reported separately.

Fixed Presenter readout clauses may use a world `address`, or a `port` and
`index`, together with `component` (`a`, `b` or `r`) and an exact decimal
`equals` string. If a spec supplies `readouts`, those declarations replace the
recipe defaults before capture. A `view` selects an address for presentation.
Neither readouts nor view selection can alter a frame.

The spec also accepts documentary `question`, `controls`, `provenance` and
`seed` fields. Computation budgets specify `max_frames`, `max_cells`,
`max_bytes` and `max_seconds`. The full initial preparation, resolved tensor,
raw ownership manifest, source hashes, spec hash and complete recording are
saved. Runtime callbacks, injected sources and per-component tensors are
rejected. Resource exhaustion is inconclusive; a failure file preserves the
spec and reason, but the recorder does not promise a completed prefix trace
when capture aborts.

## Validation and scientific decisions

`tests/test_component_composition.py` covers conflicts, source controls,
observer independence and complete-state covariance for all eight tensors and
all 48 lifts. The independent review in
`tests/test_component_research_review.py` checks raw claims, metadata transforms,
all retained preparations and the generic observer against independent
arithmetic. New confirmation and route-selection studies have their own
protocols and results in `research/component_studies/`; their scientific
acceptance is independent of the assembly library's correctness.

To repeat the exact retained-interface comparison in a new directory:

```bash
python -m research.experiments.compatibility --output runs/my-compatibility
```

## Complete replay collection

The publication stores the complete historical delivery once in
`research/artifacts/Universe24_Components.parts/manifest.json`. The numbered
parts preserve the exact original ZIP bytes; the materializer verifies and
reassembles them in memory. Before running historical
audits, the complete collection command below, or the full test suite, restore
its declared evidence paths with:

```bash
python -m research.experiments.materialize_evidence
```

The materializer verifies the pinned archive and every restored file, refuses
conflicting existing files, and writes only declared research evidence. It
cannot overwrite the live engine, component recipes, runner, tests or docs.
The generic runner and the fresh examples themselves need no restoration.
Use **Python 3.11 or newer**, consistently with the repository requirement.


`research/experiments/collection.py` packages complete saved trajectories; it
does not run a search or filter outcomes. Its collection configuration names
every source and expected family count. It creates numbered JSON parts below
the Presenter limits (64 experiments and 500,000 stored cells), copies exact
compressed native recordings, checks all declared hashes, and writes a static
`index.html` and `manifest.json`. Open `The_Presenter.html` in a script-capable
browser and import any part with **Open experiment**. The selected examples
and every imported part use the same unchanged viewer.

```bash
python -m research.experiments.collection \
  --config research/experiments/examples/complete_collection.json \
  --output runs/my-complete-collection
```

The distributed `Universe24_Components.zip` includes the collection, generic
recipes and runner, data-defined examples, original frozen study protocols
and source snapshots, and a `START_HERE.md` with reproducible commands. The
packet animation comes from consecutive saved full states rendered by the
actual generic Presenter in a DOM/native-Canvas harness. It does not certify
Safari, iPad file previews, native pointer events or responsive CSS behavior.
