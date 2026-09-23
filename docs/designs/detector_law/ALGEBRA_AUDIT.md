# The algebra's audit of the Inside and the Outside under the local detector law: is the Outside local, and which definitions still put a thing on the board (the Algebra Auditor, 2026-09-23, docs only)

The Boss's order of 2026-09-23 (about 08:43Z, on the model owner's words of
that morning, records 1321 to 1336 of [docs/LOG_2026-09-20.md](../../LOG_2026-09-20.md)):
two parts, no run, nothing derived that needs a run, no file edited but
this one and the index row. Part 1 answers the owner's question of
record 1329 ("I think they said the Outside comes out local") under the
new design, `docs/designs/detector_law/DESIGN.md` on the branch
`detector-law-design` (not on `origin/main`; read at 7eb1336c, its rule in section 2, its click and books in
section 5, its terms in sections 0 and 1). Part 2 audits the algebraic
definitions on `origin/main` (ed667ed1) against the owner's terms. Every
line number below is of that head; every quotation is verbatim; every
rewrite is a proposal for the one writer of its file, routed by the
Boss, and nothing here is a decision.

**The owner's terms, the law's terms for this audit** (records 1323 to
1329; [docs/HIGHLIGHTS.md](../../HIGHLIGHTS.md) 5.4, the split line;
[POSTULATES.md](../../../POSTULATES.md) section 26;
[docs/TERMINOLOGY.md](../../TERMINOLOGY.md), "Inside and Outside"):
the Inside is the board itself, the free Nodes and the record's rows on
them, where the ray (the record) splits at every free Node to its six
neighbours and holds its amplitudes; nothing is inserted into the Inside
as a thing of the board; the Outside has no board, only clicks passing
from Node to Node, and a passage from Node to Node is possible only
through a detector, at rest (the same Node) or moving (the next Node),
which carries the mass through the Inside in its cycle time; "there is
no field"; every instrument on the board (a lamp, a slit, a wall, a
screen, a polariser, a receiver body, a body) is the Outside; a detector
and an emitter are one generic thing with one trigger, the counting
form at the first rung (record 1288; the insertion follows the click);
there are no other kinds on the board than the free Node and the
detector-emitter; all the Inside's laws run local; and the owner asks
whether the Outside is also local.

## Part 1. Locality Outside under the new design

### 1.1 What the algebra already states, quoted

**The click frame's locality-Outside clause**,
[docs/designs/click_frame/DERIVATION.md](../click_frame/DERIVATION.md):

- Lines 55-64: "LOCALITY OUTSIDE (the owner's word, 2026-09-22, as the
  Boss relayed it: 'velocity in the real world is passing a click with
  information to the neighbouring Node and receiving that packet there,
  having in effect moved there; the packet passes from place to place,
  it cannot jump: a kind of locality also Outside'): every Outside
  passage is a chain of clicks between neighbouring places, so the
  Outside inherits the Inside's locality through the conversion. It
  forbids a reading that would need a jump, a velocity above one Node
  per interval of the tick".
- Lines 68-76: "It is A1 read from above, and it FOLLOWS FROM A1 ALONE
  together with the definition of Outside (nothing leaves the board but
  clicks, P6): every Outside event is a click, every click moves
  information one Node at most, so every Outside passage is a chain of
  neighbour steps; a theorem, not an added assumption, with the one
  exception the title names, the pair's click, one gather of one record
  from both settings, which is not a chain of neighbour steps and is the
  law's one non-local operation."
- Lines 1454-1459, the closing theorem: "Locality Outside (section 0):
  every passage in O is a chain of clicks between neighbouring places,
  so O inherits I's locality through the map, a theorem of A1 and the
  definition of O, with the pair's gather (P6) the one exception; the
  bound is one Node per interval of the tick, `1 / r_D` Nodes per the
  detector's own count."
- Lines 1852-1860, "The locality sentence, in the algebra's words":
  "The title says the law is local and the read-out is not. The
  non-locality sits in ONE object: the pair's record, an element of
  `Z[Z_N] (x) Z^2 (x) Z^2` of tensor rank 2, carried by local verbs on
  two arms (each row at its own Node with its six neighbours; no Node
  keeps anything beyond the events there, P4, the law of events) and
  read by ONE gather at two clicks (P6, the one non-local operation)."
  And lines 1874-1876: "(iii) The non-locality is the tensor rank 2 of
  one record read by one gather at two clicks; the rows are local and no
  Node keeps anything, so the law is local and its read-out is not."
- Lines 76-95, the one assumption beyond the theorem: "its second half
  (that WE are built of clicks, that the emitters and the detectors are
  themselves records of the board and not a second kind of thing) is
  MORE than A1: it is the statement that the apparatus is inside the
  law, which the law today does not carry (a detector, a lamp and an
  external body are declarations of the world file, not records that
  hop ...), so it is an assumption about the world, or a programme for
  the law, and not a theorem of the conversion."

**What [docs/ALGEBRA.md](../../ALGEBRA.md) says of it:**

- 3.1, lines 610-614: "a record is read once by one comparison and
  deleted: the only read-out, the one deletion, and the one non-local
  step (the pair's gather, 3.6)."
- 3.4, lines 708-720: "Locality Outside (a theorem of (A1) with the
  definition of Outside, P6, nothing leaves the board but clicks): every
  Outside event is a click, every click moves information one Node at
  most, so every Outside passage is a chain of neighbour steps between
  neighbouring places, and the Outside inherits the Inside's locality
  through the conversion; it forbids a reading that would need a jump
  ... and a detector reading at a place no chain of clicks reaches; the
  one exception is the pair's click, one gather of one record from both
  settings, the law's one non-local operation."
