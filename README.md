# Universe24 — a three-dimensional event simulator

Universe24 implements Reality Theory: one discrete world of Nodes and Links,
bounded integer arithmetic and one local rule. The GameBoard is a lattice of
Nodes; every record steps by Rule3 from its own values and its six neighbours';
a whole quantum moves at a click, and only a detector's click is a measurement.
The name of the framework is Reality Theory; the simulator that realizes it is
Universe24.

A run reads three files (a world, the universe it names and the start file),
steps the GameBoard a declared number of intervals and writes one output file:
the verdict, the detectors' clicks and the declared readings. The paper compares
the clicks with nature; nothing else a run writes is a measurement.

Canonical source: [Closer24/Universe24](https://github.com/Closer24/Universe24),
branch `main`. The Python package is `event_universe`.

**Start here:** [AGENTS.md](AGENTS.md) (the shared instructions and the language
rule), then the three documents: [the law](docs/ALGEBRA.md),
[the engine](docs/ENGINE.md) (with [its drawing](docs/ENGINE.svg)) and
[the decisions](docs/HIGHLIGHTS.md).
[Boss orchestration](skills/boss-orchestrator/SKILL.md) and
[the shared workflow](skills/workflow.md) define coordinated work.

## Install and run

Python 3.14 is the development and minimum runtime ([.python-version](.python-version)).
A run needs numpy, which the package installs:

```bash
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
PYTHONPATH=src python tools/run_inputs.py --out runs/first --jobs 1 <world>.json
```

One run writes one file, `runs/first/<world>.output.json` (the verdict, the
clicks, the readings). A run carries no time, so the same input gives the same
file again. The worlds recorded on the earlier engine left the repository with
the worlds' replay (the owner's decision); the worlds of record of the 24
experiments come under `examples/events/experiments/`, Bell first.

On Windows use `py -3.14 -m venv .venv` and `.\.venv\Scripts\python.exe` in place
of `python`. For development, install `python -m pip install -e '.[dev]'`.

Runs are headless: `--out` names the directory of the output files and `--jobs`
the processes at once, both required; a pins file (`--pins`) is compared only
under the start file's mode `pin`.
[docs/ENGINE.md](docs/ENGINE.md#4-the-loader-and-the-files) defines the files,
their keys and the refusals, and [docs/ENGINE.md](docs/ENGINE.md#6-how-to-run-a-world)
how to run a world.

## Check the project with one command

```bash
python tools/check.py
```

This runs lint, formatting, strict types and the tests of the changed files and
their consumers; `--full` runs everything. Every test is headless. Every path
a document or a skill cites in backticks exists in the tree; `tests/test_documents.py`
holds it on every pull request.

## Project map

| Path | Responsibility |
| --- | --- |
| `src/event_universe/core/` | The main loop, the step file's reader, the register, the six Ports, Rule3 and the bounded integers; only Main Loop writes here |
| `src/event_universe/features/` | One folder per primitive, found by the register from its name |
| `src/event_universe/loader/` | The three files checked against the frame's schemas and the folders' cards, and the loop's classes built from the checked values |
| `law/step.json` | The interval's order, one data file shared by every world; a change is a change of the law |
| `examples/events/` | The universe file, the start file and the worlds, with the shipped output of the first run |
| `tests/` | One module per generic rule on a minimal GameBoard, the regression of every shipped world and the repository gates |
| `tools/` | One command each: `check.py` (the affected check), `run_inputs.py` (a run), `state_digest.py` (a run's state digest, a HOST reading) |
| `docs/ALGEBRA.md` | The law |
| `docs/ENGINE.md` | The engine as the code holds it, with its drawing `docs/ENGINE.svg` |
| `docs/HIGHLIGHTS.md` | The decisions in force |
| `skills/` | The shared workflow and one short role card per skill |

## License and citation

Universe24 is released under the [MIT License](LICENSE), copyright Alon Gonen.
The software is archived on Zenodo under the concept DOI
[10.5281/zenodo.22738746](https://doi.org/10.5281/zenodo.22738746), which
resolves to the latest archived version. Cite the software using [CITATION.cff](CITATION.cff):

> Gonen, A. (2026). Universe24: a discrete simulator of local physical laws
> (Reality Theory) [Computer software]. Zenodo.
> https://doi.org/10.5281/zenodo.22738746
