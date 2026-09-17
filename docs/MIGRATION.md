# API and repository migration

Install from the extracted project first:

```bash
python -m pip install -e '.[render,dev]'
```

## Historical particle candidates deleted on 2026-09-17

The model owner's instruction of 2026-09-17, recorded in
[HIGHLIGHTS.md](HIGHLIGHTS.md) sections 3.3, 3.4, 3.5, 3.19, 3.20, 5.1 and 5.4
and in [RAY_EVENT_MODEL.md](RAY_EVENT_MODEL.md) section 6, is that everything
not used is deleted. Issue #164, bucket A, removed the unused historical
particle candidates from the package, tests, tools and documents:

- `core/scalar_engine.py`, `core/linked_engine.py`, `core/streaming_engine.py`,
  `core/streams.py`, `core/links.py`, `core/lattice.py`, `core/contracts.py`,
  the `models/` and `dynamics/` packages, `fields/scalar.py`, `fields/policies.py`,
  `fields/halo.py`, `fields/geometry.py`, `fields/streaming.py`, `particle_api.py`,
  `particle_scenarios.py`, `legacy_runner.py`, `compat.py`, `diagnostics/render.py`,
  `diagnostics/live.py`, `diagnostics/frames.py`, `diagnostics/measurements.py`,
  `diagnostics/recorder.py` and `diagnostics/invariants.py`;
- the notebook facade `src/persistent_source_field.py`, the diagonal-motion tool
  `tools/check_diagonal_motion.py` and the frozen archive `tests/reference/`;
- the public names `ScalarSimulation`, `LinkedSimulation`, `BalancedSimulation`,
  `CausalStreamSimulation`, `Config`, `NodeState`, `ParticleState`, `LinkConfig`
  and `CausalStreamConfig` from the `event_universe` package;
- their tests, the historical run-capture, live-display and renderer tests, and
  the documents `SCALAR_FIELDS.md`, `BALANCED_MOTION.md` and `CAUSAL_STREAM_FIELD.md`.

There is no replacement API: the active `Simulation` is initialization-defined
([DISTURBANCES.md](DISTURBANCES.md)), shared bounded arithmetic is
`core/integer.py`, and `pytest --visualize-runs` now only enables the
visualization-marked tests. `core/state.py` remains until its quantum consumers
are removed in the next step. Dated validation records keep their original scope.

## Primary initialization-based API

The quantum event storage migration removes the separate local predecessor list
and `history(register)` traversal. Events remain directly addressable in the
immutable spacetime DAG; fixed cursors retain current register heads and modeled
times. The native v3 [origin-cell contract](WAVE_ORIGINS.md) adds six local wave
references, separate from virtual register heads. The coherent path example is
now `examples/quantum/event_paths.json`; its regression suite is
`tests/test_quantum_node_events.py`.

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

## Version history

Use Git commits and tags for source versions. Each run records
a SHA-256 fingerprint of the active package files, so source identity survives
installation from a ZIP or wheel without a Git checkout.


## Explicit historical component names

The 2026-09-12 consistency cleanup made the active generic engine distinct from
historical particle models. These were source/import/command renames, not new
physical laws. The rows whose renamed target was deleted on 2026-09-17 (the
historical API, engine, model, scenario and test modules and the scalar-field
document) are omitted; the remaining rows still locate a current owner.

| Previous internal path or name | Canonical replacement |
| --- | --- |
| `examples/known-entities/run.py` | `examples/known-entities/run_reference_checks.py` |
| `examples/known-entities/run.ps1` | `examples/known-entities/run_reference_checks.ps1` |
| `examples/known-entities/collision.json` | `examples/04-unequal-mass-collision.json` |
| `examples/particle-contracts/build.py` | `examples/particle-contracts/build_reference_configurations.py` |
| `examples/maxwell/run.py` | `examples/maxwell/run_experiments.py` |
| `examples/small-space/run.py` | `examples/small-space/run_experiments.py` |

The removed collision file was byte-identical to the canonical workspace example.
The reference command resolves its logical `collision` experiment to that file;
other reference inputs retain their separate configuration and expectations.
Earlier validation records retain their original paths and hashes; use this
table to locate the current owner.


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
