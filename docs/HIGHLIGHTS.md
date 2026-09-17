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

The whole model, as decided on 2026-09-17, is four definitions and one principle; section 3 states each in full.

1. **Event and ray** (3.3, 3.20). A ray is a straight trajectory between two events and carries information. An event is where information splits, at a Node, by the declared coupling, into at most six rays. There is no third thing.
2. **Detector** (3.19, 5.4). A Node with a bit. On 1 the ray passes, and that pass is the only measurement. On 0 the Node returns the ray untouched, without reading it; the return cancels that ray's share of its event and carries it to the sibling lines. No register, nothing at a distance.
3. **Phase** (3.3). Every ray is a wave ray. Its phase advances at the rest rate of its family, which is its mass; light's rate is zero and it carries its emitter's clock. Interference is steering of content by phase difference, the Born rule as a declared table.
4. **Field** (3.5, 3.28). A ray's field is its own information spreading in ray form in all directions. It makes an event only where it meets something it changes: delay, bending, a changed trajectory, and the field ray returning with the opposite momentum. The computation field, which is gravity, obeys the same rule.

The principle (3.15): every declared invariant is exact, in bounded integers, at every event, because only then can an event be rebuilt from its parts when they return.

Think of Universe24 as a kind of multidimensional Snake game with obstacles and interactions. Multiple rays move through the same 3D Node network across compatible property and field channels. They may cross without responding, respond weakly, or interact very strongly according to their selected coupling; crossing or co-location alone is not a collision. Here, weak and strong describe response strength, not automatically the fundamental weak and strong forces. Multidimensional includes independent state channels, not extra spatial dimensions. Obstacles are an analogy for declared interactions, not invented opaque walls or a capacity fix. Ordinary evolution is deterministic; only an actual Detector generates a draw. The central specification remains the precise definition.

# 3. Foundational postulates

## 3.1 Discrete local space

The adopted board is a connected three-dimensional cubic network. Each local Node connects to six neighboring Nodes through directional Ports and Links. The selected layout is periodic; boundary choices belong to explicit experiment configuration. NodeState is the unit of local state. No fixed private-register decomposition or 36-register layer is required.

## 3.2 Ordinary Node dynamics are local

An ordinary Node operation uses only its own bounded state and information that has causally arrived through its Links. It cannot read another Node's live state or apply an instantaneous distant field, movement or inventory update. There is no exception: the Detector of section 3.19 is a Node like any other, and the number a pair shares travels on the returning ray (section 5.4). Section 3.18, which described a shared quantum-resource exception, was deleted on 2026-09-17.

## 3.3 Ray-form propagation is fundamental

**Two definitions.** The board contains Node states and their properties, not a separate fundamental object called a ray. A ray names the universal form in which those properties propagate through neighboring Nodes. The system has exactly two definitions, event and ray: a ray carries information, and an event is where that information splits; a ray is what was split off from an event.

**Interaction and event.** An interaction is a meeting of rays at a Node, decided by the coupling declared between their families, and its result is at most six events, one per Port. An event is a change of trajectory: a new straight line leaving the interaction. A ray is the trajectory of one event between two interactions, reversible in time; a Node that a ray merely crosses hosts no event. From its event, every ray carries the number of steps it has made. Outside a Detector every trajectory an interaction permits actually happens; alternatives arise only at interactions.

**Phase.** Every ray is a wave ray and carries a phase; a plain ray is a special case of the wave ray, not a second kind. Light is a wave ray with no mass and no charge. Three things change a phase and nothing else: each interval advances it at the rest rate its family declares, which is the ray's mass as a clock, and that rate is zero for light, whose phase does not advance along its own line; an interaction changes it as the declared coupling says; a bound group advances it once per interval it is held. A light ray carries the phase of the clock that emitted it at the moment of emission and delivers it unchanged, so the frequency of light is the rate of its emitter's clock.

