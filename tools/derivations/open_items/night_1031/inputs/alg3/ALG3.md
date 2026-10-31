# ALG3: what is still open, read through the coupling complex (node-all 9d75a4904)

ALG3, for the Boss, 2026-10-31, 09:4x to 10:1x UTC. It is an input for Big Pic's bench, at the owner's word, and goes to
ALG2's hostile pair. Big Pic solves the open items; ALG3 hands him the complex's view of each, with the facts and the
probes, and restates no lead. S is S.

**What this text replaces.** It replaces only the ALG2 lines it names (section 1); every other line of ALG2, and through
it of ALG1, stands.
- ALG2 is S/alg2_frozen/ALG2.md: 585 lines, sha256 4d60d6d7efe1e6ca84c415799c2afd0b74f4cbaf4700b8b62b8ca7b7fe0a472c.
- Its readers: S/alg2_math/REPORT.md (PASSED, 9 MINOR) and S/alg2_phys/REPORT.md (NOT PASSED on one renaming, 8
  MINOR).

**The owner's word that sets it** (the Boss's rulings, 09:5x UTC, second part): "The shortcut ALG2 explained something
important about the general mechanism of the clock system and the big algebra. Derive from it the solution to what is
still open."

**The tree.** node-all 9d75a4904 is extracted as a real folder, S/alg3/all. Its archive (git archive 9d75a4904 src
examples) has sha256 91a5ebd617da793c2d670add02f017c363056adf725638260dc351ba2c781bc8, the 09:1x rule: "A frozen text
carries its tree or the tree's digest (the commit and the archive's sha256), never a live symlink."

**Conduct.**
- Nothing in the repository or in any worktree was touched, and nothing was posted. I wrote only in S/alg3/.
- Probes are in S/alg3/probes and their outputs in S/alg3/out:
  - cochain3.py: ALG2's cochain2.py with the modes circ and david added;
  - member1.py, order3.py: new;
  - hodge2.py, unitlay.py: ALG2's.
- Whole numbers only, with Rule3's carry the one division; paths by joinpath.
- The live venv's Python 3.14.6 with -I (the 08:5x rule), the extracted tree's src first on sys.path, one process at a
  time under nice 19.
- The load was read before each run: 2.0 to 3.5 on 4 cores.
- One run of order3.py first ran away (its lays outside the step's window; numbers growing without bound). I stopped
  it, and its lays were brought inside the window (named in 8.4).

Every claim is DERIVED, MEASURED, OPEN or OVERTURNED.

## 0. The open items, one line each

| item | standing |
|---|---|
| 1. The miracle | OPEN, Big Pic's. DERIVED: what any closure must do (3.3). Lead (a) as passed: OVERTURNED, by David's two facts, MEASURED (3.1, 3.2) |
| 2. The uncertainty principle from the clicks | OPEN, Big Pic's. DERIVED: the exact sequence gives complementarity, not a trade-off. MEASURED: the one integer link, the lines fixing a triangle's circulation mod 3 (section 4) |
| 3. The third click's member | DERIVED and MEASURED: four numbers per triangle, one beyond the first click's three; the twin is the only new number, on D. DERIVED: the twin cannot come from an existing tooth. OPEN: whether a clean form drops it too (section 5) |
| 4. (C)'s seeds' law, the end form | OPEN, Big Pic's. DERIVED: what the complex allows: a relation on the end seeds, no cell, no signal. MEASURED: the mesh ring's loop pairings read 0 (section 6) |
| 5. The key, the stop, the click world's place, the strengths | OPEN. DERIVED: the complex fixes none of their values; what it does fix is named (section 7) |
| lead (a) | OVERTURNED (3.2) |
| lead (b) | DERIVED; MEASURED on the click world's swap lay and a toy (5.4, 3.3) |
| lead (c) | DERIVED: no trade-off from the sequence alone (section 4) |
| lead (d) | DERIVED: the room the complex leaves (section 6) |
| lead (e) | DERIVED: the key is not fixed; the energy's bound is not the 2-cochain's size (section 7) |

## 1. The renamings and the readers' items (replaces the ALG2 lines named)

### 1.1 The physicist's B1

The 10:1x ruling, verbatim: "'Place' in a text means a Node-clock, a board site, until the owner rules on the click
world's place (08:5x). ALG2's X_-1 is renamed 'the part': a connected part of the laid structure, a board fact."
- **"The part".** In ALG2 lines 65, 347-361, 520, 525 and 546, read "the part" for "the place", and in line 65 read
  "augmented by the part". X_-1 is the part, a board fact. Its theorem (no 1-chain or 2-chain books eps(omega)) is per
  part.
- **"A Node-clock".** In ALG2 lines 71, 86, 93, 140, 176, 187, 236-251, 265, 277, 298-307, 316, 320, 326, 331, 340, 445,
  447, 516, 519, 522, 531, 547 and 553, read "a Node-clock" for "a place" or "the place". Line 86 reads "triangles of
  three clocks at one Node-clock". Line 516's "0 at every place" reads "0 on every Node-clock's own part".
- **What a place of the click world is** stays the owner's question (08:5x, verbatim: "What a place of the click world is
  goes to the owner's batch with DECODE3f's Mesh meeting, the islands its stake.").

### 1.2 The mathematician's MINORs

1. The odd dial (ALG2 6.5): read "not needed by the edges' act; needed by the triangle's pair (its flip about the
   birth)", as the 09:4x ruling has it, verbatim: "The odd dial is needed by the triangle's pair (its flip about the
   birth), not by the edges' act (ALG2's mathematician, MINOR 1, MEASURED and DERIVED)."
