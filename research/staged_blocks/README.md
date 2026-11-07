# Staged building blocks

This package assembles initial preparations, runs the unchanged Rule3 engine, and evaluates complete recorded trajectories. The stages separate a transported carrier, a prepared oscillator, signal-written memory, controlled release, actual splitting, routing and acknowledgment. A later stage is not accepted merely because its prerequisites can be assembled.

All experiments use one board, 48 channels per node, six spatial neighbors, a tensor fixed before the run, and synchronous Rule3 with `num=den=1`. Component names never install runtime behavior. All state is initialized before the first update. Later signals, including any future approval messages, must arise from Rule3 without external injection; the current train demonstrations preload their sources. Readouts and the Presenter are passive.

## Open the recorded examples

The [complete inventory](evidence/final_collection/presenter/index.html) lists all selected experiments and their standalone Presenter pages. The first page starts with the four-component assembly. For readable recorded-state previews, see the [connected assembly](evidence/animation_v3/four-blocks-connected.gif), [changed phase](evidence/phase_animation_v1/phase-record-changed.gif) and [two-lane driven pause](evidence/bridge_animation_v2/two-lane-driven-pause.gif). These GIFs replay saved states; use the HTML pages for interactive controls.

## Run the mechanism

From the repository root, use a fresh output directory for every command:

```bash
python -m research.staged_blocks.run list
python -m research.staged_blocks.run demo --output runs/staged-demo
python -m research.staged_blocks.run study orbit --output runs/staged-orbit
python -m research.staged_blocks.run study interaction --output runs/staged-interaction
```

`demo` assembles several ordinary preparation components on one board and retains the source controls. Its result distinguishes separate coexistence from measured interaction. A prepared clock running beside a carrier is not a clock written or released by that carrier.

Run the reusable four-piece phase assembly and all four matched controls:

```bash
python -m research.staged_blocks.run study recipes --output runs/phase-pieces
```

The pieces are a guide, a guided packet, a joint clock/guide interface and a separate reference clock. The joint interface makes the shared halo assignments explicit, so assembling it does not overwrite a conflicting guide. The [recipe guide](recipes.md) shows native `place`/`finalize` assembly and the complete component interfaces. A minimal programmatic preparation is:

```python
from research.staged_blocks.recipes import phase_assembly

assembly = phase_assembly(side=129, r=0, phase=0, delay=1, control="11")
prepared = assembly.prepare()  # One compatible initial state and fixed tensor.
spec = assembly.experiment_spec(identifier="my-four-pieces", steps=40)
```

`spec` is ordinary experiment data accepted by `research.experiments.run`; no component callback participates in evolution. The helper reproduces all 256 validated phase preparations exactly. Parameters outside that finite domain require an explicit exploratory preparation and acquire no automatic behavioral guarantee. Collect the recipe demo as `--study recipes:composition=runs/phase-pieces`.

The reusable `effective_coupler(...)` and `two_lane_pause(...)` constructors in `composed_recipes.py` also return compatible preparations with `.prepare()` and `.experiment_spec()` methods. Their complete initial states match all 64 transmission and 32 encounter preparations, respectively; this equality check adds no trajectories. See the [recipe guide](recipes.md) for their explicit domains and examples.

The optional exact-integer synthesis study needs its research dependency. It does not add a dependency to the engine:

```bash
python -m venv .venv-research
.venv-research/bin/python -m pip install z3-solver==4.15.4.0
.venv-research/bin/python -m research.staged_blocks.run study synthesis --output runs/staged-synthesis
```

The separately registered parity-preserving encoding is selected explicitly with `study synthesis-even --output runs/staged-synthesis-even`. It has its own frozen protocol, query and result. It does not revise the original solver outcome. Collect that result using `--study parity:synthesis=runs/staged-synthesis-even`.

The solver selects initial preparations outside a run. Its proposed state is accepted only after complete forward replay and independent audit. A resource limit or solver `unknown` is inconclusive; bounded `UNSAT` excludes only the encoded family. No stage runs automatically when the package is imported. Full research validation uses the pinned optional dependency; the existing CI workflows do not install Z3 and may skip solver-specific tests. Their success alone does not certify those optional checks.

