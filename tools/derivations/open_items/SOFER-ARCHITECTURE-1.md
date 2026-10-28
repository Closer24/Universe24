# The architecture of the new engine, in one place

Sofer, 2026-10-28, 15:3x UTC, draft 2, for the owner (his words of 15:0x UTC: "you need to centralize the architecture ... it should be with me within half an hour"), the Boss, David and Animate. Draft 2 is aligned with the architect's approved design (the Boss's eaf07f596: tools/derivations/open_items/derive/architecture/ARCHITECTURE.md and REPORT.txt, "APPROVED WITH CHANGES"; the plan's section 31 says where it and the design differ the design stands). It stands on the law (docs/ALGEBRA.md at scribe-5, 1,913 lines), the plan (TENSOR24.md), the gate (SCRIBE-GATE-1.md) and the owner's words of 2026-10-28. It makes no law: where it proposes a sentence it says so and asks, and nothing is entered before the owner's word.

**One architecture, two documents that point to each other.** The design holds the modules, the signatures, the state, the lines and the order of the cuts. This file holds what the law says about them, in the order the owner reads: the closed list of operations, the data, the functions, how Node-clocks speak, the build with the law's test at each stage, the laws against each other, the gate. Where the two differ, the design stands and this file is corrected within the hour.

**One page, for the owner.**
1. The Node-clock includes its six Meshes and every operation it does (line 90: its own gears and its six Meshes' gears; line 88: the Mesh's one act takes the two ends' integers and holds none of its own).
2. Its operations are three, on whole numbers: **addition, multiplication and Rule3's carry**. Nothing else is on the list, so nothing else needs forbidding (section 1). The architect's algebra folder already holds exactly these (carry, nonneg, choose, the Gaussian product).
3. The law already closes the Node-clock at two levels (line 88, five functions and nothing else; line 90, one act). The third level, the operations, is the one the owner just named; the gate becomes a closed list (section 7).
4. How a Node-clock speaks to another: only through the Mesh between them, and what it says is a carry added at the receiving end; each Node-clock beats on its own dial, reads its neighbours' latest slots with their local times, and writes its own gears only; the order of work is the runner's (section 4). The main run is synchronous, the asynchronous run an option, and with every dial equal they give the same bytes.
5. The click law (line 156) is the only premise by name in the law; it works exactly (checked on the eight kinds); its derivation from a bigger law is open (section 6, item 10).
6. The build is the architect's nine cuts, each with the law's test that can fail; one cut is proposed before the board, so that clocks come first (section 5).

## 1. The closed list: what a Node-clock may do

The Node-clock is its own gears and its six Meshes' gears. Its one act (line 90) is one division with a carried remainder over one integer contraction of them, the same for every train, every gear read before any is written. Everything that act is made of is one of three operations:

| operation | on what | what it leaves |
| --- | --- | --- |
| addition (its inverse is the sum with a product by -1) | whole numbers; a Gaussian integer as two whole coefficients | nothing |
| multiplication | the same; the complex product is (a c - b d, a d + b c), no angle | nothing |
| Rule3's carry: n = q d + r, 0 <= r < d, d a teeth count (at least 1) | whole numbers | the quotient q leaves as a carry or an event; the remainder r stays |

Two things are no operation on a number and stand beside the list. **Reading** a gear, its own or a Mesh's, is locality (line 92): the Node-clock reads itself and its six Meshes and nothing else, and writes its own gears only. **Holding** a gear is the Node-clock's own state, a fixed count of integers (line 98). The cube's 24 act on a tensor as signed permutations (products by 0, 1 and -1, and sums), so the 24's operations are on the list too.

**What the list makes of the names we forbid.** Each is a sum and a product of carries' quotients, so none needs a place of its own and none can stand as a name (all verified on ranges of integers):

| a name | the carry it is |
| --- | --- |
| a whether, an if | the bit nonneg(n) = 1 + n div (n n + 1), 1 where n is at least 0 and 0 below, a bit for every integer; n < d is the quotient of n by d being 0 |
| a choice | b x + (1 - b) y, with b a bit (the architect's choose) |
| a minimum, a maximum | min(a, b) = a - nonneg(a - b) (a - b); max(a, b) = b + nonneg(a - b) (a - b) |
| equality | nonneg(a - b) nonneg(b - a) |
| a bound, a floor, a clamp | the remainder of the clock whose teeth count is the bound, its quotient the event (law 11: every bound is a clock's carry) |
| a count | a sum of bits |

So the closed list is complete for the logic the engine needs, and the gate need not name the dodges one by one. What it leaves out by construction: a power, a shift, a bit operation, a true division, a float, a root, a circular function, a comparison as an operation, a branch, a loop that makes a formula, a raise (a declaration), min, max, abs, clip and where, a sort.

**The one promise the list needs: a divisor is a teeth count, at least 1.** The clock that makes the divisor keeps it (the rate dial's carry), the files' checker (outside the engine) shows it at load, and the engine writes no raise; on Python integers a zero divisor fails loudly and is never silent. Where the divisor is a state gear (F2's tension t = (Gamma a) div X) the domain is the rate dial's own (David's Theorem B3, CHECKED: X at least Gamma is the stable side); item (p) is the owner's. The click of a whole at the light, w_c = 0, is the same promise unkept: the architect's OPEN 2.

**Three closed levels, two already in the law.**
1. The functions (line 88): the Node-clock is five functions and nothing else, rotate(train), drive(trains), swap(train), click(trains) and link(i, j).
2. The act (line 90): one division with a carried remainder over one integer contraction.
3. The operations (proposed, the owner's idea of 15:0x): addition, multiplication and Rule3's carry. Postulate 5's body already says it second: "its step is Rule3's division with its carried remainder and the sums and products around it", after "the Node-clock holds no if". **The proposal leads with it and closes it** (line 35, no line moved, the heading kept, the first clause's new text alone): "the Node-clock's operations are addition, multiplication and Rule3's carry, on whole numbers (a Gaussian integer as two whole coefficients) and nothing else; a whether, a sign, a bound and a choice are sums and products of carries' quotients, so the Node-clock has no if". The rest of the postulate stands. It enters on his word.

## 2. The data: vectors and tensors

The architect's state (design sections 1 and 3), read against the law:

- **Nine arrays, Python integers in numpy object arrays, dtype=object everywhere:** a, b, r, rd of shape (G, N) (the notch now, the notch before, the fine tooth, the drive's fine tooth), e of shape (H, N) (the winds' fine teeth), and go, ph, tb, tn of shape (1, N) (the turnover dial, the rate dial's remainder, and the local times of the before slot and the now slot). G counts every integer component of every train, H the windings the calibre lists, N the sites. **4G + H + 4 integers per Node-clock, fixed for the run (line 98): it fits.** The teeth counts are derived each tick, not stored.
- **The going fits as one dial per Node-clock** (the architect, from my finding that the going, the frame and the pawl are one object, the Node-clock's ratchet): its teeth are the order of T on the Node-clock's kinds, 2, or 4 where a twin kind stands. The law's ratchet has two teeth (lines 618 and 1911); the four-tooth dial is the two-tooth ratchet with one more two-tooth dial fed by its carry, and the twin hands' count modulo 4 is the architect's one dial.
- **One hand per quantum does not fit as a list** (line 98 against line 156): a train's hands per Node-clock are its rows, a calibre integer fixed at load, and the fitting cannot add rows. Item (a), the owner's.
- **The layout** (read once at load, never state): the table of the six neighbours of every site (nb, 2d by N), the torus's wrap as Rule3 on the coordinates; the kinds' integer matrices and the product table, compiled from the 24's lifts and never typed; the contraction plans; the universe file's integers (couplings, Gamma, the width) and the world and seed files, the only numbers anywhere. The couplings stand in the calibre as rows of integers (the owner's word of 15:1x); a row the 24 forbid is refused at load, by the files' checker.
- **The ring:** a hand is a Gaussian integer, two coefficients; the twin hands are two. The twin hands are exact over Z[i] for the half turns only, so the 24 bit for bit on them waits on the architect's OPEN 3 (David's ring).
- **The 24 on the storage:** fields are stored where the 24 act as signed permutations (T1, T2, A1, A2 and the three diagonal tensions); E has no such basis and serves the contractions and the tests, never the storage.
- **The width** is a key of the universe file, no limit of the engine; the files' checker reports an integer past it and changes nothing.

**The tensor operations, the engine's whole vocabulary** (each is made of the three operations or is addressing):

| operation | form | made of |
| --- | --- | --- |
| gather (the stencil) | f[:, nb]: the six Spokes at once, one axis of the result | addressing only; the one operation that crosses sites, and it crosses one Mesh |
| contraction | the plan: a gather, a product, a scattered sum over the calibre's rows | multiplication, addition |
| pointwise sum and product | on arrays | addition, multiplication |
| carry | q = u // d, r = u - q d | Rule3; the floor division and the remainder written once, in algebra/carry.py |
| choice | b x + (1 - b) y, b = nonneg(q) | multiplication, addition, one carry |
| signed permutation | an index gather and a product by 0, 1 or -1 | multiplication, addition |
| Gaussian product | (a c - b d, a d + b c) | multiplication, addition |
| scatter-add | the write at the receiving site; order-free because addition is associative | addition |
| layout | reshape, stack, transpose, an axis moved | addressing only |

## 3. The functions the engine implements

The architect's functions (design section 2) against the law's five (line 88), one map:

| the law's function (line 88) | the design's functions | folder | the operations |
| --- | --- | --- | --- |
| (under all of them) | carry; home, flip; nonneg, choose; mul, conj, norm, pair; overlap, reverse, axis | algebra/ (standard library only) | the three operations |
| rotate(train) | step, with contract, shift and pull | engine/ | one carry over one contraction |
| drive(trains) | the source J inside pull: one routine over the calibre's rows | engine/ | contraction |
| swap(train) | turnover(layout, s, q): T applied q times, the slots exchanged, r flipped, go advanced by a carry | engine/ | one carry (the top), T as a phase reversal |
| click(trains) | click_whole (whether and how many), click_split (which part), the draw | engine/ | carry; the one whether is a quotient |
| link(i, j) | shift, pull: the Mesh's g_j, Q_j, U_j read once from its two ends, the far end taking the conjugate | engine/ | gather, product, sum; M Hermitian by construction |
| (the Node-clock's own tick) | beat: (k, ph') = carry(ph, Gamma, rate); tick, untick | engine/ | one carry |
| (readings) | books; load | engine/ | sums; the files into the state |

Nothing else stands in the engine. The law's list stays as built until the new engine stands (line 90: unbuilt, the five functions standing as the built form); then the law names the new list, on the owner's word.

## 4. How a Node-clock speaks to another

The law (line 98): every Node-clock steps by the same function on its own tick; whenever every Node-clock has reached the same count the great clock is one bit for bit, whatever the order; a synchronous pass is the engine's order of work and no law. The architect's design realizes it, and this is its reading in clocks:

1. **The channel is the Mesh, and it holds nothing.** Each end holds its own two latest slots with their local times, overwritten only by its own tick, so nothing queues and nothing piles up on a link. A neighbour's newest state enters at the reader's next tick; a fast neighbour's intermediate states are folded into its latest slots by its own ticks. A word crosses one Mesh per round at most (Postulate 3), and none crosses a stopped clock.
2. **The word is a carry.** A Node-clock never writes into a neighbour. A click that joins two ends of a Mesh is two one-ended acts: the quotient is offered as the Mesh's odd number (the count n_ij, line 88: +n at one end, -n at the other) and added at the receiving site (the design: "writes as additive gathers at the receiving site"). Each end writes its own gears by what it reads, which is what lines 86, 88 and 92 say; the plan's risk 3 (locality against two-ended clicks) closes in this form.
3. **The beat is the Node-clock's own tick.** In every round each Node-clock beats once: its rate dial takes its rate W by Rule3, (k, ph') = carry(ph, Gamma, W). Where k is 1 it ticks; where k is 0 it has "no tick this tick" and its slots and local times stand. A stopped clock re-reads its rate every round, so it is never frozen for ever (Postulate 4); the coordinator's next-tick order froze it, which the architect refused.
4. **Reads before writes.** A tick reads its own slots and its six Meshes' slots as they stand at the round's start, each with its local times, so the ticks of one round are order-free and the additive writes order-free too (integer sums). The read is one term, seen(b, a, tb, tn, t): "past" takes the now slot, "lin" weighs the two slots by their local times. Where every dial is equal both give the now slot alone. Which one is item (u), **the owner's** (David and I recommend lin); the design holds one place for it.
5. **The order is a function of the state.** A Node-clock ticks in round n exactly where its tn equals n, so the rewind check undoes round n by the same test, runs the rate dial back by Rule3 with its remainder, takes the clicks' writes from the undo log and inverts the step as T^-1 step T. The order needs no log of its own, and **the engine never sees a round, a mode or a region**: the runner passes the index set and the engine acts on the arrays.
6. **The two runs are one law.** The main run is synchronous: every dial at the full rate, k is 1 everywhere, every read is the now slot, the bang is whole-board (the owner's word of 15:0x). The asynchronous run is an option for huge boards: the board in regions on their own rounds, only boundary slots and their local times crossing as halos, adjacent regions within one round of each other, one barrier at the top. The determinacy of a network of channels (Kahn's) gives the guarantee: **with every dial equal the two give the same record and the same ledger, byte for byte**, a test that can fail. The region rule is the rule I would give each Node-clock alone: step when every neighbour has reached the round before (the arrivals have stood), which keeps neighbours within one tick and a Node-clock up to d ticks ahead of one d Meshes away.
7. **Two more tests that can fail** (mine, for the runner's cut): the **order test**, many random schedules of the same board giving the same bits at equal counts, with a mutant that reads a neighbour's now where the count calls for before; and the rewind check under a random schedule.

What the law leaves to the owner here: (u) past or lin; whether the lapse enters the dial or the formula or both (the architect's OPEN 4); the whole-board bang where the Node-clocks' tops part, which would need a read of the whole board that line 92 refuses (OPEN 7, the plan's item (w)). The owner's word of 15:0x makes the bang the great clock's swing; law 10's former sentence, that every Node-clock turns at its own top, is corrected on it (section 6, item 11).

## 5. The build, stage by stage

The Boss writes every line (section 21 of the plan); each cut is approved by all four (Sofer on the laws and the gate, David on the formula, Animate on the bench, a fresh adversarial read), mine within 15 minutes of the post. The architect's nine cuts, each with the law's test that can fail (every test is shown failing on a broken copy), and one cut proposed between 3 and 4:

| cut | what is built | the law it stands on | done when (a test that can fail) |
| --- | --- | --- | --- |
| 1 | the gate amended (Sofer, on the owner's word): the fifth folder and its walls, the carry's home, the closed list | lines 35, 98, 102; the owner's 15:0x idea | the self-test 0 parted; each wall refused forward and back; no line of src/tensor24 before it |
| 2 | record/: schema version 1; Animate's converter and the decoder in parallel with every cut below | plan section 31 | the record byte for byte the same with the ledger and without it |
| 3 | algebra/: carry, home, flip, nonneg, choose, the Gaussian ring, the twin forms | lines 90, 98; law 11 | q, r unique and n = q d + r exact; q(-p) = -q(p) at both parities (the tie rule, decided first, plan risk 2); T M T = M^-1 on draft H's box; nonneg a bit on every integer; the ring's laws exact |
| 3b (proposed) | the clocks before the board: one clock (N = 1) and two clocks over one Mesh (N = 2) on the scalar kind, with beat, tb and tn, the first shift and pull | lines 88, 92, 98; Postulates 1 and 3 | rewind 20 of 20 and bijective both ways; the order test; synchronous equals asynchronous at equal dials; the one-Mesh reach |
| 4 | kinds and load: the kind table compiled from the shape, the plan | lines 90, 94 | the characters; all 24 turns bit for bit on every chart with a board that is no cube as the control; the rename test; eps on the eight kinds; no twin train before OPEN 3 closes |
| 5 | shift, pull, step on every train alike | lines 90, 96; plan section 19 | the formula against the naive loop model (David, side 3 or more); the head compared act by act, unexplained differences 0; after OPEN 1, 5 and 11 have their formulas |
| 6 | turnover, beat, tick, untick | lines 106, 1602; laws 4 and 10 | T T = +1 on A1 and -1 on the twin hands; T S T = S^-1 at every teeth count; the rewind through the top 20 of 20; the dial's order; after OPEN 7 |
| 7 | click_whole, click_split, the draw, the owed writes | lines 156, 1079 | the books closed; the exchange sign on the eight kinds; the draw's distribution; each reading with its second reading; after OPEN 2, 9, 10 and 14 |
| 8 | books and the runner: rounds, regions, the ledger, the undo log, the rewind check | plan section 31 | asynchronous equals synchronous byte for byte at equal dials; the ledger's byte-for-byte test |
| 9 | section 8's table of capabilities read on both engines' records; then the switch | plan sections 8 and 12 | the table read on both; the end check |

**Why cut 3b.** The owner's method is clocks first, then tensors, then the 24's operations. The architect's order puts the kind table (the 24) at cut 4 and the step (the clock) at cut 5. A first board of one and two clocks, scalar only, shows the carry, the dial, the local times and the Mesh speaking before any tensor stands, so every later cut runs on clocks already shown to speak. It costs one cut of about 100 lines of tests and no engine line beyond cuts 3 and 5.

The click law's derivation (or its exactness shown again) is due before cut 7, not before cut 1: the clocks, the Mesh, the 24 and the turnover stand without it.

## 6. The laws against each other

Where the laws agree, where they meet and where they do not yet agree. A law is cited by its line in docs/ALGEBRA.md.

| # | the pair | status |
| --- | --- | --- |
| 1 | Postulate 5 (no if, line 35) and law 4's trigger at the top | agree: the trigger is the quotient of the time gear's carry (law 11); the trigger's one term (X_c, the bottom as a borrow) is the architect's OPEN 7 |
| 2 | Postulate 5 and the click of a split's draw | agree if the one whether is one carry's quotient: draft K's select is choose(nonneg(t - sigma_up), the down write, the up write), the algebra folder's own forms; SCRIBE-GATE-1.md calls it "the one comparison" and is corrected to say so |
| 3 | law 9's draw, digits composed "in the order of their values" (line 1079), and the closed list | **meet:** a sort is a comparison network, refused; the architect's OPEN 10 asks a composition free of the sort (symmetric sums commute) so alike images draw alike; the plan's law 9 omits the sort without naming the departure |
| 4 | law 10 (time a circle for the gears) and laws 3 and 4 and line 1602 | agree since the owner's word of 14:37 (way 2), entered; draft K proves why a many-to-one click breaks the mirror only at itself (K1) |
| 5 | law 11 (every bound a carry) and F5's rate-dial clamp, F2's lower side | **meet:** the lower side's carry (the Node-clock's own tick) is not yet run; item (p), the owner's; the plan's law 6 still says "capped at the modulus" while the design's change 8 says the room has no cap: the design stands |
| 6 | locality (line 92) and two-ended clicks (plan risk 3) | agree as two one-ended acts with the quotient added at the receiving end (section 4, item 2) |
| 7 | the 24 bit for bit (line 94) and the twin hands exact over Z[i] for half turns only | **depart:** the plan's section 24, item 6 asks the 24 of what the clicks show for the twin hands; the architect's OPEN 3; named in the plan's laws 5 and 6 |
| 8 | Postulate 3 (one Mesh per tick) and rates (the local tick) | **meet:** "light crosses one Mesh per local tick" is the "past" read; item (u), the owner's |
| 9 | the fixed count of integers per Node-clock (line 98) and one hand per quantum (line 156) | **meet:** fixed rows by the kind's cap, one hand a family for the force carriers; item (a), the owner's |
| 10 | "only generic laws are approved" (line 106) and the click law (line 156) | agree **by name**: the click law is the only premise by name (lines 106 and 559 only mention it); it works exactly, checked on the eight kinds (draft E: +1 on A1, A2, E, T1, T2; -1 on E1/2, E5/2, G3/2; the books close); its derivation from a bigger law is open: the route is that the pair is one composite clock (what two Node-clocks do at one count, and a click is a clock's carry), David's draft J finds no derivation from the board's acts, and Animate's kind-keeping click (6472946096, a candidate, not checked on the board) is a second route; the pair's one directionless event stays the premise |
| 11 | the board's run and the bang: law 10's sentence (my entry of 14:54, that the board is asynchronous and every Node-clock turns at its own top) and the owner's word of 15:0x (the whole board one big bang, the main run synchronous, the detectors' clicks changing the information from bang to bang) | **corrected on his later word** (the law's text); the plan's runner row still says the main way is asynchronous while the design and his 15:0x word say synchronous: the design stands, the row is to be corrected |
| 12 | no raise in the engine and a zero divisor | agree: the files' checker keeps every divisor at least 1; the loud failure is the language's |
| 13 | the record cannot rebuild the state, and the rewind (line 98: the check that reads the log) | agree since the 14:37 entry: the undo log is read by runner/rewind.py alone, the record by the decoder alone, no act reads a log; the plan's law 3 sentence "a click is undone only from its log" is lawful as the check's reading |
| 14 | the law's five functions (line 88) and the design's functions | agree by the map of section 3; the law names the new list after the build |
| 15 | draft K's finding (K2: on a finite board every reading taken per bang is eventually periodic) and law 10's "every bang adds more" | **meet:** the clicks' record grows at every bang that clicks (K4); that the gears themselves grow bang after bang needs an unbounded board with carries kept (law 11); item (d), the owner's reading of "more" |

The **departures** the build carries by name: item 7 (the twin hands), the loader's exchange key (line 156: the sign declared per train until the table gives it), law 9's order (item 3), and the head's typed constants the calibre will hold as data.

## 7. The gate as a closed list

The owner's idea turns the gate round. It now names what is forbidden, one rule a dodge (the comparison rule names twenty-three functions and the clamp rule sixteen), and says in its own text that it counts masks (and, or, not, &, | and ~) nowhere. A closed list needs no dodge named: **in algebra/, engine/ and readings/, anything not on the list is refused by default.** Written by Sofer in scribe_scan.py as a rule beside the others (which keep printing their precise law); the vocabulary stands in one place at the head of the script, and the architect's additions go through Sofer by a ledger entry with the law line each serves.

The architect's change 1 is in the same pass: **a new folder, algebra/, beside record/, engine/, readings/, runner/ and decoder/, and tensor24/main.py** (spared no rule, so it holds no loop, branch or number), the carry's home moved to algebra/carry.py (the one place // and the remainder are written), the scatter-add np.add.at(out, index, values) named on the list as the contraction's scattered sum, and the walls as the design's section 4 has them: algebra/ the standard library alone; engine/ algebra, record and numpy; readings/ the standard library, record, readings and algebra; runner/ algebra, readings, record and numpy and never the engine or the decoder; decoder/ the standard library, record, readings and algebra and never the engine, the runner or numpy; main.py imports the engine and the runner and is the only place they meet. runner/ and decoder/ keep the readers' rules (they loop, compare and branch over a record).

It is built (scribe_scan.py): the self-test runs 689 cases, 0 parted; SCRIBE-GATE-1.md holds the vocabulary, the walls and the report.

## 8. What I ask

**The owner** (at 16:00 with the plan; my recommendation first in each):
1. Postulate 5 restated as the closed list (section 1): yes.
2. The gate as a closed list in the engine's folders, and the architect's new folder: yes (built; the report stands in SCRIBE-GATE-1.md).
3. A Node-clock never writes into a neighbour; the word is a carry added at the receiving end (section 4): yes.
4. The click law stands as the premise by name for the plan on its exactness; its derivation (or the exactness shown again) is due before cut 7: yes.
5. Item (u), the neighbour read as "lin" (David and Sofer): your word.
6. Law 10's sentence is corrected to your picture of 15:0x (one big bang, the main run synchronous, the asynchronous run an option; ALGEBRA.md line 106, no line moved), on the Boss's account of your word: please confirm it.

**The Boss:**
1. The architect is taken and approved (cc9da2198): thank you. Please read section 4 against the design's section 4 and tell me where they differ; I correct this file.
2. State in the plan what is built at each cut, as section 5 has it, with each cut's test and its approvals; and take cut 3b or tell me why not.
3. Correct the plan's text where it differs from the design: the runner row (main way synchronous), law 6's "capped at the modulus" (the design's change 8), law 4's "does not turn (Sofer)" (the law's pinned rest, line 1602) and the sentence that gives draft H the one mirror, law 5's "a click where q is at least 1" (q clicks, the remainder booked), law 9's order (the departure named), and the whether(q) of section 20 (a bit only for q at least 0; nonneg(n) is a bit for every integer).
4. Adopt the gate in the build's clone before the first line (SCRIBE-GATE-1.md, "Where it runs"), the closed list included once I post it.
