# H-Node-Beneath-Rule3-1: the one act beneath Rule3 (2026-10-26, toys-5 3dc12e307)

## 1. The one act (a page)

The law's clauses read: The Node ("a Node does one thing: at every interval the same list of acts, each one division with a carried remainder, every one a bijection but the writing of a line"); The line (Rule3, w a_next + r' = S a_now - w a_before + SUM_j R_j m_j + r); The direction (CA-S1: the step at -1 is the step at +1 with the slots exchanged and the remainder mirrored, w - 1 - r; RW-S1: one function with the direction); The swap at the top (the exchange conjugated by the row's K at the weak maximum, FR-S1); The click (CR-S1: the take's move one carried division of count times wall at the line's own wall; CR-S2: every end read before any is written; TC-S1: the count one carried division of the walls by the price; GP-S1: the children laid (A, 0, 0, sense B)).

Let D be the one forward act on a slot: D(t; w, r) = (q, r') with u = t + r, q = u div w, r' = u mod w in [0, w), the quotient q laid on the slot named (the level there plus q). Every state move of the Node and its six Links is D or a composition of D, and nothing else:

1. Rule3's step on a line, R: (a, y, r) -> (q, a, r') with (q, r') = D(S a - w y + f + SUM_j R_j m_j; w, r), the quotient laid on the slot the direction names, the level read becoming the other slot. One D.
2. The write and the take's move: (now, wr) -> (now + q, wr') with (q, wr') = D(numerator; wwall, wr); the move is D(count w; w, r) = (count, r), the remainder unmoved (CR-S1): the lay of a count on a slot IS the division's quotient written, so the lay is not a primitive of its own (measured: move 20,000 of 20,000; the engine's 24,784 lays on the hole 60 each the quotient of a D or the children's (A, B), two D's of A w and B w, one per slot).
3. The quarter turn Q is R with no Links and the own weight 0 (the mass 2 w, the law's own phase line at K = 0): Q(a, y, r) = (-y, a, r). One D (20,000 of 20,000).
4. The negation of a level is the move of -2 a: D(-2 a w; w, r) = (-2 a, r) laid. One D (20,000 of 20,000).
5. The mirror of a remainder is the forward division of the numerator w - 1 - 2 r: D(w - 1 - 2 r; w, r) = (0, w - 1 - r). One D with the quotient 0 (20,000 of 20,000).
6. The slot exchange with the mirror, X(a, y, r) = (y, a, w - 1 - r), is the composition mirror o negate_now o Q (20,000 of 20,000). The swap at the top is X conjugated by the row's K, and K's negation of the im line is item 4: the swap is D's alone.
7. The direction: D(t; w, r, -1) = mirror o D(t; w, .) o mirror, the quotient the same (RW-S1's theorem; 20,000 of 20,000 with the mirror itself a D by item 5). So the act at -1 is a composition of forward D's, and the direction is a reading of which slot is named, not a second act (CA-S1: the direction is the slot).

The Node's step in the law's notation, every line alike: for each line L = (a, y, r) with its wall w and its write (wr, ww): L <- R_D(L) (one D with the six arrivals through the Links, the carrier's and the shape-4 row's lines with their write D after it, the riding lines' D at the mean wall of the carrier's two levels); at the weak maximum of the carrier's level, every line L <- K X K (three D's per line); the close: for every record, every Link read once (a reading: the current F = cross(now, before; now_j, before_j), the twist h, the charge W, the draw's digit on the remainder's lattice), the count s = D(walls weight; price, .) iterated (TC-S1), every end read before any is written (CR-S2), the take L_now <- L_now + D(s w; w, r)[0] with the count's sign, the children's lay D(A w; w, .) on the re now slot and D(sense B w; w, .) on the im before slot, the credit the same take at one end; the run back the same D's in the reverse order with the mirror, the frame (the turned mask, the log) the record of the two readings that are many-to-one (the peak, the draw).

**The Node in one sentence: a Node does one thing, the carried division of a total by its wall, the quotient laid on the slot the direction names and the remainder kept; the exchange, the mirror, the lay, the write, the move and the step at -1 are this one act read three ways.**

## 2. The inventory (the engine's 274 functions, the Reader's seven modules left out; the whole table in out/inventory.md, inventory_nl1.py)

| role | functions | lines | lines less docstring |
| --- | --- | --- | --- |
| the law's act (P1 the carried division: 12 functions, 225 lines; P2 the exchange with the mirror: 3, 44; P3 the lay on a slot: 9, 264) | 24 | 533 | 511 |
| record-keeping (the log, the frame, the census, the hashes, the counts, the record's writer) | 21 | 366 | 346 |
| refusal by name (the loader's and the acts') | 9 | 123 | 115 |
| a reading (no state move: the gram, the metric, the Link's turn, the paces, the take's count, the draw, the seed's shapes, the quartet's lattice) | 153 | 1,359 | 1,222 |
| a second road (least_root, rise_of, share_at, products, plane_current, twist, the search spelt again in fitted and least_share) | 10 | 122 | 115 |
| a wrapper (a name for a composition) | 47 | 395 | 351 |
| the state's holders (Row, Line, Link, Birth, Kid) | 10 | 61 | 54 |
| total | 274 | 2,959 | 2,714 |

Of the 5,560 lines of the 33 files, 1,825 are the Reader's seven modules (board 332, clicks 338, decoder 174, events 113, gates 380, predicates 383, circle 105) and the rest module docstrings, imports and constants. The law's own act is 533 lines of 2,959 (18 percent); the readings are 46 percent; the lay's 264 lines are mostly the seed's forms (lay_world 63, lay_uniform 36, lay_packet 56, lay_cycle 55) and the children's lay.

## 3. The lean core, measured (core_nl1.py: 45 code lines; the one act `divide`, its readings `step`, `write`, `move`, `exchange`, `mirror`, `lay`, `peak`)

Commands (P = /home/user/Universe24/venv314/bin/python, W = the worktree, D = this folder, PYTHONPATH = W/src):

- `$P -I $D/one_act_nl1.py $D 20000` -> out/one_act.json: quarter_turn 20,000, negation_is_move 20,000, mirror_is_division 20,000, exchange_is_composition 20,000, direction_is_composition 20,000 of 20,000.
- `nice -n 19 $P $D/proof_nl1.py $D $W/tests/worlds/world_node.json 10 - $D/out/proof_node_10.json` (the node toy, the 3-cube, 10 forward and 10 back, under 2 s): the random lines divide 20,000, reversal X R X = R^-1 20,000, the exchange as the direction read 20,000, move 20,000, write forward and back 20,000 of 20,000; the engine's run with every carried division, every lay and every exchange replayed through the core: 73,618 divisions, 0 apart; 3 lays, 0 apart; 20 exchanges at 116 turned Nodes, 0 apart; the run back 10 of 10; the census 99 arrays, 114 bits.
- `nice -n 19 $P $D/proof_nl1.py $D $W/tests/worlds/world_hole.json 60 $W/examples/records/hole.json $D/out/proof_hole_60.json` (the hole 60, 51 s): 5,756,260 divisions, 0 apart; 24,784 lays, 0 apart; 94 exchanges at 1,114 turned Nodes, 0 apart; the run back 60 of 60; the counts equal to the committed record's (16 births, 557 turns, 1,653 body clicks) and the log 16,903 entries, equal.

The prediction before each run: 0 apart everywhere (the core's divide is the law's division and the engine's acts are its compositions); measured 0 apart.

What the core does not do: it did not run a board on its own. The readings between the divisions (the gram's matrices and the row's K, the metric's stress parts, the Link's record and its turn, the paces' table, the kick's momenta, the take's count by TC-S1's iterated division, the draw's digit, the peak) are 1,222 lines the core does not hold; so the proof is that every state move of the engine on the two worlds passes through the core's one act bit for bit, not that the core alone reproduces the record. Cut short, named: the standalone interval (the readings module) and the hole 60 by the core alone.

## 4. The map for David (the estimate of lines after; every stroke keeps every record bit for bit)

Keep as the core (one module, core/act.py, about 60 lines): rule3.carried_division (the one D), node.write and take.move (D with the quotient laid), node.rotate's division (D), the exchange written as K X K (three D's per line), take.lay as the quotient written (one line).

Fold into D, with the primitive named: rule3.division_forward, quotient, remainder, half, odd, signed_quotient (wrappers of D: 32 lines out); paces.rounded and odd_rounded (D at the doubled wall: fold into one `rounded(numerator, wall, sign)`, 10 lines out); rule3.mirrored (item 5, D with the numerator w - 1 - 2 r: 4 lines out); interval.division's riding division (D with the quotient laid, 6 lines fold into node.act); merger.write_ends and bodies.credit's move (the same take at a list of ends: CR-S2's one function, 40 lines out); rule3.least_root and the search of fall_of (TC-S1's iterated D: 30 lines out).

Record-keeping to move out of the Node into one module of the record (record.py): node.start_state's log, turns, stack, counts (COUNTS), bits_of, arrays, census, state_bytes, state_hash; interval.laid_on, Interval.close's frame, node.restore (the frame read back); close.children's log entry, merger.summed, take.momentum_of, bodies.bilinears_of; run.py whole: 366 lines moved, the Node's modules 150 lighter.

Second roads to strike (122 lines): merger.rise_of and rise (fall_of with the direction), merger.share_at and products (gram.share at a window), links.plane_current and links.twist (dead), rule3.least_root (TC-S1), seed.fitted's and wave.least_share's search by comparisons (one `least_at` in the core).

Readings to the Reader's side or to one readings module (1,359 lines; none in the Node's act path): gram.py whole, metric.py whole, links.py's bilinears, readings.py, draw.py, quartet.py (a lattice constant of the loader), seed.py's shapes and wave.py's phases (the loader's), take.fall_of (the count's reading), close.meet and list_of (the Link's readings), interval.readings and kick's momenta.

The estimate after, per module: core/act 60 (new; rule3 213 -> 90: the coefficients wall_of, mass, rule_integers, link_factor, scaled, held_wall, held_numerator, unit_of, share_weight, form_term, lattice, largest_below, balanced_pair stay as readings), node 370 -> 150, interval 282 -> 180, close 310 -> 200, merger 286 -> 140, take 98 -> 40, bodies 173 -> 120, links 128 -> 100, gram 229, metric 72, rows 152, readings 99, paces 142 -> 130, ports 35, seed 357 -> 300, wave 92 -> 80, quartet 399 (moved to the loader), draw 43, run 208 -> record 300 (with the moved record-keeping); the Node's act code (the core and its compositions in node, interval, take) 533 -> about 150 lines, 72 percent out of the act; the engine's function lines 2,959 -> about 2,250 (the second roads 122, the wrappers 250, the act's 380, the record-keeping's 60 of duplication): 24 percent out in all, since the readings do not shrink by the act's fold.

The order of strokes (each bit for bit on the ten worlds and the three records, the kit's make_flagged_copy check): (1) the dead and the second roads out (the audit's list; no course change); (2) the wrappers of D folded (division_forward, quotient, remainder, half, odd, rounded, odd_rounded: the same integers by the identity); (3) the mirror as D (item 5) and the exchange as K X K in the core; (4) the record-keeping moved to record.py (no act changed); (5) TC-S1's division for least_root (approved; the records bit for bit by tc1's measure); (6) the readings module (gram, metric, the Link's turn) moved beside the core; (7) CR-S2's one take at a list of ends over MG-S1 (the audit's item 2, the merger's end with its own form).

## 5. Beneath Rule3

Found, by name: the one forward carried division with its quotient laid on a slot. The carried division, the exchange and the lay are three readings of it: the lay is its quotient written (CR-S1's numerator count times wall), the exchange is mirror o negate o quarter-turn, each a D (the quarter turn Rule3's own step at the own weight 0, the negation the move of -2 a, the mirror the division of w - 1 - 2 r with the quotient 0), and the direction -1 is the conjugation by that mirror. The irreducible letter under it is the floor: the remainder's interval [0, w) (CA-S1's one asymmetric piece), from which the quotient's sign and the mirror follow; no act of the law stands beneath the floor.

The sentence as it would stand in ALGEBRA.md under The Node (the former three primitives kept by name): **The one act** (H-Node-Beneath-Rule3, 2026-10-26): a Node does one act: the carried division of a total by a wall from a remainder, u = total + r, the quotient u div w laid on the slot the direction names, the remainder u mod w kept in [0, w); every act of the law is this act or its composition: Rule3's step (the total from the line's two slots and the six arrivals), the write and the take's move (the numerator at the write wall, count times wall for the move), the quarter turn (the step with no Links at the own weight 0), the negation (the move of twice the level), the remainder's mirror (the division of w - 1 - 2 r, the quotient 0), the slot exchange (the mirror after the negation after the quarter turn), the swap at the top (the exchange conjugated by the row's K) and the act at -1 (the act conjugated by the mirror); the lay is the quotient written and no act of its own; what is not this act is a reading (the bilinears, the Link's record, the paces, the count, the draw, the peak), the frame's record of a reading, or a refusal by name.
