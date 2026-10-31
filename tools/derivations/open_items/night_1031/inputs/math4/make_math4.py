"""Build MATH4.md from MATH3.md (frozen, sha256 6e9a9cd0...c2b7) by replacing only named line ranges (MATH3's
numbering), bottom up, and appending section 14. Run once: python3 -I make_math4.py"""

import hashlib
from pathlib import Path

S = Path("S")
raw = S.joinpath("math3", "MATH3.md").read_bytes()
assert hashlib.sha256(raw).hexdigest() == "6e9a9cd074531da12ff5703349ef4c4f89f67fd6b22cc893c5620f858338c2b7"
src = raw.decode("utf-8").split("\n")
R = []


def rep(first, last, why, text):
    R.append((first, last, why, text.rstrip("\n")))


# ---- the header, the tree's digest, what was read
rep(1, 11, "title, date and the tree's digest", """# MATH4: the mathematics of the whole system, on node-all 9d75a4904 (MATH3 with both readers' MATH3 items folded)

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
E's sides guard and the 1.4 side fields). Every probe below ran on 9d75a4904.""")

rep(13, 27, "what was read", """**What was read.**
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
14.""")

# ---- the summary
rep(50, 53, "summary: the law of the path and the seed test", """- **The law of the path, for every click form.** 3.1 and 3.2 prove fiber dependence and the factor: the clicks are a
  function of the board's history and the fiber point, and the board does not depend on the fiber, so seeds one tooth
  apart reach one board. The seed test's twin moves an edge's one tooth on both sides; the owner's test (ii), one unit
  apart, reads NOT SHOWN on the click world's first click by structure and can show only at the third click's member.
  The test's unit is the owner's (08:5x, quoted in 3.2).""")

rep(56, 60, "summary: the law's choice and the record's teeth", """- **The law's choice.** It belongs to the third click, which is on Big Pic's bench only. It is read by Bell's test
  across a pair on the road the owner chose at about 08:35, (C): with settings independent of the hidden part, CHSH is
  at most 2 for any act, and (C) passes it only through a law of the seeds' joint measure, OPEN (08:4x and 08:5x,
  quoted in 7). It is no theorem of node-all's act.
- **The record's teeth are board fields.** The 1.4 record holds the fiber as board fields carried for the checks; the
  click world's readings read the lines and the sides alone, and a passing recovered through the teeth is a board
  check (08:5x, quoted in 3.1). "Hidden" means hidden from the board.""")

rep(70, 71, "summary: the energy", """- **The energy.** No exact energy is known. MIRACLE_A's Theorem A (under its hypotheses (D) and (H)) is NOT PASSED by
  both its readers (09:0x), and nothing here leans on it. Exact linear invariants exist. OPEN, with HAT4.""")

rep(75, 87, "summary: what the probes moved", """MEASURED, on what the probes moved:
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
quoted in 1.7); every click-world reading here is a probe's, its ticks set (3, 100 or 300 rounds).""")

# ---- the table
rep(97, 97, "table row: the split", """| the split (M2) | centred half-open division n = 2D q + s, s in [-D, D); split(-1 - n) = (-q, -1 - s) | the edge's dial of both slots | none of its own: the click world reads lines and sides alone; the passing recovered through the teeth, x = K q + k_after - k_before, is a board check (08:5x) | DERIVED (1.2); the record's identity a board check (R2) |""")

rep(106, 107, "table rows: the run back; the law of the path and the seed test", """| the run back (B1) | M T M = T^-1; T = M o (M o T); <T, M> of infinite order (one aperiodic lawful orbit, DERIVED; D1 its check), dihedral of order 2n on an n-cycle | the same act on the mirrored state | the two-record comparison R1; the end line's "exact" is a board comparison printed into the record | DERIVED (1.5); MEASURED S2 (click and well); D1 a check |
| the law of the path and the seed test (B2) | T^n injective (i); the board a factor, so seeds one tooth apart reach one board (ii), (iii); the lawful twin moves an edge's one tooth on both sides | start seed, end seed, back to the start | two records compared (R1, R2's two-record form); (ii) one unit apart NOT SHOWN on the click world's first click by structure (08:5x) | DERIVED (1.6, 3.2); S7 by construction; S5 and S5b off-lay readings, not MEASURED (08:5x) |""")

