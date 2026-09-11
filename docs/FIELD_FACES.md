# Delivered field faces: integration contract

Base: `7de319b`. This migration separates a local response interface from each
field's transport law. It is not yet an accepted new default: the combined
field-response-motion causal gate must pass before promotion.

Current unit-link matter scheduling uses
[bounded link ownership and delayed acknowledgements](CAUSAL_MATTER_TRANSPORT.md).
It corrects the tested competing-arrival feedback. The
[self-response investigation](SELF_RESPONSE_BLOCKER.md) remains blocked.
The precursor staging and failure descriptions below are historical context,
not a claim that the corrected unit-link scheduler still fails that contention case.

## Authoritative Highlights direction and remaining gaps

The user instructed this work to follow the current
[Highlights document](https://docs.google.com/document/d/1IkhSyqZZMBSgbJV-PMMwcXG0D_Rlfg4FrLy2jXBMUSs/edit).
Its sections 3.2 and 3.3 require more than this initial interface migration.
Statements describing a target capability are not evidence that this repository
already implements it. The document itself has not been edited by this change.

| Required direction | Current implementation and gap |
| --- | --- |
| One generic Field model, several simultaneous field types | GenericFaceSimulation now runs a fixed tuple of conserved scalar and octant definitions in one FieldBank; historical APIs remain separate compatibility paths, not Highlights acceptance evidence. |
| A field definition specifies magnitude representation, allowed faces/directions, link propagation, combination, decay, source and response | FieldDefinition declares fixed positive schemas, permitted ports, publish/absorb/response callbacks and explicit source/combination/decay/propagation policies. Variable-length links remain unsupported in the bank. |
| Adding a field type needs a definition, not a core engine edit | The generic bank accepts a new fixed schema and pure definition without a field-type engine branch; independent tests inject a third response policy. |
| All stored numbers are positive integers; polarity, sign and zero use integer codes | New bank state, packets and delivered faces use validated positive codes. Legacy particle, clock, momentum-ledger and sidecar records remain signed/zero/sentinel based; the whole simulator is not positive-coded. |
| Cell autonomy: own state and received values only; communicate through outgoing links | Local response reads are migrated. Unit-link contention now uses causal link ownership; moving self-response remains unresolved. Complete physical acceptance is not established. |
| Positive link length L, transfer time L/c | The linked scalar candidate retains its bounded positive-length packet contract. The scalar unit-edge and stream transports are not yet one common variable-length transport for all field types. |
| Shared integer Vector arithmetic and authoritative component views (3.3.2) | Existing signed working tuples and positive field codecs are not a complete common Vector API for field state, velocity and momentum. Exact vector storage, scale conversion and all required products remain incomplete. |
| Generic Face with concurrent typed channels and shared transport (3.3.3) | The bank separates field definitions and sign-sector channels. Crossing-face labels do not reverse octant payloads. This is not yet one Face/Transport abstraction shared by fields and matter. |
| Signed component balances and source/link/destination ownership (3.5) | Field inventories currently measure nonnegative scalar or sign-sector amounts. They cannot yet represent arbitrary signed momentum components through the same accounting interface. Particle transit and field inventory must not be described as a completed unified mechanism. |

The blocker investigation read Highlights revision
`ANLCKQlBPAyq4peJ3JSEXUjG-lsnLeQWsTUks2BDo0NOgBPrsjqfzWToVjzZrzJ5M11q-JCtjgq5f4Va8WDQ37VKC_hJvjelPhiKQeZzUZU`.
Its expanded vector, face and momentum requirements are architectural targets,
not retrospective evidence that existing tests cover them. Fixing the eight
reported acceptance failures alone would not establish every new requirement.

The implemented [generic definition contract](FIELD_DEFINITIONS.md) now provides
fixed-schema positive records and simultaneous composition through an actual
shared runtime. Its version-two definitions enforce per-channel flux conservation
and retain division remainders under Highlights section 3.3.1. An accepted joint transport/motion protocol and generic
variable-length links remain unfinished; this is not an accepted new default.

| Part | Contract |
| --- | --- |
| Response input | Six bounded signed integers in +x,-x,+y,-y,+z,-z order; each slot faces the neighbor from which its value arrived |
| Response law | Full opposite-face imbalance, with the existing bounded impulse, rational momentum scale and equal/opposite local exchange |
| Scalar transport | A replaceable pure publisher receives one old local scalar and returns six outgoing values; routing crosses one edge and commits all delivered inboxes together |
| Scalar state | Six delivered integers per materialized inbox, additional to the five scalar/momentum registers |
| Linked transport | Existing six received values, six lengths and six three-integer packets; response reads only the received values owned by its cell |
| Stream transport | Eight internal octant populations and six delivered face amounts; the six values are part of the existing fourteen-register record |
| Local bounds | Six ports and fixed payload size; no source identities, trajectory history, remote response reads or global force correction |
| API | field_faces is a read-only diagnostic mapping; face_at(address) reads one cell's authoritative delivered record |
| Errors | Validate fixed shapes, bounds and all outgoing proposals before the transport commit; unsupported conversions fail explicitly |
| Tests | Independent signed imbalance, injected publisher, one-edge propagation, source-facing order, atomic overflow and cross-phase causal intervention |

The field rule may consume its local inbox and local evolving state. A particle
response may not sample a neighbor's scalar register. The scalar and linked laws
remain distinct experiments; transporting their values through faces does not
cure their known moving self-force. A scalar is not converted into directional
octant populations without an explicit law.

Publishers are deterministic and stateless, and must map zero to six zeros:
sparse storage cannot represent a source appearing in every unvisited cell.
Scalar publication copies a potential sample to six faces; it is not conservation
of an eight-population flux. Each transport retains its own quantity and law.
The scalar transport's read-only mapping is a snapshot view of one committed
dictionary; a later advance installs a new dictionary.

## Public candidates and compatibility

`FaceScalarSimulation`, `FaceLinkedSimulation` and `FaceStreamSimulation` are
explicit experimental APIs. Their current model identifiers are respectively
`scalar-buffered-matter-v2-experimental`, `linked-delivered-faces-v1-experimental`
and `octant-buffered-matter-v2-experimental`. All select full response, including
the longitudinal component, and never select the scalar halo. The scalar API
accepts a replaceable `face_publisher`; the stream API accepts a structural
`OctantFieldRule` through `field=`. Linked publication retains its existing
length-governed six packets and delivered mailbox.

Each candidate snapshots the previous six delivered values before transport and
uses only those old local values for particle response. It also retains the old
K-slot destination eligibility for this tick, preventing a vacated slot from
enabling a vacancy cascade. These are bounded working double buffers: six extra
face values and K slot identifiers per visited cell while the tick runs. They
are reported separately from the persistent transport state. They do not prove
that competing arrivals have a causal arbitration protocol.

Historical `Simulation`, `LinkedSimulation`, `BalancedSimulation` and
`CausalStreamSimulation` remain available and have not been promoted or silently
replaced. `Simulation` preserves its historical two-stage response timing by
publishing old scalar values for the field phase and newly calculated values for
the response phase. Its particles now read a persisted inbox, but the second
publication still has the old two-edge causal defect. The historical halo also
retains its known nonlocal dependency. These compatibility paths are not claimed
to satisfy the new acceptance gates; frozen comparison remains unchanged.

Stream `flux` now uses source-facing order, consistent with linked mailboxes.
Existing emitted packets still use travel-direction order. The old
`attractive_samples` swap must not be applied to the new delivered stream faces;
the production adapter now passes the canonical values through unchanged.

## Composition gate still required

One-edge packet routing and one-hop matter movement do not prove the combined
tick causal. Delivering A to B, changing a particle at B, then moving that changed
record to C can relay information two edges in one tick. The previous stream
isolated-motion argument relied on this order. Reading an earlier face snapshot
instead does not automatically retain that argument: a moving source may meet
its own emission. An accepted scheduler must satisfy both independent tests.

The old/new-position halo is not used to fix this issue. Its writes can depend
on a move two edges from a changed target. Historical compatibility remains
explicitly labeled above. The frozen reference itself remains unchanged.

Two separate blockers remain mandatory: old-face staging can let a particle
read its own co-arriving emission, and two competing senders can change one
another's blocked-move outcomes through a destination in the same tick.
An empty-slot snapshot prevents vacancy chains but does not remove that latter
two-edge feedback. Neither a new traffic rule nor a self-field estimator is
silently introduced to hide these failures. No candidate is accepted as the new
default until its physics gates pass.
