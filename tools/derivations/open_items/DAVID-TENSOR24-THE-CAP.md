# Item 4, the cap between clicks: from the turning clock, then the family's tensor, then the 24

David, 2026-10-28, 13:5x UTC, for the Boss (Sofer and Animate copied). This page answers the owner's word to David at 12:1x UTC (12:15 by the platform's clock; Hebrew, translated): "Item 4 is something generic, to be understood from the clocks and the tensor, how it is solved from them, and not from a specific law." Item 4 is the cap between clicks: no more quanta of matter gather at one Node-clock than their kind allows. It is the board's "the cap between clicks" (Sofer's open item 3).

The page follows the owner's method of 13:21 and 13:31 UTC: the clock first, then the tensor, then the 24 operations, and then whether a big law is missing above. A helper drafted the derivation, and I reran its five probes; the outputs are identical. I added one check of my own (the junctions carried at a fixed width). All of it is in DAVID-TENSOR24-THE-CAP_CHECKS.txt, with the draft's proofs in full. The draft reads toys-5 b56643b0e (src), engine-5.0-test 08ec59132 (draft E, the protocol) and scribe-5 f32b67cc3 (line 98). This page covers protocol steps 1 to 5: the second hand confirms it, with its tightenings folded in (its section below). Sofer's check and my sign-off follow. No src is pushed.

## 1. In the clock: why the cap needs no law

1. **Every tick turns the hands; it never stretches them.** A turn keeps each hand's length and the angle between any two hands.
2. **Matter's quanta stand at right angles to one another.** Law 7's exchange sign lays each new quantum of matter at right angles to those already there: only its free part, which no occupant holds, is laid. That free part is draft E's free size.
3. **So they stay at right angles between clicks,** because every tick is a turn.
4. **So each state of a Node-clock holds at most one quantum.** A state's occupation is the sum of the squared shadows of the quanta's unit hands on it. Unit hands at right angles cast at most one unit of shadow, in all, on any unit state (Bessel's inequality). A Node-clock with m states holds at most m quanta: 2 for one twin pair, and 4 for the field beside its phase-reversed field.
5. **The force carriers' quanta need not stand at right angles** (their exchange sign is +1), so they stack.
6. **No law of caps is added.** The cap is what a turning clock does to hands laid at right angles. It rests on two things the plan already has: the tick is a turn, and matter's lay is at right angles (law 7's sign, which draft J is deriving from the clocks). PROVED (P15 to P17 in the checks).
7. **What the head lacks** (corrected by section 9: read in the wind's metric, the head's step is a turn, and the cap holds; what it lacks is the quanta held as hands). Its step, cut 0's one formula, is a second-order leapfrog. It is not a turn of the state in the one-slot count. It keeps a two-slot form that is not a length (det D = -N(det[now, before]) <= 0, DAVID-TENSOR24-PAULI.md), so a hand's count can go below 0 and no cap follows.
   - CHECKED (c4): the head's own leapfrog, run on separate hands at the vacuum's gearing and read in the one-slot occupation, breaks the cap at 582 of 1,920 Node-clock ticks on row 0 (up to about 4.37 quanta in one state), and at 2 of 1,920 on row 1. The carried form gives the same.

## 2. The turning clock in the three operations

1. **A tick is three sub-acts, one per axis, each one Mesh long:** W_a = P_a^+ T_+a + P_a^- T_-a. The up sense of the Spoke moves along +a and the down sense along -a. In the clock picture, each sub-act turns the twin pair about the axis by the Spoke's phase: W_a(k) = exp(-i k sigma_a). PROVED (P2).
2. **The formula,** at each Node-clock, with psi- = psi(x - e_a) and psi+ = psi(x + e_a):
   - z: u' = u-, d' = d+ (pure moves, no arithmetic);
   - x: 2u' = (u- + d-) + (u+ - d+), 2d' = (u- + d-) - (u+ - d+);
   - y: 2u' = (u- - i d-) + (u+ + i d+), 2d' = (i u- + d-) + (d+ - i u+).
