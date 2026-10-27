# The Scribe's full read of the engine's code against the central postulate

The Scribe, 2026-10-27, 15:2x UTC, on the owner's word of 14:5x UTC ("always read all the code"; "the central postulate, that the engine runs whole numbers with one formula of Rule3, must hold; make sure there are no contradictions"; "always make sure the engine does not know families and everything is truly generic, it is in the laws too, and only whole numbers, without formulas").

Read: every line of src/event_universe at the engine head 608d97134, 35 files, 6,325 lines (the 22 modules, core/, features/, assembly/), the engine's and the Reader's, no suite run. Against: Postulate 2 (whole numbers, every act a bijection with its remainder kept), **The law in one line** (one division act with coefficients from the train's pair and the Clock's rates, every notch written by that same act, everything else a number in a file), **The Clock and the Mesh are generic; there is no if**, **No number in the code**, **No float anywhere in the system**, the ten postulates' second ("the Clock is dumb and generic ... knowing no bob, mass, well, train, fitting or strike"), and the owner's rules of 11:3x and 14:5x UTC. The counts are the Boss's own counters (tools/engine_gates.py, 0660dd42e) and an AST scan; the lines are the Scribe's reading.

## 1. What holds

- **Whole numbers.** No float literal, no true division, no root, trig, exp or log call and no math import in src (AST scan, 0 of each). Every act is on integers; the one carried division is core/acts.py:18 and every write goes through it (clock.py:153 turn, 178 drive, tick.py:199 and 257 carries, unwind.py:77 and core/acts.py:38 the lay as acts.advance).
- **The rewind.** Every act has its inverse at direction -1 by the same function (clock.py:153, 235; tick.py:326), checked by the suite and the Reader's charts.
- **Locality of the dynamics.** A Clock reads itself and its six neighbours through core/spokes.py:37 across and unwind.py:19 neighbour. Board-wide reductions exist only as diagnostics and skip guards: clock.py:172 (the transient's bit length over the board), 255 and 263-265 (top.any(), top.sum(): the swap runs only where a Clock turned), run.py census and state_hash (the rewind's proof). Named, not breaches of the dynamics.

## 2. Where the code departs from the central postulate: the engine knows structure by kind

The five kinds are the families in the engine's own spelling: the phase clock (the walled row), light (the plane at (den, den)), the carrier (the shape-10 row), the potential (the shape-4 row at (den, den)), matter (a plane with a gap); the twin hands are a sixth by the shape 4 at a spring. They are named in every module that acts, which is why the places are so many.

- **The universe must hold exactly these.** trains.py:120-131 refuses a universe without exactly one walled row, one plane at (den, den), one shape-10 row, one shape-4 row and a plane with a gap; 124 and 128 fix the carrier's pair at (den - den div Gamma, den) and the potential's at (den, den); assembly/piece.py:38 admits the shapes 1, 2, 4 and 10 only; trains.py:62-69 gives each shape its own write teeth (drive_teeth: REGULATOR, OFFSET, HAND at (den, den)); trains.py:104 reads twin hands off the shape 4 at a spring.
- **The tick names the roles.** tick.py:66-68 holds `regulator`, `ratchet`, `offset`, `unsprung` apart; 120-147 standard_rate is the walled row's own act; 237-278 carry is the carrier's own write (held_numerator); 280-302 advances is the emitter's lay and the potential's drive by the lead; clock.py:100, 252-262 and readings.py:30-32 read the carrier's time gear by role.
- **The close does two acts by family.** unspring.py:125-127 and 209-215 take matter by the wind's fall (unspring_end) and light by moving a line toward its before (unsprung_end); striking.py:46-49 (list_of), 188 (fittings) and bobs.py:33 branch on the same line; setting.py:53, 59, 68, 80 branch on it for the lays.
- **Light's coupling is a number case.** meshes.py:20-23 coupling_of is min(den - num, 1), 0 for light and 1 for every other pair; readings.py:62-67 gives the walled row its own rule with no Meshes. The law calls a case by number lawful (**The Clock and the Mesh are generic; there is no if**, the owner's "1" of 10:4x); the owner's word of 14:5x, truly everything generic, is the question this reading puts to him.
- **Family words in names and keys.** clock.py:28-44 COUNTS (`body_clicks`, `births`), run.py:258 and 261 ("gap-0 W abs max", "gap-0 velocity max"), setting.py:26-31 FIELDS (the lay forms `sea` and `hole`), bobs(), unsprung_notches, unsprung_end; the Reader's modules name light and species throughout (reckoner.py:86-100).

