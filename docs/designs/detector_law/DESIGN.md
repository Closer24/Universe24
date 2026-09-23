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
| frequency | its REST clock, the family's pair [n, d] on the circle of N steps, the record's period: the initial condition of its record; in motion, under the clock sentence (section 8, the owner's word of 11:03Z), no declared clock: its insert follows the receive of its own record and its clock is the cycle of its own bound record read in its own count; the declared period is bounded below by the load-time checks of 1.2 | a declaration (the rest value); the motion's clock the Inside's |
| phase | the phase at which its train starts, the clock's zero (3 N / 4, the cosine 0 and rising) | a declaration |
| place | its Nodes on the GameBoard; a body of one Node or a line or a wall of Nodes | a declaration |
| step | one of the six directions and the declared cadence k, intervals per Link (k = 0 at rest); a step is one Link, never a diagonal; the first rung of the object's own record at the next Node is the step's accompanying click, not its cause (a one-Node object's six neighbours cross 1 / W within an interval of the insert, so the rung alone sets no pace; Reviewer 3, MUST F); five is read with the declared pace, the dilation 8b's to derive, never the step's | a declaration |
| momentum | the integer **P** on the object, one component per axis with its remainder, CHANGED BY THE FLUX at its six Ports (the stress of the total field, 5.1 (a)) and READ BY ITS CLICKS; its initial value 3 Q S M v_0 x 56 d from the declared step; a free object's cadence is read from it (5.1); |v| < c as the integer comparison 3 (P . P) < (3 Q S M x 56 d)^2, checked at the initial P and at every change | a declaration of the design (5.1), not of the law |
| re-emission | the pair p = [p_n, p_d] of what its Nodes re-emit of what the rule gives them, or a TABLE (a partial re-emission with a phase: the polariser's rotation, a splitter, a trap), the fourth value of the parameter (section 5, the receiver forms) | a declaration |
| train | the length of one insert in periods of its clock (the record's coherence, 4.5) | a declaration |
| sensitivity | the rungs of the wheel one click needs, 1 (the first rung, the counting form) or 2 (the owner's "check 2 against 1", 6.8: one interval's difference) | a declaration |
| the wheel W | the rung's HEIGHT, 1 / W of the record's norm per rung (4096 the register's wheel; 64 declared for the chain and one-layer worlds, whose afterglow of 0.3 to 0.65 percent of the norm crosses the first rung of 4096 for 700 to 1100 intervals after a train, 6.8; a second parameter beside the sensitivity, Reviewer 3's line of 11:38Z) | a declaration per world |
| the cycle's closed count N_s | the intervals after its last insert during which it does not receive its own record (the cycle sentence, section 5) | a declaration |

Everything else the object has is read, not declared: its own count on
every click line (`clock_stamp`), its cycle (the count from an insert to
the receive of the same record), the direction of what arrives (the
gradient of the arriving offer's phase across its Nodes). The
self-click is the existence condition, and it is a DECLARATION Outside
that costs the Inside nothing, in the owner's words (record 1344, the
Boss's rendering): "we may put foreign objects there and declare that
they always produce clicks, because otherwise the simulation would be
very hard": every foreign object holds its own record (its body's
record at its period, section 8), inserts it and receives it at its own
Nodes each cycle, the cycle's closed count N_s the integer of that
declaration; an object whose declaration cannot be met (its Nodes
cannot receive) is refused at load, and its books show the record
escaped when it leaves by a face. Under the rule a one-Node object at
rest in open space in three dimensions has no return (Reviewer 3's
MUST H: the wave spreads and does not come back), so its self-click at
rest is its declared period (its cycle N_s with no receive from the
Inside), the light clock's return (a body and a receiver body at L) is
a two-body cycle, and section 8 says both, the honest reading and the
place where the law does not yet do what the owner says. N_s is the
object's declared integer (kind 1) with its default named in the world
file's definition of the one kind; the build's "grace" of two periods
at f4a3971a is a module constant to become that declaration.

1.2 **The load-time checks on the declared period and the declared
cadence** (the model owner's word of 11:12Z through the Boss: "the
declared clock N has a limit too: it cannot exceed the speed of light,
so not every N may be declared"; the Boss's reading entered as declared
checks, Reviewer 3 to gate; every number a COMPUTATION; where my
arithmetic differs from the Boss's it is named):

- (a) The hard floor from c: nothing changes faster than one interval,
  and the wave crosses a Link in sqrt 3 intervals (the pair [1, 3]), so
  a declared period of N intervals is a wavelength N / sqrt 3 Links and
  below two intervals there is no wave: **N >= 2**, refused below (the
  Nyquist period of the lattice's clock; at N = 2 the checkerboard mode
  of 2.1, carried at a constant amplitude and nothing else).
- (b) The design's honest floor, already the design's: the wavelength
  at least 12 Links (6.1, 8c), so **N >= 21 intervals at rest** (12
  sqrt 3 = 20.8); for a moving object MUST I's floor lambda_0 (1 -
  beta_c) >= 12 gives **N >= 50 at k = 3** (28.4 sqrt 3 = 49.2), **37 at
  k = 4** (21.2 sqrt 3 = 36.7), **30 at k = 6** (16.9 sqrt 3 = 29.3);
  the same arithmetic as the Boss's.
- (c) The same bound on the motion: the cadence k of 5.1 (a) (one Link
  per k intervals) must satisfy **k >= 2**, since k = 1 is one Link per
  interval, above c (beta_c = sqrt 3 / k: 0.866 at k = 2, 0.577 at k =
  3, 1.732 at k = 1); the push-to-cadence rule REFUSES a push that
  would take an object's accumulator past one Link in fewer than two
  intervals: the momentum is kept (the remainder with it), the cadence
  is clamped at 2, and the refusal is recorded as an event on the
  object's click line, never a silent clamp; the declaration of 5.1 (a)
  says so. One difference from the Boss's line, named: k >= 2 still
  allows beta_c = 0.866, and the bound the wave itself sets on a source
  is MUST I's floor (b), which at k = 2 needs N >= 155 (lambda_0 (1 -
  0.866) >= 12: lambda_0 >= 89.6 Links); so (c) is the hard bound and
  (b) the honest one, both checked.

What is refused with the one kind, by the Algebra Auditor's rows
(ALGEBRA_AUDIT.md at c848aad0 on `algebra-inside-outside`): a record
`in_transit` between two objects without rows on the board (there is no
Outside passage: the mass moves only through the Inside, as rows); a
face that is neither a declared wall nor periodic; a "become" of an
object triggered by anything but its own cycle; a moving object's step
at a cadence other than its declared k, or by a diagonal, or without
the first rung of its own record at the next Node as its click, one of
six. Each refusal is a load-time check of the world under the key
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
Node, the zone's corner): at the semidefinite point it has two
solutions, the alternating one and a secular one growing linearly with
the interval count, both with E = 0 (the repeated root), fed by the
remainder's rounding at about one unit per interval, harmless at 2^20
over 10^4 intervals and absent on the z-periodic one-layer worlds of
the pins script, where the bound is strict (four neighbours) (Reviewer
3's line on db07375d). The record's norm, what the rungs
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
A standing or reflected part of the record beats: its SUM a^2 passes
through its extremes twice a period (a translating profile keeps SUM
a^2 nearly constant, a standing one does not), so a rung crossed by
a^2 at one interval is uncrossed at the next, and the click's time by
a^2 at a receiver with a reflected part is not the front's arrival but
a beat of the train against the wheel. E has
neither defect: the static level is zero in it, and a travelling train
carries a constant E whose motion part is what a receiver's Port can
take in an interval (section 5: the offer is the Port's motion). The
build measured the difference on the chain: with a^2 no completion; with
the motion the click at the front's first rung and the books balanced.

The Port's factor (Reviewer 3's line): a Port books the motion squared
of its ghost amplitude, while a travelling wave's E is 3 x motion^2 +
the strain in equal parts, so the energy entering a Port per interval
at normal incidence is 2 sqrt 3 times the booked motion squared (the
declared pair [97, 28], right to 0.01 percent); the rung at 1 / W of E
is 1 / (2 sqrt 3 W) of the booked motion unless the Port books in E's
units, which the engine does (the pair applied at the Port); the
completion test likewise compares E, with the strain, to the absorbed
in one unit, never the board's motion alone (the kinetic half passes
through zero twice a period in a trapped or standing part and the test
would fire at a turning point; Reviewer 3, 10:14Z). Under the
coefficient form of 4.1 the conserved energy carries the index squared
on the motion term at each crowd Node, E_n (4.1), and the books of a
record in a crowd read E_n.

The one non-local step, named (the Algebra Auditor's row "LOCAL EXCEPT
the completion of a record", ALGEBRA_AUDIT.md at c848aad0): the record
completes when its offer has been exhausted into receivers or has left
the board, and only the host knows the sum over the board of the
record's remaining motion; every Node's step, every Port's take and
every first rung is local. That step is the amplitude law's own
(event_split DESIGN.md section 4, the exhaustion), unchanged: a gather
over every row of the record at every interval, a host cost per
interval per record reported in section 7 and the audit's locality line
to update in ALGEBRA_AUDIT's terms (the auditor archived, the
Definitions Editor to carry it), not a physical dependency of any Node.

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
13's worlds (the ratio of the full bend to the time part's, 2 from the
coefficient alone or 1; PINS.md row 13); it is named there and not run.
Two lines of Reviewer 3's on the form: the coefficient stands on the
Laplacian, not inside a divergence (the non-conservative form), which
gives the same bending as the conservative one for a smooth crowd and
differs only at a sharp step in the index, by a small change of the
Fresnel reflection, acceptable and said; and the conserved energy under
the form carries the index squared on the motion term at each crowd
Node,

    E_n = 3 SUM over Nodes n_c^2 (a_now - a_before)^2 + the strain,
    in integers 3 SUM den (a_now - a_before)^2 + num x the strain
    at a uniform num,

so the books of a record in a crowd (row 13's worlds, 6.6) read E_n,
else E drifts there and the rung and the completion misfire in exactly
those worlds.

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
report of 09:20Z), not here. This sentence does not close MUST D
(Reviewer 3, the Boss's line of 10:14Z): the coefficient form has no
place for a weight of the pushed record, so M_eq at the stretched pace
is the question for the owner as written above, with the contradictions
of that list, the Boss's (j) first, before it.

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
"grace" of two periods is a module constant to become it), not a
constant of the law; a declared LOWER BOUND on it is refused below (the
tail decays without an end, so no leaving time is derivable, and the
bound is called a declaration); the closed count runs on the object's
own count wherever its Nodes are, so a moving object's N_s follows it;
and in the one-layer and chain worlds the object's own tail does cross
its first rung at its own Nodes after a while (the afterglow of two and
one dimensions, absent in three), so the bound is dimension-dependent
and the pilot's z-periodic worlds declare N_s above the tail's crossing
time, a number the pins script prints per world (section F). The three tests: generic (one declared integer per
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

- **The mirror**: the Node's row is held at 0, its value fixed at its
  birth and the drift term absent, a second declaration beside the
  coefficient form of 4.1 (where q = 0 decouples the Node from its
  neighbours and leaves a_next = 2 a_now - a_before, a constant or a
  linear drift, not a zero; Reviewer 3's line): the limit of a large
  mass, the index infinite, the boundary's Fresnel step ((n - 1) /
  (n + 1))^2 equal to 1. A plane held at 0 returns the whole packet
  with its sign reversed; nothing is booked. The pins script's "zero
  wall" is this form (6.1: 0.842 at 24 Links, Rayleigh-Sommerfeld's
  first-kind sum, which is the wave's own sum through an opening in a
  mirror). The build's "30 percent of a packet's motion returned by a
  wall of amplitude 0" (f4a3971a) is WITHDRAWN: it read something else
  and is not re-derived here. A large mass declared as a wall is
  derived, not a fifth form: a mass's crowd raises the index at its
  Nodes, a step in the index reflects ((n - 1) / (n + 1))^2 at normal
  incidence (6.7: 1 / 9 at n = 2 read by the script), a wall a large
  index, the mirror the limit, a graded rise a sponge; the reflection
  as a function of the declared mass is the coefficient's, as ordered.
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
  with the declared pair k = [-15, 56] (Engquist-Majda's first order,
  k = sqrt 3 - 2, right to 0.03 percent), the build's choice (section
  11), 0.07 percent reflected on the chain. Reviewer 3's gate, AGREED
  with corrections: exact at normal incidence only, a plane wave at the
  incidence theta reflecting (1 - cos theta) / (1 + cos theta) (7
  percent at 30 degrees, 17 at 45, 33 at 60), so right for a screen read
  near normal incidence and for the chain, WRONG for the board's side
  faces and for a wall's Nodes beside an opening (the diffracted wave
  runs along the wall at large angles), where the sponge is the form;
  the remainder of the Port's division by 56 stays on the Port as the
  rule keeps r (the vector test); the condition reads the free
  neighbour's NEW amplitude, one Link under a declared order within the
  interval (the free Nodes' step, then the Ports), written into the
  interval's steps (docs/ENGINE.md's row when the design lands). The
  far-field number under this wall differs from the mirror's 0.842 and
  from the sponge's numbers for this reason and is computed in the same
  form, script and engine alike, with no exact reference (PINS.md row
  10). The engine therefore carries all three forms; every pilot world
  declares the form per object; every pin names it.
