# The Presenter

The Presenter is a generic, local viewer for complete Universe24 reference
experiments. It translates each recorded counter pair into a clock hand and
each retained remainder into a gear position. The same code displays the
supplied demonstrations, a newly exported experiment, a native checkpoint or
a consecutive native checkpoint trace. It does not identify a special guide,
experiment ID or channel pair in order to draw an experiment.

Open [The_Presenter.html](../research/presenter/demo/The_Presenter.html) in a
browser. All code and demonstration data are embedded in that file. No server,
account or network connection is needed.

## Reading a run

1. Choose an experiment and press **Play**, or step through the saved frames.
   Playback changes the selected recorded frame; it does not run a second
   physical law or intervene in the experiment.
2. Drag the cube to rotate it, and scroll to zoom into sparse activity. Its
   nodes show clock and remainder activity. Click a node to inspect its 48
   channels. **Focus retained state** in the **⋯** view options fits the sparse
   activity; **Reset view** restores the full cube. Both change only the camera.
   A zero counter pair is at rest;
   a retained remainder may still distinguish it from the background.
3. Select any channel to inspect its exact counters and remainder. The details
   show the six signed source counters from the preceding frame, their sum,
   the quotient, and the completed Rule3 update. At the first loaded frame,
   only the snapshot is available; no predecessor is invented.
4. Use **Open experiment** to display another bundle, native checkpoint or native
   trace. An invalid, incomplete or inconsistent import is rejected. A single
   valid snapshot remains useful even though it has no recorded motion.

The clock hand represents the direction of `(a,b)`, not an added clock or a
physical-time calibration. Its length is normalized, so equal directions can
have very different amplitudes. Exact decimal values remain available in the
details, including values too large for an ordinary JavaScript number. The
gear represents retained integer arithmetic:

```text
u = the sum of the six signed old neighboring b counters
2*u + r = 6*ell + r_next,     0 <= r_next < 6
a_next = b
b_next = ell - a
```

The quotient uses floor division, including for negative inputs. Camera,
filters, selection and playback speed do not change this arithmetic or the
experiment's fixed readouts. [PRESENTER_ALGEBRA.md](PRESENTER_ALGEBRA.md)
defines the visual interpretation, parity/three-position remainder identity,
arithmetic events and snapshot ordering precisely.

## Included demonstrations

The six demonstrations contain 104 complete snapshots and 98 forward
transitions. Generation verifies every transition and its inverse, then
rewinds each entire trajectory. All use the existing `Engine`; their only
pre-run choices are the fixed tensor and initial state.

| Experiment | What to inspect | Recorded updates |
|---|---|---:|
| Positive impulse | The existing `examples/impulse.json` preparation; its full state returns at steps 6 and 12 | 12 |
| Signed inputs across a cube boundary | Channel 47, all six signed inputs, periodic wrap and `-57 = 6*(-10)+3` in the first transition | 4 |
| Two prepared neighboring clocks | Adjacent motifs and their complete remainder field return to the preparation at steps 5, 10, 15 and 20 | 20 |
| A signal starts two clock records | The full existing `guide_N24` trace, including off-axis remainders; optional fixed M6/M12 predicates | 56 |
| A stationary remainder field | Nondefault background remainder 5 and all 48 channels at the selected node; no counter motion | 4 |
| 5,001-digit counters | Exact signed counters on channel 47, with an approximate direction only in the picture | 2 |

These cases demonstrate the range of the viewer. They do not establish light,
particles, physical measurement or a universal building-block construction.
The guide's records have finite retention; replaying them does not extend it.
The optional M6/M12 readouts are fixed metadata clauses on recorded remainders.
Their observed rising edges are M6 at steps 6 and 56, and M12 at step 12.
They are distinct from generic arithmetic event classes and never write state.

## Export and package another experiment

Run commands from the repository root. Output files and demonstration
directories must be new: the tools refuse to overwrite existing evidence.

```bash
python -m research.presenter.export \
  --config examples/signed_impulse.json \
  --id my-experiment --title "My experiment" \
  --output runs/my-experiment.json

python -m research.presenter.build \
  --input runs/my-experiment.json \
  --output runs/My_Presenter.html
```

`build` accepts any valid `universe24-presenter-v1` bundle and does not select
demo-specific code. A bundle may contain several experiments or an empty
catalog-enabled workspace. It validates full states and transitions before
writing a standalone HTML file and adjacent `.html.manifest.json` file.

To package an existing native trace, export its complete snapshots first:

```bash
python -m research.presenter.export \
  --trace research/building_blocks/evidence/cases/guide_N24/states.jsonl \
  --id imported-guide --title "Imported native trace" \
  --output runs/imported-guide.json
```

Use `--checkpoint path/to/checkpoint.json` for a single native checkpoint.
The exported checkpoint is a snapshot unless additional updates are requested
through the exporter's supported options. Loading a native file directly
through **Open experiment** uses the embedded catalog of all eight reference
couplings. Consecutive trace frames must share their side, background and
tensor; missing frames are not interpolated.

Python experiments can use the exporter without a config file:

```python
from research.presenter.export import capture, bundle, write_bundle

# engine and initial are the existing Engine and complete State preparation.
recorded = capture(engine, initial, steps=20,
                   id="new-preparation", title="New preparation",
                   view={"position": [1, 2, 3], "channel": 47})
write_bundle("runs/new-preparation.json", bundle([recorded]))
```

The `view` is an initial selection only. Optional readouts use generic
`all_equal` clauses on addresses and `a`, `b` or `r`; define them before the
run. Their truth values and rising edges do not depend on the selected channel
or visible slice. The portable format and exact field names are specified in
[CONTRACT.md](../research/presenter/CONTRACT.md).

