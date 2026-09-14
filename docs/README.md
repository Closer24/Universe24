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
| [Integer Node processor](NODE_VECTOR_PROCESSOR.md) | Opt-in rule durations, indexed interactions, aggregation and pre-commit readout guards |
| [Configuration validation](CONFIGURATION_VALIDATION.md) | Read-only preflight, format ownership, explicit dependencies, CLI reports and limits |
| [Event graph configuration](EVENT_GRAPH_CONFIGURATION.md) | Enable or disable the causal graph, distinguish quantum programs, set capacity and locate saved records |
| [Disturbances](DISTURBANCES.md) | Active initialization schema, transport, expressions and transactions |
| [Spatial fields](SPATIAL_FIELDS.md) | Outward propagation, baselines, finite decay and field accounting |
| [Spatial computation delay](SPATIAL_COMPUTATION_DELAY.md) | Configurable shared field/carrier clock, fixed input buffers and integer departure timing |
| [Spatial couplings](SPATIAL_COUPLINGS.md) | Configured exchange, rotation, reaction budgets and self-interaction limits |
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
| [Quantum and classical coupling](QUANTUM_CLASSICAL_COUPLING.md) | Claims, non-claims, measured evidence and related work for the hybrid model, written for external review |
| [Two-arm interference experiment](../examples/quantum/causal_interference.md) | Phase-dependent capture weights, classical emission carrying the interference term, which-path decoherence and the measured retarded-source gap |
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
