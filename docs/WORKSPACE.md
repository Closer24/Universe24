# Local simulation workspace

The workspace edits, checks and runs world files of the law of the shadow
([ENGINE.md](ENGINE.md)) with the same parser and runner as the command line.
It supplies no other engine and infers nothing from names.

## Start

Use the project Python 3.14 environment after the normal one-time installation:

```bash
python -m event_universe.ui
```

Open the printed local URL, normally `http://127.0.0.1:8765`. Only this
computer may reach the server, and every change carries the page's token.
`--configs FOLDER` selects the template folder (`examples/shadow/` by default),
`--output FOLDER` where runs are written (`artifacts/workspace` by default),
`--port 0` an available port.

## Choose, edit, check

The sidebar lists the worlds of the template folder; **Import JSON** adds your
own file as a draft. The editor is the whole world file as JSON. **Check**
runs the preflight (the strict decoder and the world parser; the message names
the key at fault) and shows the world's model, shape, ticks, families and
contents. **Export JSON** saves the checked draft. Drafts are kept per template
in the browser's storage; **Reset** returns to the template's file.

## Run and inspect

**Run** writes a snapshot of the draft and starts `python -m event_universe`
on it in another process, headless; the page stays responsive and one run at a
time is allowed, **Stop** ends it. When the run finishes the result shows the
record: the law, the completed ticks, whether the books balanced at every
tick, the held contents, and links to `run.json`, `state.json`, `events.jsonl`
and the input as read. Earlier runs of the session are listed below the
result. Generated files expire under [retention](RETENTION.md); the running
workspace cleans them periodically. Nothing here is physical evidence: a run's
readings are made by a script over its record, as the tests and the
[experiments register](EXPERIMENTS.md) do.
