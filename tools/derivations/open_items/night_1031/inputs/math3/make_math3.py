"""Build MATH3.md from MATH2.md by replacing only named line ranges (MATH2's numbering), bottom up, and appending the
new sections. Run once: python3 -I make_math3.py"""

from pathlib import Path

S = Path("S")
src = S.joinpath("math2", "MATH2.md").read_text(encoding="utf-8").split("\n")
R = []  # (first, last, why, new text)


def rep(first, last, why, text):
    R.append((first, last, why, text.rstrip("\n")))


rep(1, 4, "title and date", """# MATH3: the mathematics of the whole system, on node-all 9d75a4904 (MATH2 with both readers' MATH2 items folded)

MATH3, for the Boss, 2026-10-31, 08:4x UTC. Read only: nothing in /home/user/Universe24 was checked out, edited or
committed. S is S. MATH3 is MATH2
with only the lines named in section 13 replaced (MATH2's line numbers); every other line is MATH2's, word for word.
The diff is S/math3/MATH2_to_MATH3.diff.""")

rep(11, 20, "what was read", """**What was read.**
- MATH1's two reports, S/math1_math/REPORT.md (3 BLOCKING, 14 MINOR) and S/math1_phys/REPORT.md (5 BLOCKING, 8
  MINOR), whole.
- MATH2's two reports, S/math2_math/REPORT.md (4 BLOCKING, 8 MINOR) and S/math2_phys/REPORT.md (4 BLOCKING, 7 MINOR),
  whole.
- The Boss's rulings of 07:5x UTC, both parts, and of 08:1x UTC (the last sections of S/BRIEF_PAIRS.md, with the push
  sentence corrected at 08:3x); the coordinator's eight rulings on MATH1 and nine on MATH2; and the owner's choice of
  road (C) at about 08:35 UTC ("8: C. Big Pic builds."; #2187 6541185833).
- S/key3_phys/REPORT.md (verdict and B1); S/third8_frozen/THIRD8.md (its lines on Big Pic's #2187 6540860812 and the
  fork).
- ALG1's probe and outputs (S/alg1/probes/cochain.py; S/alg1/out/compare_click_100.txt and books_click_L0_200.txt).
- node-all's record/schema.py (Click, Header, End), run.clicked, run.counts and run.teeth_of; load.py lines 193 to 214;
  plans.py's plan functions; files.py's RETIRED; the five worlds' universe.json.

Each item a reader raised is folded where it belongs: MATH1's in section 12, MATH2's in section 13.""")

rep(43, 44, "summary: the law of the path", """- **The law of the path, for every click form.** 3.1 and 3.2 prove fiber dependence and the factor: the clicks are a
  function of the board's history and the fiber point, and the board does not depend on the fiber, so seeds one tooth
  apart reach one board. "Different clicks" from them is the initialization's: it needs a key finer than the
  passings' grain (the owner's batch), and it fails on the mesh world, whose key 3 divides every passing.""")

rep(47, 48, "summary: the law's choice", """- **The law's choice.** It belongs to the third click, which is on Big Pic's bench only. It is read by Bell's test
  across a pair, OWED, on the road the owner chose at about 08:35, (C): the settings and the hand meet through the
  seeds, by a law not yet shown (OPEN). It is no theorem of node-all's act.""")

rep(65, 73, "summary: what the probes moved", """MEASURED, on what the probes moved:
- on rows 12 and 20 of the click world over 100 rounds, and on the well world (shipped with push 1) over 6 rounds,
  where W, J5, the drive's fine tooth and the given-first rule all move: the mirror is an involution, M o T is an
  involution, the momentum identity holds, the board is blind to the teeth, and the cocycle holds;
- on row 0 of the bang world, and rows 0 and 12 of the well, the momentum sum over the sites is kept exactly, a linear
  invariant;
- the record's x = K q + k_after - k_before equals the act's passing on 324 of 324 sides, the end teeth equal the
  act's on 162 of 162 entries, and the ledger's counts equal the act's on 405 of 405 lines;
- the cat map's factor and dial are read from the structure (G = C^T C = 3); its constants and its mod-3 law hold on
  N = 63, and its two periods on the file's dial, with R^n linear in y (11 of 11).

Only the mirror's odd-row half is read by no shipped world: the 0i rows stay 0 on all five. A test's lay is OWED for
the odd rows alone.""")

