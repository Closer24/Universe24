# H-Node-Beneath-Rule3-2: the one act beneath Rule3, the inventory, the lean core measured, the map for David

Head: toys-5 3dc12e307 (David's confirmed head). Folder: tools/derivations/open_items/H-Node-Beneath-Rule3-2/ (core_nl2.py, prove_nl2.py, inventory_nl2.py, beneath_nl2.py, out/). Nothing under src/ or tests/ edited; the proof wraps the engine's own functions in the proof script's process and compares.

## 1. The one act (step 0, the unification block, road 4: Rule3)

**The Node in one sentence.** The Node adds to each of its lines' one number the sum of what it reads on its six Links and its own two slots, and reads the level and the remainder back as the quotient and the rest at the wall; nothing else.

**The derivation from the clauses.** ALGEBRA.md, The line: w a_next + r' = SUM_j R_ij arr_j + S_i a_now - w a_before + r, 0 <= r' < w. Write the line's number N = w a + r (the level a, the remainder r in [0, w)). The line says N_next = t + r with t = SUM_j R_ij arr_j + S a_now - w a_before: the new number is the old remainder plus a sum of reads, and a_next = N_next div w, r' = N_next mod w are its two readings (the floor's). The direction (The direction): u = sigma t + rho, z = sigma (u div w), rho' = u mod w. At sigma = -1 the number read is r - t = -(w a_before - r), the same line read by the ceiling: w a_before - r with 0 <= r < w, a_before = ceil((t - r') / w). In one line: forward the number is w a + r (the floor's reading), backward it is w a - r (the ceiling's), and the mirror r -> w - 1 - r is the shift of w - 1 between the two readings of one integer: N = w a - r gives N + w - 1 = w a + (w - 1 - r), which is rule3.carried_division's code at -1 line for line. So:

- P1, the carried division with the direction, divide(t, w, r, sigma) = (sigma q, u mod w), u = sigma t + r, q = u div w: one floor reading of one addition. Checked: divide at -1 equals (-q, r2) with (q, r2) = divide(-t, w, r, +1) and equals rule3.carried_division at both signs, 20,000 of 20,000 (beneath_nl2.py, "direction").
- The mirror is a reading of P1 on the complement: w - 1 - r = divide(-1 - r, w, 0)[1] = divide(-1 - 2 r, w, r)[1] (20,000 of 20,000, "mirror"); the ceiling's reading divide(w a - r + w - 1, w, 0) = (a, w - 1 - r) (20,000 of 20,000, "ceiling").
- The lay is P1 on an exact multiple of the wall with the level carried in the numerator: divide(w (a + c), w, r) = (a + c, r) (20,000 of 20,000, "lay"); take.move is this literally (carried_division(count x wall, wall, rem)).
- The write is P1 with the level carried in the numerator at the write wall: divide(ww a + n, ww, wr) = (a + q, wr') with (q, wr') = divide(n, ww, wr) (20,000 of 20,000, "write").
- The slot exchange with the mirror, X(now, before, r) = (before, now, w - 1 - r), is the direction read at one Node (RW-S1's clause): X R X = R^-1 on random lines, and the step at -1 equals the exchanged step at +1 exchanged back, 20,000 of 20,000 ("xrx"); its two slot writes are P1 on exact numerators (w before onto now, w now onto before, read before written, CR-S2) and its mirror the complement's remainder above.

**So one primitive suffices by the algebra: the carried division with the direction (P1), the floor reading of one addition to the line's number.** The lay (P3) and the slot exchange with the mirror (P2) are its readings, as above. In the code the three stand as three names because each is called with a different numerator (the flux, the count times the wall, the other slot times the wall) and the exchange writes two slots at once; the lean core keeps the three names for the reader and derives P2 and P3 from P1 in their docstrings. The irreducible piece is the floor: by The four acts' theorem every composition of the acts is affine plus a floor's bounded term, and a level is a floor (a number is not a level until it is read at the wall); the addition alone makes no level, and no act of the letter takes a root (TC-S1 folds the take's count onto P1 too).

**The Node's step and the click in the law's notation** (sigma the direction; every act a P1 on a line's number with a named numerator; the reads R_ij, S, D, w, the frames, the turn and the arrivals m_j are readings handed in):

- the step on every line of every row: (a, y) = (now, before)[::sigma]; (lead, r') = P1(S a - w y + SUM_j R_j m_j + flux, w, r, sigma); (now, before) = (lead, a)[::sigma] [node.rotate; the riding lines the same with the kick's momentum as the numerator at the mean wall from the half wall, interval.division];
- the write on a line that writes: (q, wr') = P1(n, ww, wr, sigma); now = now + sigma q [node.write: the carrier's ten lines, the shape-4 row's charge and current, the emitter's emission];
- the swap at the top: every row (now, before, r) -> K (before), K (now), r mirrored 1 + [K_ii < 0] times [node.exchange; FR-S1's trigger a reading];
- the click: every end read (the share's fall, the count: the root as written, TC-S1's P1 iterated by the approved sentence), then every end written: the take's move now = P1(count x w_line, w_line, r)[0] (CR-S1), the children laid A on re_now and B on im_before at the two ends (P1 on exact numerators, GP-S1), the merger's whole levels laid at -1 (MG-S1); backward the same with the counts negated from the frame (RW-S1);
- the run back: the close undone from the frame, the turned Nodes exchanged back, then every P1 at sigma = -1 in the reverse order.

## 2. The inventory (inventory_nl2.py; the table in out/inventory_table.md, 274 functions; the sums in out/inventory_sums.json)

Lines of the 20 modules read (board, clicks, decoder, events, gates, predicates, circle left out): 3,729 = 2,959 in functions + 770 in headers (imports, constants, module docstrings).

| role | lines | where the most of it is |
|---|---|---|
| ACT (the law's act: P1, P2, P3 or their composition) | 500 | node.act, rotate, write, exchange, swap 100; interval.kick, division, lays 81; merger.write_ends, child_at, light_children 81; seed's three lays 152; wave.lay_cycle 55; take.lay, move 12; rule3.carried_division, mirrored 9; close.child_laid 10 |
| READ (a reading, no state move) | 1,458 | quartet 327 (the shape-8 row's matrices derived at the load), gram 168, rule3's integers 113, seed's envelopes and phases 110, bodies 105, interval.readings 87, merger's shares and read_ends 76, links 74, paces 83, readings 64, close.meet and list_of 48, metric 44, take's neighbours and fall_of 43, node's rules and arrivals 37, draw 27 |
| REC (record-keeping: the log, the frame, the census, the counts, the state's containers, the writer) | 518 | run.py 164, node.py 98 (start_state, restore, arrays, census, hashes), close.py 71 (children's log entry, Birth, Kid), interval.py 61 (the frame, laid_on, close), rows.py 51, bodies.credit 42, take.momentum_of 16, merger.summed 15 |
| WRAP (a name for a composition) | 246 | close.births and click 104, node's one-line methods 61, rule3's quotient, remainder, half, odd, rule3, division_forward, signed_quotient 24, interval 21, rows 11, merger.takes 11, seed 9, gram.rest 5 |
| REF (a refusal by name) | 126 | rows.rows_of 34, node.__init__ and node_of 31, close.refused and refuse 28, paces.certified and undecided 18, loader 15 |
| SECOND (a second road, the audit's kind) | 111 | merger.rise_of, share_at, products 64; seed.fitted 28; links.plane_current, twist 12 (dead); wave.least_share 7 |

The law's acts are 500 of 3,729 lines (13 percent); the readings 1,458 (39 percent); the record 518 (14 percent); the headers 770 (21 percent).

## 3. The lean core, measured (core_nl2.py: 67 lines with docstrings, 22 statement lines, 10 functions; integers or whole-board integer arrays alike, no name, no number of a universe, no branch on a row's kind)

The proof (prove_nl2.py): every state-moving function of the engine wrapped in the script's process (rule3.carried_division and its two aliases in node and interval; Node.rotate, Node.write, Node.exchange; take.move and take.lay with every module that imports them by name), each wrapper computing the core's composition from the same reads and comparing bit for bit with the engine's own result at every call, then returning the engine's. Commands (P the venv's python, W the worktree, F this folder):

    cd /dev/shm/tmp/nl2; PYTHONPATH=$W/src TMPDIR=/dev/shm/tmp nice -n 19 $P $F/prove_nl2.py $W node $F/out
    cd /dev/shm/tmp/nl2; PYTHONPATH=$W/src TMPDIR=/dev/shm/tmp nice -n 19 $P $F/prove_nl2.py $W hole /dev/shm/tmp/nl2/out
    cd /dev/shm/tmp/nl2; PYTHONPATH=$W/src TMPDIR=/dev/shm/tmp nice -n 19 $P $F/prove_nl2.py $W chiral /dev/shm/tmp/nl2/out
    PYTHONPATH=$W/src nice -n 19 $P $F/beneath_nl2.py
    PYTHONPATH=$W/src nice -n 19 $P $K/conservation_check.py /dev/shm/tmp/nl2/out/hole_nl2.json board off out $F/out/conservation_hole_nl2.json

Predictions written before the runs: every call equal (0 mismatches), the run back 20 of 20, the hole record equal to the committed one in every key.

Measured (out/proof_node.json, out/proof_hole.json):

- one Node and its six Links (tests/worlds/world_node.json, the 3-cube at 20 through tests/laws.run_back_exact, 20 forward and 20 back): the run back 20 of 20; calls compared: divide 103,680, rotate 440, write 560, exchange 828, lay 6; mismatches 0 (no birth on this world, so no move).
- the hole 60 with back 20 (tests/worlds/world_hole.json through event_universe.run.main): calls compared: divide 5,791,772, rotate 880, write 1,120, exchange 1,311, move 2,625, lay 48,086; mismatches 0; the record against examples/records/hole.json: every key EQUAL (world, universe, den, cube, intervals, gapped, planes, T, gamma, G, counts, turns, rows with the milliseconds struck, nodes, run_back, log of 16,903 entries); the counts 16 births, taken 172701936753844030676249, booked 164947791671769606584854, 1,653 body clicks, 557 turns; the kit's conservation check on that record (board off) 7 of 7 laws in full, the run back 20 of 20, EX-S1 1,669 of 1,669, floats 0.

- the chiral 60 with back 20 (tests/worlds/world_nature.json, out/proof_chiral.json): calls compared: divide 7,855,079, rotate 880, write 1,120, exchange 1,771, move 4,179, lay 63,882; mismatches 0; the record against examples/records/chiral.json: every key EQUAL (the log of 23,579 entries among them); 16 births, 3,119 body clicks, 630 turns.

So every integer the engine moves on the hole 60, the chiral 60 and the node world is moved by the core's three primitives bit for bit, forward and back. What the core does not hold, by name: the readings that form the numerators (the paces, paces.py; the Link's factor, frame, phase pair and fold, links.py, metric.py, readings.py; the arrivals turned, node.arrivals; the stress parts; the share, gram.share; the take's count, take.fall_of, the root the letter still writes, TC-S1's P1 iterated by the approved sentence); the record (the log's entries, the frame's push and pop, the census, the counts); the refusals by name (the loader's, the close's). The core cannot run a board alone: the interval's order of acts and the click's list of ends are programs over the core (interval.run, close.click), and they are kept as the engine's own in the proof.

## 4. The map for David

Keep as the core (fold onto core_nl2's three names, one module core/acts.py of about 70 lines): rule3.carried_division, mirrored (P1 and the mirror); node.rotate's division and slot shift, node.write, interval.division's riding division (P1 then P3 with the slots placed); node.exchange (P2 with K); take.lay, take.move, merger.child_at's lay (P3, the exact P1). After: the Node's act functions about 70 lines where 100 (node) + 12 (take) + 9 (rule3) stand.

Fold (the primitive named): interval.lays -> write (P1 P3); merger.write_ends' two branches -> move and lay (P1 P3) with the log dict formed in the record module; merger.light_children -> move or child_at (P1 P3); close.child_laid -> child_at (P3) and the senses' reading; node.act's two orders -> the one path already (RW-S1), kept; seed's lay_world, lay_uniform, lay_packet, wave.lay_cycle -> one lay of a levels tuple (P3) with the envelopes and phases as readings handed in (152 + 55 lines to about 60).

Record-keeping to move out of the Node into one module of the record (record.py): node.start_state, restore, arrays, census, state_bytes, state_hash, bits_of, COUNTS; interval's frame (Interval.__init__'s pop and close's push, laid_on, count_max, max_transient); close.children's log entry, Birth, Kid, refused; merger.summed; take.momentum_of (the booking); bodies.credit's entry; run.py whole. 518 lines, about 400 after (the audit's item 6: one dict for every take).

Second roads to strike (bit for bit by the kit's flagged copy): merger.rise_of (fall_of at -1), merger.share_at and products (gram.share at a window), seed.fitted, wave.least_share and the two searches in seed (one least_at in rule3), links.plane_current and twist (dead), quartet.gadd (dead): 111 lines to 0; the two gap branches (interval.py:149, close.py:115) folded onto links.coupling_of by arithmetic.

Readings to move to the Reader's side or to a readings package (no state move): quartet.py whole (327, the load's derivation), gram.period, cosine_count, density (37), bodies.frame_of and bilinears_of (46), draw.read_number (27, the frame's digit), close.list_of; the interval's readings and the Link's record stay the Node's reads (readings.py, links.py, metric.py, paces.py) since the step needs them, about 870 lines.

The estimate after, per module: core/acts 70; node (the class: the rows, the rules, the act's program) 120; interval (the five acts as a program over the core) 110; close with merger (the click as a list of ends over the core) 170; take and draw 60; record 400; readings (paces 142, links 110, metric 72, readings 99, gram 180, rows 110, loader 41, seed's and wave's envelopes 150) about 900; quartet 330 (the Reader's or the loader's). Total about 2,160 of 3,729 (42 percent out) with the readings kept as they stand; the Node's own acts 70 lines where the owner asked for tens to 200; the rest of his 70 percent lies in the readings and the record, which the acts do not touch.

The order of strokes, every record bit for bit at each (the kit's flagged copy check, the hole 60 and the chiral 60): (1) the dead and the second roads struck; (2) core/acts.py with the three names, node.write, take.move, take.lay, the riding division and node.rotate's division calling it (this folder's proof is the check: every call equal); (3) the record module, the log dicts spelt once; (4) node's one-line wrappers struck, the callers through the module's function (the audit's item 10); (5) the seed's four lays onto one lay with the envelopes as readings; (6) quartet to the loader or the Reader's side; (7) TC-S1 built (the count as P1 iterated), fall_of, rise_of, least_root and the root's search struck, which needs the approved sentence and tc1's 830 of 830.

## 5. Beneath Rule3: found, by name

Found: the one integer act beneath the carried division is the addition to the line's number, N' = N + sigma t read by the floor at the wall, of which the division (the floor forward, the ceiling backward: the mirror the shift w - 1 between the two readings), the slot exchange (the direction read at one Node, X R X = R^-1) and the lay (the addition of an exact multiple of the wall) are three readings; every identity 20,000 of 20,000 (beneath_nl2.py) and every state move of the hole 60, the chiral 60 and the node world one such act (prove_nl2.py). The sentence as it would stand in ALGEBRA.md under The Node:

"**The Node adds.** Each line of the Node holds one number, w a + r, the level a its quotient at the wall and the remainder r its rest; every act of the Node on a line adds to that number a sum of integers it reads (its own two slots, the six arrivals, the file's integers) and reads the level and the remainder back: Rule3's step with the flux, the write with its numerator at the write wall, the take's move and the lay with a count times the wall. The direction is the sign on the sum and on the quotient, the number read by the ceiling backward and by the floor forward, the remainder's mirror w - 1 - r the shift between the two readings; the exchange of the two slots at the top is that direction read at one Node; so one function with the direction moves every integer of the Node, and the floor is its one irreducible piece: a number is not a level until it is read at the wall."

## 6. Bugs met on the way (Addition 10)

None that breaks a record. Named for David as they stand on this head: src/event_universe/node.py:323 `digit_of` returns its two arguments unchanged (a name for nothing, called once from draw.py:32); src/event_universe/interval.py:149 and close.py:115 the two branches on the gap outside links.coupling_of (the audit's item 5, still open on this head); src/event_universe/links.py:92 `plane_current` and :126 `twist`, quartet.py:129 `gadd` dead (the audit's items 1 to 3, still on this head); src/event_universe/gram.py:134 a local import of division_forward inside `share` (a style, not a bug); merger.walls_of lays a child on zero lines through child_at, which books a momentum on zero arrays and discards it (a reading wasted, not a bug).
