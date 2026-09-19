# Documentation index

Start with [project status](PROJECT_STATUS.md) and the [repository entry point](../AGENTS.md).
Each document below owns one subject. Link to that owner instead of maintaining
another copy of its rules. A configured law, a research hypothesis and a measured
result are different claims. Revision-specific results are not a live status feed.

## The engine

Since 2026-09-19 there is one engine, the field-only engine of the law of the
shadow (`field-only-v1`; the model owner's decision, [Highlights 5.4](HIGHLIGHTS.md#54-the-detector)).

| Document | Responsibility |
| --- | --- |
| [The engine](ENGINE.md) | The world file, the interval's steps, the wait, the events, the books, the record and the preflight, as implemented |
| [The worlds](../examples/shadow/README.md) | One content, two contents, two slits and the one-slit control: what each reads |
| [Canonical terminology](TERMINOLOGY.md) | Node, NodeState, Port, Link, Event and LocalRule vocabulary, the terms of the law (content, quantum, event, family, table) and the historical terms of the law of the bit |
| [Architecture](ARCHITECTURE.md) | Module ownership, the integer contract, the dependency direction and the gates |
| [Migration](MIGRATION.md) | Every deletion and rename, dated; the one-engine cleanup of 2026-09-19 first |

## Specification, experiments and hypotheses

| Document | Responsibility |
| --- | --- |
| [Highlights specification](HIGHLIGHTS.md) | The Universe 24 Highlights specification, edited directly by the model owner since 2026-09-17; every decision dated, in the owner's words; nothing deleted |
| [Highlights coverage](HIGHLIGHTS_IMPLEMENTATION.md) | What the repository implements of Highlights, section by section, with the tests; not evidence of a physical law |
| [Derivations of the known laws](DERIVATIONS.md) | The known laws derived on paper from one interval of the engine written as an operator on the lattice, rounds 1 to 8; the law of the shadow in round 8 (sections 51 to 56) |
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
old engine (the generic disturbance simulator and the law of the bit), deleted
with it on 2026-09-19, are in git at any commit before that day.
