# The escapement: the Node-clock's act on a moving clock with time forward and backward, and no price

The Boss's deriver, 2026-10-30. On the owner's ruling "no price is allowed; solve it with time forward and backward" and
his word "the return in time is simply more gears, and there are differences between them". Read first: edge/EDGE2.md,
EDGE3.md, ROOT.md; rd_math/REPORT.md, rd_phys/REPORT.md (the physicist's theorem); mc_phys/REPORT.md;
edge_final_phys/VERDICT.md; quaternion/ONE_ALGEBRA.md (the double Node-clock, the root dial); c4_math/03_report.md
item 1; timegear/notes_01_derivation.md. Probes beside this page, whole numbers and tensor24.algebra.carry.carry the one
division, no float, root, round, math, random, fractions or decimal, paths by joinpath, no train declared (the example
universe's and SYM24's files read): fb_lib.py; probe_fb1_onegear, probe_fb2_board, probe_fb3_cone, probe_fb4_plan,
probe_fb5_hostile, each .py with its .txt; rerun/ holds every probe rerun byte for byte. Working notes: 00_notes_read,
01_derivation, 02_mirror_finding. Status: DRAFTED, for a hostile mathematician and a hostile physicist.

## 0. The answer in one paragraph

Nature's equation on a moving clock, L d_t (L d_t a) = F, is autonomous in the clock's own time: d^2 a / d tau^2 = F.
So the clock should not divide the push; it should divide TIME. The Node-clock gets one more gear, its escapement: a
first-order gear (the drive's kind) whose dial is the clock's count read at both slots, D = L(now) + L(before), pushed
by 2 L_0 every round; its whole turn (0 or 1) releases the whole train once, and every gear then steps at its REST
teeth, the standing act as built, exact and bijective. The clock's depth decides WHEN the gears turn, never by how much.
The run back is the same act on the mirrored state; the mirror flips the escapement's tooth at D and swaps the slots of
the gears that turned, which the escapement's own carry on the flipped tooth says. Measured: a free row keeps
sqrt(W) v, a hairspring its amplitude, nothing is pumped at any swing, two clocks at one site see nothing new, the 00
row runs on light's cone, every push is kept with its remainder, the kick of 1 is alive, the board's momentum is exact
on a uniform clock, the run back is exact and the 24 hold at every round on standing, rising, falling, varying,
swinging and non-uniform clocks, with J through the tables. What changes in the law: the 00 slot enters the clock's
count L = L_0 + c (linear, L_0 = rest + rest), and W = rest (L / L_0)^2 becomes a reading (rest + c to first order),
not the teeth. What it is not: the mirror is not an involution on a moving clock (a theorem: no involutive mirror
places the pivot of a round that stood), and the domain is a clock at or below its rest rate (c >= 0 at both slots),
read by the promise as W >= 1 is today.

## 1. The theorem the drafts share, and the hypothesis time forward and backward removes

**Theorem 1 (the one-tooth no-go).** Let a gear's state be (now a, before b, one tooth s), and let a round at the pivot
a carry m_in(a, b) (a - b) + s + c F(a) and split it at m_out into (v+, s+), the run back being the same act on the
state with the slots swapped and the tooth flipped. Then (C1) across rounds the tooth produced in [0, m_out(prev)) is
weighted by m_in(now): injective iff m_in = m_out(prev); (R1) within the round the mirror reads s+ at m_in(a, a+) and
must produce s at m_out(a, a+, b): one function m with m_in = m(a, b), m_out = m(a, a+). Both on a falling course
force m symmetric in its two slots, hence m(b, a) = g(W) at the half step to first order and the physics
d_t (g(W) v) = F. Nature needs g = sqrt(W), and no polynomial in W(a), W(b) gives it; no coefficient on F mends it (the
integrating factor of W dv + (1/2) dW v = F is sqrt(W) whatever multiplies F). Quarter-step dials ((W(b) + 3 W(a)) / 4
in, (3 W(a) + W(a+)) / 4 out) give nature's ratio and fail (C1) on a falling clock. The root dial takes L = sqrt(W)
whole and pays with the push's remainder at the pivot's L, which no bijection carries to the next pivot's dial (the
physicist's theorem, rd_phys item 1): a fraction with the denominator D_in is not a fraction with the denominator D_out.

The hypothesis every form shares: **the clock enters the act by dividing the push, or the momentum, at a dial that
moves with the clock.** Time forward and backward removes it: the clock is read at both slots into the dial of a gear
that divides the ROUND, and the gears' own carries stay at standing dials. The remainder carried across rounds is
time's, whose push 2 L_0 never exceeds its dial D >= 2 L_0; the force's remainder has no such bound. That is why the
theorem bites the push and not time.

## 2. The clock layer

A clock has an escapement: it releases the train one tooth at a time, and a deeper clock's escapement, with more teeth
on its wheel, releases less often. Every gear of the Node-clock turns only when the escapement releases, and then by
exactly what the standing act gives it. The 00 slot is the escapement's extra teeth; the before slot is the backward
gear and the now slot the forward gear (ONE_ALGEBRA's reading of the owner's words), and the escapement's wheel is the
two of them together, D = L(now) + L(before): time forward and backward is what the escapement reads. The return in
time is the same gears run back; the gears that did not turn have nothing to run back, and the escapement alone
reverses.

## 3. The algebra

Per Node-clock one tooth tau; per gear (a, b, r, r_d) as built. L(x) = L_0 + x_00 (the clock read of the 00 slot at
the slot x, the loader's lay: every square train's 00 slot at the factor 1), L_0 = rest + rest.

    D = L(a) + L(b)                                   (the escapement's dial, read forward and backward)
    q_tau, tau+ = carry(L_0 + L_0, D, tau)            (the escapement; q_tau in {0, 1} for D >= 2 L_0)
    q, r' = carry(rest (a - b) + s (F + T_k q_d), rest, r);  q_d, r_d' = carry(J, T_d, r_d)   (the standing act)
    a+ = a + q_tau q;  b+ = b + q_tau (a - b);  r+ = r + q_tau (r' - r);  r_d+ = r_d + q_tau (r_d' - r_d)

Additions, multiplications and Rule3's carry, nothing else; no compare, floor, mask or bound; the 2's are the two slots
(L_0 + L_0, rest + rest). W is computed nowhere. The mirror:

    q = carry(L_0 + L_0, D, D - 1 - tau)'s quotient    (did the escapement release in the round that made this state)
    tau -> D - 1 - tau;  a -> a + q (b - a);  b -> b + q (a - b);  r -> r + q (rest - 1 - 2 r);  r_d likewise at T_d

untick = mirror o tick o mirror. Rule (i): tau is born at D div 2 (the half dial), like every remainder. Rule (iii):
tau is flipped at the dial it was kept at, D, which is the same number before and after the swap. The promise, read
from outside as today: L >= L_0 at both slots, tau in [0, D), r in [0, rest).

**Theorem 2 (the run back is exact).** In the domain D >= 2 L_0 at every round: (a) q_tau <= 1, since tau < D and
2 L_0 <= D; (b) after a release tau+ = tau + 2 L_0 - D_in < 2 L_0 <= D_out, and after a stood round D is unchanged, so
the tooth always stands within the dial that reads it; (c) the mirror's q equals the round's q_tau: for a stood round
the flipped tooth D - 1 - tau - 2 L_0 plus 2 L_0 is D - 1 - tau in [0, D), quotient 0; for a release, the flipped tooth
at D_out plus 2 L_0 is D_out + D_in - 1 - tau with 0 <= D_in - 1 - tau < D_out (the release needs
tau >= D_in - 2 L_0, and D_out >= 2 L_0), quotient 1; (d) a stood round runs back by the escapement alone: the
backward carry gives (0, D - 1 - tau) and the second flip gives tau, the gears untouched and their now slot the pivot,
so every neighbour's backward pull reads what the forward pull read; (e) a release runs back as the act as built at
fixed teeth (the mirrored slots at the pivot a, the backward carry at D_out of the state (a, a+), the gears' standing
carry's lemma, the final flip at D(b, a) = D_in and the final swap by q = 1). Measured: probe_fb1 C (0 misses of
30,000 and 28,000, rewound), probe_fb2 (40 of 40 and rewound on twelve lays), probe_fb4 (6 of 6 with J), probe_fb5 D,
F, G, H (clocks halving, doubling, at the edge L = L_0, alternating; tau at 0 and D - 1; a step every 21st round;
a ring; two clocks on one Mesh, 400 of 400).

**Theorem 3 (no involutive mirror).** Hypotheses: (i) a gear's slots shift only when it turns (a stood gear keeps
(a, b), the velocity per proper step); (ii) the escapement's tooth is flipped at its dial (Theorem 2 (c) needs it);
(iii) the mirror's placement of the slots is a function of the state. Then a mirror that places the backward pivot
right must swap the slots of a gear that turned and leave a gear that stood, so it depends on q_last = "did the last
round release" (the carry of the flipped tooth); the time reversal of that fact is q_next = "will the next round
release" (the carry of the tooth itself), and (ii) maps the one to the other; so mirror o mirror = swap^(q_last +
q_next), the identity only where the two agree, and no symmetric function of (q_last, q_next) places the pivot. The
symmetric dial D = L(a) + L(b) is what lets the stood round's mirror leave the gears and still flip and read tau at one
number, and what lands the release's final flip at D(b, a) = D_in: with the now slot's dial alone the mirror's q on
the backward output reads a wrong dial (02_mirror_finding). The other way, slots
that shift every round with the velocity in a register of its own, loses the last round's release altogether: the
backward round rebuilds the before slot as now - velocity, wrong after a stood round (02_mirror_finding, dead ends 1 to
5). Measured: mirror twice = identity on 41 of 41 states at c = 0, 14 of 41 at c = 6 grips standing, 8 of 41 rising
(probe_fb2). The law's (iii) holds of every remainder (two flips the identity at one dial); Postulate 2's run back by
the same acts in the reverse order holds bit for bit; what does not hold is a time reversal of a state that is its own
inverse on a moving clock, which the act as built has only on a standing clock (step.mirror's own docstring).

## 4. The event board

One pass at every Node-clock alike: the escapement first (at the state as it stands, no next count read, no fixed
point), then every gear of a released Node-clock steps once at rest on its pushes at the now slot and its six Meshes'
now slots. The 00 row is a row like every other: it steps at rest with the escapement, and its new count is the next
round's dial through both slots. No dial is moved by its own quotient. Sites step on different rounds where their
clocks differ; a stepping site reads its neighbours' now slots whether they step or stand (probe_fb2's non-uniform
lays, probe_fb5 H). The row's momentum SUM_sites (rest v + r) is exact wherever every site steps together (a uniform
clock: drift 0 on nine lays), and moves where sites step on different rounds (-249,248 grips over 400 rounds on two
sites at c = 0 and 12 grips): the lapse gradient's force, nature's d_t SUM pi = SUM N Lap a, which the act as built
does not have. The state gains one register per Node-clock (tau); the record's schema and the runner's promise gain it.

