# Universe24 — a three-dimensional event simulator

Universe24 implements **Reality Theory (Universe24)**: one discrete world of
Nodes and Links, bounded integer arithmetic and local rules. Since 2026-09-19
the model is the law of the ray ([Highlights](docs/HIGHLIGHTS.md) section
5.4, the model owner, "DECIDED: the law of the ray"; the design
[docs/RAY_LAW.md](docs/RAY_LAW.md)): the Node holds no wave; a unit is a ray
with a record moving along the digital line of its momentum at one speed for
every direction; rays that meet at a Node are permuted by the collision
table; the interval is a bijection and the click its only one-way border; a
measured event is created here without end, its clock the count of its
self-creations, and what is seen is measured events through detectors of a
declared sensitivity, whose record is the squared coherent sum of the rays
they clicked; nothing is kept at a Node, no register, no remainder, no draw.
There is one engine, the engine of that law (`rays-v1`, the one function
`nature_beam`); the engines before it, the law of events of the same day
among them, are deleted and in git ([migration](docs/MIGRATION.md)).
The name of the framework is Reality Theory; the simulator that realizes it is
Universe24.

Canonical source: [Closer24/Universe24](https://github.com/Closer24/Universe24),
branch `main`. The Python package remains `event_universe`.

**Start here:** [AGENTS.md](AGENTS.md) contains the shared instructions and
English-only repository language rule. The active implementation lives in
`src/event_universe/`; [Boss and specialist skills](skills/boss-orchestrator/SKILL.md)
define coordinated work and independent checks.

A run is a **world file**: a JSON object with `"law": "rays"`, the GameBoard's
shape and boundary, the clock K and the phase width N, the release rate and
the suspension, the declared directions, the families (free, matter; paid,
light), the measured events at the start with their tables and directions
and, where wanted, the detectors. The engine recognizes nothing by physical
name. Read [the law of the ray](docs/RAY_LAW.md), [the engine](docs/ENGINE.md)
and the worlds under [examples/events/](examples/events/README.md) before
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
python -m event_universe --init examples/events/one_content.json --output artifacts/one_content
```

On Windows:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m event_universe --init examples/events/one_content.json --output artifacts/one_content
```

Select the environment's interpreter explicitly if activation is unavailable.
For development, install `python -m pip install -e '.[render,dev]'`.

Check a world file without running it:

```bash
python -m event_universe.configuration_validation examples/events/one_content.json --json
```

The world file is required. It supplies `ticks`; `--ticks` can override the
duration. Missing input is an error, not a request to load a built-in universe.
The GameBoard is open (`"boundary": "open"`): what leaves is booked as escaped, with
the momentum it carried; a closed GameBoard is refused. An axis may be declared
periodic (`"boundary": {"z": "periodic"}`): its departures wrap to the opposite
face and nothing escapes on that axis. Run several worlds one
process per core with `tools/run_series.py`.

| Output | When written |
| --- | --- |
| `initialization.json` | Exact input file copied for reproducibility |
| `run.json` | The record: the law, the world's keys, the books per family at every tick, the measured events, the detectors, completion and elapsed time |
| `state.json` | The measured events, the detectors and every Node with events in transit, written Node by Node |
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
`examples/events/` as a template, edit its JSON, **Check** it, and **Run**.
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
| `src/event_universe/events/world.py` | The world file: its keys, their bounds and the refusals, named |
| `src/event_universe/events/nature_beam.py` | The law of the ray (`rays-v1`): the record `NatureBeam`, the one reading `read_arrivals`, the flight table, the collision table, the store of records per family and the one function `nature_beam`, a Node's whole interval (the walk, the reading, the collision, the measured event's table, the detector's record, the self-creations, the merge) |
| `src/event_universe/events/measured.py` | The measured event's record (`Measured`) and the ledger of an interval |
| `src/event_universe/events/engine.py` | The frame around the law: the clocks, the owed count off the clock, the steps by the momentum, the books, the readings, the inverse interval, the snapshot; it computes no physics |
| `src/event_universe/events/run.py` | The artifacts of a run: the input, the events, the state, the record |
| `src/event_universe/core/integer.py` | Shared bounded integer primitives |
| `src/event_universe/core/game_board.py` | The GameBoard's addresses, the six Port headings and the bound of a declared charge and quantum |
| `src/event_universe/core/phase.py` | The phase circle's cosine and sine tables in bounded integers |
| `src/event_universe/runner.py` | `python -m event_universe`: a world file to headless artifacts |
| `src/event_universe/configuration_validation.py` | Read-only preflight of a world file |
| `src/event_universe/snapshot_writer.py` | `state.json` written Node by Node, byte for byte the snapshot's JSON |
| `src/event_universe/ui.py`, `ui_assets/` | Local configuration workspace, templates and isolated CLI jobs |
| `src/event_universe/retention.py`, `docs/RETENTION.md` | Registered output ownership, active writer protection and 24-hour cleanup |
| `src/event_universe/diagnostics/numeric_audit.py` | Static audit that `core/` holds integer arithmetic only |
| `tools/run_series.py` | The worlds of a series run one process per core, each with its log and artifacts, a summary table at the end |
| `tools/migrate_nature_beam_worlds.py` | A NatureBeam world rewritten to the form of 2026-09-19: `quantum` in place of `kind`, only the table entries that differ from the default |
| `tools/check.py` | The affected-check: changed files and their consumers; `--full` for everything |
| `examples/events/` | The worlds of the law of the ray: one content, two contents, two slits with a detector and the one-slit control; the Bell worlds, the coupling, orbit, redshift and Hubble series and the detector definitions |
| `tests/` | One module per generic rule on a minimal GameBoard (the one reading, the flight, the collision table, the bijection, the detector's record, the re-emission, the clock, the phase window, the world file, the worlds, the preflight, the decoder, retention, the repository gates) |
| `docs/HIGHLIGHTS.md` | The specification, edited by the model owner |
| `docs/RAY_LAW.md` | The law of the ray: the design, the implementation contract and the implementation notes |
| `docs/ENGINE.md` | The bookkeeping around the law as implemented: the GameBoard, the frame of an interval, the books, the world file's refusals, the record, the preflight |
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
