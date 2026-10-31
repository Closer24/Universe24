# FACE: each clock's own count, a gear of the act, and how it sits in the quaternion

The Boss's FACE deriver, 2026-10-31, from 00:46 UTC, on the Boss's brief (face/BRIEF.md) and his four notes of the
night: the owner's words of 00:3x and 00:5x UTC ("derive, and understand how it looks in the quaternion"), his
arrangement of 00:4x UTC ("Physics is only the click world. Clocks are the board."), his word of 01:0x UTC (time in the
click world must agree with special and general relativity), his rule of 01:3x UTC (a derivation, 20 minutes at
most), and Big Pic's words from above (#2187 6536836528 item 4, 00:57 UTC; 6537034824, 01:15 UTC).

**Status: DRAFTED**, for the hostile pair, cut short at 01:52 UTC by the owner's rule. DERIVED marks a step proved here
with its hypotheses; MEASURED ON THE BOARD a count of the act's own arrays (a clock fix's check, never physics); OPEN a
gap with its cause. The face is a clock fix: it is derived and checked on the board. What it gives physics is owed to
the click world, read twice from the record's lines; no board check here stands for physics, and no click-world
reading here stands for the clock fix.

**Sources.** The act at b1a50bb33 (the read-only worktree scanY: engine/step.py, state.py, kinds.py, carry.py;
runner/load.py, plans.py, rounds.py, run.py; record/schema.py; decoder/measure.py); the probes run on the venv's
tensor24 (node-live 7dcb31607, the same engine and record). The law: origin/scribe-5 docs/ALGEBRA.md line 35 (items 5,
16, 17); docs/ARCHITECTURE.md ("The board's four and the click world's three", the decoder's readings). SHADOW.md and
its probes (scratchpad/shadow). COUNT5.md P1, FAMILIES4.md, quaternion/ONE_ALGEBRA.md and RECHECK.md (origin/boss-derive).
FWDBACK3.md (scratchpad/fwdback3) for the escapement.

## 0. The answer

A clock is the record's (site, train), and the act as built holds no count of its ticks (SHADOW, DERIVED); the face
is the one gear that holds it, per train and Node-clock a whole count f with a tooth r in [0, 4), carrying each round
the window's crossings C, the sum over the train's gears of |sg(before) - sg(now)| + |sg(now) - sg(next)|, the sign
read by the loader's sign test (one carry of x by x^2 + 1) on x and on -x, at the dial 4 = senses x senses, so that f
grows by Rule3's quotient alone, one count per crossing of a gear through 0 (a line hand's half beat; a quarter turn of
a hand of one sense), and the mirror sends (f, r) to (-f, 3 - r), the face counting down on the mirrored state like a
time; it is exact (4 f + r = 2 V + v(lay) - v(last), V the gears' sign variation), has no if, mask, bound or loop and
no number beyond 0 and 1, reads only its own counts on the passing's window, runs back as the same act on the mirrored
state round by round, and is kept by the 24 and by the 48's -1 on every kind they move by signed permutations (all but
E); MEASURED ON THE BOARD, it counts 637, 318 and 159 at W, 4 W and 16 W, SHADOW's half beats exactly with no root,
1,274 with the spring 4 g, every run back exact round by round, the 24 at 24 of 24, and each mutant fails where it
must (the face kept by the mirror; its tooth kept; one pair for the window; "face = round", 40,000 at both depths; the
product's sign, 0 of 200 below a notch; the half-open sign alone, not kept by the 48's -1). In the quaternion it is one
structure with the act: its increment is the L1 step of the sign of the state quaternion q = z_now + z_before j, which
every signed permutation of the gears keeps; where the step is a unit of order 4 (L_i for the held hand, R_j for the
line hand) the face is the unit's exponent lifted to the integers, z_t = i^f z_0, by |s + t| + |t - s| = 2; a unit's
step has its order fixed by k / W (6, 4 or 3 at 1, 2 or 3), so it reads no depth, and a clock that reads depth has no
unit step and counts the whole half turns of its phase, Rule3's carry of the phase with the hand within its half turn
the remainder. The face needs one gear of its own, since no part of the act as built and none of the escapement's
bounded teeth holds a count since birth; its increment comes from the Node-clock itself, its crossings as built or the
escapement's release if FWDBACK3 stands (one gear carries both), which is where I part from Big Pic's "no additional
gear". A further finding: tonight's only clicking law cannot be laid far above a notch, since the held hand's room
bounds a tied hand's stride to about sqrt(|k|) counts a round (T6). The record's 1.4 line is {round, site, train, q,
tooth: [k, k+], face: [f, f+]}, the face read from the state and never computed; the header names each clock's face at
birth and its rest beat, and the end its last face; D6 is the later face less the earlier at one clock, with no root
and no round. Against the two theories, a standing clock's D6 is its face; a moving clock's own count is no Node-clock's
face and is owed to a bound pair that travels and ticks by its own clicks (G6, K4); the redshift is owed to two faces
at two depths between two light links (reading 7); and light's two-way count is alike along the three axes by the 24
for a standing clock, elsewhere only in long waves. No world tonight shows any of these in the click world.