rep(86, 86, "table row: the teeth W", """| the teeth W (T2) | a whole polynomial map of the counts, read given first (the loader's rule) | how much a gear carries in a turn | proper time OWED (D6, FACE2); "a deeper clock counts less" is the click world's word, OWED there | DERIVED (code, load.geared); W = rest on four shipped worlds, and W moves on the well (MEASURED C1: up to 1,248 off rest) |""")

rep(87, 87, "table row: the potential and the pull", """| the potential and the pull (T4, T6, M4) | a whole polynomial V on the readings; J = -dV/da by construction (contract.pushes; for the gradient vertex, plans.meshing's two opposite-signed pushes, summation by parts) | springs, vertices, the Meshes' tug | the rest beat as a mass OWED (reading 8) | DERIVED |""")

rep(92, 92, "table row: the run back", """| the run back (B1) | M T M = T^-1; T = M o (M o T); <T, M> of infinite order (one aperiodic lawful orbit, D1), dihedral of order 2n on an n-cycle | the same act on the mirrored state | the two-record comparison R1; the end line's "exact" is a board comparison printed into the record | DERIVED (1.5); MEASURED S2 (click and well), D1 |""")

rep(96, 96, "table row: the energy", """| the energy (a clock word: the board map's quadratic forms) | no exact energy known; exact linear invariants exist (2.2) | not kept | the books are counts of quanta, closed per edge by construction; no conservation in the click world is derived | OPEN, with HAT4; Theorem A DRAFTED, no reader |""")

rep(110, 110, "table row: the choice", """| the choice (the law of the choice) | the third click's path (bench); not a theorem of node-all's act | the triangle's hidden pair | Bell across a pair on road (C), by a law OPEN; R4 OWED; two questions to the owner (7) | OPEN |""")

rep(113, 113, "table row: the square-2 fall", """| the square-2 fall | an indefinite V along x_g = -x_t; a growing orbit, so not periodic | a tied pair's counts grow together (a clock fact) | a runaway writes no record; its view OWED | OPEN (8.1) |""")

rep(170, 171, "1.3: injective", """So B = D2 o D1 o K2 o K1. Each factor has an inverse of its own form, so B is injective wherever W(a), W(b) and
W(a+) are at least 1, and a bijection onto its image (DERIVED). The given-first rule and hypothesis (d) make the
composite triangular; both are the""")

rep(176, 187, "1.3: what the probes moved", """**What the probes moved (MATH1 m1; the coordinator's rulings 6 and, for MATH3, 1).** Four shipped worlds have push 0;
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
0i rows are 0 on all five): a test's lay is OWED for the odd rows alone.""")

rep(232, 235, "1.5: the corollary", """**Corollary.** R = M o T is an involution, so T = M o R is a product of two involutions. <T, M> has infinite order: the
bang world's layout with its wave row laid as a uniform drift (a test's lay, named so) runs lawfully, the row at
c + n + 1 after round n, 30 of 30 rounds (MEASURED D1, S/math3/probes/drift_bang_30.txt), an orbit that is not
periodic. On a cycle of length n, within the width, the group is dihedral of order 2n. The even reversors
T^(2i) M = T^i M T^-i are conjugate to the fixed-point-free M, so any state fixed by a reversor is fixed by an odd one.
MEASURED S2: R(R(s)) = s in every field, k included, 100 of 100 rounds on the click world and 6 of 6 on the well.""")

rep(256, 262, "1.7: the click world and the record's period", """- **In the click world (the physicist's m4).** The record of a closed orbit is purely periodic, so every decay recurs.
  A decay law (geometric lives) can hold only on records short beside the period, and R2 read past one period reads
  repetition. The record's period is the whole orbit's, board and fiber together (MATH2's mathematician, m5). At a
  steady passing the fiber's periods bound the within-record readings: K / gcd(P, K) at the first click, and 528,480 or
  1,585,440 at the third (3.4); Big Pic's 1,000,000 rounds are 1.89 of the shorter. Under a varying passing no fiber
  period bounds them. Bell's settings drawn inside a closed whole are functions of the whole state.
- The confinement's click-world view is OWED by name. run.run writes the record only after the last round, so a run
  that departs writes no record at all: a written record shows that its run stayed lawful and within the width for its
  ticks, and says nothing beyond them (MATH2's physicist, m6).""")

