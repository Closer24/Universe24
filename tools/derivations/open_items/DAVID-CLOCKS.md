# What each thing is as a clock

David, 2026-10-27, 09:0x UTC, for the Boss.

## The word

The owner's word of 2026-10-27, 08:4x UTC, in translation: "Look at everything as clocks and think what each thing actually is."

Read on the engine head 70ac3b30c; toys-5 carries the same src. Each row names the act it reads and how it was settled:

- **checked**: the script beside this file (DAVID-CLOCKS_CHECK.txt) ran the engine's own functions;
- **read**: read from the code, with no measurement;
- **earlier**: measured or derived in an earlier document named in the row;
- **unknown**: neither settles it.

## 1. The one clock: the carried division

**A line is a two-hand clock.** Every line holds w a + r (core/acts.py:18). Rule3's step (core/rule3.py:93) is an exact integer leapfrog. Write the line's velocity as V = w (a_now - a_before) + r. The step gives:

- V' = V + F, with F = flux - D a_now;
- a_next - a_now = V' div w;
- r' = V' mod w.

So the remainder is the fine hand, on a dial of w ticks, and it holds the fractional part of the line's velocity. The level is the coarse hand. The wall is the gear between the two hands.

Checked: 200,000 random steps at six walls with 0 departures, and the step at -1 returned every one of them bit for bit.

**Born at rest.** The kick reads the momentum as this velocity measured from the half wall: P = V - w div 2 (interval.py:162). A line is born with its fine hand at the half wall (core/acts.py:13), so it is born at rest below one level. Checked.

**The dial's two mirrors.** T is r -> w - 1 - r (core/acts.py:8); C is r -> (w - r) mod w. With the slots exchanged:

- T sends P to -P - 1;
- C sends P to -P, wherever r is not 0.

Checked on 100,000 states. The run back needs T, because only T inverts the floor; the exact negation of a velocity is C. Applying C after T moves every remainder one tick forward. C fixes 0 and w/2; at an even wall T fixes nothing. Checked at w = 12; the Boss's exhaustion at the walls 2 to 12 and at 1,000 stands.

**The direction is the slot (CA-S1).** A clock's arrow is which of its two last readings is called now.

**Everything else is built from this one clock.** Every act of the engine does one of three things to it:

- advances it by a force (the division);
- exchanges its two readings (the direction);
- lays a count on its coarse hand (the lay).

## 2. The ladder