Collect already completed studies and audit the resulting manifest:

```bash
python -m research.staged_blocks.run collect \
  --study composition=runs/staged-demo \
  --study orbit=runs/staged-orbit \
  --study interaction=runs/staged-interaction \
  --study synthesis=runs/staged-synthesis \
  --output runs/staged-report
.venv-research/bin/python -m research.staged_blocks.run audit \
  --manifest runs/staged-report/audit_manifest.json \
  --output runs/staged-report/audit.json --max-cpu-seconds 600
```

Include only studies that have completed and saved `protocol.json` and `result.json`. `collect` never runs missing experiments or changes their assessments. It retains all complete record references, including failed outcomes; a solver result can legitimately have no forward recording. The combined Presenter contains the studies' declared display selections. Complete records remain separately available for audit.

Use `--study ID:KIND=DIRECTORY` to include separately registered studies of the same kind, for example `--study signed:interaction=runs/signed-interaction`. Their protocols, control comparisons and assessments remain separate.

The additional `study phase` and `study signed` commands run separately frozen phase-memory and coupling-comparison protocols. Collect them with `--study phase:interaction=DIRECTORY` and `--study signed:interaction=DIRECTORY`. A change from `+++` to `+-+` is made before a new run. Keeping the same numerical seed and transforming a complete carrier/guide/halo preparation are distinct comparisons.

`study transmission` tests state-dependent transmission with its own controls; collect it as `--study transmission:interaction=DIRECTORY`. `study bridge` tests the bounded two-lane stop/wait/restart preparation; collect it as `--study bridge:interaction=DIRECTORY`. An isolated holding region and a center whose net input vanishes through ongoing internal driving are separate outcomes.

`study motion` audits exact translations and moving observation coordinates in pinned existing recordings; collect it as `--study motion=DIRECTORY`. Moving a readout or changing an initial placement is not evidence that the complete apparatus moves during a run. This analysis adds no duplicate Presenter trajectories.

## View the cube and clocks

The existing generic Presenter reads complete recorded states. It preserves all 48 channels, every retained remainder, all arithmetic `C0/C1/C2` events and fixed passive readouts. It does not simulate or choose a path.

Open the generated `The_Presenter.html` in a browser with JavaScript enabled. For a locally served combined report:

```bash
python -m http.server 8000 --directory runs/staged-report/presenter
```

Then open `http://localhost:8000/index.html`, whose inventory lists every recording and its self-contained Presenter page. Choose a recording in the experiment selector, use Play or Step, drag the cube to rotate it, and use Reset view to see the full cube. Select a node and channel to inspect its clocks and exact algebra. A narrow active guide can occupy one line inside a three-dimensional board; the cube boundary still represents all three spatial directions.

An attachment preview may not execute JavaScript. The HTML therefore includes a static inventory of its embedded recordings. An inventory without interactive controls is a preview limitation, not a completed browser playback test. Do not infer iPad or Safari compatibility from a server-side Canvas check.

A prepared four-cycle may rotate on every board update while producing no arithmetic C. Repeated phase-readout edges are not clicks. An encounter can change a lasting relative phase stored in the counters and halo; whether a recorded study meets that contract is assessed separately. The display retains raw arithmetic C alongside these passive observations.

Package any other complete native recording without changing the viewer:

```bash
python -m research.staged_blocks.export \
  --input path/to/record.json.gz \
  --input path/to/another-experiments.json \
  --output runs/another-presenter
```

The exporter rejects duplicate experiment IDs, malformed states, altered hashes, invalid transitions and excessive input size. `collect` uses deterministic page packing under the unchanged limits of 64 experiments, 500,000 complete sparse rows and 64 MiB per page. Each page is self-contained; `index.html` lists every experiment and page link. No experiment or frame is split or dropped. Add `--pages` to the standalone export command for the same behavior. A single experiment too large for a page fails clearly. Existing output directories are not overwritten.