## Rebuild the demonstrations and check imports

```bash
python -m research.presenter.demo \
  --output runs/presenter-demo \
  --fixtures runs/presenter-fixtures

python -m unittest discover -s tests -v

node research/presenter/data_checks.cjs

node research/presenter/browser_checks.cjs \
  runs/presenter-demo/The_Presenter.html \
  runs/presenter-browser-evidence \
  runs/presenter-fixtures
```

The browser check needs Playwright and an installed Chromium browser. It opens
the local HTML and imports held-out data whose IDs are absent from the embedded
demonstrations. Its fixtures exercise signed boundary inputs, channel 47,
channel 31, a nondefault background, large integers, snapshot-only input and
native consecutive traces. It independently computes expected displayed
arithmetic and produces a report plus screenshots. A browser execution result
must be read from that report; successful Python export alone is not a browser
rendering result.

The separate `research/presenter/dom_checks.cjs` harness runs the actual
application scripts in jsdom with native Canvas2D. It supplies explicit element
rectangles because jsdom does not lay out CSS. Its PNG files show actual canvas
drawing, not full-page browser screenshots. This check cannot establish browser
CSS layout, responsive behavior, accessibility or real pointer hit testing.

In the current workspace, the installed Chromium process exits with `SIGTRAP`
before opening a page. No successful real-browser run is claimed on the basis
of the DOM harness. The browser acceptance script remains available for a
machine where Chromium can start.

The final artifact's [DOM/native Canvas2D report](../research/presenter/evidence/dom-native-canvas/report.json)
records **10 passing check groups and zero errors**, covering all six embedded
experiments, unseen imports, exact 5,001-digit values, camera/state separation,
all-background snapshots, an empty workspace and hostile metadata. Its 73 PNGs
include a complete 57-frame recorded sequence. Those historical PNGs can be
restored from the pinned evidence archive.

The separately verified, published four-component demonstration has
[49 actual recorded frames in closeup](../research/experiments/evidence/publication_v1/render/sequence-01/recorded-clocks.gif)
and [the same 49 states in the rotating whole cube](../research/experiments/evidence/publication_v1/whole_cube_render/sequence-01/recorded-clocks.gif).
Both use the unchanged application's Canvas2D output. The real prepared
apparatus is linear within a three-dimensional periodic board; the uniform
background is omitted from drawing but retained in the full-state recording.
These animations are native-canvas checks, not browser-layout evidence.

The separate [browser attempt report](../research/presenter/evidence/browser-unavailable/report.json)
records `browser_launch_failed` and **zero executed browser checks**. Both
reports identify the exact final HTML SHA-256:

```text
3e3ddb0d86c5e05d8bc07fbbe2f939cf32da75f86d6605759074542556e9657e
```

To reproduce the DOM check with isolated local test dependencies:

```bash
npm install --prefix runs/presenter-dom-deps --no-save --ignore-scripts \
  jsdom@26.1.0 @napi-rs/canvas@0.1.80 playwright@1.56.1

NODE_PATH="$PWD/runs/presenter-dom-deps/node_modules" \
  node research/presenter/dom_checks.cjs \
  research/presenter/demo/The_Presenter.html \
  runs/presenter-dom-evidence \
  research/presenter/fixtures
```

Add `PRESENTER_RENDER_GIF=1` before `node` to generate the animation too; this
optional step requires `ffmpeg`. The report records dependency and test-source
versions. These testing dependencies are not needed to open the standalone
viewer. Documentation and reports are separate repository files; their later
updates do not change or silently replace the pinned HTML artifact.

`--data-only` on the demonstration command creates the same data and fixtures
before UI packaging. Package its `experiments.json` later with `build` if
needed. The demonstration generator has a 120 CPU-second budget; it records
actual elapsed CPU time in `generation_manifest.json`.

## Identity, exactness and limits

Each experiment records its checkout commit, dirty-tree status, source-file
hashes, tensor fingerprint, preparation state hash, complete saved states and
verification scope. A commit alone cannot identify uncommitted local work;
the source hashes identify the files actually used. The packager separately
records its input bundle hash, UI/build source hashes, verifier source hashes
and output HTML hash. Existing local traces retain their input-file hash.

A physical-state hash includes the board side, explicit sparse-background
convention and every nonbackground channel triple. It excludes the saved
step label, so returning to the same represented state gives the same hash.
Read it together with the tensor fingerprint: the same state under a different
tensor can have different future evolution.

Counters are canonical decimal strings in portable JSON and `BigInt` in the
browser. State arithmetic, comparisons and readouts do not pass through
floating-point graphics. All channels omitted from sparse storage equal the
explicit background; they remain addressable. No remainder is discarded.

| Resource | Default accepted bound |
|---|---:|
| Bundle or imported file | 64 MiB |
| Experiments in one bundle | 64 |
| Complete frames per experiment | 10,000 |
| Stored sparse channel records across the bundle | 500,000 |
| Decimal digits in one counter | 100,000 |
| Board side and recorded step | JavaScript safe nonnegative integer range; side at least 3 |
| Fixed readouts per experiment | 256 |
| Readout clauses across one experiment | 1,024 |

Limits reject unsupported input rather than silently truncating frames,
channels or digits. The Python export time budget is checked between complete
operations; it cannot interrupt a single engine step or JSON operation.
Browser memory and responsiveness also depend on the available machine.
Large accepted data should be reviewed against those practical constraints.

Generality here means all complete recorded experiments of the **current
reference family** within the format and resource bounds: one periodic cubic
board, 48 channels per site, six spatial inputs and one of the eight fixed
signed tensors. A different geometry or tensor family requires an explicit
format/model extension and separate validation. The Presenter is an observer,
not evidence that the current model already reproduces all physical phenomena.
