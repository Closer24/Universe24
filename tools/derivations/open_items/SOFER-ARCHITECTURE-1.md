# The architecture of the new engine, in one place

Sofer, 2026-10-28, 16:3x UTC, draft 4, for the owner (his words of 15:0x UTC: "you need to centralize the architecture ... it should be with me within half an hour"), the Boss, David and Animate. Draft 4 is aligned with the one architect's ruling (the Boss's 8eaf350f2: tools/derivations/open_items/derive/architecture/RULING.md and its probes), which rules between draft 1 of this file and the approved design (derive/architecture/ARCHITECTURE.md and REPORT.txt, "APPROVED WITH CHANGES"); the plan's section 31 says where the ruling and the design differ the ruling stands, and the Boss's tie rule (6474542826) keeps the going per gear, as Sofer reproduced it (200,000 of 200,000). It stands on the law (docs/ALGEBRA.md at scribe-5, 1,958 lines), the plan (TENSOR24.md), the gate (SCRIBE-GATE-1.md) and the owner's words of 2026-10-28. It makes no law: where it proposes a sentence it says so and asks, and nothing is entered before the owner's word.

**One architecture, two documents that point to each other.** The design holds the modules, the signatures, the state and the lines. This file holds what the law says about them, in the order the owner reads: the closed list of operations, the data, the functions, how Node-clocks speak, the build with the law's test at each stage, the laws against each other, the gate. Where the one architect's ruling differs from either, the ruling stands, and both are corrected to it.