rep(289, 295, "2.2: the linear invariants and the clock words", """- **On the words (MATH2's physicist, m1).** Here "energy", "momentum" (the edge's p), "work" (a term's push times a
  move) and "falls" name clock quantities of the board map. No conservation of energy or momentum in the click world is
  derived.
- **Exact linear invariants exist (DERIVED, MEASURED).** On a row whose push is the Meshes' pull alone, the sum over
  the sites of p is kept exactly: the pull is alike from both ends of every Mesh, so it sums to 0 over the board.
  - MEASURED (cover_tensor24_10.txt): row 0 of the bang world moves and keeps its sum in every round of its 10.
  - MEASURED (S/math3/probes/cover_well_10.txt): rows 0 and 12 of the well keep theirs in 10 of 10 rounds; rows 2 and
    6 to 8, the metric's 00 and ii slots, which the push lands on, do not.
  - The mathematician's V5 has the same as the bang over 200 rounds with every strength 0.
  - On the click world the moving rows 12 and 20 do not keep theirs; they carry on-site terms.
- **Also kept:** the step's law p+ = p + 4 push, a lay's invariant subspaces, and the lay's stabilizer (5.3).""")

rep(327, 327, "2.4: Theorem B not leaned on", """  - A rational orbit that is not periodic has unbounded height (Northcott). MIRACLE_A measured its lay's numbers past
    128 bits by round 3. Theorem B is not leaned on.""")

rep(360, 373, "3.1: what the record and the ledger write", """**What the 1.4 record writes (the coordinator's ruling 2), and the ledger beside it.**
- the header's dial (the edge key K) and birth (every tooth's birth, (K - 1) div senses);
- every click line's sides as [u, q_tu, k_before, k_after], and across each Mesh [u, place, q, before, after];
- the end line's teeth (record/schema.py, run.clicked, run.teeth_of);
- the ledger beside the record (run.counts): every train's now counts at every Node-clock in every round (MATH2's
  physicist, m2). The decoder reads its lines (decoder/records.py).

So x = K q_tu + k_after - k_before is the side's exact passing, read from the record alone. MEASURED (record3.py,
S/math3/probes/record3_click_3.txt; 3 rounds of the click world written by the tree's own runner into my folder):
- R1: the header's dial is 152,434,287 and its birth 76,217,143, equal to the layout's key and the lay's teeth;
- R2: x equals the act's own passing on 324 of 324 listed sides;
- R3: no Mesh side carried in those rounds (0 of 0), so the across form is not read;
- R4: the end line's teeth equal the act's end teeth on 162 of 162 entries (6 own-edge sides at 27 sites; no Mesh
  side carried);
- R5: the ledger's 405 Count lines each equal the act's now counts of their train, site and round, 405 of 405.

The physicist measured the same 324 of 324. So the click world holds the fiber and the board's exact passing, and with
the ledger the decoder holds the board's counts too: any reading that uses the ledger is a board check. "Hidden"
means hidden from the board: no board coordinate reads a tooth.""")

rep(385, 388, "3.2: what it proves", """**What it proves (the coordinator's ruling 2 on MATH1 and on MATH2).** 3.1 and 3.2 prove fiber dependence and the factor:
the clicks are a function of the board's history and the fiber point, and the board does not depend on the fiber. So
two seeds alike on the board and one tooth apart reach one board. Their clicks differ only where some side's running
sum k_0 + S_n Phi is carried differently, which no theorem gives (MATH2's mathematician, B2). "Different clicks" is
the initialization's: it needs a key finer than the passings' grain, already in the owner's batch. It fails on a
shipped world: the mesh world's key 3 divides every passing, so q = P / 3 whatever the tooth, and seeds alike on the
board write identical clicks forever. The law's "the path of the clicks is not [deterministic]" reads here as "not a
function of the board", which is the factor (the physicist's B1(d)).""")

