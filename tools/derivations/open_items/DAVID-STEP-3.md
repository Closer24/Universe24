# David's step 3 for the Boss's toy: N identical quanta of a symmetric family hold N quanta (2026-10-27, 07:5x UTC)

The owner's word, in David's session, 07:4x UTC, in translation: "Build it. What is missing: one law the engine does not have, how N identical quanta of a symmetric family sit at one Node so that the energy is N quanta and not N squared; for example the amplitude grows as the square root of N, or the second quantum enters in quadrature with the first. The law needs an exact inverse too. Make sure the toy code holds no numbers, everything read from the world and universe files, and that no bits of 32 or 64 are tied to the engine."

Built in scratch on the Boss's toy boss-toy-1 c389d5580 on top of DAVID-STEP-2.md's rule; the one diff for both steps beside this file as DAVID-STEP-3_DIFF.txt (376 lines, applies cleanly on boss-toy-1; it supersedes DAVID-STEP-2_DIFF.txt).

## 1. The law, derived

A symmetric family's quanta at one Node are one mode: a quantum laid there raises the mode, it does not add a second state beside it. The engine already has the act that raises a mode by a given energy in integers: the exact take at -1 (take.fall_of reversed, MG-S1's light lay), which moves the family's line away from its before by a count of levels. The share is quadratic in the level, so a share of N quanta needs a level of sqrt(N) times one quantum's: the square root comes from the act itself, by comparisons, with no root taken. Two letters make it exact:

1. **The greatest count within what is owed.** The lay moves the line by the greatest count whose rise stays within the quantum plus the family's account at the Node (take.fall_of at -1, one line: the least count paying, less one where it overshoots), so the field never holds more than what was booked.
2. **The account.** What the count leaves, the quantum plus the account less the rise, is kept at the Node in the family's account, the same integer the exact take forward already keeps there (node.take_rem, EX-S1's remainder), below one level's rise; the next lay or take at that Node spends it first. So the energy laid is exactly N quanta: the field's share plus the account.

The inverse: the lay is logged with its count and its account before and after (run.birth's exact_lay, now for every birth that has one, not a merger's alone), and undone by the move back and the account's own difference; the take forward is undone by its account's difference as well (close.click at -1), so every undo is a sum and the undos commute: the state returns bit for bit in any order. The quadrature option of the owner's word is not needed: one mode raised by the exact act is the law's own reading of "the same state".

## 2. The law measured alone (the test beside the diff, tests/test_the_symmetric_lay.py)

On the hole world's board, N light quanta laid at the centre by the account lay, the window's energy read by gram.share over the centre and its six neighbours:

| N | the account lay: energy | the account | the level squared over the first's | the head's quarter-turn lay: energy |
|---|---|---|---|---|
| 1 | 1 quantum less the account | below one level's rise | 1 | 1 quantum |
| 2 | 2 quanta less the account | below | 2 | 4 quanta |
| 4 | 4 quanta less the account | below | 4 | 16 quanta |
| 16 | 16 quanta less the account | below | 16 | 256 quanta |
| 100 | 100 quanta less the account | below | 100 | - |
| 400 | 400 quanta less the account | below | 402 (the level's own integer) | - |

Exact at every N to the digit (the energy plus the account equals N quanta). On a standing sea of light the same: N quanta laid hold exactly N quanta, where the quarter-turn lay made 2.3 quanta for one and 276.8 for sixteen (the cross term with the sea). The inverse, in reverse and in a shuffled order, returns the light's lines and the account bit for bit, on the empty board and on the sea.

## 3. On the worlds (the toy, then step 3; every run back exact 20 of 20, every counter compared)

| world | births | credits | widest integer (bits) | gates SHOWN / NOT SHOWN |
|---|---|---|---|---|
| nature's chiral 60 | 16 to 19 | 2,858 to 3,589 | 112 to 112 | 31 / 16 to 31 / 15 |
| the hole 60 | 16 to 15 | 2,615 to 2,114 | 112 to 112 | 31 / 15 to 29 / 17 |
| the bodies 120 | 20 to 20 | 16,905 to 14,074 | 89 to 89 | 30 / 17 to 26 / 21 |
| the bang world at 20 | 60 to 16 | 14 to 16 | 489 to 213 | 28 / 17 to 26 / 12 |
| the bang world at 48 | 62 to 20 | 99 to 64 | 18,509 to 217 | 36 / 14 to 29 / 13 |

The bang world run on to 100 intervals: the carrier's widest level 24 to 181 bits, bounded; the horizon breathing, every Node frozen at every even interval from 8 and none at the odd ones; matter born at 9 (8), 11 (8), 21 (2), 23 (2) and 95 (2); bodies clicking all through, 142 credits over the 100 (by tens: 0, 16, 16, 24, 8, 0, 8, 24, 16, 30). Step 2 alone left this world with 16 births and no click: the account lay is what lets the merger's light land without making energy, and the bodies click again.

The kit on nature's chiral 60 under step 3: the run back 60 of 60, the momentum law 58 of 58, the flux 60 of 60, the exact take 3,607 of 3,609, the born pair 13 of 18, the births' W sum 16 of 19, the 48 3 of 48; the kit's planes' W at the close 33 of 60 and its close's book 28 of 60 read lower, and both are the kit's own reading of light: its W sums the Wronskian of every plane, light's among them, which carries no charge and whose lines its own lays move; the same kit counting the charged planes alone reads 57 of 60 on the toy and 57 of 60 under step 3, the charge kept; the close's book counts the account's change by a lay as a change not in the log, the field logged in exact_lay (the kit's to re-cut).

