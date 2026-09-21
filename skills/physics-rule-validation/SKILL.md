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
from measured Detector observables to the GameBoard. Coordinate invariant/bound proofs
with the [mathematician](../mathematical-validation/SKILL.md); keep supplied
reference laws, analytic checks and empirical agreement distinct.

## Our laws are on the GameBoard; the detector sees other laws

The model owner, 2026-09-20: "Our laws are on the GameBoard; in the detector
one sees other laws." The rules under review are the GameBoard's: families
with their keys (charge and other columns per unit of content, a lifetime,
the phase per Link, the quantum), the tables from the keys, the flight and
collision tables, the click. Nature's laws (Newton, Einstein, Bohr, Yukawa's
range, Hubble, the electroweak scale) are laws of the detector's world: they
are what detectors read, and the review never asks the GameBoard to carry
their forms. A change is admissible when it is generic, local, bounded and
formula-free on the GameBoard; whether nature's laws then appear is decided
by detector readings under the [experimenter](../experimenter/SKILL.md),
never by a formula placed on the GameBoard.

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
Apply the local observer contract; do not infer
proper time, optical appearance or an emergent relativistic spacetime from the
current reception probe or an audit snapshot. This framing uses the declared
model contracts and does not add a new physical law.

## Review energy and momentum claims

Use the local conservation contract when a
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
through interference probabilities; real reference coefficients alone cannot
expose a partial-conjugation defect.

## Review the declared rules

For delayed Node rules,
distinguish a consumed start trigger from a persistent commit condition. Exercise
an arrival during the wait and inspect every frozen substep against live stock,
including chains with zero net delta. A balanced final component sum does not
prove each nonlinear rule invariant remained valid. Check that rejected proposals
leave all actual owners and already received inventory intact.

For the active engine, use [the Beam Law](../../docs/BEAM_LAW.md) and
[the engine's bookkeeping](../../docs/ENGINE.md) for active contracts (the
generic disturbance contract, DISTURBANCES.md, was deleted on 2026-09-19). Verify
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

There is no model-computation exception: the shared quantum resource
(Q-ORACLE-1) and its event storage were deleted on 2026-09-17 with Highlights
section 3.18. Diagnostics may inspect global state and reject a run but must
not supply physical repairs. Keep shared bookkeeping out of ordinary fields
and physical remote observables.

Do not infer a universal causal proof from a one-hop test or fixed callback size.
Separate tested finite cases, analytic arguments and unestablished physics. A
passing candidate does not resolve a failing baseline. For a blocker, preserve
the smallest reproducible case and hand it to its implementation owner and tests;
Boss must not mark the physics change complete until the required checks pass.

## Emergence check (2026-09-20, record 151)

When a change adds a rule or a world key for an effect that relative motion, a varying rate or a meeting could produce by itself, require the emergence test in the review: the same world with the key absent, the expectation pinned before the run (for a reader stepping one Link per k intervals through a stream of one row per interval: k + 1 rows per k intervals toward, k - 1 away, if the step reads the Link it crosses). A rule that reproduces what the flight, the step and the meeting already give is not admissible; a step that misses the effect is the defect to name, fixed in the step, not beside it. Record which case held and cite the file:line of the step and of the read.

## The main course (the owner, 2026-09-21, records 176 and 177)

A review checks the pairing: the formula with its registered integer and with the experiment, in the limit and at finite resolution; and that a new rule was stated first in its generic vector form before its integer form (skills/workflow.md).

## Notation (the owner, 2026-09-21, record 184)

Every symbol is named in English at its first use (never a Greek letter alone: "gamma (the Lorentz factor)"), and its kind is shown by its type: a scalar plain, a vector in bold lowercase (**p**), a tensor, matrix or operator in bold uppercase (**C**); skills/workflow.md, "Notation".