rep(414, 420, "3.4: the factor read from C; the affine bijection", """and the landing W is the number of wraps of tau when y is added. The shear's factor and the dial are read from the
structure, not typed (MATH2's mathematician m3, physicist m3): cat3.py takes the click world's edges at one Node-clock
from the layout's click plan (run.joined), (2, 3), (2, 4) and (3, 4), its one triangle (2, 3, 4), C = (1, -1, 1) and
G = C^T C = [[3]]. The factor is G's diagonal, 3, and the dial N = G D = 457,302,861 (MEASURED G0,
S/math3/probes/cat3_click_21.txt). That holds on a lone triangle; with shared edges the shears go by K_F = C^T C,
which is not 3 I. The passings y in my probes are stand-ins, and F4 and K1 to K3 read them, so they are board-informed
readings (the physicist's m7).

- **The matrix.** A2 A1 = [[19, 6], [60, 19]], and A1 A2 = [[19, 60], [6, 19]] = L between two rounds' carries. Trace
  38, determinant 1, so L^2 = 38 L - I. L is a hyperbolic element of SL(2, Z), Arnold's cat-map family. The round is an
  affine bijection of (Z/N)^2 for every y (F3).""")

rep(447, 448, "3.4: the period for every y", """  Any period P has M^P = I, so n divides P, and P divides 3n. R^n is the translation by S_n A2 (y, 0), with S_n the
  sum of M's first n powers; it is linear in y, and at y = 1 it is (D, 0). So R^n is the identity exactly when 3
  divides y (MEASURED K3b: R^n's translation at y is y times its translation at 1, 11 of 11 for y = 2 to 12). The
  round's order is therefore **528,480 when 3 divides y, else 1,585,440** (DERIVED from K3 and K3b), and an orbit's
  period divides it (MATH2's mathematician, m2).""")

rep(466, 471, "3.4: the finding against the bench form, in full", """- **A finding against the bench form, for the owner (the physicist's B2(a); MATH2's physicist, B3 and m4).**
  - DERIVED: for every passing sequence, the partition of the fiber by landing words refines at most |fiber| - 1
    times, so beyond a finite horizon (which depends on the passings) a triangle's sides' past fixes every later
    landing. At a steady passing, once a past of length n fixes the next landing, it fixes every later one (the map is
    the same each round).
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
    line 35 (17)).""")

rep(476, 477, "3.5: affine bijection", """  a bijection for every board point (a rotation; an affine bijection whose linear part has determinant 1), so the
  skew product is a bijection with no condition on the passing (DERIVED). The clicks are q = Q + C W.""")

rep(588, 588, "6: Z[i]", """- **Z[i].** The algebra of a reading (CONF1's Gaussian hands and norms), not of the act: the act never multiplies by
  i, and at spring 10^8 the held hand no longer turns a quarter (NOT_CLOSED 37) (MATH2's mathematician, m1).""")

rep(602, 604, "7: the law of the path", """- **The law of the path holds for every click form** (3.1, 3.2; the coordinator's ruling 2 on MATH1 and on MATH2).
  The clicks are a function of the board's history and the fiber point, and the board does not depend on the fiber,
  so seeds one tooth apart reach one board (DERIVED; MEASURED S5b, S7). "Different clicks" is the initialization's,
  needing a key finer than the passings' grain (the owner's batch); it fails on the mesh world.""")

rep(613, 614, "7: what the record and the ledger write", """- **What the record writes:** the dial, the birth, each side's k_before and k_after, and the end teeth (3.1); the
  ledger beside it writes every train's now counts. So the click world holds the fiber and the exact passing, and with
  the ledger the board's counts: a reading that uses the ledger is a board check.""")

rep(607, 608, "7: the law's choice", """- **The law's choice is the third click's.** It is on the bench only (mode 11), read by Bell's test across a pair on
  road (C), and OWED. It is not a theorem of node-all's act, which has no third click. If the owner answers (Q1) yes,
  the bench form does not meet the per-clock half beyond its horizon, at every passing (3.4).""")