**Amplitude and interference.** There is no amplitude as a number and no probability field: the phase and the ray's conserved content together are the discrete stand-in for the quantum amplitude, the phase as its angle and the conserved content as its size. Because every trajectory an interaction permits actually happens, the intensity at a place is how much content arrived there, and interference is steering: where rays meet in one layer, the declared coupling reads their phase difference and decides through which Port the shared content leaves, with every invariant exact; nothing is erased. The basic steering coupling is the Born rule stated as a coupling: for a phase difference δ it splits the shared content between the two candidate Ports in the ratio cos²(δ/2) to sin²(δ/2), as a declared table of bounded integer ratios with the remainder owned as section 3.17 requires, so that click intensities follow the Born rule with nothing read by any Detector. It is declared, not derived. The Detector reads none of this; the probability of a click is already in how much content reached it. Interference of light follows from this alone: two paths of different length reach one place at one time only if their rays were emitted at different times, so they carry different emission phases, and the difference is the emitter's rate times the difference in path length; nothing is accumulated on the way.

**Field and matter.** A traveling ray releases a field, and the field is itself made of rays (section 3.5). There is no additional substance called matter (section 3.4); references to rays below refer to this propagation and its interaction patterns.

## 3.4 Matter is emergent

**Research objective.** Particles, mass and the ordinary appearance of solid matter are intended to emerge as stable patterns of Node properties and their ray-form propagation and interactions. They are not additional fundamental substances. This is a research objective, not a claim that calibrated particle dynamics, mass or stable matter have already been derived. There is no matter in the model at this stage.

**Matter is a bound group.** Matter is the name for rays bound in one Node by a declared binding coupling (a neutron ray and a proton ray held together by the strong binding, an electron ray around them whose trajectory is changed at every step by the field rays the bound pair releases). Binding is the interaction whose result is zero events: the rays stay at the Node and interact again every interval. Mass is the retained energy of a bound group; the group's phase advance is its clock.

**Lifetime and unbinding.** A bound group has no lifetime of its own: it lasts as long as the binding interaction repeats at that Node without releasing an event. The binding may be nothing more than a very large output-clock delay (section 3.28) that the bound rays create together, a large mass making the Node very slow, so that the rays do not leave. It is unbound the same way anything else happens on the board: a ray arrives (a high-energy light ray, for instance; there is no photon, only a ray) and the coupling declared for the families present produces events that leave. Nothing else creates or destroys matter. Everything is the same generic ray with the same generic interaction, and everything follows from the generic transactions of the declared couplings; what remains is to close the binding couplings.

## 3.5 Fields are emergent descriptions

**What a field is.** A field is a local description of ray state, flux or interaction structure. It is not an additional material substance independent of the underlying rays. Every ray is the same ray; a field ray is not a second kind. A ray has a field: the field is the ray's own information spreading in ray form to the Nodes around it, without an event, and the field's presence at a Node is an interaction that makes no event. The field is released in all directions.

**When a field acts.** A field never makes an event unless it meets something it changes; the first event a field is involved in is that meeting, and the returning ray that carries the recoil is split off from it, like every ray from its event. Where a field ray meets a ray whose declared coupling responds, the meeting is an ordinary interaction and its events change that ray's trajectory; everywhere else the field crosses without an event. One of those events is the field ray itself returning reversed: the return is the opposite momentum of the field, carried back along the field ray's line to the ray that released it, which recoils when the return arrives, at finite speed. This is how section 3.14 is satisfied: the recoil is a ray. Until its field meets something, a traveling ray pays nothing for it.

**No self-field.** A ray traveling straight never meets its own field: the field is born where the ray is and leaves at the causal speed, ahead of the ray or away from it, and the ray is never faster than its field; no exclusion rule is needed. Only after a change of trajectory can a ray cross field it released earlier, and that is a meeting like any other. A ray's phase per step comes from its family rate alone (section 3.3), not from its own field.

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

