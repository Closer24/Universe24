---
name: physics-rule-validation
description: Independently validate every changed Universe24 physics-engine rule against explicit model contracts, locality, causality and bounded arithmetic.
---

# Physics-rule validation

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

## Always start from event spacetime

Ground every physical review in the modeled space of events and causal time:
event locations, state transitions, occurrence order and causal dependencies.
The object of analysis is what happens in that model, not the image an observer
sees. Distinguish the event at its source, later reception of information about
it, and its recorded or rendered appearance. Reception is itself a separate local
event; it does not relocate or retime the source event.

Label evidence as world/event audit, local observer record or display projection.
Global state, remote origins and causal IDs may support an analyst's audit but
are not automatically available to a local observer or physical update. Establish
observer claims from information that could actually arrive through the configured
causal paths; a receiving port identifies the last hop, not the remote source.

For each timing claim, identify the model/audit tick, completed local-cycle counter
or playback time being used. Equal local-counter readings do not prove simultaneous
events, and playback sampling or speed does not change physical event order.
Apply the [local observer contract](../../docs/LOCAL_OBSERVER.md); do not infer
proper time, optical appearance or an emergent relativistic spacetime from the
current reception probe or an audit snapshot. This framing uses the declared
model contracts and does not add a new physical law.

## Review energy and momentum claims

Use the [local conservation contract](../../docs/LOCAL_CONSERVATION.md) when a
model claims joint energy and momentum balance. Identify all actual owners and
fluxes, and inspect the complete update chain, including arrival merging and
later carrier rules. Distinguish declared component sums, normalized probe
quantities and independently justified physical energy. A passive audit may
report a committed violation; it neither repairs that event nor proves closure
of all admitted inputs. Require a separate scope statement for omitted energy
terms, external reservoirs and unimplemented field or spin dynamics.

## Review the declared rules

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
