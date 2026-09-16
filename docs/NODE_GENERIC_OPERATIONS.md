# Node-local generic operations: implementation specification and candidates

## Status and authority

This document responds to issue [82](https://github.com/Closer24/Universe24/issues/82).
All ordinary generic physical operations execute **at the Node**, using its
bounded owned state and causally arrived inputs. The reusable implementation may
live in the generic operations package; that is code ownership, not a second
physical location. The engine schedules, transports and validates; NodeState is
data. There is no fixed internal register decomposition or count.

Three statuses are used below:

- **Binding:** the user's Node-only, six-neighbor, bounded-integer, lossless,
  causal and formula-free-scheduling requirements.
- **Existing:** a mechanism described by a named current implementation contract;
  composition into the proposed unified profile is not implied.
- **Candidate:** an explicit proposed mathematical/model choice, ready for scoped
  implementation review but not an adopted law of nature or a runtime default.

This is a design handoff, not a claim of implementation, completed tests or
universal physical agreement. Only developers change code or tests. Preserve
existing profiles; use the explicit proposed identity `node-generic-candidate-v1`
for the candidate definitions below. Do not silently change their physics.

The [unified schema](https://docs.google.com/document/d/1jPBMb-1BoCH8Qo6y5E-j0H0ANWzbHmkO9l-9t2pxSOQ/edit)
is the single canonical owner of model definitions. [Highlights](https://docs.google.com/document/d/1IkhSyqZZMBSgbJV-PMMwcXG0D_Rlfg4FrLy2jXBMUSs/edit)
is a summary and navigation surface, not a second competing specification.
This file is a candidate implementation/acceptance annex. The central schema's
section 4 owns the accepted Detector law; the repository Detector page indexes
implementation status and profile boundaries only.
Current detailed boundaries are [architecture](ARCHITECTURE.md),
[Node execution](NODE_VECTOR_PROCESSOR.md), [lossless arithmetic](ARCHITECTURE.md#lossless-remainder-ownership)
and [Detector exchange](DETECTOR_EXCHANGE.md). This proposal does not override
closed decisions in those sources.

## What is already defined, and what is actually missing

| Mechanism | Existing definition | Remaining unified-profile work |
| --- | --- | --- |
| Local selection and frozen joint assignments | Indexed participants, deterministic bounded grouping, delayed atomic commit in Node execution | Reuse these semantics; no new private-channel restriction |
| Scalar/vector values and declared invariants | Bounded expressions; 1..32 components in Node profile; conservation readouts | Exact nonnegative-code adapter and complete remainder lifecycle remain unimplemented targets |
| Neighbor propagation and ray phase/routing | Named ray and disturbance profiles | Preserve complete semantic state in one admissible payload contract; prove compatibility with local execution |
| Spatial fields and local backreaction | Local field rules and spatial couplings | Integrate under the same complete-owner transaction; known lossless gaps remain gaps |
| Coherent joint state and conditional instruments | Native quantum event owner and event-spacetime contracts | Current Node profile does not admit this full composition; build an explicit bridge, not a hidden ordinary-state query |
| Split, recombine and multi-output reactions | Several separate existing profiles, with nonadditive split restrictions | Distinguish amplitude modes from material inventory and give every retained value a bounded owner |
| External Detector exchange | User-selected PASS/GENERATE_RETURN and causal branch return | Distribution and content law are not selected; candidates below stay separate from accepted behavior |
| Standard particles/interactions | Catalog records and partial executable profiles | A representation label is not a force law, a bound nucleus, an atom or a calibrated photon |

## Common state and transition contract

The central schema, section 1, owns the accepted channel/cabinet and bounded-work
invariant, including mobile active events and directional pushing. The earlier
capacity-wait/backpressure proposal is superseded and is not an allowed fallback. This annex
implements that boundary; it does not introduce a separate event per property
or a new normative channel model. An active event's move preserves its identity
and complete property bundle. Return addressing uses the event identity, not an
assumed permanent source Node. The routing details listed below remain open.

A model manifest fixes K resident records, D components per record (D <= 32 for
the initial candidate), F field components, R rule count, A maximum participants,
M maximum output modes, B pending transactions and Q quantum handles before a
run. Six Ports each have fixed input/output capacity. All are finite positive
bounds checked before initialization; none grows with particles elsewhere,
time, path length or the number of previous sources. Different experiments may
select bounds before starting. A parameter is not allowed to grow during a run.

State consists only of bounded Scalars/Vectors and fixed metadata: occupied bits,
type/layout references, mode/branch generation, input/output roles, Port,
ready time, transaction identity, exact scale/remainder ownership and admitted
quantum handles. A ray is the transport role of this state, not a species branch
in the engine. Field values use the same numerical and ownership contracts;
stationary retained field stock is allowed between emissions.

Candidate exact numerical convention: stored codes use the architecture's
proposed zigzag mapping; decoded intermediates may be signed. This resolves the
intermediate-sign question for this candidate only. Each component represents
an exact bounded numerator/positive denominator pair, with shared denominators
where valid. Reduction has a fixed iteration bound. Use the current 63-bit
signed work bound unless a separately reviewed arithmetic profile is selected.
Reject every overflowing intermediate before commit, even if cancellation would
make the final result small. No rounding, normalization, clipping or dropped
fraction is permitted. Denominator exhaustion is a reported finite-model limit,
not permission to modify the state. Fixed finite precision does not promise
unlimited exact rational evolution.

Every operation is one transition on a frozen local snapshot:

`(owned state, arrived inputs, immutable operator) -> pending proposal -> commit`.

At prepare, reserve participant slots and all potential output capacity. At
commit, validate live ownership, persistent guards, dimensions, integer bounds,
complete before/after conserved readouts and every intermediate frozen substep.
Intervening arrivals keep their own slots; they are neither overwritten nor
retroactively inserted into the frozen operation. Commit all affected owners,
local event metadata and reserved output banks together. A rejected transition
publishes no proposed effects and consumes no new random ticket. An earlier
successfully committed arrival remains real; atomicity does not rewind history.

Conserved quantities are model-defined exact readouts over all actual owners:
residents, local fields, in-flight payloads and declared apparatus/reservoirs.
Samples and pending proposals are not extra stock. A declared vector sum can be
tested without calling it physical momentum. Physical energy needs its own
justified expression, including interaction/apparatus terms when applicable.

### Timing and participant selection

Candidate timing explicitly names `wait_ticks` and `link_ticks`, never ambiguous
k. A local physical transformation takes positive bounded `wait_ticks`; identity
routing may have zero additional wait. One adjacent Link takes `link_ticks = 1`.
Thus a prepared identity at tick t can arrive at a neighbor no earlier than t+1;
a two-tick transformation followed by transit arrives at t+3. This is the
existing Node-profile convention made explicit, not a Planck-time calibration.
Computation-field delay is a configured bounded local integer operator over an
already received field; no mass-to-delay law is inferred.

Reuse declaration-order/earliest-unused-compatible-slot selection from the Node
contract. A failed later role does not cause combinatorial backtracking. Consume
at most the fixed groups/rules budget. Participant slots remain reserved until
commit under an admitted timing profile. Under the latest user rule, when a slot
is needed the saved event variable is pushed UP its same ray path; an opposing
return signal moves DOWN that path. Capacity does not authorize waiting. Each
tick performs the event/update unless a delay is explicitly configured. Exact
simultaneous-push and reservation semantics are not yet specified; existing
delayed reservation behavior must not silently decide them. No recursive
unbounded same-tick chain of pushes is permitted. The owner remains explicit. Unsupported
initial layouts, arithmetic overflow and unrepresentable new state still fail
explicitly before mutation. Do not choose a different physical outcome or insert
an unbounded queue. The existing slot-order rule is a candidate for resident
participant selection only; it does not settle simultaneous channel arrivals.
Slot order is
part of this candidate; indistinguishable-particle/permutation claims need their
own equivalence tests, not a claim that deterministic ordering proves symmetry.

Every operation below inherits these timing, bounds, conservation and failure
rules. Its row supplies its specific trigger, owners and outputs.

## Operation catalogue

| ID / operation | Inputs and trigger | Node-local output and ownership | Duration and invariant |
| --- | --- | --- | --- |
| N0 Admit / dispatch / push | A due adjacent-Link packet, ready output or slot demand under the directional-push contract | Ownership moves locally with the complete event ID, properties and remainders; slot demand pushes existing variable UP the same ray; current/upstream overlap detects encounters without duplicating stock | One-hop causal bound; no capacity waiting; simultaneous-push and overlap-lifetime semantics remain OPEN |
| N1 Phase / internal transform | Selected local vector and immutable exact matrix; local cycle trigger | Same owner's transformed vector; no new physical stock | Positive declared wait; preserve the operator's declared quadratic/linear invariant exactly |
| N2 Local interaction | Bounded compatible resident/arrived participants plus owned local field; declared start guard | Joint new participant/field states, including equal opposite declared exchange | Positive declared wait; all complete-owner conserved readouts and persistent guards checked |
| N3 Coherent split / mix | Coherent compatible modes and declared matrix; local interaction event | Replace a fixed mode vector with its transformed mode vector; retain a single material-stock owner or explicit common quantum owner | Positive declared wait; exact chosen mode norm; no cloned material inventory |
| N4 Recombine / merge | Arrived compatible modes or compatible additive stocks | Coherent recombination uses N3 inverse matrix; extensive-stock merge sums exact stocks only if sufficient state retained | Positive declared wait; no destructive sum of distinguishable or incompatible histories |
| N5 Emit field / products | Local source and finite owned allowance; explicit emission trigger | Debit actual source, create bounded outputs and retained fractions in one proposal | Positive declared wait; source plus products conserve declared quantities; supplied external stock is labeled external |
| N6 Absorb / convert | Local incident stock, receiving material/field owner and configured channel | Remove incident owner only as its exact quantities enter receiver and/or products | Positive declared wait; absorption is not deletion; capacity/receiver failure leaves all inputs owned |
| N7 Delay / retain | Local ready proposal and received computation field | Retain unchanged payload and reservations until explicit ready time | Bounded nonnegative added wait; field dependence selected by manifest; no dependence on host load |
| N8 Quantum operation request | Locally arrived support, bounded handle, local setting and declared instrument/gate | Node requests the explicit quantum owner; only local output is physically committed here | Q-ORACLE-1 model query cost/time convention; ordinary waits/Links remain causal; no direct ordinary remote-state updates |
| N9 Detector boundary / returned control | Causally arrived Detector signal, bounded branch generation and local exchange state | Node passes, routes or applies a causal local notice; external Detector owns action/content draw | Ordinary local wait/Link timing; no instantaneous path cancellation or past-event rewrite |

## Exact mathematical candidates and independent operation tests

These finite examples define reviewable mechanisms; their matrices and numbers
are selected test operators, not derived Standard Model interactions. Tests must
not derive the expected answer by calling the implementation under test.

### N0 and N7: transport and timing

Input at tick 4: exact component 7/3, vector (2,-1,0), ready tick 6, selected Port
+X. Expected dispatch at 6, adjacent arrival at 7 with identical values, one
owner at every audit point and no remaining source copy. In a three-Node chain,
there must be no second Link arrival at 7. Control: a not-ready record stays
owned at source only under its explicitly configured delay. Slot demand must
exercise directional pushing rather than capacity waiting, retaining each ID
and complete payload exactly once. Exact occupancy traces require the open
push-tick semantics below to be specified before implementation. No growing
queue or unbounded same-tick cascade is allowed. Test all six Ports, encoded zero, negative decoded value and
periodic crossing. A delay-operator identity control leaves baseline timing
unchanged; changing host worker count must never change model arrival times.

### N1: phase and internal actions

A minimal exact phase operator on two real components is
`J(a,b) = (-b,a)`. Input (3,4) becomes (-4,3); four applications return (3,4),
and squared norm is always 25. In a complex rational profile multiply by an
exact rational phase with unit modulus, preserving its scale. Generic internal
symmetries use a validated finite-dimensional representation and its group law;
physical names do not turn a signed permutation into SU(3) or a weak interaction.
Control: identity has no phase effect; reject a matrix that is claimed norm
preserving but changes (3,4)'s norm. A phase tag without an amplitude consumer
does not establish interference. Link transit does not update phase again if
N1 already accounts for that interval.

### N2: exchange and backreaction

A deliberately minimal reversible candidate is an equal-layout swap:
`(u,v) -> (v,u)`. With u=(3,0,0), v=(0,4,0), outputs are (0,4,0),(3,0,0),
vector sum remains (3,4,0), sum of squared norms remains 25. Both owners are
required. A configured impulse candidate uses `p' = p + j`, `f' = f - j`
with j derived only from the frozen local state. This preserves the declared
sum p+f, but generally does not preserve a kinetic-energy readout. Therefore
it cannot be admitted to a model claiming energy conservation until its full
energy owner/operator passes the independent energy test. Reject rather than
repair a failing proposal. Control: absent coupling gives identity; a missing
field owner, changed persistent guard or one-sided kick fails atomically.

This supplies a generic interaction mechanism. Electromagnetic attraction,
strong binding and weak conversion still require sourced/candidate operators,
representation and experimental targets; they cannot be inferred from the swap.

### N3 and N4: split and recombine without a measurement

Use the exact rational two-mode matrix
`U = [[3,-4],[4,3]]/5`; `U^T U = I`. Input (1,0) gives (3/5,4/5),
with squared weights 9/25 and 16/25. Applying U transpose gives (1,0)
exactly. No draw occurs merely because two output modes exist. The exact
remainders/scales travel with the modes; a material carrier is not duplicated.
Mode IDs and their common coherent state owner remain bounded.

Independent phase control: flip the second branch sign before recombination.
U transpose then gives (-7/25,-24/25), with weights 49/625 and 576/625.
These differ from the unflipped result and still sum to one. In a two-path
experiment the modes must actually leave through Links and arrive back before
mixing. A remote live amplitude or a branch that has not arrived is not input.
For incoherent mixtures, store/use a declared density representation or the
explicit quantum owner; do not add amplitudes from different coherence domains.

An extensive merge example is 1/3 plus 2/3 -> 1 with retained zero remainder.
Control: merge is rejected when mode, phase, internal-state or nonlinear
readouts would be erased; no approximate merge is permitted to fit capacity.
A three-vector alone is not a general many-particle quantum state.

### N5 and N6: funded emission, absorption and conversion

Independent ledger fixture: source scalar stock 10 and vector stock (3,0,0)
emits stock 4 and vector (1,0,0). Retained source is 6 and (2,0,0). Receiver
stock 2 and vector (0,1,0) absorbing that packet becomes 6 and (1,1,0).
This checks exact inventory, not a derived physical energy-momentum relation.
Fractions such as 1/3 must be retained or transferred even when a source stops.

Emission into multiple products supplies all output quantities explicitly and
checks totals before consuming the source. A finite constituent conversion
must also specify type/layout and applicable charge/internal selection rules.
Control: an unfunded emission, unknown channel or missing recoil owner fails
with no partial source debit. An occupied supported product destination follows
the adopted push rule once its precise tick semantics are specified; waiting
cannot be inserted as a fallback. A stopped source
emits no new packet; already emitted packets continue causally. A measurement
does not erase a remote field front before causal information arrives.

### N8: existing quantum action and missing integration

The quantum action is already defined; this section does not request a new
quantum law. Preserve [postulate 14](../POSTULATES.md),
the [event contract](QUANTUM_EVENTS.md) and
[bonded rays](SPATIAL_FIELDS.md#bonded-rays-bonded-ray-field-v1): coherent local
operations do not draw; only an actual external Detector encounter may authorize
and own sampling. A declared instrument can prepare its complete outcomes
and commits the selected conditional state; repeated event commits return the
original immutable result; subsequent physical events move forward in time.
No redraw means the same decision event is not sampled twice and its physical
outputs are not emitted twice. A new contact may create a new event for a
continuing ray, but event creation alone grants no sampling permission; there is no blanket one-draw limit
for the entire life of a ray or an arbitrarily evolving entangled group.
The accepted pair profile uses one shared number per pair. These are distinct
named profiles, not permission to replace one profile with another.

There is a concrete implementation gap: the current bonded-ray registry releases
a pair after its second answer and treats a later request as a new pair. Its
active-pair idempotence therefore does not implement terminal-event replay for
all time. Integration must reject ambiguous reuse or retain the bounded completed
event reference already supported by the event owner. A finite generation bank
must fail before identity aliasing; it cannot silently redraw a completed event
or claim unlimited replay memory. This is reconciliation with the intended
no-redraw contract, not a new probability distribution.

Reuse the named event-spacetime quantum owner; do not copy a joint density into
ordinary Node fields. A Node contributes only arrived support, local settings
and declared local actions. A quantum instrument supplies a complete bounded
outcome set and state updates. Preflight every branch and local capacity before
Detector-owned sampling. Existing generic-contact resolvers without an actual
Detector trigger do not satisfy this rule. A terminal transaction retains a bounded idempotence key; replay
returns its existing result. Failed preparation draws nothing; publication
failure must retain the reserved ticket/result and must not redraw on retry.
The provider needs a prepare/commit contract; a nontransactional random callback
is insufficient. A certain outcome uses the existing certain-outcome convention.

Single-pair shared sampling and a general conditional instrument are distinct
profiles. Do not force arbitrary repeated measurements into one preselected bit.
Do not add hidden draws or replace the external Detector action bit with the
quantum outcome. Model query cost may be one with zero model-time query delay;
actual host memory/work can scale with entangled state size and must be reported.

Acceptance: predeclare one small exact joint state, local instruments, expected
joint probabilities and order-equivalent predictions from independent matrix
algebra. Compare all outcomes, not only marginal means. Control: remove
coherence, use product state, replay, inject provider failure and exhaust local
capacity. A Bell benchmark uses four setting pairs, an independent local
control, no-signalling marginals and a fixed analysis rule. Shared-resource
Bell violation is not a local-only derivation. Communication-assisted Detector
agreement cannot be relabeled a spacelike Bell test. A real experimental target
is [Hensen et al.](https://arxiv.org/abs/1508.05949); this contract does not claim
its assumptions or result have been reproduced by Universe24.

### N9: external Detector and branch cancellation candidate

Preserve the user-selected action meanings: 1=PASS; 0=GENERATE_RETURN.
Action sampling and content generation belong to the external Detector.
PASS does not redraw content. RETURN emits a fresh Detector-origin value through
the incoming Port and advances time. There is no selected default probability,
returned-value distribution, mass-delay law or physical observable implied here.

Candidate interface closure: each named Detector experiment must provide bounded
integer action weights for every eligible local input/lock state, a separate
complete return-content channel, deterministic PASS routing, explicit lock
transition table and bounded Detector waiting time. Unknown table entries reject
initialization. Pure plumbing fixture: weights (PASS=1, RETURN=0) forwards a
SPACE value 7 unchanged; the complementary certain-return fixture generates
configured fresh value 9 without adopting 7. These are explicit test fixtures,
not adopted physical action distributions. A stochastic fixture must declare
its weights and exact expected counts over an exhaustive ticket set. Action
and content draw counts are separate acceptance outputs.

The accepted moving-event return is addressed by event ID. The saved variable
continues being pushed UP the same ray path toward its origin, preserving that
ID and every property; the event is not expired to free a slot. The counter
signal moves DOWN the same path. These directions are path-relative, not global
coordinates or a remote-source search. The user intends the two to meet; this
is an acceptance target, not a proved consequence of unspecified tick semantics.
The prior previous-Port breadcrumb candidate is not adopted as the solution.

The user's additional anti-miss proposal retains presence of the same event in
two adjacent Nodes: its current Node and the upstream Node. Treat this as a
testable two-Node overlap candidate, not two independent events or doubled
conserved inventory. There is one event identity and one actual stock owner;
the second presence is bounded detection/transition metadata. Its fields,
creation tick, expiry/transfer condition and once-only encounter acknowledgement
must be specified before implementation. Each Node may use only overlap
information already locally available through its causal transitions; the
proposal does not authorize a live read of its neighbor. Metadata cannot persist
at successively more Nodes or contain an unbounded past trajectory.

This overlap is intended to detect opposite movers even when their positions
swap in a tick. It is not yet proof of complete encounter coverage, congestion
resolution or bounded bookkeeping. A meeting must create at most one committed
encounter for the event pair even if both endpoints detect the overlap. That
causal once-only protocol, including replay and delayed acknowledgements, remains
to be specified rather than supplied by a global registry for ordinary events.

The bounded per-tick displacement and no-miss/once-only requirements are agreed.
Engineering review must choose the bounded local representation, synchronous
push/reservation and Link-crossing resolution, atomic encounter commit and
origin/periodic-path handling that satisfy them. Do not let host iteration
order invent those semantics or report the agreed requirements as undecided.
Finite identifiers must not alias continuing events; no expiration/reuse policy
is supplied here. Bounded local state cannot be assumed to retain unlimited new
event identities or path histories. Quantum action is already defined and is
not part of these missing transport decisions.

Required independent acceptance cases, with expected tick-by-tick traces fixed
against the concrete engineering resolution:

- **Push chain:** occupied adjacent channels receive slot demands; complete
  variables move UP with one owner each, no dropped properties, no capacity
  waiting and no multi-Link recursive propagation within one elementary tick.
- **Simultaneous pushes:** reverse host traversal and worker ordering for the
  same demands. The declared simultaneous rule must produce the same physical
  trace; no event is duplicated, overwritten or given arbitrary priority.
- **Opposite movers:** start on the same Node, adjacent Nodes and separated
  Nodes. Test even and odd separations. An UP variable and DOWN signal that
  swap Link endpoints must not silently pass without the declared encounter
  handling. Whether this is a Link event or endpoint event remains to be defined.
- **Two-Node overlap:** expose one event ID at the current and adjacent upstream
  Node while counting its stock only once. Exercise head-on endpoint swap,
  both endpoints detecting simultaneously, replay, staggered pushes and explicit
  delay. Require one encounter record/output, no missed admitted crossing,
  no premature metadata removal and no stale presence suppressing a later
  distinct encounter. Fix overlap lifetime and causal arbitration expectations
  before running; do not create them from observed implementation behavior.
- **Full periodic loop:** initialize every allowed channel occupied and apply
  the admissible demand. Distinguish a possible simultaneous permutation from
  an impossible extra stock insertion; no global repair, hidden spare queue,
  overwrite or unbounded cascade is allowed. The valid output trace is OPEN.
- **Explicit delays:** delay a selected Node by its configured rule while the
  counter signal approaches. Only that specified delay permits holding. Define
  encounter timing for delayed/in-flight variables; do not add capacity delay.
- **Origin and identity:** preserve ID and full properties through every push
  until origin; test periodic revisits, duplicate notices and bounded ID limits.
  Stop before aliasing rather than relabeling or expiring the continuing event.
- **Local cost:** vary chain length and elapsed history at fixed channels and
  word bounds. Local work per tick remains bounded; total return latency need
  not be bounded. Diagnostic history is outside the physical local state.

Until these traces are well-defined and pass, neither guaranteed encounter nor
a complete bounded pushing algorithm has been established. In particular,
forbidding capacity waiting does not by itself supply a scheduling algorithm.

## Physical claims and developer handoff

A Node lattice, exact arithmetic and group notation do not establish all physics.
Known quantum cellular automaton work derives specific free-field limits under
additional explicit assumptions; those conclusions cannot be imported into this
candidate just because it also has local updates. See
[D'Ariano and Perinotti](https://arxiv.org/abs/1608.02004).
Physical rest phase and processing delay remain distinct; a rest-energy phase
reference is discussed in [Feynman III, chapter 7](https://www.feynmanlectures.caltech.edu/III_07.html).
No gravitational, electromagnetic, nuclear or mass-latency law is selected here
by naming a scalar, delay or matrix after that phenomenon.

| Handoff | Developer-ready scope | Physical status / remaining owner |
| --- | --- | --- |
| A | Common exact state/ownership contract, N0/N7, selection and atomic failure | Architecture review checks compatibility and lossless gaps |
| B | N1 and rational N3/N4 candidate operators and the exact fixtures above | Experimental physicist supplies finite interference experiment and predeclared acceptance |
| C | N2, N5/N6 generic funded transactions and complete-owner checks | Species-specific physical operator choices remain physicist work, not developer invention |
| D | N8 bridge to the existing quantum owner with transactional sampling | Architecture/physics review must establish admitted composition; no local-only Bell claim |
| E | N9 manifest validation and bounded causal transport candidate | Detector distributions and physical response are explicit per-experiment hypotheses; no universal default |
| F | Catalog-to-manifest support matrix | Every entry marked stored-only, transport-tested, interaction-tested or physically-benchmarked; never infer support from a name |

Implementation readiness here means an explicit finite candidate can be written
and tested after review, not that the candidate is accepted physics. None of the
new fixtures is reported as run. Do not replace failing independent expectations
with outputs from the new implementation. No code or test implementation belongs
to this documentation change.

## Final acceptance: operator, Node and composed board

Every changed specification must retain acceptance at these levels:

1. **Operator:** run its exact numerical fixture and negative control above;
   include zero, signed decoded values, fractional ownership, invalid dimensions
   and the first overflowing intermediate. No state or ticket changes on rejection.
2. **Node:** two or more local participants plus a local field commit together;
   inject an arrival during wait and preserve it. Verify participant reservation,
   directional pushing, explicit configured delays and complete conserved readouts.
   Equivalent commuting actions cannot depend on host traversal order; physically
   noncommuting actions retain their declared causal order.
3. **Links and board:** exercise six directions, periodic crossing, no same-tick
   multi-hop relay, split/recombine only after arrivals, finite emissions,
   absorption, retained remainders and causal cancellation. Check one owner for
   each actual stock throughout. Global diagnostics observe and never repair.
4. **Bounded cost:** report fixed K,D,F,R,A,M,B,Q and arithmetic limits; operation
   count/storage per Node is independent of world size and elapsed history.
   Host scheduling, rendering and joint quantum costs are reported separately.
5. **Evidence:** save exact model identity, input, code revision, structured
   events, expected versus actual outcomes and failed cases. For each simulator
   run requested under the user's visualization requirement, generate and show
   HTML using the existing renderer. A picture alone is not acceptance.
6. **Physical scope:** distinguish configured reference behavior, candidate
   consequences and independently reproduced phenomena. No claim that all
   physics, a nucleus, an atom, a photon or a local explanation of Bell has been
   established follows from passing these software-contract checks.

## Latest target constraints and profile audit

The central model section 3 owns the six independent output clocks driven by
local computation fields; there is no input clock. Earlier shared-clock or
single-wait candidate fixtures in this annex are scoped arithmetic examples,
not an adopted replacement. Each split output needs its own face readiness and
separate fixed neighbor Link transit H. One bounded local update occurs per
tick. The same section owns used-face markers and
separate identity/family-transition metadata; no complete routing algorithm is
implied by a six-bit mask.

Strong/weak operation definitions and the long-residence/computation-field
hypothesis remain in central section 3; see [physical support](PHYSICAL_ENTITIES.md)
for current composition gaps. No ordinary operation samples. Acceptance must
include zero random tickets for all non-Detector actions, deterministic replay,
independent six-face timing and no added input delay. These are target tests,
not evidence of runtime support.

The central closure assigns energy/momentum readouts and coupling conservation
contracts to family definitions; generic complete-owner validation does not put
physical formulas into engine scheduling or NodeState. Existing free-ray
self-exclusion remains active. The separate stationary held-mass-source
candidate supports fresh local emission sampling and nonemitting probes only;
newly output-delayed moving emitters remain unsupported until their exclusion
composition is defined and tested. No candidate numerical law is copied here.
