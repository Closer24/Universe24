# Migration from the single-file simulator

Install from the extracted project first:

```bash
python -m pip install -e '.[render,dev]'
```

## Primary initialization-based API

`Simulation` now requires a validated `InitialState`; it no longer accepts an
implicit scalar Config or built-in particle semantics. Initialize the active
model with a strict JSON file:

```bash
python -m event_universe --init examples/basic.json --output artifacts/basic
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
continues to use the current defaults; use `ScalarSimulation` for component injection.
See `FIELDS.md` for the scalar protocol and an example.

Imports of `update_field`, `update_particle`, `gradient`, `transverse_gradient`,
`choose_axis` and `MODEL_ID` from `models.local_field` remain supported through
re-exports. New code uses `fields.scalar`, `dynamics.turning`, `dynamics.movement`
and `models.current_field` directly. Tests specific to the current law moved
from `test_local_laws.py` to `test_current_field.py`.

Activity decisions are now injected into `Engine` with the optional
`field_activity=` keyword. `ScalarSimulation()` explicitly keeps legacy activity;
`ScalarSimulation(field=...)` tracks both value and remainder changes by default.
This fixes prematurely stopped remainder-only evolution for replacement fields.
Explicit `ScalarSimulation(field_activity=...)` accepts a predicate over two scalar
samples and a source count. Direct `Engine` predicates receive two cell records
and a source count; omitting one retains visited cells conservatively.
Periodic geometry is shared by all engine operations in `core/lattice.py`.

## Version history

Use Git commits and tags for source versions. The v10 reference is retained under
`tests/reference/` only; application code must never import it. Each run records
a SHA-256 fingerprint of the active package files, so source identity survives
installation from a ZIP or wheel without a Git checkout.