- 3.4, lines 743-751: the same "one assumption beyond" as the click
  frame's lines 76-95, "a detector, a lamp and an external body are
  declarations of the world file, not records that hop".
- 3.5, lines 757-765: "The conversion Phi: Inside -> Outside is a
  composite of four maps ...: on the amplitude, Outside = rung o (chi_1
  of f* f) o ev on the record's element of Z[Z_N] ...; on the schedule,
  Outside = (Nodes apart) / (counts apart) in Q ...; both sides read at
  the detector's own count."
- 3.6, lines 806-809: "The non-locality sits in one object, the pair's
  record of tensor rank 2, carried by local verbs on two arms and read
  by one gather at two clicks".
- Chapter 5's hypotheses, lines 1025-1032: "(A3) Locality Outside: every
  Outside passage of a body or a signal is a chain of clicks between
  neighbouring places, so the Outside inherits the Inside's locality
  through the conversion; it forbids a velocity Outside above one Node
  per interval, a jump, and a reading at a place no chain of clicks
  reaches".
- The close, lines 2014-2015: "a transformation for every formula with
  the detector at the place, locality Outside."

### 1.2 The verdict under the design's rule and click

**LOCAL EXCEPT the completion of a record** (the design's section 5:
the exhaustion test of the record's offer over the pointers of every
detector it has reached, the choice of the cell by `cell_of` over those
pointers and the deletion of every row of the record on the board; one
gather of one record from all its detectors, the host's one non-local
step). The reason, in the algebra's words: the rule is one map on the
record's own row at a Node, `3 a_next + r' = (a_E + ... + a_D) - 3
a_before + r`, whose inputs are the six neighbours' `a_now` and the
row's own past, so information moves at most one Link per interval on
the Inside, which is (A1) exactly, the same premise the theorem used
(the row on a digital line also moved at most one Link per interval;
the theorem never used the line, only the bound); the definition of the
Outside is now the owner's own sentence (nothing leaves the board but
clicks, and a passage from Node to Node only through a detector), which
is (P6) sharpened, since a click is at one Node with what arrived there
and a moving detector is a click at this Node followed by a click at the
next; so Locality Outside remains a theorem of the same two premises
and is in fact stronger than before: the owner's rule "you must jump to
a Node through a detector" makes every Outside step a click of one
detector-emitter at one Node, whereas (A1) alone allowed a whole row to
hop between declared things without clicking, the bug of record 1323.
The click's time, the interval at which the chosen cell's pointer
crossed its first rung (the counting form, `s_D = 1 / W`), is local to
that detector's own record; the mass a moving detector carries passes
through the Inside in the record's rows and appears Outside only at the
click, a chain of neighbour steps. What is not local is exactly what was
not local before and nothing more: the read-out of one record at several
places, the one gather that decides which detector clicks and removes
the record's rows everywhere; the pair's gather at two settings (Bell,
tensor rank 2) is the two-detector case of it, and a screen of many
pixels reading one record is the many-detector case. So the owner's
"the Outside comes out local" is right for every passage and every
velocity Outside, as a theorem; the one non-local thing is the
completion, the host's, and the algebra can say no more than that
without a run (whether the design's exhaustion at the norm less the
grain gives one click per record at every wavelength is the pins'
question, section 6, not the algebra's).

**Does the earlier theorem's map still apply** when the passage Outside
happens only through a detector and the record's rows are at Nodes
rather than on lines? The theorem applies; the map changes in one of its
two halves. The schedule half is unchanged in form: Outside = (Nodes
apart) / (counts apart), read at the detector's own count; the
transponding record's step `place_(j+1) - place_j = e_j d_hat` with
`e_j` in {0, 1} (ALGEBRA 3.4, discreteness Outside (iii)) is now the
moving detector's click at the next Node, one Node per cycle, the same
quantum. The amplitude half is not the same map: the record is no longer
an element of `Z[Z_N]` evaluated at the circle by `ev`, with the click's
weight `chi_1(f* f)`; under the design the record's amplitude at a Node
is a signed integer `a_now` on the wheel, the interference is the signed
sum at the Node (verb G, the rule's own addition) and the detector's
weight is the sum over its Nodes and its intervals of `a_now^2`, the
offer, thresholded by the rung. Both maps are a positive quadratic form
followed by a rung (the lattice Gleason of ALGEBRA 4.8 in form), so the
theorem's use of the map (a click is read at a detector from what
arrived there, and nothing else leaves the board) holds; what does not
carry over unread is the conversion table of the click frame's section 7
(3) (nine Inside formulas and their Outside readings), whose amplitude
rows were written for `ev` on the group ring and must be written again
for the offer's sum; that is the algebra's work after the design's pins,
not a run's. Two things the algebra notes for the theorem's writer,
without deciding them: (i) the exception should be named as every
record's completion over all its detectors, of which the pair's gather
is the two-arm case (ALGEBRA 3.1's "the pair's gather" and the click
frame's "the pair's click" under-name it; the law as built already
completes a two-slit record over every cell of the screen by the same
gather); (ii) the "one assumption beyond" of the click frame's lines
76-95 and ALGEBRA's 743-751 is answered by the owner's terms: the
detector-emitter is a declaration of the world file, the Outside, and
not a record that hops; the sentence should say so and drop "a programme
for the law" (Part 2, row A2).

**A contract the verdict touches.** LOCALITY-1
([SIMULATOR_DEFINITIONS.md](../../../SIMULATOR_DEFINITIONS.md), lines
410-416) says every physical update uses its fixed local records and six
neighbours and that a read-only diagnostic "must never repair its
physical state"; it names no place for the host's one non-local step,
which is not a diagnostic (it deletes the record's rows and hands the
content). Highlights 5.4 line 518 names it ("the detectors' shared
record is the apparatus's, at the one-way place, the only non-local
operation") and the design's section 5 counts it as the host's. The
clause belongs in LOCALITY-1 (Part 2, the list after the table).

## Part 2. The audit of the definitions against the owner's words

The four marks: (a) lets something be inserted into the Inside or names
a thing of the board beside the records and the free Nodes (a field, a
store, a register, a remainder or a draw at a Node); (b) names an
instrument as Inside or gives an apparatus a rule at a free Node (a fan
table, a Huygens split at an opening, a line on the lattice between an
emitter and a detector, a mirror's rerelease as a law); (c) names a kind
of Node or of thing on the board other than the free Node and the
detector-emitter, or a second trigger; (d) contradicts the one generic
detector-emitter with one trigger. The last column: HISTORY is a dated
record of what was, allowed to stand as history; LAW is a statement of
the law as it is, to change (for a statement of the engine as built,
the change lands with the design's build, not before; until then the
sentence describes the baseline the pilot measures, and the rewrite is
what it becomes). A rewrite in quotation marks is the proposed sentence.

### 2.1 docs/ALGEBRA.md

| Row | Line | The sentence, quoted | Mark | The rewrite or DELETE | Status |
| --- | --- | --- | --- | --- | --- |
| A1 | 389-391 | "every count of the law is this: the flight on the digital line, the phase's turn, the age, the drive, the owed count, the release, the lamp's wheel, the push per column" | (b) | "every count of the law is this: the rule's step at the Node (the pair [1, 3]), the phase of the train, the age, the owed count, the release, the lamp's wheel, the push per column; the flight on the digital line is the engine as built" | LAW |
| A2 | 743-751 | "that the emitters and the detectors are themselves records of the board and not a second kind of thing, is MORE than (A1): it is the statement that the apparatus is inside the law, which the law today does not carry (a detector, a lamp and an external body are declarations of the world file, not records that hop), an assumption about the world or a programme for the law" | (c) (d) | "a detector-emitter, one generic kind, is a declaration of the world file, the Outside, and never a record of the board (the owner, 2026-09-23, DESIGN.md section 0, statement 6); the owner's 'we are operated Outside, by emitters and clicks' is read as: by detector-emitters, not that they are records that hop" | LAW |
| A3 | 1041 | "the fan's count K, Q, N, the lamp's pair [n_K, d_K], the quantum h" (the declared inputs the formulas carry) | (b) | drop "the fan's count K"; the lamp's train length enters in its place (DESIGN.md section 2) | LAW |
| A4 | 1497-1498 | "a row meets no surface; a mirror is the apparatus's declared table; no crowd slows or bends a row on main" | (b) | "a record meets no surface; there is no mirror on the board, the far end is a receiver body, a detector-emitter that clicks and re-emits (record 1227; Highlights 5.4 line 467)" | LAW |
| A5 | 1566-1570 | "the register's fan of 2616 directions has its ring flux falling as r^-1.83 (GAMEBOARD), so the ladder's exponent on the lattice is 2 / (3 - k) = 1.709 at k = 1.83, the fan's table and not (j / i)^2 ... (the fan the apparatus's declaration)" | (b) | the number stays as the engine as built's dated GAMEBOARD reading; the clause becomes "the fan an instrument above the board of the engine as built, gone under the design (DESIGN.md 4.2)" | HISTORY (the reading); LAW (the clause) |
| A6 | 1626-1627 | "so a row's path is the Bresenham line of its direction and its arrival count L tau_L within 1 / T_D whether or not a crowd lies on the path" | (b) | "on the engine as built ... (the bug of record 1323); under the design a record has no path: its arrival is the front of its offer at the detector's first rung, its bend the stretched pace at the Nodes (DESIGN.md 4.1)" | LAW |
| A7 | 1393-1394 | "which counts of the law are such counts is a declaration (BEAM_LAW note 48: the threshold, the window, the click and the push read the same `met`)" | (d) | "(the click and the push read the same `met`; the threshold is gone, DESIGN.md 4.3; the window is a rotation's setting, not a gate)" | LAW |
| A8 | 1825 | row 2a: "SHOWN: the counts per cell bit for bit from the fan, the weights and the wheel" | (b) | no rewrite: a registered reading of the engine as built; the row's status word changes when the design's pin (0.98 at the scaled world, DESIGN.md section 6) replaces the fan's | HISTORY |

### 2.2 POSTULATES.md

| Row | Line | The sentence, quoted | Mark | The rewrite or DELETE | Status |
| --- | --- | --- | --- | --- | --- |
| P1 | 185-186 | "An event is a local change in a node at a particular time: a field update, a particle momentum change, a move to a neighbor or a blocked move attempt." | (a) | "An event is a change of a record's row at a Node: the rule's step, a click at a detector-emitter, or the insertion that follows a click" (or the section's history marker, since lines 193-195 call this "the current implementation" of a deleted engine) | LAW (unmarked) |
| P2 | 384-385 | "A particle occupying a node remains a source every tick even without moving. Its presence in that node represents the source." | (a) | mark section 6 history (the scalar candidate, deleted 2026-09-17) or "a body at a Node is a detector-emitter; its insertions are its record's births at its own cycle (DESIGN.md section 8)" | LAW (unmarked) |
| P3 | 496-497 | "The historical scalar field law uses six neighbors, the local source and a retained remainder." | (a) | stands as history (marked "historical") | HISTORY |
| P4 | 551-553 | "They neither direct particle motion nor repair the field. Here measurement means diagnostics, not a quantum interaction that creates a new physical record." | (a) | stands; lines 548-549 already mark it superseded and kept as history | HISTORY |
| P5 | 558-566 | "the two marks of a world, the Detector and the external body (section 23, Highlights 3.19), are its whole apparatus: they are the only places where the GameBoard does something the tables do not say, and both are declarations in the initial file, never physics. The Detector's draw is the one measurement that is an interaction" | (c) (a) | "the one mark of a world, the detector-emitter, is its whole apparatus, the Outside, a declaration of the world file and never a thing of the board; nothing draws; the click is the one measurement" | LAW (a dated addition that section 10 cites as live) |
| P6 | 1039-1050 | "there is one kind of thing on the GameBoard, a ray, ... a family is a field, its free rays what physics calls the field ... the only draw is at a marked Node, and the picture of the world is the list of PASS clicks" | (a) (c) | stands as history (section 23, 2026-09-17, superseded by section 25 and the Beam Law; "ray" retired, TERMINOLOGY.md line 631); section 26.4's citation "section 23 (every trajectory an interaction permits happens ...)" should cite the record, not the superseded section | HISTORY |
| P7 | 1155-1158 | "A source is a Detector: whatever emits a ray of a known family is a marked node, because knowing the family of what it emits is a measurement" | (c); (d) in agreement | stands as history; the first statement of the one generic thing, worth citing in the design's section 0 | HISTORY |
| P8 | 1304-1323 | "beside the Detector there is one more declared element of a world, and like the Detector it is a declaration, not physics: the external body ... a reversed heading is a mirror, a split by a declared table is a beam splitter, a phase offset is a phase plate, a polarization read is a polarizer ...; a wall, a screen and a beam stop are the default" | (c) (b) | stands as history (2026-09-17); its live citation is section 10 line 559, rewritten in row P5 | HISTORY |
| P9 | 1372-1383 | "The model has exactly two definitions, event and ray ... if that event was at a Detector, the ray records that it was a Detector event and the bit drawn, 1 or 0, and the bit is all the Detector adds" | (a) (c) | stands as history (section 24, 2026-09-17; the bit retired 2026-09-18) | HISTORY |
| P10 | 1546-1549 | "A node is its six Ports and holds nothing else: the remainder is a shadow parked at the node, a mark's counter is a thing resident at the mark, and the apparatus are things with declared tables." | (a) (c) | stands as history (section 25, the law of the bit, superseded 2026-09-19) | HISTORY |
| P11 | 1629-1633 | "What arrives with a record and is read as it is: its content (the mass), its amount, its label **p** (the momentum vector, its direction and its size), its phase, its number and its own age" | (b) | "its content (the mass), its phase and its own age; its momentum a READING of the arriving offer's phase gradient across the detector's Nodes (DESIGN.md 4.1 and 5), not a label carried" | LAW (marked "by the code"; changes on the build) |
| P12 | 1658-1659 | "the fan carries every declared direction; 'all the possibilities' are the rows that could click" | (b) | "the split at every free Node carries every direction; 'all the possibilities' are the record's rows at every Node it has reached" | LAW (the Boss's precision, marked as his) |
| P13 | 1615-1617 | "the count needs a body, a measured event (an open face has no clock of its own, docs/TERMINOLOGY.md, 'A detector's clock')" | (c) | a question (Q1): whether an open face is a detector-emitter without mass, a third kind, or the board's edge and no thing; the rewrite after the owner's word | LAW |
| P14 | 1628-1629 | "a light packet carries the content of its own paid family and never the emitter's held mass, which does not pass" | (d) | "a light packet carries its own quantum h; a detector's mass passes through the Inside only in the detector's own record, at rest to its own Node and in motion to the next (the owner's statement 5; DESIGN.md section 8)" | LAW |

### 2.3 docs/TERMINOLOGY.md

| Row | Line | The sentence, quoted | Mark | The rewrite or DELETE | Status |
| --- | --- | --- | --- | --- | --- |
| T1 | 73-77 | "Row: the record of an event in transit, `NatureBeam` in the code: a Node, a direction, an age, a phase, a number, an amount and a content per unit, moving along the digital line of its direction at one pace for every direction" | (b) | "Row: a record's amplitude at a Node: `a_now` and `a_before` on the record's wheel and a remainder `r`, re-emitted every interval to the six neighbours less the row's past (DESIGN.md section 2); no direction and no line" | LAW |
| T2 | 85-90 | "carried through every split, re-emission, rotation and gate; one record is one quantum of the world's list of clicks, its rows are its paths, its click is one" | (b) | "its rows are its amplitudes at the Nodes it has reached, its click is one" | LAW |
| T3 | 109-111 | "Phase: a step of the circle of N: on a row, stamped by the emitter's clock at birth and turned by the family's `phase_per_link` at every Link crossed" | (b) | "Phase: on a record, the phase of its train at the source (`a_now(t) = A cos(2 pi t n / (d N))`, DESIGN.md section 2), carried by the rule's signed sum and read at a detector" | LAW |
| T4 | 122-128 | "Direction: an index into the world's direction table: 0 and 1 the two rest directions, 2 .. 7 the six headings in Port order, 8 .. the declared primitive vectors **D** with components in -P .. P" | (b) | "the six headings in Port order are the rule's only directions; a momentum's direction is a reading at a detector (the phase gradient); the table **D** and the width P are the engine as built" | LAW |
| T5 | 226-236 | "The label by Bresenham: a pushed row's whole momentum **P** ... is the line its label follows: among its direction and the fan neighbours the label whose next Link **h** keeps abs(**c** + **h** x **P**)^2 smallest ... **c** the row's error accumulator" | (b) | DELETE under the design (DESIGN.md 4.1: the label, the line and the accumulator gone from the free Node; the push acts on the pace at the Node); the engine as built until the build | LAW |
| T6 | 346-347 | "A rebirth at a re-emitter that is no lamp keeps u = its count of births less one mod N." | (d) | "a re-emission is an insertion by the one detector-emitter after its click; u is its own count of births" | LAW |
| T7 | 360-363 | "Split: a `rerelease` entry with `weights`: an arriving row leaves as the rows w a_i with the multiplicity m x A and the phase + t_i, the multiplication by the apparatus's integer matrix" | (b) | "Split: the rule at every free Node, the re-emission to the six neighbours (DESIGN.md section 2); an apparatus's matrix (a polariser's rotation) is a detector-emitter's rule at its own Node" | LAW |
| T8 | 364-366 | "Fan: every re-emitter emits on all primitive directions within P, each weighted by the angle it covers, Huygens on the lattice; decided, not built" | (b) | DELETE (an instrument above the board of the engine as built, DESIGN.md 4.2); the retired-words table takes it | LAW |
| T9 | 367-371 | "Re-emission: a `rerelease` entry: the rows it takes are created again at the Node's next self-creation on the body's `directions`, apportioned whole, with the arriving phase and content, the re-emitter's number, age 0 and the recoil taken" | (b) (d) | "Re-emission: the insertion that follows a detector-emitter's click (record 1288): a new record born at its own Node, driven by its clock at the arrival's phase (DESIGN.md 4.2, the receiver body); no directions" | LAW |
| T10 | 372-376 | "Transformation (`become`, `weak-v1`): ... a clock trigger (`at`, gated by `crowd`) and a click trigger (note 36 (iii))" | (c) | a question (Q2): whether the clock trigger is the detector-emitter's own cycle (its self-creation, the click at its own Node, DESIGN.md section 8) and so the one trigger, or a second; the rewrite after the owner's word | LAW |
| T11 | 378-383 | "Contact: a body's step refused because the destination holds another body, read through the occupant's table entry for the body's family: `measure` hands the momentum component over, `rerelease` returns it, `read` and `pass` leave it" | (d) | a question (Q4): under the moving detector a body reaches the next Node by a click there, so a contact is a click at an occupied Node read by the occupant; the rewrite after the design's massive form is pinned | LAW |
| T12 | 384-388 | "Window: a table entry's or a lamp's setting `phase_window` s and width `phase_width` w, the w consecutive steps of the circle about s a phase must be in to be admitted, N / 2 by default" | (d) | "Window: the setting s of a detector-emitter's rotation (the polariser's tables, DESIGN.md 4.2), never a gate on the click" | LAW |
| T13 | 389-391 | "Threshold: a detector set's `threshold`, the amount summed over the set in one interval below which every row passes with a `pass` record; the sensitivity; at a record's click the divisor of the rungs" | (d) | DELETE (DESIGN.md 4.3: the counting form at s_D = 1 / W the only trigger; a less sensitive detector is a larger body or a coarser wheel; record 1327: the sensitivity is the one thing's clock) | LAW |
| T14 | 392-395 | "Lamp: a body's declared source: at its self-creations it births rows of its family with its amount, phase and wheel value, in a recorded world one record per birth, at its declared `rate` and `wheel`" | (d) | "Lamp: the insertion act of a detector-emitter, the birth of a record at its own Node driven by its clock for the train's length (DESIGN.md section 2); not a kind of thing; its rate is the one thing's clock (record 1327)" | LAW |
| T15 | 398-401 | "Detector: a declared set of measured events (`detectors[].positions`) with one record; a click says 'here, in one of these', the set's extent the position's uncertainty" | (d) | "Detector-emitter: a declared set of measured events with mass and one record; it receives (the click) and inserts (the birth, the re-emission) through the Inside, its clock the return to its own Node (POSTULATES 26.1); a click says 'here, in one of these'" | LAW |
| T16 | 402-405 | "Step: the Link a body's drive counts on an axis; refused onto a Node that holds a body (a contact); a body on a set moves as one; before the law in the interval's order" | (d) | "Step: a body's passage to the next Node is a click there, the moving detector: its record spreads through the Inside and its first rung crosses at the next Node (DESIGN.md sections 1 and 8); the drive's count is the engine as built" (Q4) | LAW |
| T17 | 432-436 | "A detector without a body (an open face) has no clock of its own; the tick of its click line is the record's ordering, GAMEBOARD." | (c) | as P13 (Q1) | LAW |

### 2.4 SIMULATOR_DEFINITIONS.md

| Row | Line | The sentence, quoted | Mark | The rewrite or DELETE | Status |
| --- | --- | --- | --- | --- | --- |
| S1 | 5-7 | "a row with a record on the digital line of its momentum at one speed, the collision table a bijection inside its invariant classes, the detector's record the squared coherent sum of what it clicked" | (b) | "a record's rows at Nodes, each re-emitted to the six neighbours less its past (DESIGN.md section 2), the detector's record the sum of the offer it received; the digital line the engine as built" | LAW |
| S2 | 10-11 | "Coverage (a detector's Nodes), the threshold and the `reads` component are independent data." | (d) | "Coverage (a detector-emitter's Nodes) and its wheel are the declared data; there is no threshold (DESIGN.md 4.3)" | LAW |
| S3 | 93-95 | "Initialization accepts only `sampling_profile: "detector-only-v1"` under the Detector-owned sampling contract: an ordinary absorber never draws. The ray lottery, the bond registry ..." | (a) | stands as history (marked at lines 84-91) | HISTORY |
| S4 | 237-246 | "The optional initialization `conservation` member defines scalar energy and three-component momentum measurements for property-selected carrier records ... Read-only inventory snapshots bracket committed field phases" | (a) | add the history marker (the scalar candidate's audit, deleted 2026-09-17) or DELETE; the live books are ENGINE.md's | LAW (unmarked) |
| S5 | 301-303 | "The present implementation enforces the local information boundary and one-edge field propagation. It does not yet establish quantum consistency or entanglement." | (a) | "The engine enforces the local information boundary: a record's row reads its six neighbours and nothing else (LOCALITY-1); entanglement is the pair's record of tensor rank 2 read by one gather (ALGEBRA.md 3.6)" | LAW (unmarked) |
| S6 | 322-334 | "3. A node contains exactly five integer fields: `phi, px, py, pz, remainder`. ... 7. A source persists by occupancy." | (a) | stands as history (marked at lines 317-321) | HISTORY |
| S7 | 383-406 | "Defaults: dimensions `240 x 240 x 240`, `c_units=1000`, `source_strength=64`, `field_den=7` ... The scalar field is synchronous; particle movement is sequential." | (a) | DELETE or mark history (the scalar candidate deleted 2026-09-17; the world file's keys are ENGINE.md's) | LAW (unmarked) |
| S8 | 527-531 | "The optional local reception probe records completed inputs at one node with a completed-node-cycle counter. Six receiver ports identify the last hop, not distant source positions." | (a) | DELETE or mark history (a counter at a Node; nothing at a Node, Highlights item 2) | LAW (unmarked) |
| S9 | 541-543 | "A generic view must label configured fields rather than interpreting their names as scalar phi or particle momentum." | (a) | "A view labels what it draws by kind, DETECTOR or GAMEBOARD (ENGINE.md, the readings by type), and draws no field" | LAW (unmarked) |
| S10 | 551-560 | "Field proposals are validated before the field phase commits. Particle-field proposals are validated before that local exchange commits." | (a) | stands as history (marked at lines 548-550) | HISTORY |
| S11 | 832-841 | "exactly two outputs replace the same two local slots ... Representation probes do not certify physical field dynamics." | (a) | mark history (the entity profiles of the scalar candidate) or DELETE | LAW (unmarked) |

### 2.5 docs/ENGINE.md

| Row | Line | The sentence, quoted | Mark | The rewrite or DELETE | Status |
| --- | --- | --- | --- | --- | --- |
| E1 | 151-160 | "One thing. A row, with a place (a Node) and a record: a direction (an index into the world's direction table D), an age ..., a phase ..., a number ..., an amount (whole units) and a content per unit; its momentum is not stored, it is amount x content x u_d" | (b) | "One thing. A record's row at a Node: its amplitude now and one interval ago on the record's wheel and its remainder (DESIGN.md section 2); the momentum is a reading at a detector" | LAW |
| E2 | 166-172 | "the walk by the flight rule, the one reading, the collision by the table ..., the measured event's table (`read`, `measure`, `rerelease`, `pass` and, since 2026-09-20, `become`, the transformation, each gated by the detector's threshold and its window)" | (b) (d) | "the rule at every free Node (the six-neighbour sum less three times the row's past), the merge, and at a detector-emitter's Node the offer's sum and the one trigger (the counting form at the first rung); no threshold and no window gate" | LAW |
| E3 | 177-179 | "(the model owner, 2026-09-19: valid for a fan as for the six headings; a row that did not step has the direction (0, 0, 0) and enters the zeroth moment alone)" | (b) | drop the fan; the reading takes the six headings | LAW |
| E4 | 365-367 | "and it goes whole on every declared direction (n directions, n rows each of the count the family's release accumulator gained; a paid family's pending rows are apportioned whole over them)" | (b) | "a release is one record born at the emitter's own Node with amplitude A, driven by its clock for the train (DESIGN.md section 2); no directions" | LAW |
| E5 | 370-374 | "What comes home (the own number's arrivals) is taken whole and created again at the next self-creation on the declared directions with the arriving phase and content, apportioned whole ...; a `rerelease` entry does the same with another number's rows, stamped with the re-emitter's number." | (b) (d) | "what a detector-emitter receives (its click) it re-inserts as a new record at its own Node, driven by its clock at the arrival's phase (DESIGN.md 4.2); one act for the home and for the re-emitter" | LAW |
| E6 | 800-819 | "a_i^2, every weight 1 where none is declared (the equal split ...) ... a split is not a click: a `rerelease` entry takes every arriving row of its family on its own, with no pointer gate and no window, the amount gate alone" | (b) | DELETE the `rerelease`-with-`weights` split (the opening's Huygens; DESIGN.md 4.2: an opening is a hole, its Nodes free Nodes); `rotate` stays as a detector-emitter's rule | LAW |
| E7 | 820-836 | "`lamp` `{rate: [n, d], wheel: [r, W], directions, phase_window, phase_width}` ... also `turns`, a phase step per direction the born row carries beyond the clock's phase ... each one row of amount 1 per direction with the multiplicity the directions' count" | (b) | "`lamp` `{rate, wheel, train}` on a detector-emitter; no `directions` and no `turns` (DESIGN.md section 2: 'the lamp's turns per direction have no meaning here and go')" | LAW |
| E8 | 880-886 | "(an aperture two Nodes wide under a fan with the direction along it: the norm of the second opening between the siblings) are refused at load ...; the loader walks the record's paths through the openings per arm" | (b) | DELETE (no paths through openings to walk at load; the opening is free Nodes) | LAW |
| E9 | 891-893 | "`in_transit` (`position`, `family`, `number`, `direction` (a vector of D, or a rest index 0 or 1), `amount`, `phase`, optional `age`)" | (a) | a question (Q3): a declared row at a free Node is a thing inserted into the Inside by no detector; either refused in every world under the design ("nothing is inserted into the Inside") or kept as "the initial state" of Highlights 5.4 line 219; the rewrite after the owner's word | LAW |
| E10 | 893-895; 1041 | "`detectors` (`name`, `positions`, `threshold` 1 by default, `reading` `wave` by default (since 2026-09-20) or `beam`, or `sum`" and "the detectors (`detectors`: name, Nodes, threshold, `reading`, ...)" | (d) | "`detectors` (`name`, `positions`, the wheel W): one reading, the offer's sum per set (DESIGN.md section 5); no `threshold`, no `reading` key" | LAW |
| E11 | 1044-1046 | "then the face detectors, one per open face in Port order, with what clicked there in transit, the `measured_content` of the measured events that stepped off" | (c) | as P13 (Q1); the design's section 5 keeps "the faces absorb" | LAW |
| E12 | 1197 | "the clock stamp of a measured event (the world key `clock_stamp`, false by default; ...) ... a record field and no physics" | (d) | "the detector-emitter's own count, the click's time and the only time Outside (POSTULATES 26.2 and 26.5; DESIGN.md section 5), on every click line by default" | LAW |
| E13 | 1203 | "the label **p** of a row: `push` on a `click` or `read` line (the row group's label, what the reader took)" | (b) | "the momentum a click hands over: h times the wave number read from the arriving offer's phase gradient across the detector's Nodes (DESIGN.md 4.5 and 5)" | LAW |

### 2.6 docs/HIGHLIGHTS.md section 5.4 (the Boss's file: listed, never edited)

| Row | Line | The sentence, quoted | Mark | The rewrite or DELETE | Status |
| --- | --- | --- | --- | --- | --- |
| H1 | 215 | "every external entity is a detector or an emitter, an emitter also a detector at its own Node" | (d) | "every external entity is one generic detector-emitter (record 1327)" | LAW (the system table) |
| H2 | 271 | "An emitter is also a detector at its own Node, within its limits; a fixed body is both" | (d) | prune to the one generic thing, or keep as the line that led to record 1327 | LAW (a dated decision under the pruning rule, line 224) |
| H3 | 380 | "The paper says once that a thing propagates Inside as a beam, rows on digital lines at one Link per interval, and shows Outside as a wave" | (b) | DELETE under the pruning rule (contradicted by line 474; the record stays in the log) | LAW |
| H4 | 458 | "The comb: a fan bounded in Manhattan length is not a fan of every direction ...; otherwise the law's own number is the integral on the comb, computed before the run" | (b) | DELETE or mark as the engine as built's principle (the fan goes, DESIGN.md 4.2) | LAW |
| H5 | 482 | "A detector's sensitivity may be declared per (detector, family), a declared input of kind 2 (the cross-section), which row 8b's passage needs; with one sensitivity for every family the first detector takes the whole front" | (d) | "the sensitivity is not a key: a less sensitive detector is a larger body or a coarser wheel (DESIGN.md 4.3); the lamp's rate and the detector's sensitivity are the one thing's clock (record 1327)"; record 1327 says this line was rewritten to "an instrument above the board", which its head does not yet say | LAW |
| H6 | 504 | "every entity physics knows is one row of the law's keys, the external things placeable on the GameBoard" | (c) | "placeable as detector-emitters, the Outside" | LAW (a dated decision) |
| H7 | 509 | "Every external thing brought from the real world into the GameBoard carries its uncertainty like the detector; on the GameBoard it is certain" | (c) | "brought to the Outside as a detector-emitter; nothing is brought into the Inside" | LAW (a dated decision) |
| H8 | 529 | "A split is not a click ...: under the key a `rerelease` with `weights` is applied to every arriving row of its family with no pointer gate, an amount threshold only if declared" | (b) (d) | DELETE under the pruning rule (the apparatus split and the amount threshold both go, DESIGN.md 4.2 and 4.3) | LAW |
| H9 | 550 | "The fan as a width P of the law, Huygens on the GameBoard: every re-emitter (an opening, a mirror, a lamp) emits on all primitive directions within P, each direction weighted by the angle it covers ...; DECIDED (the owner, 23:55Z)" | (b) | DELETE under the pruning rule; the split line (474) already names it an instrument above the board; the record stays | LAW |
| H10 | 560 | "Detector as physical Nodes: 'The detector is itself Nodes'; 'The important thing is the detector sensitivity'" | (d) | prune the sensitivity clause, or leave the line under its heading "Decisions of 2026-09-19" as history | LAW (dated) |

### 2.7 The counts

| By mark | Rows |
| --- | --- |
| (a) | 18 (P1, P2, P3, P4, P5, P6, P9, P10, S3, S4, S5, S6, S7, S8, S9, S10, S11, E9) |
| (b) | 31 (A1, A3, A4, A5, A6, A8, P8, P11, P12, T1, T2, T3, T4, T5, T7, T8, T9, S1, E1, E2, E3, E4, E5, E6, E7, E8, E13, H3, H4, H8, H9) |
| (c) | 13 (A2, P5, P6, P7, P8, P9, P10, P13, T10, T17, E11, H6, H7) |
| (d) | 21 (A2, A7, P14, T6, T9, T11, T12, T13, T14, T15, T16, S2, E2, E5, E10, E12, H1, H2, H5, H8, H10) |

A row with two marks is counted under both. Rows in all: 73 (8 in
ALGEBRA.md, 14 in POSTULATES.md, 17 in TERMINOLOGY.md, 11 in
SIMULATOR_DEFINITIONS.md, 13 in ENGINE.md, 10 in Highlights 5.4).

| By status | Rows |
| --- | --- |
| HISTORY (stands) | 11 (A8, P3, P4, P6, P7, P8, P9, P10, S3, S6, S10), and the reading half of A5 |
| LAW (to change) | 62 (A5's clause among them), of which 8 are unmarked history in SIMULATOR_DEFINITIONS.md and POSTULATES.md sections 1 to 9 (P1, P2, S4, S5, S7, S8, S9, S11: the rewrite is the marker) and 41 are statements of the engine as built whose change lands with the design's build (the 29 (b) rows of the law and the 12 (d) rows on the threshold, the window, the lamp, the re-emitter, the contact and the step) |

**The three heaviest rows.** E9 (a declared row in transit is a thing
inserted into the Inside by no detector: the one place a world file
puts something on the board beside a detector-emitter's birth; Q3).
P5 with A2 (the postulates' live sentence still names two marks, the
Detector and the external body, and the algebra still calls the
apparatus-inside-the-law "a programme": both close to the one generic
detector-emitter declared Outside). T13 with H5, S2, A7, E10 (the
threshold, the sensitivity, in six places, a second trigger beside the
counting form).

**Places examined and standing** (no row): TERMINOLOGY.md 151-153, the
store, already "a report of the host, not a thing of the law";
TERMINOLOGY.md 176-178, the remainder on the record (the design's `r`
is the row's, not the Node's); TERMINOLOGY.md 424-430 and ALGEBRA.md
598-604, Inside and Outside as of record 768, not contradicted but to be
extended with the terms of 2026-09-23 (the Inside the board itself, the
split at every free Node, the Outside without a board, the passage only
through a detector, the instruments Outside); POSTULATES.md 26.3 and
26.4; Highlights 5.4 lines 467, 475, 476, 513, 518, 519 and 474 to 488,
consistent with the terms; ENGINE.md 163-164, "The Node holds nothing
between intervals but the rows present at it and the measured event
there", the sentence the design keeps.

**A clause to add, not a deletion** (Part 1.2): LOCALITY-1,
SIMULATOR_DEFINITIONS.md lines 410-416, needs the sentence "the
completion of a record (the exhaustion test over its detectors'
pointers, the choice of the cell and the deletion of its rows) is the
host's one non-local step, counted as host work and never as a Node's
(Highlights 5.4 line 518; DESIGN.md section 5)"; today the contract
admits no state change outside the six neighbours and the completion is
one.

## The questions the audit could not settle

- Q1 (P13, T17, E11): an open face, a detector without mass and without
  a clock: a detector-emitter (then it must have mass, POSTULATES 26.1)
  or the board's edge and no thing (then its "click" is not a click and
  its line is GAMEBOARD)? The design keeps "the faces absorb" (section
  5) without naming which.
- Q2 (T10): the `become` clock trigger (`at`, gated by `crowd`): the
  detector-emitter's own cycle, and so the one trigger read at a body's
  period (DESIGN.md section 8), or a second trigger to delete?
- Q3 (E9): a declared row in transit (`in_transit`) at a free Node:
  refused under "nothing is inserted into the Inside", or kept as "the
  initial state" that Highlights 5.4 line 219 counts among the four
  inputs?
- Q4 (T11, T16): the body's drive and the contact under the moving
  detector: the design's section 8 folds the massive form into the rule
  by construction; is the drive's step then a reading of the record's
  first rung at the next Node (no step verb), and is a contact a click at
  an occupied Node?
- Q5 (Part 1): whether the algebra's one non-local step is to be
  restated as every record's completion over all its detectors, the
  pair's gather its two-arm case, and whether LOCALITY-1 takes the
  clause above; the theorem's writer's and the definitions' owner's.
- Q6 (Part 1): the conversion's amplitude map under the design (a signed
  integer amplitude summed at the Node, its square summed at the
  detector) against the click frame's `ev` on `Z[Z_N]`: the nine rows of
  the conversion table must be written again by the algebra after the
  design's pins; not decidable here and not a run's.