2. The law's sources (ALG2 2.1): rules 1 ("at one Node-clock") and 3 cite the 10:1x ruling, verbatim: "The cross-Mesh
   triangles (ALG2 2.6) stay H_1 cycles, carried as first clicks: the owner's 'equilateral triangle' case is read as one
   triangle per Node-clock, each edge on one triangle; if his meaning differs, the item returns."
3. The owner's "each edge on one triangle" beside 2.6: filling every 3-clique would put each giver-taker edge on 7
   triangles. 2.6 is answered by the 10:1x ruling above: the cross-Mesh triangles stay H_1 cycles.
4. ALG2 2.3: read "no shipped world moves a whole-cycle quantum" for "no shipped world moves a quantum on an H_1 cycle".
5. ALG2 2.2: read "its landing is added to its three edges' sides, +w, +w, -w, in the sums q_e = Q_e + c_e w" for "a
   triangle's wraps are written as +w, +w, -w".
6. ALG2 3.1 and 4: read "the part's books, by construction" for "the part's conservation" (07:5x: "no reading of
   conservation"; 09:0x: "no conservation of energy is shown in the clicks").
7. ALG2 3.5: the 09:3x ruling, verbatim: "'Removed' needs both conditions: the step on the quartic exact, and term 11's
   passing reading that step's own exchange." The 09:0x ruling, verbatim: "it removes the residual's drift, not the
   residual."
8. ALG2 3.6's grain argument holds on L0 only. On L1 the finding (the two parts large and opposite) is MEASURED, not
   explained by the grain; the reason given is withdrawn there (as the physicist's M4).
9. The interpreter: ALG2 ran Python 3.13.17. Both readers reran under 3.14.6 byte-identical. ALG3 runs 3.14.6.

### 1.3 The physicist's MINORs

- M1: answered by the 10:1x ruling quoted in 1.2, item 2. C^T C has 3 only on its diagonal once the cross-Mesh triangles
  are filled, so such a part is outside C^T C = 3 I. 2.6 is withdrawn as a question.
- M2: as 1.2, item 4: "the click world moves none".
- M3: under rule 5 each side holds the edge's own carry plus C W, so the click world sees the two kinds of quanta only as
  a sum. They are told apart only by a reading the first click's record fails. Rule 5 withdraws NATURE1's writer item 6
  (10:1x, verbatim: "Rule 5 (the record has two levels, lines and sides) withdraws NATURE1's writer item 6 (W in the
  record apart from the sides).").
- M4: as 1.2, item 8. The teeth's term grows with the motion |a+ - b|, not with W alone.
- M5: ALG2 line 296's r is the gear's own tooth (st[2]), a board field: "the teeth's term" is the gears' rounding.
- M6: the rulings of 08:5x to 10:1x are cited verbatim in this text. The archive's sha256 is named above.
- M7: as 1.2, item 9.
- M8: rules 2 and 3 follow from rule 1. Rule 4 is not needed for "no fourth": a coupling of three trains or more would
  add only edges and triangles, or a four-clock part, which is NOT READ by name. Rule 4 matters for the dial.

The 10:1x ruling for the build, verbatim: "When the cochain act is built, the build carries the law of the build as its
own static test: no tooth outside edges and single-Node-clock triangles, and the record's two levels."

## 2. The owner's answers and rulings applied (verbatim, by section)

**The owner's answers, about 09:4x UTC** (the Boss's translation):
- 1: "'Approved': a clock reads only its own clicks (Q10). Its sides and the board are not 'what a clock can read'."
- 2: "The teeth go out of the record entirely (Q11): the record writes lines and sides, q alone; no tooth, birth or end
  tooth is written. The engine keeps its teeth; the code checks that read them read the board's own state."
- 3: "'Yes, as you recommend': Big Pic's strengths law. Every strength comes from the structure, or is laid once at the
  start for each clock; never searched, and never one choice for the whole universe."
- 4: "The three silent worlds (the bang, the live world, the well) 'out'." ALG3 runs none of them.
- 5: "On the triangle's tooth and twin (two new numbers per triangle): 'There is surely a mathematical miracle here that
  solves this cleanly.' Not approved as two new numbers; Big Pic seeks the clean form."
- 7: "'Check what an equilateral triangle gives, because that seems to me the way.' Big Pic's, first on the third click."
- 8: "D1, one number per edge: 'if it helps, and it is generic and not a fake.' Built if so."

**The click world's order** (09:3x, second part): "The click world's order is 'strictly later' (rule (t), the 07:5x
words): two meetings of one clock in one round are simultaneous in its own lines and unordered."

**The test's lay** used in 3.2 and 5.4 (MATH4's line, 09:4x on (C)'s two forms): "A test's lay that differs at a whole row
is lawful as the check of a DERIVED fact, named a test's lay (09:5x, any board shape)."
- It is S/alg3/worlds/click_swap: the click world's files with the giver's laid row laid on the taker too, at every
  Node-clock.
- It is a test's lay, never shipped. Its digests: universe 2a2aa411..., piece 85c72a56..., setting 39696ca5....
- MEASURED: the cochain act on it is byte for byte the engine's over 200 rounds (0 entries off; 12,852 click entries;
  9,639 lines), and its run back is exact.

