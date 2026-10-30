# The Mesh's tooth: the escapement on a board where the clocks differ (the second text)

The Boss's deriver, 2026-10-30, taking over the escapement after the first author's process stopped. On the owner's
ruling "no price is allowed; solve it with time forward and backward" and his word "the return in time is simply more
gears, and there are differences between them"; on Big Pic's 6532006298 item 2 (the gap and the mend, with p12 and p13
on reader-5, b49d1b4a8 and 43fcd2fe2); and on the two hostile readers' reports on the first text (fb_phys/REPORT.md,
fb_math/REPORT.md, both NOT PASSED). Read first: fwdback/FWDBACK.md and its notes. The first folder is untouched.

Probes beside this page, whole numbers, tensor24.algebra.carry.carry the one division, no float, root, round, math,
random, fractions or decimal, paths by joinpath, no train declared (the example universe's file read through
edge_lib): fb_lib.py (the first text's, copied and extended); probe_mt1_onegear, probe_mt2_board, probe_mt3_cone,
probe_mt4_plan, probe_mt5_hostile (the first text's five, re-measured), probe_mt6_step (Big Pic's step test and the
readers' steps), probe_mt7_long (the readers' lays, 2e4 to 4e5 rounds), probe_mt8_rules (seven Mesh rules), each .py
with its .txt; rerun/ holds every probe rerun byte for byte. Run from inside the folder with
t24b/.venv/bin/python -I -B. Working notes: 00_notes_derivation.md, 01_measured.md, 02_hostile_check.md. Status:
DRAFTED, for the hostile pair.

## 0. The answer in one paragraph

DERIVED: the Mesh's tooth on a moving clock is a carry whose dial is a count of the structure, 1 + 1 (the Mesh's two
ends), pushed by its two ends' own releases: h, mu+ = carry(g_i + g_j, 1 + 1, mu); its release pays the Mesh's pull
into both its ends at one event. It cannot read the clock itself: a dial read off the clock at the Mesh's ends moves
whenever an end releases while the Mesh stands, so its tooth can stand above its dial on a falling clock (Big Pic's
tooth: its promise broken at round 8, its run back 30 of 40). It forces two changes in the first text: the
escapement's dial is read at the pivot, L(now) + L(now), and the mirror reverses every gear's momentum instead of
leaving a stood Node-clock's gears. So mended, the act is exact (untick(tick s) = s on every lay in its domain), local
(a Mesh reads its two ends), rootless, with no division of the push. Its books are exact at every round, and its kick is
symplectic. At a still step of the clock it reflects what the density reading reflects (1 permille on Big Pic's lay,
against 99 for the first text). On a uniform clock with its teeth staggered it is the leapfrog itself.
MEASURED on the hostile physicist's lays at the example universe's coupling: bounded on his lay (a) (the staggered
uniform board, 2e4 rounds), at e = 1 of his sweep (b), and on the mathematician's two clocks at L_0 and 2 L_0. NOT
bounded on his sweep (b) at e = 1/2, 1/10, 1/100 and 1/1000, nor on his smooth well (c): there it grows faster than the
first text's act. Seven Mesh rules were tried,
and every one grows on the well. THE FINDING, for Big Pic and the owner: the escapement divides time by whole rounds.
Where neighbouring Node-clocks release on different rounds, that division switches every coupling on and off in
time, and a switched symplectic board resonates. The resonance falls steeply with the coupling per proper step, but at
the file's coupling it grows on the readers' lays. No Mesh tooth found both lands each impulse on both ends at one
event and keeps that board bounded. The domain c >= 0 is a PRICE. The 00 row's own law is CHOSEN. "Nature's" is struck
from the board where clocks differ in both texts.

## 1. What the first text's board was (Big Pic's finding and the readers', folded in)

In the first text each Node-clock takes its six Meshes' pull at its own release. Where a Mesh's two ends release on
different rounds, one end is kicked from the other's held count and the reaction lands on another round. The kick is
then one-ended. Three findings follow:

- Big Pic: per round that is d_t((1/N) d_t a) = N d_x^2 a, the slot reading's equation, not nature's d_t((1/N) d_t a)
  = d_x(N d_x a), whose pull is a divergence and keeps SUM a_t / N exactly.
