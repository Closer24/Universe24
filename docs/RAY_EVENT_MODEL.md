# Ray-event model: one generic definition for everything on the board

## Status and authority

This is a design candidate, model identity `ray-event-model-v1`. It records
Alon Gonen's decisions of 16 and 17 September 2026 in the coordinator's words,
for review before any implementation. Its migration is in progress (section 6
records which steps are done); it is not a measured result and not a claim
about nature. Where it contradicts an existing
implementation contract, the contradiction is listed in the migration section;
nothing here changes runtime behavior until an implementation is published
against this document under the [published-design rule](../skills/workflow.md#implement-from-a-published-design).

Authority: the [Highlights specification](HIGHLIGHTS.md) is the Highlights
text, edited directly since 2026-09-17 by the model owner's decision; the
Google Doc named in the [README](../README.md#project-specification-google-docs)
is its historical source up to the revision of 2026-09-16 and is neither
edited nor resynced. Highlights sections 3.3, 3.4, 3.5, 3.15, 3.19, 3.20, 3.26,
5.1, 5.3 and 5.4 record the decisions this document restates in the
coordinator's words;
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
Event spacetime has layers: a layer is a set of families that couple, and a
meeting exists only inside a layer. Rays whose families have no declared
coupling never meet; they cross as if the other were not there, so two
events can happen at the same Node in the same interval in layers that do
not communicate. An interaction is the only place where anything is decided. Its result is a set of
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
the Detector adds. The information of the last event and the Detector's bit stay on the ray as
hidden variables: no Detector and no ordinary coupling reads them today, they
come from no ordinary physics, and for now they affect no one; nothing on the
board feels them. Between two interactions nothing new happens
to it. A ray trajectory is therefore reversible: run backward step
by step it returns exactly to the interaction that created it, because no
information was added or lost along the line.

**Alternatives.** Outside a Detector, every trajectory that an interaction
permits actually happens: the up-to-six events leaving the interaction all
propagate, each as a straight ray, each carrying its share of the conserved
quantities and its phase. Alternatives are created only at
interactions, never at the empty Nodes a ray crosses, and only inside a
layer: events in different layers at the same Node do not communicate. A
wave ray between two
interactions is one line; at an interaction it becomes up to six lines.

**Wave ray.** Every ray is a wave ray and carries a phase (advancing along
the line for a massive ray, constant for light), together with its quantities (energy, momentum, charge, family
properties); a plain ray is a special case of the wave ray, not a second kind.
Light is a wave ray with no mass and no charge: it is an event moving in time,
exactly as defined above, not a separate photon object. Three things change
a phase and nothing else: each interval advances it at the rest rate its
family declares, which is the ray's mass as a clock, and that rate is zero
for light, whose phase does not advance along its own line; an interaction
changes it as the declared coupling says; a bound group advances it once per
interval it is held. A light ray carries the phase of the clock that emitted
it at the moment of emission and delivers it unchanged, so the frequency of
light is the rate of its emitter's clock. Interference of light follows from
this alone: two paths of different length reach one place at one time only
if their rays were emitted at different times, so they carry different
emission phases, and the difference is the emitter's rate times the
difference in path length; nothing is accumulated on the way. There
is no amplitude as a number and no probability field: the phase and the
ray's conserved content together are the discrete stand-in for the quantum
amplitude, the phase as its angle and the conserved content as its size.
Because every permitted trajectory happens, the intensity at a place is how
much content arrived there, and interference is steering: where rays meet
in one layer, the declared coupling reads their phase difference and decides
through which Port the shared content leaves, with every invariant exact;
nothing is erased. The basic steering coupling is the Born rule stated as a coupling: for a
phase difference δ it splits the shared content between the two candidate
Ports in the ratio cos²(δ/2) to sin²(δ/2), as a declared table of bounded
integer ratios with the remainder owned as Highlights 3.17 requires, so that
click intensities follow the Born rule with nothing read by any Detector. It
is declared, not derived. The Detector reads none of this; the
probability of a click is already in how much content reached it.

**Detector.** Every Node carries one bit: Detector or not. The mark is
bounded Node metadata (the bit, a setting, a ticket seed), not a record, not
an object and not an external device; "Detector behavior" is simply how a
Node behaves when the bit is set. A source is a Detector: whatever emits a
ray of a known family is a marked Node, because knowing the family of what
it emits is a measurement; the birth event of a pair therefore happens at a
marked Node, which draws on every arrival like any other. A marked Node
does one very simple thing.
What arrives at it is a wave ray carrying information; every ray is a wave
ray, so the kind of ray makes no difference to the Detector. For each
transfer that arrives,
whatever it is, it draws 1 or 0 from the mark's ticket sequence, and this
is the only place a lottery exists (`detector-only-v1`). On 1 the Node
behaves as an ordinary Node for that arrival: the transfer continues on its
line, or enters the declared interaction, as if no Detector were there, and
that pass is the measurement. On 0 there is no measurement: the Node returns
that wave ray on the same line in the opposite direction, unchanged, back the same number of
steps it has made since its event, so that it arrives at the Node it left
from with exactly the information it left with. Up to six
transfers can arrive in the same interval, one through each Port, and the
Node draws once for each arrival, independently: the arrivals that drew 1
enter the ordinary interaction together, exactly as at an unmarked Node, and
each arrival that drew 0 is returned on its own line. The Detector does not read,
change, absorb or add anything; it needs to know nothing about what passed.
A Detector sees nothing of the ray, on 1 or on 0: it sees only its own
value, the bit it drew. It is the same ray in both outcomes: not absorbed,
not split, no stock taken. The click is the record of the bit drawn, and it
exists on 1 only: a measurement exists only when the Node drew 1 and let the
ray pass; on 0 there is no measurement and no click, the Node returns the
ray without touching it and is a Node without measurement, as if the ray
had not arrived, and it waits for what the return brings back. The bit is
all the Detector adds: a ray leaving a marked Node records that its
last event was a Detector event and the bit drawn, nothing larger. When it
returned a ray with 0, that value travels with the ray through the inverse
split to the partner's line, and the second Detector of the pair receives it
on the ray that reaches it. Because a marked Node is a Node
like any other, everything else about it (rays crossing, interactions of
other families, fields) is unchanged.

**Return.** A returning ray retraces its own trajectory: it reverses its
heading and walks back exactly the number of steps it has made since its
event, unchanged. An event cannot be moved; there is no such thing. It
happened at its Node, and on a fixed lattice the returning ray reaches that
Node with certainty. The return is the ray itself, not a message and not a
separate carrier; it carries what the ray already carries (family properties,
phase, heading, the number of steps it has made since its event, the
information of its last event and, if that was a Detector event, its bit;
nothing larger). At the event Node it performs the
inverse split with its information: it transmits it, with its bit, to the
same places the event sent to, so that it cancels what was already there
and the momentum and energy of that share are restored exactly. This turns
time back for that ray's share only; the other shares are
untouched until their own rays return. For a pair, the partner ray's line is
among those places, so the partner's Detector is not missing the bit: that
is the same inverse split, not a second mechanism. The transmission is a ray like any other, with a field like any other: it
cancels the share only where it meets it, and where it meets nothing it makes
no event, by the same definitions. A share that left the event earlier on a
straight line at the same speed is met only where it was delayed: bound at a
Node, slowed by an output clock, changed by an interaction or standing at a
Detector; for a pair this is the condition of Highlights 5.4. Even when it
is never caught, the event as it was has changed: the returned ray reversed
its share, so the event lost that share, and the information is never lost,
it chases the share it cancels. If the share is delayed and caught, momentum
and everything else are conserved at the Node where they meet. What a returning ray does at its event Node when nothing is there is a
configured mode of the world, three of which are defined and tested:
siblings, the default and the rule above (it transmits its share and bit to
every line the event sent to, which needs at most six records on the ray,
one per Port); straight (it continues straight through the Node on the one
line opposite its own, enough for a pair, with no records); and annul (it
ends there, its content leaves the world into an explicitly accounted sink,
initial equals current plus escaped plus annulled at every tick, and its
information survives only in the record). If something is at the Node, a
bound group or other rays, the returning ray meets it by the declared
coupling in every mode. For a ray-interaction event whose inputs were
consumed, the returning ray cancels its own share only and continues along
the event's output lines; nothing is left at the Node.

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

**Field.** A ray has a field: the field is the ray's own information
spreading in ray form to the Nodes around it, without an event, along the
six headings, in all directions, one Link per interval, with the ordinary
dilution or declared attenuation of an outward field. Every ray is
the same ray; a field ray is
not a second kind, and field rays are not born at events: they are the
ray's information in ray form. The field's presence at a Node is an
interaction that makes no event. A field never makes an event unless it
meets something it changes; the first event a field is involved in is that
meeting, and the returning ray that carries the recoil is split off from
it, like every ray from its event. Where a field ray meets a ray whose
declared coupling responds, the
meeting is an ordinary interaction and its events change that ray's
trajectory; everywhere else the field crosses without an event. One of those
events is the field ray itself returning reversed: the return is the opposite
momentum of the field, carried back along the field ray's line to the ray
that released it, which recoils when the return arrives, at finite speed.
This is how Highlights 3.14 is satisfied: the recoil is a ray. Until its
field meets something, a traveling ray pays nothing for it. The field is
released in all directions. A ray traveling straight never meets its own
field: the field is born where the ray is and leaves at the causal speed,
ahead of the ray or away from it, and the ray is never faster than its
field, at any output-clock delay; no exclusion rule is needed. Only after a
change of trajectory can a ray cross field it released earlier, and that is
a meeting like any other. A ray's phase per interval comes from its family's
rest rate alone, not from its own field. The computation field (Highlights
3.28) is the same kind of field ray, obeying this one field rule with no rule
of its own: the retained content of a Node, its mass, is what makes it slow, and the
information that a Node is heavy spreads from it in ray form in all
directions. Where such a field ray meets a ray whose declared coupling
responds, there is an event with two effects: the ray that was met is
delayed, its output clock grows, and the field ray returns reversed to the
heavy Node. The delay is larger on the side nearer the heavy Node, so the
ray bends toward it; that bending is a change of momentum, and the
returning field ray carries the opposite momentum back to the heavy Node,
which is drawn toward the ray. Gravity is this bending by delay; it is not
inserted as a force, nothing is absorbed, and momentum is exact.

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

**External body (model owner, 2026-09-17; Highlights 3.19; named "fixed
body" earlier that day).** Beside the Detector there is one more declared
element of a world, and like the Detector it is a declaration, not physics:
a Node declared to hold a family with an amount and, if wanted, a charge,
standing for a star, a neutron star, a fixed proton, a large charge, or a
piece of apparatus. What is declared: the family, the amount (finite, of any
width, since it enters no sum; it only sets how much field leaves per
interval), the charge, and, if wanted, a trajectory. What it does: it
radiates exactly as any bound group does, by the one field rule above and
with the strength its amount gives, so its gravity and its electric field
are the ordinary field rays of this document and every ray that meets them
responds by its declared coupling. What it does not do: it does not spread,
which is its defining property: it never splits, binds, unbinds, converts or
decays, and its whole content stays at one Node; and it is not pushed:
whatever arrives at it, a recoil field ray or a ray that couples to it, is
met by the declared coupling of its family, and the body itself never
changes. Absorption into an explicitly accounted sink is the default
coupling, and the other couplings make the apparatus: a reversed heading is
a mirror, a split by a declared table is a beam splitter, a phase offset is
a phase plate, a polarization read is a polarizer once feature 11 exists; a
wall, a screen and a beam stop are the default. It may move on a declared
trajectory, and wherever it is, the Node it is at holds all of it; its
motion is declared, never caused, because nothing on the board can push it,
so two external bodies never move each other. The audit books what it
radiates as a source and what it absorbs as a sink, so conservation stays
exact at every tick. On the Node it is bounded metadata like the Detector
mark: the kind of mark, the declaration, and one exact counter (the sink
totals per family); no rays, no history. When the back-reaction is wanted, a
star that recoils or a proton that moves, the body is not used: the same
thing is declared as an ordinary bound group with a large amount, and then
it spreads and is pushed like all matter. The external body is the
approximation of infinite mass, used for the confrontation runs: light
bending by a star, an electron near a large charge, a hydrogen-like spectrum
around a fixed proton, and the two-slit and Bell geometries with their
walls, mirrors and splitters. In the Node's law it is one flag: spreading
is not enforced for this Node's content, and every other step of the law
(the arrivals, the couplings by table, the stamping, the departures of what
leaves) is unchanged. That flag is also why it has no ladder of masses: the
ladder of
[hypothesis 12](HYPOTHESES.md#12-one-mass-ladder-and-the-composite-spectrum-from-binding)
comes from the spreading law, since a bound group is rays that must keep
moving and bind again every interval, so only the closed patterns the
binding table can hold exist; a body that does not spread has no closure
condition and any amount is allowed. It is feature 7b of the migration in
section 6, after feature 7, `external-body-v1`.

## 2. The single generic rule

At a Node where two or more rays are resident in the same interval, the
declared coupling between their families decides one of:

- **no interaction**: the rays cross and continue as if the other were not
  there (no coupling declared, so the rays are in different layers and never
  meet; or the coupling's guard is false);
- **a deterministic interaction**: up to six events leave the Node, computed
  from the frozen inputs by the declared operation, with every declared
  invariant (energy, momentum component by component, charge, family counts)
  exact over all inputs and outputs, the phase of each leaving ray changed
  as the declared coupling says and, where the arriving rays' phases
  differ, the coupling reading their phase difference to decide through
  which Port the shared content leaves (interference as steering, nothing
  erased; the basic steering coupling is the Born rule stated as a coupling,
  splitting the shared content between the two candidate Ports in the ratio
  cos²(δ/2) to sin²(δ/2) for a phase difference δ, as a declared table of
  bounded integer ratios with the remainder owned as Highlights 3.17
  requires, declared, not derived), exactly as the
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
| Where is state stored | On the ray, the list of Highlights 5.1: family properties, phase, heading, the number of steps it has made since its event, the information of its last event and, if that was a Detector event, its bit; every ray is a wave ray and all the information is on the rays. On the Node: the rays resident this interval, the bounded bound group if any, and the Detector mark if the Node carries one (mark, setting, ticket seed). The origin Node of an event keeps nothing; there is no register of any kind, no occupied channel and no capacity rule: rays cross, meet or bind by their declared couplings, and nothing is pushed back or made to wait for room |
| What arrived | The rays delivered through the six Ports this interval, met layer by layer (a layer is a set of families that couple; rays of families with no declared coupling never meet); a resident bound group counts as arrived every interval |
| What operation acts | The coupling declared for the set of families present, in declared order; at a Node whose Detector bit is set, first one 1-or-0 draw for each transfer that arrived this interval, independently, the kind of ray making no difference since every ray is a wave ray; the arrivals that drew 1 then enter the declared coupling as at an unmarked Node, and each arrival that drew 0 is returned on its own line; a returning ray that has walked back its step count performs the inverse split of its share at its event Node, transmitting it, with its bit, to the same places the event sent to |
| Is an outcome recorded | Only at an interaction: the events that leave it, and at a marked Node the click on 1 only, the pass being the measurement; a return (0) is not a measurement and records no outcome; crossing records nothing |
| How long it takes | One interval per Link as today; an interaction takes its declared wait; a bound group advances its phase once per interval it is held |
| What crosses each Link | Rays only, at most one new event per Port per interaction. A returning ray is an ordinary ray with a reversed heading and a decreasing step count, and what its inverse split transmits travels the lines the event sent to, one Link per interval. No message, no registry answer, nothing that skips a Node |

## 3. Pairs, the carried bit and the price

A bonded pair is one birth interaction and two rays with opposite headings.
The source is a marked Node: whatever emits a ray of a known family is a
Detector, because knowing the family of what it emits is a measurement, so
the birth event happens at a marked Node that draws on every arrival like
any other. Each ray reaches its own Detector and is drawn there. A ray that
returns walks back exactly its step count to the birth interaction, where it
is drawn like any arrival: on 0 it is sent back out along its own line; on 1
it performs the inverse split of its share there: it transmits what happened at the event, with
its bit (the outcome of the first draw, all the Detector added), to the same
places the event sent to, the partner ray's line among them, so the partner's
Detector is not missing it: the first Detector saw only its own value, and
the second Detector receives that value on the ray that reaches it. With two
Detectors, Alice's and Bob's, whichever returns first sends its value through
the birth event and the other receives it; sometimes it is Alice's
information, sometimes Bob's. To Alice and Bob the correlation feels as if it
were decided at time zero, but nothing happened at time zero: the value was
carried through the birth event in event spacetime, one Link per interval.
Every Detector behaves the same: the second Detector draws its own bit on
that arrival like on any other and reads nothing from the ray; the received
value is information on the ray, not an input to the draw. The information of the last event and the Detector's bit stay on the ray as
hidden variables: no Detector and no ordinary coupling reads them today, they
come from no ordinary physics, and for now they affect no one; nothing on the
board feels them.

This replaces the shared registry of the historical bonded profile with a
carried bit, so the model has no owner that answers at a distance. The
price is accepted explicitly: two Detectors at equal distance from the birth
draw independently, and the CHSH value for spacelike settings is at most 2.
The quantum value appears only when the second ray's path is longer than the
round trip through the first Detector. Pair identity becomes the trajectory,
so two pairs born at one Node in one tick are distinct, which closes the
birth-code collision found on 16 September 2026 by the Bell and postulate 22
study (`examples/research/bell-postulate-22/`, deleted on 2026-09-17 with the
bond registry).

**Entanglement is the name for siblings of one event (2026-09-17, Highlights
3.20).** Entanglement is the shared last-event record of siblings and nothing
else: rays that left the same last event carry the same record of it, nothing
reads that record until a Detector, and that shared record and the trajectory
back to the event are all there is to it; no register and no state at a
distance. A Detector that draws 1 realizes its ray; one that draws 0 returns
it, and the returning ray delivers what it carries to the sibling lines
through the event by the inverse split of the Return definition, so whatever
happens between an event and the first pass, 1, is a correlated set of rays,
and a pass is the only thing that ends it. An ordinary meeting on the way is
itself an event: its outputs are new siblings of that new event, and each
ray's siblings are always those of its own last event. The earlier
correlation is not lost: the transmission from a return chases the share
through the later event by that same rule, which is how correlation passes
from one pair to another without any rule for it. The price above applies to
every such set; Highlights 3.20 is the text to follow.

## 4. Why this is consistent

- One kind of entity (an event trajectory with the state of Highlights 5.1:
  family properties, phase, heading, the number of steps since its event,
  the information of its last event and, for a Detector event, its bit),
  one kind of interaction (a meeting at a Node, declared per
  family set, exactly conserved, at most six events out), one door for
  randomness (the Detector draw, one per transfer arriving at a marked Node). Postulates 1 to 4 hold
  without exception; the registry exception of postulate 4 is withdrawn and
  Highlights section 3.18, which described the shared resource, is deleted
  (2026-09-17).
- Fields as rays satisfies Highlights 3.5 and 3.28 directly: a field is a
  local description of ray state, the ray's own information spreading in ray
  form without an event; a field ray is not a second kind and is not born at
  an event; its presence at a Node makes no event unless it meets something
  it changes; and the computation field is a propagating property.
  Highlights 3.14 is satisfied by a ray: when a field ray changes another
  ray's trajectory it returns reversed along its own line, a ray born at
  that meeting, and the ray that released it recoils
  by the opposite momentum when the return arrives, at finite speed; until
  its field meets something, a traveling ray pays nothing for it.
- Matter as bound rays satisfies Highlights 3.4: mass is the retained energy of
  a bound group, not a stored property; the group's phase advance is its own
  clock, which the light-clock measurement (`examples/research/anomalies/`, deleted on 2026-09-17)
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
| Records emit fields; rays do not | A traveling ray's own information spreads in ray form to the Nodes around it, without an event; a field ray is not a second kind and is not born at an event, and its return reversed, born at the meeting it changes, is the emitter's recoil |
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
2. Ray state, the list of Highlights 5.1: family properties, phase, heading,
   the number of steps it has made since its event, the information of its
   last event and, if that was a Detector event, its bit. The step count, the
   last event's information and the bit are added, carried, not read by any
   rule yet (hidden variables that affect no one for now); heading and phase
   exist,
   and the phase is carried by every ray, since every ray is a wave ray. No
   origin reference is stored: the count suffices on a straight line, and no
   Node keeps anything about the event. (Done on 2026-09-17, issue #169
   feature 1, `ray-event-state-v1`: `Ray` carries `steps`, `outbound`,
   `event_ports`, `event_shares` and `detector`, stamped by emissions and ray
   interactions, part of the merge identity, counted down on the walk back,
   read by no rule; see [ray state](SPATIAL_FIELDS.md#ray-state-ray-event-state-v1).)
3. Detector as a Node bit in the initialization (position, setting, ticket
   seed): each transfer through a marked Node draws 1 or 0 from the mark's
   ticket sequence, 1 ordinary behavior, 0 return on the same line reversed;
   the `detector_click` record on 1 only, a return recording no outcome; no
   stock; no detector record type. (Done on 2026-09-17, issue #169 feature
   2, `detector-mark-v1`: the `detectors` key, `DetectorMark`, one unsalted
   draw per arriving ray from the mark's own stream in Port then merge-key
   order, the ray's bit set to 2 on 1 and 1 on 0, the click on 1 only, a
   replay redrawing nothing; the reversal on 0 is step 4, feature 3, and
   until then a ray that drew 0 continues unchanged with its bit 0; see
   [Detector mark](DETECTOR_SAMPLING.md#the-detector-mark-detector-mark-v1).)
4. Return propagation: reversed heading, decreasing count; at the event Node
   the inverse split of the returning ray's share, transmitted with its bit
   to the same places the event sent to, the partner's line among them;
   meeting rule at the far Detector as in section 3. No event is moved and
   no Node keeps a register. `return_mode` in the initialization selects
   what a returning ray does at its event Node when nothing is there, with
   the three values siblings (default; at most six records on the ray, one
   per Port), straight (no records) and annul (an explicitly accounted
   sink: initial equals current plus escaped plus annulled at every tick);
   in every mode a returning ray that finds something at the Node meets it
   by the declared coupling, and for a ray-interaction event whose inputs
   were consumed it cancels its own share only and continues along the
   event's output lines.
5. Registry removal from the physical path (done on 2026-09-17, issue #164
   bucket B.5: the registry, the bonded profile, claim-gather, the lottery
   capture, the occupied-links guard and their tests and probes were deleted;
   their measurements stay in the validation log as history, not as the
   active law).
6. Light as a wave ray with no mass and no charge and rest rate zero, every
   ray being a wave ray: its phase does not advance along its line; it
   carries its emitter's clock phase at emission and delivers it unchanged;
   conversion products emitted as events from the
   interaction; the N-to-M mechanism invoked at a meeting of rays without a
   resident record, up to six events out; the steering table as a catalog
   coupling, the Born rule stated as a coupling (for 8 phase steps the
   example ratios 8/8, 7/8, 4/8, 1/8, 0/8, 1/8, 4/8, 7/8 of the shared
   content to the first candidate Port and the rest to the second, the
   remainder owned as Highlights 3.17 requires). (The wave-ray part is done
   on 2026-09-17, issue #169 feature 9, `wave-ray-family-v1`: every ray
   carries a phase of its family's declared width `phase_bits`, a mask and
   never a division; light is a family with rest rate 0 that carries its
   emitter's phase unchanged; `family` and `charge` are read-only ray
   properties and `charge x amount` summed over rays is an invariant of
   every declared interaction; see [wave-ray
   families](SPATIAL_FIELDS.md#wave-ray-families-wave-ray-family-v1). The
   meeting with N-to-M conversion and the steering table remain feature 6.)
7. Field emission by traveling rays, with the outward dilution or declared
   attenuation of the existing field contracts; a field ray whose meeting
   changes another ray's trajectory returns reversed along its own line as
   the emitter's recoil, arriving at finite speed, and a traveling ray pays
   nothing for its field until the field meets something; the field is
   released in all directions and a ray traveling straight never meets its
   own field, since the field leaves at the causal speed ahead of it or away
   from it and the ray is never faster (no exclusion rule); its phase per
   interval comes from its family's rest rate alone; the computation field
   is the same kind of field ray under this one rule, the information that a
   Node is heavy spreading in ray form in all directions, a met ray whose
   declared coupling responds being delayed (its output clock grows) and the
   field ray returning reversed with the opposite momentum to the heavy
   Node.
   Feature 7b, external body, `external-body-v1`, after feature 7 (model
   owner, 2026-09-17, Highlights 3.19; named "fixed body" earlier that day):
   a Node declared to hold a family with an amount (finite, of any width,
   since it enters no sum) and, if wanted, a charge and a trajectory,
   standing for a star, a neutron star, a fixed proton, a large charge, or a
   piece of apparatus; it radiates by this one field rule with the strength
   its amount gives, does not spread (never splits, binds, unbinds, converts
   or decays, its whole content at one Node) and is not pushed: whatever
   arrives at it is met by the declared coupling of its family, absorption
   into an explicitly accounted sink by default (a wall, a screen, a beam
   stop), a reversed heading a mirror, a split by a declared table a beam
   splitter, a phase offset a phase plate, a polarization read a polarizer
   after feature 11; the audit books what it radiates as a source and what
   it absorbs as a sink; it may move on a declared trajectory, never caused,
   and is held whole by the Node it is at; on the Node bounded metadata like
   the Detector mark (the kind of mark, the declaration, one exact counter of
   the sink totals per family; no rays, no history); the approximation of
   infinite mass for the confrontation runs (section 1), and where the
   back-reaction is wanted an ordinary bound group with a large amount is
   declared instead.
8. Binding couplings: the bound-ray-pair candidate generalized to a bound
   group of N rays of declared families in one Node (the strong binding),
   possibly nothing more than a very large output-clock delay the bound rays
   create together, unbound by an arriving ray's declared coupling; then
   the orbit: a ray whose trajectory is changed at every step by the field
   rays of a bound group; the heavy Node's field delaying a passing ray more
   on its nearer side so that it bends toward the Node, gravity as bending
   by delay, not an inserted force, momentum exact.
9. Tests and experiments: reversibility replay; the light cone of the carried
   bit; CHSH with equal distances (expected at most 2) and with a delayed
   second ray (expected the singlet value); a light clock between two
   Detectors instead of two mirrors, the family's declared rate being a rest
   rate, the mass as a clock, zero for light; the steering table as a
   catalog coupling, for 8 phase steps the ratios 8/8, 7/8, 4/8, 1/8, 0/8,
   1/8, 4/8, 7/8, click intensities following the Born rule with nothing
   read by any Detector; the bound group under load.

Layers, the "met layer by layer" of the table in section 2, are not a
numbered step of this list but feature 5 of issue #169 (done on 2026-09-17,
`ray-layers-v1`): the layers are derived once from the catalog as the
connected components of the ray fields over the participants of the declared
`ray_interactions`, a field that no rule selects is its own layer, the
interaction step at a Node meets the resident rays layer by layer so that
rules of different layers fire independently in one interval and an unruled
ray crosses unchanged, and the runner records the derived layers; see
[layers](SPATIAL_FIELDS.md#layers-ray-layers-v1).

The meeting with N-to-M outputs of step 6 is feature 6 of issue #169 (done on
2026-09-17, `ray-meeting-conversion-v1`): a `ray_interactions` rule with
declared outputs replaces its participants by up to six new event rays at
the meeting Node, without a resident record, every family's stock and the
declared invariants exact as sums over inputs and outputs; the steering
table is a declared coupling, an output amount split by the table at the
phase difference of two inputs, the rest output owning the remainder as
Highlights 3.17 requires; the momentum such a split moves is booked as an
accounted source until the field ray of step 7 owns it as recoil; see
[meetings with outputs](SPATIAL_FIELDS.md#meetings-with-outputs-ray-meeting-conversion-v1). With it the ray path no longer needs
`fields/record_operations.py` and `core/record_policy.py`, so step 6 of
issue #164, their deletion, is unlocked. The wave-ray phase rule and the
light family of step 6 follow with feature 9.

Each step is a separate published change with its own model identity, tests
and evidence, under the ordinary gates.

**After feature 10 (decided 2026-09-17, Highlights 3.26 and 5.3).** The ten
features of [issue #169](https://github.com/Closer24/Universe24/issues/169)
(ray state, the Node Detector bit, the return, the inverse split, layers, the
meeting with N-to-M conversion, the released field, binding, every ray a wave
ray with family and charge, the audits) close the engine: a step on a Link, a
phase advance, a split by a declared table, a sum, and the one draw at a
marked Node. Anything that does not change how a ray moves between events is
catalog work on that engine, a family property or a coupling table read only
at a meeting, exactly as charge is (feature 9), and none of the ten features
needs it. What follows adds no engine mechanism.

**Feature 11, polarization.** A family property: a transverse mode
perpendicular to the heading, two states for light (the two lattice axes
perpendicular to an axial heading) and two for the electron family (spin),
read by the declared couplings at a meeting. A circular polarization is not
defined; if wanted, it is a transverse direction that turns with the phase
plus one handedness bit, again a catalog choice. Pauli exclusion is a binding
coupling (feature 8) that does not fire for two electrons in the same state
with the same spin. The Bell prediction of
[hypothesis 11](HYPOTHESES.md#11-the-bell-prediction-of-the-ray-event-model-stated-so-that-it-can-fail)
is testable before this feature, in its phase form.

**The strong interaction, catalog work after feature 10.** Quark families,
colour a property with three values (a family property like charge, feature
9), the gluon the quark's own field in ray form (feature 7, Highlights 3.5),
the binding of three quarks a binding coupling (feature 8, Highlights 3.4),
and one more declared coupling, the quark's field rays binding to each
other, from which the short range and the growth with distance are expected.
Whether that yields confinement is
[hypothesis 13](HYPOTHESES.md#13-confinement-from-the-quarks-field-rays-binding-to-each-other),
a research question for a run, not an engine decision.

**The weak interaction and decay, catalog work after feature 10.** A change
of family: an N-to-M conversion at an event (feature 6) with its declared
invariants (charge, energy, momentum). A free particle never decays, because
there is no event without a meeting and a straight ray does not change. A
neutron is a bound group whose ticks are events; a bound group that can decay
is a source, and a source is a Detector (Highlights 3.19), so at each tick it
draws with its declared ratio as the setting (the mark of feature 2), 1 = the
conversion fires, 0 = the group ticks on unchanged, and half-life follows.
That is the one draw of the Detector interaction, at a Node whose Detector
bit is set; nothing else in the world draws, and no second lottery is added.

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
  Detector adds: a Detector sees nothing of the ray, only its own value; a
  ray leaving it carries its share, that its last event was a Detector event
  and the bit, nothing larger; a click is recorded on 1 only, a return is
  not a measurement and no outcome is recorded for it; replay with the same
  seed reproduces every click; changing one Detector's bit changes the world
  only inside the forward light cone of that interaction.
- An interaction never emits more than six events and never two on one Port;
  every declared invariant is exact over all inputs and all events out.
- The source of a pair is a marked Node, drawing on every arrival like any
  other. A pair with equal Detector distances gives CHSH at most 2 within
  counting error; the joint law's value appears only when the second ray's
  path exceeds the round trip through the first Detector, and no Detector
  reads the carried value: the second Detector draws its own bit and reads
  nothing from the ray. The pair test counts coincidences of clicks within a
  declared time window; a pair with one return is unpaired. The test reports
  CHSH in the symmetric geometry and in the delayed geometry; what each
  outcome means is stated in
  [HYPOTHESES.md section 11](HYPOTHESES.md#11-the-bell-prediction-of-the-ray-event-model-stated-so-that-it-can-fail).
- Conservation audits balance at every tick; no Node holds stock after an
  interaction; every ray is resident, in flight or escaped, and nothing else.
- Mode siblings (the default): a returned ray that finds nothing at its
  event Node transmits its share and bit to every line the event sent to,
  at most six records on the ray, one per Port; it cancels exactly its own
  share, the other shares are untouched until their own rays return, every
  declared invariant is equal before the split and after the return, and
  no Node keeps anything about the event.
- Mode straight: a returned ray that finds nothing at its event Node
  continues straight through it on the one line opposite its own, with no
  records; for a pair, the partner's Detector receives the bit on that ray.
- Mode annul: a returned ray that finds nothing at its event Node ends
  there and its content leaves the world into an explicitly accounted sink,
  so that initial equals current plus escaped plus annulled at every tick;
  its information survives only in the record.
- In every mode, a returned ray that finds a bound group or other rays at
  its event Node meets them by the declared coupling; for a ray-interaction
  event whose inputs were consumed, it cancels its own share only and
  continues along the event's output lines, and nothing is left at the
  Node.
- Two rays of one event that meet in one layer under the Born steering
  coupling: a phase difference of 0 sends all the shared content to one
  Port, half a turn sends all of it to the other, and a quarter turn splits
  it in half, with exact totals in every case and the remainder owned: the
  content that arrived is the content that left, and nothing is erased.
- A light ray's phase is constant along its line and equals its emitter's
  clock phase at emission, while a massive ray's phase advances by its
  family's rest rate every interval, including the intervals it is held.
- A ray with an output-clock delay traveling straight is never met by its
  own field on any seed, with the field released in all directions, while a
  second ray on a parallel line is met; the first ray's phase advances at
  its family's rest rate alone.
- A ray passing a heavy Node on a parallel line is delayed more on its
  nearer side and leaves bent toward the Node; the field ray it met returns
  reversed to the heavy Node carrying the opposite momentum, with exact
  totals; a control run with no heavy Node goes straight.

## 8. Open decisions

None remain from the model owner's side as of 2026-09-17: every question this
section listed (the lifetime and register of an open alternative, moving an
event, reassembly and re-emission, what the returning ray carries, whether a
field ray alone changes a trajectory, the funding of the released field, the
lifetime of a bound group, and how the transmission of an inverse split meets
the share it cancels) is answered in Highlights 3.3, 3.4, 3.5, 3.20 and 5.4
and restated above.

Decided on 2026-09-17 (Highlights 3.20) for the last of these, and stated in
the Return definition: the inverse-split transmission is a ray like any
other, with a field like any other; it cancels the share only where it meets
it, and where it meets nothing it makes no event, by the same definitions. A
share that left the event earlier on a straight line at the same speed is
met only where it was delayed: bound at a Node, slowed by an output clock,
changed by an interaction or standing at a Detector; for a pair this is the
condition of Highlights 5.4. Even when it is never caught, the event as it
was has changed: the returned ray reversed its share, so the event lost that
share, and the information is never lost, it chases the share it cancels. If
the share is delayed and caught, momentum and everything else are conserved
at the Node where they meet.

Deferred on 2026-09-17 (Highlights 3.26), not open: polarization is feature
11, and the strong and weak interactions and decay are catalog entries on the
same engine after feature 10, stated at the end of section 6. The one
research question they leave, whether the quark's field rays binding to each
other yields confinement, is
[hypothesis 13](HYPOTHESES.md#13-confinement-from-the-quarks-field-rays-binding-to-each-other),
answered by a run, not by an engine decision.