| Thing | What it is as a clock | Where | Status |
|---|---|---|---|
| A family (a record row's pair num / den) | A clock with its own rate at rest. With the Links at rest the step is the rotation by omega_0, where cos omega_0 = num / den (2 K / w = 2 num / den exactly) | core/rule3.py:39; metric.py:54 (Y-S2, "the clock family on the Ports") | checked on four pairs |
| Mass | That rate at rest: the Node term D = 12 (den - num) p_0^2 G^2 | core/rule3.py:34 | read |
| Light (num = den) | A clock with no rate of its own. D = 0, so it turns only through its Links | core/rule3.py:34 | checked (D = 0) |
| The Node's clock p_0 | The rate of every clock at the Node. For every family, exactly, 1 - cos omega_0' = (1 - cos omega_0) (p_0 / Gamma)^2, so sin(omega_0' / 2) = (p_0 / Gamma) sin(omega_0 / 2) | core/paces.py:90 | checked: omega_0' / omega_0 = 0.904993, 0.367985 and 0.049998 against p_0 / Gamma = 0.905, 0.368 and 0.050 at the contents 100, 1,000 and 3,000 |
| Content | The count of 1 / Gamma slowings compounded on the Node's clock, p_0 = Gamma (1 - 1 / Gamma)^c, read as the level of the carrier's time line | core/paces.py:90; interval.py:82 | checked |
| The carrier's time line X (the volume) | How many of the Node's own ticks and ruler cells one board cell holds: X = Gamma (Gamma / p_0)^(d + 1) | features/volume:37 | read |
| The Link's pace (the ruler goes with the clock) | The clock twice, p_0^2 div Gamma. The reach over the wall is (1/3)(p_link / Gamma)^2, so light's speed at a Node falls as the square of the Node's clock rate | core/paces.py:95; core/rule3.py:39 | checked: R / w = 0.2236 and 0.0061 against 0.6708 / 3 and 0.0182 / 3 at the contents 100 and 1,000 |
| Gravity | Clocks slowed by content, every family alike (the equivalence principle in one line of the rule's integers), plus the ruler going with the clock (light at twice the slowing) | the two rows above | read |
| The horizon (the frozen Node) | A stopped clock. The Link's pace rounds to 0 (content 3,793 at Gamma 1,000), no act changes the Node's state, and its proper count rests | core/paces.py:100; interval.py:89 | checked |
| The proper count | The Node's own clock: p_0 added per interval, 0 at a frozen Node | interval.py:89 | read |
| The interval | The board's one tick. Every Node takes it, its own clock turning p_0 / Gamma of it | interval.py:276 | read |
| The phase line | The reference clock: a hand of length X turning 1 / Gamma per act at the wall 2 Gamma^2 (Chebyshev's recurrence). Run at 2 Gamma for a Link's count, it turns half that per count | features/phase:24-56 | checked (D, K_0) |
| The amplitude X | The length of the reference clock's hand. It sets how finely an angle is read, never the angle; the records are bit for bit above the floor | features/phase:100 | earlier (THE-AMPLITUDE-SCALE.md) |
| The floor, 23 Gamma | The shortest hand whose rounding over half a turn stays under one of its own steps | features/phase:89 | earlier |
| The walled row | The Node's phase clock. It sums the potential read on the Node's own clock (the clocked potential, interval.py:96). Its fine hand, on a dial of 2 ticks, is the frame bit: flipped at every swap, it is the parity of the Node's reversals | interval.py:96-111; links.py:83 | read |
| A Link's phase | The angle between two Nodes' phase clocks, n_ij = K_i - f_ij K_j, read on the reference clock. The arrivals across the Link are turned by it | links.py:94 | read |
| Electromagnetism | The mismatch between neighbouring phase clocks | the two rows above | read |
| Charge W | The cross of a hand's two last positions in its plane, re_now im_before - im_now re_before: the area its tick spans, with the hand's sense as its sign | gram.py:85 | read |
| A charged child | A hand spanning half a quantum of action per tick (A B = T div 2), with its sense as the charge's sign | merger.py:18 | read |
| Particle and antiparticle | One family's clock turning in the two senses | gram.py:85 | read |
| Momentum and current | The cross of one line at two neighbouring Nodes: how far one clock leads the next (the phase gradient) | take.py:85; links.py:149 | read |
| The one bilinear | The area between two hands: two lines at one place (charge), or one line at two places (current, momentum, the twist) | links.py:26 | read |
| A quantum | The action of one beat at the family's rate, 3 T sin omega_0 | core/rule3.py:125; node.py:69-70 | read |
| Energy (the share) | The hand's length squared in the rule's form. N quanta of one symmetric family are one hand of length sqrt N | gram.py:133 | earlier (DAVID-STEP-3.md) |
| A meeting | Two neighbouring clocks, each holding a whole quantum. The + child goes where the current flows in and the twist is right-handed | close.py:45 | read |
| A birth | The field's hand shortened by the children's quanta (the take), and two new hands laid in opposite senses | close.py:112; merger.py:25 | read |
| The draw (which family is born) | The fine hands of every line at the Node and its six neighbours, read as digits and composed modulo the taken row's unit times the count of planes. Refused where every fine hand sits at the half | draw.py:17 | read |
| The click (a body's credit) | One beat at one point: a record that has held a whole quantum through one period of its beat (its re line's zero crossings) gives one quantum and is credited | bodies.py:22 | read |
| The one-click floor | The fine hands the credit's frame does not show. The frame holds levels, so the floor on x grows with the wall w | decoder.py:305 | read |
| The swap at the top | The Node's clocks reversed: the slots exchanged, the im lines negated, every fine hand mirrored | node.py:240, 256 | read |
| The bang | Every Node's volume clock at its top at once, every Node reversed, the board run back to the seed's first state (the exact return), and reversed again at the floor | bangs.py:40, 57 | read |
| The runaway | The volume clock's next top grows as the square of the last, over Gamma^2 T / 4. Under step 3 it stays bounded on the bang world to 100 intervals | THE-BANG-RUNS-AWAY.md; DAVID-STEP-3.md | earlier |
| The run back | Every clock run backward: each act at -1, with T conjugating the division | core/acts.py:18 | the head's tests |
| The 48 | The cube's relabelings of the Ports: the clocks' layout in space. It breaks where a negation mirrors a fine hand with T (P -> -P - 1) where C (P -> -P) is due, one tick apart | DAVID-ON-THE-TOY.md (j) | earlier |
| Pauli | A symmetric family: one hand per family per Node, holding any number of quanta (step 3). An antisymmetric family: one hand that holds one quantum, a second refused (step 2, close.refuse) | close.py:88 | declared by the exchange key, not derived |

## 3. What the picture unifies

1. **One object.** Every line of every row is the same two-hand clock, and every act is one of the three things in section 1.
2. **Three rates.**
   - A family's rate at rest is its pair (mass), declared by the universe file.
   - The Node's rate is its content (gravity), read from the time line.
   - The Link's rate is the ruler (light's speed): the Node's rate twice.

   Every family's rest clock slows by the same factor at a Node, exactly in the half-angle sine.
3. **The fine hands are the hidden variables.** The draw reads them to pick the family. The credit's frame cannot show them, and that is the one-click floor. The engine's chance and its uncertainty are the same hands, seen from the two sides.
4. **Light is never a body because light has no clock of its own.** A body clicks after one beat of its own clock at one Node; light's D = 0 gives it no beat at rest. This reads cs4's sentence (bodies.py: the gap-0 plane is never credited as a body) as a consequence rather than a rule.
5. **Every conserved quantity is an area between two hands** (the one bilinear).
6. **The arrow is a label.** The direction is which of the two readings is called now; the swap relabels it; the bang is every Node relabelling at once.
7. **The two mirrors coincide only at an odd wall.** There T fixes (w - 1) / 2, and the negation about a birth at (w - 1) / 2 is T itself. The law's walls are even (the 6 of the Ports and the 2 of the doubled cosine), so T and C stay one tick apart. F48-S1's uniform C (T for time's exchange, C for a negation) is the mend that fits even walls. This is a remark only, with no change proposed: an odd wall would move every record.

## 4. What the picture does not solve

**Spin.**

- *What a spin is as a clock.* A clock whose hand turns when space turns, at half the rate. The engine's hands turn in their own planes (re, im), none of which is a plane of space. No act of the engine turns the board's space: the 48 are relabelings of the Ports that the kit compares, not acts.
- *What carried it.* The struck shape-8 row carried the double cover exactly (loader/quartet.py on the head): the lifts (1 + i sigma_a) / sqrt 2 in Q(zeta) with zeta^4 = -1, the 45-degree internal turns that a 90-degree turn of the cube needs. With that row out (boss-clocks-1), no row carries a hand that turns with space.
- *Why the dial's centre A cannot replace it.*
  - A moves one line's fine hand by half the wall. That is a change of half a level per interval in the velocity at the next division, not -1 on the levels.
  - Every quotient of a dihedral group is dihedral or of order at most 2. The cube's 24 rotations form S4, which is neither. So no dihedral group maps onto the cube's rotations, and the dial's group cannot cover them.
- *On boss-clocks-1's ENGINE.md.*
  - The new paragraph's sentence "The double cover the row carried ... stands in the remainder's own symmetry" claims more than the algebra gives: the group facts stand, the cover does not.
  - Two slips in the same file, where "quartet.py, " was struck: "loader/loader/seed.py" in the modules paragraph, and "loader/py" there and in the new paragraph.

**The click's outcome.** Which family is born and which end gets which child are decided by the fine hands and the current's direction at the meeting: deterministic and local.

**Bell.**

- *Both sides of the Boss's reader are clocks* (bell2.py on boss-toy-1). The outcome is the side of the half on which the take's fine hand sits (2 r >= booked). The setting is the parity of the detector Node's proper count.
- *The setting reads the Node's content history.* At the vacuum p_0 = Gamma = 1,000 is even. So the parity of the proper count changes only at the intervals the Node spends at a content with an odd clock: 1, 3, 5 and so on (29 of the contents 0 to 59). The content is written by the stress the Node holds, the arriving quantum's among it.
- *So the setting is not free of what it measures.* That is the one door Bell's theorem leaves open, and here it is built into the engine. The pair's two clocks carry their fine hands from one birth, and each end's click reads its own Node and its six neighbours. With settings independent of the hands, |S| <= 2 would hold.
- *Whether the door carries S past 2 is unknown.* Measured so far: S = +2, +1, +2 and +2 on 12 to 17 pairs. The Boss's ensemble of 32 is the place to read it.

**Pauli is a declaration.** The exchange key declares which family holds one quantum per hand; the dial does not derive it (DAVID-ON-THE-TOY.md (j)).

**Light's quantum.**

- *The rule.* Each family's quantum is the action of one beat at its rate, 3 T sin omega_0. Light, with no rate at rest, takes the unit at sin = 1 (node.py:70: 3 T den), the quarter-turn clock of the wave lay (loader/wave.py:34).
- *The consequence.* Light laid or born at another rate carries the same unit.
- *The open question.* Should a quantum of light follow its own rate? No measurement here.

## 5. The checks

The script DAVID-CLOCKS_CHECK.txt beside this file is a Python file stored as text. Run it with the repository's src on the path. It printed:

```
1. leapfrog identity V' = V + F and the exact step back, failures: 0
2. T gives -P-1, failures: 0 ; C gives -P (r != 0), failures: 0
   born remainder w/2 at rest gives P = 0
3. C(T(r)) - r mod w over the dial: [1] ; C fixes [0, 6] ; T fixes []
4. num/den = 1655909141 / 1655909141 : 2K/w == 2 num/den exactly: True ; mass D = 0
4. num/den = 1655909140 / 1655909141 : 2K/w == 2 num/den exactly: True ; mass D = 12000000
4. num/den = 1655000000 / 1655909141 : 2K/w == 2 num/den exactly: True ; mass D = 10909692000000
4. num/den = 1200000000 / 1655909141 : 2K/w == 2 num/den exactly: True ; mass D = 5470909692000000
5. content 0 clock 1000 link pace 1000
5. content 1 clock 999 link pace 998
5. content 10 clock 990 link pace 980
5. content 100 clock 905 link pace 819
5. content 1000 clock 368 link pace 135
5. content 3000 clock 50 link pace 3
   frozen content (Link pace rounds to 0): 3793
6. content 0 p0/Gamma 1.0 omega_0'/omega_0 for two families: [1.0, 1.0]
6. content 100 p0/Gamma 0.905 omega_0'/omega_0 for two families: [0.904993, 0.900866]
6. content 1000 p0/Gamma 0.368 omega_0'/omega_0 for two families: [0.367985, 0.360327]
6. content 3000 p0/Gamma 0.05 omega_0'/omega_0 for two families: [0.049998, 0.048807]
7. content 0 R/w 0.3333333333333333  (pl/Gamma)^2 = 1.0  (p0/Gamma)^4 = 1.0
7. content 100 R/w 0.223587  (pl/Gamma)^2 = 0.6707609999999999  (p0/Gamma)^4 = 0.670801950625
7. content 1000 R/w 0.006075  (pl/Gamma)^2 = 0.018225  (p0/Gamma)^4 = 0.018339659775999998
8. phase line D, K0: 2000000 1999999 angle per act ~ 1/Gamma; half turn in acts ~ pi Gamma = 3142
```

In line 6 the ratio of the angles departs from p_0 / Gamma for the heavier family because the exact law is on the half-angle sine, not on the angle. The floats appear in the reader's print only, never in an act.

A document alone: no code and no test change.

## 6. The sync of 09:2x: a ready mend for boss-clocks-1's step 1

The owner's word of 2026-10-27, 09:0x UTC: "sync with the Boss." The thread holds no line from the Boss since 07:59, and both his branches are unmoved (boss-clocks-1 4b5c3d834, boss-toy-1 5427577aa). His step 1 of the clocks line stood red on one gate: the code ratchet, with rows.py grown from 151 to 154 lines.

The mend beside this file, DAVID-CLOCKS-STEP-1_MEND.txt, is a git diff (8 files, +15 -12) that applies cleanly on boss-clocks-1 4b5c3d834:

- **The shape refusal moved.** The refusal of a row of a shape the law does not name leaves rows.rows_of and joins the file's other refusals by name in loader/world.read_world, before the pair-or-wall check. rows.py is then 150 lines, one under the head's.
- **One line of test.** test_the_files_are_refused_by_name refuses a universe whose one row is of shape 8, by the name "no row of the law". The file stands at 600 lines; tests/ stays 145 lines under the merge base.
- **The stale docstrings re-cut.** The ones that named the quartet as present: node.records, run.credit, the bodies module, readings.scale and readings.rule_of.
- **ENGINE.md.**
  - The two path slips mended: "loader/seed.py" in the modules paragraph, and the struck module named "loader/quartet.py" in the new paragraph.
  - The double-cover sentence re-cut to what the algebra gives (section 4): the cover leaves with the row and spin is open. The Boss's dihedral centre is kept as he derived it and named as no cover of the cube's rotations.

Measured on the mended tree, with its own src on the path:

- the full check exits 0: 106 passed, and ruff, mypy, the engine gates, the code ratchet, the tests' shape and the documents' six gates hold against origin/engine-5.0-test;
- the three records regenerate SAME, key by key with the committed ones but the milliseconds (hole 60, chiral 60, bodies 120);
- the run back is exact 20 of 20 on each.

Whether to apply the mend, change it or leave it is the Boss's call.
