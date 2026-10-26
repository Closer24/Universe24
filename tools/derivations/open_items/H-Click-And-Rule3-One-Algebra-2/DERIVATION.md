# H-Click-And-Rule3-One-Algebra-2 (hand ca2, 2026-10-26, head f864dde24): the click and Rule3, the direction of time in the algebra

## 0. The unification step (the block's four roads)

The letter holds the direction twice: Rule3's `direction` (core/rule3.py carried_division: sigma on the total and on the quotient, the remainder in [0, w)) and the click's undo (close.py unclick: the lays negated in the reverse order from the frame). Road (4), Rule3 as the one step: the one object is the exchange of the line's two slots conjugated by the remainder's mirror, T: (now, before, r) -> (before, now, w - 1 - r). Rule3 at -1 IS T Rule3(+1) T (section 1, 20,000 of 20,000). The click is NOT T-covariant in its inverse: T lay_now(q) T = lay_before(q), while the undo is lay_now(-q); so the click's direction is the slot its lay distinguishes, and the record of that distinction is the Wronskian of the children (re on the now slot, im on the before slot), odd under T: the charge. One sentence (section 6) folds the two: the direction is the slot the act names; Rule3 reads it, the click writes it. What no form folds: the take's quadratic (section 3).

## 1. Rule3's direction (Q1): the slot exchange conjugated by the mirror

Clauses: ALGEBRA.md #the-direction (u = sigma(Y - w y) + rho, z = sigma(u div w)), #the-cube's-symmetry act (1) (floor((w - 1 - u) / w) = -floor(u / w) for every integer u), #the-four-acts (c) the division.

Let a line's state be (now, before, r), the step forward F: (now, before, r) -> (next, now, r') with w next + r' = Y(now) - w before + r, Y the arrivals' sum with S now. Let T be the slot exchange with the remainder mirrored. Claim: F^-1 = T F T. Proof: T(now, next, r') = (next, now, w - 1 - r'); F on it reads a = now as the doubled slot (the engine's `rule3(flux, mass, w, now, other = next, ...)`: the now slot is read as the level, the other slot as the subtracted one, so the "exchange" is the exchange of the other slot, before -> next, the now slot the same in both directions), the total u = Y(now) - w next + (w - 1 - r') = w before - r + w - 1 = w before + (w - 1 - r), 0 <= w - 1 - r < w, so the quotient is before and the remainder w - 1 - r, mirrored back to r. The head's letter writes the same function as sigma (u div w) with u = sigma(Y - w next) + r': by the complement identity the two are one integer. So the time reversal of Rule3 is BOTH the exchange of the subtracted slot and the conjugation by the remainder's mirror, and the one asymmetric piece of the algebra is the remainder's interval [0, w): the floor. Without the mirror the exchange alone is never the inverse (0 of 20,000); without the exchange the mirror alone never (0 of 20,000). Nothing else of the line carries a direction: the coefficients S, w, R are even, Y is read at the slot the direction names.

Measured (q1_rule3_direction.py, PYTHONPATH=<worktree>/src): lines 20000, back_bit_for_bit 20000, exchange_and_mirror_equal_back 20000, exchange_alone_equal_back 0, mirror_alone_equal_back 0, complement_commutes_with_floor 20000 of 20000; the 3-cube Node (world_node.json) stepped 20 forward and 20 back: 20 of 20. Predicted before the run: 20000, 20000, "only where w divides the numerator", 0, 20 of 20; measured as predicted (the exchange alone 0).

## 2. The click's direction (Q2): the slot the lay names

Clauses: ALGEBRA.md The click (the three sentences; the twist), #the-four-acts (d) the load; CR-S1 (the take one carried division of levels times the wall, the remainder unmoved); GP-S1 (re_now A, im_before sense B); CK-S1 (the crossing read in either direction); RW-S1 (the frame the record of the reversal).

The click's acts in the letter: (i) meet: reads F_ij = num(now_i before_j - before_i now_j) at the interval's start and the twist h (a product of such currents), the charges W = re_now im_before - im_now re_before; (ii) the take: now -> now + t s on the chosen line, t = sign(before - now), s the least count whose fall pays the walls (take.fall_of); (iii) the children's lay: re_now += A, im_before += sense B at each end (close.child_at); (iv) the bodies' credit: the take at the zero crossing (before now < 0 or one of them 0). The undo (close.unclick): the same lays with the sign -1 in the reverse order, the take's line restored to taken_now_was, from the frame.

