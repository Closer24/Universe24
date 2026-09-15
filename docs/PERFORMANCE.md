# Run performance

## Current generic runner - 2026-09-15

Measured on one Linux x86-64 host using Python 3.14.7, the same installed
dependencies, one Node worker, and the existing recorded HTML generator.
Five measured pairs followed one excluded warmup pair for each input, alternating
which checkout ran first. Other project checks were paused during timing.
Each sample used a fresh interpreter process. Timing starts after imports and
includes input preparation, world construction, every physical tick, all balance
checks, JSON event writing, recorded snapshots, final serialization and HTML
export. Post-run equivalence hashing is excluded. `run.json`'s narrower
`elapsed_seconds` and isolated step/export timings are also retained by the tool.

Baseline commit: `4796cb256cbdbd830aa29cc3038fea98087de58b`.
Baseline source fingerprint: `c70c279be058f8730358a9110a9a51a1c201e91f5f0d884641cbfc3ef263fb14`.
Candidate source fingerprint: `ed0297a5b0673627d46fbdd081305fa628db0296c1142cd0c6a67ad3c35cfc73`.

| Input | Ticks | Frame stride | Before, seconds | After, seconds | Time saved | Speedup |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Sparse moving carrier | 800 | 20 | 1.356004 | 0.570196 | 57.95% | 2.378x |
| Outward spatial field | 20 | 2 | 3.270860 | 2.445681 | 25.23% | 1.337x |
| Finite attenuating field | 40 | 4 | 0.195805 | 0.154935 | 20.87% | 1.264x |
| Straight-ray field | 24 | 2 | 1.765977 | 1.399698 | 20.74% | 1.262x |
| Shared field/carrier clock | 20 | 2 | 0.221196 | 0.182315 | 17.58% | 1.213x |
| Recurrent quantum contact | 48 | 4 | 0.135798 | 0.132693 | 2.29% | 1.023x |

Values are medians, not a cross-platform guarantee. The quantum case's
2.29% median difference is small and the measured ranges overlap (baseline
0.129726-0.140305 s, candidate 0.123030-0.134033 s); it does not demonstrate a
stable quantum speedup. The other five sampled ranges do not overlap, but the
measurements still do not establish a universal speedup for every input.

All 72 runs completed with unchanged input, final-state, event-trace, physical
metadata and sampled-frame hashes within each case. Frame counts, resolution,
model operations and every physical tick were preserved. Ordinary per-tick
quantity checks remained enabled. This is exact output agreement for these
experiments, not a complete proof over all configurations.

The sparse case's carrier phase visits fell from 962,000 to 2,400; its full
run is not 400 times faster because transit scans, recording and other work
remain. The shared-clock and quantum cases both correctly retained the ordinary
scheduler. Focus is on by default where eligible, not forcibly enabled there.

### Included changes

- Default-on carrier Focus with explicit false opt-out and unchanged fallback.
- One fresh spatial inventory traversal shared by each runner's combined and
  spatial-only accounting checks, with no cache across mutations.
- Focused carrier totals omit certified empty history.
- Scalar/vector payload codecs avoid generator allocation while keeping all
  integer checks and the original component evaluation order.

This change does not introduce a delivery-time queue, change the parallel
backend, reduce event logging, reduce physical resolution or change a LocalRule.
Those require separately measured changes, not extrapolation from these results.

### Reproduce

Use the same project interpreter and dependencies for both worktrees:

```bash
git worktree add --detach ../Universe24-baseline 4796cb256cbdbd830aa29cc3038fea98087de58b
python tools/benchmark_runtime.py --baseline ../Universe24-baseline --candidate . --output artifacts/runtime-comparison --repeats 5
```

The tool retains `benchmark.json`, raw `samples.json`, generated input snapshots
and each run's HTML/events/state/timing files outside source commits. It verifies
the actual imported source path and checks its fingerprint before and after
each run. Do not compare changing source trees or run unrelated CPU-heavy jobs
during a measurement. `--cases` selects a smaller experiment set.

## Historical scalar/particle renderer

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