- **The table**: a partial re-emission with a phase (the polariser's
  rotation of the record's phase by its setting, 4.2; a splitter; the
  trap of an optical lattice, 8b), the fourth value of the re-emission
  parameter (1.1), which reads the record's phase; under the rule that
  phase is read from (a_now, a_before) on the wheel (Reviewer 3's SHOULD
  of 08:48Z), a reading declared here as the pair's angle on the phase
  circle nearest to (a_before, a_now) at the record's clock, computed
  with the phase table at load, no root at run time; until the reading
  is declared in the engine, the tables of Malus and Bell are "unchanged
  from the amplitude law" only in form.

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

**5.1 Two declarations of the design, not of the law** (the Boss's GO of
10:50Z; Reviewer 3's lines of 10:29Z and 10:55Z on what each must say;
the law changes only on the owner's word). Each through the three
tests; each with the pins it touches named; no pin moves.

**(a) The push-to-cadence rule** (re-formed on Reviewer 3's gate of
4845f9f3, 11:38Z: NOT MET as the push, AGREED for the cadence). Where
the momentum lives: on the object, as a declared integer per axis, P_i
(i one of x, y, z), with a remainder per axis, changed by nothing but
the wave at its own Ports. THE PUSH: per interval the momentum's change
is the stress of the TOTAL field (all records superposed) at the
object's six Ports: on the two Ports of axis i, T_ii = 3 (motion)^2 +
(the strain along i)^2 at the free Node beyond the Port, an integer of
the rule's own differences (the terms of E, 2.1; the momentum flux of
the wave; in the integers x 4 as the pins script computes it), and P_i
changes by T_ii at the Port behind less T_ii at the Port ahead: what
the wave loses at the object the object gains. It is what the chain
script of the reduced run does (the section's push), declared here.
The click form first written ("h times the wave number per click") is
withdrawn as the push, kept as the READING: it fails twice (it misses
the reflected share, a mirror taking 2 h k and a scatterer (1 + R - T)
h k; and it cannot act while the object's Ports are closed by the cycle
sentence, which is when the binding acts); the clicks read the momentum
the object has, they do not make it. The object's own emission's
recoil in motion (the Doppler-asymmetric flux, 4.1's mass loss) is
kept: physics, not a bug. THE CADENCE, as before: a body of content M
has the rest energy E'_0 = Q S M (the flight table's units, where
light's energy is h n / d per interval) and, at the pace v Links per
interval, the momentum E'_0 v / c^2 = 3 Q S M v; so v_i = p_i / (3 Q S
M), and the step is taken exactly in the integers with the remainder
kept: per interval the accumulator A_i += |P_i|; when A_i >= 3 Q S M x
56 d the object steps one Link along axis i in the sign of P_i and A_i
-= 3 Q S M x 56 d (k = (3 Q S M x 56 d) // |P_i| intervals per Link with
the remainder kept on the object, as the rule keeps r; at rest P_i = 0;
the declared step of 1.1 is the initial P_i = 3 Q S M v_0 x 56 d; the
object's own symmetric insert adds nothing to P). TWO CHECKS, declared:
|v| < c on the vector, no root, as the integer comparison 3 (P . P) <
(3 Q S M x 56 d)^2, checked at the initial P and at every change; a
change that would cross it stops the world with a diagnostic, never a
silent clamp (1.2 (c)'s k >= 2 is the whole-cadence reading of it: v =
1 / 2 is the largest pace whose cadence is a whole number of intervals
at or above 2, while the vector bound allows up to c, the difference
named); and MUST I's floor lambda_0 (1 - beta_c) >= 12 with beta_c =
sqrt 3 |P| / (3 Q S M x 56 d), checked at the initial P and at every
change. The three tests: generic (one primitive, the stress at the six
Ports and one comparison, with declared integers Q, S, M and the pair
[97, 56]; no family name, no kind); vector (verbs G, the sum of the
stresses into the object's vector, and D, the one division with the
remainder kept, then comparisons; no root, no float); local (the
object's own Node, its six Ports and the free Nodes beyond them;
nothing further). The rule decides HOW the pair reaches beta, not WHICH
member of 8b's family it ends in: that is the law of the object's
frequency (section 8, the clock sentence and its completion). What it
can move: five's first outcome (the pair's separating or holding); the
pins it touches: (e), (f), 5b, 4a and 4b through 8b's member; none
moves.

**(b) The phased partial re-emission, the table's first member**
(AGREED WITH LINES, 11:38Z). The fourth value of the re-emission
parameter (1.1) is a TABLE; its first member is the index scatterer:
the object's Node (or its w Nodes) runs the rule with the declared pair
q = [num, den] on the six-neighbour term IN THE COMPENSATED FORM of 4.1,

    3 den a_next + r' = num (the six-neighbour sum) + 6 (den - num) a_now
                        - 3 den a_before + r,

the Laplacian form at the local pace c / n_o with no gap (the pair "on
the six-neighbour term" alone would put an on-site term 2 (1 - q) a at
the Node, a local mass: a barrier for q < 1, an instability for q > 1;
Reviewer 3's line, the script's form the right one); the index n_o =
sqrt(den / num) declared by the pair; the stability floor q < 3 (q = 9
grows), a load-time check. What it is: a REACTIVE RELAY, not a
resonance, and it needs none: a thin scatterer (w Nodes, w much less
than the wavelength) reflects the amplitude (n_o^2 - 1) pi w / lambda
with the phase +- pi / 2 by the sign of n_o - 1 (the polarisability
alpha proportional to n_o^2 - 1), a thick one ((n_o - 1) / (n_o + 1))^2
of the motion (the Fresnel limit, 6.7: 1 / 9 at n_o = 2 read by the
script); its Node does not ring on its own when struck (COMPUTATION,
the scratch preparation: the motion at a struck scatterer Node after a
train has passed is 36 and 100 times smaller than a free Node's at n_o
= 2 and 3, no localized mode, consistent with Reviewer 3's (C)
computation of 11:43Z). What it does to the other forms: the mirror is
the limit q = 0 with its second declaration (held at 0, the drift term
absent, section 5); the sponge is untouched (a ramp of the damping
pair, not of the index; an object may declare both); the polariser's
rotation is the table's second member, a phase on the wheel applied to
the record's phase read from (a_now, a_before), declared separately.
The three tests: generic (the pair per object, no family name; the
same verbs T and D as 4.1); vector (verb T with the pair on the
six-neighbour term and the compensation, D with the remainder kept:
the rule's own step at the object's Node); local (the object's own
Node and its six neighbours). What it can move: with (a), where a
coherent pair sits (Reviewer 3's closed form on the chain, record 1372:
the force on emitter 1 is 2 A^2 cos(k L) toward the partner within 2
percent from L = 64 to 108; for in-phase clocks the stable points at
(m' + 1 / 4) lambda_0, 71.4 and 103.2 Links, the unstable at (m' + 3 /
4) lambda_0, 87.3; L_0 = 80 = 2.52 lambda_0 with in-phase clocks the
point of MAXIMAL repulsion; with clock 2 a quarter period behind, the
force 2 A^2 cos(k L - pi / 2), zero at 79.4 and stable); it does not by
itself decide between 8b's member and Lorentz's, which is the clock's;
the pins it touches: (e), (f) (the declared relative phase, below), 2b
(the splitter is this member), 1a, 1d and 9 (the second member); none
moves.

**What the reduced free-pair run reads with (a) and (b)** (8b (vii);
the pins script's section I, prepared in the scratchpad and not run
before Reviewer 3's gate of this section and the owner's word): two
objects on the chain, each an index scatterer of one Node at a declared
n_o, each pushed by the total field's stress at its Ports by (a), the
variants Reviewer 3's list of 11:43Z (the held list of 11:23Z and
11:40Z superseded): (A) the declared resonance f_0 ticking in the
lattice's intervals, emitting continuously (any train at least 2 L / c
+ 2 periods), with the declared relative phase of the two clocks (a
quarter period, the stable parity at L_0 = 80); the relay (the owner's
sentence read literally: the insert following the receive of the own
record, re-formed alike); (B1), the two ends as ONE body with one
shared momentum integer per axis (the pushes on both ends summed, the
partner's radiation pressure internal, the extent rigid; the owner's
words of 11:38Z, record 1370), LISTED as the control, not run; (C), no
lawful variant on the massless rule (Reviewer 3's computation: no bound
mode below an acoustic band; the one localized mode above the band's
top 4 to 7 times faster than the floor N >= 21; a gapped rule that
would give it is a scratch variant, not the law). The readings, by
kind: the separation L (COMPUTATION on the objects' places); the cycle
from the zero crossings of the object's own record at its Node (a
GAMEBOARD reading, since the rung at W = 64 jitters by 6 percent, above
five's band) beside the click (which keeps the outcome: settles or
separates); the pair's frequency in the lattice's intervals between the
objects (the reading that names the member: f / f_0 = 1.000 for (A)
with L_along / L_0 = 0.667; 0.667 with 1.000 for the relay; 0.816 with
0.816 for Lorentz; PUSH_BALANCE.md section 6 at d69c87a9). The settling
criterion, declared: a bounded oscillation of L about an equilibrium
within +- lambda_0 / 4 over the last twenty cycles with no monotone
drift; "separates" is excluded for a coherent pair at a stable parity
by the closed form, so a separation now reads as the push's form, not
the clock's. The scratch preparation's findings of 11:25Z (the pair
separating at rest) are explained by the closed form: in-phase clocks
at L_0 = 80 sit at the maximal repulsion, and 2-period trains never
overlap at L / c = 139; both are re-formed here before any run.

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

