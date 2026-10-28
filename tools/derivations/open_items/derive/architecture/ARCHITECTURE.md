# Tensor24: the architecture of the new engine

The architect's design, APPROVED WITH CHANGES (REPORT.txt). Nothing in it is built.

- **The plan:** tools/derivations/open_items/TENSOR24.md at 8f012b9b2: sections 2, 19, 20, 27, 28, 30 (item 11, (a) to (u)) and 31.
- **The law:** docs/ALGEBRA.md on scribe-5: Postulates 2 to 5 (lines 31 to 35), lines 92 (locality), 94 (the 24), 98 (the tick), 102 (no circularity), 106 (no bound and no floor; every bound a carry; only generic laws).
- **The gate:** tools/derivations/open_items/scribe_scan.py on scribe-5 (its STRICT, READER_FOLDERS, DECODER_KEEPS, CARRY_HOME and import_ok).
- **David's generic core** (14:47 and 14:49 UTC, #2187 6472174198 and 6472218585): five laws, each here one table or one function (section 0).
- **The owner's words of 14:5x and 15:0x UTC:** how the board runs asynchronously, huge boards, and how information crosses the Meshes; then his correction of 15:0x UTC: the whole board is one big bang, the main run is synchronous, the detectors' clicks change the information from bang to bang, and the asynchronous runner stays an option for huge boards (section 4).

## 0. The core: five laws, five places

| David's law | its one table or function | module | the plan's law |
| --- | --- | --- | --- |
| 1. The kind table (2O): per kind its lifts, its still pairing B, T = J K (T T its sign), its intertwiners C_K | the table KINDS, built once by kinds(shape) | engine/kinds.py | the group, section 19 |
| 2. The tick: the one formula, every Mesh coupling its two ends alike (M Hermitian) | step, with shift and pull | engine/mesh.py, engine/step.py | law 2 |
| 3. The turnover: T = J K on every gear, at the clock's own top, as a carry | turnover | engine/step.py | law 4, items (h), (s) |
| 4. The click: law 6 on the composite, counting the action | click_whole (whether and how many) and click_split (which part) | engine/click.py | laws 5, 6, 9 |
| 5. Every bound a carry; the rate one dial whose whole turn is "no tick this tick" | carry, and beat (the rate dial) | algebra/carry.py, engine/step.py | laws 1, 11 |

**Does the core fit the packages and the gate?** Yes, with four conditions:
- the carry and the Gaussian ring go to a fifth folder, algebra/, which the decoder may import (change 1 of REPORT.txt);
- law 1's table is computed from the shape, never typed; its twin rows are exact over Z[i] only for the half-turn lifts (OPEN 3);
- law 2's "one hand per quantum" is a fixed row count per Node-clock until the owner rules 11 (a); a list that grows at run time breaks line 98 and is not built;
- law 3's trigger (X_c a universe integer, the bottom as a borrow) meets item 10 (the bottom trigger withdrawn) and law 10 ("a ceiling typed to bring one about is a bound"): OPEN 7. turnover takes the count q as an input, so only the trigger's one term changes. Law 3's "each Node-clock at its own top" is the act's place (each Node-clock turns its own gears); the bang is whole-board, every Node-clock at its top at once (the owner's correction of 15:0x UTC; no local turnover, item (v) withdrawn).

## 1. The objects and the state

**The objects** (no object holds state but the arrays below; each is an index into them):

| object | in the arrays | from |
| --- | --- | --- |
| the Node-clock | one column x of every state array; N = the product of the shape's sides | the piece |
| the Spoke | one of 2d signed unit vectors, the shape's identity and its negative | the piece (d = the count of axes) |
| the Mesh (link) | the pair (x, j) for the d positive Spokes; it holds no state (Sofer): g_j, Q_j and U_j are read from its two ends' slots each tick, once per Mesh, the far end taking the conjugate (law 2's M Hermitian by construction) | derived |
| the train | a block of rows [g0, g1) of G, its card in the layout: its kinds (indices into KINDS), its own part (1, 2 or 4), its time rank, its pinion, rim and s, its weight, its winding, its drive teeth, its coupling rows | the calibre |
| the gear | one row g of G at one Node-clock: a, b, r, rd; its teeth count derived each tick, never stored | law 2 |
| the hand | two rows (three o'clock, twelve o'clock): z = a[re] + i a[im], a Gaussian integer | section 3 |
| the twin hand | two hands (psi1, psi2), four rows; read as (rho, S) | sections 3, 27 |

