# Project status and restart guide

Audit reference: 2026-09-12, main `fb083c159fe1f51612203962d9a7921683eb31c8`.
The names below include the repository-consistency cleanup based on that revision.
Verify the current checkout, main and open PRs before continuing. A dated source
map does not certify another checkout or turn an unmerged branch into implemented work.
Use the [documentation index](README.md) for each subject's authoritative owner.

## What this checkout contains

| Scope | Implemented owner | Contract and limits |
| --- | --- | --- |
| Active generic simulator | [disturbance_api.py](../src/event_universe/disturbance_api.py), [disturbance_engine.py](../src/event_universe/core/disturbance_engine.py) | `Simulation(InitialState)`; laws and fields come from explicit initialization, not physical names |
| Local expressions and transactions | [disturbances.py](../src/event_universe/fields/disturbances.py) | Bounded integer operations, declared balances, fixed local capacities and explicit rejection |
| Spatial fields | [spatial_engine.py](../src/event_universe/core/spatial_engine.py) | Fixed neighbor transit, baselines, schema 1 transport and opt-in schema 2 finite budgets/decay |
| Local field read/response rules | [local_field_rules.py](../src/event_universe/fields/local_field_rules.py) | Six-port reads and guarded local field/carrier proposals; no implied Maxwell law |
| Entity representation | [entities.py](../src/event_universe/entities.py), [catalog.json](../examples/known-entities/catalog.json) | 46 inventory profiles compile to selected initialization records; labels are not physical derivations |
| Quantum event backend | [event_network.py](../src/event_universe/quantum/event_network.py) | Deferred joint-state evaluation and explicit instruments under the quantum owner |
| Native event programs | [event_runtime.py](../src/event_universe/integration/event_runtime.py), [event_space.py](../src/event_universe/core/event_space.py) | Optional shared causal identities, repeated local triggers and charged executed paths; rejects spatial fields |
| Historical contact experiment | [quantum_contact_trial.py](../src/event_universe/integration/quantum_contact_trial.py) | One bounded eight-tick contact trial selects a real local mechanical proposal; not a general dispatcher |
| Historical particle APIs | [particle_api.py](../src/event_universe/particle_api.py) | Explicit `ScalarSimulation`, `LinkedSimulation`, `BalancedSimulation`, `CausalStreamSimulation` |
| Application and output | [runner.py](../src/event_universe/runner.py), [ui.py](../src/event_universe/ui.py) | Headless runs by default; optional read-only recording and workspace playback |

The active package lives only in `src/event_universe/`. The
[persistent-source facade](../src/persistent_source_field.py) re-exports historical
notebook names; it contains no second engine. `tests/reference/` preserves source
history, not an active implementation or a compatibility acceptance gate.