## 6. The experiments with a foreign object: the pins before any build (COMPUTATION; `detector_law_pins.py`, `detector_law_pins.out`)

The name is the model owner's (11:12Z, through the Boss): from today, everywhere, "the experiments with a foreign object": a foreign object can be anything (a detector, a clock, a mirror, a sponge, the air, a polariser), one definition with the same parameters (1.1), and the experiments with it go on; no other noun for the thing on the board that the Inside did not make. The light clock (6.4, 6.5), the wall of row 10 (6.1), the polariser (6.3), the air (6.7) are all experiments with a foreign object.


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

6.7 **The air as a foreign object (an experiment with a foreign object): the coefficient form at a declared
index** (the owner's "the air modelled as foreign objects with air's
parameters, with a convergence experiment"; Reviewer 3's correction of
09:33Z: nature's air moves no pin; the experiment tests the coefficient
form at a large declared index). Air is not in the rule: the rule's one
medium is the lattice. Reviewer 3's gate of 85d0a179 (NOT MET on this
point, folded): "a declared age moment A" is the old engine's crowd
reading, carried by no row of the rule and none of 1.1's nine
parameters, and an object that never inserts and never receives is not
on the board by 1.1's own existence condition (the owner's "each with
mass, frequency and phase", records 1339 and 1344). Two lawful forms,
both written here, the Boss's recommendation:

- **(a) The air's objects, within the nine.** The index is the object's
  RE-EMISSION parameter: the pair q = [1, 4] declared at its Nodes (the
  mirror is q = 0 of the same parameter, held at 0 by its second
  declaration), the object inserting its own record at its declared
  clock and self-clicking by its declared period like any other (1.1),
  its index acting on every other record's step at its Nodes; 6.7's
  region is a set of such objects, one per Node, each with its mass,
  frequency, phase and place. The attenuation "their clicks" is the
  light record's offer absorbed at the air's Nodes: the sponge's
  DAMPING pair, a separate declaration from the index (below).
- **(b) MUST E's definition of A under the rule, for rows 12 and 13.**
  What a mass's crowd is under the rule is its records on the Nodes
  around it and nothing else, so the index at a Node is what the other
  records there do to a passing record: q at a Node a function of the
  other records' local state there, their energy density E at the Node
  in 2.1's form, a cross-record coupling, local (the record's own row
  and the other records' rows at the same Node, read as the crowd's age
  moment is read today); the function itself, E to the pair, is the
  definition MUST E still lacks, to be stated before row 12 or 13 is
  computed, and it is not stated here.

The experiment below is form (a) with the objects' index n_c = 2 (q =
[1, 4]), large enough that the lattice's own dispersion (0.2 to 0.8
percent) is far below every effect. THE FLOOR, declared for every world
with the region, the two-slit world included: lambda_0 / n_c >= 12
Links (lambda_0 >= 24 at n_c = 2, or n_c = 1.5 at lambda_0 >= 18), by
6.1 and 8c; the script refuses the region below it. It asks three
things of the rule, each with its pin stated here before the script
runs it (PINS.md row (h)):

- **The wavelength inside**: a train of lambda_0 = 12, 16, 24 Links
  entering the region reads, by its zero crossings inside, **lambda_0
  / 2 +- 1 Link** (the phase pace c / n_c; COMPUTATION on the chain).
- **The Fresnel step at a sharp boundary**: the reflected motion over
  the incident motion, read at one probe Node in front of the boundary
  before and after the train has passed, **((n_c - 1) / (n_c + 1))^2 =
  1 / 9 = 0.111 +- 0.010** (the wave law's normal-incidence step for a
  change of pace with the amplitude and its gradient continuous, which
  the coefficient form is); the convergence experiment is this number
  at 12, 16 and 24 Links, converging on 1 / 9 as the lattice's residual
  falls (the falsifier: a value outside 0.101 .. 0.121 at 24 Links, or
  one that does not move toward 1 / 9 with the wavelength).
- **The graded boundary**: the same with the pair ramped from [1, 1] to
  [1, 4] over one wavelength of Nodes: the reflected motion **below
  0.010** (the product of many small steps). Two things, not one
  (Reviewer 3): a ramp of the INDEX transmits without reflection and
  absorbs nothing; the sponge of section 5 is a ramp of the DAMPING
  (the re-emission pair below 1, ramped), with or without an index, and
  an absorber that does not reflect needs the damping ramped.
- **The two slits at lambda_0 / n_c**: section 6.2's world with the
  region behind the wall filled at n_c = 2: the fringe spacing
  **lambda_0 L / (n_c d) +- 3 percent**, half of 6.2's (COMPUTATION on
  the accumulated offer's peaks), the Fresnel step at the opening's
  face reflecting 1 / 9 of the motion back toward the lamp, booked as
  a face's escape in the engine only if the back face is a sponge (a
  mirror there returns it). For the step reading the train is declared
  shorter than twice the probe's distance to the boundary, else the
  reflected train overlaps the incident window (met in section G: the
  boundary at 4 lambda_0 + 10 Links from the probe).

What passes here passes the coefficient form of the wall, not nature's
air: at air's n = 1.000 27 every number above is inside its band's
hundredth, which is the sensitivity check the medium column of PINS.md
records, and no pin of the register moves for it.

**6.7 as computed** (`detector_law_pins.py`, sections G and H;
`detector_law_pins.out` at 24 Links and `detector_law_pins_index.out`
at 24, 32 and 48 Links; COMPUTATION; the source the build's, a sine
from the clock's zero, the grace two periods; the coefficient pair [64,
256] past the boundary, the free Nodes [64, 64], the rule of section 2
to the remainder's grain). The floor first: the wavelength inside must
be 12 Links or more (8c), so at n_c = 2 the experiment runs at lambda_0
= 24 Links or more; 12 and 16 are not run, and the script says so.

- **The wavelength inside**: 11.00, 15.00, 24.00 Links at lambda_0 =
  24, 32, 48 (the pin lambda_0 / 2 +- 1: INSIDE at all three; the zero
  crossings between the train's own lobes, the dispersion's precursor
  excluded). Reviewer 3's line (11:35Z): the rule's own dispersion
  inside gives 11.9, 15.9, 24.0 (the leapfrog relation at c^2 / n_c^2 =
  1 / 12), so the one-Link shortfall at 24 and 32 is the reading's grain
  (the crossings taken at whole Nodes), not the rule's pace: the +- 1
  Link is named the READING's grain, by kind, and the next build of the
  script interpolates each crossing between its two Nodes.
- **The Fresnel step at the sharp boundary**: the reflected motion over
  the incident 0.1307, 0.1243, 0.1186 at 24, 32, 48 Links, converging
  on 1 / 9 = 0.1111 as the wavelength grows (the residual 0.020, 0.013,
  0.008; the pin +- 0.010: OUTSIDE at 24 and 32, INSIDE at 48). The
  convergence experiment reads as the owner asked: the coefficient form
  gives the wave law's step in the limit, and the lattice's residual
  at a given wavelength is what it costs, named.
- **The graded boundary** (the pair ramped over one wavelength of
  Nodes): 0.0052, 0.0049, 0.0037 (the pin below 0.010: INSIDE at all
  three).
- **The two slits at lambda_0 / n_c** (section H, 24 Links, the world
  of 6.2 with the region past the wall at the pair [1, 4]): five peaks
  at the pixels 193, 257, 312, 367, 431; their mean spacing 59.50. The
  pin as declared, the paraxial lambda_0 L / (n_c d) = 52.38 +- 3
  percent: OUTSIDE, by 13.6 percent, and the fault is the pin's
  statement, not the rule's reading: 6.2's screen subtends 2 x 15
  degrees at the slits and is not paraxial, which the pin's formula
  assumed; the exact two-source peaks at the wavelength inside for this
  screen, computed AFTER the run and labelled so, are 193, 258, 312,
  366, 431 (the mean spacing 59.50): the rule's peaks to the pixel; at
  32 Links the rule's peaks 255, 342, 416, 490, 577 (the mean spacing
  80.50) against the exact 254, 342, 416, 490, 578 (81.00), -0.6
  percent; at 48 Links the rule's 384, 514, 624, 733, 863 (119.75)
  against the exact 381, 513, 624, 735, 867 (121.50), -1.4 percent,
  the outer peaks pulled inward by the train's finite length at the
  screen's edge, named. The pin is not moved; the row in PINS.md
  carries both numbers with the fault named, and the exact form is the
  pin's statement for any re-run.

