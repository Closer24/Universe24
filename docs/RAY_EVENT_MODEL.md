# Ray-event model: one generic definition for everything on the board

## Status and authority

This is a design candidate, model identity `ray-event-model-v1`. It records
Alon Gonen's decisions of 16 and 17 September 2026 in the coordinator's words,
for review before any implementation. It is not implemented, not a measured
result and not a claim about nature. Where it contradicts an existing
implementation contract, the contradiction is listed in the migration section;
nothing here changes runtime behavior until an implementation is published
against this document under the [published-design rule](../skills/workflow.md#implement-from-a-published-design).

Authority: the central model specification (the Google Doc named in the
[README](../README.md#project-specification-google-docs)) owns model
definitions; this document is the candidate text proposed for its sections 1,
3 and 4. The [Detector-only sampling contract](DETECTOR_SAMPLING.md)
(`detector-only-v1`) is preserved and made concrete here. The
[Highlights snapshot](HIGHLIGHTS.md) sections 3.3 to 3.5, 3.19, 3.20 and 5.4
state the principles this model implements.

## 1. Definitions

Two words carry the whole model: **interaction** and **event**. Everything
else is defined from them.

**Interaction.** An interaction is a meeting of rays at a Node in one
interval, decided by the coupling declared between the families present.
It is the only place where anything is decided. Its result is a set of
events leaving the Node: at most six, one per Port, because a Node has six
Ports. Fewer when some Ports stay empty; one when a ray continues or
reverses; none when the rays stay bound at the Node.

**Event.** An event is a change of trajectory: a new straight line that
starts at an interaction and leaves it through one Port. There is no event
without an interaction and no interaction without at least the possibility of
a changed trajectory. A Node that a ray merely crosses hosts no event.

**Ray.** A ray is not an object. It is the trajectory of one event between
two interactions: the same event, the same family properties, one Node per
Link interval, one heading, a straight line. Between two interactions nothing
new happens to it. A ray trajectory is therefore reversible: run backward step
by step it returns exactly to the interaction that created it, because no
information was added or lost along the line.

**Alternatives.** Outside a Detector, every trajectory that an interaction
permits actually happens: the up-to-six events leaving the interaction all
propagate, each as a straight ray, each carrying its share of the conserved
quantities and, for a wave ray, its phase. Alternatives are created only at
interactions, never at the empty Nodes a ray crosses. A wave ray between two
interactions is one line; at an interaction it becomes up to six lines.

**Wave ray and non-wave ray.** A wave ray carries a phase that advances along
the line. A non-wave ray carries quantities only (energy, momentum, charge,
family properties). Light is a wave ray with no mass and no charge: it is an
event moving in time, exactly as defined above, not a separate photon object.

**Detector.** A Detector is a Node marked as a Detector. The mark is bounded
Node metadata (the mark itself, a setting, a ticket seed), not a record, not
an object and not an external device; "Detector behavior" is simply how a
Node behaves when it carries the mark. Any wave ray entering a marked Node
undergoes a simple binary lottery, and this is the only place a lottery exists
(`detector-only-v1`): the ray either continues on the same line in the same
heading, or reverses by a half turn and goes back along the same line. It is
the same ray in both outcomes: not absorbed, not split, no stock taken. The
click is the record that the ray passed or returned. A non-wave ray entering
a marked Node is not drawn; its outcome follows from its declared coupling.
Because a marked Node is a Node like any other, everything else about it
(rays crossing, interactions of other families, fields) is unchanged.

**Return.** A returning ray retraces its own trajectory: it reverses its
heading and walks back the number of steps it counted since its last
interaction. On a fixed lattice this reaches, with certainty, the interaction
that created it. The return is the ray itself, not a message and not a
separate carrier; it carries what the ray already carries (family properties,
phase, and the Detector's outcome in a bounded register). When it reaches its
birth interaction it continues straight through it, which is by construction
the direction of the partner ray of a pair.

**Information.** Everything on the board is a transfer of information. A ray
carries a piece of information away from the interaction that created it;
the node of that interaction keeps the complementary piece, what is missing
there, in a bounded register of open alternatives for as long as the
alternative is open. A return is a deletion, not a message: the returning ray
brings the piece back to the origin, which erases the open alternative. A ray
that passes a Detector is realized, and its open piece at the origin ends
with the bounded lifetime of the register or with a later return. Sibling
events of one interaction are independent rays, each meeting its own fate;
nothing erases a sibling except its own return.

**Splitting and reconstruction.** An event is a splitting of information:
the interaction splits the piece that arrived into the pieces that leave, at
most six, each a ray. Because nothing is added or lost on a line, the event's
information is recoverable: when its rays return to the same event the
pieces reassemble and the event is complete again, as if it had not split. A
Detector that returns a ray is telling the event which piece it gives back;
the piece is the whole ray, since the Detector's outcome is binary per ray.

**Conservation as reconstructability.** The conservation laws are the
condition of reconstruction. Energy, momentum component by component,
charge and every other declared invariant are exact across an interaction so
that the event can be rebuilt from its pieces: the pieces are the
information, and the conserved totals are the check that nothing was added
or lost when they split and when they reassemble. Sums alone do not identify
an input, so what makes reconstruction exact is that each piece is preserved
on its line, and the invariants verify the whole. A Detector that returns a
ray is returning an event in time: the piece walks its line backward and the
event is undone by exactly what that piece carried. The lattice's exact
integer arithmetic is what makes the undoing exact rather than approximate.

**Moving an event.** The event is its information, not a place. The open
piece kept at the origin may be displaced along the trajectory line of the
rays it is waiting for, and a returning ray, which walks that line, still
meets it. This is the occupied-channel displacement rule of the central
specification (section 5.1): a saved event is pushed along the same path
without capacity waiting. Its exact resolution (which neighbor, what happens
when two pushes meet, how the step count of a returning ray accounts for the
displacement) is a decision this document must record before step 4 of the
migration is implemented.

**Field.** A ray that travels releases a field, and the field is itself made
of rays: family-declared outward emission along the six headings, one Link
per interval, with its own conserved quantity and the ordinary dilution or
declared attenuation of an outward field. A field ray is a ray in every sense
above: it crosses Nodes without event, it meets other rays at Nodes, and a
meeting is an interaction decided by the declared coupling between the
families.

**Matter.** There is no matter in the model at this stage. Matter is the name
for rays bound in one Node: for example a neutron ray and a proton ray held
together in one cell by a declared strong binding coupling, and an electron
ray around them whose trajectory is changed at every step by the field rays
the bound pair emits. Everything is the same generic ray with the same generic
interaction; what remains is to close the binding couplings. Until they exist,
held source records remain an explicitly labeled interim device.

## 2. The single generic rule

At a Node where two or more rays are resident in the same interval, the
declared coupling between their families decides one of:

- **no interaction**: the rays cross and continue (no coupling declared, or
  the coupling's guard is false);
- **a deterministic interaction**: up to six events leave the Node, computed
  from the frozen inputs by the declared operation, with every declared
  invariant (energy, momentum component by component, charge, family counts)
  exact over all inputs and outputs, exactly as the
  [N-to-M conversion contract](LOCAL_CONVERSIONS.md#n-to-m-family-conversion)
  already does for records: up to six inputs, up to six outputs, one output
  departure per Port;
- **a Detector interaction**: only at a Node marked as a Detector and only
  for a wave ray: one bounded integer is drawn from the mark's own ticket
  sequence and selects pass or return.

Nothing else decides anything. A ray alone at a Node never interacts. A Node
never holds a ray without a declared binding coupling. Binding is the
interaction whose result is zero events: the rays stay at the Node and
interact again every interval, their phase advancing once per interval. The
[bound-ray-pair candidate](HYPOTHESES.md#candidate-rule-bound-ray-pair-v1-a-candidate-not-implemented)
is the special case of a binding coupling between two counter-heading rays of
one family.

The rule in the form Highlights 3.27 requires:

| Question | Answer under this model |
| --- | --- |
| Where is state stored | On the ray: family properties, phase, heading, step count since the last interaction, one bounded outcome register. On the Node: the rays resident this interval, the bounded bound group if any, the Detector mark if the Node carries one (mark, setting, ticket seed), and a bounded register of open alternatives for the interactions born there |
| What arrived | The rays delivered through the six Ports this interval; a resident bound group counts as arrived every interval |
| What operation acts | The coupling declared for the set of families present, in declared order; the Detector lottery only at a marked Node and only for a wave ray |
| Is an outcome recorded | Only at an interaction: the events that leave it, and at a Detector the click; crossing records nothing |
| How long it takes | One interval per Link as today; an interaction takes its declared wait; a bound group advances its phase once per interval it is held |
| What crosses each Link | Rays only, at most one new event per Port per interaction. A returning ray is an ordinary ray with a reversed heading and a decreasing step count. No message, no registry answer, nothing that skips a Node |

## 3. Pairs, the carried number and the price

A bonded pair is one birth interaction and two rays with opposite headings.
Each ray reaches its own Detector and is drawn there. A ray that returns
walks back to the birth interaction and continues to the other side, carrying
the number that the other Detector "was missing": the outcome of the first
draw. If it reaches the second Detector before the second ray is drawn, the
second draw reads it and the pair agrees by the configured joint law; if the
second ray was already drawn, the returning ray is recorded and ignored.

This replaces the shared registry of the historical bonded profile with a
carried number, so the model has no owner that answers at a distance. The
price is accepted explicitly: two Detectors at equal distance from the birth
draw independently, and the CHSH value for spacelike settings is at most 2.
The quantum value appears only when the second ray's path is longer than the
round trip through the first Detector. Pair identity becomes the trajectory,
so two pairs born at one Node in one tick are distinct, which closes the
[birth-code collision](../examples/research/bell-postulate-22/README.md) found
on 16 September 2026.

## 4. Why this is consistent

- One kind of entity (an event trajectory with family properties and an
  optional phase), one kind of interaction (a meeting at a Node, declared per
  family set, exactly conserved, at most six events out), one door for
  randomness (the Detector interaction of a wave ray). Postulates 1 to 4 hold
  without exception; the registry exception of postulate 4 is withdrawn.
- Fields as rays satisfies Highlights 3.5 and 3.28 directly: a field is a
  local description of ray state, and the computation field is a propagating
  property.
- Matter as bound rays satisfies Highlights 3.4: mass is the retained energy of
  a bound group, not a stored property; the group's phase advance is its own
  clock, which the [light-clock measurement](../examples/research/anomalies/README.md)
  says slows with the hop time.
- The stranded-stock defect of the two-phase hold in the radiation-scattering
  candidate cannot occur: no Node owns intermediate stock; an interaction is
  one transaction at the Node where the rays actually are.
- Reversibility is testable: replaying any ray backward between two
  interactions must reproduce its forward trajectory exactly, and returning
  every piece of an interaction to its origin must reassemble the input
  piece exactly, with every declared invariant equal before the split and
  after the reassembly.
- The six-event bound is the causal bound of the lattice, the same bound the
  N-to-M contract already enforces; no interaction can create more
  alternatives than the Node has Ports.

## 5. What the current engine does differently

| Today | Under this model |
| --- | --- |
| Every interaction passes through a resident record (mirror, screen, detector, lamp) with stock and absorption | An interaction is a property of the meeting of rays; a Detector is a mark on a Node, not a record with stock |
| The shared quantum resource (Q-ORACLE-1, bond registry) is an accepted exception to locality | Withdrawn by the model owner on 2026-09-17: no owner answers at a distance; the marked-Node lottery and the returning ray are the whole quantum mechanism |
| The photon is a record of a family; conversion products are records | Light is a wave ray with no mass and no charge; conversion products are events leaving the interaction |
| A bonded pair is answered by a global registry keyed by (Node, tick) | The first draw's outcome travels back and forward on the ray itself; pair identity is the trajectory |
| Records emit fields; rays do not | A traveling ray of an emitting family releases field rays along its line |
| A record can hold, wait at zero cost and be updated in place | Nothing holds except a bound group under a declared binding coupling |
| An event is any local change at a Node | An event is a change of trajectory leaving an interaction; crossing a Node is not an event |
| Alternatives live in a separate quantum owner (deferred graph, event network) | Alternatives are the up-to-six events of each interaction, all on the board |

## 6. Migration, in order

1. This document, reviewed by the model owner; then its text proposed to the
   central specification sections 1, 3 and 4 and reflected in
   [TERMINOLOGY.md](TERMINOLOGY.md) (Event, Ray, Interaction, Detector), in
   the [postulates](../POSTULATES.md) 1, 4, 22 and 23, and in
   [SPATIAL_FIELDS.md](SPATIAL_FIELDS.md) (the bonded profile becomes
   historical).
2. Ray state: step count since the last interaction and one bounded outcome
   register added to the ray; heading and phase exist. No origin reference is
   stored: the count suffices on a straight line.
3. Detector as a Node mark in the initialization (position, setting, ticket
   seed): any wave ray entering the marked Node passes or returns, drawn from
   the mark's ticket sequence; click event recorded; no stock; no detector
   record type. Non-wave rays are not drawn.
4. Return propagation: reversed heading, decreasing count, straight through
   the birth interaction; meeting rule at the far Detector as in section 3.
5. Registry removal from the physical path; the historical bonded profile and
   its tests are retained as history, not as the active law.
6. Light as a wave ray family; conversion products emitted as events from the
   interaction; the N-to-M mechanism invoked at a meeting of rays without a
   resident record, up to six events out.
7. Field emission by traveling rays, with the outward dilution or declared
   attenuation of the existing field contracts and an explicit funding rule
   (a field released by a traveling ray carries its own conserved signal and
   no energy of the emitter unless a radiation coupling says so).
8. Binding couplings: the bound-ray-pair candidate generalized to a bound
   group of N rays of declared families in one Node (the strong binding), then
   the orbit: a ray whose trajectory is changed at every step by the field
   rays of a bound group.
9. Tests and experiments: reversibility replay; the light cone of the carried
   number; CHSH with equal distances (expected at most 2) and with a delayed
   second ray (expected the singlet value); a light clock between two
   Detectors instead of two mirrors; the bound group under load.

Each step is a separate published change with its own model identity, tests
and evidence, under the ordinary gates.

## 7. Acceptance criteria for the first implementation slice

- A wave ray meeting a Detector passes or returns; the returned ray reaches
  its birth Node after exactly the counted number of steps, on every seed, in
  every direction, and continues straight; a non-wave ray is never drawn.
- One number per Detector interaction; replay with the same seed reproduces
  every click; changing one Detector's number changes the world only inside
  the forward light cone of that interaction.
- An interaction never emits more than six events and never two on one Port;
  every declared invariant is exact over all inputs and all events out.
- A pair with equal Detector distances gives CHSH at most 2 within counting
  error; a pair whose second ray is delayed by more than the round trip gives
  the configured joint law's value.
- Conservation audits balance at every tick; no Node holds stock after an
  interaction; every ray is resident, in flight or escaped, and nothing else.
- A returned ray erases exactly one open alternative at its origin, the one
  it was; a register of open alternatives never grows beyond its bound, and a
  return to an origin whose alternative has already ended is recorded and
  ignored.

## 8. Open decisions

- Decided on 2026-09-17 (postulate 24): a return erases the open alternative
  at the origin; sibling alternatives are independent and a second Detector
  may realize one before a return from the first arrives. Remaining choice:
  the bounded lifetime of an open alternative at the origin, and what the
  origin does when the register is full.
- Moving an event: the displacement of the open piece along the trajectory
  line (which neighbor, meeting pushes, the returning ray's step count) is to
  be resolved here before step 4 is implemented.
- Whether the reassembly of all returned pieces at an event restores it as an
  interaction that can split again (re-emission), or only closes it.
- What exactly the returning ray carries: its own outcome only, or the full
  drawn number.
- Whether a field ray alone can change a ray's trajectory (a lens,
  refraction) without another ray present; under this model a field ray is a
  ray, so the meeting rule covers it, but the coupling law is not chosen.
- The funding of the field a traveling ray releases: signal without energy
  (the present outward field) or a radiation coupling paid by the ray.
- The lifetime of a bound group and what unbinds it.
