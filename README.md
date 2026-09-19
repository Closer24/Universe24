# Universe24 — a three-dimensional event simulator

Universe24 implements **Reality Theory (Universe24)**: one discrete world of
Nodes and Links, bounded integer arithmetic and local rules. Since the evening
of 2026-09-18 the model is the law of the shadow ([Highlights](docs/HIGHLIGHTS.md)
section 5.4): matter is content held at Nodes, every ray in flight is a whole
quantum spreading by the Node's mixing, and an event is a whole quantum at held
content, absorbed, held or released again by the family's table; what is seen
is events. On 2026-09-19 the model owner's law of events (Highlights 5.4)
reads all of it as events, with no fields, no matter and no registers, a single
event leaving a Node whole in one direction; it is recorded and not yet
implemented. Since 2026-09-19 there is one engine, the field-only engine of that
law (`field-only-v1`); the old engine of the law of the bit is deleted
([migration](docs/MIGRATION.md#one-engine-on-2026-09-19-the-old-engine-deleted)).
The name of the framework is Reality Theory; the simulator that realizes it is
Universe24.

Canonical source: [Closer24/Universe24](https://github.com/Closer24/Universe24),
branch `main`. The Python package remains `event_universe`.

**Start here:** [AGENTS.md](AGENTS.md) contains the shared instructions and
English-only repository language rule. The active implementation lives in
`src/event_universe/`; [Boss and specialist skills](skills/boss-orchestrator/SKILL.md)
define coordinated work and independent checks.

A run is a **world file**: a JSON object with `"law": "shadow"`, the board's
shape and open boundary, the clock K and the phase width N, the release rate
and the wait's unit, the families (free, matter; paid, light) and the held
contents with their tables. The engine recognizes nothing by physical name.
Read [the engine](docs/ENGINE.md)
and the worlds under [examples/shadow/](examples/shadow/README.md) before
defining a run.

## Project specification (Google Docs)

[docs/HIGHLIGHTS.md](docs/HIGHLIGHTS.md) is the Universe 24 Highlights
specification, the high-level project specification, edited directly since
2026-09-17 by the model owner's decision. The Google Doc
[Universe 24 Highlights](https://docs.google.com/document/d/1IkhSyqZZMBSgbJV-PMMwcXG0D_Rlfg4FrLy2jXBMUSs/edit)
is its historical source up to the revision of 2026-09-16 and is neither
edited nor resynced. Opening it requires a Google account with document
access; repository access does not grant Google Docs access.

The specification contains goals as well as requirements. Keep proposed behavior,
implemented contracts and tested results distinct. Consult
[project status](docs/PROJECT_STATUS.md#specifications-and-gaps),
[POSTULATES.md](POSTULATES.md) and
[SIMULATOR_DEFINITIONS.md](SIMULATOR_DEFINITIONS.md).

## AI-ready monorepo

Start with [AGENTS.md](AGENTS.md), the [status guide](docs/PROJECT_STATUS.md) and
[monorepo ownership](docs/ARCHITECTURE.md#monorepo-ownership). Load only the
contracts and skills needed for the task. Verify actual source and GitHub state
before integration; documentation is not evidence of the latest remote head.

## Install and run

Python 3.14 is the development and minimum runtime, recorded in
[.python-version](.python-version). Use a project environment. A run needs
numpy, which the package installs:

```bash
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m event_universe --init examples/shadow/one_content.json --output artifacts/one_content
```

On Windows:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m event_universe --init examples/shadow/one_content.json --output artifacts/one_content
```

Select the environment's interpreter explicitly if activation is unavailable.
For development, install `python -m pip install -e '.[render,dev]'`.

Check a world file without running it:

```bash
python -m event_universe.configuration_validation examples/shadow/one_content.json --json
```

The world file is required. It supplies `ticks`; `--ticks` can override the
duration. Missing input is an error, not a request to load a built-in universe.
The board is open (`"boundary": "open"`): what leaves is booked as escaped, with
the momentum it carried; a closed board is refused. Run several worlds one
process per core with `tools/run_series.py`.

| Output | When written |
| --- | --- |
| `initialization.json` | Exact input file copied for reproducibility |
| `run.json` | The record: the law, the world's keys, the books per family at every tick, the contents, completion and elapsed time |
| `state.json` | The held contents and every Node with content, written Node by Node |
| `events.jsonl` | Streamed events |

Runs are headless; there is no visualization switch. Runs require a new or
empty output directory. Generated output expires 24 hours after writing
finishes; active writers remain protected. Original world files and templates
are preserved. See [output retention](docs/RETENTION.md) for ownership and
interrupted runs. The reported `elapsed_seconds` includes world construction,
the intervals, per-tick accounting, event writing and the final snapshot.

## Simulation configuration UI

Start the local workspace with the same installed Python environment:

```bash
python -m event_universe.ui
```

Open the printed local URL, normally `http://127.0.0.1:8765`. Choose a world of
`examples/shadow/` as a template, edit its JSON, **Check** it, and **Run**.
Each run reads a saved snapshot of the draft and runs headless in another
process; the workspace stays responsive. The result shows the record (the
law, the completed ticks, the books) and links to the input, state and events. Use `--configs` to select your own
template folder, or `--port 0` to choose an available port. See the
[workspace guide](docs/WORKSPACE.md) for drafts, files and interruption.

The running workspace cleans expired outputs periodically and removes expired
result links. CLI runs also check for expired output at startup. To keep cleanup
running while both are idle, use a watcher or schedule the cleanup command:

```bash
python -m event_universe.retention --root artifacts --root runs --watch
```

Use `--dry-run` to inspect candidates without deletion. A stopped watcher or an
offline computer catches up on the next cleanup; see [retention](docs/RETENTION.md).

## Check the project with one command

```bash
python tools/check.py
```

This runs lint, formatting, strict types and the tests of the changed files and
their consumers; `--full` runs everything. Every test is headless.
On Windows, `PYTHONUTF8=1` provides consistent UTF-8 handling for the check tools.
Current results belong in identified validation evidence, not an assumed pass
from this README.

## Project map

The [documentation index](docs/README.md) assigns one owner per topic and separates
active contracts, explicit experiments and revision-specific evidence.

| Path | Responsibility |
| --- | --- |
| `src/event_universe/shadow/world.py` | The world file: its keys, their bounds and the refusals, named |
| `src/event_universe/shadow/engine.py` | The engine: the held contents, the interval's steps (the events at held content, the wait, the mixing, the releases, the steps), the books and the readings |
| `src/event_universe/shadow/layer.py` | The arrays of one family: arrivals, parked shares and departures per Node and number, the walk one Link per interval, the wait as a hold per Node |
| `src/event_universe/shadow/mixing.py` | The Node's mixing kernels (`node-mixing-v1`, the remainder rule, the momentum carried) over the layer's arrays |
| `src/event_universe/shadow/run.py` | The artifacts of a run: the input, the events, the state, the record |
| `src/event_universe/core/integer.py` | Shared bounded integer primitives |
| `src/event_universe/core/lattice.py` | The board's addresses, the six Port headings and the cell bound |
| `src/event_universe/core/phase.py` | The phase circle's cosine and sine tables in bounded integers |
| `src/event_universe/runner.py` | `python -m event_universe`: a world file to headless artifacts |
| `src/event_universe/configuration_validation.py` | Read-only preflight of a world file |
| `src/event_universe/snapshot_writer.py` | `state.json` written Node by Node, byte for byte the snapshot's JSON |
| `src/event_universe/ui.py`, `ui_assets/` | Local configuration workspace, templates and isolated CLI jobs |
| `src/event_universe/retention.py`, `docs/RETENTION.md` | Registered output ownership, active writer protection and 24-hour cleanup |
| `src/event_universe/diagnostics/numeric_audit.py` | Static audit that `core/` holds integer arithmetic only |
| `tools/run_series.py` | The worlds of a series run one process per core, each with its log and artifacts, a summary table at the end |
| `tools/check.py` | The affected-check: changed files and their consumers; `--full` for everything |
| `examples/shadow/` | The worlds of the law: one content, two contents, two slits and the one-slit control |
| `tests/` | One module per generic rule on a minimal board (the mixing, the law's readings, the preflight, the decoder, retention, the repository gates) |
| `docs/HIGHLIGHTS.md` | The specification, edited by the model owner |
| `docs/ENGINE.md` | The engine's contract as implemented: the world file, the interval, the wait, the events, the books, the record, the preflight |
| `docs/DERIVATIONS.md`, `docs/EXPERIMENTS.md` | The derivations of the known laws, and the research runs with their records |
| `POSTULATES.md`, `SIMULATOR_DEFINITIONS.md` | Shared principles and scoped candidate requirements |
| `docs/ARCHITECTURE.md` | Ownership and dependency boundaries |
| `docs/PHYSICAL_FEATURES.md` | Procedure for a new physical hypothesis |
| `docs/TEST_EXPECTATIONS.md` | Independent test inputs and expected outcomes |
| `docs/MIGRATION.md` | Every deletion and rename, dated |

## Preserved rules

- Three dimensions and six causal neighbor links.
- Bounded integer payloads, arithmetic and fixed local storage.
- Explicit ownership during local waits and transit.
- Local conservation checks, with no global physical correction.
- Read-only measurements and visualization.
- Named hypotheses and independent tests; no claim that a successful run proves
  gravity, waves, energy conservation or other emergent physics.

## Standalone generic vector lab

The opt-in [vector lab](tools/generic_vector_lab/README.md) contains externally
configured N-to-M node reactions, bounded rational vector arithmetic and exact
conservation tests. It is an independent experiment, not the active simulator.
Run `python -m tools.generic_vector_lab.run_demo` from this repository.

## License and citation

Universe24 is released under the [MIT License](LICENSE), copyright Alon Gonen.
Every version is archived on Zenodo; the concept DOI
[10.5281/zenodo.22738746](https://doi.org/10.5281/zenodo.22738746) resolves
to the latest version, and each version's own DOI is listed on that record
(0.3.0: [10.5281/zenodo.22749342](https://doi.org/10.5281/zenodo.22749342);
see [CHANGELOG.md](CHANGELOG.md)).
Cite the software using [CITATION.cff](CITATION.cff); GitHub renders it as a
citation entry on the repository page. Reference form:

> Gonen, A. (2026). Universe24: a discrete simulator of local physical laws
> (Reality Theory) (Version 0.3.1) [Computer software]. Zenodo.
> https://doi.org/10.5281/zenodo.22738746
