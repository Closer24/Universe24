# Tensor24: the build list (the architect, 2026-10-31, 03:5x UTC, for the Boss)

The owner (03:4x UTC, in translation): "No readings: build everything generically, by the approval of the hostile
mathematician and physicist." (BRIEF_PAIRS.md.) So every part that passed both hostile readers, or is DERIVED by both
end readers, is built into the engine generically. Read against node-live 1919dd64c, node-half and node-third, with
FULLPIC.md beside this file as the index of the texts.

## 1. The parts to build now

| Part | Its passing text | The build | Its prerequisites | Writer |
|---|---|---|---|---|
| The half-speed trains, HALF2's items 3 to 8 | half/HALF2.md, PASSED by both readers | on node-half: the loader pieces HALF2 names past its items 1 and 2 (runner/load.py, runner/files.py), each with its test failing on its mutant | items 1 and 2 on node-half a18901454 (the 48 lifts, the two half-speed trains) | A |
| The board's three doublets, the generations | half/GEN4c.md and half/GEN5b.md, PASSED by both readers | on node-half, a loader piece: a half-speed hand laid on the three axes under the whole units' turn (the 24 whole units as three eights), splitting into three doublets alike but for omega's charge; its test the split exact and the 48 commuting with the step | HALF2's items 3 to 8 | A |
| Big Pic's 3+1 gears, the dial and the slots | onelaw/ONELAW3.md, PASSED by both readers | the act change of section 3 below: engine/step.py, the engine's contract and Plan, runner/load.py (geared), runner/plans.py (pushing, notching), the universe's chosen units | writer D's label commit; the owner's word for an act change | D, on a new branch |
| The third click's sound parts | third/THIRD2.md, PASSED by both readers (its sound items kept through THIRD3 and THIRD4) | on node-third: the direction by the drive's law with its tooth r3 kept; q from the gears' move (a+ - a0); the 24 through the teeth; the run back exact at J5 = 0 | the act as built | C |
| The seventh code reader's fixes | code_readers/hcr7_REPORT2.md (three small blocks) | on node-live: the three blocks, each with its test | none | B |

## 2. The parts that build when passed

