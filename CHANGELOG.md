# Changelog

All notable changes to Universe24, the reference implementation of Reality
Theory (Universe24). Versions are tags on `main`; each is archived on Zenodo.

## Unreleased

- The taking at a hop (ALGEBRA.md 9.62 (3), adopted by the model owner through the Boss, record 2042; BUILD.md section 26 item 48): at a hop the rows on the Nodes a body newly covers are booked to the set bound to it at their share of the norm (`_hop_takings`, `form_share`; the fraction carried on the record), after the step and the Port booking, a covered Node's density booked only where the record's current through the Link ahead is below the body's pace (the rows that crossed the face in the body's frame); the uncovered back booked nowhere; void at rest. With it the host bug behind finding 2: the detectors' Port pairs were cached at the load and never re-read after a hop, so a moving set's Ports stayed behind; cleared at every hop. tests/test_hop_taking.py the gate.

- The stock is given-family content (ALGEBRA.md 9.51 (8), the second move of 8e8ef04e; BUILD.md section 26 item 47): an emitting block declares its stock as `held` naming the given family and its own quanta as `amount`; a giving lowers the given family's content held at the body and leaves the body's own quanta and its charge; every emitting world regenerated (the count of givings unchanged, the level at the emitter one more); the engine's spending of the body's own quantum per giving HISTORY.

- The moving seat's proper pair (ALGEBRA.md 9.63 (3), the mathematician's ruling of 2026-09-25 on Nature24's finding that the seat's clock did not slow in motion; BUILD.md section 26 item 46): a moving seeded block declares `proper_clock`, the pairs the seat rotates at by the momentum's whole part from 0 (the clock) to |P| along its one axis, the generator's 2 cos(omega_K - K v) from the mode's own dispersion (`mode_dispersion`, `moving_rotation`, `proper_clock` in the massive record's generator; on a plane wave the free dispersion of 9.24 (2) exactly); the engine reads the pair of the drive's momentum now (`seat_clock`), so the seat follows the ramp as the cube's rows follow the well; refused absent on a moving block under `body_record`, at rest, on two axes, at the wrong length or with a first entry other than the clock; the four moving worlds of the massive record and the moving emitter toward nature regenerated with the key; tests/test_body_record.py the gate.

- The law's rule with Einstein's weak field (the model owner's "switch" of record 2024 through the Boss; ALGEBRA.md 9.57 (1) to (3), 9.61 (3), 9.62 (1); BUILD.md section 26 item 44): the one rule's three integers (R, S, w) = (2 p^2 num, 12 den Gamma^2 - 6 (p^2 + Gamma^2)(den - num) - 12 num p^2, 6 den Gamma^2) at the Node's own pace p = Gamma - c, written once in `event_universe.events.rule` and read by the step, its exact inverse, the seat's record, the wheel, the conserved form and the loader's int64 bound; the first-order rule of item 36 the field families' plain step and the control; the books' second form (`record_form`) unified with the one form; the integers Gamma = 10^4, A = 2^20, the seed 50 x 2^12; every shipped world regenerated (the dark body's content 4812 below Gamma), the test suites moved to Gamma 10^4 and their formulas to the rule's integers, the light clock's digests re-read. No pin compared: the check-mode runs of 9.61 follow.

- The body's record kept at its seat Node, nothing beside the GameBoard (the model owner's question of record 2036 and his order of record 2037 through the Boss; ALGEBRA.md 9.60; BUILD.md section 26 item 42): under `body_record` a seeded block's standing record (a, b, r) is the seat Node's own (`SeatRecord`, `Block.seat`; `BodyRotation` and `Block.body` HISTORY), stepped by the engine's one rule (`one_rule`, factored out of `_advance`, and `one_rule_inverse` out of `_advance_inverse`, the same integers for every record) with the standing family's six Ports closed on the seat (S_6 = 6 a) at the declared pair [num_c, 2 den_c] and the seat's own level: six times item 37's two-term rule, the same rotation, the remainder six times, the wheel and the residue the rule's own at the seat; the state's block entry carries `seat` [a, b, r] (`rotation` HISTORY); the profile a declared constant read at the giving click alone. `tests/test_body_record.py` asserts the seat's rule once and keeps item 37's gate; the digests of `tests/test_massive_record.py` unchanged (the one rule factored bit for bit). HOST (record 2039; BUILD.md section 26 item 43): the family's wall (`kind_wall`) read once per family and kept until a pair is written, a quarter of the light clock's host time; the support-only step, the one rule evaluated on a record's box grown by one Link and zeros written elsewhere (`LiveRecord.box`, `support_box`, `_window`), the inverse on the box; both bit-identical (the digests unchanged; `tests/test_support_box.py`), the model's local work per Node unchanged.

- The runs toward nature, rows 1 to 3, without pins (the model owner's question of 2026-09-25 through the Boss, record 2030; ALGEBRA.md 9.59 (0) to (3); BUILD.md section 26 item 41): `examples/events/toward_nature/` holds the five diagnostic worlds under Gamma 10^4 (the redshift's two light clocks on the chain, the arm of the bottom one held at c_1 = 2000 by a holder body of a fifth family; the longitudinal Lorentz clock at rest and carried along its arm one Link every 4 intervals, the emitter, its mirror and its set hopping together; the bending's beam 20 wide past a dark body with U_b = 0.1 on the beam's line) with their generator and readers, no `expectations.json`, no pin, no verdict (9.59 (6)); `tests/test_toward_nature.py` gates the files, the held level, the joint hop and the reader's arithmetic. The readings of 2026-09-25 are in the folder's README, each labelled by kind: the redshift's ratio 1.283 +- 0.010 against the continuum's 1.118 and the lattice's own 1.291 at k = pi / 2 (finding 1 for the mathematician); the moving clock's returning light passing through its moving set without a click (findings 2 and 3); the dark body's beam too narrow for a centroid at 30 records.