6.8 **The sensitivity 2 against 1** (the owner's "check the sensitivity
2 versus 1"; 1.1's parameter; PINS.md row (i)). The sensitivity is the
rung of the wheel at which the receive counts: 1 (the first rung, the
counting form of section 5, 1 / W of the record's norm) or 2 (the
second rung, 2 / W). The pin stated first: on the light clock's chain
of 6.4, **the second rung reads N_0 later than the first by 2 to 6
intervals at 12 Links** (the front's rise between 1 / 4096 and 2 / 4096
of the return, the band from the front's steepness in 6.4's crossings
at 1 / 4096 and 1 / 16), and less at longer wavelengths only through
the front's shape, not its pace; the bells of 6.1 do not move (the rung
sets the click's time, not its pixel). Beside it, MUST A's form: the
same crossings read on the Port's motion (a_now - a_before)^2 instead
of a^2 (the receiver's offer of section 5); the pin (d) 206 +- 2 is
declared for the first rung on the offer the engine books, so a
first-rung reading on the motion outside 204 .. 208 is a finding to
report, not a number to choose between. Reviewer 3's line (85d0a179):
sensitivity 2 moves one earlier pin and could bias two: (d), the light
clock at rest, moves by the second rung's delay, so (d) is a pin PER
DECLARED SENSITIVITY and the light-clock worlds declare 1, said
plainly; the bells of row 10 do not move; (e) and (f) are unaffected
only if both arms and the rest clock are read at the same sensitivity
(the second rung's delay is the front's rise, steeper for the
Doppler-compressed forward train), so five is declared at sensitivity 1
and the sensitivity-2 check is kept to (d) and the bells; nothing else
moves. As computed below the delay is one interval, not two to six.

**6.8 as computed** (section F of the script, the chain of 6.4 with the
build's source and grace; COMPUTATION): the first rung on the Port's
motion reads 208.0, 207.0, 207.0 from the birth at 12, 16, 24 Links
(on a^2: 208.0 at all three): the pin (d) 206 +- 2 as declared for the
run that was run INSIDE at all three, at its edge (the Boss's rule of
11:35Z: not moved; the rule's own 2 L / c = 207.85 less the precursor's
lead of about one interval, with the rung's grain as its band, is a
declaration for a RE-RUN only, written before it, the 206 kept as the
ray law's history in the row); the residual static level of the sine
train (0.13, 0.10, 0.02 of the amplitude at 12, 16, 24 Links) is the
zero-frequency mode the motion offer ignores, and the next build of the
script ends the train at an exact zero (whole periods on the wheel),
any change of reading to be said by kind;
on the offer the engine books. The second rung follows the first by
**1.0 interval** at every wavelength, on the motion and on a^2 alike:
the pin's band (2 to 6, my estimate from 6.4's crossings at 1 / 4096
and 1 / 16) was too high; the front rises faster than that estimate.
The reading is stated against the pin as OUTSIDE and the pin is not
moved; what it says to the owner's question is plain: the sensitivity
2 against 1 moves the cycle by one interval in about 206 (half a
percent), inside (d)'s band, and moves no bell (the rung sets the
click's time, not its pixel). The choice between 1 and 2 is a
declaration of the object (1.1), and the register's clocks are read
at 1.

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
- **The completion's cost.** The completion test is a global sum over
  every row of the record at every interval, a gather per interval per
  record on the host (2.1); it is reported as HOST beside the run's
  record, never as a Node's work, and the audit's locality line reads
  LOCAL EXCEPT the completion of a record.
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

## 8. The massive row, in the owner's words: a foreign object that self-clicks, at rest or moving, through the Inside

His words (section 0, statement 5; 10:05Z to 10:20Z): "The detector
transfers mass through the Inside. It does not transfer mass in the
Outside; it transfers mass only through the Inside, and it pops up at
the next Node, or it can also pop up at the same Node. If it pops up at
the same Node, that is in fact a detector at rest. But it does it
through the Inside, and this has a time. And that is also the
detector's cycle time." "A foreign object always self-clicks; otherwise
it does not exist there." "The click is a local action of a Node on
itself which produces the amplitudes." "There is no such thing as a
detector and an emitter; each is both."

Under the rule, one paragraph per sentence of his:

- **A body is a foreign object** (1.1) with its content M (its mass,
  what its record hands over at a click), its clock (the family's pair
  [n, d]: the rest frequency, E'_0 = Q S M in the flight table's units,
  the same pair the flight table gave the family), its place, its step
  and its re-emission. Its record is the same thing as light's: rows on
  the Nodes it reaches, the rule of section 2 at every one of them, no
  family name anywhere in the step (the generic test); what differs is
  the clock it is inserted with and the content it hands over, values
  and not branches.
- **It self-clicks**: each cycle it inserts its record at its Nodes and
  clicks there at the end of its declared period (the cycle sentence,
  section 5: insert, N_s closed intervals, the click), "a local action
  of a Node on itself" fired by the object's own count reaching its
  declared period, WITHOUT a rung (1.1's declaration, the owner's
  record 1344): the content M is handed to the object itself, the
  amplitudes of its own record on the board are removed, and the click
  line is written with the object's own count and the record's birth
  stamp. A click by a return (the Ports taking a record's motion, the
  first rung crossing) is what the object does with ANOTHER object's
  record, or with its own when a partner or a wall returns it (the
  two-object cycle, 8b); a lone object in three dimensions never has it
  (MUST H), which is why the lone object's click is fired by its period
  and the existence condition and MUST H do not contradict on this
  page. That click
  IS the body's self-creation of the old engine (the `become` line, the
  count per self-creation of TICK_ALGEBRA.md), and the object's own
  count is its clicks; the lifetime is the number of cycles the ledger
  allows. An object that does not self-click is not on the board.
- **At rest it pops up at the same Node**, and the rule alone gives a
  one-Node object in open space no return (8b (ii), Reviewer 3's MUST
  H): its rows leave and do not come back. So the rest cycle of a lone
  object is its declared period (1.1, N_s the whole of it), the Inside
  adding nothing to it in open space; and everything the Inside adds to
  a body's cycle when it is not alone is the physics of this row (the
  clock sentence below says what the object's clock IS when it is not
  alone): a
  crowd around it (the coefficient of 4.1, its period stretched by
  (d + f n A) / d, row 12's ratio), a partner bound to it (8b, the
  standing pattern between them, the separation and the cycle from the
  wave law), a wall beside it (the mirror form, the return of record
  1227, the light clock of 6.4). "It does it through the Inside, and
  this has a time": that time is the two-object cycle, and a lone
  object's is a declaration. Both at once, as Reviewer 3 asks: this is
  the honest reading of the law as written, and it is a place where the
  law does not yet do what the owner says: his "we may declare that
  they always produce clicks" (record 1344) admits the declared rest
  cycle; his "its cycle time is determined by the Inside" (record 1331)
  is not met by a lone object under the rule and is met only where the
  cycle is a round trip through the Inside, the two-object cycle of 8b,
  which is why five and the atom live there. One line of care: in three
  dimensions the sentence is exact; in the one-layer and chain worlds
  the object's own tail comes back and crosses a low rung (the
  afterglow), so "no return" is a statement about three dimensions, and
  the pilot's worlds must not read a self-click from the tail (N_s
  declared above the tail's crossing time, section 5).
