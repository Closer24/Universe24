# The local detector law: the ray splits at every free Node inside the board, and nothing passes outside except through a detector (the chief physicist's design on the model owner's words of 2026-09-23, docs and pins only, no engine line)

The model owner's order through the Boss (2026-09-23, about 08:00Z):
"There is no field. Ask the physicist for the new design with the new
things that fixes the bugs you made." This document is that design, in
his terms. It replaces nothing yet: the engine at head is the ray law as
built (the pilot under (b), `docs/designs/event_split/PILOT.md`, measures
it as the baseline); the coin form of `docs/designs/event_split/DESIGN.md`
section 3.2 stays refuted (CORRECTIONS.md M11); this design is built
only on the owner's GO after Reviewer 3's gate and after its pins pass.
Every number below is a COMPUTATION of the script beside this file,
`detector_law_pins.py` (its output `detector_law_pins.out`), or a
declared integer; no engine ran; no pin of the register moves.

## 0. The owner's statements, verbatim (Hebrew, rendered), the terms as he corrected them

To the chief physicist, 07:50Z to 08:20Z, in order:

1. "Let us be precise on terms: we have Outside and Inside. The Inside is
   a ray that splits at every free Node and holds the amplitudes, right?"
2. "You cannot go between apparatus and apparatus. You cannot jump in the
   Outside. To go you must pass through a detector; it is a local law; you
   must jump to a Node through a detector. What you describe is in fact a
   moving detector. Did you understand the bug?"
3. "Confirm one critical thing: in the Inside the ray splits at every free
   Node and holds amplitudes; in the Outside, that is the detectors'
   world; there are no jumps between detectors; it is a detector that
   passes, a moving detector in fact, that transfers mass."
4. "Do not call it the board [in the Outside], because the board is the
   Inside; the board is not the Outside. In the Outside there is no board:
   it is clicks passing from Node to Node. And you cannot pass from Node
   to Node [except through a detector], exactly as you said."
5. "The detector transfers mass through the Inside. It does not transfer
   mass in the Outside; it transfers mass only through the Inside, and it
   pops up at the next Node, or it can also pop up at the same Node. If it
   pops up at the same Node, that is in fact a detector at rest. But it
   does it through the Inside, and this has a time. And that is also the
   detector's cycle time."

6. (09:03Z, on the design at 489fed62) "GO. Note that the slit and such
   are not in the Inside, they are in the Outside, right?" Confirmed: the
   slit's wall, the polariser, the screen and the lamp are declared things
   that read or emit, detectors, the Outside; only the free Nodes and the
   record's rows on them are the Inside; the opening itself is the absence
   of a wall, free Nodes, the Inside. His GO is the GO to build under the
   Boss's bounds (Reviewer 3's gate first; his word on the far-field pin
   of 6.1).

To the Boss, 07:49Z to 08:00Z (the Boss's rendering, records of
docs/LOG_2026-09-20.md after 1314): "Everything you are talking about are
things that happen in the Outside, above the board. They do not happen
inside the board. I meant that the ray splits inside the board, not above
the board." / "There is no such thing as a local lattice line, because in
the Outside you can only go through a moving detector. You cannot pass
between a detector and an emitter on a line on the lattice; there is no
such thing. It is only a moving detector. In the Inside it is a ray that
splits at every free point and holds the amplitudes if it arrived through
a detector." / "There is no field."