## 3. Item 1: the miracle

### 3.1 David's two facts (#2187 6541854539, item 4), read on my own probes (MEASURED; cochain3.py, mode david)

**Fact 1: no monomial joins three clocks.** On the shipped click world, by value positions and the clocks joined:
- 24 tie monomials of four positions: 12 on (held, giver) = (2, 3) and 12 on (held, taker) = (2, 4);
- 6 two-leg monomials on (giver, taker) = (3, 4);
- 2 springs on the held clock alone;
- 0 joining three clocks or more.

At round 1, at Node-clock 0, the tie terms' residual D (VARY4's D_i), each at the clock of the leg it pushes, is:
- the giver -192,000,000;
- the held 0;
- the taker 0;
- by the tie's edge, (held, giver) -192,000,000 and (held, taker) 0;
- the same at every Node-clock.

These are David's numbers to the unit. **Fact 1 holds.**

**Fact 2: the residual is a miss in the sum over the clocks.**
- The Node-clock's SUM D over all monomials equals its SUM D over the tie monomials at 5,400 of 5,400 site-rounds (L0,
  200 rounds; 0 off). Every two-leg and one-clock monomial has D = 0 (ALG2 3.2).
- VARY4 identified that sum with the head's books' miss to the unit (ALG2 3.2, cited).
- eps B = 0 holds on the record at every site-round: the own sides cancel, 0 off (ALG2 7.1; again here on the swap lay).
- eps B C = 0, since B C = 0 (L0, DERIVED).
- **Fact 2 holds.**

