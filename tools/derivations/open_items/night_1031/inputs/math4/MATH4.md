# MATH4: the mathematics of the whole system, on node-all 9d75a4904 (MATH3 with both readers' MATH3 items folded)

MATH4, for the Boss, 2026-10-31, 09:2x UTC. Read only: nothing in /home/user/Universe24 was checked out, edited or
committed. S is S. MATH4 is MATH3
(frozen, sha256 6e9a9cd0...c2b7) with only the lines named in section 14 replaced (MATH3's line numbers); every other
line is MATH3's, word for word. The diff is S/math4/MATH3_to_MATH4.diff. By the owner's word of about 09:05 ("No new
deriver starts on an open item unless Big Pic asks"), MATH4 maps what is derived and names what is open; it starts no
new derivation, and every open item goes to Big Pic.

**The tree.** node-all commit 9d75a4904e8abe5833e919cf113450d579fe2b88 (origin/node-all). With git 2.43.0,
`git archive 9d75a4904` has sha256 c7ac0646b1c96d7a91e23baa3a9da248fd41c675ded7e3cba218e1d30e238ef2, and
`git archive 9d75a4904 src examples` has sha256 91a5ebd617da793c2d670add02f017c363056adf725638260dc351ba2c781bc8. The
second is copied whole into S/math4/nodeall, a folder and not a link; it equals S/math2/nodeall, where the probes ran,
file for file (__pycache__ aside). (09:1x, verbatim: "A frozen text carries its tree or the tree's digest (the commit
and the archive's sha256), never a live symlink.") Its engine and runner are those of 48cd7fcf6, on which MATH1 was
written: `git diff --stat 48cd7fcf6 9d75a4904 -- src` changes five files, all in decoder/ and record/schema.py (writer
E's sides guard and the 1.4 side fields). Every probe below ran on 9d75a4904.

**What was read.**
- MATH1's two reports, S/math1_math/REPORT.md (3 BLOCKING, 14 MINOR) and S/math1_phys/REPORT.md (5 BLOCKING, 8
  MINOR), whole.
- MATH2's two reports, S/math2_math/REPORT.md (4 BLOCKING, 8 MINOR) and S/math2_phys/REPORT.md (4 BLOCKING, 7 MINOR),
  whole.
- MATH3's two reports, S/math3_math/REPORT.md (2 BLOCKING, 8 MINOR) and S/math3_phys/REPORT.md (4 BLOCKING, 6 MINOR),
  whole.
- The Boss's rulings of 07:5x (both parts), 08:1x, 08:3x, 08:4x, 08:5x, 09:0x and 09:1x UTC, and the owner's word of
  about 09:05 UTC (S/BRIEF_PAIRS.md); the coordinator's rulings on MATH1, MATH2 and MATH3. Each ruling MATH4 applies is
  quoted verbatim, by section, where it is applied (09:1x).
- S/key3_phys/REPORT.md (verdict and B1); S/third8_frozen/THIRD8.md (its lines on Big Pic's #2187 6540860812 and the
  fork); S/miracle_a_frozen/MIRACLE_A.md (its statement of (D) and (H)); Big Pic's pairwhole.py docstring
  (bigpic-3clicks ed6a1f225), for where its settings come from.
- ALG1's probe and outputs (S/alg1/probes/cochain.py; S/alg1/out/compare_click_100.txt and books_click_L0_200.txt).
- node-all's record/schema.py (Click, Header, End), run.clicked, run.counts and run.teeth_of; load.py lines 193 to 214;
  plans.py's plan functions; files.py's RETIRED; the five worlds' universe.json.

Each item a reader raised is folded where it belongs: MATH1's in section 12, MATH2's in section 13, MATH3's in section
14.

**Standing words.**
- DERIVED: the proof is here, or the text that holds it is named.
- MEASURED: said only of what a probe moved (the coordinator's ruling 6).
- OPEN or OWED: named.
- A reader's or another text's measurement is cited as theirs.

## Summary

The whole of node-all is one map T on whole numbers, built from three classical pieces.

- **(1) The board.** Its round is four integer shears in (count, edge momentum p = 2D(a - b) + r): two kicks
  p -> p + 4 push and two drifts a -> a + floor((p + D) / 2D), the remainder kept on the edge. At constant teeth it is
  the Stormer-Verlet recurrence with the drift quantized by Rule3's carry and the error fed back. So the momentum is
  exact and the rounding is a bounded coboundary.
- **(2) The mirror.** M (slots swapped, the edge tooth reflected about -1/2, the odd rows negated) is a fixed-point-free
  involution, and M T M = T^-1 under hypotheses (a) to (g), named in 1.5. So T = M o (M o T) is a product of two
  involutions, and it is a bijection of every lawful set that T and M both map into itself.
- **(3) The clicks.** They are a cocycle over the board. Each edge tooth turns on Z/K by its window's passing, and a
  side's clicks to round n are floor((k_0 + S_n Phi) / K). The board reads no tooth, so it is a factor.

What follows:
- **The law of the path, for every click form.** 3.1 and 3.2 prove fiber dependence and the factor: the clicks are a
  function of the board's history and the fiber point, and the board does not depend on the fiber, so seeds one tooth
  apart reach one board. The seed test's twin moves an edge's one tooth on both sides; the owner's test (ii), one unit
  apart, reads NOT SHOWN on the click world's first click by structure and can show only at the third click's member.
  The test's unit is the owner's (08:5x, quoted in 3.2).
- **The first click is fixed on a lay.** Its teeth are laid at their births, so the first click is fixed by its side's
  past.
- **The law's choice.** It belongs to the third click, which is on Big Pic's bench only. It is read by Bell's test
  across a pair on the road the owner chose at about 08:35, (C): with settings independent of the hidden part, CHSH is
  at most 2 for any act, and (C) passes it only through a law of the seeds' joint measure, OPEN (08:4x and 08:5x,
  quoted in 7). It is no theorem of node-all's act.
- **The record's teeth are board fields.** The 1.4 record holds the fiber as board fields carried for the checks; the
  click world's readings read the lines and the sides alone, and a passing recovered through the teeth is a board
  check (08:5x, quoted in 3.1). "Hidden" means hidden from the board.
- **The books.** At a place the trains, edges and triangles form a 2-complex with B C = 0. Its split
  3x = (3x - CC^T x) + CC^T x is the Hodge decomposition at the multiplier C^T C = 3, where each edge lies on at most
  one triangle.
- **The third click's hidden pair (bench).** It runs an affine cat map on (Z/3D)^2. Its L has trace 38, and L = I mod
  3. The u row's second difference is +18y before the carry, -18y after it, and 0 at the round's end. The period is
  528,480 when 3 divides y, else 1,585,440. After two landings the value is floor(38a)/(38a), 789 per mille at
  a = 0.1.
- **Symmetry.** On a cubic O-invariant layout alike at every site, the 24 (O = S4) and the translations commute with T.
  An equivariant bijection keeps every stabilizer, so a broken symmetry comes from the files alone.
- **The energy.** No exact energy is known. MIRACLE_A's Theorem A (under its hypotheses (D) and (H)) is NOT PASSED by
  both its readers (09:0x), and nothing here leans on it. Exact linear invariants exist. OPEN, with HAT4.
- **Closed means periodic.** A lawful bounded orbit of a lattice bijection is periodic. Whether a lay's orbit stays
  bounded is the open square-2 fall and the window (NOT_CLOSED 37).

MEASURED, on what the probes moved:
- on rows 12 and 20 of the click world over 100 rounds: the mirror is an involution, M o T is an involution, the
  momentum identity holds, and the cocycle holds; the board's blindness to the teeth (S7) holds by construction;
- on the well world (shipped with push 1) over 6 rounds, where W, J5, the drive's fine tooth and the given-first rule
  all move: S1 to S4 (the mirror, M o T, the momentum identity, the mirror's momentum). The well's S5 to S7 are vacuous:
  its edge key is 1, its fiber a point, and no tooth moved (MATH3's mathematician, m5; physicist, m6);
- on row 0 of the bang world, and rows 0 and 12 of the well, the momentum sum over the sites is kept exactly, a linear
  invariant;
- as board checks of the record against the act: x = K q + k_after - k_before equals the act's passing on 324 of 324
  sides, the end teeth equal the act's on 162 of 162 entries, and the ledger's counts equal the act's on 405 of 405
  lines;
- the cat map's factor and dial are read from the structure (G = C^T C = 3); its constants and its mod-3 law hold on
  N = 63, and its two periods on the file's dial, with R^n linear in y (11 of 11).

Only the mirror's odd-row half is read by no shipped world: the 0i rows stay 0 on all five. A test's lay is OWED for
the odd rows alone. The shipped click world itself runs 3,751 of its declared 5,000 ticks and writes no record (08:5x,
quoted in 1.7); every click-world reading here is a probe's, its ticks set (3, 100 or 300 rounds).

## 0. The map in one table

Each part: its mathematical object; the clock's view; the click world's view; its standing (ARCH_MAP's block names in
brackets). No cell is "n/a" without its reason; a click-world view the record does not give is OWED by name.

| part | mathematical object | clock | click world | standing |
|---|---|---|---|---|
| Rule3's carry (M1) | Euclidean division n + r = q d + r', 0 <= r' < d; with r kept, the translation by n of m = h d + r in two digits | a dial counts whole turns, the fine tooth stays | a click is such a quotient | DERIVED (1.2) |
| the split (M2) | centred half-open division n = 2D q + s, s in [-D, D); split(-1 - n) = (-q, -1 - s) | the edge's dial of both slots | none of its own: the click world reads lines and sides alone; the passing recovered through the teeth, x = K q + k_after - k_before, is a board check (08:5x) | DERIVED (1.2); the record's identity a board check (R2) |
| the board (M8) | the torus Z/sx x Z/sy x Z/sz with its Cayley graph on the six Spokes (a loop or a double edge where a side is 1 or 2) | each Node-clock's six neighbours | no length: labels (lengths by light's echo, OWED) | DERIVED |
| the gears' state (M6) | X = (a, b, r, rd) in a lattice; equivalently (a, p, rd), (a - b, r) the centred division of p by 2D | count now, count before, the edge tooth, the drive's fine tooth | the counts are not in the record; each clock's own count is OWED (FACE2) | DERIVED (1.1) |
| the teeth W (T2) | a whole polynomial map of the counts, read given first (the loader's rule) | how much a gear carries in a turn | proper time OWED (D6, FACE2); "a deeper clock counts less" is the click world's word, OWED there | DERIVED (code, load.geared); W = rest on four shipped worlds, and W moves on the well (MEASURED C1: up to 1,248 off rest) |
| the potential and the pull (T4, T6, M4) | a whole polynomial V on the readings; J = -dV/da by construction (contract.pushes; for the gradient vertex, plans.meshing's two opposite-signed pushes, summation by parts) | springs, vertices, the Meshes' tug | the rest beat as a mass OWED (reading 8) | DERIVED |
| the kick (T7, T8) | a gradient shear p -> p + 4 push; on the drive's rows a carry-shear on (p, rd) | the drive's whole turns pushed into the gear | seen only through the passings (the drive writes no click) | DERIVED (1.3); the momentum identity MEASURED S3 on the rows that move |
| the drift (M2 gear) | a shear a -> a + floor((p + D) / 2D), the remainder the new tooth | the momentum carried edge to edge | seen only through the passings | DERIVED (1.3) |
| the board's round B | four integer shears, triangular; at constant W the Stormer-Verlet recurrence with quantized drift and error feedback | one pass at every Node-clock alike | one round's click lines; no round is a duration (D4) | DERIVED (1.3, 2.1) under 1.5's hypotheses |
| the mirror (B1) | a fixed-point-free involution; linear in the odd momentum 2p + 1 | time's reversal of a Node-clock | none of its own (the run back writes no click) | DERIVED (1.4); MEASURED S1, S4 |
| the run back (B1) | M T M = T^-1; T = M o (M o T); <T, M> of infinite order (one aperiodic lawful orbit, DERIVED; D1 its check), dihedral of order 2n on an n-cycle | the same act on the mirrored state | the two-record comparison R1; the end line's "exact" is a board comparison printed into the record | DERIVED (1.5); MEASURED S2 (click and well); D1 a check |
| the law of the path and the seed test (B2) | T^n injective (i); the board a factor, so seeds one tooth apart reach one board (ii), (iii); the lawful twin moves an edge's one tooth on both sides | start seed, end seed, back to the start | two records compared (R1, R2's two-record form); (ii) one unit apart NOT SHOWN on the click world's first click by structure (08:5x) | DERIVED (1.6, 3.2); S7 by construction; S5 and S5b off-lay readings, not MEASURED (08:5x) |
| a closed run | a lawful bounded orbit of a lattice bijection is a cycle | the start returns exactly | the record periodic: every decay recurs (1.7) | DERIVED (1.7); confinement OPEN |
| the window (W, NOT_CLOSED 37) | the linear round in SL(2, R), trace 2 - K/W: elliptic iff 0 < K < 4W | a stiff gear outruns its step | a runaway writes no record (the runner names the round); its view OWED | DERIVED (2.3); CONF1's MEASURED |
| the energy (a clock word: the board map's quadratic forms) | no exact energy known; exact linear invariants exist (2.2) | not kept | no conservation of energy is shown in the clicks; the per-edge books close by construction, a code check (09:0x) | OPEN, with HAT4; Theorem A (MIRACLE_A, under (D) and (H)) NOT PASSED by both its readers (09:0x) |
| the click teeth (T11, C1) | a group extension of B by (Z/K)^E; its Z-lift the cylinder map kappa -> kappa + Phi | an edge's pair of teeth, born complementary | the record writes them: dial, birth, k_before, k_after, the end teeth | DERIVED (3.1); MEASURED S6, R1, R2 |
| the passing Phi (T11) | a whole antisymmetric 1-chain on the window (b, a, a+), odd under its reversal | David's split: the given on one side, the taken on the other | stays out of the click world; x = K q + k_after - k_before recovered through the teeth is a board check (08:5x) | DERIVED (code); the board check R2 |
| the first click's line (C1) | a mechanical (Christoffel) word at a steady passing, period K / gcd(P, K); on a lay a function of the side's past | a line of whole quanta | R2 NOT SHOWN, as the law expects | DERIVED (3.3) |
| the structure at a place (C2, D14) | a 2-complex (trains, edges, triangles), B C = 0 | which clocks meet at one place | the place's structure, a board check (the Boss's 07:5x ruling) | DERIVED (L0) |
| the split click (T12, C2) | the Hodge decomposition 3x = 3(I - P)x + 3Px, P = CC^T / 3 | the passing shared over a triangle's edges | the shares against the weights (3a), a board check beside a click reading; OWED as a click-only form | DERIVED (4.2) |
| the third click (C3), bench only | boundary quanta C W; the hidden pair under the affine cat map L(w + (y, 0)) on (Z/3D)^2, trace 38, L = I mod 3 | the triangle's tooth and twin, turned by the palindrome | only in the sides; its choice read by Bell across a pair, OWED | DERIVED (L0 to L9; 3.4); MEASURED K1 to K3 (pure integers); not in src |
| the books (D1, D13) | L1 the edge's orientation, by construction; L3 the vertex sum of the telescoping laws, by B C = 0 | each edge closes; each clock within its teeth | per edge by construction, a code check; E's guard reads mates, sums and teeth ranges, "admitted" meaning the mates close (08:5x); per clock within K x degree | DERIVED (4.3) |
| the 24 (X, M5) | O = S4, the 24 signed permutation matrices of det 1; irreps A1, A2, E, T1, T2 | the star's turns; every train turns by its kinds | isotropy in the meetings OWED | DERIVED; 24 of 24 MEASURED by node-edge and the bench, not by me on node-all |
| the 48 (M5 lifts) | 2O in the unit quaternions over Z[r2] / 2; spinor irreps E1/2, E5/2, G3/2, -1 as -I | half-speed trains and doublets | doublets in the clicks OWED | DERIVED (HALF2, PASSED by both) |
| the kinds' characters (M5, R) | class functions of O and 2O | the kinds by which each train's gears turn under the 24 | the record's header tables; orthogonality not read (OWED) | DERIVED |
| the lay (I1, I2) | the initial point X_0 and the layout; its stabilizer kept forever | the three files, the loader | nothing from the files but through the act | DERIVED (5.3) |
| the key (I3) | the fiber's modulus K (odd), from the laid middle | each tooth's dial | the click's unit; one key per record (the Boss's KEY3 ruling) | OPEN (8.3) |
| the record (R) | a word over the click alphabet, a function of the orbit and the fiber, carrying the fiber as board fields | the boundary of the board | the events the click world is made of: lines and sides; the teeth are board fields carried for the checks (08:5x) | DERIVED (code); board checks R1, R2, R4 and R5 |
| the choice (the law of the choice) | the third click's path (bench); not a theorem of node-all's act | the triangle's hidden pair | Bell across a pair on road (C): CHSH at most 2 for any act with settings independent of the hidden part; (C)'s law of the seeds' joint measure OPEN; R4 under (C) OWED; two questions to the owner (7) | OPEN |
| the click world's order (D11, D12) | the meeting order: a strict partial order inside the round order (10.3) | each clock's own count (OWED) | the click world's 27 of 27 forced by its alike lay; islands: 27 of 3 clocks (click), 3 of 114 / 62 / 187 (mesh); the board couples the sites with no click on both (08:5x) | DERIVED as a definition; C1's and NATURE2's MEASURED |
| the click world's geometry (D3 to D7) | a poset with counts on chains; Bondi's k-calculus on it | each clock's own count | C-a to C-e (PICTURE.md section 8) | OWED (FACE2, LIGHT2) |
| the square-2 fall | an indefinite V along x_g = -x_t; a growing orbit, so not periodic | a tied pair's counts grow together (a clock fact) | a runaway writes no record; its view OWED | OPEN (8.1) |

## 1. The state space and the one round

### 1.1 The state

- **What each site holds.** At every site of the board and every gear row: the count now a, the count before b, the
  edge tooth r in [-D, D) with D = W(a) + W(b), and the drive's fine tooth rd in [0, T_d). At every side (t, u) of
  every edge (at the site, and across each Spoke on the Mesh's edges): the click tooth k in [0, K), K the edge key
  (state.State).
- **The state space.** It is

      Omega = { (a, b, r, rd, k) : r in [-D, D), rd in [0, T_d), k in [0, K), W(a) >= 1, W(b) >= 1 },

  a subset of a lattice. X = (a, b, r, rd) is the board; k is the fiber.
- **The width** of the universe file is a promise the runner reads from outside (run.wide), not part of the map.
- **The edge momentum.** p = senses D (a - b) + r, with senses = 2. Given a, the pair (a - b, r) is the centred
  Euclidean division of p by 2D. W is read given first: the loader lays the clocks' plan so that the rows it reads
  stand at their rest teeth (load.geared cuts the 00 row's read of itself; MATH1 m3). So D is known before the
  division, and (a, b, r) <-> (a, p) is a bijection, triangular in the rows (DERIVED).

### 1.2 Rule3's carry and the centred split

carry(n, d, r) = (q, r') with n + r = q d + r', 0 <= r' < d, is Euclidean division. With its remainder kept,
(h, r) -> (h + q, r') is the translation by n of m = h d + r written in two digits. It has two laws:

- **The telescoping law.** q_0 + ... + q_(N-1) = (r_0 + n_0 + ... + n_(N-1) - r_N) / d.
- **The sign law.** If n + r = q d + r', then -n + r' = -q d + r.

The split (step.split) is n = 2D q + s with s in [-D, D). For every whole n, split(-1 - n) = (-q, -1 - s): the
half-open centred division is odd about -1/2, and in the odd coordinate 2n + 1 its mirror is negation (DERIVED).

As a quantizer this is first-order error feedback, as in Bresenham's line: the quotients' running sum follows the
inputs' running sum over d within one unit. The act has three such carries:
- the drift (remainder r);
- the drive (remainder rd);
- the clicks (remainder k).

### 1.3 The round as integer shears

From step.act, in the coordinates (a, p, rd), the round is four shears in a fixed order:

- **K1, the kick on the force's path rows** (T_d = 1, rd = 0): p_i -> p_i + 4 (s F_i(a) + s T_k J1_i(a)).
- **K2, the kick on the metric's 00 and ii rows** (T_d = senses): (p_i, rd_i) -> (p_i + 4 s F_i(a) + 4 s T_k q_i,
  rd_i'), with (q_i, rd_i') = carry(J_i, T_d, rd_i) and J_i = J1_i(a) + J5_i.
  - J5 reads the stretches and the path rows' momenta before and after K1. It never reads the momentum or the fine
    tooth of a row it lands on. That is hypothesis (d), which the loader builds: plans.pushing lays the kinetic term
    "from every row it does not land on". The act does not enforce it (MATH1 m3).
  - K2 is a carry-shear: it translates the two-digit number q T_d + rd by J and rotates rd in [0, T_d). For a fixed J it
    is a bijection of Z x [0, T_d): from (p', rd') the quotient is the one q with q T_d + rd' - J in [0, T_d). (MATH1
    called its linear part "identity blocks"; that is right for K1, D1 and D2 only, m4.)
- **D1, the drift on the rows at rest teeth (the 00 row):** a_i -> a_i + split(p_i, W_i(a) + W_i(a+)).q, with
  W_i = rest.
- **D2, the drift on every other row:** the same, with W_i reading only the D1 rows before and after D1.

Then b takes the old a, and the new tooth is r = p - 2D (a+ - a).

So B = D2 o D1 o K2 o K1. Each factor has an inverse of its own form, so B is injective wherever W(a), W(b) and
W(a+) are at least 1, and a bijection onto its image (DERIVED). The given-first rule and hypothesis (d) make the
composite triangular; both are the
loader's, not the act's. In the continuum shadow (rationals, no rounding) the kick is a gradient shear. Where J5 = 0
and T_d = 1, at constant W, the round is exactly the Stormer-Verlet recurrence and symplectic (MATH1 m5). Where W
reads the 00 slot, J5 is TERM5_FIFTH's books' form, and the round's Lagrangian reading is not proved here.

**What the probes moved (MATH1 m1; the coordinator's rulings 6 and, for MATH3, 1).** Four shipped worlds have push 0;
the well world is shipped with push 1 and notch 120,000 (MATH2's mathematician, B1).
- On the click world over 100 rounds (cover_tensor24-click_100.txt): the largest |W - rest| is 0, the largest |J5| is
  0, rd never moved, the odd rows 3 to 5 stay 0, and only rows 12 and 20 move (the mathematician's 300 rounds add
  row 14).
- On the well world over 10 rounds (S/math3/probes/cover_well_10.txt): the largest |W - rest| is 1,248, the largest
  |J5| is 346,116,240, rd moved in 10 of 10 rounds, rows 0, 2 (the 00 slot), 6 to 8 (the ii slots) and 12 move, and
  the odd rows 3 to 5 stay 0. MATH2's mathematician measured the same.
- structure.py on the well over 6 rounds (S/math3/probes/structure_well_6.txt): S1 to S7 hold, 6 of 6 each.

So S2, the run back in every field, holds where K2, J5, hypothesis (d) and D2's teeth read all move, and S3 holds
with W moving, so the given-first rule is read. Those parts are MEASURED on the well. AUDIT2's seed test (i) on the
well's 128 ticks read the run back with the push on. Only the mirror's odd-row half is read by no shipped world (the
0i rows are 0 on all five): a test's lay is OWED for the odd rows alone.

### 1.4 The mirror, exactly

    M(a, b, r, rd, k) = (b, a, -1 - r, T_d - 1 - rd, k)   on an even row (parity 1),
    M(a, b, r, rd, k) = (-b, -a, r, rd, k)                on an odd row (parity 0: the metric's 0i rows),

in code tau = senses x parity - 1 and (tau b, tau a, r - parity (senses r + 1), rd + parity (flip(rd) - rd), k).

- M o M = id on the whole lattice (DERIVED). MEASURED S1, an identity of the code.
- p(M s) = -1 - p(s) on an even row, and p(M s) = p(s) on an odd one, since D is symmetric in its two slots. MEASURED
  S4 on the rows that move.
- M fixes no state that has an even row, since r = -1 - r has no whole solution (DERIVED).

### 1.5 Reversible: M T M = T^-1, under named hypotheses

**Theorem (the run back).** On the lawful set, M T M = T^-1, provided:

- (a) both slots' teeth are at least 1;
- (b) every tooth stands within its dial;
- (c) the act's own form holds (step.act);
- (d) J5 reads the momentum of no row it lands on (the loader's plans.pushing);
- (e) W reads only even rows at their rest teeth (the loader's load.geared);
- (f) V is even under negating the odd rows. O-invariance does not give this: v . w, with v the 0i rows and w an even
  T1 train, is O-invariant and odd in v (MATH1 m2);
- (f') every Mesh coupling stays within one parity, or step.crossing is not odd under the mirror;
- (g) J5 reads sigma_in sigma_out of one row at a time.

**Proof, in the edge's terms.** The state is the oriented edge (a_(n-1), a_n) with its momentum p_n; forward,
p_(n+1) = p_n + 4 push(a_n) and a_(n+1) = a_n + Q(p_(n+1); W(a_n) + W(a_(n+1))). On an even row:
1. The mirror of (a_n, a_(n+1); p_(n+1)) is (a_(n+1), a_n; -1 - p_(n+1)).
2. Its push is read at a_n, the same push, so p' = -1 - p_n.
3. Its dial is the edge's own, symmetric, so a' = a_n + Q(-1 - p_n) = a_(n-1).
4. The mirror of the state reached is (a_(n-1), a_n; p_n).

The other parts:
- **The odd rows.** By (f) the push is odd there, so the momentum kept by the mirror returns.
- **The drive.** On an even row J + (T - 1 - rd') = q T + (T - 1 - rd): the same q. On an odd row J is negated, and the
  sign law returns rd with -q.
- **J5.** By (d) and (g) its products sigma_in sigma_out are unchanged on the mirrored state.
- **The teeth.** P is odd under the window's reversal (by (f'), crossing too), so carry(-P, K, k') = (-q, k).

This is DERIVED in the engine's texts (EDGE2, NC29b, COUNT5 M1) and restated here in shear form. The mathematician
re-derived it step by step.

**Corollary.** R = M o T is an involution, so T = M o R is a product of two involutions. <T, M> has infinite order
(DERIVED by a three-line induction; MATH3's mathematician, m1). On the bang world's layout every strength is 0, so a
wave row laid as a uniform drift (a test's lay, named so: a = c + 1, b = c, r = 0 at every site) has every stretch 0,
hence no pull, no J1 and no J5. W stays at rest, since c00 stays 0. So p = 2D stays, the split gives (1, 0), and
a_n = c + n + 1 for every n: all the states are distinct, so the orbit is not periodic, and its backward orbit (by the
mirror) is lawful, so it lies in Omega_inf. D1 checks it, 30 of 30 rounds (S/math3/probes/drift_bang_30.txt). On a
cycle of length n, within the width, the group is dihedral of order 2n. The even reversors
T^(2i) M = T^i M T^-i are conjugate to the fixed-point-free M, so any state fixed by a reversor is fixed by an odd one.
MEASURED S2: R(R(s)) = s in every field, k included, 100 of 100 rounds on the click world and 6 of 6 on the well.

### 1.6 A bijection, and of which set

- R^2 = id needs T s in Omega. Where T s leaves Omega, injectivity still comes from the shear form (MATH1 m11).
- T is a bijection of every lawful set that T and M both map into itself, since T^-1 = M T M then maps it into itself.
- The largest such set is Omega_inf, the states whose whole orbit both ways stays lawful. It is M-invariant: M keeps
  every promise, and under (e) W reads only even rows. A set that T alone maps into itself need not be covered.
- The departures the runner names are exits from Omega, not failures of injectivity.
- The seed test's (i) is the injectivity of T^n (DERIVED). AUDIT2 MEASURED it on all five shipped worlds (the Boss's
  07:5x ruling).

### 1.7 Closed means periodic (a board fact)

**Lemma (DERIVED, by pigeonhole).** An injective map whose orbit through x stays lawful and within a bounded box is
periodic at x. The box's lawful states are finite, so T^i x = T^j x for some i < j, and injectivity gives
T^(j-i) x = x.

- "Closed" is therefore sharp on the board. A lay whose orbit stays lawful and within the width is one cycle of the
  permutation T induces on the finite set of lawful states within the width whose orbits stay there. An orbit that
  stays lawful and is not periodic is unbounded (MATH1 m6; the physicist's m3: "unbounded", not "runs away").
- **In the click world (the physicist's m4).** The record of a closed orbit is purely periodic, so every decay recurs.
  A decay law (geometric lives) can hold only on records short beside the period, and R2 read past one period reads
  repetition. The record's period is the whole orbit's, board and fiber together (MATH2's mathematician, m5). At a
  steady passing the fiber's periods bound the within-record readings: K / gcd(P, K) at the first click, and 528,480 or
  1,585,440 at the third (3.4); Big Pic's 1,000,000 rounds are 1.89 of the shorter. Under a varying passing no fiber
  period bounds them. Bell's settings drawn inside a closed whole are functions of the whole state.
- The confinement's click-world view is OWED by name. run.run writes the record only after the last round, so a run
  that departs writes no record at all: a written record shows that its run stayed lawful and within the width for its
  ticks, and says nothing beyond them (MATH2's physicist, m6). The shipped click world is such a run (08:5x, verbatim):
  "The shipped click world runs 3,751 of its declared 5,000 ticks: at round 3,752 a count passes the width and the
  runner writes no record (KEY2's readers, KEY3's physicist, MIRACLE_A, UNC1). Every text that cites the click world's
  ticks names it. No tick count is cut to hide it. STOP1's bound reads it. To the owner's batch." Every click-world
  reading in this text comes from a probe's copy with its ticks set, or from the act stepped directly.

## 2. The board's own map

### 2.1 Stormer-Verlet with the drift quantized and the error kept

At constant teeth (W = rest on every row, D = 2W), p_n = 4W v_n + r_n with v_n = a_n - a_(n-1), and
p_(n+1) - p_n = 4 push(a_n). Together these give exactly

    W (a_(n+1) - 2 a_n + a_(n-1)) = push(a_n) - (r_(n+1) - r_n) / 4.

This is the Stormer-Verlet recurrence with coefficient W and unit step. W is the recurrence's coefficient, not a
mass: there is no mass on the board (the physicist's m2). The error is the discrete derivative of the bounded sequence
r / 4, so its sum over any run is below W in size (DERIVED).

The family:
- Rannou's lattice maps;
- Earn and Tremaine's lattice standard map;
- Levesque and Verlet's bit-reversible integer dynamics;
- the integer rotations of Vivaldi and coworkers;
- integer lifting steps.

Tensor24's difference from all of them is that the force is already whole, and only the velocity read from the exact
momentum is rounded, with its error fed back.

### 2.2 What the board keeps exactly, and what not

- **On the words (MATH2's physicist, m1).** Here "energy", "momentum" (the edge's p), "work" (a term's push times a
  move) and "falls" name clock quantities of the board map. No conservation of energy or momentum in the click world is
  derived.
- **Exact linear invariants exist (DERIVED, MEASURED).** On a row whose push is the Meshes' pull alone, the sum over
  the sites of p is kept exactly: the pull is alike from both ends of every Mesh, so it sums to 0 over the board.
  - MEASURED (cover_tensor24_10.txt): row 0 of the bang world moves and keeps its sum in every round of its 10.
  - MEASURED (S/math3/probes/cover_well_10.txt): rows 0 and 12 of the well keep theirs in 10 of 10 rounds; rows 2 and
    6 to 8, the metric's 00 and ii slots, which the push lands on, do not.
  - The mathematician's V5 has the same as the bang over 200 rounds with every strength 0.
  - On the click world the moving rows 12 and 20 do not keep theirs; they carry on-site terms.
- **Also kept:** the step's law p+ = p + 4 push, a lay's invariant subspaces, and the lay's stabilizer (5.3).
- **The energy (the coordinator's ruling 4 on MATH1; 09:0x).**
  - No exact energy is known. The edge energy and the polarized energy move from round 1 (CONF1's MEASURED, on the
    square-2 lay). (09:0x, verbatim: "Road A's exact energy is kept in rationals alone.")
  - Theorem A (MIRACLE_A) is stated under two hypotheses: (D), the drive's teeth are 1 wherever the plan's push lands
    ("A drive of teeth senses on a pushed row is not treated; node-all's square has one, on its 00 and ii rows"), and
    (H), each tooth's window holds two neighbouring quotients on runs longer than the degree, at counts on no algebraic
    hypersurface (MIRACLE_A's own words). It would then exclude polynomial invariants of degree below a third of the
    teeth's half-window. (D) fails on the well, whose push lands on the 00 and ii rows at T_d = senses.
  - Both MIRACLE_A's readers read it NOT PASSED (09:0x). Nothing here leans on it. OPEN, with HAT4.
- **The click world's books (the physicist's m2, the owner's D; 09:0x).** Per edge, each quantum is given on one side
  and taken on the other in the same round, by construction: the record's faithfulness to the act, a code check, not a
  law found in the clicks (the Boss's 07:5x ruling). The owner's D is answered (09:0x, verbatim): "no conservation of
  energy is shown in the clicks. The per-edge books close by construction, a code check. Each clock's work against its
  booked total does not hold within its teeth. The board's E is kept only in rationals." 

### 2.3 The window (NOT_CLOSED 37)

For a linear mode of stiffness K (push = -K a, coefficient W), the round is the element of SL(2, R) of trace
m = 2 - K/W:
- elliptic exactly when 0 < K < 4W;
- parabolic at the ends;
- hyperbolic outside, where the growth is geometric (DERIVED; classical).

CONF1 MEASURED a curvature passing 4W at round 1183 on the square-2 lay, with the counts going from 5 to 162 bits in
six rounds. The rounding's error is bounded, and the hyperbolic growth is not.

### 2.4 What an exact invariant would add

- **Confinement.** An exact invariant with finite lawful level sets would make every orbit periodic (1.7).
- **Road A, the McMillan / QRT road (08:5x, verbatim: "Road A keeps only the classical one-gear statement (McMillan,
  Northcott, Mazur). The coupled rational exactness is cited only as MIRACLE_A's claim, which its mathematician did not
  pass, and nothing leans on it.").**
  - The classical statement, for one gear: McMillan's map keeps a biquadratic invariant; an orbit of bounded height is
    periodic (Northcott), with period at most 12 (Mazur's torsion bound for an elliptic curve over Q). That bound is
    for one gear only (MATH1 m14).
  - A rational orbit that is not periodic has unbounded height (Northcott). MIRACLE_A measured its lay's numbers past
    128 bits by round 3. Theorem B is not leaned on.
  - MIRACLE_A claims that the coupled polarized step keeps the edge's energy exactly in rationals. Both its readers
    read MIRACLE_A NOT PASSED (09:0x), and nothing here leans on the claim.
- **The discrete gradient (HAT2, HAT4).** Its whole-number shadow loses the run back on two slots (HAT4).
- **Road B (MIRACLE_B, read by its pair; 08:5x, verbatim: "Road B does not close the owner's question D: it is an
  exact, time-symmetric step that keeps the gears as they are, with no energy kept exactly in whole numbers; its walk
  goes to the owner's batch when MIRACLE_B2 passes.").** Its clicks still carry the act's two-leg passing ("B-edge's
  clicks still carry the act's two-leg passing"), and the held counts' walk is MEASURED with no bound ("the
  physicist's walk of the held counts (MEASURED, no bound)").
- The miracle stays OPEN (NOT_CLOSED 37), first on Big Pic's list (the owner's word of about 09:05). No road is closed
  by an unread or unpassed theorem.

## 3. The teeth and the clicks: a skew product over the board

### 3.1 The cocycle, and what the record writes

At each side sigma = (t, u) and site, with K the edge key and Phi(X) the round's passing (step.passing and
step.crossing, a whole function of the board's window (b, a, a+)):

    k_(n+1) = (k_n + Phi(X_n)) mod K,   q_n = floor((k_n + Phi(X_n)) / K),
    Q_n = q_0 + ... + q_(n-1) = floor((k_0 + S_n Phi) / K).

So T(X, k) = (B X, k + Phi(X) mod K), a group extension of B by (Z/K)^S. Unrolled, it is the cylinder map
(X, kappa) -> (B X, kappa + Phi(X)) (DERIVED). MEASURED S6, an identity of the code: K SUM q = k_0 + SUM P - k_n on
every side and site, 100 of 100 rounds.

**The two sides of an edge.** An edge's two sides are one tooth read from two ends: born summing to K - 1 with K odd,
so k(u, t) = K - 1 - k(t, u) and q(u, t) = -q(t, u) forever. The fiber is (Z/K)^E. ALG1 measures this on the click
world: its cochain act keeps 3 own-edge teeth and 12 Mesh-edge teeth per Node-clock, against node-all's 175 side
teeth, with 0 entries off over 100 rounds, the run back exact (S/alg1/out/compare_click_100.txt; ALG1's, unread by a
pair).

**The edge key (MATH1 m7).**
- K is the file's key times kappa / 2, and kappa / 2 depends on the world: 1 on the bang and live worlds, 3 on the click
  and mesh worlds (the click world's edge key is 152,434,287; MEASURED R1).
- By plans.edging, kappa / 2 is a product over the edged monomials' leg counts, so an edged four-leg monomial would make
  the edge key even and the births non-complementary. files.py refuses only an even file key.
- The Boss's KEY3 ruling has the load show D's oddness by structure or refuse an even D by name. That is not in
  9d75a4904's loader (runner/ is unchanged since 48cd7fcf6): OWED in code.

**What the 1.4 record writes (the coordinator's ruling 2), and the ledger beside it.**
- the header's dial (the edge key K) and birth (every tooth's birth, (K - 1) div senses);
- every click line's sides as [u, q_tu, k_before, k_after], and across each Mesh [u, place, q, before, after];
- the end line's teeth (record/schema.py, run.clicked, run.teeth_of);
- the ledger beside the record (run.counts): every train's now counts at every Node-clock in every round (MATH2's
  physicist, m2). The decoder reads its lines (decoder/records.py).

The record's teeth (08:5x, verbatim): "the 1.4 record holds the fiber as board fields carried for the checks (E's guard,
the books, the run back). The click world's readings read the lines and the sides alone (shadow.py reads q alone). The
board's passing stays out of the click world; a passing recovered through the teeth is a board check." And the owner,
about 09:05 (verbatim): "by law the click world must work by the uncertainty principle, and it must come from the
clicks. So no click reading reads the teeth".

So x = K q_tu + k_after - k_before is the side's exact passing, recovered through the teeth: a board check. MEASURED as
board checks of the record against the act (record3.py, S/math3/probes/record3_click_3.txt; 3 rounds of the click
world written by the tree's own runner into my folder):
- R1: the header's dial is 152,434,287 and its birth 76,217,143, equal to the layout's key and the lay's teeth;
- R2: x equals the act's own passing on 324 of 324 listed sides;
- R3: no Mesh side carried in those rounds (0 of 0), so the across form is not read;
- R4: the end line's teeth equal the act's end teeth on 162 of 162 entries (6 own-edge sides at 27 sites; no Mesh
  side carried);
- R5: the ledger's 405 Count lines each equal the act's now counts of their train, site and round, 405 of 405.

The physicist measured the same 324 of 324. The ledger, like the teeth, is board fields: a reading that uses it is a
board check. "Hidden" means hidden from the board: no board coordinate reads a tooth.

On the bang and live worlds the edge key is 1, the fiber is a point, and the click is the passing itself; they write
no click line (no edge). The mesh world's key 3 divides every passing (their gcd is 30,000), so its teeth never move:
each click is the passing over 3 (the Boss's 07:5x ruling).

### 3.2 The board reads no tooth: the law of the path, for every click form

**What the code does.** In step.act the click teeth k enter one expression only, the last carry, and no later push
reads its quotient. So pi(X, k) = X satisfies pi o T = B o pi: the board is a factor (DERIVED; the mathematician
re-derived it). S7 holds by construction, for the same reason (MATH1 m1). S5, one unit in one side's tooth, is a
one-side twin: an off-lay reading (08:5x, below).

**What it proves (the coordinator's ruling 2 on MATH1 and on MATH2).** 3.1 and 3.2 prove fiber dependence and the factor:
the clicks are a function of the board's history and the fiber point, and the board does not depend on the fiber. So
two seeds alike on the board and one tooth apart reach one board. Their clicks differ only where some side's running
sum k_0 + S_n Phi is carried differently, which no theorem gives (MATH2's mathematician, B2). The law's "the path of
the clicks is not [deterministic]" reads here as "not a function of the board", which is the factor (the physicist's
B1(d)).

**The seed test's twin (08:5x, verbatim).** "The seed test's twin moves an edge's one tooth on both sides (k(t,u) + d,
k(u,t) - d). A one-side twin is an off-lay state that sides.paired refuses; its readings are not cited as MEASURED
(MATH3's S5b, UNC1's twin). The owner's test (ii), one unit apart, reads NOT SHOWN on the click world's first click by
structure (every passing is a multiple of G = 24,000, gcd(G, K) = 3: DERIVED by UNC1's mathematician). It can show
only at the third click's member (DECODE3f's 798 sides; UNC1's physicist's 42 and 35 quanta on a window). The test's
unit is the owner's: no unit or lay is changed to make it show. To the owner's batch as a finding."
- So S5b (the busiest side's tooth moved by half the key, 67 clicks moved, all at side 13, the side (2, 3), at site 0,
  the board alike 100 of 100; S/math1/probes/s5b_click_100.txt) and the one-unit S5 are off-lay readings, cited as such
  and not as MEASURED. S5b's twin left the complementary set: its mate, the side (3, 2), moved no click, and its record
  would carry broken mates (MATH3's mathematician, m2).
- The mesh world's key 3 divides every passing (07:5x), so there q = P / 3 whatever the tooth.
- MATH3's "needs a key finer than the passings' grain" is withdrawn as a remedy: the unit is the owner's.

### 3.3 The first click: fixed by its side's past on a lay

**On a lay (MATH1 B2).** Every tooth is born at (K - 1) div 2 (load.py), so k_n = ((K - 1) div 2 + P_0 + ... +
P_(n-1)) mod K. Each P_i reads only the side's own window and its partner's across one Mesh. So on every shipped lay
the first click is a function of the board's history: fixed by its side's past (DERIVED).

**At a steady passing.** q_n = floor((k_0 + (n + 1) P) / K) - floor((k_0 + n P) / K), the Christoffel word of slope
P / K. Its period is K / gcd(P, K), and one period of the past fixes the future. ARCH_MAP C1 has R2 NOT SHOWN for the
first click (0 of 54 sides), as the law expects: the first click draws nothing.

**At edge key 1** the click is the passing itself, a function of the present window.

### 3.4 The third click's hidden pair (Big Pic's mode 11, bench only)

Per triangle: the tooth tau and its twin eta on the dial N = 3D (odd), centred at B3 = (N - 1) / 2, with
w = (u, v) = (tau - B3, eta - B3). One round (circ.py's Stepper, read line by line; fiber.py and cat.py re-write it):

    w -> A2 (A1 w + (y, 0))  mod N,   A1 = [[10, 3], [3, 1]],   A2 = [[1, 3], [3, 10]],

and the landing W is the number of wraps of tau when y is added. The shear's factor and the dial are read from the
structure, not typed (MATH2's mathematician m3, physicist m3): cat3.py takes the click world's edges at one Node-clock
from the layout's click plan (run.joined), (2, 3), (2, 4) and (3, 4), its one triangle (2, 3, 4), C = (1, -1, 1) and
G = C^T C = [[3]]. The factor is G's diagonal, 3, and the dial N = G D = 457,302,861 (MEASURED G0,
S/math3/probes/cat3_click_21.txt). That holds on a lone triangle; with shared edges the shears go by K_F = C^T C,
which is not 3 I. The passings y in my probes are stand-ins, and F4 and K1 to K3 read them, so they are board-informed
readings (the physicist's m7).

- **The matrix.** A2 A1 = [[19, 6], [60, 19]], and A1 A2 = [[19, 60], [6, 19]] = L between two rounds' carries. Trace
  38, determinant 1, so L^2 = 38 L - I. L is a hyperbolic element of SL(2, Z), Arnold's cat-map family. The round is an
  affine bijection of (Z/N)^2 for every y (F3).
- **The second difference (the coordinator's ruling 1; MATH1 B1, the physicist's B3).** Let w_b(t) be the pair just
  before the carry. Then w_b(t + 1) = L w_b(t) + L (y, 0). By Cayley-Hamilton, w_b(t + 2) - 38 w_b(t + 1) + w_b(t) =
  (L - 37 I) L (y, 0) = (18y, 6y). So the u row's constant is:
  - **+18y before the carry;**
  - **-18y after it** (there w(t + 1) = L w(t) + (y, 0), and (L - 37 I)(y, 0) = (-18y, 6y));
  - **0 at the round's end** (there the translation is A2 (y, 0) = (y, 3y), and the u row of (M - 37 I)(y, 3y) is 0).

  It is never -y (DERIVED). MEASURED K1 (cat_21_file.txt), every pair of N = 63 over four rounds, the u row's second
  difference mod N:
  - y = 5: 0 at the start, 27 = 18y before the carry, -27 after it;
  - y = 6: 0, -18 (= 108 mod 63, centred) and 18;
  - y = -4: 0, -9 and 9.

  The readers measured the same on N = 63 and on the file's dial.
- **L = I mod 3 (MATH1 m8).** 10, 3, 1, 19, 6 and 60 are 1, 0, 1, 1, 0 and 0 mod 3, so every round keeps v mod 3 and
  moves u mod 3 by y. MEASURED K2: 47,628 of 47,628 rounds on N = 63. The 3-part of the hidden pair is a translation,
  not mixing.
- **The period (the coordinator's ruling 1).** At a steady passing the round is R(w) = M w + t, with M = A2 A1 and
  t = A2 (y, 0). L's orders on the dial's prime powers 27, 641 and 26,423 are 9, 160 and 2,936 (the readers' C1 and
  P1), lcm n = 528,480. I computed R^n and R^(3n) by squaring mod N on the file's dial, N = 457,302,861 =
  3^3 x 641 x 26,423 (MEASURED K3):
  - M^n = I for every y;
  - R^n is the identity at y = 3, 6 and 9;
  - at y = 1, 2 and 10, R^n is a translation of u by D y mod N (152,434,287, 304,868,574 and 152,434,287);
  - R^(3n) is the identity at every y tried.

  Any period P has M^P = I, so n divides P, and P divides 3n. R^n is the translation by S_n A2 (y, 0), with S_n the
  sum of M's first n powers; it is linear in y, and at y = 1 it is (D, 0). So R^n is the identity exactly when 3
  divides y (MEASURED K3b: R^n's translation at y is y times its translation at 1, 11 of 11 for y = 2 to 12). The
  round's order is therefore **528,480 when 3 divides y, else 1,585,440** (DERIVED from K3 and K3b), and an orbit's
  period divides it (MATH2's mathematician, m2).
- **After two landings (the coordinator's ruling 1).** The value is floor(38a) / (38a), 789 per mille at a = 0.1
  (DERIVED by THIRD7's mathematician; K4 computes it: floor(3.8) = 3, and 30 / 38 is 789 per mille). It is given in
  this form only, with no bracket.
- **The twin's Z/3 (DERIVED).** Every shear that moves u adds 3v to it, the carry moves u alone, and 3 (v + D) = 3v mod
  3D. So R(u, v + D) = R(u, v) + (0, D): which third of the dial the twin stands in is an exact Z/3 that no landing,
  side or line reads.
  - F4's words saturate at exactly N^2 / 3 on N = 63 only (1,323 of 3,969).
  - On N = 15 and 255 they saturate far below (10 against 75; 4,272 against 21,675), which is consistent with the Z/3
    as a lower bound but does not corroborate it (MATH1 m8; the physicist's m7).
  - For MIN1: a candidate double inside the twin. It is the owner's, since removing it changes the twin's dial.
- **The horizon (MEASURED F4, toy dials, a board-informed reading).** The first past length at which a triangle's
  landings fix the next landing for every pair is:
  - 5, 33 and 18 rounds at the steady passing (N = 15, 63 and 255);
  - 7, 22 and 27 for the walk.

  On the file's dial the horizon is not measured. As a function of the laid middle (ruling 5) it is finite there, since
  the fiber is.
- **A finding against the bench form, for the owner (the physicist's B2(a); MATH2's physicist, B3 and m4).**
  - DERIVED: for every passing sequence, the partition of the place's fiber by its side words (the sides
    q = Q + C W as output) refines at most |fiber| - 1 times, so beyond a finite horizon (which depends on the
    passings) the place's sides' past fixes every later side (MATH3's mathematician, m7). At a steady passing, once a
    past of length n fixes the next side, it fixes every later one (the map is the same each round). F4 measured only a
    triangle's own landings W.
  - If the owner answers (Q1) yes, the bench form does not meet the per-clock half of the law of the choice ("nothing a
    clock can read before its click determines the outcome, not its past") beyond its horizon, at every passing. This
    is board-informed: F4 reads the passings.
  - At some steady rates its landings are also not independent of the last two: at a = 0.1, after two landings, the
    value is floor(38a)/(38a), 789 per mille of the rate. So it does not meet, at every rate, "breakups without memory
    and landings independent of the last".
  - The line never shows the path (L4, proved).
  - Both readings set the clicks against the board's passings (F4 reads y; the lag-two value is a statistic of W,
    which the sides show only inside q = Q + C W), so each is a board check beside a click reading, with its click-only
    form OWED (the Boss's 07:5x rule).
  - Both go with the owner's memory items (the Boss's ruling on THIRD7 at 07:1x). The law does not bend for them (law
    line 35 (17)).

### 3.5 The whole skew product (bench) and node-all's

- **On the bench.** The fiber is the edge teeth in (Z/3D)^E and the triangles' pairs in (Z/3D)^(2F). Each fiber map is
  a bijection for every board point (a rotation; an affine bijection whose linear part has determinant 1), so the
  skew product is a bijection with no condition on the passing (DERIVED). The clicks are q = Q + C W.
- **In node-all as built.** The fiber is the first click's (Z/K)^E alone. The third click is not in src (ARCH_MAP C3;
  the Boss's 07:1x ruling).

## 4. The structure: a 2-complex and its Hodge split

### 4.1 The complex

At one Node-clock:
- the vertices V are its trains;
- the edges E are the pairs of trains a monomial joins (plans.edging);
- the triangles F are three trains pairwise joined.

The chain complex is C_2 = Z^F -> C_1 = Z^E -> C_0 = Z^V, with C each edge's sign on a triangle's boundary and B
+1 at an edge's lower end and -1 at its higher.
- L0: B C = 0 (DERIVED; kturn.py checks it exactly).
- The Mesh's edges join a train here to a train across a Spoke and lie on no triangle.
- On the click world, ALG1 reads the complex per place as own edges (2, 3), (2, 4) and (3, 4), twelve Mesh edges, and
  the one triangle (2, 3, 4) (S/alg1/out/compare_click_100.txt).
- Which clocks meet is read from what passes, a board check of the place's structure (the Boss's 07:5x ruling).

### 4.2 The split is the Hodge decomposition

Over the rationals, C_1 = im B^T + im C + H orthogonally, where H = (ker B) meet (ker C^T) holds the harmonic chains
(the first homology).

- **Every edge on at most one triangle.** Then C^T C = 3 I, and P = C C^T / 3 is the orthogonal projection onto im C.
  So 3x = 3(I - P)x + 3Px: the edges' own shares lie in im B^T + H, and the circulation in im C. There is no
  division: the multiplier is C^T C (DERIVED).
- **A lone triangle.** H = 0 and B^T B + C C^T = 3I, so the edges' share is the pure gradient B^T B x.
- **n clocks pairwise joined, every triangle filled.** B^T B + C C^T = n I.
- **The harmonic part.** It rides with the gradient on the edges' own teeth. Whether a shipped place's train graph has
  a cycle on no triangle is not read: OPEN.

### 4.3 The books

- **L1, each edge's books:** q at one end and -q at the other, by the edge's orientation and the sign law. No B C is
  needed: this is by construction, the record's faithfulness, a code check (the Boss's 07:5x ruling). The guard's reach
  (08:5x, verbatim): "E's guard reads mates, sums and teeth ranges; 'admitted' means the mates close, not faithful to
  the act. A code item, queued for the round after node-fold: the guard refuses by name a side on an edge the end line
  does not list and a header dial off the file's key. Until then the texts name the guard's reach." (sides.paired, in
  9d75a4904's decoder.)
- **L2, each clock's line is its own:** B q = B Q + B C W = B Q (needs B C = 0; the third click's form).
- **L3, each clock's books within its teeth:** D SUM(B Q) - SUM(B x) = B (g_0 - g_n) / 3, below D times the degree
  (needs B C = 0).
- **L4, never seen alone:** B C W = 0. A corollary of L2.
- **In node-all as built** (the first click alone), each clock's books close by the vertex sum of its edges'
  telescoping laws, with no B C: K SUM(line) - SUM(passing) = SUM_u (k_0 - k_n), within K times the degree. ALG1's
  "K booked - swept at a clock (David's identity, the teeth's part)" reads this, within a tooth, over 200 rounds
  (S/alg1/out/books_click_L0_200.txt).
- **A place's sum** is its across net: the place identity, DERIVED. It is no reading of conservation (the Boss's 07:5x
  ruling).

### 4.4 Shared edges

With an edge on two triangles, K_F = C^T C has +-1 off its diagonal. The law's split then leaves (3I - K_F) C^T x of
circulation on the edges. There are three roads:

1. The law's own split at 3D. It is proved, but it is not orthogonal.
2. The full complex's nI at nD. It is exact, but needs every triangle filled.
3. The adjugate split at det(K_F) D. It is exact where K_F is invertible, but it is not lawful as it stands: det 8 on
   two triangles sharing an edge gives an even dial, and the four-clock surface makes K_F singular. A note, not a road.

## 5. The symmetry

### 5.1 The 24 and its kinds

- **The group.** O is the 24 signed permutation matrices of determinant 1. kinds.turns finds them among the 216
  matrices whose rows are three of the six Spokes, by (det + det^2) div 2. O is isomorphic to S4.
- **Its irreducibles.** A1, A2, E, T1 and T2, of dimensions 1, 1, 2, 3 and 3, built from the matrices with no table
  typed.
- **The four-vector's square** is A1 + T1 + (A1 + E) + T2.
- **On the whole state**, the 24 act:
  - by the kinds' signed permutations on the rows;
  - on a negated row's edge tooth by r -> -1 - r, which is linear in the odd momentum 2p + 1;
  - by permuting sites and edges on the click teeth, an edge's passing being an A1 scalar.

### 5.2 Equivariance, with its conditions

**Theorem (DERIVED by construction).** For g in O and every translation t_v, T(g s) = g T(s) and T(t_v s) = t_v T(s),
on a cubic board with an O-invariant layout alike at every site. The reasons:
- every plan term is an invariant tensor (an integer Reynolds operator, the group sum c u u^T, runner/load.py's tables);
- W reads the A1 slot 00;
- the grips are alike from both ends;
- the edge key is a scalar;
- no turn negates a row with T_d > 1 (MATH1 m9).

On a non-cubic board only the turns that keep its shape act on the sites. The live (3 x 3 x 40) and mesh (180 x 1 x 1)
worlds are not cubic.

M commutes with every g, so on such a layout the symmetry is ((Z/s)^3 semidirect O) x <M>. The 24 of 24 measurements
are node-edge's (the click world's cube) and the bench's (check24 on mode 11), not mine on node-all (MATH1 m9).

### 5.3 The lay breaks it, as initialization, and only so

T commutes with G, so the stabilizer of every later state is the stabilizer of the lay (an equivariant bijection keeps
stabilizers exactly). Here the lay is the initial point and the layout, the board's shape included (MATH1 m9). Every
asymmetry in the record comes from the three files (DERIVED). CONF1 MEASURED the square-2 lay's stabilizer, 1 of 24,
kept 1194 of 1194 rounds.

### 5.4 The 48

- **The group.** 2O: the 48 unit quaternions u w^k z^m, with w = (1 + i + j + k)/2 and z = (1 + i)/r2, coordinates
  in Z[r2]/2 held doubled (kinds.lifts). The covering to O is the sandwich, with kernel +-1.
- **Its spinorial irreducibles.** E1/2, E5/2 = A2 x E1/2 and G3/2 = E x E1/2, on which -1 acts as -I. Their characters
  are 2 Re g and its A2 and E multiples; r2 enters at the 90-degree classes.
- **The trains.** The 8-gear train is the monomial representation of 2O on the cosets of C6 = <w>, and the 24-gear
  train is T1 x that.
- **In this build** no family couples a half-speed train. Standing: HALF2 PASSED by both.

## 6. The algebra the act lives in

- **Z.** Addition, multiplication and Euclidean division (Rule3) alone. Every act is a composition of whole polynomials
  and floor divisions by positive whole divisors.
- **Z[i].** The algebra of a reading (CONF1's Gaussian hands and norms), not of the act: the act never multiplies by
  i, and at spring 10^8 the held hand no longer turns a quarter (NOT_CLOSED 37) (MATH2's mathematician, m1).
- **The whole quaternions.** Hamilton's product built from the star: Q8, then 2T (with w), then 2O (with z), hence
  Z[r2]. The 24 turns are 2O's sandwiches.
- **The characters.** Class functions of O and 2O, written in the record's header. Their orthogonality as a decoder
  reading is OWED.
- **Invariant theory in whole numbers.** The plan's channels come from the integer Reynolds operator.
- **The chain complex over Z,** with the Hodge split kept whole by the multiplier 3.
- **SL(2, Z), twice.** The leapfrog's linear round, elliptic in the window, and the third click's palindrome, trace 38,
  on Z/3D.

## 7. The choice and the determinism, as the rulings place them

- **The whole has no choice.** T is a bijection of the lawful set, so the whole state fixes every round both ways
  (DERIVED). AUDIT2 MEASURED the seed test (i) on all five shipped worlds.
- **The law of the path holds for every click form** (3.1, 3.2; the coordinator's ruling 2 on MATH1 and on MATH2).
  The clicks are a function of the board's history and the fiber point, and the board does not depend on the fiber,
  so seeds one tooth apart reach one board (DERIVED; S7 by construction). The seed test's twin moves an edge's one tooth
  on both sides; the owner's (ii), one unit apart, reads NOT SHOWN on the click world's first click by structure, and
  can show only at the third click's member (08:5x, quoted in 3.2). S5 and S5b are off-lay readings.
- **The first click is fixed by its side's past on a lay** (3.3). It has no choice, as the law of the three clicks has
  it ("it draws nothing").
- **The law's choice is the third click's.** It is on the bench only (mode 11), read by Bell's test across a pair on
  road (C), and OWED. It is not a theorem of node-all's act, which has no third click. If the owner answers (Q1) yes,
  the bench form does not meet the per-clock half beyond its horizon, at every passing (3.4).
- **Struck from MATH1** (ruling 2):
  - the sentence "what a Node-clock reads is board coordinates": the act's last carry reads the tooth at the Node-clock;
  - "which nothing a clock reads contains";
  - "a theorem of the act".
- **What the record writes:** the dial, the birth, each side's k_before and k_after, and the end teeth (3.1); the
  ledger beside it writes every train's now counts. These are board fields carried for the checks: the click world
  reads the lines and the sides alone, and a passing recovered through the teeth is a board check (08:5x, quoted in
  3.1).
- **What the decoder's within-record readings must do** (the physicist's B2(b); MATH1's "need a horizon" is withdrawn,
  since a necessary reading gated below its horizon could no longer fail):
  - read the click record alone, with no board passings and no tooth read as a choice;
  - run over the whole record, at the ruled power;
  - read R2 at lag one beside a lag-two reading, against the derived value floor(38a)/(38a); and (08:4x, verbatim)
    "R2 is read in each clock's own count. Each place's whole joint past is read by R2's ladder (L = 1, 2, 4, 8), a
    necessary reading only.";
  - name the period, 528,480 or 1,585,440 at a steady passing, as a function of the laid middle (ruling 5);
  - say NOT SHOWN where they fail, naming the form's memory;
  - never read a choice. Only Bell's test across a pair reads the choice.
- **Bell, as it stands now.** The owner's word of about 08:00 UTC, "Bell is in the clicks, not on the board"; his
  choice at about 08:35 UTC, "8: C. Big Pic builds." (#2187 6541185833). The rulings, verbatim:
  - **The bound (08:4x):** "A click-setting causes nothing on the board (the law of the path); it only chooses which
    reading of a place's record is that place's outcome. So with settings independent of the hidden part, CHSH is at
    most 2 for any act (THIRD8's physicist, DERIVED)." And (08:5x): "The bound 2 holds for every form with settings
    independent of the hidden part, the pair's one hand included. Under (C) it is cited for the free-lay control (the
    member born at the middle)."
  - **Road (A) (08:4x):** "Road (A) reaches above 2 only if a click writes into a state element that the far place
    reads, which needs a channel between Node-clocks. Road (A) and road (B) stay in the record as history, with these
    corrections." Such a channel would break the law of the path ("a click writes nothing into the gears"). (A) and
    (B) are the roads not taken.
  - **The clickless influence (08:4x):** "A board influence that writes no click is measurement dependence, never a
    separate road." MATH3's "a gap in R4's order reading" is withdrawn.
  - **Road (C) (08:4x):** "The act is one-to-one and keeps the count of states, so it cannot make (C)'s correlation.
    That correlation sits in a law of the seeds' joint measure: OPEN, with Big Pic's two-ended build. A seed rule chosen
    for S above 2 is a pick for an outcome." "The seeds' law must be covariant under the swap, S_3 and the 24. A law at
    the start must fix the births to all their digits, so its natural place (the start, the end or the pair events) is
    OPEN." Big Pic's conditions are the rule: "the correlation comes from a law, never from a seed laid by hand for
    the outcome; no law is yet shown to give nature's pattern; the test must be one that can fail."
  - **The local control (08:4x):** "Until the law exists, the member is born at the middle and reads at most 2 across
    places: the local control."
  - **R4 under (C) (08:4x):** "the full correlation pattern (Tsirelson's 2 r2 and the pair's curve), not only S above
    2, with the law that couples the settings to the hand named and reached with nothing picked; no signal; the order
    reading; a free-lay control that reads at most 2, measured; all of it twice. Settings and outcomes are clicks: each
    setting a line of its own clock, and a pair named by the meeting that bore it." And (08:5x): "R4's part (b),
    measurement independence, is replaced under (C) by: 'the settings' dependence on the hand is the seeds' law's
    alone', the law named in the initialization (covariant under the swap, S_3 and the 24) and reached with nothing
    picked. The seeds write no line, so the click world reads only the law's effect: the settings' lines and the
    outcomes' lines, their meetings and their order, no signal, and the free-lay control at most 2."
  - **Where every Bell number's settings come from (08:5x: "Every Bell and GHZ row says where its settings come
    from").**
    - The first click with no draw, 2,499 per mille (PICTURE.md section 4; pairwhole.py at ed6a1f225): each place
      draws its own setting from its own turned teeth (pairwhole.py's docstring), the pair's teeth unturned. CHSH
      alone passes no choice.
    - Big Pic's toy's 2,501 per mille (pairwhole.py): the same settings, the pair's one hand read at both places; it
      rested on a read of the far setting (#2187 6540860812) and is struck as evidence.
    - The owner's toy's 2.82: its settings are not stated in his word (03:4x); OWED by name.
    - Big Pic's copies world (#2187 6540860812), at most 2: each place reads its own setting.
- **Two questions for the owner's batch, through the Boss** (named, not answered), with their stakes:
  - **(Q1)** Are a clock's sides, and its past board readings, "what a clock can read"? Its stake (08:4x, Q10,
    verbatim): "if the sides are readable, the held clock's own sides give the landing in 936 of 1,000 later rounds".
  - **(Q2)** Does the record keep writing the teeth (k_before, k_after, the birth and the end teeth), and the ledger
    the board's counts beside it? Its stake in two cases (08:5x, Q11, verbatim): "(a) if the teeth were click content,
    the record would put the board's exact passing P = K q + k_after - k_before into the click world at every listing;
    (b) as built they are board fields, and no click reading changes with them." The owner's word of about 09:05 on
    Q11: "no click reading reads the teeth".
- **Proved against measured.**
  - Proved in whole numbers: L0 to L3, L5, L6 and L9, with L4 a corollary of L2 (ALGEBRA.md's law of the three clicks).
  - L7 and L8 rest on the mirror, the sign law and the tests.
  - Measured, not proved: R2 within one record, the memory (THIRD7: fresh only at some rates; periodic at a steady
    passing), CHSH (toys) and the lives (bench).

## 8. What stays open

1. **The square-2 fall.** V is indefinite along x_g = -x_t at k = 0. CONF1 MEASURED the orbit growing past the width at
   round 1194 as built, and to 50 bits by round 1250 under HAT2's form. A periodic orbit is bounded, so this one is not
   periodic, and no invariant with finite lawful level sets holds on it. Confinement needs a coupling-family term
   positive on the tied pair, or a step that keeps an energy bounded below. OPEN.
2. **The miracle.** An exact, time-symmetric, energy-keeping whole-number step. No exact energy is known; Theorem A is
   NOT PASSED by both MIRACLE_A's readers (09:0x), and road B keeps no energy exactly in whole numbers (08:5x). OPEN
   (NOT_CLOSED 37, HAT4), first on Big Pic's list (the owner's word of about 09:05).
3. **The key's scale (the coordinator's ruling 5; the physicist's B4).**
   - MATH1's point that the law, not the file, should fix the key is struck.
   - KEY3, as the Boss took it, lays the key's middle once and has the node compute K = 2 middle + 1 and the edge dial
     at initialization. That answers the owner's C by both roads.
   - The middle may not be chosen for its period: no chosen strength.
   - Every within-record horizon is named here as a function of the laid middle: the third click's period through the
     dial's prime powers and y mod 3 (3.4); the first click's period K / gcd(P, K); and F4's horizon.
   - KEY3's physicist (S/key3_phys/REPORT.md, B1) finds that on node-all the laid middle is neither the click dial's
     middle nor any tooth's birth. On the click world the dial is 3K, and its births are 76,217,143 against KEY3's
     25,405,714. So the field's name must be derived again on node-all; KEY4 is being written. The key's value goes to
     the owner with its provenance. OPEN.
4. **Each clock's own count and light's echo: the click world's geometry.**
   - The record would give a partial order (section 10) with a count on each clock's chain.
   - PICTURE.md section 8's conversions are Bondi's k-calculus on it.
   - "Order and counts give geometry" is, for a discrete order, the causal-set conjecture (the Hauptvermutung; Bombelli,
     Lee, Meyer and Sorkin 1987), not a theorem. Malament's theorem is a continuum result (MATH1 m13; the physicist's
     m5).
   - The face (FACE2) and the echo rule (LIGHT2) are not built. OWED.
5. **The generations.** At a place the three clicks are the chain complex's three pieces:
   - the edge quanta, gradient and harmonic, seen alone;
   - the split itself;
   - the boundary quanta, divergence free, never seen alone.

   That they are the three generations is the owner's word, to be read in the click world through the decoder. OPEN.
6. **The three clicks are not in node-all's act.** R4 is NOT READ; the decay law is NOT READ on the shipped records
   (the Boss's 07:5x ruling).
7. **Smaller items.**
   - A test's lay for the mirror's odd-row half alone (1.3), OWED.
   - D's oddness by name in the loader (3.1).
   - The harmonic part (4.2).
   - Shared edges (4.4).
   - The characters' orthogonality reading (6).
   - The twin's Z/3, for MIN1 (3.4).
   - Theorem A's standing: NOT PASSED by both its readers (09:0x); nothing leans on it (2.2).

## 9. The great mathematics of the whole system, as its parts give it

- **The act and its maps.** node-all's act is a product of integer shears and Euclidean divisions (1.3), and its run
  back is the same act on the mirrored state, under named hypotheses (1.5).
- **Closed means periodic.** Within the width, on a lay whose lawful orbit stays there, the whole is one cycle of a
  permutation of a finite set of whole-number states (1.7).
- **Its symmetry.** On a cubic board with an O-invariant layout alike at every site, the permutation commutes with the
  cube's 24 turns and the board's translations, and the lay alone breaks them (5.2, 5.3).
- **A skew product.** The board is deterministic and autonomous, the factor (3.2). The fiber is the first click's
  circles (Z/K)^E, one per edge (3.1). The clicks are the cocycle's integer parts.
- **The books.** They close per edge by construction, and per clock within its teeth by the vertex sum (4.3).
- **The fiber's place.** It is hidden from the board, and the record carries it as board fields for the checks; the
  click world reads lines and sides alone (3.1).
- **The law of the path** holds for every click form (3.2).
- **The choice** the owner's law names lives at the third click. That is Big Pic's bench, where the hidden pair runs a
  finite affine cat map whose path is fixed by its own past beyond a horizon (3.4). It is read by Bell's test across a
  pair, OWED: with settings independent of the hidden part, CHSH is at most 2 for any act, the pair's one hand
  included, and the owner's road (C) passes it only through a law of the seeds' joint measure, OPEN (7).
- **Not closed:**
  - the three clicks are not in node-all's act;
  - R4 is NOT READ;
  - the click world's geometry is OWED;
  - the key's scale and the generations are OPEN;
  - no exact energy is known;
  - whether a lay's orbit stays bounded is OPEN: confinement is periodicity, and nothing known forces it.

**In one sentence, with its three conditions:** within the width, on a lay whose lawful orbit stays there; on a cubic
O-invariant layout alike at every site; and with the fiber hidden from the board and carried in the record as board
fields: node-all's whole is one reversible, symmetric permutation of whole-number states, a deterministic board
carrying a finite fiber whose wrap counts are the clicks.

## 10. The owner's 07:30 word: the families, the algebra, and the order of the clocks' world

The owner's word, in the Boss's translation: "Are the families already in the code? The coupling family too? From the
optimization check you are doing, deduce which new algebra is more correct and how it actually orders the world of
clocks better." (09:1x, verbatim: "MATH3's section 10 goes to the owner with the batch, stating what is DERIVED and
MEASURED now and naming what a place of the click world is as the owner's question.") Each part is answered from the
code and the texts as they stand, with its standing.

### 10.1 Are the families in the code? The coupling family too?

Yes, as plans laid from the structure, at strengths the files choose (DERIVED as a reading of the code). In code
(load.py lines 193 to 214, plans.py), from the 24's tables:
- the metric family's push (plans.pushing), with load.geared's clocks' read into the teeth W and the grips' read;
- the volume's notch (plans.notching);
- the held hand's spring and tie (plans.holding), and the hands' tie (plans.tying);
- the gradient vertex through the Mesh (plans.meshing);
- term 11 on the edges and across the Meshes (plans.edging, plans.crossing).

The coupling family is in the code as that one plan: "no file declares a coupling; the coupling family's one plan lays
the terms at G3" (files.py RETIRED). One read is not lawful and is being moved (08:1x, verbatim): "The one place that
read a chosen value is plans.edging's lit(factor) (plans.py:75, with among and kappa following). There a strength of 0
would have set kappa, and with it the edge dial D and the births. Writer H moves it to the structural factor on
node-fold. Nothing moves on the shipped worlds but the click world's end line, which gains the 24 Mesh sides mesh 0
kills today, at their birth. The lawful state per Node-clock on the click world is then 97 (ALG1), not 85." The
shipped strengths (read from the five universe.json files; each OPEN with its provenance, AUDIT2 A1, in the owner's
batch):

| world | the files' chosen strengths |
|---|---|
| bang, live | all 0 (key 1) |
| mesh | hold 1, spring 10^8, mesh 250,000 (key 1) |
| click | hold 1, spring 10^8, tie 96,000 (key 50,811,429) |
| well | push 1, notch 120,000 (key 1) |

### 10.2 Which new algebra is more correct

- **DERIVED from 3.1 alone.** node-all's Omega carries each side's tooth independently, and the double
  k(u, t) = K - 1 - k(t, u) holds on every lay's orbit (3.1). So the complementary set, where it holds, is invariant,
  and the cochain form on the coupling complex (one tooth per edge) is the act restricted to that set: the same map
  there, by the sign law, with no compare needed (MATH3's mathematician, m2). Off that set (a one-side twin, S5b) the
  record would carry broken mates, which sides.paired refuses.
- **Minimal, as the count gives it.** On the complementary set the fiber is (Z/K)^E, one tooth per edge; no passing
  edge's tooth is a function of the others, since each turns by its own passing (3.1), and an edge that never passes
  keeps its tooth at birth, which MIN1's cut by structure removes. On the click world that is 3 own-edge and 12
  Mesh-edge teeth per Node-clock at 9d75a4904, against node-all's 175 side teeth. When lit(factor) moves (10.1), the
  click world gains its 24 Mesh sides at birth, and the lawful state per Node-clock is 97 (ALG1's count, 08:1x).
- **ALG1's measurement, unread by a pair:** its cochain act matches node-all's round by round with 0 entries off over
  100 rounds, the run back exact (S/alg1/out/compare_click_100.txt).

So it is not a new algebra: Z with Euclidean division, the shears, the cocycle and the boundary map B, carried on fewer
state elements. "More correct" can mean only that it carries no doubles. It is pending ALG1's pair and the D1 batch.

### 10.3 How it orders the clocks' world better

- **The order is the same in both forms.** On the complementary set the record is the same in both, so the meeting
  order it gives is the same (ALG1's compare reads the record's click lines alike). "Better" can only mean minimal.
- **The events are the decoder's (A4's shadow.met).** A meeting is one quantum given and taken (q -1 and +1) between
  two clocks, each carried on one edge to the other's train in its own site, with no other side carried there. A carry
  of |q| > 1 is no meeting of A4's; under the brief's "each event one quantum passing" it would be |q| events (MATH3's
  mathematician, m8). DECODE3f's ruling that a quantum across a Mesh is a meeting at neither place alone is in the
  owner's batch (08:4x: "To the owner's batch: DECODE3f's ruling that a Mesh meeting sits at neither place alone,
  beside his 'at one place'").
- **The meeting order (DERIVED).** Each clock (a site and a train) has a chain of its lines, ordered by their rounds;
  its several sides in one line sit at one point of the chain. A meeting joins its two clocks' points at that round.
  Taking the events within one round as incomparable, every generating relation raises the round, so the transitive
  closure is a strict partial order inside the round order (MATH2's mathematician, m1). "Meeting order" is exact.
- **What the click world's numbers are (08:5x, verbatim).** "Causal order in the click world is the order of chains of
  meetings that share a clock (the 07:5x rule). C1 reports the islands (the mesh world: 3 islands, the 114 / 62 / 187
  split; the click world: 27 islands of 3 clocks), with the one-step reading beside it, named one-step. The click
  world's '27 of 27' is forced by its alike lay. The board couples the sites on both worlds with no click (NATURE2's
  mathematician: one site's lay moves sites 12 and 14 from round 1), so '27 uncoupled copies' is struck and the gap is
  named on both worlds." So the click world's 27 of 27 is forced, not shown; the mesh world's NOT SHOWN (127 of 363)
  stands; and on both worlds the board couples sites with no click.
- **The owner's question, named (08:5x, verbatim):** "A mesh world 'place' pools clocks of different islands, so the
  texts' per-place counts there are per Node-clock, a board site. What a place of the click world is goes to the
  owner's batch with DECODE3f's Mesh meeting, the islands its stake."
- **What the order is not yet.** Each clock's own count (FACE2) and light's echo (LIGHT2) are not in the record, so its
  conversion to an observer's space and time is OWED (8.4).

### 10.4 Where this map and ALG1's books meet

ALG1 (S/alg1; S/alg1_frozen/ALG1.md unread by a pair) derives the act on the clocks' coupling complex as cochains.

- **The complex.** A place's own complex (its trains, the pairs a monomial joins, its triangles) is a 2-complex; the
  Mesh edges have one end at another place, so the complex with them is the board's, on the (site, train) clocks
  (MATH2's mathematician, m1). B C = 0 is classical; in node-all the books are B alone, and C is the bench's.
- **The fiber per edge.** ALG1's cochain act keeps one tooth per edge (10.2).
- **The books per clock.** K times a clock's clicks, against its swept passing, is B applied to the telescoping law per
  edge (3.1, 4.3); ALG1 reads it within a tooth over 200 rounds (books_click_L0_200.txt).
- **The cone is withdrawn (08:5x, verbatim: "ALG1's cone is withdrawn as a record item (08:4x); the place identity
  stands DERIVED at the place.").** The 08:4x law: "teeth sit only on edges between two clocks and on triangles of
  three clocks; no tooth sits on any cell joined to a non-clock; ... the record has two levels, lines and sides", and
  "ALG1's 3.5 cone (the tie's own cell) would be a fourth kind of event, so it is withdrawn as a record item". The
  residual "is stated at the place (the sum of D_i per monomial), not as a clock's share", and "'booked' can only mean
  removed (by an exact step, then a check by construction) or read by name, never put into a store" (08:4x). The place
  identity stands DERIVED at the place (a boundary sums to 0), with no cone line.

So the two meet at the boundary map B, and the skew product (the board reads no tooth) is what lets ALG1's cochain act
run beside step.act tooth for tooth.

### 10.5 The names of section 10, derived or asserted (MATH2's mathematician, m1; physicist, m5)

- Z with Euclidean division: DERIVED from the code (1.2, 1.3).
- The bijection: DERIVED (1.3 to 1.6). It is a bijection of Omega_inf, the states whose whole orbit stays lawful, not
  of the whole lawful lattice, which T leaves.
- <T, M>: of infinite order, DERIVED by the drift's induction (1.5), D1 its check; within the width, dihedral of order
  2n on each n-cycle.
- The space group: asserted for node-all by construction (5.2's reasons); the 24 of 24 are node-edge's and the bench's.
- The cocycle: DERIVED (3.1). The skew product is the group extension of the board by (Z/K)^E; the clicks are the
  integer parts of its cocycle.
- O and 2O: classical and read from kinds.py; the characters' orthogonality reading OWED; 2O rests on HALF2.
- Z[i]: a reading's algebra (CONF1), not the act's (6).

## 11. The probes (S/math2/probes/ and S/math3/probes/, on node-all 9d75a4904, its digest in the header; whole numbers, Rule3's carry the one division; nice 19, one process at a time, the load read before each, 6.8 to 8.0)

MATH4 runs no new probe (the owner's word of about 09:05); its folds are of standing. The shipped click world runs
3,751 of its declared 5,000 ticks (1.7); every click-world probe here set its own ticks.

- **MATH3's probes** (S/math3/probes/):
  - **cover.py and structure.py on the well world** (cover_well_10.txt, structure_well_6.txt): as in 1.3 and 2.2.
  - **cat3.py** (cat3_click_21.txt): G0 reads the click world's edges, triangle, C and G = C^T C = [[3]], the factor 3
    and the dial 457,302,861. A1, A2, M, the trace 38 and det 1 are computed from the read factor. K1 to K3 then match
    cat.py's, with K2 now read mod G. K3b: R^528,480's translation is linear in y, 11 of 11. K4 is 789 per mille from
    the read trace.
  - **record3.py** (record3_click_3.txt; its record and ledger in rec3/): R1, R2 and R3 as record.py's; R4 now an
    equality, 162 of 162 entries; R5, the ledger, 405 of 405 lines.
  - **drift.py** (drift_bang_30.txt): the bang world's layout with its wave row laid as a uniform drift (a test's lay,
    named so): the row at c + n + 1 after round n, 30 of 30, and the promise met before every round, 30 of 30. A check
    of 1.5's induction, not a proof of aperiodicity.
  - **On the well,** S5 to S7 are vacuous (key 1, no tooth moved); S1 to S4 read its moving parts.

- **structure.py** (MATH1's probe, copied unchanged) on the click world, 100 rounds (structure_click_100.txt, 90 s).
  - Its first line is "edge keys (distinct): [152434287]".
  - S1 to S7 hold in 100 of 100 rounds each. The net clicks, summed in absolute value over sides and sites, total 486.
  - Standing (MATH1 m1, ruling 6): S1, S4 and S6 are identities of the code. S5 and S7 hold by construction. S3 is the
    split's identity at W = rest. S2 and S3 are read on the rows the probe moved (12 and 20).
- **cover.py on the click world, 100 rounds** (cover_tensor24-click_100.txt): |W - rest| at most 0, |J5| at most 0, rd
  never moved, the odd rows 3 to 5 at 0, rows 12 and 20 move, and neither keeps its momentum sum.
- **cover.py on the bang world, 10 rounds** (cover_tensor24_10.txt): row 0 moves and keeps its momentum sum over the
  64 sites exactly, 10 of 10 rounds: an exact linear invariant.
- **record.py on the click world, 3 rounds** (record_click_3.txt, the record in probes/rec3/):
  - the header's dial 152,434,287 and birth 76,217,143, equal to the layout's;
  - x = K q + k_after - k_before equal to the act's passing on 324 of 324 listed sides;
  - no Mesh side carried (0 of 0);
  - the end line holds the teeth;
  - 162 click lines.
- **cat.py** (cat_21_file.txt; 0.5 s):
  - K1: the u row's second difference on N = 63 at y = 5, 6 and -4: {0} at the round's start, {18y} before the carry,
    {-18y} after it.
  - K2: v mod 3 kept and u mod 3 moved by y, 47,628 of 47,628 rounds.
  - K3, on the file's dial N = 457,302,861: M^528,480 = I; R^528,480 the identity at y = 3, 6 and 9, and a translation
    by D y at y = 1, 2 and 10; R^1,585,440 the identity at all six.
  - K4: 789 per mille.
- **MATH1's probes, cited and not rerun:** s5b (S/math1/probes/s5b_click_100.txt, on 48cd7fcf6, whose engine and runner
  9d75a4904 keeps), an off-lay reading (a one-side twin, 08:5x). The readers reran fiber.py and s5b byte for byte.
- **Twice.**
  - K1 agrees with the readers' catmap C3 and own_cat (their numbers on their dials).
  - K3 agrees with both readers' periods.
  - R2's 324 of 324 agrees with the physicist's own_record.
  - structure.py's S1 to S7 agree with MATH1's 300 rounds on 48cd7fcf6.
  - cover.py's rows agree with the mathematician's V1 to V4 (who adds row 14 at 300 rounds).
- **Provenance (MATH1 m12).** MATH1's frozen structure_click_300.txt predates the probe's added key line. Here every
  output was written by the probe file as it stands in S/math2/probes.

## 12. The folds: every item of both reports

### The mathematician (S/math1_math/REPORT.md)

| item | folded in | how |
|---|---|---|
| B1 | 3.4, 7, 8.3, 11 | +18y before the carry, -18y after it, 0 at the round's end; the period 528,480 if 3 divides y, else 1,585,440; floor(38a)/(38a) = 789 per mille; no bracket; MEASURED K1 to K4 |
| B2 | 3.2, 3.3, 7, 9 | the click a function of the board's history and the fiber point; the first click fixed by its side's past on a lay; the law of the path for every form; the choice the third click's, OWED |
| B3 | Summary, 2.2, 2.4 | "No exact energy is known"; Theorem A DRAFTED with its (H) and its drive exclusion; exact linear invariants (V5, and C5 here); OPEN with HAT4 |
| m1 | 1.3, 11 | push 0 on the shipped worlds; what moved and what did not; a lay with push 1 OWED |
| m2 | 1.5 | hypotheses (e), (f), (f') and (g) |
| m3 | 1.1, 1.3 | the loader's plans.pushing and load.geared cited |
| m4 | 1.3 | K2 a carry-shear |
| m5 | 1.3 | symplectic only where J5 = 0 and T_d = 1 |
| m6 | 1.7 | "stays lawful"; the finite set lawful and within the width |
| m7 | 3.1 | kappa / 2 by world; an even edge key possible; D's oddness OWED in code |
| m8 | 3.4 | L = I mod 3 (K2); F4 corroborates on N = 63 only |
| m9 | 5.2, 5.3 | 24 of 24 not mine on node-all; no turn negates a T_d > 1 row; the lay includes the layout |
| m10 | 9 | the cubic board; the bench's cat maps kept out of node-all's whole |
| m11 | 1.6 | R^2 = id needs T s in Omega; the shear form elsewhere |
| m12 | 11 | outputs rewritten by the probes as they stand |
| m13 | 8.4 | the Hauptvermutung, a conjecture |
| m14 | 2.4 | Mazur's 12 for one gear only |

### The physicist (S/math1_phys/REPORT.md)

| item | folded in | how |
|---|---|---|
| B1 | 3.1, 3.2, 7, 9 | the law of the path proved for every form; the two phrases struck; what the record writes, MEASURED R1 to R4 |
| B2 | 3.4, 7 | the finding against the bench form for the owner; the decoder's readings as listed; Bell's local bound and R4's two roads OPEN |
| B3 | 3.4 | the corrected constant, period and value |
| B4 | 8.3 | KEY2's point struck; the middle not chosen for its period; every horizon a function of the laid middle; KEY3 weighed |
| B5 | 9 | the paragraph says what its parts give; the sentence's three conditions |
| m1 | 0 | every "n/a" given its view or OWED |
| m2 | 0, 2.1, 2.2 | "deeper" OWED to the click world; W the recurrence's coefficient; the books per edge by construction |
| m3 | 1.7 | a board fact; "unbounded"; its click view OWED |
| m4 | 1.7 | decay recurs; R2 past a period; the fiber's periods; settings inside a closed whole |
| m5 | 8.4 | Malament replaced by the causal-set conjecture |
| m6 | 0 | the run back's click view is R1; "exact" a board comparison |
| m7 | 3.4 | F4 a board-informed reading; corroboration on one dial only |
| m8 | 3.4 | the shear's 3 is C^T C's diagonal; the steady y a stand-in |

The readers' questions to the Boss are answered by the coordinator's rulings 1 to 8. The two owner's questions are in
7 as (Q1) and (Q2).

## 13. What MATH3 replaces, and MATH2's items

Every replacement, by MATH2's line numbers; every other line is MATH2's, word for word
(S/math3/MATH2_to_MATH3.diff):

| MATH2 lines | what |
|---|---|
| 1 to 4 | title and date |
| 11 to 20 | what was read |
| 43 to 44 | summary: the law of the path |
| 47 to 48 | summary: the law's choice |
| 65 to 73 | summary: what the probes moved |
| 86 | table row: the teeth W |
| 87 | table row: the potential and the pull |
| 92 | table row: the run back |
| 96 | table row: the energy |
| 110 | table row: the choice |
| 113 | table row: the square-2 fall |
| 170 to 171 | 1.3: injective |
| 176 to 187 | 1.3: what the probes moved |
| 232 to 235 | 1.5: the corollary |
| 256 to 262 | 1.7: the click world and the record's period |
| 289 to 295 | 2.2: the linear invariants and the clock words |
| 327 | 2.4: Theorem B not leaned on |
| 360 to 373 | 3.1: what the record and the ledger write |
| 385 to 388 | 3.2: what it proves |
| 414 to 420 | 3.4: the factor read from C; the affine bijection |
| 447 to 448 | 3.4: the period for every y |
| 466 to 471 | 3.4: the finding against the bench form, in full |
| 476 to 477 | 3.5: affine bijection |
| 588 | 6: Z[i] |
| 602 to 604 | 7: the law of the path |
| 607 to 608 | 7: the law's choice |
| 613 to 614 | 7: what the record and the ledger write |
| 623 to 637 | 7: Bell as it stands now, and (Q2) with the ledger |
| 679 | 8.7: the odd rows' lay |
| 700 to 702 | 9: the choice |
| 711 to 713 | 9: the sentence |
| 715 to 776 | 10: the owner's three questions, in his words |
| 777 to 778 | 11: the probes' header |

### The mathematician on MATH2 (S/math2_math/REPORT.md)

| item | folded in | how |
|---|---|---|
| B1 | Summary, table row W, 1.3, 1.5, 8.7, 11 | the well shipped with push 1: W, J5, rd and the given-first rule move and S1 to S7 hold (MEASURED here too); the test's lay owed for the odd rows alone |
| B2 | Summary, 3.2, 7 | fiber dependence plus the factor; "different clicks" the initialization's (a key finer than the grain); it fails on the mesh world |
| B3 | 10 | the families and the coupling family from the code, with the shipped strengths; the cochain form the same map, minimal; "better" means minimal |
| B4 | 2.4 | Theorem B not leaned on; Northcott; MIRACLE_A's 128 bits by round 3 |
| m1 | 10.3, 10.4, 10.5, 1.5 | each name derived or asserted; Omega_inf; <T, M> infinite by D1; the place's complex without the Mesh edges; Z[i] a reading's; a strict partial order inside the round order; Mesh meetings DECODE3f's; "meeting order"; ALG1's measurement unread; the cone's c ALG1's choice |
| m2 | 3.4 | R^n linear in y, (D, 0) at y = 1 (K3b); the round's order, and an orbit's period divides it |
| m3 | 3.4, 11 | the factor and the dial read from C (cat3.py G0); K_F with shared edges |
| m4 | 7 | settings independent of the whole shared past state, board and fiber |
| m5 | 1.7 | the record's period the whole orbit's; the fiber's bound only at a steady passing |
| m6 | table row "the potential and the pull" | plans.meshing's two opposite-signed pushes cited |
| m7 | 3.1, 11 | R3 not read (0 of 0); R4 now an equality (162 of 162); R5 the ledger |
| m8 | 1.3, 3.4, 3.5 | "injective" in 1.3; "an affine bijection of (Z/N)^2" |

### The physicist on MATH2 (S/math2_phys/REPORT.md)

| item | folded in | how |
|---|---|---|
| B1 | 7, 9, Summary | Bell as it stands now: the bound, the owner's 08:00 word, road (C) chosen at 08:35 with its law OPEN, (A) and (B) the roads not taken, the clickless influence a gap and never a road |
| B2 | 10.3 | the second-road sentence struck; the mesh world's NOT SHOWN a hole OWED to be closed; events the decoder's (A4's met); DECODE3f's Mesh case; which order NATURE1 measures; a chain of lines |
| B3 | 3.4, 7 | the per-clock half concluded in full: if (Q1) is yes, the bench form does not meet it beyond its horizon, at every passing; the lag-two value as well; L4 |
| B4 | 9 | the sentence carries all three conditions in full |
| m1 | 2.2, table rows "the energy" and "the square-2 fall" | the clock words named once; no conservation in the click world derived |
| m2 | 3.1, 7 | the ledger named in what the record writes (MEASURED R5) and in (Q2) |
| m3 | 3.4, 11 | cat3.py reads G from C |
| m4 | 3.4 | the finding a board check beside a click reading, its click-only form OWED |
| m5 | 10.5 | the skew product is the group extension; the clicks its cocycle's integer parts |
| m6 | 1.7 | a departed run writes no record; a written one says nothing past its ticks |
| m7 | 10 | the owner's words, in the Boss's translation, answered part by part |

## 14. What MATH4 replaces, and MATH3's items

Every replacement, by MATH3's line numbers; every other line is MATH3's, word for word (S/math4/MATH3_to_MATH4.diff):

| MATH3 lines | what |
|---|---|
| 1 to 11 | title, date and the tree's digest |
| 13 to 27 | what was read |
| 50 to 53 | summary: the law of the path and the seed test |
| 56 to 60 | summary: the law's choice and the record's teeth |
| 70 to 71 | summary: the energy |
| 75 to 87 | summary: what the probes moved |
| 97 | table row: the split |
| 106 to 107 | table rows: the run back; the law of the path and the seed test |
| 110 | table row: the energy |
| 112 | table row: the passing |
| 117 | table row: the books |
| 123 to 125 | table rows: the record, the choice, the click world's order |
| 249 to 253 | 1.5: the corollary, the drift DERIVED |
| 281 to 283 | 1.7: a departed run, and the click world's ticks |
| 321 to 331 | 2.2: the energy's standing and the books in the clicks |
| 347 to 356 | 2.4: road A classical only; road B as read |
| 393 to 404 | 3.1: the record's teeth, board fields and board checks |
| 414 to 428 | 3.2: S7 by construction; the law of the path; the seed test |
| 509 to 512 | 3.4: the place's sides' past |
| 566 to 568 | 4.3: the guard's reach |
| 656 to 659 | 7: the law of the path and the seed test |
| 669 to 671 | 7: what the record writes |
| 676 | 7: R2 in each clock's own count, and the ladder |
| 680 to 706 | 7: Bell as it stands now; (Q1) and (Q2) with their stakes |
| 719 to 720 | 8.2: the miracle's standing |
| 754 | 8.7: Theorem A's standing |
| 767 | 9: the fiber's place |
| 769 to 772 | 9: the choice |
| 781 to 784 | 9: the sentence |
| 786 to 879 | 10: for the owner's batch, with what a place is as his question |
| 881 to 883 | 11: the probes' header |
| 891 to 892 | 11: drift as a check |
| 916 to 917 | 11: s5b off-lay |

### The mathematician on MATH3 (S/math3_math/REPORT.md)

| item | met in | how |
|---|---|---|
| B1 | Summary, table row "the energy", 2.2, 2.4, 8.2, 8.7 | road A keeps only the classical one-gear statement; the coupled rational exactness cited only as MIRACLE_A's claim, not passed, nothing leaning on it; Theorem A's standing NOT PASSED by both (09:0x), with (D) and (H) stated |
| B2 | 10.4 | ALG1's cone withdrawn as a record item (08:4x, 08:5x quoted); the place identity DERIVED at the place, no cone line |
| m1 | 1.5, table row "the run back", 10.5, 11 | the drift's infinite order DERIVED by the three-line induction; D1 its check |
| m2 | 3.2, 10.2 | the cochain form the act on the complementary set, DERIVED from 3.1; S5b off that set (off-lay); the twin moves both sides; minimal from E independent teeth |
| m3 | 10.1, 10.2 | lit(factor) moving to the structural factor (08:1x quoted); the click world gains its 24 Mesh sides; 97 per Node-clock |
| m4 | 7, 9 | Bell from the 08:4x and 08:5x rulings, quoted |
| m5 | Summary, 11 | the well's S5 to S7 vacuous; it reads S1 to S4 |
| m6 | table row "the record" | board checks R1, R2, R4 and R5 |
| m7 | 3.4 | "the place's sides' past fixes every later side"; F4 read only W |
| m8 | 10.3 | a carry of more than one quantum is no meeting of A4's, or that many events; DECODE3f's Mesh meeting in the owner's batch (08:4x quoted) |

### The physicist on MATH3 (S/math3_phys/REPORT.md)

| item | met in | how |
|---|---|---|
| B1 | 7, 9, Summary | Bell restated from 08:4x and 08:5x verbatim: any act; (A)'s channel breaks the law of the path; the clickless influence is measurement dependence; (C)'s law of the seeds' joint measure OPEN and covariant, its place OPEN; the local control; R4 under (C) with (b) replaced; every Bell number's settings named |
| B2 | Summary, 3.1, 7, table rows "the split", "the passing" and "the record" | the teeth as board fields carried for the checks; the click world reads lines and sides alone; a passing through the teeth a board check (08:5x quoted); (Q2) with its two-case stake and the owner's 09:05 word |
| B3 | Summary, 3.2, 7, table row "the law of the path", 11 | S5b and S5 off-lay readings, not MEASURED; the twin moves an edge's tooth on both sides; (ii) NOT SHOWN by structure on the first click, showable only at the member; the unit the owner's; the key remedy withdrawn |
| B4 | 10.3, 10.4, table row "the click world's order" | 27 of 27 forced by the alike lay; the islands named on both worlds; the clickless board coupling on both; the cone withdrawn; section 10 for the owner's batch, with what a place is as his question (09:1x quoted) |
| m1 | 2.2, 2.4, 8.2, 8.7, table row "the energy" | MIRACLE_A NOT PASSED by both; the coupled exactness only as its claim |
| m2 | 2.4 | road B as 08:5x has it: exact, time-symmetric, no energy kept exactly in whole numbers, its clicks the two-leg passing, its walk MEASURED with no bound, D not closed |
| m3 | Summary, 1.7, 11 | the click world's 3,751 of 5,000 ticks named (08:5x quoted) |
| m4 | 4.3, table row "the books" | the guard's reach named (08:5x quoted) |
| m5 | the header | the tree's commit and both archive digests; a real copy, no symlink (09:1x quoted) |
| m6 | Summary, 1.5, 11 | the well's S5 to S7 vacuous; D1's "forever" DERIVED, its 30 rounds a check |