## 1. The clock: the face as a clock fix (DERIVED; MEASURED ON THE BOARD in section 3)

### 1.1 What counts as a half beat on the act

A half beat is a crossing of one of the clock's own gears through 0: its count changes sign between two consecutive
counts, directly or through exact zeros. It is read by the loader's sign test, below(x) = -q with (q, _) =
carry(x, x^2 + 1, 0), which is 1 below 0 and 0 elsewhere (x div (x^2 + 1) is -1 for x < 0 and 0 for x >= 0, the divisor
at least 1). The sign is sg(x) = below(-x) - below(x), and the change of sign between two counts is

    v(x, y) = (below x - below y)^2 + (below -x - below -y)^2 = |sg x - sg y|,

in half crossings: 2 from one side to the other, 1 into or out of an exact 0, and 0 where the sign stands. A crossing
through a run of zeros is 1 + 1, the same 2 as a direct one. Two sign tests are needed and not one. The half-open test
alone (zero on the positive side) changes when a gear is negated: (0, -1) counts and (0, 1) does not. The 24 and the
48's -1 negate gears, so it would break them (the mutant m6, section 3).

### 1.2 The gear

Per train h and Node-clock x, the face f (born 0) and its tooth r (born 0, within [0, T_f)):

    C_h(x) = SUM over h's rows g of [ v(b_g, a_g) + v(a_g, a+_g) ]        (the before, the now and the next)
    (q_f, r+) = carry(C_h, T_f, r),   f+ = f + q_f,   T_f = senses x senses = 4
    mirror: (f, r) -> (-f, T_f - 1 - r)

The window is the passing's own, (b, a, a+): the act already computes a+ for X(S+). The sum into the train is the
passing's scattered sum. The square takes the factor 0 by its flag, as in the passing, so no train is named. T_f = 4
is the 2 of the half crossings times the 2 of the window, which holds each pair twice, both read from the star as the
act reads its 2 (step.halves).

### 1.3 Theorems

**T1 (exact, no crossing missed, none counted twice).** With f and r born 0,

    4 f_t + r_t = SUM_{u=1..t} C_u = 2 V(0, t) + v(x_-1, x_0) - v(x_t-1, x_t),

where V(0, t) is the sum of v over consecutive counts from the lay's now to the last count, per gear, summed over the
train. Proof: round u reads (x_u-2, x_u-1) and produces x_u. The pair (x_m-1, x_m) enters round m's window as
(now, next) and round m + 1's as (before, now), so every pair is counted twice, except the lay's (x_-1, x_0), once at
round 1, and the last, (x_t-1, x_t), once so far. The carry's identity n + r = q T + r' summed gives the rest. Each
crossing is 2 in V, 4 in the sum, so f counts each crossing once. It is booked when its second window has passed, and
the tooth holds the part on the way.