**Exact accounting.** Whenever a quantity is declared conserved, every local interaction and transfer must account for it exactly across all actual owners, including retained participants, products, recoil, fields, apparatus, in-flight values and remainders. A gain requires a corresponding loss, transfer or explicitly accounted source. Family and coupling definitions supply the physical readouts; the engine validates them without inventing energy or momentum from a label or computation-cost scalar.

**Why: reconstruction.** The conservation laws stay in force everywhere; they are the condition of reconstruction. Every declared invariant is exact across an interaction so that the event can be rebuilt from its pieces when they return. A ray returning from a Detector holds its event in order to reconstruct it, its momentum and everything that was there; without that, a return would erase events. A Detector that returns a ray is returning an event in time, undoing it by exactly what that piece carried. Exact integer arithmetic is what makes the undoing exact.

## 3.16 Momentum is directional

Momentum and other vector quantities are conserved component by component. Preserving only speed or vector magnitude is not sufficient.

## 3.17 Remainders are physical bookkeeping

Discrete division or allocation must not silently destroy information or conserved quantity. Every indivisible remainder has an explicit bounded owner and lifecycle. An overflow or unsupported numerical representation rejects the operation before mutation; it must not silently round, clamp or drop an owner.

## 3.18 Deleted on 2026-09-17

This section described a shared quantum resource (Q-ORACLE-1) as an explicit exception to Bell-local factorization. The model owner deleted it on 2026-09-17 because it contradicts the Detector of section 3.19: no owner answers at a distance, the first draw's outcome travels on the returning ray itself through the birth interaction to the partner, and ordinary locality holds without exception. The accepted price is that two Detectors at equal distance from the birth draw independently (CHSH at most 2 for spacelike settings). The number is kept so that the repository's dated records that cite it stay resolvable.

## 3.19 Measurement is an interaction

**The mark.** A measurement is an interaction at a Node whose Detector bit is set. Every Node carries one bit, Detector or not; the mark is bounded Node metadata (bit, setting, ticket seed), not a record and not an external device, and Detector behavior is how a Node behaves when the bit is set. A source is a Detector: whatever emits a ray of a known family is a marked Node, because knowing the family of what it emits is a measurement. The birth event of a pair therefore happens at a marked Node, which draws on every arrival like any other.

**The draw.** A marked Node does one very simple thing. What arrives is a wave ray carrying information; every ray is a wave ray, so the kind makes no difference. For each transfer that arrives, whatever it is, it draws 1 or 0, the only lottery in the model. Up to six transfers can arrive in one interval, one per Port, and the Node draws once for each, independently: the arrivals that drew 1 enter the ordinary interaction together, each arrival that drew 0 is returned on its own line. It reads, changes, absorbs and adds nothing. A Detector sees nothing of the ray, on 1 or on 0: it sees only its own value.

**1, the measurement.** On 1 the Node behaves as an ordinary Node for that arrival and the transfer continues or interacts. A measurement exists only when the Node drew 1 and let the ray pass; the click is the record of that 1.

**0, no measurement.** On 0 the Node returns that wave ray on the same line in the opposite direction, unchanged, back the same number of steps it has made since its event, so that it arrives at the Node it left from with exactly the information it left with. On 0 there is no measurement: the Node returns the ray without touching it and is a Node without measurement, as if the ray had not arrived, and it waits for what the return brings back. When it returned a ray with 0, that value travels with the ray, and the second Detector of the pair receives it on the ray that reaches it.

**Nothing else samples.** Ordinary Node creation, propagation, interactions and emissions do not sample. A passive Recorder or Renderer does not perform a measurement or acquire sampling authority.

