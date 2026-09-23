# Simulator postulates in plain language

Since 2026-09-23 (the model owner, record 1421 of docs/LOG_2026-09-20.md: "all
the postulates must be changed so that they agree with the algebra; what does
not agree there is settled by the algebra") the source of every principle here
is [docs/ALGEBRA.md](docs/ALGEBRA.md); a postulate that agrees with it stands,
one that disagrees is rewritten to it and its old text marked history, and a
statement the algebra does not carry is marked a DECLARATION (world data),
HISTORY with its date, or HOST (a rule of the machine or of the document);
nothing is deleted. Nothing enters the law but on the owner's word, and the
algebra is his word here. The table of that reading, one row per statement of
this file with the verdict and the algebra's line, is
[docs/designs/detector_law/POSTULATES_BY_ALGEBRA.md](docs/designs/detector_law/POSTULATES_BY_ALGEBRA.md);
the algebra's own status words (SHOWN, MET, FAIL, NOT READ; READING,
DECLARATION, RULE, NOTHING) are the finer scale of the three categories below.

This document explains the ideas underlying the simulator without programming
details. Consult it before any change. A change contradicting a binding principle
requires an explicit decision to change the model. (History, superseded
on 2026-09-23 by ALGEBRA.md, the head: the algebra binds the postulate, never the
reverse.)

(History, marked 2026-09-23: the generic disturbance simulator the next paragraph
describes, its execution profile and its reaction contract were deleted on
2026-09-19 with the engines before the Beam Law; the law in force is
docs/ALGEBRA.md chapter 2.)

The user-authorized Node execution profile
declares h as one adjacent-node transit step and each interaction's k as an
explicit positive integer duration in h units. Sequential fired interactions add
their durations; link transit follows local completion. Operation cost is measured
separately. The earlier cost-budget delay contract below still describes profiles
without `node_execution: true`. Conserved readouts remain selected assumptions
until independently derived physical behavior is demonstrated.
Its generic reaction contract admits several local disturbances and fields in
one frozen proposal. Declared invariants and persistent validity conditions must
hold at actual commit, including after a local arrival during the wait. A consumed
start trigger is not a persistent condition. Every affected owner commits together
or remains unchanged; a failed check reports an error without repairing the law.

Distinguish three categories:

- **Binding principle:** a rule the simulator must satisfy.
- **Candidate law:** a specific hypothesis under evaluation, not a proven law of nature.
- **Open question:** an idea that has not been implemented or established.

## Physical detector candidate (2026-09-19)

