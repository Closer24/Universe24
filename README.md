# Universe24 — a three-dimensional event simulator

Universe24 implements Reality Theory: one discrete world of Nodes and Links,
bounded integer arithmetic and one local rule. The GameBoard is a lattice of
Nodes; every record steps by Rule3 from its own values and its six neighbours';
a whole quantum moves at a click, and only a detector's click is a measurement.
The name of the framework is Reality Theory; the simulator that realizes it is
Universe24.

Canonical source: [Closer24/Universe24](https://github.com/Closer24/Universe24),
branch `main`. The Python package is `event_universe`.

**Start here:** [AGENTS.md](AGENTS.md) (the shared instructions and the language
rule), then the three documents: [the law](docs/ALGEBRA.md),
[the engine](docs/ENGINE.md) and [the decisions](docs/HIGHLIGHTS.md).
[Boss orchestration](skills/boss-orchestrator/SKILL.md) and
[the shared workflow](skills/workflow.md) define coordinated work.

## Install and run

Python 3.14 is the development and minimum runtime ([.python-version](.python-version)).
A run needs numpy, which the package installs:

```bash
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m event_universe --init examples/events/one_content.json --output artifacts/one_content
```

On Windows use `py -3.14 -m venv .venv` and `.\.venv\Scripts\python.exe` in place
of `python`. For development, install `python -m pip install -e '.[dev]'`.

A run reads three files (the universe file, the world file and the start file),
steps the GameBoard a declared number of intervals and writes one output;
[docs/ENGINE.md](docs/ENGINE.md#4-the-loader-and-the-files) defines the files,
their keys and the refusals, and [docs/ENGINE.md](docs/ENGINE.md#6-how-to-run-a-world)
how to run a world. Runs are headless and require a new or empty output directory.

## Check the project with one command

```bash
python tools/check.py
```

This runs lint, formatting, strict types and the tests of the changed files and
their consumers; `--full` runs everything. Every test is headless.

## Project map

| Path | Responsibility |
| --- | --- |
| `src/event_universe/core/` | The main loop, the step file's reader, the register, the Node and the bounded integers; only Main Loop writes here |
| `src/event_universe/features/` | One folder per primitive, found by the register from its name |
| `examples/events/` | The universe file and the worlds |
| `tests/` | One module per generic rule on a minimal GameBoard, the regression of every shipped world and the repository gates |
| `tools/check.py` | The affected check: changed files and their consumers; `--full` for everything |
| `docs/ALGEBRA.md` | The law |
| `docs/ENGINE.md` | The engine as the code holds it |
| `docs/HIGHLIGHTS.md` | The decisions in force |
| `skills/` | The shared workflow and one short role card per skill |

## License and citation

Universe24 is released under the [MIT License](LICENSE), copyright Alon Gonen.
Every version is archived on Zenodo; the concept DOI
[10.5281/zenodo.22738746](https://doi.org/10.5281/zenodo.22738746) resolves
to the latest version. Cite the software using [CITATION.cff](CITATION.cff):

> Gonen, A. (2026). Universe24: a discrete simulator of local physical laws
> (Reality Theory) [Computer software]. Zenodo.
> https://doi.org/10.5281/zenodo.22738746
