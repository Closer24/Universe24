# Hand X2: the inventory of the acts and the folding plan (engine-5.0-test at 4953d9e73; the toy at toys-5 519998511; 2026-10-25)

Read-only: no file of either worktree changed. Trees: scratchpad/e5 (src/event_universe, 55 files, 7,189 lines) and scratchpad/t5 (tools/derivations/toys: lean/ 1,051 lines in 7 files, probes/ 123 lines in 3 files). Read first: THE_WAY.md, The-Three-Shapes-Metric-Potential-Plane_COMPARISON.md, H-Inventory-Against-The-Laws-1/REPORT.md, docs/ALGEBRA.md under The Node (the two laws: one act on every row alike; the two kinds of act, atomic to the row and atomic to the Node), and the toy's REPORT.md.

Scripts, all under scratchpad/hands/x2/ (Python /home/user/Universe24/venv314/bin/python -I, no shell loop):
- functions.py: every function with its range (ast end_lineno) and the branches on a row's kind, counted exactly as U2's c_acts_by_kind.py counts them (reproduced: 127 in the engine) plus a wider count of the kind in disguise (engine_functions.json, toy_functions.json).
- fold_engine.py: every engine function mapped to the place it folds into, summed (fold_engine.json).
- fold_toy.py: the toy's functions mapped, and the folded line estimate from measured ranges with the named drops (fold_toy.json).
- knots.py: per function the count of its decisions (if, elif, for, while, ternary, boolean short-circuit, comprehension filter, try) and the docstring weight (knots_engine.out, knots_toy.out).
- link_places.py: every function that reads or writes a Link's number (link_engine.json/.out, link_toy.json/.out).
- shapes.py: the shapes' arithmetic written inline or twice, by idiom (shapes_engine.json/.out, shapes_toy.json/.out).

Every number below is one of these scripts' or wc/grep; the two estimates (the folded toy's lines, the link function's lines) are sums of measured ranges under a rule stated where they appear.

## 0. The totals

