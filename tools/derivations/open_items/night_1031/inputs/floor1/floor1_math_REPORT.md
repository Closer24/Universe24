<!-- Boss note, 2026-10-31 11:06 UTC: written by the Boss from the reader's hand-back (the harness refuses report files from readers); the text below is the reader's, whole. Reader of FLOOR1 (David's DAVID-FLOOR-BALANCE.md, frozen c493a72d, toys-5 4cfca9ca7), the hostile mathematician (the ALG pair's mathematician). -->

# The hostile mathematician on FLOOR1 (David's "The floor's balance: masses against bands"), 2026-10-31

(The harness refuses report files from subagents, so here is the whole report for S/floor1_math/REPORT.md. ASCII only.)

**What I read**
- DAVID-FLOOR-BALANCE.md whole: 150 lines, sha256 c493a72d...; all 5 sums in FROZEN.sha256 check OK.
- floor_balance.py, floor_balance.txt, Big Pic's equil.py of 9771a49a4, and the brief to its end (1,139 lines, through 10:42 UTC).

**How I ran** (all in S/floor1_math/; the live venv's Python 3.14.6 with -I -B, nice 19, one process at a time, the load 2.0 to 3.0):
- copy/ is a copy of the frozen folder; node-all's src is extracted from the frozen tar into src/.
- Reruns:
  - all 24 measured lines of floor_balance.txt, byte for byte;
  - Big Pic's equil.py run itself, 5,000 rounds.
- My own probe, flat1.py: Big Pic's World and round, taken from equil.py exactly as floor_balance.py takes them, at the file's own numbers (lam 1), on lays the text does not try.
- FLOOR1's own probe at s = 0 for lam 1, 10 and 1000.

**VERDICT on FLOOR1: NOT PASSED.** One BLOCKING item: at exactly half the band the floor bounds the potential but does not hold the run. Everything else is sound, re-derived or rerun, with MINOR items.

## BLOCKING

**B1. The balance's flat direction.** At s = t/2 the potential is bounded below, but the run is free along the kernel wherever nothing lends.

**Where:**
- the finding's line: "at that balance the opposite swing ... is held by the held hand's lend alone";
- section 1, "At exactly half the band";
- 2.1, the balance, "Displaced along it with h = 0, the pair rests";
- 2.3, the equilateral triangle, "At s = t/2 those two hold no spring at all";
- the law line FLOOR1 serves: "If the algebra gives exactly half, the floor comes with nothing added."

**Derivation:**
- At s = t/2, the push on the opposite swing (r, -r) is (t - 2s) r = 0.
- The held hand's pushes, -2 S h - 2 c h (g^2 + u^2), vanish at h = 0, so h = 0 at rest is invariant. MASS2's physicist has derived that this set is reached from no other birth.
- So a lay moving along the kernel with the held hand at 0 drifts freely.
- On the equilateral triangle of two-leg bands, Big Pic's road, nothing lends at all. At s = t/2 its two-dimensional part drifts freely for every lay moving in it.
- So V's sublevel sets are unbounded along the kernel, and E32's exact identity does not confine the run.
- Confinement by energy needs the strict inequality. With s > t/2 and S > 0, V >= min(s - t/2, S) |(g, u, h)|^2 is coercive, and the run is then held, given E32's own lower bound, which is OPEN.

**MEASURED** (flat1.py, Big Pic's World and round, lam 1, 20,000 rounds; lay a = (40, -40, h0), b = (39, -39, h0)):

| case | s | held hand | giver's count | outcome |
|---|---|---|---|---|
| A1, the pair | t/2 | at 0 | 5,040, 10,040, 15,040, 20,040 at each 5,000 rounds | drifts one count a round |
| A2, the pair | 11/10 of t/2 | at 0 | within 253 | bounded |
| A3, the pair | t/2 | shipped lay, 1 | within 89 | held by the lend |
| B1, the equilateral two-leg triangle | t/2 | none | 20,040 at round 20,000 | the same drift |
| B2, the equilateral two-leg triangle | 11/10 of t/2 | none | within 253 | bounded |

In every case E32's identity holds at 20,000 of 20,000 rounds and the run back from the end is exact. So the act is sound; it is the floor that fails at equality.

**Fix:**
- State the floor as two conditions, both DERIVED:
  - bounded below exactly when s >= t/2;
  - holding the run (bounded sublevel sets) exactly when s > t/2 and S > 0.
- Name the balance's kernel as a flat direction. It is held only by a lend that never vanishes: on the shipped lay that hold is MEASURED; with the held hand at 0, or with no held hand, the drift is free.
- Tell the owner that "exactly half" gives the potential's floor, not a held run, unless he means the first.

## MINOR

1. **The networks' summary overclaims.** The one-line finding, 2.3's lead, section 6 and the law entry say "the whole band on the line networks and those in E8".
   - s = t needs lambda_min = -2 exactly. That occurs only within the class Cameron, Goethals, Seidel and Shult name: lambda_min >= -2, the generalized line networks and those in E8.
   - Many line networks have lambda_min strictly between -2 and -1, and irrational: the path of three at -sqrt 2; the path of four, the line network of the path of five, at -(1 + sqrt 5)/2; every odd ring, its own line network.
   - 2.3's body says "within" rightly, and the citation is correct (J. Algebra 43 (1976) 305-327).
2. **The grain** (section 5).
   - The control (s = 0) falls at lam 100, round 827, and at lam 1000, round 4,373.
   - It holds over 5,000 rounds at lam 1 (giver within 112) and lam 10 (within 65), by FLOOR1's own probe. Big Pic's own first reading at lam 1 reads widest 7 bits.
   - So the measured contrast with the balance holds at lam 100 and 1000 only.
   - The potential's floor is grain-free (DERIVED); the runs' falls are not. Report the control at every grain read.
3. **Section 3's "the standard reading of a polarized step".**
   - The held clock's polarized dial g = S + c (x_b x_a) can shrink where a count crosses 0 between rounds; the probe even guards "a dial of 0".
   - So E32's lower bound is not standard for the quartic. The OPEN item is right; strike "standard".
4. **The interims** (the owner's 10:34 word, "Everything from the structure. Everything.").
   - FLOOR1 does not name t = 96,000, c = 60,000, W, S and the lay as interims.
   - Resting on them: 48,000; the 315 balances (t's factors); the 3/8 edge (t/2 - c/2 at the held lay 1); every measured row.
   - Free of them: the form; s >= t/2 and s_1 s_2 >= (t/2)^2 as relations; the networks' classes.
   - Cite 10:34 verbatim. It answers section 6's open "second clause".
5. **The law line's "each a mass of at least half the band"** is the equal-mass, sufficient case. The exact condition is s_1, s_2 >= 0 and s_1 s_2 >= (t/2)^2 (2.1): one mass may sit below half the band. Say so beside the quoted law.
6. **"The click world's triangle" is Big Pic's one-count-per-clock reduction**, not derived on the shipped plan.
   - The shipped trains have several rows. The tie's lend is diagonal there by Schur, on the signed-permutation kinds; a tied train of kind E would lend off the diagonal, outside 2.3's scope.
   - The shipped world's fall (node-all's act, lam 1, round 3,752) is another act and grain than the control's (road B's round on the triangle, lam 100, round 827). Name which.
7. **The freeze.** The control's reference, split_bedge_x100_5000.txt, and equil_5000.txt are not frozen. Section 7's "reproduces exactly" cannot be checked from the freeze. The swap reading does reproduce, by running equil.py: 2 of 6 turns and flips.

## SOUND (re-derived, with numbers)

- **The lend (the press point): right.** M(h) = M(0) + c h^2 I with c >= 0, so M(h) is non-negative for every h exactly when M(0) is. The statement is pointwise in h, so h's motion does not touch V's lower bound; it touches only the run (B1).
- **V's lower bound.** V is bounded below exactly when s_1, s_2 >= 0 and s_1 s_2 >= (t/2)^2.
- **The equilibria.** With S > 0 they are h = 0 with (g, u) in ker M(0). The kernel is spanned by (t/2, -s_1).
- **The divisor count.** 48,000 = 2^7 x 3 x 5^3, so (t/2)^2 has 15 x 3 x 7 = 315 divisors: 158 unordered pairs and one equal pair. The free swing (m, -s_1) is whole.
- **The networks.**
  - The form is s I + (t/2) A.
  - A rational eigenvalue of a whole-number matrix is whole.
  - lambda_min = -1 exactly on unions of complete groups: an induced path of three sits at -sqrt 2, and Cauchy's interlacing does the rest.
  - Even rings sit at -2. Odd rings of five or more sit at -2 cos(pi/n), irrational.
  - The equilateral triangle holds s + t and s - t/2, twice.
- **Section 4's edge.** t/2 - c/2 = 18,000 = 3/8 of 48,000; it is measured between 3/8 (falls) and 2/5 (holds).
- **Reruns.** All 24 measured lines are byte for byte, and E32's identity holds at every round of every run.

## DERIVED / MEASURED / OVERCLAIMED

- **DERIVED (re-derived):** the pair's lower bound and balance, the divisor count and the network classes. My additions: the kernel's zero force; h = 0's invariance (a free drift); coercivity at s > t/2 with S > 0.
- **MEASURED:** the 24 lines; flat1's A1 to A3 and B1 to B2; the control at four grains; equil.py's first readings.
- **OVERCLAIMED:**
  - "held by the held hand's lend alone" at the balance, and the law's equality clause read as no fall (B1);
  - "the whole band on the line networks" (MINOR 1);
  - "the standard reading of a polarized step" (MINOR 3).

## Questions for the Boss

1. Does the floor law's "exactly half" mean V bounded below, or runs that do not fall? If the second, it fails with the held hand at 0 and on Big Pic's equilateral two-leg triangle, and the strict inequality is needed.
2. Should FLOOR1 report the s = 0 control at every grain? It holds 5,000 rounds at lam 1 and 10.

## Solution24 (the reader's line)

FLOOR1's balance is right for the potential: s >= t/2, the divisor pairs of (t/2)^2, and the network classes. But a floor that holds the clocks needs masses strictly above half the band. At exactly half, the opposite swing is a free direction wherever nothing lends.
