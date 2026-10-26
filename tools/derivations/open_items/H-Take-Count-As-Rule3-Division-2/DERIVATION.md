# H-Take-Count-As-Rule3-Division-2 (tc2): the take's count as Rule3's own carried division (2026-10-26, 07:06 to 08:2x UTC; toys-5 3dc12e307)

## 0. The unification block (the four roads), and the item

The letter holds the take's count twice: as "the least count of levels at which the Node's share falls by the walls" (take.fall_of, CS4-S2, EX-S1) and, in the code, as a root (rule3.least_root with largest_below, the neighbours s - 1 to s + 2 checked, and a guard loop over every count to the full move). The four roads:

1. The algebra (one bilinear where two are written): the share at a Node is one quadratic form in the levels (merger.share_at: the own term w (now^2 + before^2) - S now before - now x reached, the Links' terms). A move of the now level by t s (t the sign of before - now) changes the form by f(s) = x s (g - w s) over the weight 2 Gamma^3 G^2, with g = -t (2 w now + pull) and pull = S before + SUM_j R_j before_j, Rule3's own numerator read on the before slot (the backward numerator N(-1) = pull - w now; CA-S2's pull). The fall is the count times the form's gradient at the midpoint of the move: f(s) = s x (g - w s) / weight, one bilinear, where the letter writes a root.
2. The matrix (the Link's record as one object): the gradient g is the Link's record on the taken line (the six reaches times the six befores, plus the Node's own S before and the wall's 2 w now); nothing of the record enters twice. No second object found on this road.
3. The cube: the count depends on three scalars of the Node (the walls owed, the full move dist = |now - before|, the full fall), each invariant under the 48 (walls_of's cache is per Node and sense, dist and full read on the taken line), so the chord count is covariant under every image; measured on the chiral 3-cube to 60.
4. Rule3 (the one step, the carried division with its remainder, the special case folded): the count as ONE carried division at the direction -1, the law's own act (RW-S1: the division at -1 is the division at +1 conjugated by the remainder's mirror, so the quotient is rounded up), and no root: the four lines of the search and the dead least_root (rule3.py) taken out of the code.

## 1. The algebra (one page)

**The quadratic.** With now = n, before = b, the moved level m = n + t s, 1 <= s <= dist = |n - b|:
f(s) = x (w (n^2 - m^2) - t s pull) / weight = x s (g - w s) / weight, g = -t (2 w n + pull).
The leading coefficient -x w / weight is never 0: x the carrier's level at the Node (positive), w = 6 den Gamma^2 G^2 the wall. So f is strictly concave in s, with f(0) = 0.

**The theorem (why the least count is no division).** The own term of the form, w (n^2 + b^2) - S n b, has S = 2 w - D - SUM_j R_j with D + SUM_j R_j = 12 den Gamma^2 G^2 at the vacuum's paces and less at every content below it (p_0 <= Gamma), so 0 <= S < 2 w and the form is positive definite in (n, b): every move of any direction v at the Node changes the form by a term quadratic in the count with the coefficient Q(v) > 0. The least count paying a wall is then the least root of a quadratic; at a vanishing gradient it is the square root of the walls over x w (measured: the walls times 1, 4, 16 give the counts 1000, 2000, 4000), while every composition of carried divisions is a piecewise affine map of its integers (the quotient of an affine numerator by a fixed wall, its remainder affine too), bounded by the numerator over the wall. A square root is not piecewise affine, so no composition of the law's four acts, in either direction, gives the least count (CA-S2's theorem, here in one line). This is the law that refuses: the share's bilinearity (ALGEBRA.md, The bilinears of one pair; The conserved form) with the take's letter "the least count".

**The form that is one division (the chord).** Concave f with f(0) = 0 lies above its chord on [0, dist]: f(s) >= s f(dist) / dist. With full = fall(dist) (already read: the refusal `stop` where full < walls), the count
    s_c = ceil(walls x dist / full) = carried_division(walls x dist, full, 0, -1)[0]
(the carried division at the direction -1 at the remainder 0: carried = total + full - 1, the quotient rounded up by the remainder's mirror, RW-S1's letter) satisfies 1 <= s_c <= dist (full >= walls) and fall(s_c) >= s_c full / dist >= walls (fall the floor of f, walls an integer). The walls are paid at every take, within the full move, the surplus fall(s_c) - owed the take's remainder (EX-S1, unchanged). The least root s* <= s_c; the chord overpays where f bends (the surplus kept, nothing made).

**Where it meets the Link's record and the direction.** dist is the full reversal's move, the line now == before (the past meeting the future, CA-S2's line, reached by the head's take at the full move alone); full is the share's fall to that line, the difference of the form at the two slots' records; the count is the walls measured in the full move's mean fall per level, one quotient of the two ends' records. The division is the law's act at -1: the click's own direction (CA-S1: the click names the now slot and moves it toward the before; the count's division at -1 is the read of that move). The move stays take.move (CR-S1), the ends read before any is written (CR-S2), the slot the now slot (CA-S1): the click is one act of Rule3 at the Link with no root.

**The smallest change of the letter.** One phrase: "the least count of levels at which the Node's share falls by the walls" becomes "the count the carried division at -1 of the walls times the full move by the full move's fall names". The former least count is kept by name.

## 2. The sentence, as it would stand in ALGEBRA.md under The click (TC-S1, dated 2026-10-26; EX-S1, CS4-S2, CR-S1, CR-S2 and CA-S1 kept by name)

TC-S1 (the take's count is one carried division): the exact take at a Node moves the taken line's now slot toward its before by a count of levels that is one carried division of the law at the direction -1, the walls owed times the full move (|now - before|, the line now == before) divided by the full move's fall of the Node's share, the quotient rounded up by the remainder's mirror; the share's fall is concave in the count with no fall at no move, so the chord's count pays the walls at every take within the full move, and what it pays above the walls is the take's remainder (EX-S1); no root and no search: the former least count (the least root of the share's quadratic) is kept by name.

## 3. The measurements (the prediction before each run, the measurement after; integers only)

See REPORT.md section 3 (the same table), filled from out/ by tc2_read.py.

## 4. The spec for David (the file's key: none; no constant, no name, no switch)

- src/event_universe/take.py, fall_of: after `if full < walls: return None, full, k`, the four lines of the least-root search (the `for s in rule3.least_root(...)` loop and the `return (*next(...), k)` guard) replaced by two: `chord = rule3.carried_division(walls * dist, full, 0, -1)[0]` and `return chord, fall(chord), k` (tc2.patch, applies on 3dc12e307 with `git apply --check`). The docstring names TC-S1 and keeps the least root by name.
- src/event_universe/core/rule3.py: least_root is then called nowhere (dead): take it out (its 8 lines); largest_below stays (board, circle, decoder, node, predicates, seed call it).
- The one-Node test: test_one_node_tc2.py, two functions, 3 s: (1) on 20,000 random concave quadratics the chord pays, stays within the full move and is at least the least count; the least count at a vanishing gradient is 1000, 2000, 4000 at the walls times 1, 4, 16 (the square root, no division); (2) at the centre of the 3-cube after 4 intervals with the taken line set to (1227, 920): the head's count 10 (fall 1710840969634422502204), the chord's 11 (fall 1881413183716533877284), the walls 1637588529984138012000, within 307, the same line 0.
- The pass predicate on the records: the chord pays at every take (fall >= walls, the count within [1, dist]); taken >= owed and taken - owed == remainder at every birth and credit; the run back 10 of 10; the flag empty bit for bit (the hole 60 67eec79514fbf0f7, the chiral 60 a53897d02b433687 by the tests' state_of sha256[:16]); the births and credits as the table of REPORT.md section 3 (the course changes: first apart at 19 on the hole 60, 7 on the chiral 60).
- The reader's row: none new; the exact take's row (gate 47) reads the same predicate.

## 5. Missing by name

- The surplus: the chord overpays where f bends (the hole 60: 20 of 251 takes above the least count, 20 levels of 689); a second division (the chord of the chord, the tangent at s_c) would bring the count nearer the least at one more division; not derived here (the one division is the item).
- A1 (P and J at every birth): the count's form leaves the lay unchanged; the P balance at a birth is the head's (dP_take unpaid by the children's lay on an empty plane: 0 of 16 exact on the hole 60 head and 0 of 18 under the form): the packets' item (AJ-S6), not the count's.
- The 48 on the clicks under the chord: measured on the chiral 3-cube to 60 (REPORT.md); the 5-cube's 48 not run (the budget).
- The chiral 2,400 and the collapse under the chord: not run (the box).