rep(623, 637, "7: Bell as it stands now, and (Q2) with the ledger", """- **Bell, as it stands now** (the owner's word of about 08:00 UTC, "Bell is in the clicks, not on the board": settings,
  outcomes and pairs are clicks; his choice at about 08:35 UTC, "8: C. Big Pic builds.", #2187 6541185833; Big Pic's
  #2187 6540860812, through THIRD8).
  - **The bound (DERIVED; Bell 1964, CHSH 1969).** Every local form gives CHSH at most 2 for separated wings with
    settings independent of the whole shared past state, board and fiber (MATH2's mathematician, m4). That is the
    owner's own bound, "set by its own past alone". node-all's act is local: a Node-clock reads its gears and its six
    Meshes' neighbours once a round, no triangle spans two sites, and mode 11 reads no setting. Big Pic's copies world
    (copies of the hand carried by the board's own act, each place reading its own setting) reads at most 2, as his.
  - **Road (C), the owner's choice.** The settings and the hand meet through the seeds: the start's shared past, or,
    by the law of the path, the end. (C) passes the bound only through that dependence, and only by a law:
    - the correlation must come from a law, never from a seed laid by hand for the outcome (Form 4);
    - no law is yet shown to give nature's pattern;
    - the test must be one that can fail.

    Big Pic derived that laying the end freely reads at most 2 (his). So (C) needs a law that fixes the seeds' measure
    with nothing picked. That law is OPEN: it is the measurement dependence, by name.
  - **The roads not taken.** (A), the pair's one hand read at both places' clicks: at separated places a change to the
    locality law, the owner's to make. (B), copies carried by the board: bounded at 2 by the bound.
  - **A clickless board influence** is a gap in R4's order reading, to be closed, never a road. The mesh world's NOT
    SHOWN (10.3) is such a gap.
  - CHSH alone passes no choice: PICTURE.md section 4 records the first click with no draw at 2,499 per mille. Big Pic
    writes that his toy's 2,501 rested on a read of the far setting (#2187 6540860812; struck as evidence). The
    owner's toy's 2.82 is the owner's. R4 is NOT READ until the record names the pair event.
- **Two questions for the owner's batch, through the Boss** (named, not answered):
  - **(Q1)** Are a clock's sides, and its past board readings, "what a clock can read"?
  - **(Q2)** Does the record keep writing the teeth (k_before, k_after, the birth and the end teeth), and the ledger
    the board's counts beside it?""")

rep(679, 679, "8.7: the odd rows' lay", """   - A test's lay for the mirror's odd-row half alone (1.3), OWED.""")

rep(700, 702, "9: the choice", """- **The choice** the owner's law names lives at the third click. That is Big Pic's bench, where the hidden pair runs a
  finite affine cat map whose path is fixed by its own past beyond a horizon (3.4). It is read by Bell's test across a
  pair, OWED: every local form with settings independent of the whole shared past reads at most 2, and the owner's road
  (C) passes it only through measurement dependence by a law, which is OPEN (7).""")

rep(711, 713, "9: the sentence", """**In one sentence, with its three conditions:** within the width, on a lay whose lawful orbit stays there; on a cubic
O-invariant layout alike at every site; and with the fiber hidden from the board and written into the record:
node-all's whole is one reversible, symmetric permutation of whole-number states, a deterministic board carrying a
finite fiber whose wrap counts are the clicks.""")