## 5. The physics behind the clicks

In proper time the gear is the standing act, so everything the clicks read of a hand is the standing clock's. Proper
steps per round 2 L_0 / D = L_0 / L at the half step (a free 00 gear rising 1 a step: 20,000 steps in 30,000 rounds,
the exact integral's 20,000). c^2 = (grip / rest) (L_0 / L)^2 and omega^2 = (g / rest) (L_0 / L)^2: the static act's
relations with W_eff = rest (L / L_0)^2, which is rest + c + c^2 / (4 rest): the law's "W = the rest + c, read at the
now slot" (line 35) becomes "the clock's count L = L_0 + c, read at both slots", W a reading, linear at first order
(Postulate 6 at first post-Newtonian order either way, as the root dial's readers wrote; 1 / N = L / L_0 is the
frame's time leg at the first power, ONE_ALGEBRA's root dial reading without the root). Measured on one Node-clock
(rest 10,000, L_0 20,000, the 00 gear free at +-1 a proper step, L 20,000 <-> 40,000, W_eff x4, by windows of 1,000
rounds; probe_fb1):

| | nature | the escapement, rising | falling | the act as built | the edge | the root dial |
|---|---|---|---|---|---|---|
| a free gear's v^2 W_eff over W x4 | 1000 | 998 .. 1000 | 999 .. 1001 | 3999 | 249 | 1000 (floor on F) |
| a hairspring's A / A0 | 1000 | 999 .. 1000 | 999 .. 1000 | 1166 | 857 | 999 .. 1000 |
| T^2 / W_eff over ten beats, at the span's mid clock | 1000 | 998 .. 1000 | 997 .. 1000 | 988 | 988 | 1000 |
| a swing of the clock at half the beat, 5 / 20 percent, 50 swings (A_end / A_start) | 1000 | 1000 / 1000 | | 4920 / 1280481 | 4780 / 1418793 | 1000 / 1000 |
| the beat, ten beats, and a scan of 72 to 92 rounds about the resonance | 1000 | 1000 at every one | | | | |
| two hairsprings at one site, T1 / T2 and A1 / A2 over L x1.8 | constant | 2012 .. 2016, 996 .. 997 | | | | |

(The act as built's, the edge's and the root dial's columns are edge/probe_root's and edge_final_phys/probe_fp_swing's
numbers, the clock's course given from outside; here the clock swings by the 00 gear's own hairspring, so the swing is
a lay of the board, not a course.) The residuals are the integer act's own: the amplitude A at 10,012,xxx against the
lay's 10,000,000 is the centred split's offset (rd_phys item 4), identical at every depth; T^2 / W_eff's 997 is one
round in a span of 630. The regime: many notches a stride (v0 = 10^6 a step; the push p >= 10 counts at rest 10,000:
probe_fb5 A, 1000 .. 1001 permille of nature) and below it the standing act's own sub-notch freeze (p = 1 for 2,000
steps moves nothing, as built the same).

