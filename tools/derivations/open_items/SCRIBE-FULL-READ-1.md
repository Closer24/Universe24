# The Scribe's full read of the engine's code against the central postulate

The Scribe, 2026-10-27, 15:2x UTC, on the owner's word of 14:5x UTC ("always read all the code"; "the central postulate, that the engine runs whole numbers with one formula of Rule3, must hold; make sure there are no contradictions"; "always make sure the engine does not know families and everything is truly generic, it is in the laws too, and only whole numbers, without formulas").

Read: every line of src/event_universe at the engine head 608d97134, 35 files, 6,325 lines (the 22 modules, core/, features/, assembly/), the engine's and the Reader's, no suite run. Against: Postulate 2 (whole numbers, every act a bijection with its remainder kept), **The law in one line** (one division act with coefficients from the train's pair and the Node-clock's rates, every notch written by that same act, everything else a number in a file), **The Node-clock and the Mesh are generic; there is no if**, **No number in the code**, **No float anywhere in the system**, the ten postulates' second ("the Node-clock is dumb and generic ... knowing no bob, mass, well, train, fitting or click"), and the owner's rules of 11:3x and 14:5x UTC. The counts are the Boss's own counters (tools/engine_gates.py, 0660dd42e) and an AST scan; the lines are the Scribe's reading.

## 1. What holds

- **Whole numbers.** No float literal, no true division, no root, trig, exp or log call and no math import in src (AST scan, 0 of each). Every act is on integers; the one carried division is core/acts.py:18 and every write goes through it (clock.py:153 turn, 178 drive, tick.py:199 and 257 carries, unwind.py:77 and core/acts.py:38 the lay as acts.advance).
- **The rewind.** Every act has its inverse at direction -1 by the same function (clock.py:153, 235; tick.py:326), checked by the suite and the Reader's charts.
- **Locality of the dynamics.** A Node-clock reads itself and its six neighbours through core/spokes.py:37 across and unwind.py:19 neighbour. Board-wide reductions exist only as diagnostics and skip guards: clock.py:172 (the transient's bit length over the board), 255 and 263-265 (top.any(), top.sum(): the swap runs only where a Node-clock turned), run.py census and state_hash (the rewind's proof). Named, not breaches of the dynamics.

## 2. Where the code departs from the central postulate: the engine knows structure by kind

The five kinds are the families in the engine's own spelling: the phase clock (the walled row), light (the plane at (den, den)), the carrier (the shape-10 row), the potential (the shape-4 row at (den, den)), matter (a plane with a gap); the twin hands are a sixth by the shape 4 at a spring. They are named in every module that acts, which is why the places are so many.

- **The universe must hold exactly these.** trains.py:120-131 refuses a universe without exactly one walled row, one plane at (den, den), one shape-10 row, one shape-4 row and a plane with a gap; 124 and 128 fix the carrier's pair at (den - den div Gamma, den) and the potential's at (den, den); assembly/piece.py:38 admits the shapes 1, 2, 4 and 10 only; trains.py:62-69 gives each shape its own write teeth (drive_teeth: REGULATOR, OFFSET, HAND at (den, den)); trains.py:104 reads twin hands off the shape 4 at a spring.
- **The tick names the roles.** tick.py:66-68 holds `regulator`, `ratchet`, `offset`, `unsprung` apart; 120-147 standard_rate is the walled row's own act; 237-278 carry is the carrier's own write (held_numerator); 280-302 advances is the emitter's lay and the potential's drive by the lead; clock.py:100, 252-262 and readings.py:30-32 read the carrier's time gear by role.
- **The close does two acts by family.** unspring.py:125-127 and 209-215 take matter by the wind's fall (unspring_end) and light by moving a line toward its before (unsprung_end); striking.py:46-49 (list_of), 188 (fittings) and bobs.py:33 branch on the same line; setting.py:53, 59, 68, 80 branch on it for the lays.
- **Light's coupling is a number case.** meshes.py:20-23 coupling_of is min(den - num, 1), 0 for light and 1 for every other pair; readings.py:62-67 gives the walled row its own rule with no Meshes. The law calls a case by number lawful (**The Node-clock and the Mesh are generic; there is no if**, the owner's "1" of 10:4x); the owner's word of 14:5x, truly everything generic, is the question this reading puts to him.
- **Family words in names and keys.** clock.py:28-44 COUNTS (`body_clicks`, `births`), run.py:258 and 261 ("gap-0 W abs max", "gap-0 velocity max"), setting.py:26-31 FIELDS (the lay forms `sea` and `hole`), bobs(), unsprung_notches, unsprung_end; the Reader's modules name light and species throughout (reckoner.py:86-100).

**The Boss's counters, at 608d97134.** Reads of the unsprung hand by its identity 32: setting.py 53 59 66 68 80; bobs.py 30 33; clock.py 69 70; run.py 202 224 258 274 354; striking.py 46 47 67 131 188 263 326; tick.py 67 283 294; trains.py 67 117 128; unspring.py 125 127 209 215 233. Branches on it 15: setting.py 53 59 68 80; bobs.py 33; clock.py 69; run.py 202; striking.py 46 67 131 188; unspring.py 125 127 209 215. The counters see the words unsprung and sprung and a pair of one name; they do not see the other roles (REGULATOR 31 places in 11 files, HAND 31 in 9, OFFSET 11 in 4, `train(REGULATOR)` or `train(OFFSET)` 18 in 8, `.size ==` checks 9 in 5).

## 3. Numbers

