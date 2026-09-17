# API and repository migration

Install from the extracted project first:

```bash
python -m pip install -e '.[render,dev]'
```

## Ray-event audits on 2026-09-17 (`ray-event-audit-v1`)

Issue #169, feature 10 ([audits](SPATIAL_FIELDS.md#audits-ray-event-audit-v1),
[the world ledger](LOCAL_CONSERVATION.md#the-world-ledger-ray-event-audit-v1)):

- `Simulation.audit()` returns the world ledger at the current tick; the
  runner records one per completed tick under `audit` and
  `ray_event_audit: "ray-event-audit-v1"`, and `tools/ray_viewer/extract.py`
  carries `audit` in its `conservation` entry.
- `conserved_at_every_completed_tick` changed meaning: it is the ledger's
  identity, initial + sourced = current + escaped + annulled + absorbed, for
  amount, momentum and charge at every completed tick. It read false after
  an escape or an annulment before; escaped and annulled content are ledger
  lines, not losses, so an open world with escapes now reads true, and a
  dissipative world (schema 2) still reads false. Pins updated with a dated
  note: `test_inverse_split.py` (`annul`), `test_ray_viewer.py`,
  `test_ray_integration_guards.py`, `test_disturbance_application.py`
  ([expectations](TEST_EXPECTATIONS.md#ray-event-audit)).
- `charge_totals()` counts the stock a record holds of a charged family,
  the owners `totals()` reads, beside the rays; `escaped_charge_totals()` is
  a new readout, and the ledger's `absorbed` line is `external_body_totals()`
  (`external-body-v1`), with the bodies' own count, momentum, charge and
  sinks under `bodies`. The charge case of `test_wave_ray_families.py` reads
  the lamps' charge before the first tick.
- The local conservation audit measures charge as a fifth quantity when a
  family declares one, reported as `charge` beside `energy` and `momentum`;
  a world without a charged family reports as before. It reads every field
  release as a source at its Node and reports the sum as `sourced`, so a
  world with a `field_of` family may declare `conservation` (the viewer's
  world declares it again; its residual momentum (1, 0, 0) of 2026-09-17
  was the momentum of a single held ray's release, not a packet defect).
- A `ray_interactions` rule with outputs whose family's charge differs from
  the charge of the inputs its amount comes from is rejected at validation.

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
  (position, tick, Port, family, amount, bit 1) on 1 only. Until
  `detector-return-v1` (below) the ray continued unchanged on both outcomes.
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

## Detector return added on 2026-09-17 (`detector-return-v1`)

Issue #169, feature 3, the first half of migration step 4 of the
[ray-event model](RAY_EVENT_MODEL.md#6-migration-in-order) under
[Highlights](HIGHLIGHTS.md) 3.19, 3.20 and 5.4: a draw of 0 at a marked Node
returns the arriving ray, the same wave ray reversed on its line, unchanged,
walking back the number of steps it has made since its event
([the return](DETECTOR_SAMPLING.md#the-return-detector-return-v1),
[transport](SPATIAL_FIELDS.md#detector-return-detector-return-v1)).

- `return_ray(ray, definition)` and `DETECTOR_RETURN` in
  `core/spatial_state.py`: heading index replaced by the negated heading's
  index, `outbound` 0, accumulators, wait and interaction delay reset,
  amount, phase, steps, event record and family unchanged.
- `SpatialNode.receive`: a ray whose draw is 0 is returned in its arrival
  interval, records a `detector_return` event (position, tick, Port, family,
  amount) and no click, and is left out of the per-Port delivered readings;
  a ray that arrives already returning is not drawn for and not counted in
  those readings either. The `detector_click` list is what it was.
- A returning ray enters no coupling: `_absorb` leaves it untouched and
  takes the coherence over the outbound rays, `apply_ray_interactions` gives
  it no participant view, and the value and flux samples couplings read are
  taken over the outbound rays (`SpatialNode.coupling_rays`).
- `forward_rays` keeps a returning ray with `steps` 0 resident, inert, with
  its phase unchanged; `advance_ray` still refuses it a Link. A resident
  returned ray waits for the inverse split (feature 4).
- `ray_momentum` reads a ray with `outbound` 0 as amount times its heading
  negated, its share on the event's heading, so a return leaves the momentum
  total unchanged and every audit exact (issue #169: the Detector takes no
  recoil).
- `SpatialEngine._escape` refuses a packet holding a returning ray with a
  validation error: its event Node is not in the world.
- The runner records `detector_return: "detector-return-v1"` in `run.json`
  beside `detector_mark`.

Pinned consequences in existing tests: the four rays of
`test_detector_mark.py` that draw 0 now return to their lamps and rest there,
and the returning ray of `test_ray_hidden_state.py` is kept resident at
`steps` 0 instead of failing the forwarding ([expectations](TEST_EXPECTATIONS.md#node-detector-bit)).
A document without `detectors` has no returning ray and runs byte for byte
as before.

## Inverse split added on 2026-09-17 (`inverse-split-v1`)

Issue #169, feature 4, the second half of migration step 4 of the
[ray-event model](RAY_EVENT_MODEL.md#6-migration-in-order) under
[Highlights](HIGHLIGHTS.md) 3.20 and 5.4 and the model owner's decisions of
2026-09-17: a returned ray at its event Node performs the inverse split of
its own share by the world's `return_mode`
([the inverse split](DETECTOR_SAMPLING.md#the-inverse-split-inverse-split-v1),
[transport and bookkeeping](SPATIAL_FIELDS.md#inverse-split-inverse-split-v1)).

- The initialization key `return_mode` (`siblings`, the default, `straight`
  or `annul`; any other value rejected), `InitialState.return_mode`,
  `SpatialLaw.return_mode`, `RETURN_MODES` and `INVERSE_SPLIT` in
  `core/spatial_state.py`.
- `transmit`, `split_ports`, `split_amounts`, `event_port` and
  `port_heading` in `core/spatial_state.py`: the transmission as new event
  rays with the returned ray's phase, advance and Detector bit, the mask of
  the lines transmitted to and the amount per line, remainder by Highlights
  3.17.
- `SpatialLaw._inverse_split` and `_refund` in `fields/spatial_plan.py`,
  after absorption and before forwarding: the returned share restored to
  the event's input (a record with a funded emission rule into the field)
  and the transmission funded from it in the same interval, both booked in
  `transfer_delta`; with no input, the momentum booked in the source ledger;
  `annul` into `SpatialPlan.annulled`.
- `SpatialPlan.inverse_splits` and `annulled`, `InverseSplit`, the
  `inverse_split` event (position, tick, family, mode, ports, amounts,
  amount, bit, restored, annulled) published before the cycle's
  `spatial_cycle`, `SpatialAccounting.record_annulled`,
  `SpatialEngine.annulled`, the `annulled` entry of the spatial accounting,
  `annulled_totals()` on the engine, and the local conservation audit
  reading the annulled content of a Node into its residual and reporting
  `annulled`.
- The runner's conservation line: initial + sources = current + dissipated
  + escaped + annulled at every completed tick
  (`accounting_balanced_at_every_completed_tick`), `annulled_totals`,
  `inverse_split: "inverse-split-v1"` and `return_mode` in `run.json`.

Pinned consequences in existing tests: the returned ray of
`test_detector_return.py` (a one-line event) is restored to its lamp and
emitted again by it, and the four returned rays of `test_detector_mark.py`
are restored to their lamps, which then hold their share with its recoil
undone, that test running three ticks
([expectations](TEST_EXPECTATIONS.md#inverse-split)). A world without a mark
has no returned ray and runs byte for byte as before.
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

## Test suite reduced on 2026-09-17: one test per rule

Decision of the model owner, 2026-09-17: the engine is generic, so the test
suite keeps one module per generic rule, each exercising that rule in isolation
on a minimal board, and one module per feature of the
[ray-event model](RAY_EVENT_MODEL.md) (issue #169); modules that pin the numbers
of an example world, combine several rules to reach a pinned number, duplicate a
kept rule under another world, or exist for a study, a gallery, a probe, a
comparison of worlds, rendering or playback were deleted, and so were the dated
research studies and every `examples/` directory that no kept test loads and
`tools/check.py` does not need. Before: 108 modules, 2,194 tests (2,191 passed,
3 visual-only skipped) in 622 seconds single-process on the recording host
(about 15 minutes in CI). After: 40 modules with `test_detector_mark.py` of
the merged PR #186, 1,009 tests, 35 seconds on the same host. The kept
modules and the rule each isolates are the
[suite inventory](TEST_EXPECTATIONS.md#suite-inventory-of-2026-09-17).

Deleted test modules (69):

- world-specific probes and studies:
  `test_atomic_interactions.py`, `test_computational_response.py`,
  `test_coupled_excitations.py`, `test_de_broglie.py`,
  `test_directional_wave.py`, `test_euclidean_pace.py`,
  `test_family_conversion.py`, `test_generic_identity.py`,
  `test_gravity_probe.py`, `test_inverse_square_experiments.py`,
  `test_isotropy_probe.py`, `test_kerengonen_mirror.py`,
  `test_local_lorentz_field.py`, `test_lorentz_response_physics.py`,
  `test_matter_wave.py`, `test_maxwell_configuration.py`,
  `test_particle_gallery.py`, `test_particle_interactions.py`,
  `test_radiation_scattering.py`, `test_ray_heading_flux.py`,
  `test_redshift_sweep.py`, `test_reference_examples.py`,
  `test_small_space_experiments.py`;
- computational curvature and self-field scenarios:
  `test_arrival_port_blind.py`, `test_carried_allocation_phase.py`,
  `test_computation_field_delay.py`, `test_delay_direction.py`,
  `test_field_phase_first.py`, `test_least_delay_routing.py`,
  `test_node_work_emission.py`, `test_rotation_self_interaction.py`;
- catalog and profile data:
  `test_entity_catalog.py`, `test_entity_compiler.py`,
  `test_physical_entities.py`, `test_profile_validation.py`,
  `test_property_couplings.py`, `test_property_entity_profiles.py`,
  `test_reference_units.py`;
- duplicates of a kept rule:
  `test_active_node_contracts.py`, `test_active_ports.py`,
  `test_dissipative_initialization.py`, `test_emission_residuals.py`,
  `test_exchange_residuals.py`, `test_field_commit_guards.py`,
  `test_finite_spatial_engine.py`, `test_generic_vector_lab.py`,
  `test_interaction_spatial_integration.py`, `test_joint_node_reactions.py`,
  `test_joint_reaction_configuration.py`,
  `test_node_conservation_configuration.py`, `test_node_guard_boundaries.py`,
  `test_node_runtime.py`, `test_node_terminology.py`,
  `test_node_vector_examples.py`, `test_node_vector_integration.py`,
  `test_open_boundaries.py`, `test_parallel_node_execution.py`,
  `test_spatial_computation_delay.py`, `test_spatial_coupling_budget.py`,
  `test_spatial_engine.py`, `test_spatial_scheduling.py`,
  `test_spatial_seed_bounds.py`, `test_zero_carrier.py`;
- observer, playback, workspace and visualization:
  `test_local_observer.py`, `test_observer_playback.py`,
  `test_recorded_movie.py`, `test_workspace.py`,
  `test_workspace_integration.py`, `test_workspace_retention.py`.

The helper `tests/support/identity.py` went with `test_generic_identity.py`.
Deleted example directories (20), with their READMEs, configurations, scripts
and recorded results: `examples/charged-pair/`, `examples/collisions/`, `examples/computational-curvature/`, `examples/computational-response/`, `examples/de-broglie/`, `examples/euclidean-pace/`, `examples/family-conversion/`, `examples/gallery/`, `examples/gravity-probe/`, `examples/inverse-square/`, `examples/isotropy-probe/`, `examples/kerengonen-mirror/`, `examples/matter-wave/`, `examples/maxwell/`, `examples/observer/`, `examples/particle-interactions/`, `examples/radiation-scattering/`, `examples/relativity-probes/`, `examples/research/`, `examples/small-space/`.
The six research studies of 2026-09-16 under `examples/research/` (Bell and
postulate 22, already deleted with bucket B.5; anomalies; ray form; entity
audit; electron-photon scatter; ray gallery) are among them. Links to the
deleted paths in the documents became plain text with this date; the
hypotheses they informed stay stated in [HYPOTHESES.md](HYPOTHESES.md) and
their dated results in [VALIDATION.md](VALIDATION.md).

`tools/check.py` `RESOURCE_CONSUMERS` lost the rows of deleted examples and of
deleted consumers, except the rows that `tests/test_check_scope.py` (edited on
a running branch, left untouched) asserts: those rows still name
`test_ray_heading_flux.py`, `test_local_lorentz_field.py`,
`test_directional_wave.py`, `test_coupled_excitations.py`,
`test_property_entity_profiles.py`, `test_entity_catalog.py`,
`test_entity_compiler.py`, `test_physical_entities.py`,
`test_profile_validation.py`, `test_small_space_experiments.py`,
`test_reference_examples.py` and `test_generic_identity.py`, and the selector
still names `test_generic_vector_lab.py`, `test_workspace.py` and
`test_recorded_movie.py`; `main()` skips a selected test that does not exist.
The examples those rows name (`examples/directional-wave/`,
`examples/coupled-excitations/`, `examples/known-entities/`,
`examples/generic-ray-coupling/field-sampling.json` and the root example
inputs) stay for that reason and for the kept tests that load them (the rows
and `field-sampling.json` went with bucket B.6 later the same day, see
[records as owners deleted](#records-as-owners-deleted-on-2026-09-17)). The
modules of running feature branches (`test_energy_audit.py`,
`test_kerengonen.py`, `test_ray_integration_guards.py`,
`test_native_ray_coupling.py`, `test_ray_merge_contracts.py`,
`test_plan_reuse.py`, `test_ray_coupling_evidence.py`,
`test_detector_sampling_contract.py`, `test_check_scope.py`) were left as they
were; `test_ray_delay.py` and `test_local_focus.py` stay as their import
dependencies and as the output-clock and Local Focus modules. There is no
replacement: a rule that needs a new check gets one focused module.

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
- With `wave-ray-family-v1` every output carries its field's `family` and
  `charge`, and a meeting's appended `charge` invariant is the per-ray readout
  `charge x amount` summed over its inputs and over its outputs.
- The runner records `ray_meeting: "ray-meeting-conversion-v1"` beside
  `ray_layers`.
- The ray path no longer needs `fields/record_operations.py` and
  `core/record_policy.py`: a meeting of rays converts without a resident
  record. Both stayed for the record path until step 6 of issue #164 (bucket
  B.6) deleted them the same day, see
  [records as owners deleted](#records-as-owners-deleted-on-2026-09-17).
- Existing worlds with single-output rules run byte-identically. The
  native-ray coupling tests that asserted `outputs` are rejected now assert
  that the carrier output form (`{"type": ...}`) and malformed meeting outputs
  are rejected.
## Wave-ray families added on 2026-09-17 (`wave-ray-family-v1`)

Issue #169, feature 9, the wave-ray part of
[ray-event model](RAY_EVENT_MODEL.md#6-migration-in-order) migration step 6
under [Highlights](HIGHLIGHTS.md) 3.3 and 5.1: every ray is a wave ray, a
plain ray the special case with rest rate 0, light a family with rest rate 0
that carries its emitter's phase unchanged, and the phase the one value with
its own declared width
([wave-ray families](SPATIAL_FIELDS.md#wave-ray-families-wave-ray-family-v1)).

- `spatial_fields[i]` (ray transport) admits `phase_bits` (the phase width;
  default 0, or log2 of `kerengonen.phase_steps`) and `charge` (per quantum,
  default 0). In the `kerengonen` object `phase_advance` (the rest rate) is
  required and `phase_steps` (the coherence table) optional; `phase_steps`
  must be a power of two (every existing world's is: 4, 8, 64), and
  `phase_advance` is bounded by the width, not by `MAX_VALUE`.
- `SpatialFieldDefinition` (`core/spatial_state.py`) gains `phase_bits`,
  `charge` and the properties `coherent`, `phase_modulus` and `phase_mask`;
  `kerengonen` now means a declared phase rule (a table or a nonzero rate);
  `advance_ray(ray, heading, phase_modulus, phase_advance)` takes the modulus,
  a power of two (a Kerengonen world's `phase_steps`), and masks; `phase_mask`,
  `ray_charge`, `charge_invariant`, `RAY_WRITABLE`, `RAY_VIEW_COMPONENTS`,
  `CHARGE_INVARIANT`, `WAVE_RAY_FAMILY`, `MAX_TABLE_BITS` and
  `MAX_STORED_PHASE_BITS` are added. Every `% phase_steps` in the engine became
  a mask.
- `RAY_PROPERTIES` gains read-only `family` and `charge`; a ray interaction's
  view reads nine components per participant (`read` cost 9 instead of 7), and
  the parser appends the `charge` invariant to every `ray_interactions` rule.
  `Simulation.charge_totals()` reads `charge x amount` per ray field.
- `kerengonen_phase` on an emission requires a ray field of sufficient width,
  not the `kerengonen` key (a plain field without a width admits phase 0
  only); a carried phase and `kerengonen_mirror` require the coherence table;
  `ray_phase_per_tick` and `hold_rays` follow the declared phase rule.
- Not admitted in this slice: `self_exclusion` or `ray_interactions` on a
  family wider than 30 bits, a coherence table wider than 12 bits
  (`phase_steps` above 4096), and a non-power-of-two `phase_steps` in a field
  definition (the table builders `phase_cosines` and `phase_sines` still take
  any count from 2 to 4096).
- The runner records `wave_ray: "wave-ray-family-v1"` beside `ray_state`.

Existing worlds run unchanged: a plain field has width 0 and rate 0, a
Kerengonen field the width of its `phase_steps`; the metered `read` cost of a
ray interaction is the one recorded difference. Tests adapted:
`test_kerengonen.py` (a nonzero phase before the plain-field rejection) and
`test_ray_integration_guards.py` (odd table sizes through the builders, 32
phase steps in the table-construction guard).

## Fixed body renamed external body on 2026-09-17

Fixed body renamed external body, 2026-09-17, same specification extended.
By the model owner's statement of that day, the declared element named
"fixed body" earlier the same day is the external body: a Node declared to
hold a family with an amount, if wanted a charge, and an initial momentum
(`initial_momentum`, in place of the declared trajectory of the first
statement: its motion is caused by fields only, model owner, 2026-09-17),
standing for a star, a neutron star, a fixed proton, a large charge or a
piece of apparatus; it radiates by the one field rule, does not spread and
is not pushed by matter. [Highlights](HIGHLIGHTS.md) 3.19 is the only authoritative
text; the [postulates](../POSTULATES.md) section 23, the
[ray-event model](RAY_EVENT_MODEL.md#1-definitions) section 1 and its
migration step 7b (`external-body-v1`, after feature 7), the
[experiments register](EXPERIMENTS.md) (A1, A2, A3, A6, A8, A12, A13 and
section C), the [terminology](TERMINOLOGY.md) (External body, Apparatus)
and section 14 of the [hypotheses page](HYPOTHESES.md) restate it. What the
extension adds: the amount is finite and of any width, since it enters no
sum; absorption into an explicitly accounted sink is the default coupling of
the body's family and the other couplings make the apparatus (a reversed
heading a mirror, a split by a declared table a beam splitter, a phase
offset a phase plate, a polarization read a polarizer once feature 11
exists; a wall, a screen and a beam stop the default); on the Node the body
is bounded metadata like the Detector mark, with one exact counter, the
sink totals per family; and where the back-reaction is wanted an ordinary
bound group with a large amount is declared instead. No initialization key,
API or runtime behavior changes; `external-body-v1` is not yet in the code.
## Ray viewer added on 2026-09-17 (`tools/ray_viewer/`)

The model owner's visualization requirement of 2026-09-17 (issue #169) is
implemented as a repository tool, ready before feature 7 lands: a Renderer
under [Highlights](HIGHLIGHTS.md) 3.29 and 3.30 that reads the runner's
record and never the engine ([ray viewer](../tools/ray_viewer/README.md)).

- `tools/ray_viewer/extract.py` turns one or more records (`run.json`,
  `events.jsonl`, `initialization.json`, an optional `ray-recording.json`)
  into `runs.json` (`ray-viewer-runs-v1`): rays chained from the Link
  transits with their trails, every event as a marker with its Ports, and
  a caption per tick with the coupling, the invariants and the totals from
  the record; an event kind it does not know becomes a generic marker.
- `tools/ray_viewer/viewer.html` is the self-contained page (Three.js r128
  from cdnjs): dark, rays as segments with arrowheads and trails, hue by
  phase, field rays faint, markers that stay, Detector marks with their
  bits, lattice, axes and bounding box, a tick slider, play, a rotation
  toggle and a run selector.
- `tools/ray_viewer/render_gif.py` renders a GIF and a contact sheet with
  Playwright, headless Chromium and Pillow; `playwright` joins the `render`
  extra in `pyproject.toml`.
- `tests/test_ray_viewer.py` pins the extraction of a two-lamp, six-tick
  world ([expectations](TEST_EXPECTATIONS.md#ray-viewer-extraction));
  `tools/check.py` selects it for any change under `tools/ray_viewer/`.

No engine, schema or record change. The prototype under the session
scratchpad (`gif-electrons-3d`) is superseded by the tool.

## Binding and gravity by delay added on 2026-09-17 (`ray-binding-v1`)

Issue #169, feature 8 ([binding](SPATIAL_FIELDS.md#binding-and-gravity-by-delay-ray-binding-v1);
Highlights 3.4 and 3.28). A `ray_interactions` rule without outputs whose
assignments set `delay` 1 binds its participants as a bound group: the rays
stay at the Node, the rule fires again every interval (the group's tick,
published as the `bound_tick` record), each phase advances once per interval
by its rest rate, and a held ray releases its field on all six headings. An
earlier declared outputs rule naming a bound participant and an arriving ray
unbinds the group. New keys: `ray_delay` on a binding rule, the Node's
output-clock delay while it holds the group (every arrival of matter waits
it, a field ray never, one Node-wide wait for the six per-face clocks), and
a meeting output's `delay`
as `{"of": i, "table": [six], "per": u}`, a delay per the Port input i came
through, carried as the ray's new `lag` field (three signed integers, part
of the merge key, reset by a return) and spent one Link toward the lagging
side per phase modulus: gravity as bending by delay. New registers:
`SpatialPlan.bound_delay`, `SpatialNodeState.bound_delay`; the snapshot lists
`bound_groups`; the runner records `ray_binding: "ray-binding-v1"`.
`test_ray_binding.py` pins the acceptance criterion G_eff x N^2 = 64 over
N = 2^8, 2^10, 2^12, 2^16. Worlds without a binding rule, a `ray_delay` or a
delay table run byte-identically.

## Field as the ray's information added on 2026-09-17 (`released-field-v1`)

Issue #169, feature 7, under [Highlights](HIGHLIGHTS.md) 3.5, 3.14, 3.15,
3.17 and 3.28 and step 7 of the
[ray-event model](RAY_EVENT_MODEL.md#6-migration-in-order): a ray field
declared with `field_of` and `release` is the field of that family, released
at every Node a ray of the family crosses
([released field](SPATIAL_FIELDS.md#field-as-the-rays-information-released-field-v1)).

- `SpatialFieldDefinition.field_of`, `release_numerator` and
  `release_denominator` (`core/spatial_state.py`) carry the declaration;
  `_spatial_fields` (`initialization.py`) parses `field_of` (a family name,
  resolved once every spatial field is parsed) and `release` (`[n, d]`,
  `1 <= n <= d`), declared together; `validate_released_fields` and
  `validate_released_field_admission` admit a world at `SpatialLaw` and
  `InitialState`.
- `release_field` and `release_stock` (`core/spatial_state.py`) are the pure
  release: one ray per Port heading except the source ray's own (all six for
  resident content), amount `floor(amount x n / d)` with the fraction not
  released, the source's phase, no event stamp. `SpatialLaw._release`
  (`fields/spatial_plan.py`) calls them after the interval's emissions, adds
  the rays to the departures and books their amount, and their momentum when
  a momentum field is bound, as an explicitly accounted source. A Node whose
  record holds stock of a source family runs its cycle every interval
  (`holds_source_stock`, `core/spatial_node.py`, `core/spatial_engine.py`).
- The recoil is the declared rule: a `ray_interactions` rule with outputs that
  returns the field ray with heading `"reversed"`. No engine mechanism was
  added for it.
- The runner records `released_field: "released-field-v1"` and
  `released_fields` beside `ray_meeting`.
- Existing worlds without `field_of` run byte-identically; their run record
  carries `released_fields: []`.

## External body added on 2026-09-17 (`external-body-v1`)

Issue #169, feature 7b, Highlights 3.19 (model owner, 2026-09-17; the
"fixed body" of earlier that day): the world key `external_bodies` declares
the second apparatus element beside the Detector mark, a Node holding a
family with an amount of any width, a charge, a phase, an initial momentum
(heading and pace), a coupling (`"sink"` or a declared ray interaction) and
a momentum table ([external
body](SPATIAL_FIELDS.md#the-external-body-external-body-v1)).

- `ExternalBody` in `core/spatial_state.py` (position, family, amount,
  charge, field, coupling, phase, signs, momentum, accumulators, sink), with
  `body_release`, `body_absorb`, `body_step`, `body_token`,
  `body_coupled_families`, `validate_external_bodies` and
  `external_body_names`; `InitialState.external_bodies`;
  `SpatialNodeState.body`, `SpatialPlan.body` and `body_port`,
  `SpatialPacket.body`; the record type registered in `STATE_RECORDS`.
- `core/spatial_node.py`: a body Node stays active; the body's cycle
  (`_body_cycle`) strips a coupled body's token, releases its field on six
  headings booked as a source and steps it by its accumulators; arrivals at
  a body are met by its coupling (`_body_meet`), the sink by default; the
  new records `external_body_absorbed` and `external_body_step`.
- The audit: `SpatialAccounting.record_absorbed`, the engine's
  `absorbed_by_bodies` line, `external_body_totals()`, `external_bodies()`
  and `external_body_momentum()` on the engine; the runner's conservation
  line gains `+ absorbed_by_bodies` and the run record `external_body`,
  `external_bodies` (with positions per tick), `external_body_totals` and
  `external_body_momentum`; a body cannot leave an open world.
- Worlds without `external_bodies` are byte-identical. New test module
  `tests/test_external_body.py` (sink, stars, uniform, mirror, rejected),
  pinned in [TEST_EXPECTATIONS.md](TEST_EXPECTATIONS.md#external-body).

## Records as owners deleted on 2026-09-17

Issue #164 bucket B.6, the last deletion bucket, following
[HIGHLIGHTS.md](HIGHLIGHTS.md) sections 3.20 (all the information is on the
rays; the origin Node keeps nothing and there is no register) and 5.1 (no
occupied channel and no capacity rule) and row R1 and migration step 6 of
[RAY_EVENT_MODEL.md](RAY_EVENT_MODEL.md): an interaction is a property of the
meeting of rays, and since `ray-meeting-conversion-v1` the N-to-M arithmetic
lives at the meeting (`convert_values`), not on a resident record.

- `fields/record_operations.py` (`RecordOperations`, 139 lines),
  `core/record_policy.py` (`RecordPolicy`, 25 lines) and
  `tests/test_record_operations.py` (19 tests, 177 lines) are gone.
  `DisturbanceEngine` no longer takes `record_policy=`; `NodeServices` carries
  `spatial_types` (the carrier types a spatial coupling or interaction selects)
  in its place, and `disturbance_api.Simulation` composes nothing for it.
- A delivered record takes the first spare slot outside the pending lock and
  nothing is folded into a resident: the merge of split arrivals of one type
  and channel by summing their values (records as owners) is deleted. The
  receiving-capacity failure is unchanged ("local receiving capacity
  exhausted; no disturbance was discarded"): a bounded-state error, not a rule
  that makes anything wait. The activity predicate and the cost reporter moved
  unchanged into `core/disturbance_node.py` as the pure functions
  `carrier_work` and `report_cost` over the immutable run definition, so a
  world in which no two arrivals of one type and channel reach one Node in one
  tick runs byte-identically.
- The N-to-M conversion of records is gone: `_convert_group` and the
  `outputs` branch of `DisturbanceLaw.__call__` (`fields/disturbances.py`),
  `_conversion_interaction` (`initialization.py`) and the one-role admission
  of `core/coupling_selectors.py` (a group has two to six roles). An
  `interactions` entry with `outputs` is rejected with a dated message;
  `outputs` in `ray_interactions` is unchanged and `convert_values` stays as
  the arithmetic of the meeting. The two-to-two `output_types` rule of
  [local conversions](LOCAL_CONVERSIONS.md) is unchanged.
- The carrier commit's guard "outgoing links still occupied; no implicit
  packet queue is allowed" (`core/disturbance_node.py`) is gone, as the
  spatial pre-planning refusal went with bucket B.5.
- `tools/check.py` `RESOURCE_CONSUMERS` lost the rows of the consumers
  deleted with the test-suite reduction (`test_ray_heading_flux.py`,
  `test_property_entity_profiles.py`, `test_coupled_excitations.py`,
  `test_directional_wave.py`, `test_local_lorentz_field.py`,
  `test_entity_catalog.py`, `test_profile_validation.py`,
  `test_entity_compiler.py`, `test_physical_entities.py`,
  `test_small_space_experiments.py`, `test_reference_examples.py`,
  `test_generic_identity.py`) and the selector names
  `test_generic_vector_lab.py`, `test_workspace.py` and
  `test_recorded_movie.py`; every remaining row names a kept test, which
  `tests/test_check_scope.py` (27 tests, from 47) now asserts.
  `examples/generic-ray-coupling/field-sampling.json`, kept only for that
  table, is gone; `examples/directional-wave/`, `examples/coupled-excitations/`
  and `examples/known-entities/` stay because kept tests
  (`test_configuration_validation.py`, `test_local_conversions.py`) and
  documented tools load them.

There is no replacement API. Every deletion bucket of issue #164 is done.

## Ray viewer: releases, fields, style file and sidecar, 2026-09-17

The first render of a feature 7 run and the model owner's reading of the
page on a phone (2026-09-17) changed what the [ray viewer](../tools/ray_viewer/README.md)
draws; the record is unchanged.

- `extract.py` resolves rays per family: a field family (`field_of`) passes
  Nodes in silence, leaves a Node with a departing matter ray as a `release`
  (its own event kind, flagged `field`, never a marker or a caption line, the
  source ray's trail unbroken), and makes a meeting only where it leaves a
  Node changed; escapes and field-only events carry a `field` flag; a body's
  `external_body_absorbed` ends the rays it took; the per-tick `in_world`
  figure now adds the sources recorded by `spatial_cycle` through the
  previous tick, which equals a recording's totals tick by tick (the earlier
  figure ignored sources and could fall below the amount on the Links);
  captions list only meetings, Detector events and inverse splits, at most
  three per tick, then the escapes once; `--sidecar` names a recording per
  record, and a recording whose fingerprints differ from the run's is refused;
  `external_bodies` are read from `run.json` with their `positions` per tick.
- `viewer.html` draws no text on the board except one `family amount` label
  per matter ray, placed only where it is at least 24 px from every other
  label and overlaps none; rays about 4 px wide with a 10 px arrowhead and a
  trail fading over six Links; event kinds by marker shape and colour with a
  legend under the canvas; matter escapes as a dot, field escapes as
  nothing; sources, Detector marks and external bodies as shapes without
  text, a body's picture chosen by family and moving with its recorded
  position; captions clamped to two lines at phone width.
- `style.json` (`ray-viewer-style-v1`) holds every colour, size, drawing,
  caption and motion rule, by the model owner's decision that a change of
  look is a file edit and a re-render; the page inlines or fetches it,
  `render_gif.py --style` inlines it and takes its defaults from it.
- `record_sidecar.py` writes `ray-recording.json` beside a record by
  replaying it on the run's own source tree, refusing any other.
- `tests/test_ray_viewer.py` pins the widened world (a released field, the
  body positions and the style file); the fixture no longer declares a
  `conservation` block, because the local audit failed on a field ray at a
  lamp Node (reported, not worked around), and its pins record that the
  engine released from two rays held by a coupling in the interval they were
  held, which the released-field text does not say (reported to feature 7).

## Ray viewer: clear matter lines, textless autoplay page, 2026-09-17

Model owner's feedback on the second render, applied as defaults of
`tools/ray_viewer/style.json` so that no change of look needs a code change
([ray viewer](../tools/ray_viewer/README.md)); the record is unchanged.

- `sizes.trail_links` 0 means the whole path since the ray's event; the
  default is 10 with `trail_fade` [1.0, 0.0]: the ray bright at its Link
  and a trail as wide (6 px) fading smoothly to nothing over ten Links, one
  opacity per Link, so the path reads without a hard cut; matter families
  have a fixed high-contrast colour (`colors.families.default`, `electron`
  as the example override) and `draw.hue_by_phase` (`arrowhead`, `ray` or
  `none`) says where the phase hue shows; field rays stay faint.
- `draw.page_text` holds one boolean per block of text around the board
  (`header`, `record`, `legend`, `captions`, `totals`, `tick_counter`,
  `controls`); by default only `header` (one line, the run's title from the
  record) and `tick_counter` are on, and the ray labels (`draw.labels.rays`)
  are off, so the published page shows the board with its title and tick
  and nothing else that reads as text; markers keep their shapes.
- `motion.autoplay` and `motion.loop`, both true by default: playback starts
  on load with the slow rotation and wraps at the end; the space key pauses
  and resumes, undocumented on the page.
- `render_gif.py` validates the new keys; the page's built-in default stays
  equal to the file, checked by `tests/test_ray_viewer.py`, which pins these
  defaults.

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
