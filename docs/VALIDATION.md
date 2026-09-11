# Validation evidence

## Python 3.14 and necessary tests — 2026-09-11

Validated locally with CPython 3.14.7 in the project virtual environment, based on
main `7e517afb7a274821de05bf247ece91827c1b030b`. The runtime selection, CI and
agent workflow now use Python 3.14. Older-Python, archived-v10 equality and
historical facade API tests are no longer gates, as requested by the user.
Current physical contracts and known failure evidence remain covered.

| Check | Result |
| --- | --- |
| `python tools/check.py` | Passed: Ruff lint/format, strict mypy and 461 pytest cases |
| Static scope | 114 Python files formatted; 48 package modules type checked |
| Test reduction | Four fewer collected cases, six fewer worlds and 447 fewer simulation ticks |
| Test visualization | All 94 current-engine worlds rendered through the existing HTML/GIF pipeline |
| Contact CLI | Completed 48 ticks; momentum equal at every completed tick; all state audits passed |
| Visual inspection | Contact frame at tick 24 shows both particles, field, axes and total momentum (0,0,0) |
| Package build | Wheel and sdist built; minimum Python is 3.14 and sdist includes `.python-version` |
| Agent Skills | Boss, architecture, regression and necessary-tests Skills validated; shared workflow updated |

Installed project tools: pytest 9.1.1, Ruff 0.16.7, mypy 2.3.1, Matplotlib 3.11.1,
Pillow 12.3.0, NumPy 2.5.3 and build 1.6.1. Isolated package build used
setuptools 84.0.0. Contact source fingerprint:
`c7696ccccad62080363a35673f9e6be053c3f5461909160de8792abc8b621256`.

The remaining suite is defined in [TEST_EXPECTATIONS.md](TEST_EXPECTATIONS.md).
Local outputs are `artifacts/junit.xml`, `artifacts/test-runs.html` and
`artifacts/contact/run.html` with run metadata. The integration PR and its Actions
run record the remote result for the submitted commit. No old-Python or archived
engine compatibility run was performed. Earlier evidence below is historical.

## Historical validation — 2026-09-10

The required checks were executed locally on Python 3.12. GitHub Actions is
configured but was not executed on a remote repository in this task.

| Check | Result |
| --- | --- |
| Ruff lint | Passed |
| Ruff format | 52 Python files already formatted |
| mypy strict | Passed, 26 package modules |
| pytest | 206 passed, 0 failures, 0 errors, 0 skipped |
| Frozen-reference comparison | Exact after all 278 compared ticks |
| Contact application run | Completed 48 ticks; total momentum equal at every tick |
| Turning application run | Completed 110 ticks; total momentum equal at every tick |
| Generic field/turning | Signed and weighted fields, exact residues, direction policies and bounds passed |
| Current model | Exact field sample, source mapping, clipping and transverse response passed |
| Public component replacement | Field/turning/activity injection, remainder-only evolution and invalid-result rejection passed |
| Calculation boundaries | Absolute/relative imports and formula-free assembly checked, including forbidden-example tests |
| Dedicated expectations | Lattice, movement, source/range/activity policies and all diagnostic projections passed |
| Test visualization | 41 engine/reference runs rendered through the shared GIF/HTML pipeline |
| Full XYZ display | 48-tick contact run completed with total momentum preserved; shared GIF/HTML pipeline |
| Display equivalence | Plane and volume runs produced identical physical events and final reports |
| Visual inspection | Final frames of contact and turning checked; plane labels visible |

The full-state comparison checks every materialized cell, particle register,
occupancy slot, active-frontier member, force record, blocked move and path entry
after each step. It covers 120 stationary-source steps, 48 contact steps and 110
turning steps. This is evidence for those scenarios, not a proof over all inputs.

The contact event first has transverse impulse `(0,1,0)` at event tick 15, visible
in the completed frame labelled tick 16. Event records use the tick being
processed; completed frames use the count of finished ticks. This is the
preserved v10 convention.

Source fingerprint used by the preserved plane application runs:
`66855a6339d5ef4448c94ed8e47db7366a7387ea2d816aab7bedb1821d5494df`.

The full XYZ contact visualization uses source fingerprint
`47b24f3f6c8446a39c93e8badcb3baa305b4454e66ddc29fd76accd671914349`.
Its midpoint was visually inspected. After the suite, only display color,
marker size and opacity were adjusted; the XYZ demonstration was regenerated.

The source-only scalar field and full-vector turning variant are test fixtures.
They demonstrate component replacement through `Simulation`; the production
default model and its identifier remain unchanged.
An additional local-retention fixture verifies the expected sample sequence
`(1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (2,0)`, ensuring a replacement
field is not stopped while only its remainder changes. Calculation inputs,
expected outputs and ownership are documented in `TEST_EXPECTATIONS.md`.

| Tool | Version |
| --- | --- |
| pytest | 9.1.1 |
| Ruff | 0.16.6 |
| mypy | 2.3.1 |
| Matplotlib | 3.10.8 |
| Pillow | 12.3.0 |
| build | 1.6.0 |
| setuptools | 84.0.0 |

Detailed outputs are in `artifacts/checks.log`, `artifacts/junit.xml`,
`artifacts/test-runs.html`, and each scenario's `run.json` and `run.html`.
Known model assumptions and limits remain in `SIMULATOR_DEFINITIONS.md`.


## v11 local-link candidate validation — this change

- Required `python tools/check.py` completed: Ruff lint/format passed (60 Python
  files), strict mypy passed (31 source modules), **222 pytest tests passed**.
- All original frozen-v10 comparisons passed without changing expected traces.
- Eighteen new tests cover geometry, transport and the linked engine. The
  stationary-source regression initially exposed an owner-only directional
  artifact; the symmetric two-endpoint proposal protocol now passes it.
- 46 engine/reference test runs were captured using the existing renderer.
- The linked application completed 360 elementary ticks on a 32×24×12 lattice,
  with two particles and base link length 10. Total momentum matched the initial
  value at every completed tick. All runtime state audits passed.
- The final rendered frame was inspected: XY slice z=6 and tick=360 are visible.
  Arrows are scaled direction indicators; the drawing remains an address-grid
  view, not a geometrically stretched embedding.
- These tests establish the enumerated locality and numerical properties in
  tested cases; they do not establish Einstein geodesics or gravity. The example
  particles crossed the region on straight tracks; no attraction is claimed.

Current outputs: `artifacts/local-links-check.log`, `artifacts/junit.xml`,
`artifacts/test-runs.html`, `artifacts/local-links/run.json`, `.html`, `.gif`,
`.mp4` and `events.jsonl`. The video is a conversion of the existing GIF replay,
not a separately simulated trajectory.

Source fingerprint for the linked application: `53786817fe9f2c9a089a875894523229b6eb02d52bc077095fea2cc482693875`.


## Concurrent update reconciliation

The archive advanced from version 3 to version 4 while this change was being
implemented. The guarded write rejected replacement of that newer archive.
The full-XYZ renderer, `--view-3d`, its independent frame capture and both new
diagnostic tests were preserved. Link changes were reapplied to version 4.
The required gates were repeated on this merged tree: **224 tests passed**,
Ruff lint/format passed and strict mypy passed. The test renderer captured
48 engine/reference runs. The linked application was rerun from the merged
source; its current fingerprint is recorded in `artifacts/local-links/run.json`.
Earlier evidence is preserved under `artifacts/local-links-before-merge` and
`artifacts/local-links-check-before-merge.log`.
