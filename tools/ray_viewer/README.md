# Ray viewer

A 3D viewer and GIF renderer for the ray-event model, built to the model
owner's visualization requirements of 2026-09-17 (issue #169). It is a
Renderer in the sense of [Highlights](../../docs/HIGHLIGHTS.md) 3.29 and
3.30: it reads the record a run left on disk and never the engine's live
state. `extract.py` and `viewer.html` import nothing of the simulator;
`record_sidecar.py` is a Recorder (it replays a record through the
Simulation API to store what the runner does not write) and is the one file
here that touches the engine.

## What it shows

- Dark background. A ray is a ray, not a particle: a small bright head in
  its family colour, a short segment from its Node along its heading
  (`sizes.head_links` 0.5 of the Link, `ray_width_px` 3; `head_links` 1
  draws the whole Link), a tiny momentum arrow at the head in its heading
  whose length is its amount times `sizes.momentum_arrow_px_per_quantum`
  (1.75 px, so 14 px for an electron of 8, with an `arrowhead_px` 5 head;
  `draw.momentum_arrow`, `colors.momentum_arrow`; with the flag off the
  small arrowhead alone remains), and a faint white wake 6 px wide fading
  smoothly to nothing over the last ten Links, one opacity per Link, so the
  path is understood without a hard cut (`colors.trail`, `sizes.trail_links`
  10 and `trail_fade` [0.35, 0.0]; 0 draws the whole path since the ray's
  event).
  Matter families have a fixed high-contrast colour and the phase hue shows
  on the arrowhead (`draw.hue_by_phase`: `arrowhead`, `ray` or `none`; grey
  when the record carries no phase). A label per ray, family and amount,
  placed only where it is at least 24 px from every other label and overlaps
  none, is available (`draw.labels.rays`) and off by default, so that nothing
  on the board reads as text.
- A family declared as a field (`field_of` in its `spatial_fields` entry,
  feature 7) is drawn faint and thin, with a short trail, no arrowhead and no
  label. A release, the field rays leaving a Node with the ray that crosses
  it, is its own event kind, `release`: no marker, no caption line, and the
  source ray's trail runs through it unbroken.
- Every other event is a marker at its Node that stays for the rest of the
  run, told by shape and colour alone (the legend under the canvas names
  them): emission, meeting of rays (also a trajectory or family change),
  Detector PASS, Detector RETURN with the arrival of a returning ray at its
  event Node, inverse split, and escape through an open Link as a small dot.
  Escapes of field rays are drawn as nothing. Crossings without interaction
  and an absorption into a body's sink end or continue the rays but draw
  nothing. A record kind the extractor does not know becomes a generic
  marker.
- At a meeting the incoming trails end at the marker and the outgoing rays
  start there. The caption of a tick lists meetings, Detector events and
  inverse splits, at most three and then "and N more", says once how much
  escaped (matter and field apart) and counts the emissions; every number is
  read from the record, and the coupling named is the declared one. The
  totals line gives each family's amount in the world and escaped, and the
  run's conservation line. At phone width both lines are clamped to two
  lines.
- Motion in three dimensions: rays on y and z are drawn like rays on x; the
  lattice grid and a bounding box are the depth cues, with no text on the
  board except the ray labels; the view turns once per 120 s (a checkbox
  stops it; a GIF advances a few degrees per frame).