rep(110, 110, "table row: the energy", """| the energy (a clock word: the board map's quadratic forms) | no exact energy known; exact linear invariants exist (2.2) | not kept | no conservation of energy is shown in the clicks; the per-edge books close by construction, a code check (09:0x) | OPEN, with HAT4; Theorem A (MIRACLE_A, under (D) and (H)) NOT PASSED by both its readers (09:0x) |""")

rep(112, 112, "table row: the passing", """| the passing Phi (T11) | a whole antisymmetric 1-chain on the window (b, a, a+), odd under its reversal | David's split: the given on one side, the taken on the other | stays out of the click world; x = K q + k_after - k_before recovered through the teeth is a board check (08:5x) | DERIVED (code); the board check R2 |""")

rep(117, 117, "table row: the books", """| the books (D1, D13) | L1 the edge's orientation, by construction; L3 the vertex sum of the telescoping laws, by B C = 0 | each edge closes; each clock within its teeth | per edge by construction, a code check; E's guard reads mates, sums and teeth ranges, "admitted" meaning the mates close (08:5x); per clock within K x degree | DERIVED (4.3) |""")

rep(123, 125, "table rows: the record, the choice, the click world's order", """| the record (R) | a word over the click alphabet, a function of the orbit and the fiber, carrying the fiber as board fields | the boundary of the board | the events the click world is made of: lines and sides; the teeth are board fields carried for the checks (08:5x) | DERIVED (code); board checks R1, R2, R4 and R5 |
| the choice (the law of the choice) | the third click's path (bench); not a theorem of node-all's act | the triangle's hidden pair | Bell across a pair on road (C): CHSH at most 2 for any act with settings independent of the hidden part; (C)'s law of the seeds' joint measure OPEN; R4 under (C) OWED; two questions to the owner (7) | OPEN |
| the click world's order (D11, D12) | the meeting order: a strict partial order inside the round order (10.3) | each clock's own count (OWED) | the click world's 27 of 27 forced by its alike lay; islands: 27 of 3 clocks (click), 3 of 114 / 62 / 187 (mesh); the board couples the sites with no click on both (08:5x) | DERIVED as a definition; C1's and NATURE2's MEASURED |""")

# ---- 1.5's corollary
rep(249, 253, "1.5: the corollary, the drift DERIVED", """**Corollary.** R = M o T is an involution, so T = M o R is a product of two involutions. <T, M> has infinite order
(DERIVED by a three-line induction; MATH3's mathematician, m1). On the bang world's layout every strength is 0, so a
wave row laid as a uniform drift (a test's lay, named so: a = c + 1, b = c, r = 0 at every site) has every stretch 0,
hence no pull, no J1 and no J5. W stays at rest, since c00 stays 0. So p = 2D stays, the split gives (1, 0), and
a_n = c + n + 1 for every n: all the states are distinct, so the orbit is not periodic, and its backward orbit (by the
mirror) is lawful, so it lies in Omega_inf. D1 checks it, 30 of 30 rounds (S/math3/probes/drift_bang_30.txt). On a
cycle of length n, within the width, the group is dihedral of order 2n. The even reversors
T^(2i) M = T^i M T^-i are conjugate to the fixed-point-free M, so any state fixed by a reversor is fixed by an odd one.""")

# ---- 1.7: the shipped click world's ticks
rep(281, 283, "1.7: a departed run, and the click world's ticks", """- The confinement's click-world view is OWED by name. run.run writes the record only after the last round, so a run
  that departs writes no record at all: a written record shows that its run stayed lawful and within the width for its
  ticks, and says nothing beyond them (MATH2's physicist, m6). The shipped click world is such a run (08:5x, verbatim):
  "The shipped click world runs 3,751 of its declared 5,000 ticks: at round 3,752 a count passes the width and the
  runner writes no record (KEY2's readers, KEY3's physicist, MIRACLE_A, UNC1). Every text that cites the click world's
  ticks names it. No tick count is cut to hide it. STOP1's bound reads it. To the owner's batch." Every click-world
  reading in this text comes from a probe's copy with its ticks set, or from the act stepped directly.""")