To the Boss, 08:04Z to 08:43Z (the Boss's rendering): "A ray splits at
all the possible points. A ray is in the Inside; there is no ray in the
Outside. In the Outside it is only clicks, and clicks move exactly with
mass." / [On the paragraph of record 1297, the generic weight:] "This
needs to go in, and take out the things that contradict it." / "A
detector or an emitter: it arrives at the same point and that is its
clock; if it does not move, that is its clock, because it receives and
inserts, or inserts and receives; that has a time, and it does it through
the Inside. Confirm the genericity of detector and emitter." / "The whole
digital ray and all sorts of clock counts are not relevant at all; every
detector has its own clock time, how long it inserts or receives, its
cycle time, determined by the Inside. The old engine is not needed." /
"Every measuring instrument you put on the board is defined in the
Outside; slits, a slit, all these things are never in the Inside. GO." /
"Nothing is inserted, nothing can be inserted, into the Inside. Every
instrument that is placed is Outside and must come with all the
definitions we have for how things are measured Outside. It must be a
simple Inside and a simple Outside; all the laws we have on the Inside
must run, everything local. The detector and the emitter have a trigger
that we closed, both. There are no other kinds for the board: there is a
detector and there is an emitter."

The terms, as he fixed them (POSTULATES.md section 26; docs/TERMINOLOGY.md
"Inside and Outside", record 768): **the Inside is the board itself**, the
Nodes and the Links, where the ray splits at every free Node and holds
its amplitudes, where no one measures; **the Outside has no board**, only
clicks, one click and then the next, and a passage from Node to Node in
the Outside happens only through a detector, at rest (the same Node) or
moving (the next Node), which transfers the mass through the Inside and
whose cycle time is the time that transfer takes. The records the Boss
names: 1046 (a moving detector as it should be, with mass; Newton from
the algebra of the clicks), 1139 (a detector performs an action when it
reads), 1227 (the pulse goes inside, hits and returns; a tick is the
packet returning to the same place), 1242 (nature's atomic clock is a
detector that reads a click and waits for the next), 1282 (the
amplitudes add at the Node, what comes from the six neighbours adds and
the event propagates), 1288 (the trigger, the weights and the pace as the
physicist's recommendations), 1293 (the external things with their own
clocks; a pilot of known worlds first).

## 1. The picture

A **record** is one quantum's story from its birth at a lamp to its
click at a detector (the amplitude law, `examples/events/amplitude/README.md`;
one click per record at completion). In the law as built the record is a
set of **rows on digital lines**: each row carries a direction label,
an amount, a multiplicity, a phase and an age, walks its Bresenham line
Link by Link at the flight table's pace, and splits only where a
declared thing stands (the lamp's fan, an opening's fan table, a
polariser's half-angle table). Between two declared things the row's
line is known in advance: that is the bug the owner names (his statements
2 and 4): the row passes the Nodes on its way without anything happening
to it there, a passage "above the board".

Under the local detector law the record is instead a set of **rows at
Nodes**: at every Node the record has reached there is one row of the
record, holding the record's amplitude at that Node now and one interval
ago (two integers on the wheel) and a remainder. Every interval every
such row does one thing, the same at every Node of the board: it
re-emits to its six neighbours what arrived from them, less what it
emitted the interval before (section 2). That is "the ray splits at
every free Node and holds the amplitudes": the split is the emission to
the six neighbours; the holding is the row's two integers for the one
interval they take to be re-emitted. Where two emissions meet at a Node
they add with their sign (the merge, verb G; the owner's decision of
record 1282: "what comes from the six neighbours adds and the event
propagates"). Nothing is stored at a Node beyond the record's own row
there; no direction, no line, no error accumulator; the direction of the
record's motion is what the six neighbours carry between them.

A **detector** is a Node whose row does one more thing: it keeps a sum
across intervals of the offer that arrives at it (the record's amplitude
squared, section 5), and when that sum crosses the rung of the record's
wheel the record clicks there. Only a detector keeps a sum across
intervals; a free Node keeps nothing across intervals but its own row's
two integers and remainder. The click is the record's end: its content
(one quantum) is handed to the detector, every row of the record on the
board is removed, and the click line is written with the detector's own
count (`clock_stamp`) and the record's birth stamp. That is the Outside:
the click, and then the next click. The moving detector of the owner's
statement 3 is this rule seen from the Outside: a detector at one Node
emits (its record's rows spread through the Inside), and the record
clicks at the next Node, or at the same Node (a detector at rest); the
mass moves only through the Inside, in the record's rows, and appears
Outside only at the click.

In his words (statement 6): everything declared, the slit's wall, the
polariser, the screen, the lamp, the mirror as a receiver body, is the
Outside, a thing that reads or emits; the Inside is only the free Nodes
and the record's rows on them. The far-field question of 6.1 is
therefore a question of how a wall is declared (an Outside thing), not
of the rule.

**Two things only, on the board.** In his words: there is a detector and
there is an emitter, and they are one generic thing, the
receiver-inserter, with three acts: it RECEIVES (a click: the record's
offer summed across intervals at its Nodes, the first rung), it INSERTS
(an emission: a record born at its Nodes, driven by its clock for its
train), and it has ITS CLOCK (its own count of round trips through the
Inside: from an insert to the receive of the same record, or from a
receive to the next insert; at rest at its own Node, in motion at the
next). Every named instrument is that one thing with its declarations,
Outside, in the world file: a lamp (inserts; how many, when and the
train are declarations, not a law), a screen pixel or a wall Node
(receives, read Outside or not read), a polariser (receives and inserts
with its table), a receiver body at the far end of a clock (receives and
inserts, never a mirror), a body (receives and inserts its own record
each cycle, section 8). No third kind exists; a slit is Nodes of a wall
(receivers whose detections are not read) around free Nodes. Nothing is
inserted into the Inside and nothing can be: the Inside is the free
Nodes, the record's rows on them and the one local rule; every
declaration lives Outside with the definitions we have for how things
are measured there (POSTULATES.md section 26, the click as the law's
action on the state, the detector's own count on the click line, the
birth stamp). The board's faces are not a third kind: an open face is a
declared wall that is not read (the record's offer leaving there is
booked as escaped, as today's faces), and a periodic world has none.

**How the one kind is declared and how its clock is read.** A measured
event with a body (`amount`, `held`, its family) and, for a receiver
that inserts, its family's clock [n, d] and its train (the lamp's
declaration, in periods); the detector sets of the world file name the
cells the receives are read into. Its clock is read on the click line
as the detector's own count (`clock_stamp`), and its cycle from the
birth stamp of the record it inserted to the click that received it;
the old engine's clock counts (the count of self-creations under the age
wall, the flight accumulator, the host's tick as a time) are not
carried: the cycle time is determined by the Inside, since what the
Inside holds along the record's way changes it (a crowd's stretched
pace, section 4.1).

What is NOT in the picture: a line on the lattice between an emitter and
a detector (the row's label **u**, its flight residue, its Bresenham
error accumulator **c**: gone from the free Node); a declared fan at an
opening (the opening is a hole in a wall: its Nodes are free Nodes, the
wall's Nodes are detectors that click and end the record there); a
"field" as a thing of the board beside the records (there is none: every
amplitude on the board is a row of some record, born at a lamp, ended at
a click; the board holds records and nothing else).

1.1 **The foreign object, in the owner's words (10:05Z to 10:20Z, to
the chief physicist).** "There is no such thing as a detector and an
emitter; each is both: a foreign object with known parameters (mass,
frequency, phase, place, a step in one of six directions, re-emission)."
"A foreign object always self-clicks; otherwise it does not exist
there." "The click is a local action of a Node on itself which produces
the amplitudes." "You cannot go diagonally." One kind, then, declared
Outside per object, with these parameters and no others (Reviewer 3's
MUST F, one declared kind):

| Parameter | What it is under the rule | Kind |
| --- | --- | --- |
| mass | the object's content M (`amount`, `held`), what its record hands over at a click | a declaration |
| frequency | its clock, the family's pair [n, d] on the circle of N steps, the record's period | a declaration |
| phase | the phase at which its train starts, the clock's zero (3 N / 4, the cosine 0 and rising) | a declaration |
| place | its Nodes on the GameBoard; a body of one Node or a line or a wall of Nodes | a declaration |
| step | one of the six directions and the count k of intervals per Link; a step is one Link, never a diagonal; k = 0 at rest | a declaration |
| re-emission | the pair p = [p_n, p_d] of what its Nodes re-emit of what the rule gives them (section 5, the three receiver forms; the mirror and the sponge) | a declaration |
| train | the length of one insert in periods of its clock (the record's coherence, 4.5) | a declaration |
| sensitivity | the rungs of the wheel one click needs, 1 (the first rung, the counting form) or 2 (the owner's "check 2 against 1", a computation pending) | a declaration |
| the cycle's closed count N_s | the intervals after its last insert during which it does not receive its own record (the cycle sentence, section 5) | a declaration |

Everything else the object has is read, not declared: its own count on
every click line (`clock_stamp`), its cycle (the count from an insert to
the receive of the same record), the direction of what arrives (the
gradient of the arriving offer's phase across its Nodes). The
self-click is the existence condition: every foreign object holds its
own record (its body's record at its period, section 8), inserts it and
receives it at its own Nodes each cycle, and an object whose own record
never returns its first rung at its Nodes is not on the board (its
declaration is refused at load when its Nodes cannot receive, and its
books show the record escaped when it leaves by a face). Under the rule
a one-Node object at rest in open space has no return (Reviewer 3's
MUST H: the wave spreads and does not come back), so its self-click at
rest is its declared period (its cycle N_s with no receive from the
Inside), the light clock's return (a body and a receiver body at L) is
a two-body cycle, and section 8 is to be rewritten in the owner's words
on that basis (the pass, item H; not done in this commit).

What is refused with the one kind, by the Algebra Auditor's rows
(ALGEBRA_AUDIT.md at c848aad0 on `algebra-inside-outside`): a record
`in_transit` between two objects without rows on the board (there is no
Outside passage: the mass moves only through the Inside, as rows); a
face that is neither a declared wall nor periodic; a "become" of an
object triggered by anything but its own cycle; a moving object's step
by anything but the first rung of its own record at the next Node, one
of six. Each refusal is a load-time check of the world under the key
(section 11, step 1).

## 2. The rule, in integers, and its three tests

**The rule.** The world's pair `c2 = [1, 3]` (the exact square
`W = E'_0^2 + 3 p . p`, DERIVATIONS_BEAM 17.6; the pace c = 1 / sqrt 3
Links per interval) is the only constant. A record's row at a Node holds
`a_now`, `a_before` (integers on the record's wheel, the amplitude unit
2^20 in the pins script) and `r` (0, 1 or 2). Every interval, at every
Node with a row of the record:

    3 a_next + r' = (a_E + a_W + a_N + a_S + a_U + a_D) - 3 a_before + r,   0 <= r' < 3

where `a_E .. a_D` are the record's `a_now` at the six neighbouring
Nodes (0 where the record has no row yet; a world periodic in z of one
layer takes `a_U = a_D = a_now`); then `a_before := a_now`,
`a_now := a_next`, `r := r'`. In words: the Node re-emits the sum of
what its six neighbours held, less three times what it held the
interval before, and keeps the division's remainder on the row. The
subtraction is what makes the amplitudes cancel: without it the rule is
the copy rule of CORRECTIONS.md M10 (a Node copies what arrives), a
diffusion whose norm explodes and whose front has no phase; with it a
Node that emitted last interval takes back what it emitted, so that only
the difference travels, and a train of the record's clock moves at c on
the lattice with the phase it was born with (section 6, A: the pace by
direction 0.992 to 0.999 of c at lambda >= 12 Links). In three
dimensions with the pair [1, 3] the middle term is exactly zero (the
continuum's 2 - 6 c^2), so the rule has no coefficient but 3.

**The source.** A lamp is a measured event with a body (as today); a
birth is the record's row created at the lamp's Node with `a_now = A`
and thereafter driven by the record's clock for the record's train:
`a_now(t) = A cos(2 pi t n / (d N))` at the lamp's Node for `T_train`
intervals, the clock the family's pair `phase_per_link` [n, d] on the
circle of N steps as declared today, the train's length in periods a
declaration of the lamp (kind 1, section 4.5: the record's coherence).
The lamp's `turns` per direction (the fan's phases) have no meaning here
and go; a lamp that must emit in a direction (a beam) is a lamp whose
body is a line of Nodes driven in phase (a plane source), as the pins
script drives an opening's Nodes.

**The three tests** (skills/workflow.md, "The three tests of every rule"):

- Generic: one primitive (the six-neighbour sum less three times the
  row's past, the pair [1, 3]), no family name, no kind; a family's clock
  [n, d] and quantum h enter only at the source and at the click; a
  massive family is the same rule read at its own period (section 8);
  the engine branches on no name. PASS.
- Vector: two of the six verbs, the group-ring addition over the six
  neighbours (G) and the Euclidean division by 3 with the remainder kept
  (D); no root, no float, no rounding beyond D, the amplitude unit and
  the wheel declared at load. PASS.
- Local: the rule reads the record's own row at the Node and at the six
  neighbours (LOCALITY-1), fixed work and storage per Node per record for
  a fixed K (three integers and six reads), nothing kept at a Node beyond
  the record's own row (the remainder is the row's, not the Node's), the
  detector's sum the detector's own record's (a measured event's book, as
  today's pointer per set). PASS.

2.1 **The norm the rungs divide is the rule's conserved form, not the
sum of the squares** (Reviewer 3's MUST A). Written with the middle
term, the rule is `a_next - 2 a_now + a_before = (1 / 3) (a_E + .. + a_D
- 6 a_now)`, the leapfrog of the wave equation at c^2 = 1 / 3. The
leapfrog conserves exactly (before the remainder) one quadratic form of
the two amplitudes, the discrete energy

    E = 3 SUM over Nodes (a_now - a_before)^2
        + SUM over Links (a_now(x) - a_now(y)) (a_before(x) - a_before(y))

in the amplitude unit squared (the factor 6 chosen so that E is an
integer), the first sum the MOTION of the rows (each Node's change in
one interval), the second the STRAIN across the Links (the product of
the differences on a Link now and one interval ago). With the remainder
kept (verb D) E is conserved to the grain of the remainder, one unit
per Node per interval at most (COMPUTATION: a drift of 2 x 10^-4 of E
over 200 intervals on a 24 x 24 periodic layer of random rows, exact in
the rational form), and this is what the books read; the
form is positive when c^2 < 1 / 3 in three dimensions and it is
positive-semidefinite exactly at the pair [1, 3]: the mode it does not
bound is the checkerboard (the six neighbours the sign opposite of the
Node, the zone's corner), which the rule holds at a constant amplitude
without growth; in the z-periodic one-layer worlds of the pins script
the bound is strict (four neighbours). The record's norm, what the rungs
of the wheel W divide, is its E at the end of its insert (the train's
motion and strain, an integer of the lamp's declaration), and the
click's first rung is 1 / W of it.

Why `a^2` fails, in a paragraph: the sum of the squares of the
amplitudes is not conserved by the rule. A static level on the board
(every row of the record at the same amplitude, a_now = a_before) is an
exact solution of the six-neighbour rule with E = 0: it has a^2 at
every Node and does nothing, carries nothing and clicks nowhere; a
receiver that summed a^2 would count it, and the pins script's first
runs did (the level left behind by a train starting on a step, the
build's first chain: the sum never decayed and no record completed).
A travelling train's SUM a^2 also oscillates within each period between
the motion and the strain (the two sums of E exchange their content
every half period, as a pendulum's), so a rung crossed by a^2 at one
interval is uncrossed at the next, and the click's time by a^2 is not
the front's arrival but a beat of the train against the wheel. E has
neither defect: the static level is zero in it, and a travelling train
carries a constant E whose motion part is what a receiver's Port can
take in an interval (section 5: the offer is the Port's motion). The
build measured the difference on the chain: with a^2 no completion; with
the motion the click at the front's first rung and the books balanced.

The one non-local step, named (the Algebra Auditor's row "LOCAL EXCEPT
the completion of a record", ALGEBRA_AUDIT.md at c848aad0): the record
completes when its offer has been exhausted into receivers or has left
the board, and only the host knows the sum over the board of the
record's remaining motion; every Node's step, every Port's take and
every first rung is local. That step is the amplitude law's own
(event_split DESIGN.md section 4, the exhaustion), unchanged, and it is
the host's cost of section 7, not a physical dependency of any Node.

## 3. The new things of 2026-09-23 that the design carries

- **The detector's own count on every click line** (`clock_stamp`, the
  key of PR #834, on main): unchanged; the click line carries the
  detector's count at the click.
- **The birth stamp** (`origin/birth-stamp` 90ab27fc, the light clock's
  gate 1): the birth line carries the lamp's count; a record's cycle
  (section 8) is read from the birth stamp to the click's clock.
- **The trigger in the counting form** (record 1288; DESIGN.md section 4
  of event_split): a detector's cell accumulates the record's offer; the
  click when the accumulation crosses the rung on the wheel W = 4096 at
  the sensitivity s_D = 1 / W; no sensitivity key (the default, and no
  other value, section 4.3).
- **Equal weights and the merge** (records 1282 and 1288): the six
  neighbours weigh equally in the sum; amplitudes meeting at a Node add
  with their sign. The rule is the merge.
- **Inside and Outside** (POSTULATES.md section 26): the rule is the
  Inside; the click line is the Outside; nothing else crosses.
- **The three tests** (section 2) and **the pins before any run**
  (section 6).

## 4. The bugs we made, each named, and what replaces it

4.1 **The row on a digital line as the primitive** (the label **u**, the
flight table T_D, the Bresenham line, the error accumulator **c**;
BEAM_LAW.md, `nature_beam.py` the walk). Not relevant, by the owner's
word of 08:22Z, and owed no justification: the design does not carry
it. One line on what remains: the pace c = 1 / sqrt 3 is the pair
[1, 3] inside the rule, the only constant; the flight table is not
needed for it. The direction is only a READING at a detector, the
gradient of the arriving offer's phase across the detector's Nodes (the
momentum the click hands over, section 5), never a thing carried by a
row. The one-wall function (`age_wall`, f = 1 + gamma) and the push
(`optical_turn`) act today on a row's flight and label; under the rule
there is one place for the wall and it is a coefficient on the rule
(Reviewer 3's MUST E, the coefficient form): at a Node whose crowd has
the age moment A, the six-neighbour term is taken with the pair

    q = [d^2, (d + f n A)^2],   the step

    3 (d + f n A)^2 a_next + r' = d^2 (a_E + .. + a_D)
        + 6 ((d + f n A)^2 - d^2) a_now - 3 (d + f n A)^2 a_before + r,
        0 <= r' < 3 (d + f n A)^2

(verb T with the pair, then D with the remainder kept; the middle term
returns so that the row stays continuous, and at A = 0 the pair is
[1, 1] and the rule of section 2 returns unchanged). That is the rule's
step taken at the stretched rate d against d + f n A, the same
coefficient as the one wall, and it makes the crowd a medium of index
n_c = (d + f n A) / d for a splitting record: the train's front bends
toward the slow side (the time part of the bend, the phase), and a
gradient of the index across a packet is a force on it (the push), both
from the one coefficient, no second verb. On that reading the owner's
"W and not P" of 07:00Z holds under the rule: the wall alone carries
both parts of the bending, and Form W of CORRECTIONS.md M9 is answered
by the coefficient. What decides it is the computation of 6.6 on row
13's worlds (the bend -3.989 at gamma 1 from the coefficient alone, or
only the time part's -1.993); it is named there and not run.

4.2 **The split only at declared apparatus** (the lamp's fan of
directions with turns, the opening's fan table with angle weights, the
polariser's half-angle tables, the mirror's rerelease): instruments above
the board. Replaced: the lamp's fan by the source's train (section 2);
the opening's fan by nothing (an opening is a hole; the wall's Nodes are
detectors that end the record); the mirror by a receiver body's
re-emission (CORRECTIONS.md M4, the owner's "the receiver body never a
mirror", record 1227) driven by the record's clock at the arrival's
phase. Still needed, shown: the polariser's half-angle tables are a
DETECTOR's rule (what a polariser does to the record it reads: a click
into its own family's label with the table's weight, a re-emission with
the table's rotation), not a free Node's, and stay as declared on the
measured event (Malus, section 6.3).

4.3 **The sensitivity key** (`sensitivity` on a detectors entry,
event_split DESIGN.md section 4): gone; the counting form at s_D = 1 / W
is the only trigger; a detector that is less sensitive is a detector
with a larger body (more Nodes summing) or a coarser wheel, both
declared things, not a key.

4.4 **The coin** (a copy rule at a free Node, M10): a diffusion in the
copy form, speckle in the unitary form, refuted by its pins (M11). What
cancels in the new rule: the subtraction of the row's own last emission
(section 2). At which wavelength the lattice carries the bells: section
6 (B): at lambda = 12 Links the single opening at the Fresnel number 1.45
reads 0.946 against the exact sum 0.917 (inside 22.2's band), at 16 Links
0.930, at 24 Links 0.920; the pixel-to-pixel roughness 0.02, 0.013,
0.006 (no speckle); the dispersion stated in section 6 (A): the phase
pace by direction within 0.8 percent of c at 12 Links, 0.4 at 16, 0.2 at
24; the registered 4.654 Links is not carried (section 7).

4.5 **The two energies of light untied** (CORRECTIONS.md M9: the label's
e_D = 111 against the clock's 3 h n / d = 24; Reviewer 3's code point of
07:52Z that a born row's content is quantum x turn, so the quantum drops
out of any tie on the row form). The owner's rule (the paragraph of
record 1297, ordered in at 08:07Z with the contradictions out): **the
weight of a row in the law's push is its energy in content units, one
sentence for every family**: a body's content M as today, a free-rate
family's equivalent content M_eq = 3 h n / (Q S_w d) per unit, a rational
formed at load from the family's declared clock [n, d] and quantum h,
no root and no division at run time; `energy-weight-v1`, on by default.
Under the rule there is no label stored and no row energy on the
headings, so light has ONE energy, h f by its clock, and its weight in a
push is M_eq: at the design's clock of 12 Links (n / d = 3.08 at N = 64,
h = 1, Q = 64, S_w = 1) M_eq = 0.144 content units per unit; a push
exists only where a crowd acts (4.1, the stretched pace; 6.6), so the
weight enters there and nowhere else. E = p c holds by the rule's own
dispersion (the momentum a click hands over is h times the wave number
read from the arriving offer's phase gradient), to the lattice's 0.2 to
0.8 percent; no second energy of light remains anywhere, and neither tie
of the row form (the physicist's h = 5 and 22 / 3, Reviewer 3's label
14) applies. What the sentence removes, each named: light's push weight
read off the momentum label (content x e_D, e_D = isqrt(3 u . u),
`unit_weights`, `optical_turn`, BEAM_LAW note 35, one_wall/NOTE.md); the
rule "light's content is 0" as the weight of the turn (light's content
is h, 1 today); any weight of a free row that is not its energy in
content units; N5's status as a balance withdrawn (the quantity
3 h n / (Q S d) is M_eq, a definition on the law, not a balance to be
met; the loader's `off_identity` diagnostic becomes the computation of
M_eq at load, the refusal under `books` gone). The places in the record
that say otherwise are listed for the Boss's pass (the physicist's
report of 09:20Z), not here.

4.6 **The reader's script modelling the apparatus split differently from
the engine** (CORRECTIONS.md M11 item 1, section V of split_pins.py: a
turned row's residue). Under the rule there is no residue and no turned
row; the pins script runs the same integers the engine would run
(section 6), so a reading of the script IS a reading of the rule; what
the script still assumes above the rule is named in section 6.0.

## 5. The click and the books

**The offer.** At every Node, every interval, the record's row has an
offer, `a_now^2` (in the amplitude unit squared). A free Node does
nothing with it. A detector (a measured event with a body, as today: a
screen pixel, a wall Node, a face, a polariser) adds the offer arriving
at each of its Nodes to the record's pointer for that detector's set
(the pointer per set of the amplitude law, `amplitude.rungs` and
`cell_of`), the same number at every Node whether or not anyone reads it
(the owner's statement 5: a detector is a Node whose count is read
Outside).

**The trigger.** The counting form (record 1288): the record's total
offer is its norm (the birth's A^2 times the train's length, in the
unit); the rungs on the wheel W = 4096 divide it; the record completes
when its offer has been exhausted into detectors (the sum of the
pointers reaches the norm less the grain, the exhaustion of event_split
DESIGN.md section 4, the click's one non-local step, the host's, as
today) or when its train and its rows have left the board (an open face
is a declared wall that is not read, the offer leaving there booked as
escaped, section 1); at completion the click's cell is chosen by
`cell_of` over the pointers, one click per record, as today. The click's TIME under this
form is the interval at which the pointer of the chosen cell crossed its
first rung (s_D = 1 / W), the front of the arriving offer, not its
centre: section 6 (D) reads the detector at rest by this rule and finds
N_0 = 206 at every wavelength tried, the ray law's pin.

**The cycle sentence** (the owner, 10:12Z: "the detector's cycle time
is the time from its insert to its receive through the Inside";
Reviewer 3's MUST B, closed by this sentence only). A foreign object in
one interval either inserts or receives, never both: for the length of
its train it inserts its record at its Nodes and its Ports take nothing
of that record; for N_s declared intervals after the last insert its
Ports still take nothing of that record (the tail leaving its own Nodes
is not an arrival, and a Port that booked it would click the object on
its own emission); from then on its Ports take, and the record's first
rung at the object's Nodes is its receive. Its cycle is the count of
intervals from the first insert to that receive, read on the click line
as the detector's own count less the birth stamp; the next insert
starts a new cycle. N_s is the object's declaration (1.1; the build's
"grace" of two periods is one value of it), not a constant of the law,
and it is refused when smaller than the train's own leaving time at the
object's pace. The three tests: generic (one declared integer per
object, no family name, no kind); vector (a comparison of the record's
age, the row's own counter, against the train's length plus N_s, no
arithmetic on the state vector); local (the object's own record's age
at its own Nodes; nothing kept at a Node beyond the record's row and
its age, which the record already carries).

**The three receiver forms** (Reviewer 3's MUST C and the correction of
09:33Z: zero re-emission is a mirror, not an absorber). What a wall,
a screen, a body or a face DOES to the record's row at its Nodes is one
of three declared forms, and the world file names the form per object
(its re-emission parameter, 1.1):

- **The mirror**: the Node's row is held at 0 (or, in the coefficient
  form of 4.1, the six-neighbour term's coefficient q is 0: a body of
  infinite mass, the index infinite, the boundary's Fresnel step
  ((n - 1) / (n + 1))^2 equal to 1). The wave returns with its sign
  reversed; nothing is booked. The pins script's "zero wall" is this
  form (6.1: 0.842 at 24 Links, Rayleigh-Sommerfeld's first-kind sum,
  which is the wave's own sum through an opening in a mirror), and the
  build's chain measured 30 percent of a packet's motion returned by
  it. A large mass declared as a wall is therefore derived, not a
  fourth form: it is the mirror by the coefficient of 4.1.
- **The sponge**: a graded run of the object's Nodes, about a wavelength
  deep, whose rows take the rule's step and then re-emit the pair p of
  it (verb T, the pair per depth declared, p rising from near 1 at the
  face to 0 at the back), the part not re-emitted booked to the object
  as absorbed (the offer), so that at every Node the step in the index
  is small and the Fresnel reflection at the face is the product of many
  small steps. The pins script's "lossy 6-Node body" is this form (6.1:
  0.814 to 0.857; the reflection it did not remove is the difference
  from the mirror's sum). A wall that reads (a screen, a wall Node
  whose set is read) is a sponge whose absorbed offer is booked to its
  set; a wall that does not read is the same sponge with nothing read.
- **The Port's take**: one amplitude per Port facing a free Node,
  following the wave one way, g(t + 1) = a_f(t) + k (a_f(t + 1) - g(t))
  with the declared pair k = [-15, 56], the build's choice (section 11),
  0.07 percent reflected on the chain. It is a one-Node sponge in effect
  and cheaper by a wavelength of Nodes per wall; it is the design
  decision put to Reviewer 3 whether the engine carries it beside the
  two forms above or the sponge alone.

A face of the board is one of the three forms too, declared: an open
face is a sponge that does not read (its absorbed offer booked as
escaped), a closed face is a mirror, and a periodic world has none.

**The content and the books.** The record's content is one quantum h,
one entry in the record's ledger from the birth (the lamp pays h at the
birth as today, `cost = quantum x turn`, the turn 1) to the click (the
detector receives h); it is never at a Node and never split: the
amplitudes are the record's bookkeeping numbers (the shares of ONE
quantum's arrival), not content. The books balance as today: content in
transit until the click, then measured (`measured_content`,
`transit_content`); the rows on the board at the click are removed
(their amplitudes are not content and are not booked). The collision
rule (the meeting, M5) reads the crowd's moments from the records' rows
at a Node exactly as it reads them from rows today: the amount of a
record at a Node is its offer's share of its norm, a rational the crowd's
moments take in the unit (a declared rounding at load, the grain); the
push on a massive record's rows is the stretched pace of 4.1.

**The detector's own count and the birth stamp.** The click line carries
the detector's count (`clock_stamp`) and the record's birth stamp; a
record's cycle (section 8) is their difference in the detector's own
count when the detector is the emitter (a detector at rest or moving,
the owner's statement 5).

**Bounded integers, fixed local work.** Per record per Node: two
amplitudes (at most A x the train's length, the birth norm's square
root, within int64 at A = 2^20 and trains to 2^11 intervals), one
remainder, six reads and one division per interval; the host's cost per
record is its rows' count (section 7).

## 6. The pins before any build (COMPUTATION; `detector_law_pins.py`, `detector_law_pins.out`)

6.0 **What the script is and assumes.** The rule of section 2 on a 2D
z-periodic board in int64 with the remainder kept, exactly the engine's
integers; the source a line of Nodes driven by the record's clock for a
train of 32 periods (the coherence, a lamp's declaration); the wall
either of Nodes holding amplitude 0 (reflecting) or a lossy body of six
Nodes (a wall that takes the offer), both computed in 6.1; the reading at
the screen the accumulated offer per pixel over the window from the
train's first arrival until the train has passed the farthest pixel, with
the far edges beyond that window's light cone (nothing reflected enters
the reading); the clicks of 4096 births fall in proportion to the
accumulated offer under the counting trigger, so the offer per pixel IS
the pattern of the clicks. The pilot's worlds are scaled by lambda /
4.654 in every length (w, L, the screen's height), which keeps each
world's Fresnel number and its angular bell. The falsifier of every pin
is the band it is read against.

6.1 **The single opening** (row 10; RUN_10.md; 22.2's bands): at the
Fresnel number 1.45 (the w = 27 world: w = 70, 93, 139 Nodes at L = 278,
371, 557 Links for lambda = 12, 16, 24) the rule reads w x FWHM / lambda
= 0.946, 0.930, 0.920 against the Euclidean exact sum at the same
geometry 0.917, 0.916, 0.916 (isotropic emitters, the pilot's pin's
form, and with the obliquity cos theta alike: at this Fresnel number the
two agree) and 22.2's band 0.92 +- 0.03: INSIDE at all three, converging
on the exact sum as lambda grows (the residual 3, 1.5, 0.4 percent, the
lattice's). At the Fresnel number 0.16 (the w = 9 world: w = 23, 31, 46
Nodes) the rule reads 0.872, 0.856, 0.842 against the isotropic exact
sum 0.872 and the obliquity sum 0.842 (Rayleigh-Sommerfeld's first
solution, an aperture in a screen of amplitude 0): the rule converges on
the OBLIQUITY sum as lambda grows, which is what a wave through a hard
screen does; 22.2's band 0.886 +- 0.03: inside at 12 Links, at its edge
at 16, OUTSIDE at 24 (0.842, below the refuting bound 0.85). The pin as
declared: the rule's far-field bell must read inside 22.2's band with
the ENGINE's wall (a wall that clicks takes the amplitude). Computed,
the same run (the script's `wall = "lossy"`: the wall a body of 6 Nodes
on the source's side losing a quarter of its amplitude per interval, the
opening's line free, no Node of amplitude 0 beside the wave): 0.857,
0.830, 0.814 at lambda = 12, 16, 24, LOWER than the reflecting wall's
and further from the band. So, as the pin stands, the far-field single
slit at w = 2 lambda is a MISS of the rule: 22.2's 0.886 is the far
field's sinc constant for isotropic emitters (RUN_10.md, "nature's
0.886"), and a wave through an opening two wavelengths wide, in any
screen the rule can hold, carries an obliquity that narrows the bell by
4 to 8 percent. THE PIN IS THE OWNER'S WORD (asked by the Boss at
08:47Z with the physicist's recommendation, labelled so): either the pin
at w = 2 lambda is re-declared against a measurement of a slit that
narrow (the sinc is Fraunhofer's approximation, not a datum) or against
the wave's own obliquity sum (0.842), and then the rule reads inside; or
the owner keeps 22.2's band as the pin, and then the rule fails row 10's
far-field half at 16 Links and beyond and the design returns here. The
physicist's recommendation, not a decision: re-declare at w = 2 lambda
against the wave's exact sum (Rayleigh-Sommerfeld, 0.842 +- 0.03), keep
the near-field pin, and add a sinc pin in a world where Fraunhofer's
approximation applies (about w = 8 lambda). Nothing in the register's
pins is re-declared by this design. The near-field half (the Fresnel
number 1.45) is inside the band with either wall. The
pixel-to-pixel roughness near the peak 0.02 to 0.001: a bell, no speckle
(the coin's 0.8 to 1.0).

**The datums' kinds, before the pins.** Rayleigh-Sommerfeld's sum and
Fraunhofer's sinc are COMPUTATIONS of wave optics (the exact sum
through an opening in a mirror; its far-field limit), not readings of
nature: a pin against them is a check of the rule against the wave
law, and it says nothing about nature until a nature row is named. A
nature row for a single opening needs a named measurement with its
medium and its polarisation (the obliquity of the first-kind sum is the
polarisation's); none is at hand for a slit two or eight wavelengths
wide, and the register's row 10 carries none either. The recommendation
for the pins table (the pass, item G): a nature row at w = 4 lambda and
L = 100 lambda, where the far field is reached and a slit measurement
can be named, with the medium and polarisation columns filled; until
then (a), (b) and (c) below stand as COMPUTATION checks, so labelled
in the table.

**THE PINS AS DECLARED, on the owner's word of 10:05Z** ("declare the pin
again, because we are now in the right place"; his word to the chief
physicist directly, reported to the Boss at 10:10Z): (a) the single
opening two wavelengths wide (the Fresnel number 0.16): w x FWHM /
lambda = **0.842 +- 0.03**, the wave's own exact sum through an opening
in a wall of amplitude 0 (Rayleigh-Sommerfeld's obliquity), in place of
the sinc constant; the rule reads 0.872, 0.856, 0.842 at 12, 16, 24
Links with the reflecting wall, INSIDE at all three, and 0.857, 0.830,
0.814 with the lossy body (inside at 12 and 16); the falsifier a reading
outside 0.812 .. 0.872 at the engine's wall. (b) The near-field opening
(the Fresnel number 1.45): **0.92 +- 0.03**, kept; the rule 0.946,
0.930, 0.920, inside. (c) A new sinc pin in a world where Fraunhofer's
approximation applies, an opening of about eight wavelengths: **0.886 +-
0.03**, the far field's constant, where the rule must read it; not yet
computed by the script (the next computation of 6.1). Nothing in the
register's old pins moves; these are the new law's pins, before its
first engine reading.

6.2 **The two slits** (row 2a; the registered 0.966 in the clicks at
the fan's grain; nature's 0.98, Grangier, Roger and Aspect 1986 as the
lower bound; the ideal 1): the visibility over the two-source cosine's
bright and dark pixels 0.9588, 0.9576, 0.9575 at lambda = 12, 16, 24 with
the train 32 periods (0.845, 0.759, 0.691 with the train 8 periods, the
first run of the script): the number is set by the record's TRAIN, the
coherence length c x train against the path difference at the outer
fringes (3 lambda at the third fringe: a rectangular train of 32 periods
loses a tenth there), not by the lattice: nature's 0.98 needs a train of
about 128 periods (the path difference a fortieth of the coherence), a
declared integer of the lamp. The pin as declared: at the train the lamp
declares, the visibility over the same pixels must read at or above the
value the train's coherence gives, 0.96 at 32 periods, 0.99 at 128; the
falsifier a reading below 0.95 at 32 periods, or a reading that does not
rise with the train. This is the first row the rule could PASS against
nature: the fan's grain, the cause of the registered FAIL, has no
counterpart here.

6.3 **Malus** (the registered 128 and 128 at 45 degrees; nature's cos^2):
the polariser is a detector with the half-angle tables (4.2); under the
rule the record's train arrives along the 7-Node line and the polariser
reads it as today; the pin 128 and 128 stands unchanged and is not the
rule's to move; the script does not run it (a one-line world reads the
tables, not the rule). Bell's S on the re-arranged bars (CORRECTIONS.md
section 7's re-arrangement): a pair record is two records with one
birth stamp and opposite trains; the bars are polarisers; the pin is the
tables' S as registered; the rule's part is only that both trains reach
their bars, a computation to add after 6.1.

6.4 **The detector at rest** (the light clock's N_0 = 206 +- 2 at L = 60,
light_clock_pins.out on `origin/light-clock`; the owner's statement 5):
the light clock's world is a chain (320 x 3 x 3, periodic in y and z),
so the rule is the one-dimensional chain 3 a_next + r' = a_E + a_W + 4 a
- 3 a_before + r. A train of 2 periods sent from the detector's Node to
a mirror 60 Links away and back: the returning offer's centre reads N_0 =
223, 221, 221 at lambda = 12, 16, 24 (the packet's centre; the chain's
group pace at these clocks 0.564, 0.570, 0.574 against c = 0.577, so
2 L / v_g = 213, 211, 209, the rest the short train's spread); but the
counting trigger clicks at the FIRST rung of the returning offer (section
5), the front, and that reads 185.0 + 21, 178.5 + 27.5, 164.5 + 41.5 =
**206.0 at every wavelength**, the ray law's pin exactly, the emission's
click at the train's start. The pin as declared: N_0 = 206 +- 2 by the
first-rung click; the falsifier a first-rung reading outside 204 .. 208
at the lamp's declared train, or a dependence on the train's length
beyond the band. Reviewer 3 is asked to check that the front's pace on
the chain is c independent of the clock (a precursor at the lattice's
front speed), which is why the reading does not move with lambda.

6.5 **The moving detector** (the light clock in motion, N_par and N_perp;
row 4a; docs/designs/moving_detector): the same chain with the detector's
body and its mirror moved one Node every k intervals along +x (k = 3,
beta = 0.577), the train emitted from the body's Node as it moves, the
return read at the body's Node where it is now by the first rung
(section E of the script). At lambda = 24 Links it reads N_par = 303
against the branch's whole-tick pin 307 +- 10 (INSIDE) and the classical
medium clock's 2 L gamma^2 / c = 311.8; the ratio N_par / N_0 = 303 /
206 = 1.471 against gamma^2 = 1.5 and the pin's 1.490: the rule reads
the lattice as a medium, as the ray law does, so row 4a's registered
FAIL against Einstein's 1 (the proper time) stands under the rule as
read in the lattice's intervals, and the detector's own count remains the
only place the dilation can be read (the moving detector's design). At
lambda = 12 and 16 Links the reading (62 and 86) is not a return at all:
the two-period train's slow components (the lattice's modes near the
zone's edge, whose group pace is small) linger behind the front and the
body moving at a third of a Link per interval overtakes them, so the
first rung fires on the train's own tail; a longer train or a wavelength
of 24 Links or more is needed for a moving body, a price of section 7,
named. The across arm (N_perp) is not computed. The owner's statement 5
as a derivation (a record that must click at the NEXT Node accumulates
its first rung later) is not attempted here: the lattice's medium clock
is what the rule reads; the dilation is the detector's own count's.

6.6 **Row 13, the bend at a crowd** (-1.993 pixel at gamma 0, -3.989 at
gamma 1, the run of record 1216): under the rule the crowd's age moment
stretches the pace at the Nodes it fills (4.1); the train's front bends
toward the slow side by the wall's coefficient alone; the pin is the
time part's -1.993 at gamma 0 and 1 + gamma times it at gamma 1 if the
stretched pace carries both parts, the design's open computation on the
pin worlds (`examples/events/optical/`) scaled to the lattice's
wavelength; the script does not run it yet. If the bend reads the time
part alone (about -2.0 at gamma 1 too), the second half is a separate
verb after all and the owner's "W and not P" is answered "P is needed";
if it reads -3.99 at gamma 1, the wall alone carries both parts and no
push is needed on a splitting record. Named, not promised.

## 7. The price

- **The wavelength.** The lattice carries the bells at lambda >= 12
  Links (6.1); the registered 4.654 Links is not carried (the coin's
  speckle of M11 is the ray law's wavelength on a lattice). The family's
  clock becomes [n, d] with the period 12 sqrt 3 = 20.8 intervals or
  longer (the rate n / d = 64 / 20.8 = 3.08 steps per interval at N =
  64, against the registered 8.0).
- **The worlds' scale.** Every length of a light world scales by lambda
  / 4.654: at 12 Links by 2.58 (the single opening 120 x 161 becomes
  about 310 x 415 in the pins' geometry, 6.7 times the Nodes; the two
  slits 60 x 121 becomes 155 x 312), at 16 Links by 3.44 (12 times the
  Nodes). The register's light worlds are re-declared at the scale, the
  bodies' worlds unchanged in geometry.
- **The host's cost.** A record's rows are the Nodes its train has
  reached: in 2D at 12 Links about 3 x 10^4 to 1.3 x 10^5 Nodes per record,
  three int64 each (0.7 to 3 MB); records alive at once about 2.6 x 260
  = 700 (one birth per interval, a record complete in about 2.6 x 260
  intervals), 0.5 to 2 GB per world; the work per interval the
  six-neighbour sum over the live rows, vectorised, 0.5 to 3 s per
  interval; the intervals 2.6 x 4700 to 8800: the single opening about 3
  to 8 hours per world on this machine (the pilot's 2.7 hours for w = 9
  today), the two slits about 1 to 2 hours, Malus minutes, the light
  clock minutes. The pins script itself: 8 s per opening world at 12
  Links, 70 s at 24 (HOST).
- **The clock.** The wheel W = 4096 unchanged; the record's train a new
  declared integer of the lamp (32 periods for the bells, 128 for the
  two slits at 0.99); the lattice's pace by direction within 0.8 percent
  of c at 12 Links (6.0 A), the price paid in the far-field bells and in
  the moving clocks' pins, to be read against their bands.
- **The register's re-run.** After the build and the pilot's four worlds
  under the rule: every light world at the new scale, the bodies' worlds
  under the same rule at their periods (section 8), once, on the Boss's
  second GO, the readings on the detector's own count.

## 8. The massive row: the same rule read at a body's period

The owner's statement 5 makes the body's record the same thing as
light's: a detector at rest is a record that pops up at the same Node
each cycle, a moving one at the next Node; the mass moves only through
the Inside; the cycle time is the detector's. Under the rule a massive
family's record is born at its body's Node with its own clock (the
rest frequency, E'_0 = Q S M in the units of the flight table, the
family's [n, d]) and a train of its own period; it spreads by the same
rule; it clicks, by the counting trigger, at the Node where its offer
first crosses the rung: at rest that is its own Node (the return of
record 1227), and the click is the body's SELF-CREATION (the count per
self-creation of the light clock's algebra, TICK_ALGEBRA.md), the
detector's own count advancing by one; the body's held content (its
mass) is handed to itself; the next cycle starts. In motion (a drive,
the momentum label of the massive form) the record's train is emitted
with the phase gradient of its momentum and the first rung crosses at the
NEXT Node later than at rest by the rule's own dispersion: that is the
computation of 6.5, the candidate for gamma from the rule, attempted
there and not claimed here. The massive form's separate design (the
Boss's item 5 of 07:19Z: a body's own count as the whole part of its
record's phase, the lifetime a share per self-creation, the three keys
retired) folds into this section: the body's own count IS its clicks;
the lifetime is the number of cycles the record's ledger allows; the
keys of the massive form (`massive_rows`, `massive`, `momentum_magnitude`)
become the family's clock and the lamp's train. Whether a massive record
splits the same way: yes, by construction, the rule has no family name;
what differs is the clock and the content it hands over, values not
branches (the generic test).

## 9. The three tests of the whole, and what the reviewer must gate

Generic PASS, vector PASS, local PASS by section 2; the click's one
non-local step (the exhaustion, the host's) as today, named. Reviewer 3
is asked to gate: (i) the wall's boundary in 6.1 (absorbing against
reflecting) and its far-field number; (ii) the front's pace on the
chain in 6.4; (iii) the dispersion's effect on the moving clocks in 6.5
before any claim of gamma; (iv) whether the stretched pace of 4.1 is
the one wall of NOTE.md or a second thing; (v) the host's cost of 7
against RUN_AUDIT.md. The owner reads sections 0, 1, 5 and 8 first.

## 10. Six lines

1. The law he means: the ray splits at every free Node inside the board
   and holds its amplitudes; outside there is no board, only clicks, and
   a passage from Node to Node only through a detector, at rest or
   moving, which carries the mass through the Inside in its cycle time.
2. The rule: at every Node the record re-emits to its six neighbours the
   sum of what they held less three times what it held before, the
   remainder kept; the pair [1, 3] its only constant; verbs G and D;
   generic, vector and local.
3. What it fixes: the line on the lattice, the declared fans, the
   sensitivity key, the coin, the two energies of light (one energy, one
   clock, E = h f = p c by the rule's own dispersion), the script's
   residue.
4. The pins, computed: the single opening at the Fresnel number 1.45
   inside its band at 12, 16 and 24 Links; at 0.16 (w = 2 lambda) the
   rule reads the wave's obliquity, 0.842 with a reflecting wall and
   0.814 to 0.857 with a lossy one, inside the pin as the owner
   re-declared it at 10:05Z (0.842 +- 0.03, the wave's own sum; the sinc
   constant a new pin at eight wavelengths, not yet computed); the two
   slits at 0.958 by the train's coherence, 0.98 reachable by the train;
   the detector at rest 206.0 by the first-rung click at every
   wavelength, the pin's number;
   the moving detector along its motion 303 at 24 Links against the pin
   307 +- 10, the lattice read as a medium, row 4a's FAIL unchanged.
5. The price: the wavelength 12 Links or more, the light worlds scaled
   by 2.6 or more in length, hours per world, a train declared on the
   lamp.
6. The build's first step exists on `detector-law-build` (f4a3971a, a
   chain click with balanced books) and holds there by the Boss's order
   of 10:08Z until Reviewer 3's re-gate of this pass and the pins pass
   against nature in the script; its four choices are section 11's, put
   to the reviewer as design decisions; the massive form folds in as
   section 8.

## 11. The build's specification (docs; the engine work starts on Reviewer 3's gate)

The build is one hypothesis identity, `detector-law-v1`, selected by the
world file (`law: "beam"`, the hypothesis named), beside the ray law as
built, which stays the default until the register is re-run under the
rule; no world of the register changes until then. Its steps, in the
order the engine takes them each interval, each with its gate:

1. **The store's form.** A record's rows are `(record, node, a_now,
   a_before, r)` in int64 columns per family (the same `stores` the
   engine keeps, with the direction, amount, multiplicity, phase and age
   columns unused under the rule); the record's ledger (its content h,
   its birth stamp, its lamp's number and ordinal, its train's length and
   phase) as today's record identity. Gate: the loader accepts the four
   pilot worlds scaled (section 7) and refuses, naming the rule, a world
   that declares under the key a lamp's `turns` (the fan's phases), a
   measured event's `splits` or fan, a paid family without the pair form
   of its clock (the build's three refusals at f4a3971a), and, by the
   Algebra Auditor's rows (1.1): a record `in_transit` without rows on
   the board, a face that is neither a declared wall nor periodic, a
   "become" triggered by anything but the object's own cycle, a moving
   object's step by anything but the first rung at the next Node in one
   of six directions, and an object's N_s smaller than its train's
   leaving time.
2. **The source.** At each of the lamp's Nodes, for each live record of
   the lamp, `a_now := A cos(2 pi t n / (d N))` on the wheel (the cosine
   a table of N entries at load, the rate's whole part by `by_clock`),
   for the train's length; the lamp pays h at the birth (as today, the
   turn 1). Gate: the birth line as today with the birth stamp; the
   lamp's count `held // h`.
3. **The rule.** One vectorised step per family per interval: gather the
   six neighbours' `a_now` per row (rows absent at a neighbour read 0;
   new rows created at neighbours the record reaches, the front), form
   `total`, the Euclidean division by 3, the remainder kept, the absorbing
   Nodes (detectors) as section 5. Gate: the pins script's numbers of
   section 6 reproduced bit for bit by the engine on the same scaled
   worlds (the script is the engine's oracle: the same integers).
4. **The detectors.** Per detector set, the pointer accumulates the
   arriving offer `a_now^2` at its Nodes per record; the click by the
   first rung at s_D = 1 / W (`amplitude.rungs`, `cell_of`); the
   completion by exhaustion or the faces; the click line with
   `clock_stamp` and the birth stamp; the record's rows removed. Gate:
   one click per record; the books balanced at every completed tick;
   the stamp on every click line.
5. **The crowd and the wall** (4.1): the age moment at a Node stretches
   the rule's step there by d against d + f n A (the one wall); no push
   on a record's rows. Gate: row 13's pin worlds scaled, the bend read
   against 6.6 before the register's re-run.
6. **The host's cost.** The rows per record bounded by the world's
   Nodes; the records alive bounded by the train and the completion;
   the memory and the time per interval reported as HOST beside the
   run's record (RUN_AUDIT.md's form).

The build's first step (the branch `detector-law-build`, the module
`events/detector_law.py`, the world key `detector_law`, the lamp's key
`train`; the Boss's order of 08:47Z to build in parallel with the review)
made four choices the text above left open, each named here for Reviewer
3, none a new constant of the law beyond a declared pair:

- **The receiver's take.** A Node that receives must not send the wave
  back (a wall of amplitude 0 reflects, as 6.1's script showed; a mirror
  is a receiver body that re-emits). The record's row at a receiver holds
  one amplitude per Port that faces a free Node (the NodeState's Ports),
  the wave entering by that Port, following it one way: g(t + 1) =
  a_f(t) + k (a_f(t + 1) - g(t)) with a_f the free neighbour's amplitude
  and k = (c - 1) / (c + 1) at c = 1 / sqrt 3, the declared pair
  [-15, 56] (the first-order one-way condition; a rounding declared at
  load, no root at run time); the free neighbour reads g as the
  receiver's amplitude on that Link. Measured on the chain at 12 Links:
  0.07 percent of a packet's motion reflected, against 30 percent from a
  wall of amplitude 0 (the build's test).
- **The offer is the Port's motion**, (g(t + 1) - g(t))^2, not the
  amplitude squared: the rule has a zero-frequency mode (a static level
  on the board is a solution of the six-neighbour rule) which no receiver
  takes and which carries nothing; the motion of a Port is what a wave
  does to a receiver and what a static level does not. The record's norm
  is the motion its train inserts; the board's energy in the completion
  test is the rows' motion likewise.
- **The train begins and ends at the clock's zero** (the phase 3 N / 4,
  the cosine 0 and rising, N divisible by 4): a step in the inserted
  amplitude would leave the static level above on the board.
- **The inserter's grace.** The lamp's own Nodes read their own record
  only two periods after the train: a Port books the wave's motion beside
  it, and the record's tail leaving the lamp is not an arrival. A
  detector at rest still receives its own record's return after that (the
  light clock, section 8). The reviewer is asked whether the grace should
  be replaced by a Port that books only the entering characteristic (two
  Links deep, not local) or stays as a declaration of the receiver.

The build's chain test: a lamp at one end of an open chain, a receiver
body read as a set at 68 Links, one record per forty intervals: one click
per record, the books balanced at every tick, the screen's click at the
front's first rung 116 intervals after the birth (L / c = 118), the
stamp and the birth stamp on every click line; a record whose wheel
sends it back to the lamp returns its unit to the lamp's stock (a
detector at rest).

The gate set before any reading is called a result: the four pilot
worlds under the rule at 12 Links (the single opening at both Fresnel
numbers, the two slits, Malus, the light clock at rest) against section
6's numbers bit for bit, then the reviewer's gates of section 9, then
the pilot's readings against nature by kind, then the register's re-run
on the Boss's second GO.