3. **The mass is a turn on den's circle** between the field (L) and its phase-reversed field (R): den L' = pinion L - i s R and den R' = -i s L + pinion R, with s the engine's own sine_rim. The numbers are 1, i, 2, pinion, s and den: no root, no angle, no table.
4. **It is Bialynicki-Birula's automaton** (arXiv:hep-th/9304070, Phys. Rev. D 49, 6920 (1994)), written on the Spokes. Arrighi, Forets and Nesme (J. Phys. A 47, 465302 (2014)) prove it converges to Dirac's equation. To first order it is Dirac's equation in the chiral form. PROVED (P5).
5. **It is exactly a turn** in rationals (P1). CHECKED (c1): the symbol at 1,200 exact points, the operators on rings of 8, 12 and 16 and on the 3^3 and 4^3 tori, and the full steps, with the calibre's row 0 (den = 15162856759112389).
6. **Its rest beat is the head's,** cos w0 = pinion/den: one reading of the mass (P9). CHECKED (c2, 4 of 4 rows).
7. **Its kinetic term is three times the head's.** Along an axis, cos w_head - c = (cos w_walk - c)/3 exactly, at every k (P10). The walk's light runs one Spoke a tick; the head's runs 1/sqrt 3 of a Spoke at small k. CHECKED (c2: 1,200 of 1,200 along an axis).

## 3. The family's tensor

1. **The state:** rho(x, y) = SUM_k phi_k(x) phi_k(y)^dagger over the family's quanta, held as R / lam, with R Hermitian of Gaussian integers and lam a positive integer.
2. **The step:** R <- (D U) R (D U)^dagger and lam <- lam N(D), where D clears U's denominators (2 (1 + i) den for the field beside its phase-reversed field). These are sums of products on the rows, and the same, conjugated, on the columns.
3. **The lay of a newcomer chi on matter (e = -1):**
   - its free size F = lam chi^dagger chi - chi^dagger R chi;
   - v = lam chi - R chi, then R <- F R + v v^dagger and lam <- lam F.
   - The division by the free size is deferred into the scale, with no root. This is Gram-Schmidt done on the tensor: rho + Q chi chi^dagger Q / (chi^dagger Q chi), with Q = 1 - rho (P16).
4. **The lay on a force carrier (e = +1):** R <- (chi^dagger chi) R + lam chi chi^dagger and lam <- lam (chi^dagger chi).
5. **A newcomer whose free size is 0 has no room in the draw** (cut 1's one comparison over the room), so it is not laid. No "if" is added.
6. **The click's reads at a Node-clock x,** each one Rule3 division by the scale:
   - the count, Tr R_xx / lam;
   - the pair, det R_xx / lam^2, which is the sum of draft E's two-quantum joint sizes there (Cauchy-Binet, P18);
   - a newcomer's free size, which reads a spread quantum's partial occupation exactly (my OPEN on the Pauli page).
7. **The cap read with no root:** the cap holds at x exactly when every sum of principal minors of lam - R_xx is at least 0, the coefficients of its characteristic polynomial. For one twin pair that is its trace and its determinant.
8. **CHECKED (c3), exact, at every Node-clock and every tick:**

   | board and step | ticks | quanta laid (refused) | rho^2 = rho, Tr = N | the cap |
   | --- | --- | --- | --- | --- |
   | ring of 8, U = M W_z on (3, 4, 5) | 200 | 6 (1) | 201 of 201 | 1,608 of 1,608 |
   | ring of 12, the same | 200 | 6 (1) | 201 of 201 | 2,412 of 2,412 |
   | ring of 16, the same | 200 | 6 (1) | 201 of 201 | 3,216 of 3,216 |
   | ring of 12, the calibre's row 0 | 24 | 4 (1) | 25 of 25 | 300 of 300 |
   | 3^3 torus, one Weyl field, 2 states | 40 | 6 (1) | 41 of 41 | 1,107 of 1,107 |
   | 3^3 torus, the field beside its phase-reversed field, 4 states | 8 | 5 (1) | 9 of 9 | 243 of 243 |

   - The refused quantum is the third at a filled Node-clock, where the free size is 0. Two more are laid there once the first two have spread.
   - The tensor equals the laid hands stepped alone, SUM_k phi_k phi_k^dagger / |phi_k|^2 (9 of 9 on each ring).
   - A Node-clock of the field beside its phase-reversed field holds four quanta, and the fifth is refused.
   - The force carriers stack: three in one state read (Tr rho, Tr rho^2, Tr rho^3) = (3, 9, 27), and the local occupation exceeds 1 at 46 of 732 Node-clock ticks.
9. **The mutants fail as they must:**
   - the symmetric lay on matter: an eigenvalue 2, and the cap broken at 15 of 360;
   - one summed field, the head's board: four quanta at one Node-clock in one state;
   - Feynman's checkerboard coin, which is not a turn and grows the hands: the cap broken at 225 of 480. A coin that shrinks them breaks the projector but not the cap (the second hand's (3, 4, 6): 30 of 31 ticks, and 0 of 248);
   - the lay without its denominator.

