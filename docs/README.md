# Documentation index

Start with [project status](PROJECT_STATUS.md) and the [repository entry point](../AGENTS.md).
Each document below owns one subject. Link to that owner instead of maintaining
another copy of its rules. A configured law, a research hypothesis and a measured
result are different claims. Revision-specific results are not a live status feed.

## Active implementation contracts

| Document | Responsibility |
| --- | --- |
| [Canonical terminology](TERMINOLOGY.md) | Node, NodeState, Scalar, Vector, Port, Link, Event and LocalRule vocabulary |
| [Physical reference units](REFERENCE_UNITS.md) | Shared constants, SI dimensions and bounded Scalar/Vector authoring with explicit encoding error |
| [Architecture](ARCHITECTURE.md) | Module ownership, state boundaries and dependency direction |
| [Local Focus](LOCAL_FOCUS.md) | Optional carrier scheduling, exact-equivalence scope, wake conditions and host memory |
| [Integer Node processor](NODE_VECTOR_PROCESSOR.md) | Opt-in rule durations, indexed interactions, aggregation and pre-commit readout guards |
| [Configuration validation](CONFIGURATION_VALIDATION.md) | Read-only preflight, format ownership, explicit dependencies, CLI reports and limits |
| [Disturbances](DISTURBANCES.md) | Active initialization schema, transport, expressions and transactions |
| [Spatial fields](SPATIAL_FIELDS.md) | Outward propagation, baselines, finite decay and field accounting |
| [Ray-event model](RAY_EVENT_MODEL.md) | Design candidate `ray-event-model-v1`: ray as an event trajectory carrying a phase and its step count, a meeting of rays as the only interaction, Detector as pass-or-return, carried pair bit, fields and matter as rays; adopted target direction of 2026-09-17, migration steps 2 ([ray state](SPATIAL_FIELDS.md#ray-state-ray-event-state-v1), `ray-event-state-v1`) and 3 ([Detector mark](DETECTOR_SAMPLING.md#the-detector-mark-detector-mark-v1), `detector-mark-v1`), the layers ([layers](SPATIAL_FIELDS.md#layers-ray-layers-v1), `ray-layers-v1`), the meeting with N-to-M outputs ([meetings with outputs](SPATIAL_FIELDS.md#meetings-with-outputs-ray-meeting-conversion-v1), `ray-meeting-conversion-v1`) and the wave-ray part of step 6 ([wave-ray families](SPATIAL_FIELDS.md#wave-ray-families-wave-ray-family-v1), `wave-ray-family-v1`) implemented, the rest not |
| [Binding as a loop](LOOP_BINDING.md) | Design of feature 14, `loop-binding-v1` (2026-09-17): a bound group as a periodic orbit of the ordinary meeting table on a ring of Nodes, the unit-square electron and its corner table in today's schema, the closure condition as integer equalities, dispersal, mass and clock, the field of a loop, the ladder count for A10, the motion of a loop, the interim forms it supersedes and what it removes; the ring worlds `examples/nature/ring.json` and `ring_open.json` with their pinned expectations |
| [Spatial computation delay](SPATIAL_COMPUTATION_DELAY.md) | Configurable shared field/carrier clock, fixed input buffers and integer departure timing |
| [Spatial couplings](SPATIAL_COUPLINGS.md) | Configured exchange, rotation, reaction budgets and self-interaction limits |
| [Shared complete-ray coupling](SHARED_RAY_COUPLING.md) | Candidate common ray participants, finite phase-sensitive residence/release and carried-heading readout |
| [Computational response](COMPUTATIONAL_RESPONSE.md) | Node-owned committed work readout and an explicit directional-response candidate |
| [Local field impulse](LOCAL_LORENTZ_FIELD.md) | Configured one-shot E/B pulse and read-only formula-free-state guard |
| [Local field rules](LOCAL_FIELD_RULES.md) | Six-port read views and joint field/carrier proposals |
| [Property couplings](PROPERTY_COUPLINGS.md) | Property eligibility, shared entity profiles and legacy selectors |
| [Local conservation](LOCAL_CONSERVATION.md) | Passive energy/momentum measurement across Node Events and Link flux |
| [Entity catalog](ENTITY_CATALOG.md) | Sourced physical properties and interactions, plus explicitly selected experiment profiles |
| [Local conversions](LOCAL_CONVERSIONS.md) | Atomic two-record replacement and declared balances |
| [Rational particle candidates](RATIONAL_PARTICLES.md) | Opt-in bounded ratios, balanced routes, fractional credit and local checks |
| [Coupled excitation probe](COUPLED_EXCITATIONS.md) | Unit-state exchange between a held internal excitation and a traveling field, with local capture and release |
| [Directional-wave candidate](DIRECTIONAL_WAVE.md) | Six transverse modes and configured conservative polarization encounters |
| [Physical entities](PHYSICAL_ENTITIES.md) | Inventory, representation coverage and unestablished physical behavior |

## Experiments and hypotheses

| Document | Responsibility |
| --- | --- |
| [Hypotheses under test](HYPOTHESES.md) | Questions the framework raises, kept apart from measured results: the lottery as the only door for outside information, living and inanimate as number sources, the size of the universe, what the sequence is, the derivation program, dark matter as a closed dimension, redshift without recession |
| [Problem solving](PROBLEM_SOLVING.md) | How the project advanced: one line per problem, its solution and who solved it (the model owner, Boss or a specialist), from the field's remainder to the law of the bit, with what is open |
| [Experiments register](EXPERIMENTS.md) | The research runs of the ray-event model, one entry each with its features, run design and criterion pinned before the run: confrontation with physics (two-slit Born intensities, Bell in phase form, Detector statistics, Coulomb, light bending and G_eff N², Newtonian attraction, hydrogen levels, neutron decay, the mass ladder, the wide phase, Malus and polarization Bell), proof for the paper, the order in which features unlock them, what it replaces, and the dated demonstrations of events (a photon absorbed by a bound electron, held and emitted, photofission with its control); runs made once at one fingerprint, never test-suite tests |
| [Catalog of nature](CATALOG.md) | `catalog/nature.json`, what exists on the board of the one engine, as data: the rays of nature (rest rate, charge, phase width, field and release; colour and polarization later) with their couplings, one table per meeting, and the apparatus (the Detector and the external body); `"undecided"` with the experiment or hypothesis that decides it; the ids each register entry uses |

The dated research studies of 2026-09-16 (`examples/research/`: Bell and
postulate 22, anomalies, ray form, entity audit, electron-photon scatter, ray
gallery), the named-particle gallery (`examples/gallery/`), the family
conversion (`examples/family-conversion/`) and isotropy (`examples/isotropy-probe/`)
experiments, and the other example worlds that no kept test loads were deleted
on 2026-09-17 with the test-suite reduction; see the
[migration note](MIGRATION.md#test-suite-reduced-on-2026-09-17-one-test-per-rule).
Their dated results stay in [validation](VALIDATION.md).

The Bell probes (`examples/kerengonen-bell/`, `examples/bell-chsh/`,
`examples/research/bell-postulate-22/`), the claim-and-gather and gathered-gravity
probes and the bond registry were deleted on 2026-09-17 under
[Highlights](HIGHLIGHTS.md) 3.18 (deleted), 3.19, 3.20, 5.1 and 5.4; see the
[migration note](MIGRATION.md#bond-registry-claim-gather-lottery-capture-and-occupied-links-guard-deleted-on-2026-09-17).
Their dated results stay in [validation](VALIDATION.md). The record operations
(records as owners: the merge of delivered records into a resident, and the
N-to-M conversion of records) were deleted the same day under
[Highlights](HIGHLIGHTS.md) 3.20 and 5.1 with bucket B.6, the last of issue
#164; see the
[migration note](MIGRATION.md#records-as-owners-deleted-on-2026-09-17).

The shared quantum resource, its integration layer and their twelve documents
(`QUANTUM_EVENTS.md`, `NATIVE_QUANTUM_EVENTS.md`, `WAVE_ORIGINS.md`,
`CAUSAL_QUANTUM_SOURCES.md`, `QUANTUM_CLASSICAL_COUPLING.md`,
`EVENT_GRAPH_CONFIGURATION.md`, `QUANTUM_ENTITIES.md`,
`LOCALIZED_QUANTUM_CONTACT.md`, `RECURRENT_QUANTUM_CONTACT.md`,
`QUANTUM_CONTACT_TRIAL.md`, `QUANTUM_FOCUS.md` and `QUANTUM_DETECTOR_TRIAL.md`)
were deleted on 2026-09-17 under [Highlights](HIGHLIGHTS.md) sections 3.18
(deleted), 3.19, 3.20 and 5.4; see the
[migration note](MIGRATION.md#shared-quantum-resource-and-integration-layer-deleted-on-2026-09-17).

## Operation, validation and change procedure

| Document | Responsibility |
| --- | --- |
| [Highlights specification](HIGHLIGHTS.md) | The Universe 24 Highlights specification, edited directly since 2026-09-17; the Google Doc is the historical source up to its revision of 2026-09-16 and is not edited or resynced |
| [Highlights coverage](HIGHLIGHTS_IMPLEMENTATION.md) | Dated implementation inventory and specification coverage, not a live status feed |
| [Recovery](RECOVERY.md) | Restore a checkout, environment and authorized operational procedures without chat history |
| [Project status](PROJECT_STATUS.md) | Restart map and implemented-versus-pending distinctions |
| [Workspace](WORKSPACE.md) | Local configuration UI, templates and recorded playback |
| [Ray viewer](../tools/ray_viewer/README.md) | 3D viewer and GIF renderer of a run record: rays on their Links with trails and hue by phase, faint field rays, event markers by shape, Detector marks, external bodies with their pictures and captions from the record, every look rule in `style.json`; a rendering of a fingerprinted record, not evidence |
| [Local observer](LOCAL_OBSERVER.md) | Completed Node receptions, cycle counter and local playback prefixes |
| [Retention](RETENTION.md) | Generated-output ownership, lifetime and cleanup |
| [Performance](PERFORMANCE.md) | Revision-specific host-time measurements and reproduction |
| [Test expectations](TEST_EXPECTATIONS.md) | Independent expected results and coverage ownership |
| [Validation evidence](VALIDATION.md) | Dated, source-identified check results; not timeless certification |
| [Migration](MIGRATION.md) | Public API transitions and internal path renames |
| [Physical features](PHYSICAL_FEATURES.md) | Contract and review procedure for a new physical hypothesis |

The root [postulates](../POSTULATES.md), [simulator definitions](../SIMULATOR_DEFINITIONS.md)
and [contribution procedure](../CONTRIBUTING.md) retain their authority. This index
routes readers; it does not duplicate their technical rules.

- [Detector-owned sampling](DETECTOR_SAMPLING.md): canonical fail-closed admission, the Node Detector mark (`detector-mark-v1`: one draw per arriving ray, the click on 1 only; `detector-absorb-v1`: the click absorbs a field quantum into the mark's counter) and the external exchange blockers that remain (the return).
