# Documentation index

Start with [project status](PROJECT_STATUS.md) and the [repository entry point](../AGENTS.md).
Each document below owns one subject. Link to that owner instead of maintaining
another copy of its rules. A configured law, a research hypothesis and a measured
result are different claims. Revision-specific results are not a live status feed.

## The engine

Since 2026-09-19 there is one engine, the engine of the law of the ray
(`rays-v1`; the model owner's decision, [Highlights 5.4](HIGHLIGHTS.md#54-the-detector),
"DECIDED: the law of the ray"); the law of events of the same day is deleted.

| Document | Responsibility |
| --- | --- |
| [The law of the ray](RAY_LAW.md) | The published design and implementation contract of `rays-v1` (the model owner, 2026-09-19): the ray's record `NatureBeam`, the one function `nature_beam`, the flight table at 1 / sqrt 3, the eight-slot collision table and its inverse, the detector's squared record, the re-emission, the deletions, the tests, the expectations, and the implementation notes of the same day |
| [The engine](ENGINE.md) | The bookkeeping around the law as implemented: the GameBoard and its topology, the frame of an interval, the books, the world file's refusals, the record and the preflight |
| [Entity definitions](ENTITY_DEFINITIONS.md) | Reusable external apparatus data, placement, canonical loading, portable inputs and provenance |
| [Physical detector](DETECTOR_REQUIREMENTS.md) | Generic sensitivity requirements, the quantum goals and the unresolved scope; the reversible detector contract of 2026-09-19 absorbed into the ray law and deleted |
| [The worlds](../examples/events/README.md) | One content, two contents, two slits with a detector and the one-slit control under the ray law; the Bell worlds, the coupling, orbit, redshift, Hubble and Bohr series and the detector definitions: what each reads |
| [Canonical terminology](TERMINOLOGY.md) | Node, NodeState, Port, Link, Event and LocalRule vocabulary, the terms of the law of the ray (ray, direction, flight table, rest slot, collision, the one reading, record, re-emission), the terms kept from the law of events and the historical terms of the laws before it |
| [Architecture](ARCHITECTURE.md) | Module ownership, the integer contract, the dependency direction and the gates |
| [Migration](MIGRATION.md) | Every deletion and rename, dated; the law of the ray of 2026-09-19 first |

## Specification, experiments and hypotheses

| Document | Responsibility |
| --- | --- |
| [Highlights specification](HIGHLIGHTS.md) | The Universe 24 Highlights specification, edited directly by the model owner since 2026-09-17; every decision dated, in the owner's words; nothing deleted |
| [Highlights coverage](HIGHLIGHTS_IMPLEMENTATION.md) | What the repository implements of Highlights, section by section, with the tests; not evidence of a physical law |
| [Derivations of the known laws](DERIVATIONS.md) | The known laws derived on paper from one interval of the engine written as an operator on the GameBoard, rounds 1 to 8 (the law of the shadow in round 8, sections 51 to 56; the law of events and the law of the ray not yet derived) |
| [Experiments register](EXPERIMENTS.md) | The research runs, one entry each with its design and criterion pinned before the run, and the records of the runs made; never test-suite tests |
| [Hypotheses under test](HYPOTHESES.md) | The questions the framework raises, numbered, kept apart from measured results |
| [Problem solving](PROBLEM_SOLVING.md) | How the project advanced: one line per problem, its solution and who solved it |
| [Validation evidence](VALIDATION.md) | Dated, source-identified check results of the past; not timeless certification |

## Operation and change procedure

| Document | Responsibility |
| --- | --- |
| [Project status](PROJECT_STATUS.md) | The restart guide: where the project stands, what the checkout contains, how to resume without a conversation |
| [Test expectations](TEST_EXPECTATIONS.md) | The suite, one module per generic rule, with the expected integers written down before the first run |
| [Physical features](PHYSICAL_FEATURES.md) | Contract and review procedure for a new physical hypothesis |
| [Workspace](WORKSPACE.md) | The local configuration workspace: a world file edited, checked and run headless |
| [Retention](RETENTION.md) | Generated-output ownership, lifetime and cleanup |
| [Recovery](RECOVERY.md) | Restore a checkout, environment and authorized procedures without chat history |

The root [postulates](../POSTULATES.md), [simulator definitions](../SIMULATOR_DEFINITIONS.md)
and [contribution procedure](../CONTRIBUTING.md) retain their authority. This index
routes readers; it does not duplicate their technical rules. The contracts of the
engines before this one (the generic disturbance simulator, the law of the
bit and the law of the shadow), deleted on 2026-09-19, are in git at any
commit before their deletion.