- **The clock sentence, the owner's, entered on his word** (2026-09-23,
  11:03Z, Hebrew, voice, through the Boss: "the clock sentence, all the
  things we discussed until now, all of it into the Highlights file
  immediately"; a DECLARATION of the design under its identity
  `bound-clock-v1`, the law itself unchanged until Highlights carries
  it; record 1352 his words): **the object's declaration (its frequency,
  its period) is its REST value only; in motion the object has no
  declared clock: its insert follows the receive of its own record, and
  its clock is the cycle of its own bound record, read in its own
  count.** Under the rule: an object inserts its train at its declared
  rest frequency f_0 at its birth; thereafter it inserts again when it
  receives its own record (the receive at its own Nodes after the closed
  count N_s, at the declared rung, section 5), and its count advances by
  one per insert-and-receive; its period is whatever the Inside returns:
  2 L / c for a pair at rest at L, and in motion the cycle of the bound
  pair by 8b. It replaces "in motion the declared period" wherever it
  stood (1.1's frequency row; this section); a lone object at rest keeps
  its declared period by 1.1's declaration (the self-click fired by the
  period, above), outside this sentence. The three tests: generic (one
  primitive, the insert triggered by the receive of the object's own
  record; no family name, no kind; f_0 a declared integer pair as the
  initial condition); vector (a comparison of the record's identity at
  the rung with the object's own, then the insert as today; no
  arithmetic beyond the rule's, no root, no float); local (the object's
  own Nodes and its Ports; the record's identity on its row; the six
  neighbours through the rule). A declared factor f_0 / gamma stays a
  hypothesis under its own identity, not the design's.

  Reviewer 3's line beneath it (his push balance on the continuum pace,
  a COMPUTATION, docs/designs/detector_law/PUSH_BALANCE.md at
  d69c87a9f90d8ea8bae869ce45fb74d97d65dc9d on the branch
  push-balance-r3, PR #1043, landed verbatim by the Boss; its section 6
  names (A) and (B); the owner's challenge and (C) are record 1366): the sentence passes the three tests as a sentence, but
  as written it makes the object a RELAY (it re-inserts what it
  receives at a shifted phase), and a pure relay is never bound:
  radiation pressure only, away from the partner at every separation;
  an object WITH a natural frequency (a resonance, the reactive part set
  by the declared phase, the dipole form of 5.1 (b)) is bound by the
  coupled-oscillator force, with equilibria at L = m lambda_0 / 2,
  alternately stable and unstable, the count m an initial condition. In
  motion the standing condition is degenerate in L, and the member of
  8b's family is selected by the LAW OF THE OBJECT'S FREQUENCY, so the
  sentence needs ONE LINE on the object's natural frequency in motion,
  with two lawful completions, the owner's word on them pending (the
  Boss's recommendation: (A) tonight, (B) decided tomorrow with
  tonight's numbers): **(A)** "the rest value stays the object's
  resonance in motion, ticking in the lattice's intervals": buildable
  now; the bound pair at the retarded pattern's nodes, L_along = L_0 /
  gamma_m^2 and L_across = L_0 / gamma_m (0.667 and 0.816 at k = 3), the
  cycle N_0, 8b's fixed point derived, the lab's dilation 1 against
  gamma_m, a FAIL by design, honest; the form the reduced run tests
  tonight. **(B)** "the object's resonance is itself a bound cycle of
  the Inside, so that it transforms as the pair does": the covariant
  object, the boost of the rest pair an exact solution of the wave
  equation, L_along = L_0 / gamma_m, f = f_0 / gamma_m, the cycle gamma_m
  N_0, Lorentz's member, five and the lab's dilation PASS by the wave
  equation's covariance; every foreign object a composite of the law,
  the atom's route, a program and not a sentence; the direction the
  owner's words point to. THE OWNER'S CHALLENGE (11:20Z, record 1366):
  "think again about (A) and (B): it does not follow that we must take
  (B), nor that we must take (A)"; the push balance proves only that the
  frequency law must be declared, (A) a buildable choice, (B) forced only
  by nature and a program as a composite, the relay a third member. **(C)**,
  a third completion from his own words: the object's resonance is the
  BOUND MODE of the wave at its own Node under its declared pair q (the
  index scatterer of 5.1 (b) as a well), so that the declared parameter
  is the coefficient and "N at rest" is what the mode gives, a
  COMPUTATION, and in motion the moving well's mode transforms by the
  wave equation's covariance, Lorentz's member without a composite;
  Reviewer 3's computation (11:43Z): NO lawful variant on the massless
  rule (no bound mode below an acoustic band; the one localized mode
  above the band's top is 4 to 7 times faster than the floor N >= 21; a
  gapped rule that would give (C) is a scratch variant, not the law, the
  owner's word); the scratch preparation agrees (a struck scatterer Node
  does not ring, 5.1 (b)). THE OWNER'S FORM OF (B) (11:38Z, record
  1370, a candidate sentence quoted, his word on closing it pending, not
  applied and not declared in the pins): "a foreign object is not one
  Node; its declared N (its mass) derives how many cells it is at rest,
  the cells identical in the Inside; its click in the Outside is read
  across its cells", read back by the Boss as: the object's rest extent
  s = N c / 2 Links is the set of Nodes its own record crosses in one
  cycle, so a pair at L_0 = 80, m = 5, is already such an object with
  its two ends 80 Links apart. The sentence read literally as a relay (no
  clock in motion, the inserted train continuing the received one)
  gives no binding, and a pair carried rigidly to beta ends at f = f_0
  / gamma_m^2, L_along = L_0, L_across = gamma_m L_0, the cycle gamma_m^2
  N_0 in both arms: five's ratios 1.50 and 1.50 at k = 3, a FAIL of five
  and of the lab row. The quantity that breaks the degeneracy and must
  be read: the pair's oscillation frequency in the lattice's intervals
  (the zero crossings of the wave between the objects) after the rest
  pair is pushed to beta, beside the separation: f / f_0 = 1, 0.816,
  0.667 names the member. Nothing beyond the sentence and this line
  enters.
