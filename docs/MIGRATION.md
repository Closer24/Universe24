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
of the same issue. The source-envelope modules, the causal event ledger and
the bond registry were deleted in the next steps, below.

## Source envelopes deleted on 2026-09-17

Under the same instruction, issue #164 bucket B.3 removed the source
envelopes, following [HIGHLIGHTS.md](HIGHLIGHTS.md) section 3.5 and
[RAY_EVENT_MODEL.md](RAY_EVENT_MODEL.md) section 5 (row R5) and section 6,
step 7: a field is the ray's own information spreading in ray form to the
Nodes around it, and no Node retains a source envelope.

- `core/source_envelope_node.py`, `core/source_envelope_state.py`,
  `core/source_emission.py`, `core/source_emission_node.py`,
  `fields/source_envelope.py` and `fields/source_emission.py` are gone, with
  the `CausalSourceResolver` protocol of `core/event_resolution.py`,
  `SpatialEngine.commit_source` and its `spatial_envelope_source` event, the
  `source_envelope` member of the disturbance NodeState and the envelope
  records of the formula-free state audit in `diagnostics/node_contract.py`.
- `tests/test_source_envelope.py` and `tests/test_null_notices.py` are gone;
  the envelope cases of `test_active_node_contracts.py` and
  `test_node_state_contract.py` and the envelope rows of the architecture
  gate went with them. No example declared an envelope source, so no example
  or `tools/check.py` consumer row changed.

## Causal event ledger deleted on 2026-09-17

`core/event_space.py`, `core/event_links.py` and `tests/test_event_links.py`
were deleted on 2026-09-17 under issue #164 bucket B.4, following
[HIGHLIGHTS.md](HIGHLIGHTS.md) section 3.20 and the "Where is state stored"
row of [RAY_EVENT_MODEL.md](RAY_EVENT_MODEL.md): all the information is on
the rays, the origin Node keeps nothing and there is no register.

- `DisturbanceEngine` and `SpatialEngine` no longer accept `event_space=`.
  `NodeEvents(observer)` takes the observer alone; `message()` builds the
  observer message that `publish()` sends, and `record()`, `require_room()`
  and `enabled` are gone. Observer messages carry no `event_id` or `parents`.
- `Packet`, `LocalPlan`, `PendingCycle`, `SpatialPacket` and
  `PendingSpatialCycle` lost `cause_id`; `SpatialNodeState` lost `cause_id`,
  `sample_cause_id` and `cost_cause_id`; `DisturbanceNodeState` lost
  `cause_id`, `event_cursors` and `event_references`; `NodeView` lost
  `event_heads` and `event_origins`; `LocalContext` lost `cause`.
- `computation_report()` no longer reports `causal_events`,
  `causal_event_capacity`, `event_ledger_cost` or
  `carrier_model_operations_cost`; `state.json` and recorded frames carry no
  `event_support`, and the playback page draws none. The profile tool reports
  no `event_history_enabled`.

There is no replacement API. `core/event_resolution.py` and
`fields/record_operations.py` stay until bucket B.6 of the same issue.

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
`ticket_draw`, `phase_cosines`). `core/event_resolution.py` and
`fields/record_operations.py` stay until bucket B.6; the source-envelope
modules went with bucket B.3 and the causal event ledger with bucket B.4 on
the same day.

## Ray hidden state added on 2026-09-17 (`ray-event-state-v1`)