**The external body (model owner, 2026-09-17; named "fixed body" earlier that day).** Beside the Detector there is one more marked element of a world, and like the Detector it is a declaration, not physics: an external body, a Node declared to hold a family with an amount and, if wanted, a charge, standing for a star, a neutron star, a fixed proton, a large charge, or a piece of apparatus. What is declared: the family, the amount (finite, of any width, since it enters no sum; it only sets how much field leaves per interval), the charge, and, if wanted, a trajectory. What it does: it radiates exactly as any bound group does, by the one field rule of section 3.5 and with the strength its amount gives, so its gravity and its electric field are the ordinary field rays of the model and every ray that meets them responds by its declared coupling. What it does not do: it does not spread, which is its defining property: it never splits, binds, unbinds, converts or decays, and its whole content stays at one Node; and it is not pushed: whatever arrives at it, a recoil field ray or a ray that couples to it, is met by the declared coupling of its family, and the body itself never changes. Absorption into an explicitly accounted sink is the default coupling, and the other couplings make the apparatus: a reversed heading is a mirror, a split by a declared table is a beam splitter, a phase offset is a phase plate, a polarization read is a polarizer once feature 11 exists; a wall, a screen and a beam stop are the default. It may move on a declared trajectory, and wherever it is, the Node it is at holds all of it; its motion is declared, never caused, because nothing on the board can push it, so two external bodies never move each other. The audit books what it radiates as a source and what it absorbs as a sink, so conservation stays exact at every tick. On the Node it is bounded metadata like the Detector mark: the kind of mark, the declaration, and one exact counter (the sink totals per family); no rays, no history. When the back-reaction is wanted, a star that recoils or a proton that moves, the body is not used: the same thing is declared as an ordinary bound group with a large amount, and then it spreads and is pushed like all matter. The external body is the approximation of infinite mass, used for the confrontation runs: light bending by a star, an electron near a large charge, a hydrogen-like spectrum around a fixed proton, and the two-slit and Bell geometries with their walls, mirrors and splitters.

## 3.20 Coherent alternatives and Detector-authorized outcomes

**Alternatives.** Outside a Detector every trajectory an interaction permits actually happens; determinism does not select one classical trajectory. A new ordinary event does not authorize sampling. The 1-or-0 draw at a marked Node is the measurement itself. Replaying one committed Detector decision returns the same result without another draw, emission or inventory charge. Later calculation must preserve recorded history, not rewrite the past.

**Everything is information on rays.** Everything on the board is a transfer of information. An event is a splitting of information: each ray carries its own share of what happened at the event away from it. All the information is on the rays; the origin Node keeps nothing, and there is no register. Every ray carries the information of the last event it was involved in. If that event was at a Detector, the ray records that it was a Detector event and the bit drawn, 1 or 0; the bit is all the Detector adds. An event cannot be moved; there is no such thing. It happened at its Node, and a returning ray walks back exactly the number of steps it has made to reach it.

**Entanglement is the name for siblings of one event (2026-09-17).** Rays that left the same last event carry the same record of it, and nothing reads that record until a Detector; that shared record, and the trajectory back to the event, are all there is to entanglement. Nothing else is shared: no register, no state at a distance. A Detector that draws 1 realizes its ray; a Detector that draws 0 returns it, and the returning ray delivers what it carries to the sibling lines through the event (section 5.4). Whatever happens between an event and the first PASS is therefore a correlated set of rays, and PASS is the only thing that ends it. An ordinary meeting on the way is itself an event: its outputs are new siblings of that new event, and each ray's siblings are always those of its own last event. The earlier correlation is not lost: the transmission from a return chases the share through the later event by the rule above, which is how correlation passes from one pair to another without any rule for it. The price of section 5.4 applies to every such set.

**A return is the inverse split.** A ray that meets a Detector is not obliged to return; the Detector may continue it as usual (1). A return (0) turns time back for that ray's share only: the returning ray carries what happened at the event, and at the event Node it performs the inverse split with its information, transmitting it to the same places the event sent to, so that it cancels what was already there and the momentum and energy of that share are restored exactly. A ray that passes is realized. Sibling events of one interaction are independent rays, each meeting its own fate; the other shares are untouched until their own rays return.