| | engine src | toy lean/ | toy with probes |
| --- | --- | --- | --- |
| files, lines | 55, 7,189 | 7, 1,051 (lean_full 667, decoder_full 200, five tests and diagnostics 184) | 10, 1,174 |
| functions and methods | 416 (428 FunctionDef nodes with the nested ones) | 58 (63) | 58 |
| lines inside functions / at module level (docstrings, imports, constants) | 5,317 / 1,872 | lean_full: 569 in functions, 36 the class header, 29 module level, 33 the __main__ block (667) | |
| docstring lines / blank / comment / code | 492 / 1,143 / 13 / 5,541 | 43 / 73 / 54 / 1,004 | |
| branches on a row's kind (U2's method) | 127 in 25 files (wronskian 31, held 22, rotation 21, plane 15, axes 11, charged() 10, motion_volume 9, quanta 8, turns() 8, carried() 4, flux 3, world.seed 3, reads_content() 1) | 1 (probes/stability_probe.py:20, .wronskian on the engine's families) | |
| the kind in disguise (my wider count) | 47: direction== 28, pair[0]==pair[1] 8, .reads 7, num==den 3, weight_of() 3, kind-in-disguise row 3, .level_weight 2, .width 2, line is self.phi 2, .laid .name .planes .rest by_charge() charge_of() readers_of() 1 each | 18 in lean_full.py: os.environ 10 (lines 134, 141, 210, 230, 232, 233, 270, 480, 572, 612), link_birth 2 (391, 411), shape_ == 1 2 (64, 66), row == 0 1 (93), sense ternaries 2 (114, 115), line is self.phi 1 (318) | |
| decisions in all functions | 892 | 204 | |
| lambdas / np.vectorize calls | 9 / 1 | 15 / 12 (lean_full lines 27, 147, 159, 198, 307, 309, 451, 454, 455, 458, 584, 628) | |
| carried divisions written (calls of carried_division, division_forward, division_back, held_write) | 92 call sites in 30 files (circle 14, start 8, phase 8, rule3 6, rooms 5, derived 5, share 4, meeting_board 4, digits 4, ...) | lean_full: carried_division 9, division_forward 3, division_back 11 | |

The engine's functions by the place they fold into (fold_engine.py; a class counted once for its header, its methods each):

| target | functions | lines | kind branches (of the 127) | wider branches |
| --- | --- | --- | --- | --- |
| ROTATE, rotate(row) | 52 | 656 | 12 | 15 |
| WRITE, write(rows) | 34 | 495 | 10 | 8 |
| SWAP, swap(row) | 7 | 153 | 5 | 4 |
| CLICK, click(rows) | 52 | 949 | 6 | 5 |
| the four together | 145 | 2,253 | 33 | 32 |
| PRIM, the Node's integer primitives the four share | 40 | 211 | 0 | 1 |
| LOOP, the interval's order and the state | 15 | 172 | 5 | 1 |
| LOADER | 73 | 834 | 30 | 6 |
| WRITER (the lines out) | 13 | 195 | 2 | 1 |
| DECODER (den's circle, names: tools/) | 14 | 173 | 0 | 0 |
| OUT (dead under the laws, or the host's runner) | 141 | 1,479 | 57 | 6 |
| module level | | 1,872 | | |

So 145 engine functions fold into the four, and 87 of the 127 kind branches stand outside them (LOADER 30, OUT 57); the four hold 33, the loop 5, the writer 2.

## 1. The acts, place by place

### 1a. rotate(row): every place that steps a line or a plane

Engine, 52 places, 656 lines (the list in fold_engine.json under places/ROTATE). The step of a line is written in five forms:

| form | file, function, lines | what distinguishes it (the inputs that differ) |
| --- | --- | --- |
| Rule3's flux line, one carried division | core/rule3.py: flux_total 80-82, rule3 85-89, carried_division 73-77; flux.py: link_fluxes 22-37 (the six Links' sum by slices), gathered_line 73-77, step_line 80-86 | the plain line: reaches R_ij, mass D, wall w, the six arrivals |
| the plane's complex line | flux.py: turned_link_fluxes 40-70, gathered_plane 127-131, step_plane 134-165 (rule3 twice, once per part; the plain fallback at 145-146 where pairs is None) | the Link's pair (R^c, R^s) per Port and the frame sign per Port: the phase as an input |
| the tension lines at the moving wall | flux.py: step_momentum 89-124 (its own numerator and division_forward at the wall 3 w (X_now + X_ahead), the complement by hand at 116 and 119), shear.py: stepped 65-83, inverted 86-93, written 32-62 (the order around the time line's write) | the volume's triple (X_behind, X_now, X_ahead): the wall w X as an input |
| the phase pair's act (the Link's (cos, sin) along the one orbit) | features/phase/__init__.py: act 57-70 (rule3 with 0 reads, twice by direction), iterate 79-98, chosen 73-76, read 173-176, signed_read 179-182, fold 190-194; node.py: phase_counts 204-217, phase_carried 220-256 (Orbit.pairs_at) | a line with no Links at the pair (K_0, D) = (2 Gamma^2 - 1, 2 Gamma^2): a table of (Gamma, X) alone (see the loader) |
| the Node's phase row | node.py: phase_rows 259-273 (Phi_next = 2 Phi_now - Phi_before + c, the division at the wall 2 by hand, forward and back as two branches) | a line with no Links, mass 0, wall 2, the write c inside the step |

Around them the dispatch by kind: flux.step_family 168-203 (plane or not, `traced = axes and not wronskian`), flux.step_records 260-279 (per record), flux.pairs_of 206-257 (the plane's phase inputs, a memo), node.read_lines/read/rulers 59-129 (the content: the volume row's level, the sign's |L| by `plain`, every row but the record's own by registry.row_of), node.turning 144-161, node.rule_of 307-313, frames.frames_of 12-21, plane.py: link_levels 23-32, link_wall 35-37, frame_signs 54-62, phase_links 65-76, sign_pairs 79-89, link_pairs 92-112; features/read: content_of, link_tension(s), link_factors 32-62; features/volume: level_of 72-86, searched_levels 89-119, levels_read 142-144 (the content from the volume X); board_readings.row_level 164-166; Lattice.read 195-198; readings.framed 19-23. The 12 kind branches inside: step_family 182, 184; pairs_of 226, 230; frames_of 16; read_lines 63, 80; read 102; turning 148, 150; shear.inverted 89, 93.

Toy, 10 places, 78 lines: content 118, link_factors 140-148 (the switch LEAN_FLAT_FACTORS 141-142), rule 150-152, step_line 155-161, frames 163-165, step_plane 167-186, centred_count 188-190, link_phases 192-200, back_line 505-511, back_plane 513-528; and the phase row stepped inline twice (step 274-275, step_back 561-566). Six places step a line in two forms (carried_division; the phase row by hand), three of them the inverse written again (back_line, back_plane, 561-566).

The one function: `rotate(row, node, links, direction)`: in, the row's shape and pair (num, den); the Node's clock p_0 and pace p_i at its content, the wall w (6 den Gamma^2 G^2) or the riding wall w X; per Port from link(): the factor Q_ij, the reach R_ij = 2 num p_i^2 Q_ij, the arrival of the row's line (or plane) in the Node's frame, and for a plane the Link's pair (c, s) over X and the odd tangent triple; the direction +1 or -1. One division: carried_division(total, wall, remainder, direction), once per line (a plane: once per part on the same wall). Out: the row's lines as (next, now, remainder') (or back, (now, before, remainder)), and the row's booking the write reads (the levels about the step). The variants are the inputs: a scalar line reads six arrivals; a plane reads six turned arrivals; the riding line reads the wall w X; the phase row has no Links; the inverse is the sign of the direction in the one division and nothing else.

### 1b. write(rows): the held write and its branches

Engine, 34 places, 495 lines (places/WRITE). The branches on wronskian/rotation/motion_volume/axes/flux/held/quanta inside the write (the 10 kind branches): records.write_sources 154-223 (173-175 `trace = not family.wronskian`, 185 `write.factors if family.wronskian else None`, 198 `parts = AXES if trace and position < AXES`, 218 motion_volume), Lattice.held_write 289-325 (302 `turns if family.wronskian else forms`, `senses if family.rotation else stresses`, 304 motion_volume, 325 motion_volume), Lattice.advanced_to_the_close 241-267 (258 motion_volume, 259 quanta), bookings.booked_of 41-57 (47 wronskian), shear.written 32-62 (42 carried), node.rulers 116-129 (120 rotation), node.clocked_potentials 180-201 (188 turns()), plus the walls per kind in loader/derived.held_write_of 262-289 (axes 273, flux 275, rotation 277, 270 rotation, 271 wronskian: six branches, counted under the loader). The sources: records.form 79-84, wronskian 87-94, scaled_sum 123-148, pressure_term 254-282, readings.sense_current_of 47-59, currents_of 62-79, stresses_of 96-107, axis_sources_of 110-116, axis_neighbours 119-125, features/currents tension 46-49, stress 52-55, board_readings stresses 47-56, sense_currents 59-65, sense_fluxes 68-72; the factor: paces.write_factor 141-171, write_factor_terms 174-183, within_width 191-198, axis_pace 136-138, features/read.axis_paces 65-70, records.rulers_write_factor 102-107, node.rulers 116-129, rulers_of 132-141, Lattice.rulers 200-202; the division: features/held_write.held_write 12-20 (one function, direction inside), node.held_write_at 316-333; the phase row's write: paces.turn_factor 211-213, node.clocked_potentials 180-201, node.phase_rows 259-273; the inverse: Lattice.booked_back 341-363.

Toy, the write is written inside step and again inside step_back: tensions 128-138 (the stress parts of the light and the planes with the switch LEAN_FORMER_TENSION at 134-135), step 246-251 (the forms, the Wronskian W and the sign currents J_a accumulated inside the planes' rotate loop), step 260-275 (the five writes: the volume's time line 263, the three axis lines 264-265, the sign's time line 266, its odd lines 267-268, the light's lay of the Wronskian's change 270-272 under the switch LEAN_NO_WS1, the phase row 274-275); step_back 568-579, 586-597, 609-619 (the same three sections written backward). Beside them write_walls 298-299 (the walls per line, five numbers from den, Gamma, T).

The one function: `write(rows, node, direction)`: in, every row's booking from its rotate (the levels about the step), the Node's clock p_0, the frame signs per Port, the walls per line (the loader's five numbers); the volume's time line gets 4 X (3 den SUM forms - trace) p_0^4 over 3 den Gamma^5 T... as the toy has it at 263, its axis lines the traceless parts (3 T_a - trace) over their wall, the sign's time line 2 SUM W over T, its odd lines SUM J_a over T, the massless line the change of SUM W over T, the phase row 2 c over 2; one division per line: carried_division(numerator, wall, write_remainder, direction). Out: the held rows' levels and the write remainders after. The sums run over every row of the list alike: the form of every row at one weight into the volume (the toy's sum over the light and the planes, the held rows excluded, is the one departure from "every row alike" the toy's REPORT names), the Wronskian of every plane into the sign (0 for a scalar). No branch on a row's kind: the parity of the bilinear decides (even into the metric, odd into the potential; The-Three-Shapes-Metric-Potential-Plane_COMPARISON.md), and a scalar's Wronskian is 0.

### 1c. swap(row): the complement at the top

Engine, 7 places, 153 lines: swap.at_top 31-34, floor_of 37-43, at_floor 46-49, swapped 52-119 (the exchange of every line, the complement at its wall; the branches: shear.carried 62 for the tension lines' wall 3 w (X_now + X_before), turns and plane 89-91 for the im lines' conjugation), swapped_phases 122-163 (rotation 127, the phase row's frame bit complemented at the wall 2, direction 132, 147), acted 166-190 (the trigger row by motion_volume and the pair's gap 168-172; direction 177), records.complement 346-348. Their 5 kind branches: swapped 62, 89; swapped_phases 127; acted 171 (two names). The trigger reads the volume row's triple (the law's own, allowed: the row selected by its pair).

Toy, 4 places, 24 lines: swap 304-313 (the trigger; two np.vectorize lambdas 307, 309), exchange 315-322 (`wall = 2 if line is self.phi else self.w` at 318, `sgn = -1 if im` at 319, the write remainders complemented at 321-322), is_im 290-293 (which lines are im by their position in all_lines), floor 295-296.

The one function: `swap(row, held, mask, wall)`: in, the row's lines as the interval started (the held pre-state), the mask of the turned Nodes (the trigger on the volume row's triple and the floor X_f, computed once per interval, the one reading of one row the law names), each line's own wall (w, 3 w (X_now + X_before) for a riding line, 2 for the phase row, the write wall for a write remainder) and the line's parity (a plane's im line conjugated: the sense exchanged by time's reversal alone, U-S3). No division. Out: the row's lines exchanged, (before, now, wall - 1 - r), the im line negated. The direction is none: the act is an involution, the inverse the same call.

### 1d. click(rows): the read, the pick, the take, the lay, the credit, the refusals

Engine, 52 places, 949 lines (places/CLICK); the centre meeting_board.closed 68-297 (230 lines, 38 decisions, the engine's largest knot), and around it:

| part | engine (file, function, lines) | toy (lean_full.py) |
| --- | --- | --- |
| the read of whole quanta (the share at the Node) | share.py: share 35-75, family_share 78-94, board_share 97-124 (a memo), over_pace 27-32, quanta_of 127-131, frozen 22-24; core/rule3.form_term 119-121; Lattice.share_of 204-206, quanta 208-211; meeting_board.meetings 54-65 | share 202-218 (the switch LEAN_NODE_SHARE 210-212; the flag vacuum), close 383-388 (the light's share and every record's own) |
| the one-Link read, the number | digits.py: digits_of 101-112, odd_line 115-119 (the plane's im digit folded), at_origin 122-130, lattice_of 133-148 (F_i = gcd(w, D, R), F_ij = gcd(w, R_ji)), read_of 151-202; features/click: read_number 18-23, drawn_from 26-59 (the whether: the number divided by the unit once), Refused 10-15 | read_number 328-344 (the lattices, the two refusals origin and coarse, the mixed radix) |
| the pick | meeting_board.child_of 40-42, drawn_among 45-51; act.affordable 60-66, list_walls 78-85 (the lists whose walls fit) | close 405 and 415, 419: `(number // unit) % nl` |
| the Link birth's two ends | meeting_board.closed 85-129 (one meeting per Node; no orientation by the current: the engine lays both children at the Node, the sentence 1 not built; x1 and the toy's REPORT) | close 391-406: every Link once from its +a end, both ends at a whole quantum, F_ij = num (now_i before_j - before_i now_j) at the start, F = 0 refused by the name orientation, the + child at the end the current flows into; 407-419 the two former modes (link, node) |
| the lay's refusal | take.below_quantum 26-31, meeting_board.refused_by 308-316 (REFUSED_LAY, REFUSED_STOP) | close 421-426 (owns[...] > units[s_]: the child's family above one quantum at its Node) |
| the take | hole.py: Take 23-30, walls_of 33-35, moved 38-47, taken_at 50-92 (the frame's seven shares' fall as one rational, the Link's term reach_back across each Port), take_of 95-113 (the level search one by one) | take 346-373 (the exact quadratic in the levels moved, the root by largest_below, the guard loop 371-372), close 427-438 (one take per Node of the children's walls summed) |
| the lay | lay.py: written 71-109, laid 112-127 (shares_of 20-29, division_act 32-43, guarded 46-57, corrected 60-68: the massless uniform-mode correction with weights, reached by no caller: the four call sites seed.py:36, emission.py:52, meeting_board.py:188, 196 every one with weights None); emission.emitted_lines 21-26, laid_by_count 29-53 (the amplitude from the count, features/click.squared 62-71, amplitude 74-76); act.click 22-24, written 27-57, born_items 111-120 | lay_amplitude 478-488 (the least A with (2 D + SUM R) A^2 >= unit 4 p^2 G^2; the switch LEAN_FIXED_A 480, 485), close 439-442 (the lay of A into re.now and sense A into im.before), __init__ 93-101 and 110-115 (the seed's lays: the sea, the hole, one quantum more, a plane record), step_back 536-541 (the lay undone) |
| the bodies' closing and the credit | bound_body.py: beats_of 20-28, bodies_closing 43-89; meeting_board.readings_at 335-388, Clock 319-324, agreed 327-332, holes_of 300-305; reports.point_of 176-184; readings.momentum_of 82-93, features/currents.momentum_terms 38-43 | close 447-468 (standing, crossed, beats per record, the closing, the take of one unit, the credit), credit 490-503 |
| the refusals by name | origin, vacuum, unit (features/click.Refused), lay, stop (reports.REFUSED_*): 5 causes, 17 lines name them | origin, coarse (unnamed in the log: `return None` at 341), lay, stop, orientation: 5 causes, counted in self.counts (12 keys) |
| the inverse (the lays and takes undone from the log) | meeting_back.py: crossed 74-98, logged 101-103, node_of 60-64, same_lay 67-71 | step_back 533-545 |

Toy: 5 functions, 175 lines (share, read_number, take, close, lay_amplitude) plus the undo 533-545 (13 lines) and the seed's lays in __init__.

The one function: `click(rows, node, links, log, direction)`: in, every row's lines at the interval's start (the read) and as the step left them (the write), the Node's pace, from link() per Port the current F_ij of the massless row, the neighbour's remainder digit on the Link's lattice gcd(w, R_ji) and the reach R_ji for the take's Link term, the units per row (3 T sine, the loader's), the log. The one division: the number divided by the unit once (the whether the remainder, the pick the quotient). Out: the rows' lines after the takes and the lays, and the credit lines (point, row, sense, beat, proper, windows, momentum) or the refusal lines (origin, coarse, lay, stop, orientation) for the writer; at direction -1 the lays and takes undone from the log in reverse order. Inside it the lay is one function, `lay(row, at, amplitude, sense, direction)`, the seed's (the loader calls it before the first interval) and the click's alike.

### 1e. The paces and the Link factor

Engine: core/paces.py 218 lines, of which the memo of the clock and the Link pace per (Gamma, content) is 60 (Side 45-60, sides 64-66, side_of 69-74, clock 77-79, link_pace 82-84, looked_up 101-118, clock_of 121-123, link_pace_of 126-128, node_paces 131-133; an economy, no act), clock_alone 37-41 (the one formula), rounded 19-21, odd_rounded 24-29; the Link factor core/rule3.link_factor 65-70 (one rounding) with features/read.link_tension 40-45, link_tensions 48-57 (the two ends' axis lines, (aa_i + aa_j + 1) div 2, read the same from both ends; the horizon's wall np.minimum(t, Gamma) at 55-57), link_factors 60-62; the rule's integers core/rule3.rule_integers 33-48, node.rule_of 307-313. Toy: rule 150-152 (clock_of, link_pace_of, rule_integers), link_factors 140-148 (the two ends' mean and link_factor with the wall min(t, Gamma) at 147). Fold: `paces(content)` -> (p_0, p_i) one function (the memo an economy inside it), `link()` gives Q_ij (1f).

### 1f. link(i, j): the act on the Link, one place (the owner's addition)

Measured (link_places.py: a function that reads a neighbour's integer through a Port or is one of the named Link readings):

| | engine src | toy lean/ |
| --- | --- | --- |
| functions that read or write a Link's number | 69 in 21 files, 1,176 lines | 20 in 2 files, 520 lines |
| Port reads (calls of arrival, shifted, ports, roll, slices, ported, frame_of, ports_of, opposite, frame_nodes) | 32 | 20 (roll 17, frame_nodes 2, and the birth's F_ij by index at close 399) |

The Link's numbers and where each is formed:

| the Link's number | engine | toy |
| --- | --- | --- |
| the arrival through a Port (the neighbour's level) | core/ports.shifted 16-21, arrival 24-26; readings.ports 42-44, framed 19-23 (the frame sign on an im arrival); flux.link_fluxes 22-37 and turned_link_fluxes 40-70 (by slices, both ends at once); features/start.arrivals 46-48 (dead) | roll 19-20; every `roll(` at 135, 137, 145, 158, 173, 177, 197, 206, 250, 509, 518, 520, 573, 575, 583, 593 |
| the tension on the Link, read the same from both ends | features/read.link_tension 40-45, link_tensions 48-57 (with the horizon's wall) | link_factors 145-147 (aa_i + aa_j + 1) div 2, min(t, Gamma) |
| the Link factor Q_ij | core/rule3.link_factor 65-70, features/read.link_factors 60-62, node.read 92-113 | link_factors 140-148 (and again in step_back 580-585) |
| the Link's pace p_a (the Node's pace by the two factors' mean) | paces.axis_pace 136-138, features/read.axis_paces 65-70, node.rulers 116-129 | none (the toy's write factor is the clock's alone) |
| the reach R_ij = 2 num p_i^2 Q_ij | core/rule3.rule_integers 46 | rule 152 (rule_integers) |
| the current F_ij | features/currents.current 33-35, momentum_terms 38-43; readings.currents_of 62-79, momentum_of 82-93, axis_sources_of 115 (the flux F_(-a) - F_(+a)) | close 399 (the birth's orientation); the credit carries no current |
| the frame sign per Port | plane.frame_signs 54-62, frames.frames_of 12-21 | frames 163-165 |
| the Link's count n_ij = K_i - f K_j and its pair (c, s) | node.phase_counts 204-217, phase_carried 220-256, plane.phase_links 65-76, features/phase.signed_read 179-182, fold 190-194 | centred_count 188-190, link_phases 192-200 (and step_back 599) |
| the odd line on the Link (the two ends' sum with the direction's sign) | plane.link_levels 23-32 (the declared pair of weights `ends`), link_wall 35-37, sign_pairs 79-89 (the tangent triple), link_pairs 92-112 | step_plane 176-178 (and back_plane 520-521) |
| the one-Link read of the click (the neighbour's remainder on the Link's lattice gcd(w, R_ji)) | digits.lattice_of 133-148 (opposite 63-66, ports_of 48-60, frame_of 43-45, ported 29-40), digits_of 101-112, read_of 151-202 | read_number 335-339 (frame_nodes 325-326) |
| the take across a Link (the neighbour's one term that moves) | hole.taken_at 80-89 (reach_back at the opposite Port) | take 353-355 (L = SUM R_j before_j), fall 358 |
| the Link birth's two ends | none (the engine lays both children at one Node) | close 396-406 |
| the horizon (a Link at the wall reads 0) | features/read.link_tensions 55-57, board_readings.horizon_ports 37-44, readings.currents_of 77-78 | link_factors 147 |
| the tension's part on the axis (two neighbours' difference squared) | features/currents.tension 46-49, readings.axis_neighbours 119-125, stresses_of 96-107 | tensions 133-137 |
| the sign's current J_a across the two a-Ports | readings.sense_current_of 47-59, board_readings.sense_currents 59-65, sense_fluxes 68-72 | step 248-251 |

The one function: `link(i, j, row, state)` -> the Link's record, read the same from both ends, the odd parts with the opposite sign: in, the two ends' integers (the volume row's axis line a at i and j for the tension; the volume's time line at both ends for the paces; the sign's odd line a at both ends; the phase rows' K and frame bits at both ends; the row's own line at j for the arrival, its remainder for the digit; the massless row's two levels at both ends for the current). Out, one tuple per Port: t_ij (the tension, min(t, Gamma)), Q_ij (the factor, G^2 at no tension, 0 at the wall), R_ij (the reach for the row), f_ij (the frame sign), n_ij (the odd sum, odd under i <-> j), K_ij = K_i - f_ij K_j (odd) with its pair (c, s) (s odd), m_ij (the arrival in the Node's frame), d_ij (the neighbour's digit on gcd(w, R_ji)), F_ij (the current, odd). Called once per Link per interval from the Node's loop over its six Ports; rotate takes R, m, (c, s), n; write takes the tension part and J_a (or they are formed from m); click takes F, d and R_ji. Estimated lines from the toy's measured bodies that become it: frames 3 + link_factors 7 (less the switch) + link_phases 9 + the odd sum and the frame-turned arrival of step_plane 174-177 (4) + the current 1 + the digit 2 + the reach 1 = 27 lines; the loop over the six Ports in the Node's step 3 more. In the engine the 69 functions and 1,176 lines fold to this one function and the callers' six-Port loop.

### 1g. The lay, the seed's and the click's as one

Engine: 4 call sites of lay.laid (seed.py:36 the uniform seed, emission.py:52 the lay by the count, meeting_board.py:188 and 196 the holes), every one with weights None, so lay.py's correction and guard (shares_of, division_act, guarded, corrected, 43 lines) are reached by nothing; lay.written 71-109 (39 lines, the lay line logged for the run back) and laid 112-127 are the act. Toy: four lays written by hand (__init__ 93-101 the sea and the hole and one quantum more by `largest_below((1 + n) sea^2)`, 110-115 a plane record, close 439-442 a child, step_back 536-541 the child undone). Fold: `lay(row, at, amplitude, sense, direction)`: re.now += A, im.before += sense A (a scalar row: now += A), the remainder at the origin where the line is empty, one lay line to the log; the seed is this call per seed entry of the world file, the click's child this call per end.

### 1h. The inverse as the same function with a direction

Engine: 28 branches on `direction` (records.py 49, 220; flux.py 75, 84, 116, 119, 122, 143, 144, 156, 160, 162, 194; shear.py 47, 58, 77; features/held_write 18; features/phase 59, 66, 81; swap.py 132, 147, 177; meeting_back.py 85, 95, 97; node.py 265, 269) and six inverse functions beside the forward ones (Lattice.step_inverse 365-398 34 lines, booked_back 341-363 23, shear.inverted 86-93 8, swap.inverted 198-200 3, meeting_back.crossed 74-98 25, core/rule3.division_back 97-99 3: 96 lines), where core/rule3.carried_division 73-77 already takes the direction. Toy: back_line 505-511 (7), back_plane 513-528 (16), step_back 530-624 (95): 118 lines written again backward, 9 of them textually identical to step's. Fold: the direction an argument of rotate, write and click (the swap needs none); carried_division as it is; the loop `interval(board, direction)` runs the four in order (+1) or in reverse order (-1) on the same numbers.

## 2. The other knots of logic (not one of the four, not the loader, the writer or the decoder)

Engine (knots.py, the functions with the most decisions, and the OUT groups of fold_engine.py; the lines are the functions'):

| knot | lines | decisions | where it goes |
| --- | --- | --- | --- |
| meeting_board.closed 68-297 | 230 | 38 | CLICK (the read, pick, take, lay, credit in one function) and WRITER (204-292, the lines out, 89 lines) |
| slabs.py (the parallel runner: Slabs.advanced 271-333 22 decisions, served 202-240, in_the_boards_frame 161-193, tile_of 138-158, conformed 124-130, born_points 119-121) | 279 in functions, 342 in the file | 22 + 8 + 7 + ... | OUT: the host's driver of the loop, no act; kept apart from the Node or dropped (the law is the one loop) |
| Lattice.step_inverse 365-398 and booked_back 341-363 (the readers' queue, the cycle assertion) | 57 | 14 | LOOP with direction -1: the four in reverse order; the queue falls with the per-row sourcing |
| records.write_sources 154-223 and scaled_sum 123-148, pressure_term 254-282 | 125 | 13 | WRITE: the sums over the rows and the one division per line |
| swap.swapped 52-119 (the tension lines' wall by shear.carried, the im lines by turns and plane) | 68 | 11 | SWAP with the wall and the parity as the line's data |
| Lattice.start 123-181, features/start/__init__.py 1-324, rests.py 1-130, bookings.booked_sources 60-104 (the rests' fixed point, the start's bookings) | 59 + 258 + 109 + 45 | 11, refined 10, rest 9, 11 | OUT: the volume row is laid at Gamma and no rest is solved (x1 list 1a) |
| the per-record and per-row machinery: registry.py 1-63, records.record_slice 52-55, rows_total 58-65, row_levels 68-76, bookings.sources_of 20-26, record_lines 29-38, emission.born_point 56-83, unborn_point 86-101, Lattice.born_point/unborn_point/lines_of/record, credit.py (Books, born, counted, count_of, support_of 42 lines), take.Item.record, act.written's deficit path 56-57 | 39 + 43 + 62 + 44 + 10 + 42 | | OUT: the sign one row read whole (S2), the fixed count (no row born at a birth), the count a reading of the writer |
| loader/derived.FamilyRule and its kind properties (held, quanta, width, planes, laid, power, exponent, axes, record, link_read 49-107), turns, charged, children_of, with_records, with_reads, family_rules, shared_clock, weight_of, readers_of 115-250; loader/interval.volume_rows; loader/universe.resolved; features/volume at_start/resting/started; shear.carried, shear_lines; walls.sourced | 160 + 8 + 18 + 17 + 10 + 6 | 7 (with_reads) | OUT: the row is (shape, pair); the kind is the shape's number; the reads are every row's alike |
| conversion.py (the Gaussian exactness, the baryon count, the general enumeration, the reducible meetings) | 63 of 138 | lists_of 9 | OUT (the pair on den's circle is the loader's one check, sine_of; the pick list is the plane rows, birth_of and walls_of to the loader: 30 lines) |
| the memos: features/read.READS and read_again 19-24, node.read_key 44-56, flux.pairs_of 206-257 (the memo part), digits.ruled 75-84, rule_and_pairs 87-98, share.board_share 97-124 (the memo part), features/phase.Orbit/seeded/orbit_of 106-170, paces' memo 45-133, features/volume.LEVELS | about 230 | | an economy and no act: inside paces() and the loader's orbit table, or out |
| the amplitude bound and the width: loader/rooms.py 1-153, derived.amplitude_bound 297-344, partial_rooms, plane.turned_room, Lattice.bounded 327-339, records.largest | 153 + 46 + 11 + 7 + 13 + 3 | bound_under_rooms 9 | LOADER (derived once; the law's 128 bits a gate reading, the census) |
| the guard once at load: features/read.paces_guard 95-142, stability_bound, edge_squared, edge_of, node.guarded 286-296, plane.link_guard 40-51, loader/world.even_box_refused 52-60, loader/charge.pythagorean_readers 9-25 | 48 + 11 + 11 + 12 + 9 + 17 | 8 | LOADER (the refusals by name at the load) |
| lay.py's correction never reached (shares_of, division_act, guarded, corrected 20-68) | 43 | | OUT |
| the eras log: board_readings.uniform_mode, Eras, volume_sums, eras 75-161, paces.exponent_products 201-208, derived.exponent_of | 89 + 8 + 3 | eras 7 | WRITER (the board's own view; the decoder never reads it) |
| meeting_back.named/arrays_of/snapshot/first_difference 19-57 | 33 | | OUT (a test's helper: tools/) |
| the dead: act.born_table 69-74, born_list 88-108 (the emission into standing light), features/phase.quarter_turn 211-221, features/volume.fill_of 62-64, board_readings.horizon_ports 37-44, features/read.plain 27-29, share.half_action/charge_of/charged/by_charge/count_read 134-161, node.sign_holder 164-172, least_pace 299-304 | 27 + 11 + 3 + 8 + 3 + 20 + 9 + 6 | | OUT |
| loader/circle.py 1-226 | 173 in functions | is_prime 8, circle_points 8 | DECODER (tools/) |
| the module docstrings and the comments | 1,872 lines at module level of 7,189 (docstring lines 492 in the ast's count, the module docstrings one line each and long) | | the sentence per function (one line) and the law's text in docs/ |

Toy (lean_full.py unless named; the lines are measured):

| knot | lines | where it goes |
| --- | --- | --- |
| the 10 switches on os.environ: LEAN_FORMER_TENSION 134-135 and 572-573, LEAN_FLAT_FACTORS 141-142, LEAN_NODE_SHARE 210-212, LEAN_NO_PHASE 230-231, LEAN_NO_PHI 232, LEAN_NO_ODD 233, LEAN_NO_WS1 270 and 612, LEAN_FIXED_A 480 (with self.A at 102, 485, 539) | 19 | out: the former clauses kept by name in the toy's REPORT, not in the code |
| the three modes of link_birth (391-419; `current` the law's, `link` the label, `node` the former toy) | 29 (13 of them the two former modes) | out: the Link close alone |
| step_back 530-624 written again backward (9 lines textually equal to step's, the rest the mirror), back_line 505-511, back_plane 513-528 | 118 | the direction argument (1h) |
| the credit's frame 495-501 (the Node's phases, odd lines, factors, neighbours' levels, X) and decoder_full.solve 34-64, which re-runs the Node's fold from it; residuals.py 1-38 on the same | 7 + 31 + 38 | out: the decoder reads the seven readings (point, row, sense, beat, proper, windows, momentum) and never the board's frame (ALGEBRA.md, The Node) |
| the seed's lays by the row's kind in __init__ 89-101 (`row == 0`: the sea, the hole, one quantum more) and 110-115 (the plane lays) | 19 | lay(): one loop over the seed entries |
| exchange 318 `wall = 2 if line is self.phi else self.w` and 319 `sgn = -1 if im`; is_im 290-293 (the im lines by their position in all_lines) | 6 | the line carries its wall and its parity as data (the row's shape): no test by identity |
| the detectors 87, 91, 469-476 (the light credits read at named Nodes) | 11 | WRITER (a reading, no state) |
| self.counts with 12 keys, written at 108 and in 14 places, and the rows' cadence 647-658 | about 25 | WRITER |
| the 12 np.vectorize(lambda ...) at 27, 147, 159, 198, 307, 309, 451, 454, 455, 458, 584, 628 and the 15 lambdas | 12 | np.where on integer arrays, or a plain loop: the same integers, readable |
| self.lifts = (None, num, sine) with a dead first slot 69 and 666; self.units 86 | 3 | LOADER: the unit per row (3 T sine(pair)), one list |
| gcd_arr 23-28 | 6 | out (never called) |
| tensions 128-138 sums the light's and the planes' lines and not the held rows' (the toy's REPORT names it) | 11 | WRITE over every row alike (the held rows' num = den - den div Gamma and den; the law's form at one weight), or the owner's word |
| the bodies' counters standing, crossed, beats per plane record 80, 448-468 and the restore 545 | about 25 | CLICK's state per row (the row's own three counters), kept |
| decoder_full.py: the names 'electron', 'proton', 'neutron' at 14 | 1 | DECODER's own, allowed (names are the decoder's) |

## 3. The shapes' functions (the owner's addition)

Measured (shapes.py: the lines of each function matching an idiom of vector or tensor arithmetic; a function counted once however many idioms):

| | engine src | toy lean/ |
| --- | --- | --- |
| functions holding the shapes' arithmetic inline | 37 | 21 (lean_full 15, cube48_test 4, mirror_diag 3, decoder 1) |
| matching lines, by idiom | 63: AXIS_LOOP 33, COMPLEMENT 9, CONJUGATE 7, FORM 4, BILINEAR 3, TRACE 3, SENSE_J 2, TENSION 2, IMAGE48 0 | 73: IMAGE48 18, AXIS_LOOP 14, CONJUGATE 10, BILINEAR 8, TENSION 6, TRACE 6, SENSE_J 4, COMPLEMENT 4, FORM 3 |

The places and the one function each folds into (the module `shapes.py`, integers in and out, no state, used from there alone):

| the operation | engine places (file:function lines) | toy places (lean_full.py lines unless named) | the one function and its signature |
| --- | --- | --- | --- |
| the bilinear of two level pairs (the Wronskian of a plane, the current across a Link) | features/currents.current 35; records.form 83 (now^2 - next before), wronskian 93; meeting_board 199 and share.charge_of 142 (the sign of W) | 239, 247, 493, 551, 590, 611 (W written six times), 399 (F_ij), mirror_diag.compare 41 | `bilinear(a_now, a_before, b_now, b_before) -> a_now b_before - a_before b_now`; `wronskian(z) = bilinear(re, im)`, `current(num, i, j) = num bilinear(now_i, before_i, now_j, before_j)` |
| the form of a line about the step | core/rule3.form_term 119-121; records.form 79-84; share.share 61 | 246, 254, 607, 615 (the form accumulated four times) | `form(now, before, next) -> now^2 - next before` and `form_term(S, w, now, before)` |
| the sign's current J_a across the two a-Ports | readings.sense_current_of 52-57 | 248-251, 591-594 (twice) | `sense_current(z_i, z_plus, z_minus, f_plus, f_minus) -> re (f+ im+ - f- im-) - im (re+ - re-)` per axis |
| the tension's part (the centred difference squared) and the Link's tension (the two ends' mean) | features/currents.tension 49, readings.axis_neighbours 124, features/read.link_tension 44 | 135, 137, 573, 575 (the part twice with its former form), 146 and 583 (the mean twice) | `tension_part(num, a_plus, a_minus) -> num (a_plus - a_minus)^2`; `link_tension(aa_i, aa_j) -> (aa_i + aa_j + 1) div 2` |
| the trace and the traceless parts | records.write_sources 200 (AXES axes - sum), 191 pressure_term 274-275 (the weighted trace), flux.step_momentum 109 (the traceless flux) | 261, 263, 265 and 576, 579, 619 (the trace and 3 T_a - trace twice) | `trace(parts) -> parts[0] + parts[1] + parts[2]`; `traceless(parts, a) -> 3 parts[a] - trace(parts)` |
| the axis loop with the two Ports (the vector's components by position: 2a, 2a + 1) | 33 lines in 22 functions: digits.ported 33, opposite 65-66, features/read.link_tensions 51, axis_paces 68, flux.link_fluxes 28-29, turned_link_fluxes 59-60, node.read_lines 84, phase_counts 214-215, phase_carried 232-233, plane.frame_signs 58, phase_links 69-70, 75, readings.ports 44, sense_current_of 52-53, momentum_of 87, axis_sources_of 115, axis_neighbours 124, records.write_sources 200, pressure_term 274, axis_positions 289, shear.shear_lines 28, meeting_board.readings_at 377, board_readings.eras 142, 145, loader/keys.node_of 39, features/start.arrivals 48 | 15, 133, 248-249, 264, 267, 326, 354, 396-397, 571, 578, 591-592, 595 | one constant `PORTS = ((0, 1), (0, -1), (1, 1), (1, -1), (2, 1), (2, -1))` and two functions `port(axis, side) -> 2 axis + (side < 0)` and `opposite(port) -> port ^ 1`; every loop `for port, (axis, side) in enumerate(PORTS)` |
| the sense's exchange (the conjugation of a plane, the frame sign on the im part) | flux.turned_link_fluxes 55-57 (add), swap.swapped 95-96, node.phase_counts 215, plane.phase_links 75 (-signs), readings.framed 23 | 165, 174, 180, 250, 319, 519, 522, 553, 593, decoder 52 | `conjugate(z, sign) -> (re, sign im)` with sign +1 or -1; the frame sign one function `frame_sign(bit_i, bit_j) -> 1 - 2 (bit_i xor bit_j)` |
| the carry's mirror (the complement at the wall) | records.complement 346-348, swap.swapped 78, 100, 113, swapped_phases 142, flux.step_momentum 116, 119, digits.read_of 172 | 320, 322, 554, 565 | `complement(r, wall) -> wall - 1 - r` (the engine has it: records.complement; swap and step_momentum write it by hand) |
| the cube's 48 on a Node and on a row (the signed permutations; the vector's components permuted and signed; the tensor's; the plane kept) | none in src (the 48 live in the tests: tests/test_the_board_is_the_cube_48.py) | cube48_test.signed_permutations 9-11, image 14-16, mapped 24, world_image 27-32; mirror_diag.image 13, world_image 14-19, compare 24-43 (the axis lines permuted and signed at 28-35, the planes by the determinant 39-41) | `cube48() -> the 48 signed permutation matrices`; `image(g, node, cube)`; `turned(g, row) -> the row's lines under g`: a scalar as it is, a vector's three lines permuted with the signs, a tensor's six lines by the two indices, a plane's two lines as they are (the sense kept, U-S3); used by the tests and by nothing in the Node |

Counted: 9 shape functions (bilinear with wronskian and current, form, sense_current, tension_part with link_tension, trace with traceless, the Port constant with port and opposite, conjugate with frame_sign, complement, cube48 with image and turned) in place of 37 engine functions holding the arithmetic inline (63 lines) and 21 toy functions (73 lines, of which 18 are the 48 in the two tests).

## 4. The folding plan for David, in order

The target modules (one file for the Node, one for the shapes, one each for the loader, the writer, the decoder; two tests):

1. `shapes.py` (first, since every other file calls it): the 9 functions of section 3. Docstrings: bilinear "a_now b_before - a_before b_now, the Wronskian of a plane's two lines and the current across a Link"; form "now^2 - next before, the line's form about its step"; sense_current "re (im_+ - im_-) - im (re_+ - re_-), the sign's current across the two a-Ports in the Node's frame"; tension_part "num (a_+ - a_-)^2, the stress of a line on one axis"; link_tension "the two ends' mean rounded, read the same from both ends"; trace, traceless "the sum of the three parts; 3 T_a less the sum"; PORTS, port, opposite "the six Ports in the law's order and the Port back across a Link"; conjugate, frame_sign "the sense exchanged; +1 where the two ends' frame bits agree, -1 where they differ"; complement "wall - 1 - r, the carry's mirror"; cube48, image, turned "the 48 signed permutations and a row's lines under one of them". Estimated 60 lines (9 functions of 3 to 8 lines with a one-line sentence each; the measured engine bodies they replace are 3 to 13 lines each).
2. `node.py` (the Node): `paces(content) -> (p_0, p_i)` (the memo inside), `link(i, j, row, state)` (1f), `rotate(row, node, links, direction)` (1a), `write(rows, node, direction)` (1b), `swap(row, held, mask, wall)` (1c), `lay(row, at, amplitude, sense, direction)` and `click(rows, node, links, log, direction)` (1d), and the loop `interval(board, direction)`. Docstrings, one sentence each: paces "the clock Gamma (1 - 1 / Gamma)^c and its square over Gamma, one rounding each"; link "the Link's record from its two ends' integers, the same from both ends, the odd parts with the opposite sign"; rotate "one Rule3 step of the row's lines at the Node from the six arrivals, one carried division per line, the plane's arrivals turned by the Link's pair, the wall w or w X an input, backward the same division at -1"; write "the held rows written from every row's booking alike: the forms into the volume, the Wronskians into the sign, the currents into the odd lines, one carried division per line"; swap "at a turned Node every line exchanged and complemented at its own wall, the im line conjugated, an involution"; lay "one quantum laid into a row at a Node at a sense, the remainder at the origin, one line to the log"; click "the read of whole quanta on every Link, the one number and the pick, the take by the exact fall, the lay at the two ends, the credit or the refusal by name, backward the lays and takes undone from the log"; interval "the acts in the law's order, or in reverse at -1". The loops, in `interval`:

```
links = [link(i, j, row, state) for every Port j]        # once per Link per interval, the six-Port loop
for row in rows: rotate(row, node, links, direction)     # one act on every row alike
write(rows, node, direction)                             # one sum over the rows per held line
mask = top(volume_row) | floor(volume_row)               # the one reading of one row the law names
for row in rows: swap(row, held, mask, row.wall)         # the exchange where the mask holds
click(rows, node, links, log, direction)                 # the read, the pick, the take, the lay, the credit
```

   with direction -1 the same lines bottom to top on the same numbers (the swap's mask read on the undone triple). Inputs from the universe file's numbers: den, Gamma, T, G and the rows' (shape, pair); from the Node's integers alone: every line's (now, before, remainder), the write remainders, the phase row, the three counters per plane row. Nothing else enters: no name, no kind flag, no switch.
3. `loader.py`: `load(world_path) -> (constants, rows, state, seed_lays)`: the two files read once, the derived numbers each one function of the file's numbers (w = 6 den Gamma^2 G^2, the five write walls, X from the width 128, the orbit table of (cos, sin) at the count n for (Gamma, X), the unit 3 T sine(pair) per row, the volume pair (den - den div Gamma, den), the floor X_f = volume_of(Gamma, -Gamma), the frozen content), the state built at every Node (the lines at (0, 0, w div 2), the volume row at Gamma, the write remainders at half their walls, the phase row at (0, 0, 1)), then `lay()` called once per seed entry. Docstring: "the two files in, the numbers derived once, the state at every Node, the seed laid by the Node's own lay; no act". Measured: the toy's loader bodies kept 62 lines (fold_toy.json).
4. `writer.py`: the credit line (point, row, sense, beat, proper, windows, momentum), the birth line, the refusal line, the light line, the census row (integers per Node, max bits, max transient bits, the counts) at the rows' cadence, the record dumped; the __main__ run. Docstring: "the lines out, as the Node read them; no act". Measured kept: 54 lines.
5. `decoder.py`: decoder_full.py less solve (31 lines): the gates from the credit lines alone in integers; the names the decoder's. Kept: 169 lines.
6. `cube48_test.py` and `runback_test.py` (58 + 19 = 77 lines), each under 15 s on the 3-cube; mirror_diag, freeze_diag kept under tools/ or dropped (69 lines), residuals.py falls with solve (38).

The order of the work: (i) shapes.py; (ii) link() with its six-Port loop, every roll() of lean_full.py replaced by a read of the Link's record (17 roll calls, 20 Port reads); (iii) rotate() from step_line and step_plane with back_line and back_plane deleted (23 lines), the run back MATCH checked by runback_test after each step; (iv) write() from tensions and step 246-275 with step_back 568-619 deleted, the switches out (10 os.environ lines); (v) swap() from swap, exchange, is_im, floor with the wall and the parity as the line's data; (vi) lay() from the four hand-written lays, then click() from close, read_number, take, lay_amplitude, share with the two former modes out and the undo 533-545 as direction -1; (vii) interval(direction) in place of step and step_back; (viii) the loader from __init__, load_world, write_walls, pair_angle; (ix) the writer from credit (the frame out), census, the detectors, the __main__ block; (x) the decoder less solve; after every step the two tests (the 48 at 48 of 48, the run back exact) and the owner's six: the conserved form, MATCH, the one-Link reach, the 48, the fixed count and the 128 bits, integers only, one act on every row alike and the two kinds, the exact take, no name and no number in the code.

### The estimate (fold_toy.py; every term a measured range under the stated rule: kept whole, dropped whole, or kept less named ranges)

| part | measured (toy) | folded |
| --- | --- | --- |
| the Node file: rotate 53 (step_line 7, step_plane 20, rule 3, frames 3, centred_count 3, link_phases 9, link_factors 7, content 1), write 30 (tensions 9, the forms/W/J 6, the writes 15), swap 24, click 153 (close 81, take 28, read_number 17, share 14, lay_amplitude 10, the undo 13 counted under the loop, lay 3), primitives 8, loop 59 (step 37, the undo 13 within step_back's 16, snapshot 4, all_lines 2, the rest) | lean_full.py functions 569 (of 667) | 327; with link() split out of rotate and click and its six-Port loop added, 332 (link 27 of them) |
| the shapes module | inline in 15 functions of lean_full | 60 (estimate: 9 functions of 3 to 8 lines, the measured engine bodies 3 to 13) |
| the loader | __init__ 63, load_world 5, from_files 3, write_walls 2, pair_angle 8 | 62 |
| the writer | credit 14, census 4, state_bytes 2, the detectors 8, the __main__ block 33 | 54 |
| the decoder | 200 | 169 |
| the two tests | 77 | 77 |
| imports and constants carried over | 29 module level + 36 class header | 20 (estimate) |
| total | 1,051 (lean/), 1,174 with the probes | 709 without the shapes module as a separate file (the 60 lines of shapes are inside the 327 of the Node as inline arithmetic now; split out they add about 30 net, the duplicates gone): about 740 |

Against the toy's 1,051: about 740 (the Node file 332 of them), the diagnostics (mirror_diag, freeze_diag 69) and the probes of the 4.0 engine (123) beside, out of the toy's module. Against the engine's 7,189: the engine's four hold 2,253 lines in 145 functions plus 211 of primitives and 172 of the loop (2,636), with 1,872 lines at module level (the docstrings one line each); the folded toy's Node file is 332 lines, a factor of about 8 on the functions' lines alone, and the toy's loader (62), writer (54) and decoder (169) stand where the engine's are 834, 195 and 173 (plus tools/clicks_read.py's 1,393, x1).

## 5. The counts in one place

- Engine src: 416 functions and methods, 7,189 lines; 127 branches on a row's kind (U2's count reproduced) and 47 of the kind in disguise (28 of them the inverse as a branch on direction); 892 decisions; the places folding into the four: rotate 52 (656 lines), write 34 (495), swap 7 (153), click 52 (949), 145 in all (2,253 lines); the primitives 40 (211), the loop 15 (172), the loader 73 (834), the writer 13 (195), the decoder 14 (173), out 141 (1,479); the Link's number read or written in 69 functions (1,176 lines, 32 Port reads, 21 files); the shapes' arithmetic inline in 37 functions (63 lines); the step of a line in 5 forms; 92 carried divisions written in 30 files; 4 lay call sites, every one past a correction of 43 lines reached by none.
- Toy lean/: 58 functions, 1,051 lines (1,174 with the probes); 18 branches of the kind in disguise (10 switches on os.environ, 2 modes, 6 by position or identity); 204 decisions, close 48 of them; the places folding into the four: rotate 10 functions (78 lines; 6 of them step a line, 3 the inverse written again), write 3 sections (tensions 11 lines, step 246-251, step 260-275) written twice (their mirrors in step_back), swap 4 (24), click 5 (175) plus the undo; 118 lines of the inverse written again; the Link's number in 20 functions (520 lines, 20 Port reads); the shapes' arithmetic inline in 21 functions (73 lines, 18 of them the 48 in the tests); 12 np.vectorize and 15 lambdas; 5 refusal causes against the engine's 5.
- The fold: one Node file of about 332 lines (rotate, write, swap, click, lay, link, paces, interval), shapes about 60, loader 62, writer 54, decoder 169, two tests 77: about 740 against the toy's 1,051 and the engine's 7,189.