- No cubes: sources, Detector marks, external bodies and ray heads are
  smooth spheres (`draw.marker_shape` `sphere`; `cube` and per-kind
  `shape_overrides` remain) with a soft specular, a little emissive light of
  their colour and an additive glow behind them (`draw.glow`); they differ by
  colour and size (`source_size`, `detector_size` with `detector_alpha`,
  `body_size`, `head_radius_px`), not by polygon. Every external body keeps
  its identifying mark (Highlights 3.19: "In a rendering every external body
  carries its own identifying picture (a star, a mirror, a wall), so it is
  never mistaken for matter"): its colour and size, and in `cube` mode the
  picture chosen by family in the style (`star`, `plane`, `slab`); it stands
  at the position the record gives for the tick shown. None of them carries
  text.
- The picture is soft: a dark blue-black vignette (`colors.scene` fading to
  `scene_edge`, `draw.vignette`), a faint lattice (`lattice_alpha`,
  `node_dot_alpha`) inside a thin box (`box_alpha`), field rays as faint
  cyan-white hairlines with additive glow (`draw.field_additive`), event
  markers as thin glowing rings (`marker_ring_thickness`, `marker_alpha`),
  small dim escape dots (`escape_alpha`), and, in the `full` GIF preset, a
  GIF rendered at twice the size and scaled down (`gif_supersample`) for
  gentle anti-aliasing.
  The camera fits the action (`motion.camera_fit` `rays`): the box around
  every matter ray path, source, Detector mark and body over the run, padded
  by `camera_fit_margin_links`, holds the lattice and the thin box, with the
  board's own edges fainter around it; `board` fits the whole board.
- Text is at least 14 px; the page works at 400 px width. By default the
  page shows the board with one title line, the run's title from the record,
  and the tick counter; every other block of text around it (record line,
  legend, captions, totals, controls) is off in `draw.page_text` and switched
  on there when wanted; playback starts on load with the slow rotation and
  loops (`motion.autoplay`, `motion.loop`), and the space key pauses and
  resumes.

## The eye view

By the model owner's decision on Highlights 5.4 ("everything begins and is
realized at a marked Node"), the physical picture is the list of PASS
clicks; the board rendering is the record's view. `draw.view` chooses:
`board` (the default, everything above) or `eye`, which draws only the
marked Nodes as dim spheres and each PASS click as a bright flash of its
family's colour at its Node, sized by amount (`click_flash_px_per_quantum`,
`click_flash_min_px`), fading over `click_flash_ticks` and leaving a
persistent dim dot (`click_dot_px`, `click_dot_alpha`), like a screen
accumulating hits; no rays, fields or other markers; the title, the tick
and the camera fit as before. A run without a mark has an empty eye view,
which is itself the point. `extract.py` writes the `eye` block of every run
(marks, clicks, hits per Node); `render_gif.py --view eye` renders that
view, and `--side-by-side` renders the board view and the eye view as two
panels, left and right, in one GIF and one contact sheet. A mark's sphere
is drawn without depth writing and without glow, the flash and the dot on
top of it, so hits inside the sphere show, and the dot's radius grows with
the square root of the hits at its Node (its area with the count), a spot
on a screen. `examples/nature/screen.json`
([its README](../../examples/nature/README.md#the-screen-the-field-of-an-electron-at-rest-on-seven-marks))
is the demonstration: an electron at rest releasing its field in front of
a screen of seven marks, one of which clicks before feature 12.

## The look lives in `style.json`

Everything about how the renderer looks and what it shows is in
`tools/ray_viewer/style.json` (`ray-viewer-style-v1`), by the model owner's
decision of 2026-09-17: a change of look is a file edit and a re-render,
never a code change. Its sections and keys, all of them, are:

| Section | Keys |
| --- | --- |
| `colors` | `background`, `surface`, `scene` (the vignette's centre), `scene_edge` (its edge), `ink`, `muted`, `line`, `accent`, `lattice`, `box`, `trail` (the wake), `momentum_arrow`; `families` (`default` and `field` rules, plus one entry per family name to override: `hue` `phase` or `fixed`, `color`, `trail`, `saturation`, `lightness`, `alpha`); `markers` (a colour per event kind: `emission`, `meeting`, `deflection`, `conversion`, `click`, `return`, `arrival`, `split`, `escape`, `other`); `source`, `detector`, `external_body` |
| `sizes` | `ray_width_px`, `head_radius_px` (a sphere head, on screen), `head_links` (a segment head's length as a fraction of its Link), `arrowhead_px`, `momentum_arrow_px_per_quantum`, `momentum_arrow_width_px`, `trail_links` (0 for the whole path since the ray's event), `trail_width_px`, `trail_fade` (opacity at the newest and the oldest trail Link), `field_width_px`, `field_trail_links`, `field_arrowhead`, `marker_radius`, `marker_ring_thickness`, `marker_alpha`, `escape_dot_radius`, `escape_alpha`, `click_flash_ticks`, `click_flash_px_per_quantum`, `click_flash_min_px`, `click_dot_px`, `click_dot_alpha`, `mark_alpha` (the eye view), `source_size`, `detector_size`, `body_size`, `detector_alpha`, `glow_scale`, `glow_alpha`, `sphere_roughness`, `sphere_metalness`, `sphere_emissive`, `label_font_px`, `label_min_distance_px`, `node_dot_px`, `node_dot_alpha`, `lattice_alpha`, `box_alpha` |
| `draw` | `view` (`board` or `eye`), `markers` (the event kinds that get a marker), `marker_shapes` (kind to `diamond`, `ring`, `cube`, `octahedron` or `dot`), `marker_shape` (`sphere` or `cube` for sources, Detector marks, bodies and heads) with `shape_overrides` (per kind: `source`, `detector`, `body`, `head`), `glow`, `vignette`, `field_additive`, `labels` (`rays`, `fields`, `markers`, `sources`, `detectors`), `label_text` (`{family}`, `{amount}`, `{phase}`), `escapes` (`matter`, `all` or `none`), `sources`, `detectors`, `external_bodies`, `apparatus` (`default` picture and one per family or coupling name: `star`, `plane`, `slab`), `trails`, `momentum_arrow`, `hue_by_phase` (`arrowhead`, `ray` or `none`), `silent_field_events`, `page_text` (`header`, `record`, `legend`, `captions`, `totals`, `tick_counter`, `controls`, each a boolean) |
| `caption` | `kinds` (the event kinds listed), `max_per_tick`, `more`, `emissions`, `escapes`, `field_escapes`, `empty`, `totals` (`{family}`, `{in_world}`, `{escaped}`, `{on_links}`, `{held}`, `{sourced}`), `conservation` (`{status}`, `{balanced}`, `{every_tick}`) |
| `motion` | `rotation_seconds_per_turn`, `autoplay`, `loop`, `page_ticks_per_second`, `gif_degrees_per_frame`, `gif_frames` (null for ticks + 1 + hold), `gif_hold_frames`, `gif_width_px`, `gif_frame_ms`, `gif_colors`, `gif_supersample`, `gif_preset` (`phone` or `full`, the GIF preset the renderer uses without `--preset`), `gif_presets` (one object per preset name, each overriding `gif_width_px`, `gif_panel_px` (per panel side by side), `gif_max_frames`, `gif_hold_frames`, `gif_hold_still`, `gif_colors`, `gif_supersample`, `gif_seconds`, `gif_frame_ms`, `gif_target_bytes` and `contact_stills`), `contact_stills`, `elevation_deg`, `start_angle_deg`, `camera_fit` (`rays` or `board`), `camera_fit_margin_links` |

`viewer.html` reads the style from its inlined `<script type="application/json"
id="style">` block when the renderer filled it, else from `?style=URL`, else
from `style.json` next to the page, else from its built-in copy of the
default (`id="style-default"`, kept equal to the file by the test). A partial
style file overrides only the keys it names. `render_gif.py --style FILE`
inlines that file and takes every default of its arguments from the file's
`motion` block; an unknown key is refused.

## What the record must contain

`extract.py` reads the files the runner writes next to `run.json`:

| File | Used for |
| --- | --- |
| `run.json` | model, status, shape, boundary, completed ticks, fingerprints (`source_sha256`, `initialization_sha256`), `ray_state`, `detector_mark`, `released_field`, `external_bodies` (declaration, `positions` per tick, final state), initial, final, escaped and source totals, the conservation report, and `audit`, the world ledger per completed tick (`ray-event-audit-v1`: amount, momentum and charge lines with initial, sourced, current, escaped, annulled and absorbed), carried into the `conservation` entry for the caption |
| `events.jsonl` | `spatial_sent` (position, Port, arrival tick) and `spatial_received` (per-Port family amounts) build the Link transits; `spatial_escaped` the escapes; `spatial_cycle` deltas count the sources tick by tick and annotate emissions; `detector_click` the PASS markers; `external_body_absorbed` ends the rays a body took, and gives their transit into the body's Node the amount the receiver's reading leaves out (at a coupled body only the absorbed families end there); any other kind becomes a generic marker (`cycle_started`, `cycle_committed`, `spatial_cycle_started` and `external_body_step` are host timing or already in `run.json` and are skipped) |
| `initialization.json` | families and which are ray fields (and fields of a family, with their `release`), sources (`seeds`), Detector marks (`detectors`), the declared couplings (`ray_interactions`, `spatial_couplings`) |
| `ray-recording.json` (optional) | a per-tick ray listing: phase per Link, and the ray-event fields `steps`, `outbound`, `event_ports`, `event_shares`, `detector` when the recording carries them |

The runner's record alone gives rays, trails, markers, amounts, momentum
and per-tick totals (initial plus the sources through the previous tick
minus the escapes, which equals a recording's totals tick by tick); it does
not carry a phase or the ray-event fields, so those show as unknown until a
recording supplies them. Rays are chained from the Link transits: a Node
that receives one share and sends it on continues the ray; a Node where two
or more matter shares are present, or where one share leaves changed, is an
event, and its outputs are new rays; a field ray passes a Node in silence
unless it leaves changed there, which is a meeting with the matter at that
Node, and field rays leaving with a departing matter ray are its release.
From the transits alone a swap of two equal rays without a delay cannot be
told from a crossing, and a released share that joins a passing field ray on
the same Link is drawn with it.

### The sidecar

The runner does not write `ray-recording.json`. `record_sidecar.py` writes
it beside a record by replaying the preserved `initialization.json` through
the Simulation API for the recorded ticks, capturing every tick with
`examples/generic-ray-coupling/evidence.capture`, and checking first that the
source fingerprint equals the run's `source_sha256` and then that the
replay's event stream equals `events.jsonl` line for line; it refuses
otherwise, so a sidecar always belongs to its record. It must run on the
source tree that made the run:

```bash
PYTHONPATH=src python tools/ray_viewer/record_sidecar.py artifacts/run
python tools/ray_viewer/extract.py artifacts/run --sidecar artifacts/run/ray-recording.json --out runs.json
```

`--sidecar` names the recording explicitly (one per record, in order);
without it `extract.py` uses a `ray-recording.json` beside `run.json` when
one exists, and a recording whose fingerprints differ from the run's is
refused.

## Run

```bash
python tools/ray_viewer/extract.py artifacts/run/run.json --out runs.json
python tools/ray_viewer/render_gif.py runs.json --output electron.gif
```

`extract.py` takes one or more records (a `run.json` or its directory) and
writes one `runs.json` (`ray-viewer-runs-v1`); `--label` names each run in
order and `--sidecar` its recording. `render_gif.py` writes the GIF and
`render-summary.json` under `--work` (the GIF's size in bytes is always
printed), and with `--html PAGE` the viewer page with the runs and the
style inlined. `--preset` picks a GIF preset from the style's
`motion.gif_presets`; without it the style's `gif_preset` applies. `phone`
(the default; the model owner's phone, 2026-09-17): 640 px wide, 480 px per
panel side by side, at most 20 frames spread evenly over the run so it
still reaches its end (at most a quarter of them holding the last tick,
the camera still during the hold, `gif_hold_still`, so the GIF stores the
hold once with its whole duration), 128 colours, no supersampling, the
frame duration set so the GIF reads in about six seconds (`gif_seconds`),
a target of under 1 MB (`gif_target_bytes`, noted beside the size when
exceeded, never refused), no contact sheet and no stills. `full`: the
large GIF, 640 px per panel, every tick and twelve hold frames turning on,
supersampled, with a contact sheet of
`contact_stills` frames (`--contact-sheet`, default `<output>-contact.png`)
and a few stills under `--work`. The arguments `--frames` (a frame count
the run is spread over), `--hold`, `--step`, `--start-angle`,
`--elevation`, `--width`, `--colors`, `--frame-ms` and `--contact-stills`
(0 for none) override the preset; `--run KEY` selects runs (stacked
vertically); `--three PATH` names a local copy of Three.js r128.

To use the page interactively, open `viewer.html` with a `runs.json` (and
optionally a `style.json`) beside it over HTTP (`python -m http.server` in
that folder), pass `?runs=URL&style=URL`, or open the page from disk and pick
the file. The page loads Three.js r128 from
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

`tests/test_ray_viewer.py` runs a two-lamp world with a released field for
six ticks through the runner and checks the extracted rays, releases,
events and captions against the pins in
[test expectations](../../docs/TEST_EXPECTATIONS.md#ray-viewer-extraction),
pins the extraction of a body's recorded positions, and checks that
`style.json` has exactly the documented keys, equals the page's built-in
default and reaches the inlined page; no browser. The page and the renderer
are checked by rendering a record and looking at the stills; that is a
visual check, not a test. To type-check the tools, run
`MYPYPATH=src mypy --follow-imports=silent tools/ray_viewer`.
