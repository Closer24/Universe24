# Universe24 Highlights

This file is the Universe 24 Highlights specification. Until 2026-09-16 the
live document was the Google Doc
[Universe 24 Highlights](https://docs.google.com/document/d/1IkhSyqZZMBSgbJV-PMMwcXG0D_Rlfg4FrLy2jXBMUSs/edit),
and this file was taken verbatim from its revision modified on 2026-09-16 at
11:57 UTC. By the model owner's decision of 2026-09-17 this file is edited
directly and is the authoritative Highlights text; the Google Doc is the
historical source up to that revision and is neither edited nor resynced.
After every change here, [POSTULATES.md](../POSTULATES.md),
[RAY_EVENT_MODEL.md](RAY_EVENT_MODEL.md) and every other document that restates
a changed rule are brought into step with this file, and
[Highlights coverage](HIGHLIGHTS_IMPLEMENTATION.md) records what the repository
implements. Section numbering is the document's own.

Revision 2026-09-17 (the model owner's decisions on the ray-event model):
sections 3.3, 3.4, 3.5, 3.15, 3.19, 3.20 and 5.4 restated; section 3.18
deleted; section 5.1 replaced, its occupied-channel rule deleted; the
sentences of 3.2, 3.6, 3.8, 3.10, 3.12, 3.17, 3.29, 3.30, 4, 5.3, 5.5, 6 and 8
that relied on the shared quantum resource or on the occupied-channel rule
adjusted accordingly. All other text
is the 2026-09-16 revision verbatim.

---

*Sole author: Alon Gonen*

# 1. Purpose and navigation

This English-language Highlights document summarizes the central model specification; it is not a competing source of physical laws. Section 3 restates the adopted principles at summary level. The central specification owns their full definitions, exceptions and acceptance criteria. Latest explicit user decisions supersede older prose. Adopted requirements, proposed numerical profiles, implemented mechanisms and tested results must remain distinct. An implementation gap does not reopen an adopted decision, and documentation must not invent a missing physical law.

[Central model specification: Universe24 — Unified Node Theory: a unifying schema for rays, fields and interactions.](https://docs.google.com/document/d/1jPBMb-1BoCH8Qo6y5E-j0H0ANWzbHmkO9l-9t2pxSOQ/edit)

# 2. Intuitive picture: multidimensional Snake

Think of Universe24 as a kind of multidimensional Snake game with obstacles and interactions. Multiple rays move through the same 3D Node network across compatible property and field channels. They may cross without responding, respond weakly, or interact very strongly according to their selected coupling; crossing or co-location alone is not a collision. Here, weak and strong describe response strength, not automatically the fundamental weak and strong forces. Multidimensional includes independent state channels, not extra spatial dimensions. Obstacles are an analogy for declared interactions, not invented opaque walls or a capacity fix. Ordinary evolution is deterministic; only an actual Detector generates a draw. The central specification remains the precise definition.

# 3. Foundational postulates

## 3.1 Discrete local space

The adopted board is a connected three-dimensional cubic network. Each local Node connects to six neighboring Nodes through directional Ports and Links. The selected layout is periodic; boundary choices belong to explicit experiment configuration. NodeState is the unit of local state. No fixed private-register decomposition or 36-register layer is required.

## 3.2 Ordinary Node dynamics are local

An ordinary Node operation uses only its own bounded state and information that has causally arrived through its Links. It cannot read another Node's live state or apply an instantaneous distant field, movement or inventory update. There is no exception: the Detector of section 3.19 is a Node like any other, and the number a pair shares travels on the returning ray (section 5.4). Section 3.18, which described a shared quantum-resource exception, was deleted on 2026-09-17.

## 3.3 Ray-form propagation is fundamental

The board contains Node states and their properties, not a separate fundamental object called a ray. A ray names the universal form in which those properties propagate through neighboring Nodes. An interaction is a meeting of rays at a Node, decided by the coupling declared between their families, and its result is at most six events, one per Port. An event is a change of trajectory: a new straight line leaving the interaction. A ray is the trajectory of one event between two interactions, reversible in time; a Node that a ray merely crosses hosts no event. The system has exactly two definitions, event and ray: a ray carries information, and an event is where that information splits; a ray is what was split off from an event. From its event, every ray carries the number of steps it has made. Every ray is a wave ray and carries a phase; a plain ray is a special case of the wave ray, not a second kind. Light is a wave ray with no mass and no charge. Outside a Detector every trajectory an interaction permits actually happens; alternatives arise only at interactions. A traveling ray releases a field, and the field is itself made of rays. There is no additional substance called matter; references to rays below refer to this propagation and its interaction patterns.

## 3.4 Matter is emergent

Particles, mass and the ordinary appearance of solid matter are intended to emerge as stable patterns of Node properties and their ray-form propagation and interactions. They are not additional fundamental substances. This is a research objective, not a claim that calibrated particle dynamics, mass or stable matter have already been derived. There is no matter in the model at this stage. Matter is the name for rays bound in one Node by a declared binding coupling (a neutron ray and a proton ray held together by the strong binding, an electron ray around them whose trajectory is changed at every step by the field rays the bound pair releases). Binding is the interaction whose result is zero events: the rays stay at the Node and interact again every interval. Mass is the retained energy of a bound group; the group's phase advance is its clock. A bound group has no lifetime of its own: it lasts as long as the binding interaction repeats at that Node without releasing an event. The binding may be nothing more than a very large output-clock delay (section 3.28) that the bound rays create together, a large mass making the Node very slow, so that the rays do not leave. It is unbound the same way anything else happens on the board: a ray arrives (a high-energy light ray, for instance; there is no photon, only a ray) and the coupling declared for the families present produces events that leave. Nothing else creates or destroys matter. Everything is the same generic ray with the same generic interaction, and everything follows from the generic transactions of the declared couplings; what remains is to close the binding couplings.

## 3.5 Fields are emergent descriptions

A field is a local description of ray state, flux or interaction structure. It is not an additional material substance independent of the underlying rays. Every ray is the same ray; a field ray is not a second kind. A ray has a field: the field is the ray's own information spreading in ray form to the Nodes around it, without an event, and the field's presence at a Node is an interaction that makes no event. A field never makes an event unless it meets something it changes; the first event a field is involved in is that meeting, and the returning ray that carries the recoil is split off from it, like every ray from its event. Where a field ray meets a ray whose declared coupling responds, the meeting is an ordinary interaction and its events change that ray's trajectory; everywhere else the field crosses without an event. One of those events is the field ray itself returning reversed: the return is the opposite momentum of the field, carried back along the field ray's line to the ray that released it, which recoils when the return arrives, at finite speed. This is how section 3.14 is satisfied: the recoil is a ray. Until its field meets something, a traveling ray pays nothing for it.

## 3.6 One underlying physics

Classical, quantum and field descriptions concern one modeled system of Node properties, events and Links, not separate material worlds. The Detector of section 3.19, a marked Node, is the only measurement mechanism within that description. A common framework and selected coupled experiments do not yet establish a complete derived unification of matter and fields.

## 3.7 Universal local laws

Equivalent local states with equivalent received inputs obey the same local rules, independent of position, total universe size or the labels assigned to an entity.

## 3.8 Causality has a finite speed

Ordinary physical propagation and transport cross adjacent Links at the finite causal speed bound c. A new event cannot instantaneously move stock, change a distant ordinary field or erase a remote path. A returning ray is ordinary propagation; it does not waive Node processing, output readiness or Link transit.

## 3.9 Fundamental propagation is local and stepwise

A physical ray advances only through connected neighboring Nodes. No physical trajectory may skip intermediate space.

## 3.10 Time is physical ordering

Model time orders local events and propagation in integer multiples of the minimum interval delta_t_min; no numerical SI value is assigned. Additional physical processing, output delay and Link transit have declared model durations. Host bookkeeping is measured separately. There is no zero-delay query; the Q-ORACLE-1 convention lapsed with section 3.18.

## 3.11 Discrete physical state

The adopted storage design uses bounded nonnegative integers, including zero, for values stored within a Node. Signed mathematical values require an explicit exact encoding; stored codes must not be confused with the values they represent. Ordinary core operations and their intermediates use bounded integers, without floating point, roots or trigonometry. The particular encoding is profile-specific; whether all working intermediates must also be nonnegative remains open.

## 3.12 Local bounded processing

Each Node performs one bounded local update per tick using fixed-capacity channels, bounded payloads and identifiers, and six adjacent connections. Per-Node work and storage must not grow with world size or elapsed history. No growing queue, remote search or same-tick multi-Link push cascade is allowed. These are accepted requirements; their encounter implementation still needs verification. History storage and total host work are accounted separately.

## 3.13 Interactions create observable properties

Properties attributed to a particle are inferred from how the underlying ray pattern interacts. A name such as electron, proton or mass does not itself supply a physical law or a hidden value.

## 3.14 No self-created force

An isolated closed physical structure cannot create net momentum from its own internal interactions. Local recoil is allowed only when an opposite momentum transfer is carried by rays or another explicitly owned local degree of freedom, so the total isolated system remains balanced.

## 3.15 Conservation is local accounting

Whenever a quantity is declared conserved, every local interaction and transfer must account for it exactly across all actual owners, including retained participants, products, recoil, fields, apparatus, in-flight values and remainders. A gain requires a corresponding loss, transfer or explicitly accounted source. Family and coupling definitions supply the physical readouts; the engine validates them without inventing energy or momentum from a label or computation-cost scalar. The conservation laws stay in force everywhere; they are the condition of reconstruction. Every declared invariant is exact across an interaction so that the event can be rebuilt from its pieces when they return. A ray returning from a Detector holds its event in order to reconstruct it, its momentum and everything that was there; without that, a return would erase events. A Detector that returns a ray is returning an event in time, undoing it by exactly what that piece carried. Exact integer arithmetic is what makes the undoing exact.

## 3.16 Momentum is directional

Momentum and other vector quantities are conserved component by component. Preserving only speed or vector magnitude is not sufficient.

## 3.17 Remainders are physical bookkeeping

Discrete division or allocation must not silently destroy information or conserved quantity. Every indivisible remainder has an explicit bounded owner and lifecycle. An overflow or unsupported numerical representation rejects the operation before mutation; it must not silently round, clamp or drop an owner.

## 3.18 Deleted on 2026-09-17

This section described a shared quantum resource (Q-ORACLE-1) as an explicit exception to Bell-local factorization. The model owner deleted it on 2026-09-17 because it contradicts the Detector of section 3.19: no owner answers at a distance, the first draw's outcome travels on the returning ray itself through the birth interaction to the partner, and ordinary locality holds without exception. The accepted price is that two Detectors at equal distance from the birth draw independently (CHSH at most 2 for spacelike settings). The number is kept so that the repository's dated records that cite it stay resolvable.

## 3.19 Measurement is an interaction

A measurement is an interaction at a Node whose Detector bit is set. Every Node carries one bit, Detector or not; the mark is bounded Node metadata (bit, setting, ticket seed), not a record and not an external device, and Detector behavior is how a Node behaves when the bit is set. A marked Node does one very simple thing. What arrives is a wave ray carrying information; every ray is a wave ray, so the kind makes no difference. For each transfer that arrives, whatever it is, it draws 1 or 0, the only lottery in the model. On 1 it behaves as an ordinary Node for that arrival and the transfer continues or interacts; on 0 it returns that wave ray on the same line in the opposite direction, unchanged, back the same number of steps it has made since its event, so that it arrives at the Node it left from with exactly the information it left with. Up to six transfers can arrive in one interval, one per Port, and the Node draws once for each, independently: the arrivals that drew 1 enter the ordinary interaction together, each arrival that drew 0 is returned on its own line. It reads, changes, absorbs and adds nothing; the click is the record of the bit drawn. A Detector sees nothing of the ray, on 1 or on 0: it sees only its own value. When it returned a ray with 0, that value travels with the ray, and the second Detector of the pair receives it on the ray that reaches it. Ordinary Node creation, propagation, interactions and emissions do not sample. A passive Recorder or Renderer does not perform a measurement or acquire sampling authority.

## 3.20 Coherent alternatives and Detector-authorized outcomes

Outside a Detector every trajectory an interaction permits actually happens; determinism does not select one classical trajectory. A new ordinary event does not authorize sampling. The 1-or-0 draw at a marked Node is the measurement itself. Replaying one committed Detector decision returns the same result without another draw, emission or inventory charge. Later calculation must preserve recorded history, not rewrite the past. Everything on the board is a transfer of information. An event is a splitting of information: each ray carries its own share of what happened at the event away from it. All the information is on the rays; the origin Node keeps nothing, and there is no register. Every ray carries the information of the last event it was involved in. If that event was at a Detector, the ray records that it was a Detector event and the bit drawn, 1 or 0; the bit is all the Detector adds. An event cannot be moved; there is no such thing. It happened at its Node, and a returning ray walks back exactly the number of steps it has made to reach it. A ray that meets a Detector is not obliged to return; the Detector may continue it as usual (1). A return (0) turns time back for that ray's share only: the returning ray carries what happened at the event, and at the event Node it performs the inverse split with its information, transmitting it to the same places the event sent to, so that it cancels what was already there and the momentum and energy of that share are restored exactly. The transmission is a ray like any other, with a field like any other: it cancels the share only where it meets it, and where it meets nothing it makes no event, by the same definitions. A share that left the event earlier on a straight line at the same speed is met only where it was delayed: bound at a Node, slowed by an output clock, changed by an interaction or standing at a Detector; for a pair this is the condition stated in section 5.4. Even when it is never caught, the event as it was has changed: the returned ray reversed its share, so the event lost that share, and the information is never lost, it chases the share it cancels. If the share is delayed and caught, momentum and everything else are conserved at the Node where they meet. A ray that passes is realized. Sibling events of one interaction are independent rays, each meeting its own fate; the other shares are untouched until their own rays return.

## 3.21 Emergence, not insertion

Large-scale laws must be derived from repeated local interactions. The desired macroscopic equation must not be inserted directly into the elementary update rule.

## 3.22 Scale independence

The same elementary laws apply in small test regions and in larger universes. Increasing the simulated size may add more Nodes and events, but it must not change the underlying local physics.

## 3.23 Symmetry is a requirement

Equivalent experiments under allowed shifts, orientations and other relevant transformations should produce equivalent physical behavior, subject only to genuine lattice effects that must be measured rather than hidden.

## 3.24 Geometry is relational

Spatial geometry is determined by the network of local connections and their propagation structure. Global coordinates are useful descriptions, not information required by local physics.

## 3.25 Complexity is emergent

Complex structures, apparent particles, material behavior and macroscopic laws must arise from repeated simple interactions among rays in local discrete space.

## 3.26 From symmetry groups to states and interactions on the board

Known symmetry groups and their representations constrain how property vectors transform and which couplings are allowed. A mathematical group is not a collection of moving objects: collections are interacting or correlated Node degrees of freedom whose propagation takes ray form. Families such as quarks are represented by property sectors; strong and weak interactions are operations on those sectors. Generic definitions must specify the local participants, transformations, conserved quantities and output channels, rather than infer a law from an entity or interaction name.

## 3.27 Generic laws, symmetry and vector operations define board events

The design chain is: generic schema → symmetry requirements → scalar/vector and matrix operations → events and Links in our spacetime. The same local rule applies to equivalent resident states and arrived inputs. Under allowed lattice transformations S, require F(SX, SI) = S F(X, I), or the corresponding equality of outcome distributions. A directed propagation pattern may break state symmetry without breaking law symmetry; generic code alone does not establish symmetry. Every proposed rule must identify where state is stored, what arrived, what operation acts, whether an outcome is recorded, how long it takes and what crosses each Link.

## 3.28 The computation field is a propagating property

The computation field is a Node property that propagates in ray form through ordinary neighboring Links, not an external scheduler instruction or additional substance. Once causally received, it may affect output timing through the declared local family rule. Each Node has six independent output-face clocks and no input clock delay. A split or emitted branch waits for its own output-face readiness; equal face values do not turn these into one shared Node clock.

```text
tau_out(v,d) = k_out(v,d) * delta_t_min; d in {+x, -x, +y, -y, +z, -z}
```

The bounded integer output count k_out is supplied by a declared local family/profile rule, including its application time and pending-output policy. Fixed neighboring Link transit H is separate: total travel time is the output delay plus H, without an input delay, double counting or same-tick multi-Link relay. Symmetry-equivalent inputs and directions require equivalent timing. Neither host CPU load nor a rest-phase formula defines this delay. Field transport, emission funding and remainders retain the same explicit ownership as other properties.

## 3.29 Observation is a frame-dependent representation of board reality

What an observer sees is a representation of the same underlying Node states and events, determined by the observer's reference frame, orientation, motion and measurement interaction. Observable records arise only from information that has causally reached the measuring system, not from an instantaneous view of the whole board.

```text
observed_description = Transform_frame(Readout(local_measurement_records))
```

Changing coordinates or basis changes an event's description; a measurement interaction may change state and record an outcome. These are distinct operations. Equivalent descriptions preserve declared invariants and consistent records. The Detector is a marked Node on the board (section 3.19), not an external device; it acts on what arrives through its Ports, on the board clock. A material eye or observer emerging on the board is a research goal, not a completed implementation. Detector, passive Recorder and Renderer remain distinct; a global audit display is not a physical observer.

## 3.30 One property engine, from abstract structure to detector experience

The purpose of Universe24 is to turn abstract mathematical descriptions of groups, representations, particle families and their properties into explicit board dynamics and, through a modeled detector, observable experience. Abstract does not mean imaginary. The engine uses one generic state schema and operation framework: fields, electrons, muons and gluons are distinguished by property content, representations and permitted interactions, not by separate fundamental engines. A ray is the propagation form of these properties, not an additional entity class. Uniform representation must retain physical differences, including charges, spin, statistics and couplings.

```text
property definitions + symmetry representations → Node state → propagation and interaction → detector records → observer-dependent display
```

At each Node, separately implemented generic operations evaluate owned properties and arrived inputs under immutable family/coupling definitions. The engine schedules, transports and validates; NodeState stores bounded data rather than physical formulas or executable expressions. Ordinary evolution is deterministic, while only a Node whose Detector bit is set draws. A Recorder stores evidence and a Renderer presents it. The material-eye and full species-dynamics goals remain separate from supported profiles; a visualization does not establish agreement with nature.

# 4. Central statement

Universe24 investigates one discrete Node-and-Link world in which properties propagate in ray form and matter, particles and mass are intended to emerge as stable patterns. Ordinary dynamics are local and deterministic; the only draw is at a Node whose Detector bit is set, and there is no shared resource, no hidden ordinary access and no second material world. Symmetry representations constrain generic property operations. Every mechanism must specify local state, arrivals, operations, owners, output clocks and causal transfers. The aim is to derive and test effective behavior without inserting the desired macroscopic laws. A defined contract or configured experiment is not yet a complete derived theory of nature.

# 5. Reading map

## 5.1 Node state and ray form

The state that moves is the ray (family properties, phase, heading, the number of steps it has made since its event, the information of its last event and, if that was a Detector event, its bit); a Node holds nothing but the rays resident this interval and, under a declared binding coupling, a bounded bound group. At a meeting of rays the declared coupling between their families decides no interaction, a deterministic interaction with exact invariants and at most six events out, or a Detector interaction. There is no occupied channel and no capacity rule: rays cross, meet or bind by their declared couplings, and nothing is pushed back or made to wait for room. The occupied-channel displacement rule of the 2026-09-16 revision was deleted on 2026-09-17.

## 5.2 Generic operations at a Node

Arrived input, one bounded local update per tick, a local proposal and atomic commit. Physical execution is at the Node; the separate generic operations package is code organization, not another physical place. Immutable family and coupling definitions own physical transformations and conserved readouts. The engine schedules, transports and validates, while NodeState contains bounded data and ownership, not physical formulas.

## 5.3 Couplings, fields and timing

Propagation, funded emission, remainders, six independent output clocks, no input delay and fixed neighboring Link transit H. Mass representation, rest phase and computation delay are distinct. Preserve existing free-ray self-field exclusion; newly output-delayed moving emitters remain unsupported until their composition is defined and tested. The strong-interaction long-residence and computation-field-emission idea is a research hypothesis, not proof of nuclear binding; weak conversion channels need their own explicit operators.

## 5.4 The Detector

Only a Node whose Detector bit is set may draw, and replay never redraws or re-emits. 1 = PASS is the marked Node behaving as an ordinary Node for that arrival, the ray continuing on its line or interacting; 0 = RETURN is the same wave ray reversed on its line, unchanged, walking back the number of steps it has made since its event. One draw per arriving transfer, independently for up to six arrivals in one interval; every ray is a wave ray, so the kind of ray makes no difference. A returning ray retraces its own trajectory by its step count, reaches its birth interaction with certainty and there performs the inverse split of its share: it transmits what happened at the event, with its bit, to the same places the event sent to, the partner ray's line among them, so the partner's Detector is not missing it: the first Detector saw only its own value, and the second Detector receives that value on the ray that reaches it. With two Detectors, Alice's and Bob's, whichever returns first sends its value through the birth event and the other receives it; sometimes it is Alice's information, sometimes Bob's. To Alice and Bob the correlation feels as if it were decided at time zero, but nothing happened at time zero: the value was carried through the birth event in event spacetime, one Link per interval. No registry answers at a distance; pair identity is the trajectory. The accepted price: two Detectors at equal distance from the birth draw independently and the CHSH value for spacelike settings is at most 2; the joint law's value appears only when the second ray's path exceeds the round trip through the first Detector. PASS/RETURN at a marked Node is the quantum measurement itself. The action distribution is not assumed to be 50/50. The return content is the arriving content unchanged; the return-content/phase laws, LOCK lifecycle, clock mapping and cancellation handling of the former shared resource lapsed with section 3.18.

## 5.5 Acceptance tests and open decisions

Every supported operation needs declared initial ownership, input, operator, expected output and model time, conserved readouts, edge cases and failure conditions. Accepted principles are not reopened by missing code or tests. Numerical family rules and Detector distributions need explicit closure where still undefined. The once-only encounter requirement needs independent tick traces and implementation evidence. A stated acceptance requirement is not a passing test.

# 6. History, implementation and evidence

The Evidence and references tab in the central specification collects code anchors and scoped previous results. Immutable event and wave-origin history is distinct from a Node's bounded active references and does not authorize remote history reads. Cancellation must follow the selected branch causally without deleting past records, unrelated paths or spatial topology. Exact bounded lookup, stopping, conflicting-notice and future-packet handling still require closure. A return undoes a share of an event on the board; it does not rewrite the recorded history, and no event is moved.

Git documents and source code describe particular software interfaces and experimental profiles; each result applies only to its identified source revision and tested scope. Existing generic-contact or capture samplers do not by themselves satisfy the Detector-only rule of section 3.19. Older shared-clock profiles and an incomplete six-output-clock candidate do not establish the complete adopted engine contract. Candidate annexes support implementation review but cannot silently replace adopted definitions. Bell results recorded with the former shared resource (section 3.18, deleted) are historical and are not evidence for the current model, and PASS/RETURN values carried on returning rays do not by themselves establish entanglement or spacelike Bell correlations. This documentation review adds no simulator execution or new passing result.

# 7. Working method

Only developers write or modify runtime code and tests. The architect coordinates interfaces; physics and mathematics own meanings and operators; experimental review fixes independent expectations; documentation maintains definitions and evidence status. These roles do not imply continuously running agents.

# 8. Documentation integrity check

The central specification owns adopted model decisions, the defined Detector and Node/Link acceptance, with open items identified explicitly. This document summarizes that owner rather than maintaining competing detailed laws. Review ordinary locality without exception, Detector-only sampling at marked Nodes, six-output timing and exact ownership. Distinguish unresolved numerical choices, engineering gaps and unproved emergence from already adopted principles. A candidate, unsupported profile or historical result must never silently override an adopted definition.

# 9. Assistant working instruction

Do not suggest a next step or follow-up action unless Alon explicitly asks for it.
