# Ray-event model: one generic definition for everything on the board

## Status and authority

This is a design candidate, model identity `ray-event-model-v1`. It records
Alon Gonen's decisions of 16 and 17 September 2026 in the coordinator's words,
for review before any implementation. It is not implemented, not a measured
result and not a claim about nature. Where it contradicts an existing
implementation contract, the contradiction is listed in the migration section;
nothing here changes runtime behavior until an implementation is published
against this document under the [published-design rule](../skills/workflow.md#implement-from-a-published-design).

Authority: the [Highlights specification](HIGHLIGHTS.md) is the Highlights
text, edited directly since 2026-09-17 by the model owner's decision; the
Google Doc named in the [README](../README.md#project-specification-google-docs)
is its historical source up to the revision of 2026-09-16 and is neither
edited nor resynced. Highlights sections 3.3, 3.4, 3.5, 3.15, 3.19, 3.20, 5.1
and 5.4 record the decisions this document restates in the coordinator's words;
where the two differ, Highlights is the text to follow and this document is
corrected. The [Detector-only sampling contract](DETECTOR_SAMPLING.md)
(`detector-only-v1`) is preserved and made concrete here.

## 1. Definitions

The system has exactly two definitions, **event** and **ray**: a ray carries
information, an event is where that information splits, and a ray is what
was split off from an event. An interaction, the meeting of rays at a Node,
is where events are made; everything else is defined from these.

**Interaction.** An interaction is a meeting of rays at a Node in one
interval, decided by the coupling declared between the families present.
It is the only place where anything is decided. Its result is a set of
events leaving the Node: at most six, one per Port, because a Node has six
Ports. Fewer when some Ports stay empty; one when a ray continues or
reverses; none when the rays stay bound at the Node.

**Event.** An event is a change of trajectory: a new straight line that
starts at an interaction and leaves it through one Port. An event is where
information splits: what the arriving rays carried leaves as the shares of
the rays that depart. There is no event
without an interaction and no interaction without at least the possibility of
a changed trajectory. A Node that a ray merely crosses hosts no event.

**Ray.** A ray is not an object. It is the trajectory of one event between
two interactions: the same event, the same family properties, one Node per
Link interval, one heading, a straight line. A ray carries information: it is
what was split off from an event, its own share of what happened there, and
all the information is on the rays. From its event, every ray carries the
number of steps it has made. Every ray carries the information of the last
event it was involved in; if that event was at a Detector, the ray records
that it was a Detector event and the bit drawn, 1 or 0, and the bit is all
the Detector adds. Between two interactions nothing new happens
to it. A ray trajectory is therefore reversible: run backward step
by step it returns exactly to the interaction that created it, because no
information was added or lost along the line.

**Alternatives.** Outside a Detector, every trajectory that an interaction
permits actually happens: the up-to-six events leaving the interaction all
propagate, each as a straight ray, each carrying its share of the conserved
quantities and its phase. Alternatives are created only at
interactions, never at the empty Nodes a ray crosses. A wave ray between two
interactions is one line; at an interaction it becomes up to six lines.

**Wave ray.** Every ray is a wave ray and carries a phase that advances along
the line, together with its quantities (energy, momentum, charge, family
properties); a plain ray is a special case of the wave ray, not a second kind.
Light is a wave ray with no mass and no charge: it is an event moving in time,
exactly as defined above, not a separate photon object.

**Detector.** Every Node carries one bit: Detector or not. The mark is
bounded Node metadata (the bit, a setting, a ticket seed), not a record, not
an object and not an external device; "Detector behavior" is simply how a
Node behaves when the bit is set. A marked Node does one very simple thing.
What arrives at it is a wave ray carrying information; every ray is a wave
ray, so the kind of ray makes no difference to the Detector. For each
transfer that arrives,
whatever it is, it draws 1 or 0 from the mark's ticket sequence, and this
is the only place a lottery exists (`detector-only-v1`). On 1 the Node
behaves as an ordinary Node for that arrival: the transfer continues on its
line, or enters the declared interaction, as if no Detector were there. On 0
the Node behaves as a Detector for that arrival: it returns that wave ray on
the same line in the opposite direction, unchanged, back the same number of
steps it has made since its event, so that it arrives at the Node it left
from with exactly the information it left with. Up to six
transfers can arrive in the same interval, one through each Port, and the
Node draws once for each arrival, independently: the arrivals that drew 1
enter the ordinary interaction together, exactly as at an unmarked Node, and
each arrival that drew 0 is returned on its own line. The Detector does not read,
change, absorb or add anything; it needs to know nothing about what passed.
It is the same ray in both outcomes: not absorbed, not split, no stock taken.
The click is the record of the bit drawn, and the bit is all the Detector
adds: a ray leaving a marked Node records that its last event was a Detector
event and the bit drawn, nothing larger. Because a marked Node is a Node
like any other, everything else about it (rays crossing, interactions of
other families, fields) is unchanged.

**Return.** A returning ray retraces its own trajectory: it reverses its
heading and walks back exactly the number of steps it has made since its
event, unchanged. An event cannot be moved; there is no such thing. It
happened at its Node, and on a fixed lattice the returning ray reaches that
Node with certainty. The return is the ray itself, not a message and not a
separate carrier; it carries what the ray already carries (family properties,
phase, its step count, its share of what happened at the event, and the bit
of its Detector event, nothing larger). At the event Node it performs the
inverse split with its information: it transmits it, with its bit, to the
same places the event sent to, so that it cancels what was already there.
This turns time back for that ray's share only; the other shares are
untouched until their own rays return. For a pair, the partner ray's line is
among those places, so the partner's Detector is not missing the bit: that
is the same inverse split, not a second mechanism.

**Information.** Everything on the board is a transfer of information. An
event is a splitting of information: each ray carries its own share of what
happened at the event away from it, along its line. All the information is
on the rays; the origin Node keeps nothing, and there is no register of any
kind at the origin. A return is not a message: the returning ray brings its
share back to the event Node and performs the inverse split there, which
cancels what was already there. A ray that passes a Detector is realized.
Sibling events of one interaction are independent rays, each meeting its own
fate; the other shares are untouched until their own rays return, and
nothing cancels a sibling's share except its own return.

**Splitting and the inverse split.** An event is a splitting of information:
the interaction splits what arrived into the rays that leave, at most six,
and each ray carries its own share of what happened at the event. Because
nothing is added or lost on a line, a returning ray brings its share back
exactly: at the event Node it performs the inverse split with its
information, transmitting it to the same places the event sent to, so that
it cancels what was already there. This turns time back for that ray's share
only. A Detector that returns a ray is telling the event which share it
gives back; the share is the whole ray, since the Detector's outcome is
binary per ray.

**Conservation as reconstructability.** The conservation laws are the
condition of reconstruction. Energy, momentum component by component,
charge and every other declared invariant are exact across an interaction so
that the event can be rebuilt from its pieces when they return: the pieces
are the information, and the conserved totals are the check that nothing was
added or lost when they split and when a share is returned by the inverse
split. Sums alone do not identify an input, so what makes the undoing exact
is that each share is preserved on its line, and the invariants verify the
whole. A Detector that returns a ray is returning an event in time: the
share walks its line backward and the event is undone by exactly what that
share carried, and only that. The lattice's exact integer arithmetic is what
makes the undoing exact rather than approximate.

**Field.** A ray has a field: a ray that travels releases a field, and the
field is itself made of rays, family-declared outward emission along the six
headings, one Link per interval, with the ordinary dilution or declared
attenuation of an outward field. Every ray is the same ray; a field ray is
not a second kind. The field's presence at a Node is an interaction that
makes no event: a field never makes an event unless it meets something it
changes. Where a field ray meets a ray whose declared coupling responds, the
meeting is an ordinary interaction and its events change that ray's
trajectory; everywhere else the field crosses without an event. One of those
events is the field ray itself returning reversed: the return is the opposite
momentum of the field, carried back along the field ray's line to the ray
that released it, which recoils when the return arrives, at finite speed.
This is how Highlights 3.14 is satisfied: the recoil is a ray. Until its
field meets something, a traveling ray pays nothing for it.

**Matter.** There is no matter in the model at this stage. Matter is the name
for rays bound in one Node: for example a neutron ray and a proton ray held
together in one cell by a declared strong binding coupling, and an electron
ray around them whose trajectory is changed at every step by the field rays
the bound pair emits. A bound group has no lifetime of its own: it lasts as
long as the binding interaction repeats at that Node without releasing an
event. The binding may be nothing more than a very large output-clock delay
(Highlights 3.28) that the bound rays create together, a large mass making
the Node very slow, so that the rays do not leave. It is unbound the same way
anything else happens on the board: a ray arrives (a high-energy light ray,
for instance; there is no photon, only a ray) and the coupling declared for
the families present produces events that leave. Nothing else creates or
destroys matter. Everything is the same generic ray with the same generic
interaction, and everything follows from the generic transactions of the
declared couplings; what remains is to close the binding couplings. Until
they exist, held source records remain an explicitly labeled interim device.

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
- **a Detector interaction**: only at a Node whose Detector bit is set, for
  each transfer arriving through a Port this interval, independently, up to
  six at once: 1 or 0 is drawn from the mark's own ticket
  sequence; 1 means that arrival enters the two cases above together with
  the other arrivals that drew 1, 0 means the Node returns that arrival on
  its own line in the opposite direction.

Nothing else decides anything. A ray alone at a Node never interacts. A Node
never holds a ray without a declared binding coupling. Binding is the
interaction whose result is zero events: the rays stay at the Node and
interact again every interval, their phase advancing once per interval. A
bound group has no lifetime of its own: it lasts as long as that interaction
repeats without releasing an event, and it is unbound when a ray arrives and
the coupling declared for the families present produces events that leave.
The
[bound-ray-pair candidate](HYPOTHESES.md#candidate-rule-bound-ray-pair-v1-a-candidate-not-implemented)
is the special case of a binding coupling between two counter-heading rays of
one family.

The rule in the form Highlights 3.27 requires:

| Question | Answer under this model |
| --- | --- |
| Where is state stored | On the ray: family properties, phase (every ray is a wave ray), heading, the number of steps it has made since its event, the information of its last event (its share of what happened there) and, if that was a Detector event, its bit; all the information is on the rays. On the Node: the rays resident this interval, the bounded bound group if any, and the Detector mark if the Node carries one (mark, setting, ticket seed). The origin Node of an event keeps nothing; there is no register of any kind |
| What arrived | The rays delivered through the six Ports this interval; a resident bound group counts as arrived every interval |
| What operation acts | The coupling declared for the set of families present, in declared order; at a Node whose Detector bit is set, first one 1-or-0 draw for each transfer that arrived this interval, independently, the kind of ray making no difference since every ray is a wave ray; the arrivals that drew 1 then enter the declared coupling as at an unmarked Node, and each arrival that drew 0 is returned on its own line; a returning ray that has walked back its step count performs the inverse split of its share at its event Node, transmitting it, with its bit, to the same places the event sent to |
| Is an outcome recorded | Only at an interaction: the events that leave it, and at a Detector the click; crossing records nothing |
| How long it takes | One interval per Link as today; an interaction takes its declared wait; a bound group advances its phase once per interval it is held |
| What crosses each Link | Rays only, at most one new event per Port per interaction. A returning ray is an ordinary ray with a reversed heading and a decreasing step count, and what its inverse split transmits travels the lines the event sent to, one Link per interval. No message, no registry answer, nothing that skips a Node |

## 3. Pairs, the carried bit and the price

A bonded pair is one birth interaction and two rays with opposite headings.
Each ray reaches its own Detector and is drawn there. A ray that returns
walks back exactly its step count to the birth interaction and there performs
the inverse split of its share: it transmits what happened at the event, with
its bit (the outcome of the first draw, all the Detector added), to the same
places the event sent to, the partner ray's line among them, so the partner's
Detector is not missing it. If that transmission reaches the second Detector
before the second ray is drawn, the second draw reads it and the pair agrees
by the configured joint law; if the second ray was already drawn, the
transmission is recorded and ignored.

This replaces the shared registry of the historical bonded profile with a
carried bit, so the model has no owner that answers at a distance. The
price is accepted explicitly: two Detectors at equal distance from the birth
draw independently, and the CHSH value for spacelike settings is at most 2.
The quantum value appears only when the second ray's path is longer than the
round trip through the first Detector. Pair identity becomes the trajectory,
so two pairs born at one Node in one tick are distinct, which closes the
[birth-code collision](../examples/research/bell-postulate-22/README.md) found
on 16 September 2026.

## 4. Why this is consistent

- One kind of entity (an event trajectory with family properties, a phase
  and its step count), one kind of interaction (a meeting at a Node, declared per
  family set, exactly conserved, at most six events out), one door for
  randomness (the Detector draw, one per transfer arriving at a marked Node). Postulates 1 to 4 hold
  without exception; the registry exception of postulate 4 is withdrawn and
  Highlights section 3.18, which described the shared resource, is deleted
  (2026-09-17).
- Fields as rays satisfies Highlights 3.5 and 3.28 directly: a field is a
  local description of ray state, a field ray is not a second kind, its
  presence at a Node makes no event unless it meets something it changes, and
  the computation field is a propagating property. Highlights 3.14 is
  satisfied by a ray: when a field ray changes another ray's trajectory it
  returns reversed along its own line, and the ray that released it recoils
  by the opposite momentum when the return arrives, at finite speed; until
  its field meets something, a traveling ray pays nothing for it.
- Matter as bound rays satisfies Highlights 3.4: mass is the retained energy of
  a bound group, not a stored property; the group's phase advance is its own
  clock, which the [light-clock measurement](../examples/research/anomalies/README.md)
  says slows with the hop time. A bound group has no lifetime of its own and
  is unbound only when an arriving ray's declared coupling produces events
  that leave; nothing else creates or destroys matter.
- The stranded-stock defect of the two-phase hold in the radiation-scattering
  candidate cannot occur: no Node owns intermediate stock; an interaction is
  one transaction at the Node where the rays actually are.
- Reversibility is testable: replaying any ray backward between two
  interactions must reproduce its forward trajectory exactly, and returning
  any ray to its event Node must cancel exactly that ray's share by the
  inverse split, with every declared invariant equal before the split and
  after the return and the other shares untouched.
- The six-event bound is the causal bound of the lattice, the same bound the
  N-to-M contract already enforces; no interaction can create more
  alternatives than the Node has Ports.

## 5. What the current engine does differently

| Today | Under this model |
| --- | --- |
| Every interaction passes through a resident record (mirror, screen, detector, lamp) with stock and absorption | An interaction is a property of the meeting of rays; a Detector is a mark on a Node, not a record with stock |
| The shared quantum resource (Q-ORACLE-1, bond registry) is an accepted exception to locality | Deleted by the model owner on 2026-09-17 (Highlights section 3.18): no owner answers at a distance; the marked-Node lottery and the returning ray are the whole quantum mechanism |
| The photon is a record of a family; conversion products are records | Every ray is a wave ray with a phase; light is a wave ray with no mass and no charge; conversion products are events leaving the interaction |
| A bonded pair is answered by a global registry keyed by (Node, tick) | The first draw's outcome travels back and forward on the ray itself; pair identity is the trajectory |
| Records emit fields; rays do not | A traveling ray of an emitting family releases field rays along its line; a field ray is not a second kind, and its return reversed is the emitter's recoil |
| A record can hold, wait at zero cost and be updated in place | Nothing holds except a bound group under a declared binding coupling |
| An event is any local change at a Node | An event is a change of trajectory leaving an interaction; crossing a Node is not an event |
| Alternatives live in a separate quantum owner (deferred graph, event network) | Alternatives are the up-to-six events of each interaction, all on the board |

## 6. Migration, in order

1. This document, reviewed by the model owner; its decisions recorded in
   [Highlights](HIGHLIGHTS.md) (done on 2026-09-17: sections 3.3, 3.4, 3.5,
   3.15, 3.19, 3.20, 5.1 and 5.4, with 3.18 deleted) and reflected in the
   [postulates](../POSTULATES.md) 1, 4, 22, 23 and 24 (done on 2026-09-17),
   in [TERMINOLOGY.md](TERMINOLOGY.md) (Event, Ray, Interaction, Detector)
   and in [SPATIAL_FIELDS.md](SPATIAL_FIELDS.md) (the bonded profile becomes
   historical).
2. Ray state: the number of steps made since its event, the information of
   its last event (its share of what happened there) and, for a Detector
   event, the bit drawn added to the ray; heading and phase exist, and the
   phase is carried by every ray, since every ray is a wave ray. No origin
   reference is stored: the count suffices on a straight line, and no Node
   keeps anything about the event.
3. Detector as a Node bit in the initialization (position, setting, ticket
   seed): each transfer through a marked Node draws 1 or 0 from the mark's
   ticket sequence, 1 ordinary behavior, 0 return on the same line reversed;
   click event recorded; no stock; no detector record type.
4. Return propagation: reversed heading, decreasing count; at the event Node
   the inverse split of the returning ray's share, transmitted with its bit
   to the same places the event sent to, the partner's line among them;
   meeting rule at the far Detector as in section 3. No event is moved and
   no Node keeps a register.
5. Registry removal from the physical path; the historical bonded profile and
   its tests are retained as history, not as the active law.
6. Light as a wave ray with no mass and no charge, every ray being a wave
   ray; conversion products emitted as events from the
   interaction; the N-to-M mechanism invoked at a meeting of rays without a
   resident record, up to six events out.
7. Field emission by traveling rays, with the outward dilution or declared
   attenuation of the existing field contracts; a field ray whose meeting
   changes another ray's trajectory returns reversed along its own line as
   the emitter's recoil, arriving at finite speed, and a traveling ray pays
   nothing for its field until the field meets something.
8. Binding couplings: the bound-ray-pair candidate generalized to a bound
   group of N rays of declared families in one Node (the strong binding),
   possibly nothing more than a very large output-clock delay the bound rays
   create together, unbound by an arriving ray's declared coupling; then
   the orbit: a ray whose trajectory is changed at every step by the field
   rays of a bound group.
9. Tests and experiments: reversibility replay; the light cone of the carried
   bit; CHSH with equal distances (expected at most 2) and with a delayed
   second ray (expected the singlet value); a light clock between two
   Detectors instead of two mirrors; the bound group under load.

Each step is a separate published change with its own model identity, tests
and evidence, under the ordinary gates.

## 7. Acceptance criteria for the first implementation slice

- A transfer through a marked Node draws 1 or 0; on 1 the Node's behavior is
  identical to the unmarked Node (same events, same totals); on 0 the
  returned ray reaches its birth Node after exactly the number of steps it
  had made since its event, on every seed, in every direction, with its
  information unchanged, and performs the inverse split of its share there;
  an unmarked Node never draws.
- Six transfers arriving at a marked Node in one interval receive six
  independent draws, whatever they carry, every ray being a wave ray; those
  that drew 1 interact exactly as at
  an unmarked Node, each that drew 0 is returned on its own line, and the
  totals of the two groups together equal the totals that arrived.
- One bit per transfer arriving at a marked Node, and the bit is all the
  Detector adds: a ray leaving it carries its share, that its last event was
  a Detector event and the bit, nothing larger; replay with the same seed
  reproduces every click; changing one Detector's bit changes the world only
  inside the forward light cone of that interaction.
- An interaction never emits more than six events and never two on one Port;
  every declared invariant is exact over all inputs and all events out.
- A pair with equal Detector distances gives CHSH at most 2 within counting
  error; a pair whose second ray is delayed by more than the round trip gives
  the configured joint law's value.
- Conservation audits balance at every tick; no Node holds stock after an
  interaction; every ray is resident, in flight or escaped, and nothing else.
- A returned ray cancels exactly its own share at its event Node by the
  inverse split, transmitted to the same places the event sent to; the other
  shares are untouched until their own rays return; every declared invariant
  is equal before the split and after the return; no Node keeps anything
  about the event.

## 8. Open decisions

None remain from the model owner's side as of 2026-09-17: every question this
section listed (the lifetime and register of an open alternative, moving an
event, reassembly and re-emission, what the returning ray carries, whether a
field ray alone changes a trajectory, the funding of the released field, the
lifetime of a bound group) is answered in Highlights 3.3, 3.4, 3.5, 3.20 and
5.4 and restated above.

One consequence is not stated in Highlights and is for the design owner to
record before migration step 4, not for this document to choose: how the
transmission of an inverse split meets the share it cancels when that share
is still in flight on its line (it left the event Node earlier, at the same
one Link per interval), and what it meets when that share was already
realized at a Detector. Highlights 3.20 states the cancellation, not the
meeting.
