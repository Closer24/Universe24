# Local simulation workspace

The workspace selects and edits initialization-defined simulations using the
same [JSON contract](DISTURBANCES.md) and validator as the CLI. It does not supply
another engine or infer laws from field names.

## Start

Use the project Python 3.14 environment after the normal one-time installation:

```bash
python -m event_universe.ui
```

On Windows, without activation:

```powershell
.\.venv\Scripts\python.exe -m event_universe.ui
```

Open the printed URL. The default is `http://127.0.0.1:8765`; keep the terminal
open while using the interface. `--port 0` chooses a free local port. The server
listens only on this computer. It is a local research tool, not public hosting.

The UI uses plain HTML, CSS and JavaScript with the Python standard library.
There is no frontend compiler, Node dependency or build command. Changing a JSON
configuration does not require compilation, package installation or restarting
the UI. The runtime validates and reads each submitted input afresh.

## Choose and configure

The default templates include two approaching particles, parallel particle beams,
a spreading conserved pulse, an unequal-mass elastic collision, Basic and Exchange,
all packaged from `examples/`. The Rules tab accepts atomic interaction definitions
with simultaneous assignments and conservation invariants.
The first three are idealized transport experiments, not validated electron,
proton, photon, electromagnetic-force or collision models. The approaching pair
meets and passes through; names and signed charge do not create attraction.
Their labels
describe data, not built-in physical laws. The separate collision example supplies
an explicit classical elastic law through generic expressions; its two unequal
masses rebound with conserved momentum and kinetic energy.
To use another directory:

```bash
python -m event_universe.ui --configs my-configurations --output artifacts/workspace
```

Valid JSON files in that directory appear on page load. Refresh after changing
the template files. Invalid files and files over 1 MiB are omitted. **Import
configuration** loads a validated JSON file as a custom draft; the original file
is preserved.

- **Names:** particle/type and field names, with references updated consistently.
- **General:** model identifier, ticks, world dimensions, capacity and timing.
- **Fields:** names, scalar/vector structure, units, signs, scale and conservation.
- **Disturbances:** owned fields, defaults, transport and local updates.
- **Initial state:** seed positions, disturbance types and value overrides.
- **Rules & costs:** local exchange couplings and primitive operation prices.
- **JSON:** the complete schema, including optional members without form controls.

Nested rule/value editors accept JSON data. Both those editors and full inputs
reject duplicate JSON keys. Configuration cannot execute Python or JavaScript.
Check it before running or switching from raw JSON to forms. Errors identify
invalid members or references. Name controls update type, seed, field, default
and rule references together; they do not change model arithmetic. Names are
unique within their category. A particle name identifies its disturbance type;
records of that type share it. The two-particle presets use distinct types so
each particle can have its own name. Raw JSON edits and removals still require
valid references.

Drafts are saved per template in this browser. Switching templates keeps them;
**Reset** restores a template. **Export JSON** downloads the checked configuration
for later import or direct CLI execution. Browser storage is not a backup.
Exports are also saved in the workspace's `exports/` directory. If automatic
download is unavailable, use the **Download JSON** link shown after export.

The initial-placement diagram reads configured seed positions, not computed
motion. It is an isometric projection; concentric rings denote co-located seeds.
The preview never supplies physical inputs.

## Movie and folded settings

The preset chooser, movie and Run & watch action are prominent. Configuration,
recording options, initial placement and result files start folded and open on
request. The Names tab gives quick naming controls without exposing local laws.

Run & watch creates a recorded movie by default. It appears inside the workspace
when calculation finishes; Open full view opens the same self-contained HTML.
Play/Pause, Restart, speed, XY/XZ/YZ projection and the timeline operate only on
saved samples. Playback stops on the final frame; Replay starts again. Scrubbing
pauses playback. Reduced-motion preference suppresses automatic playback.
Detailed field values and ownership remain available in the movie's folded table.

Filled markers are recorded resident disturbances. Link transfers use their
recorded origin, port and arrival time with the configured fixed transit time.
Concentric rings distinguish co-located records. The viewer does not invent
trajectories between snapshots or draw a false trail across a periodic seam.
The grid uses actual integer lattice nodes and equal axis scale. Tick arrows
select recorded frames; the default stride records every tick. Zoom and drag
expose individual nodes at larger scales. A dense view asks for zoom instead of
substituting a schematic grid. The approaching preset takes two ticks per link.

## Phone layout

Phone screens initially show the recorded movie and one Experiment controls
button. Presets, configuration, launch options and files remain hidden until
that button is opened; Back to movie restores the simple results view.
The self-contained animated HTML is the phone playback format, not a GIF export.
When controls are open, narrow screens use stacked panels, wrapping template cards and visible configuration
tabs. Movie, Run and Settings shortcuts jump to the relevant section without
discarding edits. Form text is at least 16 CSS pixels and buttons have at least
44 CSS pixels of touch height. Number fields request a numeric keyboard; JSON
editors keep their own horizontal scrolling. Conserved values wrap inside the
results table, and safe-area padding leaves room for phone cutouts in landscape.
Browser zoom remains enabled.

This layout adaptation does not change networking. The default loopback URL is
reachable only on the computer running the server; opening that same URL on an
iPhone does not connect to the computer. Phone network access requires a separate
deployment or connection setup.

## Run and inspect

**Run & watch** submits an immutable snapshot. Later edits apply to the next
run. One run is active at a time; the existing CLI runs in a separate process.
Results show status, requested/completed ticks, elapsed host time, conservation
checks and artifact links. The current server session lists its latest 20 runs.
Page reloads preserve that list; restarting the server starts a new session,
while all saved output directories remain on disk.

Turn off **Create a recorded movie** under Recording options for a headless run.
CLI runs remain headless by default. Frame stride changes recording only.
This is recorded generic-state playback after completion, not a live image stream.

During a lecture, use the prepared simulator to select or create a configuration,
export it, and run the saved file again. The lecture can produce a new reusable
experiment; it is not a simulator build session. Update and prepare the local
simulator separately when its GitHub version is outdated. Keep configuration
files and source versions together when comparing reproducible results.

Inputs are saved under `artifacts/workspace/inputs/<run-id>.json`, with runner
errors in an adjacent `.log`. Results are under `artifacts/workspace/runs/<run-id>/`.
Earlier runs are never overwritten. Metadata preserves source/input identities
and failed physical checks.

**Stop current run** terminates only that child. A cancelled run is explicitly
incomplete; files may be partial and final state/metadata may be absent. It is
not a completed or conservation-verified result. Ctrl+C stops the UI and its
active child. Forced OS shutdown cannot guarantee complete output.

Local Host/Origin checks and a per-session request token protect submissions.
Downloads are restricted to known artifacts from runs started in this session;
the server does not expose arbitrary filesystem paths or accept shell commands.