- The mathematician: d SUM_x P_x = SUM_x q_x push_x, minus the pushes the stood ends did not take. No fixed weights
  keep a momentum. The kick's Jacobian [[I, 0], [s Q Lap, I]] is symplectic iff q_x = q_y on every Mesh.
- The physicist: the multipliers leave the circle and the act runs away exponentially inside its promise. The 00 row
  rides the same one-ended kick, d_t SUM P_00 >= 0, and pumps every clock deeper.

The first text's section 4 read the first 400 rounds of that runaway as "the lapse gradient's force, nature's d_t SUM
pi = SUM N Lap a". That is struck: nature keeps SUM pi, and the first text's board where clocks differ is not nature's
in its books, its reflection (99 permille at a still step of 1 to 4/5, nature's 0) or its stability. The second text
measures all three again with each Mesh's pull paid into both its ends at one event (probe_mt6, probe_mt7):

| at a still step N 1 -> 4/5 (Big Pic's lay, the engine's floor act) | reflected (permille) | the books' largest move (permille of the packet's) |
|---|---|---|
| the slot reading (the act as built, teeth rest / N^2) | -112 | 0 |
| the density reading (teeth rest / N, grips N on the Mesh: nature's form) | -2 | 0 |
| the first text's escapement | -99 | 99 |
| Big Pic's Mesh tooth (its own dial L(i) + L(j)) | 1 | 0 |
| this text's Mesh tooth (pushed by its ends' releases at 1 + 1) | 1 | 0 |

Every form's 700 rounds, undone one by one, return the lay exactly.

## 2. The clock layer

