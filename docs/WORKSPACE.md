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

The default templates are the canonical `examples/basic.json` and
`examples/exchange.json`, also included with installed packages. Their labels
describe data, not built-in physical laws. To use another directory:

```bash
python -m event_universe.ui --configs my-configurations --output artifacts/workspace
```

Valid JSON files in that directory appear on page load. Refresh after changing
the template files. Invalid files and files over 1 MiB are omitted. **Import
configuration** loads a validated JSON file as a custom draft; the original file
is preserved.

- **General:** model identifier, ticks, world dimensions, capacity and timing.
- **Fields:** names, scalar/vector structure, units, signs, scale and conservation.
- **Disturbances:** owned fields, defaults, transport and local updates.
- **Initial state:** seed positions, disturbance types and value overrides.
- **Rules & costs:** local exchange couplings and primitive operation prices.
- **JSON:** the complete schema, including optional members without form controls.

Nested rule/value editors accept JSON data. Both those editors and full inputs
reject duplicate JSON keys. Configuration cannot execute Python or JavaScript.
Check it before running or switching from raw JSON to forms. Errors identify
invalid members or references. Renaming or removing a field requires updating
its references; the editor does not silently rewrite model laws.

Drafts are saved per template in this browser. Switching templates keeps them;
**Reset** restores a template. **Export JSON** downloads the checked configuration
for later import or direct CLI execution. Browser storage is not a backup.
Exports are also saved in the workspace's `exports/` directory. If automatic
download is unavailable, use the **Download JSON** link shown after export.

The initial-placement diagram reads configured seed positions, not computed
motion. It is an isometric projection; concentric rings denote co-located seeds.
The preview never supplies physical inputs.

## Run and inspect

**Run simulation** submits an immutable snapshot. Later edits apply to the next
run. One run is active at a time; the existing CLI runs in a separate process.
Results show status, requested/completed ticks, elapsed host time, conservation
checks and artifact links. The current server session lists its latest 20 runs.
Page reloads preserve that list; restarting the server starts a new session,
while all saved output directories remain on disk.

Runs remain headless unless **Create a recorded view** explicitly enables the
existing generic sampled-state HTML. Its frame stride changes recording only.
The result link appears after completion. This is a generic data view, not the
historical particle animation or a live image stream.

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
