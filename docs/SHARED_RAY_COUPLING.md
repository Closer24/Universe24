# Shared complete-ray coupling: bounded implementation candidate

> **History (2026-09-19).** The engine this document describes was deleted on
> 2026-09-19 with the old engine ([migration](MIGRATION.md#one-engine-on-2026-09-19-the-old-engine-deleted));
> the one engine is the field-only engine of the law of the shadow
> ([SPATIAL_FIELDS.md](SPATIAL_FIELDS.md#the-law-of-the-shadow-field-only-v1)).
> The text below is kept as the record of what was built and measured; its
> links to code, worlds and tests name files that no longer exist.

## Authority and scope

The user requires a nucleus to consist of rays retained by the same generic
coupling used elsewhere, and authorizes implementation. A separate species
binding flag, supplied contact energy gap, prescribed orbit, external mirror or
permanent retention block does not implement that target. The earlier contact
candidate remains historical evidence with its original model identity.

This document closes a necessary executable interface under the explicit model
identity `node-ray-coupling-v1`. Its numerical fixture demonstrates finite,
phase-sensitive residence followed by release. It is not a nuclear law, an
electron bound state, an empirical frequency prediction or a new runtime default.
The [generic operation annex](https://github.com/Closer24/Universe24/blob/docs/architecture-entity-layers/docs/NODE_GENERIC_OPERATIONS.md),
[spatial fields](SPATIAL_FIELDS.md), [architecture](ARCHITECTURE.md) and
[local conservation](LOCAL_CONSERVATION.md) retain their existing ownership.

Implementation base: remote main
`d5d24271a63a29fee5f5caa848068a9973ffb42f`. Generic carrier interactions already
evaluate bounded expressions on a frozen participant set. Complete spatial rays
must enter that same evaluation mechanism through a typed projection, rather
than through a second species-specific evaluator. N-to-M carrier conversion
alone does not provide this spatial-ray composition.

## Complete participant and atomic proposal

| Part | Contract |
| --- | --- |
| Physical location | One Node; bounded resident rays including causally arrived Link payloads |
| Participant view | Amount, integer heading vector, phase, phase advance and interaction delay; projections are non-owning |
| Preserved state | Complete native ray metadata, including DDA state, pace remainder and continuation identities |
| Operation | Existing bounded generic expression evaluator and frozen simultaneous assignments; property requirements and guards select participants |
| Result | Complete replacement rays plus explicit bounded retention metadata, validated together before any publication |
| No-op | No complete eligible group, false guard, or a participant already delayed |
| Error | Invalid heading, range, intermediate overflow, missing owner, insufficient capacity or failed invariant rejects the proposal before changing its participants |
| Cost | Fixed rule, participant and resident-slot bounds; no history-growing structures, distant reads or quantum-owner queries |

Use declared property mappings into the generic evaluator. Immutable heading
tables may resolve an output vector to an admitted heading; no particle name or
world coordinate selects a law. Non-participants keep their complete state.
The top-level `ray_interactions` option reuses indexed `participants`,
`assignments`, `invariants` and `when`. At most six participants are selected
greedily into disjoint groups. The selected spatial fields of one layer have at
most 32 declared ray slots in total, matching the fixed existing indexed-selector
capacity; rays are met layer by layer
([layers](SPATIAL_FIELDS.md#layers-ray-layers-v1)), so fields of different
layers do not share that capacity.
A participant's configured spatial-field type or
required structural properties selects its non-owning view. The projection
properties are `amount`, `heading`, `phase`, `advance`, `delay`, `family`,
`charge` and `detector` (`RAY_PROPERTIES`); `delay` maps to native
`interaction_delay`, `family` is the index of the ray's spatial field,
`charge` the whole charge of the thing the ray is, its family's times the things a merged ray carries ([wave-ray families](SPATIAL_FIELDS.md#wave-ray-families-wave-ray-family-v1), [charge per thing](SPATIAL_FIELDS.md#charge-per-thing-charge-per-thing-v1))
and `detector` the Detector bit it carries, `0` none, `1` a draw of 0, `2` a
draw of 1 ([the bit as a property](SPATIAL_FIELDS.md#the-detectors-bit-as-a-property-detector-bit-property-v1)).
Only heading, phase and delay are writable in this first interface. Amount,
advance, family, charge and detector are read-only, and `charge x amount`
summed over the participants is an invariant appended to every rule; the
outputs of every rule that fires carry the bit its inputs hand down. The shared value-level
evaluator is also the carrier path's evaluator, not a copied implementation.
Native ray operations without outputs preserve the number and identity of
complete owners. They reject `output_types`, including typed initialization and
direct local-law calls; a rule with `outputs` is the meeting with N-to-M outputs
of `ray-meeting-conversion-v1` ([meetings with outputs](SPATIAL_FIELDS.md#meetings-with-outputs-ray-meeting-conversion-v1)), which replaces its
participants by new event rays with the arithmetic `convert_values`; the
N-to-M conversion of records that shared it was deleted on 2026-09-17 (issue
#164, bucket B.6), and a meeting has at least two participants.
Process each selected ray at most once in one local coupling pass. An earlier
successfully received packet remains an owned input when a proposal is rejected.

Changing heading starts a new lattice line: reset its DDA accumulators only
when the heading changes. The initial coupling sector uses unit axial headings
and unpaced Link transport, so the existing pace remainder is zero. Heading
changes must not silently discard a nonzero remainder in a later extension.
Fields with attenuation, self-exclusion, or other consumers that
cannot preserve the full interaction/ownership contract must be rejected for
this coupling at initialization until their composition is separately supported.

## Timing, retention and phase

Add one bounded nonnegative `interaction_delay` to the complete ray. It is
distinct from `Ray.wait`, which remains the Euclidean pace remainder. A positive
interaction delay keeps that ray locally owned and excludes it from new coupling
selection. It is not an independently conserved inventory quantity.

Within the admitted spatial processing lane:

1. Read causally available resident rays and select eligible zero-delay
   participants; evaluate the generic operation on a frozen view.
2. Validate and publish every complete participant replacement atomically.
3. For a ray with positive delay, decrement by one and advance its phase once;
   retain it for that interval, including when the remaining delay becomes zero.
4. A zero-delay ray follows the existing one-Link forwarding operation, which
   advances its phase once. Link transit never advances it a second time for
   that same accounted interval.

No configured `k` is accepted in `ray_interactions` for this first fixed-interval
interface; residence is the explicit `delay` output. Carrier Node-execution
duration semantics are not silently applied to these spatial participants.

The coupling pass occurs before absorption and transport. Newly emitted rays
are not participants until a later interval. A delayed ray's stock remains an
ordinary resident owner available to admitted local absorption only if that
absorption explicitly preserves the complete delay/phase ownership contract;
unsupported combinations are rejected before the run.

For the fixture, phase is an integer in `0..7`, and one accounted interval adds
one modulo eight. The phase recurrence is therefore eight intervals by the
configured rule. This is a phase-tag recurrence, not evidence of eight-tick
spatial motion, proper time, a quantum energy-frequency relation or interference.
The prepared integer phase table remains the existing phased-ray convention.
Conserved amount is actual ray stock; a phase-dependent signed amplitude or
cosine-table projection is not substituted for that stock in the energy audit.

The initial implementation uses the existing fixed Link clock with `H = 1`.
The selected main tree has no six-output-clock implementation to compose here;
this work does not silently import one from an unmerged historical branch.
It does not enable composition with that six-output-clock profile,
shared computation delays or Node execution.
Unsupported compositions fail initialization. A later extension must specify
the additional phase intervals and complete-owner readiness explicitly.
For this first interface, `ray_interactions` requires `detector-only-v1`, the
only sampling profile. The claim, bond and lottery owners that this rule once
had to exclude, selected or not, were deleted on 2026-09-17, so no field can
supply a draw or a mutable registry effect outside the complete proposal.

## Numerical fixture and independent expectations

At the same Node, prepare two complete rays with positive amounts `a = b = 5`,
headings `(1,0,0)` and `(-1,0,0)`, phases zero, phase advance one, and zero
interaction delay. Select them by properties. The configured guard requires
equal positive amounts, opposite unit headings and both phases zero.

The shared operation swaps their heading vectors and assigns interaction delay
two to each. Amounts, phases and phase advances are unchanged by this operation.
The subsequent interval advances the phases as specified above. The number two
is a declared demonstration parameter; it is not a measured nuclear constant.

| Local processing step | Phase after step | Delay after step | Owner and motion |
| --- | --- | --- | --- |
| Initial state | 0 | 0 | Two residents at the encounter Node |
| 0 | 1 | 1 | Headings exchanged; both remain residents |
| 1 | 2 | 0 | Both remain residents |
| 2 | 3 | 0 | Guard is false; rays depart through opposite Ports |

The adjacent receiver cannot own a departure earlier than its send time plus
`H`. An independent integration fixture must pin the actual `Simulation.tick`,
send-event tick and arrival-event tick for its known initial preparation before
running; it must not accept multiple timestamp conventions to hide an off-by-one
error. The table above indexes local processing calls, while event timestamps
use the existing engine convention. The delay belongs to both actual rays, not a shadow copy of their
stock. After release, the rays separate under the ordinary transport rule.

Use the declared axial readouts `E = sum(a)` and `P = sum(a*h)` across all actual
owners. Before and after the encounter, `E = 10` and `P = (0,0,0)`. Thus
`E*E - dot(P,P) = 100` in these configured units. This arithmetic illustrates
the rest-energy readout of two opposing axial rays; it does not prove that the
pair remains localized or has inertial mass ten under a boost.

The fixture must declare these complete-owner readouts as ordinary generic
invariant expressions. The shared evaluator enforces the declared expressions;
the native-ray adapter must not hardcode physical energy or momentum formulas,
infer them from particle labels, or dispatch them by `model_id`. Positive axial
admission is the stated implementation limit, not a universal family energy law.
Amount remains structurally read-only in this interface. For two participants,
the required fixture invariants are:

```json
[
  {
    "name": "fixture_energy",
    "expression": {"op": "add", "args": [
      {"field": "amount", "participant": 0},
      {"field": "amount", "participant": 1}
    ]}
  },
  {
    "name": "fixture_momentum",
    "expression": {"op": "add", "args": [
      {"op": "mul", "args": [
        {"field": "amount", "participant": 0},
        {"field": "heading", "participant": 0}
      ]},
      {"op": "mul", "args": [
        {"field": "amount", "participant": 1},
        {"field": "heading", "participant": 1}
      ]}
    ]}
  }
]
```

A heading swap does not conserve momentum for arbitrary amounts. For example,
amounts five and three along opposite headings have `P_x = 2`; swapping only
their headings would give `P_x = -2` and must not commit. The fixture's equal-
amount guard avoids this case, while the configured generic invariant rejects
an incorrect assignment. A different configuration without these declared
readouts has no certification for this candidate's energy/momentum claims.
Extending the interface to amount changes would require exact inventory and
declared energy/momentum closure. Negative values are not positive-energy rays
in this fixture.

Independent acceptance is fixed before execution:

- Coupling absent: both rays depart without the two retained intervals.
- Phase control: phases one and one do not meet the guard and depart immediately.
- Missing partner or unequal amounts: no finite-residence operation occurs.
- Eligible encounter: exactly the residence/phase sequence above and actual
  opposite-Port release, preserving all owners and continuation metadata.
- Invalid one-sided heading/amount update: invariant failure, unchanged input
  owners and no partial output.
- Translation, axis permutation and selector-label renaming: corresponding
  traces and conserved readouts agree; no preferred nucleus coordinate exists.
- Repeated/late arrivals and full capacity: the bounded ownership/error contract
  holds without lost inventory, duplicate interactions or an unbounded queue.
- No Detector: zero lotteries. Unsupported Detector composition is rejected,
  never replaced by a legacy in-engine draw. Existing supported Detector tests
  remain separate evidence until their composition is implemented.

A fixed phase guard can retain a specially prepared state forever when phase
advance is zero. That would impose retention through initial data; it is not
acceptance evidence for an emergent stable nucleus. Do not replace this releasing
fixture with such a preparation to obtain a visually bound result.

## Optional carried-heading field readout

A separate compatible interface makes directional information explicit without
inventing a force. A ray spatial field may select
`"flux_projection": "carried_heading"`; the existing default is `"ports"`.
The ordinary `flux` expression then uses the selected projection.

For the new projection, use only pre-emission rays actually resident at the
sampled Node: `F = sum(ray.amount * headings[ray.heading])`. Sample locally
retained rays again on each admitted carrier cycle; this is a local directional
field readout, not a count of unique arrival events. Fresh same-cycle emission
is not retroactive input. The existing Port projection remains unchanged.

General bounded integer headings are admissible for this readout. For a heading
such as `(2,1,0)`, calling amount the ray's energy and `amount*heading` its physical
massless momentum would be unjustified. The projection is exact directional
accounting until a physical observable convention is supplied.

Any supported free-emitter self-exclusion must subtract the same carried-heading
projection of its causally local owned bookkeeping. Subtracting last-hop Port
flux from carried-heading flux is inconsistent. Reject non-ray fields and the
`arrival_port_blind` composition for this option. No remote source coordinates,
global origin scan, normalized heading, new recoil law or hidden force is added.
In addition to the existing scalar-field sample tariff, charge four reads and
six updates for each declared ray slot when this projection is selected, even
for unused slots. This is a fixed conservative model tariff for the bounded
scan, multiplication and accumulation; it is not measured host instructions.
The cost changes only under the explicit projection selection and must be
reported separately from host execution time.

## What this implementation can establish

Passing the fixtures establishes a common bounded operator over complete local
rays, conserved declared axial readouts, phase-sensitive finite residence, actual
release and causal field-direction access. Canonical HTML and an actual-state
GIF accompany requested simulator experiments; rendering never fills in a
missing orbit or feedback law.

The nucleus target still requires a numerical common coupling that produces
robust localization with open escape/product channels, perturbation and funded
release controls, plus a moving-system test. Two equal/opposite rays reflecting
once subsequently separate; zero total momentum is insufficient for binding.
The surrounding electron target separately requires spatial localization and
measured recurrence with the same admitted laws, not a prescribed circular path.
No empirical strong/weak law, atom or electron frequency follows from the
interface fixture. These are recorded acceptance limits, not permission to
reintroduce the superseded species-specific binding law.
