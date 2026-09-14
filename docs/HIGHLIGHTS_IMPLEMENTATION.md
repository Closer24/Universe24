# Highlights implementation coverage

## The ray: one object for wave and particle - 2026-09-14

This entry maps the straight-ray field and its Kerengonen extension to the
Highlights sections on fields, quanta and the classical limit (1.2, 4.7, 10.3).
It reconciles the repository at main `c3c39d0` after
[PR #98](https://github.com/Closer24/Universe24/pull/98) plus the eight later
commits on the working branch; the live document was not edited.

A ray is a whole amount of one scalar field with a fixed integer heading and
three routing accumulators that keep it on one lattice line, one link per tick.
With the `kerengonen` key it also carries a phase that advances per link, and
each ray may carry its own advance, stamped at emission from an expression over
the emitter's fields (`|p| / D` is the de Broglie rule). Rays that meet at a
Node combine by phase; the coherence of what met, from a fixed-point integer
cosine table, gates the value a reader samples and the share an absorber
takes. Amounts are never changed by phase: the audit sums quanta. Absorption
is a run-time choice, the coherent share or a whole-ray lottery drawn by a
record-row ticket. A record that absorbs keeps the phase, advance and heading
of what it took: an emission may carry that phase on (a Huygens slit), send
the amount back along the mirrored heading (a mirror), or pay a record out on
a schedule (`dissolve`: a particle becoming its own wave train).

| Highlights sections | Implemented contract and limits | Repository owner |
| --- | --- | --- |
| 10.3.2 | Straight rays: isotropic inverse square, shell conservation, a small stock sweeping the heading sequence in turn. | [Straight-ray contract](SPATIAL_FIELDS.md#straight-ray-transport-isotropic-ray-field-v1) |
| 4.7, 10.3 | Energy closure: funded emission with recoil, absorption with momentum, signed quanta paid by the absorber, rays measured as quanta by the event audit. Attraction that the pulled body pays for. | [Funded emission and absorption](SPATIAL_FIELDS.md#funded-emission-and-absorption), [gravity probe](../examples/gravity-probe/README.md) |
| 1.2, 4.7 | Kerengonen phased rays: coherence-gated sampling and absorption, share or lottery capture, Huygens slits, mirrors, per-ray de Broglie advance, dissolution. Identity `kerengonen-ray-field-v1`. | [Kerengonen contract](SPATIAL_FIELDS.md#kerengonen-phased-rays-kerengonen-ray-field-v1) |
| 1.2, 4.7 | Measured: two-lamp and single-lamp double slits with exact additivity without phase, single quanta building the fringe, fringe period inverse to momentum for beams and for a dissolving particle, standing waves with period `phase_steps / (2 x advance)`, a thick screen absorbing what a thin one lets pass, a round front and a Euclidean fringe on the Euclidean pace. | [Double slit](../examples/kerengonen-double-slit/README.md), [de Broglie](../examples/de-broglie/README.md), [matter wave](../examples/matter-wave/README.md), [mirror](../examples/kerengonen-mirror/README.md), [Euclidean pace](../examples/euclidean-pace/README.md), [validation](VALIDATION.md) |
| 1.2, 10.6 | Quantum-to-classical seams on existing rules: a dephased walk equals the classical chain, quanta click whole and average to the inverse square, repeated captures follow the geometric decay law. | [Quantum-to-classical probes](../examples/quantum-classical/README.md) |

What the ray is not, recorded rather than claimed: a single particle's matter
lands spread as its wave, not at one Node, because rays carry conserved stock
at link speed and no local rule can retire the rest of a wave when one Node
captures without a faster signal; a mirror reflects across a lattice axis or a
lattice diagonal, whole or by a fraction, not at an arbitrary angle; fringes
follow Manhattan path difference on the links metric and Euclidean path
difference on the [Euclidean pace](SPATIAL_FIELDS.md#euclidean-pace-metric-euclidean)
(`euclidean-ray-pace-v1`), where rays wait at Nodes and are slower, never
faster, than one link per tick; the lottery ticket is a configured local
sequence, not physical randomness; the event audit re-measures every owner per
event, so audited worlds stay small.
The `|p| / D` rule and every mixer are configured laws, measured to hold, not
derived. Exact sources and completed checks are in
[validation evidence](VALIDATION.md).

## Causal quantum source envelopes - 2026-09-13

The user's latest selection extends the preceding localized-source choice:
each wave mode may source an ordinary field with its local squared weight, and
weight changes or cancellation must travel through Nodes and Links with delay.
This maps Highlights sections 1.2.7, 4.7.1-4.7.7 and 10.3/10.6 to the explicit
[causal source candidate](CAUSAL_QUANTUM_SOURCES.md). The live document remains
read-only; this reconciliation reuses the same-hour read at revision
`ANLCKQlo9slgaScJWuZCbzOF1YiWfHysY-vP-NhMlUFzFa10_DrgmhOoK5onyxvmYeBwWJdovQJJm4If_lGbAJCgJ7HzWLE1j14J4YJjmiY`,
modified `2026-09-13T18:53:30.879Z`.

`causal-contact-fields-v1` retains a bounded complex source envelope at each
participating ordinary Node, immutable definitions outside NodeState, finite
allowances and fixed packet/proposal slots. Actual contact creates the source;
successful local absorption creates one full-strength ordinary output and sends
terminal notices over physical Links. Existing field stock continues. Shared
origin status remains quantum bookkeeping and never controls remote ordinary
emission, response or delay. The older localized-only profile is unchanged.

After measurement the local source weights are retarded and may be unnormalized;
their sum is not conserved charge or proof of field/matter energy closure. The
candidate preserves one inventory owner and specifies separate source accounting,
phase-sensitive propagation, causal termination and unsupported combinations.
Its implementation owners and numerical acceptance expectations are linked from
the contract. Exact source, completed runs and review outcomes belong in
[validation evidence](VALIDATION.md); no pending test is represented here as a
passed result. This extension does not complete the broader unified-dynamics goal.

## Localized quantum contacts - 2026-09-13

Live Highlights was reconciled read-only at revision
`ANLCKQlo9slgaScJWuZCbzOF1YiWfHysY-vP-NhMlUFzFa10_DrgmhOoK5onyxvmYeBwWJdovQJJm4If_lGbAJCgJ7HzWLE1j14J4YJjmiY`,
modified `2026-09-13T18:53:30.879Z`. Its sections 1.2.7, 4.7.1-4.7.7 and
10.3/10.6 map to the [localized contact candidate](LOCALIZED_QUANTUM_CONTACT.md).
The later user selection explicitly chooses ordinary fields only at localized
events. This finite hybrid is an additional configured candidate, not a claim
that the project's separate goal of emergent unified dynamics is complete.

Actual local source contact creates an origin only at committed event time.
Finite coherent domains retain one configured inventory through number-preserving
operations; a complete local absorption instrument transfers it into one ordinary
record. Existing classical fields evolve causally. Quantum probabilities never
reconstruct or erase remote ordinary field stock. Definitions, implementation
owners, tests and configuration are linked in the candidate contract.

The separate predecessor list remains absent. Node state adds only a bounded
reservation token; six-entry origin banks and immutable event history retain their
owners. Common local field reactions preserve every coupled resident, including
third participants, and all alternatives validate before sampling. Unknown
momentum is explicit; no sharp momentum or physical energy is inferred from a
position record. Public snapshots serialize with event-backed commits and expose
possible support separately from localized charge.

The focused acceptance suite covers fifty-one numerical and failure cases, including
3:4 interference, exhaustive Born tickets, delayed ownership, external-field
exchange, finite emission, six periodic directions and unchanged unconditional
receiver statistics. The authoritative run/gate evidence belongs in
[validation](VALIDATION.md). Full quantum fields, unrestricted no-signalling,
exterior quantum escape and shared Node clock composition remain outside scope.
The live Google Doc was not changed. Its section 11 reports other unmerged
branch candidates; those results are not imported or claimed by this change.

## Quantum origin cells and event spacetime - 2026-09-13

Live Highlights revision
`ANLCKQm21ChtG5HceOfGOhoBYGoFe1Cevq9Birt---q9RtLGv682cdVsad6nwquwgJtGWbHqSKP2pw9ExatR-Mlf533Guti25QsAZLMtJ0c`
was reread; its modification time was `2026-09-13T15:06:39.393Z`. Implementation
starts from `fb54f3306ce8172f5ed3f2d3a65eb03cb021a6b7`, integrating current main
`2c20d00094639263fbe387c0a62420dcef108285` with the prior Node-event work.

The user's later explicit contract replaces the separate per-stream predecessor
list. Sections 1.2.7 and 4.7.1-4.7.6 now map to
[event spacetime](QUANTUM_EVENTS.md#event-spacetime-and-current-references) and
[origin cells](WAVE_ORIGINS.md): immutable events are the sole history, each
participating Node stores up to six origin IDs, and a direct origin status check
does not traverse a history. Current virtual-register heads remain separate
bounded state. One conditional terminal decision atomically resolves its selected
origins; peers prune their local references on their next native tick. Every v3
gate declares participating origins. Unarrived support cannot execute the gate;
suppression after resolution requires unchanged complete correlated density.
A retired instrument also needs an explicit `null_outcome` that is certain and
preserves that density. Unsafe suppression fails. One origin may describe several
disturbances; interaction lists accept one to six names, not a particle count.
Untagged gates and the older carrier bindings are rejected in
this profile. Continuing outcomes retain the conditional state and do not assign
sharp momentum after a position record. Origin bookkeeping does not grant an
ordinary remote field read.

Explicit matrices and exact joint state retain interference and correlation.
Component checkpoints preserve phases, origin identity and individual Link
readiness. `examples/quantum/event_paths.json` retains the four-Node coherent,
phase, record and checkpoint cases; the v3 origin contract specifies the new
local-capacity, contention, conditional-sampling and pruning acceptance checks.
The terminal policy stops future operations requiring its named origins; it does
so only through the guarded contract. The example instrument explicitly resets
occupation on its terminal branch; this is not a derived absorption or energy law.
Direct origin lookup is O(1); cancellation certification is separately counted
quantum-owner work, without an added physical observer or carrier-delay channel.
Check results require the exact tested tree and completed validation evidence.

This is a finite configured candidate. It does not establish spontaneous free
dynamics, a universal trigger or conservation law, general field composition,
full Focus, host O(1) evaluation or bounded total memory for infinite spacetime.
The live Google document was read only; its text was not changed by this
repository reconciliation.

## Quantum time-direction clarification - 2026-09-13

Highlights sections 1.2.7 and 4.7 distinguish direct origin relevance lookup
from deferred quantum evaluation. Neither is reverse physical-time computation.
Required stored dependencies and recorded constraints are collected as bounded
host work; their recipes evaluate forward from sources or exact checkpoints.
Earlier events and outcomes are not rewritten or resampled.

This terminology review uses merged main
`63983788140bc06d5e8f581e3609c0520c00f43b` and the then-reported
`Quantom -> Classic` run in [PR #91](https://github.com/Closer24/Universe24/pull/91),
head `49bcbc74c69a47814945efce8600edbc824ee04f`. PR #91 was open and unmerged
at review. Its `local-quantum-events-v3` candidate removes separate chronological
predecessor lists and `history(register)` traversal, while retaining immutable
events and quantum dependencies. Direct event-ID/status lookup is O(1); full
retained-state evaluation and cancellation certification are separate host work.
Source resolution adds a later write-once status without rewriting the source.

The PR reports `wave_origins.json` completing 5/5 ticks in 0.0123118 seconds:
one outcome draw, origin 3 resolved at tick 2 to record 13, peer references retired
at tick 3, and origin 4 still active. Three oracle calls include two cancellation
certifications. These are branch-reported results, not a new experiment in this
documentation task or proof of a universal quantum-to-classical limit.
See [the quantum contract](QUANTUM_EVENTS.md#time-direction-and-origin-lookup).
The Google Doc receives the same clarification in sections 1.2.7, 4.7.2 and 4.7.7.
No reaction law or evaluation algorithm changes in this correction.

## Latest synchronized snapshot - 2026-09-13

This is the repository implementation map for
[Universe 24 Highlights](https://docs.google.com/document/d/1IkhSyqZZMBSgbJV-PMMwcXG0D_Rlfg4FrLy2jXBMUSs/edit),
not a second specification or an automatic live mirror. Both this map and the
Google Doc were reconciled against main
`cc042ce6c51a34775c292371538c5cd6acd4e423`, including merged
[PR #89](https://github.com/Closer24/Universe24/pull/89),
[PR #90](https://github.com/Closer24/Universe24/pull/90) and
[PR #92](https://github.com/Closer24/Universe24/pull/92).
The older entries below retain their historical source and validation scope;
their statements that the live document was not edited refer to those earlier tasks.

### Current implementation coverage

| Highlights sections | Implemented contract and limits | Repository owner |
| --- | --- | --- |
| 2.2.1-2.2.2 | Bounded integer physical inputs and intermediates; shared SI unit/constant registry prepares Scalar/Vector values outside physical stepping. Explicit conversion errors are separate from measurement uncertainty. Model time h is not Planck action. | [Reference units](REFERENCE_UNITS.md), [architecture](ARCHITECTURE.md) |
| 3.3.4, 3.5.5, 4.3.1 | Declared aggregation, indexed local participants, joint carrier/field proposals and complete-owner conserved readouts. Nonlinear balances use actual before/after state; labels do not supply physical laws. | [Node processor](NODE_VECTOR_PROCESSOR.md) |
| 4.4.1-4.4.2 | Explicit k*h Node execution and optional shared field/carrier cost-budget timing remain separate, incompatible modes. Waiting input has bounded destination ownership. | [Node processor](NODE_VECTOR_PROCESSOR.md), [shared clock](SPATIAL_COMPUTATION_DELAY.md) |
| 4.4.3 | Emission can read the Node's last committed work. Configured received-Port response exchanges momentum with a local field register; this is not derived gravity or physical energy. | [Computational response](COMPUTATIONAL_RESPONSE.md) |
| 6.5-6.7, 10.10 | Node-owned commits, immutable worker planning, deterministic barriers and bounded physical-owner memory have scoped tests. Total host memory and full-world work are separate costs. | [Architecture](ARCHITECTURE.md), [validation](VALIDATION.md) |
| 10.3.1 | Schema 2 localizes attenuation residue by default. Explicit dissipate retains the earlier loss policy. Stationary deposits remain owned inventory and are not sampled by local rules. | [Spatial fields](SPATIAL_FIELDS.md) |
| 10.3.2 | Scalar straight-ray transport retains heading and integer routing phase; ray_slots bounds resident capacity. Unsupported vector, octant-seed, field-rule, joint-interaction and alternative-clock combinations are rejected. | [Straight-ray contract](SPATIAL_FIELDS.md#straight-ray-transport-isotropic-ray-field-v1), [ray tests](../tests/test_ray_field.py) |
| 10.9, 10.11 | Sourced particle reference data, explicit representation profiles, preflight, finite quantum events and read-only observers remain distinct from verified species dynamics. | [Entity catalog](ENTITY_CATALOG.md), [project status](PROJECT_STATUS.md) |

### Merged field changes and evidence

PR #90 adds `residue: localize`, selected when a schema 2 decay definition omits
the key. At completed interior arrival, the removed fraction becomes bounded
stationary stock at the receiving Node. It is included in inventory, not
dissipation; moving flux still diminishes. Explicit `residue: dissipate` selects
the earlier loss law. Open exit, signed components, source allowances and in-flight
ownership retain their separate accounting. The 40-tick finite-source run
accounted for 720 emitted units as deposits, with zero dissipation. Tests include
signed vectors, mixed residue policies and overflow rejection without partial
receipt. Neither a component ledger nor a stationary deposit establishes physical
field energy or a gravitational law.

PR #92 adds `transport: ray` under `isotropic-ray-field-v1`. A source sweeps
configured integer headings using its emission cursor. Each ray retains its
heading index, three integer routing accumulators and amount while moving over
adjacent Links. Matching heading and phase may merge; capacity exhaustion fails.
Ray fields currently reject vector payloads, octant seeds/weights, field rules,
spatial interactions, `node_execution` and `spatial_computation_delay`.

The published [inverse-square probe](../examples/inverse-square/README.md) reports
a 41-cubed open world with 4,096 headings, 64 rays per tick and a 64-tick measurement
sweep. Finite fitted slopes are -2.25, -2.05 and -1.92 on the axis, face diagonal
and body diagonal. Angular-patch coefficients of variation are 6-8 percent over
72 patches at tested radii. This statistic is not a maximum error bound or exact
isotropy; individual nodes show greater variation. These are reported world/event
audit measurements of stock, not operational observer records or an independent
rerun in this documentation task. Scalar shell stock is not oriented surface
flux, and finite fits do not establish asymptotic scaling, mass coupling,
attraction, Newton's law or physical energy conservation.

### Unmerged amendments remain separate

The live document's section 11 contains branch-reported self-field policies,
carried allocation phase, scattering and collision results. Its cited
[PR #93](https://github.com/Closer24/Universe24/pull/93), head
`7149ec961df330b460dd3dc7262c4a98c5c17221`, was open and unmerged when checked
against the main commit above. The live section now states that scope explicitly.
Its findings are retained without being promoted to merged-main capabilities or
independently revalidated physical results. This sync does not merge PR #93.

The Google Doc update adds sections 6.7 and 10.3.1-10.3.2, reconciles the prior
decay accounting bullets, and labels section 11's branch scope. Existing Node,
unit, quantum and pending-hypothesis content is retained. Documentation-only
validation applies here; no simulator behavior or experiment input changes.

## Joint local reaction contract - 2026-09-13

The live source was reread at revision
`ANLCKQluUGX_afG63QQM9IQBX-qmjBbhP-b8UVvMJ-mCjZQ30ZYQ_Kkyk4MKp-O_P1PvMixFu3_pO-w-dDxrnekqUXbwar_XXVKECHy5vBA`.
Implementation base: `a7a0000e3005ae41b37639f5dcf76e56532be69f`.
Sections 3.1, 3.3 and 4.3 motivate the bounded property-selected
[joint Node reaction](NODE_VECTOR_PROCESSOR.md#local-rules). The user's explicit
reaction contract refines delayed execution: one group reads several carriers
and fields from one snapshot, and each frozen substep must still pass its
declared invariants and optional persistent condition before atomic commit.
Start triggers remain separate. The supplied register-rotation example checks
externally defined readouts; it does not derive physical species, energy laws or
quantum behavior. No live Highlights text was edited.

## Integer Node timing reconciliation - 2026-09-13

The live Highlights source was read again with modification timestamp
`2026-09-13T05:10:29.655Z`; integration started from main
`bb177121ec2efdc6c998a8290b9e7b09c7706c62`.
Sections 3.2, 3.3 and 4.3 motivate bounded generic local properties and rules.
The user's subsequent explicit h/k clarification selects the new
[Node profile](NODE_VECTOR_PROCESSOR.md): h is one hop; k is configured per
interaction, independently of operation cost. This supersedes the cost-derived
k description in section 10.6 for the opt-in profile only. Node vector width is
also explicitly generalized while world topology remains the current six-port
lattice. Section 1.3's distinction between assumptions, tested consequences and
emergence claims remains binding. The live document was not edited.

## Shared field computation cycle reconciliation - 2026-09-13

The live Highlights revision
`ANLCKQluUGX_afG63QQM9IQBX-qmjBbhP-b8UVvMJ-mCjZQ30ZYQ_Kkyk4MKp-O_P1PvMixFu3_pO-w-dDxrnekqUXbwar_XXVKECHy5vBA`
was read against source base `1784acdd140f260c0fb5e568b2e28241df573fa2`.
Section 4.4 maps to the opt-in
[shared field/carrier cycle](SPATIAL_COMPUTATION_DELAY.md): C counts combined
local work once, one integer ceiling sets the entire cycle, proposals stay
frozen and later input belongs to the next cycle. Section 3.5.3 maps to
distinct waiting, input-buffer and transit owners in inventory.
The empty-input stream is implicit zero and allocates no event history.
This timing candidate does not establish nonlinear energy conservation,
gravity or quantum/spatial composition. The live document was not edited.

## Property coupling and local conservation reconciliation - 2026-09-13

The live Highlights document was read at revision
`ANLCKQluUGX_afG63QQM9IQBX-qmjBbhP-b8UVvMJ-mCjZQ30ZYQ_Kkyk4MKp-O_P1PvMixFu3_pO-w-dDxrnekqUXbwar_XXVKECHy5vBA`.
Source base: `ed65f829a6ddc797cafec1bf34156ca59bdcb7dd`. Sections 10.2, 10.5,
10.6 and 10.7 map to [property selection](PROPERTY_COUPLINGS.md), shared explicit
entity profiles and [passive local conservation](LOCAL_CONSERVATION.md).
The clarified user rule requires joint energy/momentum and actual boundary flux;
internal transfer is not an external source and checking cannot repair a law.
The audit detects violations after committed owner changes. Per-rule validation
no longer sets computation delay. Catalog metadata remains formula-free;
experiment profiles define their own quantities and elementary assignments.
No physical species law or universal proof follows. The live document was not edited.

## Coupled excitation candidate reconciliation - 2026-09-13

The [unit-excitation probe](COUPLED_EXCITATIONS.md) applies Highlights sections
3.2, 3.3, 3.5 and 4.3: independently owned field/internal states exchange through
local generic operations and a coordinated commit. A local capture gate retains
the input while a carrier computation is pending. This is a configured mechanism
under the unverified emergence hypothesis in sections 1.1.3 and 1.3.3, not a new
claim that electron/photon dynamics or quantum occupation have emerged.

The live document was read on 2026-09-13 at revision
`ANLCKQmE1CS353UW3vWf9cdweVRw0CiohpQ85_euvi1zz8TP_ijhldHMIs45KNJzO19_xt67LnVLnj03t2IyvWRQ8kS8TCH8jcFGKfmj3UE`.
Source base: `6a2816526083c23069bf3b0f3fcb6a9dc5b17944`. The finite unit-state,
single-packet and held-receiver restrictions belong to this experiment. No core
law, catalog measurement or live Highlights text changes in this work.

## Configuration validation reconciliation - 2026-09-13

The [read-only preflight](CONFIGURATION_VALIDATION.md) implements explicit input
rejection and shared ownership under Highlights sections 4.5 and 10.7. It validates
configuration data without generating a physical state or inferring a law from
catalog measurements. Passing preflight remains distinct from the verified
behavior and physical hypotheses in sections 1.3 and 6.3. The live document was
read on 2026-09-13 at revision
`ANLCKQnu00jY0NhSjcfyTkt2A8oPZs3_d4dpkEsZ7TI37moZ-eXNntyf4MfeRPttXmu_vnMlIlwe1xt0qmZsn1KXkJoxrMoESFC4_eG9MWA`.
Source base: `521b63567d186bab2fac982a1e1f9d0a592a73a5`. This is a host validation
and Skill workflow change; it adds no physical law and does not edit Highlights.


## Physical reference catalog reconciliation — 2026-09-12

The version 2 [entity catalog](ENTITY_CATALOG.md) expands descriptive coverage
without supplying physical evolution laws. Sourced measured properties remain
external comparison targets. Possible interactions describe channels and their
conditions; the simulator still needs explicit elementary operations and evidence
of emergence. The original 46 experiment profiles move to a separate file.

This implements the Highlights goals of deriving effective laws from local
operations, preserving generic field/type definitions and separating established
physics from hypotheses and verified results. The live document was read on
2026-09-12 at revision
`ANLCKQnu00jY0NhSjcfyTkt2A8oPZs3_d4dpkEsZ7TI37moZ-eXNntyf4MfeRPttXmu_vnMlIlwe1xt0qmZsn1KXkJoxrMoESFC4_eG9MWA`.
This repository update does not modify that document or claim additional derived
physics. Source base: `98b774ac3b02aa5cd350d5513b1e1fddbe3a2c81`.

## Historical implementation inventory

This versioned companion records the implementation inventory added to
[Universe 24 Highlights](https://docs.google.com/document/d/1IkhSyqZZMBSgbJV-PMMwcXG0D_Rlfg4FrLy2jXBMUSs/edit).
Scope: main `09464b41b2c44a191aa2fcbdf4b036680bd646a5`.
The live document was updated on 2026-09-12 with section 10 below, preserving
all earlier paragraphs. Verified revision:
`ANLCKQkcdo3E9Q9qA92kvEzUjmFE9kJmMiJsmZQ8jTo0wroDlz5YbBRcKpGlvLu6PDzqvRncp0x2R4ecCgECBJFygKGssxx8uQW2M6WYTQg`.
Highlights is the high-level specification; linked contracts define exact schemas
and rejection cases. Neither a prose document nor Git restores credentials or
expired outputs. Together, this map, the contracts and versioned initialization
files allow reconstruction without chat history.

This is a dated inventory for the revision above. Later native event programs,
local probes and internal path changes are described in [project status](PROJECT_STATUS.md),
[the documentation index](README.md) and [migration](MIGRATION.md). Preserve this
record as historical evidence rather than treating its omissions as current gaps.

This is a dated inventory for the revision recorded above. Later native event programs,
quantum entity support, Maxwell research examples, local probes and internal path changes
are described in [project status](PROJECT_STATUS.md), [the documentation index](README.md)
and [migration](MIGRATION.md). Preserve this record as historical evidence rather than
treating its omissions as current gaps.

## 10. Implemented entities and rules

### 10.1 World, nodes and links

- The active world is a bounded three-dimensional lattice with six directed
  neighbor ports: +X, -X, +Y, -Y, +Z, -Z.
- A node owns bounded resident records, field stock, residuals and pending local
  proposals. A link owns dispatched payloads until their fixed arrival tick.
- Periodic boundaries wrap all three coordinates. Open boundaries remove outgoing
  contents and record their escaped quantities; they do not reflect or reinsert them.
- Integer value, field, type, slot, expression and rule limits are validated.
  Exhaustion or overflow is an error, never silent deletion or unlimited allocation.
- Addresses route events; ordinary local laws cannot query distant state.

### 10.2 Field definitions and disturbance records

- A field declares its label, one or three components, units, scale, signedness,
  extensivity and whether its quantity is conserved. Labels select no physical law.
- Signed values and zero use positive integer payload codes internally. External
  JSON and diagnostics expose decoded values, including negative vector components.
- A disturbance type selects fields, defaults, local updates and transport policy.
  Seeds instantiate typed records at configured nodes.
- Transport may hold a record, move a whole record or distribute declared contents
  according to its policy. Direction, six routing weights and a scalar/vector
  payload are different concepts. No floating-point normalized vector is required.
- Rate accumulators and integer residuals preserve discrete allocations over time.
  They are physical bookkeeping, not accumulated computation debt.
- Mass, charge, momentum and emission in examples are configured quantities.
  The engine does not recognize electrons, protons or physical material classes.

### 10.3 Spatial fields and finite propagation

- Spatial fields separate immutable background from dynamic contributions.
  Background is observable locally and excluded from dynamic decay.
- Outward propagation uses bounded directional populations, including eight octant
  channels, and routes allocated amounts through six links. Six ports do not mean
  every field must contain six vector components.
- Scalar/vector payload sign is preserved on receipt; the receiving face does not
  automatically reverse it. Opposing directional populations can coexist.
- Emissions add configured field amounts. In schema 2, finite emission and reaction
  allowances prevent an inexhaustible source; dynamic fields have declared decay.
- Unsigned dynamic stock cannot decay below zero. Signed components retain their
  declared sign semantics; dissipation is tracked component by component.
- Conservation includes resident and in-transit stock, configured sources, recorded
  dissipation and escaped quantities. A balanced decay ledger does not mean the
  remaining physical inventory is conserved indefinitely.
- Self-field attribution is not implemented as a general source-identity filter.
  Arrival order is not a general proof of ownership after turning or periodic return.
  A ray field's `self_exclusion` subtracts a departing emitter's own one-link rays
  on arrival, from its own registers only.
- A ray is a whole amount on one lattice line; with `kerengonen` it carries a
  phase and its own advance, combines by phase where rays meet, and is absorbed
  whole or by its coherent share. Slits, mirrors and dissolving particles are
  emissions that carry the absorbed phase, heading or schedule on.

### 10.4 Local field rules and field groups

- Schema 1 optionally supports retained local fields alongside outward fields.
  Schema 2 rejects local field rules and joint spatial interactions; policies are
  distinct candidates and cannot be silently mixed.
- Field groups give related scalar/vector fields a logical label. Groups neither
  duplicate stock nor implement an electromagnetic law.
- Local rules read retained values and completed incoming values independently
  for all six travel channels. They may also read outgoing proposals from earlier
  rules in the same phase.
- Assignments replace retained dynamic stock or an explicitly selected outgoing
  payload. Background is not an assignable stock.
- Expressions, conditions, ordering and invariants are bounded configuration data.
  No arbitrary Python or hidden neighboring-node read is accepted.

### 10.5 Couplings, interactions and rotation

- Local updates and pair exchanges use generic integer expressions, coefficients
  and retained remainders. Sources must be declared.
- Atomic pair interactions evaluate coordinated assignments from a frozen pair and
  validate configured invariants before commit. A failed transaction cannot apply
  only one participant's change.
- Spatial exchange and exact quarter-turn response change a carried vector and
  account for the corresponding field reaction within the selected policy.
- Joint carrier/field interactions can assign carried and local/outgoing field
  quantities with declared invariants and guards. Validation and commit cover the
  participating state together, including delayed proposals and competing inputs.
- Momentum conservation requires the configured component balance across all
  participants. Preserving vector magnitude alone does not conserve momentum.
- The unequal-mass collision example supplies its elastic law and energy invariant
  in JSON; its successful outcome is not evidence that collision laws emerged.

### 10.6 Cost, timing and ownership

- Each declared model primitive has a configured positive cost. A local carrier
  cycle sums its work C and compares it with budget B.
- With link time tau, k = max(1, ceil(C/B)); additional wait is (k-1) tau and the
  subsequent link transit remains tau. Already dispatched arrivals never slow down.
- Pending proposals remain fixed while waiting; newly received inputs are handled
  according to the scheduling and transaction contract, never read from the future.
- Carrier and field phases have separate clocks and recorded costs. Do not infer
  that a spatial field named computation automatically measures all engine work.
- The optional cost-reporting field belongs to a held nonconserved scalar record.
  A separately emitted computation field requires an explicit configured law.
- Host elapsed time, visualization work and global diagnostics are not model costs.

### 10.7 Initialization, results and display

- Initialization selects model identity, schema, boundaries, capacities, timing,
  costs, field/type definitions, seeds, transport, emissions and applicable rules.
- The prepared simulator reads new JSON without compilation. Unknown definitions
  and incompatible policies fail explicitly.
- Normal runs save the input, event trace, final state and run metadata. They check
  combined quantity accounting at each completed tick and retain failure evidence.
- The runner can submit each active Node's immutable disturbance and spatial-field
  plan to isolated Python interpreters. A tick barrier and address-ordered commit
  preserve the serial result. Shared delayed field/carrier cycles use two planning
  barriers before their joint commit. Host worker counts never change modeled local cost.
- Visualization is opt-in. Playback and workspace consumers read recorded labels,
  values, groups, positions and transfers without changing physical state.
- Views distinguish resident records from fields and in-transit payloads, and
  display signed loss/escape accounting without confusing dissipation with failure.
- Saved configuration editing must preserve references when fields are renamed.
  Arbitrary labels and declaration order must not select hidden behavior.

### 10.8 Research scope and reproducibility

- Historical scalar, linked, balanced and causal-stream APIs remain explicitly
  named comparisons, not default laws of the generic Simulation.
- Quantum and Focus modules have separate research contracts. They do not authorize
  nonlocal ordinary fields or establish real quantum input, Maxwell equations,
  emergent gravity or a complete physical theory.
- Reproducible examples include approaching/parallel motion, spreading, configured
  elastic collision, three carriers with finite fields, and both boundary modes.
- Check renamed and reordered configurations, integer limits, residuals, local
  transaction failure, rotation, signed balances and generic result consumers.
- Run the recurring genericity procedure from the repository skill. Report exact
  source identity and coverage; finite passing tests do not prove universal behavior.
- Preserve source, specifications, skills and original configurations in Git.
  Generated results expire under the 24-hour policy; idle cleanup needs a scheduler.

## Coverage map

### Local observer reconciliation

For the [local reception observer](LOCAL_OBSERVER.md), Highlights was reread on
2026-09-12 at revision
`ANLCKQnu00jY0NhSjcfyTkt2A8oPZs3_d4dpkEsZ7TI37moZ-eXNntyf4MfeRPttXmu_vnMlIlwe1xt0qmZsn1KXkJoxrMoESFC4_eG9MWA`.
Sections 2.1, 4.6, 5.1-5.2 and 10.7 require discrete connected nodes, causal
delivery and read-only output. The probe records completed local inputs and
preserves exact playback prefixes. The user's event-time interpretation
motivates a local cycle counter; perceived time and a derived spacetime remain
hypotheses. The live document itself was not edited by this implementation.

### Directional-wave candidate reconciliation

Read the live Highlights on 2026-09-12 at revision
`ANLCKQnu00jY0NhSjcfyTkt2A8oPZs3_d4dpkEsZ7TI37moZ-eXNntyf4MfeRPttXmu_vnMlIlwe1xt0qmZsn1KXkJoxrMoESFC4_eG9MWA`.
The [directional-wave contract](DIRECTIONAL_WAVE.md) is a new explicit candidate
under sections 3.3, 3.3.2, 3.5, 10.4 and 10.5. Six transverse directional modes,
bounded vector operations and local encounter guards preserve the declared
U=sum of squared mode amplitudes and P=sum of their direction-weighted energies,
with resident and in-flight ownership counted once. Same-law cubic rotations and
periodic return are tested. E/B are derived readouts, not duplicated stock.

The candidate demonstrates conditional polarization interaction and declared
balances. It does not promote the emergence hypothesis to a verified physical
law, or claim Maxwell dynamics, charge response or trajectory scattering.
The [configuration Skill](../skills/simulation-configuration/SKILL.md) supports
section 10.7 with reusable input definitions and separate recording/display controls.
Its commands and template are executable evidence; technical workflow remains in
the repository. This reconciliation does not edit the live Google document.

### Local Maxwell research reconciliation

For the [configuration-only Maxwell experiment](../examples/maxwell/README.md),
Highlights was reread on 2026-09-12 at live revision
`ANLCKQnu00jY0NhSjcfyTkt2A8oPZs3_d4dpkEsZ7TI37moZ-eXNntyf4MfeRPttXmu_vnMlIlwe1xt0qmZsn1KXkJoxrMoESFC4_eG9MWA`.
Sections 1.3.3, 1.3.4 and 10.4 are reconciled as follows: the existing generic
local field interface can express a transverse reflection and one-link
streaming hypothesis without adding an engine field equation. Conditional
leading vacuum dynamics and small-space mode frequencies agree with the
independent forecast. Exact centered Gauss conservation, complete macroscopic
energy, physical light speed and indefinite bounded-integer mixing remain gaps.
The experiment does not promote full electromagnetic emergence to a verified
result. This entry records repository coverage; it does not claim a live
Highlights edit or replace the earlier revision record above.

### Source contracts and evidence

| Highlights section | Authoritative contract / implementation owner | Evidence owner |
| --- | --- | --- |
| 10.1 | [Disturbances](DISTURBANCES.md), core/topology.py | test_open_boundaries.py, test_boundary_configuration.py and architecture tests |
| 10.2 | [Disturbances](DISTURBANCES.md), core/disturbance_state.py | test_generic_identity.py |
| 10.3 | [Spatial fields](SPATIAL_FIELDS.md), fields/spatial.py, fields/spatial_decay.py | finite-field and spatial transport tests |
| 10.4 | [Local field rules](LOCAL_FIELD_RULES.md), fields/local_field_rules.py | test_local_field_rules.py |
| 10.5 | [Spatial couplings](SPATIAL_COUPLINGS.md), fields/spatial_interactions.py | test_spatial_interactions.py, test_atomic_interactions.py |
| 10.6 | [Definitions](../SIMULATOR_DEFINITIONS.md), core/disturbance_engine.py, core/spatial_engine.py | disturbance and spatial scheduling tests |
| 10.7 | [Workspace](WORKSPACE.md), runner.py, diagnostics/disturbance_render.py, ui_assets | test_workspace_integration.py, test_recorded_movie.py |
| 10.8 | [Architecture](ARCHITECTURE.md), [recovery](RECOVERY.md), [regression skill](../skills/regression-check/SKILL.md) | [test expectations](TEST_EXPECTATIONS.md), [validation](VALIDATION.md) |