- **The 37 literals beyond 0 and 1.** Engine 14: assembly/cycle.py:21 (4); assembly/setting.py:23-24 (2, 3), 104 and 108 (2, 2); core/acts.py:15 (2); core/rule3.py:126 and 136 (2, 2); core/spokes.py:7-8 (3, 2); meshes.py:127 (4); trains.py:15-17 (2, 4, 2). The writer run.py 3: 26 (12), 27 (24, 60). The Reader's modules 20: reckoner.py:15-29 (1000000, 100, 1000, 10, 20, 2, 2, 3, 4, 8, 6, 4, 2, 2), rim.py:7-8 (2, 4), gates.py:299 and 301 (2, 3), great_clock.py:30 (2), swings.py:9 (2).
- **Numbers spelled by name.** The counter sees literals; the engine also builds numbers from two typed ones: AXES = 3 (core/spokes.py:7) is read in 58 places of the engine proper (an AST count of the names, the writer and the Reader's modules apart) and builds SPOKES = 6 (13 places), REGULATOR = 1 + 3 AXES = 10 (trains.py:13), OFFSET = AXES + 1 = 4, HELD_DRIVE_WEIGHT = AXES + 1 (core/rule3.py:14), WINDING_WEIGHT = AXES (17), EXPONENT = AXES + 1 (features/stretch/__init__.py:14); HAND = 2 is read in 31 places; 40 doubled operands (x + x) stand for a typed 2 in the engine proper. The universe file holds four integers (den, node_clock, quantum_action, trace; the fifth, amplitude, struck at 0d59ff812) and each row's shape, pair or wall; the dimension, the sides, the shapes 1, 2, 4 and 10, the powers 4 and 2, the quarter turns, the half spans 1, 2 and 3 and the marks 12, 24 and 60 are typed in the code.
- **The enforcement is looser than the rule.** tests/test_rule3.py:108-130 and 139-154 allow {0, 1} in the law's files and, by file, spokes {2, 3}, rule3 {2, 3, 4}, trains {2, 4, 8, 10}, meshes {4}, setting {2, 3}, cycle {4}, run {12, 24, 60}, acts {2}, tools {0, 1, 2, 3, 4, 6}, and exempt nine modules whole (reckoner, gates, events, rim, great_clock, swings, clicks, predicates, symmetries). The Boss's gate counts every literal beyond 0 and 1 in all of them, on a ratchet: the test passes what the gate counts.

## 4. Formulas beyond Rule3's one

The one formula is the flux line, core/rule3.py:81-85 (pull_total, rule3) with its integers teeth_of (29), spring (34), gearing (39). Beside it the code types these as integer formulas, weights, tables or searches (44 functions, the Scribe's classification; each is a clause of the law, none is data):

- core/rule3.py: mesh_factor 57, mesh_unit_of 88, held_teeth 96, held_numerator 101, winding_of 113, wind_weight 139, mean_teeth_of 129.
- core/rates.py: the clock's table p_0(c) = Gamma (1 - 1/Gamma)^c by carries, Side.fill_to 41, stopped_load 100. features/standard: standard_rate 19, standard_teeth 24, standard_pinion 29, shortest_hand 89. features/stretch: stretch_of 37, load_of 51.
- meshes.py: coupling_of 20, offset_pair 47, factors 64, offsets 94, centred_count 88, skewed 114, mesh_teeth 125, through_mesh 130 (the Gaussian square).
- hands.py: wind 58 (the conserved share), sweep 42, lead 48, moving 108, rest 119, cosine_count 124. regulation.py: stress_parts 18, shear_parts 28, tensor_parts 39, net_flow 45, rest_rate_of 50.
- unwind.py: fall_of 35 (the exact take, a quadratic by search), push_of 85. unspring.py: fitted_windings_of 62.
- tick.py: impulse 202 (the kick), carry 237 (the carrier's write), twin_pulls 182, advances 280.
- assembly/setting.py: raised_cosine 98, rim_point 132, running_rotation 178 (the band's dispersion typed); assembly/cycle.py: cycle_angles 25.

The law's own text carries these as clauses (ALGEBRA.md, **The teeth counts are algebra and not code**: "in the code each is one primitive named by its clause"), so the contradiction lies between that text and the central postulate of one formula: either each clause is derived from Rule3 and the universe file's numbers (and then it stands in a file as a number, or as an argument of the one formula) or it is a formula beside Rule3's. The question is the owner's.

## 5. The documents against the code

- **README.md, the engine paragraph** said "no number of physics, no formula and no train's name in it. The gates keep it so on every check": false at 608d97134 by sections 2 to 4. Corrected with the date and the counts.
- **ALGEBRA.md, No number in the code** allows "Rule3's own integers alone (the law's 0, 1, 2, 3 and 6 and the line's 4 and 12)": contradicted by the owner's word of 11:3x UTC (the only numbers in the files) and by the Boss's gate (beyond 0 and 1). Marked struck by that word, dated.
- **ALGEBRA.md and ENGINE.md, The Node-clock and the Mesh are generic; there is no if** and **The tick is one function of the Node-clock** state the norm (no branch on a train's identity); the code departs by section 2. The norm stands, the departure is named, no sentence of the law changes.
- **The postulates against the code** named the gates "no float, no root, no number beyond the law's": updated to the Boss's gates of 12:30 UTC.
- **src docstrings** repeat the norm as fact (clock.py:1 "the Node knows nothing, there is no if"): the Boss's stage 1b.

## 6. What the postulate needs from the code, by name

1. The row kinds out of the code: no accepted-shape list (assembly/piece.py:38), no required roles (trains.py:120-131), the write teeth by shape (trains.py:62-69) read from the calibre.
2. One close act for every train: unspring_end and unsprung_end one act (unspring.py:146, 169), the children's train chosen by numbers alone (striking.py:43).
3. The tick's five acts over the list of trains with no role by name (tick.py:66-68, 120-147, 237-302).
4. The coupling of light by the pair alone, no number case (meshes.py:20-23, readings.py:62-67), or the owner's word that a case by number stays.
5. The dimension and the sides, the shapes and the powers from the piece or the calibre, or the owner's word that the lattice's three axes are the law's one typed number.
6. tests/test_rule3.py's whitelist and the nine exempt modules replaced by the Boss's gate; the counts to 0 by David's derivation (DAVID-GENERIC-ENGINE.md, asked at 12:2x UTC).

## 7. The owner's answers of 15:5x UTC and what each takes out of the code

His words (in translation): "There is no such thing as light's coupling. A specific number is forbidden except in a world or universe file. The dimension is a row's and it is only in the universe file; the engine is generic. The engine itself is supposed to be only Rule3 on integers. No formulas, no sines or cosines.. let them check how to do this. Rule3 on tensors, vectors and the like is allowed. Numbers in the code are forbidden altogether, only in the world, universe and seed files.. Update the Boss."

- **No light's coupling, no case by number:** meshes.py:20-23 coupling_of, readings.py:62-67, trains.py:62-69 drive_teeth and 104, core/rule3.py:88-95 mesh_unit_of; the law's allowance of the owner's "1" of 10:4x is struck.
- **The dimension and the shapes in the universe file alone:** core/spokes.py:7-8 AXES and SIDES, SPOKES in 13 places, AXES in 58 places of the engine proper, trains.py:13-17, assembly/piece.py:38, core/rule3.py:14-17, features/stretch/__init__.py:14; the universe file's rows already carry shape, pair and wall, so the shapes 1, 2, 4 and 10 and the three axes are the file's to hold.
- **Rule3 on integers alone, no formula, no sine or cosine:** the 44 functions of section 4; the integer sines and cosines among them are core/rates.py:25 sine_rim, core/rule3.py:88 mesh_unit_of (the root by the search largest_below at 173), assembly/setting.py:98 raised_cosine, 132 rim_point, 153 angle_of, 161 angles_of, 178 running_rotation, assembly/cycle.py:25 cycle_angles, readings.py:35 standard_angle, hands.py:124 cosine_count; the Reader's reckoner.py:197 rim_points and rim.py read den's circle too. Rule3 on tensors, vectors and complex numbers is allowed: DAVID-TENSORS.md (the regulator as one symmetric tensor) and DAVID-GAUSSIAN-HAND.md are the way in; how each function goes is for the Boss and David to check (DAVID-GENERIC-ENGINE.md, asked 12:2x UTC).
- **No number in the code at all:** the 37 literals of section 3, the typed constants, the 40 doubled operands, tests/test_rule3.py's whitelist and the gate's free 0 and 1 (the reading of 0 and 1 is the Boss's to give); the numbers stand in the world files, the universe files and the settings.

## 8. Re-read at 0d59ff812 (2026-10-27, 16:3x UTC)

The engine head moved from 608d97134 to 0d59ff812 (stage 1b of the clock-name rename, the spin one half and Pauli tests, the amplitudes' fold, X = Gamma rim; the full check 110 passed). The whole tree compared with 608d97134 by an AST comparison with the names of locals and parameters normalized: 27 of the 35 files of src are pure renames (no attribute, constant or structure changed, every rename bijective per function), 8 carry a function renamed (cycle.least_share to least_wind, setting.share_of to wind_of, one each in hands, striking, unspring, symmetries and clock) or the amplitudes' fold (assembly/piece.py: four integers named, a declared amplitude refused; clock.py:55: the standard's length Gamma rim). The counts of sections 2 to 4 are unchanged: numbers beyond 0 and 1 37 in 13 files, reads of the unsprung hand by identity 32 in 8 files, branches on it 15 in 6, family-name strings 0, floats 0, true divisions 0; the lines of the identity reads, the branches and the definitions are identical to 608d97134, so every citation above stands. The departures of sections 2 to 4 and 7 all stand; tests/test_rule3.py's whitelist is unchanged.

## 9. Re-read at 5f8680de2 (2026-10-27, 16:4x UTC)

The engine head moved from 0d59ff812 to 5f8680de2 (the Boss's tensors in the clock; the suite 110 passed). The whole src diff read (10 files, +68 -96): whole numbers hold (no float, no true division, no math or trig import); the counts of sections 2 to 4 unchanged (numbers beyond 0 and 1 37 in 13 files, reads of the unsprung hand by identity 32 in 8 files, branches on it 15 in 6, no new literal, no new branch); the file is 6,297 lines under src. New: regulation.stress_of (the regulator's nine axis sources one outer product, Rule3 on a tensor), meshes.train_twists, hands.spoke_places and draw.kept_pitch (pure memos by integers, the latter cleared at every click), unspring's store of the hands' winds (filled by one read of the whole great clock at the first miss, kept across the reads of one unwinding and cleared after its write, striking.py:204). Section 4's list stands with stress_parts, shear_parts, net_flow, train_twist and net_lead replaced by the two functions above; `coupling_of` (meshes.py:20, read at tick.py) still stands against the owner's click of 15:5x. The Reader's finding that the close's coordinate order breaks the torus's invariance in the clicks (reader-5 12a3db05e, ledger row 238) is a departure from the generic clause that this read did not find and adds to section 2.

## 10. The register of breaches at 5f8680de2, for the Boss (2026-10-27, 16:5x UTC)

On the owner's order ("Make sure the Boss is aware of the breaches."): every breach named so far, with its lines at the head 5f8680de2 (the lines of sections 2 to 4 are those of 608d97134 and 0d59ff812; tick.py, unspring.py, striking.py, bobs.py, meshes.py, hands.py and regulation.py shifted by a few lines at the tensors push, and these are the current ones). The Boss answers by number: built, ruled or objects.

**A. Against the owner's rules for the engine** (his words of 11:3x, 14:5x, 15:1x and 15:5x):

- **R1. Five kinds of train known by role** (the generic clause; "the engine generic"): trains.py:118-131 refuses a universe without exactly one walled row, one plane at (den, den), one shape-10 row, one shape-4 row and a gapped plane (124 and 128 fix the pairs), assembly/piece.py:38 admits their shapes alone, trains.py:62-69 drive_teeth by shape and :104 twin hands; tick.py:66-67 the roles, 117-144 standard_rate (the walled row's act), 233-274 carry (the regulator's write), 276-298 advances (the emitter's lay, the offset's drive); clock.py:100 and 258-259, readings.py:30-32 and 62-67 (the walled row's own rule); the identity counters, 32 reads in 8 files and 15 branches in 6 (setting.py 53 59 68 80; bobs.py 33; clock.py 69; run.py 202; striking.py 46 67 131 188; unspring.py 127 129 211 217), and the role words outside them (REGULATOR 31 places in 11 files, HAND 31 in 9, OFFSET 11 in 4).
- **R2. Light's coupling** ("there is no such thing as light's coupling"): meshes.py:20-23 coupling_of read at tick.py:70, 162, 163 (a table indexed by it) and 224; it stands in the tensors push; wave item 7 covers it only if it removes the case by number.
- **R3. The dimension and the shapes typed** ("a row's, only in the universe file"): core/spokes.py:7-8 AXES and SIDES (AXES read in 58 places, SPOKES in 13), trains.py:13-17, assembly/piece.py:38, core/rule3.py:14-17, features/stretch/__init__.py:14.
- **R4. Numbers in the code** ("forbidden altogether"): the 37 literals of section 3 (13 files; cycle.py:21, setting.py:23 24 104 108, acts.py:15, rule3.py:126 136, spokes.py:7 8, meshes.py:124, trains.py:15-17, run.py:26-27, and the Reader's modules), the typed constants, the 40 doubled operands, the gate's free 0 and 1.
- **R5. Formulas beside Rule3's one, sines and cosines** ("only Rule3 on integers"): the 44 functions of section 4; the integer sines and cosines among them: core/rates.py:25 sine_rim, core/rule3.py:88 mesh_unit_of (the root by the search at :173), assembly/setting.py:98 raised_cosine, 132 rim_point, 153 angle_of, 161 angles_of, 178 running_rotation, assembly/cycle.py:25 cycle_angles, readings.py:35 standard_angle, hands.py:128 cosine_count.
- **R6. The enforcement looser than the rule:** tests/test_rule3.py:110-132 and 141 allow integers by file and exempt nine reader modules whole.

**B. Against the law's letter** (David's close law, approved by the owner at 15:5x as items 1 to 4 of the wave, none built at 5f8680de2):

- **R7. The take's fall has the wrong sign:** unwind.py:35-74 fall_of (the closed form and its price) and TC-S1's sentence; the charts' matter booked from nothing (David; the Reader's second hand at 47 of 47 and 154 of 154 takes).
- **R8. The unspringing drops its excess:** unspring.py:148-168 unspring_end (181.9 walls on the bodies).
- **R9. The vernier reads grips[p], not R_ji:** draw.py:20-35.
- **R10. The light's take reads the live great clock where CL-S2 names the tick's start:** unspring.py:171-197 unsprung_end.
- **R11. The shears are written every tick and read by no act:** regulation.py:15-19 stress_of (DAVID-TENSORS.md); the owner's word asked.
- **R12. The engine knows light** (the owner, 17:0x UTC: "The engine is not supposed to know light at all.. it is generic."; it joins R1, R2 and R10): the unsprung hand is the engine's name for it and stands 54 times in 11 files (setting.py 5, bobs.py 4, clock.py 4, run.py 11, striking.py 10, tick.py 4, trains.py 3, unspring.py 8, and the readers' reckoner.py 2 and gates.py 3); the two acts by family, the light's take (unwind.py:35-74 fall_of, unspring.py:171-197 unsprung_end) against the matter's (unspring.py:88-105 wind_fall, 148-168 unspring_end); the setting's sea forms (assembly/setting.py: `sea` 4, `drift` 5); bobs.py:33 (a light never chimes into itself); trains.py:118-131 requiring the plane at (den, den); meshes.py:20 coupling_of; the word `light` itself stands once in the engine proper (assembly/setting.py) and 58 times in the Reader's modules (events.py 21, strikes.py 20, symmetries.py 9, gates.py 7, predicates.py 1), readers of the chart and no acts: whether the rule reaches them is the Boss's to put. David's (B), the two takes and the two seas as two acts each, is answered by this word: one act each.
- **R13. The integers' bound** (the law's "every integer within 128 bits", the owner's word of 2026-10-25, 04:1x UTC, ALGEBRA.md:76, 90 and 92; known, listed for completeness): One Big Bang's regulator time gear, 234 bits at the tick 48 and about doubling at each live tick of its two blinking Node-clocks, 3,372,178 bits at 80 (the Reader, comment 6448056770); the cycle setting's runaway of the swing pair (the Boss's 6416499848); named by the Boss as his item (a); the engine bounds no integer (no width, the owner's words of 2026-10-27, 04:0x and 04:4x UTC), so the law's sentence and the engine differ.

- **R14. The click reads its factors after the step** (David, DAVID-DISENGAGED-MESH.md, "a second finding"; against CL-S2's one moment): striking.py:326 `read = factors(clock, None, stopped)` takes the regulator's notches after the carry, while the step used the start's (tick.py:109 clock.start_factors); on the hole 15,942 of 45,000 Mesh ends differ between the two in 60 ticks, so the click's gearings, the winds at the tick's start and the vernier's pitches, mix two moments; not measured further; CL-S2's one moment would read the start factors there too (wave item 3 names the unwind's push alone).
- **R15. The engagement ignores the Mesh's factor** (David, the horizon finding; against BH-S1): striking.py:52-114 engage reads the two ends' windings and the stopped mask (:64, :71) and never the factor, so a pair fits across a Mesh whose start factor is 0 (a horizon on that axis); David's act, a disengaged Mesh engages nothing, moves no committed chart and moves the bang; the owner's word asked through the Boss.


**C. Two proposals read against the owner's words** (ledger row 236): David's (B) and the picture's row 10, the coupling min(spring, 1) in the code; his (C) and row 6, four named trains built in the engine from d and den; his (A) and row 7, small formulas of d.

**Withdrawn:** the close's coordinate order against the torus (the owner's word of 16:4x, "The result does not need to be a torus..."; ledger row 239).

**Not in the Boss's wave:** R1 to R6 and R11; the wave is the seven law changes of the law's last paragraph (R7 to R10 among them).

## 11. The register at 9e1f1a8be, the wave built (2026-10-27, 19:0x UTC)

The Boss's wave (ledger row 248) read whole: the 11 files of src it moved (265 insertions, 100 deletions) and the tests and records beside them; the counts by `tools/engine_gates.py` and by hand, the lines by the gate's own reading. The lines of sections 2 to 4 and 10 are those of the earlier heads; where the wave did not touch a file (tick.py, trains.py, meshes.py, regulation.py, assembly/piece.py, readings.py, core/) they stand; these are the current ones for the rest. The Boss answers by number: built, ruled or objects.

**The counts, unchanged from 5f8680de2:** numbers beyond 0 and 1, 37 in 13 files (assembly/cycle.py 21; assembly/setting.py 24 25 111 115; core/acts.py 15; core/rule3.py 126 136; core/spokes.py 7 8; gates.py 299 301; great_clock.py 30; meshes.py 124; reckoner.py 15 to 27 and 29; rim.py 7 8; run.py 26 27 27; swings.py 9; trains.py 15 16 17); identity reads, 32 in 8 files (setting.py 54 60 67 69 81; bobs.py 35 141; clock.py 61 62; run.py 205 227 261 277 357; striking.py 46 47 67 131 188 263 333; tick.py 67 279 290; trains.py 67 117 128; unspring.py 160 162 249 255 273); branches by `is`, 15 in 6 files (setting.py 54 60 69 81; bobs.py 35; clock.py 61; run.py 205; striking.py 46 67 131 188; unspring.py 160 162 249 255); family-name strings 0, floats 0, true divisions 0, no import of math or trigonometry. Src 6,462 lines in 22 top-level modules (165 more); the tests 6 files and 59 functions, the full check 112 passed. The names: `unsprung` stands three more times (bobs.py two, striking.py one; 57 against 54 by section 10's count), and the word `light` in the code of the engine proper 4 against 1 (bobs.py:33, 82 and 139 beside assembly/setting.py:70).

**Built by the wave, closed:**

- **R7. The take's sign:** unwind.py's closed form is removed; unspring.fall_of (47-76) finds the least count by comparisons (rule3.least_at) at which the window wind, read by hands.wind, falls by what is due; tests/test_rule3.py:249 reads every chime's fall as the window's wind before less after.
- **R8. The unspringing's excess:** unspring.unspring_end (181-204) carries `slack_was + fall - tallied` into the slack, signed; the unsprung hand's end (207-235) pays the slack first (`due = tallied - slack_was`, read_ends at unspring.py:160-161).
- **R9. The vernier:** draw.vernier (20-46) reads the neighbour's grip at `grips[(k - 1) ^ 1]`, R_ji, and its own clock's at the spring.
- **R10. The light's take at the tick's start:** unspring.unsprung_end reads its push at `clock.start_gears` (CL-S2's one moment for every unwind's push).

**Standing, with the current lines:**

- **R1. Five kinds of train known by role:** trains.py:117-131 (the unsprung hand by its ratio at (rim, rim), the four counts and the refusal), 62-69 drive_teeth by shape and :104 twin hands; assembly/piece.py:38; tick.py:66-67, 117-144 standard_rate, 233-274 carry, 276-298 advances; clock.py:94 and 252-253; readings.py:30-32 and 62-67; the identity counters above (the wave moved them and added none: bobs.py's read of the unsprung hand's place left the chime for light_lead, 141).
- **R2. Light's coupling:** meshes.py:20-23 coupling_of, read at tick.py:70, 162, 163 and 224; not touched by the wave.
- **R3. The dimension and the shapes typed:** core/spokes.py:5-8, trains.py:13-17, assembly/piece.py:38, core/rule3.py:14-17, features/stretch/__init__.py:12-16; the wave adds draw.py:33's `(k - 1) ^ 1`, the pairing of a clock's two spokes of one axis by the parity of the index.
- **R4. Numbers in the code:** the 37 above, the typed constants and the gate's free 0 and 1; the wave adds none and the count is the head's.
- **R5. Formulas beside Rule3's one, the integer sines, cosines and roots:** the 44 functions of section 4 (counted at 608d97134): core/rates.py:25 sine_rim, core/rule3.py:88 mesh_unit_of (the root by the bisection at 174), assembly/setting.py:105 raised_cosine, 139 rim_point, 160 angle_of, 168 angles_of, 185 running_rotation, assembly/cycle.py:25 cycle_angles, readings.py:35 standard_angle, hands.py:128 cosine_count; the wave removes unwind.fall_of's closed form and adds R16's.
- **R6. The enforcement looser than the rule:** tests/test_rule3.py:109-131 allow integers by file and exempt nine reader modules whole, the test at 140; the Boss's gate is the stricter.
- **R11. The shears:** regulation.py:15-19 stress_of is written every tick and read by no act (DAVID-TENSORS.md); the owner's word asked, 3 of row 249.
- **R12. The engine knows light:** the unsprung hand is the engine's name for it (the counters above); the take stands in two functions chosen by the hand's identity, unspring.read_ends (146-175: 160 and 162) and unwind_ends (238-258: 249 and 255) calling wind_fall (121-138) and unspring_end for a sprung hand and fall_of (47-76) and unsprung_end for the unsprung one; bobs.py:35 (a light never chimes into itself) and light_lead (139-142); trains.py:117-131; meshes.py:20; the setting's sea forms. The wave moved the take of the light onto the wind's own fall but kept the two functions.
- **R13. The integers' bound:** the law's "every integer within 128 bits" against the engine that bounds none; One Big Bang's regulator time gear 234 bits at the tick 48 and 3,372,178 at 80 (the Reader); the owner's word asked, 11 of row 249.
- **R14. The click reads its factors after the step:** striking.py:332 `read = factors(clock, None, stopped)`, the regulator's notches after the carry, while the step used the start's (tick.py:109 clock.start_factors); the wave's CL-S2 names the unwind's push alone; the owner's word asked, 10 of row 249.
- **R15. The engagement ignores the Mesh's factor:** striking.py:52-114 engage reads the two ends' windings and the stopped mask (64 and 71) and never the factor, so a pair fits across a Mesh whose start factor is 0 (DAVID-DISENGAGED-MESH.md; against BH-S1); the owner's word asked, 7 of row 249.

**R16. The wave's own additions against the owner's words** (new at 9e1f1a8be; none of it is the letter of the seven law changes, all of it is how they were built; the Boss rules by number):

- **(a) Cases by a number, the light by its number** (the generic clause, "there is no if"; the owner's words of 15:1x, 15:5x and 17:0x): assembly/setting.py:263 (`if s == 0` in set_even: a hand whose rim sine is 0 is counted by its wind at the target, any other by its sweep), :321 (`if sine == 0` in fitted, the same two counts for a packet), :372 (`sweeping = sine_rim(train.ratio[0], clock.rim) != 0` in set_packet: the target half the key against the hand's winding), and :249 and :270 (`senses = (1, -1) if sense == 0 else (sense,)`, a case by the sense 0). The sine 0 is the unsprung hand's by trains.py:117 (its ratio (rim, rim)), so the case names the light without its name.
- **(b) light_lead:** bobs.py:139-142 is a function of the engine's own named for the light (it reads the unsprung hand at :141 and its lead across its six Meshes at the tick's start, what arrives at each clock), read at :33 (bobs) and :82 (splits): the chimes' test of where light arrives; David's reading (row 247) is that the test is the head's own lay-back test, the lead over the six Meshes of the hand the take draws on, so with R12 built it reads the taken hand's lead, whichever hand.
- **(c) Two more integer roots by search** (R5; the owner's "no formulas, no sines, no cosines", "let them check how"): features/standard/__init__.py:53 (`twice = largest_below(...)`, the sine seed's root of (2 X)^2 (2 D - 1) div D^2) and bobs.py:103 (the split's collapse sets each gear to `largest_below` of v^2 times the summed sweeps over the picked sweep); the search is core/rule3.py's largest_below, the bisection by comparisons of the mesh unit's root, a root and not Rule3's one act.
- **(d) New formulas beside Rule3's one:** assembly/setting.py:209-221 carried_rest (the rest lay's one carry, `teeth * now - carries(teeth, rim) * numerator`), 224-230 rest_numerators (`base * ratio[0]` and `sense * base * sine_rim(ratio[0], rim)`), 247-250 swept (the senses' |sweep| summed), 253-298 set_even's two counts, 306-325 fitted, 348-397 set_packet; bobs.py:72-136 splits (the vernier's pick against the twins' sweeps and the collapse's formula); the owner's word of 15:5x allows Rule3 on tensors and vectors, so the question is which of these are Rule3's one act on arrays and which a formula; the Boss answers.
- **(e) The names:** `unsprung` three more times and `light` four against one (the counts above).

**Not in the Boss's wave, still open:** R1 to R6 and R11 to R16 (his task of 18:56 UTC names none of them); the owner's thirteen words (ledger row 249) are the Boss's list of what waits on the owner; row 249 marks 5 answered by the owner's word of 16:4x, 6 partly covered by his words of 15:5x and 17:0x, and 3, 7, 10 and 11 as the register's R11, R15, R14 and R13.

## 12. The register at 87a168c16, the great clock's bounds built (2026-10-27, 21:0x UTC)

The Boss's head (ledger row 254) read whole: the 7 files of src it moved (bobs.py, clock.py, meshes.py, predicates.py, readings.py, striking.py, tick.py; 25 more lines) and the tests, the three records and the new world beside them; the counts by `tools/engine_gates.py` and by the lister and the AST scan of the Scribe's scratchpad (lines.py, astscan.py). Files the head did not touch keep the lines of sections 10 and 11. The Boss answers by number: built, ruled or objects.

**The counts, unchanged from 9e1f1a8be:** numbers beyond 0 and 1, 37 in 13 files (section 11's lines); identity reads, 32 in 8 files (setting.py 54 60 67 69 81; bobs.py 35 163; clock.py 60 61; run.py 205 227 261 277 357; striking.py 46 47 67 134 191 266 336; tick.py 67 279 290; trains.py 67 117 128; unspring.py 160 162 249 255 273); branches by `is`, 15 in 6 files (setting.py 54 60 69 81; bobs.py 35; clock.py 60; run.py 205; striking.py 46 67 134 191; unspring.py 160 162 249 255); family-name strings 0, floats 0, true divisions 0, no import of math or trigonometry (the one `pow` at rim.py:28 stands from before). Src 6,487 lines in 22 top-level modules; the tests 6 files and 60 functions; the full check 113 passed (160 s on the merged tree).

**Closed by the build:**

- **R13. The integers' bound:** the three bounds (meshes.py:74, readings.py:21-22, tick.py:241-242) hold the one big bang within 111 bits through 1,000 ticks and the Reader's ga2 bang within 115 (the Boss's measure), and tests/worlds/world_bang.json holds 8 bangs in 40 ticks within 128 bits with the run back 20 of 20 (read in the full check); the law's "every integer within 128 bits" and the engine agree at the bang; the engine still bounds no integer by a width, the bounds being the full rate and the stretch's own size.
- **R14. The click reads its factors after the step:** striking.py:335 `read = clock.start_factors`, the step's own (tick.py:109).
- **R15. The engagement ignores the Mesh's factor:** striking.py:83-84 skips a Mesh whose start factor reads 0 (the jam cause `disengaged`, the count `refused_disengaged` at clock.py:32).

**Built earlier, closed:** R7 to R10 (section 11).

**Standing, with the current lines:**

- **R1. Five kinds of train known by role:** trains.py:117-131; assembly/piece.py:38; tick.py:66-67, 117-144 standard_rate, 233-274 carry (the drive's clamp at 241-242), 276-298 advances; clock.py:93 and 251-252; readings.py:30-32 and 62-67; the identity counters above.
- **R2. Light's coupling:** meshes.py:20-23 coupling_of, read at tick.py:70, 162, 163 and 224; not touched.
- **R3. The dimension and the shapes typed:** core/spokes.py:5-8, trains.py:13-17, assembly/piece.py:38, core/rule3.py:14-17, features/stretch/__init__.py:12-16, draw.py:33's `(k - 1) ^ 1`.
- **R4. Numbers in the code:** the 37 above; the head adds none.
- **R5. Formulas beside Rule3's one, the integer sines, cosines and roots:** the 44 functions of section 4 and R16's; the three bounds are clamps by comparison with no number beyond 0 (meshes.py:74, readings.py:21-22, tick.py:241-242), not formulas of a train, and are the owner's generic fixes of 18:5x as the Boss reads his word (ledger row 255).
- **R6. The enforcement looser than the rule:** tests/test_rule3.py:109-131 and 140; the head did not touch the whitelist.
- **R11. The shears:** regulation.py:15-19 stress_of written every tick and read by no act; next on the Boss's list (struck; the vernier reads their fine teeth, so the draws move).
- **R12. The engine knows light, and the take-free chime adds a place:** bobs.still_chime (65-91) names the unsprung hand by `rec0` (line 74, `clock.hands()[rec0]`) and calls fall_of, the light's take function, at no winding to choose its logged gear; beside `light_lead` (161-164, read at 33 and 104), bobs.py:35 (a light never chimes into itself) and the two takes by identity in unspring.read_ends (146-175: 160 and 162) and unwind_ends (238-258: 249 and 255); trains.py:117-131; meshes.py:20; the setting's sea forms.
- **R16. The wave's own additions against the owner's words:** (a) cases by a number at assembly/setting.py:263, 321, 372 and :249, :270; (b) `light_lead`, as under R12; (c) two integer roots by `largest_below`, features/standard/__init__.py:53 and bobs.py:125 (splits 94-158); (d) new formulas, assembly/setting.py:209-250, 253-298, 306-325, 348-397 and bobs.py:94-158; the head moved none of them.

**Not in the Boss's head, still open:** R1 to R6, then R11, R12 and R16 (his task of 20:54 UTC names the shears, the generic folds and the lead at the kick as next); the owner's words 1, 2, 4, 5, 8, 9 and 13 of ledger row 249 are answered by "Go for all of them" as the Boss reads it and are unbuilt (row 255).

## 13. The register at 0a3b16bc1, with the Boss's answers by number (2026-10-27, 21:4x UTC)

The Boss answered the register on #2187 (comment 6454163264, 21:35 UTC; ledger row 258) and built the generic folds at 0a3b16bc1 (row 257). His head read whole: the 22 files of src it moved (assembly/cycle.py, piece.py, setting.py; bobs.py; clock.py; core/acts.py, rule3.py, spokes.py; meshes.py; predicates.py; reckoner.py; striking.py; tick.py; trains.py), the tests, the six universe files and the three records; the counts by `tools/engine_gates.py` and the Scribe's lister and AST scan (lines.py, astscan.py). Files the head did not touch keep the lines of sections 10 to 12.

**The counts at 0a3b16bc1:** numbers beyond 0 and 1, 24 in 7 files (core/spokes.py 8, AXES = 3, the one in the engine proper, 14 before; the Reader's modules gates.py 299 301, great_clock.py 30, reckoner.py 15 to 27 and 29, rim.py 7 8, run.py 26 27 27, swings.py 9); identity reads of the unsprung hand 28 in 8 files (setting.py 49 55 62 64 76; bobs.py 161; clock.py 60 61; run.py 205 227 261 277 357; striking.py 46 47 131 188 263 333; tick.py 67 279 290; trains.py 69; unspring.py 160 162 249 255 273); branches by `is`, 13 in 5 files (setting.py 49 55 64 76; clock.py 60; run.py 205; striking.py 46 131 188; unspring.py 160 162 249 255); family-name strings 0, floats 0, true divisions 0, no import of math or trigonometry. Src 6,477 lines in 22 top-level modules; the tests 6 files and 60 functions; the full check 113 passed (155 s on the merged tree).

**The Boss's answers, with the Scribe's reading:**

- **R7 to R10:** built (9e1f1a8be). **R13, R14, R15:** built (87a168c16), the bounds' third, the stretch's own size in a tick, "the tick's resolution, and the owner's to weigh: asked".
- **R4:** built at 0a3b16bc1 in the gate's count (the engine's literals 14 to 1). The values stand as derived constants: SIDES = len(SIGNS) with SIGNS = (1, -1) typed (core/spokes.py:10-11), AXES + 1, AXES SIDES, QUARTERS = len(QUARTER); AXES = 3 typed (core/spokes.py:7-9) is the one left, under R3. The readers' 23 literals (reckoner.py 14, gates.py 2, rim.py 2, run.py 3, great_clock.py 1, swings.py 1) the Boss rules to stand, "the decoder's"; the owner's 15:5x word names the engine.
- **R6:** built. tests/test_rule3.py:109-113 `FILE_INTEGERS` holds spokes.py's 3 and run.py's 12, 24 and 60 alone; the nine readers stay exempt.
- **R11, the shears:** the Boss objects for now. The register's premise, "read by no act", is amended: they are read through draw.vernier's digits (every gear's fine tooth at the clock), and struck they break the polarization's mirror (the x and y sources part at the tick 6). Standing: regulation.py:15-19 stress_of; the click waits on David's reading of the draw.
- **R1 and R12, partly built:** the file holds the matter alone and the four fixed trains are built from the rim and Gamma (trains.rows_of, 93-102: the light `{"shape": HAND, "pair": [rim, rim]}` as row 0, the file's rows, the regulator at (rim - rim div Gamma, rim), the offset at (rim, rim), the ratchet of SIDES teeth); the role refusals of trains_of are gone; two branches on the light's identity became products by `coupling_of` (bobs.py:35, striking.py:67). Reading: the engine now builds the light itself, against the owner's 17:0x word; it still tells the unsprung hand from the rest by its number (trains.py:69 reads the hand at (rim, rim) for its drive teeth; the coupling's product is the same case in arithmetic); the 28 reads and 13 branches stand: the two takes (unspring.read_ends 146-175: 160 and 162; unwind_ends 238-258: 249 and 255), the light's pick of the fitted hands' hand (striking.py:46 and 131), the setting's seas (assembly/setting.py:49, 55, 62, 64, 76), clock.py:60-61, run.py, tick.py:67 and the take-free chime's naming of the unsprung hand (bobs.py:63-89, `rec0`, and fall_of at no winding on :73) beside `light_lead` (159-162, read at 33 and 102). The Boss: "two acts of the law each; they need the owner's word, one act for both moves the charts: to be asked."
- **R2:** ruled to stand ("coupling_of = min(spring, 1) is the coupling as one value of the ratio; the general form K / Gamma (Y-S1) is the owner's word"). Reading: against the owner's 15:5x word; read at six places now (meshes.py:20 defines; tick.py:70, 162, 163, 224; bobs.py:35; striking.py:67).
- **R3:** the Boss objects for now ("113 reads in 22 files; the twist, the cross and the curl are three-dimensional acts; next after the owner's word on R12"). Standing: AXES = 3, the loader's shapes (assembly/piece.py:40, shapes HAND and HAND + HAND alone, which David's one-gear mediator would need widened), trains.py's sizes REGULATOR and OFFSET typed by AXES, core/rule3.py:14-17, features/stretch/__init__.py:12-16, draw.py:33's `(k - 1) ^ 1`.
- **R5:** stands (the Boss: "one clock, three acts, every division the carry; the integer searches are comparisons by Rule3's carry; each formula's fold is David's derivation first"). The lines: raised_cosine (assembly/setting.py:100-110, now by the half turn's closure), carried_rest 204-216, rest_numerators 219-225, swept 242-245, set_even 248-293, fitted 301-320, set_packet 343-392, bobs.splits 92-156, the sine seed features/standard/__init__.py:53 and the three bounds' clamps (meshes.py:74, readings.py:21-22, tick.py:241-242), which carry no number beyond 0.
- **R16:** (a) the setting's cases by a number (setting.py:244, 258, 265, 316, 367) and (b) `light_lead`, with R12; (c) the two integer roots (features/standard/__init__.py:53, bobs.py:123) and (d) the formulas, with R5; (e) the names, with stage 2 of the names.

**The order of what stands, the Boss's:** R12 with R1 (the owner's word first), then R3, then R5.

**Asked of the owner (the Scribe, through the Boss's list):** R12 with R1 (one act for both takes, the light's pick of the fitted hands' hand and the seas: the charts move), the coupling's general form K / Gamma (Y-S1), the third bound (the stretch's tick resolution).

## 14. The register at 6a853217f, the held field built (2026-10-27, 22:5x UTC)

The Boss's head (ledger row 261) read whole: the 8 files of src it moved (assembly/piece.py, clock.py, events.py, gates.py, readings.py, run.py, tick.py, trains.py) and the new phenomena.py (320 lines), the tests, the new universe tests/worlds/universe_bang.json and the three records; the counts by `tools/engine_gates.py` and the Scribe's lister and AST scan. The Boss's answers of section 13 stand; files the head did not touch keep the lines of sections 10 to 13.

**The counts, unchanged from 0a3b16bc1:** numbers beyond 0 and 1, 24 in 7 files (section 13's lines; core/spokes.py:8 alone in the engine proper); identity reads of the unsprung hand 28 in 8 files (setting.py 49 55 62 64 76; bobs.py 161; clock.py 60 61; run.py 205 227 261 283 369; striking.py 46 47 131 188 263 333; tick.py 67 292 303; trains.py 68; unspring.py 160 162 249 255 273); branches by `is`, 13 in 5 files (setting.py 49 55 64 76; clock.py 60; run.py 205; striking.py 46 131 188; unspring.py 160 162 249 255); family-name strings 0, floats 0, true divisions 0, no import of math or trigonometry. Src 6,850 lines in 23 top-level modules; the tests 6 files and 61 functions; the full check 115 passed (185 s on the merged tree).

**Standing, with what the head changes:**

- **R1, a sixth kind of train by role (grows):** the held field is told from the rest by its `weight` (trains.py:34 and :123, `Train.weight`; tick.py:71, :106 and :227-229; run.py:284 and :297) and by the shape 1 with a ratio (trains.py:66; assembly/piece.py:40-44); the four fixed trains built by trains.rows_of (93-102) as in section 13.
- **R3:** the loader now admits the shapes 1, HAND and HAND + HAND (assembly/piece.py:40-44), the shape 1 meaning two things by the ratio (the ratchet by its teeth, the field by its ratio and weight); AXES = 3 and the rest as in section 13.
- **R5 and R16 (d), a formula beside Rule3's one (grows):** the field's source, the mass density SUM D |a|^2 div w (tick.py:239-240, the carry at :227-229), and the spring's rate read at the held load (readings.py:60-63); the owner's 15:5x word allows Rule3 on tensors (`hands.dot`), so the question is whether the source is Rule3's one act; for David and the Boss.
- **R11, the shears:** David's reading of the draw (22:08, row 262) is that the shears carry no mirror of their own and striking them only changed which draws the polarization's run met; the Boss's blocker, the polarization's mirror, is open against it.
- **The readers (new):** phenomena.py, a tenth reader, names the light by its number (phenomena.py:35, 221 and 252), copies the clock's winding formula (`windings_of`) and stands exempt from the integer and the word gates with the nine (tests/test_rule3.py:116-119).
- **R12, R2, R4, R6, R13 to R15:** as section 13; R12 with R1 first in the Boss's order.
- **New, David's (row 262):** the cube's 24 hold at 3 of 24 in the click on nature and the hole, the draw's digits mirroring about their origin; the one mirror, F48-S1's letter, is the owner's word.

**Asked of the owner, as in section 13, and one more:** R12 with R1; the coupling's general form K / Gamma (Y-S1); the third bound; and the remainder's one mirror about its origin (F48-S1).

## 15. The register at e41c51e6b, row 74 read at the clock (2026-10-27, 23:2x UTC)

The Boss's head (ledger row 264) read whole: the two files of src it moved (phenomena.py, 326 lines, 22 added and 16 taken; run.py, 397 lines, 2 added and 1 taken), the tests (the bang's test at the weight 2, the committed charts' SHOWN sets gaining 74, the bang test's room 26 lines, tests/worlds/universe_bang.json) and the three records; the counts by `tools/engine_gates.py` against 6a853217f and the Scribe's lister and AST scan. Sections 10 to 14 stand; files the head did not touch keep their lines.

**The counts, unchanged from 6a853217f:** numbers beyond 0 and 1, 24 in 7 files; identity reads of the unsprung hand 28 in 8 files; branches by `is`, 13 in 5 files; family-name strings 0, floats 0, true divisions 0, no import of math or trigonometry. Src 6,857 lines in 23 top-level modules (7 more than at 6a853217f); the tests 6 files and 61 functions; the full check 115 passed (178 s on the merged tree).

**Standing, with what the head changes:**

- **R1, the roles (a line more):** run.py:294's `odd` reads the offset's odd gears by role (`clock.train(OFFSET).gears[1:]`), the chart writer's second line of the kind beside `kick` at :293; the rest as in section 14.
- **The readers:** phenomena.py names the light by its number at :35, :227 and :258 (the lines :35, :221 and :252 of section 14, moved by six lines); its second difference a - 2 b + c is spelt with two b's (:140) and the span's two ticks as `t - 1 - 1` (:133), the gate counting no number in either; the reader exempt whole.
- **The weight 2, a setting by trial:** the universe file's weight is chosen among 3, 2 and none on the polarization's tally (the commit gives no derivation); with no field the polarization already reads on all three axes (144 of 570, 69 of 584 and 114 of 538 kicks read, the Scribe's run of the same bang) and row 9 reads NOT SHOWN, which at the weight 3 reads SHOWN: the weight serves the binding alone, and at the weight 3 it spoils the polarization's third axis (48 against 50).
- **Row 74's definition:** the own-axis tally's net agreement is 15, 14 and 14 percent of the kicks read at the weight 2 (25, 12 and 21 percent with no field); whether the kick's carry on its gear is the light or the kick's own landing is for David (DAVID-FOUR-PHENOMENA.md section 1).
- **The test's sample:** the bang test reads binding on 6 of 14 pairs at one tick (22 of 66 at the weight 3), above twice the board's own share; the 250-tick figures carry more (52 of 144 and 32 of 68).
- **R12, R2, R3, R5 and the others:** as section 14.
- **Lines moved by the head:** run.py after :294 by one line (the identity reads stand at 205, 227, 261, 283 and 370; the held field's `field` line at :298), phenomena.py after :133 by six (`windings_of` at 216-223); no other file.
- **reader-5 at 6ec4828c0 (23:13, 6a853217f and e41c51e6b merged), read at the same hour:** its src beyond the engine's is the Reader's readers (great_clock.py, reckoner.py, strikes.py and symmetries.py, 84 lines added and 43 taken since 0a3b16bc1, read at 22:1x) and one line of phenomena.py (the bound families' lines in row 76); the counts on that tree are the head's (24 numbers in 7 files, 28 reads in 8 files, 13 branches in 5, 0 floats, 0 true divisions; src 6,899 lines); not merged into engine-5.0-test.

**Verified by the Scribe's run:** the one big bang at 250 ticks at the weight 2, at the weight 3 and with no field, from tests/worlds/world_bang.json with the universe file's field edited, reads the Boss's tallies, fittings (410, 318 and 356), chimes (11,497, 11,548 and 12,564) and rows integer for integer.

**Asked of the owner, as in section 14:** R12 with R1; the coupling's general form K / Gamma (Y-S1); the third bound's tick resolution; and the remainder's one mirror about its origin (F48-S1).

## 16. The register at 13f58bb25, the close's books (2026-10-27, 23:3x UTC)

The Boss's head (ledger row 265) read whole: the four files of src it moved (striking.py 389 lines, +34; unspring.py 330, +21; reckoner.py 325, +4; strikes.py 399, unchanged in length), the tests (the books test, the control's counts, the committed charts' verdicts) and the three records; the counts by `tools/engine_gates.py` against e41c51e6b and the Scribe's lister and AST scan. Sections 10 to 15 stand; files the head did not touch keep their lines.

**The counts, unchanged from e41c51e6b:** numbers beyond 0 and 1, 24 in 7 files; identity reads of the unsprung hand 28 in 8 files (striking.py 46 47 131 188 297 367, the last two moved from 263 and 333); branches by `is`, 13 in 5 files; family-name strings 0, floats 0, true divisions 0, no import of math or trigonometry. Src 6,916 lines in 23 top-level modules; the tests 6 files and 62 functions; the full check 116 passed.

**Standing, with what the head changes:**

- **Two acts of the cross term (R1 and R12, the goal line's one act for every hand):** a merger's unspring.wind_cross (unspring.py:286) and a pair's striking.lay_window and lay_wind (striking.py:267 and :278) are two readings of one thing, the board's wind over the windows before less after less what was paid; the engine tells the two kinds of unwind by a test of the log, `"takes" not in unwind` (striking.py:260, beside the standing :236) and `len(reads) > 1` (unspring.py:278).
- **The log's `taken` (a reader's input changed):** the first end's logged `taken` carries the cross term (unspring.py:282, the slack at :281); row 73's reader (symmetries.py:307-338) reads that `taken` as the pair's share and its cause text says the excess is booked nowhere (:336 and :338), where gate 15 reads the same ends exact with the excess in the remainder; the decoder's rows 15 and 73 disagree on the same merger ends (378 of 482 ends exceed at 250 ticks), the Reader's table having read 73 SHOWN by the slack at 22:1x.
- **Measured, not derived (R5):** both cross terms are the board's wind read before and after over the windows (unspring.py:286-300, striking.py:278-292); the books close on the measure and the test's whole-board reading shows no wind moves outside the windows; whether one Rule3 act gives the term without the second read is for David.
- **The cross term's clock (the cube's 24):** the term lands at the first end's clock, `first = reads[0][0]` (unspring.py:280-281), by the list's order, and the remainders are what the draw reads; whether the same end is first under each of the cube's 24 is for David's harness to re-measure (3 of 24 as built, row 262).
- **R12, R2, R3, R5 and the others:** as section 14; the held field's lines as section 15.

**Verified by the Scribe's run:** the test's own identity (the board's wind lost against the chimes' booked plus the slack's rise at every click) on the bang's first 100 ticks from tests/worlds/world_bang.json: 100 of 100 clicks close on 13f58bb25, 78 of 100 on e41c51e6b (22 open: 15 with a merger and 7 with a pair birth and no merger), 210 fittings and 3,131 chimes at both; the bang at 250 ticks on 13f58bb25 reads the Boss's 382 fittings, 11,592 chimes, 31 numbered rows SHOWN and 6 in part, 15 SHOWN exact, 74 SHOWN (95, 160 and 61) and 76 SHOWN (35 of 145 and 26 of 26 pairs one mesh apart), with 73 and 75 NOT SHOWN.

**Asked of the owner, as in section 14:** R12 with R1; the coupling's general form K / Gamma (Y-S1); the third bound's tick resolution; and the remainder's one mirror about its origin (F48-S1).

## 17. The register at 42e9fb4af, R12's folds (2026-10-28, 00:2x UTC)

The Boss's head (ledger row 269) read whole: the six files of src it moved (assembly/setting.py, clock.py, run.py, striking.py, tick.py and unspring.py; 6,917 lines under src, one more) and tests/test_the_node.py; the counts by `tools/engine_gates.py` against 13f58bb25 and the Scribe's lister and AST scan. Sections 10 to 16 stand but for R12 and R2 below; files the head did not touch keep their lines.

**The counts:** numbers beyond 0 and 1, 24 in 7 files (unchanged); identity reads of the unsprung hand 18 in 7 files (28 in 8 at 13f58bb25): setting.py 49 55 65 77; bobs.py 161; run.py 205 227 261 283; striking.py 187 296 366; tick.py 292 303; trains.py 68; unspring.py 163 250 274; branches by `is`, 8 in 4 files (13 in 5): setting.py 49 55 65 77; run.py 205; striking.py 187; unspring.py 163 250; family-name strings 0, floats 0, true divisions 0, no import of math or trigonometry. Src 6,917 lines in 23 top-level modules; the tests 6 files and 62 functions; the full check 116 passed.

**Standing, with what the head changes:**

- **R12, the light known by its numbers (folded in part, bit for bit):** the pick of the fitted hands' hand and the jam (striking.py:46-47 and :130), the take's slack (unspring.py:161), the hole's drift (setting.py:63) and the cross term's clause (unspring.py:250) read by the couplings or struck; three dead reads struck (Tick.unsprung, clock.sprung and clock.winding_unsprung); what stands, the Boss's G1 (the take, unspring.py:163), G3 (the sea every chime draws on), G4 (the release on the light's first gear) and G5's rest (the setting's four, setting.py:49, :55, :65 and :77), moves the charts and waits on the owner's word and David's derivation; the engine proper holds 14 reads and 7 branches.
- **R2 grows:** `coupling_of` is called 13 times in 6 files, 6 in 3 at 13f58bb25 (bobs.py:35; run.py:372; striking.py:46, :47, :66 and twice at :130; tick.py:70, :166, :167 and :235; unspring.py:161; assembly/setting.py:63), as a product, a comparison and an index (tick.py:167); the owner's 15:5x word, no such thing as light's coupling, stands as the law.
- **SL-S1 as a selection rule:** the code's reading (striking.py:46-47 and :130), no sentence of the law, whose SL-S1 has the Mesh's one number name the fitted hands' hand.
- **Generalization beyond the worlds:** list_of picks among every HAND-sized hand at the coupling 0 for a coupled hand (a second such hand would move the pick off the light), and unwind_ends calls the recoil with a zero cross term for a two-ended unwind at the unsprung hand: neither in a shipped world, the suite, the charts or the bang.
- **From section 16, answered by David (ledger row 267):** (d) the cross term at the first end's clock parts the polarization's swap at the tick 11 on 13f58bb25, and booked at the fitting's own clock the swap holds (the mend unbuilt at 42e9fb4af); row 73's words are stale (the Reader reads 73 SHOWN by the signed remainder on the same 378 of 482 ends, row 268); (a) and (c) answered by a one-act letter, each end read on the great clock as the earlier ends leave it, the Boss's kept unless the owner wants the single read; R11 follows the cross term's clock, not the one mirror.
- **David's bang at 1,000 ticks (ledger row 270):** the great clock holds (200 exact returns, 13 bits) while row 74 fades as built (in part at 500, NOT SHOWN at 750 and 1,000) and row 76 fails at 1,000 by five chimes, holding with the cross term at the fitting's own clock; the law's 250-tick reading of row 74 is dated so; the world that stops at tick 104 is asked of the Boss.
- **R5, R1, R3 and the others:** as sections 14 to 16.

**Verified by the Scribe's run:** the bang at 250 ticks from tests/worlds/world_bang.json on 42e9fb4af against 13f58bb25: the whole chart equal (the log, the clock lines, the counts, the turns, `gapped`, `planes` and the run back 20 of 20; the rows equal but for their milliseconds) and the reading equal to the character.

**Asked of the owner, as in section 14, with David's letters:** R12 with R1 (its rest, G1, G3, G4 and G5); the coupling's general form K / Gamma (Y-S1); the third bound's tick resolution; the remainder's one mirror about its origin (F48-S1, with its price: the fold silences the hole and the swap parts at the tick 9); the field's reach to the regulator's spring; a composite family for fusion.

## 18. The register at e910698f9, the swap's images (2026-10-28, 01:0x UTC)

The Boss's head (ledger row 272) read whole: the five files of src it moved (events.py, phenomena.py, run.py, symmetries.py and unspring.py; 6,912 lines under src, five fewer), the tests (the polarization test's swap at every tick, row 73's test, the control's counts), tools/tests_shape.py and the three records; the counts by `tools/engine_gates.py` against 42e9fb4af and the Scribe's lister and AST scan. Sections 10 to 17 stand but for what is closed or changed below; files the head did not touch keep their lines.

**The counts, unchanged from 42e9fb4af:** numbers beyond 0 and 1, 24 in 7 files; identity reads of the unsprung hand 18 in 7 files (setting.py 49 55 65 77; bobs.py 161; run.py 205 227 261 283; striking.py 187 296 366; tick.py 292 303; trains.py 68; unspring.py 163 250 274); branches by `is`, 8 in 4 files (setting.py 49 55 65 77; run.py 205; striking.py 187; unspring.py 163 250); `coupling_of` 13 calls in 6 files; family-name strings 0, floats 0, true divisions 0, no import of math or trigonometry. Src 6,912 lines in 23 top-level modules; the tests 6 files and 62 functions; the full check 116 passed.

**Closed:** section 16's (b), the first end's logged `taken` carrying the term while row 73's reader read it as the pair's share, rows 15 and 73 disagreeing (row 73 now reads every merger end by its own book, its stale words struck), and (d), the cross term's clock (unspring.py:280-282, the end at the fitting's own clock by `.index(at)`, the swap of x and y an exact image through its 12 ticks).

**Standing, with what the head changes:**

- **Two spellings of one meaning:** the gear's momentum W (now - before) + fine - mid(W) stands in the writer (run.py:294) beside the impulse's own (tick.py:216).
- **Rows 15 and 73 read one identity,** which the remainder is defined by at a merger end (unspring.py:191 writes the slack as the slack plus the fall less the booked, the cross term added to the taken and to the remainder alike): both can fail only by a bookkeeping error; whether the carried excess is paid to light later is read by no row.
- **The weight's reason is gone:** under the momentum reading row 74 reads on all three axes at the weights 2 and 3 and with no field; the weight 2 stands on row 76 (both heavy families bound at 2, gapped 1 alone at 3) and on row 9 (SHOWN at the weight 3 alone).
- **Row 74's reading changed in the commit that would have lowered it** (the stride's reading 1 of 3 with the term moved), on David's analysis; the momentum reading holds on all three axes through 750 ticks and fails the z axis at 1,000 (228 against a cross 122); row 76 holds at every cut to 1,000 (gapped 1 throughout, gapped 2 at 250 alone).
- **For David, the order effect that stands:** the two images' credits at the tick 5 of the polarization world split their takes one unit apart (684 and 278 against 685 and 277), two credits of one click at image clocks read in the list's order.
- **R2, R12's rest, R1, R5 and the others:** as section 17.

**Verified by the Scribe's runs:** the bang at 250 ticks on the head at the weight 2, at 3 and with no field, and the one chart of 1,000 ticks cut at four ticks (the Boss's counts and tallies integer for integer; the cuts as in row 272).

**Asked of the owner, as in section 17:** R12 with R1 (its rest, G1, G3, G4 and G5); the coupling's general form K / Gamma (Y-S1); the third bound's tick resolution; the remainder's one mirror about its origin (F48-S1, with its price: the fold silences the hole and the swap parts at the tick 9); the field's reach to the regulator's spring; a composite family for fusion.

## 19. The register at 97e5b3fd6, the great clock through its bottom (2026-10-28, 01:1x UTC)

The Boss's head (ledger row 274) read whole: the one file of src it moved (tick.py, 9 added and 3 taken; 6,918 lines under src, six more), tests/test_the_record.py (the bang at 40 times its quanta), tools/tests_shape.py and the hole's chart; the counts by `tools/engine_gates.py` against e910698f9 and the Scribe's lister and AST scan. Sections 10 to 18 stand but for what is added below.

**The counts, unchanged from e910698f9:** numbers beyond 0 and 1, 24 in 7 files; identity reads of the unsprung hand 18 in 7 files; branches by `is`, 8 in 4 files; `coupling_of` 13 calls in 6 files; family-name strings 0, floats 0, true divisions 0, no import of math or trigonometry. Src 6,918 lines in 23 top-level modules; the tests 6 files and 63 functions; the full check 117 passed.

**Standing, with what the head changes:**

- **The floor at the symptom:** Tick.end_teeth (tick.py:289) reads the mean teeth of the tick's start where the end's are not above 0 (`np.where`, the idiom of tick.py:78 and :108); the bound for the whole step, |X_new - X_now| <= X_now, and a floor that keeps a stretch off its bottom within a tick stand open, the Boss names them for David; bound (3) stays asked of the owner (row 256).
- **David's R12 rest (ledger row 273):** the take as one act by the coupling (the payer's own quantum given back at -1: the whole notches at c = 1, one notch at c = 0), the chime's payer, the release and the setting's seas fold by the coupling bit for bit and are unbuilt in the engine; the local book (each child paid at its own end) moves the charts, for the owner; two uncoupled hands would split the release and the chime's payer between them; the identity branches that remain (unspring.py:163 and :250, setting.py:49, :55, :65 and :77, striking.py:187, run.py:205) would become reads of the coupling, R2 growing once more.
- **The weight (ledger row 273):** the bang decides none; the weight 2 stays on e910698f9, its derivation open and the owner's; the unit (one weight, no key) keeps the binding on 42e9fb4af and loses it on e910698f9.
- **R2, R12's rest, R1, R5 and the others:** as sections 17 and 18.

**Asked of the owner, as in section 18, with the local book, the weight's derivation and the bound for the whole step.**

## 20. The register at the Boss's sync, 97e5b3fd6 with the night's comments (2026-10-28, 02:2x UTC)

The sync read whole: the engine head 97e5b3fd6, unchanged since 01:03 UTC (scribe-5 28063fe6d holds it, 0 behind, the source and tests of the tree equal to the engine head's), and every comment after the Scribe's line of 01:15 UTC: David's of 01:15, 01:24 and 01:44 (toys-5 95573578a, 536d7ea9b and ad088678e: DAVID-THE-STRIKES-ORDER.md, DAVID-TEMPERATURE.md and DAVID-THE-BINDING-WINDOW.md, with their checks), the Reader's of 01:25 (reader-5 e5ce3c41, ce19abf2 and 763bba04) and the Reader's question of 02:14 to the Boss (ledger rows 275 to 279). Sections 10 to 19 stand but for what is added below.

**The counts, unchanged from 97e5b3fd6:** numbers beyond 0 and 1, 24 in 7 files; identity reads of the unsprung hand 18 in 7 files; branches by `is`, 8 in 4 files; `coupling_of` 13 calls in 6 files; family-name strings 0, floats 0, true divisions 0, no import of math or trigonometry. Src 6,918 lines in 23 top-level modules; the tests 6 files and 63 functions; the full check 117 passed (the merged tree's source unchanged since 73f3b3718, the suite not run again; the engine gates and the documents' six gates hold on the tree).

**The Scribe's runs of this sync** (the tree 28063fe6d, the bang at 250 ticks, each run back 20 of 20): David's six seeds on the head's bang (transposed 324 fittings, shifted a column 420, cz 3 398, the mirror 1 380, 4,000,000 quanta 341, with the merger ends 428, 530, 566, 572 and 456 each exact by the signed remainder, row 74 on all three axes on all six, row 76 NOT SHOWN under the mirror alone) and the window's seeds of 1.5, 3 and 20 million quanta (207, 282 and 262 fittings; row 76 NOT SHOWN at all three, SHOWN at 4 million), the tables of DAVID-THE-BINDING-WINDOW.md and the matter's wind of DAVID-TEMPERATURE.md reproduced to the integer, and with the committed bang's events and the shifted bang's events mapped by the translation equal at every tick through 79 and parting at tick 80 by one birth and one credit.

**Standing, with what the comments change:**

- **The click's order (ledger row 275):** the push's cross term is the live great clock's push less the start's (unspring.py:246-256, the docstring's own words), so the click reads a second moment for the push alone and the clocks' index order enters; the run is no image of itself under a translation of the seed (the events through tick 79, David's state through tick 2) nor under the transposition of its p1 (324 fittings against 450), the books closing in each; David's letter, every take on the tick's start board with each clock's remainder booking what its wind gains or loses beyond the reads, is unmeasured beyond its first step and the owner's to weigh with the cube's 48.
- **F48-S1's one mirror (row 275):** David corrects his harness (the ratchet's fine tooth, the clock's turnover parity, is not mirrored; its reversal is the flip) and accepts the Boss's fold about each gear's own origin as the exact form; T0 and T4 are the Boss's trial builds (T4 at his local 639c3c7ff, unpushed), the whole 48 against the owner's 24 with chiral reflections, answered by the owner's word through the Boss of 02:0x UTC, in David's rendering of 02:2x UTC: the 24 is the target (section 21).
- **The crash (rows 274 and 275):** David keeps the reading at the start's teeth; the whole-step bound and the floor within the tick are the owner's (bound 3's kind).
- **Row 75 (row 276):** the row reads a classical equipartition where a capped family's law is an occupation against 1/2; the light holds its seed's spectrum and the matter does not take its temperature within 50 bangs; on my five seeds the row reads NOT SHOWN but at 3,000,000 quanta (SHOWN in part, the spread narrowing with no common mean).
- **Row 76 (row 278):** the verdict is no law of the heat (SHOWN at 4, 5, 10 and 30 million of 13 seeds), a pair counted at every chime and the row reading whether a birth's two children both chime where laid (46 of the 53 distinct pairs one mesh apart); the law of nuclei would need three acts the bang lacks (the matter taking the light's heat, a heavy bob that moves, the cooling).
- **The Reader (row 277):** 47 of 77 SHOWN, 33 derived, the one big bang at 32 rows SHOWN and 6 in part, all sixteen readings byte for byte those of e910698f9; the question of 02:14 on the commits' identity is the Boss's (row 279).
- **As section 19:** R2, R12's rest, R1, R5, the local book, the weight's derivation (the bang decides none), row 73's one reader (the engine's decoder keeps Chart.ends, the Reader's page slack_of), the held field's role and formula, the seed that stops at tick 104.

**Departures to name for the Boss, new at this sync:** (a) the push's cross term is read on the live board where CL-S2 reads every take on the tick's start board (unspring.py:246-256); (b) the run is covariant neither under a translation nor under the transposition of the seed beyond its first ticks, the books closing in each; (c) rows 75 and 76 read a classical equipartition and a count of chimes per pair, readings that are the Boss's and the Reader's to change on David's letters; (d) the Scribe's pointer spelt the one mirror at every fine tooth and David excepts the ratchet's (pointer amended, the law's verbatim sentence unchanged).

**Asked of the owner, as in section 19, with the order-free click (the 24 being the target by his word through the Boss, the cube's 48 for the reflections), row 76 by distinct pairs and whether the bang is to exchange heat with the matter and cool.**

## 21. The register at 02:5x UTC, David's order-free click and mirror (2026-10-28)

The two comments since the sync of section 20: David's of 02:28 (toys-5 b666e0386, DAVID-THE-ORDER-FREE-STRIKE.md) and of 02:33 (toys-5 e1400bddf, DAVID-THE-MIRRORS-FITTING.md), ledger rows 280 and 281; the engine head 97e5b3fd6 unchanged, no push of the Boss since. Sections 10 to 20 stand but for what is added below.

**Corrected from section 20:** T0 to T4 are not spellings of a note the Scribe could not find; they are the Boss's trial builds of the one mirror (T4 at his local 639c3c7ff, unpushed), by David's DAVID-THE-MIRRORS-FITTING.md; row 275, the law's pointer and section 20 say so. The owner's word of 02:0x UTC through the Boss, in David's rendering, "the 24 is the target", is a relay, recorded as the Boss's line and not as the owner's direct word.

**The Scribe's runs of this register** (the tree 28063fe6d): the no-field control reproduces on my own chart of the bang without the field (250 ticks): fittings by line 33, 34, 50 and 240 and chimes by line 12,591 on the zero line alone, his numbers to the integer; the cycle setting (world_ga2.json) reads 64 fittings at tick 2 and 1,216 lay jams by tick 20, his numbers; world_nature.json reads its first fitting at tick 5, and my count of its credit events is not his chimes (not reconciled); the source lines he cites (striking.py, unspring.py, bobs.py) read as he says.

**Standing, with what the comments change:**

- **The click's two moments (row 280):** the jam reads the start board and the unwind reads the live board, the order entering by the sorted fittings and the indexed chimes (bobs.py:47); 5,319 of 17,156 end reads of the bang's first 100 ticks see a window an earlier unwind wrote (his harness); the order-free letter (every read on the start board, one take per clock and hand, the cross terms booked clock by clock in the remainders, a negative remainder the light's debt) is spelled and unbuilt.
- **The reflection (row 281):** a reflection's image of a fitting is the fitting at the image clock with its two children exchanged, as the click already makes it (264, 72 and 192 fittings through the images, at the setting, the cycle and the bang); the hands' image is z to -conj z; the twelve gear's fold alone parts at the first fitting.
- **The binding control (row 281):** without the held field the heavy families are laid and never chime (my chart: 34 and 50 fittings, all 12,591 chimes on the zero line); T4's heavy chimes without the field, its cycle setting's 64 lay jams and its quiet chiral are to be traced in its diff, T4 being a local build.
- **As section 20.**

**Departures to name for the Boss, new:** (a) the click's two moments (row 280, as section 20 (a)); (b) T0 to T4 are builds the Scribe cannot read (local, unpushed); (c) the owner's "the 24 is the target" reaches the Scribe by David's rendering alone.

**Asked of the owner, as in section 20, and his direct word on the 24 as the target.**

## 22. The register at the owner's names, the click kept and the Clock-node (2026-10-28, 03:0x UTC)

The owner's direct word of 02:4x UTC to the Scribe (ledger row 282): the name click stays and a node is called clock-node. The documents' prose was renamed in one pass (3,427 places strike to click, 4,728 places Clock to Clock-node), the dictionary page CLOCK_WORDS.md amended; the engine head 97e5b3fd6 unchanged, no push of the Boss since 01:03 UTC. Sections 10 to 21 stand but for the words below, which the pass renamed.

**Departures and questions to name for the Boss, new:** (a) the code spelling of the two names (the class Clock, striking.py, strikes.py, the identifiers and the chart's keys named strike) is the Boss's; the documents hold the tree's names in code spans until his push; (b) the lowercase word clock naming a node in running text stands, for the Boss's word or the owner's; (c) the prose spelling Clock-node follows the law's proper nouns Mesh and Spoke.

**Asked of the owner, as in section 21, and whether the lowercase word clock for a node is to become clock-node too.**

## 23. The register at 03:1x UTC, David's Bell build and the owner's leave (2026-10-28)

David's comment of 03:00 UTC (#2187 comment 6459479329, ledger row 283): the owner's words to him of 02:50, "Contradict a word of mine if needed in the solution", and of 02:59, "Sync with the Boss. Build the above click solution locally. Make sure it works. Then give him OK." (in David's rendering); his solution that keeps locality for Bell (a fitting's two children carrying one open axis to the first click of either) is built in a local worktree of 97e5b3fd6, unpushed; the engine head 97e5b3fd6 unchanged, no push of the Boss since 01:03 UTC. Sections 10 to 22 stand but for what is added below.

**Standing, with what the comment changes:** the law holds locality and no sentence changes; the second child's record written at the first click is the departure David names against the owner's word of 2026-10-25, 08:02 UTC, to be read by the Boss against locality; David takes the name click.

**Departures to name for the Boss, new:** (a) the open-axis solution writes the second child's record at the first click in the great clock's forward run (row 283), inside the cones when read along them; the owner's leave covers a contradiction of his word, the Boss's read of the build against Postulate 1 and **Only local** stands before the OK.

**Asked of the owner, as in section 22, and whether the open axis is the locality he meant.**

## 24. The register at the owner's measures and kinds of click (2026-10-28, 03:2x UTC)

The owner's direct words of 03:1x UTC (ledger row 284): what the speed c and the length of the link are in the language of the clocks, a definition for each kind of click, and "Sync with the Boss." The two kinds of click stand in the law (**The two kinds of click**, his sentences verbatim) and in HIGHLIGHTS.md; the speed and the length stand in CLOCK_WORDS.md as the law's own lines in clock words (the causal speed one Mesh per tick, light 1 / sqrt 3 of a Mesh per tick, the Mesh the ruler, the Node-clock's rate twice); the engine holds both kinds as built (`bobs.bobs` the whole, `bobs.splits` the split). The engine head 97e5b3fd6 unchanged, no push of the Boss since 01:03 UTC. Sections 10 to 23 stand but for what is added below.

**Departures and questions to name for the Boss, new:** (a) the letter c names light's speed and the load in the law; (b) the vernier is read by the fitting and the unspringing too (striking.py:107, :196), where the owner's sentence makes the split click the only place a choice enters, so which kind a fitting is, and whether the plane read at a fitting is a choice, is asked; (c) whether the twins upper and lower of the owner's sentence are the twin pair of `bobs.splits` alone or also the two children of a fitting laid on a twin pair is asked.

**Asked of the owner, as in section 23, and whether the fitting's plane read from the fine teeth is a choice in his sense.**

## 25. The register at the owner's word node-clock (2026-10-28, 03:3x UTC)

The owner's direct word of 03:2x UTC to the Scribe (ledger row 285): "node-clock. So they won't be confused with clock". His word of 02:4x ("a node be called node-clock and not only clock") had reached the documents as Clock-node (section 22), the order the Scribe had rendered it in; his Hebrew has the node first. The documents' prose was turned in one pass, 4,752 places Clock-node to Node-clock (the law 3,256, ENGINE.md 194, the ledger 450, HIGHLIGHTS.md 183, README.md 52, CHANGELOG.md 4, llms.txt 18, FOLLOW_UP_PAPERS.md 5, FURTHER_RESEARCH.md 495, the report 10, CLOCK_WORDS.md 85); the two names are of one length, so no line, offset or link moved, and every file read with the swap reversed equals the file before. Kept as written: code spans, paths, file, branch and hypothesis names, the former-name quotes, the Reader's generated blocks, and the records of the 02:4x naming (row 282, the CHANGELOG's entry of 02:4x, section 22 above). The dictionary page, the law's passage on the renaming and HIGHLIGHTS.md's were amended by hand, tools/numbers.json's one canonical form changed with the text, and the six gates hold.

**Departures and questions to name for the Boss, as in section 22:** (a) the code spelling (the class Clock to NodeClock or his own choice, striking.py, strikes.py, the identifiers and the chart's keys named strike, the Reader's keys) is the Boss's; (b) the lowercase word clock where it names a node in running text is the confusion the owner names, and this pass did not read those places one by one; (c) David's files write clock-node, the order the owner has turned; (d) the Reader's generated blocks still carry Node (9 places) until the Boss's push.

**Asked of the owner, as in section 24, and whether the lowercase word clock for a node is to become node-clock too.**

## 26. The register at the owner's request for the postulates as one clock (2026-10-28, 03:4x UTC)

The owner's direct request of 03:3x UTC to the Scribe (ledger row 286): a wording for the postulates, the world built of clocks that make a kind of system of a great unifying clock. The Scribe's draft is SCRIBE-POSTULATES-AS-ONE-CLOCK-1.md beside this report: a picture over the postulates, the four postulates in the owner's titles with the great clock in their bodies, and a paragraph of what the four make (the clauses that already say how many clocks are one), each sentence's ground in the law named in a table; the law's postulates stand unchanged until his word. No src is read or moved; the counts of the engine stand as in section 19.

**Departures and questions to name for the Boss, new:** none in the engine. **Asked of the owner:** (a) whether Postulate 3's title is to read one Mesh per tick at most (the law's light is 1 / sqrt 3 of a Mesh per tick, below the causal speed); (b) whether the picture's last sentence stays; (c) whether the paragraph of what the four make stays a consequence; and, as in section 25, whether the lowercase word clock for a node is to become node-clock too.

## 27. The register at the owner's unifying of the two speeds (2026-10-28, 03:5x UTC)

The owner's direct request of 03:5x UTC to the Scribe (ledger row 287): unify the causal speed and the speed of light. The draft of section 26 is amended: light's hand on the law's [1, 1] train (cos omega the mean of the three axes' cos k) crosses 1 / sqrt 3 of a Mesh per tick in a straight line in every direction, c, and, counted in Meshes, 1 / sqrt 3 along an axis, 0.82 along a face diagonal and exactly 1 along the cube's diagonal at every wavelength, and never more elsewhere (checked on 400,000 random wave vectors, the largest 1.0000, and by the Cauchy inequality written in the draft), so the causal bound is light's own speed counted in Meshes along the diagonal. The numbers agree with the law's own (**The lattice constants**: 1 / sqrt(3) and the bound 1; **The click writes on the lattice**: 1 / sqrt(3) along an axis, 0.82 along a face diagonal, the front keeping rate along the body diagonal). The arithmetic is the Scribe's; no src is read or moved.

**Departures and questions to name for the Boss, new:** none in the engine; **to check before the sentence enters the law (the Boss and David):** the Mesh-count speed of light at most 1 at every wave vector and exactly 1 along the diagonal, and a gapped train's at most num / den. **Asked of the owner:** whether the caveat of the axis (the word's one Mesh per tick is sqrt 3 times light's straight-line speed, no hand carries it and no click measures it) stands in the postulate or only in the clause; and, as in section 26, the questions (b) and (c) and whether the lowercase word clock for a node is to become node-clock too.

## 28. The register at the owner's choice of the full form (2026-10-28, 04:0x UTC)

The owner's direct word of 04:0x UTC to the Scribe (ledger row 288): "The full one.", on whether the caveat of the axis stands in Postulate 3's text. The draft of sections 26 and 27 is amended: Postulate 3 says in a third sentence that along an axis a bare word crosses a Mesh in one tick, sqrt 3 times light's straight-line speed, that no hand carries it and no click of nature's measures it, and that what a bob measures of another by clicks never exceeds c; the sentence says only what **The lattice constants**, **The measured speed** and **Only clicks against clicks** already say. No src is read or moved.

**Departures and questions to name for the Boss, new:** none in the engine; the check of the two derivations (section 27) stands. **Asked of the owner:** whether the whole wording is to enter docs/ALGEBRA.md now, the former text kept by name and dated.

## 29. The register at the owner's word to enter the wording, only what is new (2026-10-28, 04:1x UTC)

The owner's direct word of 04:1x UTC to the Scribe (ledger row 289): there is no need to keep an old wording, always only what is new. The wording of the postulates entered docs/ALGEBRA.md, **The postulates**: the picture over the postulates, Postulates 1 to 4 in their new bodies (Postulate 3 in three sentences, the second and third derived from the dispersion of light's train) and the paragraph of what the four make; the old bodies are not kept. The law's head and the postulates' head now say that a changed line holds its new wording alone; the 145 notes of the form (the former "...") and the closing section **The former clauses, kept by name** stand as they are until his word. SCRIBE-POSTULATES-AS-ONE-CLOCK-1.md keeps the derivation and the table of grounds. No src is read or moved.

**Departures and questions to name for the Boss, new:** none in the engine; the Boss's and David's check of the two derivations of Postulate 3 (section 27) is asked in the hour's line, and the Boss reads every push against the new postulates by name. **Asked of the owner:** whether the 145 notes and the closing section are to be removed now, and, as in section 25, whether the lowercase word clock for a node is to become node-clock too.

## 30. The register at David's Bell click (2026-10-28, 04:3x UTC)

David's comments of 03:45, 03:49 and 04:1x UTC (ledger row 290; toys-5 9edc6a479 and 5f692fbf7): the click solution built on 97e5b3fd6, the integer cosine of the first form replaced on the owner's order of 04:01 UTC (in David's rendering) by the twins turned by an integer quaternion and split by their own draw. The patch (+115 -2: bobs.py bell_answers, bell_turn and _bell_index, striking.py one call, predicates.py row 56) applied in a scratch worktree: the engine gates hold against 97e5b3fd6, the counts unchanged (24 numbers in 7 files, identity reads 18 in 7, branches 8 in 4, no float, no true division, no cosine, no sine, no root, src 7,031 lines), the suite not run. The rule alone, rerun on integers with fair draws and no board, gives S = -2.824 and -2.828 (Born's -2.8284).

**Departures and questions to name for the Boss, new:** the effect is local as built (the click of a child is recognised only at the Node-clock where the child was laid, so a pair's two clicks stand one Mesh apart, inside each other's cones, and S above 2 tests nothing about locality); (a) the form is not local: a module-level index of the whole log keyed by id(clock), the setting picked by the global count of answered clicks, a pass over the strike's log slice, and nothing that refuses a far partner once children are set moving apart (David's own Locality item); (b) the phenomenon is in the rule and not in the great clock, the quaternion turn an integer act outside Rule3 and the singlet (1, 0, 1, 0) typed into the code; (c) the law holds no sentence that a detector is a turn of the twins; (d) the law's own route (**The meeting's reading**) is not the route built. **Asked of the owner, directly:** whether the correlation may live in the rule or must come from the twin hands' own state read through the Mesh.

## 31. The register at the owner's request for the law of the 24 (2026-10-28, 04:2x UTC)

The owner's direct request of 04:2x UTC to the Scribe (ledger row 291): whether the 24 that the Boss and David are working on can enter the law as a kind of law, and its name. The proposal is SCRIBE-THE-24-AS-LAW-1.md beside this report: the clause **No direction is special**, a law not to be crossed (the step commutes with each of the cube's 24 turns, bit for bit, the click included; the reflections not asked), the theorem of **The cube's symmetry** at the 24 turns, with F48-S1's one mirror about the origin as its letter. The state read: 3 of the 24 turns run alike in the click as built, the step keeps all 24, F48-S1 derived and unbuilt, T0 and T4 the Boss's trial builds (unpushed); the engine head 97e5b3fd6 unchanged since 01:03 UTC; the Boss's session on "Rerunning the full check after the refactor", David's on a local derivation without cosine. No src is read or moved.

**Departures and questions to name for the Boss, new:** none in the engine; the 24 stands at 3 as built, a bug and not a gap (row 262). **Asked of the owner:** the 24 in place of the 48 as the law's claim, the kind and the name; **asked of the Boss and David in the thread:** the state now, whether the text says what is built, the tag.

## 32. The register at the owner's checks of 04:3x UTC (2026-10-28)

The owner's direct words of 04:3x UTC to the Scribe (ledger row 292): David's Bell click checked again, the recommendation stated plainly, and the code read for numbers, whole-number operations only and no cosine, sine or circularity that makes phenomena happen; a violation told to the Boss and to him, and no postulate or law changed without his word. Checked: the effect of David's patch is local as built and its form is not (section 30). The head 97e5b3fd6 stands as at section 19 (24 numbers beyond 0 and 1 in 7 files, 18 identity reads in 7, 8 branches in 4, no float, no true division, no math or trigonometric import, the one pow at rim.py:28); an independent read of every file of src under the owner's five rules runs beside the Scribe's own. No src is moved.

**Departures and questions to name for the Boss, new:** those of section 30; the independent read's findings are added as they come. **Asked of the owner:** his word on the two recommendations (the Bell click only in a local form; the 24 as the law No direction is special).

## 33. The register at the owner's word on the 24 (2026-10-28, 04:4x UTC)

The owner's direct word of 04:4x UTC to the Scribe (ledger row 293): the 24, and the law's name with the 24. Entered in docs/ALGEBRA.md as the law not to be crossed **The cube's 24 turns hold** (the step commutes with each of the cube's 24 turns, bit for bit, the click included; the reflections not asked); the code departs as built, holding 3 of the 24 in the click, a bug and not a gap, and F48-S1's one mirror about the origin is the mend, derived and unbuilt. The step's theorem at the 48, the findings on parity as findings of the step and ENGINE.md's tests of the 48 images stand as they are until the Boss's code moves. No src is read or moved.

**Departures and questions to name for the Boss, new:** none beyond the click's 3 of the 24 (row 262); **asked of the Boss and David in the thread (comment 6460557629):** the state now (T0 or T4, the refactor), the tag, and whether the findings on parity leave once the click is chiral. **Asked of the owner:** nothing new on the 24.

## 34. The register at the owner's prohibition of circularity (2026-10-28, 04:5x UTC)

The owner's direct words of 04:5x UTC to the Scribe (ledger row 294): the recommendation on David's Bell click is mandatory (a local form, the correlation from the twins' state), circularity that makes a phenomenon happen is a general prohibition in the code, a script reads every push, and the existing code is checked. Entered in docs/ALGEBRA.md as the law not to be crossed **No circularity that makes a phenomenon happen**. The script tools/derivations/open_items/scribe_scan.py ran on the head 97e5b3fd6: 166 hits in 36 files that stand (24 numbers beyond 0 and 1, the one pow(a, d, n), 21 state hits, 124 circular words), the numbers agreeing with the Boss's counter; on David's twins patch 6 new hits. The existing code departs at the integer sines, cosines, angles and roots of R5 (core/rates.py sine_rim, core/rule3.py largest_below and its callers, assembly/setting.py raised_cosine, rim_point, angle_of, angles_of, running_rotation, assembly/cycle.py cycle_angles, readings.py standard_angle, hands.py cosine_count). No src is moved.

**Departures and questions to name for the Boss, new:** R5's functions as above, each against the new law; the module-level caches and the id() keys as state beyond the Node-clock; David's twins patch (the rule outside Rule3, the module-level index). **Asked of the owner:** his word on removing R5 (the pair's sine and the envelope's weights as data in the universe and setting files).

## 35. The Scribe's scan becomes a gate (2026-10-28, 05:0x UTC)

The owner's direct words of 05:0x UTC (ledger row 295): the correlation from the twins' state, and the laws in scripts that refuse a push, so that a session that brings in circles, numbers, cosines or formulas is shouted at before it reaches the Scribe, logical and smart. The scan of row 294 is now tools/derivations/open_items/scribe_scan.py as a gate: a ratchet against the push's merge base (a hit keyed by rule, file and detail, a moved line no new hit, a renamed module carrying its counts), thirteen rules in two tiers (eleven refusals, two notes), the owner's allowed list empty and read from origin/scribe-5, the baseline of 209 hits the Scribe's audit of the whole. It runs at the push by git (--install), at the push by Claude Code (a PreToolUse hook on `git push` and a SessionStart hook that installs the git hook) and at the merge (a one-line patch of tools/check.py's RATCHETS); the last two files are the Boss's to adopt (SCRIBE-GATE-1.md, scribe_gate_check_py.patch, scribe_gate_claude_settings.json). Replayed over the last 40 pushes to engine-5.0-test it refuses 9, each a real hit under today's rules. The law's clause **No circularity that makes a phenomenon happen** names the gate at the push and at the merge.

**Asked of the Boss:** the adoption (a patch, a settings file). **Asked of the owner:** whether the server should refuse too (a required status check on engine-5.0-test).

## 36. The Boss's order-free click and one mirror (2026-10-28, 04:39 UTC push, read at 05:1x UTC)

The head 42d5448b7 (ledger row 296), merged into scribe-5 at 99abe82ee with the suite at 118 passed. The gate: no refusal, one note (a second pure memo, draw.kept_mid). The 24 is built: every rotation of the cube's 24 runs alike on the nature setting over 20 ticks (tests/test_the_board.py), every reflection parts at its first fitting, the great clock chiral: T0, the owner's 24. The prices the tests record: the light's cycle setting (CS5-S2) fits nothing by 20 ticks (every fit jammed at the lay), MG-S1's merger test asserts no births and no stops where 64 and 384 stood, the hole 23 fittings and 877 chimes against 17 and 920, other counts and every state hash struck again. The law's four sentences on the 24 (the clause, the decision list, the symmetry's paragraph) read built.

**Departures and questions to name for the Boss:** phase.py's books read a window two Meshes from the write; the gate of the 24 on every chart; the tag. **Asked of the owner:** his word on the price (the light's cycle setting born nothing).

## 37. David's local Bell carriage (toys-5, 04:42 UTC, read at 05:1x UTC)

DAVID-THE-BELL-LOCAL.md and its patch (ledger row 297): the marks on the Node-clocks and the closure that crosses one Mesh a tick, the answers equal the global index's click by click on 13 seeds (S = -2.859 over 688 pairs), the rewind exact, his own limit named (a partner that clicks before the closure arrives loses the correlation, Bell's theorem). The gate on the patch at 97e5b3fd6: ten refusals (two module-level containers, two id() keys, four reads of the log, the typed twins, bell_turn's four bilinear sums) and three notes. Not yet the owner's form: the marks and the turns stand in module-level tables, the quaternion turn is a rotation by a setting outside Rule3 and the twins a typed result. The carriage is the specification the Boss builds from.

**Departures to name for the Boss:** the ten refusals by file and line (row 297). **Asked of David:** his answer on the five departures.

## 38. The independent read of every src file (delivered 05:1x UTC)

The owner's order of 04:3x UTC (ledger rows 292 and 298; tools/derivations/open_items/SCRIBE-AUDIT-97E5B3F-1.md): a subagent read the 36 modules of 97e5b3fd6 whole and the Scribe checked every count against the tree (24 literals in 7 files, no float or true division, the one pow, `**` with a name 10 and 5 times, 19 id() keys, six module-level caches, the readers' hard-coded verdicts at run.py:68, gates.py:368 and predicates.py:296-309). The read lists nineteen places where a formula holds the phenomenon it makes (E1 to E19) and the reads beyond one Mesh. No postulate or law is changed by it.

**Departures and questions to name for the Boss:** the register's R5 and the list E1 to E19 against the clause **No circularity that makes a phenomenon happen**. **Asked of the owner:** his word on removing R5 and on the formulas E1, E3, E5, E8 and E19.

## 39. The Boss's shears struck (2026-10-28, 05:04 UTC push, read at 05:3x UTC)

The head d09f1a8a5 (ledger row 299): the regulator holds its time gear, its three tensions and its three flows, 12 integers fewer at every Node-clock, and the images gate asserts all 48 images alike on the nature setting over 20 ticks, reflections included; the hole 22 fittings and 529 chimes. The gate: no refusal, no note. The law asks the 24 and allows the reflections; the great clock is no longer chiral on this setting.

**Departures and questions to name for the Boss:** the gate of the images on every chart. **Asked of the owner:** the reflections parted (a chiral click, nature's parity violation) or held.

## 40. Rows 76 and 56 read anew (2026-10-28, 05:12 UTC push)

The head 123256cd5 (ledger row 300): row 76 by distinct pairs with a fitting's own two children left out; row 56's Bell at each end's own detector click, a click of the second kind, no longer the fitted child's typed sense. The verdict stays the local bound. The gate: no refusal, no note.

**Asked:** nothing new; the Bell click from the twins' state (row 297) is what would move row 56.

## 41. The click's name in the code (2026-10-28, 05:21 UTC push)

The head 526a5666d (ledger row 301): striking.py and strikes.py are click.py and clicks.py, clock.strikes clock.clicks, no strike stands in src. The gate carries the renamed modules' counts: no refusal, no note. The merge of the three pushes at 7acf9d1dd, the suite 118 passed. docs/ENGINE.md and docs/CLOCK_WORDS.md follow.

**Asked of the Boss:** the node's code spelling (the class Clock) and the Reader's keys.

## 42. David's finding of the unfair draw and the Boss's replies (2026-10-28, 04:48 to 05:23 UTC)

The thread's items 1214 to 1217 (ledger row 302): David measured the Bell click on the Boss's head 42d5448b7 and found the vernier's draw skewed (c over room by tenths, 2c < room at 390 of 914, S = -3.018 past Tsirelson's bound); the cause is the centre's own digit framed to the upper half while its base stays whole (draw.py:28-43); the Boss accepts it and builds the fair draw in the toy. The Boss answers that the class Clock stays the great clock, and that he builds the Bell click only on the owner's word on the quaternion turn (to be put at 10:30 Israel time). The Scribe's reading: a defect of the pushed head and no breach of a rule; the clause allows a turn by a setting only as Rule3's act.

**Asked of the Boss:** the fair draw pushed with its numbers. **Asked of the owner:** his word on the turn at 10:30 Israel time; told of the defect.

## 43. The system as a tensor machine (the owner's question, 2026-10-28, 05:4x UTC)

The owner asks whether the whole system works as tensors, the Node-clock a simple tensor machine and every family a kind of tensor (ledger row 303). The Scribe's answer: yes in the state (trains by kind: a scalar one gear, a plane two, a vector three, a tensor six; the metric of seven gears since the shears were struck, the potential of four, the plane of two), in the act (one division over the integer contraction of the Node-clock's and its six Meshes' gears: the quotient leaves, the remainder stays; acts.carry) and in the symmetry (all 48 images alike on the nature setting), and not yet in the form: the Node-clock is Rule3 and about 26 acts written by hand per phenomenon, the ranks constants in the code.

**Asked of the owner:** whether David tries the Node-clock's step as one act and counts the acts that fall into it.

## 44. The singular points of the tensor machine (the owner's question, 2026-10-28, 05:5x UTC)

The owner asks whether, the families being tensors and the engine so simple, a singularity can be caught (ledger row 304). The Scribe's answer: three singular points where the tensor degenerates: the light (the null element, the pair [1, 1], known by identity at 18 reads in 7 files), the points the cube's turns fix (the vernier's frame has no direction there, which is David's unfair draw, S = -3.018), and the frozen Node-clock (the metric's time gear 0); and one uniqueness: a train's kind is one of five representations of the cube's rotations (dimensions 1, 1, 2, 3 and 3), so the index logic is five integer tables and Rule3's carry. A reading and no proof.

**Asked of the owner:** whether the symmetric points are passed first to the Boss and David.

## 45. How everything converges to the clock (the owner's question, 2026-10-28, 05:5x UTC)

The owner asks how everything converges to the clock and whether the 24 arranges it (ledger row 305). The Scribe's answer: yes, through the dial: every component of every tensor is a gear (an integer with a carried remainder) and the only dynamics is the dial's turning over; the 24 acts on gears by exchanging dials and by reflecting a dial about its mid tooth (the one mirror), so a kind is a way of doing so (five); the clock is the kind the 24 leaves in place (the scalar: time gear, rate, load, trace); the couplings follow from the group's product table (the stress, a product of two gradients, is the trace, E and the shears). The 24 does not arrange the pair, Rule3 and the Mesh factor, or handedness.

**Asked of the owner:** whether the symmetric points and the trial in this wording are passed to the Boss and David.

## 46. The Boss synced on the tensor machine (the owner's order, 2026-10-28, 05:5x UTC)

The owner's order "Sync the Boss" (ledger row 306), after his three questions of rows 303 to 305, and the Reader's proposal of 05:49 (the Node-clock's step as one act, cut act by act and measured). The Scribe's reply to the Reader, the Boss and David (the thread's item 1221): the counts confirmed; the 26 acts of the step are five kinds (nine contractions, eight pointwise maps, five of bookkeeping, two gate acts, two global reductions that are readings and leave the step); the law cannot come first, the cuts need none; the kinds' tables follow from the vector kind; the draw reads invariants at the fixed points; the order of the cuts and the checks after each. The sentence proposed for the law stays in SCRIBE-THE-NODE-AS-ONE-ACT-1.md until the owner's word.

**Asked of the Boss:** his word on the order and on who cuts. **Asked of the owner, later:** the sentence.

## 47. The one tensor plan passed to the Boss (the owner's order, 2026-10-28, 06:0x UTC)

The owner's order: pass everything to the Boss so that everyone works on one tensor plan (ledger row 307). The Boss's reply of 05:53 (items 1220) brings the owner's final goal (recurring bangs; the board of clocks a giant machine that makes the clicks that human beings see), his call for generic operations and one operation that shortens everything, his questions (one place for the 24, detectors on the board, fusion and the clock of clocks), the fair draw built and measured in the toy and not pushed, a finding on the bang (the near-light family never born under the fair draw: the seed's symmetry) and the condition that only the Boss writes code. The Reader's reply of 05:54 (item 1222) takes the five kinds. The Scribe's plan is one file, TENZOR24.md: the goal, the Node-clock as one act, the one place of the 24 (the engine never turns anything; the table builder in core/spokes.py), the roles, the cuts in order, the owner's questions with readings and his list for 08:30 UTC.

**Asked of the Boss:** his word on the plan and the module-line process. **Asked of the owner:** the law's sentence and the list for 08:30 UTC.

## 48. Tenzor24 (the owner's word, 2026-10-28, 06:0x UTC)

The owner names the one tensor plan the program Tenzor24 and puts the Boss in charge of it (ledger row 308). Its file is tools/derivations/open_items/TENZOR24.md: the goal in his words, the Node-clock as one act, the one place of the 24, the roles (the Boss manages and writes, David derives and confirms, the Reader benches, the Scribe documents and keeps the gate), the cuts in order with the state of each, the owner's questions and his list for 08:30 UTC. The Scribe reports to the Boss each hour under the name Tenzor24. No law changed.

**Asked of the Boss:** his word on the plan.