# ---- 2.2: the energy and the click world's books
rep(321, 331, "2.2: the energy's standing and the books in the clicks", """- **The energy (the coordinator's ruling 4 on MATH1; 09:0x).**
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
  booked total does not hold within its teeth. The board's E is kept only in rationals." """)

# ---- 2.4: road A and road B
rep(347, 356, "2.4: road A classical only; road B as read", """- **Road A, the McMillan / QRT road (08:5x, verbatim: "Road A keeps only the classical one-gear statement (McMillan,
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
  by an unread or unpassed theorem.""")

# ---- 3.1: the record's teeth as board fields
rep(393, 404, "3.1: the record's teeth, board fields and board checks", """The record's teeth (08:5x, verbatim): "the 1.4 record holds the fiber as board fields carried for the checks (E's guard,
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
board check. "Hidden" means hidden from the board: no board coordinate reads a tooth.""")

# ---- 3.2: the law of the path and the seed test
rep(414, 428, "3.2: S7 by construction; the law of the path; the seed test", """re-derived it). S7 holds by construction, for the same reason (MATH1 m1). S5, one unit in one side's tooth, is a
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
- MATH3's "needs a key finer than the passings' grain" is withdrawn as a remedy: the unit is the owner's.""")

# ---- 3.4: the place's sides
rep(509, 512, "3.4: the place's sides' past", """  - DERIVED: for every passing sequence, the partition of the place's fiber by its side words (the sides
    q = Q + C W as output) refines at most |fiber| - 1 times, so beyond a finite horizon (which depends on the
    passings) the place's sides' past fixes every later side (MATH3's mathematician, m7). At a steady passing, once a
    past of length n fixes the next side, it fixes every later one (the map is the same each round). F4 measured only a
    triangle's own landings W.""")

# ---- 4.3: the guard's reach
rep(566, 568, "4.3: the guard's reach", """- **L1, each edge's books:** q at one end and -q at the other, by the edge's orientation and the sign law. No B C is
  needed: this is by construction, the record's faithfulness, a code check (the Boss's 07:5x ruling). The guard's reach
  (08:5x, verbatim): "E's guard reads mates, sums and teeth ranges; 'admitted' means the mates close, not faithful to
  the act. A code item, queued for the round after node-fold: the guard refuses by name a side on an edge the end line
  does not list and a header dial off the file's key. Until then the texts name the guard's reach." (sides.paired, in
  9d75a4904's decoder.)""")

# ---- 7
rep(656, 659, "7: the law of the path and the seed test", """- **The law of the path holds for every click form** (3.1, 3.2; the coordinator's ruling 2 on MATH1 and on MATH2).
  The clicks are a function of the board's history and the fiber point, and the board does not depend on the fiber,
  so seeds one tooth apart reach one board (DERIVED; S7 by construction). The seed test's twin moves an edge's one tooth
  on both sides; the owner's (ii), one unit apart, reads NOT SHOWN on the click world's first click by structure, and
  can show only at the third click's member (08:5x, quoted in 3.2). S5 and S5b are off-lay readings.""")

rep(669, 671, "7: what the record writes", """- **What the record writes:** the dial, the birth, each side's k_before and k_after, and the end teeth (3.1); the
  ledger beside it writes every train's now counts. These are board fields carried for the checks: the click world
  reads the lines and the sides alone, and a passing recovered through the teeth is a board check (08:5x, quoted in
  3.1).""")

rep(680, 706, "7: Bell as it stands now; (Q1) and (Q2) with their stakes", """- **Bell, as it stands now.** The owner's word of about 08:00 UTC, "Bell is in the clicks, not on the board"; his
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
    Q11: "no click reading reads the teeth".""")

rep(676, 676, "7: R2 in each clock's own count, and the ladder", """  - read R2 at lag one beside a lag-two reading, against the derived value floor(38a)/(38a); and (08:4x, verbatim)
    "R2 is read in each clock's own count. Each place's whole joint past is read by R2's ladder (L = 1, 2, 4, 8), a
    necessary reading only.";""")

