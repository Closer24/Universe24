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

**Ray.** A ray is not an object. It is the trajectory of one event along one
straight line of Nodes: the same event, the same family properties, one Node
per Link interval, one heading. Between two interactions nothing new happens
to it. A ray trajectory is therefore reversible: run backward step by step it
returns exactly to the event that created it, because no information was added
or lost along the line.

**Event.** An event is an endpoint of a ray: its birth, or a break. A ray
connects two events. This replaces the current reading of an event as any
local change at a Node in a tick; a Node that a ray merely crosses hosts no
event.

**Interaction (break).** An interaction is a break of the line: a split (one
event becomes several) or a change of heading. Only at a break is anything
decided. Everything between breaks is a ray.

**Wave ray and non-wave ray.** A wave ray carries a phase that advances along
the line. A non-wave ray carries quantities only (energy, momentum, charge,
family properties). Light is a wave ray with no mass and no charge: it is an
event moving in time, exactly as defined above, not a separate photon object.

**Detector.** A Detector is a break with a simple binary lottery, and it is the
only place a lottery exists (`detector-only-v1`). A wave ray meeting a Detector
either continues on the same line in the same heading, or reverses by a half
turn and goes back along the same line. It is the same ray in both outcomes:
not absorbed, not split, no stock taken. The click is the record that the ray
passed or returned. A non-wave ray meeting a Detector is not drawn; its outcome
follows from its declared coupling.

**Return.** A returning ray retraces its own trajectory: it reverses its
heading and walks back the number of steps it counted since its last break. On
a fixed lattice this reaches, with certainty, the event that created it. The
return is the ray itself, not a message and not a separate carrier; it carries
what the ray already carries (family properties, phase, and the Detector's
outcome in a bounded register). When it reaches its birth event it continues
straight through it, which is by construction the direction of the partner
ray of a pair.

**Field.** A ray that travels releases a field, and the field is itself made
of rays: family-declared outward emission along the six headings, one Link
per interval, with its own conserved quantity and the ordinary dilution or
declared attenuation of an outward field. A field ray is a ray in every sense
above: it crosses Nodes without event, it meets other rays at Nodes, and a
meeting is a break decided by the declared coupling between the families.

**Matter.** There is no matter in the model at this stage. Matter is the name
for rays bound in one Node: for example a neutron ray and a proton ray held
together in one cell by a declared strong binding coupling, and an electron
ray around them whose line is broken at every step by the field rays the
bound pair emits. Everything is the same generic ray with the same generic
break; what remains is to close the binding couplings. Until they exist,
held source records remain an explicitly labeled interim device.

## 2. The single generic rule

At a Node where two or more rays are resident in the same interval, the
declared coupling between their families decides one of:

