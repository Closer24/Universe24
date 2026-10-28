# Draft A: what a click of a whole writes, the unspringing, and the setting's lay

Drafter A, 2026-10-28, for the Boss's owed list of Tensor24 (TENSOR24.md section 19: "what a click writes", "the unspringing", "the setting's lay"). Read on the head as it stands in the scratchpad worktree t24 (22149d2b2 with the plan's working copy; the engine as at 526a5666d/834cfd72e), with David's files on toys-5 (DAVID-TENSOR24-THE-CLICK, -THE-ORDER-FREE-STRIKE, -THE-LIGHTS-LAST-ROLES, -AMPLITUDES, -THE-MIRRORS-FITTING, -THE-MERGERS-BOOK, -CLOSE-LAW). No file of the repository or its worktrees is changed; every probe is a harness that reads the head or a pure-integer property test, and runs with `python -I` (S/derive/A/p*.py, each output beside it as p*.txt).

This draft covers the protocol's steps 1 to 4 (the formula in the three operations, its proof, an executable probe that can fail, and what it replaces). Steps 5 and 6 (a second, independent hand; Sofer's law check and David's sign-off) are not mine. Every claim is marked **PROVED** (the proof is given), **CHECKED** (with the probe's count) or **OPEN** (with what blocks it).

## 0. The answer in one page

| what | the formula (three operations) | status |
| --- | --- | --- |
| F1, the senses at a Mesh | sigma_e = sgn(h F_(o,e)): the sense of each end is the sign of the twist times the lead flowing into it | PROVED unique up to one declared sign; CHECKED bit for bit with the head at 26,822 oriented engagements and under the 48 at 72,000 Meshes |
| F2, the fitting's write | the drawn train's fitted hand sigma_e (A, i B) at each end e; each end's light pays its own fitted hand's own wind by F3 | PROVED (books, charge, 48, rewind from the record); CHECKED 100 random fittings; the charts move (each end pays its own fitted hand) |
| F3, the take (the payer unwound at one Node-clock by a due) | the steepest notch u_k = -sgn(G_k) [G_k G_k >= G_l G_l], the least count by the ladder of carries s -> ceil(D M / (P - a s)), the zero where the top of the fall cannot pay | PROVED; CHECKED: the ladder's count = the head's least count at all 479 takes where the head's gear is the steepest; F3 keeps the 48 on the running engine as the head does (24 + 24 on the chiral setting) and its rewind is exact (20 of 20 on two charts) with its signed move in the record. OPEN: the ladder is a loop of carries of no fixed length |
| F4, the write's own charge book | write only where c_T dQ_T = 0, dQ_T the sweep the write moves | PROVED; CHECKED against the head's sense and lay jams; OPEN: it states the conservation as a gate, and the step itself does not keep the sweep |
| F5, the unspringing | the pair unwound whole at both ends; at each end (released + r) = q w_l + r' (Rule3); q whole light windings written by F3 at -1 | PROVED; CHECKED 100 random pairs (the fitting read backward); OPEN: its gate W_x + W_y = 0 closes on almost every evolved pair, because the step does not conserve the sweep |
| the chime | the payer unwound by F3 by the windings the chiming hands book | PROVED as F3; OPEN which hand the plan's "the hand unwound" names |
| S1 to S5, the setting's lay | the setting is data laid by the one advance act; the rest turn one Gaussian product and one carry per part; i^p by products; quanta read, never set | PROVED; CHECKED 17 of 17 committed worlds laid bit for bit and 5 ticks alike; the rest turn bit for bit at 341 Node-clocks |

The fakes this replaces (labels of TENSOR24.md section 16): R1, R2, R3 (in part), R6, R7, E16 (in part), E17, the stop, E5 and E4 at the setting, and the setting's searches. What is OPEN is listed in section 12 with what blocks each.

## 1. The words, the marks, and the lemmas of the three operations

**The words** (docs/CLOCK_WORDS.md): the Node-clock x, its six Spokes j, the Mesh (x, y) with y = x + e_a; a train T, its hand at x with the notch now z_now(x) = n3 + i n12 and the notch before z_before(x) = b3 + i b12 (Gaussian integers, the three-o'clock and twelve-o'clock gears), each gear's fine tooth and teeth count; the window of x (x and its six neighbours); the wind E (hands.wind: per gear and Node-clock the carry of (2 own - shared) X by M = 4 Gamma^3 G^2); the winding w_T = 3 key s_T (w_l the light's, at s = rim); the coupling c_T, an integer of the calibre, 0 exactly for the train with no spring (the light: the unsprung hand, known by its integer and never by its name); the sweep W(x) = Im(conj(z_now) z_before) = n3 b12 - n12 b3 (hands.sweep), the charge of a coupled train Q_T = SUM_x W_T(x); the remainder r(x) at each Node-clock (the slack, EX-S1), signed; the fitted hand (child) of sense sigma, (z_now, z_before) = (sigma A, i B) with A B = key div 2 (MS-S1).

**L0, the whethers as quotients. PROVED.** For an integer n and d > 0, with div the floor of Rule3:
- n div (n n + 1) is -1 where n < 0 and 0 elsewhere (|n| < n n + 1). So
- sgn(n) = n div (n n + 1) - (-n) div (n n + 1);
- [n >= 0] = 1 + n div (n n + 1);
- [n = 0] = 1 + (-n n) div (n n n n + 1);
- ceil(n / d) = (n + d - 1) div d.

CHECKED: 0 off at 200,008 integers (p2_senses.txt), 100,001 (p4_charge_gate.txt) and 6,001 plus four of 150 and more bits (p5_write.txt). These make every whether below a quotient, as section 26 of the plan asks. They do not by themselves make a rule derived: each use below stands on its own formula.