Every Mesh gets a tooth of its own, a small escapement shared by its two ends. Each time one of its ends releases,
the Mesh's tooth is pushed by one count. Its dial is two, one count for each end, so it turns once for every two of its
ends' releases. When it turns, the Mesh pays its pull into both its ends at the same moment, so what one end gains the
other loses. Where both ends release together, the Mesh turns with them, so on a uniform clock it is invisible. The
Node-clock's own escapement now pays only the Node-clock's own push (the coupling's, through its drive) and moves its
gears forward. The clock is read where the round turns, at the now slot that the forward round and its run back share.
A gear whose Node-clock stood can still be paid by a Mesh: its momentum changes while its count stands. The return in
time therefore reverses every gear's momentum, and moves a gear back only if its Node-clock stepped.

## 3. The algebra

Per Node-clock one tooth tau; per Mesh one tooth mu (3 per Node-clock on the cube, the load's Mesh numbering); per gear
(a, b, r, r_d) as built. L(x) = L_0 + x_00, L_0 = rest + rest (a unit choice: one count of c is one count of W = rest (L
/ L_0)^2 at first order, the mathematician's minor 7). The round, one pass at every Node-clock alike:

    g, tau+  = carry(L_0 + L_0, L(a) + L(a), tau)                          (the escapement, read at the pivot)
    h, mu+   = carry(g_i + g_j, 1 + 1, mu)                                  (every Mesh (i, j): its ends' turns)
    q_d, r_d+ = carry(g J, T_d, r_d)                                        (the drive; J at the now slot)
    q, r+    = carry(rest (a - b) + s (SUM_Spokes h_e G_e (a_e - a) + T_k q_d), rest, r)
    a+ = a + g q;   b+ = a+ - q

The gear's carry is always taken; at g = 0 with no Mesh released it returns (a - b, r), so the gear stands. Where
every Mesh turns with its ends (a uniform clock, its teeth in phase), the round is the first text's act; at c = 0 it is
the act as built state for state (probe_mt2: 40 of 40 at c = 0, 40 of 40 against the first text at 6 grips standing).
Additions, multiplications and Rule3's carry; no compare, floor, mask or bound; the 2's are two slots or two ends. The
mirror:

    f = carry(L_0 + L_0, D, D - 1 - tau)'s quotient,  D = L(a) + L(a)       (did the round that made this state release)
    a -> a - f (a - b);  b -> a_m + (a - b);  r -> rest - 1 - r;  r_d -> T_d - 1 - r_d      (every gear)
    tau -> D_m - 1 - tau,  D_m = L(a_m) + L(a_m);   mu -> 1 - mu                            (untick = mirror o tick o mirror)

In (x, P) form, with P = rest (a - b) + r and b = a - (P div rest): the round is Dr o K, every kick K (P += a push read
at the now slots) before the drift Dr (a += g (P div rest)); all kicks commute. The mirror is S = Dr_f o M with M: P ->
rest - 1 - P. Then M K M = K^-1 and M Dr M = Dr^-1.

**Lemma A (a Mesh pays a stood end).** A payment X into a gear whose Node-clock stands gives (a, b, r) -> (a, a - q, r')
with q, r' = carry(rest (a - b) + X, rest, r). Its before slot moves on a round where it stood.

**Lemma B (its mirror).** The backward round pays the same pull with the same sign: the pull reads only the now slots,
which the mirror returns. It is undone only if that gear's momentum is reversed, (a, b, r) -> (a, 2 a - b, rest - 1 -
r). The first text's mirror, which leaves a stood Node-clock's gears, fails: 25 of 40 (probe_mt2 B).

**Lemma C (the dial at the pivot).** The first text's dial L(a) + L(b) reads the 00 gear's before slot. That slot moves
on a stood round (Lemma A) and again under the mirror (Lemma B), so Theorem 2 (b) fails: its tooth can stand above its
dial. Measured: with either mirror its promise breaks at round 3, and the run back is 0 and 23 of 40 (probe_mt2 B).
A dial that every stood round leaves alone reads only the now slot. With it:
- (b') After a release tau+ = tau + 2 L_0 - D < 2 L_0 <= D(next), given L >= L_0 at the now slot. After a stood round
  the now slot did not move, whatever the Meshes paid, so D is unchanged.
- (c') The flag f is 1 iff tau < 2 L_0, which is the last round's turn, read in one carry inside the domain.
- The mirror moves a released gear back to its pivot, so the backward round reads D(pivot), the forward round's own
  dial. The tooth flipped at D(pivot), the dial of the carry that made it (rule (iii) literally), gives the backward
  carry the forward turn and the tooth D_in - 1 - tau_0.
- The final mirror reads its flag at the backward state's now slot, which is the forward state's before slot; that
  needs L >= L_0 there. Its flip returns tau_0.

**Theorem 4 (the Mesh's tooth).** Hypotheses on a Mesh's tooth:
- (i) it is a first-order carry whose quotient is the Mesh's release;
- (ii) its push never exceeds its dial;
- (iii) its dial stands still on every round the Mesh stands, whatever its ends do;
- (iv) its push per round is a whole number read from its two ends alone, with no remainder of its own;
- (v) it is symmetric in its two ends (the 24 carry a Mesh's ends into each other);
- (vi) on a uniform clock with its teeth in phase it releases exactly when its ends release;
- (vii) its rate is the mean of its ends' rates (nature's lapse on the edge, at first order in the contrast).

Then:
- By (iii) the dial reads no clock: a dial read at the ends' counts moves when an end releases while the Mesh stands.
  Big Pic's tooth has (i) and (ii) but not (iii); on a non-uniform moving clock its promise breaks at round 8 and its
  run back is 30 of 40 (probe_mt2 B).
- By (iv), (v) and (vii) the push is g_i + g_j, the ends' own turns, each 0 or 1 by Theorem 2'.
- By (vi) a joint release (push 2) turns the Mesh once and leaves its tooth, so the smallest dial is 1 + 1.
- So mu is in {0, 1} and h in {0, 1} on every state: the Mesh's tooth has no domain of its own. Its rate per proper step
  of the end x is (N_x + N_y) / (2 N_x) = (L_x + L_y) / (2 L_y). The physicist's 2 L_x / (L_x + L_y) is the same at
  first order in the contrast, and his and Big Pic's density-reading runs used the arithmetic mean on the step's Mesh.

**Theorem 2' (the run back is exact).** In the domain (L >= L_0 at the now and the before slot of every forward state,
tau < 2 L(now), mu in {0, 1}, r in [0, rest), r_d in [0, T_d)), untick(tick s) = s.
1. The Node-clocks' turns are reproduced (Lemma C).
2. The Meshes' turns are reproduced: the backward push is g_i + g_j again and the flipped tooth is 1 - mu_1, so h' =
   ((1 - mu_1) + g_i + g_j) div 2 = h + (1 - mu_0) div 2 = h, and the tooth is 1 - mu_0.
3. Every push reads only the now slots, which the mirror returns to the pivots. The drive's carry on its flipped tooth
   gives its forward quotient.
4. S (Dr K) S = Dr_f M Dr_f K Dr_f M = M K Dr_f M = K^-1 Dr_f^-1 = (Dr K)^-1. This holds for any whole pushes, with no
   bound on them.

Measured: probe_mt2 (40 of 40 and rewound on twelve lays), probe_mt4 (6 of 6 with J), probe_mt1 (0 misses in 30,000 and
28,000), probe_mt5 (every case in the domain), probe_mt6 (700, 1225 and 1000 rounds undone to the lay).

**Theorem 5 (the books and the kick).** Each round, for every row: d SUM_x P_x = SUM_x (the Node-clock's own push paid
at x). The Meshes pay + X and - X at one event. On the example board (no J) every row's SUM P is therefore exact at
every round, the 00 row's included. The round's kick matrix is s SUM_e h_e G_e B_e (B_e the Mesh's symmetric
Laplacian block) plus the own pushes' diagonal. It is symmetric, so the kick is symplectic, the mathematician's (d)
met. Measured: the identity at 40 of 40 rounds on all twelve lays (probe_mt2 A, the spring lays' 00 row moving by
exactly its spring's paid pushes) and at 6 of 6 with J (probe_mt4); every ring run's books at 0 over 2e4 to 4e5
rounds (probe_mt7).

**Theorem 3 still holds.** No involutive mirror places the pivot. Its scope is the mathematician's: every clock below
rest, standing included. This mirror twice is Dr_f Dr_f'^-1 on the gears and moves tau by D(a) - D(a - f v), so it is
the identity only where the last and the next round agree and, after a release, the clock did not move. Measured: 41
of 41 at c = 0, 14 of 41 at 6 grips standing, never at one Node-clock on a moving clock (0 of 30,000; the first text's
mirror 10,000 of 30,000). The run back is exact throughout.

**Locality and the 24.** A Mesh reads its two ends' turns and counts; a Node-clock reads its own gears, its six Meshes'
turns and their ends. The 24 move every Mesh tooth with its Mesh (the turn's Spoke map) and flip a flipped row's teeth
as built. Measured: 24 of 24 at every round on twelve lays (probe_mt2 A) and through the tables (probe_mt4); the mutant
with a flipped row's drive tooth unflipped holds 3 of 24.

## 4. The event board (the first text's section 4, folded)

One pass at every Node-clock alike, in this order:
1. every escapement at the state as it stands;
2. every Mesh's tooth from its two ends' turns;
3. every push at the now slots, each Spoke's pull by its Mesh's turn;
4. every gear's carry, and its drift by its Node-clock's turn.

There is no fixed point, and no dial is moved by its own quotient. The state gains one tooth per Node-clock (tau) and
one per Mesh (mu); the record's schema and the runner's promise gain both.

**What the Mesh's tooth mends (MEASURED):**
- The books are exact at every round on every lay (Theorem 5).
- The reflection at a still step is the density reading's (the table above; probe_mt6 B and C: -9 and -5 permille at
  the physicist's steps of 4/5 and 1/2, -14 at the mathematician's 2:1, against the density reading's -1, -4 and -14
  and the first text's -90, -284 and -318).
- The staggered uniform clock is the leapfrog itself, one half of the board a round behind the other. Its two halves
  release on alternate rounds and the boundary Meshes pay on one half's rounds; a kick that reads only one half's counts
  commutes with the other half's drift. By windows its energy equals the aligned lay's to the permille (probe_mt7 A and
  C): 7..8 bits for 2e4 rounds on the board, the first text's 6 -> 306.
- The 00 row's one-way pump is gone: the 00 row's books are exact, and in the continuum d_t SUM F(c) = SUM u with F' =
  L / L_0. probe_mt2 C:
  - on the physicist's P5c B lay the mean clock holds at 36 grips + 187 permille for 1e4 rounds (the first text's: 36
    -> 7,747 grips in 4000);
  - on probe_fb2's own lay the clocks stay within 43..78 grips for 4000 rounds (the first text's: 52..72 -> 2,080..3,395
    grips in 400).

**What it does not mend (MEASURED, probe_mt7):**

| lay (the physicist's; H against its start, by windows) | rounds | the first text | Big Pic's tooth | this text's tooth |
|---|---|---|---|---|
| (a) the board, uniform 2 L_0, teeth staggered (light osc / H, bits) | 2e4 | 306 / 687 | (on the ring, next row) | 8 / 92 (bounded) |
| ring, equal clocks, teeth staggered | 2e4 | x2^146 | 978..1081 | 978..1081 (bounded) |
| (b) the deep half at L_0 (1 + e), e = 1 | 2e4 | x2^59 | 7396 | 1100..1341 (bounded) |
| e = 1/2 | 2e4 | x2^42 | x2^365 | x2^136 |
| e = 1/10 | 4e4 | x2^26 | x2^74 | x2^67 |
| e = 1/100 | 2e5 | x2^12 | x2^67 | x2^35 |
| e = 1/1000 | 4e5 | 1858 | 49121 | x2^17 |
| (c) the smooth well, L_0 -> 1.1 L_0 | 4e4 | x2^389 | x2^1251 | x2^443 |
| the mathematician's two clocks, L_0 and 2 L_0, s = 625, 156, 39 | 4e4 | 431, 201, 64 bits | 20 bits | 20 bits (bounded) |
| his ring of 8, dc = L_0 / 4, s = 625, 156, 39 (bits) | 4e4 | 407, 211, 66 | 155, 21, 21 | 159, 88, 21 |
| his ring of 8, dc = L_0 / 10 | 4e4 | 402, 141, 49 | 446, 21, 21 | 22, 21, 21 (bounded) |
| his ring of 8, dc = L_0 / 100 | 4e4 | 39, 27, 23 | 129, 30, 21 | 36, 52, 21 |

The controls stay bounded on the sharpest lay: the act as built, the density reading and the uniform clock, 984..1081
permille over 2e4 rounds (probe_mt7 D). Seven Mesh rules on the same lays (probe_mt8, 8000 rounds):
- every one grows on the smooth well, from x2^71 to x2^260;
- every one but "or" (pay when either end releases) grows on at least one step lay;
- every one but the first text's keeps the books exactly.

**What the growth is (DERIVED in outline, MEASURED).**
- On a standing non-uniform clock the turns g(t) and h(t) are periodic in the round. The board's linear map over a
  period is a product of symplectic shears whose couplings are switched on and off.
- Its multipliers stay on the unit circle away from the sum resonances omega_j + omega_k = 2 pi m / T of the board with
  no switching. The switching opens a band of instability about each, as wide as the switching's weight at that
  frequency.
- At the file's coupling (c^2 = grip / rest = 1/6 a proper step^2, omega up to 0.82 a round) the modes' sums reach the
  release patterns' frequencies on most lays. Dividing the grip moves the spectrum below them: the well's growth falls
  from x2^174 to x2^69, x43.8 and x1.12 in 16,000 rounds at the grip divided by 1, 4, 16 and 64 (probe_mt7 F). A
  smooth well's slow slips between neighbours keep a resonance in reach even then.
- The first text's one-ended kick is not symplectic, so it grows on every lay at a rate in proportion to the coupling.
  The Mesh's tooth turns that into resonance bands, which narrow steeply with the coupling but are wide at the file's.
- The lever (section 6, item 2) divides each proper step into m rounds but does not tame it: the well grows x2^85,
  x2^96, x2^83 and x2^34 in 8000 proper steps at m = 1, 2, 4 and 8 (probe_mt5 I).

**So the board where the clocks differ is nature's in neither text.** The second text's books and reflection are
nature's, but it is not stable there at the file's coupling. The slot reading (the act as built) is stable, with the
impedance's reflection (112 permille at 4/5). The density reading is stable and nature's, but its dial rest / N and its
Mesh's grip N G divide the push at dials that move with the clock, which is Theorem 1's hypothesis (H) for the Mesh's
part (the physicist's item 2). Big Pic's "the density reading, divided in time" holds for the books, the beat and the
reflection. It does not hold for the stability: dividing time by whole rounds switches the couplings, and the density
reading taken every round does not.

**The 00 row's own swing can leave the domain.** On the first text's case H (two Node-clocks laid at c = 0 and 12
grips, a full L_0 apart) this text's act keeps the books, but the 00 row's own swing carries site 1 below rest at round
4. The act then is no longer the standing act, and the clocks run off (9,295 and 9,484 grips by round 1000; 14 of the
first 400 rounds miss the run back). Laid with room above rest (12 grips and 12 grips + 6, 3 or 1 grip), the pair stays
in the domain for 4000 rounds, its light row at most 1,715 counts at round 4000 and its books at 0; laid 12 grips apart
above rest it leaves at round 32. The first text's act stayed in the domain on that lay only because its pump drove
both clocks deep: 770 and 838 grips by round 400, not "c = 0 and 12 grips" (the physicist's minor 8). Probe_mt5 H.

## 5. The physics behind the clicks

**At one Node-clock** the Mesh's tooth does not enter. The pivot dial gives nature's tests to the permille (probe_mt1;
rest 10,000, L_0 20,000, the 00 gear free at +-1 a proper step, L 20,000 <-> 40,000):

| | nature | this text, rising | falling | the first text (rising .. falling) |
|---|---|---|---|---|
| a free gear's v^2 W_eff over W x4 | 1000 | 1000 .. 1003 | 999 .. 1001 | 998 .. 1001 |
| a hairspring's A / A0 | 1000 | 1000 | 999 .. 1000 | 999 .. 1000 |
| T^2 / W_eff over ten beats | 1000 | 1000 | 999 .. 1000 | 997 .. 1000 |
| a swing at half the beat, the beat, ten beats; 5 and 20 percent; 50 swings | 1000 | 1000 at every one | | 1000 |
| two clocks at one site, g = 100 and 400: their periods in releases (minor 7) | constant | 62..63 and 31..32 | | 62..63 and 31..32 (the physicist) |

**The rising course now starts in the domain** (c = 1, its before slot at 0; the first text's had c(before) = -1, the
mathematician's minor 5), and so does the doubling case (from 2 L_0; the first text's had L(before) = 0).

**The phase** (minors 4 and 6). The releases are read as n + tau / D against the clock's own course S = SUM over
rounds of L_0 / L(now); the offset starts at 500 milli-steps, the tooth born at the half. Over L x2 it moves -235 with
this text's dial and +110 with the first text's; over L / 2, +220 and -83 (the physicist's +95 and -100). It is bounded
on a monotone course, within (1/2) ln of the clock's change, but not "no secular rate". Under a swing (the 00 gear on
its own spring) it drifts -12 and +14 milli-steps a swing: a swing drifts it at second order in the clock's change per
step, either dial, and the two dials drift with opposite signs.

**Every push kept** (probe_mt5 A to C, as the first text): a constant push p = 10 .. 50,000 at W_eff = 4 rest moves
a(T) within 1 permille of nature's; a hairspring laid at a0 = 10 .. 1000 swings between -a0 and a0; the kick of 1 moves
one notch at proper step 5000; the ring's long wave has twice the period at W_eff = 4 rest (2,212 against 1,106).

**One cone in a uniform well** (probe_mt3: unchanged, every Node-clock and Mesh releasing together): T_light^2 / T_00^2
= 1000 at L = 18, 30 and 66 grips. Light's beat scales as W_eff / rest: 2250, 6252 and 30257 against 2250, 6250 and
30250. Light's delay through a well is lapse-only (gamma = 0, the physicist's minor 5): half of general relativity's at
weak field. The spatial part belongs to the ii slots (G2). Where the first text said "one cone" and "nature's", read
"one cone, lapse only".

**The 00 row's own law is CHOSEN** (the physicist's item 3, the mathematician's minor 8). The 00 row rides the
escapement like every row: in proper time it is the standing act, so a free uniform 00 gear keeps its proper velocity,
L c', which is k = 1/2 in W a'' + k a'^2 = F (the physicist's P1 C: 999..1000 permille from 1e3 to 1e6 rounds).
General relativity gives a uniform lapse no equation of its own. The covariant action of a lapse-sourcing field keeps
sqrt(L) c' (k = 1/4); k = 0 keeps c', and k = 1 keeps L^2 c'. "The clock's field ticks with its site" is an argument for
a choice, not a reading of nature. So it is CHOSEN, k = 1/2, with k = 0, 1/4 and 1 to the owner on their consequences.
The first text's "CHOSEN nowhere" and "the 00 row's own law ... retire" are struck. Where clocks differ, its equation
here is d_t(c_t / N(c)) = div(N_e grad c), with its books exact; its own wave resonates like any row's.

**Postulate 6.** The first text's "at first post-Newtonian order either way" is struck. L linear gives ln N = -c / L_0
+ (1/2)(c / L_0)^2 and W linear gives -c / L_0 + (c / L_0)^2; they differ at 1PN. Which the law intends is the owner's,
with term 5.

## 6. DERIVED, MEASURED, OPEN, and the prices

**DERIVED:**
- Lemmas A, B and C (why the first text's dial and mirror must change once a Mesh pays a stood end);
- Theorem 4 (the Mesh's tooth from (i) to (vii));
- Theorem 2' (the run back exact in the domain);
- Theorem 5 (the books' identity and the symmetric kick);
- Theorem 3's scope;
- the staggered uniform clock = the leapfrog;
- the 00 row's pump removed (continuum);
- the resonance's mechanism, in outline.

**MEASURED:** every number above, each probe rerun byte for byte (rerun/).

**OPEN and the prices, named:**

1. **The stability where neighbouring Node-clocks release on different rounds (the finding).** No Mesh rule found
   keeps that board bounded at the example universe's coupling while paying both ends at one event and staying exact,
   local and rootless (seven tried, probe_mt8). For Big Pic and the owner, the choices as I see them:
   - accept the slot reading (the lapse in the inertia only, the impedance's reflection);
   - find an exact whole-number density reading on a moving clock: the push divided at a dial that moves, Theorem
     1's (H), not found;
   - take a coupling per proper step well below the file's (the file's integers, not the deriver's);
   - find a Mesh rule whose switching cancels at first order, such as half payments at each end's release with a
     remainder at the standing dial 2, the shape of an asynchronous variational integrator. Not derived here.
2. **The domain c >= 0 is a PRICE** (the mathematician's item 2), not a promise like W >= 1:
   - Below D = 2 L_0 the escapement turns 2, so it can only slow a clock: the rest clock is the fastest clock of every
     world. One count faster than rest turns 2 at round 9,999 (probe_mt5 E); the 00 mode about rest cannot be laid
     (its promise breaks at round 0, probe_mt3); the 00 row's own swing can carry a clock out (case H, round 4).
   - The first text's "read by the promise as W >= 1 is today" is struck.
   - One observation: outside the domain this text's gear keeps its tooth in range (its carry is always taken), and on
     a standing clock a turn of 2 still runs back (probe_mt5 E). But a turn of 2 is one kick and two drifts, not two
     proper steps. OPEN.
   - The lever is the way out, at its cost. L_0 = 2 rest m^2, the escapement pushed by 4 rest m (2 rest m a slot: the
     first text's "2 rest m" was per slot), the domain c >= -2 rest m (m - 1). With this text's act it is sound
     arithmetic: one release in m rounds at rest (6000 and 4000 of 12,000 at m = 2 and 3); the run back exact down to
     the edge (0 misses in 7500 and 10,000 rounds); the turn 2 one count past it.
   - The lever's cost: a staircase m deep everywhere (light per round 1/m at rest), the mirror no involution even at
     rest, and the board's resonance not tamed (item 1).
3. **The 00 row's own law is CHOSEN**, k = 1/2 (section 5).
4. **The mirror is no involution** (Theorem 3); the run back is exact.
5. **The phase** is bounded on a monotone course, and a swing drifts it at second order (section 5).
6. **Light's delay is lapse-only** (gamma = 0) until the ii slots move (G2).
7. **The record and the runner.** The state gains tau per Node-clock and mu per Mesh. The promise gains L >= L_0 at
   both slots, tau < 2 L(now) and mu < 2. The rewind is n unticks.
8. **The click teeth (term 11)** step with the escapement like r_d; not probed.

## 7. The readers' blocking items, answered

| item | answer | where |
|---|---|---|
| physicist 1: the runaway; one event per Mesh; bounded by windows over >= 1e4 rounds on his lays | One event per Mesh: derived and measured (the books at every round on every lay). His lay (a): bounded, 2e4 rounds. His lay (b): bounded at e = 1, NOT at e = 1/2 .. 1/1000. His lay (c): NOT bounded, faster than the first text's. The clock's own runaway: gone. Strike "nature's" in section 4 and step 6: done. | probe_mt7 A, B, C; probe_mt2 C |
| physicist 2: not nature's where clocks differ; the weight 2 L_x / (L_x + L_y) with no division of the push; the reflection and the books | The Mesh releases at the mean of its ends' rates: the weight in time, nature's at first order, no division of the push. Reflection -9 / -5 permille at 4/5 and 1/2 (density -1 / -4); the books exact. The board is still not nature's: it is unstable there. | Theorem 4; probe_mt6 B |
| physicist 3: the lapse's law CHOSEN | Written CHOSEN (k = 1/2) with the argument; "CHOSEN nowhere" and "retire" struck. | section 5 |
| mathematician 1: both ends on one event (books, symplectic kick) and the edge's lapse (reflection); long runs, clocks and books printed | Both: Theorems 4 and 5. Reflection -14 at his 2:1 step (density -14, first text -318). His two clocks and his ring of 8 at dc = L_0 / 10: bounded; dc = L_0 / 4 and L_0 / 100: growing at s = 625 and 156. The 00 pump gone with the clocks' course printed. The resonance named. | probe_mt6 C; probe_mt7 E; probe_mt2 C |
| mathematician 2: the domain a price, or probe the lever | Named a PRICE plainly; the lever probed, its arithmetic sound, its costs named. | section 6 item 2; probe_mt5 E, I |

The minors:
- the physicist's 4 (the phase), 5 (gamma = 0), 6 (the lever's push per slot), 7 (two clocks in releases) and 8
  (case H's clocks);
- the mathematician's 3 (Theorem 1 is an outline: the three properties that free the escapement are taken here as
  Theorem 4's hypotheses, and "every form" is too wide), 4 (Theorem 3's scope), 5 (the lays in the domain), 6 (the
  phase measured, not bounded by the first text's formula), 7 (L_0 a unit choice) and 9 (the books checked at every
  round, the releases counted from the turns, the "uniform to the permille" lay named, the J case's 6 rounds named:
  its quartic products explode past 6);
- the physicist's "Postulate 6 either way" (struck, section 5).

All are answered in sections 3, 5 and 6.

## 8. Solution24

1. Does it follow by itself? The Mesh's tooth follows from (i) to (vii). The dial at the pivot and the mirror's M follow
   from Lemmas A to C. What does not follow is a stable board where clocks differ.
2. The picture: every Mesh has an escapement of its own, kept by its two ends.
3. The big things only: 1 + 1 is the Mesh's two ends; L_0 + L_0 is two slots; no number, root or square condition.
4. The four layers above.
5. No click in it.
6. The books: exact at every round on every lay, the first text's one-ended drift gone.
7. Both ways, by windows over 2e4 to 4e5 rounds on the readers' own lays. What does not match nature is named: the
   growth on (b) and (c).
8. Every case run locally on the real act's carry, board and tables, src untouched.
9. For the pair.
10. One act for every gear, the 00 row's included.
12. What does not follow: the board's stability where clocks differ (the finding), the domain (a price), the 00 row's
    law (CHOSEN). These go to the owner through the Boss and Big Pic.