**The state** (Python integers in numpy object arrays, dtype=object everywhere):

| array | shape | holds | law |
| --- | --- | --- | --- |
| a | (G, N) | the notch now | law 2 |
| b | (G, N) | the notch before (a-) | law 2 |
| r | (G, N) | the fine tooth | laws 1, 2 |
| rd | (G, N) | the drive's fine tooth (always 0 where the drive teeth are 1) | law 2's K |
| e | (H, N) | the wind's fine tooth r_E of each winding the calibre lists (a hand, a composite) | law 5 |
| go | (1, N) | the turnover dial: H's going, the frame f and the pawl as one dial (Sofer; David's law 3); its teeth the order of T on the Node-clock's kinds, read from KINDS (2, or 4 where a twin kind stands) | law 4, (h), (s) |
| ph | (1, N) | the rate dial's remainder (David's law 5) | law 11 |
| tb, tn | (1, N) each | the local times of the before slot and the now slot (the count of rounds at which each was written) | line 98 |

G = the sum over trains of (the dimension of its kinds) times its own part; H = the windings the calibre lists. Both are fixed at load.

**Line 98, the integers per Node-clock: 4G + H + 4, fixed for the run.**
- **The going fits:** one dial per Node-clock (go), fed by the turnover's carry; it is no second carried integer per gear (line 805, item (j)).
- **One hand per quantum does not fit as a list:** a train's hands per Node-clock are its rows, a calibre integer fixed at load; the fitting cannot add rows. Fixed rows cap the quanta per Node-clock, a bound law 11 forbids. **OPEN, the owner's item 11 (a)**; no code depends on the row count beyond the layout.

**The layout** (integers, read-only, built once by load): per row g of G its train, kind, component, own index, time rank, coefficients (pinion, rim, s, weight, winding, drive teeth, the stage flag: its own teeth or the lapse) and T's row (tperm, tsign, the conjugated rows, eps = T T); the lapse's row index; nb (2d, N), the six neighbours of every Node-clock, the torus's wrap as Rule3 on the coordinates; the contraction plans (section 3).

## 2. The generic functions: the whole engine

Z is an integer or an object array of integers, a Gaussian integer is a pair of Z, a twin hand a pair of Gaussian integers. Every function is pure: every input passed, nothing hidden.