### 3.2 Lead (a) as passed fails, and why (DERIVED; MEASURED)

**Why.** The residual is a miss in eps, the sum over the clocks. A tooth booked through an edge changes that sum by eps B
= 0, and one booked through a triangle by eps B C = 0. Indeed B C = 0 already changes no clock's line at all. So no tooth
on the triangle can book the residual. And each tie monomial joins two clocks on one edge (fact 1). The residual belongs
to the ties' edges, not to the triangle.

**MEASURED: the residual is no function of the triangle's circulation** (cochain3.py, mode circ, 200 rounds).
- On the swap lay (2), the triangle's circulating passing y = P(2,3) + P(3,4) - P(2,4) is 0 at 5,400 of 5,400
  site-rounds. P(2,3) = P(2,4) and P(3,4) = 0 at every one.
- On the same lay the tie's residual reaches |SUM D| = 529,920,000 at a Node-clock. At site 0, round 200, it is
  -187,440,000 on each tie edge.
- On L0, by contrast, y is not 0 at 4,698 of 5,400 site-rounds (|y| up to 4,827,840,000), with the residual up to
  708,840,000.

**What of the equilateral triangle's S_3 still stands for Big Pic** (DERIVED; MEASURED where marked).
- S_3 acts on the 2-cell by the sign character: a transposition reverses the triangle's orientation, so every
  2-cochain, a tooth there included, is odd under it.
- The residual is even: it is a sum at the Node-clock, and the swap maps the (held, giver) ties onto the (held, taker)
  ties. MEASURED: on the swap lay the two ties' residuals are equal, -187,440,000 each.
- So no map that commutes with S_3 can carry the residual onto a 2-cell (Schur's lemma, trivial to sign).
- What stands for Big Pic is the triangle's own symmetry, to be read for the step and the member: 3.3 and 5.4.

### 3.3 What the complex fixes for any closure (DERIVED; MEASURED on a toy)

**Where the residual lives.**
- An edge's work over the window splits into two parts:
  - an odd part under the edge's orientation, the passing: a 1-cochain, booked by the edge's tooth;
  - an even part, unchanged when the edge is read from its other end.
- The even part is no cochain of the oriented complex. It is the coupling's own: its stored form plus its residual.
- For degree 2 the even part is an exact difference of the stored form E, read off the counts. For the tie it is not:
  the free-window degree theorem (ALG2 5).
- The law of the build's rule 2 keeps any tooth off a cell joined to the coupling.
- So, in the complex, the residual can only be removed by the step, never booked. 09:3x, verbatim: "'Removed' needs both
  conditions: the step on the quartic exact, and term 11's passing reading that step's own exchange."

**What the step's order does** (DERIVED).
- Kicks commute: each clock's kick reads only counts and writes only its own momentum. Drifts commute too.
- So the step that reads every push at the round's counts, then moves every gear (today's order), commutes with every
  relabelling the plan admits, S_3 on an equilateral triangle among them.
- A step that moves one family after another, each reading the others' new counts, orders the clocks. It commutes with
  no relabelling that changes that order, unless its sub-steps commute.
- In exchange, each sub-step sees the others' counts as fixed coefficients. Every coupling of degree 4 that joins two
  families (the tie, k^2 x x) is then of degree 2 in the moving family, and its work an exact difference within the
  sub-step. That is road B's mechanism (MIRACLE_B2).
- On the click world the plan's structure supplies the order (08:5x). On an equilateral triangle it would not. The
  10:1x ruling, verbatim: "if the three edges were equal in strength and kind, no family would be picked by structure
  and any order would break S_3".

**MEASURED** (order3.py; a toy of whole numbers, never src).
- The toy is three alike clocks, one gear each (W = 200), pairwise joined by three equal quartic couplings f x_i^2 x_j^2
  and held by equal springs g x_i^2, on 14 lays, 40 rounds, using the engine's step.gear. Its counts stay within 8 on
  every lay.

