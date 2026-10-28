# Tensor24: the Node-clock as one act

The owner's words of 2026-10-28, 06:0x to 06:4x UTC (Hebrew, translated):
- "You be the owner of the plan, the node as one act."
- "Call the plan Tensor24. Write it for me here and for everyone in such a file, make sure it stands, divide the work. At its end the whole engine is tensor arithmetic only: say of which order. Explain how the clock enters here, what the node takes and what it gives, and what all the families are. For now only close the plans with everyone, implementing nothing. Make sure that at its end there are no numbers in the code and no circular proofs."
- "Understand how the click enters the plan, its kinds, all the families and what they are, the family you wanted to add included. Reach the main formula of the Node-clock, just as general relativity has a tensor equation, but that one is not for the node."
- "Only when everyone agrees on the plan, present it to me. It must bring the whole engine to work as an integer tensor machine that represents the clocks and everything the system has now: clicks, time reversal, everything. There is no problem that the tensor has complex numbers, is there? Maybe it simplifies, but the acts are on the complex numbers' coefficients, so they are integers. Call them by the names they have now."
- "First reach a plan that closes everything, everything, everything, and that everyone approves. If the push helps the plan, push. You manage the plan Tensor24 and present it to me, right? Remember: all of you must approve it after you have checked it, locally, in the code. Every part of this plan you must check that it works and reflects nature in the end one to one, and that it has all the clocks needed, all the gears, all the hands, everything that is needed there."

