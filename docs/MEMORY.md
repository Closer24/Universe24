# Memory architecture and review

Every change requires review of system ownership and memory architecture.
`python tools/check.py` always selects `tests/test_architecture.py` and
`tests/test_memory_contracts.py` for changed work, including configuration and
documentation. They complement review; they cannot certify every possible world.
The durable process is in [shared workflow](../skills/workflow.md#memory-and-system-architecture).

## Ownership and lifetime

| Storage | Owner and bound |
| --- | --- |
| Parsed laws | Immutable definitions outside dynamic payloads; one composed law per world/worker |
| Carrier defaults | One immutable empty-record tuple and default coupling-remainder tuple per engine |
| Changed residuals | Copy-on-write local tuple; unchanged results reuse their original immutable tuple |
| Empty links | One immutable tuple per slot width; address order and physical metadata remain retained |
| Spatial defaults | One immutable blank-state tuple per engine; only fully equal state is interned |
| Local work | Lazy immutable input messages; at most two queued chunks per worker plus the current result chunk |
| Batch work | Inputs frozen to disk one at a time; at most two pending jobs per worker |
| Recording | Disk-backed JSON records and fixed-width disk indexes; no growing RAM item/offset history |
| Expression cache | At most 1,024 immutable roots per interpreter; no cached dynamic physical inputs |

The scheduler keeps sorted candidate addresses to preserve commit order, but
does not retain a second full tick of proposal inputs. Worker transport still
copies messages and each interpreter retains its own modules/law/cache. The MPI
adapter keeps the complete world on its coordinator; it does not distribute RAM.

Batch input bytes are released after each validated temporary snapshot. All
snapshots are frozen before workers start, so editing an original cannot change
an in-flight job. Ordered job summaries still grow with job count. Temporary
snapshots and workers are cleaned up on failure.

The generic runner uses `archive.JsonArchive` for optional frames and observer
receipts/samples. Each append writes JSON plus a 16-byte index entry to temporary
files. Reading loads one indexed item; export streams raw chunks of at most
64 KiB before HTML escaping. Closing removes the files. Failed encoding never
publishes an incomplete record. Capacity errors preserve whole reception batches
and exact capture prefixes. JSON arrays read back as lists; serialized values
and order are unchanged. Observations use compact JSON formatting. Direct
`LocalObserver` callers retain the compatible in-memory list default; use
archives for long recordings.

## Intentional limits

Fixed local physical capacity does not imply constant total memory. Visited
addresses retain timestamps, causal IDs, residuals and insertion order even when
there is no current particle. Removing this state requires an equivalence proof.
Nondefault residuals can still cost `3 * coupling_count * slots**2` entries per
cell. Shared defaults reduce allocation without reducing logical capacity.

Each recorded frame must still fit in memory. Full recording size grows on disk;
the self-contained browser player also loads the complete recording. Historical
renderers and explicit in-memory tracing retain their documented history costs.
Disk exhaustion is an error, never permission to omit frames or receipts. Quantum
ancestor sets and ledgers retain their separate capacity/checkpoint semantics.

Block-based SoA/AoSoA storage and distributed spatial ownership remain potential
future work. Do not narrow exact integer registers, alter operation costs,
discard remainders or change delivery/commit order to fit another storage format.

## Measure a representative run

Use a fresh process per before/after run with identical configuration, duration,
worker options and identified source:

```bash
python tools/benchmark_memory.py --init examples/basic.json --ticks 100 --output artifacts/memory-serial --trace-python
python tools/benchmark_memory.py --init examples/basic.json --ticks 100 --workers 4 --output artifacts/memory-parallel
```

The tool preserves the ordinary headless run and all conservation checks, then
writes `memory.json` with source/configuration hashes, actual execution, failures
and OS process-memory readings. Peak resident memory is a process-lifetime
high-water mark, not an allocation attributed solely to this run. Windows also
reports current resident/private bytes; unavailable readings are null.
Same-process interpreter workers are included; MPI/other child processes need
separate monitoring.

Optional `--trace-python` records Python allocation peak/current values during
the audited serial run, separately from RSS/native memory. It requires one
worker and cannot replace an existing tracer. Normal runs remain uninstrumented.

Permanent tests cover maximum capacities, shared-default isolation, pending
nonzero remainders, periodic storage stabilization, bounded archive export,
same-tick receipt prefixes and failed-run cleanup. Focused batch/worker tests
cover lazy consumption and pending-window limits. Add affected cases when
ownership or lifetime changes, and inspect measurements before claiming an
improvement. Results belong in [validation](VALIDATION.md).