**Every push kept.** The gear's carry is at the standing dial rest: a constant push p = 10, 49, 50, 51 .. 50,000 at
W_eff = 4 rest moves a(T) within 1 permille of nature's p T^2 / (2 rest) (the root dial's floor was L / 2 = 20,000
there); a hairspring g = 1 laid at a0 = 10, 25, 49, 50, 51, 100, 1000 swings between -a0 and a0 exactly (the root dial
froze a0 < 50); the kick of 1 moves one notch at proper step 5,000 = rest div 2 (the tooth born at the half); the ring's
long wave of peak 8,000 at W_eff = 4 rest has twice the period of the rest ring's (2,212 against 1,106 rounds over ten
periods) and runs back (probe_fb5 A, B, C, G).

**One cone.** On a line of 6, the 00 row's wave and light's wave have the same beat at every depth (T_light^2 / T_00^2
1000 at L = 18, 30, 66 grips on L_0 = 12), and both scale as W_eff / rest (2250 / 2250, 6252 / 6250, 30257 / 30250
permille; probe_fb3). The cut's second cone (2012, 4039) is gone with the cut; the 00 row needs no law of its own
beyond riding the escapement (what the timegear deriver's carried dial does for the edge form is not needed here).

**The 24 and J.** On edge_lib's board (12 rows, 324 gears): 24 of 24 at every one of 40 rounds on twelve lays
(standing at c = 0 and 6 grips, rising by 1 grip and 1 grip + 1, falling by 1 grip and 3 grips + 1, drawn in time, laid
per site in [40, 60] grips standing and moving, three swings of the 00 row); at c = 0 the act coincides with the act as
built state for state (40 of 40). With SYM24's plan 1 through the tables (s = 3, T_k = 2, T_d = 5, 18 rows): 24 of 24
at every round standing, rising, falling and at c = 0, the run back 6 of 6, rewound; the mutant with a flipped row's
drive tooth unflipped 3 of 24 (probe_fb2, probe_fb4).

## 6. What it costs and what stays OPEN (named, none a price of the physics)

1. **The law's line 35.** "W = the rest + c, read at the now slot" becomes "L = L_0 + c, read at both slots, L_0 =
   rest + rest; W = rest (L / L_0)^2 a reading"; term 2's teeth become the rest; term 13's N^2 = rest / W becomes
   N = L_0 / L (linear in c at first order: Postulate 6 at that order). The owner's word, as for the root dial (rd_phys
   item 3) but with no root, no square condition on den and no typed number: L_0 = rest + rest is the derivative of
   the square at c = 0, so that one count of the 00 slot is one count of W at first order.
