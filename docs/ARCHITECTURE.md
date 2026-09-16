# Architecture and change boundaries

## Binding system architecture

The following project-wide design is user-approved and binding for new work.
Agents must not replace it with whole-Node scanning, lossy arithmetic or another
topology/ownership model without explicit user approval. Implementation gaps
below are unresolved work, not optional exemptions or permission to change the
design. Documentation approval does not itself implement a runtime change.

| Stage | Responsibility and boundary |
| --- | --- |
| Experiment authoring | Select external JSON entity catalogs and representation profiles; physical names, properties and numbers are data, while generic operators have one reusable code owner. |
| Preparation and validation | Resolve declared references, units, shapes, bounds and supported compositions into explicit integer initialization. Reject unsupported or inexact preparation under the lossless contract; no implicit physical law or hidden runtime catalog lookup. |
| Logical world | Nodes form the selected periodic 3D layout. Each Node owns one bounded NodeState and initially six computational Registers, one per Port. |
| Local execution | Every Register uses identical generic rules over bounded local inputs/state; joint dependencies use a coordinated Node-owned atomic commit. |
| External scheduling and transport | Host infrastructure maps endpoints and schedules only active/due Register work. Current/future work sets preserve next-tick-or-later delivery and declared delays. |
| Structured output and Recorder | Record committed events, results and snapshots through read-only interfaces; no physical update or global repair comes from output production. |
| Renderer | Present structured output separately from the Engine and Recorder; display controls do not change physical state. |

Several catalogs/profile sets may be selected explicitly for an experiment.
This is an authoring composition requirement, not a claim that the current CLI
accepts arbitrary lists or merges them automatically: existing compilers require
their explicit catalog/profile inputs. Identity collisions, incompatible units,
missing references and combined capacity must be resolved and validated before
initialization; file order cannot silently replace a physical definition.
The [entity contract](ENTITY_CATALOG.md) and
[preflight contract](CONFIGURATION_VALIDATION.md) retain their current API limits.

### Input, Engine, Output and Renderer

These are distinct responsibilities with explicit data interfaces, not a
requirement for separate processes or a new package hierarchy.

