# The architecture of the new engine, in one place

Sofer, 2026-10-28, 15:3x UTC, draft 1, for the owner (his words of 15:0x UTC: "you need to centralize the architecture ... it should be with me within half an hour"), the Boss, David and Animate. It stands on the law (docs/ALGEBRA.md at scribe-5, 1,913 lines), the plan (TENSOR24.md at 8f012b9b2, sections 19, 20, 21 and 31), the gate (SCRIBE-GATE-1.md) and the owner's words of 2026-10-28. It makes no law: where it proposes a sentence for the law it says so and asks, and nothing is entered before the owner's word. Every number it names is a count the law or the plan already holds.

**One page, for the owner.**
1. The Node-clock includes its six Meshes and every operation it does (line 90: its own gears and its six Meshes' gears; line 88: the Mesh's one act takes the two ends' integers and holds none of its own).
2. Its operations are three, on whole numbers: **addition, multiplication and Rule3's carry**. Nothing else is on the list, so nothing else needs forbidding (section 1).
3. The law already closes the Node-clock at two levels (line 88, five functions and nothing else; line 90, one act). The third level, the operations, is the one the owner just named; the gate can then be a closed list (section 7).
4. How a Node-clock speaks to another: **only through the Mesh between them, and what it says is a carry**; it never writes into a neighbour; the order of work is the runner's (section 4).
5. The click law (line 156) is the only premise by name in the law; it works exactly (checked on the eight kinds); its derivation from a bigger law is open (section 6, item 10).
6. The build goes clocks first, then tensors, then the 24's operations, asynchronous from the first stage (section 5).

## 1. The closed list: what a Node-clock may do

The Node-clock is its own gears and its six Meshes' gears. Its one act (line 90) is one division with a carried remainder over one integer contraction of them, the same for every train, every gear read before any is written. Everything that act is made of is one of three operations:

| operation | on what | what it leaves |
| --- | --- | --- |
| addition (its inverse is the sum with a product by -1) | whole numbers; a Gaussian integer as two whole coefficients | nothing |
| multiplication | the same; the complex product is (a c - b d, a d + b c), no angle | nothing |
| Rule3's carry: n = q d + r, 0 <= r < d, d a teeth count (at least 1) | whole numbers | the quotient q leaves as a carry or an event; the remainder r stays |

Two things are no operation on a number and stand beside the list. **Reading** a gear, its own or a Mesh's, is locality (line 92): the Node-clock reads itself and its six Meshes and nothing else, and writes its own gears only. **Holding** a gear is the Node-clock's own state, a fixed count of integers (line 98). The cube's 24 act on a tensor as signed permutations (products by 0, 1 and -1, and sums), so the 24's operations are on the list too.

**What the list makes of the names we forbid.** Each is a sum and a product of carries' quotients, so none needs a place of its own and none can stand as a name:

| a name | the carry it is |
| --- | --- |
| a whether, an if | the bit nonneg(n) = 1 + n div (n n + 1), 1 where n is at least 0 and 0 below; n < d is the quotient of n by d being 0 |
| a choice | b x + (1 - b) y, with b a bit |
| a minimum, a maximum | min(a, b) = a - nonneg(a - b) (a - b); max(a, b) = b + nonneg(a - b) (a - b) |
| equality | nonneg(a - b) nonneg(b - a) |
| a bound, a floor, a clamp | the remainder of the clock whose teeth count is the bound, its quotient the event (law 11: every bound is a clock's carry) |
| a count | a sum of bits |

So the closed list is complete for the logic the engine needs, and the gate need not name the dodges one by one. What it leaves out by construction: a power, a shift, a bit operation, a true division, a float, a root, a circular function, a comparison as an operation, a branch, a loop that makes a formula, a raise (a declaration), min, max, abs, clip and where, a sort.

**The one promise the list needs: a divisor is a teeth count, at least 1.** The clock that makes the divisor keeps it (the rate dial's carry), the files' checker (outside the engine) shows it at load, and the engine writes no raise; on Python integers a zero divisor fails loudly and is never silent. Where the divisor is a state gear (F2's tension t = (Gamma a) div X) the domain is the rate dial's own (David's Theorem B3, CHECKED: X at least Gamma is the stable side); item (p) is the owner's.

**Three closed levels, two already in the law.**
1. The functions (line 88): the Node-clock is five functions and nothing else, rotate(train), drive(trains), swap(train), click(trains) and link(i, j).
2. The act (line 90): one division with a carried remainder over one integer contraction.
3. The operations (proposed, the owner's idea of 15:0x): addition, multiplication and Rule3's carry. Postulate 5's body already says it second: "its step is Rule3's division with its carried remainder and the sums and products around it", after "the Node-clock holds no if". **The proposal leads with it and closes it** (line 35, no line moved, the heading kept, the first clause's new text alone): "the Node-clock's operations are addition, multiplication and Rule3's carry, on whole numbers (a Gaussian integer as two whole coefficients) and nothing else; a whether, a sign, a bound and a choice are sums and products of carries' quotients, so the Node-clock has no if". The rest of the postulate stands. It enters on his word.

## 2. The data: vectors and tensors

- **The state** (plan section 31): four arrays of shape (G, N) of Python integers, the notch now, the notch before, the fine tooth and the drive's fine tooth with the winds' fine teeth. G counts every integer component of every train (a hand two rows, twin hands four) and N the sites. Teeth counts are derived each tick, not stored. **One count per site is added** (section 4): the Node-clock's own tick count, a whole number, state in the Node-clock like the rest.
- **The layout** (read once at load, never state): the table of the six neighbours of every site, built from the piece's shape with the torus's wrap as Rule3 on the coordinates; the kinds' integer matrices and the product table, compiled from the 24's lifts; the universe file's integers (couplings, Gamma, the width) and the world and seed files. These are the only numbers anywhere.
- **The ring:** a hand is a Gaussian integer, two coefficients; the twin hands are two. The twin hands are exact over Z[i] for the half turns only, so the 24 bit for bit on them waits on David's ring (Z[zeta8] or the double cover; the carries break the double cover's exactness in 956 of 2,000 draws).
- **The 24 on the storage:** the fields are stored where the 24 act as signed permutations (T1, T2, A1, A2 and the three diagonal tensions); E has no such basis and serves the contractions and the tests, never the storage.
- **The width** is a key of the universe file, no limit of the engine: Python integers in object arrays (numpy has no 128-bit integer); the architect names how it is held.

**The tensor operations, the engine's whole vocabulary** (each is made of the three operations or is addressing):

| operation | form | made of |
| --- | --- | --- |
| gather (the stencil) | f[:, nb]: the six Spokes at once, one axis | addressing only; the one operation that crosses sites, and it crosses one Mesh |
| contraction | the product table compiled to index arrays: a gather, a product, a scattered sum (einsum) | multiplication, addition |
| pointwise sum and product | on arrays | addition, multiplication |
| carry | q = u // d, r = u - q d | Rule3; the floor division and the remainder written once, in engine/carry.py |
| choice | b x + (1 - b) y, b = nonneg(q) | multiplication, addition, one carry |
| signed permutation | an index gather and a product by 0, 1 or -1 | multiplication, addition |
| Gaussian product | (a c - b d, a d + b c) | multiplication, addition |
| scatter-add | the write at the receiving site; order-free because addition is associative | addition |
| layout | reshape, stack, transpose, an axis moved | addressing only |

## 3. The functions the engine implements

The law's five functions (line 88) are the entry points; the plan's eleven generic functions (section 20) are what they call. They map one to one, so there is one list:

| the law's function (line 88) | the plan's functions (section 20) | module | the operations |
| --- | --- | --- | --- |
| rotate(train) | step, contract, pull | node_clock | carry over one contraction |
| drive(trains) | the source J inside pull: one routine over the calibre's rows | node_clock | contraction |
| swap(train) | the turnover inside gate | click | one carry (the time gear's top), T as a phase reversal |
| click(trains) | the clicks inside gate: whole, split; draw | click, vernier | carry; the one whether is a quotient |
| link(i, j) | shift, transport: U_j from the two ends | mesh | gather, product, sum; the even parts alike, the odd parts opposite |
| (under all of them) | carry, mid, mirror, the Gaussian mul, conj, norm, turn; kinds, products; books | carry, ring, spokes, books | the three operations |

The law's list stays as built until the new engine stands (line 90: unbuilt, the five functions standing as the built form); then the law names the new list, on the owner's word.

## 4. How a Node-clock speaks to another, asynchronously

The law says each Node-clock steps on its own clock, only when the arrivals it needs from its six neighbours stand, and whenever every Node-clock has reached the same count the great clock is one bit for bit whatever the order was (line 98); a synchronous pass is the engine's order of work and no law. The architecture that realizes it, in clocks:

1. **The channel is the Mesh, and the word is a carry.** A Node-clock never writes into a neighbour. It computes its own carry; the quotient is offered on the Mesh as the Mesh's odd number (the count n_ij, line 88), read as +n at one end and -n at the other, and each end writes only its own gears by what it reads. The Mesh holds no state of its own: link(i, j) returns the numbers read the same from both ends (the even parts alike, the odd parts opposite). A word crosses one Mesh per tick (Postulate 3).
2. **The two slots are the channel's buffer.** The state holds the notch now and before (the second-order form), so a neighbour one tick ahead still shows the tick a Node-clock needs. No further history is held.
3. **The Node-clock's count c and the arrivals rule.** A Node-clock at count t steps to t + 1 when each of its six neighbours stands at a count at least t. Then neighbours differ by at most one tick, their slots always hold the tick needed, and a Node-clock can run ahead of one d Meshes away by up to d ticks (the cone). The bit due = the product of six bits nonneg(c_nb - c); it is a carry on counts, so it stands inside the engine with no if. The rewind has the mirror rule: a Node-clock steps back when no neighbour is ahead of it.
4. **The schedule is the runner's.** The runner passes a 0 or 1 per site, allowed; the engine multiplies: go = due x allowed x (the rate dial's bit), and new = go x stepped + (1 - go) x old. The runner's loop over sweeps and its choice of which due Node-clocks fire are the order of work: no law, and no engine code.
5. **What it guarantees.** The state at count t is a function of the start state within t Meshes, so every schedule that fires only due Node-clocks gives the same state at equal counts (the determinacy of a network of channels, Kahn's), and the rewind is the same function at -1. Two tests can fail: the **order test** (many random allowed masks, the same bits at equal counts; a mutant that reads a neighbour's now where the count calls for before fails it) and the rewind under a random schedule.
6. **Where two clocks of different counts meet: the Mesh's reading rule.** With rates (local ticks, the rate dial: a whole turn is no tick) two neighbours' counts part. The Mesh then reads the neighbour's slot chosen by the count difference, a choice by a bit, in one place (link). Whether the neighbour is read as it stands (the cone keeps, the rewind breaks) or interpolated (David's and my recommendation) is item (u), **the owner's**; the architecture holds the one place for it and nothing else changes.
7. **A click that joins two ends of a Mesh** (plan risk 3, locality against two-ended clicks) is two one-ended acts with the quotient carried by the Mesh's odd number (item 1), not an act that writes two Node-clocks; a rendezvous of two Node-clocks at one count is the other reading, and it is the click law's composite clock (item 10 of section 6). The one-ended form is what lines 86 and 88 say.
8. **From the first stage.** The count and the go bit are in the first function written, so every later stage is tested under a random schedule. Changing a synchronous engine to an asynchronous one late changes every signature.

## 5. The build, stage by stage

The Boss writes every line (section 21 of the plan); each stage is approved by all four (Sofer on the laws and the gate, David on the formula, Animate on the bench, a fresh adversarial read), within 15 minutes of the post. The order is the owner's method: clocks first, then tensors, then the 24's operations. Every test below is shown failing on a broken copy.

| stage | what is built | the law it stands on | done when (a test that can fail) |
| --- | --- | --- | --- |
| 0 | the frame, before the first line: the gate in the build's clone, the three files and their checker, the record's schema, the test harness running on a trivial engine | line 86, the plan's sections 21 and 31 | the gate clean; the five tests run and fail on a mutant |
| 1 | the carry, Rule3 on arrays, forward and at -1: carry, mid, mirror, nonneg | lines 90, 98; law 11 | n = q d + r exact; r in [0, d); the tie rule odd, decided before the first line (plan risk 2) |
| 2 | one clock: a gear with its fine wheel, its count c and the go bit, the rate dial | lines 90, 98 | rewind 20 of 20 and bijective both ways on one Node-clock |
| 3 | two clocks over one Mesh: link, the two slots, the arrivals rule | lines 88, 92, 98; Postulates 1 and 3 | the order test passes; the rewind under a random schedule |
| 4 | the board: the stencil gather over the six Spokes from the piece's shape; the scalar light with its spring | lines 92, 98 | the one-Mesh reach test forward and backward; the formula against the naive loop model on side 3 or more; equal to the head on the light alone |
| 5 | the ring: the Gaussian integers, the hand | the plan's section 3 | the ring's laws exact; T T = +1 on a hand, -1 on the twin hands |
| 6 | the 24 and the kinds: the table of the kinds, the product table compiled, contract | lines 90, 94 | all 24 turns bit for bit on every chart, with a board that is no cube as the negative control |
| 7 | the Node-clock's one act on every train alike: the regulator, the offset, the hands | line 90, 96; plan section 19 | the formula test; the rename test; the head compared act by act, unexplained differences 0 |
| 8 | the turnover: T as the kind's phase reversal, its trigger a carry | lines 106, 1602; laws 4 and 10 | T S T = S^-1 at every teeth count (the plan owes it, David's); the rewind through the top 20 of 20 |
| 9 | the clicks and the draw: whole, split, the vernier; the click law | lines 156, 1079 | the books closed; the exchange sign on the eight kinds; each reading with its second reading |
| 10 | the record, the decoder, the ledger (Animate, in parallel from stage 0) | plan section 31 | the record byte for byte the same with the ledger and without it |
| 11 | section 8's table of capabilities on both engines' records; then the switch | plan sections 8 and 12 | the table read on both; the end check |

The click law's derivation (or its exactness shown) is due before stage 9, not before stage 1: the clocks, the Mesh, the 24 and the turnover stand without it.

## 6. The laws against each other

Where the laws agree, where they meet and where they do not yet agree. A law is cited by its line in docs/ALGEBRA.md.

| # | the pair | status |
| --- | --- | --- |
| 1 | Postulate 5 (no if, line 35) and law 4's trigger at the top | agree: the trigger is the quotient of the time gear's carry (law 11) |
| 2 | Postulate 5 and the click of a split's draw | agree if the one whether is written as one carry's quotient; SCRIBE-GATE-1.md calls it "the one comparison" and is corrected to say so |
| 3 | law 9's draw, digits composed "in the order of their values" (line 1079), and the closed list | **meet:** a sort is a comparison network, refused; the draw needs an order-free composition (symmetric sums commute) so alike images draw alike; the architect's, or it moves to the readings |
| 4 | law 10 (time a circle for the gears) and laws 3 and 4 and line 1602 | agree since the owner's word of 14:37 (way 2: the reversed run leaves the clicks undone), entered |
| 5 | law 11 (every bound a carry) and F5's rate-dial clamp, F2's lower side | **meet:** the lower side's carry (the Node-clock's own tick) is not yet run; item (p), the owner's |
| 6 | locality (line 92) and two-ended clicks (plan risk 3) | agree as two one-ended acts with the Mesh's odd number (section 4, item 7); the plan states it as a risk |
| 7 | the 24 bit for bit (line 94) and the twin hands exact over Z[i] for half turns only | **depart:** the plan's section 24, item 6 asks the 24 of what the clicks show for the twin hands; named a departure in the plan's laws 5 and 6; David's ring closes it |
| 8 | Postulate 3 (one Mesh per tick) and rates (the local tick) | **meet:** "light crosses one Mesh per local tick" is the "past" read; item (u), the owner's |
| 9 | the engine's fixed count of integers per Node-clock (line 98) and one hand per quantum (line 156) | **meet:** the slots by the kind's cap, one hand a family for the force carriers; item (a), the owner's |
| 10 | "only generic laws are approved" (line 106) and the click law (line 156) | agree **by name**: the click law is the only premise by name (lines 106 and 559 only mention it); it works exactly, checked on the eight kinds (draft E: +1 on A1, A2, E, T1, T2; -1 on E1/2, E5/2, G3/2, the books close); its derivation from a bigger law is open: the route is that the pair is one composite clock (what two Node-clocks do at one count, and a click is a clock's carry), and David's draft J finds no derivation from the board's acts, so the pair's one directionless event stays the premise |
| 11 | asynchrony (line 98) and the great clock's simultaneous top | agree with the owner's word of 14:54: every Node-clock turns over at its own top; more complex clocks come by the detector's click |
| 12 | no raise in the engine and a zero divisor | agree: the files' checker keeps every divisor at least 1; the loud failure is the language's |
| 13 | the record cannot rebuild the state and the rewind (line 98: the check that reads the log) | agree: only the check, a reader, reads the log; no act does (the log-read rule); the plan's risk 1 asks for an inverse from the state alone, which is the stronger form |
| 14 | the law's five functions (line 88) and the plan's eleven | agree by the map of section 3; the law names the new list after the build |

The three **departures** the build carries by name: item 7 (the twin hands), the loader's exchange key (line 156: the sign declared per train until the table gives it) and the head's typed constants the calibre will hold as data.

## 7. The gate as a closed list

The owner's idea turns the gate round. It now names what is forbidden, one rule a dodge (the comparison rule names twenty-three functions and the clamp rule sixteen), and says in its own text that it counts masks (and, or, not, &, | and ~) nowhere. A closed list needs no dodge named: **in the folders engine/ and readings/ of the new engine, anything not on the list is refused by default.** Written by Sofer in scribe_scan.py as a rule beside the others (the others keep printing their precise law); the vocabulary is in one place at the head of the script, and the architect's additions go through Sofer by a ledger entry with the law line each serves.

At the time of writing it is being built: the vocabulary (statements, expressions, calls) will be the gate's own file and the report of what was built will stand in SCRIBE-GATE-1.md, with the self-test's count. runner/ and decoder/ keep the readers' rules (they loop, compare and branch over a record); record/ keeps the standard library alone.

## 8. What I ask

**The owner** (at 16:00 with the plan; my recommendation first in each):
1. Postulate 5 restated as the closed list (section 1): yes.
2. The gate as a closed list in the engine's folders: yes (being built; the report will stand in SCRIBE-GATE-1.md).
3. A Node-clock never writes into a neighbour; the Mesh is where two clocks of different counts meet; the word is a carry; the board asynchronous from the first stage (section 4): yes.
4. The click law stands as the premise by name for the plan on its exactness; its derivation (or the exactness shown again) is due before stage 9: yes.
5. Item (u), light across a Mesh per local tick, read as "lin" (David and Sofer): your word.

**The Boss:**
1. Take one architect, a reading agent with no stake, for the architecture only: confirm sections 2, 3 and 4 in code, name how the width is held, close the five meeting points of the earlier sync (law 9's sorted draw; the draw's one whether and the take's loop; one hand per quantum against fixed arrays; the twin hands' ring; the width).
2. State in the plan what is built at each stage, as section 5, with each stage's test and its approvals.
3. Keep one architecture: this file is the law-side frame and the one place the owner reads; section 31 of the plan keeps the architect's design and the detail (the record, the ledger, the prior art, the line budget), and each points to the other. Where the architect's design differs from this file, I correct this file within the hour of the Boss's post.
4. Adopt the gate in the build's clone before the first line (SCRIBE-GATE-1.md, "Where it runs").
