# Project status and restart guide

The host [experiment contract](EXPERIMENTS.md) now provides reusable JSON parts,
packaged Draft 2020-12 schemas, [optional SI dimensional checks](UNITS.md) and
[exact checkpoint continuation](CHECKPOINTS.md). Existing direct initialization
remains supported. These interfaces organize and validate existing laws; they
do not supply missing physical dynamics. Check the associated PR/CI before
assuming this change is integrated into main. External output adapters remain
outside this extension.

Optional [configured topology](CONFIGURED_TOPOLOGY.md) supports 2 to 26 reciprocal
ports with three-dimensional vectors, bounded site patterns and causal local
field/carrier transfers. Omitted topology retains the six-cardinal-port model.
The [BCC vector encounter](../examples/topology/README.md) demonstrates a guarded
polarization rotation; its normalized diagnostics do not establish Maxwell
dynamics. Specialized six-port couplings, outward octant transport and the
native event program explicitly reject unsupported topology combinations.

[Configuration preflight](CONFIGURATION_VALIDATION.md) checks initialization,
physical reference catalogs, all supplied representation profiles and observer
sidecars without running a world. It shares parsing and preparation with runtime
entry points. Configuration validity is separate from run and physics acceptance.

The optional [local reception observer](LOCAL_OBSERVER.md) records arrivals at
one node configured in the ordinary initialization JSON, using a completed local-cycle counter and the existing HTML player.
Global state remains available as an explicit audit view. Optical images, radar
geometry, proper time and Maxwell laws in an emergent spacetime remain open.

An optional [directional-wave candidate](DIRECTIONAL_WAVE.md) supplies six modes
and a configured polarization encounter with exact normalized energy/momentum
guards. It uses the existing local field engine and does not replace the catalog
probes or establish Maxwell dynamics. Verify the current Git tree and PR status
before using historical validation evidence.

For a clean machine or deleted conversation, follow
[recovery without chat history](RECOVERY.md), including the versioned daily
genericity skill and local retention setup.
The [Highlights implementation map](HIGHLIGHTS_IMPLEMENTATION.md) records the
live specification reconciliation, entity coverage and exact source contracts.

The [finite quantum-register extension](QUANTUM_ENTITIES.md) adds unobserved
channels, mixed conditional states, grouped outcomes, finite multilevel registers
and quantum preparation profiles for the existing 46 catalog entries. Species
dynamics, spatial-field clock composition and general classical emergence are
not established. Reproduce with `examples/quantum/run_physics_checks.py`.


The [local Maxwell experiment](../examples/maxwell/README.md) selects a
six-population reflection and causal streaming through configuration only.
Its conditional long-wavelength vacuum generator and eleven small-world runs
give two transverse modes with leading speed one half link per tick. Centered
Gauss conservation, exact macro electromagnetic energy and indefinite integer
mixing remain explicit blockers; this is not a complete electromagnetic law.

The [small-space comparisons](../examples/small-space/README.md) record 24
9-cubed/15-cubed entity, source and response experiments. Local accounting and
selected mechanisms pass; field/particle physical laws remain incomplete.
Finite owned-reservoir transfer, a ray-speed parameter and a restricted
zero-total-momentum unequal-mass candidate are explicit configuration solutions,
not replacements for the default entity profiles or derived universal laws.

The [physical reference catalog](ENTITY_CATALOG.md) separates sourced properties
and possible interactions from explicitly supplied representation experiments.
It covers 11 field families, 35 particle records and 14 disturbance families, with
17 interaction families and 33 representative channels. No catalog formula,
measured mass or interaction label becomes a simulation law. The original 46
bounded probes live in a separate file and compile into ordinary run inputs.
The [local conversion interface](LOCAL_CONVERSIONS.md) supports explicit atomic
two-to-two type replacement with declared balances. These additions do not
establish physical annihilation, general particle production or physical field
dynamics. Consult current PR/CI evidence for the exact integrated tree.

The [physical entity inventory](PHYSICAL_ENTITIES.md), based on main
`09464b41b2c44a191aa2fcbdf4b036680bd646a5`, separates descriptive entities from
executable mechanics and unestablished emergence. New equal-mass charged-pair
and two-vector port probes use elementary operations only. They do not provide
Maxwell dynamics, gravity or matter/antimatter creation and annihilation.
Use the linked catalog and exact PR evidence instead of treating physical labels
as implemented laws.

Local field-rule extension base: 2026-09-12, main
`12c85316f011d0601adcd0f4a31f0f52e59eaa27`. The opt-in
[local rule contract](LOCAL_FIELD_RULES.md) adds logical field groups, independent
six-port reads, retained/outgoing field assignments and guarded joint
field/carrier transactions. This is a bounded generic research interface, not
an implemented electromagnetic law. Integration and validation status require
the current PR and its exact tested tree; this paragraph does not certify a run.

