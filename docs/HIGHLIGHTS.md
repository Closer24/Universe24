# Universe24 Highlights (repository snapshot)

This file is a verbatim snapshot of the Google Doc
[Universe 24 Highlights](https://docs.google.com/document/d/1IkhSyqZZMBSgbJV-PMMwcXG0D_Rlfg4FrLy2jXBMUSs/edit),
taken on 2026-09-16 from the document revision modified at 11:45 UTC that day.
The live document remains the authoritative summary and may change after this
snapshot; the central model specification named in section 1 owns model
definitions, and [Highlights coverage](HIGHLIGHTS_IMPLEMENTATION.md) records
what the repository implements. Section numbering and wording below are the
document's own.

---

# Universe24 Highlights

*Sole author: Alon Gonen*

# 1. Purpose and navigation

This document merges the Highlights material into one English-only summary. It is a summary of the central model specification, not a parallel source of physical laws. Full definitions and adopted model decisions belong in the central model specification. An explicit user decision overrides older text; an approved decision must not be changed, and a missing physical law must not be invented while documenting the project.

Central model specification: Universe24 — Unified Node Theory: a unifying schema for rays, fields and interactions.

# 2. Intuitive picture: multidimensional Snake

Think of Universe24 as a kind of multidimensional Snake game with obstacles and interactions. Multiple rays move through the same 3D Node network across compatible property and field channels. They may cross without responding, respond weakly, or interact very strongly according to their selected coupling; crossing or co-location alone is not a collision. Here, weak and strong describe response strength, not automatically the fundamental weak and strong forces. Multidimensional includes independent state channels, not extra spatial dimensions. Obstacles are an analogy for declared interactions, not invented opaque walls or a capacity fix. Ordinary evolution is deterministic; only an actual Detector generates a draw. The central specification remains the precise definition.

# 3. Foundational postulates

## 3.1 Discrete local space

Reality is represented by a connected discrete space. The elementary spatial unit is a local Node connected only to neighboring Nodes.

## 3.2 Only local information exists physically

A Node can act only on its own state and on information that has physically arrived through its links. No physical influence can jump directly to a distant Node.

## 3.3 Ray-form propagation is fundamental

The board contains Node states and their properties, not a separate fundamental object called a ray. A ray names the universal form in which those properties and coherent alternatives propagate through neighboring Nodes. Interactions act on the local degrees of freedom that meet. There is no additional substance called matter; references to rays below refer to this propagation and its interaction patterns.

## 3.4 Matter is emergent

Particles, mass and the ordinary appearance of solid matter are stable interaction patterns of rays. They are not fundamental ingredients added to the model.

## 3.5 Fields are emergent descriptions

A field is a local description of ray state, flux or interaction structure. It is not an additional material substance independent of the underlying rays.

## 3.6 One underlying physics

Classical, quantum and field behavior must arise from the same underlying local system. The model must not introduce separate fundamental classical and quantum worlds.

## 3.7 Universal local laws

Equivalent local states with equivalent received inputs obey the same local rules, independent of position, total universe size or the labels assigned to an entity.

## 3.8 Causality has a finite speed

Physical influence propagates through adjacent links at a finite causal speed c. A new physical event cannot instantaneously modify distant physical state.

## 3.9 Fundamental propagation is local and stepwise

A physical ray advances only through connected neighboring Nodes. No physical trajectory may skip intermediate space.

## 3.10 Time is physical ordering

Physical time is the ordered progression of local events and propagation. Computation or interaction that requires additional physical steps requires additional model time; bookkeeping outside the physical world does not.

## 3.11 Discrete physical state

All physical state is discrete. The physical core uses integer-representable state and exact discrete operations rather than continuous floating-point physical variables.

## 3.12 Local bounded processing

Each elementary physical update uses bounded local state, bounded local inputs and bounded local work. No local rule may depend on world size or an unbounded search through distant state.

## 3.13 Interactions create observable properties

Properties attributed to a particle are inferred from how the underlying ray pattern interacts. A name such as electron, proton or mass does not itself supply a physical law or a hidden value.

## 3.14 No self-created force

An isolated closed physical structure cannot create net momentum from its own internal interactions. Local recoil is allowed only when an opposite momentum transfer is carried by rays or another explicitly owned local degree of freedom, so the total isolated system remains balanced.

## 3.15 Conservation is local accounting

Whenever a quantity is declared conserved, every local interaction and transfer must account for it exactly. A gain by one physical owner requires the corresponding loss or transfer from another owner or a declared source.

## 3.16 Momentum is directional

Momentum and other vector quantities are conserved component by component. Preserving only speed or vector magnitude is not sufficient.

## 3.17 Remainders are physical bookkeeping

Discrete division or allocation must not silently destroy information or conserved quantity. Any indivisible remainder remains explicitly owned until a later local operation resolves it.

## 3.18 No hidden nonlocal physics

Global summaries, diagnostics, quantum dependency graphs and Focus-style computational shortcuts may organize calculation, but they cannot provide a physical Node with instantaneous access to remote physical state.

## 3.19 Measurement is an interaction

A physical measurement is itself a local interaction. It does not merely read a globally available hidden value; the observable result must arise from the state and interaction that reached the measuring system.

## 3.20 Quantum alternatives remain physical possibilities until an event resolves them

The ray-based state may encode multiple coherent alternatives before a recorded event resolves an observable outcome. These alternatives are not a separate physical substance or nonlocal matter layer. A recorded outcome does not rewrite the past, and later calculation must remain consistent with already recorded events.

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

In this model, computation-field state is a property of Nodes, like other represented field properties, not an external scheduler instruction or an additional material substance. It propagates in ray form through the same neighboring Links. Once it arrives and interacts locally, it can change the receiving Node's own modeled computation or interaction duration.

```text
tau_v = Delay(computation_state_v, local_state_v, arrived_inputs_v)
```

Delay is a shared bounded-integer local rule whose precise formula, timing of application and effect on an ongoing operation must be defined. Symmetry-equivalent inputs must produce equivalent timing. This physical duration is distinct from host CPU work; it cannot read a global load estimate, bypass causal transit or rewrite past events. The field's transport, interaction and any declared conserved inventory use the same generic accounting as other properties.

## 3.29 Observation is a frame-dependent representation of board reality

What an observer sees is a representation of the same underlying Node states and events, determined by the observer's reference frame, orientation, motion and measurement interaction. Observable records arise only from information that has causally reached the measuring system, not from an instantaneous view of the whole board.

```text
observed_description = Transform_frame(Readout(local_measurement_records))
```

Changing coordinates or basis changes the description of an event; performing a physical measurement is an interaction that can change the state and record an outcome. These are distinct operations. Equivalent descriptions must preserve the model's declared invariants and consistent records, while different measurement interactions can reveal different properties. The observer, detector and their timing are themselves represented on the same board; a host visualization is not an extra physical observer.

## 3.30 One property engine, from abstract structure to detector experience

The purpose of Universe24 is to turn abstract mathematical descriptions of groups, representations, particle families and their properties into explicit board dynamics and, through a modeled detector, observable experience. Abstract does not mean imaginary. The engine uses one generic state schema and operation framework: fields, electrons, muons and gluons are distinguished by property content, representations and permitted interactions, not by separate fundamental engines. A ray is the propagation form of these properties, not an additional entity class. Uniform representation must retain physical differences, including charges, spin, statistics and couplings.

```text
property definitions + symmetry representations → Node state → propagation and interaction → detector records → observer-dependent display
```

At each Node, the shared engine reads resident properties and arrived inputs, applies the permitted transformations and interactions, accounts for declared conserved quantities, records an outcome only when the interaction requires one, advances modeled local time and transfers outgoing properties through Links. A detector, including a modeled eye, participates through the same property-and-interaction schema. The display is derived from its records; visualization alone does not establish that the chosen dynamics reproduce nature.

# 4. Central statement

Universe24 starts from local discrete Node states whose propagation takes ray form. There is no fundamental matter layer, mass substance or separate ray substance. What we call matter, particles and mass are emergent stable patterns of local state and interactions. Known symmetry structures constrain the generic property representations and operations; every proposed mechanism must end in an explicit account of Node state, local events, Link transfers and modeled time. The purpose is to test what behavior follows without inserting the desired macroscopic laws.

# 5. Reading map

## 5.1 Node state and ray form

NodeState, ownership, neighborhood, postulates and property representation. Work happens at the Node; this summary does not define a separate 36-register layer.

## 5.2 Generic operations at a Node

Arrived input, local encounter, proposal and atomic commit. A separate operations package is a code-separation choice, not an additional physical place; the engine schedules, and the state itself does not contain formulas.

## 5.3 Couplings, fields and timing

Propagation, emission funding, remainders, transit time and waiting. The representations of mass, phase and computation time remain distinct concepts.

## 5.4 Quantum action and Detector

The state transformation is defined, but only an actual external Detector encounter may generate a draw. Ordinary propagation and interactions remain deterministic; a new event alone grants no sampling authority. Replaying the same committed Detector event never redraws or emits again. Pair profiles, general shared state and external PASS/RETURN exchange have distinct integration boundaries.

## 5.5 Acceptance tests and open decisions

Every operation has an input, expected result and failure condition; tests apply to Nodes and Links. The distinction between an adopted law, a mathematical candidate, a missing implementation connection and a measured result must be preserved.

# 6. History, implementation and evidence

The Evidence and references tab in the central specification collects code anchors and previous results. Event history and wave-source history are preserved; this is not permission for a Node to read remote history. The contract for locating or stopping a local cancellation message is a separate gap from the requirement to preserve history.

Git documents describe software interfaces, profiles and defined experiments. The candidate operations appendix proposes implementation examples and tests; it does not replace the central definitions and does not prove that the laws of physics have already been derived.

# 7. Working method

Only developers write or modify runtime code and tests. The architect coordinates interfaces; physics and mathematics own meanings and operators; experimental review fixes independent expectations; documentation maintains definitions and evidence status. These roles do not imply continuously running agents.

# 8. Documentation integrity check

The central specification must contain all adopted model decisions, the defined quantum action, and Node/Link acceptance with explicit open items. This summary must point to that owner rather than repeat full laws. A candidate, unsupported profile or historical result must never silently override an adopted definition.

# 9. Assistant working instruction

Do not suggest a next step or follow-up action unless Alon explicitly asks for it.
