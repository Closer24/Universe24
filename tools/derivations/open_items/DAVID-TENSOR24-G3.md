# G3: term 6's four strengths, in clocks, in the tensor algebra, and in the clicks

David, 2026-10-30, 08:3x UTC, for the Boss's TENSOR24_NODE.md 4.2 (term 6: the coupling vertex and the gear's spring), on the owner's words to David (in Hebrew; in translation):

- 07:4x UTC: "Start now" (G3, ahead of term 12 and G2).
- 07:5x UTC: "Of course a mathematician and a physicist reviewer to approve.. note that everything must have the clock's explanation, the algebra's (the tensor's) explanation, and then the physics obtained after the clicks; one can also start from the physics and end with the clock."

This page goes forward (the law's line 35, item (10)): the clock, then the algebra, then the physics. Its first results (#2187 6517738078, probe f89b76a33) went to a hostile mathematician and a hostile physicist, and both refused them; this page's first text went to both again, and each found more; section 5 lists what changed at each reading. The probes, whole numbers alone (Sofer's census finds nothing in them), stand in derive/david_open/node/ with their outputs beside them, read on the head's src (tensor24-review 9751f91c1):

- g3_strengths.py: each kind's spring through an A1 held count; lam's bound, exact and not strict, for one tied family and for several sharing the held count; Animate's operation on the head's gear at four swings, for one family and for two; the two beats;
- g3_kinds_and_parts.py: an E family under four pushes; a family of two parts; the held count's own E potential.

The probes lay g, kappa and n by hand (the head's W, n = 10^6, g n = W div 400, kappa = W div 16) to show the mechanism; this page derives none of the three. Status words as the protocol's: DERIVED and CHECKED, CHOSEN (a value the law leaves to a choice), OPEN and REFUSED.

## 1. In clocks

- **The hairspring.** A family's hand at a Node-clock is pulled only sideways, by its six neighbours, as light's is. It becomes a clock, with a beat of its own (its mass, decision 37), where a hairspring inside its own Node-clock pulls it back toward 0. The hairspring's stiffness is the coupling family's held hand there, k, times a pull per count, g.
- **The held hand's own spring.** The held hand stands wound at n because a spring of its own, kappa, pulls it back to n. Laid off n, it beats by itself, at kappa's beat: a held boson.
- **The stop.** A spring that stiffens as it winds, lam (the four-leg term), stops a large swing from running away. It pulls the gear alone, never the held hand. A large swing still winds the held hand down, since the hairspring pulls on the held hand as the held hand pulls on the gear; past 0 the hairspring pushes the gear out instead of in. The stop takes over what the hairspring loses. At its least it takes over that and no more, so a large swing keeps beating near its mass's rate, the held hand far below 0, while the held hand can follow where the swing pulls it. A stop much stiffer than its least adds a stiffening of its own, and a large swing then beats faster than the mass. So the clock's mass stands between a floor (a swing of about a count a round, board2mass 3.3) and a ceiling at the smaller of two swings, where the stop's excess over its least tells and where the held hand can no longer follow; the held hand's sign does not set it (Animate's 1.7 reads the ceiling at twice the least).
- **What the clock fixes, and what it leaves.** The stop must outpull what the hairspring loses as the held hand winds down: lam at or above g^2 / (2 kappa) for one gear on the hairspring. Several gears on one held hand all wind it down together, so a stop on each gear alone must be as many times stiffer, and then a gear swinging alone has a ceiling; one stop on all their swings together needs only the one gear's least and keeps every gear near its mass. Nothing else is fixed: the pull g, the held hand's spring kappa, the stop's value at or above its least and its form (one stop on all the gears, or one on each), how many counts make n, and which gears hang on the hairspring.
- **Every gear on the one hairspring beats alike.** A gear of any kind and any number of parts hung on the hairspring with the one g gets the one stiffness g n: one mass. A gear of kind E has two hands whose teeth are not square to each other; read in the square's three slots, or with E's own form, it hangs like the others. Read row by row on square teeth with the form's slope, its two ways of swinging would beat apart, which the 24 refuse.
- **Light and the board must hang free.** Light's gears and the board's own (the metric's teeth and grips) must not hang on the hairspring: hung on it, light would beat by itself, a mass, and the board's teeth and grips would get a spring. Light's sideways pull reads only how its neighbours stand against a hand, so turning every light hand by one amount changes nothing, and a hairspring would break that. The board's own hands are read whole, as every gear's teeth and every Mesh's grip, so they have no such turn to keep; why they hang free is a question of its own. The clock answers neither, and a row that says so apart would be a special code, which the law refuses.
- **A held hand with parts.** A held hand of kind E or T2 pulls the three hands of a T1 gear differently, so they beat apart. But such a held hand is itself a family's hand, and its own springs set where it stands: with up to four legs and a three-leg pull of its own, an E held hand stands where two of the three beats meet.

## 2. In the tensor algebra

### 2.1 The operation (4.2, Animate's)

At every Node-clock, every round, x a tied family's hands there and k the held count there: c = sum over i, j of C[i, j -> A1] x_i x_j; P_i = -g k x_i - lam c x_i; Q = -(g / 2) c - kappa (k - n); V = (g / 2) k c + (lam / 4) c^2 + (kappa / 2) (k - n)^2.

### 2.2 One spring for every tied family (DERIVED; CHECKED)

- C[K, K -> A1] is the identity for A1 and A2 and for T1 and T2 (probe (a)), so P = -dV/dx and each such family's hands at k = n get the one spring g n: 64 sign changes in 4,000 rounds against 63.7 from 4 sin^2 (omega / 2) = g n / W (probe (d)).
- **E.** C[E, E -> A1] = G = [[2, -1], [-1, 2]] in the head's oblique basis (e1 - e2, e2 - e3). In the square's three diagonal slots s = (a, b - a, -b), whose sum is 0, c = s . s and P = -g k s - lam c s = -dV/ds: the one spring. Carried back by s = B x (B^T B = G), the same motion on the two oblique rows has c = x^T G x and 4.2's push as written, -g k x - lam c x, which is G^-1 times minus the gradient; the continuous motion keeps (W / 2) r^T G r + (W / 2) k_r^2 + V (r the rows' rates and k_r the held count's, each stepping at the teeth W), so lam's bound bounds an E family too (the mathematician agrees at the second reading). CHECKED (probe (e), (f)): the modes (1, 1) and (1, -1) give 64 and 64 in the slots and on the rows; laid at 10^7 the least lam holds both, and lam 0 runs away (rounds 36 and 26).
  - The push -g k (G x) on unit oblique teeth, the gradient with the wrong inertia (my first results' form), gives the modes the springs g n and 3 g n: 64 and 110, beats in the ratio of the root of 3. The push through 3 G^-1 gives both 3 g n: 110 and 110.
  - The square's three slots let the carries walk their trace (up to 59 counts at a swing of 10^5); the two oblique rows have no trace to walk, at the cost of the table E x E -> A1 holding a 2. The Boss chooses, with that cost named.
- **Two parts.** For a family of two parts, c sums both parts' squares (the turn between the parts keeps it), and each part's push is the one-part push with that c. CHECKED (probe (g)): 64 and 64; both parts laid at 10^7 stay under the least lam and run away at lam 0 (round 36).

### 2.3 lam: the bound DERIVED, the value CHOSEN

- **The identity:** 8 kappa V = (2 kappa (k - n) + g c)^2 + 4 kappa g n c + (2 kappa lam - g^2) c^2. With c >= 0, V >= 0 for every k and c exactly when 2 kappa lam >= g^2; below it the valley k = n - g c / (2 kappa) takes V below 0 at a large c. The bound is not strict: at lam = g^2 / (2 kappa), V = (g / 2) n c on the valley. The least whole lam is the ceiling, (g^2 + 2 kappa - 1) div (2 kappa), one carry.
- CHECKED (probe (b)): the identity on all 1,600 pairs g, kappa up to 40, at three lams and 81 points each; a written point with V < 0 one below the ceiling in all 1,600; my first form, g^2 div (2 kappa) + 1, is one too high in 136 pairs, exactly those where 2 kappa divides g^2. At the probe's numbers the two agree, 4,548,858 (2 kappa lam - g^2 = 11,056,751,168,873,926,210,775).
- **Several tied families share the one held count** (the mathematician's second reading). With C the sum of their c_f and a four-leg term on each family's own c: 8 kappa V = (2 kappa (k - n) + g C)^2 + 4 kappa g n C + 2 kappa lam (the sum of the c_f^2) - g^2 C^2, bounded below exactly when the sum over the families of g_f^2 / (2 kappa lam_f) is at most 1, so N alike families need lam at or above N g^2 / (2 kappa). With one four-leg term on the summed C and one common g, V is the one family's with c read as C, and the one-family bound serves; with the g_f differing, lam at or above the largest g_f^2 / (2 kappa). CHECKED (probe (b2), (c2)): the two-family identity on 72 points; a written point with V < 0 for two families at the one-family least, each with its own term; laid alike at 10^7 and 2 x 10^7 they run away (rounds 66 and 43), and they stay at the two-family least, 9,097,715, and under one summed term at the one-family least. Which four-leg term the one plan lays is OPEN (the united page's 3.8.7).
- **What lam bounds:** the coupled motion, x and k together, by V bounded below and the kept energy. It holds no held hand: it stands in P alone. The held hand's valley is n - g c / (2 kappa); it reaches 0 at c = 2 kappa n / g (50 n^2 at the probe's numbers, a swing near 7.1 x 10^6), and a held hand laid at n swings past its valley.
- **The ceiling is not the held hand's sign** (the physicist's second reading; both readers' third). On the valley, V = (g / 2) n C + (2 kappa lam - g^2) C^2 / (8 kappa) for one family or one summed term: at the bound the stop cancels, on the valley, exactly the pull the hairspring loses. The valley drops the held hand's own motion, so the beat leaves the mass at the smaller of two scales: the excess's, C near 4 kappa g n / (2 kappa lam - g^2), and the held hand's own, x near kappa / g (25 n at the probe's numbers), where following its valley costs as much motion as the gear's own swing; and the held hand follows only while its beat stays well above the gear's. CHECKED (probe (c) to (c4)), sign changes in 4,000 rounds against the mass's 63.7:
  - the least lam, the held hand laid at n: 64, 68, 62, 76 and 78 at 1, 1.4, 2, 3 and 4 x 10^7 (below 0 in 1,933 and 3,131 rounds at 1 and 2 x 10^7), running away at 5 x 10^7 (round 1,627); laid on its valley, 61 and 55 at 1 and 2 x 10^7;
  - a few thousand above the least, as near or nearer: least + 100 and + 3,000 give 67 and 61 at 4 x 10^7, least + 10,000 gives 64 at 2 x 10^7; every lam within about lam / 800 of the bound puts the excess's scale past the step's domain (lam c reaching 4 W near a swing of 2.8 x 10^8);
  - twice the least: 95 and 206 at 1 and 2 x 10^7, the excess's ceiling;
  - two families: laid alike under one summed term, 68 and 69 from n and 59 and 49 from the valley; the first swinging alone with the second at rest, 64 and 62 under one summed term at the one-family least, and 95 and 206 with a term on each at the two-family least, where the lone family's excess, (N - 1) g^2 / (2 kappa), sets a ceiling;
  - the held hand's spring at 25, 9, 4, 2 and 1 times g n (its own least lam, the held hand laid on its valley, at 1 and 2 x 10^7): 61 and 55, 59 and 65, 60 and 72, 52 and 48, 73 and 30, near the mass while kappa stays at or above about 4 g n.
- CHECKED (probe (c)), one family, X laid at rest and K at n; for each lam: the least K, the valley's K at the largest swing seen, and the largest c against its reach (the largest c the kept energy allows on the valley), both in tenths of the laid c:

| laid | lam 0 | the least lam | twice the least |
| --- | --- | --- | --- |
| 10^5 | stays | 999,555; 999,800; 10 and 10 | 999,547; 999,800; 10 and 10 |
| 10^7 | runs away at round 49 | -2,739,187; -1,003,150; 10 and 19 | -3,112,719; -1,005,649; 10 and 13 |
| 2 x 10^7 | runs away at round 29 | -39,861,523; -39,377,640; 50 and 49 | -8,012,331; -7,082,465; 10 and 13 |
| 10^8 | runs away at round 15 | runs away at round 88 | runs away at round 14 |

  - At 2 x 10^7 the least lam lets the swing grow to the root of 5 times its lay, as its reach allows (near the bound a lay x0 reaches x_max^2 of about x0^2 + lam x0^4 / (2 g n)), and the held hand follows the valley to -40 n. The step keeps an energy near this one, so c passes its reach by under a tenth.
  - At 10^8 the reach is near 10^9 and the local spring lam c passes 4 W: that runaway is the step's domain, not lam's.
- **CHOSEN:** any whole lam at or above the bound serves to bound the potential, and every lam within about lam / 800 of it keeps the beat near the mass at the swings the step holds. Taking the least is a choice by minimality, like K-S1's least unit, and owes its sentence (line 100; Sofer, 6517919800, item 1).

### 2.4 kappa and n

- kappa holds the held count at n and sets its own beat: laid off n, 4 sin^2 (omega / 2) = kappa / W. CHECKED (probe (d)): 319 sign changes against 319.2.
- n is the law's one quantum per Node-clock (line 35). Its unit in counts is OPEN: a standing count sweeps no area, so term 11's quantum, counted on the swept area, does not count it.

### 2.5 g, and the freedoms counted

- g sets the spring against W: g n / W = 4 sin^2 (omega0 / 2).
- What the algebra leaves free (both readers' count): g for each tied family, one for all being an assumption; lam's value at or above its bound (CHOSEN), and its form, one four-leg term on the summed c of all tied families or one on each (OPEN; the bound follows the form); kappa for each kind the held count holds (the 24 allow separate springs for an A1, an E and a T2 part); the relative strengths of the vertex's channels (4.2: no single integer serves all tables, OPEN); n's unit (OPEN); which families tie to k (OPEN); and a split held count's own spring, quartic and cubic.
- The held count's components are no freedom: a held count is a family's hand, so it stands where its own potential is least (decision 40 (h): nothing is typed).

### 2.6 A held count with E parts (DERIVED; CHECKED)

- E's invariant forms under the 24, by degree 2 to 6, number 1, 1, 1, 1, 2 (probe (h), a sum over the 24's matrices): x^T G x, one cubic f, at four legs (x^T G x)^2 alone, and a second form first at six legs.
- The act's table C[E, E -> E] is not 0, and f = (G e) . C(e, e) = 9 e1 e2 (e1 - e2) is that cubic: kept by the 24 on 81 whole points, a multiple of the 24's one cubic.
- So an E held count's potential of up to four legs, (mu / 2) e^T G e + (gamma / 3) f + (nu / 4) (e^T G e)^2, depends on its direction through f alone, and at a fixed size its least lies where f is extreme, if gamma is not 0; at gamma = 0 the direction is free at four legs, and only a six-leg term fixes it. The Lagrange form det[grad f, G e] = -9 (e1 + e2)(2 e1 - e2)(e1 - 2 e2): the extremes lie on the three lines e1 = -e2, e2 = 2 e1 and e1 = 2 e2.
- On each line the E part of a T1 family's spring (C[E, T1 -> T1]) is diagonal with two entries alike: (1, -2, 1), (1, 1, -2), (2, -1, -1) and their negatives. Of the 168 whole points off 0 with entries up to 6, the 144 off the lines give three different springs and the 24 on them two alike.
- Three different springs from E alone need a six-leg term of the right sign outweighing the cubic, which moves the least off the lines, or a T2 part, whose own potential then decides where it stands. Either brings its own strengths (2.5).

### 2.7 What a tie breaks (OPEN, a candidate)

- **Light.** Term 4's pull reads only differences of neighbours' counts, so for a family read by the pull alone it keeps a uniform shift of the family's counts: the uniform wave does not beat (board2mass m3). Term 6's spring at a Node-clock breaks that shift for every family tied to k. A law that keeps the shift for light and breaks it for the massive families would keep light off k with no row apart. No such law is derived: OPEN, the candidate named.
- **The metric has no such shift** (both readers' second reading). Every gear's teeth read the metric's 00 slot (W = the rest + that count, term 2) and every grip its ii slots (term 3): absolute counts, not differences. A uniform shift of the metric's slots changes every W and every grip, so the board's step does not keep it, even before term 6; it is invisible only in the clicks (line 695: the tick is no observable), as a constant rescaling of the metric is in general relativity. So the candidate can at most keep light off k, and what keeps the metric off it is OPEN on its own.

## 3. In the clicks (the physics, last)

- **Mass.** A tied family's clicks read its rest beat as its mass (decision 37), between the floor and the ceiling of section 1. With one g, every tied family reads one mass. Nature reads many, so one g for every family is REFUSED by nature: the families must differ in their tie (2.5), which the law does not derive.
- **Light and the metric.** The clicks read no mass for light (the photon below 10^-18 eV, PDG) and none for gravity (the graviton at or below 1.27 x 10^-23 eV, LIGO, Virgo and KAGRA), so neither may tie to k. Nature keeps both massless by a symmetry (the photon's gauge, the graviton's general covariance); for light, the clock's candidate is the shift of 2.7, and the metric's case is OPEN on its own. What keeps them off k with no row apart is OPEN (4.2: which families the plan ties to k).
- **The held boson.** kappa's spring holds the held count at n, as nature's Higgs potential holds its v, and kappa's beat is a held boson's mass. This held boson differs from nature's Higgs boson in three readings:
  - it couples to every tied row with the one g, where nature's Higgs couples by mass (its decay to two muons is seen near the standard rate, CMS 2021; a coupling alike for all would put it near the decay to two taus, about 300 times larger);
  - its vertex k x x on a second-order hand is a scalar three-leg coupling of strength g, the spring over n, growing as the mass squared where a family's whole spring is the A1 count's: the shape of nature's Higgs couplings to the W and the Z, not of a Yukawa coupling; with the one g, rows split by an E or T2 count have different masses and the same coupling;
  - a count held at n by a spring breaks no symmetry, so there is no Higgs mechanism.
  - lam is the tied family's own quartic; the Higgs quartic's counterpart is nu, the quartic of 4.2's hat for the held count.
- **Ratios.** A held count's E or T2 parts split one T1 family's three beats, and the split is alike in every family of one kind and part, while nature's three sectors (the charged leptons, the up quarks, the down quarks) split differently: what tells families apart is OPEN (the united page 3.11.3). With up to four legs an E count splits one beat from two alike, where nature's three masses in each sector all differ (2.6). A standing E or T2 count reads space's axes apart only if some coupling reads its kind index against the board's directions: the metric's shear slots (its kinds are theirs, the united page 3.9.2), the grips, or the gradients. Under 3.9.2's condition its index is the family's own and space stays the same in every direction; the risk is the one plan's vertex to the metric's E and T2 slots, which the cavities bound near 10^-18 and the clocks' comparisons too. Comparing chosen whole parts with nature's ratios would be numerology: the parts must come from the held count's own potential.

## 4. What stands, and what is owed

- **DERIVED:** lam's bound, at or above g^2 / (2 kappa) for one tied family or one summed term, and the sum of g_f^2 / (2 kappa lam_f) at most 1 for a term on each, by the identities; the ceiling not set by the held hand's sign, but at the smaller of the excess's scale and the held hand's own; the one spring g n for every tied family of every kind and part, E read in the square or through its form; the valley n - g c / (2 kappa) and its zero at c = 2 kappa n / g; an E held count of up to four legs least on the three lines where two of a T1 family's springs meet.
- **CHECKED:** each line above with its probe.
- **CHOSEN:** lam's value (the least by minimality); g, kappa and n laid by hand in the probes.
- **OPEN, the next, in this order:** (1) which families tie to k, and what keeps light and the metric off it with no row apart (2.7); (2) the held count's own potential, its kinds and strengths, derived and not chosen; (3) n's unit in counts; (4) the vertex's channel strengths; (5) the four-leg term's form, one on the summed c or one on each family: one summed term keeps every tied family near its mass at every swing the step holds, and makes the tied families' rows interchangeable, so a scattering across families equals one within a family (the physicist's note).

## 5. What changed, by the readers' items

At the first reading (of #2187 6517738078):

1. lam is no ratchet on the held hand (both readers): it bounds the coupled motion, and the held hand falls to -2.7 n and -40 n at the least lam (2.3).
2. The bound is not strict (the mathematician): the least whole lam is the ceiling, and 4.2 reads "at or above" (2.3).
3. lam's bound is DERIVED and its value CHOSEN (the physicist; Sofer's note) (2.3).
4. "Every family gets g n" is restricted to the tied families; light and the metric stay off k, OPEN (the physicist, blocking) (1, 2.7, 3).
5. E's "two rows beat at 1 and 3 times g n" is withdrawn (both): that is the push on unit teeth with the form's gradient, springs g n and 3 g n, beats in the ratio of the root of 3; 4.2's push gives one spring, and its kept energy bounds E too (2.2).
6. The physics layer is rewritten (both): lam is the tied family's quartic; kappa holds the held value and sets the held boson's beat; that boson differs from nature's Higgs in three readings (3).
7. The freedoms are recounted (both): n's unit, a kappa for each held kind, the channel strengths, a split count's strengths; the held count's components are no choice (2.5, 2.6).
8. "Nature's ratios from the held count's parts" is withdrawn, and comparing chosen parts with nature's ratios is named numerology (the physicist) (3).
9. Two parts: c sums both parts' squares (the mathematician, minor) (2.2).

At the second reading (of this page's first text; the physicist's blocking item met, and the mathematician's E item withdrawn on 2.2's argument):

10. The ceiling is lam's excess over the bound, not the held hand's sign: at the least lam the beat stays near the mass's with the held hand below 0, the held hand's lag the rest (the physicist, major; the lag my own check, probe (c3)) (1, 2.3).
11. Several tied families sharing the held count: the bound is the sum of g_f^2 / (2 kappa lam_f) at most 1 for a term on each, the one-family bound for one summed term; which the plan lays is OPEN (the mathematician, major) (1, 2.3, 2.5, 6).
12. The shift candidate holds for light alone: the metric's slots are read whole, as teeth and grips (both, major and minor) (1, 2.7).
13. The quadrupole reads space's axes only through a coupling to the board's directions (the physicist, major) (3).
14. Minor: the kept energy carries W (the mathematician); the cubic's lines need gamma not 0 (the physicist); with the one g, split rows share one coupling (the physicist) (2.2, 2.6, 3).

At the third reading:

15. The beat near the mass at the least lam holds only up to the held hand's own scale, x near kappa / g, and every lam within about lam / 800 of the bound does as well; "alone" is dropped and minimality is the reason (the mathematician, major) (1, 2.3).
16. With a term on each family, a family swinging alone has a ceiling; one summed term keeps every family near its mass and makes the families' rows interchangeable (the physicist, major) (1, 2.3, 4).
17. Minor: the held hand follows only while kappa stays well above the gear's spring (the physicist); one summed term with the g_f differing needs the largest g_f^2 / (2 kappa) (the mathematician); section 3's light candidate (the physicist) (2.3, 3).

## 6. For term 6 (the Boss's TENSOR24_NODE.md 4.2) and the united page (Animate's)

- "the potential is bounded below exactly when lam is above g^2 / (2 kappa)" reads "at or above", and so does "A clock needs both: lam above g^2 / (2 kappa)"; both hold for one tied family or for one four-leg term on the summed c of all tied families with one common g (with the g_f differing, the largest g_f^2 / (2 kappa)). With a term on each family, the sum of g_f^2 / (2 kappa lam_f) is at most 1 (N alike: N g^2 / (2 kappa)).
- "the beat is the mass's only while that shift stays far below n" (the united page's 3.8.7 and 1.7, and 4.2's ceiling beside the floor) reads: the beat is near the mass's at swings below the smaller of two scales, the excess's, C near 4 kappa g n / (2 kappa lam - g^2), and the held hand's own, x near kappa / g, for one family or one summed term; the held hand's sign does not set it.
- "push each gear: P_i = -g k x_i - lam c x_i" stands for every kind, E read in the square's slots (c = s . s) or on the two oblique rows with c through E's form G; never -g k (G x) on unit teeth, never through 3 G^-1; the slots' trace walks by the carries (2.2).
- "both are minus the derivatives of one potential": for E on the oblique rows, minus the derivative raised by E's form.
- The tests tie no light and no metric family to k.
