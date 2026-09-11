# Working on this simulator

Start with [AGENTS.md](AGENTS.md), the shared entry point for all contributors.
The canonical repository is https://github.com/Closer24/Universe24. Branch from
current origin/main; use isolated worktrees for concurrent tasks and submit a PR.

1. Read `POSTULATES.md` and `SIMULATOR_DEFINITIONS.md` before changing a
   physical module. A postulate change must update both documents and its tests.
2. Keep scheduling, generic field/dynamics calculations, model choices and output
   code in their documented modules. Reuse the generic arithmetic; choose and
   connect it in `models/current_field.py` rather than copying it into a model.
3. Use named immutable physical records, typed public interfaces and short local
   functions. Do not add growing per-source structures or render imports to core.
4. For a defect, add a focused test of the failed behavior before the correction.
   Tests should assert a contract or observed result, not mirror implementation.
5. For refactors, retain exact differential equivalence to the frozen baseline.
   A change to a physical hypothesis needs a separate model identity and review;
   do not change baseline expectations merely to make a test pass.
6. Run `python tools/check.py`. Inspect the HTML for affected run scenarios.
   Test reusable calculations in `test_scalar_field.py` and `test_turning.py`,
   current choices in `test_current_field.py`, and public component replacement
   in `test_field_composition.py`.
   Specify input, expected output and a boundary case for each calculation;
   maintain `docs/TEST_EXPECTATIONS.md`. Movement, lattice geometry, field
   policies and diagnostic projections have their own focused test modules.
   Assembly modules must contain no independent arithmetic; the architecture
   gate also checks absolute and relative dependencies.
7. Commit code and documentation together. Keep generated outputs outside source
   commits; attach them to reviews or saved experiment packages.

Formatting is managed by Ruff. The development dependencies are declared in
`pyproject.toml`; exact tool versions used for the delivered validation are
recorded in `docs/VALIDATION.md`. No coverage percentage substitutes for tests of
integer bounds, causality, occupancy, momentum and known historical regressions.

Write all comments, docstrings and repository documentation in English under
the repository language rule in AGENTS.md. Run the language gate along with
the architecture tests. Translate prose from older branches before integration.

## Shared repository and Git workflow

The canonical development source is https://github.com/Closer24/Universe24,
branch `main`. ZIP files are backups after the project has been uploaded. For each task:

1. Read these instructions and relevant documents from the current repository.
2. Check `git status`, fetch `origin`, and record the base commit. Never overwrite
   local work belonging to the user or another conversation.
3. Create a short-lived branch from `origin/main`, such as `fix/field-bounds` or
   `feat/volume-controls`. Use a separate worktree or clone for concurrent work.
4. Keep the task focused and commits small, explaining why each change is needed.
   Do not mix physical changes with display changes or architecture cleanup.
5. Before pushing, inspect `git diff --check`, the diff and changed-file list.
   Never commit secrets, installed environments, caches or generated outputs.
6. Run `python tools/check.py` on the version being submitted. Show the HTML for
   world runs. CI outputs are available as GitHub Actions artifacts.
7. Open a pull request to `main` explaining the problem, change, expected behavior,
   validation, limitations and compatibility impact. State which tests were not run.
8. If `main` advances, integrate its changes and recheck the resulting risks.
   Merge only after successful CI and within the user's authorization; never bypass
   a failing check.

Do not push directly to `main` during routine work or force-push a shared branch.
An initial upload to an empty repository is allowed when the user requests it.
These workflow rules are not technical branch protection; do not claim server-side
protection exists without verifying it.


## Code and test quality

- Give each component one responsibility, clear names and a small typed interface.
  Prefer composition and short functions over deep inheritance or unnecessary
  plugin registries. Introduce abstractions when there is a clear shared contract.
- Write each generic calculation once. Keep model parameters and choices in the
  model. Never add scenario-name conditions to a general law.
- Validate inputs at component boundaries and represent failure explicitly. Never
  swallow exceptions, repair momentum globally or change expectations to hide failure.
- Unit tests use independent numerical examples, boundaries and errors. Integration
  tests check replacement and composition; regressions compare established behavior.
  Simple documentation edits need link and packaging checks, not artificial tests.
- Dependency changes require a concrete need and installation validation. Preserve
  Ruff, strict mypy, integer audits and layer checks; never disable a quality gate.
- Report the change, PR or commit, validation and remaining work. Never present a
  model hypothesis as proof of real-world physics.

## Multiple conversations

Every conversation starts from the current repository and works on its own branch.
Conversations do not synchronize automatically, and AGENTS.md cannot update an old
checkout already in use. Never import an old ZIP into `main`; integrate a focused
change against its recorded base. Before merging older branches, translate their
remaining prose and preserve the repository language gate.
