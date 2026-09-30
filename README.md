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
[the engine](docs/ENGINE.md) and
[the decisions](docs/HIGHLIGHTS.md).
[The shared workflow](skills/workflow.md), [the Boss's card](skills/boss-orchestrator/SKILL.md)
and [the advisor's card](skills/advisor/SKILL.md) define the team's work.

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
clicks and the books). A run carries no time, so the
same input gives the same file again. A world's bodies are laid first by
`tools/pixel_mode.py`, which writes the mode file beside it.

On Windows use `py -3.14 -m venv .venv` and `.\.venv\Scripts\python.exe` in place
of `python`. For development, install `python -m pip install -e '.[dev]'`.

Runs are headless: `--out` names the directory of the output files and `--jobs`
the processes at once.
[docs/ENGINE.md](docs/ENGINE.md#4-the-loader-and-the-files) defines the files,
their keys and the refusals, and [docs/ENGINE.md](docs/ENGINE.md#6-how-to-run-a-world)
how to run a world.

## Check the project with one command

```bash
python tools/check.py
```

This runs lint, formatting, strict types and the tests of the changed files and
their consumers; `--full` runs everything. Every test is headless.

## Project map

| Path | Responsibility |
| --- | --- |
| `src/event_universe/node.py` | The Node: every family's NodeState and the interval's acts, each a call of Rule3 |
| `src/event_universe/game_board.py` | The GameBoard: the NodeStates, the bodies' ledgers, the detectors, the interval forward and back, the output lines and the books |
| `src/event_universe/core/` | Rule3, the six Ports and the working bound; changed only by the Boss's worker on a brief that names the law's line |
| `src/event_universe/features/` | The count's line, the hold, the write, the signed read and the start, each a pure function of arrays |
| `src/event_universe/loader/` | The world's files checked into the GameBoard's world, and the families from the rule |
| `examples/events/` | The universe files, the engine start file and the two slits' worlds with their blind expectation |
| `tests/` | One module per generic rule on a minimal GameBoard and the repository gates |
| `tools/` | One command each: `check.py` (the affected check), `run_inputs.py` (a run), `pixel_mode.py` (the generator's lay of the bodies and the messages), `back_in_time.py` (the back-in-time gate), `click_counts.py` (a detector's rises against its blind expectation) |
| `docs/ALGEBRA.md` | The law |
| `docs/ENGINE.md` | The engine as the code holds it |
| `docs/HIGHLIGHTS.md` | The decisions in force |
| `skills/` | The shared workflow, the Boss's card and the advisor's card |

## License and citation

Universe24 is released under the [MIT License](LICENSE), copyright Alon Gonen.
The software is archived on Zenodo under the concept DOI
[10.5281/zenodo.22738746](https://doi.org/10.5281/zenodo.22738746), which
resolves to the latest archived version. Cite the software using [CITATION.cff](CITATION.cff):

> Gonen, A. (2026). Universe24: a discrete simulator of local physical laws
> (Reality Theory) [Computer software]. Zenodo.
> https://doi.org/10.5281/zenodo.22738746