rep(715, 776, "10: the owner's three questions, in his words", """## 10. The owner's 07:30 word: the families, the algebra, and the order of the clocks' world

The owner's word, in the Boss's translation: "Are the families already in the code? The coupling family too? From the
optimization check you are doing, deduce which new algebra is more correct and how it actually orders the world of
clocks better." Each of its three parts is answered here from the code and the texts as they stand (MATH2's
mathematician, B3; physicist, m7).

### 10.1 Are the families in the code? The coupling family too?

Yes, as plans laid from the structure, at strengths the files choose. In code (load.py lines 193 to 214, plans.py),
from the 24's tables:
- the metric family's push (plans.pushing), with load.geared's clocks' read into the teeth W and the grips' read;
- the volume's notch (plans.notching);
- the held hand's spring and tie (plans.holding), and the hands' tie (plans.tying);
- the gradient vertex through the Mesh (plans.meshing);
- term 11 on the edges and across the Meshes (plans.edging, plans.crossing).

The coupling family is in the code as that one plan: "no file declares a coupling; the coupling family's one plan lays
the terms at G3" (files.py RETIRED). The shipped strengths (read from the five universe.json files; each OPEN with its
provenance, AUDIT2 A1, in the owner's batch):

| world | the files' chosen strengths |
|---|---|
| bang, live | all 0 (key 1) |
| mesh | hold 1, spring 10^8, mesh 250,000 (key 1) |
| click | hold 1, spring 10^8, tie 96,000 (key 50,811,429) |
| well | push 1, notch 120,000 (key 1) |

### 10.2 Which new algebra is more correct

The deduction the materials support: the cochain form on the coupling complex (ALG1) is the same map as node-all's
act, minimal, pending ALG1's pair and the D1 batch. The materials:
- one tooth per edge suffices: 3 own-edge and 12 Mesh-edge teeth per Node-clock on the click world, against node-all's
  175 side teeth (ALG1's count, unread by a pair);
- the second side tooth is a double, k(u, t) = K - 1 - k(t, u) forever (3.1, DERIVED; MIN1's D1, in the owner's batch);
- ALG1's cochain act matches node-all's round by round with 0 entries off over 100 rounds, the run back exact
  (S/alg1/out/compare_click_100.txt; ALG1's measurement, unread by a pair).

So it is not a new algebra. It is the same: Z with Euclidean division, the shears, the cocycle and the boundary map B,
carried on fewer state elements and terms. "More correct" can mean only that it carries no doubles.

### 10.3 How it orders the clocks' world better

- **The order is the same in both forms.** The record is the same in both (ALG1's compare: 0 click entries off, the
  record's click lines alike), so the meeting order it gives is the same. "Better" can only mean minimal.
- **The events are the decoder's (A4's shadow.met; the coordinator's ruling 6 for MATH3).** A meeting is one quantum
  given and taken (q -1 and +1) between two clocks, each carried on one edge to the other's train in its own site,
  with no other side carried there. Under the brief's "each event one quantum passing", a carry of |q| > 1 is not one
  meeting. A quantum across a Mesh is ruled by DECODE3f a meeting across the Mesh, at neither place alone, pending its
  pair.
- **The meeting order (DERIVED).** Each clock (a site and a train) has a chain of its lines, ordered by their rounds;
  its several sides in one line sit at one point of the chain. A meeting joins its two clocks' points at that round.
  Take the events within one round as incomparable: then every generating relation raises the round, so the transitive
  closure is a strict partial order inside the round order (MATH2's mathematician, m1). "Causal" is a name for it
  only; "meeting order" is exact.
- **Which order NATURE1's numbers measure.** NATURE1 reads each later clock's first event against a chain of meetings
  reaching it, reading causes through the across sides as well (MATH2's physicist, B2(b)): the meeting order with the
  Mesh's meetings included, DECODE3f's case, and not the order itself. On the click world it is SHOWN, 27 of 27. On the
  mesh world it is NOT SHOWN, 127 of 363 later clocks uncaused: later clocks move with no chain of meetings, because
  the board's wave carries influence with no click. That is a hole in the record's causal order, OWED to be closed.
- **What the order is not yet.** Each clock's own count (FACE2) and light's echo (LIGHT2) are not in the record, so its
  conversion to an observer's space and time is OWED (8.4).

### 10.4 Where this map and ALG1's books meet

ALG1 (S/alg1; S/alg1_frozen/ALG1.md unread by a pair) derives the act on the clocks' coupling complex as cochains.

- **The complex.** A place's own complex (its trains, the pairs a monomial joins, its triangles) is a 2-complex; the
  Mesh edges have one end at another place, so the complex with them is the board's, on the (site, train) clocks
  (MATH2's mathematician, m1). B C = 0 is classical; in node-all the books are B alone, and C is the bench's.
- **The fiber per edge.** ALG1's cochain act keeps one tooth per edge and matches node-all's: 3.1's fiber (Z/K)^E,
  measured by ALG1, unread by a pair.
- **The books per clock.** Its "K booked - swept at a clock (David's identity, the teeth's part)" is B applied to the
  telescoping law per edge (3.1, 4.3); ALG1 reads it within a tooth over 200 rounds (books_click_L0_200.txt).
- **The cone.** ALG1 adds one cone edge per coupled clock, booking the share of a clock's work that no clock-pair
  carries: the cone over the place's own complex. A clock's own work w then splits as w = B x + c with c on the cone
  edges. The split is not unique; c is ALG1's choice (MATH2's mathematician, m1). The cone vertex's line is the place's
  net, the place identity of the Boss's 07:5x ruling.

So the two meet at the boundary map B, and the skew product (the board reads no tooth) is what lets ALG1's cochain act
run beside step.act tooth for tooth.

### 10.5 The names of section 10, derived or asserted (MATH2's mathematician, m1; physicist, m5)

- Z with Euclidean division: DERIVED from the code (1.2, 1.3).
- The bijection: DERIVED (1.3 to 1.6). It is a bijection of Omega_inf, the states whose whole orbit stays lawful, not
  of the whole lawful lattice, which T leaves.
- <T, M>: of infinite order by D1's aperiodic lawful orbit (a test's lay, MEASURED); within the width, dihedral of order
  2n on each n-cycle.
- The space group: asserted for node-all by construction (5.2's reasons); the 24 of 24 are node-edge's and the bench's.
- The cocycle: DERIVED (3.1). The skew product is the group extension of the board by (Z/K)^E; the clicks are the
  integer parts of its cocycle.
- O and 2O: classical and read from kinds.py; the characters' orthogonality reading OWED; 2O rests on HALF2.
- Z[i]: a reading's algebra (CONF1), not the act's (6).""")