| Boundary | Contract and current owner |
| --- | --- |
| Input | Author JSON, validate explicit catalog/profile dependencies and prepare initialization. [Configuration validation](CONFIGURATION_VALIDATION.md) is the semantic entry point, not a runtime law or renderer. |
| Engine | Apply configured generic physical transitions to bounded owned state. Node/Register locality, timing, capacities and atomicity are enforced here; host scheduling delivers only causally due inputs. |
| Output | Produce structured committed events, results, state snapshots and execution metadata through explicit read-only interfaces. [Run outputs](DISTURBANCES.md#run-and-initialize) document existing files; output is not a rendered picture. |
| Renderer | Present structured Output as an image, animation, HTML or other view. It is separate from the Engine and output producer/Recorder; presentation, replay speed and camera choices never feed physical state. |

Locality is an input-provenance and ownership contract, not something proved by
putting components in different classes. Trace every physical input to bounded
local state or a completed causal delivery. Register logic has no remote-world
read; the scheduler cannot supply a global correction as if it were local data.
Observers may reject a run for diagnostics but cannot repair the physical state.

#### Detector, Recorder and Renderer

| Role | Meaning and unresolved boundary |
| --- | --- |
| Detector | A physical/model observation mechanism with specified coupling, observable and model-time mapping. Its response and any state-changing interaction require explicit rules; a displayed signal does not define those rules. |
| Recorder | A diagnostic output producer that records committed events or read-only snapshots in structured form. It does not perform a physical detection or choose an outcome merely by saving data. |
| Renderer | A presenter of those records; it can show a Detector's recorded output but is neither the Detector nor the Recorder. |

The existing [local reception observer](LOCAL_OBSERVER.md) is a passive recorder
of actual arrivals, not an implemented human/material Detector response or a
proper-time derivation. A Detector can be modeled through an explicit interface,
but its coupling and time interpretation remain to be specified; this document
does not invent a new transition. Recording cadence and display frame rate are
not physical detector time. Preserve exact outputs independently of rendering.

The [Detector exchange draft](DETECTOR_EXCHANGE.md) owns the latest external
Detector action-bit, PASS, fresh-return and causal branch-cancellation definition.
Its explicit open decisions are not supplied by the existing observation profiles;
this definition is not an implementation or run authorization.

### Architecture responsibilities

These are review and delivery responsibilities, not a requirement for a fixed number of
always-running agents or independent implementations.

| Responsibility | Required contribution |
| --- | --- |
| Theoretical physicist | Specify physical meanings of state, couplings, Detector observables and predictions with the mathematician; label assumptions and unestablished claims. |
| Computational experimental physicist | Design simulation experiments with independent predictions, tolerances and controls fixed before running; compare behavior with relevant classical/quantum theory and measured evidence, without fitting expectations afterward. This is not a physical laboratory role. |
| Mathematician | Specify state/vector spaces, applicable groups, operators, invariants and exact bounded integer encoding, including remainder ownership; establish preservation where possible and state proof limits. |
| Architect | Translate the agreed Node/Port contract into Register decomposition and interfaces while preserving locality, ownership, timing and joint atomicity. |
| Developer | Implement the authorized shared operators, schemas and configuration adapters; do not invent physical assumptions or hide species-specific formulas in scheduling. |
| Independent tester/reviewer | Check requirements against independent expectations, boundary/failure cases and identified source; separate software acceptance from physical validity. |
| Documentation | Keep authoritative definitions and implementation gaps synchronized in their responsible documents; distinguish proposal, agreement, implementation and tested result. |
| Boss | Converse with the user, clarify decisions, route bounded work and report results/blockers; preserve user approval boundaries. |

Vector/group notation alone does not prove energy conservation. Each claimed
invariant needs a defined quantity, its complete owners and applicable
transitions. The mathematical argument and independent tests must address those
definitions, not merely the operation's name.

### Physical goals and staged acceptance

The central research goals are a natural nucleus representation from simple
generic rules, an electron around a nucleus, and a photon representation.
They are unverified goals, not completed species dynamics. The Engine must not
recognize species names or execute electron/nucleus/photon-specific branches.
Physical representation JSON selects properties, preparation and supported
generic local Node actions; shared operators implement those actions once.
Do not insert a known equation and then report its configured consequences as
emergence. The [physical support inventory](PHYSICAL_ENTITIES.md) and
[entity catalog](ENTITY_CATALOG.md) remain the sources for present limitations.

| Goal | Required distinction and evidence |
| --- | --- |
| Nucleus | A prescribed charged source is a useful control, not an emergent nucleus. Charge alone does not establish nuclear structure, binding or stability; constituent state and the responsible interactions must be specified and tested. |
| Electron around a nucleus | Decide whether the experiment asks for a quantum bound state or a classical orbit proxy. A circulating marker is not atomic-state or stability evidence; observables and comparison targets must match the chosen meaning. |
| Photon | Distinguish a classical field pulse/ray proxy from coherent quantum propagation and single-quantum detection. A moving packet or an isolated click does not establish all photon properties or matter coupling. |

The computational experimental physicist owns prospective independent expected
results, numerical tolerances, negative controls and applicable classical/quantum
references, including comparisons of Detector outputs. Expectations must not be
adjusted to make a run pass. Supplied laws, derived consequences and genuinely
emergent behavior must be labeled separately from software correctness.

A staged acceptance proposal, requiring explicit scope before any execution:

| Stage | Proposed acceptance focus |
| --- | --- |
| Small controlled tests | Independently specified local transport, timing, ownership, remainder retention and interactions; include a no-interaction/absent-coupling control and compare structured outcomes, not only rendered motion. |
| Bound source or nucleus | First distinguish a prescribed source benchmark from a dynamically bound composite; define constituents, binding/stability observables, perturbations, observation duration and tolerances before claiming a nucleus. |
| Atomic and photon Detector evidence | Define electron-state meaning, source/field preparation, Detector coupling/time mapping and target outcomes; compare suitable classical/quantum references and negative controls, without inferring agreement from a visual orbit or pulse. |

To start a bounded implementation or experiment, select one stage and specify its
initial state, admitted generic rule set, exact representation and timing, output
observable, independent expectation and pass/fail tolerance. Do not invent
interactions, masses, numerical scales or a Detector transition to fill these
gaps. Resolving one stage does not certify the others. This draft proposes
acceptance structure only; it authorizes no new runs, implementation or merge.

### Open contracts before implementation closure

The binding principles above are agreed; the architecture is not yet a closed
implementation specification. Resolve the following contracts without silently
choosing physics or treating existing code as the final design.

| Contract to close | Required decision or evidence | Responsible reference |
| --- | --- | --- |
| NodeState and per-Port ownership | Exact fields, encodings, bounds, fixed capacities and Register-owned parts of the single NodeState; no duplicate stock | [Terminology](TERMINOLOGY.md), [stored codes](#stored-codes-and-mathematical-values) |
| Generic transition | Exact local inputs, outputs, participant selection, shared reads/writes, guards, failure behavior and atomic publication | [Node execution](NODE_VECTOR_PROCESSOR.md), [local integer operations](#local-integer-operation-contract) |
| Due-work scheduling | Readiness rules, current/next queue order, same-time arrivals, internal events, bounded rescheduling and proof of skipped no-op intervals | [Register target](#register-level-execution-target) |
| Units, timing and arithmetic | Scales, all remainder lifecycles, overflow rejection and whether intermediates must be nonnegative; whether k includes transit remains OPEN | [Reference units and timing](REFERENCE_UNITS.md#minimum-model-time-and-output-delay), [lossless ownership](#lossless-remainder-ownership) |
| Invariants and acceptance | Concrete quantities and owners, preservation arguments and independent experiment/Detector expectations; not assumed from vector syntax | [Test expectations](TEST_EXPECTATIONS.md), [physical support](PHYSICAL_ENTITIES.md) |
| Detector | Explicit coupling, observable, response and time mapping; keep physical observation distinct from diagnostic recording | [Observation boundaries](#detector-recorder-and-renderer), [local observer](LOCAL_OBSERVER.md) |
| Catalog/profile mapping | Exact reference-to-initial-state mapping and configured dynamic laws; compatible multi-catalog/profile selection and conflict handling | [Entity catalog](ENTITY_CATALOG.md), [configuration validation](CONFIGURATION_VALIDATION.md) |
| Input/Output/Renderer interfaces | Versioned initialization and structured-output formats, errors, record ordering/completeness and read-only rendering contract | [Input/output boundary](#input-engine-output-and-renderer), [run outputs](DISTURBANCES.md#run-and-initialize) |
| Implementation reconciliation | Identify unchanged code, required migrations and tests for fixed-six topology, Register scheduler, encoding and each listed no-loss gap | [Current execution](#current-node-execution-ownership), [lossless gap audit](#lossless-remainder-ownership) |

Nonnegative integer waiting can span zero, one or many ticks; zero waiting is not
same-tick Link traversal. Do not settle the open k/transit convention with an
unconditional additional tick. Small implementation tasks can begin once their
own interface and acceptance contract are closed; that is not approval to claim
the entire architecture complete or to change another unresolved contract.

### Spatial topology and endpoint routing

The selected world is spatially periodic: opposite boundaries are connected.
Open boundaries are a supported alternative experiment configuration, not this
selection. Spatial periodicity does not make time cyclic and does not assert a
spherical geometry. The initial topology uses six Ports per Node; configurable
bounded degree is a design requirement while the implementation still fixes six.

The transport/scheduler infrastructure owns the mapping
`(node_id, port_id) -> (neighbor_node_id, receiving_port_id)`.
IDs are routing handles, not physical inputs to Register logic. A Register
receives only its local values, local timing and already-delivered inputs; it
must not inspect global coordinates, the world or an "edge" condition. A periodic
boundary transfer has the same local rules and Link delay as any other adjacency,
with no extra physical jump. This is the binding dependency boundary, not a claim
that existing host-facing Node classes contain no position metadata.

### Mathematical schema and operation meaning

Sets define allowed values, components, participants and domains; vectors define
structured quantities with explicit bases, shapes and scales. A declared group
defines its elements, composition, identity and inverses only where that structure
actually applies. Vector addition, group composition and Port/Link connectivity
are distinct operations/relations and must not share an ambiguous generic symbol.
Not every matrix or LocalRule is invertible, unitary or a group action.

Definitions select supported generic operators and validated compositions.
They do not create arbitrary tensor support, new topology or a new operator
merely by naming it in JSON. Current shape limits remain in the
[local integer contract](#integers-vectors-and-tensors). State, representation
and transformation semantics must be explicit; notation alone is not evidence
of a physical law.

### Properties and field participation

The schema must permit many-to-many participation: one owned property can enter
several configured local coupling operators, and a field can couple through
several properties. This structural requirement is intended to represent nature,
not to declare every schema-expressible combination physically valid. A property
is data; a coupling operator is a separately justified transformation using it.

Each admitted operator needs its physical regime/source, units, causally arrived
inputs, joint updates/backreaction, conserved readouts, ordering and bounded exact
arithmetic. Shared quantities retain one owner; overlapping updates require a
generic local joint transaction preserving declared totals and every remainder.
A property-to-field link alone cannot choose an interaction law.

For example, electric and magnetic components belong to one electromagnetic
field, and charge enters both force terms; this is not evidence for two unrelated
fundamental forces. See [Feynman II, section 1-1](https://www.feynmanlectures.caltech.edu/II_01.html).
This reference does not adopt a new force law in the Engine. Actual supported
couplings still require physical review and implementation reconciliation.
Rest mass does not automatically select gravity or a Node-delay policy; keep
[mass representation, rest phase and delay](REFERENCE_UNITS.md#mass-encoding-rest-phase-and-node-delay)
distinct. No species-specific branch or additional coupling is implemented here.

#### Physical checks for composed couplings

Check dimensions and the symmetry transformations of the selected regime.
Electric field and velocity are polar vectors; magnetic field and spin are axial
vectors. The charge-force terms and magnetic-moment energy therefore have
different tensor roles. A shared magnetic field can affect orbital motion and
spin magnetic moment; property identity is not operator identity. The spin
reference is [Feynman III, section 10-6](https://www.feynmanlectures.caltech.edu/III_10.html).

Composition must retain physical cross terms and event ordering. In the
nonrelativistic charged-particle reference, `H = (p-qA)^2/(2m) + q*phi`;
splitting A into contributions creates cross terms. Independent update matrices
cannot simply be summed and presumed unitary, and noncommuting sequential pulses
depend on order. Gauge-dependent potential components do not gain independent
observable meaning from JSON names. See
[Feynman III, section 21-1](https://www.feynmanlectures.caltech.edu/III_21.html).
These reference expressions do not authorize adding those laws to the Engine.

Conservation must identify matter, field and apparatus owners, or explicitly
declare an external drive. General-relativistic gravity involves stress-energy
and spacetime geometry, not only a rest-mass Scalar; do not infer a universal
global scalar-energy ledger from a generic schema. See
[Tong's general-relativity introduction](https://davidtong.org/pdfs/teaching/general-relativity/gr1.pdf).
Mass quantization and mass-dependent Node latency remain separate unchosen laws.

#### Prospective finite spin-pulse check

A proposed bounded example uses one unentangled spin-1/2 Bloch vector r with
`rho = (I + r dot sigma)/2` and two sequential external magnetic pulses sharing
one gyromagnetic-ratio property. From `r=(0,0,1)`, an x-axis quarter turn followed
by a z-axis quarter turn gives `(1,0,0)`; reverse order gives `(0,-1,0)`.
Signed permutation matrices implement these rotations exactly and preserve
squared norm one; inverse pulses restore the initial vector. These are proposed
independent expected results, not simulator validation evidence.

The pulse rotations are configured reference operations, not emergent spin
dynamics. They are sequential local events within one electromagnetic interaction,
not arbitrary simultaneous field summation. This example does not close spin
measurement, electromagnetic source dynamics, apparatus energy/momentum or full
electron physics. Physical context:
[Feynman III, sections 10-6 and 10-7](https://www.feynmanlectures.caltech.edu/III_10.html).
It does not expand currently authorized implementation or experiment scope.

### Stored codes and mathematical values

The approved Node storage domain is bounded nonnegative integers, including
zero. This describes stored codes, not a prohibition on signed mathematical
values. A proposed generic signed encoding is `0 -> 0`, `+1 -> 1`, `-1 -> 2`,
`+2 -> 3`, `-2 -> 4`. Exact generic arithmetic must operate on the represented
values and return valid bounded codes; adding codes as values is incorrect.
Do not silently replace an existing valid encoding with this example.

Whether intermediate working values must also be nonnegative remains open;
bounded integer intermediates are required regardless. Overflow or a value
without an admitted representation rejects the operation before its mutation.
All remainders retain the explicit ownership and lifecycle defined below.

This is a binding storage-domain decision, not an implemented conversion.
Existing signed payload contracts and any positive-only code mapping retain
their documented runtime behavior pending explicit adaptation and verification.
The [canonical timing clarification](REFERENCE_UNITS.md#minimum-model-time-and-output-delay)
separately defines model time, output waiting and the unresolved transit-count
convention; permitting the number zero does not permit zero-time Link transit.

### Lossless remainder ownership

No remainder may be lost in physical arithmetic, evolving state or transport.
Represent each nonexact division with a bounded quotient and remainder whose
owner, denominator/scale, update and transfer lifecycle are explicit. Retain the
full represented value when waiting, moving, merging, splitting or replacing
an owner. A remainder may become zero through exact consumption or transfer,
never because its slot departs, a budget expires or a storage slot is reused.
Quotient-only truncation, rounding, clipping and dropping fractional information
are not permitted ways to fit a value. Exact-division operations still reject
nonexact results; overflow or lack of bounded representation must raise an
explicit error rather than silently lose information.

This requirement also applies at the boundary that prepares physical initial
state: measured uncertainty may remain reference metadata, but an encoding-error
report outside that state does not retain a missing arithmetic remainder inside
the simulation. Choose an exact supported encoding or report the representation
gap. Display rounding and host-only reporting do not alter state and remain
separate. Retaining arithmetic remainders does not prove all operations reversible,
unitarity, physical energy conservation or correctness of a selected law.

The following existing behaviors require reconciliation; this documentation
change preserves their historical/current descriptions, not compliance:

| Existing documented behavior | Relation to the binding requirement |
| --- | --- |
| [Pair exchange](DISTURBANCES.md#paired-exchange-couplings) resets its pair-owned remainder when a participant departs | Nonzero reset is a no-loss gap; a replacement owner/transfer is required, not a silent reset. |
| [Finite field emission](SPATIAL_FIELDS.md) clears an exhausted component's fraction and discards unfulfilled demand | Fraction clearing needs lossless ownership; unfulfilled external demand is separately modeled and must not be confused with already-owned stock. |
| [Dissipative decay](SPATIAL_FIELDS.md#finite-completed-link-decay) retains no decay remainder | This explicit historical loss law is not a compliant no-loss implementation merely because a diagnostic ledger records the loss. |
| [Localizing residue](SPATIAL_FIELDS.md#localizing-residue) deposits integer stock after quantized transport | Preserving inventory alone does not preserve the exact fractional propagated value; the fractional representation still needs review. |
| [Reference-unit encoding](REFERENCE_UNITS.md) permits explicit `max_error` rounding | Remains a host approximation tool, not permission for lossy initialization of the binding model; exact encoding is required there. |
| Historical scalar clipping and configured quantization | These retain their named historical behavior; they cannot be promoted as compliant generic arithmetic without a lossless representation and audit. |

This is a scoped documentation audit, not proof that every physical path has
been checked. Runtime code, tests and old evidence are unchanged. Do not weaken
a failing test or relabel one of these gaps as solved; any correction needs its
own authorized implementation and validation.

## System layers: Nodes, mathematics and physical entities

The architecture separates where state lives, how it changes and what a
configured state represents. A physical entity is not a special kind of Node:
an electron or a field is represented by explicitly configured properties and
rules on the same generic Node/Link machinery.

| Layer | Responsibility | Canonical owner |
| --- | --- | --- |
| Nodes and transport | A Node owns bounded local NodeState, resident values, Ports and pending timing/ownership metadata. Links own values in transit. | [Terminology](TERMINOLOGY.md), [Node execution](NODE_VECTOR_PROCESSOR.md) |
| Computational Registers (target) | One generic input/output unit per Port within the same NodeState; identical logic, data-selected state/direction/delay. | [Register-level execution](#register-level-execution-target) |
| Generic mathematics | Reusable bounded integer scalar/vector operators evaluate local inputs and propose changes. Supported operations are implemented once in code; validated JSON selects their compositions. | [Local integer operation contract](#local-integer-operation-contract), [disturbance expressions](DISTURBANCES.md#local-updates-and-expressions) |
| Physical entity definitions | External JSON describes particles, fields and other entities through identities, sourced physical properties, numerical values, units and evidence status. These are data, not species-specific engine branches. | [catalog.json](../examples/known-entities/catalog.json), [entity catalog contract](ENTITY_CATALOG.md) |
| Representation and preparation | Explicit JSON profiles bind selected entities to supported fields, initial values and configured rules. Optional reference-unit authoring encodes selected physical values into bounded integer components before initialization. | [representation-probes.json](../examples/known-entities/representation-probes.json), [reference units](REFERENCE_UNITS.md), [initialization validation](CONFIGURATION_VALIDATION.md) |

Physical numbers and names belong in external data, not hardcoded electron,
proton or field-specific logic. Shared constants and unit definitions live in
[physical-units.json](../examples/known-entities/physical-units.json). A catalog
measurement retains its unit, source, uncertainty and context when supplied;
unknown properties are not silently assigned zero. The runtime receives the
explicitly prepared integer values and declared scales, not decimal measurement
objects or a live catalog lookup.

The preparation boundary is explicit: choose an entity and its supplied profile;
when physical calibration is wanted, encode selected catalog values with the
reference-unit authoring tool into matching field initialization values; validate
the resulting initialization; then execute generic LocalRules on Nodes.
Calibration and encoding-error reports remain host-side evidence. The profile
compiler does not automatically turn a measured mass, spin or listed interaction
into a law. Merely editing reference metadata must not silently change runtime
equations. A new unsupported operation requires an explicitly reviewed generic
implementation, not executable code hidden in JSON.

The default field schema supports Scalars and three-component Vectors, with a
constant 3-by-3 integer matrix transform. The opt-in Node execution profile also
admits bounded 1..32-component properties with its declared operations and
composition limits; this is not arbitrary tensor support. The physical-quantity
encoder currently prepares only scalar/three-component values. The linked
contracts own the detailed dimensions, bounds and rejection rules.

The existing entity/configuration separation is implemented for its supported
paths; the Register execution target below is not. Complete
physical species dynamics and emergence remain separate research goals. A JSON
entry named electron or electromagnetic field does not establish electron
dynamics or Maxwell's equations. Keep the [physical support inventory](PHYSICAL_ENTITIES.md)
and each experiment's assumptions distinct from the generic mechanism.

## Register-level execution target

Use [canonical terminology](TERMINOLOGY.md) for the logical Node and its per-Port
computational Registers. The intended initial cube has six Registers, each using
the same generic rule machinery with different local data. These are subunits of
one Node, not new physical Nodes or an extra lattice. NodeState remains the single
bounded local ownership boundary; a Register's state is a part of it, not a full
replica. Immutable generic rule definitions can be shared.

An external host scheduler must index active or due work by `(node, port)`.
Changed output schedules delivery to the affected destination Register at the
declared Link arrival time; changed local state wakes dependent local Registers.
Only declared dependencies may expand that work set, rather than a blanket
scan of every Register or Node. A timer expiry, autonomous emission, internal
phase evolution or other configured rule can also require work without a new
input. Skipping an interval requires an exact no-change or closed-form transition
contract; "no packet arrived" alone is not sufficient.

At each logical tick, process only the current scheduled active/due Register
operations. Keep current and future work sets distinct: a newly routed output
becomes eligible on the next tick or later according to the declared delay,
never through an accidental same-tick cascade caused by iteration order.
Register commits collectively evolve the owning NodeState in the 3D event-space
layout. Same-time joint operations still use the coordinated commit boundary.

The same generic executor applies to every Register. Port-specific state,
orientation, parameters and delay select data, not separate hardcoded port logic.
A rule that reads or writes several Registers must use one coherent local input
snapshot, reserve its required owners and publish an atomic joint result under
the Node's coordination. Same-time arrivals, rule order and pending ownership
must remain explicit; independent scheduling cannot expose a half-committed
interaction or silently serialize away another input.

Register delay and Link propagation remain distinct. Preserve the chosen C/h
timing and all externally visible arrival/commit times; splitting host work does
not charge another physical delay or introduce instantaneous remote reads.
Current timing profiles remain separately defined in
[Node execution](NODE_VECTOR_PROCESSOR.md) and [disturbances](DISTURBANCES.md).
Register-local pending values and future-event slots need fixed capacities.
Host queues/indexes are separately accounted; cancelled or rescheduled entries
must not create an unbounded retained history.

**Implementation status:** current `core/node_services.py:port_count` returns six.
The [Focus scheduler](LOCAL_FOCUS.md) skips certified empty Nodes, but occupied
and pending carrier Nodes remain awake; transport indexes occupied banks rather
than maintaining the required due-Register scheduler. Existing Node-owned
planning/commit and parallel-worker interfaces remain unchanged. Configurable
port count, explicit per-Port computational Registers and due-only Register
execution are binding design requirements, not completed features or measured speedups.
Any implementation must demonstrate equal state, ownership, timing, event order,
failure behavior and model costs before claiming an equivalent host optimization.

### Computational layer implementation map

The Node/Register architecture above is already binding. Its specification was
not replaced by the property-transport or finite-wave examples; the missing work
is the actual computational Register and due-endpoint runtime. Configuration
benchmarks exercise existing mechanisms and cannot establish this implementation.

| Planned component | Owned responsibility and boundary |
| --- | --- |
| Shared Register contract | One writer defines the proposed `core/register_contracts.py` interface: bounded Node-local Register state, per-slot ownership/readiness and coherent joint reservation/commit. This path is planned, not an existing implementation claim. |
| Node-local execution | Each initial Node contains six per-Port computational Registers using the same generic rules. Their state is part of one NodeState; joint operations take one coherent snapshot and commit all affected owners atomically. Do not invoke the full Node planner six times or duplicate inventory. |
| External due scheduler and transport | Index active/due endpoints and timers, keep current/next-or-later work separate and route only at declared Link arrival times. Topology and periodic endpoint mapping remain external; local rules receive no global reads. |
| Simulation integration | Adapt the selected profile through the existing Simulation owner, with explicit support checks and unchanged accounting, failures and causal timing. Do not substitute fixture configuration for this adapter. |

The first proposed executable slice is exact whole-record movement plus local
joint generic transactions. Unsupported spatial-ray or native-quantum composition
must fail explicitly, not silently fall back to another scheduler. This is an
incremental supported scope, not a permanent narrowing of the general design.
The shared contract is settled before dependent concurrent writes; implementation
owners use isolated files/branches and one writer per shared interface.

Completion requires actual source and focused tests for Register ownership,
due-only dispatch, dormant wakeup/internal timers, causal ordering, joint atomicity,
bounded pending state and explicit unsupported-mode rejection, with independent
review. Until that evidence exists, this map remains planned implementation work,
not a completed runtime or a speedup claim.

### Dual-execution acceptance and measured selection

The user requires two parallel execution implementations: a conventional
whole-Node reference and a Register worklist implementation per model clock.
Run the same experiment with the same physical configuration, preparation,
topology, local laws and declared timing in both. Retain independent analytical
expectations; agreement between implementations alone can share the same error.

First establish exact equivalence of physical state, committed events, structured
outputs and model timing at every tick, including joint ownership, failures and
declared model costs. Host indexes, queue entries and diagnostic visit counters
need not be identical and must not be mistaken for physical state. Register
worklists retain separate current/next sets and due future wakeups for timers
and internal events, not only arrivals.

Only after equivalence passes, compare speed fairly on the verified identical
workload and machine: control setup, recording/rendering, repetitions and timing
boundaries, and report host time/storage separately from model time. Select the
faster verified implementation for that measured workload while retaining the
conventional reference and the independent expectations. No automatic assumption
that Register scheduling is faster, universal speed claim or unmeasured selection
is allowed. Keeping this reference and measurement-based host choice is explicitly
authorized; it does not change Node/Register physical ownership, locality or
causal behavior. The initial six-Register topology remains unchanged pending
explicit resolution of the later four-Register wording.

## Current Node execution ownership

[Integer Node execution](NODE_VECTOR_PROCESSOR.md) owns receive, preparation,
pending completion and publication in `core/disturbance_node.py` and
`core/spatial_node.py`. Shared services contain seed-free immutable definitions,
local law providers and write-side accounting; Nodes receive no world lookup.
Transport indexes local fixed output banks and validates adjacent delivery.
`core/node_conservation.py` is a DTO/protocol boundary; generic readout arithmetic
lives in `fields/node_conservation.py`, and its parser reuses initialization's
expression grammar. A configured exact balance check precedes physical mutation.
The profile's declared k and counted operation cost are separate quantities.
Indexed spatial rules reuse carrier role selection and the existing expression
evaluator with an additional local field owner. Pending proposals contain bounded
slot snapshots and deltas, never executable expressions. Field-only pending
proposals similarly retain per-rule deltas and outgoing views. Shared immutable
law services revalidate them before Node-owned commits; they receive local state
only. The [rule contract](NODE_VECTOR_PROCESSOR.md#local-rules) separates consumed
start triggers from persistent conditions and defines their failure behavior.

The opt-in [shared field computation cycle](SPATIAL_COMPUTATION_DELAY.md)
extends `PendingCycle` with one immutable spatial proposal, reaction phases
and cached joint-guard input. `SpatialNodeState` retains fixed incoming populations,
port readings, counts and decay cost while pending. Inventory includes these
actual input owners once and excludes proposals. No expressions or histories
enter evolving state. The carrier Node coordinates both local owners atomically.

[Property selectors](PROPERTY_COUPLINGS.md) compile into fixed layout compatibility
sets in `core/coupling_selectors.py`, shared by parsing, scheduling and local laws.
`core/validation.py` retains bounded checks without charging the physical clock.
The optional [local conservation audit](LOCAL_CONSERVATION.md) lives in
`diagnostics/local_conservation.py`; public assembly attaches it to committed
events and exposes immutable `core/conservation_state.py` inventory views.
Its host work is separate from model operation costs; it never provides an update or repair.

The [quantum-register extension](QUANTUM_ENTITIES.md) keeps density arithmetic in
`quantum/mixed.py`, reusable matrix builders in `quantum/operations.py`, and the
finite entity-profile compiler in `integration/quantum_entities.py`. The generic
core is unchanged; native v2 selection extends the existing event-program owner.


`entity_catalog.py` validates descriptive reference metadata and its links.
Its decimal measurement parsing is host-side only and never updates physical
state. `entities.py` requires separate explicit experiment profiles for version 2
catalogs, compiles them into ordinary initialization, and delegates runtime schema
validation to `initialization.py`. Reference properties and interaction lists do
not enter runtime laws or select species-specific behavior. See
[entity catalog](ENTITY_CATALOG.md).
The [reference units](REFERENCE_UNITS.md) authoring tool owns the shared external
constant/unit registry and one-time exact rational conversion into bounded
Scalar/Vector initialization components. Rational calibration and error reports
remain host metadata; they are never a physical arithmetic fallback or a runtime
unit conversion. Integer scales and future physical intermediates still obey
the ordinary bounds. Unit names do not select interactions or propagation laws.
Optional two-record type conversion follows the existing frozen pair proposal
and delayed engine commit; its ownership restrictions are in
[local conversions](LOCAL_CONVERSIONS.md).

## Configuration validation ownership

The [configuration preflight contract](CONFIGURATION_VALIDATION.md) defines the
shared JSON decoder, supported format dispatch and explicit context dependencies.
`configuration_validation.py` coordinates existing format owners and returns
reports without constructing a simulation. It shares initialization/observer
preparation with the runner; the UI consumes its read-only validation result.
Semantic rules remain in initialization, native programs, catalog, profiles and
observer owners. Runtime execution and physical acceptance remain separate checks.

## Local integer operation contract

This contract applies to all new and changed physical code, entity definitions,
configuration adapters and prototypes intended for the active Simulation.
Use [DISTURBANCES.md](DISTURBANCES.md) for the supported operation vocabulary
and [LOCAL_FIELD_RULES.md](LOCAL_FIELD_RULES.md) for delivered field inputs.
LOCALITY-1 and the numeric bounds in SIMULATOR_DEFINITIONS.md remain authoritative.

### Generic operations and law ownership

Express active laws as initialization-defined compositions of supported scalar
and vector operations. Particle names, charges, masses, couplings, thresholds,
interaction eligibility and participant limits are data; names must not select
hidden physical equations. Reuse generic operators instead of adding a special
electron, proton, electromagnetic or computation-load branch to the engine.

The engine owns scheduling, addresses, capacities, transport timing, validation
and atomic commits. It must not own a model-specific force, energy, momentum or
field equation. Generic arithmetic belongs to its documented reusable owner;
model/API assembly only composes it. Scheduler indexing and timing arithmetic
are necessary bookkeeping, not permission to hide physical laws in the scheduler.
An externally configured equation is still a chosen law, not evidence that it
emerged from the lattice.

Keep immutable parsed law definitions outside dynamic node, disturbance,
pending-proposal and packet payloads. Payloads carry bounded state values and
declared identifiers, never copied expression trees, formula strings, Python
callbacks or executable code. Read-only diagnostics may calculate global
measurements but cannot supply a physical update or repair conservation.

### Integers, vectors and tensors

All physical numeric inputs, registers, intermediate results and transmitted
components use the declared bounded integer domains. Reject booleans and
floating-point inputs rather than coercing them. Python's arbitrary-precision
integers do not remove the model's working-register bounds: check intermediates
before cancellation, scaling or assignment. Never add float, complex, NumPy,
Decimal or Fraction arithmetic as a physical fallback.

Represent scales and ratios with explicit bounded integer numerators and
denominators. Exact-division operators must reject a zero divisor or a nonexact
result. A rule that permits division with remainder must declare the existing
bounded remainder owner, update and lifetime; do not silently discard a remainder,
round through floating point, wrap overflow or clamp a failed calculation.
The binding [lossless remainder requirement](#lossless-remainder-ownership)
supersedes permission to discard fractions in older split/quantization policies;
retain their documented behavior as an implementation gap until corrected. Arithmetic failure must not leave a partially committed transaction.

The active field schema currently supports scalars and three-component vectors.
Its constant 3-by-3 integer matrix transform is not general tensor-valued state.
Do not claim arbitrary tensor support or silently flatten an unsupported shape.
A future tensor extension must declare fixed rank and dimensions, component
bounds, generic operators, transport coding and all state/diagnostic consumers,
with shape, overflow and locality tests before use. Tensor notation alone does
not make a calculation generic, integer or local.

### Local inputs and bounded work

A physical rule may read its own fixed local records and information already
delivered through the six neighbor ports under the transport contract. Neighbor
coordinates do not authorize instantaneous reads of remote physical state.
Trace every input to its causal owner, including self-field subtraction,
computation-load fields, energy bookkeeping and collision eligibility.

Fix local record, field, rule and participant capacities in validated definitions.
Only supported configured participant limits may be used; a larger value does
not create an unsupported many-body operator. Bound local loops and storage by
those capacities, independently of world size. Never compute responses from an
all-particle scan, global field reconstruction, growing per-source history or a
host-side correction. Charge, momentum and declared energy balances need explicit
local owners and transaction checks; a diagnostic total alone is not a law.

### Review evidence and scope

For each affected operator or rule, identify its owner, scalar/vector shape,
integer input/intermediate/output bounds, causal input path and failure behavior.
Run the affected checks selected by tools/check.py, including related integer,
initialization, architecture and locality gates when those contracts change.
The existing entry points include tests/test_integer_contract.py,
tests/test_initialization.py, tests/test_architecture.py and tests/test_locality.py.
Review gaps in scanner coverage explicitly; passing static checks is not a proof
about arbitrary Python or every possible configuration.

Read-only rendering and host timing may use noninteger arithmetic outside the
physical path; their results must never feed physical state. Historical named
models retain their explicit contracts and must not be copied into the active
generic engine. External floating-point or globally coupled reference prototypes
are not compliant active-engine implementations, even if their GIFs look useful.

Q-ORACLE-1 is an existing explicitly scoped opt-in quantum exception, documented
below. It is not a local-law implementation and cannot justify nonlocal inputs
to ordinary physical rules. This instruction contract neither removes that
separate research backend nor certifies it as local. Report such scope limits
instead of claiming that every repository path already satisfies the active
local integer contract.

## Generated output ownership

The optional [local observer](LOCAL_OBSERVER.md) belongs to diagnostics.
`observer_configuration.py` owns placement validation shared by initialization and
the runner. Initialization validates the optional `observer` member without adding
it to physical state; the runner selects recording without eager diagnostic imports.
`diagnostics/local_observer.py` whitelists completed events at one node and
archives copied reception values plus a cycle counter. The runner captures exact
receipt prefixes beside playback frames. Enriched spatial reception events are
emitted after ownership commits. Neither archive, display nor clock count is a
physical planner input or a quantum oracle query.

`retention.py` owns host-only artifact registration, writer leases and expiry.
Runners own complete fresh output directories; the workspace owns exact input,
log and export files and declares the child-output dependency for companions.
Cleanup uses recorded filesystem generations and operating-system locks, with
recoverable quarantine before removal. The module never imports or changes
physical engine state. Its one-shot and singleton watcher interfaces share the
[same retention contract](RETENTION.md).

## Active generic ownership

The engine receives an explicit `core/record_policy.RecordPolicy` alongside its
local planner. `fields/record_operations.RecordOperations` owns the existing
activity predicate, delivered-record merging and configured cost reporting.
It stores immutable definitions and receives only fixed local slots, delivered
records, pending-slot locks or a local plan. It receives no world, address or
clock. The engine alone determines arrival eligibility, supplies locks, validates
slot capacity, and commits proposals before clearing packets. Public Simulation
and the explicit contact trial assemble this component; direct DisturbanceEngine
callers must supply `record_policy=`. Configuration files are unchanged.

This is an ownership refactor: arithmetic order, transport/channel distinctions,
source bookkeeping, cost prices and frozen pending semantics are preserved.
Generic operations and configured physical meaning remain separate; this change
does not add a physical force, a tensor schema or an arbitrary Python plugin API.
See tests/test_record_operations.py and the existing disturbance, spatial and
native-event regressions. The independent spatial scheduler retains its current
ownership and is outside this refactor.


`disturbance_api.Simulation(initial: InitialState)` composes the generic engine
and local law; it is exported as the primary package Simulation.
`initialization.py` reads strict JSON data and resolves names to bounded typed
definitions. `core/disturbance_state.py` owns fixed schemas and payload coding;
`fields/disturbances.py` owns expression arithmetic, updates, paired coupling
and transport proposals; `core/disturbance_engine.py` owns addresses, capacity,
fixed transit and delayed atomic commits. No layer branches on a physical field
name or imports Python code named by initialization.

The opt-in rational extension stays within these owners: `fields/ratios.py`
owns finite exact arithmetic and projections; `fields/routing.py` owns balanced
six-port selection and fractional credit. Neither receives world state. Fixed
carrier bookkeeping travels through the existing scheduler. The numerical and
cost amendment is explicit in [RATIONAL_PARTICLES.md](RATIONAL_PARTICLES.md).
Physical formulas in its examples are reference benchmarks, separate from the
elementary emergence probes in [PHYSICAL_ENTITIES.md](PHYSICAL_ENTITIES.md).

Field, type, model and unit labels are data. Reordering field/type declarations
must preserve the same resolved behavior; declared update/coupling order and
spatial axes can be meaningful and are not interchangeable. The executable
cross-layer checks live in `tests/test_generic_identity.py`. Genericity is scoped
to the supported integer scalar/vector schema, three-dimensional six-port
geometry, fixed capacities and declared operation set; it does not imply an
arbitrary equation interpreter.

Atomic interaction definitions share that path: initialization resolves bounded
assignments, invariants and activation expressions; `fields/disturbances.py`
evaluates frozen-pair proposals and exact per-transaction balances before routing.
They add no per-source memory or alternate commit path. Example physics remains
JSON data, including vector transforms and the unequal-mass elastic contact law.
The shared evaluator propagates explicitly supplied spatial flux through nested
operators. Atomic interactions operate after proposed spatial responses and
ordinary exchanges, retaining carried emission/reaction allowances and the
prepared opposite field reaction until the common delayed commit.

The complete source contract is [DISTURBANCES.md](DISTURBANCES.md). Its six-port,
bounded-record schema replaces the implicit scalar/particle schema for the
primary API. Global diagnostics never drive physical rules, and rendering is
absent unless explicitly requested.

The optional spatial extension uses `core/spatial_state.py` for fixed schemas,
`fields/spatial.py` for bounded emission/splitting and `fields/spatial_plan.py`
for pure local proposals. `core/spatial_engine.py` schedules and owns field
packets; `disturbance_api.py` composes its planner without formulas. The shared
engine combines diagnostics and costs while retaining separate field and
carrier clocks. See [SPATIAL_FIELDS.md](SPATIAL_FIELDS.md) for the contract and
the remaining self-attribution requirement. `fields/spatial_coupling.py` owns
local sampling, fractional exchange, exact quarter-turn rotation and reaction
allocation. The injected `SpatialCoupler` protocol keeps those calculations out
of engine scheduling. Carrier and field owners validate together before committing
the response; fixed sample registers and departure timestamps prevent future
reads or edits to old in-flight packets. See [SPATIAL_COUPLINGS.md](SPATIAL_COUPLINGS.md).

The optional phased-ray law retains its bounded prepared cosine/sine tuples in
immutable `SpatialFieldDefinition`, outside NodeState. Per-record departure,
capture-ticket and absorbed-phase rows have fixed configuration-derived sizes.
Each departure row carries four integers (amount, cursor, phase, advance); an
absorbed-phase row carries phase and advance. These bounded owner registers
preserve a ray's emitted advance without looking up a later emitter state;
Nodes validate that a field proposal changes only selected stock/vector fields
and permitted bookkeeping, preserving transport metadata. Funded/absorbed owners
currently reject delayed carrier plans on the independent spatial clock. The
read-only runner inventory binds ray momentum through explicit recoil/absorption
field references and counts actual resident, in-flight and escaped owners.

The opt-in [local field-rule contract](LOCAL_FIELD_RULES.md) reuses these owners.
`fields/local_field_rules.py` evaluates bounded multi-field retained/outgoing
proposals using delivered six-port data; `fields/spatial_plan.py` composes them
with existing emission and outward routing. Logical groups reference existing
scalar/vector fields and allocate no second physical owner.
`fields/spatial_interactions.py` extends the injected coupler with generic
field/carrier assignments and actual-commit invariant guards. The engine freezes
carrier transaction views and additive field deltas, then validates the complete
commit against current local field stock before either owner mutates. It never
replaces live fields with sampled state. Old emission metadata keeps its owner
through delayed carrier commits. Transformation ledgers are diagnostics, not
sources or inputs to physical laws. The schema, bounded expression evaluator,
fixed field clock and existing outward path remain shared.

The remaining scalar, stream, linked, collision and balanced sections describe
explicitly named research APIs. Their record layouts, extension points, tick
orders and acceptance limits remain scoped to those candidates.

## Causal-stream candidate extension

`fields/streaming.py` owns bounded pure octant splitting and delivered-flux
selection. `core/streams.py` owns the fourteen-register stream records and
one-edge packet routing; its full-state validation is a read-only host audit.
`core/streaming_engine.py` schedules that phase before the existing local
particle update. `models/causal_stream.py` selects full-vector response and
ordinary movement through `ScalarFieldModel`; `particle_api.CausalStreamSimulation`
assembles them. No field law receives an Engine or mutable source history.
The ordinary scalar seeding interface is rejected for this distinct state type.
The existing scalar and linked candidates retain their own implementations.

[AGENTS.md](../AGENTS.md) is the shared contributor entry point.
`POSTULATES.md` is the plain-language conceptual entry point.
`SIMULATOR_DEFINITIONS.md` translates those principles into exact technical
requirements, and this document describes the code boundaries that enforce them.

## Monorepo ownership

Universe24 is one versioned repository, not a requirement that every component
run in one process. Keep the current package layout until an actual independently
built component justifies another package; do not create empty apps/packages trees.
The [README project map](../README.md#project-map) is the path index; the dependency
table below defines code boundaries. Architecture owns this repository policy.

| Information | Single owner | Update rule |
| --- | --- | --- |
| Executable code and model selection | [src/event_universe](../src/event_universe/) | Keep shared formulas generic; models select them |
| Generic initialization schema and transition law | [DISTURBANCES.md](DISTURBANCES.md) | Keep the active source contract separate from historical candidates |
| Physical contracts | [POSTULATES.md](../POSTULATES.md), [SIMULATOR_DEFINITIONS.md](../SIMULATOR_DEFINITIONS.md) | Plain-language principles and exact contracts have distinct roles |
| Test expectations | [TEST_EXPECTATIONS.md](TEST_EXPECTATIONS.md) | Link the responsible tests, inputs and outcomes without copying laws |
| Installation and execution | [README.md](../README.md) | Reuse the package CLI and [tools/check.py](../tools/check.py) |
| Contribution and integration | [CONTRIBUTING.md](../CONTRIBUTING.md) | One coordinated change includes affected providers and consumers |
| Durable agent procedures | [skills/workflow.md](../skills/workflow.md) and specialist Skills | Shared rules live once; specialist Skills reference them |
| Current task, owner and evidence | Repository Issues and PRs | Record head/base, acceptance target, blockers and next action |
| Checkout orientation | [PROJECT_STATUS.md](PROJECT_STATUS.md) | A dated, commit-pinned snapshot links to live work; no duplicate task ledger |

Use existing definition headings or stable rule IDs when mapping a change to code
and tests. Record the exact contract, implementation path and test path in the PR;
extend the responsible test-expectation entry if coverage changes. Never treat a
test's existence as proof it passed. Architectural decisions belong here or in a
linked focused decision document; physics decisions belong in their contracts.

Store reproducible scenario inputs, configuration and test fixtures with the code.
Keep generated videos, HTML, traces and large outputs outside source commits.
Link them from the PR with the code identity, command and relevant parameters;
artifact retention is finite, so preserve required evidence before it expires.
There is no automatic chat-to-repository or Google-Doc-to-code synchronization.

## Dependency direction

| Module | Allowed dependencies |
| --- | --- |
| `core/integer` | Standard-library types; owns working bounds, integer division and decoded component arithmetic |
| `core/state` | Standard-library data types and `core/integer` |
| `core/disturbance_state` | Bounded arithmetic and immutable generic definitions |
| `core/disturbance_engine` | Generic records, local planner interface, scheduling and ownership |
| `core/node_execution` | Host-only isolated-interpreter Node tasks and execution measurements; no physical state ownership |
| `fields/disturbances` | Generic records and bounded integer arithmetic; no world or diagnostics |
| `initialization` | JSON input and generic typed definitions; no arbitrary execution |
| `core/contracts` | State types |
| `core/lattice` | State types and integer bounds |
| `core/scalar_engine` | State, lattice and local contracts |
| `fields/scalar` | Integer primitives and fixed vector types from `core/state` |
| `fields/policies` | Integer primitives and scalar samples |
| `dynamics/turning`, `dynamics/movement` | Integer primitives and fixed vector types from `core/state` |
| `models/scalar_field` | State, local contracts, generic fields and dynamics |
| `models/local_field` | Compatibility re-exports only |
| `disturbance_api` | Generic engine and disturbance local law |
| `particle_api` | Historical engine and explicitly chosen research model |
| `diagnostics` | Read-only engine views, immutable events, rendering libraries |
| `runner` | Generic public API, initialization and optional diagnostics |
| `ui` | Local HTTP, strict initialization validation and isolated CLI process ownership |
| `scenarios`, `legacy_runner` | Historical public APIs and optional diagnostics |

The historical scalar engine receives field and particle callables and an optional activity
predicate. `ScalarSimulation` assembles them from a scalar
field and a turning component through `ScalarFieldModel`. Callers can replace
either component independently with the keyword arguments `field=` and
`turning=`. `ScalarEngine` itself imports no field, dynamics, model, rendering or
file-writing module. No plugin registry or inheritance hierarchy is needed.
`PeriodicLattice` is the single implementation of periodic wrapping and the
six directional neighbors used for reads, activation and movement.

## Configuration workspace

`ui.py` serves packaged `ui_assets/` HTML, CSS and JavaScript without a frontend
build. Templates remain the canonical JSON files in `examples/`, included as
package data files for installed use; `--configs` selects another directory.
Full inputs and JSON fragments share `initialization.parse_json_document`
duplicate-key enforcement. The existing validator checks configurations before
runs. The browser previews initial seed positions, not computed motion.

Each accepted request becomes immutable JSON passed to the existing runner in
a separate Python process using the server's package source. The UI never steps
an Engine or supplies physical arithmetic. It owns one active job, session
history, cancellation and links restricted to known artifacts. Configuration
edits require no compilation or restart. Output directories are unique;
Run & watch explicitly requests a movie; recording can be disabled and the CLI
remains headless by default. `diagnostics/disturbance_render.py` embeds copied
frames and metadata in the packaged self-contained player. Neither the player
nor its speed/projection controls supply simulation inputs. Name controls update
declarative references only. Cancelled runs are labeled incomplete. Loopback
binding, Host/Origin checks and a session token constrain HTTP access.
See [WORKSPACE.md](WORKSPACE.md) for lifecycle and persistence behavior.

## Generic calculations and model choices

`core/integer.py` owns shared decoded component addition/subtraction, ordered
sums, dot/cross products and nonnegative ceiling division. Products and ordered
partial sums retain their working-register checks, including overflow before
cancellation. Ceiling division retains the existing adjusted-numerator bound;
`signed_divrem` instead rounds toward zero and returns a signed remainder.
Callers supply schema-bounded components and retain payload encoding, field
validation, operation pricing and atomic commit ownership. The expression
interpreter delegates arithmetic while retaining broadcasting and AST costs.
See [shared arithmetic tests](../tests/test_integer_arithmetic.py).

`ScalarFieldRule.advance(sample, neighbors, source=..., denominator=...)`
returns a `ScalarSample(value, remainder)`. The built-in `ScalarField` implements
one weighted six-neighbor stencil, with optional local retention. It supports
signed values and retains integer division residues. It knows neither source
occupancy nor particle or node records. A different local scalar law can satisfy
the same protocol without inheriting from it.

`FieldTurning.apply(...)` takes particle momentum, field momentum, a supplied
local vector and carried residues. The selected direction function receives
only momentum and that vector. The component performs the bounded impulse
calculation and equal-and-opposite exchange once, regardless of the selected
direction policy. It does not compute or store a field, or interpret node state.
`full_response` and `dominant_axis_transverse` are available policies; neither is
an implicit default. The transverse policy is a discrete dominant-axis filter,
not a geometric rotation or orthogonal projection.

`ScalarFieldModel` is the single adapter for the existing physical state. It
maps occupancy to source strength, enforces the current nonnegative scalar
policy, obtains a gradient, calls turning and movement, and builds validated
node and particle proposals. `SCALAR_MODEL` explicitly selects six unit
neighbor weights, no local retention and dominant-axis transverse response.
Denominators come from `Config` so arithmetic and state audits share one value.
The reusable components never import `Config`, `NodeState` or `ParticleState`.
Source multiplication, nonnegative clipping and scalar activity predicates live
in `fields/policies`; the adapter selects and calls them. Bounded scaling with a
carried remainder is implemented once in `core/state.scaled_divrem`, including
a bound on the product before adding a potentially cancelling remainder.

`SCALAR_MODEL` explicitly retains `value_changed_or_source` for exact v10
scheduling. Supplying `ScalarSimulation(field=...)` instead selects
`sample_changed_or_source`, which also tracks remainder-only evolution. Callers
can override either choice with `field_activity=`. The engine validates the
boolean result before committing any field proposal. Direct `ScalarEngine` callers
that omit an activity predicate conservatively retain every visited node.
Custom scalar laws must preserve a zero sample with zero neighbors and zero
source; this is the quiescent state assumed by sparse scheduling. They must not
depend on an unstated time input or on private evolving state.

These extension points preserve the current five-register scalar node schema.
A signed field can be calculated by the generic primitive, but the current
adapter clamps negative results. A vector field or several simultaneous fields
requires another schema rather than a replacement scalar callable. The active
disturbance engine supplies that separate fixed-size multi-field contract; this
historical adapter remains scalar-only.
The practical extension guide is `SCALAR_FIELDS.md`.

## Local contracts

`update_field(node, six_neighbor_values, source_count, config)` returns one new
five-field node record. `update_particle(particle, node, six_neighbor_values,
config, tick)` returns new particle and field records, a hop direction, gradient
and impulse. Their inputs are immutable and their output size is fixed.

The engine owns position changes. A candidate must not change position in its
proposal, may request only one cardinal direction, and must mark the tick.
The current law computes both sides of the local momentum exchange and validates
them before returning. Contract tests must accompany another candidate law.
Custom field laws and direction functions are trusted deterministic local code;
they must use bounded integer arithmetic and retain no evolving private state.

Public mappings contain immutable named tuples and are read-only views. These
views reflect future engine updates, so they are not snapshots. `capture_frame`
creates independent diagnostic copies; changing a frame cannot change physics.

## Tick order

1. Check that the world is healthy and the next tick fits its register.
2. Build the sparse field work set from the previous active frontier and neighbors.
3. Read all old scalar values before computing any new scalar values.
4. Compute and validate all field proposals, then commit them together.
5. Snapshot occupancy-address order; visit each address and its fixed slots.
6. For each particle not yet updated this tick, compute and validate a local
   particle-field proposal, commit it, then attempt the requested hop.
7. Emit immutable force/move/blocked records after their corresponding commits.
8. Increment the tick. New occupancy becomes the source for the next field phase.

Steps 5–6 preserve first-insertion and slot ordering from v10. Contended moves
are not claimed to be permutation-invariant. There is no hidden global repair
phase. `last_update_tick` prevents a moved particle from receiving another
update when its target address appears later in the occupancy snapshot.

An event is stamped with the tick being processed. A frame captured after the
step is stamped with the incremented tick. Thus an impulse recorded at event
tick 15 is first visible in completed frame 16; this convention is unchanged.

## Recording and resources

`ScalarSimulation` defaults to `NullObserver`, retaining no trace. `TraceRecorder` is
intended for small tests or old notebooks; its memory grows with history.
`JsonlRecorder` writes events immediately and does not retain them. Rendering
frames live only in the runner. `--frame-stride` controls their sampling cost.
The engine never reads an observer result. Observers are trusted application
code, not a security sandbox; an observer exception during a tick stops the world.

Run and test visualization is opt-in. When explicitly requested for a historical
scalar run, the renderer captures independent `VolumeFrame` records with full XYZ
coordinates and renders at 1500×1275; `volume=False` chooses a plane slice.
The authoritative headless/default output rule is in `SIMULATOR_DEFINITIONS.md`.
The volume renderer shows nonzero scalar nodes, sampled particle trails and
momentum arrows with a rotating camera. Plane and volume renderers share one
GIF/HTML output function. Camera rotation, color and marker scaling are purely
diagnostic; they do not change the engine or particle motion.

With visualization enabled, the historical runner captures only the selected
view. A capture may receive momentum already measured from that same state;
otherwise it measures the state itself.
Every completed tick still gets its momentum acceptance check, including ticks
without a saved frame. A failed step is captured with a fresh measurement because
its partially committed state can change without advancing the tick counter.

The volume renderer retains static axes, grid and compass artists between frames
and extends diagnostic trail history incrementally. It resets that history when
playback seeks backward or the domain changes. Dynamic artists are replaced for
each frame, preserving the existing draw order and camera. The shared Pillow
writer copies the Agg canvas already drawn by FuncAnimation and encodes the
non-looping GIF once. Custom savefig backgrounds or transparency use savefig to
preserve their rendering semantics. See [PERFORMANCE.md](PERFORMANCE.md).

`diagnostics/live.py` owns disposable historical preview coordination.
`legacy_runner` enables it only with explicit `--live` or API `live=True`, which
also enables recorded visualization. Ordinary generic and historical runs are headless.
The parent alone steps the Engine, copies and retains every canonical frame,
and records events. Before nonblocking queue submission, the
preview serializes the copied frame, preventing later producer mutation from
reaching the consumer. A spawned process receives only serialized frames and
display configuration. Its queue holds one waiting snapshot and its trail window
holds at most eight; intermediate preview messages may be coalesced.

The worker uses the same volume/slice scene builders to publish the latest PNG
inside an atomically replaced `live.html`. Its scales are provisional because
future extrema are not yet known. An integer meta-refresh interval supports
ordinary local-file browsers without a server. After computation, the parent
signals a separate stop event, reaps the worker with bounded waits, and closes
queues without waiting for an abandoned feeder. Only then does the canonical
renderer publish selected already-drawn rasters through a read-only callback.
This preserves one live-page writer and avoids recomputing final frames.

Final GIF/HTML still uses the entire retained history and unchanged fixed scales.
Preview failures warn without changing physical stepping or canonical export;
physical failures keep their original exception and failed report. A final redirect
is registered only for the current run's successfully written artifact, preserving
failure status and avoiding a stale report left by an earlier run. Preview work,
IPC and page updates are host costs, not part of the physical model.

Sparse world storage is distinct from constant-size physical state. Existing
materialized nodes and occupancy-address order are retained for exact legacy
equivalence. Reclaiming them is a separate scheduler change requiring physical
contract checks. This refactor does not claim constant total memory or
worst-case constant-time Python dictionary operations.

## Commit-time local quantum transfer

The [localized contact candidate](LOCALIZED_QUANTUM_CONTACT.md) uses a generic
`CommitResolver` protocol. Pending Node state carries one bounded integer token;
immutable definitions and bounded reservations stay with the resolver. The Node
validates all reserved replacement alternatives and the common field reaction
before requesting a choice. Routing, sources and cycle cost cannot vary between
those alternatives. Spare unreserved slots remain available during a wait.
The event-backed tick and snapshot use the same transaction lock, making quantum
transfer and ordinary installation one observable publication.

`integration/contact_program.py` validates configuration and
`integration/contact_runtime.py` composes existing owners. Occupation/capture
arithmetic constraints belong to `quantum/contact_rules.py`; the quantum semantic
owner enforces them even for typed callers. Ordinary core and fields do not import
quantum laws. Inventory sector totals and possible-origin display are diagnostic
reads, not physical inputs. Contact model limits are owned by its linked contract.

The opt-in [causal source extension](CAUSAL_QUANTUM_SOURCES.md) adds a bounded
source-envelope component attached to the same ordinary Node. The `core/source_*`
modules own formula-free amplitudes, finite source state, pending proposals,
twenty-four Port slots (amplitude, terminal, null-notice and correction), one
rational weight scale, at most one null record and local transitions. No component holds a world reference,
quantum query, executable matrix or expression tree in its physical state.
`fields/source_envelope.py` owns the shared rational complex and weighted-source
arithmetic; `fields/source_emission.py` composes generic spatial primitives.
Immutable matrix/emission definitions and initialization routing remain outside
NodeState in `integration/causal_contact_runtime.py`.

Only actual Link packets supply neighbor inputs. The controller transports frozen
messages and advances local owners; it does not reconstruct sources from the
quantum state or shared origin flags. Local source commits use write-only
`NodeEvents` provenance and the existing ordinary spatial accounting. A local
capture atomically ends its source and installs its ordinary output; remote
termination requires a received notice and local delay. The candidate contract
owns its retarded approximation, numerical bounds and clock restrictions.

The [recurrent extension](RECURRENT_QUANTUM_CONTACT.md) preallocates one to six
such envelope banks per participating Node. The root envelope retains a flat
tuple of at most five additional same-address owners, exposing all evolving
state to the transitive NodeState audit. Fixed generation routing and emission
turns keep old packets isolated without storing growing local history. The
recurrent resolver composes existing envelope arithmetic and inventory commits;
`quantum/contact_outcomes.py` validates matrix/effect support, and the quantum
event network owns atomic result/origin creation and idempotent result lookup.

## Opt-in quantum ownership — Q-ORACLE-1

The `deferred-unit-cost-oracle-v1` assumption is defined in POSTULATES.md and its
numeric, timing and resource contracts in SIMULATOR_DEFINITIONS.md. The feature
contract and limits are in [QUANTUM_DETECTOR_TRIAL.md](QUANTUM_DETECTOR_TRIAL.md).
The existing physical engines and schemas above are unchanged.

| Module | Responsibility and allowed dependencies |
| --- | --- |
| `quantum/state`, `quantum/query`, `quantum/terminal` | Fixed records and bounded integer helpers; may use core.state, never an engine |
| `quantum/deferred` | Sole owner of deferred history, cache, accounting and one terminal result |
| `integration/quantum_bridge` | Sole production adapter between spacetime references and quantum APIs; no Engine or write callback |
| `tests/quantum_detector_fixture` | Test-only controller with one detector-event slot and two detector bits |

Physical modules, models, application assembly and diagnostics must not import
quantum. Quantum must not import physical engines, models, dynamics, fields,
diagnostics or integration. Shared bounded arithmetic from core.state is allowed.
The architecture tests reuse the existing import resolver and cover relative,
member and aliased imports. They are static guards, not a sandbox against dynamic
Python. The bridge does not duplicate evaluation or maintain another quantum cache.

Queries are explicit, not automatically polled. Only DeferredQuantum evaluates
histories or chooses the terminal output. Replies are immutable. The test
controller records that result without writing NodeState, ParticleState, time or
Engine events. A future native physical commit needs an explicit engine contract;
it cannot be added by turning a diagnostic observer into a second state owner.

### Selected joint-state event backend

`DeferredQuantum.bind_event_network` composes the selected finite backend from
`quantum/event_network.py`. That module owns immutable quantum payloads,
conditional-record closure and exact host checkpoints. `core/event_space.py`
owns immutable event identities, dependency edges and write-once origin-resolution
slots. It stores no separate predecessor list. Each native Node and the quantum
backend share fixed `EventCursor` handles for current register state, preserving
each register's physical time across checkpoints. Native v3 also gives each
participating Node a bank of at most six integer wave-origin references. These
are distinct from the finite virtual register heads, never amplitudes or a local
history. `quantum/wave_origins.py` owns their configured quantum lifecycle;
ordinary field rules cannot consume remote resolution state. See
[event spacetime](QUANTUM_EVENTS.md#event-spacetime-and-current-references) and
[origin cells](WAVE_ORIGINS.md) for the transaction, polling and cost contracts.
Retired-gate and null-instrument cancellation require exact correlated-density
certificates in the quantum owner; direct origin lookup does not replace them.
`quantum/event_rules.py`
owns generic bounded local matrix validation/evaluation. It does not infer a
physical law from a name. The existing scalar-expression backend is preserved;
an owner cannot mix the two representations or silently switch a live history.

`integration/quantum_event_trial.py` is an explicit headless test controller, not
an Engine adapter. It supplies example matrices and one externally supplied
integer ticket. Native disturbance schemas, scheduling, fields and momentum
updates are unchanged. The existing quantum import boundary applies to the new
modules. Host full-state inspection and controller-conditioned weights are not
local physical observables. See [QUANTUM_EVENTS.md](QUANTUM_EVENTS.md) for the
selected contract and [TEST_EXPECTATIONS.md](TEST_EXPECTATIONS.md) for its tests.

## Verification scope

LOCALITY-1 in SIMULATOR_DEFINITIONS.md governs the complete dependency path of
every non-quantum physical update, including self-field inputs. Shadow/reference
computations cannot be hidden behind a local adapter. `test_locality.py` checks
exactly six baseline neighbor reads independent of world extent and rejects
known world access and replay in field, dynamics and model modules. Code review
must still check causal input provenance and bounded loops; static checks do
not prove arbitrary Python is O(1). Global scheduling and diagnostics retain
their explicitly separate host costs.

| Reviewed path | Local bound | Separate host cost |
| --- | --- | --- |
| Generic disturbance local cycle | Fixed fields/types/rules and resident slots; up to six outgoing channels per record | Sparse scheduler and diagnostic totals grow with materialized nodes and packets |
| Baseline scalar update | Six neighbor samples, five node registers and at most K source slots | Work/frontier sweeps grow with visited nodes |
| Field response and movement | Three vector components; one hop request; at most K destination slots | Occupancy-address scheduling grows with retained addresses |
| One node's particle phase | At most K particles, each with at most K slot work | K is fixed; no all-source search supplies force inputs |
| Link transport and geometry | Six ports per node, one packet per port, at most two delivered proposals per edge | `advance` visits materialized link nodes |
| Matter transit | Four integers per in-flight particle; one neighbor destination | Tick scheduling visits in-flight particles |
| Diagnostics and rendering | Not a physical update; cannot feed state repairs | Full-state audits, histories and rendering are not O(1) |

The implementation therefore supports bounded local model work, not a claim that
the entire non-quantum Python program or a full simulation tick is O(1).

The archived frozen reference has SHA-256
`822f62ac790c0b8477ed634d24454774152bcba8fb3322a53d039c251376163f`.
It was used for historical tick-by-tick comparisons, totaling 278 ticks
(120 stationary, 48 contact, 110 turning). It is no longer imported or executed
by the suite. Current physical regression coverage is described in
[TEST_EXPECTATIONS.md](TEST_EXPECTATIONS.md).

Generic unit tests cover weighted and signed scalar values, exact fractional
response, selectable directions and overflow on both sides of an exchange.
`test_scalar_field_model.py` pins the current model's source, clipping and transverse
response choices. `test_field_composition.py` injects a distinct source-only law
and full-vector response through the public API, verifies their observed
behavior and local conservation, and rejects an invalid law before commit.
These alternative laws are test fixtures, not a newly adopted physical model.
The numeric audit and import-boundary tests include both new generic packages.
The boundary audit resolves absolute and relative imports and rejects runtime
arithmetic in model assembly, API assembly and compatibility facades, while
allowing type annotations and literal configuration. It is tested with both
allowed and forbidden examples. Dedicated tests also cover periodic lattice
geometry, scalar policies, digital movement and each diagnostic projection.
Inputs and expected outcomes are listed in `TEST_EXPECTATIONS.md`.

Stricter input checks and exception atomicity are intentional boundary fixes.
They can reject invalid inputs that old code accepted. They do not alter the
successful regression trajectories. Preserved model limitations are listed in
`SIMULATOR_DEFINITIONS.md`; an architecture cleanup does not establish new physics.


## Local-link candidate (v11)

`LinkedSimulation` / historical CLI `--scenario links` explicitly selects
`scalar-field-v11-local-links`. `ScalarSimulation` retains the previous model and its
physical behavior checks. This is a new geometry/transport hypothesis,
not an architecture-only change to the baseline.

| Module | Responsibility |
| --- | --- |
| `fields/geometry.py` | Reusable bounded integer mean-to-length mapping |
| `dynamics/transit.py` | Reusable departure selection and per-edge travel time |
| `core/links.py` | Fixed six-port records, ownership, old-message delivery and commits |
| `core/linked_engine.py` | Scheduling transport around the existing field/particle engine |
| `models/linked_field.py` | Select the candidate components and identify the model |
| `api.LinkedSimulation` | Assemble the engine; inject the symmetric merge policy |

The existing model adapter accepts a `MovementRule`; it still contains no
independent arithmetic. Linked movement selects direction at departure and
schedules an integer arrival. Its motion and scalar inputs use delivered local
mailboxes. `ScalarEngine` adds extension hooks without copying its occupancy, local
impulse exchange, record validation or observer logic.

Each node owns its three positive edges. The opposite endpoint keeps a copy of
the active length. Ownership is storage identity, not a privileged physical
source. Either endpoint sends a proposed length on the current edge. At expiry,
both ends know that delivered proposal: the sender from its own old timer,
the receiver from its incoming packet. If two proposals arrive on the same edge
in the same tick, the candidate selects their maximum. This commutative merge is
injected; it is a candidate choice, not a derived gravity equation.

The host collects at most two proposals per edge and commits the two endpoint
records together. This is equivalent to each endpoint merging its own expired
proposal and the opposite incoming proposal. No global measurement, remote
source lookup or global repair supplies a value. Subsequent communication uses
the committed length; packets and particles already in flight retain theirs.

Tick order: complete due matter transits, deliver old port packets, compute and
commit fields from delivered inboxes, publish changed values/proposals, then
run the existing local particle-field exchange for particles ready to depart.
No field/particle rule reads current remote scalar registers. Sequential
capacity conflict resolution is inherited from the baseline and is not a claim
of full parallel particle scheduling. In-flight particles remain resident
sources and do not receive new impulses until arrival. This is explicit model
behavior, not continuous geodesic integration.

A materialized node adds exactly 30 integer link registers to its five scalar
registers. Each in-flight particle adds four integer registers, bounded by K
resident slots per node. Dictionary storage and full work-set iteration remain
host costs, not strict worst-case O(1). There is no per-source field map or
unbounded local message queue. Busy channels retain one snapshot; intermediate
versions are coalesced to the current node value after delivery.


## Adding physical features

Follow [the physical-feature procedure](PHYSICAL_FEATURES.md) before adding a
law or state contract. It separates explicit local inputs, evolving state,
immutable parameters, derived values and model assembly. Dependencies between
physical inputs remain explicit; code separation does not imply statistical
independence. Formula-free assembly is checked for every module beneath
`models/`, including future and nested models, rather than a fixed name list.

### Audit against main e74f2fd

- `ScalarField.advance` receives samples, six neighbors, source and denominator;
  it does not import model state or the world.
- `FieldTurning.apply` receives momenta, a vector, residues and rational coupling;
  direction selection is injected. Local exchange is implemented once.
- `MeanStretch` stores immutable coefficients and receives two local samples.
  Its caller supplies already delivered neighbor information.
- `ScalarFieldModel` extracts values from physical records, invokes the generic
  laws and constructs proposals. The engine owns the subsequent commits.
- API assembly independently accepts field, turning and (for linked worlds)
  length policies. Tests exercise alternate laws and numerical parameter changes.
- The baseline fixed state does not accept arbitrary vector/multiple-field
  records. Such an extension needs a new explicit contract and diagnostic support.

These are code and tested-contract findings, not a proof of every possible
plugin's locality or physical correctness. Dynamic imports, arbitrary callbacks
and hidden external state still require review; the static gate is not a sandbox.

## Repository language

English is required for all repository comments, docstrings, documentation,
instructions, diagnostic messages and new identifiers. The authoritative rule
is [Repository language: English](../AGENTS.md#repository-language-english).
`tests/test_repository_language.py` guards against legacy non-English scripts;
review checks the actual language. Older branches must follow this rule when
merged. Mathematical notation remains valid. This affects documentation and
review, not physical laws.

### Run acceptance diagnostics

`diagnostics/invariants.py` compares immutable momentum values and raises on an
isolated-motion violation. The runner establishes the initial applicability
(single particle and zero field records), calls the check each tick before frame
sampling, and uses the existing failure-output pipeline. No check result is fed
back into a physical law to repair state. The engine remains separate from this
application-level acceptance policy.

## Massive point-contact extension

The user-authorized v13 contract is in SIMULATOR_DEFINITIONS.md. Shared integer
ratio reduction stays in core/state (a fixed 128-step bound, no numeric imports).
`dynamics/collision.py` accepts only two fixed CollisionBody records and implements
the elastic law once. `models/collisions.py` selects it and maps records without
arithmetic. Engine receives the callable, resolves co-resident fixed slots,
validates both output records and commits the pair before notifying observers.

The original particle schema appends four integers; defaults preserve every
legacy trajectory. Mass remains constant. Momentum and movement-credit
numerators have explicit denominator owners. Generic movement, turning and
transit accept these independent inputs without a Config or world reference.
Neither diagnostics nor the optional quantum bridge feeds the collision law.
Contact state is at most K*K flags per contacted address. Each local sweep has
at most K(K-1)/2 pair candidates; sparse world iteration is a separate host cost.

Historical frozen comparisons projected the original twelve fields and checked
the four appended defaults. Current fixed-schema, numeric and behavior tests
cover the active records without requiring equality to the archived engine.

## Opt-in balanced motion and local halo

`ScalarSimulation(movement=..., post_motion_halo=...)` passes generic local components
to the existing adapter and engine. `BalancedSimulation` selects
`advance_balanced_movement` and the current model's scalar-halo adapter. Movement
remains in `dynamics/`; the scalar transformation remains in `fields/`; the model
maps fixed records; the engine alone schedules the old/current six-neighbor union
after all particle responses. No core schema changes. The law and evidence are
documented in [BALANCED_MOTION.md](BALANCED_MOTION.md).

## Standalone vector-lab experiment

The user-requested [tools/generic_vector_lab](../tools/generic_vector_lab/README.md)
is an opt-in mechanism experiment with its own explicit JSON laws. It does not
import, replace or extend the active engine or its schema. The lab runtime owns
its local transactions; its separate movie tool reads saved states. Generated
outputs go under artifacts and remain outside source commits. Its local quantum
coupling is a toy experiment, not an implementation of the active Q-ORACLE-1
bridge contract. The active source-of-truth boundaries above remain unchanged.

## Shared native event extension

The [native event contract](NATIVE_QUANTUM_EVENTS.md) adds a domain-neutral causal
ledger and local resolver protocol under core. The integration owner composes
quantum payloads, initialization-selected instruments and classical control codes.
Only primary API assembly and initialization reference that integration owner;
core and ordinary field arithmetic never import quantum.

The [generic graph contract](EVENT_GRAPH_CONFIGURATION.md#spatial-provenance-and-resource-bounds)
also covers the independent spatial scheduler. `SpatialNodeState` owns three optional
host IDs for state, frozen response sample and charged field phase; `SpatialPacket`
owns one final-departure cause. These IDs never enter the pure field planners.
Carrier emission bookkeeping and joint responses connect the owners through
local event IDs, with fixed parent fan-in and capacity checked before local
ownership commits. Shared history remains a bounded host audit; quantum-plus-field
clock composition and observer inference are separate features.


Parallel planning preserves Node-owned transitions. A transient scheduler-thread
continuation yields only immutable carrier or spatial planning records; the spatial
request includes the colocated committed-cost scalar. Worker interpreters receive
no Node, continuation, world or event graph. After each bounded planning phase,
the scheduler resumes owners in address order. Each owner performs its existing
validation and atomic commit. Continuations are closed and discarded every tick;
they are never part of NodeState. Shared-clock cycles use two planning barriers,
while ordinary carrier and field phases each use one.


### Local carrier scheduling and prepared ray laws

[Local Focus](LOCAL_FOCUS.md) defaults on. `core/plan_reuse.py` shares immutable
pure transition results through the host `NodeExecution` service with bounded
per-simulation caches. Full input equality is required; laws cannot read cache
state. Local commits, guards, model charges and timing remain Node-owned.
Mutable bond planners and event resolvers bypass reuse. `PortTable` indexes only
active transport banks and retains stable creation order; schedulers refresh
changed banks without adding callbacks or world references to PortBank.
The detailed limits, metrics and supercell boundary are in the Focus contract.

Local Focus owns a host address set and visit counters, never
physical history or a new per-Node state type. Nodes certify dormancy from fixed
local state; actual delivery wakes them. The spatial active index remains shared
by both scheduling modes. Frozen field definitions own bounded immutable phase
and pace tables prepared before any tick; no lazy pace cache grows across runs.
New retained-ray and claim owners pass the same trusted pre-commit/receipt
validation boundary as outgoing payloads. The global bond reference is excluded
from ordinary initialization and planner composition.
