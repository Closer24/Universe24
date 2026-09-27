# Working on this simulator

Start with [AGENTS.md](AGENTS.md). The canonical repository is
https://github.com/Closer24/Universe24, branch `main`. The law is
[docs/ALGEBRA.md](docs/ALGEBRA.md), the engine [docs/ENGINE.md](docs/ENGINE.md),
the decisions [docs/HIGHLIGHTS.md](docs/HIGHLIGHTS.md); the procedure in full is
the short procedure of [the shared workflow](skills/workflow.md).

## The procedure

1. `main` is the one version that works; no one pushes to it directly and no one
   force-pushes a shared branch. Every task is one short branch from `origin/main`
   (`feature/...`, `core/...`, `exp/...`), merged within days and deleted after the
   merge. Check `git status`, fetch `origin` and record the base commit; never
   overwrite local work of the user or another conversation; use a separate
   worktree for concurrent work.
2. Only Main Loop touches `src/event_universe/core/`. A new primitive is one folder
   under `src/event_universe/features/`, acting only when the run's files declare
   it, approved by the mathematician with `APPROVED-MATH` on its pull request; with
   it undeclared, every old run comes out identical to the bit. A new module of
   `core/` needs `APPROVED-CORE` in the pull request's body.
3. A physics change starts from the law's line in `docs/ALGEBRA.md`; a bug (the
   code differs from the law) is fixed by whoever finds it with a test that fails
   before and passes after; a change to the step file is a change of the law and
   needs the owner's decision.
4. Keep the task focused and the commits small; commit code, tests and documents
   together; never commit secrets, installed environments, caches or generated
   outputs. Before pushing, inspect `git diff --check` and the changed-file list.
5. Format and check: `python -m ruff format` and `python -m ruff check` on the
   changed Python files, then `python tools/check.py`, which selects the changed
   files and their consumers (`--base REVISION` for another base, `--dry-run` to
   print the selection, `--tests` to add a dependency the selector cannot see,
   `--full` only for an explicitly justified complete audit). Never drop a related
   failing test or disable a gate (Ruff, strict mypy, the integer audits, the layer
   checks, the language gate, the document gates, the ratchets on the code's shape).
6. Open a pull request to `main` stating the problem, the change, the validation,
   the lines it adds and deletes in `src/` and `tests/`, what it deleted from the
   documents, and which tests were not run. If `main` advances, merge it in (a merge
   commit, never a rebase) and recheck.
7. Only the Boss merges into `main`, only on green CI and with `main` merged in;
   never bypass a failing check. The Boss's reviewer reads a change to the law, a
   physics folder or `core/`; everything else merges on green CI. Every result names
   the `main` commit it ran on; there are no tags.

## Tests and documents

- A test exercises one generic rule alone on a minimal GameBoard, its expected
  integers written before the first run, with an edge case; no test pins the
  numbers of an example world. `tests/` may not grow, only shrink, until it is below
  `src/`. Shared test builders live in focused helper modules under `tests/`.
- Runs and tests are headless; inspect a run's output and events, never a frame.
- A change to a document replaces what it touches and deletes what no longer holds
  in the same pull request; no history note or record number stays. A decision of
  the model owner is one line in `docs/HIGHLIGHTS.md`, replacing the line it
  changes; a finding or approval of one pull request is a comment on it; a list
  across pull requests is one issue with a checklist.
- Write all comments, docstrings and documents in English under the rule in
  [AGENTS.md](AGENTS.md#repository-language-english); translate prose from older
  branches before integration.
- Report the change, the pull request or commit, the validation and the remaining
  work. Never present a model hypothesis as proof of real-world physics.
