# Project status and restart guide

Contract update: 2026-09-11. The earlier scalar-model snapshot reviewed main at
[7e517af](https://github.com/Closer24/Universe24/commit/7e517afb7a274821de05bf247ece91827c1b030b).
That commit does not identify the new generic implementation described here.
This guide is not a claim that a particular remote branch or validation run has
completed. Verify the actual checkout, current main and submitted evidence.

## What this checkout contains

The active package is [event_universe](../src/event_universe/).
`Simulation(initial: InitialState)` uses named fields, disturbance types and laws
from JSON initialization. The CLI requires `--init`; ordinary execution and tests
are headless. Start with [DISTURBANCES.md](DISTURBANCES.md) and the README.

`ScalarSimulation`, `LinkedSimulation`, `BalancedSimulation` and
`CausalStreamSimulation` retain explicit historical research laws. Their
regression tests do not make those laws the primary generic model. Check
[the public API](../src/event_universe/__init__.py) and the selected configuration,
not an old chat. Historical contracts remain scoped in
[SIMULATOR_DEFINITIONS.md](../SIMULATOR_DEFINITIONS.md).

Use the default interpreter in [.python-version](../.python-version) with the
project environment described in [README.md](../README.md#install-and-run).
The package's minimum required Python version is separately declared in
[pyproject.toml](../pyproject.toml); it does not select the runtime for a shell.

The generic delivered-face/conservative-field work, unit-link matter ownership
and Computational Field display rename are tracked in
[PR #19](https://github.com/Closer24/Universe24/pull/19).
It was closed without merge on 2026-09-11 at head
`e69a77fee97dcbb385cb2565240fafdd6b6a6179` and is not included in the reviewed main.
Its acceptance evidence and blockers belong
in that PR; do not infer that it is ready from this navigation document.

## Specifications and gaps

[Universe 24 Highlights](https://docs.google.com/document/d/1IkhSyqZZMBSgbJV-PMMwcXG0D_Rlfg4FrLy2jXBMUSs/edit)
is the user's high-level specification. Its requirements are not automatically
implemented: distinguish the active initialization-defined disturbance contract
from historical scalar/particle candidates. Read relevant current sections for specification work.
Keep accepted executable contracts in the repository and record source revision
or retrieval date in the related PR. Resolve differences explicitly; do not
overwrite the baseline to make a description appear true.

The generic schema supports bounded integer expressions, extensive splitting,
whole-record movement, paired exchange, explicit sources and local computation
delay with fixed neighbor transit. Operation prices, ordinary cost and field laws
are initialization choices. The cost output is local; propagating a computation
influence requires a separate law. Capacity exhaustion stops a run rather than
discarding content. Gravity, waves, relativity and general energy conservation
are not established by the framework.

Software validation and physical acceptance are separate. In particular, the
[isolated-motion rejection contract](../SIMULATOR_DEFINITIONS.md#reject-isolated-self-force-in-application-runs)
detects a baseline failure; a passing detector test does not fix that law.

## Resume without a conversation

1. Read [AGENTS.md](../AGENTS.md); inspect checkout status, current main and
   [open PRs](https://github.com/Closer24/Universe24/pulls).
2. Resolve the task from its [Issue](https://github.com/Closer24/Universe24/issues)
   or user request. Record the intended model, base, owned files and acceptance.
3. Install and run using [README.md](../README.md#install-and-run) and explicit
   initialization. Use a new output directory; enable visualization only when
   requested.
4. Follow [CONTRIBUTING.md](../CONTRIBUTING.md). Run the required gate and attach
   actual results for the submitted tree, including not-run checks and failures.
5. Hand off through [skills/workflow.md](../skills/workflow.md), then verify any
   authorized integration against current GitHub state.

If GitHub or Highlights cannot be read, say which information is unavailable.
Do not claim the snapshot is current. Work within verified local contracts where
the task permits; stop for clarification when a missing decision affects the law.