# ---- 8
rep(719, 720, "8.2: the miracle's standing", """2. **The miracle.** An exact, time-symmetric, energy-keeping whole-number step. No exact energy is known; Theorem A is
   NOT PASSED by both MIRACLE_A's readers (09:0x), and road B keeps no energy exactly in whole numbers (08:5x). OPEN
   (NOT_CLOSED 37, HAT4), first on Big Pic's list (the owner's word of about 09:05).""")

rep(754, 754, "8.7: Theorem A's standing", """   - Theorem A's standing: NOT PASSED by both its readers (09:0x); nothing leans on it (2.2).""")

# ---- 9
rep(767, 767, "9: the fiber's place", """- **The fiber's place.** It is hidden from the board, and the record carries it as board fields for the checks; the
  click world reads lines and sides alone (3.1).""")

rep(769, 772, "9: the choice", """- **The choice** the owner's law names lives at the third click. That is Big Pic's bench, where the hidden pair runs a
  finite affine cat map whose path is fixed by its own past beyond a horizon (3.4). It is read by Bell's test across a
  pair, OWED: with settings independent of the hidden part, CHSH is at most 2 for any act, the pair's one hand
  included, and the owner's road (C) passes it only through a law of the seeds' joint measure, OPEN (7).""")

rep(781, 784, "9: the sentence", """**In one sentence, with its three conditions:** within the width, on a lay whose lawful orbit stays there; on a cubic
O-invariant layout alike at every site; and with the fiber hidden from the board and carried in the record as board
fields: node-all's whole is one reversible, symmetric permutation of whole-number states, a deterministic board
carrying a finite fiber whose wrap counts are the clicks.""")

# ---- 10, whole
rep(786, 879, "10: for the owner's batch, with what a place is as his question", """## 10. The owner's 07:30 word: the families, the algebra, and the order of the clocks' world

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
- Z[i]: a reading's algebra (CONF1), not the act's (6).""")

# ---- 11
rep(881, 883, "11: the probes' header", """## 11. The probes (S/math2/probes/ and S/math3/probes/, on node-all 9d75a4904, its digest in the header; whole numbers, Rule3's carry the one division; nice 19, one process at a time, the load read before each, 6.8 to 8.0)

MATH4 runs no new probe (the owner's word of about 09:05); its folds are of standing. The shipped click world runs
3,751 of its declared 5,000 ticks (1.7); every click-world probe here set its own ticks.

- **MATH3's probes** (S/math3/probes/):""")

rep(891, 892, "11: drift as a check", """  - **drift.py** (drift_bang_30.txt): the bang world's layout with its wave row laid as a uniform drift (a test's lay,
    named so): the row at c + n + 1 after round n, 30 of 30, and the promise met before every round, 30 of 30. A check
    of 1.5's induction, not a proof of aperiodicity.
  - **On the well,** S5 to S7 are vacuous (key 1, no tooth moved); S1 to S4 read its moving parts.""")

rep(916, 917, "11: s5b off-lay", """- **MATH1's probes, cited and not rerun:** s5b (S/math1/probes/s5b_click_100.txt, on 48cd7fcf6, whose engine and runner
  9d75a4904 keeps), an off-lay reading (a one-side twin, 08:5x). The readers reran fiber.py and s5b byte for byte.""")

out = list(src)
for first, last, why, text in sorted(R, key=lambda x: -x[0]):
    out[first - 1:last] = text.split("\n")

section14 = """

## 14. What MATH4 replaces, and MATH3's items

Every replacement, by MATH3's line numbers; every other line is MATH3's, word for word (S/math4/MATH3_to_MATH4.diff):

| MATH3 lines | what |
|---|---|
""" + "\n".join(f"| {a} to {b} | {why} |" if a != b else f"| {a} | {why} |" for a, b, why, _ in sorted(R, key=lambda x: x[0])) + """

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
"""
text = "\n".join(out).rstrip("\n") + section14
S.joinpath("math4", "MATH4.md").write_text(text + "\n", encoding="utf-8")
print("replacements:", len(R), "lines:", len(text.split("\n")))