**L1, the link's two bilinears. PROVED.** At the Mesh (x, y) the time-link bilinear is B_xy = conj(z_now(x)) z_before(y) - conj(z_before(x)) z_now(y).
- Its real part is the lead, F_xy = SUM over the gears (now_x before_y - before_x now_y) (meshes.mesh_lead, train_lead). F_yx = -F_xy.
- Its imaginary part, Im(conj(z_now(x)) z_before(y)) + Im(conj(z_now(y)) z_before(x)), is the Mesh's sweep, even under the exchange of the ends (2 W at x = y).
- The same-time bilinear conj(z_now(x)) z_now(y) has the dot as its real part and the charge current J_xy = Im(conj(z_x) z_y) (hands.lead's term) as its imaginary part.

**A correction to the plan's words (CHECKED, p2_senses.txt).** Section 27 says the Mesh's wind is read by "conj(z_x) z_(x+j): its real part is the dot, and its imaginary part the lead". The head orients every fitting by F, the real part of the time-link bilinear, and J cannot stand in for it:
- on nature the light is real (no twelve gear) and J = 0 at all 1,262 Meshes the light engages;
- on the hole, J = 0 at 4,565 of 13,586;
- on the one big bang J is never 0, but sgn J = -sgn F at all 768 (a travelling wave: F goes as -sin k sin omega, J as sin k).

So the orienting lead is Re B_xy, and the plan's sentence should read so.

**L2, the twist. PROVED.** With u(k) = SUM_b e_b [F(k, k - e_b) - F(k, k + e_b)] (the net transverse lead, meshes.train_twists), the twist of the Mesh is h = e_xy . (u(x) x u(y)).
- The head computes it at the +a end, from the transverse pair (b, c) = (a + 1, a - 1).
- It is even under the exchange of the ends (e_yx = -e_xy, and u(y) x u(x) = -(u(x) x u(y))): a reading of the unoriented Mesh.
- Under g in the 48, F moves with the Mesh and u(gk) = g u(k), so h -> det(g) h, since (g u) x (g v) = det(g) g (u x v). It is a scalar of the 24 and a pseudoscalar of the 48.
- Under z -> lambda z (lambda real): F -> lambda^2 F and h -> lambda^4 h. Under the hand's units z -> i z, -z, -i z and under conj, F and h are unchanged (Re(conj(eps n) eps b) = |eps|^2 Re(conj(n) b)).

CHECKED: the pure lead and twist of p5_write.py equal the head's train_lead and train_twists at 375 Meshes, 0 off.

**No train known, and no number. PROVED, by reading each formula below.**
- F1 to F5 and S1 to S5 read only these: the hands' notches and fine teeth; the gearing's integers (the teeth count, the hold, the six grips, the stretch); the windings; the fitted hand's (A, B); each train's coupling c; and the train's kind (one hand, or twin hands).
- A train enters by its integers alone. The payer and the receiver are "the hand whose c is 0", and the fitted train is drawn by the sizes c.
- The only numerals in the formulas are 0, 1 and 2 = 1 + 1 (the central difference's halving and the vertex's), as the protocol allows. M = 4 Gamma^3 G^2 is hands.wind's own carry and w = 3 key s the head's winding, both read from the calibre and neither added here. The 14 and 15 of the bounds belong to the proofs, not to the formulas.
- There is no clamp: abs(G) is written sgn(G) G, and every whether is a quotient (L0).
- There is one loop, the ladder of carries: section 3, OPEN 1.

## 2. F1: the senses at a Mesh (replaces E17's typed rule and the jams `orientation` and `twist`)

**The formula.** At the Mesh (x, y), read from the hand whose quanta meet (the giver), the sense of the fitted hand laid at the end e is

    sigma_e = sgn(h F_(o,e)),   o the other end

with sgn as in L0. In clock words: each end takes the sign of the twist times the lead flowing into it.

**PROVED.**
1. sigma_x + sigma_y = 0 at every Mesh, since F is odd under the exchange of the ends and h even. So the pair's charge is 0 by the formula, and no sense is typed.
2. sigma_x = sigma_y = 0 exactly where h F = 0. The formula's zero lays nothing, and so replaces the two jams by name `orientation` (F = 0) and `twist` (h = 0).
3. Under the 24 the senses move with the image Mesh. Under a mirror h -> -h, so the fitted hands are exchanged at the image ends (CP kept, P and C broken: the law's own pattern, DAVID-THE-MIRRORS-FITTING.md).
4. **Uniqueness.** Take any placement sigma_e = g(h, F_(o,e)) with values in {-1, 0, 1} that is
   - (a) odd in F (the charge book of every Mesh: sigma_x + sigma_y = 0);
   - (b) odd in h (a mirror exchanges the two fitted hands);
   - (c) read from the two orientations alone, the lead's direction and the twist's hand, as the law's sentence reads them ("oriented by the light's current, and the + fitted hand by the twist"), and not from their sizes. A size rule would compare h with c F^2 for some typed c.

   Then g(0, .) = g(., 0) = 0 by oddness, and g(s_h, s_F) = kappa s_h s_F with kappa = g(1, 1). So F1 is the only such rule up to kappa in {-1, 0, 1}.
   - kappa = 0 lays nothing.
   - kappa = +1 is the head's.
   - kappa's sign is the one declaration left: which hand of the twist goes with which charge, the one-hand coupling's sign. OPEN, the owner's.

**CHECKED** (p2_senses.txt, a harness on click.engage).
- F1 equals the head's + and - ends at every engagement the head orients:
  - nature, 60 ticks: 1,262 from the light and 8,423 from coupled pairs;
  - the hole, 60 ticks: 13,586 and 2,783;
  - the one big bang, 12 ticks: 768.

  That is 26,822 of 26,822.
- sigma = 0 at every jam by name `orientation` or `twist`: 185, 1,200 and 1,344.
- Under the 48 on random fields (p5_write.txt): 36,000 of 36,000 Meshes alike under the rotations and 36,000 of 36,000 exchanged under the reflections, with sigma_x + sigma_y = 0 at all 72,000.

**What it replaces.** E17 (the pair set at senses -1 and +1, the + end by the twist's sign): the senses are now one sign of one product, derived up to kappa, their sum 0 by the lead's oddness. The jams `orientation` and `twist` become the formula's zero. The charts do not move (bit for bit).

## 3. F3: the take, the payer's unwind at one Node-clock (replaces R7, the head's least_at search, and the stop's refusal by name)

Every click of a whole pays through one act: the payer, the hand with c = 0 at the Node-clock, gives a due D of wind (in wind units). The head's chime, the head's fitting and the head's split all pay this way (unspring.fall_of at going 1). Its inverse, the payee advanced by a due, is the unspringing's light (fall_of at going -1).

**The wind as a quadratic in one gear's notch. PROVED.** Fix every integer of the great clock but the payer's notch now at x. The window's exact numerator N = SUM over the window and the gears of (2 own - shared) X is then SUM_k [a n_k n_k + beta_k n_k] + const, separate in the two gears, with
- a = 2 w X, the bend, the same for both gears (w the teeth count at x, X the stretch at the tick's start);
- beta_k a linear form of the window's other notches.

The reason: own(x) holds w n n and n times the befores alone; every shared term SUM_j R_j (b - b_j)(n + n_j) is linear in each notch now; a neighbour's own reads only befores of x. So the slope of the wind on gear k is exactly

    G_k = (N(n_k + 1) - N(n_k - 1)) div 2 = 2 a n_k + beta_k,   a = (N(n_k + 1) + N(n_k - 1) - 2 N(n_k)) div 2

with both divisions exact, the central difference of a quadratic.

**The formula F3.**
- The steepest notch: u_k = -sgn(G_k) [G_k G_k >= G_l G_l]. This is the gear of the larger slope, both gears where they tie, moved down its slope.
- The fall of s units: f(s) = s P - a' s s, with P = -SUM_k u_k G_k >= 0 and a' = a |u|^2.
- The top of the fall: s_v = (P + a') div (2 a'), the nearest whole count to the vertex.
- **The zero:** where s_v P - a' s_v s_v < D M, the payer cannot pay and nothing is written. This replaces the stop's refusal by name.
- **The count:** the least s with f(s) >= D M, by the ladder of carries s_0 = ceil(D M / P), s_(j+1) = ceil(D M / (P - a' s_j)), to its fixed point.
- **The write:** z_now(x) += s u. The fall F is the window's wind before less after (with its carries), and r'(x) = r(x) + F - (the windings booked), where D = (the windings booked) - r(x): the remainder pays first, as in EX-S1.

**PROVED.**
1. **The ladder is exact.**
   - s_0 <= s*, the least count, since f(s) <= s P.
   - If s_j <= s* then s_(j+1) <= s*, since s* (P - a' s*) >= D M and 0 < P - a' s* <= P - a' s_j.
   - The ladder is monotone, because s -> ceil(D M / (P - a' s)) is non-decreasing below the vertex.
   - A fixed point s = ceil(D M / (P - a' s)) has f(s) >= D M, so s >= s*.

   So the fixed point is s*, and s* <= s_v.
2. **The write is local.** Only the window's winds move, so the great clock's fall is the window's.
3. **The books.** SUM over the Node-clocks (wind + remainder) falls by exactly the windings booked, which leave as the click's quanta.
4. **The bounds.** The carried window differs from N / M by less than 1 per gear and Node-clock (14 in all), and f(s*) - f(s* - 1) < P. So D - 14 < F < D + P div M + 15: the remainder moves by the overpay, one notch's fall at most.
5. **The hand's units and the conjugation.**
   - Under z -> eps z at every Node-clock (eps in {i, -1, -i}), the two gears' numerators exchange (each is even in its gear), so G -> eps G, u -> eps u, and s and F are kept.
   - Under conj, u_12 -> -u_12.

   So the gear is chosen by no index: on a tie both gears move.
6. **The 48.** G is a sum over the window read through the Spokes, so on the imaged great clock (the grips with their Spokes, the stretch with its Node-clock) the take at the image Node-clock is the same (u, s, F).
7. **Free of order.** The numerator holds no product of two Node-clocks' notches now. So takes at different Node-clocks add exactly in the numerator, and after the carries within 1 per gear at each Node-clock both windows hold (4 for two neighbours). Every take is read on the tick's start board, as David's order-free letter asks.
8. **The rewind** from the click's record (x, u, s): z_now(x) -= s u, the fall read again, r restored. The direction must be in the record. The head's undo infers it as toward the before, which is the head's rule and not F3's (CHECKED below).

**CHECKED.**
- p3_take.txt, a read-only harness on the head's own takes (nature 60 ticks, 522 takes; the hole 60, 537; the bang 12, 64):
  - the ladder's fixed point is the head's least count at every take where the head's gear is the steepest: 188 of 188, 259 of 259 and 32 of 32;
  - F3 pays wherever the head pays (0 exceptions);
  - the head stops where F3 pays (F3's zero read at the whole top) at 211 and 144 takes;
  - 171 and 84 of the head's stops come from R7 naming a gear whose notch now equals its notch before (no direction), the empty twelve gear of a real light;
  - one carry alone (the linear count) equals the head's at 182 of 188, 205 of 259 and 32 of 32;
  - the ladder takes up to 19, 7 and 0 carries past the first;
  - no tie of the two slopes occurred.
- p5_write.txt, 400 random draws (the head's integers, random fields, the vacuum or random rates):

  | property | count |
  | --- | --- |
  | the least count | 400 of 400 |
  | the fall inside its bounds | 400 of 400 |
  | local | 400 of 400 |
  | the books | 400 of 400 |
  | the rewind bit for bit | 400 of 400 |
  | covariant under i, -1, -i and conj | 400 of 400 each |
  | alike under a drawn image of the 48 | 400 of 400 |
  | the inverse within its bounds | 400 of 400 |

- p8_images.txt, the head's own images test (the chiral setting, 14 ticks, its 48 images) with F3 put in the running engine:
  - the rotations alike 24 of 24, the reflections alike with the fitted hands exchanged 24 of 24, as on the head;
  - with 173 chimes against the head's 93 and 405 stops against 477.

  On the hole (p8_images_hole.txt, 20 ticks) F3 again matches the head: the rotations alike 24 of 24 both ways, and the reflections 0 of 24 both ways, with 63 chimes against 3. The head's reflections part on the hole already by tick 16, before any of this draft's writes would act (the same file's 16- and 17-tick runs). That is the head's, and not read further here.
- p10_rewind.txt, 20 ticks forward and back:
  - the head: 20 of 20 on nature and on the hole;
  - F3 with the head's undo: 2 of 20 on nature, and the hole breaks (the undo moves toward the before where F3 moved down the slope);
  - F3 with its signed move in the record: 20 of 20 and 20 of 20.

**What it replaces.**
- R7 (unspring.py:53, the paying gear the largest now^2 - before^2, the first by index on a tie): the gear is the steepest slope, both on a tie. This also removes the head's 171 and 84 spurious stops.
- The head's least_at search (a root search) becomes the ladder of carries.
- The stop's refusal by name becomes the top of the fall's zero.
- The charts move: on nature 173 chimes against 93 by tick 14, and 516 against 395 by tick 20; on the hole 63 chimes against 3 by tick 20.

**OPEN.**
1. The ladder is a loop of Rule3 carries whose length is not fixed: up to 19 on the charts, 41 on random dues near the top. Under the protocol's "no loop that makes a formula", the exact least count has no fixed formula that I know.
   - One carry (the linear count) is a fixed formula. It is exact at 419 of 479 head's takes, and elsewhere leaves a signed debt in the remainder below a' s^2 div M (CHECKED within its bound at 881 of 881).
   - Whether "the carry carried until it stands", a ladder of carries on one gear, is one act is the owner's word, or Sofer's.
2. The inverse from a hand with no slope at all (G = 0 on both gears) has no steepest notch. Any choice there is a choice by name, as the head's (the three gear, the tie's sign -1). It never occurred on the charts.

## 4. F4: the write's own charge book (replaces R1 and the charge part of E16's lay jam)

**The formula.** A click of a whole writes the notches of a coupled train T only where the charge its write moves is zero:

    c_T dQ_T = 0,   dQ_T = SUM over the written Node-clocks e of [ W(z_e + d_e) - W(z_e) ]

with the indicator [dQ = 0] of L0. Since W(z + d) - W(z) = W(d) + X(z, d), with X(z, d) = Im(conj(z_now) d_before) + Im(conj(d_now) z_before) (the sweep's cross term with the hand standing there):
- **at a fitting**, d_e = sigma_e (A, i B), W(d_e) = sigma_e e with e = A B, the sum 0 by F1, so dQ_T = X_x + X_y;
- **at an unspringing**, d_e = -z_e (the hand unwound whole), so dQ_T = -(W_x + W_y).

**PROVED.**
1. With the gate open, the write keeps SUM_T c_T Q_T exactly. The light carries no charge whatever its sweep, c = 0.
2. **The charge is no sum of notches.** q fitted hands at one Node-clock written as one hand, (q sigma A, i q B), carry the sweep q q sigma e and not q sigma e. A hand of the sweep q sigma e at the least wind would need the root of q. So law 5's "q whole quanta" cannot be laid as q pairs on one Mesh: the fitting lays one pair per Mesh per tick, whatever the giver's quotient q, and the rest of the giver's wind stays with the giver. The book (the pair's total, q q (sigma_x + sigma_y) e = 0) would not forbid it; the quantum does.
3. **Equal charges at one Node-clock.** k fitted hands of one train at one Node-clock, of senses sigma_i on zero gears, write W = k e SUM sigma_i against their own SUM sigma_i e. The excess is (k - 1)(SUM sigma_i) e, zero only for k = 1 or opposite senses summing to 0. So two equal charges of one train never land at one Node-clock in one click: a Pauli-like exclusion of equal charges at a Node-clock, from the sweep's quadratic form alone. It is not Pauli's exchange sign, which is law 7's.

**CHECKED** (p4_charge_gate.txt, a harness on click.jam, every candidate the head judges; and p1_charge_books.txt).
- **The unspringing:** the head's R1 passes every pair of opposite signs. Of its candidates, W_x + W_y = 0 at only 69 of 8,469 (nature), 84 of 2,836 (the hole) and 1,408 of 1,408 (the bang).
  - Of the 6 unspringings the hole actually makes in 60 ticks, 3 change the charge: their pairs held 2,938, -4,987 and -21,882 sweep units (e = 18,000), and the unwind removed them.
  - So the head's annihilation rule does not conserve the charge.
- **The fitting, coupled fitted trains:**
  - the head jams by standing (wind above 0 at an end) where F4 would write (the cross terms cancel): 93 of 962 (nature), 1,826 of 10,223 (the hole), 128 of 576 (the bang);
  - the head passes where F4 refuses: 2, 2 and 0. These are hands standing at a wind of 0 or less, which the head's wind test misses, and whose lay would change the charge.
- **Crowds** (two or more fitted hands of one hand at one Node-clock, all jammed by the head): the summed write's book closes at 88 of 219, 394 of 910 and 320 of 320, of them 74, 293 and 320 with one + and one -.
- Every fitting the head actually lays keeps the charge: 3 of 3, 22 of 22, 64 of 64.

**What it replaces.**
- R1 (click.py:95, a merger only as a conjugate pair, else jammed `sense`) becomes the charge book W_x + W_y = 0.
- The charge part of E16's lay jam (click.jam's `standing`) becomes X_x + X_y = 0.

**What it is, and the charge against it.** F4 does not derive the charge's conservation from the write. It states the conservation as the write's gate, by a computed integer and not by a name, which is the plan's own replacement for R1 ("the sweep's conservation at the click"). The charge stays exact without the gate only where the write is fresh: fitted hands on empty ends (F1's oddness) and a pair just laid. Elsewhere any write of a coupled train moves charge, and the gate is what refuses it. Sofer's check may read F4 as a rule written for its phenomenon; that charge is answered only by a step that keeps the sweep (OPEN 1 below).

**OPEN.**
1. **The step's own charge drift.** CHECKED, p1_charge_books.txt: the step (law 2 with its carries and the Mesh's turn) does not keep SUM_x W_T.
   - On nature the three coupled trains' charges change at 55, 51 and 44 of 60 ticks, by up to 21,792 in one tick (1.2 e).
   - On the hole they change at 44, 46 and 48 ticks, by up to 40,028 (2.2 e).
   - The bang keeps it through 12 ticks.

   So "the charge's conservation, derived from the one formula" (section 19) does not hold on the head bit for bit. A pair laid at -e and +e drifts, and F4's exact gate then closes on almost every evolved pair (the counts above). The step's carry that would keep the sweep exactly is owed: law 2, David's. Until it stands, F4 conserves the click's charge exactly on a board whose step does not.
2. **Lays over standing matter.** F4 opens the lays over a standing hand of the same train whose cross terms cancel (93, 1,826 and 128 above). Their wind's cross term then goes to the remainder, signed, and not bounded by one notch's fall. Whether matter may be laid where matter stands is Pauli's (law 7, owed), and so is the setting's refusal by name (assembly/setting.py, "Pauli at the setting"). E16 is replaced here in its charge part alone.
3. **Crowds that close.** An opposite-sense crowd could be summed and written. Doing that free of order needs an iteration, because a refused fitting changes its other end's sum. So the crowd's jam of all its fittings is kept here as the order-free strike's own letter (DAVID-THE-ORDER-FREE-STRIKE.md, item 3), and not as E16.

## 5. F2: the fitting's write (the click of a whole at both ends of a Mesh)

**The formula.** At the Mesh (x, y), every read on the tick's start board:
1. **The whether** (law 5, the head's engagement): the giver, the hand with c = 0, holds a whole winding at both ends, q(x) = E(x) div w_l >= 1 and q(y) >= 1, and neither end is stopped.
2. **The senses:** sigma_x, sigma_y by F1, read from the giver's lead and twist.
3. **The fitted train:** drawn among the hand trains by their sizes (section 7).
4. **The fitted hands:** d_e = sigma_e (A, i B) on the drawn train at each end. For twin hands, the - end on one of the train's two hands and the + end on the other. On the head, the - end takes the hand the draw named and the + end its twin (hands.twin_of). Here the twin train is one part of the draw, so the - end takes its first hand by the calibre's order. Which twin takes which sense is not derived here: OPEN, with the twin hands' own derivation (11 a).
5. **The gate F4:** c_T (X_x + X_y) = 0.
6. **The payment:** each end's giver pays its own fitted hand's own wind. The due at e is the fitted hand's wind alone on zero gears over e's window: the same integer for every train and every Node-clock of one load (unspring.fitted_windings_of), 1,010,027 millionths of a light winding by the carry (CHECKED, p9_fitted_train.txt, at all four trains). It is paid by F3 at e. F3's zero at either end writes nothing.
7. **The books per end** (David's order-free book): each end's remainder takes its own write's fall over every train, read alone on the start board, and every Node-clock the cross term arising there.

**PROVED.**
1. **The charge:** dQ_T = 0 with the gate open; on empty ends, by F1 alone.
2. **The books** are exact: SUM over the Node-clocks (every train's wind + every remainder) is unchanged, since a fitting moves wind between trains and none leaves. Each end's remainder moves by its take's overpay (section 3, item 4) and the cross term at that end.
3. **The two takes commute** exactly at the numerator: no now-now product (section 3, item 7). The two fitted hands' own cross term is 0 for the shape (sigma A, 0 | 0, B) on zero gears at two neighbours: their befores lie on the twelve gear and their nows on the three. So the cross terms are the carries' alone.
4. **The 48:** F1 (item 3), F3 (item 6), and the draw (law 9, fair under the 24 by cut 1, not mine).
5. **The rewind** from the record (the senses, the train, each end's (u, s)), bit for bit.

**CHECKED** (p5_write.txt, 100 random fittings):

| property | count |
| --- | --- |
| dQ = 0 on zero gears | 100 of 100 |
| the two takes' joint fall equals their two falls alone, within 4 | 100 of 100 |
| the books exact | 100 of 100 |
| the cross terms only at the two ends | 100 of 100 |
| each end's remainder inside [kappa, kappa + one notch's fall) | 200 of 200 |
| abs(kappa) below a hundredth of a light winding | 200 of 200 |
| the rewind bit for bit | 100 of 100 |
| alike under a drawn image of the 48, the fitted hands exchanged by a reflection | 100 of 100 |

**What it replaces, and what it changes.**
- The head pays both fitted hands from the end the lead flows into (one take of two windings). F2 pays each at its own end: the local book David names for the owner's word (DAVID-THE-LIGHTS-LAST-ROLES.md (a) 4). The charts move: a fitting now needs each end's light to pay its own fitted hand. This is not measured on the running engine here; only F3 was put in it (p8, p10).
- R2's "family picked at number 0" and R3: section 7.

**A contradiction with nature, inherited and not resolved here (CHECKED, p9_fitted_train.txt).** A fitted hand at one Node-clock costs the same 1,654,009,903,854,256,729,287 of wind for every train: the light lift, both heavy trains, and the light itself. That is 1,010,027 millionths of a light winding. So the fitting's threshold does not depend on the mass, and E = mc^2's threshold is not in the one-Node-clock lay. The light lift's own winding is 536 millionths of a light winding: its fitted hand is born holding 1,882 of its own windings and a remainder. A pair at its own rest form would cost rim / s light windings, 1,863 for the light lift (DAVID-AMPLITUDES.md section 5). OPEN: what a fitted hand's shape is, so that a pair costs its own two quanta.

## 6. F5: the unspringing, a pair returned to the light (its own click; the fitting read backward; with its books)

**The formula.** At the Mesh (x, y), every read on the start board:
1. **The whether** (law 5): the coupled train T holds a whole winding of its own at both ends, E_T(e) div w_T >= 1, and neither end is stopped.
2. **The gate F4:** W_T(x) + W_T(y) = 0. No lead and no twist are read. The light the pair returns carries no charge, so nothing at the unspringing has a sense (as the head already writes: "the end's sense enters no notch of the unsprung windings").
3. **The receiver:** the hand with c = 0, the one part. There is no draw.
4. **The unwind:** T's hand at x and at y unwound whole, z_T(e) -> 0, all four notches. A coupled hand's quantum at a Node-clock is its whole notches, so no count is sought (DAVID-THE-LIGHTS-LAST-ROLES.md (a) 2).
5. **Rule3 at each end:** with rho_e the window's fall of T for e's unwind alone, read on the start board, rho_e + r_e = q_e w_l + r'_e, 0 <= r'_e < w_l. q_e is the number of whole light windings the end writes, the event's quanta.
6. **The write:** the receiver at e advanced by q_e w_l by F3 at -1: the steepest notch up its slope, the least count by the backward ladder s -> s - (R(s) - D M) div (R(s) - R(s - 1)) from ceil(D M / P). R(s) = s P + a' s s is convex, so this ladder stays at or above the least count and stops on it.
7. **The books per end**, as at the fitting.

**PROVED.**
1. **The charge** moved is -(W_x + W_y), so the gate keeps it exactly.
2. **The books** are exact, with each end's Rule3 remainder in [0, w_l). The receiver's rise is at most q_e w_l + one notch's rise + 15. That is the backward ladder's proof: moving back d = (R(s) - D M) div sigma notches lowers R by at most d sigma, sigma the last notch's rise being the largest, so the ladder never passes below the least count, and its stop R(s) - D M < sigma means R(s - 1) < D M.
3. **The 24,** per end and per Mesh.
4. **The rewind** from the record (each end's unwound notches, the receiver's (u, s), r_e).
5. **The fitting read backward.** On a pair just laid by F2 and read before any tick, F5 returns at each end the whole light windings the fitted hand's wind and the remainder hold, and keeps the rest in the remainders. The energy of the fitting comes back exactly by the books, not the notches: the light's notches are not those it had, since F3 went down the slope and F3 at -1 comes up it from another place. The notch-exact inverse is the rewind with the record.

**CHECKED** (p5_write.txt, 100 random pairs read just after their fitting):

| property | count |
| --- | --- |
| the gate open | 100 of 100 |
| the end's Rule3 remainder in [0, w_l) | 200 of 200 |
| one whole light winding written at an end | 200 of 200 |
| the books exact | 100 of 100 |
| each end's remainder within one light winding of where it started | 200 of 200 |
| the charge moved -(W_x + W_y) | 100 of 100 |

On the head (p4, p1), as in section 4: the gate closes on almost every evolved pair, and 3 of the hole's 6 unspringings would remain.

**What it replaces.**
- R2 (click.py:90, 96 to 106: the pair at rest by its own branch, the + end by the sweep, the twist not read, the train picked at number 0 with no draw). The rest branch and the moving branch become one gate. The + end goes, since no sense is written. The receiver is the one part with c = 0, so there is no draw and no number.
- R1 (section 4).
- **The stop** (the unspringing jammed below the light's quantum): the Rule3 quotient. An end whose released wind and remainder hold no whole light winding writes no light, and its wind stays in its remainder, below one light winding. This is "the click of a whole: a whole winding of the light, nothing else" (section 22 of the plan) made a formula.

**OPEN.**
1. With q_x >= 1 and q_y = 0, the pair is gone and one end's energy waits in its remainder. Whether the unspringing should instead ask q >= 1 at both ends (the zero otherwise) is the owner's word, within his E = mc^2 example (A2, Sofer).
2. The gate W_x + W_y = 0 on evolved pairs waits on the step's charge (section 4, OPEN 1).

## 7. The fitted train (R3) and the receiver

**The formula.** The fitting's fitted train is a click of a split among the hand trains. Every hand train is one A1 Gaussian integer, and A1 times A1 holds A1, so the product table admits every hand train; a twin train is one part of two hands. The sizes are the couplings, sigma_T = c_T. The light's own size is c = 0, so the light is never fitted from the light. The pick is the plan's law 6 form, c SUM sigma = t room + r_t, the part whose running sum brackets t, the parts in the calibre's order, with c and room from the draw (law 9). The unspringing's receiver is the train with c = 0: one part, no draw.

**PROVED.**
- The odds are sigma_T / SUM sigma, exact where SUM sigma divides room.
- No train is named: the couplings are the calibre's integers.
- The parts' order is the calibre's and is not acted on by the 24.

**CHECKED** (p9_fitted_train.txt).
- No fitting on the charts sets light into light: SL-S3's 300, 3,363 and 192 candidates are all jammed by the head, since the light stands everywhere (p4).
- With the head's coupling min(spring, 1), the sizes are (1, 1, 1) for the three matter trains, which are the head's even odds among them.

**OPEN, and a contradiction with nature.** With R4's word, "the coupling the spring itself", the sizes give the light lift 86 billionths of the fittings and the two heavy trains 502,415,788 and 497,584,125 billionths (p9). In nature the lightest charged pair is the commonest. The sizes are the owner's (R4), and this draft does not decide them.

## 8. R6, the split's gate, and the chime

**R6** (bobs.py:160: a split clicks only where light arrives, the light's lead over the six Meshes not 0). Replaced by the split's own whether, the parts' sizes alone (neither twin holding a whole winding, the two together holding one, at the pair's beat), and the payment's own zero (F3). No light-arrival read remains. E1, the split's root, is not mine.
- CHECKED (p6_split_gate.txt, the hole and nature with every matter train made twin hands, in memory only, 60 ticks): 4 split-due Node-clocks on the hole, all with light arriving, and none on nature. So R6 blocked no split on these worlds, and its replacement reads them alike.
- OPEN: a world where a due split meets no arriving light, to read the difference.

**The chime** (one hand at one Node-clock). The head's chime is the detector's click. The hands H chiming at x book their windings T_w = SUM_H w_H, one each per beat on the head (law 5 would book q_H w_H, the owner's word). The payer at x is unwound by F3 by D = T_w - r(x), one take per Node-clock and payer (the dues summed), and r' = r + F - T_w. F3's zero writes nothing. Its books, 48, rewind and bounds are F3's (section 3). The still chime (R5) is not in this draft.

OPEN: the plan's sentence "the hand unwound by q windings at the chime" may mean the chiming hand itself.
- For a coupled hand that is F5 at one Node-clock: its whole notches, Rule3 into light windings.
- F4 then lets it fire only where the hand's sweep there is 0, so a charged bob could never chime away.
- Which reading the plan means is the owner's.

## 9. The setting's lay (replaces E5's closed forms, E4's table at the setting, A10's typed digits as an act, and the setting's searches)

**S1, the setting is data.** For each Node-clock and train, the piece names the gears' integers: notches now and before, and the fine tooth where it names one, born at mid elsewhere. The lay is the one advance act, a sum over the entries, so it is free of the entries' order:

    n_k(x) += N_k(x),   b_k(x) += B_k(x)

**S2, the rest turn,** where an entry names a rest at a sense sigma (s the pair's third integer, pinion^2 + s^2 = rim^2, the calibre's per R11 and E19). One Gaussian product and one carry per part:

    N = SUM over the entries at x of z_now (pinion + i sigma s)
    V = W now - (W div rim) N + mid(W),   before = now - V div W,   fine = V mod W

with W div rim = 3 Gamma^2 G^2 (X_before + X_now), whole. This is DAVID-AMPLITUDES.md section 3's carried lay, on a complex hand.

**S3, a moving entry** names its notches before too, as data. The Pythagorean point of a stride and the band's rotation, rim_point's root and running_rotation's sine, are computed by the piece's maker outside the engine, where a closed form harms no law. A composition of the three axes' points, where one is still made, is the exact Gaussian product rounded once.

**S4, the wave:** z_now = A i^p and z_before = i z_now, with i^p by p products by i (an exchange and a sign). No quarter table. The digits p and the amplitude A are the piece's data.

**S5, quanta are read, never set:** q(x) = E(x) div w_c, the click's own quotient, on the laid state. The piece names amplitudes, not quanta.

**PROVED.**
1. S1 is the advance; its sum commutes.
2. S2's momentum is P = W (now - before) + fine - mid(W) = W now - (W div rim) N exactly: the carry's quotient times W plus its remainder. So P is linear in (z_now, N), and under the hand's units P(eps z) = eps P(z). For a real z_now and the head's senses it is the head's carried rest lay.
3. The exact Gaussian product is commutative, so S3's composition needs no sort to be free of the axes' order. The head's angle_of sorts because its two roundings do not commute.
4. The setting as data commutes with the 48: the imaged piece is the data moved.
5. No train is named: the lay reads the row's integers.

**CHECKED** (p7_setting.txt).
1. **S1:** the head's laid state taken as the piece's data and laid by S1 on a clock with no setting is the head's bit for bit on all 17 committed worlds, and five ticks of the two runs stay bit for bit on all 17 (every gear, every fine tooth and the slack).
2. **S2** equals the head's rest lays (the before and the fine tooth) at every Node-clock they touched, each train's read once: 125 (packet), 54 (bodies), 27 (emission_one), 27 (pair_3), 27 + 27 (plasma_3), 27 + 27 (universe_3). That is 341 of 341. On random complex hands the rest momentum turns exactly under i: 0 off of 2,000.
3. **S4** equals the head's quarter table at 64 of 64 Node-clocks (the bang, ga2).
4. **S3:** the head's double rounding gives an order-dependent point in 2,290 of 3,000 random strides (hence its sort); the exact product rounded once in 0 of 3,000; the head's sorted angle_of differs from it by a tooth in 1,344 of 3,000. So a moving lay's integers move by a tooth at some Node-clocks; world_polarization's second packet is the one committed such lay.
5. **S5:** the piece's quanta are never the quanta the laid state holds:

   | world | the piece names | the summed quotients read |
   | --- | --- | --- |
   | nature | 6 | 24 |
   | node | 1 | 3 |
   | the bang | 5,000,000 | 320,000,000 |
   | ga2 | 5 | 320 |
   | packet | 218 | 400 |
   | bodies | 250 | 492 |
   | pair_3 | 1 | 27 |

   The piece's "quanta" is a search target in another unit, never an input of the law.
6. **The searches and roots** the head's setting runs, beyond the bare clock's (searches, roots):
   - none on the hole, nature, node, sea and sea_3;
   - (1, 0) on the bang and ga2 (set_cycle);
   - (1, 35) on pair_3, (2, 50) on plasma and plasma_3, (2, 40) on universe and universe_3 (set_even, with sine_rim inside it);
   - (1, 28) on packet and emission_one, (2, 56) on bodies and emission, (2, 35) on polarization (fitted, with sine_rim inside it, and rim_point and running_rotation for its moving packet).

   Under S1 all of them leave the engine.

**What it replaces.**
- E5 (raised_cosine's Chebyshev weights, rim_point, angle_of, running_rotation): data, or the exact product.
- E4's quarter table at the cycle setting: i^p.
- The setting's searches (least_at in set_even, fitted and set_cycle) and roots (largest_below, sine_rim): the piece names the amplitudes.
- A10: the sixteen digits are data here. Their derivation, the A1 light pattern of the one big bang, is section 23's and not this draft's.

**OPEN.**
1. The roots the bare clock itself takes from the calibre are not the setting's:
   - the drift, largest_below(key);
   - the fitted hand's (A, B) = balanced_notches(key div 2), a root and a downward search;
   - each train's s by sine_rim, already decided to be the calibre's (R11, E19).

   They become the calibre's integers by the owner's word (A12). The key could be named as its two factors (A, B) with key = 2 A B.
2. E16's setting refusal (two quanta on a twin hand at a Node-clock) is the piece's checker's, outside the engine. Its physics is law 7's.

## 10. The rewind of the writes

**PROVED.** Every write above is a sum of notches at named Node-clocks and a change of remainders. Each is undone bit for bit by the same advance at -1 from the click's own record, a few integers the Node-clock gives (section 5 of the plan):

| write | what its record holds |
| --- | --- |
| F1 | nothing (it is a reading) |
| F2 | the train, the senses, each end's (u, s) |
| F3 | (x, u, s) |
| F5 | each end's unwound notches, the receiver's (u, s), the remainders before |

**CHECKED.** p5_write.txt: 400 and 100 of 100 bit for bit. p10_rewind.txt: the running engine with F3, 20 of 20 on nature and on the hole, once the record holds F3's signed move.

**OPEN, the undo with no record** (the plan's "the click undone from the Node-clock's own gears and remainders, with no log read"; Sofer's G1).
- From the post-state alone, F3's unit is recoverable below the top: the slope's sign is kept. Its count is not: given the fall, s solves w s s + L' s - F = 0, which is a root, or a ladder again.
- F5's unwound notches are gone from the gears.

So the record must stay part of the Node-clock's state. A write that is its own inverse on the gears, as the step and the turnover are, is not found here.

## 11. Findings on the head beyond the listed fakes

1. **The step does not conserve the charge** bit for bit (section 4, OPEN 1; p1_charge_books.txt). This bears on section 19's "derived from the one formula: the charge's conservation", and on E17's replacement "the senses from the books".
2. **The plan's "imaginary part the lead"** names the wrong bilinear (L1). On a real light it is 0 at every Mesh.
3. **R7 makes the head's takes refuse** wherever a real light's notch now is nearer 0 than its notch before. It picks the empty twelve gear: 171 and 84 spurious stops (p3).
4. **R1 lets charge-changing annihilations through:** 3 of the hole's 6 (p1, p4).
5. **The head's lay jam reads the wind, not the hand.** It passes 2 lays (nature, the hole) over hands standing at a wind of 0 or less, whose lay would change the charge (p4).
6. **A fitted hand costs the same wind for every train**, 1,010,027 millionths of a light winding (p9): no mass threshold at the fitting.

## 12. What replaces what, and what stays OPEN

| the head's | where | its replacement here | status |
| --- | --- | --- | --- |
| R1, a merger only as a conjugate pair, else jammed `sense` | click.py:95 | F4: W_x + W_y = 0 | PROVED, CHECKED; OPEN on evolved pairs (the step's charge) |
| R2, the pair at rest by its own branch | click.py:90, 96-106 | F5: one gate, no sense, the one receiver | PROVED, CHECKED |
| R3, the families a click may lay, the pick even | click.py:49 | F2's split by the sizes c_T; F5's one receiver | PROVED; OPEN the sizes (R4), a contradiction with nature under the spring |
| R6, a split only where light arrives | bobs.py:160 | the parts' sizes and F3's zero | PROVED; CHECKED inert on the twin worlds |
| R7, the paying gear by now^2 - before^2, the first on a tie | unspring.py:53 | F3's steepest notch, both on a tie | PROVED, CHECKED |
| the least_at search of the take | unspring.fall_of | F3's ladder of carries | PROVED, CHECKED; OPEN its length is not fixed |
| the stop, refused by name | unspring.read_ends | F3's zero (the top of the fall); F5's Rule3 quotient | PROVED; OPEN q at one end only (the owner's, A2) |
| E16, the lay jam's standing test | click.jam | F4: X_x + X_y = 0 (the charge's part) | PROVED, CHECKED; OPEN the rest is law 7's |
| E16, the setting's refusal (Pauli at the setting) | assembly/setting.py | the piece's checker outside the engine | OPEN, law 7 |
| E17, the pair's senses typed, the + end by the twist | click.engage | F1, unique up to one declared sign | PROVED, CHECKED bit for bit |
| the jams `orientation`, `twist` | click.engage | F1's zero | PROVED, CHECKED |
| the crowd's jam | click.jam | kept, as the order-free strike's letter; equal charges never pass F4 | PROVED; OPEN summing opposite crowds |
| E5, raised_cosine, rim_point, angle_of, running_rotation | assembly/setting.py | S1 to S3 | PROVED, CHECKED |
| E4 at the setting, the quarter table | assembly/cycle.py | S4 | PROVED, CHECKED |
| the setting's searches and roots | set_even, fitted, set_cycle, sine_rim | S1 and S5 | PROVED, CHECKED |

**OPEN, by what blocks each:**
1. **The ladder's length** (F3): the protocol's rule on loops. One carry is fixed but leaves a bounded debt. The owner's word, or Sofer's.
2. **The step's charge drift** (F4, F5): law 2's carry and the Mesh's turn. David's.
3. **Lays over standing matter, and the setting's refusal:** law 7 (Pauli). David's.
4. **The sizes of the fitted train:** R4 (the coupling) and nature's pair odds. The owner's.
5. **kappa,** the twist's sign: one declaration. The owner's.
6. **The chime's hand** (the payer or the chiming hand) and its q: the owner's.
7. **The unspringing with a whole light winding at one end only** (A2): the owner's.
8. **The fitted hand's shape,** which costs the same for every train (no E = mc^2 threshold): David's.
9. **The bare clock's own roots** (the drift, (A, B)) as calibre integers: A12, the owner's.
10. **The undo with no record:** G1, Sofer's and David's.
11. **The still payee** (no slope on either gear): a choice no formula makes; never met on the charts.
12. **A world where R6 would act:** not found among the committed ones.
13. **Which twin takes which sense** at a fitting of twin hands: the calibre's order, inherited. With the twin hands' derivation (11 a), David's.
14. **F4 as a gate:** it states the conservation rather than deriving it. Sofer's law check decides, and a step that keeps the sweep answers it (item 2).
15. **F2 and F5 on the running engine:** only F3 was put in it. The local payment and the one-gate unspringing move the charts, unmeasured.

## 13. The probes and their outputs

Every probe sets sys.path to the head's worktree (t24/src and t24) and runs with venv314's python -I. The runs:
- `p1_charge_books.py <t24> <world> <ticks>`: the total sweep per train at the tick's start, after the step, after the click; every fitting's and unspringing's ends. Its output p1_charge_books.txt holds nature 60, the hole 60 and the bang 12.
- `p2_senses.py`: F1 against click.engage, and the sign lemma.
- `p3_take.py`: F3 against unspring.fall_of at every take of the head.
- `p4_charge_gate.py`: F4 against click.jam and R1.
- `p5_write.py <t24> 400`: the pure-integer formulas F1 to F5 and their property tests.
- `p6_split_gate.py`: R6 on twin-hand worlds.
- `p7_setting.py <t24>`: S1 to S5 on the 17 committed worlds.
- `p8_images.py <t24> <ticks> head|f3 [world]`: the head's images test, as it is and with F3 in the running engine. Its outputs: p8_images.txt (the chiral setting, 14 ticks) and p8_images_hole.txt (the hole, 20 ticks, then the head at 16 and 17).
- `p9_fitted_train.py`: the fitted hand's cost per train and the fitted trains.
- `p10_rewind.py <t24> <world> 20 head|f3|f3signed`: the rewind.

P8's counts:

| world, ticks | engine | rotations alike | reflections alike, fitted hands exchanged | fittings | chimes | stops |
| --- | --- | --- | --- | --- | --- | --- |
| the chiral setting (nature), 14 | the head | 24 of 24 | 24 of 24 | 2 | 93 | 477 |
| the chiral setting (nature), 14 | with F3 | 24 of 24 | 24 of 24 | 2 | 173 | 405 |
| the hole, 20 | the head | 24 of 24 | 0 of 24 | 13 | 3 | 31 |
| the hole, 20 | with F3 | 24 of 24 | 0 of 24 | 13 | 63 | 337 |

The hole's reflections part on the head itself by tick 16 (16- and 17-tick runs: 0 of 24 each).