The detector itself is ordinary Nodes and Events. (AGREES with the algebra on the
model owner's word of 2026-09-23, record 1425: every thing on the board is an
algebraic object declared under the algebraic laws; ALGEBRA.md 3.4, chapter 2.11
as rewritten on the branch algebra-chapter-2-11, and
docs/designs/detector_law/MASSIVE_RECORD.md section 4: a declared set of cells
running the one map with one declared pair, read by the evaluation E across its
cells.) Its complete physical state
is definite; a common visible result is formed by local physical interactions.
Information preservation is a separate requirement from determinism. The
uncertainty relation is an identity of the click: the record's element of Z[Z_N]
(the integer group ring of the phase circle) is evaluated at the roots of unity
(ALGEBRA.md 2.5), and on the phase circle the supports of a record and of its
transform obey abs(supp f) x abs(supp f_hat) >= N (4.11), Kennard's relation the
thing compared with in the limit. The owner's
hypothesis is that cell sensitivity together with on-board information retention
can produce Heisenberg uncertainty; this remains a research target (history,
superseded on 2026-09-23 by ALGEBRA.md 4.11).
Under the Beam Law (`beam-v1`, 2026-09-19) the interval is a bijection
on a GameBoard without a measured event and the click is the one one-way border;
the detector's record is the squared coherent sum of the rows it clicked,
read at the detector, a DETECTOR reading (ALGEBRA.md 3.2), never on the GameBoard
(the earlier words "read on the GameBoard": history, superseded on 2026-09-23 by
ALGEBRA.md 3.2). This inserts no quantum bound and does not claim that a
world with clicks is reversible. The law and its open limits are in
[the Beam Law](docs/BEAM_LAW.md) and
[the detector requirements](docs/DETECTOR_REQUIREMENTS.md), following
[Highlights 5.4](docs/HIGHLIGHTS.md#54-the-detector).

## GameBoard topology (2026-09-19)

The GameBoard is the torus of ALGEBRA.md 1.6, the translation group Z_X x Z_Y x
Z_Z (the extents per axis) modulo the sides; its faces are the torus's unless a
world declares a face open, and an open face is the border of that axis, a
click at the face detector (1.6) (the model owner, 2026-09-23, record 1421).
The engine's key `boundary` at head defaults to open (docs/ENGINE.md, the
per-axis topology): a declaration of the world file and of the engine as built,
aligned by the engine's writer, not by this document.
The owner-approved run parameter selects open or periodic topology independently
per axis; open is the default (history, superseded on 2026-09-23 by ALGEBRA.md 1.6
and the owner's word, record 1421). The exact schema, one-interval Link transfer,
extent-one return, unchanged carried momentum and mixed-axis refusal rules are
in [the engine contract](docs/ENGINE.md#per-axis-gameboard-topology-2026-09-19-implementation-amendment)
(DECLARATION: the world file's keys `shape` and `boundary`, ALGEBRA.md 1.6; the
engine's refusals are the engine's).
This choice does not change a local contact law or establish equivalence between
a thin periodic GameBoard and full 3D matter. Earlier topology descriptions below
belong to their dated models, not an implicit events-world default.


## Initialization-defined model (history: deleted on 2026-09-19)

History marker (2026-09-19): the generic disturbance simulator this section
describes was deleted on 2026-09-19 with the engines before the Beam Law
([migration](docs/MIGRATION.md#one-engine-on-2026-09-19-the-old-engine-deleted));
the active contract is [the Beam Law](docs/BEAM_LAW.md) with
[the engine's bookkeeping](docs/ENGINE.md) and its algebra
[docs/ALGEBRA.md](docs/ALGEBRA.md). The text is kept as written.

The canonical Detector-owned sampling contract
allows draws only at an actual external Detector encounter. Ordinary evolution
is deterministic. The earlier autonomous lottery, bond and contact descriptions
below are historical: the `historical-autonomous-v1` research profile, the
lottery capture and the bond registry were deleted on 2026-09-17 (issue #164,
bucket B.5), and the text is kept with that date, not renumbered.

The opt-in bounded rational candidate preserves
finite integer state while representing fractional quantities in explicitly
configured whole/remainder/denominator fields. Its larger finite intermediate
registers, balanced neighbor selection and exact fractional clock are named
choices. They do not establish isotropic light propagation or electromagnetic
energy. The six-neighbor causal boundary remains binding.

The active model treats physical content as configured disturbances carrying
named fields. The engine supplies integer local updates, causal transport,
conservation enforcement and scheduling; initialization supplies identities and
candidate laws. It does not infer familiar physics from names.

All interactions use generic definitions. A configured local pair transaction
may transform several fields together only when its declared invariants and
conserved pair totals hold exactly. Existing elastic-collision formulas remain
explicit reference benchmarks; reproducing them does not mean they emerged from
a computational field. New emergence experiments must use simple local vector
operations to produce states, not supplied continuum force or collision formulas.
Guards and conservation diagnostics validate proposals without replacing this
elementary rule. See physical entities and the example in
DISTURBANCES.md.

The optional bounded conversion also permits two
local records to become two explicitly configured output types under the same
atomic conservation checks. This is a supplied transformation, not evidence of
emergent annihilation. Executable entity profiles
describe bounded representations; physical identity and dynamics cannot be
inferred solely from the ability to store or transport their registers.

The user-defined cost of a local cycle sets a general node delay above the
normal cost. Neighbor transit is fixed, and no computation debt accumulates
between cycles. The exact schema, exchange, timing and source rules are in
the disturbance contract.

The optional outward spatial-field candidate separates
source records from the fields they emit. By default its field transport uses a fixed
clock; priced field work contributes to new local carrier cycles while field
forwarding continues at causal link speed. Schema 1 preserves conservative
transport. Schema 2 explicitly selects finite attenuation, `finite-localizing-v1` by default: finite source
and response allowances bound dynamic input, and declared integer attenuation
removes magnitude at interior arrivals while exempting immutable background.
The explicit dissipate option tracks signed loss; neither option establishes physical
momentum through decay. Self-field exclusion by arrival order remains an unverified
hypothesis and is not enabled by this extension. For straight-ray fields an
optional local one-link exclusion exists: a departing emitter subtracts the rays
of its own departure cycle from the flux it samples on arrival, using only its
own registers; returning self-field at any other distance is not excluded.

Two explicit opt-in policies now
exist for the generic engine, described in spatial couplings:
`field_phase_first` completes every field link before carriers sample, so an
emitter's own field is one link ahead on every free-space path; `arrival_port_blind`
keeps the default clock and lets an arriving carrier ignore, for that one sample,
the travel port it came in on, so straight paths are self-blind while maximum-speed
corners still coarrive. Both pass isolated-source and external-source controls;
neither uses source identity, and neither is a derived physical law.

The opt-in shared computation cycle applies
the same budget delay to all local fields and carriers. It freezes updates and
directional departures together; later input belongs to the next cycle.
The integer link transit remains fixed. This alternative timing candidate is
selected with `spatial_computation_delay`; existing inputs keep the default.

The optional spatial response candidate can turn a
configured vector while preserving its length exactly, transferring the opposite
vector change to the same spatial field. This is an integer quarter-turn law;
it does not infer physical names, continuous angles or energy conservation.
Straight cardinal self flux is parallel to its carrier and cannot turn that
vector under the flux-driven law. Turns, periodic return and other coupling
laws require separate self-interaction analysis.

The optional local field-rule framework treats a
location as a node with six directional connections. Several scalar/vector
components can evolve together from local state and received information, with
explicit retained and outgoing amounts. Joint field/carrier transactions must
pass declared balances before both owners commit; delayed transactions cannot
overwrite intervening field evolution. A logical group of two vectors does not
itself identify an electromagnetic field or supply a photon. Known physical laws
remain independent acceptance targets. A historical benchmark that explicitly
inserts them is not an emergence experiment. This extension is a research
interface, not evidence of their emergence.

Initialization independently chooses periodic or open boundaries. Periodic space
connects opposite faces on each of X, Y and Z without changing a carried direction.
An open terminal link instead removes the original packet after its full transit
time and records the escaped quantities. No exterior node or exterior decay is
simulated. Being spatially closed does not cancel a separately configured decay.

Sections 1–5 and 10–11 state shared locality, arithmetic and evidence principles.
Sections 6–9 document the source, self-force, momentum and turning requirements
of the explicitly selected historical research models; they are not implicit
laws of every configured disturbance. Sections 13 and 15 likewise belong to
named historical candidates. Section 14 described the shared quantum query
assumption; its implementation and the model law were deleted on 2026-09-17
with Highlights section 3.18 (section 23). Section 23 states the
ray-event model adopted as the target direction on 2026-09-17, with
implementation pending. Section 25 states the law of the bit of 2026-09-18,
which supersedes the sentences of sections 3, 4, 6, 9, 10, 22, 23 and 24 that
it names. Section 16 explicitly
selects its native local-cycle integration without changing unselected worlds.
Section 25 was superseded on 2026-09-19 by the law of the ray (ALGEBRA.md chapter
2), and every section is read against ALGEBRA.md by the table of
docs/designs/detector_law/POSTULATES_BY_ALGEBRA.md (2026-09-23).

For a configured law claiming energy and momentum conservation, account for the
fields and disturbances together at every local event. The combined node change
must match actual incoming and outgoing flux. An internal exchange must balance the
participants' energy changes and all three momentum changes at that node;
external sources and losses must be distinguished from closed transfers.
The local conservation contract defines the optional
read-only audit and its supported ownership boundaries. It measures declared
quantities without repairing state, choosing laws or adding model-time cost
(history: the scalar candidate's audit, deleted on 2026-09-17; the books in force
are ALGEBRA.md 4.3).
Locality, a passing component ledger and catalog properties alone do not establish
physical energy, momentum or an emergent field law.

## 1. The world consists of locations and events

Space is divided into three-dimensional nodes with six directional connections:
right, left, forward, backward, up and down. A connection reaches one nearest
neighbor, or exits the simulated domain at an explicitly open boundary.

An event is a wall crossed by an accumulator of the state vector at a Node: a Link
crossed, a phase step taken, a count completed, a birth, a push, and the click that
ends a record; nothing else happens (ALGEBRA.md chapter 2, the one central
formula; 3.1). An event is a local change in a node at a particular time: a field update, a particle
momentum change, a move to a neighbor or a blocked move attempt (history,
superseded on 2026-09-23 by ALGEBRA.md chapter 2).

(History, marked 2026-09-23: the ray-event model of 2026-09-17 in the next
paragraph was superseded on 2026-09-19 by the law of the ray and on 2026-09-23 by
ALGEBRA.md chapter 2; the implementation the paragraph calls current was deleted
on 2026-09-19.)

Adopted direction (model owner, 2026-09-17; implementation pending, see
[section 23](#23-the-ray-event-model)): an event is a change of trajectory
leaving an interaction, a new straight line through one Port. A ray is the
trajectory of one event between two interactions, and a node that a ray
merely crosses hosts no event. The definition above
describes the current implementation; the ray-event definition is the target
every future profile is measured against.

Every physical name is the name of an element of the algebra's structure
(ALGEBRA.md 1.2, the dictionary): the mass a body's content M, gravity the first
column, momentum the label; the masses and the charges are declared inputs;
Newton's, Einstein's, Lorentz's and Bohr's forms are reached under named
hypotheses (chapter 5) and are the things compared with, never inserted and never
called emergent. The simulator does not assume every familiar physical phenomenon is fundamental.
Mass, gravity, curvature or a known particle can count as an emergent result only
if they arise from local events and laws, rather than being inserted under another name
(history, superseded on 2026-09-23 by ALGEBRA.md 1.2).

## 2. Every location has only bounded local information

A physical node does not store a picture of the entire universe. It stores a fixed
amount of information and reads its own state and information already delivered
by its six neighbors. The shared quantum query primitive of section 14 was
deleted on 2026-09-17; there is no read beyond the six neighbors.

Local disturbance capacity is fixed in advance. A node has no list that grows with the
number of sources in the universe and does not retain its entire history.

Physical work per local update is therefore bounded and constant. Total host
runtime for a large world is not constant: all active locations still require updates.

This includes estimating or subtracting a particle's own field. A second simulated
world or a search through source histories cannot supply a physical input merely
because its final subtraction happens in one node. LOCALITY-1 in the definitions
document specifies this end-to-end rule and its test/reference boundary.

## 3. Consistency is maintained locally and causally

Each location must be consistent with all information that could already have
reached it. It need not know about a distant event before information arrives.

There is no instantaneous update of the whole universe or central repair of all
space. An event first changes its own location. Its influence travels from neighbor
to neighbor, and each location updates upon receipt under the same local law.
There is no host-computation exception: the oracle of section 14 was deleted
on 2026-09-17. The one exception is the completion of a record read at more than
one detector: the pair's gather, one gather of one record from both settings, the
law's one non-local operation and the host's (ALGEBRA.md 3.1, 3.4); no Node reads
it.

Global consistency emerges from consistent local updates. New information does
not rewrite completed events; it becomes causal input to future events.

**Contract of the generic disturbance simulator (history: deleted on
2026-09-19; the active contract is [the Beam Law](docs/BEAM_LAW.md)):**
disturbance transfers cross one neighbor link after its fixed transit time;
updates use already available local records. Extra node delay can make
propagation slower. There is no global correction at the end of a tick.

Established in the algebra: entanglement is a record of tensor rank 2 carried by
local verbs on two arms and read by one gather at two clicks (ALGEBRA.md 3.6);
the marginals are no-signalling exactly and the Bell value an exact rational of
N, met by series L and L6 (DETECTOR) (4.9, 4.10); the one failure is the order
channel, a RULE the law lacks (chapter 6, row 1c). **Not established:** that these local laws suffice for every kind of physical
consistency, particularly quantum consistency and entanglement (history,
superseded on 2026-09-23 by ALGEBRA.md 3.6, 4.9 and 4.10).

(History, marked 2026-09-23: the Node's law of 2026-09-17 in the next paragraph
and its amendment of 2026-09-18 were superseded on 2026-09-19 by the law of the
ray, ALGEBRA.md chapter 2 and 2.11; the clause that the marks are declarations of
the world file and never physics stands, ALGEBRA.md 3.4.)

Addition (model owner, 2026-09-17; Highlights 5.2, "the Node's law in five
steps"): under the ray-event model of section 23 the same local law is
this. A node knows nothing about electrons or stars; it is a switchboard
with six Ports, six output clocks and a table to read. Each interval: (1)
receive what arrived on the six Ports, with what is resident (a bound
group); (2) apply its mark, if any: a Detector draws once per arrival, 0
returned and 1 continued; an external body absorbs into its sink and
radiates by its amount; (3) meet by table, layer by layer: families with no
declared coupling cross as if alone, families with one produce the outputs
the table says, with exact invariants and the remainder placed by
Highlights 3.17; (4) stamp every output as a new event ray, with its
event's Ports, shares and steps 0; (5) depart, each ray through its Port
when that face's clock is ready. The two marks, the Detector and the
external body, are the whole apparatus of a world: they are the only places
where the GameBoard does something the tables do not say, and both are
declarations in the initial file, never physics. Since 2026-09-18 (section
25): a node has no output clocks and no departure waits for one, the one
wait being the tick a thing pays per whole quantum it reads; a mark draws
nothing, it absorbs a thing and returns a shadow; the shadows of one owner
are mixed among the six Ports and a shadow meeting a thing is a push and a
return; the tables of step (3) stand for a thing meeting a thing.

## 4. There is a maximum causal speed

Physical influence cannot skip nodes. It travels at most one neighboring node per
elementary step. This is the role of c: the maximum propagation speed of causal
influence in the simulator.

Adopted direction (model owner, 2026-09-17): the bound has no exception. The
joint outcome of a pair travels on the returning ray itself, one Link per
step, back to the birth event and on to the partner ray
([section 23](#23-the-ray-event-model)) (history: the returning ray of
2026-09-17; superseded on 2026-09-19 by the law of the ray; the pair's click is one
gather, ALGEBRA.md 3.6). The registry exception described in
the next paragraph is withdrawn as a model law; the `bonded-ray-field-v1`
profile that implemented it was deleted on 2026-09-17 (issue #164, bucket
B.5), and its measurements stand in the validation log as evidence about that
profile, not for the current model. Highlights section 3.18, which described
the shared resource, was deleted on 2026-09-17.

Historical (withdrawn as a model law on 2026-09-17; the shared quantum resource
of Highlights section 3.18 and the bond registry described here were deleted
the same day, issue #164 buckets B.1 and B.5): the bound was split in two, as the experiments split it. Energy, momentum,
matter and every message that a record can control move at most one Node per
step, without exception. The joint outcome of a bonded pair, two rays emitted
together, is the one thing that does not: each ray carries the Node and tick
of its birth through the GameBoard at link speed, and when either end is
measured, the bond registry answers for both ends at once, at any distance (the
bonded ray field).
That answer carries no energy, no momentum and no message: each end alone sees
an even coin whatever the other end does, which the Bell probe measures as
plus rates that do not move with the other side's setting, not a consequence
of the answer carrying no energy. It is the correlation Bell's test measures
beyond the local bound, and nothing else. In Bell's terms the registry is a
deterministic, measurement-independent, parameter-dependent model: the end
that answers second reads the first end's setting, which the
causal probe (`examples/bell-chsh/`, deleted on 2026-09-17)
measured as an outcome that moves with the other end's setting at fixed
hidden variable. It is a nonlocal resource, not a local explanation of the
Bell value, and the unmoved plus rates are no-signalling, not locality. The
registry keeps a bounded bank of
open pairs, one identity per pair from its birth Node and tick, releases a
pair at its second answer, and answers a repeated question the same way, so
it is bounded and idempotent like every other owner. A world with no bonded
field has no exception at all.

A particle can also move at most one neighbor per step. The same movement law
applies at all speeds; there are no separate low-speed and high-speed laws.

The pace of every direction is c_D = Q abs(D)_2 / T_D Links per interval (Q the
label's scale, D the direction, T_D its flight period), within 1 / T_D of 1 /
sqrt 3, the flight operator's norm (ALGEBRA.md 4.2); c is not chosen (1.3, item
5); that a row's flight is free of dispersion is the declared postulate P9 and
not a theorem of the six verbs (4.14). (Re-read on 2.11's landing: under the
derived law c is the rule's own, from three inputs, PUSH_BALANCE.md 12.6 (a)
and MASSIVE_RECORD.md 1.1 on the branch detector-law-design.)
A ray on the Euclidean pace waits at a Node for part of its journey so that
every heading covers the same Euclidean distance per step. Waiting is slower,
never faster: the bound holds for every heading, and the GameBoard metric is a
configured choice, not a derivation (the last clause: history, superseded on
2026-09-23 by ALGEBRA.md 4.2 and 4.14).

Addition (model owner, 2026-09-17; Highlights 3.28, "speed is a clock
slowing"): everything on the GameBoard moves at one Link per interval, and
there is no other speed in the engine. Matter is slower only because the
output clock of its bound group delays its departures: a group that moves
one Link every k intervals has speed 1/k in units of c, and light, with
delay 0, has c. Three things slow a clock, and all three are content
meeting content by a declared table: the content retained at the node
itself (the group's own mass), the field of another mass that a ray meets
(gravity as bending by delay, section 23), and a declared interaction whose
output assigns a delay (binding among them). Nothing slows a clock because
of motion: there is no kinematic rule, and the slower ticking of a moving
group, if it appears, must emerge from its rays spending intervals on Links
instead of resident
([hypothesis 15](docs/HYPOTHESES.md#15-time-dilation-from-transit-a-moving-bound-groups-clock-runs-at-1--v),
experiment A14 of [docs/EXPERIMENTS.md](docs/EXPERIMENTS.md)). Mass, time
dilation and gravity are therefore one bookkeeping of integer delays read
from different tables, and the tables, not the engine, are what the
confrontation runs test. Superseded on 2026-09-18 (section 25; Highlights
5.4, points 9, 21 and 23): every ray moves one Link per interval and a thing
delays nothing; no output clock delays a departure, and the only wait is
the tick a thing pays for every whole quantum it reads. (And on 2026-09-19 by the
law of the ray, ALGEBRA.md 2.1, the drive.)

Addition (decided by the orchestrator on the model owner's delegation,
2026-09-17; Highlights 3.28, "the phase circle stays small"): a family's
phase is read only at a meeting and only as a difference, so its width
`phase_bits` is the family's choice of the resolution its couplings need,
eight steps resolving the Born table and a wider circle allowed but never
required. The delay a field ray lays on the ray it meets is carried in a
lag register with its own declared modulus, spent as one Link toward the
lagging side when it reaches that modulus, exactly as a heading is carried
with a resolution of one part in 2^30 through six Ports; that modulus, not
the phase circle, is the N of hypothesis 14 of
[docs/HYPOTHESES.md](docs/HYPOTHESES.md), and it may be of any width
because it enters no phase sum. The weakness of gravity therefore lives in
a register, not in the phase, and nothing on the road to the confrontation
runs needs a wide phase. The lag register is retired on 2026-09-18 with the
word register (Highlights 5.4, point 22) and the delay with point 21; N, the
phase width, is the one input behind interference, and the Born table is
computed from it (point 17).

## 5. Physical calculations use integers only

Every value affecting simulation evolution is an integer: position, time, field,
momentum, counter and remainder.

Core calculations contain no floating-point values, trigonometry, roots or vector
normalization, with two declared exceptions on main: the run-time roots under the
keys `meeting` and `optical` (ALGEBRA.md 2.7, the seventh verb, not admitted to
the law, each declared by its design), and the cosine and sine tables at the
scale 256 formed at load, a declared rounding (2.5). Conservation-preserving division retains the missing fraction as
an integer remainder carried into the next calculation.

(History, marked 2026-09-23: the finite-attenuation candidate of the next
paragraph was deleted on 2026-09-17; the law's one division is ALGEBRA.md 2.6.)

Schema 2 finite attenuation changes each packet/octant/component reaching an
interior receiver from `v` to `sign(v) * floor(abs(v) * p / q)`, with integer
`0 <= p < q`. Signed inventory is preserved: by default the removed signed quantity is
deposited as stationary stock at the receiving node, so total inventory is
preserved and a thinning wave ends as whole units at known nodes rather than
fading to nothing. The explicitly selected `"residue": "dissipate"` candidate is
the historical exception: it records the removed quantity as loss, not saved in
a remainder, and makes integer dynamic fields vanish after their last input. The
immutable background is exempt in both cases. It can change a vector's direction and does not
preserve momentum or energy. It does not alter conservative splitting, fractional
source requests or the historical models' remainder rules. See
the finite field contract.

Numbers have fixed bounds. An out-of-range calculation stops the run with an error
rather than hiding overflow or distorting the result.

Displays, the host's diagnostics (GAMEBOARD readings) and the conversions of
counts into Outside numbers (CONVERSION) may use floating-point values, provided
none feeds back; a measurement is a detector's click, an integer event of the law
(ALGEBRA.md 3.1, 3.2). Display and measurement code may use floating-point values, provided none of its
results feed back into the simulation (history, superseded on 2026-09-23 by
ALGEBRA.md 3.1).

## 6. A resident source remains a source

A body at rest releases at every self-creation of its own count, by its family's
declared release per unit of content (ALGEBRA.md 2.1, the release; 5.6 (a) and
(e)); the tick is GAMEBOARD and no rule of the body reads it (3.1). A particle occupying a node remains a source every tick even without moving.
Its presence in that node represents the source (history, superseded on
2026-09-23 by ALGEBRA.md 2.1 and 5.6).

The simulator does not repeatedly add a source's own new emission to itself.
A stationary source should form a persistent surrounding state, rather than grow
without bound or disappear because there was no movement event.

Addition (model owner, 2026-09-17; Highlights 3.5, "the release does not
wait for the clock"): under the ray-event model of section 23 a field
release is information, not a departure of matter. Every interval, the
content resident at a node says in all six headings that it is there, with
the strength its amount gives, and this is booked as a source; the node's
output clock delays only what leaves it as matter, never its field. So a
heavy node radiates every interval, its field is static and its strength
grows with its content, as a mass at rest should; if the clock slowed the
field too, a heavier body would radiate less. The engine's reading of the
no-self-field rule (2026-09-17): a traveling ray releases in the five
headings other than its own, because at one Link per interval a forward
field ray would share its packet at every step, so the forward field of a
ray at the speed of light is the ray itself; resident content releases in
all six. On the GameBoard the field spreads as a diamond at the scale of
Links and as a sphere at large scale, because the number of paths to a node
after k steps is the multinomial count, which is rotationally symmetric to
leading order; whether the bending of a passing ray is the same on an axis
and on a diagonal is a measurable prediction (experiment A6 of
[docs/EXPERIMENTS.md](docs/EXPERIMENTS.md)), not an assumption. Superseded
on 2026-09-18 (section 25; Highlights 5.4, "A thing does not emit"): a
thing does not release shadows interval after interval; its shadows are
given with the GameBoard and circulate, booked as initial content and never
sourced. (And on 2026-09-19 by the law of the ray, ALGEBRA.md chapter 2.)

Addition (model owner, 2026-09-17; Highlights 3.5, "light is the field, and
the field spreads"): light and the field of a charge are one family of the
catalog, the electromagnetic field in ray form; a photon is one quantum of a
field ray, an emission is a release of that family at an event, and an
absorption is a meeting of a field ray with a bound group. Because light
spreads, the field spreads by the same rule: every node that field content
reaches releases it again in all six headings by a declared split table of
the family, the backward heading included, the remainder owned (Highlights
3.17). Field content meeting at a node combines by phase before it spreads;
a single quantum cannot split, and where the table would give a heading less
than one the remainder leaves whole through the heading the phase selects,
so a quantum never waits and only a Detector decides where it is realized.
The field of a static charge then fills space, the net momentum through a
node falling as 1/r² (Gauss), and diffraction needs no rule of its own, a
wall being a body that absorbs. This is one catalog entry of the light
family, not an engine mechanism: feature 12, field spreading, of the
ray-event model, its cost measured before adoption; until it lands the field
lives on the six axis lines of its source and light goes straight.
Superseded on 2026-09-18 (section 25): there is no field family, a shadow
is a ray of its owner's family with bit 0 and light emitted at an event is
a thing of the light family (Highlights 5.4, point 12); the split table is
superseded by the node's mixing (point 24), and the remainder is a shadow
parked at the node (point 22). (And on 2026-09-19 by the law of the ray,
ALGEBRA.md chapter 2.)

Addition (model owner, 2026-09-17; Highlights 3.5, "the field is matter's
message about itself"): a field ray says "I am here", from which heading,
how much, at what phase and with which sign of charge, and what happens to
the ray that meets it is that ray's own table reading the message, so a
force is how a ray reads the message of another; the message tells where
its source was r intervals ago, since it travels at the causal speed, and
it is not free, every field ray carrying momentum and its source paying
the recoil. A field ray is a ray with an empty event record, rest rate 0
and charge 0, and nothing else, which is why it merges by family and phase
and spreads and why nothing in the engine knows what a field is. The sign
of the source's charge travels on the field ray as a visible property,
like the Detector's bit, read by the coupling that meets it and never
encoded in the phase, which is reserved for interference; feature 12
carries it, and the catalog's open entry on the attraction of opposite
charges closes with it (experiment A5). Since 2026-09-18 the message is the
shadow: it carries its owner's identity, charge and content, is read by
content or by charge (Highlights 5.4, point 16), has no mass and no clock,
and returns as a field (point 3). (And on 2026-09-19 by the law of the ray,
ALGEBRA.md chapter 2; the push in force is the bilinear form, 2.2.)

## 7. An isolated symmetric source does not push itself

For a single stationary source in symmetric space, field values on opposite sides
of every axis must be equal. Opposite influences cancel, leaving its momentum unchanged.

This is a fundamental local-consistency test: a particle must not start moving
solely because of its own symmetric field.

(History, marked 2026-09-23: the candidates and tests named in the next
paragraph were deleted on 2026-09-17.)

For an accepted free-motion candidate, this requirement also applies to moving
isolated particles: their momentum and impulse remainders must not change due
to their own field. Baseline failures remain evidence, not approved corrections.
The generic engine's default clock fails this requirement for a value-driven
exchange response: a carrier and the field it emits in its departure interval
cross one link together, and `tests/test_field_phase_first.py` (deleted on 2026-09-17) records that
baseline. The opt-in `field_phase_first` and `arrival_port_blind` policies in
spatial couplings satisfy
it for straight motion by ordering alone; the flux-driven rotation law satisfies
it under the default clock by geometry, as `tests/test_rotation_self_interaction.py` (deleted on 2026-09-17)
shows. None of these selects a self-force law under acceleration.
The historical `causal-octant-stream-v1` candidate, deleted on 2026-09-17, tested
this through outward one-link transport before the particle response, with no
source identity or subtraction. Its free-space guarantee ended at periodic return,
which is a boundary effect requiring separate evidence. Its fixed state and limits
remain recorded in `SIMULATOR_DEFINITIONS.md`.

## 8. Momentum is exchanged at the event location

For a paid family the label leaves the emitter at the birth (the recoil) and
enters the reader at the click, so the third law holds message by message and
the books balance at every tick; for a free family the release costs no recoil
and the third law is a symmetry between two readers at rest, not shown in motion
(ALGEBRA.md 5.6 (f); 4.3). When a particle receives a momentum change, the field receives an equal and
opposite change in the same event. Both sides are validated before committing
(history, superseded on 2026-09-23 by ALGEBRA.md 5.6 (f)).

Never calculate missing momentum at the end of a run and distribute a correction
throughout the universe. The books' total momentum is a GAMEBOARD reading of
the ledger, a check that the books balance (ALGEBRA.md 4.3), never a measurement
(3.2). Total momentum is a measurement for validation only (history, superseded
on 2026-09-23 by ALGEBRA.md 3.2 and 4.3).

The books are exact at every tick in amount and content, and in momentum for
every paid message (ALGEBRA.md 4.3); a click's content is E = h s, the
release's identity (h the action per Link, s the lamp's turn; 4.11); a body's
energy of motion is not on the law (E = E_0 at every speed, 5.3, the FAIL rows
4a and 4b), reached only under the identity covariant-readings-v1 beside the
law (5.10). (Re-read on 2.11's landing: a body's energy of motion under the
massive record kind is its dispersion and its conserved form I,
MASSIVE_RECORD.md sections 2, 3 and 9 on the branch detector-law-design.)
**Open:** energy conservation has not been established, and there is no complete
law for transporting field momentum between locations (history, superseded on
2026-09-23 by ALGEBRA.md 4.3, 4.11 and 5.3).

## 9. Field and turning laws are hypotheses under test

The historical scalar field law uses six neighbors, the local source and a retained
remainder. A turning law lets transverse field imbalance change motion direction.

These are **candidate laws**. They are not called gravity and do not establish
Newton's or Einstein's equations (the law's own column is named gravity by the
dictionary, ALGEBRA.md 1.2, and Newton's form is the thing it is compared with,
5.6). A successful experiment describes the tested
conditions only.

Introduce another law as a separate candidate and compare results. Do not change
old tests merely to make a new law appear successful.

Addition (model owner, 2026-09-17; Highlights 5.5, "the constants: what is
derived and what is an input"): mass ratios are derivable, the ladder of
hypothesis 12 being the set of loop-closing contents under the catalog's
binding table, which experiment A10 counts against the known spectrum, the
proton-to-electron ratio first; the strength of the electric coupling and
the strength of gravity are inputs today, the release ratio n/d of a field
family and the modulus N of the lag register (Highlights 3.28) being
declared widths, so hypothesis 14's G = ħc/(N m₀)² is a reparametrization
until something fixes N, as the Born table's ratios are until something
fixes n/d; hypotheses 16 (what fixes the lag modulus: the top of the mass
ladder, the resolution the spreading field needs, or nothing) and 17 (what
fixes the release ratio and the table: the symmetry of Highlights 3.27 and
the path counting of 3.5, or nothing) record the question, and until they
are answered the model predicts forms, 1/N² and 1/r², and not the values
of G and α. (2026-09-18: the field family is retired, the ratio being the
size of a family's shadow set; the lag register is retired with the word
register; the Born table is computed from the phase width N, Highlights 5.4,
point 17; what fixes G stays hypothesis 16's question.) (Superseded on 2026-09-20, the model owner on issue #369, Highlights 5.4 and the log's record 106: mass ratios are not derivable in this law; the masses and the charges are the initialisation, the catalog's declared contents and charge per unit; the ladder and A10's count are closed by decision; the strengths of the couplings stay inputs.)

## 10. Measurement and display are outside the physics

Addition (the model owner, 2026-09-23, record 1421, on the algebra): a
measurement is a detector's click, an action of the law on the state
(ALGEBRA.md 3.1; the model owner, record 1139): a record is read at a detector
by the evaluation E of the detector's own record in the detector's own clock
(2.5, the evaluation at the roots of unity; the weight the norm f^T **G** f, f
the record's element of the group ring and **G** the click's Gram matrix), the
click stamped with the detector's own count n_D (3.1, 3.2); a light record ends
only where a take is declared, in the absorbing worlds (a screen, a sponge),
and a clock body takes nothing: the record passes on and is read again (the
model owner, 2026-09-23, record 1421); the flight of every other record is
untouched; nothing else measures. The click is the one deletion of the interval
(4.7) and, read at several detectors, the one non-local step (3.1). Displays
and the host's diagnostics are outside the physics and only read (3.2).

Addition (the model owner, 2026-09-23, record 1139, the Boss's translation:
"the detector does not only read; when it reads it performs an action; it
must perform an action in the reading, and that is the whole point; that is
what explains that a detector changes the outcome; we know this, it is a
clear assumption from experiments"): the title and the first paragraph below
are read as follows. Displays and the host's diagnostics are outside the
physics and only read. A measurement is a detector's click, an action of the
law: the absorption of the record at the mark, its content into the
detector's record, the click stamped with the detector's own count (`clock`
under the world key `clock_stamp`; the count itself advances at every
self-creation, engine.py line 706, click or none); it is the one interaction
that is a measurement. A detector changes what it reads, as nature's
which-path experiments show (the thing compared with); the law carries that
as the click's rule and no more: the record ends at the detector, its
content moves, the flight of every other row is untouched (no back-action);
nothing else measures. In the code the click is the `measure` rule of step
4, `nature_beam._measure` (nature_beam.py line 5677; the `click` line
written at line 5536 with the units, the content and the label moved into
the measured event's record), the record's completion
`nature_beam.gather_records` (line 6537), and the detector's own count
`entry.age += 1` in `engine._frame_all` (engine.py line 706). The sentence
"measurement means diagnostics, not a quantum interaction" in the first
paragraph is superseded by this addition and kept as history. (This addition
of record 1139 as worded, the absorption of the record at the mark and the code
lines: history, superseded on 2026-09-23 by ALGEBRA.md 2.5 and 3.1 and the owner's
word of record 1421, the addition above; the code lines are the engine as built.)

Trajectories, reports, images and HTML only read run results. They neither direct
particle motion nor repair the field. Here measurement means diagnostics, not a
quantum interaction that creates a new physical record (history, superseded by
the additions above and by ALGEBRA.md 3.1).

Every application run saves initial conditions, parameters, code identity and
completion or failure evidence. Runs and ordinary tests are headless. Only an
explicit visualization request adds frame capture and a visual artifact identifying
its displayed quantity and geometry. A slice does not change the underlying 3D world.
(HOST: a rule of the machine, not of the law.)

The apparatus of a world (a detector, a lamp, an external body; since
2026-09-23 one generic detector-emitter, a receiver-inserter, Highlights 5.4,
record 1327) is a declaration of the world file, the Outside, never physics
(ALGEBRA.md 3.4); nothing draws (2.7); the click is the one measurement (3.1),
in the form of the addition of record 1421 above.

Addition (model owner, 2026-09-17; Highlights 5.2): inside the physics, the
two marks of a world, the Detector and the external body (section 23,
Highlights 3.19), are its whole apparatus: they are the only places where
the GameBoard does something the tables do not say, and both are declarations
in the initial file, never physics. The Detector's draw is the one
measurement that is an interaction; the diagnostics of this section stay
outside the physics as before. Since 2026-09-18 nothing draws (section 25,
point 14): the measurement is the absorption of a thing at a mark. (The draw and
the absorption: history, superseded on 2026-09-19 by the law of the ray and on
2026-09-23 by ALGEBRA.md 3.1 and the owner's word of record 1421.)

## 11. A result must pass tests to be considered reliable

A phenomenon seen once in an animation is not a general model result. Check that it:

- is not a bug, an accidental update-order effect or a display artifact;
- persists under the translations, reflections and coordinate-plane changes tested;
- obeys local rules and numerical bounds;
- repeats from documented initial conditions;
- passes checks that were not used to construct the law.

Failure is information about the model. Do not add a special correction just to hide it.

(History, marked 2026-09-23: the octant, straight-ray, signed-quanta and
phased-ray candidates of the next paragraph were deleted on 2026-09-17; de
Broglie's fringe is ALGEBRA.md 5.7 under massive-rows-v1, 5.10.)

The outward octant candidate conserves flux through every closed shell but
concentrates it near body diagonals. The straight-ray candidate keeps the same
shell conservation and makes the time-averaged flux follow solid angle in every
direction, because each ray carries its own heading and phase and never spreads.
Signed quanta are the attraction hypothesis under test: a source emits negative
quanta paid into its own stock, a body absorbs a share proportional to its mass
and pays for the momentum it gains toward the source. Energy and momentum stay
exact at every event; no gravitational constant is derived, and a source's stock
rises by what it emits. Kerengonen phased rays are the interference hypothesis:
a ray carries a phase that advances per link, rays that meet combine by phase,
and the coherence gates what is absorbed and sampled while every quantum stays
whole and accounted for. Quanta that cancel continue; whether that is the right
place for them is the question the candidate is meant to test. A ray's advance
per link may come from its emitter's momentum, `|p| / D`, the de Broglie
hypothesis: measured as a fringe period inverse to momentum, not derived.

A record lands whole at one detector: one click per record, the ladder choosing
one cell and deleting the offers, the completion the host's one non-local step
and no signal on the board (ALGEBRA.md 3.1, 4.12); the fringes follow the
Euclidean path difference, C(y) / W as 5.7 gives it (C(y) the count at the
pixel y over W births); a mirror's reflections are the 48's, the signed
permutations of the axes (1.1). (The next paragraph: history, the ray candidate
of 2026-09-14 to 2026-09-17, superseded on 2026-09-23 by ALGEBRA.md 3.1, 4.12
and 5.7.)

Three limits of the ray were tested rather than assumed. A single particle
dissolved into rays lands where its wave is absorbed, spread over the screen;
it cannot land whole at one Node, because each ray carries conserved stock at
link speed and no local rule can retire the other rays when one is captured
without a signal faster than the rays themselves, which postulate 4 forbids.
Whole landing needs either inventory that a domain owns rather than rays
carry, as the quantum layer keeps it, or matter rays slower than the causal
speed with a retirement that travels at that speed. A mirror can reflect
across a GameBoard axis or a GameBoard diagonal, and a fraction makes it partial;
an arbitrary angle needs a heading map beyond a signed permutation. The
fringe follows Manhattan path difference on the links metric and Euclidean
path difference on the Euclidean pace: the metric is a configured choice
under test, with every quantum still counted whole.

Historical (the claim-and-gather rule was deleted on 2026-09-17, issue #164
bucket B.5; under Highlights 3.20 the return travels on the ray itself and no
Node keeps a register): the whole landing was then built by the second route,
claim and gather: a
matter wave slower than link speed, and a claim that spreads from the
capturing Node at link speed, Node to Node, each Node remembering the port it
came from. Rays of the claimed train that meet the claim turn homeward along
those ports, and the capturing record takes them whole. The wave becomes one
particle at one known place, but not at once: the rest arrives over the ticks
the claim and the return take, and until it does the particle is a claim plus
matter in transit, all counted. Where two captures race, the earlier one wins
when their claims meet and the later keeps only what it took first. This is
the hypothesis under test for postulate 12's open question: a local,
causal, exactly counted collapse, whose measured signature is a landing that
takes time.

## 12. Quantum behavior and entanglement remain open

(The title: history, superseded on 2026-09-23 by ALGEBRA.md 4.9 to 4.12; the
closing paragraph of this section states what is reached and what is not.)

The physical core describes discrete fields and particles. The selected quantum
candidate was a deferred event network: a saved joint state plus local operations
and immutable outcome records defined the wave without evaluating it every tick,
and an explicit query followed the required past dependencies and evaluated
forward. That bounded finite-state model, with the earlier scalar-amplitude and
terminal-trial interfaces, was deleted on 2026-09-17 (section 23): the Detector
of Highlights 3.19 and the returning ray of 3.20 replace it (and the returning ray
was superseded on 2026-09-19 by the law of the ray; the pair's click is one
gather, ALGEBRA.md 3.6).

The law's joint results are the pair's record of tensor rank 2 read by one gather
(ALGEBRA.md 3.6); the marginals are no-signalling exactly (4.9); the one signal
is in the order of the clicks, a RULE the law lacks (chapter 6, row 1c). A future full quantum layer must preserve both consistent joint results and the
inability to use those correlations to send information faster than c (history,
superseded on 2026-09-23 by ALGEBRA.md 3.6, 4.9 and 4.10).

Historical (measured on 2026-09-14; the Bell probe, the lottery capture and
the bonded ray field were deleted on 2026-09-17, issue #164 bucket B.5, and
the numbers stay in the validation log): the ray was put to Bell's test. Two
rays from one Node share a hidden phase,
each side's detector takes its ray with the coherence of that phase against a
local reference (Malus's law on the Kerengonen coherence), and the
CHSH probe (`examples/bell-chsh/`) measured the correlations. The
result is what a local model must give: S near the value the two independent
lotteries predict, below the local bound 2, and far from the quantum 2 sqrt 2.
The ray explains the shared origin, the no-signaling and the collapse's
timing; it cannot explain the correlations beyond the bound, and no local
rule on this GameBoard can. Replacing the lottery by deterministic hidden
variables (the `threshold` capture) raises S to exactly 2 and no further, as
the theorem says. The excess is reached only by the bonded ray field, which
takes the split of postulate 4: the pair's joint outcome is answered for both
ends at once by the bond registry, with no energy, momentum or message in it,
and S rises to the quantum value. The ray then carries everything physical at
link speed and the bond carries the one thing the experiments say is not
carried: the correlation. It is not a local derivation of the quantum
correlations, and it does not claim to be. What remains open is what the
registry is.

The dark-matter question was put to the same rule. Gathering a gravity train
to whoever catches a ray of it does focus the pull, but into the momentum of
the part of the train the flood can reach: it falls slowly while the catch
is partial and cancels when the catch is complete, and a rotation curve from
it would rise, not stay flat. The plain ray gravity stays inverse square. The
gathered gravity probe (`examples/gathered-gravity/`, deleted on 2026-09-17
with claim-gather) recorded it: the
GameBoard has no focusing that mimics unseen mass.

What the law claims on entanglement is the exact identities of ALGEBRA.md 4.9,
4.10 and 4.12, met by series L and L6 (DETECTOR); a click is one comparison and
one deletion per record (3.1, 4.7), and no other "collapse" is claimed; the one
failure is the order channel (chapter 6, row 1c). Until these requirements have been tested for the proposed laws, do not claim that
the simulator solves quantum collapse or entanglement consistency (history,
superseded on 2026-09-23 by ALGEBRA.md 4.9 to 4.12).

## Overall principle

Physical nodes keep bounded local state and exchange influence with neighbors.
Section 14 adds an explicitly authorized shared computation primitive alongside
that local world. It does not turn host evaluation into physical communication
(history: section 14 was deleted on 2026-09-17; there is no primitive beside the
six operations, ALGEBRA.md 2.7).

`SIMULATOR_DEFINITIONS.md` contains the exact executable requirements.
`docs/ARCHITECTURE.md` separates the engine, laws and measurements.
`docs/ALGEBRA.md` is the one statement of the algebra of the law, the source of
this document since 2026-09-23.

## 13. Experimental extension: variable-length links

This historical candidate was selected explicitly through a named research API
that was deleted on 2026-09-17. It did not replace the active disturbance model's fixed neighbor transit time.
In this candidate, each node also stores fixed information about its six links.
It owns the three positive-direction links and keeps local copies of the other
three. Ownership organizes storage; it must not privilege a physical direction.

Both endpoints can propose a length from their local field and information
already delivered by their neighbor. A proposal travels along the old length.
Both endpoints activate it only on arrival. Simultaneous proposals use the larger
length. This is an explicit experimental choice, not a consequence of Einstein's
work. Length changes do not alter a transit already in progress.

The default address spacing is 100 elementary length units; length 110 represents
a tenth of the default spacing added. Light travels one elementary length unit
per elementary tick, so its speed is 1. Each link has at most one packet traveling
in each direction. There are no per-source lists.

A moving particle remains a source at its origin until arrival. Direction and
length are locked at departure; interaction with the field resumes on arrival.
A nonintegral arrival time rounds up to the next tick. Unlike field and momentum
remainders, excess travel time cannot shorten the next transit: crossing a link
faster than c to repair an average is forbidden.

Tests verify stationary-source symmetry, neighbor-only influence and fixed local
storage capacity. They do not establish gravity or geodesics.

## 14. Shared quantum query postulate — Q-ORACLE-1

Deleted on 2026-09-17: the shared quantum resource and this assumption were
removed with Highlights section 3.18 (issue #164, buckets B.1 and B.2); no
owner answers at a distance. The text below is history and is not renumbered.

The user explicitly authorized `deferred-unit-cost-oracle-v1`: one successful
query to the shared quantum space counts as one elementary model operation and
consumes zero world ticks. This is a model assumption, not an established physical
fact or a claim that host computation takes constant time.

The quantum owner may evaluate a long deferred history outside the physical
six-neighbor computation. Its work and resource budgets are measured separately.
Bounded integer arithmetic still applies. Exhaustion and overflow are errors,
not absence of a particle, collapse or a new physical event.

Pure queries do not sample outcomes or change past records. Repeated queries are
consistent. The optional `terminal-two-output-trial-v1` test chooses one complete,
absorbing output using a supplied uniform integer ticket; repeated readout returns
the same shared record. This does not implement general measurement or establish
no-signalling. The test controller's record is not an Engine-native event.

Only the main engine may commit physical events through an explicit interface.
The later native extensions in sections 16 and 18 define their limited interface
and origin polling; quantum-field feedback is not supplied by this original
terminal-trial addition. Exact contracts and ownership are specified in
`SIMULATOR_DEFINITIONS.md` and `docs/ARCHITECTURE.md`.

## 15. Supplied mass and local elastic collisions

The historical scalar/contact candidate explicitly adds a positive integer inertial
mass per particle, default
one. This mass is a model input; it has not emerged from events. At the same
momentum a heavier particle moves more slowly, subject to the existing causal
speed limit. Mass does not silently replace the source-strength or field laws.

(History, marked 2026-09-23: the elastic-collision candidate of the next
paragraph was deleted on 2026-09-17; the collision in force is the permutation of
ALGEBRA.md 2.4.)

In the opt-in collision candidate, particles meeting at the same node and tick
undergo elastic backscattering. For equal and opposite momenta both return in the
opposite direction. With unequal masses the result is calculated in the pair's
center-of-mass frame, preserving the pair's total momentum and classical kinetic
energy. Fractions are kept exactly using bounded integer numerators and
denominators. No global correction supplies missing momentum or energy.

A contact occurs once per encounter, without an extra position jump. Link transit
particles can collide only after arrival. Fixed local flags distinguish a new
encounter from particles still occupying the same node. The exact two-body law,
multiparticle ordering, schema extension and limits are in the v13 section of
SIMULATOR_DEFINITIONS.md. This classical GameBoard hypothesis does not establish
relativistic physics or energy conservation of the existing field law.


### Selected event-network method

`deferred-event-network-v1` extended the existing quantum owner, not the ordinary
physical nodes; it was deleted on 2026-09-17 with its contract document.
Queries compute possibilities without choosing historical paths. Only an explicit
instrument request can select a result; it retains the conditional joint state,
including a no-event branch. No universal interaction-to-collapse trigger is claimed.

A known event location does not supply a simultaneous sharp momentum. Position
and GameBoard-momentum diagnostics use the same state. Exact host checkpoints may
replace complete correlated histories without sampling. Unused branches remain
available until an exact sufficient replacement is saved. These choices neither
make host computation O(1) nor establish a Newtonian or continuum field limit.

## 16. Selected native event-program extension

An explicitly selected initialization program may connect the shared quantum
owner to ordinary local cycles through a generic event resolver. A local result
can select a configured mechanical continuation; it is not a free remote state
read. Every executed physical path retains its local operation costs. A query
is one additional model operation, with zero direct world ticks; total local
cycle cost may still produce the ordinary computation delay. No cost is erased
to manufacture the classical endpoint. The native contract and its
implementation were deleted on 2026-09-17 with the integration layer.
This extended section 14 only for the declared candidate, not all interactions.

## 17. Explicit finite-register and unobserved-channel extension

The selected native v2 candidate permits finite local registers, complete
unobserved channels and grouped measurement outcomes. An unobserved Kraus label
is not a classical record and is not sampled. Preserve its density sum and all
remaining coherent information. Mixed checkpoints represent the complete live
component. Local supports, integer bounds, classical cycle charges and zero
direct oracle ticks remain unchanged. This is a representation/channel extension,
not a new collapse law or a derived physical species Hamiltonian. Its
implementation and document were deleted on 2026-09-17.

## 18. Event-spacetime origin cells - Q-ORIGINS-3

The user-selected origin-cell candidate keeps history solely in immutable event
spacetime, with no separate linked list per Node or wave. A participating Node
holds at most six origin IDs. Configured local operations propagate possible
causal support; they do not sample a hidden particle path. Current virtual
register heads and exact joint quantum state retain their existing owners.

At an explicit local wave interaction, the owner calculates every instrument
outcome from the current conditional state. A configured terminal outcome marks
its selected origins resolved once, atomically with the result. Other Nodes
check their local references each native tick and discard resolved origins;
commit never sweeps all wave fragments. A later gate executes only if every
declared participating origin remains active and has arrived at a local endpoint.
Suppressing a retired-origin gate requires unchanged complete correlated density.
Suppressing a retired instrument additionally requires its sole possible outcome
to be the declared no-event result with unchanged density. Otherwise reject the
cancellation; a remote flag cannot remove observable dynamics arbitrarily.
These certificates are separately priced quantum-owner work, not O(1) status
lookups or physical observer signals. One origin may encode several disturbances;
the interaction definition names one to six origins without inferring particle
count. A continuing outcome
preserves the conditional state. A position record does not assign sharp momentum,
and a coherent interaction need not sample at all.

Resolution status is quantum-owner bookkeeping associated with the source event,
not a mutation of its historical physical data or an ordinary remote field read.
The finite candidate, initialization requirements, cost distinctions and open
physical questions were defined in a document deleted on 2026-09-17 with the
origin cells themselves.
Bounded local lookup does not make total host evaluation or memory constant.

## 19. Localized quantum contact candidate

The explicitly selected localized contact hybrid (its contract and
implementation deleted on 2026-09-17)
transferred one configured ordinary inventory into a finite coherent domain only
when an actual local contact commits. Undefined momentum is explicit information
state, not a zero vector or a derivation of propagation amplitudes. A complete
local absorption instrument restores one localized record and leaves quantum
vacuum. Number-preserving propagation and origin retirement keep one inventory.

Ordinary fields are emitted only by localized records under their finite configured
allowances. Existing field stock continues causally. Neither conditioned
probabilities nor shared origin flags drive a remote ordinary field update.
This is the user-selected approximation, not a derivation of quantum fields,
physical momentum or the general classical limit. Its clock and representation
limits are explicit and do not silently extend the older native profiles.

## 20. Causal local quantum source candidate

The explicit causal source extension (its contract, runtime and envelope
modules deleted on 2026-09-17; issue #164, bucket B.3) permitted
ordinary emission weighted by a bounded complex envelope retained at the same
Node. Phase evolution uses frozen local and causally received neighbor inputs.
Only an actual local contact can prepare or localize the configured inventory.
A successful capture creates one full-strength localized source and sends
termination through Links with local delay. Shared quantum origin retirement
never controls remote ordinary fields or their clocks.

After measurement these are retarded, potentially unnormalized source weights;
the candidate does not silently substitute global conditional probabilities.
Previously emitted fields remain causal, finite source allowances do not refill,
and charge inventory is counted separately from field-source weights. This
extends section 19 only for `causal-contact-fields-v1`, preserving its older
localized-only selection and making no new quantum-field or energy-closure claim.

The optional null notice extension (deleted on 2026-09-17 with the same runtime)
lets a Node that records a null result send its own renormalization factor
`1/(1-p)` through Links. Receiving Nodes multiply a local weight scale after
their control delay and forward the notice. The factor is computed from local
state only and travels at Link speed; for one excitation it equals the exact
conditional renormalization once delivered. Between decision and arrival the
remote weights remain stale. This is a candidate rule that closes a measured
gap in the single-excitation sector; it is not a general Born-rule mechanism
for entangled registers and it never reads the shared quantum state.

The optional field-dependent phase (deleted on 2026-09-17 with the same runtime)
lets a configured one-mode gate choose its exact integer phase from the Node's
own classical field value at the schedule tick. The classical field then acts
on the wave, locally and causally, as a phase only. Its `unit / vacuum` ratio
is configured data, not a derived coupling constant, and no field-plus-matter
conservation follows from it. Negative field exponents invert that relative
phase by conjugating both coefficients; a common phase on the coefficient pair
does not change observable probabilities.

The optional funded envelope emission (deleted on 2026-09-17 with the same runtime)
pays the wave's classical field from the wave's own conserved stock instead of
an external source, so the field and the wave close together: totals stay
constant, the localized winner inherits the unspent stock, and the only
external term is the retarded emission committed after a remote localization,
which is reported. The stock is held by the quantum owner like charge and mass;
it is not transported between modes, and the field still exerts no force on it.

## 21. Configured recurrent contact outcomes

The explicit recurrent contact candidate (deleted on 2026-09-17 with its
contract and runtime),
`recurrent-contact-fields-v1`, extended section 20 with complete configured local
outcome instruments. A source encounter can retain its localized record or
transfer it into a vacuum domain. A capture can leave vacuum, localize the
inventory, continue the conditional wave, or resolve its origin and begin a new
local continuation. Only the instrument and current conditional state determine
the lottery; a certain result consumes no random ticket.

One inventory owner survives each transfer. New-wave creation and old-origin
resolution are atomic, with immutable event history and bounded current references.
At most six explicitly preallocated source generations retain separate causal
packets and finite allowances. A local vacuum result clears every nonretired
local envelope; remote quantum generation changes cannot choose an ordinary
source bank. Existing field stock follows its configured transport and decay.
This is a finite configured hypothesis, preserving the older profiles and their
limits; it does not derive the matrices or establish physical energy closure.

## 22. Historical autonomous sampling candidates

Adopted direction (model owner, 2026-09-17): the only draw in the model is the
Detector interaction, 1 or 0 for each transfer arriving at a marked node,
every ray being a wave ray, 1 ordinary behavior and the only measurement,
0 return and no measurement (nothing measured or recorded as an outcome),
one bit per arriving transfer, and the bit is all the Detector adds
(the Detector-only contract made concrete in
[section 23](#23-the-ray-event-model)). A pair's bit is drawn at the first
Detector and carried by the returning ray, which walks back the same number
of steps it has made since its event and transmits it by the inverse split
at the birth event to the partner ray's line, and the second Detector
receives it on the ray that reaches it and draws its own bit on that
arrival like on any other; a Detector sees nothing of the ray, only its
own value, the received value is information on the ray, not an input to
the draw, and no owner answers at a distance (superseded on 2026-09-17 for
rays that carry a bit: a Detector reads the bit, below). The information
of the last event, its Ports and shares, stays on the ray as a hidden
variable: no Detector and no ordinary coupling reads it, it comes from no
ordinary physics, and nothing on the GameBoard feels it. The Detector's bit is
different (model owner, 2026-09-17; Highlights 5.4, "the Detector's bit is
a property of the ray"): it travels with the ray as a visible property
like charge, seen by every meeting, by the record and by the rendering,
inherited by the outputs of any event a marked ray takes part in (where
the inputs carry different bits the declared coupling says which the
outputs carry, by default 1 outranks 0 and 0 outranks none), readable by a
coupling in the catalog as charge is, and read by a Detector (model owner,
2026-09-17, closing the open decision of that morning): a ray carrying 1
is already realized and passes a later Detector without a draw, as a
measurement repeated in the same basis repeats its result, a ray carrying
0 is a transmission and is never drawn, and only a ray carrying no bit is
drawn, how a marked Node meets each bit being its declared coupling in the
catalog with this as the default and the draw on every arrival, as before,
the declarable alternative (feature 2b of the ray-event model, after
feature 10, implements both; until it lands the engine draws on every
arrival). The price of Highlights 5.4 is to be re-derived under this rule
by hypothesis 11 and experiment A13 before it is quoted again. With two
Detectors, Alice's and Bob's, whichever returns first sends its value
through the birth
event and the other receives it; sometimes it is Alice's information,
sometimes Bob's. To Alice and Bob the correlation feels as if it were decided
at time zero, but nothing happened at time zero: the value was carried
through the birth event in event spacetime, one Link per interval.
For two Detectors at equal distance from the birth the CHSH value is at most 2,
and the joint law's value appears only when the second ray's path exceeds the
round trip through the first Detector. This price is accepted. The text below
describes the historical candidates, including the shared registry, and their
measurements; the lottery capture, the bond registry, the Bell probes and the
`historical-autonomous-v1` profile were deleted on 2026-09-17 (issue #164,
bucket B.5), and the measurements stay in the validation log. Superseded on
2026-09-18 by the law of the bit (section 25): nothing draws, what arrives
at a mark is a thing or its shadow and that was decided at birth; a mark
absorbs a thing and returns a shadow, and a shadow's return is a field, not
a walk back by a step count. (And on 2026-09-19 by the law of the ray: no draw,
ALGEBRA.md 2.7; the pair's click one gather, 3.6; the price of the round trip is
gone, the Bell value one gather's exact rational, 4.10.)

(History, marked 2026-09-23: the marked Node and its draw of 2026-09-17 in the
next paragraph were superseded on 2026-09-19; the picture of the world as the
list of clicks stands, ALGEBRA.md 3.1 and 3.2; "a source is a Detector" is the
first form of the one generic detector-emitter of Highlights 5.4, record 1327.)

Addition (model owner, 2026-09-17; Highlights 5.4, "everything begins and
is realized at a marked Node"): a source is a Detector, so every ray's
history begins at a marked Node; between marked Nodes it is content on
paths, combining by phase where paths meet; a marked Node that draws 1
realizes one path of events, and its return cancels the others through
their event. The picture of the world is the list of PASS clicks in the
frame of the observer, and nothing else is ever seen: the rendering of the
GameBoard is the record's view, which no observer inside the world has, and
the same run drawn as clicks only is the physical picture.

(History, marked 2026-09-23: the sequence of tickets of the next three
paragraphs was deleted on 2026-09-17; the law has no draw, ALGEBRA.md 2.7; the
one selector is the birth wheel, a counter on Z_W, 3.6 and 6.1.)

Every interaction whose outcome is not certain consumes exactly one bounded
integer from a configured sequence, and nothing else decides it: the record's
own ticket for a lottery capture on a ray field, the quantum owner's ticket at
a contact, and the bond registry's number for a bonded pair. The world's
history is fixed by its rules, its initial state and this sequence of integers,
one per interaction, and the same sequence replays the same history. Replay
establishes reproducibility, not reversibility, and no physical origin for
the probabilities.

A bonded pair is one interaction and draws one number, whichever end asks
first, Alice's or Bob's. The number is a fixed function of the registry seed
and the pair's birth code. Its upper half is the first end's even coin; its
lower half, read against the difference of the two settings, decides whether
the second end agrees, with the singlet's probability
`(1 - cos(difference)) / 2`. Neither end can read the number: each sees an even
coin whatever the other end's setting, so the number carries no message and
postulate 4 holds for everything physical. The number is a hidden variable in
Bell's sense, local for a lottery capture, where it lives in the detector's
record row and `S` stays at or below 2, and shared for a bonded pair, where
one number answers both ends and `S` reaches the quantum value. The
bonded ray field
implemented the pair's single number; the Bell probe (`examples/bell-chsh/`,
deleted on 2026-09-17) measured it. What the sequence is, beyond a configured seed, is the open
question of postulate 12 in another form.

Three things follow from this postulate without a further assumption. The
sequence is the only place where information not already in the world's
state enters the world, because everything else is fixed by the rules and the
initial state. The model does not fix the generator of the sequence: a
seed, a file or a source outside the world give the same physics as long as
the numbers are used the same way. It does fix how a number is read, and that
decides which of Bell's assumptions is at stake: a number chosen before the
settings and read by one end only is a local hidden variable and keeps `S` at
or below 2 (the lottery); a number chosen before the settings and read by
both ends keeps measurement independence and breaks parameter independence
(the registry); a number correlated with the settings would relax measurement
independence, and no rule in the model does that. And the two halves of a bonded pair's number are bound
differently: a supply biased in the coin half moves one end's plus rate
with the other end's setting, a signal faster than the causal speed,
measured as such; a supply biased in the agreement half moves no marginal
and is not a signal, and it is not held to the quantum value either, since a
fixed lower half gives the Popescu-Rohrlich box, `S = 4`, with even
marginals. No-signalling bounds the coin, not the correlation; what bounds
the correlation at the quantum value is the singlet law in the lower half,
and that law is configured. The [hypotheses page](docs/HYPOTHESES.md) states the tests.

## 23. The ray-event model

(History, marked 2026-09-23: the ray-event model of 2026-09-17; superseded on
2026-09-19 by the law of the ray, ALGEBRA.md chapter 2; its document was deleted
on 2026-09-19. The whole section is history; the algebra's lines it touches are
in docs/designs/detector_law/POSTULATES_BY_ALGEBRA.md, rows 23a to 23l.)

Adopted as the target direction by the model owner on 2026-09-17 and recorded
in [docs/HIGHLIGHTS.md](docs/HIGHLIGHTS.md) (sections 3.3, 3.4, 3.5, 3.15,
3.19, 3.20, 5.1 and 5.4), the Highlights specification edited directly since
that date. The design candidate `ray-event-model-v1` in
docs/RAY_EVENT_MODEL.md holds the complete
statement, the migration order and the acceptance criteria.
Nothing in this section is implemented yet; every implementation step is a
separate published change measured against that document. Since 2026-09-18
the law of the bit (section 25) supersedes the sentences of this section
that it names, and the features of the ray-event model's migration list
record what is implemented.

Addition (model owner, 2026-09-17; Highlights 3.6, "one ray, one
catalog"): there is one kind of thing on the GameBoard, a ray, content in
whole quanta with an amount, a phase, a heading and a family, moving one
Link per interval, and everything else is a name for a situation of rays:
a family is a field, its free rays what physics calls the field and one
quantum of them its particle in flight, and matter is a bound pattern of
rays of a family, the particle at rest, its content its mass and its
clock. The catalog, the families with their properties and the couplings
with their tables, is the whole content of the theory, what the Lagrangian
is in physics; the engine is the one law that runs it, stepping, counting
and dividing, never knowing what an electron or a star is; the only draw
is at a marked Node, and the picture of the world is the list of PASS
clicks. The model owner's reading is that this one ray, in whole quanta,
is what physics calls the quantum field, a reading the confrontation runs
test.

The model has exactly two definitions, event and ray: a ray carries
information, an event is where that information splits, and a ray is what
was split off from an event. An interaction is a meeting of rays at a node in
one interval, decided by the coupling declared between the families present;
it is the only place where anything is decided, and its result is at most six
events, one per Port. Event spacetime has layers: a layer is a set of
families that couple, and a meeting exists only inside a layer; rays whose
families have no declared coupling never meet and cross as if the other were
not there, so two events can happen at the same node in the same interval in
layers that do not communicate. An event is a change of trajectory: a new straight line
leaving the interaction through one Port. A ray is not an object; it is the
trajectory of one event between two interactions, the same event with the
same family properties, one node per Link interval, one heading. From its
event, every ray carries the number of steps it has made (for a shadow
retired on 2026-09-18, section 25: its return is a field with no step
count), and every ray
carries the information of the last event it was involved in; if that event
was at a Detector, the ray records that it was a Detector event and the bit
drawn, 1 or 0, and the bit is all the Detector adds. A ray trajectory is
reversible: run backward it returns exactly to the interaction
that created it, because nothing was added or lost along the line. A node
that a ray merely crosses hosts no event.

Outside a Detector every trajectory an interaction permits actually happens:
the up-to-six events all propagate, each as a straight ray with its share of
the conserved quantities and its phase. Alternatives are created only at
interactions, never at the empty nodes a ray crosses. Every ray is a wave ray
and carries a phase; a plain ray is a special case of the wave ray, not a
second kind. Light is a wave ray with no mass and no charge, an event moving
in time. Three things change a phase and nothing else: each interval advances
it at the rest rate its family declares, which is the ray's mass as a clock,
and that rate is zero for light, whose phase does not advance along its own
line; an interaction changes it as the declared coupling says; a bound group
advances it once per interval it is held. A light ray carries the phase of
the clock that emitted it at the moment of emission and delivers it
unchanged, so the frequency of light is the rate of its emitter's clock.
Since 2026-09-18 the rate is the thing's content / K, one K for the world,
and a shadow has no clock (section 25, point 19).
Interference of light follows from this alone: two paths of different length
reach one place at one time only if their rays were emitted at different
times, so they carry different emission phases, and the difference is the
emitter's rate times the difference in path length; nothing is accumulated
on the way. There is no amplitude as a number and no probability field: the
phase and the ray's conserved content together are the discrete stand-in for
the quantum amplitude, the phase as its angle and the conserved content as
its size. Because every permitted trajectory happens, the intensity at a
place is how much content arrived there, and interference is steering:
where rays meet in one layer, the declared coupling reads their phase
difference and decides through which Port the shared content leaves, with
every invariant exact; nothing is erased. The basic steering coupling is the Born rule stated as a coupling: for a
phase difference δ it splits the shared content between the two candidate
Ports in the ratio cos²(δ/2) to sin²(δ/2), as a declared table of bounded
integer ratios with the remainder owned as Highlights 3.17 requires, so that
click intensities follow the Born rule with nothing read by any Detector. It
is declared, not derived. Since 2026-09-18 the table is computed from the
family's phase width N and declared by no one (Highlights 5.4, point 17).
The Detector reads
none of this; the probability of a click is already in how much content
reached it.

At a node where rays meet, the declared coupling decides one of three things:
no interaction, and the rays cross as if the other were not there; a
deterministic interaction, up to six
events computed from the frozen inputs with every declared invariant exact
over all inputs and outputs; or a Detector interaction, at a node whose Detector
bit is set, which draws 1 or 0 for each arriving transfer, independently,
up to six in one interval: 1 ordinary behavior together with the other
arrivals that drew 1, 0 return of that arrival on its own line. A ray alone
at a node never interacts. Since 2026-09-18 a mark draws nothing: it
absorbs a thing and returns a shadow (section 25, points 6 and 14).
Binding is the interaction whose result is zero events: the rays stay at the
node, interact again every interval, and their phase advances once per
interval.

Addition (model owner, 2026-09-17; Highlights 3.4, "binding is a periodic
orbit of the meeting rule"): a ray never stops, and "bound" does not mean
"resident", it means "back at the same place in the same state"; a bound
group is a set of rays whose meetings, under the ordinary coupling table,
reproduce the rays that entered them: the outputs leave, walk their Links,
meet again, and the meeting gives the same amounts, the same phases modulo
the circle and the same headings, so the pattern repeats forever; a
pattern whose meeting does not close disperses. There is no binding rule:
a bound group is a fixed point of the meeting table over a loop, and the
only declared thing is the table. On the cubic GameBoard the smallest loop
is a unit square of four nodes with rays circulating both ways, each
corner meeting every interval two rays that leave through each other's
Ports; a group therefore lives on a ring of nodes, not at one node, its
size is the ring, its clock is the period of the loop and its mass is its
content (Highlights 3.28); its field is released by rays in motion, five
headings each, and its motion as a whole comes from its loop, the corners
shifting, not from a register on a node. The ladder of hypothesis 12 is
the set of contents and phases that close a loop under the table, which
experiment A10 counts. The held-ray binding of feature 8 (a rule with
delay 1 and no outputs, and its ray_delay wait), which holds any content
and therefore has no ladder, and the register-driven motion of feature 8c
are the interim forms, superseded by feature 14, binding as a loop, after
features 12, 8c, 2b and 8b; the sentences of this section that speak of
rays that stay at the node describe the interim form.

Every node carries one bit, Detector or not; the mark is bounded node
metadata (bit, setting, ticket seed), not a record and not an external
device, and Detector behavior is how a node behaves when the bit is set. A
source is a Detector: whatever emits a ray of a known family is a marked
node, because knowing the family of what it emits is a measurement; the
birth event of a pair therefore happens at a marked node, which draws on
every arrival like any other. A
marked node does one very simple thing. What arrives is a wave ray carrying
information; every ray is a wave ray, so the kind makes no difference. For
each transfer that arrives, whatever it is, it draws 1 or 0. On 1 it behaves
as an ordinary node for that arrival and the transfer continues or interacts.
On 0 it returns that wave ray on the same line in the opposite direction,
unchanged, back the same number of steps it has made since its event, so that
it arrives at the node it left from with exactly the information it left
with. Up to six transfers can arrive in one interval, one per Port, and
the node draws once for each, independently: the arrivals that drew 1 enter
the ordinary interaction together, each arrival that drew 0 is returned on
its own line. The Detector reads, changes,
absorbs and adds nothing; the click is the record of the bit drawn. A
measurement exists only when the node drew 1 and let the ray pass: on 0
there is no measurement, the node returns the ray without touching it and
is a node without measurement, as if the ray had not arrived, and it waits
for what the return brings back; nothing is measured or recorded as an
outcome. A
Detector sees nothing of the ray, on 1 or on 0: it sees only its own
value, except the bit a ray already carries, which it reads since
2026-09-17 (Highlights 5.4, feature 2b): a ray carrying 1 passes without a
draw, a ray carrying 0 is a transmission and is never drawn.
When it returned a ray with 0, that value travels with the ray, and the
second Detector of the pair receives it on the ray that reaches it.
A returning ray retraces its own trajectory by its step count, reaches its
birth interaction with certainty and there performs the inverse split of its
share: it transmits what happened at the event, with its bit, to the same
places the event sent to, the partner ray's line among them, so the
partner's Detector is not missing it: it receives that value on the ray
that reaches it. Pair identity is the trajectory, not the birth node and
tick. Superseded on 2026-09-18 (section 25): the mark has no seed and draws
nothing; a thing that arrives is absorbed or passed by the mark's declared
table, a shadow is returned as a field with no step count, and a returning
shadow performs no inverse split.

A ray has a field: the field is the ray's own information spreading in ray
form to the nodes around it, without an event; a field ray is not a second
kind and is not born at an event. The field's presence at a node is an
interaction that makes no event. A field never makes an event unless it
meets something it changes; the first event a field is involved in is that
meeting, and the returning ray that carries the recoil is split off from
it, like every ray from its event. Where a field ray meets a ray whose declared
coupling responds, the meeting is an ordinary interaction and its events
change that ray's trajectory; everywhere else the field crosses without an
event. One of those events is the field ray itself returning reversed: the
return is the opposite momentum of the field, carried back along the field
ray's line to the ray that released it, which recoils when the return
arrives, at finite speed. That is how postulate 7 and Highlights 3.14 are
satisfied: the recoil is a ray. Until its field meets something, a
traveling ray pays nothing for it. The field is released in all directions,
and the release does not wait for the clock (model owner, 2026-09-17;
Highlights 3.5, section 6): resident content releases every interval on all
six headings, a traveling ray on the five headings other than its own, and
the output clock delays only what leaves as matter, never the field.
A ray traveling straight never meets its own field: the field is born where
the ray is and leaves at the causal speed, ahead of the ray or away from it,
and the ray is never faster than its field, at any output-clock delay; no
exclusion rule is needed. Only after a change of trajectory can a ray cross
field it released earlier, and that is a meeting like any other. A ray's
phase per interval comes from its family's rest rate alone, not from its
own field.
There is no
matter in the model at this stage: matter is the name for rays bound in one
node by a declared binding coupling, a neutron ray and a proton ray held
together by the strong binding, an electron ray around them whose trajectory
is changed at every step by the field rays the bound pair releases. Mass is
the retained energy of a bound group, and the group's phase advance is its
clock. A bound group has no lifetime of its own: it lasts as long as the
binding interaction repeats at that node without releasing an event. The
binding may be nothing more than a very large output-clock delay (Highlights
3.28) that the bound rays create together, a large mass making the node very
slow, so that the rays do not leave. It is unbound the same way anything
else happens on the GameBoard: a ray arrives (a high-energy light ray, for
instance; there is no photon, only a ray) and the coupling declared for the
families present produces events that leave. Nothing else creates or
destroys matter. The computation field obeys the one field rule above, with
no rule of its own: the retained content of a node, its mass, is what makes it slow, and the
information that a node is heavy spreads from it in ray form in all
directions. Where such a field ray meets a ray whose declared coupling
responds, there is an event with two effects: the ray that was met is
delayed, its output clock grows, and the field ray returns reversed to the
heavy node. The delay is larger on the side nearer the heavy node, so the
ray bends toward it; that bending is a change of momentum, and the
returning field ray carries the opposite momentum back to the heavy node,
which is drawn toward the ray. Gravity is this bending by delay; it is not
inserted as a force, nothing is absorbed, and momentum is exact. Held source records remain an explicitly labeled interim
device until the binding couplings exist. Superseded on 2026-09-18 (section
25): the field of a thing is its shadow set, rays of its own family with bit
0, given with the GameBoard and never released per interval; a shadow spreads
by the node's mixing, pushes a thing by the thing's reading and turns back
as a field with its momentum inverted; nothing delays a ray and there is no
output clock; gravity is the push read times the content of what is pushed,
and the wait per whole quantum read is where the bending beyond Newton's
comes from (Highlights 5.4, points 3, 9, 12, 16, 21, 23 and 24).

Addition (model owner, 2026-09-17; Highlights 3.26 and 5.3): forces and
polarization are catalog entries, not engine mechanisms. The engine performs
only the simple operations: a step on a Link, a phase advance, a split by a
declared table, a sum, and the one draw at a marked node. Anything that does
not change how a ray moves between events is therefore a family property in
the catalog or a coupling table, read only at a meeting, exactly as charge
is, and no new engine mechanism is added for it. Polarization is such a
property: a transverse mode perpendicular to the heading, two states for
light (the two GameBoard axes perpendicular to an axial heading) and two for
the electron family (spin), read by the declared couplings at a meeting; a
circular polarization is not defined and, if wanted, would be a transverse
direction that turns with the phase plus one handedness bit, again a catalog
choice. Pauli exclusion is a binding coupling that does not fire for two
electrons in the same state with the same spin. Polarization is feature 11
of the ray-event migration (issue #169), after its ten features; none of
them needs it. The strong interaction is the same pattern: quark families,
colour a property with three values, the gluon the quark's own field in ray
form, the binding of three quarks a binding coupling; its short range and
its growth with distance are expected from one more declared coupling, the
quark's field rays binding to each other, and whether that yields
confinement is a research question
([hypothesis 13](docs/HYPOTHESES.md#13-confinement-from-the-quarks-field-rays-binding-to-each-other)),
not an engine decision. The weak interaction is a change of family: an
N-to-M conversion at an event with its declared invariants (charge, energy,
momentum). A free particle never decays, because there is no event without
a meeting and a straight ray does not change; a neutron is a bound group
whose ticks are events, and a bound group that can decay is a source, and a
source is a Detector (Highlights 3.19): at each tick it draws with its
declared ratio as the setting, 1 = the conversion fires, 0 = the group ticks
on unchanged, so half-life follows. That draw is the one draw of section 22,
at a node whose Detector bit is set; nothing else in the world draws. None
of this adds anything to the engine; all of it comes after feature 10.
(Superseded on 2026-09-18: a decay is a table on the group's own state and
nothing draws, section 25, point 20.)

Addition (model owner, 2026-09-17; Highlights 3.26, in the language of
binding as a loop, section 3.4): the strong field differs from light by
one catalog line, its rays couple to each other, so the field between
quarks does not spread as a sphere but closes into loops of gluon rays
along the line between them, a string whose content, and so whose mass,
grows with the distance; only colour-neutral patterns close a loop, which
is confinement as a closure condition; and a string stretched to the
content at which a new loop closes with a quark and an antiquark breaks
into two hadrons, which is hadronization. None of this is inserted:
hypothesis 13 says whether the two catalog lines produce it, in a research
run after feature 14.

Addition (model owner, 2026-09-17; Highlights 3.19; named "fixed body"
earlier that day, renamed the external body the same day with the same
specification extended): beside the Detector there is one more declared
element of a world, and like the Detector it is a declaration, not physics:
the external body, a node declared to hold a family with an amount and, if
wanted, a charge, standing for a star, a neutron star, a fixed proton, a
large charge, or a piece of apparatus. What is declared: the family, the
amount (finite, of any width, since it enters no sum; it only sets how much
field leaves per interval), the charge, and an initial momentum (a heading
and a pace, zero for a body at rest). What it does: it radiates exactly as
any bound group does, by the one field rule of this section (Highlights
3.5) and with the strength its amount gives, so its gravity and its
electric field are the ordinary field rays of the model and every ray that
meets them responds by its declared coupling. What it does not do: it does
not spread, which is its defining property: it never splits, binds,
unbinds, converts or decays, and its whole content stays at one node; and
it is not pushed by matter: whatever arrives at it, a recoil field ray or a
ray that couples to it, is met by the declared coupling of its family, and
the body's content never changes. Absorption into an explicitly accounted
sink is the default coupling, and the other couplings make the apparatus: a
reversed heading is a mirror, a split by a declared table is a beam
splitter, a phase offset is a phase plate, a polarization read is a
polarizer once feature 11 exists; a wall, a screen and a beam stop are the
default. Its motion is caused by fields only (model owner, 2026-09-17,
replacing the declared trajectory, never caused, of earlier that day): it
starts with its declared momentum, an arriving field ray of a family its
coupling table names changes that momentum by the table, and nothing else
moves it, since matter that arrives is absorbed without a push; its
velocity is its momentum over its amount, kept as an exact accumulator that
steps one Link when a full amount has accumulated on an axis, so against an
electron it stands still while two stars turn each other over long times;
and wherever it is, the node it is at holds all of it. The audit carries
the bodies' momentum as its own line, so momentum stays exact when a field
ray is absorbed. The audit books what it radiates as a source and what it
absorbs as a sink, so conservation stays exact at every tick. On the node
it is bounded metadata like the Detector mark: the kind of mark, the
declaration, and one exact counter (the sink totals per family); no rays,
no history.
When the back-reaction is wanted, a star that recoils or a proton that
moves, the body is not used: the same thing is declared as an ordinary
bound group with a large amount, and then it spreads and is pushed like all
matter. The external body is the approximation of infinite mass, used for
the confrontation runs: light bending by a star, an electron near a large
charge, a hydrogen-like spectrum around a fixed proton, and the two-slit
and Bell geometries with their walls, mirrors and splitters. In the node's
law it is one flag: spreading is not enforced for this node's content, and
every other step of the law (the arrivals, the couplings by table, the
stamping, the departures of what leaves) is unchanged. That flag is also
why it has no ladder of masses: the ladder of
[hypothesis 12](docs/HYPOTHESES.md#12-one-mass-ladder-and-the-composite-spectrum-from-binding)
comes from the spreading law, since a bound group is rays that must keep
moving and bind again every interval, so only the closed patterns the
binding table can hold exist; a body that does not spread has no closure
condition and any amount is allowed. It is feature 7b of the migration in
docs/RAY_EVENT_MODEL.md,
after feature 7, `external-body-v1`. Since 2026-09-18 (section 25, point 22
and the settled rule (v)) the external body is a thing with declared
tables: its shadows are given with the GameBoard, it radiates nothing per
interval, and nothing is sourced.

Postulates 1 to 4 hold under this model without exception; the registry
exception of postulate 4 and the shared query of section 14 lapsed with
Highlights section 3.18, deleted on 2026-09-17, and the price stated in
postulate 22 is accepted. (The price of section 22 is superseded by ALGEBRA.md
4.10; sections 1 to 4 hold with the one read-out exception of 3.4.)

## 24. Everything is information transfer; a return is the inverse split at the event

(History, marked 2026-09-23: the returning ray and the inverse split of
2026-09-17, the lanes of 2026-09-18; superseded on 2026-09-19 by the law of the
ray, ALGEBRA.md chapter 2; that a Node keeps nothing stands, 2.8.)

Adopted as the target direction by the model owner on 2026-09-17, together
with section 23, and restated by him the same day (Highlights 3.3, 3.20 and
5.4); implementation pending.

Everything on the GameBoard is a transfer of information. The model has exactly
two definitions, event and ray: a ray carries information, an event is where
that information splits, and a ray is what was split off from an event. An
event is a splitting of information: the interaction splits what arrived
into the rays that leave, at most six, and each ray carries its own share of
what happened at the event away from it, along its line, one node per
interval. All the information is on the rays; the origin node keeps nothing,
and there is no register of any kind at the origin, no occupied channel and
no capacity rule: rays cross, meet or bind by their declared couplings, and
nothing is pushed back or made to wait for room. Every ray carries the
information of the last event it was involved in; if that event was at a
Detector, the ray records that it was a Detector event and the bit drawn,
1 or 0, and the bit is all the Detector adds. An event cannot be moved;
there is no such thing. It happened at its node, and a returning ray walks
back exactly the number of steps it has made to reach it (for a shadow,
superseded on 2026-09-18: its return is a field and walks nothing back,
section 25, point 3). Since 2026-09-18 (section 25, point 25, the model owner) a Port is two
lanes and a lane carries per interval one real ray and one shadow per
owner, which supersedes, for real rays on a lane, the sentence above that
no capacity rule holds a ray back: a thing steps into a lane only if the
lane is free and otherwise keeps its heading, two real rays of one family
given one lane are one, nothing queues and nothing waits for room, the lane
being a condition on a thing's step and not a tie-break.

A Detector that returns a ray is not sending a message to anyone. The
returning ray carries what happened at the event, its own share only, with
its bit and nothing larger, and at the event node it performs the inverse
split with its information, transmitting it to the same places the event
sent to, so that it cancels what was already there and the momentum and
energy of that share are restored exactly. This turns time back for that
ray's share only; the other shares are untouched until their own rays
return. A ray that passes the Detector is realized. For a pair, the
partner ray's line is among the same places, so the partner's Detector is
not missing the bit; that is the same inverse split, not a second mechanism.
The transmission is a ray like any other, with a field like any other: it
cancels the share only where it meets it, and where it meets nothing it makes
no event, by the same definitions. A share that left the event earlier on a
straight line at the same speed is met only where it was delayed: bound at a
node, slowed by an output clock, changed by an interaction or standing at a
Detector; for a pair this is the condition of Highlights 5.4. Even when it
is never caught, the event as it was has changed: the returned ray reversed
its share, so the event lost that share, and the information is never lost,
it chases the share it cancels. If the share is delayed and caught, momentum
and everything else are conserved at the node where they meet.

What a returning ray does at its event node when nothing is there is a
configured mode of the world, three of which are defined and tested:
siblings, the default and the rule above (it transmits its share and bit to
every line the event sent to, which needs at most six records on the ray,
one per Port); straight (it continues straight through the node on the one
line opposite its own, enough for a pair, with no records); and annul (it
ends there, its content leaves the world into an explicitly accounted sink,
initial equals current plus escaped plus annulled at every tick, and its
information survives only in the record). If something is at the node, a
bound group or other rays, the returning ray meets it by the declared
coupling in every mode. For a ray-interaction event whose inputs were
consumed, the returning ray cancels its own share only and continues along
the event's output lines; nothing is left at the node.

Each ray meets its own fate. Sibling events of one interaction are
independent rays; nothing cancels a sibling's share except its own return.
The once-only requirement of the central specification is therefore a
property of the returns, not of a shared owner, and it is accepted that a
sibling can be realized at a second Detector before a return from the first
arrives.

Addition (model owner, 2026-09-17; Highlights 3.20): entanglement is the
shared last-event record of siblings and nothing else. Rays that left the
same last event carry the same record of it, and nothing reads that record
until a Detector; that shared record and the trajectory back to the event
are all there is to entanglement, with no register and no state at a
distance. A Detector that draws 1 realizes its ray; one that draws 0 returns
it, and the returning ray delivers what it carries to the sibling lines
through the event by the inverse split above, so whatever happens between an
event and the first pass, 1, is a correlated set of rays, and a pass is the
only thing that ends it. An ordinary meeting on the way is itself an event:
its outputs are new siblings of that new event, and each ray's siblings are
always those of its own last event. The earlier correlation is not lost: the
transmission from a return chases the share through the later event by the
rule above, which is how correlation passes from one pair to another without
any rule for it. The price of section 22 applies to every such set.

The conservation laws exist for this. Energy, momentum component by
component, charge and every other declared invariant are conserved exactly
across an interaction so that the event can be rebuilt from its pieces when
they return: the pieces are the information, and the conserved totals are
the check that nothing was added or lost when they split and when a share is
returned. A Detector that returns a ray is therefore returning an event in
time: the share walks its line backward and the event is undone by exactly
the amount that share carried, and only that. Exact integer conservation on
the GameBoard is what makes this undoing exact rather than approximate.

The design candidate in docs/RAY_EVENT_MODEL.md
carries this section's consequences for ray state and for the acceptance
criteria.

## 25. The law of the bit: the thing or its shadow

(History, marked 2026-09-23: the law of the bit of 2026-09-18, superseded on
2026-09-19 by the law of the ray, ALGEBRA.md chapter 2; its records are
docs/LOG_2026-09-18.md; the sentences it superseded in sections 3, 4, 6, 9, 10,
22, 23 and 24 are history twice over.)

Decided by the model owner on 2026-09-18 and amended by him the same day;
recorded in [docs/HIGHLIGHTS.md](docs/HIGHLIGHTS.md) section 5.4 (the
definitions, points 1 to 25, "A thing does not emit", "Every action is a
message that returns", "A meeting is reported to its owner" and the five
settled rules), which is the text to follow where this restatement differs.
It supersedes the sentences of sections 3, 4, 6, 9, 10, 22, 23 and 24 marked
above.

**The bit.** Every ray carries one bit, and the bit says what the ray is:
1, *real*, a thing, the ray itself; 0, *shadow*, its field. Nothing else
distinguishes rays: there is no light and no matter as kinds, one kind of
content with declared properties and one bit (Highlights 3.3). A shadow is a
ray of the same family as its thing, with bit 0; there is no field family
(point 12). A thing has an amount, a phase, a heading, a bit and a momentum;
a shadow carries its owner's identity, charge and content as a message, has
no mass and no clock, and returns as a field. "Thing" is the noun for a
real ray, and the word register leaves the model with the stores it named
(point 22).

**Birth and motion (points 1, 2, 10, 21).** What is born from content is a
thing; what is given as field is a shadow, and a shadow releases nothing.
A thing moves whole on its line, one Link per interval, and turns by its
momentum: every push adds to it, and when its component on an axis reaches
the thing's content the thing steps to that axis and the momentum drops by
that content; momentum sets direction only, never speed. A thing has one
path and only one; its bit never changes at a meeting, and only a mark
takes it off the GameBoard. A shadow spreads by the node's mixing (point 24).

**The node mixes the six (point 24).** At every node, the shadows of one
owner that arrive in an interval are one coherent sum on the phase circle
of N steps; each of the six Ports sends out one third of that sum less the
arrival that came in through it, sent back; the amounts leaving are the
total arriving, shared among the six Ports by the squared sizes of their
sums in whole quanta, the remainder a shadow parked at the node, each share
at the phase of its sum. Nothing is declared: N is the one input. The split
table of Highlights 3.5 and the pairwise phase steering of point 17 are
retired for shadows; the steering table, computed from N as cos² of half
the phase difference in N-ths and rounded, serves a thing meeting a thing of
one family (points 4, 17).

**The push and the return (points 3, 15, 16, 23).** A shadow meeting a
thing: the thing takes the push the coupling declares, what it multiplies
the message by (its content for gravity, the owner's charge over its
content times its charge for electricity), and the shadow turns back with
the opposite sign: the same shadow, its heading reversed and its momentum
inverted, a field like any other from then on, mixing at every node, and
absorbed wherever it reaches its owner. There is no return walk: no step
counter, no trace, no chase; the recoil is delivered through the field,
globally, and the books close at every interval with that momentum in
flight. A thing meeting its own shadow is the same rule with a round trip
of zero. A push is not an event. A thing pays a tick for every whole
quantum it reads: in that interval it neither moves nor advances its phase;
a shadow pays nothing.

**Meetings and events (points 4, 5, 13).** A thing meeting a thing is the
declared table of Highlights 5.2; a shadow meeting a shadow is a sum of
phases that decides the heading, never an amount; events happen only at
nodes that hold a thing, and the GameBoard has two layers, the nodes that hold
a thing cycled in full and the nodes that hold shadows alone computed as
one step.

**The mark (points 6, 8, 14, 20).** A thing that arrives at a marked node
is absorbed into the mark's resident thing and counted, with its momentum,
or passes if the mark's declared coupling for its family says pass, and a
thing the mark misses is sent back on its steps to its birth event by the
mark's declared table (a thing has steps: it has one path and counts it,
the real counts and the shadow does not; the model owner, 2026-09-18); a
shadow is returned as at any thing and counted by nothing. There is no
lottery: what a mark "draws" is whether a 0 or a 1 arrived, decided at the
ray's birth and along its one path; an imperfect mark is a declared table,
and the seed is retired. A decay is a table on the group's own state, not a
draw. The only thing not known at a node is whether a 0 or a 1 comes next.

**The books (points 7, 11, 22).** Things conserve amount, momentum and
charge exactly among themselves, with no source line; shadows are free,
given with the GameBoard as initial content and never sourced; a source is a
thing that spends its content by an emission table; the books are kept per
bit. A node is its six Ports and holds nothing else: the remainder is a
shadow parked at the node, a mark's counter is a thing resident at the
mark, and the apparatus are things with declared tables. The world's
computation per interval is the sum of its things' content; shadows cost
nothing.

**Mass, clock and the shadow set (points 9, 18, 19).** A thing's content
is its mass and its clock: it advances its phase by content / K per
interval, one K for the world, and no family declares a rest rate; a shadow
has no clock and moves at the causal speed. A thing has one shadow set, of
size proportional to its content, read twice, by content and by charge;
the `mass_field` of the catalog is retired.

**A thing does not emit.** Its shadows are given with the GameBoard and
circulate: a shadow that comes home leaves again from where the thing now
is, nothing is created, and what escapes the GameBoard is the only loss.

**Lanes (point 25).** A Port is two lanes, in and out, twelve per node; in
one interval a lane carries at most one real ray and one shadow per owner.
There is no queue and no wait in this: a thing steps into a lane only if
the lane is free, otherwise it keeps its heading and steps at the next
node; a source always emits; two real rays of one family given one lane
are one real ray, their amounts, momentum and charge adding and their
owners kept as a set; two of different families are a meeting by the table
for the pair. The only wait in the world is the clock's (point 23).

**In one sentence.** Every action is a message that returns: 1 is what
there is, 0 is what is said; what is said returns, as a field, and what
there is stays.

The identities named below were deleted on 2026-09-19 with the engines before the
Beam Law (docs/MIGRATION.md); the law in force is the Beam Law, ALGEBRA.md
chapter 2.

**Implementation.** `bit-law-v1`, `node-mixing-v1`, `clock-readings-v1`,
`node-is-ports-v1` and `lanes-v1` (feature 18, the lanes of point 25) are
on `main`
(spatial fields);
the return as a field (point 3 as amended, in place of the walk on the
trace those features implement) is pending (history, superseded on 2026-09-19).

## 26. The Inside and the Outside

The model owner's word, 2026-09-23, 03:57Z, record 1242 (Hebrew, dictated;
the Boss's English): "Everything we say here goes into the postulates,
because it is very important later; and if it is contradicted, it must be
thrown out of there." The two words are defined in
[docs/TERMINOLOGY.md](docs/TERMINOLOGY.md#the-readings) ("Inside and
Outside", record 768): Inside is inside the GameBoard, the Nodes, the
integer rows and the tick, where no one measures; Outside is the game above
the board, the detectors and their clicks only, which is not reality but is
claimed to represent it. In each postulate the owner's statement comes
first, the Boss's reading after it where one is given and marked as his,
and the citations last. The records are in
[docs/LOG_2026-09-20.md](docs/LOG_2026-09-20.md) and their decisions in
[Highlights 5.4](docs/HIGHLIGHTS.md#54-the-detector); records 1242 to
1245 are cited by number. Where
[section 10](#10-measurement-and-display-are-outside-the-physics)
or sections [23](#23-the-ray-event-model),
[24](#24-everything-is-information-transfer-a-return-is-the-inverse-split-at-the-event)
and [25](#25-the-law-of-the-bit-the-thing-or-its-shadow) already say a
thing, this section cites them and does not restate. Section 23's phrase
"Outside a Detector" predates record 768 and means "away from a Detector",
not the Outside of this section.

**26.1 Nature's atomic clock.** The owner: nature's atomic clock, by our
definition, is a detector that reads a click and waits for the next click;
it must have mass, the held content of its own record; this is the law we
defined, and the laws of the clock are closed. The detector's own count
under the age wall is its time; its tick is the return of its own packet to
its held mass, at rest to the same Node and in motion to the next Node, one
rule for both; there is no second clock and no rate from outside. The
code's fact beside the owner's premise: the count needs a body, a measured
event (an open face has no clock of its own, docs/TERMINOLOGY.md, "A
detector's clock"; an open face is the border of an axis a world declares open,
ALGEBRA.md 1.6, a DECLARATION of the world file; the faces are the torus's unless
so declared, the model owner, 2026-09-23, record 1421; its click line's time is
GAMEBOARD), and the tick algebra finds the count's rate independent
of the held mass (docs/designs/new_rows/TICK_ALGEBRA.md, records 1248 and
1257). Records 678, 709, 1217, 1226, 1227, 1232 and 1234; section 10 (the click stamped with the detector's own count);
docs/TERMINOLOGY.md, "A detector's clock".

**26.2 What passes from the Inside to the Outside.** The owner: from the
Inside to the Outside the mass passes as it is: the row's record's content
in the family's units (docs/TERMINOLOGY.md, "Content": content on a body or
a row, the mass). By the code (the Tick Algebraist's paragraph,
docs/designs/new_rows/TICK_ALGEBRA.md, records 1248 and 1257, confirmed by
the code): the mass is one integer in one column, `content`,
in the family's units; a light packet carries the content of its own paid
family and never the emitter's held mass, which does not pass. What arrives
with a record and is read as it is: its content (the mass), its amount, its
label **p** (the momentum vector, its direction and its size), its phase,
its number and its own age (the click line, `nature_beam.py` lines 5536 to
5566; [ENGINE.md, the detector's readings by type](docs/ENGINE.md#the-detectors-readings-by-type):
the age of a row on the click line is a DETECTOR reading). The click's
time is the detector's own count and its place the detector's own Node;
what does not pass is the host's tick and any place but the detector's
Node. Record 1234 (the detector's mass and the Inside's mass are one
quantity in one record); section 10.

**26.3 The Outside has Nodes.** The owner: the Outside has Nodes as the
Inside has: the detectors' Nodes. The distance between two Outside Nodes is
the distance between the two detectors; the time of the passage from one
Outside Node to the next is the time between click and click, in the
detector's own count. Both are read by clicks: the distance as the chain
of clicks between neighbouring detectors (Locality Outside, DERIVATION.md
section 0) or as a packet's round trip in the detector's own count (record
1234). Records 1216 and 1234; the click theorem's
definitions (a click is a triple: the Node, the detector's count at the
arrival, what arrived; a velocity Outside is a ratio of two integers and
never a reading of the tick).

**26.4 The Outside is reached from the Inside only by clicks.** The owner:
the Inside is something we reach only by clicks. The Outside is the possibility that was fixed by
the actions coming in from the Inside: one realized possibility at a given
count of a detector, not always all the places; the Inside carries all the
possibilities that can be. The Boss's precision, marked as his: the Inside
is one deterministic state with many rows; there is no draw at a Node
(section 25, "The mark": there is no lottery; nothing at a Node, Highlights
item 2, record 155; the paper's P4 as a cross-reference); the fan carries
every declared direction (the fan's width a DECLARATION of the world, ALGEBRA.md
6.2 row 2a; under chapter 2.11 as rewritten on the branch algebra-chapter-2-11 the
splitting at every free Node carries every direction and the fan is gone); "all
the possibilities" are the rows that could
click, and the Outside is the subset that clicked. Record 1201 (no passage
Outside without a packet Inside); section 23 (every trajectory an
interaction permits happens, and the picture of the world is the list of
clicks; a history section since 2026-09-19, the standing statement ALGEBRA.md
3.1); section 25.

**26.5 No time in the Outside apart from the detectors' counts.** The
owner: there is no time in the Outside apart from the detectors' counts: no
fixed time and no global time, because everything can happen from different
things. The host's tick is a GAMEBOARD diagnostic and never the Outside's
time. Records 281, 1216 and 1217; docs/TERMINOLOGY.md, "The readings";
Highlights 5.4, the line of record 1196 (the time axis and the kind of a
reading).

**26.6 The Outside compared with Einstein's spacetime.** The owner: the
Outside is compared with Einstein's spacetime; what is compared with
Einstein's spacetime is determined from the Inside and read by clicks. The
click theorem
([docs/designs/click_frame/DERIVATION.md, section 0](docs/designs/click_frame/DERIVATION.md#0-the-click-theorem-the-owners-word-records-745-and-749-the-assumptions-the-theorem-the-proof-sketch-the-papers-frame))
gives Lorentz's form under its two assumptions together, A1 (a click
passes information at most one Node per interval) and A2 (a click's
content is an amplitude with a phase that splits each interval between
staying and hopping), up to a correction of relative order m^2 v^2 (m the
mass angle of the amplitude and v the velocity, as the theorem defines
them), exact in the continuum limit. The law as built meets A1 and not A2:
its rows hop whole and on the board no clock slows by motion
([docs/HIGHLIGHTS.md](docs/HIGHLIGHTS.md), the head, item 8; records 687
and 749), and the tick algebra finds that the law as built departs from
Einstein's form at order v^2 by the whole beta^2 term (beta the velocity
in units of c; the count rate 1 against 1 / gamma, gamma the Lorentz
factor), not by the theorem's residual (docs/designs/new_rows/TICK_ALGEBRA.md,
records 1248 and 1257). Whether the law as built matches Einstein's forms
is what the light clock reads, its pins
pending (records 1226 to 1235); until it passes, this postulate states the
comparison and no derivation. Einstein's forms are the thing compared
with: the law's result matches nature and is never said to be nature;
"compared with", never "is" (records 762 and 817; section 9 says the same
of Newton's and Einstein's equations). (Re-read on 2.11's landing: the bound
mode's clock reads 1 / gamma_m to first order in eps, gamma_m the Lorentz factor
of the medium's pace and eps the binding depth, MASSIVE_RECORD.md section 8 on
the branch detector-law-design.)

**26.7 Removal on contradiction.** The owner: if any statement of this
section is contradicted by a reading (a detector's click) or by a later
word of the owner, it is removed from the postulates with the record of
the contradiction cited; the log keeps the history (records 1242 and 1244:
what is outdated is deleted, its record staying in the log; the marking
rule of records 802 and 941 superseded). Nothing else in POSTULATES.md
changes by this section; where section 10 or sections 23 to 25 already say
a thing, they are cited instead of restated.

**26.8 The three levels.** The owner (2026-09-23, 04:04Z, record 1243,
and in his own words at 04:09Z, record 1245): there are three levels.
Level 1 is "what we see, what they measure": the experimenters'
measurements, the detectors' clicks. Level 2 is "Einstein: hard for a
person to see, but it predicts what we see very well": his event space,
his spacetime. Level 3 is "our level, the Inside, what we call the
GameBoard", from which level 2 follows. Level 2 is a model, not a datum,
so the paper's test is double (the owner, confirmed, record 1245): that
level 3 gives level 2's form, and that level 3's numbers, read by clicks,
match level 1, the comparison table. "Gives level 2's form" is read as the
comparison of 26.6, tested by the light clock: the click theorem gives
that form under A1 and A2 together, the law as built meets A1 and not A2,
and no derivation is claimed for the law as built until the light clock
passes. The light clock tests both at once: if it reads gamma squared and
gamma (gamma the Lorentz factor) where Einstein's forms read 1 and 1, the
claim that level 3 gives level 2's form, the double test's first half,
fails in its present form; 26.6, which states a comparison and claims no
derivation, then stands as a disagreement in the comparison table, and
26.7 is not invoked against it. Level 3 reaches level 1 only by clicks
(26.4); nothing
of level 1 is read from level 3 directly. Records 1216, 1220 (the three
levels named first there), 1243 and 1245;
[docs/designs/click_frame/DERIVATION.md, section 0](docs/designs/click_frame/DERIVATION.md#0-the-click-theorem-the-owners-word-records-745-and-749-the-assumptions-the-theorem-the-proof-sketch-the-papers-frame).