**The transmission is a ray.** The transmission is a ray like any other, with a field like any other: it cancels the share only where it meets it, and where it meets nothing it makes no event, by the same definitions. A share that left the event earlier on a straight line at the same speed is met only where it was delayed: bound at a Node, slowed by an output clock, changed by an interaction or standing at a Detector; for a pair this is the condition stated in section 5.4. Even when it is never caught, the event as it was has changed: the returned ray reversed its share, so the event lost that share, and the information is never lost, it chases the share it cancels. If the share is delayed and caught, momentum and everything else are conserved at the Node where they meet.

**Return modes.** What a returning ray does at its event Node when nothing is there is a configured mode of the world, three of which are defined and tested: siblings, the default and the rule above (it transmits its share and bit to every line the event sent to, which needs at most six records on the ray, one per Port); straight (it continues straight through the Node on the one line opposite its own, enough for a pair, with no records); and annul (it ends there, its content leaves the world into an explicitly accounted sink, initial equals current plus escaped plus annulled at every tick, and its information survives only in the record). If something is at the Node, a bound group or other rays, the returning ray meets it by the declared coupling in every mode.

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

**Forces and polarization are catalog entries, not engine mechanisms (approved 2026-09-17).** The engine performs only the simple operations: a step on a Link, a phase advance, a split by a declared table, a sum, and the one draw at a marked Node. Anything that does not change how a ray moves between events is therefore a family property in the catalog or a coupling table, read only at a meeting, exactly as charge is. Polarization is such a property: a transverse mode perpendicular to the heading, two states for light (the two lattice axes perpendicular to an axial heading) and two for the electron family (spin), read by the declared couplings at a meeting; a circular polarization is not defined and, if wanted, would be a transverse direction that turns with the phase plus one handedness bit, again a catalog choice. Pauli exclusion is a binding coupling that does not fire for two electrons in the same state with the same spin. Polarization is feature 11, after the ten features of the ray-event migration; none of them needs it, and the Bell prediction of hypothesis 11 is testable without it in its phase form. The strong interaction is the same pattern: quark families, colour a property with three values, the gluon the quark's own field in ray form (section 3.5), the binding of three quarks a binding coupling (section 3.4); its short range and its growth with distance are expected from one more declared coupling, the quark's field rays binding to each other, and whether that yields confinement is a research question, not an engine decision. The weak interaction is a change of family: an N-to-M conversion at an event with its declared invariants (charge, energy, momentum). A free particle never decays, because there is no event without a meeting and a straight ray does not change; a neutron is a bound group whose ticks are events, and a bound group that can decay is a source, and a source is a Detector (section 3.19): at each tick it draws with its declared ratio as the setting, 1 = the conversion fires, 0 = the group ticks on unchanged, so half-life follows and nothing else in the world draws. None of this adds anything to the engine; all of it comes after feature 10.

## 3.27 Generic laws, symmetry and vector operations define board events

The design chain is: generic schema → symmetry requirements → scalar/vector and matrix operations → events and Links in our spacetime. The same local rule applies to equivalent resident states and arrived inputs. Under allowed lattice transformations S, require F(SX, SI) = S F(X, I), or the corresponding equality of outcome distributions. A directed propagation pattern may break state symmetry without breaking law symmetry; generic code alone does not establish symmetry. Every proposed rule must identify where state is stored, what arrived, what operation acts, whether an outcome is recorded, how long it takes and what crosses each Link.

## 3.28 The computation field is a propagating property

The computation field is a Node property that propagates in ray form through ordinary neighboring Links, not an external scheduler instruction or additional substance. Once causally received, it may affect output timing through the declared local family rule. Each Node has six independent output-face clocks and no input clock delay. A split or emitted branch waits for its own output-face readiness; equal face values do not turn these into one shared Node clock.

```text
tau_out(v,d) = k_out(v,d) * delta_t_min; d in {+x, -x, +y, -y, +z, -z}
```

