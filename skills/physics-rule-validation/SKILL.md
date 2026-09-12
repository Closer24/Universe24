---
name: physics-rule-validation
description: Independently validate every changed Universe24 physics-engine rule against explicit model contracts, locality, causality and bounded arithmetic.
---

# Physics-rule validation

Audit the ordinary schema 3 boundary as well as formula-free payloads; see
[elementary fields](../../docs/ELEMENTARY_FIELDS.md). Attempt supplied expressions
through updates, transport, emissions, exchange descriptors and typed initialization.
Reference validation is a separate contract. For local component exchanges check
joint sums and squared norms, finite spending, actual signed turns and stale
delayed arrivals. Distinguish those normalized invariants from physical kinetic
energy. For per-field waiting verify ownership, cost, arrival and final-unit decay.


Read [the shared workflow](../workflow.md), [postulates](../../POSTULATES.md),
[definitions](../../SIMULATOR_DEFINITIONS.md) and the
[feature procedure](../../docs/PHYSICAL_FEATURES.md). This review is mandatory
when a change affects physics-engine behavior.

**Inputs:** exact source/diff, model identity, feature contract and independent
test/run evidence. **Output:** a scoped pass or blocking findings, with the rule,
source location, counterexample/evidence and admissible correction for each.
Use read-only Git/source and existing Python checks unless assigned a focused
counterexample test. Review does not grant permission to change a physical law.
An undefined or contradictory contract, or missing evidence for the exact source,
means incomplete or blocked; do not fill the gap with an assumed pass.

For initialization-defined simulation, use
[DISTURBANCES.md](../../docs/DISTURBANCES.md) for active contracts. Verify
whole-record versus extensive transport, exact source accounting, paired
exchange, fixed transit and cost-dependent frozen local commits. Historical
self-force and particle-momentum laws apply only to their named candidates.

For each changed rule, verify:

- the operation, units, parameters, assumptions and expected behavior are explicit
  and mapped to a binding postulate or a labeled candidate hypothesis;
- each input has a local owner and a causal delivery path, including estimators,
  scheduling decisions and reads hidden behind adapters;
- evolving state and local loops have fixed bounds for fixed K; integers and
  intermediate operations respect the current register limits;
- event order cannot relay information across multiple links in one tick merely
  because each individual callback or particle move uses one link;
- local momentum exchange and commit/error behavior satisfy the declared contract;
- isolation, external-source response and relevant boundary cases have independent
  expectations, with no global repair or failure-hiding special case.

Q-ORACLE-1 applies only to the explicit quantum owner and its reported host work;
it does not exempt ordinary field, force, movement or geometry inputs. Diagnostics
may inspect global state and reject a run but must not supply physical repairs.

Do not infer a universal causal proof from a one-hop test or fixed callback size.
Separate tested finite cases, analytic arguments and unestablished physics. A
passing candidate does not resolve a failing baseline. For a blocker, preserve
the smallest reproducible case and hand it to its implementation owner and tests;
Boss must not mark the physics change complete until the required checks pass.