## 4. The 24

1. **The 24 permute the three sub-acts** (P11). CHECKED (c1): the group generated by diag(1, i) and Q_x has 24 turns, and the operators on 3^3 map as claimed, 24 of 24. As matrices it has 96 elements, since Q_x^2 = i: the 24 turns times the four unit phases.
2. **The junctions between the sub-acts are the 24's own lifts over (1 +- i).** W_a = Q_a S_a Q_a^dagger, with S_a the integer shift:
   - Q_x = [[1, 1], [1, -1]] / (1 - i), the edge half turn's lift;
   - Q_y = [[1, 1], [i, -i]] / (1 - i);
   - Q_z = 1.

   The mass cannot come from the 24, whose lifts turn by multiples of a quarter and a third of a turn. It comes from den's circle, as the engine's pairs do.
3. **One field alone keeps only the tetrahedron's 12 in its beat,** losing the other 12 at third order in k (P12). This holds for Bialynicki-Birula's automaton too.
4. **The field beside its phase-reversed field keeps all 24 and the inversion** (P13). Its beat reads only cx cy cz, (sx sy sz)^2 and SUM sa^2 sb^2. CHECKED, and the mutant without the phase reversal loses 12 of 24. So matter's step is the pair, and the pair's second field is the owner's phase reversal (draft E).
5. **No one-tick step on the six Spokes, or on the eight corners, is covariant under the 24** (P14, a no-go). So the tick must be three sub-acts, which the 24 permute.

## 5. Integers

1. **An exactly unitary step on Gaussian integers of fixed width only permutes states with unit phases** (P6), so it has no interference. Either the scale grows, or the count is kept up to the carry's remainders.
2. **The exact form:** the scale grows by log2 N(D) bits a tick, about 110.5 for the field beside its phase-reversed field at the calibre's den, and a lay into spread occupants roughly doubles the widest integer (c5: 186 to 376 bits). The count is kept and the rewind by (D U)^dagger returns the start bit for bit (c1: 300, 80 and 30 ticks).
3. **The carried form, at a fixed width:**
   - the mass turn as three carried shears is exactly reversible (c1: 400 ticks there and back, bit for bit);
   - **each junction is a unit phase times three shears,** two with coefficients 1 or i (exact) and one with (+-1 +- i)/2 (one Rule3 division by 2, with one fixed rule at its ties, since c times a Gaussian integer can land on a half). Carried, each is undone exactly: 6,000 of 6,000 states return bit for bit, and undoing in the wrong order fails 600 of 600 (my check, junctions.py);
   - so the whole tick runs at a fixed width and rewinds exactly, with no stack;
   - but the count moves by the remainders (c1: a worst relative drift of 1.0e-6 at 10^6 a quantum; the junctions move it at 2,993 of 6,000 states). So the projector and the cap hold up to the remainders, the head's own status for its two-slot form.

## 6. The price, OPEN for the owner

1. **The integers:** a growing scale, or the count kept up to the remainders.
2. **The speed.** If matter walks while the light keeps the leapfrog, matter outruns the light by sqrt 3 at small k. One cone for matter and light needs the light to walk too; not built.
3. **Locality.**
   - The tensor's step reads the coin at both Node-clocks of an entry (P23). With a coin that varies (the Pauli pull, the lapse), a row reads coins beyond one Mesh wherever rho couples the two places: 4 of 64 entries of the row at 0 changed when only a coin 8 Meshes away changed (c5). The ring's walk splits into two parities, and a state on one parity sees no change (the second hand).
   - One hand per quantum, phi_k -> U phi_k, reads only its own Node-clock's coin.
   - The lay's write reaches every row that holds a column at the lay's Node-clock, in either form: this is the exchange hole (c5: 14 of the 26 rows beyond one Mesh changed).
   - A lay that writes within one Mesh exists and is exact (P21), but it refuses every newcomer once the occupants span the Mesh's local states (P22; c5: 21 of 21 refused, all globally free).