- **no break**: the rays cross and continue (no coupling declared, or the
  coupling's guard is false);
- **a deterministic break**: a split or heading change computed from the
  frozen inputs by the declared operation, with every declared invariant
  (energy, momentum component by component, charge, family counts) exact over
  all inputs and outputs, exactly as the [N-to-M conversion contract](LOCAL_CONVERSIONS.md#n-to-m-family-conversion)
  already does for records;
- **a Detector break**: only if one participant is a declared Detector and
  the other is a wave ray: one bounded integer is drawn from the Detector's
  own ticket sequence and selects pass or return.

Nothing else decides anything. A ray alone at a Node never breaks. A Node
never holds a ray without a declared binding coupling. The
[bound-ray-pair candidate](HYPOTHESES.md#candidate-rule-bound-ray-pair-v1-a-candidate-not-implemented)
is the special case of a binding coupling between two counter-heading rays of
one family.

The rule in the form Highlights 3.27 requires:

| Question | Answer under this model |
| --- | --- |
| Where is state stored | On the ray: family properties, phase, heading, step count since the last break, one bounded outcome register. On the Node: nothing but the rays resident this interval and the bounded bound-group, if any |
| What arrived | The rays delivered through the six Ports this interval; a resident bound group counts as arrived every interval |
| What operation acts | The coupling declared for the set of families present, in declared order; the Detector lottery only for a Detector and a wave ray |
| Is an outcome recorded | Only at a Detector break (the click) and at a split or heading change (the break event); crossing records nothing |
| How long it takes | One interval per Link as today; a break takes its declared wait; a bound group advances its phase once per interval it is held |
| What crosses each Link | Rays only. A returning ray is an ordinary ray with a reversed heading and a decreasing step count. No message, no registry answer, nothing that skips a Node |

## 3. Pairs, the carried number and the price

A bonded pair is one birth event and two rays with opposite headings. Each ray
reaches its own Detector and is drawn there. A ray that returns walks back to
the birth event and continues to the other side, carrying the number that the
other Detector "was missing": the outcome of the first draw. If it reaches the
second Detector before the second ray is drawn, the second draw reads it and
the pair agrees by the configured joint law; if the second ray was already
drawn, the returning ray is recorded and ignored.

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
  optional phase), one kind of interaction (a break at a meeting, declared per
  family set, exactly conserved), one door for randomness (the Detector break
  of a wave ray). Postulates 1 to 4 hold without exception; the registry
  exception of postulate 4 is withdrawn.
- Fields as rays satisfies Highlights 3.5 and 3.28 directly: a field is a
  local description of ray state, and the computation field is a propagating
  property.
- Matter as bound rays satisfies Highlights 3.4: mass is the retained energy of
  a bound group, not a stored property; the group's phase advance is its own
  clock, which the [light-clock measurement](../examples/research/anomalies/README.md)
  says slows with the hop time.
- The stranded-stock defect of the two-phase hold in the radiation-scattering
  candidate cannot occur: no Node owns intermediate stock; a break is one
  transaction at the Node where the rays actually are.
- Reversibility is testable: replaying any ray backward between two breaks
  must reproduce its forward trajectory exactly.

## 5. What the current engine does differently

| Today | Under this model |
| --- | --- |
| Every break passes through a resident record (mirror, screen, detector, lamp) with stock and absorption | A break is a property of the meeting of rays; a Detector is a rule on the line, not a record with stock |
| The photon is a record of a family; conversion products are records | Light is a wave ray with no mass and no charge; conversion products are rays emitted from the break event |
| A bonded pair is answered by a global registry keyed by (Node, tick) | The first draw's outcome travels back and forward on the ray itself; pair identity is the trajectory |
| Records emit fields; rays do not | A traveling ray of an emitting family releases field rays along its line |
| A record can hold, wait at zero cost and be updated in place | Nothing holds except a bound group under a declared binding coupling |
| An event is any local change at a Node | An event is a birth or a break; crossing a Node is not an event |

## 6. Migration, in order

1. This document, reviewed by the model owner; then its text proposed to the
   central specification sections 1, 3 and 4 and reflected in
   [TERMINOLOGY.md](TERMINOLOGY.md) (Event, Ray, Break, Detector), in the
   [postulates](../POSTULATES.md) 4, 12 and 22 (the number is carried, not
   shared), and in [SPATIAL_FIELDS.md](SPATIAL_FIELDS.md) (the bonded profile
   becomes historical).
2. Ray state: step count since the last break and one bounded outcome register
   added to the ray; heading and phase exist. No origin reference is stored:
   the count suffices on a straight line.
3. Detector as a break on the field: pass or return, drawn from the Detector's
   ticket sequence; click event recorded; no stock. Non-wave rays are not drawn.
4. Return propagation: reversed heading, decreasing count, straight through
   the birth event; meeting rule at the far Detector as in section 3.
5. Registry removal from the physical path; the historical bonded profile and
   its tests are retained as history, not as the active law.
6. Light as a wave ray family; conversion products emitted as rays from the
   break; the N-to-M mechanism invoked at a meeting of rays without a resident
   record.
7. Field emission by traveling rays, with the outward dilution or declared
   attenuation of the existing field contracts and an explicit funding rule
   (a field released by a traveling ray carries its own conserved signal and
   no energy of the emitter unless a radiation coupling says so).
8. Binding couplings: the bound-ray-pair candidate generalized to a bound
   group of N rays of declared families in one Node (the strong binding), then
   the orbit: a ray whose line is broken at every step by the field rays of a
   bound group.
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
- One number per Detector break; replay with the same seed reproduces every
  click; changing one Detector's number changes the world only inside the
  forward light cone of that break.
- A pair with equal Detector distances gives CHSH at most 2 within counting
  error; a pair whose second ray is delayed by more than the round trip gives
  the configured joint law's value.
- Conservation audits balance at every tick; no Node holds stock after a break;
  every ray is resident, in flight or escaped, and nothing else.

## 8. Open decisions

- What exactly the returning ray carries: its own outcome only, or the full
  drawn number.
- Whether a field ray alone can break a line (a lens, refraction) or only a
  meeting of two rays at a Node; under this model a field ray is a ray, so the
  meeting rule covers it, but the coupling law is not chosen.
- The funding of the field a traveling ray releases: signal without energy
  (the present outward field) or a radiation coupling paid by the ray.
- The lifetime of a bound group and what unbinds it.
