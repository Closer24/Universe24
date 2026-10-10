# Contributing

Contributions are welcome: a bug found in the implementation, a derivation checked, a world built by the paper's method, a formula tested against a measurement. The way in is a fork, a branch and a pull request to `main`, which takes a pull request only, with the CI checks green and one review. The papers' text in `papers/` (the first paper in `papers/one_rule/`, the time paper in `papers/spacetime_events/`) is the version of record, and changes to it are the author's.

Universe24 is the implementation of the law in [docs/ALGEBRA.md](docs/ALGEBRA.md), described in [docs/ENGINE.md](docs/ENGINE.md). The engine the paper reports is the tag v1.1.0 (the commit 441b2399's engine plus the version line), run from the tag: the lines of the law entered after the freeze are not in it, and the paper's two slits' run alone is the implementation's. main carries the engine V2 ([docs/ENGINE.md](docs/ENGINE.md); what changed from the tag in [CHANGELOG.md](CHANGELOG.md)); a change of the engine enters only as the implementation of a law line of [docs/ALGEBRA.md](docs/ALGEBRA.md), with the three tests (generic, vector, local), by pull request. A contribution is read against the law.

## The ground rules

- A physics change starts from the law's line in `docs/ALGEBRA.md` and passes the three tests, generic, vector and local, before it enters; a hypothesis that needs more is stated under its own name.
- Physical calculations use bounded integers, a fixed local NodeState and the six neighbouring Nodes; nothing is kept at a Node beyond the law's own numbers, and the engine holds no number of physics: every value comes from the run's files.
- Only a NodeDetector's click is a measurement; a lattice reading is a diagnostic and is labelled so. Runs and tests are headless: inspect a run's output and its events, never a frame.
- A test exercises one generic rule alone on a minimal lattice, its expected integers written before the first run, with an edge case; no test pins the numbers of an example world.
- A change to a document replaces what it touches and deletes what no longer holds, in the same pull request; a document cites a path in backticks only where the tree holds it.
- Everything in the repository is in English, comments, docstrings, documents, test descriptions and identifiers alike; `tests/test_repository_language.py` checks it.

The gates are the rule for the engine: integers only; every division in `src/event_universe` is listed in the acts table (`tests/test_the_acts_table.py`) with its kind, R a carried division on levels with the remainder kept, D a coefficient's division once with the remainder discarded, S a search by comparing integer products, and a new division anywhere fails the table until it is listed; no root anywhere (`tests/test_the_gates.py`: no `isqrt`, no `sqrt`, no float power; the one search is `core/rule3.largest_below`); no shear, no rotation act and no trigonometric call (`tests/test_rule3.py`: `cos`, `sin`, `tan`, `atan`, `atan2`, `exp`, `log` and the hyperbolics are forbidden tokens, and `rotation` stands only as a family's declared key in the loader). A change that needs any of these is not an engine change; it is a line of the law first.

## The checks

With Python 3.14 or later, which `pyproject.toml` requires, format and check the changed Python files with `python -m ruff format` and `python -m ruff check`, then run `python tools/check.py`: it selects the changed files and their consumers and runs Ruff, strict mypy, the gates and the tests they need (`--dry-run` prints the selection, `--tests` adds a dependency the selector cannot see, `--full` is the explicit complete audit). Never drop a related failing test or disable a gate.

## Pull requests

Keep a pull request small and focused, one task, with its code, its tests and its documents together; state the problem, the change, the validation and which tests were not run. Never commit secrets, installed environments, caches or run outputs (`runs/`, `artifacts/`). A model hypothesis is reported as a hypothesis, never as proof of real-world physics.
