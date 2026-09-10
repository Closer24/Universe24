# Migration from the single-file simulator

Install from the extracted project first:

```bash
python -m pip install -e '.[render,dev]'
```

Use `python -m event_universe` for runs with automatic HTML. Use
`from event_universe import Config, Simulation` for programmatic work.

## Existing notebook imports

`from persistent_source_field import IntegerO1Field3D, Config, PX` still works.
`IntegerO1Field` remains an alias. The compatibility facade keeps `paths`,
`force_records`, `collisions`, momentum methods, `audit()`, `report()`,
`xy_slice(z)` and `particles_on_xy_slice(z)`. This facade opts into in-memory
recording. The modern `Simulation` has no retained history by default.

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

Existing `Simulation(config, observer=...)` calls retain the same defaults.
Optional `field=` and `turning=` keywords replace the respective component
without changing scheduling. The compatibility `IntegerO1Field3D` facade
continues to use the current defaults; use `Simulation` for component injection.
See `FIELDS.md` for the scalar protocol and an example.

Imports of `update_field`, `update_particle`, `gradient`, `transverse_gradient`,
`choose_axis` and `MODEL_ID` from `models.local_field` remain supported through
re-exports. New code uses `fields.scalar`, `dynamics.turning`, `dynamics.movement`
and `models.current_field` directly. Tests specific to the current law moved
from `test_local_laws.py` to `test_current_field.py`.

Activity decisions are now injected into `Engine` with the optional
`field_activity=` keyword. `Simulation()` explicitly keeps legacy activity;
`Simulation(field=...)` tracks both value and remainder changes by default.
This fixes prematurely stopped remainder-only evolution for replacement fields.
Explicit `Simulation(field_activity=...)` accepts a predicate over two scalar
samples and a source count. Direct `Engine` predicates receive two cell records
and a source count; omitting one retains visited cells conservatively.
Periodic geometry is shared by all engine operations in `core/lattice.py`.

## Version history

Use Git commits and tags for source versions. The v10 reference is retained under
`tests/reference/` only; application code must never import it. Each run records
a SHA-256 fingerprint of the active package files, so source identity survives
installation from a ZIP or wheel without a Git checkout.
