# Instructions for every project contributor

These instructions apply to the entire project and every subdirectory. This is
the entry point for coding agents and developers. Read the current files rather
than relying on memory from another conversation.

## One project and one source of truth

The only active implementation is `src/event_universe/` in this project.
`src/persistent_source_field.py` is a compatibility facade only.
`tests/reference/` is a frozen comparison source; never edit it to make a test pass.
`artifacts/`, distributions, patches and backups are outputs or history, not
alternative development sources. Models v10 and v11 are explicit models in the
same package.

## Repository language: English

All repository comments, docstrings, documentation, contributor instructions,
test descriptions, diagnostic messages and newly written identifiers must be in
English. This applies to every directory and every contributor, including files
brought in from an older branch. Keep English simple and precise. Mathematical
symbols and established technical names are allowed. This is a documentation and
architecture rule; it does not change physical laws or the language of conversation
with the user. The user's explicit request replaces the previous Hebrew-documentation
preference.

Before submitting a change, translate any non-English prose it introduces and run
`tests/test_repository_language.py`. The script check catches the legacy Hebrew
text and several other non-Latin scripts; it does not prove that Latin-script prose
is English. Reviewers must check the language as well. Do not exempt a directory,
disable the gate, or encode non-English prose as escapes to evade this rule.

## What to read before making changes

| File | Authoritative responsibility |
| --- | --- |
| [POSTULATES.md](POSTULATES.md) | Principles in plain language |
| [SIMULATOR_DEFINITIONS.md](SIMULATOR_DEFINITIONS.md) | Exact contracts, model exceptions and display defaults |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Layer boundaries and dependency direction |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Change and validation workflow |
| [docs/TEST_EXPECTATIONS.md](docs/TEST_EXPECTATIONS.md) | Test inputs and expected outcomes |

Do not duplicate all rules across parallel documents. Update the responsible
document and its references and tests. Explicit user instructions take precedence;
document authorized changes. An unresolved contradiction does not authorize a
silent change to a physical law.

## Change boundaries

- Physical calculations use bounded integers, fixed local state and six neighbors.
  Measure host computation and storage separately from the model's local cost.
- Field, response, movement and transit calculations belong in generic components.
  Models select policies and compose components without copying formulas. The engine
  schedules work and validates contracts.
- Displays and measurements only read state. Every world run produces HTML through
  the existing renderer, with enhanced 3D as the default, including test runs, as
  specified in the definitions document.
- A behavior change needs a dedicated test with inputs, an expected result and an
  edge case. Preserve the frozen v10 comparison. A new physical hypothesis needs
  an explicit model identity.
- Run `python tools/check.py` and inspect the HTML report before delivery. Static
  checks are partial enforcement, not proof of locality or correct physics.

## Adding a physical feature

Follow the [physical feature procedure](docs/PHYSICAL_FEATURES.md) before coding.
Define the law, local inputs, evolving state, fixed parameters and outputs
separately. Generic calculations must not receive a world or an entire Config;
the adapter passes only the required values. The procedure also requires
independent tests and explicit extension limits.

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
