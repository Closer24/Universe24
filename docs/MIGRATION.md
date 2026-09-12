# API and repository migration

## Closed elementary input (schema 3)

This is an intentional ordinary-input compatibility change. Use
`Simulation`, `parse_initial_state`/`load_initial_state` and the ordinary CLI only
with [schema 3](ELEMENTARY_FIELDS.md). Start with `examples/elementary_motion.json`,
`elementary_contact.json` or `elementary_open.json`. Merely changing a version
number does not translate a supplied force program into elementary operations.

Existing schema 1/2 configurations remain unchanged as reference inputs. Import
`ReferenceSimulation`, `parse_reference_state`, `parse_reference_json` and
`load_reference_state` from `event_universe.reference_api`; execute with
`python -m event_universe.reference_runner --init examples/basic.json --output
artifacts/reference-basic`. The Python runner wrapper is `run_reference_initialization`
in `event_universe.reference_runner`. There is no ordinary CLI or JSON reference
flag. Workspace templates and validation use the active schema only.

The catalog and native event programs still describe their supplied candidate
laws. Their compilers and test consumers now select the reference path explicitly;
their numerical assertions are retained. The earlier migration below concerns
the original initialization API and separate historical scalar models.

Install from the extracted project first:

```bash
python -m pip install -e '.[render,dev]'
```

## Primary initialization-based API

`Simulation` now requires a validated `InitialState`; it no longer accepts an
implicit scalar Config or built-in particle semantics. Initialize the active
model with a strict JSON file:

```bash
python -m event_universe.reference_runner --init examples/basic.json --output artifacts/basic
```

Programmatic users import `Simulation` from `event_universe` and
`load_initial_state` from `event_universe.initialization`. Field/type names,
transport, updates, coupling and costs are data. Read
[DISTURBANCES.md](DISTURBANCES.md) for the complete schema and limits.

Runs are headless. Visualization requires `--visualize`; standard tests do not
produce animation reports. `pytest --visualize-runs` explicitly enables them.
The active runner requires an empty output directory and preserves the original
initialization, events, final state and metadata.

For the old scalar engine, change `Simulation(...)` calls and imports to the
explicit name `ScalarSimulation(...)`. `LinkedSimulation`, `BalancedSimulation`
and `CausalStreamSimulation` remain named research APIs. Historical scenarios
run through `python -m event_universe.legacy_runner --scenario ...`; the primary
CLI does not accept `--scenario`. The old runner function is
`event_universe.legacy_runner.run_scenario`, headless unless `visualize=True`.
The following notebook/component notes concern only those historical APIs.

## Existing notebook imports

`from persistent_source_field import IntegerO1Field3D, Config, PX` still works.
`IntegerO1Field` remains an alias. The compatibility facade keeps `paths`,
`force_records`, `collisions`, momentum methods, `audit()`, `report()`,
`xy_slice(z)` and `particles_on_xy_slice(z)`. This facade opts into in-memory
recording. The modern `ScalarSimulation` has no retained history by default.

| Old usage | New usage or behavior |
| --- | --- |
| `world.particles[pid][PX]` | Still supported for reading; prefer `.px` |
| `world.particles[pid][PX] = value` | State is immutable; supply momentum in initial conditions |
| `world._cell(address)[PHI] = value` | `world.seed_field(address, value)` before the first tick |
| `world.config = other_config` | Create a new world; configuration is immutable |
| `self_tests()` | `python -m pytest` or `python tools/check.py` |
| `regression_two_particle_plane()` | `test_original_180_tick_two_particle_regression` |
| `report()["bounded_core_integers"]` | `report()["checks"]["bounded_integer_state"]` |
| `make_v7_run_html.render_xy_run(...)` | Application runner, or `diagnostics.render.render_run(...)` |

Private engine mutation helpers are no longer a supported initialization API.
Negative particle IDs are rejected because `-1` is the empty-slot sentinel.
`audit()` validates state with exceptions, also under optimized Python.

The physical source is now one package. The saved `persistent_source_field.py`
is a small import facade and requires this package to be installed; downloading
that facade alone is insufficient. The delivered ZIP contains all required
source, tests, documentation and the preserved reference.

## Field and turning components

