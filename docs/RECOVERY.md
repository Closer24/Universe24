# Recovery without chat history

Git is the durable source for simulator code, JSON examples, repository skills,
tests and GitHub workflow definitions. Start with [AGENTS.md](../AGENTS.md) and
[project status](PROJECT_STATUS.md), then verify current main and open PRs.
Clone the canonical repository and follow [installation](../README.md#install-and-run)
using the Python version in `.python-version`. Dependencies and entry points are
declared in `pyproject.toml`; an installed virtual environment is not backed up.

Run the known-entity environment using the
existing interpreter after setup. Configuration edits do not require compilation.
Use `python tools/check.py` for changed code and its affected consumers.

## Genericity audit

The authoritative daily audit and scheduling restoration procedure lives in
[the regression-check skill](../skills/regression-check/SKILL.md#daily-genericity-audit).
It covers both the generic simulator and its result consumers, including headless
JavaScript checks. Read that skill rather than recovering instructions from chat.
No dedicated daily GitHub Actions job is added for this audit.

## Local retention and optional chat automation

Follow [retention](RETENTION.md) to restore local cleanup. Run the existing module
with `--watch` and explicit `--root` paths for each checkout's generated artifacts
and the workspace runs directory. Do not enroll source or original configurations.
Start the watcher after login or through the operating system scheduler if idle
cleanup is needed. GitHub Actions does not clean a user's local disk.

Chat-bound automations and their running processes are not Git objects and are
not recreated by cloning. The optional chat audit should run once daily after
09:00 Asia/Jerusalem, inspect current main and the genericity scope above, and
report concrete findings with paths, reproduction, commit/tree and test counts.
It can share an hourly retention heartbeat using a last-audit date to prevent
duplicate daily runs. Restore the authorized automation using the skill; cloning the repository alone
does not schedule it. Avoid duplicate local retention watchers.

Git cannot restore account credentials, service connections, machine permissions,
uncommitted work or expired generated results. Reauthorize services separately;
never commit credentials. Recreate results from the versioned JSON inputs.