## 4. The audit the owner asked for (src on boss-toy-1 with the diff)

- **No number of a universe in the code.** den, node_clock (Gamma), quantum_action (T), trace and amplitude are the universe file's integers; every row's shape, pair and exchange the file's rows; the board's shape, the intervals and the seed the world file's. Derived from them at the load: G from Gamma (rule3.link_unit_of), the clock's table from Gamma (paces), the amplitude's floor from Gamma (phase.floor), A and B from T (rule3.balanced_pair), the drift from T (rule3.largest_below).
- **The literals left, every one the lattice's own count or the writer's sampling, none a universe's:** core/ports.py 2 and 3 (SIDES, AXES), core/acts.py 2 (the birth's halving), core/rule3.py 2, 3 and 4 (the halving, the unit's 3 T s, the held write's 4), rows.py 2, 4, 8 and 10 (the four shapes PLANE, POTENTIAL, QUARTET and CARRIER; the held walls' powers 4 and 2), links.py 4 (the tangent triple's wall 4 Gamma), loader/seed.py 2 and 3 (the envelope's half spans), loader/wave.py 4 (the cycle's Z_4), loader/quartet.py 2, 3 and 4 (the spinor's lattice), run.py 12, 24 and 60 (MARKS and EARLY: when the writer writes the reader's rows, read by no act); the readers' display units (decoder.py's per thousand and per million and the gates' row numbers) are the Reader's. The steps add no literal: the names gate (tests/test_rule3.py) passes on the step-3 tree and fails on the toy itself, on a string my carried-paces diff left at readings.py:21 (`getattr(node, "paces_now", None)`), which this diff mends.
- **No 32 or 64 bits in the engine.** Every integer of every act is a Python int in an object array (rows.zeros, dtype object); no int32, int64, uint or float type in any act; the masks are bool arrays; the one machine integer is core/paces.py:127's index into the clock's table, `(values - low).astype(int)`, an offset of contents on the board and no value of the physics; the numbers 32, 63 and 64 stand in src as the gates' row labels alone (events.py, symmetries.py); WIDTH, ROOM and HALF_WIDTH left the engine at e48273be8.

## 5. The toy's tests

The whole suite on the Boss's toy: 18 failed, 94 passed (its course pins moved by the carried paces and the trace 6, and the names gate on the string above). Under step 3: 19 failed, 94 passed, the new test passing: the names gate passes; two pins more: test_the_node.py's SL-S2 (the merger's light lays -190 levels where it laid -191, the law's own greatest count within the quantum and the account) and SL-S1 (7 births where 6, the draw by exchange). The pins are the Boss's to re-cut with the course or to hold.

## 6. What it does not touch

The runaway's letter on the toy's other worlds (THE-BANG-RUNS-AWAY.md; on the bang world the steps keep it bounded); Bell (DAVID-ON-THE-TOY.md item 7); the emitter's role left in close.list_of, the merger's read_ends and the bodies (DAVID-STEP-2.md section 4); one account per symmetric family when a universe has more than one (the toy's have one, and node.take_rem is its account).
