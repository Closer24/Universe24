# Project status and restart guide

Integration reference: 2026-09-12. [PR #27](https://github.com/Closer24/Universe24/pull/27)
combines reviewed spatial-field feature head
`137830fd621b9522598e0719e7bd2055ead595a9` with main
`15029ba8d02bd7f1bb1dd1148fe55405ec1536b1`, which adds atomic generic interactions
and the configured unequal-mass elastic example through PR #28. Spatial fields,
finite budgets, boundaries, output retention and arbitrary-name handling remain
included. GitHub-supplied blob, tree and commit hashes were verified before local
integration. Verify live checkout, remote and PR state before continuing; this
reference is not a claim about the version in another checkout. Identified checks
and run evidence belong in [VALIDATION.md](VALIDATION.md).

Registered run outputs,
workspace copies/logs/exports and test reports expire after 24 hours, with live
writer protection; see [RETENTION.md](RETENTION.md). Idle cleanup requires the
watcher or a scheduled invocation. Generated evidence paths in older validation
records are temporary, while their recorded conclusions remain in the repository.

## What this checkout contains

The active package is [event_universe](../src/event_universe/).
`Simulation(initial: InitialState)` uses named fields, disturbance types and laws
from JSON initialization. The CLI requires `--init`; ordinary execution and tests
are headless. Start with [DISTURBANCES.md](DISTURBANCES.md) and the README.

The [local configuration workspace](WORKSPACE.md) provides template selection,
editable JSON and isolated runs through `python -m event_universe.ui`.
Configuration changes are runtime data and require no compilation or rebuild.
The workspace includes recorded movie playback, folded settings, names and three
idealized motion presets, plus a configured unequal-mass elastic collision.
The latter uses atomic generic interactions with explicit invariants; see
[the candidate contract](DISTURBANCES.md#configured-unequal-mass-elastic-example).
These transport demonstrations do not establish the
behavior of real electrons, protons, photons or electromagnetic interactions.

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
delay with fixed neighbor transit. Atomic pair transactions also support multiple
assignments, vector transforms and declared pre/post invariants. Operation prices, ordinary cost and field laws
are initialization choices. The cost output is local; propagating a computation
influence requires a separate law. Capacity exhaustion stops a run rather than
discarding content. Gravity, waves, relativity and general energy conservation
are not established by the framework.

The optional [spatial-field extension](SPATIAL_FIELDS.md) adds independent
outward emission, baselines and combined balance diagnostics. Its fixed
field clock is separate from carrier computation delay. The new example selects
that candidate explicitly; configurations without it preserve their old laws.
[Spatial couplings](SPATIAL_COUPLINGS.md) add configured exchange and exact
discrete rotation with an atomic opposite field reaction. The scalar-flux-driven
rotation has a restricted straight cardinal isolation property. General automatic
self attribution remains unsupported, particularly after turns or periodic
return.

The local schema 2 candidate `finite-dissipative-v1` requires completed-link
integer decay at interior receivers for every spatial field and finite per-record budgets for emitted
amounts and coupling reactions. [finite_fields.json](../examples/finite_fields.json)
is the small headless example. Baselines are exempt; dynamic populations vanish
after their last nonzero input. This candidate explicitly records loss and does
not conserve physical momentum or energy through decay. Schema 1 preserves its
conservative transport and unlimited declared sources and responses. Candidate
identity is selected by schema version, independently of field and model names.
Verify current validation evidence and the running source version before reusing
results. No Highlights update is implied by repository edits.

Both schemas support `boundary: "periodic"` (the default) or `boundary: "open"`.
Periodic particles and fields wrap across every X, Y and Z face without changing
direction or link time. Open terminal packets leave after full transit and their
unchanged signed amounts enter an escaped ledger; no exterior cell is simulated.
See [the boundary contract](DISTURBANCES.md#domain-boundary) and
[open_world.json](../examples/open_world.json). A host scheduling index skips
dormant spatial cells while preserving local costs and physical updates. The
runner records elapsed host seconds separately from simulation ticks.

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
