# Documentation index

The [spatial momentum and position-output experiment](../examples/quantum/position_moment_response.md)
distinguishes evolved wave readouts, locally derived capture moments and missing
gate/measurement energy closure.

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
| [Event graph configuration](EVENT_GRAPH_CONFIGURATION.md) | Enable or disable the causal graph, distinguish quantum programs, set capacity and locate saved records |
| [Disturbances](DISTURBANCES.md) | Active initialization schema, transport, expressions and transactions |
| [Spatial fields](SPATIAL_FIELDS.md) | Outward propagation, baselines, finite decay and field accounting |
| [Ray-event model](RAY_EVENT_MODEL.md) | Design candidate `ray-event-model-v1`: ray as an event trajectory, break as the only interaction, Detector as pass-or-return, carried pair number, fields and matter as rays; not implemented |
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

## Explicit quantum experiments

The [catalog contact example](../examples/catalog-contact/README.md) connects
established particle references to the existing causal source/contact mechanism.

| Document | Responsibility |
| --- | --- |
| [Native event programs](NATIVE_QUANTUM_EVENTS.md) | Shared causal ledger, optional quantum composition, repeated triggers and charged mechanical paths |
| [Quantum entities](QUANTUM_ENTITIES.md) | Quantum entity definitions and native integration ownership |
| [Quantum events](QUANTUM_EVENTS.md) | Selected deferred joint-state event backend and decision semantics |
| [Quantum origin cells](WAVE_ORIGINS.md) | Six local origin references, atomic terminal decisions and next-tick local invalidation in event spacetime |
| [Localized quantum contacts](LOCALIZED_QUANTUM_CONTACT.md) | Commit-time inventory transfer, finite localized field sources and repeating coherent propagation |
| [Causal quantum sources](CAUSAL_QUANTUM_SOURCES.md) | Locally retained complex source envelopes, finite weighted ordinary emission and Link-delivered termination |
| [Recurrent quantum contacts](RECURRENT_QUANTUM_CONTACT.md) | Configured outcome instruments, atomic new origins and finite isolated source generations |
| [Repeated-contact experiment](../examples/quantum/repeated_contacts.md) | Reproducible local continuations, fresh origins, final localization and finite field decay |
| [Quantum-to-classical investigation](../examples/quantum/quantum_classical_check.md) | Exact interference suppression/reversal, classical probabilities and the unestablished trajectory limit |
| [Local moment-response candidate](../examples/quantum/local_moment_exchange.md) | Post-capture mean/variance exchange, finite detector lifecycle and slow ordinary transport |
| [Quantum and classical coupling](QUANTUM_CLASSICAL_COUPLING.md) | Claims, non-claims, measured evidence and related work for the hybrid model, written for external review |
| [Hypotheses under test](HYPOTHESES.md) | Questions the framework raises, kept apart from measured results: the lottery as the only door for outside information, living and inanimate as number sources, the size of the universe, what the sequence is, the derivation program, dark matter as a closed dimension, redshift without recession |
| [Research explorations of 2026-09-16](../examples/research/README.md) | Six dated exploration studies (Bell and postulate 22, anomalies, ray form, entity audit, electron-photon scatter, ray gallery) with pre-registered expectations, scripts and recorded results at one fingerprint; evidence, not integrated behavior or proof of physics |
| [Two-arm interference experiment](../examples/quantum/causal_interference.md) | Phase-dependent capture weights, classical emission carrying the interference term, which-path decoherence and the measured retarded-source gap |
| [Crossing null notices](../examples/quantum/crossing_nulls.md) | Two nulls before either notice arrives: the stale product, the local correction by the later Node and the exact conditional scale after Link transit |
| [Two-wing Bell test](../examples/quantum/bell_chsh.md) | CHSH 14/5 from two separated lattice wings on the canonical runner, seeded coincidence counts, no-signalling marginals and a dephased control at 6/5 |
| [Named-particle gallery](../examples/gallery/README.md) | Electron-positron elastic contact, catalog electron/positron contact fields, and configured annihilation, muon-pair and beta-decay conversions, rendered from recorded runs with names, charges and masses |
| [Family conversion](../examples/family-conversion/README.md) | Generic N-to-M conversion between catalog families: electron-positron annihilation into two or three photons, a four-ray joint conversion, threshold two-photon pair production with a crossing control, and a Compton-like exchange as supplied integer laws in catalog keV units, with exact accounting up to 10 GeV on a 48-cubed board |
| [Isotropy probe](../examples/isotropy-probe/README.md) | Directional ratio of the outward and straight-ray fields against the isotropic expectation: exact path counts, counting spread and the heading cost of isotropy |
| [Bell test on the phased-ray field](../examples/kerengonen-bell/README.md) | CHSH on the classical Kerengonen candidate: 1.40 exact against the quantum owner's 14/5 at the same settings, plain field at the bound of 2 |
| [Many-contact experiment](../examples/quantum/many_contacts.md) | Six simultaneous domains, 200 seeded repetitions, recorded captures and the one-shot limit |
| [Quantum focus](QUANTUM_FOCUS.md) | Optional hierarchical candidate selection, not a default physical law |
| [Quantum contact trial](QUANTUM_CONTACT_TRIAL.md) | Bounded one-contact composition with the active disturbance engine |
| [Quantum detector trial](QUANTUM_DETECTOR_TRIAL.md) | Historical opt-in detector/controller experiment |

## Historical particle candidates

These named APIs remain testable; none is the implicit active `Simulation`.
Historical documents may quote legacy identifiers that predate the canonical
Node vocabulary; those names are compatibility references, not separate physical
concepts.

| Document | Responsibility |
| --- | --- |
| [Scalar fields](SCALAR_FIELDS.md) | Historical scalar field composition and turning policies |
| [Balanced motion](BALANCED_MOTION.md) | Digital movement and local halo candidate, including its limits |
| [Causal-stream field](CAUSAL_STREAM_FIELD.md) | Outward stream candidate and pre-wrap isolation result |

## Operation, validation and change procedure

| Document | Responsibility |
| --- | --- |
| [Highlights snapshot](HIGHLIGHTS.md) | Dated verbatim copy of the Universe 24 Highlights specification; the live Google Doc stays authoritative |
| [Highlights coverage](HIGHLIGHTS_IMPLEMENTATION.md) | Dated implementation inventory and specification coverage, not a live status feed |
| [Recovery](RECOVERY.md) | Restore a checkout, environment and authorized operational procedures without chat history |
| [Project status](PROJECT_STATUS.md) | Restart map and implemented-versus-pending distinctions |
| [Workspace](WORKSPACE.md) | Local configuration UI, templates and recorded playback |
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

- [Detector-owned sampling](DETECTOR_SAMPLING.md): canonical fail-closed admission, explicit historical research profiles and external exchange blockers.