Existing `ScalarSimulation(config, observer=...)` calls retain the same defaults.
Optional `field=` and `turning=` keywords replace the respective component
without changing scheduling. The compatibility `IntegerO1Field3D` facade
continues to use the historical scalar defaults; use `ScalarSimulation` for component injection.
See `SCALAR_FIELDS.md` for the scalar protocol and an example.

Imports of `update_field`, `update_particle`, `gradient`, `transverse_gradient`,
`choose_axis` and `MODEL_ID` from `models.local_field` remain supported through
re-exports. New code uses `fields.scalar`, `dynamics.turning`, `dynamics.movement`
and `models.scalar_field` directly. Tests specific to the historical scalar law moved
from `test_local_laws.py` to `test_scalar_field_model.py`.

Activity decisions are now injected into `ScalarEngine` with the optional
`field_activity=` keyword. `ScalarSimulation()` explicitly keeps legacy activity;
`ScalarSimulation(field=...)` tracks both value and remainder changes by default.
This fixes prematurely stopped remainder-only evolution for replacement fields.
Explicit `ScalarSimulation(field_activity=...)` accepts a predicate over two scalar
samples and a source count. Direct `ScalarEngine` predicates receive two cell records
and a source count; omitting one retains visited cells conservatively.
Periodic geometry is shared by all engine operations in `core/lattice.py`.

## Version history

Use Git commits and tags for source versions. The v10 reference is retained under
`tests/reference/` only; application code must never import it. Each run records
a SHA-256 fingerprint of the active package files, so source identity survives
installation from a ZIP or wheel without a Git checkout.


## Explicit historical component names

The 2026-09-12 consistency cleanup makes the active generic engine distinct from
historical particle models. These are source/import/command renames, not new
physical laws. Public `event_universe.Simulation`, `ScalarSimulation`,
`LinkedSimulation`, `BalancedSimulation` and `CausalStreamSimulation` keep the same
implementations. Internal imports in downstream scripts must use the new paths.
No second implementation or duplicate compatibility module was added for these names.

| Previous internal path or name | Canonical replacement |
| --- | --- |
| `event_universe.api` | `event_universe.particle_api` |
| `event_universe.core.engine.Engine` | `event_universe.core.scalar_engine.ScalarEngine` |
| `event_universe.models.current_field.CurrentFieldModel` | `event_universe.models.scalar_field.ScalarFieldModel` |
| `CURRENT_MODEL` in the historical field module | `SCALAR_MODEL` |
| `event_universe.scenarios` | `event_universe.particle_scenarios` |
| `tests/test_engine.py` | `tests/test_scalar_engine.py` |
| `tests/test_current_field.py` | `tests/test_scalar_field_model.py` |
| `tests/test_application.py` | `tests/test_legacy_application.py` |
| `docs/FIELDS.md` | `docs/SCALAR_FIELDS.md` |
| `examples/known-entities/run.py` | `examples/known-entities/run_reference_checks.py` |
| `examples/known-entities/run.ps1` | `examples/known-entities/run_reference_checks.ps1` |
| `examples/known-entities/collision.json` | `examples/04-unequal-mass-collision.json` |
| `examples/particle-contracts/build.py` | `examples/particle-contracts/build_reference_configurations.py` |
| `examples/maxwell/run.py` | `examples/maxwell/run_experiments.py` |
| `examples/small-space/run.py` | `examples/small-space/run_experiments.py` |

The removed collision file was byte-identical to the canonical workspace example.
The reference command resolves its logical `collision` experiment to that file;
other reference inputs retain their separate configuration and expectations.
Archived files under `tests/reference/` are unchanged. Earlier validation records
retain their original paths and hashes; use this table to locate the current owner.


## Duration-only reference configuration

The reference three-mass case now reads `examples/three_mass_finite.json` and
passes `ticks=120` to the existing runner rather than keeping a second JSON
initialization. Replace the former `examples/known-entities/three-masses.json`
command with:

```sh
python -m event_universe --init examples/three_mass_finite.json --ticks 120 --output artifacts/three-masses
```

The original initialization retains its 100-tick default and is copied unchanged
into the output. Actual execution length is recorded separately. The reference
wrapper preserves its 120-tick numerical checks; physical coefficients, budgets
and laws are unchanged.
