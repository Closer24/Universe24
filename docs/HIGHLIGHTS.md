# Universe24 Highlights (repository snapshot)

This file is a verbatim snapshot of the Google Doc
[Universe 24 Highlights](https://docs.google.com/document/d/1IkhSyqZZMBSgbJV-PMMwcXG0D_Rlfg4FrLy2jXBMUSs/edit),
taken on 2026-09-17 from the document revision modified on 2026-09-16 at
11:57 UTC. The live document remains the authoritative summary and may change
after this snapshot; the central model specification named in section 1 owns
model definitions, and [Highlights coverage](HIGHLIGHTS_IMPLEMENTATION.md)
records what the repository implements. Section numbering and wording below
are the document's own.

Proposed revision of 2026-09-17 (model owner's decisions on the ray-event
model): the paragraphs marked "Revision 2026-09-17" below are proposed for
the live document and are not yet in it. Their full statement is
[RAY_EVENT_MODEL.md](RAY_EVENT_MODEL.md) and postulate 23. By the model
owner's decision of 2026-09-17, section 3.18 (the shared quantum resource) is
withdrawn and is to be deleted from the live document, and the shared-resource
sentences of 5.4 lapse with it; the live text is kept below only until that
edit is made, with the decision recorded in place.

---

# Universe24 Highlights

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

An ordinary Node operation uses only its own bounded state and information that has causally arrived through its Links. It cannot read another Node's live state or apply an instantaneous distant field, movement or inventory update. The explicitly accepted shared quantum-resource exception is described in section 3.18; it is not a hidden extension of ordinary local access.

## 3.3 Ray-form propagation is fundamental

The board contains Node states and their properties, not a separate fundamental object called a ray. A ray names the universal form in which those properties and coherent alternatives propagate through neighboring Nodes. Interactions act on the local degrees of freedom that meet. There is no additional substance called matter; references to rays below refer to this propagation and its interaction patterns.

Revision 2026-09-17: an interaction is a meeting of rays at a Node, decided by the coupling declared between their families, and its result is at most six events, one per Port. An event is a change of trajectory: a new straight line leaving the interaction. A ray is the trajectory of one event between two interactions, reversible in time; a Node that a ray merely crosses hosts no event. Outside a Detector every trajectory an interaction permits actually happens; alternatives arise only at interactions. A wave ray carries a phase; light is a wave ray with no mass and no charge. A traveling ray releases a field, and the field is itself made of rays.

## 3.4 Matter is emergent

Particles, mass and the ordinary appearance of solid matter are intended to emerge as stable patterns of Node properties and their ray-form propagation and interactions. They are not additional fundamental substances. This is a research objective, not a claim that calibrated particle dynamics, mass or stable matter have already been derived.

Revision 2026-09-17: there is no matter in the model at this stage. Matter is the name for rays bound in one Node by a declared binding coupling (a neutron ray and a proton ray held together by the strong binding, an electron ray around them whose trajectory is changed at every step by the field rays the bound pair releases). Binding is the interaction whose result is zero events: the rays stay at the Node and interact again every interval. Mass is the retained energy of a bound group; the group's phase advance is its clock. Everything is the same generic ray with the same generic interaction; what remains is to close the binding couplings.

## 3.5 Fields are emergent descriptions

A field is a local description of ray state, flux or interaction structure. It is not an additional material substance independent of the underlying rays.

## 3.6 One underlying physics

Classical, quantum and field descriptions concern one modeled system of Node properties, events and Links, not separate material worlds. The accepted shared quantum owner is an explicit computational and measurement mechanism within that description. A common framework and selected coupled experiments do not yet establish a complete derived unification of matter and fields.

## 3.7 Universal local laws

Equivalent local states with equivalent received inputs obey the same local rules, independent of position, total universe size or the labels assigned to an entity.

## 3.8 Causality has a finite speed

Ordinary physical propagation and transport cross adjacent Links at the finite causal speed bound c. A new event cannot instantaneously move stock, change a distant ordinary field or erase a remote path. The named shared quantum resource does not waive ordinary Node processing, output readiness or Link transit.

## 3.9 Fundamental propagation is local and stepwise

A physical ray advances only through connected neighboring Nodes. No physical trajectory may skip intermediate space.

## 3.10 Time is physical ordering

Model time orders local events and propagation in integer multiples of the minimum interval delta_t_min; no numerical SI value is assigned. Additional physical processing, output delay and Link transit have declared model durations. Host bookkeeping is measured separately. The zero query-delay convention of Q-ORACLE-1 applies only to the permitted quantum query, not to ordinary transport or waiting.

## 3.11 Discrete physical state

The adopted storage design uses bounded nonnegative integers, including zero, for values stored within a Node. Signed mathematical values require an explicit exact encoding; stored codes must not be confused with the values they represent. Ordinary core operations and their intermediates use bounded integers, without floating point, roots or trigonometry. The particular encoding is profile-specific; whether all working intermediates must also be nonnegative remains open.

## 3.12 Local bounded processing

Each Node performs one bounded local update per tick using fixed-capacity channels, bounded payloads and identifiers, and six adjacent connections. Per-Node work and storage must not grow with world size or elapsed history. No growing queue, remote search or same-tick multi-Link push cascade is allowed. These are accepted requirements; their complete displacement and encounter implementation still needs verification. Shared quantum/history storage and total host work are accounted separately.

## 3.13 Interactions create observable properties

Properties attributed to a particle are inferred from how the underlying ray pattern interacts. A name such as electron, proton or mass does not itself supply a physical law or a hidden value.

## 3.14 No self-created force

An isolated closed physical structure cannot create net momentum from its own internal interactions. Local recoil is allowed only when an opposite momentum transfer is carried by rays or another explicitly owned local degree of freedom, so the total isolated system remains balanced.

## 3.15 Conservation is local accounting

Whenever a quantity is declared conserved, every local interaction and transfer must account for it exactly across all actual owners, including retained participants, products, recoil, fields, apparatus, in-flight values and remainders. A gain requires a corresponding loss, transfer or explicitly accounted source. Family and coupling definitions supply the physical readouts; the engine validates them without inventing energy or momentum from a label or computation-cost scalar.

Revision 2026-09-17: the conservation laws are the condition of reconstruction. Every declared invariant is exact across an interaction so that the event can be rebuilt from its pieces when they return; a Detector that returns a ray is returning an event in time, undoing it by exactly what that piece carried. Exact integer arithmetic is what makes the undoing exact.

## 3.16 Momentum is directional

Momentum and other vector quantities are conserved component by component. Preserving only speed or vector magnitude is not sufficient.

## 3.17 Remainders are physical bookkeeping

Discrete division or allocation must not silently destroy information or conserved quantity. Every indivisible remainder has an explicit bounded owner and lifecycle. An overflow or unsupported numerical representation rejects the operation before mutation; it must not silently round, clamp or drop an owner. Numerical rejection is distinct from the adopted occupied-channel displacement rule, which does not authorize capacity waiting.

## 3.18 Local dynamics and the explicit shared quantum exception

Q-ORACLE-1 and the named shared quantum profiles are already accepted project mechanisms. A permitted quantum query costs one model operation and zero query-delay model time; shared-state storage and host work are measured separately and need not be O(1). Only the declared quantum interface may use that shared state. It supplies no hidden remote input to ordinary fields, forces, movement or geometry, and no autonomous draw authority. Focus and diagnostics do not alter those boundaries. This is an explicit exception to Bell-local factorization, not a local hidden-variable derivation; no-signalling and symmetry must be checked separately.

Decision 2026-09-17 (model owner): this section is withdrawn and is to be deleted from the live document, because it contradicts the Detector as now defined. No owner answers at a distance. The first draw's outcome travels on the returning ray itself, through the birth interaction to the partner, and ordinary locality holds without exception. The accepted price is that two Detectors at equal distance from the birth draw independently (CHSH at most 2 for spacelike settings). The paragraph above is kept here only until the live document is edited; section 3.2's reference to it lapses with it.

## 3.19 Measurement is an interaction

A measurement requires an actual encounter with the external Detector through its declared causal interface. Only that Detector may authorize a draw under the declared measurement or exchange law. Ordinary Node creation, propagation, coherent interactions and emissions do not sample autonomously. The quantum owner may deterministically prepare states, operators, weights and conditional updates. A passive Recorder or Renderer does not perform a measurement or acquire sampling authority.

Revision 2026-09-17: every Node carries one bit, Detector or not; the mark is bounded Node metadata (bit, setting, ticket seed), not a record and not an external device, and Detector behavior is how a Node behaves when the bit is set. A marked Node does one very simple thing. What arrives is a ray carrying information, wave or not; the kind makes no difference. For each transfer that arrives, whatever it is, it draws 1 or 0, the only lottery in the model. On 1 it behaves as an ordinary Node for that arrival and the transfer continues or interacts; on 0 it returns that transfer on the same line in the opposite direction, unchanged, so that it arrives at the Node it left from with exactly the information it left with. Up to six transfers can arrive in one interval, one per Port, and the Node draws once for each, independently: the arrivals that drew 1 enter the ordinary interaction together, each arrival that drew 0 is returned on its own line. It reads, changes, absorbs and adds nothing; the click is the record of the bit drawn.

## 3.20 Coherent alternatives and Detector-authorized outcomes

The state may retain coherent alternatives and joint correlations during deterministic evolution. Determinism does not assign a sharp hidden value to every unmeasured observable or select a classical trajectory. A new ordinary event does not authorize sampling. An actual Detector measurement applies its specified conditional update; PASS/RETURN exchange is not automatically that quantum measurement. Replaying one committed Detector decision returns the same result without another draw, emission or inventory charge. Later calculation must preserve recorded history, not rewrite the past.

Revision 2026-09-17: everything on the board is a transfer of information. A ray carries a piece of information away from the interaction that created it, and that Node keeps the missing piece in a bounded register of open alternatives. A return is a deletion, not a message: the returning ray brings the piece back to its origin, which erases the open alternative; a ray that passes is realized. Sibling events of one interaction are independent rays, each meeting its own fate. An event is a splitting of information, and the information is recoverable: when its rays return to the same event the pieces reassemble. The event is its information, not a place, so it can be moved along the trajectory line and a returning ray still meets it.

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

Changing coordinates or basis changes an event's description; a measurement interaction may change state and record an outcome. These are distinct operations. Equivalent descriptions preserve declared invariants and consistent records. The current adopted Detector is external to the ordinary board and acts only through its defined causal interface. Detector clock mapping remains open. A material eye or observer emerging on the board is a research goal, not a completed implementation. Detector, passive Recorder and Renderer remain distinct; a global audit display is not a physical observer.

## 3.30 One property engine, from abstract structure to detector experience

The purpose of Universe24 is to turn abstract mathematical descriptions of groups, representations, particle families and their properties into explicit board dynamics and, through a modeled detector, observable experience. Abstract does not mean imaginary. The engine uses one generic state schema and operation framework: fields, electrons, muons and gluons are distinguished by property content, representations and permitted interactions, not by separate fundamental engines. A ray is the propagation form of these properties, not an additional entity class. Uniform representation must retain physical differences, including charges, spin, statistics and couplings.

```text
property definitions + symmetry representations → Node state → propagation and interaction → detector records → observer-dependent display
```

At each Node, separately implemented generic operations evaluate owned properties and arrived inputs under immutable family/coupling definitions. The engine schedules, transports and validates; NodeState stores bounded data rather than physical formulas or executable expressions. Ordinary evolution is deterministic, while only an actual external Detector encounter authorizes a draw. A Recorder stores evidence and a Renderer presents it. The material-eye and full species-dynamics goals remain separate from supported profiles; a visualization does not establish agreement with nature.

# 4. Central statement

Universe24 investigates one discrete Node-and-Link world in which properties propagate in ray form and matter, particles and mass are intended to emerge as stable patterns. Ordinary dynamics are local and deterministic; the accepted shared quantum resource and external Detector interface are explicit mechanisms, not hidden ordinary access or a second material world. Symmetry representations constrain generic property operations. Every mechanism must specify local state, arrivals, operations, owners, output clocks and causal transfers. The aim is to derive and test effective behavior without inserting the desired macroscopic laws. A defined contract or configured experiment is not yet a complete derived theory of nature.

# 5. Reading map

## 5.1 Node state and ray form

NodeState, six-neighbor topology and fixed K channels: each channel retains at most one active event ID with its complete property bundle. The adopted occupied-channel rule pushes the saved event toward its origin along the same path while the counter-signal travels the other way; it does not use capacity waiting. Presence of the same event at the current and adjacent upstream Node must prevent missed encounters, with one actual inventory owner and one committed effect. Exact simultaneous-update, overlap-retirement and finite-identity handling require implementation evidence; the principles are already adopted.

Revision 2026-09-17: the state that moves is the ray (family properties, phase, heading, step count since the last interaction, one bounded outcome register); a Node holds nothing but the rays resident this interval and, under a declared binding coupling, a bounded bound group. At a meeting of rays the declared coupling between their families decides no interaction, a deterministic interaction with exact invariants and at most six events out, or a Detector interaction.

## 5.2 Generic operations at a Node

Arrived input, one bounded local update per tick, a local proposal and atomic commit. Physical execution is at the Node; the separate generic operations package is code organization, not another physical place. Immutable family and coupling definitions own physical transformations and conserved readouts. The engine schedules, transports and validates, while NodeState contains bounded data and ownership, not physical formulas.

## 5.3 Couplings, fields and timing

Propagation, funded emission, remainders, six independent output clocks, no input delay and fixed neighboring Link transit H. Mass representation, rest phase and computation delay are distinct. Preserve existing free-ray self-field exclusion; newly output-delayed moving emitters remain unsupported until their composition is defined and tested. The strong-interaction long-residence and computation-field-emission idea is a research hypothesis, not proof of nuclear binding; weak conversion channels need their own explicit operators. Physical interaction delay is not occupied-capacity waiting.

## 5.4 Quantum action and Detector

The shared quantum action and resource exception are already accepted; profile integration is separate. Only an actual external Detector encounter may draw, and replay never redraws or re-emits. Its separate exchange interface uses 1 = PASS and 0 = RETURN/CANCEL. PASS can follow an action draw but preserves received content and provenance without another content draw; passing Detector-generated content adopts it under LOCK. RETURN generates under its declared law and proceeds backward along the selected branch in space, forward in time, without erasing history. The action distribution is not assumed to be 50/50. Return-content/phase laws, LOCK lifecycle, clock mapping and complete bounded cancellation handling remain open. Pair profiles, general shared state and PASS/RETURN are not interchangeable.

Revision 2026-09-17: 1 = PASS is the marked Node behaving as an ordinary Node for that arrival, the ray continuing on its line or interacting; 0 = RETURN is the same ray reversed on its line, unchanged. One draw per arriving transfer, wave or not, independently for up to six arrivals in one interval. A returning ray retraces its own trajectory by its step count, reaches its birth interaction with certainty and continues straight toward the partner ray, carrying the number the partner's Detector was missing. No registry answers at a distance; pair identity is the trajectory. The accepted price: two Detectors at equal distance from the birth draw independently and the CHSH value for spacelike settings is at most 2; the joint law's value appears only when the second ray's path exceeds the round trip through the first Detector. By the decision of 2026-09-17 PASS/RETURN at a marked Node is the quantum measurement itself; the separate shared resource that the paragraph above keeps distinct is withdrawn together with section 3.18.

## 5.5 Acceptance tests and open decisions

Every supported operation needs declared initial ownership, input, operator, expected output and model time, conserved readouts, edge cases and failure conditions. Accepted principles are not reopened by missing code or tests. Numerical family rules and Detector distributions need explicit closure where still undefined. The no-capacity-wait displacement, bounded two-Node presence and once-only encounter requirements need independent tick traces and implementation evidence. A stated acceptance requirement is not a passing test.

# 6. History, implementation and evidence

The Evidence and references tab in the central specification collects code anchors and scoped previous results. Immutable event and wave-origin history is distinct from a Node's bounded active references and does not authorize remote history reads. Cancellation must follow the selected branch causally without deleting past records, unrelated paths or spatial topology. Exact bounded lookup, stopping, conflicting-notice and future-packet handling still require closure. Moving an active event is not rewriting its recorded history.

Git documents and source code describe particular software interfaces and experimental profiles; each result applies only to its identified source revision and tested scope. Existing generic-contact or capture samplers do not by themselves satisfy the latest external-Detector-only rule. Older shared-clock profiles and an incomplete six-output-clock candidate do not establish the complete adopted engine contract. Candidate annexes support implementation review but cannot silently replace adopted definitions. Bell results using the admitted shared resource are not evidence of a Bell-local derivation, and communicated PASS/RETURN values do not by themselves establish entanglement or spacelike Bell correlations. This documentation review adds no simulator execution or new passing result.

# 7. Working method

Only developers write or modify runtime code and tests. The architect coordinates interfaces; physics and mathematics own meanings and operators; experimental review fixes independent expectations; documentation maintains definitions and evidence status. These roles do not imply continuously running agents.

# 8. Documentation integrity check

The central specification owns adopted model decisions, the defined quantum action and Node/Link acceptance, with open items identified explicitly. This document summarizes that owner rather than maintaining competing detailed laws. Review ordinary locality together with the named quantum exception, external Detector-only sampling, six-output timing, exact ownership and the no-capacity-wait requirement. Distinguish unresolved numerical choices, engineering gaps and unproved emergence from already adopted principles. A candidate, unsupported profile or historical result must never silently override an adopted definition.

# 9. Assistant working instruction

Do not suggest a next step or follow-up action unless Alon explicitly asks for it.