4. **The representation:** the tensor (2 m^2 V integers per family and Node-clock, fixed for the run, line 98) with a step that leaves the Mesh, or one hand per quantum (2m integers a quantum, with its norm kept) with a local step and a count that varies. Neither needs a root: a hand that keeps its own norm is read as phi_k phi_k^dagger / n_k. This is the same choice as the composite's (DAVID-TENSOR24-THE-COMPOSITE.md).
5. **The force carriers' state** is not carried by their tensor: two boson pairs with one tensor give 2 and 5/2 in one state after one lay (P19).
6. **The Dirac sea:** a Node-clock of the pair has four states, two at the rest beat's positive frequency and two at its negative. Which of them matter's lay uses is OPEN.
7. **The interacting coin:** the walk's coupling to the lapse and to the Pauli pull is not written. Its exact form is a Cayley coin, (1 - iA)^2 / (1 + |phi|^2) for A = phi . sigma, rational with no root (P4).

## 7. A big law missing above? (the owner's 13:21 and 13:26 words)

1. **The candidate: every tick of every family is a turn of its state.** It is built from the 24's lifts and den's circle.
2. **It does more than the cap:**
   - the count is kept exactly and is positive at every Node-clock;
   - the rewind is the turn's inverse, with no stack;
   - the quanta's overlaps, draft E's sizes, stay fixed between clicks;
   - with law 7's sign, it gives the cap.
3. **It contradicts a small law:** cut 0's one formula as matter's step, the second-order leapfrog. On the owner's word of 13:26 ("If there is a beautiful big law that contradicts small laws, bring it to me for approval"), it goes to him as such, through the plan's section 30, item 11.
4. **For the light,** the same law asks a walk as well. That would also give matter and light one cone (6, item 2). OPEN, not built.

## 8. What it replaces

1. **The OPEN bound between clicks,** in two places:
   - draft E, part 12, item 2: "no bound on the board follows from the step as written";
   - my Pauli page: "between clicks it is kept only by the antisymmetric algebra on the board ... which representation the plan takes is the owner's word".

   It is kept by the turning clock on the family's tensor, one law for every family with the kind's sign.
2. **The head's matter step for the twins** becomes the walk on the field beside its phase-reversed field, with the same rest beat. The two-slot form stops being matter's count.
3. **My cut (d) on the Pauli page** gets a sharper answer: the route needs both the phase-reversed field (for a step that is a turn) and the quanta as a projector (the tensor, or hands at right angles). One summed field gathers (c3).
4. **My direction to the helper had two sentences wrong,** and the draft corrects them:
   - "each entry updates from its neighbours' entries in both indices" holds only for a coin that is the same at every Node-clock;
   - "the click reads rho_xx alone" holds for the draw, not for the write.
5. **A row, proposed:** per family and tick, the cap's principal minors of lam - R_xx at their least over the Node-clocks. On matter it is never below 0; on the force carriers it is free. It would replace row 43's count of lay jams by a reading of the cap.

## The second hand (protocol step 5)

1. **An independent exact probe, written from the claims alone,** confirms all eleven claims: 51 checks with 0 failures, and 23 mutants, each failing as it must. It runs in 44 s, and I reran it: identical. Its guard reads the source before the run (no float, no complex, no true division) and every value as it is recorded. Among its counts:
   - the symbols, operators and full steps unitary on rings of 8, 12 and 16 and on the 3^3 and 4^3 tori;
   - all 390,625 Gaussian 2x2 matrices with parts in [-2, 2]: 32 unitary, and all 32 monomial;
   - one Weyl field's beat kept by exactly 12 of the 24, and the pair's by all 24 and the inversion;
   - the 24 permuting the sub-acts, 24 of 24, with all six permutations of the axes occurring;
   - the tensor a projector holding the cap at every Node-clock and tick on five boards, equal to the hands stepped alone;
   - Lagrange at 3,000 cases, Cauchy-Binet at 1,527;
   - the bosons' 2 and 5/2;
   - the far coin, 4 of 64 entries;
   - the junctions: the same three factorisations as mine, 19,683 of 19,683 carried states returned, and a carried tick on 3^3 run 30 ticks there and back bit for bit, 4 of 4, within 22 bits.