**One page, for the owner.**
1. The Node-clock includes its six Meshes and every operation it does (line 90: its own gears and its six Meshes' gears; line 88: the Mesh's one act takes the two ends' integers and holds none of its own).
2. Its operations are three, on whole numbers: **addition, multiplication and Rule3's carry**. Nothing else is on the list, so nothing else needs forbidding (section 1). The architect's algebra folder already holds exactly these (carry, nonneg, choose, the Gaussian product).
3. The law already closes the Node-clock at two levels (line 88, five functions and nothing else; line 90, one act). The third level, the operations, is the one the owner just named; the gate becomes a closed list (section 7).
4. How a Node-clock speaks to another: only through the Mesh between them, and what it says is a carry added at the receiving end; each Node-clock holds a beat count, its beat is due when its six neighbours stand at a count at least its own (a product of six bits, inside the engine), it reads a neighbour as of its own count and writes its own gears only, and a stopped clock blocks no one; the runner chooses only which due beats fire (section 4). The main run is synchronous, the asynchronous run an option on the same rule, and with every dial equal they give the same bytes.
5. The click law (line 156) is the only premise by name in the law; it works exactly (checked on the eight kinds); its derivation from a bigger law is open (section 6, item 10).
6. The build is the ruling's twelve stages, clocks first, then tensors, then the 24's operations, each with a test that can fail (section 5).

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
| a power with a state exponent (the turnover's T^q, q the top's quotient, 0 or 1 in a tick) | choose(q, T x, x), one choice of a signed permutation by the bit q |
| a sort (law 9's digits "in the order of their values") | a rank count: rank_i = the sum over j of [v_j < v_i] plus the sum over j < i of [v_j = v_i], each bracket a product of nonneg bits, the composed number the sum over p of place[p] times (P v)[p] (the ruling, section 8 (i)) |

So the closed list is complete for the logic the engine needs, and the gate need not name the dodges one by one. What it leaves out by construction: a power with a state exponent, a shift, a bit operation, a true division, a float, a root, a circular function, a comparison as an operation, a branch, a loop that makes a formula, a raise (a declaration), min, max, abs, clip and where, a sort. The plan's former whether(q) = 1 - 1 div (q + 1) is no sign test (a zero divisor at q = -1, 2 below it); whether(q) = nonneg(q - 1), a bit at every integer, its divisor n n + 1 at least 1 always.

**The one promise the list needs: a divisor is a teeth count, at least 1.** The clock that makes the divisor keeps it (the rate dial's carry), the files' checker (outside the engine) shows it at load, and the engine writes no raise; on Python integers a zero divisor fails loudly and is never silent. Where the divisor is a state gear (F2's tension t = (Gamma a) div X) the domain is the rate dial's own (David's Theorem B3, CHECKED: X at least Gamma is the stable side); item (p) is the owner's. The click of a whole at the light, w_c = 0, is the same promise unkept: the architect's OPEN 2.

**Three closed levels, two already in the law.**
1. The functions (line 88): the Node-clock is five functions and nothing else, rotate(train), drive(trains), swap(train), click(trains) and link(i, j).
2. The act (line 90): one division with a carried remainder over one integer contraction.
3. The operations (proposed, the owner's idea of 15:0x): addition, multiplication and Rule3's carry. Postulate 5's body already says it second: "its step is Rule3's division with its carried remainder and the sums and products around it", after "the Node-clock holds no if". **The proposal leads with it and closes it** (line 35, no line moved, the heading kept, the first clause's new text alone): "the Node-clock's operations are addition, multiplication and Rule3's carry, on whole numbers (a Gaussian integer as two whole coefficients) and nothing else; a whether, a sign, a bound and a choice are sums and products of carries' quotients, so the Node-clock has no if". The rest of the postulate stands. It enters on his word.

## 2. The data: vectors and tensors

The architect's state (design sections 1 and 3), read against the law:

- **Ten arrays, Python integers in numpy object arrays, dtype=object everywhere:** a, b, r, rd and go of shape (G, N) (the notch now, the notch before, the fine tooth, the drive's fine tooth, the gear's going), e of shape (H, N) (the winds' fine teeth), and ph, tb, tn, c of shape (1, N) (the rate dial's remainder, the local times of the before slot and the now slot, and the beat count). G counts every integer component of every train, H the windings the calibre lists, N the sites. **5G + H + 4 integers per Node-clock, fixed for the run (line 98): it fits** (the design's 4G + H + 4 with the beat count c by the ruling, and the going per gear by the tie rule of 6474542826). The teeth counts are derived each tick, not stored.
- **The going fits as one two-tooth dial per gear** (the Boss's tie rule, 6474542826, reproduced by Sofer: with home(w, go) = (w - go) div 2 and the step on p + home, a gear's negation, a and b to -a and -b, r to w - 1 - r, go to 1 - go, commutes with the step in 200,000 of 200,000 cases at teeth counts 1 to 12, both parities, and the fine tooth stays inside [0, w); a going left unchanged under the negation commutes in 99,385 of 200,000): each gear's going is its own pawl, the law's ratchet of two teeth (lines 618 and 1911), and T toggles it exactly where T's sign on that gear reverses its stride (the layout's tsign per row). The 24's turns negate some gears of a Node-clock and not others, which a going shared by the Node-clock cannot follow. The frame is the same object seen from the Node-clock: each gear's going is its image, so my reading of draft 3, one dial per Node-clock, is withdrawn. Whether the twin kinds' turnover (T T = -1) needs more than the per-row going is the question of the build's stage 8 (T S T = S^-1 at every teeth count, the 24's images bit for bit).
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
| swap(train) | turnover(layout, s, q): T applied q times, the slots exchanged, r flipped, each gear's go toggled where T's sign on it reverses its stride | engine/ | one carry (the top), T as a phase reversal |
| click(trains) | click_whole (whether and how many), click_split (which part), the draw | engine/ | carry; the one whether is a quotient |
| link(i, j) | shift, pull: the Mesh's g_j, Q_j, U_j read once from its two ends, the far end taking the conjugate | engine/ | gather, product, sum; M Hermitian by construction |
| (the Node-clock's own clock, line 98) | beat: the beat count c, the due bit (the product of six nonneg(c_nb - c)), (k, ph') = carry(ph, Gamma, rate); tick, untick (the same act at -1) | engine/ | one carry; sums and products of bits |
| (readings) | books; load | engine/ | sums; the files into the state |

Nothing else stands in the engine. The law's list stays as built until the new engine stands (line 90: unbuilt, the five functions standing as the built form); then the law names the new list, on the owner's word.

## 4. How a Node-clock speaks to another

The law (line 98): every Node-clock steps by the same function on its own tick, "each Node-clock stepping only when the arrivals it needs from its six neighbours stand"; whenever every Node-clock has reached the same count the great clock is one bit for bit, whatever the order; a synchronous pass is the engine's order of work and no law. The one architect's ruling (derive/architecture/RULING.md, section 4, with its probes) fixes it, and this is its reading in clocks:

1. **The channel is the Mesh, and it holds nothing.** Each end holds its own two latest slots with their local times, overwritten only by its own tick, so nothing queues and nothing piles up on a link. A neighbour's newest state enters at the reader's next beat; a fast neighbour's intermediate states are folded into its latest slots by its own ticks. A word crosses one Mesh per beat at most (Postulate 3), and none crosses a stopped clock.
2. **The word is a carry.** A Node-clock never writes into a neighbour. A click that joins two ends of a Mesh is two one-ended acts: the quotient is offered as the Mesh's odd number (the count n_ij, line 88: +n at one end, -n at the other) and added at the receiving site. Each end writes its own gears by what it reads, which is what lines 86, 88 and 92 say. This holds only if everything a Node-clock reads across a Mesh is a notch with its before slot; a fine tooth read across a Mesh would need a slot of its own, which the Boss checks against section 19's formulas at stage 3.
3. **Each Node-clock holds a beat count c, and its beat is due inside the engine.** The beat is due when each of its six neighbours stands at a count at least c: due = the product of six nonneg(c_nb - c), read across its six Meshes, a carry on counts, local, no if. It is the Node-clock's own law (line 98), and the engine sees counts and slots, never a round, a mode or a region; c equals the runner's round only in the synchronous run.
4. **Every allowed due beat advances c by one and turns the rate dial by Rule3,** (k, ph') = carry(ph, Gamma, W). The gears step only where k is 1. Where k is 0 ("no tick this tick", always for a stopped clock) the count advances and the gears, the two slots and their local times stand, so a stopped clock blocks no one (Postulate 4). My first text wrote go = due x allowed x (the rate bit), which advanced neither the count nor the dial at a "no tick" and froze the board around a stopped clock (the architect's probe: a ring of 10, one clock at rate 0, the counts held between 0 and 5 for ever); the rule is corrected, and with it every count reaches 30 and 40 of 40 random schedules equal the synchronous pass.
5. **A Node-clock reads a neighbour as of its own count c:** the neighbour's now slot where its tn is at most c, else its before slot; one choice by one bit, written once, in link. The slot chosen by the count difference alone reads a stale slot after a "no tick" (the order test: 0 of 40 once rates part, 40 of 40 read by tn). tb serves lin only. Item (u), **the owner's**, is past or lin: lin is one carry with divisor tn - tb, at least 1 by construction, since the before slot is older; the ruling closes (u) before stage 3.
6. **The runner chooses only which due beats fire.** The main run fires all of them every sweep: synchronous, whole-board, the head's order, one big bang (the owner's 15:0x). The asynchronous run is an option on the same rule: random masks and, for huge boards, regions with halos, which are the same rule at a region's grain and add no law. A hold the runner needs (the bang's barrier in the option) is passed as a "no tick" on the rate bit, never as a withheld beat. The determinacy of a network of channels (Kahn's) gives the guarantee: the state at count t is a function of the start within t Meshes, whatever the order.
7. **The rewind** has the mirror rule (a Node-clock steps back when no neighbour is ahead of it); k at the beat being undone is 1 exactly where tn = c, so the dial runs back by Rule3 with its remainder, the clicks' writes come off the logged Out, and the step inverts as T^-1 step T.
8. **Asynchronous-ready from the first stage:** c, the due bit and the allowed mask stand in the first beat written (stage 2), and the order test runs from stage 3, so no signature changes late.

**Tests that can fail:** the order test (40 random masks equal the synchronous pass at equal counts, rates parted, one clock stopped; the mutant that reads by count difference fails it); the stopped-clock test (its count advances, its gears stand, no neighbour waits); the rewind under a random schedule; synchronous equals asynchronous with every dial equal, byte for byte.

What the law leaves to the owner here: (u) past or lin; whether the lapse enters the dial or the formula or both (the architect's OPEN 4); the whole-board bang where the Node-clocks' tops part, which would need a read of the whole board that line 92 refuses (OPEN 7, the plan's item (w)). The owner's word of 15:0x makes the bang the great clock's swing: no local turnover, every Node-clock turning over in the same round, each by its own act.

## 5. The build, stage by stage

The Boss writes every line (section 21 of the plan); each stage is approved by all four (Sofer on the laws and the gate, David on the formula, Animate on the bench, a fresh adversarial read), mine within 15 minutes of the post. The ruling's twelve stages (its section 6; the plan's section 12 carries the same table): clocks first, then tensors, then the 24's operations, the owner's method. No line of src/tensor24 before stage 0; every test is shown failing on a broken copy; record/, the decoder and Animate's converter run in parallel from stage 0.

| stage | what is built | law lines | its test that can fail | OPEN that closes first |
| --- | --- | --- | --- | --- |
| 0 | the gate amended: algebra/ and its wall, the carry's home in algebra/carry.py, the closed list in engine/ and readings/, main.py; the three files and their checker; record schema 1; the harness on a trivial engine | 86, 88, 106; plan 21, 31 | the scan refuses a planted if, a literal 2 and a sort in engine/; the harness fails on a mutant | the owner's yes on the closed list (Postulate 5's first clause) and on the gate amendment |
| 1 | algebra/carry.py: carry, nonneg, choose, home, flip, forward and at -1 | 35, 90, 98; law 11 | n + r = q d + r' exact, 0 <= r' < d, unique; q(-p) = -q(p) at both parities; nonneg exact across 0 | items (h), (e) and the tie rule |
| 2 | one clock: a gear with its fine tooth; beat: the rate dial, the count c, the due and allowed bits, tb and tn | 34, 35, 98; law 11 | rewind 20 of 20, bijective both ways; a rate-0 clock beats, its count advances, its gears stand | none |
| 3 | two clocks over one Mesh: link (each coefficient once, the far end conjugate), the slot read by tn, the arrivals rule; the runner's synchronous pass and random masks | 88, 92, 98; Postulates 3, 4 | the order test: 40 random masks equal the synchronous pass at equal counts, rates parted, one clock stopped; the mutant reading by count difference fails it; the rewind under a random schedule | item (u), past or lin, the owner's |
| 4 | the board: nb from the shape (the wrap as Rule3 on the coordinates), the gather over the six Spokes, the scalar light with its spring (shift, pull, step on one train) | 92, 98; Postulate 3 | the one-Mesh reach test forward and backward; the formula against a naive loop model on side 3 or more; equal to the head on the light alone, act by act | 1 (N, U_j, J; W+ >= 1), 5 (the cap's step), 11 (F2, F5, the horizon), 15 (the doubler's vacuum) |
| 5 | the ring: algebra/ring.py (mul, conj, norm, pair); the hand (two rows), the twin hand (four rows): reverse, overlap, axis | plan 3; Postulate 2 | the ring's laws exact; T T = +1 on a hand, -1 on a twin hand | none |
| 6 | the kinds and the contraction: kinds(shape) as weighted group sums, plan and contract as index arrays; load: the calibre's trains and coupling rows | 88, 90, 94 | the characters; a coupling the table lacks gives 0 and the checker names it; the rename test | 6 (item (a)); 3 for any twin train (none loads before it) |
| 7 | the one act on every train alike: step over the plan, two stages (own teeth, then the lapse) | 90, 96; plan 19 | the formula test; the head compared act by act, unexplained differences 0 | 1 and 5 for every train; 13 (the charge under M Hermitian) |
| 8 | the 24's operations: the 24 on the state; the turnover, T = J K per row, T^q as a choice by q, the going per gear; tick and untick | 94, 106, 1602; laws 3, 4, 10 | all 24 turns bit for bit on every chart, a board that is no cube as the control; T S T = S^-1 at every teeth count; the rewind through the top 20 of 20; the bang's spread 0 | 7 (the trigger as a carry; the bang where the tops part) |
| 9 | the clicks: click_whole, click_split, the rank-count draw, the take, the owed writes; books | 156, 1079; laws 5, 6, 8, 9 | the books closed; the exchange sign on the eight kinds; the draw's distribution test; the draw alike on alike images; each reading with its second reading | 2, 9, 10, 14; the click law's derivation or its exactness shown again |
| 10 | the runner: rounds, the ledger, the undo log, runner/rewind.py; the asynchronous option: masks, regions and halos, the bang's barrier as a "no tick" | 92, 98; plan 31 | synchronous and asynchronous runs with every dial equal: the same record and ledger, byte for byte; regions against single sites at equal counts; the ledger's byte-for-byte test | 4 (lin's formula, if chosen); 7's barrier |
| 11 | section 8's capability table on both engines' records; then the switch | plan 8, 12 | the table read on both; the end check | 12 (every bang shows more) for its row; the owner's word on the switch |

The click law's derivation (or its exactness shown again) is due before stage 9, not before stage 1: the clocks, the Mesh, the 24 and the turnover stand without it.

## 6. The laws against each other

Where the laws agree, where they meet and where they do not yet agree. A law is cited by its line in docs/ALGEBRA.md.

| # | the pair | status |
| --- | --- | --- |
| 1 | Postulate 5 (no if, line 35) and law 4's trigger at the top | agree: the trigger is the quotient of the time gear's carry (law 11); the trigger's one term (X_c, the bottom as a borrow) is the architect's OPEN 7 |
| 2 | Postulate 5 and the click of a split's draw | agree if the one whether is one carry's quotient: draft K's select is choose(nonneg(t - sigma_up), the down write, the up write), the algebra folder's own forms; SCRIBE-GATE-1.md calls it "the one comparison" and is corrected to say so |
| 3 | law 9's draw, digits composed "in the order of their values" (line 1079), and the closed list | agree, **resolved by the ruling (section 8 (i)):** the order by a rank count, sums of nonneg bits, no sort and no law changed; the composed number is the same whatever the order of the digits, so alike images draw alike (line 94; probe: 300 random draws); the draw's fairness stays item 6 |
| 4 | law 10 (time a circle for the gears) and laws 3 and 4 and line 1602 | agree since the owner's word of 14:37 (way 2), entered; draft K proves why a many-to-one click breaks the mirror only at itself (K1) |
| 5 | law 11 (every bound a carry) and F5's rate-dial clamp, F2's lower side | **meet:** the lower side's carry (the Node-clock's own tick) is not yet run; item (p), the owner's; the plan's law 6 now says the room has no cap, as the design's change 8 does |
| 6 | locality (line 92) and two-ended clicks (plan risk 3) | agree as two one-ended acts with the quotient added at the receiving end (section 4, item 2) |
| 7 | the 24 bit for bit (line 94) and the twin hands exact over Z[i] for half turns only | **depart:** the plan's section 24, item 6 asks the 24 of what the clicks show for the twin hands; the one architect's finding (ruling, section 8 (iv)): 2T has no subgroup of index 2, so in no basis of four or eight rows do the third turns act as signed permutations, and no ring alone keeps the 24 bit for bit under element-wise carries; the departure stands until David's route (OPEN 3: carries on what the 24 permute, the axis form (rho, S)); no twin train loads before it |
| 8 | Postulate 3 (one Mesh per tick) and rates (the local tick) | **meet:** "light crosses one Mesh per local tick" is the "past" read; item (u), the owner's |
| 9 | the fixed count of integers per Node-clock (line 98) and one hand per quantum (line 156) | **meet:** fixed rows by the kind's cap, one hand a family for the force carriers; item (a), the owner's |
| 10 | "only generic laws are approved" (line 106) and the click law (line 156) | agree **by name**: the click law is the only premise by name (lines 106 and 559 only mention it); it works exactly, checked on the eight kinds (draft E: +1 on A1, A2, E, T1, T2; -1 on E1/2, E5/2, G3/2; the books close); its derivation from a bigger law is open: the route is that the pair is one composite clock (what two Node-clocks do at one count, and a click is a clock's carry), David's draft J finds no derivation from the board's acts, and Animate's kind-keeping click (6472946096, a candidate, not checked on the board) is a second route; the pair's one directionless event stays the premise |
| 11 | asynchrony (line 98) and the great clock's top | agree by the owner's correction of 15:0x (item (v) withdrawn), as the ruling words it: the whole board is one big bang; the main run is synchronous, and every Node-clock turns over in the same round, each by its own turnover act on its own trigger's carry, with no read of the great clock; no region turns over while its neighbours run on; the detectors' clicks change the information from bang to bang; where the tops part, a whole-board turnover would read the great clock (line 92): OPEN 7, the owner's. Law 10's sentence of my entry of 14:54 (every Node-clock turning at its own top) is corrected to it (4de7a1b68) |
| 12 | no raise in the engine and a zero divisor | agree: the files' checker keeps every divisor at least 1; the loud failure is the language's |
| 13 | the record cannot rebuild the state, and the rewind (line 98: the check that reads the log) | agree since the 14:37 entry: the undo log is read by runner/rewind.py alone, the record by the decoder alone, no act reads a log; the plan's law 3 sentence "a click is undone only from its log" is lawful as the check's reading |
| 14 | the law's five functions (line 88) and the design's functions | agree by the map of section 3; the law names the new list after the build |
| 15 | draft K's finding (K2: on a finite board every reading taken per bang is eventually periodic) and law 10's "every bang adds more" | **meet:** the clicks' record grows at every bang that clicks (K4); that the gears themselves grow bang after bang needs an unbounded board with carries kept (law 11); item (d), the owner's reading of "more" |
| 16 | the closed list and the design's T^q (a power with a state exponent) and the plan's whether(q) | agree after the ruling: T^q = choose(q, T x, x), q the top's quotient, a bit; whether(q) = nonneg(q - 1); both on the list |

The **departures** the build carries by name: item 7 (the twin hands), the loader's exchange key (line 156: the sign declared per train until the table gives it), law 9's order (item 3), and the head's typed constants the calibre will hold as data.

## 7. The gate as a closed list

The owner's idea turns the gate round. It now names what is forbidden, one rule a dodge (the comparison rule names twenty-three functions and the clamp rule sixteen), and says in its own text that it counts masks (and, or, not, &, | and ~) nowhere. A closed list needs no dodge named: **in algebra/, engine/ and readings/, anything not on the list is refused by default.** Written by Sofer in scribe_scan.py as a rule beside the others (which keep printing their precise law); the vocabulary stands in one place at the head of the script, and the architect's additions go through Sofer by a ledger entry with the law line each serves.

The architect's change 1 is in the same pass: **a new folder, algebra/, beside record/, engine/, readings/, runner/ and decoder/, and tensor24/main.py** (spared no rule, so it holds no loop, branch or number), the carry's home moved to algebra/carry.py (the one place // and the remainder are written), the scatter-add np.add.at(out, index, values) named on the list as the contraction's scattered sum, and the walls as the design's section 4 has them: algebra/ the standard library alone; engine/ algebra, record and numpy; readings/ the standard library, record, readings and algebra; runner/ algebra, readings, record and numpy and never the engine or the decoder; decoder/ the standard library, record, readings and algebra and never the engine, the runner or numpy; main.py imports the engine and the runner and is the only place they meet. runner/ and decoder/ keep the readers' rules (they loop, compare and branch over a record).

It is built (scribe_scan.py): the self-test runs 695 cases, 0 parted; SCRIBE-GATE-1.md holds the vocabulary, the walls and the report.

## 8. What I ask

**The owner** (at 16:00 with the plan; my recommendation first in each):
1. Postulate 5 restated as the closed list (section 1): yes. Until your word it stands in the law's closing section, **Laws with a question mark**, as "The Node-clock's operations are addition, multiplication and Rule3's carry?" (? checked), and nothing stands on it.
2. The gate as a closed list in the engine's folders, and the architect's new folder: yes (built at scribe-5 ab7e4b308; the report stands in SCRIBE-GATE-1.md).
3. A Node-clock never writes into a neighbour; the word is a carry added at the receiving end; each Node-clock holds a beat count and its beat is due inside the engine, a stopped clock blocking no one (section 4): yes.
4. The click law stands as the premise by name for the plan on its exactness; its derivation (or the exactness shown again) is due before stage 9: yes.
5. Item (u), the neighbour read as "lin" (David and Sofer): your word; the ruling closes it before stage 3.
6. Law 10's sentence is corrected to your picture of 15:0x (one big bang, the main run synchronous, the asynchronous run an option; ALGEBRA.md line 106, no line moved), on the Boss's account of your word: please confirm it.

**The Boss:**
1. The one architect's ruling is taken (8eaf350f2) and the tie rule (6474542826) after it, and this file is corrected to both (draft 4); my three sentences are fixed, thank you.
2. The wording points of draft 3 are folded in the head (45bac0c81 and 67b765312). Two remain: the plan's lines about the going (162, and 542 to 543: "one go dial per Node-clock" and "one remainder of the Node-clock's ratchet") read each gear's ratchet, on the tie rule; and "Odd teeth stay struck" reads "a rule that needs a parity stays struck", against line 100 (the owner's word of 10:5x, "Obviously allow odd teeth").
3. Adopt the gate in the build's clone before the first line (SCRIBE-GATE-1.md, "Where it runs").