The bounded integer output count k_out is supplied by a declared local family/profile rule, including its application time and pending-output policy. Fixed neighboring Link transit H is separate: total travel time is the output delay plus H, without an input delay, double counting or same-tick multi-Link relay. Symmetry-equivalent inputs and directions require equivalent timing. Neither host CPU load nor a rest-phase formula defines this delay. Field transport, emission funding and remainders retain the same explicit ownership as other properties.

**Gravity is bending by delay.** The computation field obeys the one field rule of section 3.5, with no rule of its own: the retained content of a Node (its mass, section 3.4) is what makes it slow, and the information that a Node is heavy spreads from it in ray form in all directions. Where such a field ray meets a ray whose declared coupling responds, there is an event with two effects: the ray that was met is delayed (its output clock grows, the action of this section), and the field ray returns reversed to the heavy Node. The delay is larger on the side nearer the heavy Node, so the ray bends toward it; that bending is a change of momentum, and the returning field ray carries the opposite momentum back to the heavy Node, which is drawn toward the ray. Gravity is this bending by delay; it is not inserted as a force, nothing is absorbed, and momentum is exact.

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

**State.** The state that moves is the ray (family properties, phase, heading, the number of steps it has made since its event, the information of its last event and, if that was a Detector event, its bit); a Node holds nothing but the rays resident this interval and, under a declared binding coupling, a bounded bound group.

**Meetings.** At a meeting of rays the declared coupling between their families decides no interaction, a deterministic interaction with exact invariants and at most six events out, or a Detector interaction. There is no occupied channel and no capacity rule: rays cross, meet or bind by their declared couplings, and nothing is pushed back or made to wait for room. The occupied-channel displacement rule of the 2026-09-16 revision was deleted on 2026-09-17.

**Layers.** Event spacetime has layers: two events can happen at the same Node in the same interval in layers that do not communicate, because rays whose families have no declared coupling never meet; they cross as if the other were not there. A layer is a set of families that couple; a meeting exists only inside a layer.

## 5.2 Generic operations at a Node

Arrived input, one bounded local update per tick, a local proposal and atomic commit. Physical execution is at the Node; the separate generic operations package is code organization, not another physical place. Immutable family and coupling definitions own physical transformations and conserved readouts. The engine schedules, transports and validates, while NodeState contains bounded data and ownership, not physical formulas.

## 5.3 Couplings, fields and timing

Propagation, funded emission, remainders, six independent output clocks, no input delay and fixed neighboring Link transit H. Mass representation, rest phase and computation delay are distinct. A free ray never meets its own field because the field is faster and leaves ahead of it or away from it (section 3.5); newly output-delayed moving emitters remain unsupported until their composition is defined and tested. The strong-interaction long-residence and computation-field-emission idea is a research hypothesis, not proof of nuclear binding; weak conversion channels need their own explicit operators. Both, and polarization, are catalog entries on the same engine (section 3.26), scheduled after feature 10.

## 5.4 The Detector

**PASS and RETURN.** Only a Node whose Detector bit is set may draw, and replay never redraws or re-emits. 1 = PASS is the marked Node behaving as an ordinary Node for that arrival, the ray continuing on its line or interacting; 0 = RETURN is the same wave ray reversed on its line, unchanged, walking back the number of steps it has made since its event. One draw per arriving transfer, independently for up to six arrivals in one interval; every ray is a wave ray, so the kind of ray makes no difference. PASS/RETURN at a marked Node is the quantum measurement itself. Only PASS is a measurement; RETURN is none: nothing is measured, nothing is recorded as an outcome, the Node waits. The action distribution is not assumed to be 50/50. The return content is the arriving content unchanged; the return-content/phase laws, LOCK lifecycle, clock mapping and cancellation handling of the former shared resource lapsed with section 3.18.