**The Boss's counters, at 608d97134.** Reads of the unsprung hand by its identity 32: setting.py 53 59 66 68 80; bobs.py 30 33; clock.py 69 70; run.py 202 224 258 274 354; striking.py 46 47 67 131 188 263 326; tick.py 67 283 294; trains.py 67 117 128; unspring.py 125 127 209 215 233. Branches on it 15: setting.py 53 59 68 80; bobs.py 33; clock.py 69; run.py 202; striking.py 46 67 131 188; unspring.py 125 127 209 215. The counters see the words unsprung and sprung and a pair of one name; they do not see the other roles (REGULATOR 31 places in 11 files, HAND 31 in 9, OFFSET 11 in 4, `train(REGULATOR)` or `train(OFFSET)` 18 in 8, `.size ==` checks 9 in 5).

## 3. Numbers

- **The 37 literals beyond 0 and 1.** Engine 14: assembly/cycle.py:21 (4); assembly/setting.py:23-24 (2, 3), 104 and 108 (2, 2); core/acts.py:15 (2); core/rule3.py:126 and 136 (2, 2); core/spokes.py:7-8 (3, 2); meshes.py:127 (4); trains.py:15-17 (2, 4, 2). The writer run.py 3: 26 (12), 27 (24, 60). The Reader's modules 20: reckoner.py:15-29 (1000000, 100, 1000, 10, 20, 2, 2, 3, 4, 8, 6, 4, 2, 2), rim.py:7-8 (2, 4), gates.py:299 and 301 (2, 3), great_clock.py:30 (2), swings.py:9 (2).
- **Numbers spelled by name.** The counter sees literals; the engine also builds numbers from two typed ones: AXES = 3 (core/spokes.py:7) is read in 58 places of the engine proper (an AST count of the names, the writer and the Reader's modules apart) and builds SPOKES = 6 (13 places), REGULATOR = 1 + 3 AXES = 10 (trains.py:13), OFFSET = AXES + 1 = 4, HELD_DRIVE_WEIGHT = AXES + 1 (core/rule3.py:14), WINDING_WEIGHT = AXES (17), EXPONENT = AXES + 1 (features/stretch/__init__.py:14); HAND = 2 is read in 31 places; 40 doubled operands (x + x) stand for a typed 2 in the engine proper. The universe file holds five integers (den, node_clock, quantum_action, trace, amplitude) and each row's shape, pair or wall; the dimension, the sides, the shapes 1, 2, 4 and 10, the powers 4 and 2, the quarter turns, the half spans 1, 2 and 3 and the marks 12, 24 and 60 are typed in the code.
- **The enforcement is looser than the rule.** tests/test_rule3.py:108-130 and 139-154 allow {0, 1} in the law's files and, by file, spokes {2, 3}, rule3 {2, 3, 4}, trains {2, 4, 8, 10}, meshes {4}, setting {2, 3}, cycle {4}, run {12, 24, 60}, acts {2}, tools {0, 1, 2, 3, 4, 6}, and exempt nine modules whole (reckoner, gates, events, rim, great_clock, swings, strikes, predicates, symmetries). The Boss's gate counts every literal beyond 0 and 1 in all of them, on a ratchet: the test passes what the gate counts.

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
- **ALGEBRA.md and ENGINE.md, The Clock and the Mesh are generic; there is no if** and **The tick is one function of the Clock** state the norm (no branch on a train's identity); the code departs by section 2. The norm stands, the departure is named, no sentence of the law changes.
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