| Part | Its text now | What it builds | Writer |
|---|---|---|---|
| The third click's trigger and pick (THIRD5, THIRD6) | THIRD5 DRAFTED with its pair; THIRD6 in derivation | builds when passed: under the law of the choice, the draw reads the pair's one hand, not each place alone, read in the clicks by Bell's test (the local bound 2 against the pair's 2 r2, with drawn settings and no signal) | C |
| The draw, term 12's pick (G5) | term 12 DERIVED by both of G5's end readers (David's report, #2187 6538212739); its pick in derivation | builds when passed, with the third click's draw | C |
| The shared tooth for every pair of clocks (NC29b) | nc29/NC29.md (David's split); NC29b in derivation | builds when passed: every passing between clocks carried on an edge between two clocks, at that edge's pair of complementary teeth; three clocks meeting at one place as a triangle, each edge closing | named when it passes |
| The edge teeth | in derivation | builds when passed | B |
| The face (FACE2) | face/FACE2.md DRAFTED, PASSED by its mathematician | builds when its physicist passes it, as a board clock fix | named when it passes |

## 3. ONELAW3's act change, in detail (its sections 3 and 4A; writer D's plan, nightD_work/adm_plan.md)

- The gears. The square train keeps its kinds (A1 and T1, A1, E and T2) and its ten rows: row 00 holds the dial L =
  1/N, rows 0i the shift b^i, rows ii and jk the densitized space grips gt^ij. Every row steps by the one gear tick,
  its push the books' form, -dH/d row, with H = W v_in v_out / 2 + gg^0i v D_i + SUM gg^ij D_i D_j / 2 + spring
  det(gt) L^2 rho^2 / 2 over the rows on the force's path. Gone: W = rest + k0 c00, grip = grip_rest + ii, the unread
  0i.
- The products the act reads, every one a product of gears with no root, no carry by a unit, no sign test and no
  indicator: W = det(gt) L^4 (kinds.det's triple product, the off-diagonal doubling from the expansion, no typed 2);
  gg^ij = gt^ij - W b^i b^j (the diagonal on the six Spokes, the off-diagonal on the centred differences D_i D_j);
  gg^0i = W b^i; the spring det(gt) L^2 m^2 on the held rows.
- (a) The 0i cross terms: the joined act reads d_t(W b^i d_i a) + d_i(W b^i d_t a), so engine/step.py's gear keeps
  W (v - b . D a) on the edge, not W v (sections 3.3 and 3.6).
- (b) The widened given-first step: D_out = W(a) + W(a+) needs W(a+) = det(gt(a+)) L(a+)^4, so the L gear and the six
  gt gears step first, each on teeth that read no W: seven gears against the engine's one 00 row; with the cross terms
  the three b gears too: all ten. The engine's two-stage round is widened; a one-pass D_out = 2 W(a) is refused, as it
  would break the edge's dial that the run back shares (3.4).
- (c) The k-leg monomials: the contract and Plan take four legs, and the act needs det(gt) L^4 v v (9 legs), det(gt)
  L^2 a a (7), gt Da Da (3), and with the shift W b v Da (10) and W b b Da Da (11), term 5's push on a slot one leg
  fewer: a k-leg monomial up to 9, or 11 with the cross terms, the unit standing for the legs a term lacks (3.7).
- (d) The units re-laid: the whole action times one constant, one unit per kind (one for L, one for the three b^i, one
  for the six gt^ij), Lam = gam^3 lam^4 u^2: exact, no motion changed (4A.1: 0 of 192,000 counts missed at Lam 7 and
  1000; the run back at Lam 1, 7 and 1000, 4A.3). The universe's chosen block gets "flat", its units whole and at
  least 1, refused by name; the metric rows' teeth are re-laid by the same factor; every carry in the joined engine is
  scaled with it (the drive's T_d, the kick, the click key). Rest / grip = (gt0 L0^2)^2 is a square, so 6 never fits
  (9 at gt0 3, L0 1), and the board wave's c^2 = 1/6 stays out of reach.
- The loader: load.geared's linear read of the clock becomes the product plan, the grips' read becomes gg^ij, and the
  0i rows get the cross plan; plans.pushing is re-derived as -dH/d row; notching (h tr^2) is restated on gt.
- The 24 and the run back: L is A1, b is T1 and odd under time's reversal, gt turns as the axes' permutation on ii
  (A1 + E) and as T2 on jk; mirror() stands; hypothesis (d) is kept (no metric push reads a metric row's own
  momentum), its price, the metric's self-stress, OPEN as before.
- The digests: since rest / grip cannot be 6, the units cannot give W0 = 6 den Gamma^2 with grip0 = den Gamma^2, so
  all five worlds' digests move; tests/tensor24_prefixes.jsonl is regenerated by write.py.
- Its OPEN items (ONELAW3 section 5), sorted:
  - They block a part of the build:
    - the run back with the kept momentum W (v - b . D a) (3.6): the cross terms (a) ship only once it is measured on
      the board; until then the code holds them with every world laid at b = 0;
    - the step's bound with the shift, both halves (failing in 11 of 12 runs): no world is laid with b off 0 until it
      holds.
  - They do not block the build, each carried as a world's condition or as OPEN in its docstring:
    - the slots' own law: the ten gears step by the generic act (their neighbours' pull and fixed teeth), the law
      OPEN (3.1);
    - L off 0, with crossings as well as landings, and a small abs(L) breaking the bound; gt positive definite under
      strides; the act's window with the spring (12 gt + spring <= 4 W at b = 0): conditions the run's promise and
      the run tool's window read from outside, as now;
    - de Donder: the lay's condition only, its seeds a nonlinear problem, laid at the flat meanwhile;
    - the zero mode on the periodic board (a net source drives W's like t^2): a world's condition on long runs.
- It waits on the owner's word for the act change, and is built on D's new branch until he gives it.

## 4. The order

- A: HALF2's items 3 to 8 on node-half, then the three doublets.
- B: the seventh reader's three fixes on node-live, then the edge teeth when they pass.
- C: the third click's sound parts on node-third; its trigger and pick, and term 12's draw, when THIRD5 and THIRD6
  pass.
- D: his label commit, then ONELAW3's act change on a new branch, (d) and (c) first (exact, no motion changed), then
  (b), then (a) behind b = 0; the owner's word before it merges.
- No two writers share a file: A holds runner/load.py and files.py on node-half, D holds them on his branch; they
  meet only at the merge, where D's geared read and A's half-speed kinds touch load.py, in that order.
