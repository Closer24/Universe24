# Ray viewer

A 3D viewer and GIF renderer for the ray-event model, built to the model
owner's visualization requirement of 2026-09-17 (issue #169). It is a
Renderer in the sense of [Highlights](../../docs/HIGHLIGHTS.md) 3.29 and
3.30: it reads the record a run left on disk and never the engine's live
state. Nothing under `tools/ray_viewer/` imports the simulator.

## What it shows

- Dark background. A ray is a ray, not a particle: a bright segment on the
  Link it is crossing, an arrowhead in its heading, a fading trail of the
  Links it walked since its event, and a label with family and amount. Hue
  is the phase when the record carries one (grey when it does not).
- A family declared as a field (`field_of` in its `spatial_fields` entry,
  feature 7; until then a family whose name says `field`) is drawn faint and
  thin, with a short trail and no label.
- Every event is a marker at its Node that stays for the rest of the run:
  emission, meeting of rays, crossing without interaction, Detector PASS
  click, Detector RETURN, reversal, trajectory change, family change, the
  arrival of a returning ray at its event Node, escape through an open Link,
  and a generic marker for any record kind the extractor does not know. The
  Ports the event sent to are short spokes from the marker.
- At a meeting the incoming trails end at the marker and the outgoing rays
  start there. The caption of that tick names the declared coupling and the
  invariants (amounts, momentum, phase in and out) read from the record.
- Motion in three dimensions: rays on y and z are drawn like rays on x; the
  lattice grid, the axis ranges and a bounding box are the depth cues; the
  view turns once per 120 s (a checkbox stops it; a GIF advances a few
  degrees per frame).
- Detector marks are drawn as marked Nodes with their setting and the bits
  drawn so far; the family totals and the run's conservation line are in the
  caption, tick by tick.
- External bodies, by [Highlights](../../docs/HIGHLIGHTS.md) 3.19: "In a
  rendering every external body carries its own identifying picture (a star,
  a mirror, a wall), so it is never mistaken for matter." That picture is
  distinct from matter and from the Detector mark; a splitter, a phase plate
  and a screen get theirs as well. The record does not carry external bodies
  yet (`external-body-v1` is feature 7b); once the runner writes
  `external_bodies` into the record, the viewer draws each one at its Node
  with such a marker. Until then, a record kind the extractor does not know,
  an external body's events included, is drawn as a generic marker.
- Text is at least 14 px; the page works at 400 px width.

## What the record must contain

`extract.py` reads the files the runner writes next to `run.json`:

| File | Used for |
| --- | --- |
| `run.json` | model, status, shape, boundary, completed ticks, fingerprints (`source_sha256`, `initialization_sha256`), `ray_state`, `detector_mark`, initial, final and escaped totals, the conservation report |
| `events.jsonl` | `spatial_sent` (position, Port, arrival tick) and `spatial_received` (per-Port family amounts) build the Link transits; `spatial_escaped` the escapes; `spatial_cycle` deltas annotate emissions; `detector_click` the PASS markers; any other kind becomes a generic marker (`cycle_started`, `cycle_committed` and `spatial_cycle_started` are host timing and are skipped) |
| `initialization.json` | families and which are ray fields (and fields of a family), sources (`seeds`), Detector marks (`detectors`), the declared couplings (`ray_interactions`, `spatial_couplings`) |
| `ray-recording.json` (optional) | a per-tick ray listing written by a recording tool such as `examples/generic-ray-coupling/run_experiments.py`: phase per Link, and the ray-event fields `steps`, `outbound`, `event_ports`, `event_shares`, `detector` when the recording carries them |

The runner's record alone gives rays, trails, markers, amounts and
momentum; it does not carry a phase or the ray-event fields, so those show
as unknown until the record does. Rays are chained from the Link transits:
a Node that receives one share and sends it on continues the ray; a Node
where two or more shares are present, or where one share leaves changed,
is an event, and its outputs are new rays. A returning ray (feature 3) will
appear as a reversal at a marked Node and as an arrival marker when it
reaches its event Node; field rays (feature 7) as faint rays of their
family. Both need only the record kinds above, or the ray fields when the
runner starts writing them on `spatial_sent`.

## Run

```bash
python tools/ray_viewer/extract.py artifacts/run/run.json --out runs.json
python tools/ray_viewer/render_gif.py runs.json --output electron.gif
```

`extract.py` takes one or more records (a `run.json` or its directory) and
writes one `runs.json` (`ray-viewer-runs-v1`); `--label` names each run in
order. `render_gif.py` writes the GIF, a contact sheet (`--contact-sheet`,
default `<output>-contact.png`), a few stills and `render-summary.json`
under `--work`, and with `--html PAGE` the viewer page with the runs
inlined. Arguments: `--frames` (default ticks + 1 + `--hold`), `--step`
degrees of azimuth per frame, `--width`, `--colors`, `--frame-ms`,
`--elevation`, `--start-angle`, `--run KEY` to select runs (stacked
vertically), `--three PATH` for a local copy of Three.js r128.

To use the page interactively, open `viewer.html` with a `runs.json` beside
it over HTTP (`python -m http.server` in that folder), pass `?runs=URL`, or
open the page from disk and pick the file. The page loads Three.js r128 from
`https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js`; the GIF
renderer answers that request from a local copy (an explicit `--three`, a
cached copy under `$XDG_CACHE_HOME/ray_viewer/`, or one download checked
against the pinned SHA-256) and blocks every other request, so a capture
needs no network. Playwright and Chromium must be installed (`pip install
-e '.[render]'`, then `playwright install chromium` where a browser is not
already present).

## A GIF is a rendering, not evidence

A GIF or page made here is a rendering of a fingerprinted record: the
caption carries the model, `source_sha256` and `initialization_sha256` of the
run, and every number on it comes from `run.json`, `events.jsonl` and the
recording. It shows what the record holds and nothing more; it is not a
measurement, does not establish agreement with nature, and does not stand
in for the test or the [validation entry](../../docs/VALIDATION.md) that
identifies the source tree. Judge a claim by the record and its checks; use
the picture to read them.

## Test

`tests/test_ray_viewer.py` runs a two-lamp world for six ticks through the
runner and checks the extracted rays, events and captions against the pins
in [test expectations](../../docs/TEST_EXPECTATIONS.md#ray-viewer-extraction),
with no browser. The page and the renderer are checked by rendering a
record and looking at the stills; that is a visual check, not a test.