2. **Its tightenings, folded above:**
   - the group as matrices has 96 elements, the 24 turns times the unit phases (section 4);
   - a coin breaks the cap only if it grows the hands (section 3);
   - the junction's rounding needs one fixed tie rule (section 5);
   - the far coin is read where rho couples the two places (section 6).
3. **It also found the pair's beat in closed form:** Tr(U_L(k) U_L(-k)) / 2 = 1 - 2 SUM sa^2 sb^2 + 4 (sx sy sz)^2.

## 9. Sofer's question, answered: the head's own step is a turn in the wind's metric (added 14:4x UTC)

Sofer asked (6471863755, item 1): "In the wind's form (positive, kept by the step: law 8's books) is the step a turn, and does the cap follow by Bessel with no walk, no corners and no growing width?" Yes. This simplifies the page.

1. **The step is a turn in the wind's metric.**
   - The one formula at fixed coefficients is w (a+ + a-) = M a, with M = S + SUM_j R_j shift_j.
   - Its wind is the Hermitian form G = [[w, -M/2], [-M/2, w]] on the two-slot state (a, a-).
   - Wherever M is Hermitian, G(Sx, Sy) = G(x, y) for every two states. M is Hermitian where every Mesh couples its two ends alike, the charge page's condition (QR1). PROVED, since w a+ = M a - w a- gives both sides as w <a, b> - w Re<a+, b-> terms.
   - CHECKED (wind_turn.py, exact rationals, a ring of 8 at three pairs): 18 of 18 random pairs of states over 30 ticks.
2. **The wind is positive for matter.** G is positive definite exactly where M's eigenvalues lie strictly inside (-2w, 2w). At the vacuum that means pinion < rim, so every massive train qualifies; the light sits on the edge, with its zero mode. This is the law's own edge, "D plus twice the grips summed at most 4 w" (line 1909).
3. **So the cap follows by Bessel, with the head's own step.** Quanta laid at right angles in the wind's metric stay at right angles, and every state's occupation lies in [0, 1].
   - CHECKED: 0 of 1,920 site-state ticks outside [0, 1], and the orthogonality is kept at every tick.
   - No walk, no corners and no growing width: the step keeps its one Mesh and all 24.
4. **When the coefficients change from tick to tick** (the regulator, the lapse), the wind is not kept, and the orthogonality is lost (40 of 40 ticks).
   - The cap still holds if matter's state is read as the projector onto its quanta's span, H (H^dagger G_t H)^-1 H^dagger G_t. That is the antisymmetric state's density (P19).
   - It is a projector in any positive metric, and an invertible step keeps the span's dimension, which is the count. PROVED.
   - What a changing clock moves is the quanta's wind, which the books track. The action is what is kept (DAVID-TENSOR24-THE-MASS.md).
5. **What this changes on this page:**
   - **Section 1, item 7, and the c4 mutant:** the head's step breaks the cap only when read in the one-slot count without the quanta's Gram. In the wind's metric it keeps it.
   - **Section 2's walk is one route, not needed for the cap.** Its prices need not be paid: the speed, three Meshes a tick (Sofer: the corners, and covariance only in the beat), and the growing width.
   - **What the head lacks is the representation alone:** one summed field per family gathers (c3). So matter's quanta are to be held as hands, or as their tensor (cut (d)), laid at right angles in the wind's metric.
   - **Section 7's big law becomes:** every tick keeps the books' own metric, the wind. The one formula already does so wherever every Mesh couples its two ends alike. It contradicts no law, and item (q) needs no walk.

## For the Boss and the plan

1. **The cuts** (for the plan, not for an engine before the owner's approval):
   - matter's step: the one formula as it stands, read in the wind's metric, with every Mesh coupling its two ends alike (section 9). The walk (section 2) is the route only if the owner wants a first-order step;
   - each family's quanta: the tensor, or hands at right angles in the wind's metric with their norms (the owner's choice, with the composite's);
   - the lay with the kind's sign, as in section 3;
   - the click's reads: the count, the pair and the free size at a Node-clock.
2. **For the owner, through section 30, item 11:** the big law of section 7, and the price of section 6 (the integers, the speed, locality).
3. **For Sofer:** law 7's sentence on the cap: "between clicks the cap is kept by the turn of the clock on hands at right angles; no bound is written". Line 98's width clause against the owner's ruling (gates.py:178) is for Sofer and me.
