# Tensor24: the Node-clock as one act

The owner's words of 2026-10-28, 06:0x to 06:4x UTC (Hebrew, translated):
- "You be the owner of the plan, the node as one act."
- "Call the plan Tensor24. Write it for me here and for everyone in such a file, make sure it stands, divide the work. At its end the whole engine is tensor arithmetic only: say of which order. Explain how the clock enters here, what the node takes and what it gives, and what all the families are. For now only close the plans with everyone, implementing nothing. Make sure that at its end there are no numbers in the code and no circular proofs."
- "Understand how the click enters the plan, its kinds, all the families and what they are, the family you wanted to add included. Reach the main formula of the Node-clock, just as general relativity has a tensor equation, but that one is not for the node."
- "Only when everyone agrees on the plan, present it to me. It must bring the whole engine to work as an integer tensor machine that represents the clocks and everything the system has now: clicks, time reversal, everything. There is no problem that the tensor has complex numbers, is there? Maybe it simplifies, but the acts are on the complex numbers' coefficients, so they are integers. Call them by the names they have now."

The plan's owner: the Boss. Its base: engine-5.0-test at 526a5666d. Its status: a plan, with nothing built under it.

- **This file is the one plan.** The Scribe's record of the program (the state of the cuts, the owner's list with his recommendations, the ledger) stands on scribe-5 and points here.
- **Its words** are the clock words of docs/CLOCK_WORDS.md (scribe-5): the great clock, the Node-clock, the Mesh, the Spoke, the tick, the train, the hand, the gear, the notch, the teeth count, the carry, the drive, the wind, the load, the bob, the fitting, the fitted hand, the unspringing, the regulator, the swing, the turnover, the rewind, the calibre, the piece, the setting, the chart, and the code names chime, vernier, unwind, stopped and lead.
- **The law's sentence is entered** as decided and not built: "The Node-clock is one act" (docs/ALGEBRA.md, scribe-5 8c0a0cd01), on the owner's "Yes and yes" to the Scribe at 06:0x UTC.
- **What it takes in whole:** the Reader's proposal of 05:49 UTC (#2187, 6461767760) and the Scribe's SCRIBE-THE-NODE-AS-ONE-ACT-1.md (scribe-5 d2d78b945, #2187, 6461843937).
- **What it adds:**
  - the main formula, read from the head's code;
  - the click's two kinds;
  - the trains by their names;
  - the hand as a Gaussian integer;
  - everything the engine does on the head, with its form here (section 8);
  - the Boss's check;
  - David's derivations of 06:0x UTC (6462024199) and the Reader's reading of the mirror of 06:2x UTC (6462233147);
  - who does what.

## 1. The end state

- **One integer tensor machine.** The whole engine is one integer tensor machine of the clocks. Every Node-clock steps every gear of every train by one formula (section 2), then one carry. The quotient leaves; the remainder stays.
- **Nothing the engine does on the head is lost** (section 8): every click, the rewind bit for bit, the books, the order-free phase, the swing, the stopped Node-clock, the bottom, the held field, the twin hands, the standard.
- **The order.** The engine is integer tensor arithmetic of the second order:
  - its highest tensors, the metric and the stress, are of rank 2;
  - each equation is linear in the gear it moves, with the metric's components as its coefficients;
  - each source is a product of at most two other trains' gears, weighed by the clock (degree 3 with the clock counted, as David writes);
  - the only steps that are not tensor arithmetic are the carry and the gate's comparisons (a whole winding, the top of a dial, the draw).
- **The 24.** The cube's 24 turns hold by construction. The kinds come from the six Spokes alone, so no act knows an axis.
- **No numbers, no circularity.** There is no number beyond 0 and 1 in src, no circular function, no root search, no angle and no closed form of a phenomenon. Every integer of a train stands in the calibre, the piece and its setting.

## 2. The main formula of the Node-clock

General relativity has one tensor equation, G = kappa T: the metric's curvature equals the matter's stress. It is an equation of a continuum, not of a node. The Node-clock's formula is the same kind of statement, written as the Node-clock's own step: in integers, on the Node-clock and its six neighbours, closed by the carry.

**The form, read from the head's code** (clock.turn, tick.impulse, tick.carry). For every gear a of every train at a Node-clock x:

    W+ (a+ - a) - W (a - a-) = s [ sum over the six Spokes j of g_j (a_j - a) - D a + J ]

then the carry: the quotient goes to the notch and the remainder stays in the fine tooth. The terms:

- a-, a and a+ are the gear's notch before, now and next. a_j is the same gear at the neighbour across Spoke j.
- W and W+ are the clock: the mean teeth count of the regulator's time gear at the step's start and end (the lapse).
- s is the stretch, the time gear's notch.
- g_j are the Mesh's grips: twice the mesh rate squared, times the Mesh's factor Q_j (from the tensions), times the train's pinion. They carry the metric's spatial part.
- D is the spring, the train's mass term, from its pair and the clock's rate.
- J is the source: one contraction of the other trains' gears, its kind's part of the product table, weighed by the calibre's couplings.

**Its two halves, as in general relativity:**
- **The metric's half** (the Einstein part): the regulator's gears are driven by the matter's stress. J is kappa times the stress's part of each kind: the trace and the forms on the time gear, the traceless part on the tensions, the flows on the flow gears.
- **The matter's half** (the motion part): every hand moves by the same form, with the metric's W, s and Q_j as its coefficients.

**On the head the form is written twice.** The regulator steps by clock.turn plus a separate drive carry; the driven trains step by the impulse and tick.carry. These are two paths of one form, and Tensor24 makes them one (cut 6).

**Its degrees (David, 6462024199):**
- The stress, the masses, the forms and Pauli's numerator are of degree 2 in the gears. The release is of degree 3 with the clock's s counted: the stretch times the cross of a hand and its pull.
- The grips and springs are maps of the load.
- So the one act is one division over one multilinear contraction, and a cut keeps its bits within what clock.max_transient reads on the head.

**The work:**
- David derives the formula exactly: each term's integers, where each carry's remainder goes, and the drive's teeth count.
- The Boss checks it bit for bit against the head's step on the committed charts, with a probe and no engine change.
- The Scribe proposes it as the law's formula for the owner.

## 3. The hand as a Gaussian integer

- **A hand is one complex number with integer coefficients.** Its three-o'clock and twelve-o'clock gears are z = three + i twelve, so every act is on the coefficients and stays in integers (the owner's word: "the acts are on the complex numbers' coefficients, so they are integers").
- **The products are the complex product's two coefficients.** The hand's own two products are the real and imaginary coefficients of conj(z) w: hands.dot and meshes.cross (David, 6462024199). A product of two hands is one complex product.
- **A quarter turn of a hand's plane is the multiplication by i:** (three, twelve) to (-twelve, three), an exchange and a sign, the one mirror's own act. The 24 act on a hand's plane by i alone.
- **A train's kind is its cube kind times its own.** Its own part is one gear, one Gaussian integer (a hand), or two Gaussian integers (the twin hands).
- **The twin hands.** A spinor's quarter turn is the multiplication by the eighth root of unity, (1 + i) over the root of 2.
  - Over the eighth roots, the integer ring Z[zeta8] with four integer coefficients a + b zeta + c zeta^2 + d zeta^3, that multiplication is an exchange of the coefficients with one sign. So it is exact in integers.
  - The cube's three-fold turns of a spinor still ask a half.
  - David derives the way (open item 11 a).

## 4. The click in the plan

**The click is the same carry, one level up.** The clocks' hierarchy is a ladder of carries:
1. the gear's notch is the carry of its dial;
2. the hand's click is the carry of its wind at the winding;
3. the Node-clock's turnover is the carry of its time gear at the top or bottom;
4. the great clock's swing is every Node-clock's top at once.

**The law's two kinds of click** (docs/ALGEBRA.md, The two kinds of click; docs/CLOCK_WORDS.md):
1. **The click of a whole.** One hand holds the whole winding. There is nothing to choose, and the wind decides where the click happens. These are the chime (the unwind), the setting of a fitted hand, and the unspringing's two ends.
2. **The click of a split.** The winding is divided between two twin hands, upper and lower. Neither holds a whole winding, but together they do, so the great clock draws who receives it, by the parts' sizes (Born). This is the detector's click, and the one place a choice enters.

Beside the two kinds stands **the clock's own click, the turnover:** the time gear at its top or bottom mirrors every fine tooth of its Node-clock (the one mirror).

**Four points:**
- **The fitting's train.** On the head it is drawn evenly among the trains it may set (click.list_of, the vernier), not by the parts' sizes. Tensor24 makes every draw the one draw by sizes (cut 5, by David's derivation).
- **The detector** is no typed object. It is a bob, a sprung hand standing at a Node-clock that counts its swings, and its reading is its click. Where its winding is shared, that click is the click of a split (the Scribe, 6461915413).
- **The click shows the hand; it does not decide it** (the Reader, 6462233147). The draw stays fair, by the parts' sizes alone, under the 24. A one-hand coupling (one row of the calibre's couplings, open item 11 b) sets the sizes, and the fair click then comes out on one side.
- **The one big bang has no twin hands.** Its calibre (universe_bang.json) holds no twin train, so no click of a split happens there, and neither Born nor Bell can be seen in the one big bang until the calibre holds one (open item 11 e).

## 5. What the Node-clock takes and what it gives

- **It takes** the great clock as the tick starts, at itself and at its six neighbours one Mesh away. From each it reads every train's gears: each gear's notch now and before, its fine tooth and teeth count, and its drive fine tooth. It reads nothing else: no index of the great clock, no read of the log, nothing beyond one Mesh.
- **It does** the main formula for every gear, then the gate.
- **It gives** three things:
  1. its own gears, written only after every read of the tick (the order-free phase, phase.py);
  2. its clicks: the turnover, the click of a whole and the click of a split, each a few integers (the hand, the Node-clock, the windings);
  3. its books: every winding unwound is booked, and the remainder is signed.

## 6. The trains, by their names now

A train (the engine's word for a family) is a kind and its integers in the calibre (its pair, its spring, its couplings, its weight), nothing more. The engine knows kinds and integers, never a train's name in nature.

The five kinds are the five irreducible representations of the cube's rotation group, each derived from the vector kind (the six Spokes) by its products, so no table is typed. The Boss checked this on the 24 signed permutation matrices of determinant 1, by characters:
- the vector V is T1;
- its symmetric square is A1 + E + T2;
- its antisymmetric square is T1;
- the product xyz is A2;
- 1 + 1 + 4 + 9 + 9 = 24.

| kind | dimension | what it is on the great clock |
| --- | --- | --- |
| A1 | 1 | the clock: the time gear, the rate, the load, the trace; also each hand's own Gaussian integer |
| A2 | 1 | the sign of xyz, which a quarter turn reverses (none on the head) |
| E | 2 | the tensions less their trace |
| T1 | 3 | a gradient, a flow, the offset's odd gears, a curl |
| T2 | 3 | the off-diagonal products (struck from the regulator at d09f1a8a5) |

The twist the engagement reads is kept by every turn and reversed by every mirror. So it is an A1 of the 24, and the pseudoscalar of the 48 (David).

| the train (its name now) | nature | its kind | its integers in the calibre |
| --- | --- | --- | --- |
| the unsprung hand | the light | one Gaussian integer, A1 | the pair (rim, rim), the spring 0, so the coupling 0: the null element, known by its spring and never by identity |
| the sprung hands (a bob where one stands) | matter | one Gaussian integer, A1 | its pair, so a spring above 0, so a mass; the one big bang's calibre holds three |
| the twin hands | spin one half | two Gaussian integers as one spinor, upper and lower | its pair (open item 11 a) |
| the regulator | the metric | 2 A1 + E + T1, seven gears: the time gear, three tensions, three flows | its pair, the trace weight |
| the offset | the potential | A1 + T1, four gears: a time gear and three odd gears | its pair (rim, rim) |
| the held field | the mediator | one gear, A1, with a weight | its gapped pair, its weight |
| the ratchet | the parity of the turnovers | one gear of its own two teeth | none: it counts the turnovers (the pawls) |
| the standard | the reference clock | one hand turning 1 / full rate per act | the full rate |
| the composite (proposed) | a bound pair: fusion | the product of its two parts' kinds, by the product table | derived from its parts', with no new number: a bound pair become one larger clock, the clock of clocks (open item 11 c) |

## 7. How the clock enters

- **The clock is the A1 kind,** the kind the 24 leave in place. At a Node-clock that a turn of the cube fixes, only A1 can be read. So the clock is what every image reads alike.
- **In the main formula it is W, W+ and s:** the step's teeth count (the lapse) and the weight of every force. The rate it sets enters D and the grips.
- **It is the dial:** every gear's carry is a tick of a clock, and its quotient a turn.
- **Its own click is the turnover** (section 4).
- **The hierarchy:**
  - the great clock;
  - the Node-clock with its time gear;
  - the hand, a small clock;
  - the composite, a clock of clocks.

## 8. Everything the engine does on the head, in Tensor24

| what the engine does on the head | where it stands now | its form in Tensor24 |
| --- | --- | --- |
| the tick's five acts: the readings, the impulse, the carry, the turnover, the click | tick.py | the main formula for every gear, then the gate |
| the rewind, every act backward bit for bit (time reversal) | the going -1: the carry's inverse, Tick at -1, the rewind note | the same formula with a+ and a- exchanged and the carry run backward; the turnover's mirror an involution; the click undone from its note; 20 of 20 on every chart after every cut |
| the books, taken + remainder before - remainder after = booked (EX-S1) | phase.books, the remainder | every carry's remainder kept and signed; the books closing at every click |
| the order-free phase | phase.py | every gear read, then every gear written |
| the vernier's draw | draw.py | the one draw by the parts' sizes, the click of a split |
| the turnover and the pawls | clock.turnover, the ratchet | the clock's own click and its count |
| the swing, the great clock's exact returns | the regulator's time gear | every Node-clock's time gear at its top at once, read by the reckoner |
| the stopped Node-clock and the horizon | readings.stopped_of | a comparison of the gate |
| the bottom (the stretch through 0) | Tick.end_teeth | a comparison of the gate, the start's teeth count read |
| the held field, the offset's kick by the lead, Pauli's twin hands, the release's advance of the unsprung hand, the recoil on the Mesh | tick.py, clock.drive | terms of J, each a product from the table |
| the fitting, the fitted hands' setting, the chime (the unwind), the unspringing | click.py, bobs.py, unspring.py, unwind.py | the gate: the click of a whole and the click of a split |
| the standard, the reference clock | features/standard | a train of the calibre |
| the setting, the piece, the calibre | assembly/, the loader | data alone: every integer of a train |
| the readers (the rows, the gates, the charts) | the reckoner, gates.py, run.py | outside the engine, reading the chart alone |

## 9. The head as it is (526a5666d)

- **The step.** The Scribe's table of 26 acts (SCRIBE-THE-NODE-AS-ONE-ACT-1.md, read on 97e5b3fd6) stands on 526a5666d by kind: 9 contractions, 8 pointwise maps of one gear, 5 acts of bookkeeping, 2 gates and 2 global reductions. Since 97e5b3fd6:
  - the stress's shear products are struck (d09f1a8a5);
  - the click's phase is order-free (phase.py, 42d5448b7);
  - the turnover mirrors (42d5448b7).
- **The Scribe's scan** (scribe_scan.py, scribe-5 abfbd6ee9) on 526a5666d, counting its blocking rules only:
  - the engine's modules: 95 hits (circular words in names 62, root searches 14, state beyond the Node-clock 14, log reads 3, a typed table 1, a number 1);
  - the readers' modules: 57 hits (numbers 23, circular words 13, root searches 11, state 7, typed tables 2, a float 1).
- **The unsprung hand** is read by identity at 18 places in 7 files (the Boss's count).

## 10. The cuts, and who does what

Every cut goes the same way:
1. David derives it and confirms it on toys-5 before it is built; he writes no engine code.
2. The Boss builds it in his toy and measures it.
3. The Reader benches it.
4. The Scribe's scan passes, with every count falling or equal.
5. The full check exits 0, and the Boss pushes on the owner's go.

The cuts, in order:

0. **The main formula.** David derives it (section 2); the Boss checks it bit for bit against the head; the Scribe proposes it as the law's formula. Every later cut builds toward it.
1. **The fair draw.** Built in the Boss's toy and measured: the 24 on nature and the hole, the rewind 20 of 20, the suite 118. The owner's go came through the Scribe at 06:0x UTC; it is held by his later word to the Boss at 06:1x UTC ("for now only close the plans, implementing nothing") until he confirms. Before the push: the Scribe's scan against 526a5666d, and the Reader's bench within the hour.
2. **The gate.** The Scribe's scan goes into tools/check.py's ratchets and the push hook, so it holds every later cut.
3. **The pure contractions, bit for bit:** regulation.stress_of; the hands' products (dot, lead, sweep, products) as complex products; the Meshes' cross and gradient; the offset's curl; Pauli's numerator. They become J, one contraction over the Node-clock and its neighbours, its weights from the kinds' product table.
4. **The pointwise maps:** the rate table and its inverse by search (stretch.load_of, readings.rates_of), the mesh factor, rest_rate_of, the clamps, rounded(p + p + 1, d) and the end teeth count's selection. Each becomes a chain of carries or integers in the calibre.
   - David has derived three already (6462024199):
     - the rate table is a chain of carries on the head, one carry per unit of load at the teeth count Gamma, kept, then one rounding (core/rates.py);
     - its inverse by search is that chain read backward;
     - rest_rate_of is a constant of the setting, kept on the clock rather than an act of the step.
   - He derives the others (the mesh factor, the clamps, the selections) before the cut.
   - With them, every sine, cosine and root search of src leaves for integer data: core/rates.sine_rim; assembly/setting.py's raised_cosine, rim_point, angle_of, angles_of and running_rotation; assembly/cycle.cycle_angles; readings.standard_angle; hands.cosine_count. The three integers of each pair go into the calibre, and the setting's weights into the setting.
5. **The gate as one act for every train:** the turnover, the click of a whole and the click of a split with the one draw by the parts' sizes (engage, jam, unwinds, winds, the bobs, the unspringing's ends), read whole and then written whole. The unsprung hand is known by its spring 0, never by identity.
6. **One path:** the regulator's turn and drive, and the driven trains' impulse and carry, become the one formula.
7. **The state beyond the Node-clock goes out:** the id() keys, the module-level containers and caches, and the log reads (tick.py, click.py, draw.py, features/).
8. **The two global reductions** (count_max, max_transient) leave the step for the readers.
9. **The end check** (section 12).

| who | the part |
| --- | --- |
| the Boss | owns the plan and this file; writes every line of code; checks the formula against the head; builds each cut in his toy, measures it and pushes it on the owner's go |
| David | derives the main formula and every cut before it is built (the contraction table from the Spokes, the pointwise maps, the twin hands, the gate and its one draw, the composite, the detector's reading) and confirms or refutes each build; writes no engine code |
| the Reader | benches each cut: the 77 rows on the 16 charts and the 3 committed charts, the head against the cut, within the hour of each push; clears the readers' own modules under the scan; takes the reductions into the readers |
| the Scribe | the gate on every push; the law's sentence (entered, scribe-5 8c0a0cd01) and the formula (proposed, entered on the owner's word); the program's record on scribe-5, pointing here; the documents after each cut; the ledger |
| the owner | the formula as law; the 24 with one coupling, or the 48; the Bell click's form; the one big bang's setting; a twin train in its calibre; the fair draw's push |

## 11. Open, by name

- **(a) The twin hands.** A spinor's quarter turn needs the root of 2 over the Gaussian integers: on the z axis it is the diagonal (1 - i, 1 + i) over the root of 2. Its half turn is a Gaussian integer. Over the eighth roots of unity (section 3) the quarter turn is exact, but the three-fold turns ask a half. David derives which way stands:
  - the twin hands' gears over the eighth roots, with the half carried as an integer scale exponent; or
  - the twin hands read only through their bilinears (the density, A1, and the spin, T1), with the 24 asked of those.

  Until then the 24 is asked of the five kinds and of the twin hands' bilinears.
- **(b) The 24 with one coupling, or the 48.** With the reflections, every kind splits in two, giving ten kinds. The Reader's reading (6462233147), which the Boss recommends:
  - the law is the 24 exactly; under the 24 alone a vector and a mirror vector are one kind;
  - the mirror's break, nature's one hand (row 69), enters at one place only: a one-hand coupling, one row of the calibre's couplings, with no act of its own;
  - the test: the 24 rotations alike bit for bit always; the reflections part only through that coupling, where it acts; a parting anywhere else is a bug;
  - the fixed-point test names its group (David): at a point the 48 fix, the twist reads 0; at a point only the 24 fix, it may stand.

  This is the owner's word at 08:30 UTC.
- **(c) The composite train.** Fusion: a bound pair as one larger clock, its kind the product of its parts' kinds and its integers derived from theirs, with no new number. It waits on David's derivation. It is not seen on the head: row 76 reads NOT SHOWN on the one big bang.
- **(d) The Bell click.** Its form is the owner's word: a detector hand's gear by the carry (the Scribe's recommendation), or another. The twin hands' state holds the correlation; the detector's reading is David's, after the owner's word.
- **(e) Detectors in the one big bang.** Its calibre has no twin train, so it has no click of a split, and neither Born nor Bell is seen there. Adding one is the owner's word on that calibre.

## 12. The end check

- **No numbers:** no number beyond 0 and 1 in src; every integer in the calibre, the piece and its setting. The scan's number and table rules stand at 0.
- **No circularity:** no sine, cosine, root search, angle or closed form of a phenomenon in src, so the scan's circle, root, word and mix rules stand at 0. The Scribe's audit items E1 to E19 are cleared one by one. The click's draw by the parts' sizes is the one chance.
- **Locality:** no state beyond the Node-clock, and no act reads the log. The state and log rules stand at 0.
- **No circular test:**
  - every test compares two runs or reads what the engine wrote;
  - no test asserts a number the code typed in;
  - the 24 is read by the images' test on every chart.
- **The step:** the one formula for every gear, and the gate as one act for every train.
- **Everything of section 8 stands,** the rewind 20 of 20 on every chart among it.
- **The counts to bring to 0,** from 526a5666d: the engine's 95 hits (the Boss) and the readers' 57 (the Reader).

## 13. After every cut

- the Reader's per-row diff (77 rows, 16 charts, 3 committed charts);
- the rewind 20 of 20;
- the books closed at every click;
- the 24 on nature and the hole, and the 48 on nature while the reflections hold;
- the suite under the 30 s bound;
- the scan with no count risen;
- the full check exiting 0 before any push.
