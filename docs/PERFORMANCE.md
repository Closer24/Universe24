# Run performance

## Active engine: default Focus and exact plan reuse

Measured on Linux with Python 3.14.7 on 2026-09-15. Baseline:
`4796cb256cbdbd830aa29cc3038fea98087de58b`, with its original default Focus off.
The proposed default enables certified empty-carrier scheduling and pure plan
reuse; both transport engines additionally index occupied output banks.

| Input | Ticks | Baseline median | Optimized median | Elapsed time change |
| --- | ---: | ---: | ---: | ---: |
| One moving carrier leaving an empty trail | 240 | 0.2041 s | 0.0849 s | 58.4% shorter |
| 32 repeated moving carriers, periodic domain | 120 | 1.1858 s | 0.8199 s | 30.9% shorter |
| 16 repeated local two-field configurations | 48 | 6.7063 s | 4.5271 s | 32.5% shorter |
| Existing finite-field example | 16 | 0.1898 s | 0.1960 s | 3.3% longer |

Each value is the median of three fresh processes. Variant order alternates.
Timers include `step()` and the same ordered event serialization, while excluding
initialization, imports, per-tick comparison reads and HTML export. CPU time is
recorded separately. These are small input-specific benchmarks, not universal
speed guarantees. The low-repetition finite-field input showed no benefit;
cache lookup and index maintenance can outweigh savings in such a short world.

For repeated carriers, 3840 local planning requests required only two actual law
evaluations. The 16 repeated field configurations required 47 spatial evaluations
for 752 requests and one carrier evaluation for 736 requests. Every Node still
performed its own guarded commits, event publication and modeled cost accounting;
reducing planner work by more than 90% does not reduce whole-run time by 90%.

Across all 24 measured runs, the cumulative hashes of every completed tick's
snapshot, actual inventory and computation report matched within each input.
Full ordered event trace hashes and final accounting also matched. Every run
produced HTML using the existing `render_disturbances` generator. Browser visual
inspection was unavailable because the browser policy blocked local-file access;
HTML generation and embedded recording integrity were checked separately.

Baseline source fingerprint:
`c70c279be058f8730358a9110a9a51a1c201e91f5f0d884641cbfc3ef263fb14`.
Optimized source fingerprint:
`7c5375d1731082a27cb9f50fd2fe5e87c0bad761d8a67b6c679b469d2f83b346`.
The fingerprint covers active Python source, not generated outputs or this text.

A subsequent constructor correction preserves the original spatial planner object
for direct law inspection while passing the same reuse adapter to execution.
Its source fingerprint is
`4e0c9eeffd4a1ce1bb832c0687913c71a8c44dd4d79d100296c42e9238f50c36`.
All four inputs were replayed on this corrected source and matched the recorded
state, event, cost and accounting evidence exactly. The table remains the earlier
isolated timing measurement: constructor setup is outside its timer, the stepping
callback is unchanged, and timings from the extra acceptance replays are not used.

Reproduce with the same environment and `tools/benchmark_focus.py`, setting
`PYTHONPATH` to each chosen checkout's `src`. Select `--case trail`, `repeated`,
`fields` or `finite`, provide that checkout with `--source`, and use a fresh
`--output` directory. `--focus true` or `--focus false` provides an explicit
control. Run each comparison at least three times. Inputs, events, result JSON
and canonical HTML are written together; generated outputs stay outside commits.
See [Local Focus](LOCAL_FOCUS.md) for eligibility, bounds and supercell limits.

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