**algebra/** (standard library only; the same code serves integers and object arrays):

| function | signature | its term (section 19) | lines |
| --- | --- | --- | --- |
| carry | carry(n: Z, d: Z, r: Z) -> (Z, Z) | law 1: n + r = q d + r', 0 <= r' < d; the one place // and the remainder are written | 10 |
| home, flip | home(w, go, sides) -> Z; flip(r, w) -> Z | draft H: the fine tooth's home (w - go) div sides; the turnover's flip w - 1 - r (item (e)) | 8 |
| nonneg, choose | nonneg(n) = 1 + n div (n n + 1); choose(k, x, y) = k x + (1 - k) y | the one whether, a quotient (the gate's own sign test) | 8 |
| the Gaussian product | mul(z, w), conj(z), norm(z) = z conj(z), pair(z, w) = conj(z) w (its real part the dot, its imaginary part the cross) | section 3; the wind, the lead | 20 |
| the twin forms | overlap(phi, psi), reverse(psi) = (-conj psi2, conj psi1), axis(psi) -> (rho, S) | laws 6 and 7 | 20 |

**engine/** (numpy object arrays):

| function | signature | its term (section 19) | lines |
| --- | --- | --- | --- |
| kinds | kinds(shape) -> Kinds | David's law 1: the 24's weights, the lifts, B, J, eps = T T, C_K per kind pair | 100 |
| contract | plan(kinds, layout, couplings) -> Plan; contract(p: Plan, f, g) -> field | law 2's J; the wind's A1; the composite's parts | 40 |
| shift | shift(layout, s: State, u) -> (2d, rows, N) | law 2's U_j a_j: the six Spokes at once, through nb, each read by seen (section 4) | 30 |
| pull | pull(layout, s: State, j) -> field | law 2's F = sum_j g_j (U_j a_j - a) - D a + J, with the gearing W, s, Q_j, g_j, D | 50 |
| step | step(layout, s: State) -> State | law 2: p = W (a - b) + (r - home); p+ = p + s F + K, K = T_k s carry(J, T_d, rd); a+ and r+ by carry; two stages (own teeth, then the lapse) | 60 |
| turnover | turnover(layout, s: State, q: Z) -> State | David's law 3: T^q = (J K)^q on every gear, slots exchanged, r flipped, go advanced by q (a carry modulo its teeth), T^-1 = eps T | 35 |
| beat | beat(layout, s: State) -> (State, Z) | David's law 5: (k, ph') = carry(ph, Gamma, rate); k ticks, 0 is "no tick this tick" | 10 |
| click_whole | click_whole(layout, s: State) -> Whole | law 5 on every composite: (q, r') = carry(E, winding, e); q leaves, r' stays | 50 |
| click_split | click_split(layout, s: State, w: Whole) -> Split | laws 6 and 9: sizes by B and C_K, the draw's c and room, t by carry(c sum sigma, room), the part by the cumulative quotients; one part: no choice | 70 |
| books | books(layout, before, after, o: Out) -> Booked | law 8, per Node-clock: every quotient that left and every remainder, signed | 25 |
| load | load(universe: Columns, world: Columns) -> (Layout, State) | section 28: the calibre, the piece, the setting; the integers of the files as columns | 90 |
| tick, untick | tick(layout, s, at) -> (State, Out); untick(layout, s, at, o) -> State | law 3: tick = step, the trigger's q, turnover, the clicks, books at the Node-clocks at; untick = o's writes taken off, T^-q, then T^-1 step T | 30 |

Nothing else stands in the engine. The owed writes (what a click writes, the unspringing, the setting's lay; draft A) live inside click_whole, about 60 lines.

**Out**, what tick emits (dense, per Node-clock): the clicks (whole and split, with every field section 31's record names), the turnover's q, the additive writes, the rate, the wind, the sweep and the push, and the booked remainders. The runner turns it into events and the ledger; untick takes it back from the undo log.

## 3. How the tensors connect

**The layout of a field:** (components, N). The components are the train's kind dimensions times its own part, stored where the 24 act as signed permutations (A1, A2, T1, T2, and the three diagonal tensions for A1 + E); E serves the contractions and the tests, never the storage (section 31). The Spokes are an axis of their own: shift returns (2d, rows, N), and pull sums over it.

**The kind table (David's law 1), compiled once from the 24's lifts, with no typed table:**
- the candidates are the Spokes' d-fold power (an index grid from the shape); each is weighed by an exact Rule3 quotient, 1 on the signed permutations of determinant +1 and 0 elsewhere. No candidate is dropped: every group sum is an einsum over the candidate axis with these weights (neutral elements; no filter, no loop, no branch);
- the twin kinds' lifts: the half turns' lifts (Q8) are built from the own part's identity by the ring's product; the lifts of the quarter and third turns are OPEN 3;
- per kind K: its matrices on the storage basis; B_K, the A1 intertwiner of K x K; J_K with T = J K, and eps_K = J conj(J), +1 on the 24's five kinds and -1 on the twin kinds;
- **one contraction table per kind pair:** C[K1, K2 -> K3], of shape (dim K3, dim K1, dim K2) times the own parts' ring product, the weighted group sum of the pair's matrices on a seed of eye(d), normalized by its own seed entry with an exact quotient (remainder 0, tested). The characters stand only in the tests.

**How a train's kind selects its contractions, with no branch on its name:** the calibre's coupling rows are integers (train i and its operand, train k and its operand, the target train m, the strength c), and every train carries its kinds as indices. plan gathers C at (kind i, kind k -> kind m) by those indices and expands it over the trains' rows into four index arrays: rows1, rows2, target, coef. In a step, contract is one gather, one product and one scattered sum over the whole plan. A channel the table does not hold contributes 0, and the files' checker names it. No step reads a name, a kind or a train index as a condition; the names in the files stay labels for the record's header.

**T per gear (David's law 3):** compiled at load from each row's kind (J K), its own part (conj on a hand, reverse on a twin hand) and its time rank; a gear whose stored value is a rate takes its source's sign, read from the coupling rows. It stands as tperm, tsign and eps per row.

## 4. Allowed and forbidden, by folder; the two runs

| folder | may import | refused | allowed | notes |
| --- | --- | --- | --- | --- |
| algebra/ (new) | the standard library | NUMBER, TABLE, FLOAT, IMPORT, DTYPE, CIRCLE, ROOT, WORD, OPERATION (outside carry.py), CLAMP, LOOP, REFUSE, STATE, MEMO, LOGREAD, BRANCH, COMPARE, MIX, ISOLATE | // and the remainder in algebra/carry.py alone (the carry's home, moved from engine/carry.py) | INDICATOR on nonneg |
| engine/ | algebra, record, numpy | all seventeen, with MIX and ISOLATE | none | INDICATOR only on the turnover's q, the click's q and pick, the beat's k and the 24's weights at load; each read by Sofer for a mask |
| record/ | the standard library, record | all seventeen | none | the schema alone |
| readings/ | the standard library, record, readings, algebra | all seventeen | none | one formula per event or per emitted array; no sum written as a loop |
| runner/ | algebra, readings, record, numpy; never engine/ or decoder/ (the step is passed in) | NUMBER, FLOAT, IMPORT, DTYPE, CIRCLE, ROOT, WORD, TABLE, STATE | LOOP, BRANCH, COMPARE (the schedule), LOGREAD in runner/rewind.py alone | the files read into columns here |
| decoder/ | the standard library, record, readings, algebra | NUMBER, FLOAT, IMPORT, DTYPE, CIRCLE, ROOT, WORD, TABLE, STATE, OPERATION, REFUSE, CLAMP | LOOP, LOGREAD (the record), BRANCH, COMPARE, min and max as reductions | never engine/, runner/ or numpy |
| tensor24/main.py | engine, runner | every rule but the imports | none | about 15 lines: passes load, beat, tick and untick into the runner |

**Where a loop may live:** in runner/ (the rounds and the rewind check), in decoder/ (its folds over a finished record), and in the tests. Nowhere else in src/tensor24.

**Where the log may be read:** the undo log (each round's Out, kept by the runner beside the record) is read by runner/rewind.py alone: the rewind check, which undoes every click from its log (law 3; item (o), approved 14:37 UTC). The record is read by decoder/ alone and is never fed back. The engine reads no log: untick receives the logged Out as an argument.

**The synchronous run: the main way** (the owner's correction of 15:0x UTC):
- every dial at the full rate, so the beat's k is 1 at every Node-clock in every round, and every read is the now slot: the head's pass, run against the head one act at a time by the comparison harness (section 31);
- **the bang is whole-board:** the great clock's swing, every Node-clock at its top at once. The act stays turnover at each Node-clock, its q its own trigger's carry; from the one seed every Node-clock reaches its top in the same round, so the whole board turns with no read of the great clock. A reading that can fail: the decoder reads the round of every turnover, per region and over the board, and their spread must be 0. Where the tops part, a whole-board turnover would be an act that reads the whole great clock, which line 92 refuses: OPEN 7, the owner's;
- **no local turnover** (item (v) withdrawn): no region bangs while its neighbours run on;
- **the palindrome is broken by the clicks:** the reversed run leaves them undone (item (o), approved 14:37 UTC); what a detector's click wrote runs on into the next bang, so the information changes from bang to bang;
- **the readings per bang** (decoder/, no engine act): the bangs' count and their recurrence (the rounds between tops), row 46 per bang (every bang shows more), and the spread above, each per region and over the board.

**The asynchronous runner: an option, for huge boards** (the owner's words of 14:5x and 15:0x UTC; line 98; David's law 5):
- **Each Node-clock owns its clock.** The rounds are the reader's count and no observable (line 98). In every round each Node-clock beats once: its rate dial takes its rate, the lapse W, by Rule3, (k, ph') = carry(ph, Gamma, W). Where k is 1 it ticks; where k is 0 it has "no tick this tick", and its slots and local times stand.
- **The reads.** A tick reads only its own slots and its six Meshes' slots as they stand at the round's start, each with its local times (tb, tn): reads before writes, so the ticks of one round are order-free, and integer sums make the clicks' additive writes order-free too. The read is one term, seen(b_y, a_y, tb_y, tn_y, t): "past" takes the now slot; "lin" weighs the two slots by their local times (David's formula; item 11 (u), the owner's; Sofer and David recommend lin). Both bodies give the now slot alone where every dial is equal.
- **How information crosses a Mesh without sticking.** A Mesh holds nothing (Sofer). Each end holds its own two latest slots with their local times, overwritten only by its own tick, so nothing queues and nothing piles up on a link. Each tick reads its neighbours' latest slots, so every neighbour's newest state enters at the reader's next tick. A fast neighbour's intermediate states are not queued: its own ticks fold them into its latest slots. A slow or stopped clock's slots stand and are read as they are. A word crosses one Mesh per round at most (Postulate 3), and none crosses a stopped clock.
- **The order is a function of the state:** a Node-clock ticked in round n exactly where its tn equals n. The rewind check undoes round n by the same test, runs the rate dial back by Rule3 with its remainder, takes the clicks' writes from the undo log, and inverts the step as T^-1 step T. The rewind stays exact, and the order needs no log of its own.
- **The engine never sees the order.** beat and tick act on the arrays and the index set the runner passes. They see no round, no mode and no region: the neighbour's slots and its local times are all the step needs from the runner.

**Checks on the coordinator's design** (its points 1 to 5):
1. CONFIRMED, corrected in one word: the slots belong to the Node-clocks, not to the Mesh.
2. CORRECTED. "Tick when no neighbour's next tick comes before its own" (Chandy, Misra and Bryant, with zero lookahead) never deadlocks, since the earliest next tick can always go. But it needs the next tick time as a division by the rate, with no divisor at rate 0. Under it a stopped clock never ticks again, never re-reads its Meshes and stays frozen for ever, against Postulate 4 (line 35). The beat is the same discipline with a lookahead of one round, and every clock re-reads its rate each round.
3. CONFIRMED. A stopped clock beats with k = 0, blocks no one, and its slots are read as they stand. Its restart is the formula's (the horizon, OPEN 11).
4. CORRECTED. Under either order a neighbour is never ahead of the round being read, so lin has no interpolation between a neighbour's slots across the reading moment. It reads the neighbour's two latest slots by their local times. That is item (u)'s formula, not the order's.
5. CONFIRMED (below).

**The two runs are one law.** The synchronous run is the asynchronous runner with every dial equal. A test that can fail: on a setting with every dial equal, the two give the same record and the same ledger, byte for byte.

**The bang in the asynchronous runner:** one global step of the runner, its one barrier. A Node-clock whose tick emits its top (q not 0) has "no tick this tick" from then on, until every region reports its top; then one step of the runner calls turnover on every Node-clock at once, and the beats resume. The barrier is the runner's schedule, never an engine act. Between bangs the Node-clocks tick on their own dials in the beats' order.

**Huge boards:**
- the board is split into regions; each region runs its own rounds;
- only the boundary slots and their local times cross between regions, as halos;
- round n of a region starts once its adjacent regions have finished round n - 1, so adjacent regions stay within one round of each other and far regions drift freely: no global barrier between bangs, and the region with the least round can always go;
- at the top, the bang's one barrier (above);
- a Mesh across a boundary is computed by the region that owns its positive Spoke, and its additive writes to the far end travel in the next halo;
- each region keeps its own undo log, and the rewind check runs region by region in reverse with the halos exchanged backward. The exact rewind stays the log-reading check.

## 5. The decoder

Separate, Animate's. decoder/ imports the standard library, record/, readings/ and algebra/, and never engine/, runner/ or numpy. It computes the 80 rows from the record alone, with the ledger file as the conservation rows' second reading (those rows read NOT READ without it). Each row declares its two readings' fields, disjoint (tested), with one control record that reads SHOWN and one that reads NOT SHOWN. An unknown major version is refused, an older one upcast. The converter from the head's records (Animate's, about 150 lines) is a tool outside src/tensor24.

## 6. The line budget

| module | lines |
| --- | --- |
| algebra/carry.py | 30 |
| algebra/ring.py | 40 |
| engine/kinds.py (kinds, plan, contract) | 140 |
| engine/mesh.py (shift, pull, with the gearing and seen) | 80 |
| engine/step.py (step, turnover, beat, tick, untick) | 135 |
| engine/click.py (click_whole, click_split, the draw, the owed writes) | 180 |
| engine/books.py | 25 |
| engine/load.py | 90 |
| **the engine with algebra/** | **720** |
| the formulas that close OPEN items inside the build | 130 |
| **the engine's total** | **850** |

Around it: record/ 60, readings/ 120, runner/ 260 (rounds 80, regions and halos 70, files 40, ledger 30, rewind 40), main.py 15, decoder/ about 950 (section 31's), the tests about 650, the comparison harness about 250.

## 7. The order of the cuts

1. **The gate amended** (Sofer's files, on the owner's word): algebra/ and its wall; the carry's home in algebra/carry.py; decoder/ and readings/ may import algebra/; main.py's imports. No line of src/tensor24 before it.
2. **record/:** schema version 1; Animate's converter and the decoder on the converted records, in parallel with every cut below.
3. **algebra/:** after the owner's yes on (h) (the going, the home, the flip) and on the tie rule. Tests: the unique (q, r'), q(-p) = -q(p) at both parities, T M T = M^-1 on draft H's box.
4. **kinds and load:** the kind table. Tests: the characters, the images (the 24 on the state, the translations, a board that is no cube as the control), rename, eps on the eight kinds. No twin train loads before OPEN 3 closes.
5. **shift, pull and step:** law 2, after OPEN 1, 5 and 11 have their formulas in section 19; the comparison harness one act at a time against the head.
6. **turnover, beat, tick and untick:** after OPEN 7. Tests: bijectivity both ways, the palindrome toy, the dial's order.
7. **click_whole and click_split:** after OPEN 2, 9, 10 and 14; the draw's distribution test as a gate.
8. **books and the runner:** the rounds, the regions, the ledger, the undo log and the rewind check; the asynchronous-against-synchronous test; the ledger's byte-for-byte test.
9. **Section 8's capability table** read on both engines' records; then the switch.

## 8. What stays OPEN, and where it closes inside the build

| # | open | item | closes before cut | whose |
| --- | --- | --- | --- | --- |
| 1 | law 2's N (the drive's numerator, J's metric half in place of held_numerator), U_j (the Mesh's turn on Z[i]: the units, Z4, or lifting shears; Hermitian), J (the calibre's rows through C_K); the divisor W+ >= 1 proved | M1 | 5 | David |
| 2 | law 5 at w_c = 0 (the light) and at a negative E: the quantum per mode; David's law 4 counts the action (item (r)) against law 5's fixed winding | M2, (r) | 7 | the owner rules (r); David the formula |
| 3 | the twin hands' 24 beyond the half turns: the quarter and third turns' lifts over Z[i]; 2O's table (E1/2 x T1 = E1/2 + G3/2) | M5, M6 | 4 | David |
| 4 | the asynchronous read: past or lin, the one term seen; and whether the lapse enters the dial, the formula's W, or both | (u), M7 | 8 | the owner; David the formula |
| 5 | the cap's step: matter's step a turn (Bessel) or the leapfrog; David's law 2 claims the cap from M Hermitian, which the carries keep only up to the remainders (section 27) | (q) | 5 | David, the owner |
| 6 | one hand per quantum against line 98 | (a) | 4 | the owner |
| 7 | the turnover's trigger as a carry: David's carries(X - Gamma, X_c - Gamma) with the bottom as a borrow, against law 4's weak maximum, item 10's withdrawn bottom trigger and law 10's typed ceiling; and the whole-board bang where the Node-clocks' tops part, which no local act gives (line 92) | R9, (d), (f), (v) | 6 | David, Sofer, the owner |
| 8 | the going, the home and the flip in place of the one mirror | (h), (e) | 3 | the owner (Sofer: yes) |
| 9 | Pauli's one premise, the pair dial; eps from KINDS | (m) | 7 | the owner |
| 10 | the draw's fairness: a composition free of the sort, the room with no cap | item 6, M3 | 7 | David, Sofer |
| 11 | law 11 against the stability bounds: F2's lower side, F5, the horizon. David's rate dial is the candidate for F2's upper side and the horizon. The engine writes none of them | (p), (i) | 5 | David, the owner |
| 12 | every bang shows more: the detector's click (draft K) | (d), (f), (t) | after 7 | David, Animate |
| 13 | the charge Q* under M Hermitian (Noether up to the remainders); no second carried integer | (j), (n) | 6 | David |
| 14 | what a click writes, the unspringing, the setting's lay | draft A | 7 | David |
| 15 | the doubler's vacuum | (g) | 5 | David |
| 16 | the readings of momentum, current, stress, spin, angular momentum and helicity, with their second readings | section 19 | the decoder | David, Animate |
| 17 | Bell at a distance: a contradiction that stands; no composite beyond one Mesh | item 2, (l) | none | the owner |

No OPEN item is written as a placeholder, a fallback or a clamp. Its cut waits for its formula in section 19.
