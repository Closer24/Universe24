# Run performance

## Active generic engine

The active engine now indexes active carrier work, delayed completions and link
arrivals, while retaining physical cells, fixed packet slots and original event
ordering. Spatial work checks its fixed clock before copying residents. The runner
shares a spatial reduction within each tick's accounting without dropping checks.
Prepared integer expression execution selects operators once and charges every
original operation; exact rational arithmetic is unchanged. These changes improve
host execution, not the model's computation budget, delay or physical laws.

For independent worlds, `python -m event_universe.batch` uses a bounded process
pool. It saves validated input copies before starting workers, preserves each
ordinary run's evidence, reports partial failure and joins interrupted workers.
Inputs are runtime JSON; changing them requires no package rebuild. Process
startup may outweigh parallelism for short runs. This command increases experiment
throughput. The separate single-world interface below parallelizes local proposals.

### Parallel local work inside one world

```bash
python -m event_universe --init my-simulation.json --workers 4 --output artifacts/parallel-world
```

`--workers` defaults to 1. Larger values select a persistent Python 3.14
`InterpreterPoolExecutor`: each worker has its own interpreter and GIL, so pure
Python calculations can use several CPU cores. Immutable laws are installed once
per worker. A job carries fixed local records, residuals and already received
counts; it cannot read neighboring cells or advance the world. Configurations
remain runtime data and require no compilation.

The scheduler dispatches bounded chunks when at least `--parallel-threshold`
eligible cells are ready (default 64), using `--chunk-size` proposals per job
(default 32). The owner applies results and failures in the existing address
order, interleaving each begin and commit exactly as before. Worker completion
order does not select a collision outcome, change a delay or reorder events.
All arithmetic, integer bounds and modeled charges use the same generic law.

Spatial evolution, field-coupled carrier work, shared native-event resolution
and custom components retain their serial owner. `run.json.execution` records
actual parallel work and fallback reasons separately from physical `computation`.
Requesting several workers therefore does not mean every phase ran in parallel.
The runner closes workers on completion and failure. Direct API consumers should
use `with Simulation(initial, workers=4) as world:` or call `world.close()`.

Small local laws may cost less than serialization and dispatch; the default
remains serial. Measure your configuration before selecting more workers. Each
batch job also defaults to serial stepping, avoiding nested pools by default.
GPU kernels and independent partition ownership are not part of this backend.
The optional MPI transport below uses the same local-proposal protocol.

Reproduce a substantial local-work control and compare exact physical traces:

```bash
python tools/make_parallel_benchmark_input.py --output parallel-inputs --cells 128 --ticks 20
python tools/benchmark_engine.py --init parallel-inputs/rational-pairs.json --workers 1 --repeat 3 --output artifacts/parallel-serial
python tools/benchmark_engine.py --init parallel-inputs/rational-pairs.json --workers 4 --repeat 3 --output artifacts/parallel-four
```

The generator reuses the existing configured electron/proton rational scattering
reference, holds one pair at each cell, and evaluates the reversible transaction
each cycle. It is a computation control, not a realistic repeated-collision
trajectory. Ordinary physical conservation checks remain enabled. Benchmark
stepping includes fresh worker startup and shutdown for each run, with complete
trace hashing performed separately. Audited timing retains every runner check,
event and artifact. Compare both timings and the exact trace digests.