- Through David, 06:3x UTC (#2187 6462481390): "If it is needed to see natural phenomena, and another family is needed, no problem. Everything should be in the plan Tensor24." And: "In my opinion go with the 24 without the 48, no?" To David, 06:1x UTC (6462435432): "Work only on the Tensor24 program. Only once it is whole, implement by the Boss."

The plan's owner: the Boss. The names are the ones the owner sees in his app: Boss, Sofer, David and Animate (the owner's word through Animate, 06:3x UTC, #2187 6462416209). Its base: engine-5.0-test at 526a5666d. Its status: a plan, with nothing built under it.

- **This file is the one plan.** Sofer's record of the program (the state of the cuts, the owner's list with his recommendations, the ledger) stands on scribe-5 and points here.
- **Its words** are the clock words of docs/CLOCK_WORDS.md (scribe-5): the great clock, the Node-clock, the Mesh, the Spoke, the tick, the train, the hand, the gear, the notch, the teeth count, the carry, the drive, the wind, the load, the bob, the fitting, the fitted hand, the unspringing, the regulator, the swing, the turnover, the rewind, the calibre, the piece, the setting, the chart, and the code names chime, vernier, unwind, stopped and lead.
- **The law's sentence is entered** as decided and not built: "The Node-clock is one act" (docs/ALGEBRA.md, scribe-5 8c0a0cd01), on the owner's "Yes and yes" to Sofer at 06:0x UTC.
- **What it takes in whole:** Animate's proposal of 05:49 UTC (#2187, 6461767760) and Sofer's SCRIBE-THE-NODE-AS-ONE-ACT-1.md (scribe-5 d2d78b945, #2187, 6461843937).
- **What it adds:**
  - the main formula, read from the head's code;
  - the click's two kinds;
  - the trains by their names;
  - the hand as a Gaussian integer;
  - everything the engine does on the head, with its form here (section 8);
  - the Boss's check;
  - David's derivations of 06:0x UTC (6462024199) and Animate's reading of the mirror of 06:2x UTC (6462233147);
  - who does what.

## 1. The end state

- **One integer tensor machine.** The whole engine is one integer tensor machine of the clocks. Every Node-clock steps every gear of every train by one formula (section 2), then one carry. The quotient leaves; the remainder stays.
- **Nature one to one.** Every one of the 77 rows of the gates is shown on the one big bang's chart, its calibre holding every train the rows need (section 14 names the trains, acts and settings still missing).
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

**The exact integer form, checked bit for bit on the head.** The gear's momentum is p = W (a - a-) + (r - mid W), the notch's step in the clock's teeth count with the fine tooth's offset. The step is

    p+ = p + s F + K,    a+ = a + (p+ + mid W+) div W+,    r+ = (p+ + mid W+) mod W+

- F is the pull: the sum over the six Spokes of g_j (U_j a_j - a), less D a, with Pauli's term for the twin hands.
- U_j a_j is the neighbour's hand carried across the Mesh: turned by the Mesh's turn (the offset's pair of each Spoke) and by the pawl's reflection. So the Laplacian is the covariant one, and the Mesh carries the potential's connection.
- K is the kick, T s q, with q a whole carry of the source: the lead's on the offset, the masses' on the held field.
- The regulator steps by Rule3's turn, T (a+ - 2 a + a-) = the grips times (a_j - a) less D a, then by the drive of its numerators, q = carry(N, its drive teeth count, its drive fine tooth).
- The unsprung hand's first gear takes the release's advance, and its recoil drives the regulator's flow gear on the Mesh.

**The Boss's probe** (formula0.py, a harness on the head's own acts, no engine change) read every gear at every Node-clock:

| world, ticks | sprung and unsprung hands, sites with K != 0 | offset and held field kicks equal to T s q | driven gears where p+ = p + s F + K | regulator gears where turn + drive |
| --- | --- | --- | --- | --- |
| the hole, 30 | 0 of 30,000 | 276 of 276 | 41,250 of 41,250 | 26,249 of 26,250 |
| nature, 20 | 0 of 20,000 | 29 of 29 | 27,500 of 27,500 | 17,500 of 17,500 |
| the one big bang, 12 | 0 of 6,144 | 768 of 768 | 9,216 of 9,216 | 5,376 of 5,376 |

The one regulator site and the one unsprung site on the hole not read by the form are the release's advance of the unsprung hand and its recoil, the two terms of J the formula names for them.

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
- Sofer proposes it as the law's formula for the owner.

## 3. The hand as a Gaussian integer

- **A hand is one complex number with integer coefficients.** Its three-o'clock and twelve-o'clock gears are z = three + i twelve, so every act is on the coefficients and stays in integers (the owner's word: "the acts are on the complex numbers' coefficients, so they are integers").
- **The products are the complex product's two coefficients.** The hand's own two products are the real and imaginary coefficients of conj(z) w: hands.dot and meshes.cross (David, 6462024199). A product of two hands is one complex product.
- **A quarter turn of a hand's plane is the multiplication by i:** (three, twelve) to (-twelve, three), an exchange and a sign, the one mirror's own act. The 24 act on a hand's plane by i alone.
- **A train's kind is its cube kind times its own.** Its own part is one gear, one Gaussian integer (a hand), or two Gaussian integers (the twin hands).
- **The twin hands, checked by the Boss's probe spinor24.py:**
  - **One axis.** Over the eighth roots of unity, the ring Z[zeta8] with four integer coefficients a + b zeta + c zeta^2 + d zeta^3, a spinor's quarter turn about its own axis is the multiplication by zeta: an exchange of the coefficients with one sign, exact. Four quarter turns give -1 and eight give +1, spin one half's sign.
  - **The other turns.** The quarter turns about the other two axes and the three-fold turns ask 1 over the root of 2. That is no integer of Z[zeta8], since the norm of the root of 2 there is 4.
  - **The scale exponent holds for the turns alone.** With an integer scale exponent e carried with the twin hands (the state psi over the root of 2 to the e), every turn of the double cover is an integer matrix over the Gaussian integers: a quarter turn with e + 1, a three-fold turn with e + 2, a half turn with e unchanged.
  - **It does not survive the carries** (David, 6462435432): a carry of a sum is not the sum of the carries, and they differ in 956 of 2,000 random draws.
  - **So the twin hands are read only through (W, S),** their density (A1) and their spin (T1), which move by an exchange and a sign under all 24.
  - **Their motion** keeps the 24 only if it too is written on (W, S): the axis turned about the offset's curl. Written on the gears, as tick.twin_pulls is, it keeps the half turns alone. The twin hands' interference lives on their gears, so the motion's way is the owner's word (open item 11 a).

## 4. The click in the plan

**The click is the same carry, one level up.** The clocks' hierarchy is a ladder of carries:
1. the gear's notch is the carry of its dial;
2. the hand's click is the carry of its wind at the winding;
3. the Node-clock's turnover is the carry of its time gear at the top or bottom;
4. the great clock's swing is every Node-clock's top at once.

**The law's two kinds of click** (docs/ALGEBRA.md, The two kinds of click; docs/CLOCK_WORDS.md):
1. **The click of a whole.** One hand holds the whole winding. There is nothing to choose, and the wind decides where the click happens. These are the chime (the unwind), the setting of a fitted hand, and the unspringing's two ends.
2. **The click of a split.** The winding is divided between two twin hands, upper and lower. Neither holds a whole winding, but together they do, so the great clock draws who receives it, by the parts' sizes (Born). This is the detector's click, and the one place a choice enters.

The kinds are the ways the whole is held (David, 6462435432):
- by one hand: the chime;
- at both ends of a Mesh: the setting of the fitted hands and the unspringing's ends, where the Mesh's lead and twist place the children;
- split among parts: the twin hands, or the trains a fitting may set.

Beside them stands **the clock's own click, the turnover:** the time gear at its top or bottom mirrors every fine tooth of its Node-clock (the one mirror).

**Four points:**
- **The fitting's train.** On the head it is drawn evenly among the trains it may set (click.list_of, the vernier), not by the parts' sizes. Tensor24 makes every draw the one draw by sizes (cut 5, by David's derivation).
- **The detector** is no typed object. It is a bob, a sprung hand standing at a Node-clock that counts its swings, and its reading is its click. Where its winding is shared, that click is the click of a split (Sofer, 6461915413).
- **The click shows the hand; it does not decide it** (Animate, 6462233147). The draw stays fair, by the parts' sizes alone, under the 24. A one-hand coupling (one row of the calibre's couplings, open item 11 b) sets the sizes, and the fair click then comes out on one side.
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

- **The step.** Sofer's table of 26 acts (SCRIBE-THE-NODE-AS-ONE-ACT-1.md, read on 97e5b3fd6) stands on 526a5666d by kind: 9 contractions, 8 pointwise maps of one gear, 5 acts of bookkeeping, 2 gates and 2 global reductions. Since 97e5b3fd6:
  - the stress's shear products are struck (d09f1a8a5);
  - the click's phase is order-free (phase.py, 42d5448b7);
  - the turnover mirrors (42d5448b7).
- **Sofer's scan** (scribe_scan.py, scribe-5 abfbd6ee9) on 526a5666d, counting its blocking rules only:
  - the engine's modules: 95 hits (circular words in names 62, root searches 14, state beyond the Node-clock 14, log reads 3, a typed table 1, a number 1);
  - the readers' modules: 57 hits (numbers 23, circular words 13, root searches 11, state 7, typed tables 2, a float 1).
- **The unsprung hand** is read by identity at 18 places in 7 files (the Boss's count).

## 10. The cuts, and who does what

Every cut goes the same way:
1. David derives it and confirms it on toys-5 before it is built; he writes no engine code.
2. The Boss builds it in his toy and measures it.
3. Animate benches it.
4. Sofer's scan passes, with every count falling or equal.
5. The full check exits 0, and the Boss pushes on the owner's go.

The cuts, in order:

0. **The main formula.** David derives it (section 2); the Boss checks it bit for bit against the head; Sofer proposes it as the law's formula. Every later cut builds toward it.
1. **The fair draw. Pushed** as 834cfd72e on the owner's word of 06:5x UTC ("if the push helps the plan, push"): the 24 on nature and the hole, the rewind 20 of 20, the full check 118 passed, Sofer's scan clean against 526a5666d; Animate's bench within the hour.
2. **The gate.** Sofer's scan goes into tools/check.py's ratchets and the push hook, so it holds every later cut.
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
| Animate | benches each cut: the 77 rows on the 16 charts and the 3 committed charts, the head against the cut, within the hour of each push; clears the readers' own modules under the scan; takes the reductions into the readers |
| Sofer | the gate on every push; the law's sentence (entered, scribe-5 8c0a0cd01) and the formula (proposed, entered on the owner's word); the program's record on scribe-5, pointing here; the documents after each cut; the ledger |
| the owner | the formula as law; the Bell click's form; the twin hands' motion, on (W, S) or on their gears; the one big bang's setting; the shears' return (R11). Decided by him: the 24 without the 48, a twin train where it is needed, the fair draw's push |

## 11. Open, by name

- **(a) The twin hands.** A spinor's quarter turn needs the root of 2 over the Gaussian integers, and a carried scale does not survive the carries (section 3). So **the second way stands** (David): the twin hands are read only through (W, S), and the 24 is asked of those. **For the owner:** the twin hands' motion written on (W, S), which keeps the 24, or on their gears, which keeps their interference and the half turns alone.
- **(b) The 24 with one coupling, or the 48.** With the reflections, every kind splits in two, giving ten kinds. Animate's reading (6462233147), which the Boss recommends:
  - the law is the 24 exactly; under the 24 alone a vector and a mirror vector are one kind;
  - the mirror's break, nature's one hand (row 69), enters at one place only: a one-hand coupling, one row of the calibre's couplings, with no act of its own;
  - the test: the 24 rotations alike bit for bit always; the reflections part only through that coupling, where it acts; a parting anywhere else is a bug;
  - the fixed-point test names its group (David): at a point the 48 fix, the twist reads 0; at a point only the 24 fix, it may stand.

  **Decided:** the owner's word through David, "go with the 24 without the 48". The twist, an A1 of the 24 reversed by every mirror, is the coupling's carrier, with no new number (David).
- **(c) The composite train.** Fusion: a bound pair as one larger clock, its kind the product of its parts' kinds and its integers derived from theirs, with no new number. It waits on David's derivation. It is not seen on the head: row 76 reads NOT SHOWN on the one big bang.
- **(d) The Bell click, in the gear's form** (David, DAVID-TENSOR24-THE-CLICK.md on toys-5 1cadb3931), with no turn, no quaternion, no cosine and no number:
  - **the split's share** is one trace of two twin readings: up where c (W + W) W_d < room (W W_d + S . m). Here (W, S) is the pair's reading, and (W_d, m) a second twin pair standing at the Node-clock, the detector. Without one, the detector is the pair's own upper twin, as on the head (30,388 draws alike);
  - **the closure:** the fitting sets the open axis on both fitted hands (S = 0), so the first click is half and half by the rule itself. The first answer travels one Mesh a tick to the partner, whose reading becomes (W1, -a m1). The answers then correlate as -(m1 . m2) / (W1 W2), Born's singlet exactly;
  - **the one thing put in, named:** the closure, the fitting's opposite senses carried to the first click.

  Its form is the owner's word (a detector hand's gear, Sofer's recommendation, against bell_turn).
- **(e) Detectors in the one big bang.** Its calibre has no twin train, so it has no click of a split, and neither Born nor Bell is seen there.
  - **Decided:** the owner's word through David, "if another family is needed, no problem".
  - The twin train goes into the one big bang's calibre with its own pair.
  - It shows the click of a split (Born), and Bell wherever a second twin pair stands at a fitted hand's Node-clock.
  - Its pair and its place in the setting are David's to derive after the main formula.

## 12. The end check

- **No numbers:** no number beyond 0 and 1 in src; every integer in the calibre, the piece and its setting. The scan's number and table rules stand at 0.
- **No circularity:** no sine, cosine, root search, angle or closed form of a phenomenon in src, so the scan's circle, root, word and mix rules stand at 0. Sofer's audit items E1 to E19 are cleared one by one. The click's draw by the parts' sizes is the one chance.
- **Locality:** no state beyond the Node-clock, and no act reads the log. The state and log rules stand at 0.
- **No circular test:**
  - every test compares two runs or reads what the engine wrote;
  - no test asserts a number the code typed in;
  - the 24 is read by the images' test on every chart.
- **The step:** the one formula for every gear, and the gate as one act for every train.
- **Everything of section 8 stands,** the rewind 20 of 20 on every chart among it.
- **The counts to bring to 0,** from 526a5666d: the engine's 95 hits (the Boss) and the readers' 57 (Animate).

## 13. After every cut

- Animate's per-row diff (77 rows, 16 charts, 3 committed charts);
- the rewind 20 of 20;
- the books closed at every click;
- the 24 on nature and the hole, and the 48 on nature while the reflections hold;
- the suite under the 30 s bound;
- the scan with no count risen;
- the full check exiting 0 before any push.

## 14. Nature one to one: the 77 rows and what each needs

**The count.** The 77 rows of the gates on the four charts at 834cfd72e (the one big bang at 250 ticks), shown whole or in part:
- the hole 36, the chiral 33, the bodies 18, the one big bang 34;
- 44 of the 77 rows on at least one chart, 33 on none.

For nature one to one, every row must be shown on the one big bang's chart. What the 33 need, by kind (the Boss's reading of the rows' names and verdicts, for Animate to check row by row):

| what is missing | the rows | of what kind | who |
| --- | --- | --- | --- |
| twin hands in a calibre and a setting (the click of a split) | 39 the Zeeman and Stark shifts, 41 the spinor's two beats, 42 the split along the gradient (Stern-Gerlach), 57 GHZ; 56 Bell past the local bound | a train, the twin hands, in the one big bang's calibre | decided (11 e); David derives its pair and its setting |
| the one-hand coupling | 20 the twist's 24 and 24, 52 the neutrino; 69 on the one big bang | one row of the calibre's couplings, carried by the twist | decided, the 24 without the 48 (11 b); David derives its row |
| the composite train | 76 nuclear binding and fusion, 77 the baryon as a shape | a train, the product of two kinds, with no new number | David derives (11 c) |
| the conversion of one train into its list | 28 the conversion list, 49 the exponential decay | the click of a whole into several trains, the unspringing's generic form | David derives |
| the metric's shears read by an act | 36 the shears as waves, 35 frame dragging | the regulator's T2 back, with the act that reads it (R11 struck the shears because no act read them; general relativity's metric has ten components, the regulator seven) | David derives; the owner's word, R11 standing until then |
| gravity on light and on an orbit | 11 gravitational redshift, 12 light's delay or deflection, 13 free fall, 29 the redshift of light, 31 the deflection and the Shapiro delay, 32 the perihelion, 33 free fall by the tail | a setting, a mass with light or a bob passing, and its reading | the Boss sets; Animate reads |
| a stopped Node-clock | 14 the horizon, 34 the horizon and the stopped clock, 61 the horizon radiates | a setting that collapses to a stopped clock | the Boss sets; Animate reads |
| settings of packets | 38 the Aharonov-Bohm phase, 44 the moving setting's velocity against k, 50 light on light, 51 the Casimir force and the running alpha, 53 a fast packet binds at its setting, 54 scattering, 55 the two slits | pieces and their readings | the Boss sets; Animate reads |
| a common temperature | 48 the black body, 75 temperature and equipartition | an exchange that shares the wind among the trains (the unsprung hand's wind stands 10^7 above matter's) | David derives |
| the reading across the turnover | 58 the fast expansion after the bang; 2, 3, 5 and 6 on the one big bang | the relics between swings read through the clocks' reversal (the owner's word of 05:4x UTC: because of the clocks' reversal, contraction is seen as expansion) | Animate reads |
| the momentum across the click | 23 the momentum across the click | the fitting's momentum read across its two ends | cut 5; Animate reads |

**The order:**
- the cuts of section 10 make the engine one act, row for row as the head;
- the trains, acts and settings above then bring the rows in, each derived by David before it is built, each read by Animate on the one big bang's chart;
- a train or act that needs a new number is refused, and goes to the owner.

## 15. The checks, by who ran them

- **The Boss:**
  - kinds24.py: the five kinds by characters on the 24;
  - spinor24.py: the twin hands' turns in integers (section 3);
  - formula0.py: the main formula bit for bit on the hole, nature and the one big bang (the table in section 2);
  - the scan's counts at 526a5666d (section 9);
  - the rows' table at 834cfd72e (section 14);
  - the fair draw, cut 1, pushed as 834cfd72e (the full check 118 passed, the scan clean).
- **David, done:**
  - the twin hands' scale exponent refuted at the carries (956 of 2,000 random draws differ);
  - the Bell click in the gear's form, alike with the head at 30,388 draws, Born's singlet exactly (DAVID-TENSOR24-THE-CLICK.md, toys-5 1cadb3931, full check 118, Sofer's gate clean);
  - the twist checked over all 48 images (6462024199).
- **David, asked** (#2187 6462600571):
  - the main formula against the head on toys-5;
  - the twin hands' integer turns;
  - section 8's completeness;
  - the fair draw on toys-5;
  - the derivations of section 14.
- **Animate** (asked): the 77 rows against the trains each needs (section 14, row by row); the bench of 834cfd72e.
- **Sofer** (asked): the plan against the law clause by clause; the names against docs/CLOCK_WORDS.md; the scan on every push.
- **The plan goes to the owner** when all four have checked and approved.