Integration reference: 2026-09-12. [PR #27](https://github.com/Closer24/Universe24/pull/27)
combines reviewed spatial-field feature head
`137830fd621b9522598e0719e7bd2055ead595a9` with main
`15029ba8d02bd7f1bb1dd1148fe55405ec1536b1`, which adds atomic generic interactions
and the configured unequal-mass elastic example through PR #28, followed by
main `64d26a89842637ab71517ec45aebfa7c3deae331` and its affected-check selection
through PR #29. Validation selects changed code and reviewed consumers by default;
complete audits require explicit `--full`. See [CONTRIBUTING.md](../CONTRIBUTING.md).
Spatial fields,
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

| Scope | Implemented owner | Contract and limits |
| --- | --- | --- |
| Active generic simulator | [disturbance_api.py](../src/event_universe/disturbance_api.py), [disturbance_engine.py](../src/event_universe/core/disturbance_engine.py) | `Simulation(InitialState)`; laws and fields come from explicit initialization, not physical names |
| Record operation policy | [record_operations.py](../src/event_universe/fields/record_operations.py) | Fixed local activity, delivered-record combination and cost reporting; the engine retains scheduling |
| Rational particle candidates | [rational contract](RATIONAL_PARTICLES.md) | Explicit bounded rational regions, balanced routes, fractional movement credit and local checks; supplied reference laws |
| Local expressions and transactions | [disturbances.py](../src/event_universe/fields/disturbances.py) | Bounded integer operations, declared balances, fixed local capacities and explicit rejection |
| Spatial fields | [spatial_engine.py](../src/event_universe/core/spatial_engine.py) | Fixed neighbor transit, baselines, schema 1 transport and opt-in schema 2 finite budgets/decay |
| Local field read/response rules | [local_field_rules.py](../src/event_universe/fields/local_field_rules.py) | Six-port reads and guarded local field/carrier proposals; no implied Maxwell law |
| Entity reference and representation | [entity_catalog.py](../src/event_universe/entity_catalog.py), [entities.py](../src/event_universe/entities.py), [catalog.json](../examples/known-entities/catalog.json) | Sourced properties and interactions are validated separately; 46 explicitly supplied experiment profiles compile without deriving laws from labels |
| Quantum event backend | [event_network.py](../src/event_universe/quantum/event_network.py) | Deferred joint-state evaluation and explicit instruments under the quantum owner |
| Native event programs | [event_runtime.py](../src/event_universe/integration/event_runtime.py), [event_space.py](../src/event_universe/core/event_space.py) | Optional shared causal identities, repeated local triggers and charged executed paths; rejects spatial fields |
| Historical contact experiment | [quantum_contact_trial.py](../src/event_universe/integration/quantum_contact_trial.py) | One bounded eight-tick contact trial selects a real local mechanical proposal; not a general dispatcher |
| Shared integer arithmetic | [integer.py](../src/event_universe/core/integer.py) | Shared bounded integer primitives; expression evaluation retains its separate owner |
| Local E/B pulse candidate | [local impulse contract](LOCAL_LORENTZ_FIELD.md) | Held one-shot probes, finite pulse transport and an opposite local reservoir; not derived Maxwell dynamics |
| Formula-free state diagnostic | [cell_contract.py](../src/event_universe/diagnostics/cell_contract.py) | Read-only structural guard for state ownership; host diagnostics are not physical updates |
| Standalone vector laboratory | [laboratory guide](../tools/generic_vector_lab/README.md) | Separate research/reference process, not the active generic Simulation |
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

The audit reference now includes the standalone vector laboratory, shared bounded
arithmetic, the local E/B pulse and formula-free cell-state guard, and the
Highlights/recovery documentation. Their appearance in the checkout does not
promote reference experiments into the active physical engine. The
[Highlights coverage record](HIGHLIGHTS_IMPLEMENTATION.md) preserves its stated
historical revision; use this map and current contracts for later additions.
Consult [live PRs](https://github.com/Closer24/Universe24/pulls) for any subsequent
work rather than inferring integration from a branch description.
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

## Repository naming and ownership audit

The repository-wide naming/ownership audit is reconciled against main
`8ceb1fd00e9f23020965d8c2873caf0eff384f92`. It preserves the integrated
native quantum, quantum-entity and Maxwell research additions while keeping
one active implementation owner per documented responsibility. Historical
research APIs and standalone laboratories remain explicitly labeled.