The runtime mechanism follows the [Python 3.14 executor contract](https://docs.python.org/3.14/library/concurrent.futures.html#interpreterpoolexecutor).

Measured on this Windows/Python 3.14.7 host with 12 logical CPUs, after other
validation work stopped: 128 held pairs, 20 ticks, three fresh runs per mode and
one unmeasured warmup. Both modes used source
`8439ddb9ec137ce8a44ae948f7fdef9b53f4aebe44150d7bc56e93392b3fac4c`
and initialization
`556ce186745b09ccbd9bd886bb9457371b0b678c86d47752442a52235e5bbf4a`.

| Execution | Median stepping | Median complete audited run |
| --- | ---: | ---: |
| One worker, serial | 7.489746 s | 7.751503 s |
| Four interpreter workers | 2.483324 s | 2.532277 s |

This control improves stepping by **3.02 times** and audited execution by
**3.06 times**. Every repetition used four distinct worker interpreters, 80
chunks and 2,560 local proposals, with no serial fallback. All 21 per-tick state
hashes and 5,120 ordered events match both modes and the PR #60 predecessor.
Startup and shutdown are included; trace hashing is separate. These results
apply to this substantial rational workload, not small runs, spatial-only work,
GPU execution or general distributed scaling.

### Optional MPI processes

Install the optional `mpi` dependencies once, then start ranks before the run:

```bash
python -m pip install ".[mpi]"
mpiexec -n 3 python -m event_universe.mpi_runner --init my-simulation.json --output artifacts/mpi-world
```

Three ranks provide one coordinator and two calculation workers. On this Windows
host, `python -m pip install impi-rt` installs the optional Intel runtime locally
in the environment. Its launcher is in the environment's `Library/bin` directory;
use its `-localonly` option for one computer. The MPI entry point uses an existing
communicator and does not dynamically spawn ranks. Ordinary runs neither import
nor require MPI. Every rank needs the same simulator source and Python runtime;
multi-computer deployment also requires an MPI launch environment and shared
access to that source.

Only the coordinator reads the initialization and writes run artifacts. The
worker initializer receives the canonical immutable planner created from that
same parsed input, pins its source before deserialization, and reuses it across
jobs. MPI transports the same bounded local proposal batches; it does not own
spatial partitions or change the serial phase and fallback rules above. Errors
from initialization and physical stepping release the waiting ranks. Successful
MPI launch alone does not establish a speedup or multi-computer scaling.

The adapter follows the [mpi4py futures communicator contract](https://mpi4py.readthedocs.io/en/stable/mpi4py.futures.html#mpicommexecutor).

### Reproduce active measurements

Use one installed Python 3.14 environment. Set `PYTHONPATH` to the selected
checkout's `src` directory and verify `package_path` in the report; an editable
installation may otherwise select a different checkout. Use distinct outputs:

```bash
python tools/benchmark_engine.py --init examples/basic.json examples/finite_fields.json examples/particle-contracts/electron-proton.json --repeat 3 --output artifacts/engine-benchmark
python tools/make_scheduling_benchmark_inputs.py --output benchmark-inputs
python tools/benchmark_engine.py --init benchmark-inputs/sparse.json benchmark-inputs/dense.json --repeat 3 --output artifacts/scheduling-benchmark
```

The benchmark reports stepping separately from complete audited-run time.
Stepping excludes setup, event serialization and diagnostics, after one warmup;
each repetition uses a fresh world. Audited time includes source fingerprinting,
validation, every event write, all per-tick acceptance checks and final artifacts.
A separate untimed pass hashes every tick's physical records, pending proposals,
packet ownership, field registers, ledgers, model costs and events. Compare these
digests before interpreting a timing ratio. Source/input fingerprints identify the
tested payloads. No visualization is loaded or generated. No CI wall-time
threshold is imposed; timings depend on workload and host load.

### Current measured scope

Measured on Windows with Python 3.14.7 and its GIL enabled, comparing main
`992e0006469bb1156f517ae8273a80a980df7c57` with the optimized source. Three
repetitions per case, one core warmup, identical inputs and ticks. All six
complete physical traces and event streams below matched exactly, including
modeled costs. These small runs do not demonstrate a general speedup:

| Initialization | Ticks | Core before | Core after | Audited before | Audited after |
| --- | ---: | ---: | ---: | ---: | ---: |
| basic | 8 | 0.018091 s | 0.017682 s | 0.254285 s | 0.263030 s |
| exchange | 8 | 0.001171 s | 0.001169 s | 0.264722 s | 0.295227 s |
| finite_fields | 40 | 0.106828 s | 0.110372 s | 0.354443 s | 0.373928 s |
| local_lorentz_field | 20 | 0.235470 s | 0.238826 s | 0.479458 s | 0.498264 s |
| particle-contracts/electron-proton | 180 | 0.190578 s | 0.189664 s | 0.451530 s | 0.448815 s |
| quantum/native_cost_delay | 40 | 0.004440 s | 0.005416 s | 0.245908 s | 0.246803 s |

Baseline source SHA256:
`c45f9ee8d8696965414cea77b4d2c13fec0fc9f1b412ff2d7047470176c1b935`.
Optimized source SHA256:
`bde2dfc56db7dbb7e4dc44bd8ddb4627bb575317b51010b006d7d840bbb9f818`.
The millisecond native-event case and runner setup are sensitive to overhead;
native resolver worlds deliberately retain full cell polling. Do not extrapolate
the sparse scheduling benefit or expression microbenchmarks to these runs.

The generated scheduling controls use five repetitions per source with the same
observer-free core timing and separately audited runner protocol:

| Control | Ticks | Core before | Core after | Audited before | Audited after |
| --- | ---: | ---: | ---: | ---: | ---: |
| One moving record, accumulating dormant history | 500 | 0.353218 s | 0.053331 s | 0.466814 s | 0.217455 s |
| 100 held active records | 100 | 0.532673 s | 0.526483 s | 0.906152 s | 0.814282 s |

The sparse control improves core stepping by 6.62 times and complete audited
execution by 2.15 times; dense core execution is effectively unchanged. Each
control's complete physical-state hashes and ordered event digest match between
sources: 2,000 events for the sparse case and 20,000 for the dense case. These
results apply to the identified host and configurations, not arbitrary worlds.

The implementation was subsequently integrated with main `98b774ac`, which adds
inline passive observer placement. Scheduler and expression implementation files
remain byte-identical to the measured optimized version. The final integrated
source fingerprint and checks are recorded in [validation](VALIDATION.md).

## Historical renderer measurements

These are historical scalar/particle renderer measurements. The optimization
changes host diagnostics and export without changing that candidate's physical
engine, scenario inputs, frame sampling or output resolution. It does not measure
the active initialization-defined disturbance engine. Current generic and
historical runs are headless unless visualization is explicitly requested.

## Measured contact run

Measured on the same Windows host on 2026-09-11, using Python 3.14.7,
Matplotlib 3.11.1, Pillow 12.3.0 and NumPy 2.5.3 in one existing environment.
The baseline was commit `1168463ae7d211f86274200dd75c5e03c556c8f3`.
Each measurement used the historical contact scenario: 48 physical ticks, 49 saved
frames, stride 1, and enhanced 1500x1275 3D GIF and standalone HTML.

| Measured phase | Before | After |
| --- | ---: | ---: |
| Simulation, capture and metadata before rendering | 0.724 s | 0.697 s |
| Rendering and GIF/HTML export | 44.106 s | 20.349 s |
| Total run after imports | 44.831 s | 21.046 s |

This run completed **2.13 times faster**, with a **53.1% shorter elapsed time**.
These are single before/after wall-clock measurements, not a cross-platform
guarantee or a statistical benchmark. Setup, dependency installation and imports
are excluded. Larger fields or longer runs can have different bottlenecks.

The baseline source fingerprint is
`c7696ccccad62080363a35673f9e6be053c3f5461909160de8792abc8b621256`;
the optimized source fingerprint is
`49c8e8fe8401f038d463ab20ab331392ae8a41c723bd25309a9af571eb2be506`.
Fingerprints identify the active Python source, independently of documentation.

## What changed

- Reuse the Agg canvas drawn by FuncAnimation instead of rasterizing every
  default frame again in PillowWriter. Preserve custom savefig settings through
  a fallback to savefig.
- Encode the stopped GIF once, without decoding and re-encoding it to remove
  its loop flag.
- Keep static 3D axes, grid and compass artists. Extend trail history as frames
  advance, with safe reset on a seek or domain change.
- Capture only the requested view and reuse each completed tick's measured
  momentum. Recompute it after a failed step, including a partial commit that
  did not advance time.

All physical ticks, event recording and acceptance checks remain enabled. The
existing `--frame-stride` option is still an explicit sampling choice; none of
the measured improvement comes from fewer frames or reduced resolution.

## Reproduce the measurement

These saved-output measurements used no live preview. In the current historical
API, request recorded output with `visualize=True` and leave `live=False`.
Explicit live viewing adds a separate preview process and throttled PNG page
updates so images become available before the final GIF. This can add host work; concurrency
improves time to visible results and does not promise a shorter whole-run duration.
Use `--visualize` without `--live` on `event_universe.legacy_runner` to compare
final-output throughput, and record first-image latency separately when
comparing live viewing. Short physical calculations can finish
before the first preview image; updates continue during canonical export.

Use the same installed dependencies for the baseline and optimized checkouts.
Use each checkout's recorded API and explicit historical scenario in a fresh
Python process, with its `src` directory on `PYTHONPATH`. Use distinct output
directories for each measurement. The example below targets the current tree:
its lazy renderer lookup must be patched in `diagnostics.render`. The historical
baseline exposed the eager renderer and `run_scenario` through `runner` instead.

```python
import time
from pathlib import Path
from event_universe import legacy_runner
from event_universe.diagnostics import render as render_module
from event_universe.particle_scenarios import get_scenario

render = render_module.render_volume
started = time.perf_counter()


def measured_render(*args, **kwargs):
    print("simulation/capture/metadata:", time.perf_counter() - started)
    rendering = time.perf_counter()
    result = render(*args, **kwargs)
    print("render/export:", time.perf_counter() - rendering)
    return result


render_module.render_volume = measured_render
legacy_runner.run_scenario(
    get_scenario("contact"),
    Path("artifacts/contact-benchmark"),
    visualize=True,
    live=False,
)
print("total:", time.perf_counter() - started)
```

Keep other heavy jobs idle during comparison. Reuse the installed environment
for normal later runs; setup work is not part of running the simulator.

## Validation scope

Before integration with the generic/headless runner, live output was observed
externally on the same Windows/Python 3.14.7 environment,
without slowing or modifying physical steps. These times start at CLI launch,
including imports and preview startup; they are not directly comparable to the
earlier after-import throughput measurements.

| Run | First live page | First PNG | Final HTML | CLI exit |
| --- | ---: | ---: | ---: | ---: |
| Contact, 48 ticks, stride 1, 49 frames | 1.277 s | 3.779 s | 28.854 s | 29.686 s |
| Turning, 110 ticks, stride 10, 12 frames | 1.117 s | 2.558 s | 8.651 s | 8.872 s |

In the turning run, preview images for ticks 20 and 90 were published before
final metadata existed at 3.193 s. A separate observation of the same 110-tick
scenario recorded a monotonic timestamp immediately after the final physical
step; its first PNG was verified 0.507 s before that timestamp. This confirms
actual overlap, using one final-step marker and no delays or numerical changes.
The short contact calculation finished before its first image; that image and later
updates arrived during export. All 49 final contact frames were pixel-identical
to the prior output, with identical frame durations and all 136 events unchanged.
The measurements describe file availability, not a browser's paint latency.

The export and capture contracts are covered by `tests/test_render_export.py`
and `tests/test_run_capture.py`; see [TEST_EXPECTATIONS.md](TEST_EXPECTATIONS.md).
The unchanged `python tools/check.py` gate retains current physical regressions
and runs headlessly. Visual artifact tests and historical 3D test-world reports
require an explicit `pytest --visualize-runs` request. Timing thresholds are
deliberately kept out of CI because shared-runner load varies. The historical
measurements above are not a claim that visual checks were repeated on the
integrated generic/headless tree.

The Windows validation environment enables UTF-8 mode (`$env:PYTHONUTF8 = '1'`
in PowerShell) before the unchanged gate. Some existing tests read UTF-8 source
and HTML through the platform default encoding; a legacy Windows code page
cannot decode those files. This setting does not change simulation arithmetic.

Generated GIFs, HTML, event traces and timing records belong in run outputs,
outside source commits. Their comparison and the executed gate results are
recorded in the implementation PR.
