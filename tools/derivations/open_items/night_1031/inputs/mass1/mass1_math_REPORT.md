# MASS1, read by the hostile mathematician (2026-10-31)

(Written by the Boss from the reader's hand-back at 08:4x UTC, the reader's harness refusing the write; the text is
the reader's, word for word.)

I did not write REPORT.md: last time the harness refused that file, so the whole report is here.

S is S. I read the text whole: S/mass1_frozen/MASS1.md, sha256 a703dff9343123333d252eb027d215842e331f7628d952322b6e559afaa3bd77, 464 lines. All 1,224 sums in FROZEN.sha256 check.

My files, in S/mass1_math/:
- copy/: the three probes, tree/src and tree/examples/tensor24-click. All 33 files match their frozen sums.
- copy/out/: the frozen probes rerun from the copy.
- mass_math.py: my own probe, with outputs mass_math_1.txt and mass_math_2.txt, which are byte for byte alike.

Every run went one at a time under nice -n 19, starting at loads of 7.68 to 8.00. All arithmetic is in whole numbers, with Rule3's carry the one division.

## VERDICT on MASS1: NOT PASSED

There are two BLOCKING items:
- **B1:** The lone member's "bound at every size" is false.
- **B2:** Section 4 and the Statuses lean on MIRACLE_A and MIRACLE_B as if they were results.

Everything else is sound or MINOR. The headline still stands: the structure fixes only equalities and counts, and no mass can be read in the clicks today.

## BLOCKING

### B1. "A lone member tied to the held hand stays bound at every size" is false (section 4.4; verdict-first "The miracle sorts the designs"; Statuses)

The text derives it from V = s |k|^2 + c |k|^2 |x|^2 being "positive definite". It is not.
- V is only positive semi-definite: V = 0 on the whole line k = 0, whatever x is.
- That line is invariant: the force on k is -2 (s + c |x|^2) k, which is 0 at k = 0.
- On that line the member feels no force under the explicit step. Under the polarized step its force is -c k^2 (x+ + x-), also 0.

MEASURED exactly:
- I laid the explicit step with k = 0 and x = 40 moving one count a round.
- After 1,000 rounds, k = 0 and x = 1,040, with V = 0 along the whole orbit: an unbounded orbit.
- Positive E does not confine either, because the level set of E holds that line.

This is the same invariant line the text uses for the pair's runaway, and the click world reaches it: the held count stands at 0 in some rounds (1.3).

**Fix:** the lone member is bound only while the held hand is not at rest at 0, which is OPEN. "The miracle sorts the designs" falls with it.

### B2. Section 4 and the Statuses lean on MIRACLE_A and MIRACLE_B as results (4.2, 4.3, 4.4, verdict-first, Statuses; beat.py's docstring)

The coordinator's rule is that nothing may lean on MIRACLE_A as passed. MASS1 does so in four places.

- **"No rotation number for the coupled step", listed as DERIVED.**
  - It rests on road A's measured height growth ("about threefold a round"). That is evidence of non-integrability, not a proof.
  - Even granted, non-integrability does not take rotation numbers away from every orbit: KAM tori near an elliptic point keep them.
  - So it is neither derived nor implied.
- **4.3's "No" in rationals rests on Theorem B.**
  - It holds classically without Theorem B: a non-torsion orbit on a McMillan curve has canonical height growing like n^2, so no fixed width holds it.
  - Cite that instead.
- **4.3's B-edge conclusions and the verdict take MIRACLE_B's measurements as facts.** These are the heating from 1 to about 30 counts, and the 1,080 and 1,038 per mille past 4W.
- **Other places:**
  - 4.4's "E positive at every size, with no window (road A, 2.4)";
  - beat.py's "runs away after round 3751, MIRACLE_A".

**Fix:** mark each of these CONDITIONAL on MIRACLE_A or MIRACLE_B (both unread), and take them out of DERIVED.

The McMillan facts themselves are classical and SOUND. I checked that the polarized step for V = s x^2 + c x^4 is x+ + x- = 2 W x / (W + s + 2 c x^2), which is McMillan's form, so cos theta = W / (W + s) at small swing.

## MINOR

### 1. Press point 5, "how near" and the chance (3.5 and the verdict)

The count of 454 is right only as multisets: 12 + 78 + 364. Because the twelve integers have only the primes 2, 3, 5 and 19, the products coincide heavily:
- there are only 169 distinct products;
- 1,824 alone has 5 representations: 48 x 38, 2 x 24 x 38, 3 x 16 x 38, 4 x 12 x 38 and 6 x 8 x 38;
- it is the only distinct product inside the window.

The honest chance, MEASURED:
- the text's own model, applied to distinct products, gives 0.19 rather than 0.52;
- the local density gives 0.32: there are 8 distinct products in [1,536, 2,136], and the window is 24.3 wide.

The integer 38 is in the set only because it is a factor of the hit. Without 38 the nearest products are 1,920 (4.6 per cent above) and 1,728 (5.9 per cent below).

The verdict-first says "about one such miss", but 3.5 says 0.5. Write 0.2 to 0.3, and add the look-elsewhere effect: the set was chosen after the hit, and 12^3, (3 + r10)^4, 48^2 and 6 pi^5 were also tried. The conclusion, no evidence, stands and is strengthened.

### 2. Press point 3, the "about 245" (verdict and 3.3)

The formula is right as a ratio of curvatures:
- the tied curvature 2 f |k|^2 over the held spring's 2;
- f = W div Gamma = 6 den Gamma = 60,000;
- the root of 60,000 lies between 244 and 245.

But the text's "on the click world... at its lay" is wrong, because it drops the held row's 2 c |x|^2 term.
- At the lay that term is 192,000,000 (|x|^2 = 1,600).
- With every strength at 1, the held over the tied curvature is 1,600 and 2/120,000. The beats come out about 40, which reads the lay's 40, not 245.

The per-gear curvatures at the lay are not normal-mode beats either. The (held, giver) minor of the Hessian is indefinite:

| strengths | entries | determinant |
|---|---|---|
| the file's | 392,000,000; 9,600,000; 120,000 | -45,120,000,000,000 |
| all read as 1 | 192,000,002; 9,600,000; 120,000 | -69,119,999,760,000 |

So the 216,000 and 24,000 split, the "beats about 3" and the "beats about 128" are diagonal readings at a saddle. The last one is also the small-angle root: at 163 per mille of 4W the explicit step's beat is about 3 per cent above it.

The conclusion holds and is reinforced: every unequal ratio reads a strength, the lay or the file's integers.

### 3. "Not whole" (3.3) is no argument

A whole lay comes within 4 parts in 10^7: den Gamma |k|^2 = 561,909 gives the root of 3,371,454, which is 1,836.152. The bar is the fake's fourth form, not wholeness.

### 4. Press point 1, the four checks (1.2)

- **M1 to M3 can fail as definitions.**
- **M4 is M1 for the pair (X, Z).** Within one window N_Y cancels, so "N_X / N_Z in another window agrees with the product" is exactly the steadiness of N_X / N_Z across windows. That makes three checks, not four.
- **M1's stated no is too broad.** A ratio cannot see a drift two clocks share. By 3.2 (b) every tied train shares the beat 2 hold f |k|^2 / W, so two tied clocks pass M1 while the held count walks - the very walk 4.3 describes.
- **None of the checks can run on any world** (no light's lines). The text says so honestly.

### 5. 1.3's "own lines" are not 1.2's lines

They are sides with a quotient not 0, counted per side per round: 238 and 292 exceed a window's 200 rounds. They equal site 0's per-edge landings in NATURE1's record:
- held: 150 + 88 = 238;
- giver: 150 + 11 = 161;
- taker: 88 + 11 = 99.

So they read the edges' passing, not a beat. Rename them. M1's arithmetic is right: 8,456, 6,792 and 8,112 against 853, 779 and 572.

### 6. Press point 2, the characters: every decomposition re-derived by hand from 2O's table

The table, with class sizes 1, 1, 8, 8, 6, 6, 6, 12:

| kind | E | R | C3 (ord 6) | C3 (ord 3) | C2 | C4 | C4R | C2' |
|---|---|---|---|---|---|---|---|---|
| E1/2 | 2 | -2 | 1 | -1 | 0 | r2 | -r2 | 0 |
| G3/2 | 4 | -4 | -1 | 1 | 0 | 0 | 0 | 0 |

My hand derivations, all matching the probe:
- The squares of the dimensions sum to 1 + 1 + 4 + 9 + 9 = 24, and with 4 + 4 + 16 to 48.
- E1/2 cubed has characters (8, -8, 1, -1, 0, 2r2, -2r2, 0):
  - its E1/2 multiplicity is (16 + 16 + 8 + 8 + 24 + 24) / 48 = 2;
  - its G3/2 multiplicity is (32 + 32 - 8 - 8) / 48 = 1;
  - it is odd under R, so it holds no whole kind.
- E1/2 x T1 has characters (6, -6, 0, 0, 0, r2, -r2, 0):
  - its E1/2 multiplicity is (12 + 12 + 12 + 12) / 48 = 1;
  - its E5/2 multiplicity is 0, and its G3/2 multiplicity is 48 / 48 = 1.
- On 2T (A2 = +1, 24 lifts): 2 x 3 = 2 + 2' + 2''. G3/2 restricts to 2' + 2'', and E1/2 and E5/2 restrict alike.
- Under 2O this gives a, b, b by Schur.

The sharpening is the Frobenius-Schur indicators, MEASURED from the engine's own characters:
- E1/2, E5/2 and G3/2 are all quaternionic (-1);
- the check uses G3/2 = E1/2 x E, verified at every lift.

What that changes:
- In a real train each half-speed kind sits at an even multiplicity.
- The 8-gear train's 2 G3/2 is one real irreducible, so it takes one beat under every symmetric 2O coupling, not "up to 2".
- The 24-gear train takes at most 4 beats, not 8.
- "A doublet's two rows, G3/2's four" cannot be real rows: they are 4 and 8.
- The generations' a, b, b stands: the hand's real form is the real E1/2 and the real G3/2, each once.

The probe also printed "the full turn acts as -I" from the engine's flag, not as a measurement. I measured it: at the full turn (lift 24) each half-speed character is minus its dimension.

### 7. Press point 4, the factorisation (3.4)

The text's 3^3 x 16,937,143 is a true product with a composite cofactor. THIRD8's 3^3 x 641 x 26,423 is the prime factorisation: both primes checked by trial division, and the key = 3 x 641 x 26,423.

MEASURED, with the orders:

| modulus | case | order |
|---|---|---|
| 27 | L = I mod 3 | 9 |
| 641 | 10 a square: split, order divides 640 = 2^7 x 5 | 160 = 2^5 x 5 |
| 26,423 | 10 not a square: inert, order divides 26,424 = 2^3 x 3^2 x 367 | 2,936 = 2^3 x 367 |

- The lcm modulo the cofactor is 58,720, as the text says.
- Modulo the dial it is 528,480, and L^528,480 = I.
- So 2 and 5 come from 641 - 1, and 367 comes from 26,423 + 1: the key's primes through p -+ 1.

Give THIRD8's factorisation and this origin.

(3 + r10)^4 = 721 + 228 r10 lies between 1,441 and 1,442. I checked both bounds: 518,400 < 519,840 < 519,841. The probe checked only the upper one.

### 8. Load breaches

beat_load.txt shows both of the writer's beat runs started at loads of 9.01 and 8.19, above the rule's 8. The text does not name this.

## SOUND

- **The reruns:** families.py, triangle.py and beat.py (400 rounds, 2 minutes) from my copy are byte for byte the frozen outputs.
- **The characters' decompositions (6), and a, b, b under 2O.**
- **The triangle:**
  - B C = 0, K = 3 and B^T B + C C^T = 3 I;
  - the spectra {0, 3, 3} and {2, -1, -1}, from L (L - 3 I) = 0 and (A - 2 I)(A + I) = 0 with traces 6 and 0;
  - m(2') = m(2'').
- **The cat map:**
  - L = [[19, 6], [60, 19]], with trace 38 and det 1;
  - its eigenvalues are 19 +- 6 r10 = (3 +- r10)^2;
  - it is hyperbolic, with exact orders.
- **One beat for every tied train:** the kept forms are identities, since signed permutations are orthogonal.
- **The alike-members ratio:** with every strength at 1, (kt + 2 tie) / (kt - tie) = 1 + 3 / 119,999, which is 25 parts per million.
- **The pair's runaway:** the pair is indefinite exactly where 2 c |k|^2 < tie, which is |k|^2 < 0.8.
- **"Lines per beat read the key and the amplitude."**
- **No fit anywhere:** no nature number is typed in any probe, and no strength or key is picked toward 1,836. The old engine's 1,836.15265582 is rightly named a fit; its citation at ALGEBRA.md lines 324 and 354 checks.

## DERIVED / MEASURED / OVERCLAIMED

**DERIVED, sound:**
- the decompositions;
- the triangle's spectra;
- the tied beat's universality;
- the pair's indefiniteness;
- McMillan for a lone gear.

**MEASURED, sound:**
- the three probes;
- the cat map's order (now with its prime orders).

**OVERCLAIMED:**
- the lone member bound (B1);
- no rotation number for the coupled step (B2);
- "about 0.5" and "about one" (M1);
- "about 245 on the click world" and the beats at the lay (M2);
- "four checks" (M4);
- "up to m beats" for the 8-gear train (M6);
- "own lines" in 1.3 (M5);
- "-I" read as MEASURED when it was a flag (M6).

## Questions for the Boss

1. The held hand at rest at 0, which the click world reaches, frees a lone tied member. Must the electron's design lay the held hand away from 0? That would be an owner's initialization number.
2. May MASS1 cite McMillan's integrability and the height growth on elliptic curves as classical, independent of MIRACLE_A, with every road-A and road-B result marked CONDITIONAL?
3. A ratio reading is blind to a drift shared by construction, and every tied train shares one beat that walks with |k|^2. Is a ratio enough for the decoder's mass row?

## A line on Solution24

MASS1 shows rightly that the structure fixes only equalities and counts, and that node-all cannot yet read a mass in the clicks. But its one positive design claim fails on the invariant line k = 0, so neither base mass's design is shown to be bound by the structure alone.
