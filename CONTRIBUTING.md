# Contributing

Contributions are welcome: a bug found in the implementation, a derivation checked, a world built by the paper's method, a formula tested against a measurement. The way in is a fork, a branch and a pull request to `main`, which takes a pull request only, with the CI checks green and one review. The paper's text in `paper/general_formula/` is the version of record, and changes to it are the author's.

Universe24 is the implementation of the law in [docs/ALGEBRA.md](docs/ALGEBRA.md), described in [docs/ENGINE.md](docs/ENGINE.md). The engine is frozen at the commit 441b2399 and is not updated: the lines of the law entered after the freeze are not in it, and the paper's two slits' run alone is the implementation's. A contribution is read against the law.

## The ground rules

- A physics change starts from the law's line in `docs/ALGEBRA.md` and passes the three tests, generic, vector and local, before it enters; a hypothesis that needs more is stated under its own name.
- Physical calculations use bounded integers, a fixed local NodeState and the six neighbouring Nodes; nothing is kept at a Node beyond the law's own numbers, and the engine holds no number of physics: every value comes from the run's files.
- Only a NodeDetector's click is a measurement; a lattice reading is a diagnostic and is labelled so. Runs and tests are headless: inspect a run's output and its events, never a frame.
- A test exercises one generic rule alone on a minimal lattice, its expected integers written before the first run, with an edge case; no test pins the numbers of an example world.
- A change to a document replaces what it touches and deletes what no longer holds, in the same pull request; a document cites a path in backticks only where the tree holds it.
- Everything in the repository is in English, comments, docstrings, documents, test descriptions and identifiers alike; `tests/test_repository_language.py` checks it.

## The checks

Format and check the changed Python files with `python -m ruff format` and `python -m ruff check`, then run `python tools/check.py`: it selects the changed files and their consumers and runs Ruff, strict mypy, the gates and the tests they need (`--dry-run` prints the selection, `--tests` adds a dependency the selector cannot see, `--full` is the explicit complete audit). Never drop a related failing test or disable a gate.

## Pull requests

Keep a pull request small and focused, one task, with its code, its tests and its documents together; state the problem, the change, the validation and which tests were not run. Never commit secrets, installed environments, caches or run outputs (`runs/`, `artifacts/`). A model hypothesis is reported as a hypothesis, never as proof of real-world physics.