The historical scalar scheduler is `core/scalar_engine.py` (`ScalarEngine`), and
its selected scalar policy is `models/scalar_field.py` (`ScalarFieldModel`).
The active `Simulation` still resolves to `disturbance_api.py`. See
[migration](MIGRATION.md#explicit-historical-component-names) for renamed internal
imports and commands. Public named simulation classes keep their identities.

The unequal-mass collision configuration has one canonical file:
[04-unequal-mass-collision.json](../examples/04-unequal-mass-collision.json).
Both the workspace and [reference checks](../examples/known-entities/run_reference_checks.py)
consume it. The reference runner does not maintain a second copy of the law.
Its three-mass case likewise uses [three_mass_finite.json](../examples/three_mass_finite.json)
with a 120-tick override instead of a duration-only copy of the initialization.

## Specifications and gaps

[Universe 24 Highlights](https://docs.google.com/document/d/1IkhSyqZZMBSgbJV-PMMwcXG0D_Rlfg4FrLy2jXBMUSs/edit)
is the high-level specification, not automatic evidence of implementation.
Repository cleanup does not modify that external document. Read its current
revision when working on specification changes and reconcile differences explicitly.

The active [disturbance contract](DISTURBANCES.md) supports named scalar/vector
fields, whole-record movement, extensive splitting, atomic interactions, explicit
sources and computation-dependent local waits. Physical work/storage per fixed
local configuration is distinct from total host scheduling and history costs.
Capacity exhaustion rejects a run rather than silently losing state.

[Spatial fields](SPATIAL_FIELDS.md) and [couplings](SPATIAL_COUPLINGS.md) retain
candidate-specific behavior. Schema 2 (`finite-dissipative-v1`) records completed-link
loss and finite source/response allowances; accounting for decay is not physical
energy or momentum conservation through decay. Periodic and open boundaries have
separate explicit contracts. General automatic self-field attribution after turns
or periodic return remains unsupported. A passing isolated-motion rejection test
identifies invalid behavior; it does not repair the underlying candidate law.

[Quantum events](QUANTUM_EVENTS.md) implement the selected finite deferred-state
method. Querying computes branch weights; an explicit instrument and ticket select
a recorded outcome without advancing the physical clock. Host dependency evaluation
is counted separately from Q-ORACLE-1. [Focus](QUANTUM_FOCUS.md) remains a separate
opt-in candidate-selection experiment. The [native event program](NATIVE_QUANTUM_EVENTS.md)
now composes the optional quantum owner through the ordinary `Simulation` and
runner, with shared causal identities, repeated local encounters and explicit
computation charges. Configured deterministic endpoints reproduce an ordinary
mechanical path when both costs fit the budget; resolver overhead is not hidden.
Combining an event program with spatial fields is rejected. These finite controls
do not derive universal scattering, an objective collapse criterion, a general
classical limit or quantum-plus-matter energy conservation. The earlier
[contact trial](QUANTUM_CONTACT_TRIAL.md) remains a historical eight-tick fixture,
not the current scope of the native event-program interface.

The [entity inventory](PHYSICAL_ENTITIES.md), [catalog](ENTITY_CATALOG.md) and
[conversion interface](LOCAL_CONVERSIONS.md) separate representation from physical
acceptance. Maxwell dynamics, gravity, general physical creation/annihilation,
relativity and universal energy conservation are not established merely by these
interfaces or by successful software tests.

The [small-space comparisons](../examples/small-space/README.md), integrated through
PR #40, record 24 experiments in 9-cubed/15-cubed worlds. Finite reservoir transfer,
a ray-speed parameter and a restricted zero-total-momentum unequal-mass candidate
are explicit configuration solutions, not changed entity defaults or derived
universal laws. Their limitations and revision-specific results remain in the
experiment README.

As of the audit reference, PRs #31, #33, #37 and #38 are separate unmerged work:
standalone vector lab, Highlights/skill reconciliation, rational particle contracts
and local E/B response probes respectively.
Consult [live PRs](https://github.com/Closer24/Universe24/pulls); do not infer their
integration from their descriptions or overwrite their shared files during cleanup.
Historical integration chronology remains in Git and [validation records](VALIDATION.md),
not a competing current-status list.

## Resume without a conversation

1. Read [AGENTS.md](../AGENTS.md), inspect local changes, fetch main and record the
   actual base. Use a separate branch/worktree for the task.
2. Use [README installation instructions](../README.md#install-and-run) and the
   interpreter in [.python-version](../.python-version). The minimum package version
   in [pyproject.toml](../pyproject.toml) does not select the shell interpreter.
3. Select an explicit initialization and an unused output directory. The
   [workspace](WORKSPACE.md) changes runtime JSON without rebuilding the engine.
   Visualization is opt-in. Registered outputs expire under [retention](RETENTION.md);
   idle cleanup needs the existing watcher or a scheduled invocation.
4. Follow [CONTRIBUTING.md](../CONTRIBUTING.md), inspect the affected selection from
   `python tools/check.py`, and attach actual results for the submitted tree.
   Use `--full` only for an explicitly justified complete audit.
5. Hand off the scope, validation, limits and integration state through the PR and
   [shared workflow](../skills/workflow.md). A Git rename changes the source fingerprint;
   retain older fingerprints as historical evidence rather than relabeling old runs.
