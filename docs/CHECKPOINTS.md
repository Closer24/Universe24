# Exact simulation checkpoints

A checkpoint stores the complete state of the canonical `Simulation` at a
completed `step()` boundary. Loading restores that state directly. It does not
rerun prior ticks, redraw a recorded quantum outcome, or regenerate a pending
physical proposal. This differs from a display snapshot, which deliberately
omits state required to continue the physical computation.

```python
from pathlib import Path
from event_universe import Simulation
from event_universe.initialization import load_initial_state

world = Simulation(load_initial_state(Path("examples/topology/bcc_vectors.json")))
for _ in range(3):
    world.step()
world.save_checkpoint(Path("outputs/saved-encounter/checkpoint.json"))

events = []
resumed = Simulation.from_checkpoint(
    Path("outputs/saved-encounter/checkpoint.json"), observer=events.append
)
resumed.step()  # Continues at tick 3; the completed step ends at tick 4.
```

The host functions `event_universe.checkpoint.save_checkpoint(world, path,
initialization=None, lease=None)` and `load_checkpoint(path, observer=None)`
provide the same functionality. Parsed initial states carry their normalized
source JSON. A manually constructed `InitialState` must provide its original
valid initialization JSON through the explicit `initialization` argument;
the parsed configuration must equal the world's initial state.

The runner saves at its final successful tick with `--checkpoint PATH` and
continues a saved file with `--resume PATH`. On resume, an explicit `--ticks N`
means **N additional steps**. Omitting it runs the remaining configured duration,
`max(0, initial.ticks - saved_tick)`. A checkpoint inside the run output must be
named `checkpoint.json`; the runner protects original inputs from replacement.
Use a new or empty output directory for the resumed run.

## Saved state and exact continuation

The version 1 format includes immutable initialization, topology and optional
unit calibration; the tick and fault flag; every resident record and in-flight
carrier; allocation phases, carried remainders, routing counts and fractional
movement credit; frozen replacements, departures, spatial guards and their
ready/next times; received counters; and all operation/source/loss/escape ledgers.
It also stores spatial populations, delivered directions, samples, active
scheduling membership, field clocks, reaction phases and in-flight field bundles.

When native events are configured, the same file stores the ordered causal
ledger, native resolver counters, random generator state, live quantum payloads,
heads, constraints, prepared decisions and recorded outcomes. Restore preserves
the identity relationship between each recorded outcome and its prepared
decision. Quantum backend compaction is retained as state, with its remaining
live payloads and historical audit records.

Observers, open files, callbacks and presentation history are not serialized.
The optional new observer receives only future events and cannot affect loading.
Runner observer diagnostics and display archives start fresh at the resumed
boundary. They are separate from the exact physical and native event state.
Physical state remains exact when the observer is replaced. The caller must
pause stepping while saving; saving from an observer callback during a step or
concurrently with physical mutation is outside this API's boundary contract.

## Compatibility and rejection

The envelope identifies its format/version, SHA-256 payload checksum, normalized
configuration digest, exact Python implementation/version and a digest of all
runtime Python source bytes. Python compatibility includes the patch version.
A changed source tree, interpreter version or
schema is rejected explicitly. There is no implicit migration or replay fallback.
The checksum detects damaged content; it is not an author signature.

The JSON codec admits only a fixed registry of data records and explicit
primitive containers. It never imports a class named by input, evaluates input
code, or accepts pickle. The file limit is 64 MiB; nesting, integer and container
limits also apply.
Physical payloads retain their narrower bounds; rational calibration metadata
may use the separately bounded 256-bit host integer range.

Loading reparses and validates the original configuration, then constructs a
private canonical assembly and checks the decoded state before returning it.
Checks include capacities, selected sites, physical ownership, clocks, field
signs, fractional credit, pending conserved balances, total conserved stock
against initial values and ledgers, active spatial ownership, causal references,
and quantum event/payload/outcome consistency. No live caller world is mutated
when input is rejected. These checks establish structural consistency; they do
not prove that an arbitrarily edited, internally consistent history occurred.

Only the canonical `Simulation` composition is supported. Subclasses, replaced planners,
custom resolvers, unknown instance attributes and unrelated use of another
quantum backend on the bound owner are rejected. This prevents silently omitting
custom callback state and pretending a restore is exact.

## Atomic writes and retention

Serialization and a full codec validation finish before writing. The host writes
and flushes a temporary file beside the destination, then atomically replaces
the checkpoint. An interrupted write before replacement leaves an earlier
checkpoint intact. An existing unrelated JSON document cannot be overwritten.

The normal [24-hour generated output retention](RETENTION.md) applies. A runner
can pass its active output-directory `ArtifactLease`; the checkpoint verifies
that the destination belongs to that directory and avoids a nested registry.
Standalone checkpoints enroll their generated file separately. Keep original
configuration and source files outside output directories. Concurrent writers
must not target the same standalone checkpoint path.

## Verification

[Checkpoint tests](../tests/test_checkpoint.py) compare uninterrupted runs with
save/load/continue across delayed commits and arrivals, split transport, BCC
periodic encounters, rational motion, finite source/loss/open-boundary fields,
spatial coupling, native event outcomes, mixed/grouped quantum branches,
uncommitted prepared decisions and compacted quantum histories. They compare
every future observer event, snapshots, computation costs, totals, accounting
and all stored private phase/index state. Separate corruption cases verify
rejection of invalid configuration, missing capacity, inflated pending/resident
stock, hidden spatial ownership, unsigned negative bins, inconsistent quantum
metadata, invalid movement credit, malformed JSON and incompatible source.
