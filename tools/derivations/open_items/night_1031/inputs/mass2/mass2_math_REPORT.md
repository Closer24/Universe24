<!-- Boss note, 2026-10-31 09:22 UTC (first labelled ~09:5x, ahead of the clock): written by the Boss from the reader's hand-back (the harness refuses report files from readers); the text below is the reader's, whole. Reader of MASS2 (frozen c41cbea6), the hostile mathematician (MASS1's mathematician). -->

# MASS2, read by the hostile mathematician (2026-10-31), the reader of MASS1

The report is handed back whole, not filed as REPORT.md, because this harness refuses report files from me.

S is S. I read the text whole: S/mass2_frozen/MASS2.md, sha256 c41cbea66d76321eb83e6174df74bbffd5d3ed98102328685f33367141d764f0, 618 lines. All 65 sums in FROZEN.sha256 check. I read it against my own MASS1 report (S/mass1_math/REPORT.md) and against the brief's rulings of 07:5x to 09:0x.

My files, in S/mass2_math/:
- copy/: the probes and tree. All 48 files match their frozen sums.
- copy/out/: the five reruns.
- gate_run.sh: my load-gated runner.
- loads.txt: the start load of each rerun.
- overlap.py, with outputs overlap_1.txt and overlap_2.txt, which are alike.

How I ran them:
- The five reruns started at loads of 7.37 to 7.90, one process at a time, under nice -n 19.
- One probe rule broken, named: my overlap.py (no engine, under a second) ran both passes at a load of 8.89, without the gate.

## VERDICT on MASS2: PASSED

Every BLOCKING and MINOR item of my MASS1 report is met. What is new in MASS2 holds when I measure and derive it; the items left are MINOR. All five probes reproduce byte for byte from my copy. beat_long.py does so only with the arguments 5000 100, which the text does not record (MINOR 9).

## MASS1 items, met or not

| item | met? | how |
|---|---|---|
| B1, the lone member bound | MET | 4.4: V only semi-definite; k = 0 invariant; lone.py (a) by the engine's own act, 41 to 1,041 with V = 0; "the miracle sorts the designs" struck; the held hand at 0 sent to the owner's batch |
| B2, leaning on the roads | MET | every road result CONDITIONAL; only McMillan, Northcott and Mazur cited, as classical (the 08:5x MATH3 ruling); "no rotation number" struck, with KAM; the width passage measured here, not taken from MIRACLE_A. The label's wording is stale (MINOR 1) |
| M1, the chance | MET | 169 distinct products; 0.2 to 0.3; look-elsewhere named; no product printed; out of the verdict |
| M2, "about 245" and the lay | MET | the held row's 2 c \|x\|^2 term restored; the indefinite minor MEASURED; the 60,000 named as the tied curvature over the held spring with the tied counts at 0 |
| M3, "not whole" | MET | 561,909 is whole, within 4 parts in 10^7; only the fake's fourth form bars it |
| M4, the checks | MET | M4 is M1 for (X, Z), so three checks; each clock is read against light's links |
| M5, "own lines" | MET | own lines as the record writes them; MASS1's count renamed side landings |
| M6, the characters | MET | Frobenius-Schur from g g; the 8-gear train takes one beat, the 24-gear train at most four; -I measured |
| M7, the factorisation | MET | 3^3 x 641 x 26,423; split and inert; the primes through p -+ 1 |
| M8, the loads | MET | MASS1's 9.01 and 8.19 named; MASS2's runs all at 8 or below, logged |
| Q1 to Q3 | answered | owner's batch; classical citations; the per-clock test |

## BLOCKING

None.

## MINOR

1. **The CONDITIONAL label is out of date** (labels; section 0). MASS2 says the roads are "which no hostile reader has read yet" and "unread by any reader". By the 09:0x ruling, both of MIRACLE_A's readers read it NOT PASSED; by the 08:5x ruling and the coordinator, MIRACLE_B's physicist did not pass it either. Nothing leans on either road, so only the wording changes.

2. **THIRD7's period is cited uncorrected** (3.4). L's order modulo the dial is exactly 528,480. But the 07:5x ruling requires THIRD7's corrected form: its period is 528,480 rounds when 3 divides y, else 1,585,440. Cite that form, or call 528,480 "L's order" alone.

3. **"No minimum" and "readings at a saddle" are loose** (verdict; 3.3). This came from my own MASS1 report.
   - The lay is not a critical point. At the lay, dV/dk = k x d2V/dk2 = 392,000,000, not 0. A saddle is a critical point.
   - The click world's V has no minimum anywhere: it is unbounded below along x_g = -x_t on the invariant line k = 0 (lone.py (c) measures V reaching -6.3 x 10^17).
   - So no normal-mode beat exists at any lay, and 3.1's "a beat is read from the motion" is the right road.
   - Fix: "the lay is no equilibrium, the Hessian there is indefinite, and V is unbounded below".

4. **The E1/2-cubed row reads a tensor cube as a train** (2.3 table).
   - Three half-speed members in a real engine are three trains, a direct sum of 3 x 4 real rows.
   - Their beats under 2O x S3 are 3.2 (c)'s two modes, kt + 2 tie and kt - tie.
   - No clock train holds the tensor cube, so "beats at most 3" belongs to no train.
   - It also contradicts 3.2 (e): "multiplicities, not beats".

5. **GEN3's qualifier is dropped** (2.4). GEN3 says "a real spring never parts 2' from 2''", meaning time-even. MASS2 writes "every real coupling the 24 units keep". On the hand's real form that is false:
   - P(2') - P(2''), the difference of the isotypic projectors in the complex hand, is complex-linear, Hermitian and 2T-equivariant.
   - So on the real form it is a real symmetric coupling the 24 units keep, which gives 2' +1 and 2'' -1.
   - It is time-odd: time reversal is antilinear and swaps 2' and 2''. That is exactly the kind of GEN5's parting term.
   - DERIVED. Write "every time-even (real-spring) coupling". MASS2's own parting-term sentence then agrees with it.

6. **"Necessary" is too strong for the thresholds** (4.4, Statuses).
   - lone.py (b) keeps the lone member within -43 to 44 although |k|^2 = 0 in 558 of 2,000 rounds.
   - What is derived is the runaway on the invariant line k = 0: the lone member drifts, and the pair grows wherever |k|^2 stays below tie / 2c.
   - So the necessary condition is that the held hand not rest at 0 (or stay below 0.8). It is not |k|^2 > 0 (or > 0.8) at every round.

7. **The mass row's definition** (1.2, MASS3's business).
   - M1's "windows of whole beats": state how a window of whole beats is read from clicks alone, for example as the own lines' period. Otherwise the calibre must carry one beat's lines.
   - The per-clock test against S's links sees a drift unless the source shares it, so S should be of a third design.
   - M2 is an identity on the side-by-side lay, as the text says. It fails only on the swap lay at two Node-clocks: a second reading of place-independence.

8. **1.3's per-clock calibre is loose.** The window's rounds are exact counts, so the per-clock M1 calibre is R1 + R2 (782), not n1 + R1 + n2 + R2 (1,122). No verdict changes: the FAILS stand a fortiori, and giver's 391 holds at 782 too.

9. **Recording and probe rules.**
   - beat_long.py's arguments (5000 100) are recorded nowhere. My first rerun, at 3750 100, differed by the width line.
   - lone.py line 86 uses `%` outside the carry, for its print cadence.

10. **1.3's one-Node-clock reduction needs its reason named.** It stands for the cube by the alike lay's translation symmetry: every site's neighbours equal it, so a 1 x 1 x 1 board whose Meshes return to itself carries the same act (DERIVED). It was checked over 100 rounds. Its reason is that symmetry, not "27 uncoupled copies". My NATURE1 report used that phrase and the Boss struck it at 08:5x.

11. **The chance formula.** For a fixed set of products and a target at random, the chance of a hit is the windows' covered fraction, not 1 - e^(-lambda), which is a random set's formula.
    - MEASURED (overlap.py): 37 neighbour pairs' windows overlap, 6 of them in 1,836's octave.
    - So the exact chance lies between 0.16 and 0.20 globally, and between 0.25 and 0.36 in that octave.
    - The text's 0.2 to 0.3 stands.

## SOUND

**The new material:**
- **The cat map's orders**, by triangle2.py and by my MASS1 probe independently:
  - the dial is 3^3 x 641 x 26,423, both primes by trial division;
  - 10 is a square modulo 641 (split), with order 160 = 2^5 x 5;
  - 10 is a non-square modulo 26,423 (inert), with order 2,936 = 2^3 x 367;
  - the order is 9 modulo 27;
  - the lcm is 528,480, each order certified by L^(n/q) not I.
- **The Hessian, from the loader's own monomials:**
  - the second derivatives are right term by term (2f for x^2; 2f y^2 and 4f x y for x^2 y^2);
  - the minors are -45,120,000,000,000 at the file's strengths and -69,119,999,760,000 with every strength at 1;
  - held over tied is 1,600 + 2/120,000.
- **Frobenius-Schur:** +1 for the five whole kinds, -1 for E1/2, E5/2 and G3/2. This is confirmed by a second method in my MASS1 probe (chi(g^2) = chi(g)^2 - 2, and G3/2 = E1/2 x E).
- **The beat counts, checked by hand:**
  - the 8-gear train has commutant H and one symmetric form;
  - the 24-gear train has commutant H + H + M_2(H), with 8 symmetric forms and at most 4 beats;
  - the hand has 2 symmetric forms on its real form, (8 - 4) / 2;
  - a, b, b holds under 2O.
- **The chance:** 454 multisets and 169 distinct products, with the octave counts.

**The probes' other numbers:**
- **lone.py:**
  - (a) the lone member, 41 to 1,041 with V = 0;
  - (c) the pair grows about 3.54 times per 100 rounds, which is e^(100 root(tie / W)), DERIVED from V = tie x_g x_t at k = 0.
- **beat_long.py:**
  - one Node-clock is alike with the cube for 100 rounds;
  - a count passes the width after round 3,751, as the 08:5x ruling names it;
  - the half-beats 196, 195, 196, 195, 196 (rounds 645 to 1,623), then the walk (93 to 77, 55, 95 and 90, 173 to 144, 83 to 27);
  - the M1 entries (836/673, 184/673, 999/666, 1,564/1,122, 391/1,115, 1,955/1,115) and the hold counts (5, 11, 4; 3 or 4).
- **"1,836.15 is a number to meet, never a target":** kept everywhere. No probe types it, no product is printed for its nearness, and no strength is moved.

## DERIVED / MEASURED / OVERCLAIMED

**DERIVED, sound:**
- the thresholds' runaway on k = 0;
- M2's (r_a / r_b)^2 inversion;
- Frobenius-Schur's consequences;
- the orders' origin in the key's primes;
- the classical facts of 4.1. One small gap: the degenerate genus-0 levels are not named, but they also grow without bound unless periodic.

**MEASURED, sound:** all five probes, twice, byte for byte, reproduced by me.

**OVERCLAIMED:**
- "a saddle" and "no minimum" (MINOR 3);
- "beats at most 3" for E1/2 cubed (MINOR 4);
- "every real coupling" (MINOR 5);
- "necessary" (MINOR 6);
- "THIRD7's period" (MINOR 2).

## Questions for the Boss

1. Should GEN3's 2T statement be cited as "every time-even (real-spring) coupling"? The real symmetric time-odd P(2') - P(2'') parts 2' from 2'' and is GEN5's kind.
2. For MASS3: is the whole-beat window read from the clicks alone (the own lines' period), and must the light source be of a third design so that a shared drift shows?
3. Does a test's lay on another board shape (lone.py and beat_long.py on one Node-clock) fall under the 08:5x test's-lay rule, which names one-site differences?

## A line on Solution24

MASS2 is now a sound statement of what the structure fixes about beats (equalities, counts, one beat per real irreducible, and the key's primes in the period) and of what a mass in the clicks still lacks. On node-all both designs' binding is the held hand's state, and the board's one beat walks with it.