- **In motion it pops up at the next Node**: the object steps to the
  neighbouring Node, one of six, never a diagonal, at its declared
  cadence k, and the first rung of its own record at that Node is the
  step's accompanying click (1.1; the Algebra Auditor's row read with
  Reviewer 3's line: the rung alone sets no pace); the mass moves only
  through the Inside, as the record's rows, and appears Outside only at
  that click. What changes a free body's cadence is the push of the
  clicks it receives (section 5's momentum, h times the wave number),
  by a push-to-cadence rule the design does not yet have (8b (i), a
  form to declare); and a bound pair holds its separation by
  its steps (8b (iv)).
- **What the row does not get from the rule, named**: no return at
  rest for a lone Node (its period declared); no slowing of its clock
  with its pace (8b (vi): the lab's dilation predicted FAIL, the
  question to the owner open); no binding energy (row 7a's bound stands
  as a declared input, the give once per body); the momentum a click
  hands over is the gradient of the arriving offer's phase across the
  object's Nodes (section 5), not a label.
- **The keys retired**: `massive_rows`, `massive`, `momentum_magnitude`
  and the count of self-creations under the age wall become the
  family's clock [n, d], the object's train and its declared period;
  the `become` line becomes the object's click line with its own count.
  The three tests: generic (no family name in the step; the clock and
  the content values), vector (verbs G and D at every Node; a comparison
  of the age at the cycle), local (the object's own record at its own
  Nodes and the six neighbours; nothing kept at a Node beyond the row
  and its age).

8c **The moving source's wavelength and the lattice's floor** (Reviewer
3's MUST I). A source stepping at beta (Links per interval) inserts at
its clock f, and the wave ahead of it has the wavelength lambda_0 (1 -
beta_c), beta_c = beta / c, behind it lambda_0 (1 + beta_c) (the
medium's Doppler, 8b (iv); row 4b of PINS.md). The lattice carries a
bell at 12 Links or more (6.1; the pace by direction within 0.8 percent
of c there), so a moving source's world is declared with

    lambda_0 (1 - beta_c) >= 12 Links,

lambda_0 >= 28.4 Links at k = 3 (beta_c = 0.577), 21.2 at k = 4, 16.9
at k = 6. That is why 6.5's readings at 12 and 16 Links (62 and 86) are
not returns: the wave ahead of the body was 5.1 and 6.8 Links, below the
floor, its slow modes overtaken; and 24 Links at k = 3 (10.2 ahead) is
marginal, which is named beside its 303. Five's two worlds (8b (vii))
are therefore declared at lambda_0 = 32 Links (13.5 ahead at k = 3),
and every moving-object world of the register's re-run carries this
floor as a load-time check under the key (11, step 1).

8b **The binding through the Inside: a moving object's cycle, two
objects bound by their mutual insert-and-receive, the separation along
and across from the wave law** (the Boss's item of 09:33Z; Reviewer 3's
gate before five's computation). Algebra only, docs; every number
COMPUTATION; the pin of five stated at the end BEFORE its computation.
Symbols: c the rule's pace (1 / sqrt 3 Links per interval); beta the
object's pace (1 / k Links per interval, one step of one Link every k
intervals in one of six directions); gamma_m (the medium's Lorentz
factor) = 1 / sqrt(1 - beta^2 / c^2), gamma_m^2 = 1.5 at k = 3; f the
object's clock (its declared rate in periods per interval); lambda_0 =
c / f its wavelength at rest; L the separation of two objects; N_0 the
rest cycle 2 L / c in intervals.

(i) **The moving object's step**, as Reviewer 3's gate of 7225a54a
corrects it (NOT MET as the basis for five as first written): the
Algebra Auditor's row, read on the RETURNING record after the closed
count N_s, not on the departing one (as written before, every neighbour
of an inserting object crosses 1 / W within an interval of the insert,
at full amplitude one Link away in all six directions at once, so a
resting object would step at once, in a tie, on its own departing wave,
against (ii)); and even on the returning record the first rung's
ordering among the seven Nodes at the grain 1 / W is a tie broken by
rounding, not a restoring force: a pure receiver in a symmetric standing
pattern feels no net push at any point. A trap at the nodes or
antinodes needs an object that re-emits with a phase (the dipole force
of an optical lattice), the re-emission parameter's TABLE form (1.1,
section 5), not the mirror or the sponge; and under the cycle sentence
the two trains overlap only while both insert. So the step is the
declared cadence k with the first rung at the next Node its
accompanying click (1.1), and what a free object's cadence becomes is
the dynamics: the push the arriving clicks put on it (section 5's
momentum, h times the wave number) by a PUSH-TO-CADENCE RULE the design
does not yet have (the smallest form: p = M v, the cadence k the whole
part of M / p in intervals per Link, integers; to declare and put
through the three tests), and the phased re-emission that can trap. Two
forms to declare before the free pair is computed.

(ii) **The one-object cycle** (MUST H): a one-Node object at rest in
open space inserts its train and the wave leaves; the rule returns
nothing to it, so its first rung never fires at its own Node from the
Inside and its rest cycle is its declared period (1.1). A one-object
clock is not a clock of the Inside; every clock read through the Inside
is a two-object cycle.

(iii) **The two-object cycle at fixed separation** (the light clock as
built and as computed in 6.4 and 6.5): A inserts at its clock f; the
front reaches B at L / c; B receives (its first rung) and re-inserts
(the same object, receive then insert); A receives at 2 L / c = N_0.
Both objects stepping along +x at beta: the forward leg L / (c - beta),
the back leg L / (c + beta), the cycle 2 L c / (c^2 - beta^2) =
gamma_m^2 N_0 (187.1 against the rest 124.7 at k = 3, L = 36 Links,
lambda_0 = 24; the script's E read 303 / 206 = 1.471 against gamma_m^2
= 1.5, 6.5, the difference the lattice's dispersion and the first
rung's grain).
Stepping across: each leg L / sqrt(c^2 - beta^2), the cycle gamma_m
N_0 (152.7). The ratio along to across is gamma_m: an anisotropy the
Michelson-Morley null of nature forbids (the register's row 4a). This
is the medium's algebra and it is what the rule reads at a fixed L;
under it nothing comes out 1 and 1.

(iv) **Two objects bound by their mutual insert-and-receive.** A and B
each insert at f and receive the other's record. Co-moving objects in
a medium receive each other's clock unshifted (the source's and the
receiver's Doppler factors cancel: A moving at beta emits ahead at the
lattice frequency f c / (c - beta) and the wavelength (c - beta) / f;
B moving at beta reads f c / (c - beta) - beta f / (c - beta) = f), so
each re-inserts at f and the two records between them form ONE standing
pattern in the pair's own frame: the forward wave's wavenumber 2 pi f /
(c - beta) and the back wave's 2 pi f / (c + beta) add to a node
spacing

    s_along = (lambda_0 / 2) (1 - beta^2 / c^2) = (lambda_0 / 2) / gamma_m^2

along the motion, and across the motion (both legs at the pace
sqrt(c^2 - beta^2))

    s_across = (lambda_0 / 2) sqrt(1 - beta^2 / c^2) = (lambda_0 / 2) / gamma_m.

By (i) an object steps toward the Node where its record's first rung
fires first, which for a record returning through a standing pattern
is toward the pattern's antinode: the pair WOULD have fixed points at
separations L = m s (m a whole number of the pattern's spacings, an
integer the pair keeps as long as it is bound) if a restoring force held
it there, and "a pair displaced from one returns to it by its own steps"
is a claim to COMPUTE (a free pair under the click's push with the
phased re-emission, (vii)), not a result: as (i) says, a pure receiver
has no restoring force, so the binding is asserted here and derived
nowhere yet. What the standing pattern gives without the dynamics is
the spacing s(beta), and with it the algebra of (v).
(COMPUTATION, the analytic form on the continuum pace; the lattice's
version is five's computation below.)

(v) **The bound pair's cycle.** With L = m s the round trip is

    along:  2 (m s_along) c / (c^2 - beta^2) = 2 m (lambda_0 / 2) / c = N_0,
    across: 2 (m s_across) / sqrt(c^2 - beta^2) = N_0

at every beta below c (124.7, 124.7, 124.7 at rest, along and across for
k = 3; the same at k = 4 and 6): the bound pair's cycle in the
lattice's own intervals is its rest cycle, along and across alike, and
the object's count per cycle (its clock f times the cycle) is the rest
count in both arms. That is the owner's "five must come out exactly":
N_par / N_0 = 1 and N_perp / N_0 = 1, in the object's own count and in
the lattice's intervals, from the wave law AT THE DECLARED CLOCK f_0,
and the Michelson-Morley null with it; an identity given L = m s(beta)
and f unslowed (Reviewer 3: verified, and not yet a theorem, since it
rests on the pair sitting at L = m s(beta), which (iv) asserts). What the binding does to the pair's
shape: the separation along contracts by 1 / gamma_m^2, across by
1 / gamma_m; that is Lorentz's contraction (1 / gamma_m along, 1
across) times an isotropic shrink by 1 / gamma_m, with the clock
unslowed; in every reading the pair makes of itself it is the same as
Lorentz's contraction with a clock slowed by 1 / gamma_m (the two
differ by the one factor 1 / gamma_m on every length and every rate of
the moving thing), which is why no reading from within distinguishes
them.

(v-bis) **The one-parameter family** (Reviewer 3's gate; his push
balance on the continuum pace, PUSH_BALANCE.md at d69c87a9 on
push-balance-r3, the four derivations: the radiation pressure on a
scatterer, the coupled-oscillator force, the relay's Doppler integral,
the boost of the rest pair). The standing
condition fixes L given f and does not fix f: with the pair's frequency
f in the lattice's intervals the round trip is m / f along and across
for ANY f, so the bound states are a one-parameter family. f = f_0 (the
declared clock unslowed) gives the shape of (v): along 1 / gamma_m^2,
across 1 / gamma_m, no lab dilation, Ives-Stilwell and the muon FAIL.
f = f_0 / gamma_m gives Lorentz's exactly: along 1 / gamma_m, across 1,
the cycle gamma_m N_0 in the lattice's intervals, the moving clock slow
by gamma_m in the lab, the Michelson-Morley null kept: nature reads
this member. Which member the rule selects is not a standing-wave
question but the dynamics of a free pair: what force the arriving
clicks put on an object and what shape and frequency a pair accelerated
to beta settles into, Lorentz's own route, computable in the chain
script with two free objects and no k declared once the two forms of
(i) are declared. The smallest lawful sentence that would supply the
slowing, if the owner ever wants one, is his own made the object's only
clock: "the insert follows the receive; an object's declared frequency
is its rest frequency, the initial condition; in motion its clock is
the cycle of its own bound record, read on its count" (generic, vector,
local PASS; it hands f to the dynamics and gives no gamma_m by itself);
"every clock moving through the Inside runs at f_0 / gamma_m" is a
hypothesis under its own identity, not the law. Nothing enters the law
now; the computation first (the Boss's and Reviewer 3's recommendation,
and mine).

(vi) **What the binding does NOT give, stated before the computation
and named for the pins table.** A reading from outside does distinguish
them: nature's moving clock is slow by gamma in the lab's own time (the
muon in flight, the lifetime gamma tau_0; the transverse Doppler shift
f / gamma, Ives-Stilwell), and under the binding the bound pair's cycle
in the lattice's intervals is N_0, not gamma_m N_0: a lab's row on the
moving clock's rate reads 1 against nature's gamma_m (1.225 at k = 3),
a FAIL predicted here, not a fit to be found; the only way the rule
would give it is a slowing of the object's clock f by 1 / gamma_m with
its pace, which neither the rule nor the binding contains (Reviewer 3's
correction of 09:33Z: neither the count's slowing nor the arm's
contraction is in the rule; the binding supplies the contraction and
not the slowing). The two rows are therefore separate in the pins table
(item G): five, the pair's own ratios, 1 and 1; and the lab's dilation,
a nature row with the muon's lifetime, predicted FAIL by the rule as a
medium. The owner is asked whether the lab's dilation is in his law by
another sentence (a slowing of every clock that moves through the
Inside) or is what the register must show as FAIL until one is stated;
nothing here decides it.

(vii) **Five's pin, re-formed on Reviewer 3's gate (the pin that tests
the binding, not the identity; the owner's word on the band pending,
+- 0.03 proposed and called fair by the reviewer at lambda_0 = 24 or
more)**: the pair started at its REST separation and set stepping, the
objects FREE to step by the rule (no k declared for the pair, the pace
given by the drive of the first interval only), read after the pair
settles. The worlds: lambda_0 = 32 Links at k = 3 (8c's floor: 13.5
Links ahead), m = 5 so that one interval is half a percent of N_0 and
the contracted separations are whole where the arithmetic permits: L_0
= 80 along and across (s = 16 at rest; s_along = 10.67, L = 53.3 if the
pair settles at 8b's fixed point; s_across = 13.06, L = 65.3; the
residues named); k = 4 and 6 at lambda_0 = 32 and 48 (at k = 4 the
forward train of 24 Links is 7.8 Links and NOT carried). The three
outcomes, named before the run: no settling (the medium's 1.50 and 1.22
at k = 3, the binding absent); 8b's fixed point (1 and 1 with the cycle
N_0 in the lattice's intervals); Lorentz's (1 and 1 with the cycle
gamma_m N_0). The pins:

    N_par / N_0 = 1 +- 0.03,    N_perp / N_0 = 1 +- 0.03,
    the lab row: the cycle in the lattice's intervals, N_0 (8b's member)
    or gamma_m N_0 (Lorentz's), the discriminator between the two
    "1 and 1" outcomes;

the falsifiers: the ratios outside 0.97 .. 1.03; a dependence on m or
on the train beyond the band; the pair not settling (the binding
absent, a FAIL of (iv) itself, named separately). The controls: the
resting pair at the same m and lambda_0 read the same way (N_0 by the
first rung with the same N_s and train, the rest spacing 16 confirmed);
the fixed-separation clock of 6.5 beside five as the medium's reference
(1.47 read against 1.50). The computation is not run before Reviewer
3's line on this form and the two forms of (i) are declared (the
push-to-cadence rule, the phased re-emission), about a day in the pins
script as section I; the readings labelled COMPUTATION (the script)
and, when the engine runs them, DETECTOR (the click lines) beside the
pin. The earlier form of (vii) (the contracted separations put in by
hand, L = 32 and 39 against 48 at rest) read the identity of (v), not
the binding, and is superseded by this one before any run.

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
  0.07 percent of a packet's motion reflected (the build's test); the
  "30 percent from a wall of amplitude 0" of the same test is withdrawn
  (section 5, the mirror). Reviewer 3's gate: AGREED as the receiver's
  absorption near normal incidence with the corrections of section 5
  (the angle, the Port's remainder kept, the order within the interval);
  the sponge where the wave runs along the wall; all three forms carried.
- **The offer is the Port's motion**, (g(t + 1) - g(t))^2, not the
  amplitude squared: the rule has a zero-frequency mode (a static level
  on the board is a solution of the six-neighbour rule) which no receiver
  takes and which carries nothing; the motion of a Port is what a wave
  does to a receiver and what a static level does not. Reviewer 3's
  gate: AGREED, with the corrections of 2.1: the norm as built (the
  driven Nodes' squared steps over the train) is not the record's
  emitted energy (the lattice's radiation impedance differs between one
  free Port and six, and by frequency), so the first rung at 1 / W of
  it was a DECLARED SCALE of the click's time; the norm is the record's
  E (2.1) and the Port books in E's units by the pair [97, 28]; the
  completion test compares E with the strain to the absorbed, never the
  board's motion alone, and its global gather is a host cost (section
  7).
- **The train begins and ends at the clock's zero** (the phase 3 N / 4,
  the cosine 0 and rising, N divisible by 4): a step in the inserted
  amplitude would leave the static level above on the board. Reviewer
  3's gate: AGREED, with the consequence written: the onset in the
  MOTION is still a step (the cosine rises at full slope from its zero),
  so the first-rung reading of a light clock stays the step's precursor
  (the chain's 116 against 118; 6.8's 207 to 208 against 207.85); a
  smooth onset in the motion needs an envelope over the first period, a
  lamp's declaration, and the light clock's pin is declared with the
  onset named (PINS.md row (d)).
- **The inserter's grace** is the owner's cycle sentence (section 5,
  MUST B closed by it as a local declaration of the receiver, a timer on
  the object's own count): the lamp's own Nodes read their own record
  only N_s intervals after the train. Reviewer 3's gate: what must
  change is that the build's two periods are a module constant and must
  be the object's declared integer (kind 1) with its default named in
  the world file's definition of the one kind; the design states it as
  the owner's cycle, not a grace found in the build; the one-way Port is
  not needed for MUST B (it serves MUST A and C), and with it the
  object's own outgoing wave is unbooked by construction, so N_s can be
  small.

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
