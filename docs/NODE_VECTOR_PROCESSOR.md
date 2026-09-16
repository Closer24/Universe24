# Generic integer Node processor

This is the current Node-owned execution contract, not the revised 24-directed-Register
scheduler for six external Ports. Existing six-Port readiness/bank behavior is
not evidence of this internal computational graph. The [canonical Node/Register distinction](TERMINOLOGY.md) and
[Register execution target](ARCHITECTURE.md#register-level-execution-target)
define the intended decomposition. Storage-register counts and quantum registers
in existing contracts do not count these computational Registers. No runtime
behavior or timing changes through the terminology update.

The [canonical timing clarification](REFERENCE_UNITS.md#minimum-model-time-and-output-delay)
distinguishes the accepted Register timing design from this existing profile's
explicit additional-wait convention. Its local symbol h is not Planck's constant.
The [approved storage domain](ARCHITECTURE.md#stored-codes-and-mathematical-values)
is likewise a target representation decision, not a change to this profile's
current signed values or remaining counters.

This implements the bounded local execution part of [task 82](https://github.com/Closer24/Universe24/issues/82).
The configuration opts in with `node_execution: true`. Existing configurations
retain their existing timing. It is one execution path in the active engine,
with a different explicit timing contract, rather than a second simulator.

## Model contract

| Part | Contract |
| --- | --- |
| State | Integer property vectors, fixed record slots, local field populations, routing residuals and pending proposals |
| Inputs | Resident values and packets delivered over adjacent links; local readouts have no world or causal-history lookup |
| Operations | Validated scalar/vector expressions and indexed assignments; names select definitions, never physical formulas |
| Time | One clock step is h, the duration of an adjacent hop. A fired rule declares positive integer k and takes k local steps; the subsequent hop takes one further step |
| Cost | Counted operation work is separate from the new profile's configured duration |
| Conservation | Externally declared scalar/vector readouts are checked across complete actual owners before committing an accepted transition |
| Failure | Invalid dimensions, integer overflow, unavailable capacity or an unequal declared balance fail explicitly |

The current world topology is still the six-port three-dimensional lattice.
Record capacity and interaction arity are separate from its six fresh input
directions. A six-role rule can consume six resident records; later arrivals and
pending records do not create unlimited storage. Local output banks have fixed
capacity and do not provide a neighbor lookup. Arbitrary graph topology and
general exact interacting coarse-graining are not introduced by this change.

## Properties and aggregation

With Node execution, each field explicitly declares `aggregation`. One scalar
or 1 through 32 integer vector components are supported. `sum` and `vector_sum`
permit componentwise accumulation; `keep_equal`, `phase_bins` and
`interaction_state` require matching state. `nonmergeable` forbids merging.
This first profile rejects split transport and spatial ownership for nonadditive
properties, so those policies are retained on separate whole carriers.
Routing credits and internal phases remain relevant to merge compatibility.
Three-dimensional operations, such as a cross product, retain their dimension
checks even though generic addition and dot products admit other lengths.

Adding observable totals does not authorize destructive merging of carriers.
For example, an externally chosen square readout gives 2 squared plus 3 squared
equal to 13, whereas merging amplitudes first gives 25. A balance check rejects
that transition. A successful balance check alone also does not establish that
all future behavior is independent of omitted identity or phase information.

## Local rules

An indexed interaction declares `participants`, `k`, and `assignments`.
Each participant selects a type or required properties. An assignment identifies
its target participant and field; a field expression may read another participant
by its zero-based index. All right-hand sides read the same frozen input for that
group. Outputs are applied together after validating the group.

Selection is bounded and deterministic: in declaration order, take the earliest
unused compatible slot for each role. Repeat for disjoint groups. There is no
combinatorial search or implicit reassignment if a later role cannot be filled.
Successive fired groups and rules add their declared durations. A false condition
does not charge an interaction duration. A rule's operation tariff cannot change k.

Public Node views expose an independent integer arrival mask and `delay_counts`.
In the new profile the counts are the remaining local h steps, reach zero at
completion, and are separate from the immutable scheduled `ready_tick`. A local
cycle reserves the same duration across its port bank. Original cost-budget
profiles retain their historical duration reporting.

Spatial and carrier rules use the same declared properties. A joint carrier/field
interaction can declare the same indexed `participants` and reference several
locally owned fields. A participant reference or assignment uses `participant: i`;
`side: "right"` selects the joint local field owner. A default or left-side
reference is rejected in an indexed rule because it would be ambiguous. All
assignments in one group read all selected participants and fields from one
frozen snapshot. Each participating slot stays reserved, including a participant
whose values the rule only reads. Later groups see preceding proposed changes.
Received-port presence
is distinct from its numeric value: a zero packet or canceling contributions can
still represent an arrival. Copied field samples are inputs, not extra stock.

`field_rules` and `spatial_interactions` accept an optional scalar `commit_when`.
It must be positive both when selecting a rule and immediately before committing
its frozen substep. `when` remains a start trigger and is not replayed. Persistent
conditions read owned carrier/field values only; received samples, arrival-presence
bits, flux and proposed outgoing leaves are rejected. Validation does not charge
physical operation cost or change k. An initially false guard skips the rule;
a guard invalidated during the wait faults before any owner in that proposal
changes. There is no automatic retry, silent cancellation or new choice of R.

For a delayed field-only phase, each fired rule retains a bounded field delta
and six-channel outgoing snapshot. At completion, every rule's declared invariants
and persistent condition are rechecked in order against live stock plus preceding
frozen deltas. This includes an intermediate change whose net phase delta is zero.
Intervening arrivals remain owned. Assignment expressions are never rerun to
manufacture a different delayed result. The same revalidation applies to joint
carrier/field groups. Rule invariants constrain their own substep; the mandatory
conservation contract additionally checks the complete final owner transition.

In mathematical notation n is the participant count, while k specifies duration.
Scalar energy and vector momentum can be declared readouts of the underlying
registers; they are not mandatory state fields or engine formulas. Nonlinear
readout changes are evaluated from actual before/after states, including fields.

## Conserved readouts

`conservation_contract` is mandatory for the new profile. It names a nonempty
list of `quantities`. Each quantity declares `name`, `components`, `units`, and
`carriers`; it also requires a `spatial` expression when spatial fields exist.
Carrier entries select `requires` properties and supply a `value` expression.
Every carrier layout must be covered exactly once. Expressions use the existing
validated expression language; arbitrary executable code is not accepted.

Energy may be a scalar readout, momentum a vector, charge another scalar, and
total angular momentum another vector, provided the selected model actually
defines and owns their contributions. The engine has no special energy, mass,
charge, electron or proton branch. A label and unit string do not establish a
physical interpretation or perform dimensional analysis.

The guard counts resident originals, fields and individual real packets exactly
once. Pending replacements and samples are not additional owners. Individual
packet readouts are evaluated before summation, so nonlinear definitions are not
silently applied to a merged packet. Guard calculations are validation work and
do not change physical work cost or k. They reject a proposal; they never add a
compensating reservoir or repair a physical result.

`Simulation.conservation_report()` returns each configured quantity's current
scalar/vector value over resident and in-flight stock. This read-only host
projection measures individual owners before summation, excluding pending copies.
Its explicit scope excludes stock that has already left an open boundary. A
`guarded` status identifies enforcement; it is not a statement of physical proof.

This first opt-in profile accepts schema 1 closed local rules with zero spatial
baselines. Native quantum programs, external emission/update sources and legacy
unpriced coupling mechanisms require their existing profiles. Unsupported
combinations are rejected during initialization rather than silently ignored.

## Claims and evidence

The operation language, ownership boundaries, declared duration, merge policies
and conservation requirements are assumptions of this model. Numerical examples
can demonstrate consequences of those assumptions. Imposing a conserved readout
and then observing its balance is a correctness check, not a derivation of a law
of nature. A conditional expression such as E squared minus dot(P, P) can be
declared as a comparison readout; that does not derive elementary masses.

This implementation does not claim emergent electron/proton dynamics, universal
quantum selection rules, probability normalization, unitary evolution or quantum
interference. Such claims need separate mechanisms and independent evidence.
The experimental compression work in [PR 85](https://github.com/Closer24/Universe24/pull/85)
remains research evidence rather than an admitted general macro evolution law.

Storage is bounded per Node at fixed schema, degree and capacity. The host may
retain a spatial index and optional diagnostic history; neither is a physical
input to local rules. Node isolation is an API and validation boundary, not a
security sandbox against arbitrary Python reflection. See [architecture](ARCHITECTURE.md)
and the recorded validation evidence for tested limits and measurements.
O(1) describes one bounded local event relative to world size, not a whole tick.
Pending guard storage scales with fired rules, selected slots, field components
and the fixed outgoing degree; it does not grow with elapsed event history.

## Reproducible configurations

- [Six records](../examples/node-vector/six-records.json): a frozen six-role cyclic
  permutation, with k=3 and eight registers per carrier. Initial declared totals
  are energy 21, momentum (3, 0, 0), charge 0 and angular momentum (0, 15, 0).
- [Two fields](../examples/node-vector/two-fields.json): one carrier exchanges its
  first vector with the second local field, with k=2. Joint initial totals are
  energy 7 and zero momentum, charge and angular momentum. The other field remains
  independently addressable. The rule is an explicit register swap, not an
  inferred electromagnetic force.
- [Joint reaction](../examples/node-vector/joint-reaction.json): two carriers and
  two local fields rotate four vectors from one snapshot with k=3. Independently
  defined squared-length and vector-sum readouts remain 34 and (4, 6, 2). The
  configuration calls these readouts energy and momentum; this tests the generic
  machinery and does not establish a physical energy law.

Run a configuration with `python -m event_universe --init
examples/node-vector/six-records.json --output artifacts/node-vector-six` from the
repository root, with `PYTHONPATH=src`. Use a new output directory. No rendering
is needed. The configuration validator accepts the same file without advancing
the world. The example readouts are externally selected projections of eight
registers; their physical names do not make this a calibrated particle model.