**T2 (the run back, round by round).** untick = mirror o act o mirror on (a, b, s, r_d, k, f, r). By the engine's
theorem, the backward round reads the forward window reversed, (a+, a, b) on an even row and (-a+, -a, -b) on an odd
one. Since v is symmetric in its two counts and v(-x, -y) = v(x, y), C is the same on the backward round. The carry
lemma for an even increment then gives the result. From C + r = 4 q + r' it follows that C + (3 - r') = 4 q + (3 - r),
with 0 <= 3 - r < 4. So carry(C, 4, 3 - r') = (q, 3 - r). The backward round takes -f+ to -f+ + q = -f, and the mirror
returns (f, r). The face counts down on the mirrored state. A face kept by the mirror would need an increment that is
odd under the reversal, and the crossings' count is even (the mutant m1). A tooth kept would need r + r' to be constant
(m2), and one pair in place of the window is not even (m3).

**T3 (the 24 and the 48's -1).** Every turn of the 24 moves the rows of an A1, A2, T1 or T2 kind by a signed
permutation (kinds.py: 1, the sign, the turn, the sign times the turn; the square by its signed permutation). v is
kept by a sign and C is a sum over the train's rows, so C, and with it the face, is the same on the turned lay's run as
on the lay's. The face is A1. The 48's -1, the full turn of a half-speed hand's frame, negates every gear of the hand,
and the face is kept, as Big Pic's item 4 asks: the face counts beats alone, never the hand's sign or its tooth. On E
the 24 act by integer matrices that are not signed permutations, so the face of an E hand is not kept (OPEN; no matter
train of kind E is laid in any world tonight).

**T4 (the laws of the Node-clock).** No if, loop, mask or bound: two sign tests and one carry are Rule3's carries; the
squares and the sum are products and a scattered sum. There is no number beyond 0 and 1, since x^2 + 1 and the 4 are
read from the star's senses. Locality: the face reads its own train's counts at its own Node-clock, at the before slot,
the now slot and the next, as the passing does. Nothing is declared. The face pushes nothing into a, b, s, r_d or k, so
the act's state, clicks and record are what they were.

**T5 (the calibre).** At one count a round a beat locks to the integers' cycle (term 13; NOT_CLOSED 7). The held hand's
exact quarter turn gives one face count a round, the round itself. The line hand at the quarter mode (spring 2 W) gives
one face count every two rounds, the same at every depth. There the face is the mutant "face = round", which is why
the depths must be laid far above a notch and far below the cutoff (section 3, G5).

**T6 (the room bounds the click world's stride; DERIVED by scaling, MEASURED A5).** Tonight's only clicking law ties
each tied hand x to the held hand k by (hold f C; x, x, k, k). The held hand's spring is then 2 rest + 2 hold f |x|^2,
and its quarter turn stays exact only while the tie's extra push, 2 hold f |x|^2 per count of k, rounds away on the
dial W: |x|^2 at most of order W / (hold f |k|), about 10^2 counts at the rest teeth (f = rest div Gamma, Gamma =
10^4). That is NOT_CLOSED 29's room. The tied hand beats at sqrt(2 hold f |k|^2 / W), so its stride is at most about
sqrt(|k|) counts a round. The beat far below the cutoff needs 2 hold f |k|^2 << W, that is |k| << (Gamma / (2 hold))^(1/2),
so the stride stays at a few counts a round at most. **So no world of tonight's clicking law can be laid far above a
notch while its held hand keeps its room: Big Pic's calibre (his item 2) holds for the lone gear's three depths, and
D6 on any record of this law reads the act's rhythm about a notch (SHADOW 4.7: 410 rounds against the continuum's
444).** A D6 world far above a notch needs another clicking clock (OPEN). Measured: the click world laid at 25,000
times leaves the room at once (A5).

## 2. The algebra: the face in the quaternion (DERIVED on paper; the probes cover each case named)

**The ground (ONE_ALGEBRA finding 2 and 3, passed SOUND by both readers of RECHECK).** A train of kinds A1 + T1 is one
whole quaternion h = a + x i + y j + z k per Node-clock. The act on it is componentwise, the 24 act by the sandwich
g h conj(g) / N(g) (Hurwitz units, and norm-2 Lipschitz elements whose sandwich divides by 2 with remainder 0), and
parity is conjugation. For a hand of two parts, the two slots make one quaternion q = z_now + z_before j, z = re + im i.

**(Q1) The face's increment is the L1 step of the sign of the state quaternion.** The window's C is SUM over the
components of |sg(q_t) - sg(q_t+1)|, with q_t = (now, before) and q_t+1 = (next, now): the now slot steps a -> a+ and
the before slot steps b -> a (section 1.3, T1). sg(q) has its components in {-1, 0, 1}. The 24's sandwiches move the
components of h by signed permutations (the real part fixed). Left and right multiplication by +-1, +-i, +-j and +-k
are signed permutations of the four components. On fam_math's 24-gear train, the group ring Z[2O], left and right
multiplication by all 48 units are signed permutations of its gears (Cayley; ONE_ALGEBRA "The units as gears"). So the
face is kept by every one of them, and by the 48's -1 on any hand. The units (+-1 +-i +-j +-k) / 2 do not move the
four Lipschitz components of a 4-gear hand by signed permutations, nor keep them whole. There the face's keeping is
not defined (OPEN with the half-speed carrier, FAMILIES).

**(Q2) Where the beat is a unit's step, the face counts the units.** Let s = sg(u) and t = sg(w), not both 0. Then

    |s + t| + |t - s| = 2,

since if one is 0 each term is 1, and if both are nonzero one term is 2 and the other 0.
- The held hand at its exact quarter turn, (re, im) -> (-im, re), is left multiplication by i. Each pair (z_t, z_t+1)
  then has v summed over re and im equal to |sg re - sg(-im)| + |sg im - sg re| = 2 for every nonzero whole z. The
  window holds two pairs, C = 4, and the face grows by exactly 1 per i applied: z_t = i^f z_0, the face the unit's
  exponent lifted from Z / 4 to Z.
- The line hand at the quarter mode (spring 2 W), (now, before) -> (-before, now), is the right multiplication by j.
  Each step has C = |sg b - sg a| + |sg a + sg b| = 2, and the face grows by 1 every two rounds, by 1 per j^2 = -1: a
  half beat is the count negated, a+2 = -a.
MEASURED ON THE BOARD: the line hand's face 200 in 400 rounds at W and at 4 W (G5). The held hand's face 40 in 40
rounds on the click world's own act (A1).

**(Q3) Whole speed and half speed.** A whole-speed hand at its quarter turn is back after one turn, 4 units, its face 4
on: the face mod 4 is the hand's phase, and the face itself the lift. A half-speed hand's lift of the quarter turn
about an axis has order 8: its full turn is the 48's -1, which flips its sign, and it is back after two turns. Its face
is kept by that -1 (T3, Q1), so it counts on through the sign's flip: 8 units per return, the face mod 8 its phase. No
half-speed train can be laid tonight (the loader lays the five single-valued kinds), so this is DERIVED and not
measured on a half-speed hand. The 48's -1 is measured on the tied hands' sign (A3, G6).

**(Q4) A unit's step reads no depth; a clock that reads depth counts its phase's half turns.** The time plane's step
[[2 - k / W, -1], [1, 0]] is whole only where W divides k, with trace 2 - k / W. It has a finite order only at
k / W = 1, 2 and 3, the orders 6, 4 and 3, since a whole trace 2 cos(2 pi / n) leaves n in {3, 4, 6} for a matrix that
is not +-1; at 0 and 4 it is parabolic (the crystallographic restriction; ONE_ALGEBRA finding 5, RECHECK). So a unit's
step has its order, and the face's count a round (2 crossings per period: per 6, 4 or 3 rounds), fixed by k / W. It
reads no depth: the quarter-mode line hand counts 200 in 400 rounds at W and at 4 W alike (G5). A clock that reads depth has k / W off the five ratios, so its step is no
unit (RECHECK: nature's hands have none). Its face counts the crossings, the whole part of the hand's phase in half
turns: f = the quotient of the phase by the half turn, the hand within its half turn the remainder. That is Rule3's
carry on the phase, read with no root and no angle computed. It is the law's own beat, "the carry of the clock's dial,
the clock's own event and no kind of click" (line 35, item 5).

**(Q5) One structure, not a counter beside it.** The face reads the passing's window and carries it as the click tooth
carries the passing. The passing is odd under the window's reversal, so the mirror keeps the click tooth. The crossings
are even, so the mirror negates the face and flips its tooth. The click tooth counts what passes; the face counts how
far the clock turned. Both are per train and Node-clock, both are Rule3's carries, and both run back as the same act on
the mirrored state. In the quaternion, the face is the integer lift of the hand's unit part (Q2) and the quotient of
its phase where no unit steps it (Q4).

## 3. The board: the probes' numbers (MEASURED ON THE BOARD; clock fixes, no physics)

**face_p1_gear (the engine's lone gear, step.gear; output face_p1_gear.txt).**
- G1. The lay a = b = 10^6, g = 1,500,000 (g / W = 1 / 400 at the rest teeth 600,000,000), rounds 1 to 40,000, stride
  1, far above a notch (no exact zero in the counts). The face is 637, 318 and 159 at W, 4 W and 16 W. SHADOW's reader
  counts the same, 637, 318 and 159, and the identity of T1 holds at all three. By cross products 637, 636 and 636; by
  squares 405,769, 404,496 and 404,496: N = sqrt(rest / W) read by counting alone.
- G2. 40,000 unticks return (a, b, s, f, r) = (10^6, 10^6, 0, 0, 0) at each depth. Round by round, untick(tick S) = S
  at 4,000 of 4,000 rounds above a notch and 4,000 of 4,000 at the click world's stride.
- G3, the no. The spring 4 g at W gives 1,274 (the reader 1,274): the face reads g / W.
- G4, the mutants, round by round over 4,000 rounds (above a notch / at the click world's stride):
  - m1, the face kept by the mirror: fails at 64 / 20;
  - m2, its tooth kept: fails at 128 / 60;
  - m3, one pair (now, next): fails at 128 / 40;
  - m4, "face = round": runs back (0 / 0) but counts 40,000 at W and at 4 W, where the face counts 637 and 318. So it
    fails at two depths, as Big Pic's item 3 says it must.

  My own measurement overturned my test here. The whole run's return (40,000 rounds) passed m2 and m3, since their
  errors cancel over a whole run that starts and ends with the tooth at 0. Only the round-by-round check catches them.
- G5, the calibre. At the click world's stride (the lay 40, spring 120,000, rounds 1 to 41,000, at most one count a
  round, 200 exact zeros) the face is 200 and the reader's 200; m5, the product's sign, counts 0 there and agrees above
  a notch; the run back is exact. The quarter mode gives the face 200 in 400 rounds at W and at 4 W. The rest's quarter
  spring (2 rest) gives 200 at W and 92 at 4 W, the lattice's angle (arccos 3/4 against a quarter turn) and not the
  continuum's square root, a reading at the cutoff.
- G6, the 48's -1. A gear leaving an exact 0 (now 40, before 0) against its negative: the face and its tooth (18, 1)
  both ways, kept. m6, the half-open sign alone: (18, 0) against (18, 2), not kept.

**face_p2_act (the engine's whole act, step.act on the loader's layout; output face_p2_act.txt).** The windows are
short by the hand-back time (rounds 1 to 40 on the full board, 1 to 300 on the lone Node-clock).
- A1, the click world as shipped (27 Node-clocks, 5 trains): one run back undoes one round at 40 of 40. The faces at
  site 0 after 40 rounds are [0, 0, 40, 0, 0]: the held hand 1 a round (Q2, T5) and the giver 0, its beat being 410
  rounds. m1 fails at 40 of 40. m3 is not caught in 40 rounds, since the held hand's quarter-turn pairs are all alike
  (2 each, Q2) and the giver has not crossed yet; the lone gear catches it (G4).
- A2, the 24 at a lone Node-clock (sides 1, 1, 1; the click world's law; the giver laid at (20, -11, 7; 0, 0, -4), at
  rest inside the held hand's room; the taker born at 0; two windows, rounds 1 to 200 and 1 to 300). Each turn was laid
  by each kind's matrix from the engine's kinds on the train's own rows. In both windows the turned run equals the run
  turned (counts and click teeth) at 24 of 24, and the faces and their teeth equal the unturned run's at 24 of 24:
  [0, 0, 200, 1, 0] and [0, 0, 300, 2, 0], the held hand 1 a round. The half-open mutant m6 also holds 24 of 24 here, since no gear of this lay left an exact 0 in the window
  (the taker's tooth stayed 0). So m6 is caught on the lone gear (G6) and not yet on the full act (OPEN 11).
- A3, the 48's -1 on the tied hands (every count of the giver and the taker negated at the lay). After 200 rounds their
  counts are the negated run's, and the faces and teeth are kept (m6 not caught, as in A2).
- A4, locality. The face's increment from each Node-clock's own columns equals the board's at 27 Node-clocks x 10
  rounds, with one Node-clock laid apart: 0 misses.
- A5, T6's no. The click world's law laid at 25,000 times (the key times its square, made odd) at one Node-clock: the
  held hand leaves its room at the first round (its counts -200,000,000 and 1, then about 4 x 10^16 at round 2 and
  10^50 at round 3), and its face runs at 2 a round (1, 3, 5, 7, 9, 11). The scaled world on the full board was
  stopped for the same cause.

## 4. Its own gear, or the Node-clock's? (the escapement)

- **DERIVED: a count since birth needs one gear of its own.** The act's state per Node-clock is two counts per gear and
  three bounded remainders (r in [-D, D), r_d in [0, T_d), k in [0, K)). The round is counted by the runner alone. So
  nothing in the act accumulates a clock's ticks (SHADOW 1.1, item 2), and a quantity that grows without bound cannot
  be any bounded remainder. FWDBACK3's escapement, (g, tau+) = carry(rest, L, tau), adds a tooth tau in [0, L): its
  releases g leave and are not held either.
- **Where the face's increment comes from: the Node-clock itself.**
  - (a) As built: the clock's own crossings (section 1). Its rate goes as sqrt(rest / W), read with no root (G1).
  - (b) If FWDBACK3's escapement stands: its release g, f+ = f + g. The increment is even under the reversal (rest +
    tau = g L + tau+ gives rest + (L - 1 - tau+) = g L + (L - 1 - tau) on a standing clock), so the same mirror
    (-f, flip) serves. Under the
    carried release (W_eff = L^2 / rest, every spring carried at its lapse) the release count goes as rest / L and every
    hand's crossings go as rest / L times its own rest beat. So the two faces stand in one ratio at every depth, and one
    gear carries both (Big Pic's item 1), to the calibre: the hunt's row 2 break parts them at a fast gear.
  - (c) As built, the release's rest / W is the square of every beat's rate sqrt(rest / W). A release face would then
    disagree with every hand at that Node-clock, so as built it is no clock's own count.
- **Where I part from Big Pic.** "No additional gear is needed to read time" holds for a reading of the beats on the
  board, from the ledger's counts. It fails for the click world: there the face must be held by the clock and read at
  its events, never computed (his own item 1), and the act as built holds no such count. So the face is one gear (two
  integers per train and Node-clock), with its increment from the Node-clock's own crossings or its release.

## 5. Special and general relativity (the owner's word of 01:0x UTC)

1. **A standing clock (both theories).** Its own count between two of its events is its face's difference (D6). The
   face changes nothing in the act's state. The theories ask nothing more of it at one Node-clock.
2. **The special theory: a moving clock (DERIVED, a no).**
   - A Node-clock never moves, so a moving clock is a pattern, and the face counts the crossings of the gears at its own
     Node-clock. For a packet A(x - v t) cos(k x - w t), a fixed Node-clock's face counts the carrier's half periods at
     the rate w / pi, the lab's.
   - The moving clock's own count is its phase along its path, at the rate (w - k v) / pi = m sqrt(1 - v^2) / pi for
     w^2 = m^2 + k^2 in the continuum. That count is spread over the Node-clocks it crosses, and the faces' differences
     between two sites hold the spatial phase k (x2 - x1), a hand's phase, which stays on the board.
   - So no face at a fixed Node-clock gives a moving clock's own count.
   - What would: Big Pic's bound pair (6537034824 item 3), two tied hands carried as one packet. Its inner passing
     clicks steadily, so its ticks are its own clicks, named by its lay on every click (1.2's K4). Its count crosses as
     events, its clicks counted between two meetings, and no phase has to. The dilation is then the pair's own E^2 =
     p^2 + m^2.
   - OWED: no world lays a moving bound pair (G6). The click world's pair stands and is not steady (runs of 1 to 7
     lines; SHADOW).
   - Light's two-way speed. A clock's echo count to a mirror a fixed number of Meshes away. For a standing clock it is
     alike along x, y and z by the 24, which permute the axes on a board alike along them (T3's equivariance, a board
     statement). Along a diagonal, and for a moving clock, it is alike only at the calibre, in long waves: the act has
     no boost (RECHECK qa_phys 5). OWED in the click world: light writes no click line.
3. **The general theory: the redshift.** On the board the face counts 637, 318 and 159 at W, 4 W and 16 W (a board
   reading). In the click world it is two clocks of one kind at two depths between two light links, read twice:
   - (1) n of the deep clock's faces between two emissions, against the high clock's face difference between the two
     takes;
   - (2) the link back, the two ratios reciprocal.

   OWED: reading 7; no world holds a well and a click line; light writes none.
4. **Does this change the gear?** Its form, no. Its scope, yes: the face is the standing clock's count; a moving clock's
   count must come from its own clicks, not from a face; and the header must give each clock's rest beat, since two
   kinds' faces compare only as a ratio of beats (Big Pic's item 1). The act as built gives every spring's beat and
   light's the same factor sqrt(rest / W) at one Node-clock (one redshift for every clock, to the calibre). Under
   FWDBACK3 the factor is rest / L.

## 6. The record's 1.4 line, and the click-world readings owed

- **Header:** "clocks", per train, its rest beat as the pair [g, W] of the dispersion's measure 4 sin^2(w / 2) = g / W
  (the train's own spring at the lay, and the rest teeth), and per site its face and tooth at birth [f, r].
- **Click line:** {"kind": "click", "round", "site", "train", "q", "tooth": [k, k+], "face": [f, f+]}, the clock's face
  before the round and after it, read from the state as the tooth is (run.clicked reads before.f and after.f), never
  computed. The run back's line would carry [-f+, -f].
- **End:** "faces", the last face and tooth of every clock.
- **D6 on 1.4:** at one clock (site, train) and two of its lines m < n, its own count is face_n[1] - face_m[1], the
  decoder's 1.2 formula with "face" for "tooth": whole half beats, never below 0, within one half beat at each end
  (T1's booking). Asked between two clocks with no two common events, it is refused (D7's rule).
- **The click-world readings, owed (nothing here is read in the click world tonight):**
  - D6, twice: one clock's faces at two of its events, against its partner's at the same two meetings (two clocks of
    one kind at one place). It needs a 1.4 record far above a notch, which tonight's clicking law cannot lay (T6), so
    on the click world's own law it would read the act's rhythm about a notch, named as such.
  - The twins: the bound pair that travels (5.2).
  - The redshift: two faces at two depths between two light links (5.3).

## 7. OPEN (one line each)

1. A clicking clock far above a notch (T6: the held hand's room bounds tonight's law to a few counts a round), its 1.4 record and D6 read on it twice.
2. The face of an E hand: E's matrices are no signed permutations, so the 24 do not keep it.
3. The half-speed hand's face on a 4-gear Hurwitz hand, where (+-1 +-i +-j +-k) / 2 are no signed permutations.
4. The rest beat's form in the header for a tied hand, whose spring reads the held hand's norm at the lay.
5. The moving clock: a bound pair that travels and clicks steadily, named by its lay (G6, K4).
6. The redshift: light's links (reading 7) and a world with a well and a click line.
7. Light's two-way count along the Spokes and the diagonals, and for a moving clock, in the click world.
8. The escapement's release as the face's increment, if FWDBACK3 stands (the hunt's row 2 at a fast gear).
9. The quaternion probe (the 24's sandwiches, the units' counts, the three whole modes) as its own probe; covered tonight
   only by G5, A1 to A3 and paper.
10. The owner's word on the face as an act change, and the law lines it touches (line 35 item 5's beat, item 16's D6).
11. The half-open mutant m6 on the full act: a lay whose gear leaves an exact 0 inside the room (A2's taker stayed at 0).
12. The full act's run back over the click world's whole 5,000 rounds with the face (only 40 rounds round by round tonight).

## 8. The probes (beside this page; run from this folder with the venv's python -I)

- face_lib.py: the face's functions (below, varied, crossed, face_act, face_mirror, face_untick; the lone gear's
  gear_face and gear_mirror). No if, loop, mask or bound in them.
- face_p1_gear.py, output face_p1_gear.txt: G1 to G6, about 2 s.
- face_p2_act.py, output face_p2_act.txt: A1 to A5 (A2 at 300 rounds), about 1 minute; with the argument turns it
  writes face_p2_turns.txt (A2 to A5, A2 at 200 rounds). A first version, whose world scaled 25,000 times left the
  room, was stopped and replaced (A5 keeps that world as T6's no).

They keep the laws: whole numbers only, Rule3's carry the one division, no float, true division, root, round, math,
random, fractions, decimal, sine or cosine; paths by joinpath; no train named in code (the square by its flag). The
reader beside the face in face_p1_gear compares, outside the act, as SHADOW's did. The engine and the branches are
untouched; nothing is committed or pushed.