Where the forward and the undo differ in the letter, and who writes it:
- the order of the lines: reversed in the undo. Written by the click alone (the inverse of a composition); Rule3's own inverse is one act.
- the slot moved: the same slot in both (the now slot for the take; re on now and im on before for the children). Written by the click alone: Rule3's inverse exchanges the subtracted slot, the lay's inverse negates the load. This is the click's direction: T lay_now(q) T = lay_before(q) is not lay_now(-q).
- the trigger's sign: the crossing is read even in the slots (CK-S1): no direction in it; a touch of zero is a crossing from either side alike. Forced by nothing; neutral.
- the cone's side (the end the current flows into, the + child by the twist): F and h are odd under T, so under T the current reverses and the + child goes to the other end: the senses exchanged (U-S3's reading). Forced by Rule3's own algebra: the current is Rule3's conserved bilinear and T-odd by its form.

So: a quantum laid on the now slot alone is the record present at this interval and absent one before (the quantum to the future); on the before slot alone it is present one interval ago and absent at this one (the quantum to the past); the take removes s levels from the now slot alone (the future's side; the front stays in the before). The children's lay puts one foot in each: re on now, im on before, and their product W = A sense B is the charge: the record of the direction.

Measured on the records (q8_takes.py <world> 60; the take's slot and sign read at every call of take.fall_of from take_at, no src edited): the hole 60 and the chiral 60: the counts in section 8 (takes, slot_moved_now, t_up, t_down, crossing, touch, no_crossing, child_lays_re_now, child_lays_im_before).

## 3. Q8 first: is the click Rule3 at -1 at the Node?

Candidate equation: click = R(-1) at the taken Node on the taken line composed with R(+1) elsewhere; the take's moved level now + t s against a_{-2} = R(-1)((before, now), rem) = (Y(before) - w now + (w - 1 - rem)) div w, Y(before) = S before + SUM_j R_j before_j.

Derived: the take's pull in take.fall_of, pull = own before + SUM_port R before_j, IS Rule3's numerator Y read at the before slot: the take reads R(-1)'s own numerator. But its move is the least s with fall(s) >= walls, fall(s) = X (w (now^2 - (now + t s)^2) - t s Y) div (2 Gamma^3 G^2) = -X t s (2 w now + Y + w t s) div (2 Gamma^3 G^2): a root of a quadratic in the levels, found by largest_below (a search by comparisons). By the theorem of #the-four-acts, every composition of Rule3's acts in either direction is piecewise linear in the levels with integer slopes, and nothing quadratic comes from them; the take's s is quadratic (the booking: the children's share). So no time reversal of the Node, at the Node or on the line, gives the take: the piece the click holds that no reversal gives is the booking, the walls paid by the share's fall. The one-Node measurement: the 3-cube's emitter line laid (now, before) = (1227, 920) at the centre: the take moved 10 levels to 1217; a_{-2} = -369: not equal (test_one_node_ca2.py, printed). The records: the count of takes with now + t s == a_{-2}, and with the sign agreeing, in section 8.

What the click does use of the Node's reversal: it reads the T-odd bilinears (the current, the twist, the Wronskian: which end is the future of the record) and the backward numerator Y(before) (the pull), and it writes the slot. The Node's own time reversal in the letter is the swap (FR-S1: now and before exchanged at the top), which the click does not call. The meeting of the past with the future at the Node is the zero crossing between the two slots (before now < 0): the T-fixed line now = before is where the two slots meet, and the take moves the now toward it by s <= |now - before|, reaching it only at the full fall (counted in section 8: full_fall_now_eq_before).

## 4. The conservations (Q4): what flips under T

Clauses: #the-conserved-form (w(now^2 + before^2) - S now before: even under the exchange), The charge written is the Wronskian (W = re_now im_before - im_now re_before: odd), The lattice momentum (P_a = 2 num SUM (now_(i+a) before_i - now_i before_(i+a)): odd), the current F_ij (odd), the count (the share, even), the energy as the beat per proper interval (a count of crossings, even by CK-S1).

Under the time reversal of the frame (every line's slots exchanged, the remainders mirrored): the form and the count unchanged at every Node; the Wronskian, the current and the lattice momentum negated exactly. Measured on the end state of each run (section 8: W_flips_sign, W_zero, form_same, F_flips_sign, F_zero, P_axis_flips_sign, P_axis_zero). The direction's record is the Wronskian/charge: the click's lay with no direction (the same quantum on both slots, (A, A, sense B, sense B)) writes W = 0 at one Node (test_one_node_ca2.py, measured 0); under it the gapped close's selector W_minus W_plus < 0 refuses every meeting by name `sense`, the children carry no sense and the record no charge: the charge conservation is not broken but emptied, and with it the momentum across the click (the lay's P is the T-odd Link record). The control behind the flag CA2_EVEN_LAY in /dev/shm/tmp/ca2/src_ca2 (make_flagged_copy_ca2.py, 4 replacements each matched once): the 3-cube 20 with the flag empty the head's hash fe1e50e94b0192bb bit for bit, run back 20 of 20; the hole 60 with the flag in section 8 if run.

## 5. The cube (Q5)

The one object: the cube's 48 (the signed permutations of the three axes, a signed component's remainder carried as w - 1 - r) extended by the exchange of the two slots T with the remainder's mirror, the same complement: the group 48 x {1, T} of order 96, the signed permutations of the four axes that keep the time axis as an axis (the hyperoctahedral group B3 x Z2, the fourth sign the direction). Generators: the three transpositions of the axes, the three axis reflections, and T. Rule3's step commutes with all 96 (the 48 by the theorem of The cube's symmetry; T by section 1). The click as a map of the state with its frame: covariant under the 48 with the senses exchanged under the 24 reflections (the twist a pseudoscalar), and under T with the senses exchanged (W T-odd); its inverse is not its T-image. The 48 on the chiral 3-cube's clicks under the form: not run in the box (the kit's clicks_48_example needs the lean toy's lean_full.py, which origin/toys-5 at 3dc12e307 no longer holds; cut short, section 8).

## 6. Everything the click does (Q6), one act of the form or a departure by name

- The cone: Rule3's reach is one Link per interval; the children are laid at the two ends of one Link, inside the one-interval cone: one act. Bell's band 4 < S^2 <= 8 is NOT SHOWN (|S| <= 2, BK-S1, BC-S1): a departure by name, the setting.
- The quantum to the past or the future: the slot: one act of the form (the take on the now slot; the im child on the before slot).
- The exact take (CR-S2): the move is one lay on the now slot (one act); its count s is the booking's root: a departure by name (quadratic, no act of Rule3 in any direction).
- The children's lay (GP-S1): the load act on the two slots at the quarter turn: one act; the W it writes is the direction's record.
- The birth's momentum (the recoil): the lay's P on the Link, T-odd, the Link's record (AJ-S5): one act; its T-image is the negated recoil.

## 7. The sentences, as they would stand in ALGEBRA.md under The direction (dated 2026-10-26, the former clause kept by name)

**CA-S1 (the direction is the slot).** The direction sigma of every act of the law names which of a line's two slots is read as the level and which is the other: Rule3's step at -1 is the step at +1 with the other slot exchanged (before for next) and the remainder mirrored, w - 1 - r, one function, the former sigma (u div w) kept by name as the same integer; a lay on the slot the direction names is a quantum to the future of the run, on the other slot a quantum to the past; the click's take and its re child lay on the now slot, its im child on the before slot, and the Wronskian of the two, the charge, is the record of the direction, odd under the exchange of the slots as the current and the lattice momentum are, the form and the count even. The click's undo is the lay negated from the frame and not the click's image under the exchange; the arrow is the click's alone because the lay names a slot.

**CA-S2 (a finding, no sentence).** The click is not Rule3's step at -1 at the Node nor a time reversal of the Node: its take's count is the root of the share's quadratic (the booking), which no composition of the four acts in either direction gives (the theorem of The four acts); the click reads the backward numerator Y(before) as its pull and the T-odd bilinears as its orientation, and writes the slot.

## 8. The measurements on the records (filled after the runs)

All runs in the engine at f864dde24 (src/, no edit), PYTHONPATH=<worktree>/src, TMPDIR=/dev/shm/tmp, the test worlds of tests/worlds (the hole seed world_hole.json 5-cube 60, the chiral seed world_chiral.json 5-cube 60, the 3-cube world_node.json 20, the ga2 wave world_ga2.json 4-cube), the load below 3 before each run (poll_load.py), one record at a time. Commands: `python q8_takes.py world_hole.json 60 out/q8_hole_60.txt` (7 s), `python q8_takes.py world_chiral.json 60 out/q8_chiral_60.txt` (10 s), `python q2_records_count.py <worktree>/examples/records/{hole,chiral,bodies}.json`, `python run_flag_3cube.py <src> <world> <n>` with CA2_EVEN_LAY empty or 1 (run_six.sh), `python make_flagged_copy_ca2.py`.

Predictions written before the runs: the slot moved the now slot at every take (by the letter of take.lay with `line=`); equal_rule3_minus1 0 (the take quadratic, Rule3 linear); the run back 60 of 60; the form even at every Node, W, F and P flipping sign exactly wherever nonzero; the flag empty the head's hash; the flag set: W_children 0 at every birth in the hole, the gapped meetings refused by `sense` more often, the run back 60 of 60.

Q2 (the records, the engine runs and the published records examples/records/*.json of the head, equal counts):
- hole 60: takes 793 (16 births' + 777 credits'), slot_moved_now 793 of 793, the move's sign t = -1 (the now above the before) 793 of 793, the taken line's slots never straddling 0 at a take (no_crossing 793; the trigger CK-S1 is read on the record's re line and is even: the credits' frames show re_before > 0 >= re_now 62, re_before < 0 <= re_now 65, neither 650), the children's lays re on now 32, im on before 32, W_children opposite at 16 of 16 births, SUM W 0, SUM senses 0; full falls (the line sent to now == before) 16 of 793.
- chiral 60: takes 2960 (17 births' + 2943 credits'), slot_moved_now 2960 of 2960, t = -1 2960 of 2960, no_crossing 2960; the credits' frames down 72, up 87, neither 2784; the children's lays 34 and 34; W opposite 17 of 17, SUM W 3149 (the children laid on standing levels), SUM senses 0; full falls 121 of 2960; laid back 3.
- bodies 300 (the published record, 7-cube): takes 1973, slot now 1973, t = -1 1973 of 1973; the frames down 174, up 193, neither 1606; full falls 108.

Q8 (the take against Rule3 at -1 on the taken line at the Node):
- hole 60: equal_rule3_minus1 0 of 793; sign(a_{-2} - now) == t 793 of 793; a_{-2} between now and before 0 of 793 (the backward level lies beyond the before at every take).
- chiral 60: equal 0 of 2960; the sign agreeing 2948 of 2960 (12 against); a_{-2} between now and before 27 of 2960.
- the one Node: moved 1217 against a_{-2} = -369 (test_one_node_ca2.py).
So the candidate click = R(-1) at the Node holds at 0 of 3753 takes; the direction of the take agrees with the direction toward the backward level at 3741 of 3753, by the pull Y(before) being R(-1)'s numerator; the count s is the booking's root and never the quotient.

Q4 (the time reversal of the frame on the end state, every plane row at every Node; 4 rows x 125 Nodes):
- hole 60: form_same 500 of 500; W flips sign exactly 206, W zero 294 (206 + 294 = 500); F (1500 Links) flips 1026, zero 474; P per axis-row (12): flips 4, zero 8.
- chiral 60: form_same 500 of 500; W flips 311, zero 189; F flips 1271, zero 229; P flips 12 of 12, zero 0.
- the 3-cube 20: form 108 of 108; W zero 108; F flips 63, zero 261; P flips 1, zero 11.
Not one quantity flipped where the letter says even, nor stayed where odd: 0 departures.

Q4's control (the click with no direction, CA2_EVEN_LAY in /dev/shm/tmp/ca2/src_ca2; run_flag_3cube.py):
- the flag empty: the hole 60 hash 1b02171052fcda74 and the chiral 60 hash 53cf4788e979752b equal to the head's src bit for bit; the 3-cube fe1e50e94b0192bb equal; the run back 60 of 60 and 20 of 20.
- the flag set, hole 60: hash cf19611e44324307, births 13 (16 at the head), W_children [0, 0] at every birth, refused_sense 7602 (5792 at the head), takes 1103 (793), the run back 60 of 60; taken - booked 3253978332339930229408 (2378881870249535792016 at the head); dP_lay [187651042576657975770, -585174192381968010482, -578723220097904797982] (the head's [0, 0, 0]).
- the flag set, chiral 60: hash 95263903452b29b3, births 19 (17), refused_sense 10630 (10555), SUM W 1924 (3149; the standing levels' cross), the run back 60 of 60.
The conservations in the clicks at the head (from the log, the credit and birth lines alone): the exact take taken 3470162596899443439299239 against booked 3467783715029193903507223 on the hole (taken >= booked at every take, the least s paying the walls), 8742592564662732340015875 against 8740676240523117950003511 on the chiral; the senses' sum 0 on both; the momentum across the click SUM dP_take [-1087813669612241011638, 0, 0] and SUM dP_lay [0, 0, 0] on the hole, [-877686800644461524876, 736035392800833586838, -546044797609155352668] and [207014759398364951532, 289887539016826024630, 16221484407646020760] on the chiral (the head's own numbers, unchanged by this hand).

The 48 on the chiral 3-cube's clicks and ga2 450: section 9.

## 9. What was cut short, by name

- The 48 on the clicks under the form (Q5): not run; the kit's clicks_48_example.py imports the lean toy (lean_full.py, lean_pa2), absent from origin/toys-5 at 3dc12e307 (toy.py alone); an engine form of the 48 on the clicks was not written in the box. The 48 on the step stands by the theorem; the form CA-S1 adds T, under which Rule3 is exact (section 1) and the click's senses exchange (U-S3).
- ga2 450: run in the background behind the load poll (run_ga2.sh; out/q8_ga2_450.txt and out/flag_ga2_on.txt); its numbers are in REPORT.md if it finished in the box, else named there as cut.
- The conservation check of the kit (conservation_check.py --toy) is the lean toy's; the clicks' conservations above are read from the engine's log by this hand's runner instead.

## 10. The spec for David (no new function where one exists)

CA-S1 is the toys-5 fold's form (3dc12e307: carried_division at -1 the division at +1 conjugated by the mirror; rotate's two slots read reversed by the direction; unclick struck): nothing further to build for Rule3. For the click: no code; the sentence names the slot the lay moves (take.lay with `line=` on now; close.child_at's (A, 0, 0, sense B)) as the direction, so no key of the world's four and no row of the universe file; the one-Node test test_one_node_ca2.py (3 tests, under one second (24 hundredths)) is the test: Rule3's reversal the exchange + mirror on 2000 lines; the take on the now slot alone with the before and the remainder unmoved; the lay's T-image the lay on the other slot with W negated, the undo the lay negated, the lay with no direction W = 0. The pass predicate on the records: slot_moved_now == takes (793 on the hole 60, 2960 on the chiral 60), equal_rule3_minus1 == 0, form_same == 500, the run back 60 of 60.

## 11. Missing by name

1. The 48 on the clicks under CA-S1's 96 (the time reflection added): the chiral 3-cube's clicks compared through T (the senses exchanged, the takes equal): one run of the kit's clicks_48 on the engine once a toy or an engine runner exists.
2. The charge's sum over the births on the chiral 60 is 3149 and not 0 (the children laid on standing levels, W = cross of the sum): whether the charge made at a birth is the children's own (-+ T div 2) or the Node's cross after the lay is a reading the decoder owes (row: the charge in the clicks).
3. The take's direction t = -1 at every take of 5726 (the taken line always above its before and positive): whether CS4-S2's line choice (the largest now^2 - before^2) forces t = -1 by the form, to be derived.
4. The owner's word on CA-S1.

## 12. The ledger row (Addition 6)

H-Click-And-Rule3-One-Algebra-2 | derived: Rule3's reversal = the slot exchange conjugated by the remainder's mirror (one function, the floor the one asymmetric piece); the click's direction = the slot the lay names, its record the Wronskian (T-odd), its undo the lay negated and not its T-image; the click is not R(-1) at the Node (the take quadratic) | one-Node test: test_one_node_ca2.py 3 passed under one second (24 hundredths); 20000 of 20000 lines; the take moved 10 against a_{-2} = -369 | toy: the engine's hole 60 and chiral 60: takes 793 and 2960 all on the now slot, equal to R(-1) 0 of 3753, run back 60 of 60, form even 500 of 500, W/F/P odd 0 departures; the flag empty bit for bit (hashes equal), the no-direction control W_children 0 at every birth of the hole, births 16 -> 13, refused_sense 5792 -> 7602 | gates touched: none moved (row 56 Bell stays NOT SHOWN, |S| <= 2; the charge in the clicks: the senses' sum 0, SUM W 3149 on the chiral named) | Universe: the form holds at every length (an identity of the floor), the width unchanged | spec: no build; CA-S1 documents; the toys-5 fold is its code | missing: the 48 x T on the clicks; the charge's sum on the chiral; t = -1 at every take; the owner's word.