rep(777, 778, "11: the probes' header", """
## 11. The probes (S/math2/probes/ and S/math3/probes/, on node-all 9d75a4904; whole numbers, Rule3's carry the one division; nice 19, one process at a time, the load read before each, 6.8 to 8.0)

- **MATH3's probes** (S/math3/probes/):
  - **cover.py and structure.py on the well world** (cover_well_10.txt, structure_well_6.txt): as in 1.3 and 2.2.
  - **cat3.py** (cat3_click_21.txt): G0 reads the click world's edges, triangle, C and G = C^T C = [[3]], the factor 3
    and the dial 457,302,861. A1, A2, M, the trace 38 and det 1 are computed from the read factor. K1 to K3 then match
    cat.py's, with K2 now read mod G. K3b: R^528,480's translation is linear in y, 11 of 11. K4 is 789 per mille from
    the read trace.
  - **record3.py** (record3_click_3.txt; its record and ledger in rec3/): R1, R2 and R3 as record.py's; R4 now an
    equality, 162 of 162 entries; R5, the ledger, 405 of 405 lines.
  - **drift.py** (drift_bang_30.txt): the bang world's layout with its wave row laid as a uniform drift (a test's lay,
    named so): the row at c + n + 1 after round n, 30 of 30, and the promise met before every round, 30 of 30.""")

# the closing lines of section 12 (MATH2 855 to 856) are kept; section 13 follows them
out = list(src)
for first, last, why, text in sorted(R, key=lambda x: -x[0]):
    out[first - 1:last] = text.split("\n")

section13 = """

## 13. What MATH3 replaces, and MATH2's items

Every replacement, by MATH2's line numbers; every other line is MATH2's, word for word
(S/math3/MATH2_to_MATH3.diff):

| MATH2 lines | what |
|---|---|
""" + "\n".join(f"| {a} to {b} | {why} |" if a != b else f"| {a} | {why} |" for a, b, why, _ in sorted(R, key=lambda x: x[0])) + """

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
"""
text = "\n".join(out).rstrip("\n") + section13
S.joinpath("math3", "MATH3.md").write_text(text + "\n", encoding="utf-8")
print("replacements:", len(R), "lines:", len(text.split("\n")))