| step | commutes with the six relabellings | books |
|---|---|---|
| all at once (today's order) | on 14 of 14 lays, each of the six | the Node-clock's running SUM D is not 0 at 457 of 560 lay-rounds, largest 4,968 |
| one clock after another | the identity on 14; each other relabelling on 1 or 2 lays only (lays it fixes, with the potential's sign flips) | each sub-step exact: 0 of 1,680 sub-steps off their own staggered energy |

- So exactness by order costs S_3, and S_3 by today's order keeps the quartic residual.
- An exact step on an equilateral triangle must be simultaneous. Whether a simultaneous exact step exists in whole
  numbers for degree 4, runs back by the same act on the mirrored state, keeps the 24 and holds the held walk is OPEN,
  Big Pic's.
- Its 24: a simultaneous step built from invariant tensors keeps it (ALG1 2.2's argument, DERIVED).

### 3.4 What stays OPEN on item 1

- The exact step itself.
- Its walk's bound: STOP1's, a board fact (section 7).
- Its books on node-all's sides: OWED until term 11's passing reads the step's own exchange (09:3x).

## 4. Item 2: the uncertainty principle from the clicks (lead (c))

**The carriers.**
- A clock's line is a 0-chain, (B q) at its vertex.
- The sides are a 1-chain q.
- A triangle's circulation c . q is the 2-cell's evaluation of q.
- The H_1 cycles are the 1-cycles no laid triangle bounds.

**DERIVED.**
- **The lines leave the cycles free.** Given every clock's line, q is fixed up to ker B = im C plus the H_1 cycles: the
  circulations and the harmonic parts are free given the lines. The lines' part (im B^T) and the circulations' (im C)
  are complementary.
- **Both are sharp at once** when the sides are written. So the exact sequence gives complementarity, not a trade-off.
  10:1x, verbatim: "As built, every click observable is sharp (Q_W, a clock's own count, the sides, the meetings and
  their order); the only band is the board's hidden passing, which no click reading reads."
- **One integer link.** On a triangle i < j < k, c . q = 3 q_ij + L_j - L_i, where L is a line. So the lines fix the
  circulation mod 3, which is C^T C. A single clock's line fixes nothing of it.
- **Under the owner's answers 1 and 2** (a clock reads only its own clicks; the teeth out of the record), a clock reads
  one number a round, its own line. Its line is blind to every circulation and fixes nothing of another clock's.

**MEASURED** (cochain3.py, mode circ, 200 rounds):
- c . q = 3 q_ij + (L_j - L_i) and c . q = L_j - L_i mod 3 hold at 5,400 of 5,400 site-rounds on L0, L1 and the swap
  lay (checks by construction).
- What the lines leave open is c . q itself: not 0 at 4,158 site-rounds on L0 and 3,164 on L1 (|c . q| up to 32 and 91
  quanta), and 0 on the swap lay.

**OPEN, Big Pic's.** A trade-off between two click observables. The 08:5x ruling keeps the name for "a relation between
two click observables (place and motion, by the echo and Bondi's k): OWED, waiting on LIGHT3's lines and echo". The
complex's linear algebra gives none by itself, and on the integers only the mod-3 link above. Any band must come from the
counts and the dynamics, not from the sequence.

## 5. Item 3: the third click's member (the owner's answers 5 and 7)

### 5.1 The edges' teeth on a triangle are a cocycle (DERIVED)

- Under the member, each edge of a triangle carries its share p_e = 3 x_e - c_e y at the dial 3D, and
  c^T p = 3 y - 3 y = 0.
- So the edges' teeth keep c . g = c . g at the birth (mod 3D) forever: in the centred teeth, c . g = 0 mod 3D.
- On the triangle that means g = delta phi mod 3D for a 0-cochain phi of the three clocks, unique up to a constant. phi
  turns by each clock's own net passing (B x), whose sum is 0.
- So the three edge teeth hold two numbers, and the third is read back from the other two: g_ik = g_ij + g_jk mod 3D,
  in centred teeth.
- THIRD9 saw this only mod 3 (its residues, 8.10). It holds mod 3D, a whole number's worth: a double by MIN1's rule, of
  the kind of D1.

### 5.2 So of the two new numbers, tau is not new (DERIVED)

- The first click holds three edge teeth on D.
- The member holds two edge teeth and tau on 3D: the Hodge split of the same three, gradient and circulation, 2 + 1.
- The twin is the only number beyond them: four numbers per triangle against the first click's three.
- With the twin on D (THIRD9 1), the member's states per triangle are (3D)^3 x D.

### 5.3 MEASURED on node-all's own passings (member1.py; Big Pic's Stepper, circ.py ed6a1f225, run read only)

At every Node-clock, Big Pic's mode 11 Stepper is fed node-all's own edge passings P(t, u), and so is the four-number
member (two edge teeth and tau on 3D, the twin on D, the third edge's tooth read back):

| lay (200 rounds, 27 Node-clocks) | c . g not 0 mod 3D | quanta apart, edge-site-rounds | landings apart | landings; side quanta not 0 | run back from the end alone |
|---|---|---|---|---|---|
| L0, the shipped click lay | 0 of 5,400 | 0 | 0 | 3,915; 7,938 (THIRD7's numbers) | 27 of 27 |
| L1, VARY3's lay | 0 of 5,400 | 0 | 0 | 2,695; 5,487 | 27 of 27 |

The run back keeps the edge teeth and tau, flips the twin on D, and negates the passings in reverse order.

### 5.4 The equilateral triangle (the owner's answer 7; lead (b))

**What C's symmetry forces on the member** (DERIVED).
- **The cochain spaces split.** S_3 acts on the triangle's cochains by characters:
  - C^0 = trivial + standard;
  - C^1 = sign + standard (character (3, -1, 0) on the classes of the identity, a transposition and a 3-cycle);
  - C^2 = sign.
  So the triangle's existing cochains hold exactly one sign-character number: the circulation, tau's.
- **Hence the twin is new.** A turn that mixes reversibly needs a second number of the same character beside tau. The
  edges' gradient part is the standard representation, and phi's invariant part is trivial, so a shear from either into
  tau is no S_3 map (Schur's lemma). So no existing tooth can be the twin: the one new number is forced, for a linear
  turn run back by the same act on the mirrored state with tau kept (THIRD7 5).
- **The odd dial.** A transposition negates tau and the twin, so the pair's dial must be odd for that to be a flip about
  the birth (1.2, item 1).
- **No circulation on a symmetric lay.** A lay that a relabelling reversing the triangle fixes stays fixed (the act is
  equivariant), and y, odd under that relabelling, is 0 at every round. So on an equilateral triangle the third click
  lives only on lays that break every such relabelling.

**MEASURED.**
- **The click world's swap lay:** y = 0 at 5,400 of 5,400 site-rounds (3.2).
- **The toy (order3.py)**, where the potential is even in each count:
  - y = 0 at every round on the 10 lays that a relabelling, with the potential's sign flips, fixes;
  - y is not 0 at 35 to 40 of 40 rounds on the 4 lays that none fixes.
- **The member's S_3 itself:** THIRD7 measured its six relabellings at 0 apart in the toy (cited).

### 5.5 What stays OPEN on item 3

- Whether a clean form drops the twin too. That needs a turn that is not linear or not run back by the same act; each
  would break a law here. Big Pic's: the owner's "mathematical miracle".
- For the owner's batch: one new number per triangle (the twin, on D), and the third edge's tooth read back from the
  other two. The owner's answer 8 ("if it helps, and it is generic and not a fake") bears on the read-back; it is generic
  (every triangle under the member) and exact (c^T p = 0).

## 6. Item 4: (C)'s seeds' law, the end form (lead (d))

The owner's word, verbatim (about 09:4x, the Boss's translation): "Of Big Pic's two forms for (C)'s seeds' law, the end
form (a tie of the two wings' ends, with no signal) comes first on Big Pic's bench".

**What the complex allows** (DERIVED).
- **The end form is the start form, pulled back.** The act is a bijection, so a relation imposed on the end seeds is the
  relation T^-N pulls back onto the start seeds. The two forms are one law read at two boundaries. Which is the natural
  one is OPEN (08:4x, verbatim: "its natural place (the start, the end or the pair events) is OPEN").
- **No cell carries it.** Two wings at two Node-clocks are joined by no cell, unless a chain of Mesh edges joins them.
  Rules 2 and 3 put no tooth on a cell joined to a non-clock or on an H_1 cycle. So the tie is a law of the joint measure
  of the end teeth, never a cell or a tooth. 08:4x, verbatim: "That correlation sits in a law of the seeds' joint
  measure".
- **No signal, by construction.** Each wing's act reads its own cells and its six Meshes. The far wing's setting enters
  no act, so each wing's counts are its own whatever the tie, and no signal passes.
- **In H_1.** Where a cycle z runs through both wings, the pairing z . q, the sides' quanta summed round the loop, is a
  quantity with no labels that involves both wings. It is a candidate for what an end tie relates. Its telescoping
  identity, D SUM z . q = z . SUM P + z . (k_0 - k_N), reads the end teeth round the loop, which the owner's answer 2
  keeps out of the record.

**MEASURED** (cochain3.py, mode circ, the mesh ring, 125 rounds).
- The loop pairings round the ring's two strands are 0 at every round. It is not an identity: the strand's sum is
  f SUM_y [M(y+1)(dL(y) + dL(y+2)) - dM(y+1)(L(y) + L(y+2))], which a general state does not zero. So it is this lay's
  (DERIVED).
- So on the shipped mesh ring H_1 carries nothing. There q = P / 3 exactly (10:1x), so the loop pairing is a board
  quantity with no room for a law.
- The shipped click world cannot host the test (09:4x, verbatim: "The shipped click world cannot host it (no meeting
  joins two Node-clocks there)").

**OPEN, Big Pic's:** the law itself, covariant under the swap, S_3 and the 24 (08:4x).

## 7. Item 5: the key, the stop, the click world's place, the strengths (lead (e))

**The key.**
- Every law of the complex holds for every odd dial (DERIVED; MATH1 8.3's list: the books, the run back, the 24, the
  Hodge split): d d = 0, the balanced cochains, the run back, the 24 as cellular maps, the member.
- What the structure fixes is only:
  - the dial's multipliers: kappa div senses = 3 on an edge (D = 3 x key), and C^T C = 3 on a triangle (3D);
  - the oddness the pair needs.
- So the complex does not fix the key's value. It goes with KEY3 and Big Pic's item 6.
- The grain relation is a fact of the strengths, not of the complex. 10:1x, verbatim: "The mesh world's key 3 divides its
  grain 30,000, so there q = P / 3 exactly".

**The stop.**
- The energy's bound is a board fact (ALG2 3.5). The 2-cochain (the circulation) lies in ker B, outside the energy's
  books, which are the part's sum and the edges' even parts.
- So the bound is not a statement about the 2-cochain's size (DERIVED). One direction holds: a bounded energy bounds the
  passings, and so |y| <= SUM |x_e|.
- A stop term's degree decides its books (DERIVED from ALG2 3.3 and 5): degree 2 adds no residual, degree 3 or more adds
  one, even on one clock.
- 10:0x, verbatim: "its four choices (the pairing, the held hand's own square, the factor, the reach) decide the worlds'
  outcomes". Read so: a stop of degree 2 in the counts adds no residual; one of degree 4 (a square of the held hand's
  square, say) adds one.

**The click world's place.**
- The owner's question (08:5x).
- The complex's facts: with its 12 Mesh cells laid, the click world is one part of 108 coupled clocks (ALG2 4, MEASURED).
  At mesh 0, the islands are 27 of 3 clocks (08:5x, cited).

**The strengths.**
- They are the cochains' coefficients on the coupling cells, and every law of the complex is homogeneous in them.
- The owner's answer 3 reads "laid once at the start for each clock". A coupling joining two clocks has one coefficient,
  on its cell, so the complex asks which clock's: per cell, not per clock. OPEN, the owner's.

## 8. MEASURED (ALG3's probes, on node-all 9d75a4904, Python 3.14.6)

### 8.1 cochain3.py, mode david (L0, 200 rounds)

Fact 1's counts, round 1's D by clock, and SUM D = SUM D over the ties at 5,400 of 5,400 (3.1).

### 8.2 cochain3.py, mode circ

| lay (rounds) | y not 0 | c . q not 0 | c . q - 3 q_ij - (L_j - L_i) not 0 | largest SUM D at a Node-clock |
|---|---|---|---|---|
| L0 (200) | 4,698 of 5,400 | 4,158 | 0 | 708,840,000 |
| L1 (200) | 4,201 of 5,400 | 3,164 | 0 | 10,023,720,000 |
| the swap lay (200) | 0 of 5,400 | 0 | 0 | 529,920,000 |
| the mesh ring (125) | no triangle | - | - | 107,040,000; loop pairings 0 at every round |

### 8.3 member1.py

As in 5.3.

### 8.4 order3.py

As in 3.3 and 5.4.
- The toy's lays are whole numbers in [-6, 6], plus (5, 5, 5) and (7, 3, 3), with W = 200, f = 1 and g = 3, so the
  curvature stays below 4W.
- Its first form, with lays to 30 and W = 1000, ran outside the step's window, and its numbers grew without bound. It was
  stopped, and no number from it is cited.

### 8.5 cochain3.py, mode compare on the swap lay

Byte for byte, with the run back exact (2).

## 9. OPEN, for Big Pic (in his order)

1. The miracle: an exact simultaneous step for degree 4 in whole numbers, run back by the same act, the 24 kept, the
   held walk bounded (3.3, 3.4).
2. Two click observables with a trade-off (section 4).
3. Whether the twin, the member's one new number, can go too (5.5).
4. (C)'s law of the joint measure at the end (section 6).
5. The key's value, the stop's term, the click world's place, the strengths per cell or per clock (section 7).

## 10. DERIVED, MEASURED, OVERTURNED, and where my measurement overturned my derivation

**DERIVED:**
- lead (a)'s failure (eps B C = 0 against a miss in eps; the sign character against an even residual);
- the edge's even part as the coupling's own, removable only by the step;
- kicks and drifts commute, and an order breaks S_3;
- complementarity of the lines and the circulations, and the mod-3 link;
- the edges' cocycle on a triangle, tau as the Hodge split of the three, and the twin forced new by S_3's characters;
- no circulation on a lay a reversing relabelling fixes;
- the end form as the start form pulled back, with no cell and no signal;
- the key, the stop and the strengths as the complex's non-values.

**MEASURED:**
- David's two facts;
- y = 0 on the swap lay, with the residual alive there;
- the mod-3 identity;
- the four-number member on node-all's passings, with its run back;
- the toy's six relabellings, its books and its circulation;
- the mesh ring's loop pairings.

**OVERTURNED:** lead (a), by David's two facts (MEASURED here).

**Where my measurement overturned my derivation:**
1. I first read lead (a)'s premise ("the held hand's square times the giver's and taker's rows") as one coupling on three
   clocks. Fact 1 shows two couplings, each on one edge.
2. My first toy lay meant to be generic, (-4, 4, -3), read y = 0 at every round. It is fixed by the transposition of the
   first two clocks together with the potential's sign flips. The derivation then named that symmetry, and four lays
   with no such symmetry read y non-zero.

## 11. Files (all under S/alg3/)

- ALG3.md: this text.
- probes/:
  - cochain3.py (modes compare, circ, david, and ALG2's kinetic and the others);
  - member1.py;
  - order3.py;
  - hodge2.py and unitlay.py (ALG2's).
- out/:
  - circ_click_L0_200.txt, circ_vary3_L1_200.txt, circ_click_swap_200.txt and circ_mesh_125.txt;
  - david_click_L0_200.txt;
  - member_click_L0_200.txt and member_vary3_L1_200.txt;
  - order3_40.txt;
  - compare_click_swap_200.txt.
- worlds/: click_swap (the test's lay), vary3_L1 and mesh_key7 (ALG2's). unit/: the unit-strength lays.
- all/: node-all 9d75a4904's src and examples. Its archive's sha256 is in tree_9d75a4904.sha256.
