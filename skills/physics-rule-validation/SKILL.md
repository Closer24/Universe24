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

## Empirical targets and observable mapping

For physics comparisons, follow the shared
[physics comparison method](../workflow.md#physics-comparison-method).
Own the primary physical reference, its regime and uncertainty, and the mapping
from measured Detector observables to the board. Coordinate invariant/bound proofs
with the [mathematician](../mathematical-validation/SKILL.md); keep supplied
reference laws, analytic checks and empirical agreement distinct.

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

For [ordinary/quantum contact conversion](../../docs/LOCALIZED_QUANTUM_CONTACT.md),
check ownership at the actual delayed commit, not merely at branch planning.
Exercise a coupled third resident and arrivals into spare slots. Validate all
local outcomes before sampling, including common field reactions; require a
semantic-owner occupation guard in addition to JSON preflight. Test finite
localized emission, causal field fronts and equal vacuum/click controller cost.
Keep possible origin references distinct from probability or copied inventory.

For [causal weighted sources](../../docs/CAUSAL_QUANTUM_SOURCES.md), trace every
ordinary source weight to retained local amplitudes and actual frozen Link
packets. Quantum conditional queries, global normalization and shared retirement
flags must not control ordinary field values or clocks. Check phase-sensitive
split/recombination, rational complex vacuum normalization, receipt and evaluation
tariffs, and every intermediate Link/control delay. Compare remote ordinary
source, field and cost prefixes before a terminal notice can arrive. Exercise
null results without remote renormalization, capture during pending emission,
charged duplicate notices and stale packets after local termination. Inspect
transitive NodeState for bounded values, indices and fixed proposal/Port banks,
with immutable laws outside it. Keep retarded source weights, single conserved
carrier inventory and finite field injection as separate quantities; do not
report a source-weight sum as charge conservation or physical energy closure.

Use the [local conservation contract](../../docs/LOCAL_CONSERVATION.md) when a
model claims joint energy and momentum balance. Identify all actual owners and
fluxes, and inspect the complete update chain, including arrival merging and
later carrier rules. Distinguish declared component sums, normalized probe
quantities and independently justified physical energy. A passive audit may
report a committed violation; it neither repairs that event nor proves closure
of all admitted inputs. Require a separate scope statement for omitted energy
terms, external reservoirs and unimplemented field or spin dynamics.

For unresolved momentum, distinguish a missing value from a declared zero mean
with nonzero variance. A local kick cannot recover an unknown incoming momentum.
If a candidate transfers uncertainty, identify its receiving owner and retained
state. Conserving means and second moments is expectation-level closure; it does
not prove conservation in every sampled branch or retention of quantum phase and
correlations. Check mass assumptions in kinetic-energy readouts, and reject
missing diagnostic payloads instead of treating them as zero.

For wave-derived moments, distinguish the incident density, selected measurement
state and any ordinary output re-encoding. Absorption vacuum has no particle
momentum distribution. A finite derivative observable is not automatically
canonical momentum; check phase-sensitive states with identical position
probabilities, mixed states and boundary rows. Keep exact density diagnostics
outside physical inputs. Separate nonselective operation drift from selected
conditional changes; neither is a simulated apparatus recoil without an actual
owner and interaction. Audit propagation against a newly introduced energy
readout instead of reusing an older fixed inventory as proof of closure.

For configured relative phases, compare equivalent coefficient pairs that differ
by a common complex factor. Exercise negative exponents and inverse composition
through interference probabilities, including the ordinary envelope consumer;
real reference coefficients alone cannot expose a partial-conjugation defect.

## Review the declared rules

For [recurrent contact outcomes](../../docs/RECURRENT_QUANTUM_CONTACT.md),
enumerate complete instrument weights and validate every output before drawing.
Exercise occupied-domain preparation, capacity exhaustion, same-tick replay after
resolution and several local origins without inventory duplication. Compare
remote ordinary prefixes across outcomes that change the quantum generation;
a local vacuum result must not select its ordinary source bank from remote
quantum progress. Keep finite allowances and stale packets isolated by generation.

For [delayed Node rules](../../docs/NODE_VECTOR_PROCESSOR.md#local-rules),
distinguish a consumed start trigger from a persistent commit condition. Exercise
an arrival during the wait and inspect every frozen substep against live stock,
including chains with zero net delta. A balanced final component sum does not
prove each nonlinear rule invariant remained valid. Check that rejected proposals
leave all actual owners and already received inventory intact.

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

For quantum event storage, follow the
[event-spacetime contract](../../docs/QUANTUM_EVENTS.md#event-spacetime-and-current-references)
and [origin-cell contract](../../docs/WAVE_ORIGINS.md). The immutable spacetime
is the history; do not add a second linked list per Node or wave. Distinguish
six local origin IDs from finite virtual-register heads and exact joint state.
An origin is a continuation identity, not a disturbance count; one-origin joint
interactions require explicit state/coupling/instrument evidence like any other.
Check atomic conditional sampling and terminal marking, next-tick local pruning,
no-click/continuation semantics, and unchanged source events. Independent stale
lotteries followed by first-writer selection do not prove correct probabilities.
Require origin-tagged gates and instrument requests in the wave profile. Verify
that unarrived support cannot execute a gate. Retired-gate suppression must preserve
the complete retained correlated density, not only one marginal; otherwise it
must fail before publication. A retired instrument additionally needs its explicit
null outcome to be the sole possible result with unchanged full density. Exercise
an unsafe remote X, a deterministic non-null record and a state-changing null.
Check native recertification when a target head changes without a fresh arrival.
Count guard queries/audit costs separately from O(1) origin lookup; neither audit
cost nor suppression metadata is an ordinary physical observer or delay channel.
Check that no older untagged binding bypasses the lifecycle. Distinguish retained
conditional audit state from a claim of physical
absorption. Verify Link readiness, phase and correlation preservation across checkpoints.
Keep shared quantum bookkeeping out of ordinary fields and physical remote
observables; bounded origin lookup does not make the complete host query O(1).

Do not infer a universal causal proof from a one-hop test or fixed callback size.
Separate tested finite cases, analytic arguments and unestablished physics. A
passing candidate does not resolve a failing baseline. For a blocker, preserve
the smallest reproducible case and hand it to its implementation owner and tests;
Boss must not mark the physics change complete until the required checks pass.
