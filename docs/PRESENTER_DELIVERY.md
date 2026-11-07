# Opening The Presenter

`research/signal_clocks/evidence/presenter_delivery/Signal_Clocks.html` is a
self-contained, read-only viewer with the same 44 complete experimental
recordings as `interfaces_presenter_final/Signal_Clocks.html` (1,868 states).
The viewer does not need a separate experiment file for these recordings.

## Start and choose an experiment

1. Download the HTML file and open it in a current desktop browser.
2. Wait for the recorded states to be checked. The page reports progress.
3. Choose a recording from **Experiment**, above the cube. Use **Play** or the
   timeline to replay it. Drag the cube to rotate it and use **Look inside** to
   inspect a node.

**Open experiment** imports an additional recording. It is not the selector
for the recordings already embedded in this file.

If opening the local file does not supply Web Crypto, place the HTML in a local
folder and, from that folder, run:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Open `http://localhost:8000/Signal_Clocks.html` in that computer's browser.
This serves the saved recording locally; it does not evolve the model or
publish the recording. Stop the server with Ctrl+C when finished.

## Attachment previews and iPad

Some contexts display an HTML document without running its scripts. A static
preview can show the embedded recording list, but cannot play or rotate the
cube. This file cannot enable scripts inside another app. On a device that only
opens a file preview, the same HTML needs a browser context that executes it,
for example an HTTPS page. No hosting or deployment has been performed here.

The supplied screenshot is consistent with disabled scripts, but does not
establish that cause. The previous page also displayed a blank body when a
script failed before startup reached its existing error handler. The attachment
viewer and iPad Safari have not been tested in this environment.

## What changed

The generic viewer now shows a startup card before any JavaScript runs. The
standalone build includes a static inventory derived from the complete input
bundle, so the recordings remain visible when the interactive application does
not start. That inventory is explicitly labelled as a static list.

A small bootstrap runs before the data and application scripts. It reports
missing BigInt, TextEncoder, Promises, Canvas 2D or Web Crypto support, early
script errors and a missing application initialization. The normal startup card
is hidden only after the application has rendered or displayed its empty state.
The file-import button stays disabled until its handlers have been installed.

This is a delivery and diagnostics repair. It does not override a host's script
restrictions or establish that interactive playback works on the user's iPad.

## Evidence and preservation

- The 44-experiment source bundle was reused without changing any recorded
  frame, channel, remainder, readout or coupling.
- The prior 44- and 64-experiment standalone files remain unchanged. Their
  hashes, all 12 prior generic source files, and the engine source hashes are
  recorded under `research/signal_clocks/evidence/presenter_delivery/source_before/`.
- The new HTML has a separate build manifest recording its sources and input.
- All 94 Python regression tests passed; output is in
  `presenter_delivery/python-tests.txt`.
- DOM/native Canvas checks and independent delivery checks are reported in
  their corresponding evidence subdirectories. DOM checks supply browser APIs
  and geometry explicitly; they are not evidence of Safari execution, actual
  pointer hit testing, CSS layout or attachment-preview compatibility.
- `presenter_delivery/delivery_report.json` records the repair's hashes, checks
  and limits. The original and new embedded JSON payloads are byte-identical.

No engine code, model contract, preparation, coupling or readout definition was
changed. No repository changes were committed, pushed or deployed for this
delivery repair.