2. **The domain.** D >= 2 L_0, that is c >= 0 at both slots: a Node-clock at or below its rest rate. Outside it the
   escapement's turn can be 2 (probe_fb5 E: q = 2 at c = -L_0 / 2, the run back 0 of 20) and the form is no act,
   as the act as built is none at W < 1. The promise reads it. If term 9's notch or term 5's push must take c below
   0, the lever is the rest clock's own rate: L_0 = 2 rest m^2 with the push 2 rest m (m a whole number of the file)
   makes the rest clock release one round in m and the domain c >= -2 rest m (m - 1), the effective rest m^2 rest;
   not probed here. OPEN with term 9.
3. **The mirror is not an involution** on a moving clock (Theorem 3); the run back is exact. If the law wants the
   state's time reversal its own inverse at every round, the escapement form cannot give it, and nothing with a
   skipping clock can.
4. **The half-step clock.** The escapement reads the clock at the half step (D = L(a) + L(b)): a bounded phase of at
   most (1 / 2) ln(L_end / L_start) proper steps over a course, no secular rate; a swing moves it back and forth.
   Measured only through the physics table (nature to the permille) and the step count (20,000 exact).
5. **The staircase.** Between releases a gear stands in coordinate time; at the calibre (c / L_0 about 10^-6 in a
   galactic well) one round in a million is skipped; in a well of L = 2 L_0 every other round. A click reads windows.