Issue #169, feature 1, the first implementation step of the
[ray-event model](RAY_EVENT_MODEL.md#6-migration-in-order) (step 2) under
[Highlights](HIGHLIGHTS.md) 3.3, 3.19, 3.20 and 5.1: every ray carries the
number of steps it has made since its event and the information of that
event, as hidden variables that no rule reads
([ray state](SPATIAL_FIELDS.md#ray-state-ray-event-state-v1)).

- `Ray` (`core/spatial_state.py`) gains `steps`, `outbound`, `event_ports`,
  `event_shares` (six bounded entries in Port order) and `detector`, all with
  defaults, so a `Ray(heading, accumulators, amount, ...)` call still
  constructs; `validate_rays` bounds them; `advance_ray` counts `steps` up
  while outbound and down on the walk back and moves the phase the same way;
  `merge_rays` keys on them, so rays of different events never merge;
  `emit_rays`, a mirror's reflection and a firing `ray_interactions` group
  stamp every ray they create with the event's mask and shares.
- The runner records `ray_state: "ray-event-state-v1"` in `run.json` beside
  `sampling_profile`.
- Behavior of existing worlds is unchanged except where rays of different
  events used to merge: `ray_count` and slot use count events, and one-Link
  self-exclusion excludes exactly the departure cycle's rays, so a moving
  absorber-emitter absorbs its earlier cycle's quantum back
  (`test_energy_audit.py`, [expectations](TEST_EXPECTATIONS.md#ray-hidden-state)).
- Tests that construct rays or compare emitted or interacted rays directly
  include the stamp (`test_ray_field.py`, `test_native_ray_coupling.py`,
  `test_ray_merge_contracts.py`, `test_ray_integration_guards.py`).

No initialization key changes. No rule, coupling, absorber, readout or
Detector reads the new fields in this step.

## Node Detector bit added on 2026-09-17 (`detector-mark-v1`)

Issue #169, feature 2, migration step 3 of the
[ray-event model](RAY_EVENT_MODEL.md#6-migration-in-order) under
[Highlights](HIGHLIGHTS.md) 3.19, 3.20 and 5.4: a Node marked in the
initialization draws one bit per arriving ray from its own ticket stream and
is otherwise an ordinary Node
([Detector mark](DETECTOR_SAMPLING.md#the-detector-mark-detector-mark-v1)).

- New optional initialization key `detectors`: a list of marks, each with
  `position`, `setting` `[n, d]` and `seed`, all required, no default rate,
  one mark per position, admitted only under the shared Detector admission
  (schema 1, `link_ticks` 1, ray fields on the links metric at pace 1/1
  without decay, unit-axial headings closed under negation)
  ([schema](SPATIAL_FIELDS.md#detector-mark-detector-mark-v1)).
- `DetectorMark(position, pass_numerator, pass_denominator, seed)`,
  `DETECTOR_MARK`, `MAX_DETECTORS`, `detector_draw` and `ray_merge_key` in
  `core/spatial_state.py`; `InitialState.detectors`;
  `SpatialNodeState.detector` and `detector_ticket`, installed by
  `SpatialEngine` when a marked Node is created.
- `SpatialNode.receive` draws once per arriving ray, unsalted
  (`next_ticket(state, 0)`, `ticket_draw`, bit 1 when
  `number x d < n x TICKET_MODULUS`), in Port then merge-key order, sets the
  ray's `detector` to 2 on 1 and 1 on 0, and records a `detector_click` event
  (position, tick, Port, family, amount, bit 1) on 1 only. In this slice the
  ray continues unchanged on both outcomes; the return is feature 3.
- The runner records `detector_mark: "detector-mark-v1"` in `run.json`
  beside `sampling_profile` and `ray_state`.
- The ticket rule keeps its signature (`next_ticket(state, salt)`); the mark
  passes salt 0 and no other caller exists. `stamp_event` still stamps every
  created ray with Detector bit 0.
- `DetectorMark` is a registered formula-free state record of the Node
  contract audit (`diagnostics/node_contract.py`, `STATE_RECORDS`): a
  position and three bounded integers, no law and no reading of any ray.

A document without `detectors` has no marked Node, calls the ticket rule
nowhere and runs exactly as before.

## Ray layers added on 2026-09-17 (`ray-layers-v1`)

Issue #169, feature 5, under [Highlights](HIGHLIGHTS.md) 5.1 and the
[ray-event model](RAY_EVENT_MODEL.md#6-migration-in-order): event spacetime
has layers, a layer is a set of families that couple, and a meeting exists
only inside a layer ([layers](SPATIAL_FIELDS.md#layers-ray-layers-v1)).

- `ray_layers` (`core/spatial_state.py`) derives the layers from the catalog
  as the connected components of the ray fields over the participants of the
  declared `ray_interactions`; a ray field that no rule selects is its own
  layer. `SpatialLaw` derives them once when it is built (`layers`) and
  `apply_ray_interactions` (`fields/ray_interactions.py`) meets the resident
  rays of a Node layer by layer: each layer's rules fire over that layer's
  rays alone, in declared order, and a ray of a layer without a firing rule
  crosses unchanged. Rules of different layers fire independently in one
  interval.
- The 32-slot participant capacity of `validate_ray_participants` is now a
  bound per layer with a rule (the `ray_slots` of that layer's fields sum to
  at most 32) instead of over every selected field.
- The runner records `ray_layers: "ray-layers-v1"` and `ray_layer_families`
  (the derived layers as sorted lists of field names) in `run.json` beside
  `ray_state`.
- A world with a single layer runs byte-identically to before: the same
  owners, rules, charges and events. No initialization key changes; no
  draw, absorber, readout or Detector is touched.

## Experiments register added on 2026-09-17

By the model owner's decision of 2026-09-17, the research runs of the
ray-event model are listed in one register,
[docs/EXPERIMENTS.md](EXPERIMENTS.md): section A, the confrontations with
known measurements in which the model can be falsified (A1 to A13); section
B, the demonstrations the manuscript needs (B1 to B12); section C, the order
in which the features of issue #169 unlock them; section D, what the register
replaces. Every entry names the features it needs, its run design and its
pass or fail criterion before the run, and runs once at one runtime source
fingerprint under [Highlights](HIGHLIGHTS.md) 5.5; none is a test of the test
suite. The register replaces the historical example worlds and study
directories removed the same day; their dated results stay in the
[validation log](VALIDATION.md) with their original scope. The
[documentation index](README.md) routes to the register and the
[hypotheses page](HYPOTHESES.md) points to it. No initialization key, API or
runtime behavior changes.
## Meeting of rays with N-to-M outputs added on 2026-09-17 (`ray-meeting-conversion-v1`)

Issue #169, feature 6, under [Highlights](HIGHLIGHTS.md) 3.15, 3.17, 3.26
and 5.1 and step 6 of the
[ray-event model](RAY_EVENT_MODEL.md#6-migration-in-order): a rule of
`ray_interactions` with declared `outputs` replaces its participants by one
to six new event rays at the meeting Node
([meetings with outputs](SPATIAL_FIELDS.md#meetings-with-outputs-ray-meeting-conversion-v1)).

- `convert_values` (`fields/disturbances.py`) is the arithmetic of the record
  conversion's `_convert_group` factored into one pure function over bounded
  integers (guard, outputs from the frozen inputs, table splits, conserved
  sums, invariant sums, returning the outputs and the remainder), used
  unchanged by the record path and by the meeting of rays.
- `InteractionDefinition.outputs` names spatial fields for a ray rule and
  `InteractionDefinition.splits` holds its `TableSplit` entries
  (`core/disturbance_state.py`); `_ray_meeting` (`initialization.py`)
  compiles each output's `field`, `amount`, `heading`, `phase`, `delay` and
  `input` to assignments and splits; `apply_ray_interactions`
  (`fields/ray_interactions.py`) removes the participants, stamps the outputs
  as the events of the meeting (`steps 0`, the mask and shares of the
  outputs' Ports) and checks every family's stock; `ray_layers` puts a rule's
  output fields in its layer; `validate_ray_participants` admits outputs and
  still rejects `output_types` and `k`.
- The momentum a split by a table moves between two Ports is booked by the
  spatial law as an explicitly accounted source of the momentum field until
  the field ray of feature 7 owns it as recoil; `source_totals` shows it.
- The runner records `ray_meeting: "ray-meeting-conversion-v1"` beside
  `ray_layers`.
- The ray path no longer needs `fields/record_operations.py` and
  `core/record_policy.py`: a meeting of rays converts without a resident
  record. Both stay for the record path until step 6 of issue #164 deletes
  them.
- Existing worlds with single-output rules run byte-identically. The
  native-ray coupling tests that asserted `outputs` are rejected now assert
  that the carrier output form (`{"type": ...}`) and malformed meeting outputs
  are rejected.

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