Recorded-state GIFs can be rebuilt without a browser using the optional Node.js packages `jsdom 26.1.0` and `@napi-rs/canvas 0.1.80`, followed by Pillow (`13.0.0` in the recorded environment). With those dependencies available:

```bash
STAGED_PRESENTER_IMAGE_PLAN=research/staged_blocks/presenter_images.json \
STAGED_PRESENTER_ANIMATION_PLAN=research/staged_blocks/presenter_animations.json \
node research/staged_blocks/presenter_smoke.cjs runs/staged-canvas \
  research/staged_blocks/evidence/composition/The_Presenter.html
python -m research.staged_blocks.animation \
  --report runs/staged-canvas/report.json --output runs/staged-animation
```

Every animation image corresponds to one saved native state. Large side panels reuse the Presenter clock/gear SVGs and show exact counter/remainder values and raw C. Their addresses are taken from the saved assembly ports. This is Canvas/SVG rendering with an emulated viewport; it does not verify a browser's CSS layout. The [research report](../../docs/STAGED_BLOCKS.md) links the reviewed previews and their limitations.

## Composition and acceptance

The same complete tensor, board, background and initial time must be shared by joined components. Conflicting channel assignments and incompatible reservations are errors, not opportunities to add counters or replace one component. Different couplings can be compared in separate preparations; they cannot be installed locally or changed during an experiment.

An assembly report answers whether the initial definitions are compatible. Each behavior still requires its own fixed controls, response window, retained local state and complete-board audit. A real splitter requires one input to produce two outgoing carriers. Two initially prepared packets only test a two-input interaction. A quiet outlet does not erase information from the reversible full state. A supplied approval tests conditional response before an internally returned approval is claimed.

The stage catalog is a research checklist with explicit evidence domains. Its barriers are reporting barriers; no catalog decision, complexity score or software timeout alters the board. A periodic waiting candidate has a separate complete center-and-halo predicate, covers all four arrival phases, and does not retroactively satisfy the earlier zero-counter waiting contract.

## Implementation map

| File | Responsibility |
|---|---|
| `contracts.py`, `stages.json` | Evidence categories, prerequisites and acceptance gates |
| `composition.py` | Compatible one-time assembly and multi-component controls |
| `recipes.py` | Reusable carrier/interface/reference/guide preparation and passive phase observation |
| `composed_recipes.py` | Data-only effective coupler and scheduled two-lane pause preparations |
| `orbit.py` | Prepared four-cycle and complete halo contract |
| `interactions.py` | Fixed-protocol carrier/apparatus interaction studies |
| `synthesis.py` | Bounded external preparation search with exact integer constraints |
| `audit.py` | Independent full-state replay and control validation |
| `run.py`, `export.py` | Explicit commands, evidence indexing and generic replay packaging |

Research evidence belongs under this package; regression checks belong under `tests/`. The engine and Presenter implementations remain shared and unchanged. See the [research report](../../docs/STAGED_BLOCKS.md) for measured outcomes, limitations and the next decision, and the [algorithm review](../algorithm_analogues/README.md) for the source-backed architectural proposals.

The [light-bridge hypothesis](light_bridge_hypothesis.md) separates mathematical board carriers from observed photons and states the tests needed for an invariant-light-speed interpretation. The claim that light is the sole observable invariant remains a hypothesis; it is not an accepted result of these demonstrations.

## Validation of this release

The [validation receipt](evidence/release_validation/receipt.json) records 202 passing tests with zero skips in the pinned optional-solver environment, two reference CLI audits, the complete independent certificate and the final 56-recording Presenter smoke. The collection's saved `audit_status=not_run` predates that certificate and remains unchanged for provenance. Verification success does not convert rejected behavior criteria or solver timeouts into positive components.

Replay the published audit without generating new experiments:

```bash
.venv-research/bin/python -m research.staged_blocks.run audit \
  --manifest research/staged_blocks/evidence/final_collection/audit_manifest.json \
  --output runs/staged-audit.json --max-cpu-seconds 600
```

Run `python -m research.experiments.materialize_evidence` first in a fresh checkout to restore the pinned historical evidence required by the full repository test suite.