- The seated detector (ALGEBRA.md 9.46 (8) (c); the model owner's "start" of 2026-09-25; BUILD.md section 26 item 40): under `body_record` a detector may be one Node, its seat, its six Links its Ports and the click the seat's; a set of more than one Node keeps the cube rule of record 1899; a seat's inflow per interval is its Ports' share of a cube's, so its clicks come later and, where records can leave, fewer, the pattern the same; tests/test_seated_detector.py. The eighteen's files and pins untouched until the owner says the engine is stable.

- The dark body row, built and not run (the model owner's question and his "yes" of record 2015; ALGEBRA.md 9.54; BUILD.md section 26 item 39): `examples/events/dark_body/` with `make_worlds.py`, the dark world (a body of the family `dark` of content 100000 beside a beam's line: charge 0, no emitter, on no set), the bright control (the same M in the light clock's family with an emitter and a set bound to it) and `expectations.json`, the pins declared blind from the algebra (every record arrives past the dark body, the shadow of the bright one, the bend 13.7 Links toward the body by the ray through the static Coulomb field, the same in both worlds within one cube); `tests/test_dark_body.py` reads the files, the declarations and 120 intervals of each world without the pins. No run against the pins until the owner says the engine is stable.

- The one test of the board's reversibility and the clicks' physics (the model owner's records 2010 and 2011; BUILD.md section 26 item 38): tests/test_board_reversible.py on one small world with every piece; between clicks the board returns bit for bit, across a click no rule undoes it and only the taking click's deleted rows are lost once the click's ledger is undone by hand, a giving click losing nothing; on every click line the quanta and the charge totals, the whole quantum, the residue and the counted interval, Born's rule at the taking end; between clicks the weighted form exact. A piece listed for the mathematician: a giving click's interval carries two holds (the records step at the interval's start hold, the fields at the click's), which the engine's one inverse cannot serve.

- The giving click and the taking click, not birth: the rename of record 2016 (the model owner's word of 2026-09-25, "we need to stop using unclear names like births; is a birth a click?"; docs/TERMINOLOGY.md): one commit of names, no physics. Every click has two ends: at the taking click a body takes one whole quantum and its content rises by one; at the giving click a body gives one whole quantum and its content falls by one (what was called a birth); what it writes is the given record, of the given family, with the given rows. The engine's line `birth` is `giving`, its fields `given_norm` and `pace` as before; the click line's `birth` stamp of the runner's output is `giving` (the interval of the giving click); the emitter's file key `born` is `given` (the light clock regenerated, its stamp moved); the identifiers, docstrings, messages and the gate's tests swept (`GivenTrain`, `given_train_norm`, `givings`, `tests/test_given_train.py`); the readers of run records accept the old names for history; the ray law's own words, BUILD.md section 26 and the dated logs stay as history. Born's rule keeps its name.

- The body record (the model owner's word of 2026-09-25, "already now, because it is generic"; ALGEBRA.md 9.46 (1) to (3) and (9), 9.50 (8), 9.49 (3); BUILD.md section 26 item 37): under the world key `body_record` (false by default) every seeded block is held as one Node with a shape: its profile stored and never stepped, its own rows off the GameBoard, one rotation (a, b, r) stepped by the two-term rule on its clock pair at the pace of its Nodes, its residue its own remainder on its own wheel read at the seat, its tick the count of intervals as the lattice body's, its cycles the rotation's sign crossings, the born rows the file's, the inverse exact; the equivalence to the lattice body (the rotation within the profile's rounding, the count, the field, the ticks' distribution) is the gate in tests/test_body_record.py; the registered worlds keep the key off, no file or pin moved (the chain's state digest moved with the block entry's `rotation`).

- The Node's own pace, form (A) ruled (the model owner's ruling of record 2003, "take only from the current Node, not from the neighbours"; ALGEBRA.md 9.50 (13), with 9.50 (8) and (9) and 9.51 (2); BUILD.md section 26 item 36): under the constant wall 3 den Gamma the pace p_i = Gamma - c_i + q Lambda d_i of the Node alone multiplies the Node's own six-neighbour sum, 3 den Gamma a_next + r' = p_i num S_6(a_now)_i + 6 den c_i a_now - 3 den Gamma a_before + r (the Node steps the vacuum's rule at its own pace; the pace on each read's far end of item 34 HISTORY); the inverse with the same integers, exact everywhere; the conserved form the Node's terms weighted by 1 / p_i less the plain Link sum, an exact rational carried by the books and the state as [numerator, denominator]; the click's flux the plain current, Born's rule unchanged by one bit; a born record's form the exact rational `norm` / `pace` on the record and the birth line (p times it whole at one level, the body's own units), the ladder reading 2 W pace C against (2 u + 1) norm; the wheel the gcd of p_i num, 6 den c_i and the wall; the excitation norm in the body's own units; every registered world regenerated (stamps and norms), the chain digests moved, no pin moved.

- The family of charge (the model owner's decision of 2026-09-25; ALGEBRA.md 9.48 (1), (2), (3) and (5), derived from 9.45 by one sign; BUILD.md section 26 item 35): under the detector law every family declares its `charge` q, -1, 0 or +1 per quantum, no default; a body's charge Q is the sum of the signs of the quanta it holds, moved with the labels at the clicks and the births; a fifth family, named by the world key `charge_family` (the pair [1, 1], the quantum 1, no clock and no charge of its own; required under the detector law, refused without it), is held at every body's Nodes at Q and moves elsewhere by its own plain step, stepped last with the family of clicks and inverted with it; a record of charge q reads the effective content c - q Lambda d at every Node, Lambda the world key `charge_strength` (an integer from 1, required), so its pace under the fixed wall is Gamma - c + q Lambda d: a body of the opposite sign a deeper well, of its own sign a hill, light untouched; the clock pair and the wheel per family at the effective content, the birth line's `charge`; the run refused where the effective content reaches Gamma in size, the load where a body's content plus Lambda times its charge is not below Gamma; at most five families. Every registered family declares the charge 0: the field is 0 and the rows are bit for bit as before (the light clock's diagnostic run identical line for line to item 34's), the stamps and the chain digests moved; no pin moved. The charge suite `tests/test_charge.py`; the generators and every test world declare the fifth family and the keys.

- The fixed wall, the backward run exact everywhere (the model owner's ruling of record 1994 and his word of 2026-09-25; ALGEBRA.md 9.35 (2) amended, the mathematician's section asked; BUILD.md section 26 item 34): the wall of every family's rule is 3 den Gamma at every Node, a constant of the declared region, and the family of clicks' level enters the numerator as the pace Gamma - c of each of the six reads (3 den Gamma a_next + r' = num SUM_j (Gamma - c_j) a_j + 6 den c a_now - 3 den Gamma a_before + r), so the remainder's range never changes and the joint step is one to one at every Node for every clock history: the joint inverse is exact bit for bit, remainders and the field included, wherever the level falls (item 32's finding A resolved; the property (4) of 9.20 (B) restored in full). The rotation at uniform content 1 - cos omega' = (1 - cos omega)(Gamma - c) / Gamma, the same as before to first order; the vacuum bit for bit; the forms with integer weights at the scale 3 Gamma L (Gamma^2 times the plain form in the vacuum) and the current on a Link weighted by the pace at both ends; the wheel from the rule with the six reads' paces, the birth line's `read_clocks`; the guard |c| below Gamma; the load bound with (Gamma + M) on the reads. The light clock regenerated (the excitation norm in the new units, the stamp moved); the chain digests moved once more. The light clock's diagnostic run without pins (GAMEBOARD, no verdict): LAWFUL, 64 births and 64 clicks, the mean click interval 300.3 with the rms 15.8, no burst.

- The reseed retired, the residue at the click at the first shell Node, the tick a count of intervals (ALGEBRA.md 9.43 (3) and (4), 9.44 (5) (c), 9.47 (5), (6) and (9); BUILD.md section 26 item 33): a body's own record is never rewritten: a click sets the born rows, lowers the stock and the content, and leaves the body's own levels, phase and remainders as they are, the standing record going on after the stock is spent (the reseed with the kept remainder and the click rule on the running total HISTORY); the residue u is the own record's remainder at the body's first shell Node in the declared order, read at the click on the body's wheel there, the born record's residue and the next excitation's alike; the next click fires at the first count t of intervals with 2 W t >= (2 u + 1) P, P the emitter's `period` (required); the birth line carries `wait`, `period` and `read_node`; the chain digests moved once more. The light clock's diagnostic run without pins (GAMEBOARD, no verdict): LAWFUL, 64 births and 64 clicks, the mean click interval 299.1 with the rms 18.5, no burst (the mathematician's expectation of 9.43 (4) read as expected).

- The family of clicks (the model owner's closing of record 1982; ALGEBRA.md 9.41 and 9.45; BUILD.md section 26 item 32): the Node clock's content is the level of a fourth family, declared in every world file (the pair [1, 1], the quantum 1, no clock of its own) and named by the world key `clock_family` (required under the detector law, refused without it; a massive pair, another quantum, a clock, a body of it, a `held` naming it or an emitter birthing into it refused by name); one record of it over the board, held at every body's Nodes at the body's content (at the load and at every interval's end) and moving elsewhere by its own plain step, stepped last in the interval; every other family reads the clock pair (Gamma, Gamma + c) with c the family's level at the Node, so the content spreads from the bodies at the plain step's pace; the joint inverse (every family backward at the level of the interval's start, then the clock); the run refused at a level at or below -Gamma; the load bound with twice the world's content; at most four families. Every registered world regenerated with the family and the key (the profiles unchanged, the stamps moved); the chain digests moved once more. The findings for the mathematician's ruling, the merge held by the rule of three: (A) the joint step's inverse is exact only while the family's level stands or rises at every Node with a record, the property (4) of ALGEBRA.md 9.20 (B) weakened by about one part in Gamma per unit of the fall (the property test and the Node clock test assert the exact return before the first fall and a bounded loss after it); (B) at unit contents the field around a body is the plain step's rounding walk, not a potential; (C) a click's content spreads to an emitter body and moves the residues of its later births (the ladder orders' six of eight residues agree, the later two differ). The light clock's diagnostic run without pins (GAMEBOARD, no verdict, no pin moved): LAWFUL, 64 births and 64 clicks, the mean click interval 299.8 with the rms 28.7 (298.1 and 18.0 under item 31).

- The Node clock (the model owner's decision (5) of record 1962; ALGEBRA.md 9.35 (2) and (3); BUILD.md section 26 item 31): at every Node the clock pair (e, f) = (Gamma, Gamma + M), the same for every family, Gamma the world key `node_clock` (required under the detector law, no default; 10^6 in every registered world) and M the content held at the Node (the measured events' quanta on their Nodes, 0 in the vacuum), enters every family's rule as 3 den f a_next + r' = e num S_6 + 6 den (f - e) a_now - 3 den f a_before + r with the wall 3 den f, the inverse with the same; the vacuum the plain rule bit for bit with the remainder Gamma times the plain one, a Node with content slowed by e / f (2 cos omega' = 1.982200 at e / f = 0.8 on [800, 809], the mathematician's number, read on the engine), light through a slab delayed by the slowed dispersion (4.73 Links against 4.76 predicted); the content rebuilt from the held books as every interval begins and after a birth (down at a birth, up at a click, moved with a stepping body); the forms with the clock's weights and the flux booking times Gamma (the flux itself carries no weight of the clock: the share's identity, exact); the born record's norm its conserved form as written on the board; the wheel read from the rule at the Node, W = 3 den f / gcd(Gamma num, 6 den M, 3 den f), the pair's own in the vacuum and the body's content's at its Nodes (the tests read it from the rule); the load bound with Gamma and the world's content, the ceiling of `amplitude_bound` 2^28; every registered world regenerated with the keys (the profiles unchanged); `tests/test_node_clock.py`. THE LIGHT CLOCK'S DIAGNOSTIC (GAMEBOARD, no verdict, no pin moved): 64 births and 64 clicks, the mean click interval 298.1 with the rms 18.0 and the least wait 257, the births by 3098 with no burst (the countdown of item 30 does not form: the wheel changes with the content at every birth).

- The coupling is the click alone (the model owner's decision (2) of record 1962; ALGEBRA.md 9.34 (B); BUILD.md section 26 item 30): the dielectric coupling of MASSIVE_RECORD.md section 7 (the response records, the receive and source terms, the folded denominators, light's common wall and the index in motion) retired from the engine, every record advancing by the rule alone with the wall 3 den; the block key `coupling` refused by name; the light clock's A and every emitter body of the tests without it; the transparency reading retired; the chain digests moved once more. THE FINDING for the mathematician: with the remainder kept and no coupling, a residue below W / P makes the births count down one per interval (the light clock: 64 births by 1647 instead of 3311, two bursts), a GAMEBOARD reading; no pin moved.

- The remainder is the cell's (the model owner's decision (1) of record 1962 and his order of record 1968; ALGEBRA.md 9.34 (A), 9.35 (6) and (7); BUILD.md section 26 item 29): the engine's reseed after a birth keeps the ended excited record's division remainder at the body's cells, bit for bit and in its scale, never reset (the load's seed alone starts at 0, the file's integers), so the residues of the stock's births spread from the kept remainder with no coupling and no draw; the emitter suite reads it at every birth; the chain digests moved once more (all three); nothing else moves.

- The tightenings of the input (the model owner's rules through the Boss, 2026-09-25; BUILD.md section 26 item 28): one border for every family (the family key `faces` refused by name; every family reads the world's `boundary`), the cavity refused by name (`cavity_24` and `cavity_24_moving` cancelled, their files held as written), the stamp over the whole file (`input.hash` the digest of the document without `input`; every seeded file regenerated with the same integers), no implicit seed (every well declares `seed`; the loader's 2^20 gone), `N` required and `face_depth` required on an open board under the detector law (refused without it), and the tail check (a body's profile 0 at every Node of every other body of its family; the mathematician's 86e1df43): the gate's tests on the one border, the refusals, the restamped documents and the tail (two emitter bodies a hundred Links apart); the iterated mode's readings on the closed emitter chain move with the border (2487 iterations, 467 units from the eigensolver's, COMPUTATION); nothing physical moves.

- The born train as built, its birth's form HELD on the model owner's word of record 1950 (a birth as the emitter's own mode times its momentum's character, measured on this head at 1.00002 of the norm with the mode's tails and at 1.00023 as the box's own lowest mode on the cells; the mathematician's 9.35), the one form of a birth of ALGEBRA.md 9.17 (6a), 9.25 (11), 9.22 (7a) (iv) (BUILD.md section 26 item 27): the emitter's `train` (the direction and the periods) and `born` (the train's two levels over the body's cells and its norm on the vacuum), the generator's integers checked at load in integers (the flux sign along the way, the norm, the wavelength whole and the extent the train's length; the two-integer born refused by name); the generator's train (the character under the tapers and the window, uniform across a spanned periodic axis) with its checks on its own check board (the passage within 2 x 10^-3 of the norm, the transparency of a coupled body at 0.99, the placement one train's length from every face slab); the engine writing the train and the norm as written; the light clock restated in the one table's form ([760, 3, 3], the face slabs 32 deep, A [32, 3, 3] with its train, at_well A's own cells, the blind pins the mean interval 300 +- 9 and the first click 250 +- 8); the one command's `mean_interval` and the click line's `birth`; the 26 other emitting worlds held under the train (their builders retired, the files in held_worlds, to be rebuilt from the table); `tests/test_born_train.py` and the emitter suites on the train.

- The generator's working amplitude 2^28 (BUILD.md section 26 item 25 amended): at 2^20 the iteration for the muon layer's well hovered at 1.5 times the loader's residual bound for 2^20 iterations and wrote nothing, so the committed generator could not reproduce the muon files; at 2^28 it stops at 36694 iterations; every seeded world regenerated in about four minutes, the profiles and clocks moving by the floor (the muon's by 1650 units, the light clock's by 90, the chains' by at most 5; the chain digests of `tests/test_massive_record.py` with them).

- The property test of the board on the engine (ALGEBRA.md 9.20 (B), the gate of the unification's cleanup, record 1875; `tests/test_board_properties.py`): equivariance under the 48, translation, conservation of the content and of the form I with the exact remainder identity, reversibility by 8.8's inverse (`step_inverse`), locality, only the click reads, and the scaling check at 12^3, 24^3 and 48^3 (HOST). E as the one-way flux at every set and T as the record's conserved form (9.19 (3)): the cumulative ladder read at every interval, the record deleted whole at its rung, the open face the receiver `face` last on every ladder; the take, the sponge, the completion, the close, `escaped` and the clock body's booking retired with their tests; the ladder by name in the named order; every emitter's `norm` regenerated on the flux after the step; the line's test worlds on closed faces (an open face behind an emitter clicks the half that leaves); the four Malus worlds held with the Bell four (under the cumulative ladder as written the two cells at one Node give no distribution: the finding for the mathematician in tests/test_detector_law.py) (BUILD.md section 26 item 14). The residue from the law (ALGEBRA.md 9.22 (4)): no declared residue or wheel anywhere; u the clicking record's rule remainder at the body's centre cell in the remainder's step and W = 3 den / gcd(num, 3 den) the record's own, carried on the birth line; the loader refuses a poor birth cell (below 500 remainder values) and the retired keys `absorbing`, `take`, `emits`, `own_grace`, `wheel`, `residue_order`, `residue_seed` by name; the take's data structures removed from the engine; every one-cell emitter on the rich well [801, 700] and every emitting body on [800, 801]; the worlds regenerated (BUILD.md section 26 item 15). The increment ladder (ALGEBRA.md 9.25 (2), the cumulative sums withdrawn): the record's running total over its ladder's cells against its threshold fixed at birth, the click at the first crossing at the cell whose segment of that interval's increment holds the threshold (Born's rule its theorem); a detector is one connected region (9.25 (7), refused on disconnected pieces); the same input gives the same output (the property test's test 8, two runs and two processes byte for byte); a Port only where the neighbour is of another set (a Link inside one set carries no offer); a body that births needs its seed as the composed mode's profile (BUILD.md section 26 item 16). No table in the engine: the born pair the world's two integers `born` [now, before] (the generator's, checked at load), the cosine and sine tables and the phase reading gone from the engine (the phase reading a host reader); the tables retired (the table body, the splitter, the joint weights), a measured event with a table refused under the detector law; the worlds regenerated (BUILD.md section 26 item 17). The detector cube (the model owner's decisions of 2026-09-25, record 1899; ALGEBRA.md 9.25): a detector is one region, a cube of side 3 or more, its sensitivity its whole cube read as the flux into it through its Ports from outside, the click the detector's and never a Node's; the loader refuses a detector below side 3 naming its sides (cut by the GameBoard on a thin axis), a set that fills no box, and a disconnected set; a set bound to a block is the block's cells (side 3 or more) or a cube of free Nodes beside it; the worlds and the line's test worlds on cube detectors (the two slits' screen 67 cubes, the matter waves' 41); the Malus four held as written (BUILD.md section 26 item 18). The emitter's coupling and the residue's read point (ALGEBRA.md 9.19 (4e), the mathematician's answers to item 15's findings): every emitting body declares (g, G) for its born family, both nonzero, refused absent (the born records act back on the excited record's rows through g and spread its residues); the excited record's residue and wheel are read from its own remainder at the centre cell after its first advance, the offer counting from that interval; the worlds regenerated with the coupling on every emitting body (BUILD.md section 26 item 19). The input checked lawful or refused in integers (the model owner's record 1886; ALGEBRA.md 9.22 (7)): every seeded body's profile carries its mode's clock `clock` [a, b] (the generator's rational for 2 cos omega, b at least twice the amplitude), and the loader checks at load, in Python integers with no float, the eigen-equation's residual at every Node within the proved bound on the family's composed operator (outside the other bodies' cells), the clock above the band's top and below 2, the bodies whole and disjoint, at most three families; the generator's mode is now ARPACK's (scipy's `eigsh`, a declared dependency of the diagnostics and the generator, never of the engine) after the check found the Lanczos profiles off the mode by up to 3 x 10^-4 (hundreds of units at 50 x 2^20); every world regenerated; `tests/test_initial_state.py` (BUILD.md section 26 item 20). The input stamp, the integer generator and the one command (records 1886, 1898 and 1887): every seeded world carries `input` {law, hash}, the law identifier and the SHA-256 of its profiles, clocks and born pairs, checked at load (a stamp missing, under another law, or not the digest of the integers refused); the power iteration in integers with the remainder kept and shifted (`integer_mode_iteration`, bit for bit reproducible, its floor about 1 / gap units at the amplitude read against ARPACK); `tools/run_inputs.py`, input files in and one output file per experiment out, each in its own process, LAWFUL or REFUSED at load, the clicks per detector and the registered pin's verdict, no time in the output so runs together equal runs alone; `tests/test_run_inputs.py` (BUILD.md section 26 item 21). The light clock in the table's form (ALGEBRA.md 9.22 (8) row 13: the chain of 674 with the face receivers and the mirror as a gap of light's kind) run by the one command against its registered pin (`examples/events/pins.json`, a pin on a count or on a detector's first click): MISS, the first click at 76 against 214, and the fault found for the mathematician: the born pulse of one pair per cell is broadband and dispersive, so the one-way flux a receiver books exceeds the record's energy (2.6 times on a passage, 4.65 times beside the emitter) and the ladder is met by sloshing, not by the record's passage; no pin moved; the travelling born profile is the remedy (BUILD.md section 26 item 22). Bodies with extents and the face slab (ALGEBRA.md 9.22 (8), 9.25 (10)): a block is the box of `extents` [x, y, z] per axis (`side` the cube's shorthand), placed whole and checked per axis, its centre cell the box's; the world key `face_depth` makes the face receiver at every open border a slab of that depth, one cell, last on every ladder (a packet books more than 0.9 of its energy into a slab of its depth, less than 0.5 into a face one Node deep); `tests/test_extents_and_face_slab.py` (BUILD.md section 26 item 23).

- The click's cost, the detectors' inflow read at the Ports alone (the model owner's record 1934; BUILD.md section 26 item 26): `detector_inflow_tally` reads a record's two levels at the Port pairs listed once per family (`_inflow_ports`), the same integers as the board-wide reading bit for bit; the board-wide `flux_offer` retired; the cost printed as HOST (4 Ports of 80 Nodes on the emitter chain, 40 of 216 on the detector-law layer; `tests/test_flux_reading.py`).

- The registered worlds named by their experiments (the model owner's rule, record 1924; the names review, record 1925): every world of `examples/events/massive_record/` renamed to its canonical name with the drive's speed as a fraction of a Link per interval and `at_rest` (the migration table in that folder's README; the identities follow the names, the files regenerated with the same integers); the light clock's set `at_well`, Sagnac's `at_near_well` and `at_far_well`; the pins file's key `light_clock`; the readers, the pins and the readings on the new keys; the run list marked history with the canonical names; the code's constants, comments, refusal messages and 72 test names named (the directional drive's identity, the amplitude series' detectors and the other series' family letters left, with the reason, to their own renames).

- The generator as the board's own operator iterated in integers, with the stop (the model owner's word of 2026-09-25, 04:10Z, closing record 1898; BUILD.md section 26 item 25): `iterated_mode` in the margin module iterates 3 den v' = num S_6(v) + 6 den v + r from the cells' indicator, reads the clock as the operator's quotient over the whole board, and stops at the first iteration at which the scaled profile passes the loader's own residual bound, iterating at 2^20 or the declared amplitude, whichever is larger (`_operator_step` the one copy of the step; `integer_mode_iteration` its fixed-count diagnostic; `clock_denominator`); the massive record generator's `mode_profile` and every seeded test world use it; the host's eigensolver (`accurate_mode`, ARPACK) stays a diagnostic, `mode_clock` retired; every seeded world regenerated (the generator test of `tests/test_initial_state.py`). The build order's letter-and-number codes retired from the documents by the owner's rule of the same minute: bodies with extents, the travelling born profile, the face slab, packets with momentum and the moving name, the polariser's axis and the crystal.

- The click rule of ALGEBRA.md 9.17 (7) (f) in the engine (the model owner's word, record 1918; BUILD.md section 26 item 24): the excited record's running total accrues each interval its centre cell's share of its conserved form (`form_share`; `conserved_form` its sum over the board) in place of the one-way flux there, the norm one period's action P e_c (the generator's `norm`, the share summed over `period` intervals of the mode advanced alone; admitted up to 2^126, `NORM_BOUND`), the rung and the residue's read point unchanged; every emitter body seeded at 2^20 (the born light's back-action swamps a seed of 100, 9.17 (7) (c)); every world with an emitter regenerated; the six births of the emitter world at (2 u + 1) P / (2 W) after their reads within two intervals (`tests/test_emitter.py`); the chain digests' events and audit moved once.

- The emitter's norm as the one-way flux into its centre cell over one period of its mode (ALGEBRA.md 9.17 (5) item 1 in the flux's units of 9.19 (3); BUILD.md section 26 item 13): the generator's integers `period` and `norm` on every emitter body, recomputed at load and a mismatch refused; the write on the circle of 2 N with before = -now (9.17 (6)); the `born` profile as material (9.17 (5) item 3); the driven mask with no branch on the kind; the composed operator's stability condition at load (9.19 (2)); the flux reading's integers (`inward_flux`, `flux_offer`, `conserved_form`) checked on the board with planted values against the rule (`tests/test_flux_reading.py`); the Malus bar's ticks 3800.

- The lamp retired under the detector law (BUILD.md section 26 items 7 to 12): `lamp`, `emits` and `own_grace` refused at load, the grace, the exemption, the emitter's own take, the cycle births and the coupling's source term retired from the engine; every world of the run list regenerated onto emitter bodies of the kind [7, 8] with the well [8, 7] seeded on their modes (the massive worlds' family `source`; the four Bell worlds held in `docs/designs/detector_law/held_worlds/` until the crystal); the margin module refuses a RUNAWAY well (the largest eigenvalue at or above 2: the deep wells of the first smoke runs, their cadences withdrawn) and skips an axis the body spans; content found on a take Node is taken as the hop rule takes an entered Node's content (the self-click of a set at its own emitter's cells); the tests rewritten onto the emitter, every reading in them the engine's on this head (COMPUTATION); the one-cell birth's character (a velocity impulse: a static level between two fronts for light's kind, a standing part for a massive kind) named for the mathematician's gate with the line's per-Link pair owed.

- The emitter as a clicking body (ALGEBRA.md 9.17 (4), the mathematician's integers; LAB_TOOLS.md A.1): the key `emitter` on a body of a massive kind with its seed and a stock `amount`: its excited records in turn (the seed at both levels, the residue from the emitter's wheel), each clicking at its own rung on its own cells (2 T u + T <= 2 W C on its own booked motion), X ending it and E^T writing the photon once at both levels (now = A C[phase(0)], before = A C[phase(-1)]), the next excited record while the stock lasts; no rate, no drive, no source term, no grace, no own take. `tests/test_emitter.py`; BUILD.md section 26. The lamp and the cycle emitter stay loadable until the worlds are regenerated (the next push of the same line).

- The polariser (a table body of two cells) splits a record's offer by the record's own state: the channel pointers J(o) from the record's label weights and the half-angle pair (`joint_weights` with one body), the weights J^2; before, the split read the setting alone and a record on label 1 or a superposition was split as label 0 (Reviewer 3's bug line, 2026-09-24). Malus's four counts unchanged; tests d2 and d3 in `tests/test_detector_law_tables.py`.

- The body's conditions exact in the initial state, checked at load (the model owner's word of 2026-09-24, 16:48Z): the loader refuses a body that does not lie whole on the board (`_body_fit_check`; before, the cube was cut to the board silently); the margin module's `check_body_conditions`, called by the runner and by `tools/preflight_worlds.py` on the engine as constructed, recomputes every bound body's mode as an integer profile and refuses a world whose body's own record differs from it at either level on any Node, naming the Node, and refuses a pushed body whose `ramp` is below ten relaxation times of its own well; `tests/test_body_conditions.py`. The massive generator's `seed_on_the_mode` seeds every bound body on its mode at the declared amplitude (the deep well, the boxes, the light clock, sagnac and redshift regenerated; the flat seed history) and the layer pin worlds carry the ramp 12000 with ticks 20500, so every listed massive world loads clean under the check (DECLARATIONS.md section 15 M1-11).
- The World Generator writes the three declared world forms (2026-09-24, the one list): `two_slits.json` in L-3's second draft (160 x 256 with x and y open, d = 26, L = 113, the openings of width 3, the lamp's `receiver` the 201 screen sets with the rung wheel 2^20, the wheel [1, 1024], 5500 intervals); the four Malus worlds on the bar of 8 without the which-path read body and its set; `matter_waves_{12,16}.json` in section 12's sized form (the wheel [1, 2048] at one per 2, the lamp's `receiver` the 121 screen sets with the rung wheel 65536, 4700 intervals); `RECEIVER_KEY` on, so every emitting block's `receiver` comes from the generator (the redshift, sagnac and light clock files unchanged by it).

- detector-law-v1: a lamp's `receiver`, its records' ladder by name (the named detector sets; every other set and every face a sink, taken and booked but never chosen), the cell of u over the ladder's own sum; the gather line's `ladder` and `sunk` fields (SIZING.md; BUILD.md section 20).

### flow-link-v1 under its key, and the split ladder of the pushed row's wall (2026-09-22)

- The world key `flow_link` (off by default; the model owner's decision of
  record 915): every flow sum counts an arriving row with the flow label per
  Euclidean Link (`nature_beam.flow_label`), the ring worlds of
  `examples/events/flow_link/` with their pins before the run and the run's
  record. The pushed row's wall T(P) by the split ladder
  (`nature_beam.split_ladder`, the physics-rule reviewer's route (b)): the
  wall's square X = R^2 + 3 |P|^2 bounded, X Q^2 never formed, the same floor
  as the root; the three crowd clocks' worlds that refused at the working
  bound under the generic entry (series T, U and V, eleven worlds) run under
  the split ladder since 89f43572, their readings a record in their
  registers (`read_under_the_split_ladder_89f43572`), no pin.

### The generic entry of the bending: the row's flight in the age wall's set for every world (2026-09-22)

- The model owner's word (record 847, "do not freeze; bring it back
  immediately", then "implement it, now"): the row's flight is a member of
  the age wall's declared set for every world at the coefficient 1 + gamma,
  gamma the world key `optical`'s declared value and 0 by default (the time
  part alone, the law's own number; nature's 1 a declaration per world and
  never a default), the same one wall function that slows a body's clock
  in a crowd delaying and bending every family's rows (`measured.age_wall_set`
  with no None state, `world.NatureBeamWorld.optical` an integer,
  `nature_beam` acting in every world, `run.json` carrying `optical` for
  every world). `optical-v1` names no hypothesis any more. The three load
  refusals of the key are lifted (at suspension 0 nothing is stretched and
  nothing pushed; under `meeting` the meeting's turn keeps the heading; a
  heading without a neighbour turns to nothing); the inverse interval is
  refused at a pair with n > 0 only. The snapshot writes a row's flight
  accumulator only where a crowd moved it off the table's own count at its
  age (the value the walk seeds from), so every world in which no crowd
  acts keeps its record and its state byte for byte (the crowd worlds at
  [0, d] and every crowd-free world; `tests/test_optical.py` (e), the gate
  set's digests). The registered crowd worlds at a pair with n > 0 read
  the light stretched by their crowd's age moment as their clocks are (at
  their declared inputs the light freezes in the mass rows and one world
  refuses on the pushed momentum's square); the model owner's word of
  record 871: they are not needed and not in the paper, the Register
  Architect's to remove after this entry merges; series T's four stay
  with NATURE row 12 and are redeclared in the weak field, the pins
  before any run (docs/designs/one_wall/EVERY_FAMILY.md section 6, step
  5; docs/designs/one_wall/GENERIC_BENDING_PRICE.md; ENGINE.md).
- Three rules the entry needed, found by the suites (the law acting where
  the key never did): the click's exact time is the count's own on a row
  no crowd moved and the accumulator's where one did
  in one form for every row, (age r - s + T d) / r with T the half wall
  of the row's present pair (`optical_last_link`, the walk's `last_link`;
  the reviewer's line on PR #855: the count's own floor on a row no crowd
  moved, by identity, and no row reads two forms; the amplitude worlds'
  clicks byte for byte); the pushed row's wall T(P) by a comparison ladder
  of squares in place of the root at run time (`square_ladder`, the same
  floor; the Register Architect's NODE_ALGEBRA.md section 2); a row whose direction a
  collision or the meeting changed reads its age on its present line, its
  accumulator reseeded from the table there (`nature_beam.reseed_flight`;
  the merge as without a crowd); the inverse interval at n = 0 returns
  the rows fresh, the store bit for bit. With `drive_b` (PR #813 merged
  in): the drive member at gamma, at gamma 0 declared at 0 and
  unstretched; a moving body's weight the pair under `drive_b` alone; a
  moving body at gamma > 0 without `drive_b` refused at load.
- The tests of the crowd worlds at a pair with n > 0 record what the law
  does with them as declared, the readings before the entry kept in the
  comments, nothing deleted or skipped: `crowd_clock` (5 of 8 refuse at
  interval 6; `still_1`'s presence 190 F), `clock_word` (all 4 refuse at
  6 or 11), `cluster_clock` (both refuse at 6), `reader_clock` (the
  presences 3.5 times), the step drive's (g) (its deuteron world at d =
  2^27 with a light lamp refuses at interval 4; the bound pair read on
  the same world without the light), and the gate set's `weak/j3_deuteron`
  (refuses at interval 596 of its 700: the entry carries `refusal` beside
  its digests, read by `test_nature_beam_worlds`, `test_massive_rows` and
  `test_amplitude_click`). The weak register's `become` blocks of
  `j1_lattice`, `j1_source` and `j3_deuteron` (the warm run's count ranges
  and trigger ticks) move, their crowds' rows stretched by the other
  numbers' crowds: each keeps its registered block and carries
  `under_the_generic_entry`, the warm run under the law as it stands (a
  derivation, no pin), which `test_weak_readings` (e) reads; the paper's
  row 8a rests on J1's run, its standing the model owner's decision.
  `test_become` (c) and `test_clock_age` (d) read the law (the crowd's
  own rows stretched at a test world's pair [1, 128]; the flight a member
  for every world).

### Series L6, Bell at N = 2048, 8192 and 16384: the plateau of 24.4 measured (2026-09-22)

- Twelve worlds by the generator (`examples/events/amplitude/bell_n2048_*`,
  `bell_n8192_*`, `bell_n16384_*`: the registered Bell world of L6 with the
  one declared integer N changed), the pin per N written before the run
  from the closed form of DERIVATIONS_BEAM 24.4 (`expectations.json` under
  `bell_24_4`: S = 181 / 64 at 2048 and 8192, 5793 / 2048 at 16384, where
  the plateau ends), the runs and their replications in the register's
  block `run_2048_8192_16384` and the L6 entry, `tests/test_amplitude_bell_24_4.py`
  extended to the five N and the closed form. The worlds' duration is
  declared from the lamp's clock (BEAM_LAW note 41) where N + 20 intervals
  end before the wheel's last records gather (8221 at 8192, 16439 at
  16384; every registered world unchanged). No engine change.
### drive-b-v1, the directional drive of a body under its own key (2026-09-22)

- The world key `drive_b` (absent by default) and the identity `drive-b-v1`
  (the model owner's approval of form B, record 652; the design
  `docs/designs/drive_b/DESIGN.md`, form B in the integer form (c) of
  `light_speed/FORM.md` 3.1; BEAM_LAW note 49): a body's three drive
  accumulators gain p_a Q each against one wall Q^2 S M + |p|_1 T_h
  (`world.drive_wall`, T_h = 110 formed at load) and the axis furthest over
  the wall steps (`core.integer.by_line`), the Bresenham line of the
  momentum with no coincident fire lost; the one-axis refusals of
  `covariant_readings` lifted under the key. Series X
  (`examples/events/drive_b/`, six worlds by the generator, the pins before
  the runs, 19 readings inside); `tests/test_drive_b.py`; `plane_b` in the
  gate set. With the key absent every registered world reads as it did,
  byte for byte; nothing re-registered.

### Series L7, the cone: which length a row's phase counts (2026-09-20)

- Two worlds of one geometry under the amplitude law
  (`examples/events/amplitude/cone_links.json` and `cone_intervals.json`,
  by the generator; `expectations.json` under `cone`;
  `tests/test_amplitude_cone.py`; the register's L7 entry): a row on the
  heading +x and a row on the plane diagonal (1, 1, 0) reach counters at
  the same Euclidean distance at the same age (the flight table, 1 / sqrt 3
  in every direction); the integer form of `phase_per_link` turns the
  phase per Link stepped (51 and 8 at the two counters), the pair form per
  interval of age (23 and 23). No engine change.

### The verdicts of series D and H re-read under the step drive (2026-09-20)

- The physics-rule reviewer's re-read of the two registered verdict
  clauses the step drive overturned, added to the register as the next
  bullet of each series (nothing re-run, nothing tuned): series D's "no
  orbit closes by the criterion at any width or radius" is superseded
  (the S = 32 probe at r = 24 closes by the criterion, T 623 against the
  derived 687, the mean radius 23.63, C 1.37) and series H's "what the
  law lacked here is not the turn but a stable closed orbit under whole
  kicks" is superseded (`r8` closes four times and stays on the
  GameBoard, the phase's turn per orbit 0.75 to 0.83 against 0 and C(4)
  = 1.01 against 2.0: the orbit closes and is not quantised); the summary
  lines of PROJECT_STATUS, ENTITY_CATALOG and the examples READMEs
  replaced, the registered numbers kept as history
  ([D](docs/EXPERIMENTS.md#d-the-orbit-under-the-beam-law-on-the-plane-2026-09-19),
  [H](docs/EXPERIMENTS.md#h-bohrs-lines-behind-the-detector-2026-09-20)).

### The phase circle's bound raised to 65536 steps (2026-09-20)

- The model owner's instruction ("raise the bound"): the pair of
  `amplitude-v1` rotates its labels through the half-angle tables at 2N, so
  `core.phase.MAX_PHASE_STEPS` is 65536 (was 4096) and the world parser
  imports the one bound; N = 65536 is accepted with its tables (0.2 s once,
  every entry within 256), 131072 refused; the same change as commit
  7c147e9f of the paper's branch, applied here by hand.

### The `wave` threshold on the pointer's square; the escaped momentum per family (2026-09-20)

- The model owner's decision (issue #359 step A;
  [BEAM_LAW note 32](docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)):
  under `wave` a detector set's threshold reads the square of the
  coherent pointer of its arrivals in units of one ray (the nearest
  integer to (X^2 + Y^2) / 2^26; one unit at any phase 1, a rays in phase
  a^2, rays that cancel 0), so a pair in antiphase passes whether or not
  a window is declared; under `beam` the amount as before; no memory
  between intervals. Of the 66 example worlds 65 are byte-identical (the
  slits and the Bell ten among them, S = 2 exactly); A10's `w27_wave`
  alone changes (2312 antiphase pairs passing a pixel and going on) and
  is re-registered old against new. The escaped
  momentum is booked and reported per family (issues #360 and #361 item
  1): `run.json`'s `escaped` line per family carries the family's own
  momentum where the world's total was written into every line
  ([MIGRATION](docs/MIGRATION.md); `tests/test_nature_beam_detector.py`
  (i), `tests/test_nature_beam_books.py`).

### The columns of the one coupling, the lifetime, the held content and the contact through the table (2026-09-20)

- The model owner's decision ("one mechanism for all the laws on the
  GameBoard", [Highlights 5.4](docs/HIGHLIGHTS.md#54-the-detector); the
  mathematician's verified form, "correct and working";
  [BEAM_LAW note 31](docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)):
  the push a measured event takes from a free family's rays is a signed
  inner product over the columns the families declare per unit of
  content, every column the whole part off the reader's clock of V x
  (the reader's charge in the column, read at the frame from what it
  holds) x (the arriving family's value), floored on its own; `gravity`
  the built-in first column of every family (the value [1, 1], the sign
  minus), `charge` the built-in second (the sign plus, the family key
  `charge` its value), and per family `columns` (`{"<name>": {"value":
  n or [n, d], "sign": 1 or -1}}`) for any further column, one sign per
  name across the world, [0, 1] where a family names none, 0 on a paid
  family, 8 at most. The two built-in columns are the form landed the
  same day integer by integer (the 66 example worlds' `events.jsonl`
  byte-identical; the series 7 `read` records replayed). The products
  are tested by division before they are formed and the partial sum is
  bounded after every column; the parser refuses at load a reader whose
  push over a column from the largest release of a family could pass the
  bound. `run.json` carries the world's `columns`, every family's aligned
  `columns` and `columns-v1` under `hypotheses` when a column beyond
  `charge` is declared; the states carry `charges` by column. The strong
  force is a column with the sign minus, no code of its own
  ([MIGRATION](docs/MIGRATION.md); `tests/test_columns.py`).
- The lifetime and the held content (the model owner, 2026-09-20, "the
  strong force's range is a lifetime, L: the event whose age reaches L
  makes no next event but an escape click in the ledger, as at an open
  face"; the physicist's D-1;
  [BEAM_LAW note 31](docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)
  (vii) and (viii)): per family `lifetime` (an integer L from 1, one
  scalar; absent, forever): a ray whose age reaches L at the end of its
  walk, after that interval's reads and before the merge, clicks on the
  border `lifetime`, a detector without Nodes listed after the faces,
  booked exactly as an open face books an escape (the ledger's lifetime
  lines summed into the escaped lines, one `click` record per row naming
  the border); refused beyond `age_bound`, a declared ray at or beyond it
  refused, the inverse interval refused with such a family; the reach the
  flight table's (L = 1 the six neighbours, 2 the face diagonals, 3 the
  cube diagonals and two Links). Per measured event `held` (family name
  to content): the content the sum, the charge in every column the
  rational sum over what is held, every free family held released beside
  the own. `run.json` carries `lifetime` per family, the border among the
  `detectors` and `columns-v1` under `hypotheses` when a lifetime is
  declared. No existing world changes ([MIGRATION](docs/MIGRATION.md);
  `tests/test_lifetime.py`).
- The contact through the table (the model owner, 2026-09-20, on the
  physicist's design of the strong force, section 4.4;
  [BEAM_LAW note 31](docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)
  (ix)): a body whose step on an axis is refused because the destination
  holds another measured event has arrived at that occupant, and the
  occupant's table entry for the body's family decides as it decides for
  a ray: `measure` (the rule wherever the entry is the keys' own for the
  body's family, declared or not: a paid arrival, the body's momentum its
  own label) hands the body's momentum component on that axis to the
  occupant, the sum unchanged; `rerelease` returns it; `pass` and a
  `read` declared against the keys leave the labels as they were (the
  rule until now, under which a bound pair's labels grew without bound); a
  body on a set hands the component apportioned whole over the occupants
  of its destination set by their contents; one `contact` record per
  hand-over, `contacts` on the occupant's state. No key. Of the 66
  example worlds 60 are byte-identical; the coupling `1b_*`, Bohr `r2`
  and `r4` and the orbit `s8_r12` change from the first refused step of
  a body and are registered old against new
  ([VALIDATION](docs/VALIDATION.md); [MIGRATION](docs/MIGRATION.md);
  `tests/test_contact.py`).

### The names NatureBeam and GameBoard and the glossary's single names (2026-09-20)

- The model owner's names, a mechanical rename with no behaviour change
  ([MIGRATION.md](docs/MIGRATION.md), "The names NatureBeam and GameBoard
  and the glossary's single names"): the law's things are `NatureBeam*`
  in the code (`NatureBeamWorld`, `NatureBeamSimulation`,
  `NatureBeamStore`, `NatureBeamTables`, `parse_nature_beam_world`,
  `execute_nature_beam_run`, `is_nature_beam_world`,
  `nature_beam_tables`; `tests/test_nature_beam_*.py`;
  `tools/migrate_nature_beam_worlds.py`); the physical lattice of Nodes
  is the GameBoard everywhere (`src/event_universe/core/game_board.py`,
  the canonical entry in [TERMINOLOGY.md](docs/TERMINOLOGY.md), the rule
  in AGENTS.md, every message and document); and the 23 redundancies of
  Highlights 5.6 take their single names in the code (`Moments`,
  `GameBoardDiagnostics`, `presence`, `flow`, `arrived`, `NO_ARRIVAL`,
  `TALLIES`, `DOCUMENT_KINDS`, `resolution`, `turned`, `K`,
  `face_amount`, `escaped_amount`, `clicks`, `taken`) with every
  world-file and run-record key deferred. Every integer is unchanged;
  the tests pass with the same bodies.
- The Beam Law (the model owner, 2026-09-20): the law itself is renamed
  from "the law of the ray". `docs/RAY_LAW.md` -> [`docs/BEAM_LAW.md`](docs/BEAM_LAW.md)
  (the anchors unchanged; nothing stays at the old path); "the law of
  the ray" -> "the Beam Law" in every live
  document, skill, README, example, tool, test and docstring; the
  identity `RAYS_LAW = "rays-v1"` -> `BEAM_LAW = "beam-v1"` and the world
  key `"law": "rays"` -> `"law": "beam"`, every world file rewritten by
  `tools/migrate_nature_beam_worlds.py` (extended), the parser refusing
  the old value naming the migration, the preflight's kind `beam`;
  `run.json` records `beam-v1`; the registered runs' records stay as
  they were (rays-v1 is beam-v1, the same law); `bohr-v1` untouched; the
  prose word "ray" stays the informal name, the documents' first mentions
  say "beam (the record of an event in transit)".

### The catalog of the entities (2026-09-20)

- The model owner's decision ("Make sure that every entity the world of
  physics knows exists in our entity definitions, and that we can also
  support external ones such as the sun, a planet, a neutron star, so that
  they can be placed on the GameBoard and things tested";
  [Highlights 5.4](docs/HIGHLIGHTS.md#54-the-detector)):
  [the catalog of the entities](docs/ENTITY_CATALOG.md), every entity
  physics knows as one row of the law's keys as `world.py` accepts them
  today (the fundamental things, the composites, the external things),
  each with the world file that places it, the rows that wait for the
  changes in flight marked by the names their designs give them (the
  strong column, `lifetime`, the held content, the contact, `become`,
  `phase_width`, D-1, a hand), the gap list (colour and
  confinement, the Higgs, a black hole as the integer bound or as a body
  whose clock the crowd stops, antimatter, spin, molecules, dark matter and
  dark energy, light in a field) and the architect's judgements on what
  could not be placed. Four placement worlds under
  `examples/events/catalog/` written by `make_worlds.py`: `sun_planet`,
  `neutron_star`, `lamp_mirror_screen`, `clock_near_mass`, each parsing and
  running 40 to 50 intervals headless with the books balanced;
  `tests/test_entity_catalog.py` checks each is what its page says and
  pins no number ([expectations](docs/TEST_EXPECTATIONS.md#the-entity-catalog));
  [entity definitions](docs/ENTITY_DEFINITIONS.md) stays the owner of the
  definitions layer and links the catalog.


### Series G, the Hubble diagram behind the detector (2026-09-20)

- The four worlds of `examples/events/hubble/` (`make_worlds.py`: a
  301^3 cube, twenty-four thrown sources at 0.05 c to 0.6 c, a `wave`
  detector at the centre reading the age, six masses inside; a coasting
  and a pushing crowd, each with `scalar` and `age` clocks), the readings
  tool `tools/hubble_readings.py` (the redshift from the pointer's turn,
  the distance from the arrivals' ages, the fits against the coasting,
  decelerating and accelerating forms, every line labelled a detector or
  a GameBoard reading) and its test `tests/test_hubble_readings.py`; the
  register entry G in [EXPERIMENTS.md](docs/EXPERIMENTS.md) and the
  evidence in [VALIDATION.md](docs/VALIDATION.md). No law changed; the
  findings for the law (a diagonal throw is not straight, a beam's push
  does not dilute, a source stepping into its own row takes it home) are
  registered there.

### Series H, Bohr's lines behind the detector (2026-09-20)

- The run of the model owner's decision on Bohr ([EXPERIMENTS.md](docs/EXPERIMENTS.md),
  "H, Bohr's lines behind the detector"; `examples/events/bohr/`,
  `tools/bohr_readings.py`, `tests/test_bohr_readings.py`): a fixed proton
  releasing the physicist's fan of 2616 directions, an electron that is a
  body on three Nodes turning its phase by its momentum, its released rays
  read at the open faces as the `wave` detectors of what comes out of the
  atom; the orbit, the phase's turn per orbit and the faces' coherent
  record per turn and cumulatively, every line labelled DETECTOR or
  GAMEBOARD. Measured: no orbit closed well enough for the coherence
  reading (the reference orbit at r = 8 held its mean radius for two
  eccentric turns and was thrown out at a close pass; C(2) = 0.84 against
  the expected 1.0), registered as the finding, nothing tuned; the next
  steps (a smoother field, a tilted orbit, a wider body, the absorption
  reading with a lamp) are in the register ([validation](docs/VALIDATION.md)).

### The turn by momentum: Bohr as parameters outside the board (2026-09-20)

- The model owner's decision ("On Bohr, go, and put it as parameters
  outside the board like the age"; [Highlights 5.4](docs/HIGHLIGHTS.md#54-the-detector);
  [RAY_LAW note 30 (ii)](docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)):
  the world key `action` (h, an integer from 1, absent by default) and
  the measured-event key `phase_by_momentum` (false by default): at the
  Link a body steps on an axis whose momentum component is p, its phase
  turns by `by_clock(k0, |p| x N, h)`, the difference of two floors of
  k x |p| x N / h with k0 the count of Links the step rule gives at its
  age (derived from the age as the owed count is read off the clock; no
  register, no remainder), so that after k Links at a constant momentum
  the phase has turned floor(k x |p| x N / h) mod N; the axes compose,
  x before y before z; the product is bounded at parsing (`ticks x |p|
  x N`) and before it is formed. A rule of the measured event, the
  external thing, read from its own record: the rays' flight and
  collision are untouched (`test_ray_body` (e)), the rays a body releases
  carry its phase as before, and without `action` every world reads the
  same integer by integer. The identity `bohr-v1` is carried under
  `hypotheses` in `run.json` when `action` is declared; the `step` line
  gains the body's `phase`. Tests: `test_ray_body` (d) to (f)
  ([expectations](docs/TEST_EXPECTATIONS.md#a-body-on-a-set-and-the-turn-by-momentum),
  [migration](docs/MIGRATION.md#the-turn-by-momentum-bohr-as-parameters-outside-the-board-on-2026-09-20-action-phase_by_momentum-bohr-v1)).
  The run that reads Bohr's lines behind the detector is series H
  ([EXPERIMENTS.md](docs/EXPERIMENTS.md)).

### A body on a set of Nodes with one record (2026-09-20)

- The model owner's decision on Bohr, the body on a set taken with it as
  the condition for a closed orbit (the physicist's proposal 1, "the
  electron of width 3"; [Highlights 5.4](docs/HIGHLIGHTS.md#54-the-detector);
  [RAY_LAW note 30](docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)):
  the measured-event key `span` (three odd integers from 1, `[1, 1, 1]`
  by default) makes a measured event a body on the block of Nodes centred
  on its `position`, one record on all of them: the threshold, the
  clock's count and the push read the one reading set summed over its
  Nodes, the releases are apportioned whole over the set (the leftover to
  the Nodes from `age mod w`, the total the content's whatever the
  width), the step moves the whole set as one (refused when a Node of the
  moved set holds another measured event, the whole body clicking on the
  face when any Node would leave, every Node wrapping on a periodic axis),
  no collision acts at any of its Nodes. A set of one Node is the measured
  event as it was, bit for bit. `engine.step_axis` and `engine.count_owed`
  hold the step rule of one axis and the owed count once, for the tools.
  Tests: `test_ray_body` (a) to (c), (f)
  ([expectations](docs/TEST_EXPECTATIONS.md#a-body-on-a-set-and-the-turn-by-momentum),
  [migration](docs/MIGRATION.md#a-body-on-a-set-of-nodes-with-one-record-on-2026-09-20-span)).

### `wave` is the default reading of a detector (2026-09-20)

- The model owner's decision ("on the board a ray, in the world a
  wave"): `world.DETECTOR_READINGS` = ("wave", "beam"); a detector
  without a `reading` and every measured event outside a declared
  detector read `wave`, `beam` is declared ([RAY_LAW section 5](docs/BEAM_LAW.md#5-the-detectors-record-the-re-emission-the-face-detectors)
  and note 29; [migration](docs/MIGRATION.md#wave-is-the-default-reading-of-a-detector-on-2026-09-20)).
  Re-pinned: `test_ray_readings` (d) (the window reads the set's phase:
  2 units at phase 0 and 1 at 32 all pass the window 32; the `beam`
  variant kept beside it), `test_ray_collision` (d) declares `beam` on
  its windowed taker. Unchanged: the Bell worlds (S = 2, 326 criteria
  through `tools/bell_chsh.py`), the two-slit and Heisenberg worlds
  (declared), series C and D.

### Charge per unit of content; the push one product; the record's two columns gone (2026-09-20)

- The model owner's decision (Highlights 5.4): the family key `charge` is
  the charge per unit of content, rho, an integer or a pair `[n, d]`; a
  measured event's charge is rho x its content (a report, the pair) and
  the per-event `charge` is refused naming MIGRATION. The push is ONE
  product per arriving free ray, `push_A = M_A x (rho_A rho_B - 1) x V_B`
  (`nature_beam.push_form`, the function five documents named), the
  electric part off the reader's clock by the declared pairs, equal
  integer by integer to the earlier `q_A q_B / M_B` form on every series
  7 world (the six worlds' `read` records, `pushed` and momenta equal;
  [validation](docs/VALIDATION.md)); the record loses `charge` and `mass`
  (the family suffices), and the architect's B2 (a re-emitted free ray
  of another family stamped with a mass of 0, a charged reader dividing
  by it) cannot arise: a re-emitted ray is its family's ray with the
  re-emitter's number (the orchestrator's D2). The series 7 worlds
  declare two free families with their pairs (`q` [±1, 2] on the source,
  `p` [±2, 1] on the probe, [1, 2] on the content-4 probe);
  `tools/migrate_ray_worlds.py` converts a per-event charge to the pair
  and refuses a family whose events imply two. A detector named as a
  face detector is (`face:+x` and the five others) is refused;
  `FACE_NAMES` moves to `events/world.py`; the re-exports
  `engine.by_clock` and `engine.FACE_NAMES` are gone (A11); one
  materialization of a ray's record, `RayStore.rows` and
  `NatureBeam.record`, writes `state.json` (A3) ([RAY_LAW section 2](docs/BEAM_LAW.md#2-the-record-of-a-ray-and-the-world-file),
  step 4 and note 28; [migration](docs/MIGRATION.md#charge-per-unit-of-content-on-2026-09-20-the-familys-charge-a-pair-no-charge-on-a-measured-event-the-records-two-columns-gone);
  [expectations](docs/TEST_EXPECTATIONS.md#the-push-as-one-form): (a) to
  (e), (i) re-fixtured with the same integers, (k) and (l) added).

### The push reads the content the frame read (2026-09-20)

- The architect's B3 (blocking): the gravity push read the reader's
  content inside step 4's per-family loop, after earlier families' clicks
  had joined it, so the world file's family order changed the integers.
  The orchestrator's D1: M_A is the content the frame read at the start
  of the interval (`Measured.frame_content`, set once in `_frame_all`
  beside the clock's age and turn) and the push reads it for every
  family's rays ([RAY_LAW step 4](docs/BEAM_LAW.md#3-the-nodes-interval-nature_beam)
  and note 27; [ENGINE](docs/ENGINE.md)). Test: `test_ray_push` (j), the
  architect's probe world in both family orders reads the same integers;
  no registered pin moves ([expectations](docs/TEST_EXPECTATIONS.md#the-push-as-one-form)).

### The label's product checked before it is formed (2026-09-20)

- The architect's B1 (blocking): the born labels' product was formed in
  int64 and checked after, so a wrap inside the bound passed silently
  with the books balanced at the wrong integer. Now every label the law
  forms is checked per row before the product, the weight times the
  largest component of the row's u_d within 2^62 - 1
  (`nature_beam.label_overflow_rows`, inside `momentum_labels` and, in
  bulk, `first_label_overflow`), the post-check at the births is deleted
  and the refusal names the Node and the amount ([RAY_LAW section 2](docs/BEAM_LAW.md#2-the-record-of-a-ray-and-the-world-file)
  and note 26). The check is exact per direction: a merged row of weight
  2^56 on (1, 1, 0) is accepted (45 x 2^56 fits) where a heading's is
  refused. Re-pinned: `test_ray_label` (c) (`label_weights` no longer
  bounds by Q; the label does); added (d), the probe's world through a
  merge and through a mirror ([expectations](docs/TEST_EXPECTATIONS.md#the-label-along-the-unit-vector)).

### The age of a ray kept whole and read by the measured event (2026-09-20)

- The model owner's "go for it" on the clock beside a mass (2026-09-19,
  [Highlights 5.4](docs/HIGHLIGHTS.md#54-the-detector); [RAY_LAW section 10](docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation),
  note 25): the ray's age, the count of intervals since the measured event
  that created it, is kept whole on the record (the flight reads it modulo
  the direction's period, the collision never; the board's step is
  unchanged, `tests/test_ray_age.py` (e)); the one reading gains the age
  moment `sum amount x age` (`Reading.age`, `reads: "age"`), a reading aid
  of the measured event, the external thing; the clock of a table entry
  that reads `age` counts it in place of the presence
  (`measured.count_component`, `Measured.counted`), so a clock beside a
  mass reads (M / r^2) x r = M / r in space while the push keeps reading
  the flow, M / r^2 (Einstein's pair from two readings of the same rays);
  the world key `age_bound` bounds the age (twice the flight bound by
  default on a board with an open axis, required on a board periodic on
  every axis; a ray beyond it refuses the run, nothing on the board
  changed). Every world without the key reads the same integer by integer;
  the all-periodic test worlds declare the key. Tests: `test_ray_age` (a)
  to (e) ([expectations](docs/TEST_EXPECTATIONS.md#the-age),
  [migration](docs/MIGRATION.md#the-age-of-a-ray-kept-whole-and-read-by-the-measured-event-on-2026-09-20)).
  The experiment in space is series E ([EXPERIMENTS.md](docs/EXPERIMENTS.md)).
### The label along the unit vector of the direction (2026-09-19)

- The momentum label of a ray is along the unit vector u_d of its
  direction at the flight table's scale Q = 64, the integer vector
  nearest Q D / |D| computed once in the world's direction table by the
  physics-rule reviewer's exact integer rule (`nature_beam.unit_label`,
  the flight table's `labels`), in place of the integer direction D whose
  length grew with the declaration ([RAY_LAW section 2](docs/BEAM_LAW.md#2-the-record-of-a-ray-and-the-world-file)
  and [note 23](docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation);
  the model owner, "go for it", on the reviewer's verdict: the D-label was
  the right direction and the wrong magnitude). Every unit carries one
  length of momentum, Q per unit of weight, for every direction within
  1.35 %, exactly Q e_d on a heading; every conservation stays exact.
  The four corrections of the verdict are implemented: the rounding rule
  in integers only; the step rule `by_clock(age, |p|, Q x S x M + |p|)`
  (`_move`, every registered step bit-identical); the parser's and
  `label_weights`' bound at Q x content x amount <= 2^62 - 1, refused
  loudly with the number; the reading's vector and tensor moments on u_d
  (a fan's flow reads Q x q direction-blind). Every momentum of a world
  file and of the record is now in label units, x 64 for a heading
  ([migration](docs/MIGRATION.md#the-label-along-the-unit-vector-of-the-direction-on-2026-09-19-the-momentum-units-change-by-q--64)).
  Re-registered: series C (every push and momentum x 64 exactly, the
  tool dividing by Q where it compares with q; 392 criteria, 0 failed,
  19 readings inside and 9 outside as before), Bell (unchanged, S = 2,
  326 criteria) and series D re-derived with L = 1 in label units under
  the Q S M rule and re-run (p = 3, 5, 9 units of the probe's content,
  192, 320, 576 in label units; no orbit closes by the criterion, the
  S = 32 probes now bound for many turns; [EXPERIMENTS](docs/EXPERIMENTS.md#d-the-orbit-under-the-beam-law-on-the-plane-2026-09-19),
  [validation](docs/VALIDATION.md)). Tests: `test_ray_label` (new),
  `test_ray_readings` (f), every momentum pin x 64 (the fan fixtures on
  u_d), the bound-edge worlds at 1/64 of their amounts, the detector's
  beyond-register row 2^52 -> 2^49 ([expectations](docs/TEST_EXPECTATIONS.md)).
### The Heisenberg run A10 registered (2026-09-20)

- `examples/events/heisenberg/` (eight worlds by `make_worlds.py`: one
  opening of width 1, 3, 9 or 27 Nodes declared as one detector, a plane
  wave on it, a screen of one-Node pixels 108 Links behind it, under the
  readings `wave` and `beam`), `tools/heisenberg_readings.py` and the
  register entry
  [A10](docs/EXPERIMENTS.md#a10-the-width-of-an-opening-and-the-spread-behind-it-under-the-beam-law-2026-09-20):
  the `wave` record narrows with the width and the count does not; the
  product w x FWHM reaches 0.886 lambda within 22 % at w = 27 and is not
  read at the smaller widths on the sparse fan; `beam` gives no bound
  ([validation](docs/VALIDATION.md)). A research run, pinned by no test.

### The detector as a set with one record, its two readings and the phase returned (2026-09-19)

- The model owner's principle of the detector's sensitivity ("a detector
  measuring three Nodes sees one electron that can be on any of the
  three"): a detector is a set of Nodes with ONE record. The threshold is
  on the amount arriving over the whole set in one interval, the coherent
  pointer and its squared record are over the set (one `record` line per
  detector naming it, its `node` None for a set of several Nodes), the
  window reads the set's phase; the click's content, momentum and
  re-emission stay at the Node the ray reached. After a click the set's
  phase (the pointer's nearest step, `nature_beam.pointer_phases`) is
  returned to every measured event of the set, so a lamp or a re-emitter
  releases at the phase it received, the frame's turn added after it. A
  detector declares its `reading`: `wave` (the coherent pointer, the
  square, the phase returned: the one imported law of physics, kept as an
  option) or `beam` (the default; the owner's "only events": the rays
  that would click are paired by opposite phase over the set, a paired
  couple passes on whole, the rest click, the record the count).
  `Measured.record` is gone (`DetectorSet.record`, `run.json`'s
  `detectors[]` with `reading` and `phase`; no `measured[].record`). The
  two-slit worlds declare their screen as 121 one-Node `wave` detectors
  (their record per pixel and the pinned correlation unchanged); the Bell
  worlds read the same under the default; every `click` and `pass` line
  of the 45 example worlds but the two-slit screens' declaration is
  unchanged ([validation](docs/VALIDATION.md)). Tests:
  `test_ray_detector` (f), (g), (h) new, (a), (b), (e) under `wave`
  ([expectations](docs/TEST_EXPECTATIONS.md),
  [RAY_LAW section 5](docs/BEAM_LAW.md#5-the-detectors-record-the-re-emission-the-face-detectors)
  and note 23,
  [migration](docs/MIGRATION.md#the-detector-as-a-set-with-one-record-the-reading-key-and-the-phase-returned-on-2026-09-19)).

### The detector's record exact, never refused (2026-09-19, after the batching)

- The night's affordable amount (`RECORD_AMOUNT_BOUND` = 261123, the
  amount a detector Node or a face could click of one family in one
  interval) refused a lawful world: `examples/events/two_contents.json`,
  which had run 200 intervals before the bound, was refused at its 20th
  interval when its two +y beams of 2^17 left through `face:+y` together
  (262144). The record is a host reading, not the law's local work, so it
  is now exact and never refused ([RAY_LAW section 5](docs/BEAM_LAW.md#5-the-detectors-record-the-re-emission-the-face-detectors)
  and [note 19](docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)):
  the coherent pointer (X, Y) is summed in the int64 register while the
  clicked amount is within `POINTER_AMOUNT_BOUND` = (2^62 - 1) // (32 x
  257) = 560759486676481 and in Python integers beyond it
  (`nature_beam.coherent_pointer`); the square and the cumulative record
  are Python integers always (`Measured.record`, `Ledger.face_record`).
  `RECORD_AMOUNT_BOUND`, `check_record_amount`, `record_amount` and the
  refusal are deleted. The `record` of `events.jsonl`, `run.json` and
  `state.json` can exceed 2^63 and is parsed as an arbitrary-precision
  integer. Bit-exact on every world that ran: 44 of the 45 example worlds
  byte-identical before and after, `two_contents` completing its 200
  intervals with the books closed, its first 19 intervals' `events.jsonl`
  the byte prefix of the new one ([validation](docs/VALIDATION.md)).
  Tests: `test_ray_detector` (e) rewritten, `test_ray_worlds` (e) new
  ([expectations](docs/TEST_EXPECTATIONS.md),
  [migration](docs/MIGRATION.md#the-detectors-record-exact-never-refused-on-2026-09-19-after-the-batching)).

### The host's batching of the law of the ray (2026-09-19)

- Five optimizations of how the host runs the law, none of the law
  ([RAY_LAW section 10](docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation),
  note 22): step 4 taken in bulk across the measured events
  (`FamilyPlan`); the dense readings of the board decomposed on request
  for the active Nodes (`Readings`, `ArrivalRows`); the merge by one
  packed key with the lexsort as the fallback (`RayStore.merge_key`); the
  books as running ledger lines (`Ledger.transit_momentum`,
  `RaySimulation.recount`, `books(recount=True)`) and the collision table
  cached per process; the clocks' frame in bulk (`_frame_all`), the
  self-creations visiting only the emitters, `events.jsonl` buffered.
  Bit-exact: the 45 example worlds' `events.jsonl` and `state.json`
  byte-identical to the base and the tools' outputs the same
  ([validation](docs/VALIDATION.md)); the plane source of series C 2.97 ->
  1.61 ms per interval, two slits 12.4 -> 3.5 ms, the suite 16.8 -> 5.5 s.
  Tests: `test_ray_books` (new), `test_ray_bijection` (the merge),
  `test_ray_readings` (e), `test_ray_push` (i)
  ([expectations](docs/TEST_EXPECTATIONS.md)).

### The push as one form, the one label and the affordable amount (2026-09-19, the night)

- The physics-rule review of the law of the ray and the model owner's
  proposal 2 ([RAY_LAW section 10](docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation),
  notes 18 to 21). Every momentum the law reads or moves is the one label
  of the rows (`nature_beam.momentum_labels`): the push's moment, the
  click's momentum, the face click's, the recoil, what comes home and the
  transit line; no collision at a Node that holds a measured event (rays
  meet the table, not each other); the push is one bilinear form
  `push_A = sum kappa(A, B) . V_B` (`push_form`) with the emitter's factor
  (q_B, M_B) carried on a free family's record as two integer columns
  `charge` and `mass`, the lookup by number and the lcm deleted; the
  amount a detector Node or a face clicks in one interval bounded by the
  affordable amount 261123 before the record's products are formed
  (`RECORD_AMOUNT_BOUND`), every reduction exact. The series C, series 7
  and Bell runs are unchanged record by record; series D is re-registered
  with the momenta re-derived for the label's magnitude (no orbit closes;
  the open question of the label's magnitude for the owner,
  [PROJECT_STATUS](docs/PROJECT_STATUS.md)). Tests: `test_ray_push` (new),
  `test_ray_collision` (d), `test_ray_detector` (e)
  ([migration](docs/MIGRATION.md#the-push-as-one-form-the-one-label-and-the-affordable-amount-on-2026-09-19-the-night),
  [expectations](docs/TEST_EXPECTATIONS.md), [validation](docs/VALIDATION.md)).

### Cleanup after the law of the ray (2026-09-19)

- The contributor instructions and the definitions that still sent a reader
  to the deleted generic disturbance contract (docs/DISTURBANCES.md, deleted
  on 2026-09-19) carry the history marker with the date and the pointer to
  [the law of the ray](docs/BEAM_LAW.md) and [the engine](docs/ENGINE.md):
  the four skills and the shared workflow that named DISTURBANCES.md as the
  active contract; SIMULATOR_DEFINITIONS "Active generic disturbance model"
  (now "Historical ... (deleted on 2026-09-19)") and its display section's
  pointer; POSTULATES "Active initialization-defined model" and its "Active
  contract: disturbance transfers ..." line; TERMINOLOGY "Ray-event terms";
  DETECTOR_REQUIREMENTS' status line; PHYSICAL_FEATURES' schema pointer.
  No physics text was rewritten; the sections are marked, not deleted.
- `core/integer.py` loses the component arithmetic of the deleted engines
  (`signed_divrem`, `ceil_div`, `checked_sum`, `add_components`,
  `subtract_components`, `dot_product`, `cross_product`, `reduced_ratio`:
  no caller left) and `core/lattice.py` loses `MIXING_OPPOSITE` (no caller);
  their 13 tests go with them, and `test_integer_arithmetic.py` pins the
  primitives the ray law uses (`checked_work`, `integer_root`, `bounded_gcd`)
  ([migration](docs/MIGRATION.md#cleanup-after-the-law-of-the-ray-on-2026-09-19)).
- `pyproject.toml` declares numpy (`numpy>=2.5.3,<3`, the version of the
  validated environment as the floor) as a dependency of the package: the
  engine imports it at module level, and `pip install -e .` installed
  nothing before; the render extra keeps matplotlib, Pillow and playwright.
- `event_universe.__version__` is 0.3.1, the version of `pyproject.toml`,
  `CITATION.cff` and the 0.3.1 release of 2026-09-15 (the string read 0.3.0
  since then); `run.json` records `package_version` 0.3.1 from now on.
- `import event_universe` loads the engine (numpy) on the first read of
  `RaySimulation`, as the `events` package promised: the package, the world
  parser and the preflight import only the generic physics.
### The table from the keys and the moments (2026-09-19, the night)

- Two decisions of the model owner on the mathematician's review of the
  table of the physical entities (Highlights 5.4, "I approve 1 and 3";
  [RAY_LAW section 10](docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation),
  notes 15 and 16), generic replacing generic. The table of a measured
  event is generated from the families' keys (`world.default_table`: a
  free family read, a paid one measured, no window) and a world declares
  only what differs (a window, a rule off the default, a `reads`
  component; `rule` optional in the object form; an entry equal to the
  default accepted and changing nothing); the kind of a family is derived
  from its `quantum` (0 free, 1 or more paid; `quantum` required) and the
  key `kind` is refused naming MIGRATION. The one reading `read_arrivals`
  is the amount-weighted moments of order 0, 1 and 2 of the arrivals'
  direction vectors (the count split outside / here, the flow, the
  traceless tensor `3 x sum amount x D (x) D - tr I`, exact integers,
  bounded), valid for a fan as for the six headings, in place of the
  seven-slot decomposition; on the six headings it reads exactly as
  before, on a fan a ray enters with its own vector. The example worlds
  are rewritten by `tools/migrate_ray_worlds.py` (new) to declare only
  what differs; every example world parses as before and the Bell and
  coupling runs are unchanged record by record
  ([validation](docs/VALIDATION.md)). Tests: `test_default_table` (new),
  `test_ray_readings` (a) re-pinned
  ([migration](docs/MIGRATION.md#the-table-from-the-keys-and-the-moments-on-2026-09-19-the-night),
  [expectations](docs/TEST_EXPECTATIONS.md)).
### The width of the push (2026-09-19)

- The world key `width` (S, an integer from 1; the model owner's D1,
  2026-09-19, Highlights 5.4, "try D1"): a free measured event of content M
  with the momentum component p on an axis steps one Link per
  (S x M + p) / p self-creations on that axis, `by_clock(age, |p|, S x M +
  |p|)` in `RaySimulation._move` in place of `M + |p|`, no remainder kept.
  S = 1 is the default and the rule as it was (one Link per (M + p) / p),
  so every existing world file reads the same and no migration note is
  needed; the parser refuses 0, a negative width, a string and a fraction
  naming the key; `run.json` records `width`. One unit of net flow gives
  any body p = M, so the speed it gives is 1 / (S + 1) for every content:
  the equivalence principle is kept and a world can declare slow motion
  ([RAY_LAW section 3](docs/BEAM_LAW.md#3-the-nodes-interval-nature_beam)
  step 5 and note 15, [the engine](docs/ENGINE.md),
  [terminology](docs/TERMINOLOGY.md)). Test: `tests/test_push_width.py`
  ([expectations](docs/TEST_EXPECTATIONS.md#the-width-of-the-push)).
- The orbit series D on the plane (`examples/events/orbit/`, six worlds by
  `make_worlds.py`, `tools/orbit_readings.py`): a fixed source releasing
  one shell every 10 intervals on a fan of 120 primitive in-plane
  directions and a free probe of content 1 at r = 12 or 24 with the
  tangential momentum derived for a circular orbit under the measured push
  law, at `width` 1, 8 and 32. Registered in
  [D, the orbit under the law of the ray, on the plane](docs/EXPERIMENTS.md#d-the-orbit-under-the-beam-law-on-the-plane-2026-09-19):
  one orbit closes by the criterion (S = 32, r = 12: 346 intervals against
  343 derived, an eccentric loop), no other closing, the mean push as
  derived (C 1.1), the grain of the push the reason. No test pins the
  registered run (the owner's rule of 2026-09-17).

### The law of the ray (2026-09-19)

- The engine of the law of the ray, `rays-v1` (the model owner, 2026-09-19,
  Highlights 5.4, "DECIDED: the law of the ray"; the design
  [docs/BEAM_LAW.md](docs/BEAM_LAW.md)): the record `NatureBeam` and the one
  function `nature_beam` (`src/event_universe/events/nature_beam.py`), a
  Node's whole interval for the rays present; the flight table at
  1 / sqrt 3 on the digital line of every direction (at most one Link per
  interval, the age modulo the period); the eight-slot collision table
  generated from its rule and checked at load (a bijection inside invariant
  classes); the one reading `read_arrivals` (two scalars, the flow, the
  tensor; every coupling selects its component by `reads`); the detector's
  squared coherent record per interval (`record`); the re-emission on
  declared directions; the inverse interval (`inverse_step`) on a board
  without a measured event; the store of records per family. The world
  selects it with `"law": "rays"` and gains `directions`,
  `direction_bound`, `phase_per_link`, a measured event's `directions`, a
  table entry's `reads`, a ray's `direction` and `age`. `events-v1` is
  deleted with `mixing.py`, `transit.py`, `reversible.py`, the
  `reversible-detector-v1` candidate and fourteen test modules; every rule
  the ray law keeps is re-pinned in the ten `test_ray_*` modules
  ([migration](docs/MIGRATION.md#the-law-of-the-ray-on-2026-09-19-rays-v1),
  [expectations](docs/TEST_EXPECTATIONS.md)). The example worlds, the Bell
  and coupling generators and the detector definitions are ray worlds; the
  Bell run A2 and the coupling series C are re-registered under `rays-v1`
  ([experiments](docs/EXPERIMENTS.md)). Package version 0.3.1 (the
  `__version__` string read 0.3.0 until the cleanup above).

### The engine of the law of events (2026-09-19)

- The ray is `NatureBeam` and its one function `nature_beam` (module
  `events/nature_beam.py`), the model owner's name of 2026-09-19 replacing
  GonenBeam given earlier the same day; a mechanical rename, nothing else
  changed ([migration](docs/MIGRATION.md#the-ray-is-naturebeam-on-2026-09-19-the-night)).
- The three reversible corrections that every path shares (the model
  owner, 2026-09-19, Highlights 5.4; the architect's D2 and D3). No merge:
  a measured event's step onto a Node that holds a measured event is
  refused, the stepping event staying where it is with its momentum, the
  resident untouched and the step counted (the `merged` record and the
  merge branch of `_move` deleted; a world where two bodies met and merged
  now keeps both). An open face is a detector: every escape through an open
  face, in transit or a measured event's step, is a `click` on the face
  detector named by the face (`face:+x` ... `face:-z`), recorded with the
  tick, the Node, the number, the amount, the phase, the momentum and the
  content, the face detectors listed in the run's `detectors` after the
  declared ones, and the books' escaped lines their sums; nothing physical
  changes at the face (the `escaped` record of a measured event becomes
  that click). The clock's count read off the clock: the count a measured
  event owes after its self-creation is `by_clock(age, k x n, d)` from the
  presence k, like every other rate, no remainder kept, so the mean slowing
  is k n / d (a presence of 1 at [1, 4] slows the clock by 1 / 4 where
  `k x n // d` gave none; exact multiples unchanged)
  ([the engine](docs/ENGINE.md),
  [migration](docs/MIGRATION.md#no-merge-a-step-onto-a-measured-event-is-refused-on-2026-09-19)).
  Tests: `test_border_and_clock_corrections` (new); `test_event_boundaries`
  (the wrapped target held: the refusal), `test_phase_window` (a) (two face
  clicks among its records) re-pinned; `test_event_suspension` unchanged;
  the Bell worlds unchanged
  ([expectations](docs/TEST_EXPECTATIONS.md#the-border-and-the-clocks-count)).
- One reading set for every coupling (the model owner, 2026-09-19, on the
  mathematician's list: "everything present at the Node but the reader's
  own number, including here"). The presence at a Node counts, beside the
  arrivals and the units waiting there as arrivals, the content of the
  measured event at the Node under its number (`EventSimulation.step`), so
  a transit bundle of another number reads it (a unit of light passing a
  content of 2^10 at `suspension` [1, 4] now carries 256 where it read 0)
  and the measured event, reading every number but its own, does not; a
  detector's threshold is met by the family's amount summed over every
  number but the Node's own, and a phase window reads the phase of their
  coherent sum (`Transit.phase_at(position, ranks)` over a sequence of
  ranks), one verdict for the set, the record per number with the set's
  phase (`_meet`, split into `_home` and `_respond`); the push was already
  the sum over the numbers of each number's flow (the emitter's electric
  factor its own) with the own number home, and now follows the set's gate.
  What came home is not content and not presence ([the engine](docs/ENGINE.md),
  [terminology](docs/TERMINOLOGY.md),
  [migration](docs/MIGRATION.md#one-reading-set-for-every-coupling-on-2026-09-19)).
  Test: `test_one_reading_set` (new;
  [expectations](docs/TEST_EXPECTATIONS.md#one-reading-set));
  `test_event_suspension` (e) reads 17 where it read 16, its counts
  unchanged; no other pin moves. The Bell worlds run unchanged (326
  criteria of `tools/bell_chsh.py`, S = 2).
- The integer bounds of the measured line and of the emission (the
  architect's review of 2026-09-19, findings F2, F4 and F9). `engine.bounded`
  checks a measured event's momentum after a push, a recoil or a merge, the
  push taken and its terms, its content after a click or a merge, and what
  waits to be created again with its content against 2^62 - 1
  (`transit.MOMENTUM_BOUND`, the bound of a declared and of a carried
  momentum) before they are assigned; beyond it the run is refused with
  `OverflowError` naming the measured event, its Node and the quantity
  (until now `Measured.momentum` and `pushed` were unbounded Python
  integers). The parser refuses a measured event of a free family whose
  release per Port per self-creation, amount x n // d at the world's
  `release`, times 3 exceeds the mixing's cell bound 2^30 - 1
  (`world.EMISSION_CELL_BOUND`, `EMISSION_MARGIN`: a neighbour's slot holds
  up to about 2.3 x the release per Port), naming the Node, the amount, the
  release and the bound, where until now the preflight certified a content
  of 2^36 at [1, 128] and the first crowded mixing refused the run at
  interval 4 to 14; every shipped example passes (the largest free emission,
  2^24 at [1, 128], is 3 x 131072 = 393216). The four refusals of
  `mixing.py` that said "value exceeds the disturbance integer bound" (the
  retired engine's word) now name the quantity: the amount in a cell, the
  momentum carried by a departure, the amount placed on a departure, and the
  coherent sum's component ([the engine](docs/ENGINE.md),
  [migration](docs/MIGRATION.md#the-emission-bound-at-parsing-and-the-bounded-measured-line-on-2026-09-19)).
  Test: `test_integer_bounds_of_measured_and_emission` (new;
  [expectations](docs/TEST_EXPECTATIONS.md#the-integer-bounds-of-the-measured-line-and-of-the-emission)).
- A release costs the emitter by its phase rate (the model owner,
  2026-09-19, "I approve the proposal"): at a self-creation whose turn is
  s = `by_clock(age, content, K)` phase steps, each unit a lamp releases
  costs it `quantum` x s content, carries that content and the momentum
  `quantum` x s along its heading, and gives it to the measured event that
  measures it, so the content of a click is proportional to the emitter's
  frequency, E = h f with h the declared `quantum` (the content of one unit
  per phase step). A turn of 0 releases nothing (no quanta of zero content).
  The content is carried per slot in transit (`Transit.arr_con`, `fly_con`)
  and goes with the units at every Node exactly as the momentum does; the
  books carry a content line balanced at every interval; measurement
  records and `state.json` carry the content. A free family's release costs
  nothing and its units carry no content, so `measure` on a free family adds
  nothing ([the engine](docs/ENGINE.md#a-release-costs-the-emitter-by-its-phase-rate),
  [migration](docs/MIGRATION.md#a-release-costs-the-emitter-by-its-phase-rate-on-2026-09-19-e--h-f)).
  Tests: `test_release_costs_by_phase_rate` (new); `test_event_clock` (c)
  at K 82, `test_detector_sensitivity` (c) at K 24, `test_phase_window` (a)
  records with `content`, `test_event_suspension` (c) re-pinned,
  `test_event_worlds` (d) the screen's content
  ([expectations](docs/TEST_EXPECTATIONS.md#a-release-costs-the-emitter-by-its-phase-rate)).
  The Bell worlds run unchanged (326 criteria of `tools/bell_chsh.py`).
- One rule of the Node: the phase-less scatter is the diagonal of the
  coherent sum inside `mix_arrivals` (the model owner, 2026-09-19:
  "everything generic must be replaced by generic"; the physics-rule
  reviewer's identity: with c_h = S - 3 a_opp(h), dropping every cross term
  of |c_h|^2 between mutually incoherent arrivals leaves
  weight_h = 32^2 x (the number's amount over the six Ports + 3 x its
  amount through the side's own Port), 4 : 1 : 1 : 1 : 1 : 1 for a lone
  arrival, exact integers, no root). `mixing.scatter_arrivals` and
  `SCATTER_BACK`, `SCATTER_TOTAL` are removed; `mix_arrivals` reads the
  family's `phased` and takes its weights from `coherent_weights` or
  `diagonal_weights`, the placement, the group with no whole by its
  momentum, `apportion_carried` and the leaving phase (0 without a phase
  circle) the same code for every family; `Transit.cycle` calls it for
  every family. The shares agree with the scatter in the mean exactly; the
  rounding and the momentum labels fall once per group where they fell once
  per Port, and a number's weights are its own (no cross term between
  numbers: another number's field does not steer its labels). About four
  times faster than the scatter on 29^3 ([the engine](docs/ENGINE.md),
  [migration](docs/MIGRATION.md#one-rule-of-the-node-the-phase-less-scatter-folded-into-mix_arrivals-on-2026-09-19)).
  Tests: `test_phaseless_family` (b) re-pinned (the labels of two opposite
  9s 0 each, old -3 and 3; the edge [4, 2, 2, 1, 1, 1], old
  [6, 1, 1, 1, 1, 1]), (d) the identity of the weights added;
  `test_event_worlds` (a) to (c) unchanged within their bands
  ([expectations](docs/TEST_EXPECTATIONS.md#a-family-without-a-phase-circle)).
- The coherent sum at a Node runs over all the arrivals present, whatever
  their number (node-mixing-v3, the model owner's decision of 2026-09-19:
  "the Node reads what is present"; the number is a label for the detector,
  not a kind). `mixing.mix_arrivals` sums the amplitude vectors over the
  number axis per Port before the coherent sum; the leaving amplitude of
  each side is the common sum less three times what came in through its
  Port over all numbers; the weights per side are common to every number at
  the Node and each number places its own units by them (the largest
  remainder with the tick's ties, per number; a number with no whole by its
  own momentum); the leaving phase of a side is the common one; every unit
  keeps its number and the momenta are apportioned per number as before.
  Two numbers' crowds at one Node now interfere (in antiphase nothing leaves
  sideways) where before they passed through each other; a family with one
  number at every Node, every example world, runs as before, and
  `Transit.sizes` and `phase_at` stay per number ([the engine](docs/ENGINE.md),
  [migration](docs/MIGRATION.md#the-coherent-sum-at-a-node-over-all-numbers-present-on-2026-09-19-node-mixing-v3)).
  Test: `test_node_mixing_numbers` (new; `test_node_mixing` is the control
  of one number, unchanged; [expectations](docs/TEST_EXPECTATIONS.md#the-coherent-sum-over-the-numbers)).
  With the field of matter phase-less (the next entry) the pair world of
  `test_event_worlds` (c) reads as that entry's pins say: its `m` never
  enters `mix_arrivals`, so v3 does not act on it.
- The field of matter without phase, the suspension as presence with a
  fractional width, and the push as the net flow (the model owner,
  2026-09-19, three decisions implemented together, to be reverted if the
  physics-rule reviewer's numbers say otherwise): a family may declare
  `"phase": false` (its events carry phase 0 and never turn, its measured
  events never turn, and at a Node each Port's arrival scatters on its own,
  four ninths back and one ninth each other way, `mixing.scatter_arrivals`,
  its momentum apportioned per Port); `suspension` is `[n, d]` and a reader
  owes `presence x n // d` intervals, the presence being the amount that
  arrived at its Node this interval over every family and every number but
  its own (an integer w reads as `[w, 1]`; the sizes no longer feed it); a
  free family's push is the content times the net flow of the bundle
  (amount times travel heading over the six Ports), the electric part
  likewise, a paid family's push its carried momentum as before. The example
  worlds `one_content` and `two_contents` declare `"phase": false` for `m`;
  `run.json` records `suspension` as a list and `phase` per family
  ([the engine](docs/ENGINE.md),
  [migration](docs/MIGRATION.md#the-field-of-matter-without-phase-the-suspension-as-presence-with-a-fractional-width-and-the-push-as-the-net-flow-on-2026-09-19)).
  Tests: `test_phaseless_family` new; `test_event_suspension` (a) to (c)
  re-pinned at `[1, 4]`, (d) and (e) added; `test_event_worlds` re-pinned
  ([expectations](docs/TEST_EXPECTATIONS.md)).
- A periodic axis as a declared run parameter of the world, the model
  owner's approved exception to the open board (2026-09-19): `boundary`
  accepts, beside `"open"`, an object with any of `x`, `y`, `z` set to
  `"open"` or `"periodic"`, the missing axes open. On a periodic axis the
  departures that would leave through one face are created at the first Node
  of the opposite face (`Transit.walk`), nothing escapes on that axis and the
  momentum they carry stays on the board; with an extent of 1 the two
  departures on that axis return to the same Node in the next interval as
  its arrivals through those Ports (a four-Port node with a one-interval
  stub). Open stays the default; `"closed"` and every other word stay
  refused. `run.json` and `state.json` carry `boundary` as declared; the
  preflight's summary shows the boundary per axis ([the engine](docs/ENGINE.md),
  [migration](docs/MIGRATION.md#a-periodic-axis-as-a-declared-run-parameter-of-the-world-on-2026-09-19-boundary-per-axis)).
  Test: `test_periodic_axis` ([expectations](docs/TEST_EXPECTATIONS.md#a-periodic-axis)).
- A measured event's step wraps on a periodic axis, one rule for the board
  (the model owner, 2026-09-19): its step by its momentum (`_move`, step 6)
  lands on the first Node of the opposite face as the departures do, and
  with an extent of 1 on its own Node, no move and no merge with itself, the
  momentum untouched and the step counted in `steps`; through an open face
  it escapes with its content and momentum as before (the first periodic
  axis escaped a measured event on every face; [the engine](docs/ENGINE.md),
  [migration](docs/MIGRATION.md#a-periodic-axis-as-a-declared-run-parameter-of-the-world-on-2026-09-19-boundary-per-axis)).
  Test: `test_periodic_axis` (d) ([expectations](docs/TEST_EXPECTATIONS.md#a-periodic-axis)).
- A measured event is created again first and then reads its suspension:
  the count it owes, `suspension` intervals per whole unit of the other
  numbers' sizes at its Node, is read after its self-creation from this
  interval's sizes and paid before the next, so in a steady size of k whole
  units its clock is slowed by 1 / (k + 1), never frozen (Highlights 5.4:
  "releases and turns slower"). The first `events-v1` read before the
  self-creation and froze the clock of every measured event in a steady
  field of one whole unit or more (found by the physics-rule review of
  2026-09-19); worlds with `suspension` 0 are unchanged
  (`EventSimulation.step`, `_release`, `_suspend`, [the engine](docs/ENGINE.md),
  [migration](docs/MIGRATION.md#the-suspension-of-a-measured-event-read-after-its-self-creation-on-2026-09-19)).
  Test: `test_event_suspension` (b) re-pinned, (c) added
  ([expectations](docs/TEST_EXPECTATIONS.md#the-suspension)).
- The engine of the law of events (`events-v1`, `src/event_universe/events/`)
  is the one engine: one thing, the event, created at every interval at its
  next place from its record, at a neighbour or here; a measured event's clock
  the count of its self-creations and every rate read off it (`by_clock`); the
  suspension a count the event carries; the sides from the vectors in whole
  units, a single quantum whole by its momentum; no turn in transit; no
  register, remainder, parked share or draw; detectors by sensitivity
  ([the engine](docs/ENGINE.md), [migration](docs/MIGRATION.md)). The engine of
  the law of the shadow (`field-only-v1`) is deleted with its tests and worlds;
  the world file's keys are renamed (`measured`, `in_transit`, `suspension`,
  `detectors`; `phase_turn` gone). Tests: `test_node_mixing` (node-mixing-v2),
  `test_event_transit`, `test_event_suspension`, `test_event_clock`,
  `test_event_worlds` ([expectations](docs/TEST_EXPECTATIONS.md)).
- A detector's threshold gates every response of a detector's Node (`read`,
  `measure`, `rerelease`), receivers and re-emitters alike, by the model
  owner's instruction of 2026-09-19 that every kind of external apparatus
  works with the sensitivity: a bundle of one number below the threshold
  passes with no push and mixes on; a release reads no threshold
  (`EventSimulation._meet`, [the engine](docs/ENGINE.md)). Test:
  `test_detector_sensitivity` ([expectations](docs/TEST_EXPECTATIONS.md#a-detectors-sensitivity)).
- The phase window, `phase_window`, by the model owner's decision of
  2026-09-19 ("Approve the phase window as a declared width of a detector,
  and of the emitter too"; [Highlights 5.4](docs/HIGHLIGHTS.md#54-the-detector)):
  a setting on the circle of N steps and the half circle centred on it. On a
  table entry (`{"rule": ..., "phase_window": s}`, any rule but `pass`; the
  string form still accepted) the response, after the threshold, only to a
  bundle whose phase at the Node falls in the window, a bundle outside it
  passing with a `pass` record; on a lamp a release only at the
  self-creations whose clock phase falls in it, the clock and the phase
  turning regardless; the phase read on every measurement record
  (`Transit.phase_at`, `engine.in_window`, [the engine](docs/ENGINE.md),
  [migration](docs/MIGRATION.md#the-phase-window-on-2026-09-19-phase_window)).
  Test: `test_phase_window` ([expectations](docs/TEST_EXPECTATIONS.md#the-phase-window)).

### The law of events recorded (2026-09-19)

- The model owner's law of events, after the one engine and `phase_turn`
  ("there are no registers"; "there are no fields; a field is an event";
  "there is no matter either; matter is a measured event"; "a single quantum
  does not split; in the space of events the quantum leaves in one
  direction"; "there is no shadow and no real; on the board there are only
  events"), is recorded in [Highlights 5.4](docs/HIGHLIGHTS.md#54-the-detector)
  after "One speed, and what is seen", in the owner's words with the
  orchestrator's readings flagged, and the paragraphs it changes carry a dated
  sentence. Nothing of it is implemented: [Highlights coverage](docs/HIGHLIGHTS_IMPLEMENTATION.md),
  [ENGINE.md](docs/ENGINE.md), [PROJECT_STATUS.md](docs/PROJECT_STATUS.md) and the
  README say so. No code changes. The same day: every event carries momentum
  from birth ("By the momentum"); no return to the source; the suspension is a
  count the event carries; fifteen principles recorded after the law with the
  owner's decision on each, the fixing mechanism of their points 8 to 12 not
  adopted; what follows for Highlights and the engine, and the tests of the
  engine of events in 5.5.

### One engine (2026-09-19)

- The engine of the law of the shadow (`field-only-v1`, feature 20) is the one
  engine, by the model owner's decision of 2026-09-19 ("The field is, in fact,
  a field of events. No confrontations are needed. Only tests that everything
  is as designed."; [Highlights 5.4](docs/HIGHLIGHTS.md#54-the-detector)). The
  old engine of the law of the bit, its worlds, catalog, tools and tests are
  deleted ([migration](docs/MIGRATION.md#one-engine-on-2026-09-19-the-old-engine-deleted)).
  The substrate the new engine took from the old one moved to
  `core/lattice.py`, `core/phase.py` and `shadow/mixing.py`, byte-identical in
  what it does; the Node's mixing has its own isolated test again,
  `tests/test_node_mixing.py`, on one Node of the engine's layer.
- The runner takes `--init`, `--output` and `--ticks` only; the preflight
  checks world files only; the workspace lists the worlds of `examples/shadow/`
  and runs headless.
- The same day, earlier: the three pending decisions of the morning's status
  line (`transmitted_number`, the wait's unit, ε_g) were withdrawn ("We do not
  need these three things at all"), so the gate of feature 20b is not written;
  the wait is the delayed clock and `wait_per_quantum` stays a declared width
  of the world; and the owner's reading "A quantum passes, like everything, at
  the speed of light between Nodes" is recorded in 5.4 ("One speed, and what
  is seen").

- `families[i].phase_turn` (features 21 and 23; the owner's "what can be put
  as a parameter, put" and "constant frequency for light? Yes, make it the
  default for light. That is, per family."): how a family's quanta turn their
  phase per Link walked. `"quantum"`, the default for a paid family: by the
  family's quantum over K, the same for every quantum of the family wherever it
  is, the remainder carried per family, so light keeps the frequency it was
  born with (round 8, S5); `"none"`, the default for a free family; `"amount"`,
  the old rule by the amount in the cell, which slowed as the field thinned and
  stopped a few Links from a lamp, kept as a choice. Replaces the key
  `turns_in_flight` of the same morning ([migration](docs/MIGRATION.md#the-phase-turn-in-flight-per-family-on-2026-09-19-phase_turn));
  `tests/test_family_turns.py`.

- `families[i].quantum` (the owner's "put it in, without an experiment"): the
  units of a family that make one event at a holder that absorbs them (`keep`,
  the click; `rerelease`), per number, the rest waiting in the holder's
  register (`pending` in the content's state and on the held line of the
  books, `events` per family); 1 by default, every unit its own event as
  before; the derivation's q_γ as a declared width; `tests/test_family_quantum.py`.

### The law of the shadow, the field-only engine (`field-only-v1`, feature 20, 2026-09-18)

- A new engine mode beside the old one, `event_universe/shadow/`, selected by
  a world's `"law": "shadow"` key ([the law of the shadow](docs/MIGRATION.md)):
  only shadows and events. Matter is content held at Nodes; every ray is a
  shadow, a whole quantum in flight that moves one Link per interval and
  spreads by the Node's mixing, the dense layer's kernels by import; an event
  is a whole quantum at a Node with content, absorbed, held or released again
  by the holder's table (the free families read at a holder and passed on,
  the push by the holder's content and charge; light kept, the click, or
  re-released; the own number sunk for its amount and pushing nothing); a
  held content releases its field at the world's rate, a lamp spends its
  light; the wait reads the size; the step is the accumulator's, at most
  once in two intervals (round 8's Node rule, DERIVATIONS.md sections 51 to
  56); the books per family close at every tick. The old engine, its worlds and its
  tests are untouched ([migration](docs/MIGRATION.md#the-law-of-the-shadow-a-new-engine-mode-on-2026-09-18-field-only-v1)).
- The worlds `examples/shadow/` (one content, two contents, two slits and
  the one-slit control) and the isolated test `tests/test_field_only.py`
  ([expectations](docs/MIGRATION.md)), the
  numbers from DERIVATIONS.md round 7.

### Charge per thing (`charge-per-thing-v1`, feature 16g, 2026-09-18)

- The charge of a thing is one declared number of its family, whatever its
  content (the model owner, Highlights 5.4 point 16 as amended): a family's
  `charge` and a body's are the charge of one thing, whole, never a charge
  per quantum. The electricity reading multiplies the shadow's message (its
  owner's charge over its content, unchanged) by the whole charge of what is
  pushed; the worked example of point 16 holds exactly, a body of 1000 quanta
  with charge 1 is pushed by nine units and not nine thousand, and the
  catalog's electron of 20 does not turn at its first push.
- The charge readout, the ledger's charge line and the local audit count the
  whole charge of things: a merged ray of k things carries k times the
  family's charge (the identities a merge keeps), a record's stock the things
  it has not yet emitted, a shadow none; every table conserves it (the
  appended invariant sums the things' charges; a join keeps every identity).
- `run.json` records `charge_per_thing`; the refusal of a pushed body whose
  charge was not a multiple of its amount is gone. No example world's
  declaration changes; the tests whose bodies declared `-amount` to mean -1
  per quantum re-declare it ([migration](docs/MIGRATION.md#charge-per-thing-on-2026-09-18-charge-per-thing-v1)).

## 0.3.1 - 2026-09-15

Concept DOI 10.5281/zenodo.22738746 (the version DOI is listed on the Zenodo
record).

### Redshift from delay growth (second manuscript)

- `redshift_sweep.py`: a train of twelve rays crosses closed rows of 16 to 96
  Nodes under `ray_delay` to an absorbing eye that counts its own cycles;
  `1 + z = k_o / k_e` on the eye's clock, durations stretch by the same
  ratio, `z` from 0.07 to 2.81 with the distance, the slope scaling with the
  emission; the wave's frequency follows the gaps under the default phase
  rule by construction (the phase difference between rays is conserved along
  the path), read over the span it is measured on and converging with the
  tick resolution; a single source emitting at a fixed interval of its own
  clock (`--labels "single source"`) gives the same law. Moving bodies stall the
  clocks of the Nodes they wait at and are
  not used (report (`examples/relativity-probes/`, deleted on 2026-09-17)).
- `redshift_hubble.py`: the law's shapes against the Pantheon+ Hubble-flow
  sample, with the diagonal errors and (`--covariance`) the release's full
  covariance, the exponent fitted under each error model with its interval
  (refined in steps of 0.001 around the minimum) and the reading-A family
  bounded by its `n -> infinity` limit; the model's own load histories are
  behind LambdaCDM, and the best power law by nine units of chi-square with
  one fitted parameter each, as preferences between models (the shapes pass
  a goodness-of-fit test on their own); the Tolman exponent is the
  discriminating test, an indication against the lattice until the data
  are reduced under its own distance relations. Manuscript in `paper/redshift/` ([hypotheses](docs/HYPOTHESES.md)).


A review pass on the paper's Bell narrative. No engine change; the Bell probe
gains two modes and the framework's claims are narrowed to what is measured.

### Bell's test

- The bonded value carries its statistics: `--sweep` re-measures the bonded
  CHSH value with fresh pairs for every setting pair, 64 to 4096 pairs per
  correlation on the lattice with four replicas each and the registry alone
  to a million pairs, with binomial standard errors; every lattice outcome
  equals the registry's answer from the same seed, and `S` converges to the
  table expectation `724/256 = 2.828125`. The first run's 2.889 was sampling
  spread on correlated samples (report: `examples/bell-chsh/README.md`, deleted on 2026-09-17).
- Which assumption of Bell's theorem each candidate breaks is measured at
  fixed hidden variable by `--causal`: the lottery and the threshold are
  parameter independent; the bonded pair is deterministic and
  measurement-independent and breaks parameter independence (Bob's answer
  moves with Alice's setting for 0.72 of the hidden variables at
  `b'`); the quantum owner breaks outcome independence
  (report: `examples/bell-chsh/README.md`, deleted on 2026-09-17;
  coupling (`docs/QUANTUM_CLASSICAL_COUPLING.md`, deleted on 2026-09-17)).
- The door of postulate 22 is measured half by half: `--source agreement`
  keeps the coin even and fixes the agreement half, giving S = 4 (the
  Popescu-Rohrlich box) with even marginals and no signal; no-signalling
  bounds the coin, not the correlation (report: `examples/bell-chsh/README.md`, deleted on 2026-09-17).
- Postulates 4 and 22 name the broken assumption: the registry is a nonlocal
  resource in Bell's sense, its unmoved plus rates are no-signalling and not
  locality, and how a number is read (one end, both ends, or correlated with
  the settings) decides which assumption is at stake ([POSTULATES](POSTULATES.md)).

### Paper

- The manuscript is reframed as a finite-integer causal-lattice testbed: the
  configured laws are named as inputs, the Bell section carries errors and the
  causal analysis, "what is new" and "what is not claimed" are explicit, and
  the bonded pair is stated not to be a local explanation of the Bell value
  ([paper](paper/main.tex)).

## 0.3.0 - 2026-09-14

153 commits since 0.2.0. Zenodo DOI 10.5281/zenodo.22749342. Every number
below is recorded with its source fingerprint in [validation](docs/VALIDATION.md).

### Framework

- The framework is named Reality Theory (Universe24); the simulator stays
  Universe24 ([README](README.md)).
- Postulate 4 is split: energy, momentum, matter and every controllable
  message move at most one Node per step; the joint outcome of a bonded pair is
  the one declared exception, answered by a bounded registry that carries
  nothing physical ([POSTULATES](POSTULATES.md)).
- Postulate 22: every uncertain interaction consumes exactly one bounded
  integer; a bonded pair draws one number, whichever end asks first; the
  sequence is the only door for outside information and is bound by
  no-signalling.
- A [hypotheses page](docs/HYPOTHESES.md) keeps the questions the framework
  raises apart from measured results.

### Quantum and classical coupling (causal source candidate)

- Two-arm interference on the canonical runner: exact capture weights, a
  balanced Hadamard splitter, which-path decoherence, causal termination
  (report (`examples/quantum/causal_interference.md`, deleted on 2026-09-17)).
- Opt-in null notices restore the exact conditional Born weights after Link
  transit; crossing nulls are corrected locally by the later Node
  (crossing nulls (`examples/quantum/crossing_nulls.md`, deleted on 2026-09-17)).
- Opt-in field-dependent phase: an external classical field on one arm shifts
  the fringe by an exact configured phase per field unit.
- Opt-in funded emission: the wave pays for its own field from its conserved
  stock; totals constant; the retarded emission after a capture is the measured
  residual.
- Emission-scale sweep: the integer field follows `amount x |psi|^2` within one
  unit per tick at every scale.
- Two-wing Bell CHSH on the finite quantum owner: 14/5 exact, no-signalling
  marginals, dephased control 6/5 (report (`examples/quantum/bell_chsh.md`, deleted on 2026-09-17)).

### Straight and phased rays (Kerengonen candidate)

- Kerengonen phased rays with a fixed-point cosine table: double slit, Huygens
  slits, single-quantum lottery, de Broglie advance from momentum, mirror
  standing waves, matter-wave dissolution, Euclidean pace, claim and gather,
  bonded pairs.
- Bell's test on the ray with five captures on one scale: share 1.40 exact,
  lottery 1.48 and 1.38, threshold 2.00 exactly, bonded 2.89 against the
  quantum 2.83, plain field 2 (`examples/kerengonen-bell/` and `examples/bell-chsh/`,
  both deleted on 2026-09-17).
- An outside number source for bonded pairs: uniform is invisible, biased is
  a measured signal.
- Signed-quanta gravity with a closed ledger, gathered gravity (no dark-matter
  substitute from focusing), isotropy probe, relativity probes (lensing,
  redshift without recession, flat curves from a compressed closed dimension,
  gravitational phase in an interferometer, replay).

### Engine

- Local Focus scheduling (opt-in), ray ownership guards, carried allocation
  phases, ray delay and ray phase per tick, bounded prepared tables, 24-slot
  envelope output banks.

### Repository

- MIT license, `CITATION.cff`, Zenodo DOI 10.5281/zenodo.22738746 (0.2.0);
  named-particle gallery; documentation cleaned of process noise.

## 0.2.0 - 2026-09-14

First archived version: the integer lattice simulator with configured
disturbances, spatial fields, the finite quantum owner and the causal source
candidate. Zenodo DOI 10.5281/zenodo.22738746.
