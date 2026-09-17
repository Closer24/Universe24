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
visualization-marked tests. `core/state.py` was deleted in the next step,
below. Dated validation records keep their original scope.

## Shared quantum resource and integration layer deleted on 2026-09-17

Under the same instruction, issue #164 buckets B.1 and B.2 removed the shared
quantum resource and the integration layer built on it, following
[HIGHLIGHTS.md](HIGHLIGHTS.md) sections 3.18 (deleted), 3.19, 3.20 and 5.4
and [RAY_EVENT_MODEL.md](RAY_EVENT_MODEL.md) section 6, steps 3 and 4: no
owner answers at a distance, the Detector is a marked Node and every
alternative is an event on the board.

- The `quantum/` package (`deferred`, `event_network`, `event_rules`, `focus`,
  `mixed`, `state`, `query`, `terminal`, `postulates`, `wave_origins`,
  `operations`, `contact_outcomes`, `contact_rules`) and the `integration/`
  package (`event_program`, `event_runtime`, `contact_program`,
  `contact_runtime`, `causal_contact_runtime`, `recurrent_contact_runtime`,
  `quantum_entities`, `quantum_bridge`, `quantum_contact_trial`,
  `quantum_event_trial`) are gone.
- The `event_program` initialization member and `InitialState.event_program`
  are gone: a document that still carries the member is rejected as an unknown
  key, no configuration selects a native program, a quantum profile or the
  classical `causal-events-v1` ledger, and `causal-events.jsonl` is no longer
  written. `Simulation` no longer refuses `node_workers > 1` for a program.
- `event_universe.entities` compiles classical profiles only: the
  `representation` argument, the `--representation` option, the
  `quantum_profile` binding key and the `quantum` count of `validate_profiles`
  are gone, and the 46 `quantum_profile` members left
  `examples/known-entities/representation-probes.json`.
- `core/state.py` and `tests/test_integer_contract.py` are gone;
  `fields/source_envelope.py` imports `bounded_gcd` from `core/integer.py`.
- `examples/quantum/`, `examples/quantum-classical/`,
  `examples/catalog-contact/`, `examples/spatial_causal_events.json`, the
  relativity probes `quantum_gravity.py`, `quantum_from_the_side.py` and
  `time_symmetry.py`, the three quantum entity-audit inputs and the
  contact-fields experiment of the named-particle gallery are gone;
  `examples/spatial_computation_delay.json` lost its `event_program` member.
- The twelve quantum documents named in the [documentation index](README.md),
  the `quantum-contact-trial` workflow, 36 test modules and the fixtures
  `tests/quantum_detector_fixture.py`, `tests/support/quantum.py` and
  `tests/support/contact.py` are gone; the Node-level source-envelope and
  event-ledger cases of `test_causal_contact_fields.py`,
  `test_null_notices.py` and `test_native_event_runtime.py` moved to
  `test_active_node_contracts.py`, `test_null_notices.py` and
  `test_event_links.py`.

There is no replacement API. `core/event_space.py`, `core/event_links.py`,
`core/event_resolution.py`, the source-envelope modules, the bond registry,
claim/gather and `fields/record_operations.py` stay until buckets B.3 to B.6
of the same issue.

## Bond registry, claim-gather, lottery capture and occupied-links guard deleted on 2026-09-17

Under the same instruction, issue #164 bucket B.5 removed the last owners that
answered at a distance, kept a register at a Node or made a ray wait for room
([Highlights](HIGHLIGHTS.md) 3.18 deleted, 3.19, 3.20, 5.1 and 5.4;
[ray-event model](RAY_EVENT_MODEL.md) section 5 and section 6 step 5):

- `fields/bonds.py` (`BondRegistry`), the ray fields `bond`, `train` and
  `homing`, the `Claim` record, the spatial-field keys `bond` and `claim`, the
  emission keys `bond_field` and `train_field`, the absorb-rule keys
  `bond_setting`, `claim` and `capture_salt`, the Kerengonen
  `"capture": "lottery"` and `capture_seed`, the record rows `absorb_tickets`
  and `absorbed_trains`, the runner metadata `spatial_claims` and
  `spatial_bonds`, the sampling profile `historical-autonomous-v1` and the
  planner argument `claims`: the spatial planner now takes states, records,
  received count, node cost, rays, tick and ray hold;
- the pre-planning refusal "outgoing spatial links are occupied": there is no
  occupied channel and no capacity rule, rays leaving on one Link in one
  interval travel in one packet bounded by `ray_slots`, and
  `SpatialNode.require_free_links` rejects at commit a departure that would
  overwrite a packet still in transit, a host scheduling error rather than a
  physical rule;
- the examples `bell-chsh/`, `kerengonen-bell/`, `claim-gather/`,
  `gathered-gravity/`, `research/bell-postulate-22/` and the ray-gallery
  panels `4-bonded-pair`, `5-claim-gather` and `8-lottery-detector`; the
  double-slit probe's lottery columns; the redshift sweep reads its train by
  arrival order instead of a claim-stamped label;
- the tests `test_bonds.py`, `test_ray_bell_chsh.py`, `test_kerengonen_bell.py`,
  `test_claim_gather.py`, `test_research_sampling_admission.py` and
  `test_gathered_gravity.py`, and the lottery cases of `test_kerengonen.py`,
  `test_ray_integration_guards.py` and `test_detector_sampling_contract.py`.

There is no replacement API: `capture` is `share` or `threshold`, and the
Detector mark of Highlights 3.19 (issue #169, feature 2) will own the ticket
sequence that `core/spatial_state.py` keeps (`TICKET_MODULUS`, `next_ticket`,
`ticket_draw`, `phase_cosines`). `core/event_space.py`, `core/event_links.py`,
`core/event_resolution.py`, the source-envelope modules and
`fields/record_operations.py` stay until buckets B.3, B.4 and B.6.

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
