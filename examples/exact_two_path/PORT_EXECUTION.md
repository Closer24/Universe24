# Interim Port execution comparison

`Simulation(initial, execution_strategy="node")` is the ordinary reference.
`execution_strategy="port"` selects a due-work adapter for serial whole-record
carriers. Both receive exactly the same initialization, generic rules and tick
count. The default remains `node`. Spatial fields, native event programs,
split transport and parallel workers fail explicitly in the interim adapter.

This adapter schedules the six external Ports. It does **not** execute the newly
specified 24 internal Registers. Those Registers have separate immutable graph
and single-input/single-output channel contracts. Mapping straight transfer and
return to the orthogonal internal graph remains undefined; this implementation
does not add an intermediate spatial detour, extra physical time or a hidden
choice of axis. No performance result selects or validates that missing kernel.

Each external Port owns a fixed view of local record slots and locks. The existing
Node owns the actual payload, pending proposal, costs and one atomic transaction.
Grouping ready Port views invokes that existing Node evaluator once. It does not
factor the evaluator into independent internal Register arithmetic. Zero-amplitude
records retain their semantic ownership and readiness; no record is copied into
each Port or Register.

The external indexed heap keeps one live entry per work handle. Replacement and
cancellation remove old entries immediately, so repeated rescheduling does not
retain a growing list of stale events. Separate queues admit opening computation,
completed Link receipts and closing commits. All same-tick receipts precede closing
local computation, and outgoing Links arrive at a strictly later tick. The queue
contains handles; the existing PortBank remains the sole in-flight payload owner.

Actual Link delivery preserves original bank-creation/slot order. Destination
admission validates the complete local batch before releasing source slots and
publishing receipts. A failure preserves actual owners and faults the world.
No operation scans idle Nodes or advances sleeping deadlines on each tick.
Required fixed local readiness/ownership checks remain bounded by Node capacity.

For the explicit `node_execution` clock, the pending absolute deadline is
authoritative. Passive snapshots and immutable Node views derive `delay_counts`
at observation time. The reference's eagerly maintained countdown cache and the
candidate's retained cache can differ while waiting; canonical observable state,
pending deadline, physical values, remainders and events remain equal. The
projection never repairs physical state or influences the next local law.

Run the same file through both paths, alternating order across fresh worlds:

```sh
PYTHONPATH=src python examples/exact_two_path/compare.py \
  --source . --initialization examples/exact_two_path/initialization.json \
  --output artifacts/port-comparison --repeats 3
```

The comparison requires complete canonical state, actual inventory, pending
plans, Link packets, model costs and ordered-event hashes to match at **every**
tick before reporting timing. Initialization, stepping and canonical HTML export
are timed separately. Stepping includes the identical event callback and excludes
read-only snapshots/hashing. Each actual run produces HTML through the existing
renderer. This small finite workload cannot establish a universal speedup.
Queue counts describe structural storage; peak process memory is not measured.

The focused tests cover three independent phase expectations, conserved quadratic
norm, exact-division rejection before commit, every-tick reference parity, the
seven-tick explicit local rule delay, indexed-queue replacement/cancellation and
skipped-deadline rejection. They are analytical/software controls, not measured
evidence that the model reproduces an electron or other physical species.

## Recorded finite comparison

On Python 3.14.7, three fresh pairs of the 12-tick input matched canonical hashes
at every tick. Source fingerprint:
`64a10c8a5d49d7b52756738c52391c5f3b63044040e84b28fd3f6dbc7b3ea5fa`.

| Execution | Median step time | Node phase visits |
| --- | ---: | ---: |
| Ordinary Node | 3.67 ms | 38 |
| Interim Port | 4.47 ms | 18 |

The interim adapter was about 22% slower for this small workload despite fewer
Node visits. Its dispatch overhead outweighed the work saved. This is useful
negative performance evidence, not a measurement of the unimplemented 24-Register
kernel. All six runs produced canonical HTML with 13 actual frames; embedded
recordings were checked. Browser interaction and visual layout were not verified.