**A pair.** A returning ray retraces its own trajectory by its step count, reaches its birth interaction with certainty and there performs the inverse split of its share: it transmits what happened at the event, with its bit, to the same places the event sent to, the partner ray's line among them, so the partner's Detector is not missing it: the first Detector saw only its own value, and the second Detector receives that value on the ray that reaches it. With two Detectors, Alice's and Bob's, whichever returns first sends its value through the birth event and the other receives it; sometimes it is Alice's information, sometimes Bob's. To Alice and Bob the correlation feels as if it were decided at time zero, but nothing happened at time zero: the value was carried through the birth event in event spacetime, one Link per interval. Every Detector behaves the same: the second Detector draws its own bit on that arrival like on any other and reads nothing from the ray; the received value is information on the ray, not an input to the draw. The information of the last event and the Detector's bit stay on the ray as hidden variables: no Detector and no ordinary coupling reads them today, they come from no ordinary physics, and for now they affect no one; nothing on the board feels them.

**The price.** No registry answers at a distance; pair identity is the trajectory. The accepted price: two Detectors at equal distance from the birth draw independently and the CHSH value for spacelike settings is at most 2; the joint law's value appears only when the second ray's path exceeds the round trip through the first Detector.

## 5.5 Acceptance tests and open decisions

Every supported operation needs declared initial ownership, input, operator, expected output and model time, conserved readouts, edge cases and failure conditions. Accepted principles are not reopened by missing code or tests. Numerical family rules and Detector distributions need explicit closure where still undefined. The once-only encounter requirement needs independent tick traces and implementation evidence. A stated acceptance requirement is not a passing test.

**How tests are written and run (model owner, 2026-09-17).** The engine is generic and its rules are separated, so a test exercises one generic rule in isolation on a minimal board and nothing else: one test module per rule, one per feature of the ray-event model, with the expected integers written down before the first run. No test pins the numbers of an example world, compares two worlds or reproduces a known experiment; those are research runs (section 6), made once, recorded with a fingerprint and a date, and never repeated as tests. A change is checked only against the tests that depend on what it changed, selected by the import graph; the whole suite runs together only when the shared core changes (the Node and its Ports, the order of the cycle, the bounded integers, the phase), and then once, in parallel. A physical milestone, a phenomenon that several rules produce together, is one run of the engine with a fingerprint and a dated record, not a suite. The cost of checking is proportional to the risk of the change, never constant.

# 6. History, implementation and evidence

The Evidence and references tab in the central specification collects code anchors and scoped previous results. Immutable event and wave-origin history is distinct from a Node's bounded active references and does not authorize remote history reads. Cancellation must follow the selected branch causally without deleting past records, unrelated paths or spatial topology. Exact bounded lookup, stopping, conflicting-notice and future-packet handling still require closure. A return undoes a share of an event on the board; it does not rewrite the recorded history, and no event is moved.

Git documents and source code describe particular software interfaces and experimental profiles; each result applies only to its identified source revision and tested scope. Existing generic-contact or capture samplers do not by themselves satisfy the Detector-only rule of section 3.19. Older shared-clock profiles and an incomplete six-output-clock candidate do not establish the complete adopted engine contract. Candidate annexes support implementation review but cannot silently replace adopted definitions. Bell results recorded with the former shared resource (section 3.18, deleted) are historical and are not evidence for the current model, and PASS/RETURN values carried on returning rays do not by themselves establish entanglement or spacelike Bell correlations. This documentation review adds no simulator execution or new passing result.

# 7. Working method

Only developers write or modify runtime code and tests. The architect coordinates interfaces; physics and mathematics own meanings and operators; experimental review fixes independent expectations; documentation maintains definitions and evidence status. These roles do not imply continuously running agents.

# 8. Documentation integrity check

The central specification owns adopted model decisions, the defined Detector and Node/Link acceptance, with open items identified explicitly. This document summarizes that owner rather than maintaining competing detailed laws. Review ordinary locality without exception, Detector-only sampling at marked Nodes, six-output timing and exact ownership. Distinguish unresolved numerical choices, engineering gaps and unproved emergence from already adopted principles. A candidate, unsupported profile or historical result must never silently override an adopted definition.

# 9. Assistant working instruction

Do not suggest a next step or follow-up action unless Alon explicitly asks for it.
