# Universe24 — a three-dimensional event simulator

Universe24 implements **Reality Theory (Universe24)**: one discrete world of
Nodes and Links, bounded integer arithmetic and local rules. Since 2026-09-19
the model is the Beam Law ([Highlights](docs/HIGHLIGHTS.md) section
5.4, the model owner, "DECIDED: the law of the ray"; the design
[docs/BEAM_LAW.md](docs/BEAM_LAW.md)): the Node holds no wave; a unit is a row
(the record of an event in transit, `NatureBeam` in the code; the system has
rows and bodies, the model owner, 2026-09-21; [the glossary](docs/TERMINOLOGY.md))
moving along the digital line of its momentum at one speed for
every direction; rows that meet at a Node are permuted by the collision
table; the interval is a bijection and the click its only one-way border; a
measured event is created here without end, its clock the count of its
self-creations, and what is seen is measured events through detectors of a
declared sensitivity, whose record is the squared pointer of the rows
they clicked; nothing is kept at a Node, no register, no remainder, no draw.
There is one engine, the engine of that law (`beam-v1`, the one function
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

A run is a **world file**: a JSON object with `"law": "beam"`, the GameBoard's
shape and boundary, the clock K and the phase width N, the release rate and
the suspension, the declared directions, the families (free, matter; paid,
light), the measured events at the start with their tables and directions
and, where wanted, the detectors. The engine recognizes nothing by physical
name. Read [the Beam Law](docs/BEAM_LAW.md), [the engine](docs/ENGINE.md)
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
process per core with `tools/run_inputs.py`.

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
| `src/event_universe/core/integer.py` | Shared bounded integer primitives |
| `src/event_universe/core/game_board.py` | The GameBoard's addresses, the six Port headings, the cube's group of 48 with its hand, and the bound of a declared charge and quantum |
| `src/event_universe/core/phase.py` | The phase circle, the cyclic group of N steps with its unit vectors, and its cosine and sine tables in bounded integers |
| `src/event_universe/retention.py`, `docs/RETENTION.md` | Registered output ownership, active writer protection and 24-hour cleanup |
| `src/event_universe/diagnostics/numeric_audit.py` | The two static audits: `core/` holds integer arithmetic only, `events/` integer numpy and nothing that leaves the integers |
| `tools/check.py` | The affected-check: changed files and their consumers; `--full` for everything |
| `tools/record_shipped_worlds.py`, `tests/shipped_worlds.json`, `tests/test_shipped_worlds.py` | Every shipped world bit for bit (record 2214 point 7; issue #1155): the recorder writes one SHA-256 digest of the engine's whole state per world after a recorded number of intervals; the test replays them and is selected by `tools/check.py` on every pull request |
| `tests/test_genericity.py` | The genericity test (the Boss's record 2234): a seeded generator draws one to twenty families with random English names and random admitted attribute combinations; every draw loads and runs, and five properties hold on each (rename bit for bit, reorder bit for bit, no source stays zero, Rule3's conserved form where no click and no load acts, backward returns the start); a failing draw is kept with its seed; selected by `tools/check.py` on every pull request |
| `tools/record_code_shape.py`, `tests/code_shape_baseline.json`, `tests/test_code_shape.py` | The ratchet on the shape of the code (records 2239 and 2241): per file of `src/` the lines, docstring lines, comment lines, record references, Rule3 arithmetic sites and level-shift sites ratchet for a file beyond the limits (a docstring beyond one line, a record reference, 400 lines, a site), never above the merge base's baseline either, and a file within them passes; no two functions share one abstracted body beyond the baseline; a feature imports `core/` alone, `core/` imports nothing outside itself, nothing outside `core/` imports the loop's internals; selected by `tools/check.py` on every pull request |
| `tools/engine_gates.py`, `tests/engine_gates_baseline.json`, `tests/test_engine_gates.py` | The reviewer's recurring findings as gates (issue #1198, item 4 (a)): per file of `src/` no new numeric literal beyond 0, 1, 2, 3, 4, 6 and 8 and no new family name as a string, ratcheted against the merge base; a new module of `core/` needs an `APPROVED-CORE` line in the pull request's body; selected by `tools/check.py` on every pull request |
| `tools/preflight_worlds.py` | The pre-GO check of the world files: every world a run list names (`docs/designs/detector_law/RUN_LIST.md` by default) is resolved, loaded by the runner's own loader, its margin rule read and its engine constructed, no interval stepped; one line per world, LOADED, REFUSED or MISSING; nothing here runs a rule |
| `examples/events/` | The worlds of the Beam Law: one content, two contents, two slits with a detector and the one-slit control; the Bell worlds, the coupling, orbit, redshift and Hubble series and the detector definitions |
| `tests/` | One module per generic rule on a minimal GameBoard (the one reading, the flight, the collision table, the bijection, the detector's record, the re-emission, the clock, the phase window, the world file, the worlds, the preflight, the decoder, retention, the repository gates) |
| `docs/HIGHLIGHTS.md` | The specification, edited by the model owner |
| `docs/BEAM_LAW.md` | The Beam Law: the design, the implementation contract and the implementation notes |
| `docs/ENGINE.md` | The engine as the code holds it on main: the main loop and its five places, Rule3, the folders and the register, the loader and the files, the output, the gates, how to run a world and how to add a feature |
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
