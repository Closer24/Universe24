# Run performance

The optimization changes host diagnostics and export, without changing the
physical engine, scenario defaults, frame sampling or output resolution.

## Measured contact run

Measured on the same Windows host on 2026-09-11, using Python 3.14.7,
Matplotlib 3.11.1, Pillow 12.3.0 and NumPy 2.5.3 in one existing environment.
The baseline was commit `1168463ae7d211f86274200dd75c5e03c556c8f3`.
Each measurement used the default contact scenario: 48 physical ticks, 49 saved
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

These saved-output measurements use the API's `live=False` default. CLI live
viewing now adds a separate preview process and throttled PNG page updates so
images become available before the final GIF. This can add host work; concurrency
improves time to visible results and does not promise a shorter whole-run duration.
Use `--no-live` to compare final-output throughput, and record first-image latency
separately when comparing live viewing. Short physical calculations can finish
before the first preview image; updates continue during canonical export.

Use the same installed dependencies for the baseline and optimized checkouts.
Run the following from each checkout in a fresh Python process, with its `src`
directory on `PYTHONPATH`. Use distinct output directories for each measurement.

```python
import time
from pathlib import Path
from event_universe import runner
from event_universe.scenarios import get_scenario

render = runner.render_volume
started = time.perf_counter()


def measured_render(*args, **kwargs):
    print("simulation/capture/metadata:", time.perf_counter() - started)
    rendering = time.perf_counter()
    result = render(*args, **kwargs)
    print("render/export:", time.perf_counter() - rendering)
    return result


runner.render_volume = measured_render
runner.run_scenario(get_scenario("contact"), Path("artifacts/contact-benchmark"))
print("total:", time.perf_counter() - started)
```

Keep other heavy jobs idle during comparison. Reuse the installed environment
for normal later runs; setup work is not part of running the simulator.

## Validation scope

Live output was observed externally on the same Windows/Python 3.14.7 environment,
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
The unchanged `python tools/check.py` gate also retains current physical
regressions and produces a 3D HTML report for test worlds. Timing thresholds
are deliberately kept out of CI because shared-runner load varies.

The Windows validation environment enables UTF-8 mode (`$env:PYTHONUTF8 = '1'`
in PowerShell) before the unchanged gate. Some existing tests read UTF-8 source
and HTML through the platform default encoding; a legacy Windows code page
cannot decode those files. This setting does not change simulation arithmetic.

Generated GIFs, HTML, event traces and timing records belong in run outputs,
outside source commits. Their comparison and the executed gate results are
recorded in the implementation PR.