6. **The 00 row's own dynamics** is the metric's push (term 5, DRAFTED): on this board the 00 row's own pull at rest
   teeth moves a laid gradient of 20 grips by 5 grips a step (probe_fb2's non-uniform lays stay in the domain for 40
   rounds). Whether term 5 keeps c >= 0 is term 5's.
7. **The click teeth (term 11)** step with the escapement like r_d, at the standing key; not probed (DRAFTED there).
8. **The record and the runner.** NodeState gains tau per Node-clock; the promise gains L >= L_0 and tau < D; the
   runner's rewind is n unticks as today.

## 7. Solution24

1 (does it follow by itself: the standing act is exact and nature's in proper time; what did not follow was the
division of time, named as the escapement, one gear, not declared); 2 (the picture: a clock's escapement releases the
train; the 00 slot its extra teeth); 3 (the big things only: rest + rest and L_0 + L_0 are the two slots' counts; no
number, no root, no square condition; the form is DERIVED where nature's equation is autonomous in proper time and
CHOSEN nowhere); 4 (the four layers above); 5 (no click in it; the escapement's turn is no click, as the time gear's
turn is none); 6 (the books: per gear exact at rest, the row's sum exact on a uniform clock and nature's where the
clocks differ; the run back as the act itself on the mirrored state, Theorem 2); 7 (both ways: forward from the
escapement, backward from nature's five readings, each measured by windows at the stride named; the pump measured
across the swing's periods; what does not match nature is named: none found, the integer act's own offsets aside);
8 (every case run locally on the real act's carry, board and tables, src untouched); 9 (for the pair); 10 (one act for
every gear, the drive and the click teeth included; the 00 row no row apart; the 00 row's own law and the cut both
retire); 12 (what does not follow: the domain c >= 0 and the law's line 35, asked of the owner through the Boss).
