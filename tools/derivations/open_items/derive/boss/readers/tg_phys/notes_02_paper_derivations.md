# Notes 02: what follows on paper from the symmetric law, before any probe

Law: 4 W (q - v) + q^2 + v^2 = 4 push + s - s+, W = W(a) the pivot, v = W(a) - W(b), q = W(a+) - W(a).
Act: M = 8 W^2 - D_in^2 + s + 4 push, u nearest root (u(u-1) <= M < u(u+1)), s+ = M - u^2, W(a+) = u - W.

## D1. v = 0: the symmetric form IS the carry (identical act)
D_in = 2W, M = 4 W^2 + s + 4 push. u = 2W iff 2W(2W - 1) <= M < 2W(2W + 1) iff -2W <= s + 4 push < 2W: the carry's own
cell at the dial 2D = 4W. s+ = s + 4 push: the carry's own tooth. So wherever the 00 slot does not move by a whole count
in a round, the root is u = 2W with no search, and the form coincides with every carry form (the edge, the carried dial
with D = 2W, the twin at rest). The root decides nothing at v = 0.

## D2. v = +1, push = 0: the quotient is 1 for ever (the lock-in), exactly
D_in = 2W - 1, M = 4W^2 + 4W - 1 + s. Cell of u = 2W + 1: [4W^2 + 2W, 4W^2 + 6W + 1].
M >= 4W^2 + 2W iff s >= -2W + 1 = -D_in: always (the tooth is within its dial). M <= 4W^2 + 6W + 1 iff s <= 2W + 2:
always (s <= D_in - 1 = 2W - 2). So q = 1 whatever the tooth. s+ = M - u^2 = s - 2.
New dial D_in' = 2W + 1 = 2W' - 1 (W' = W + 1); s+ >= -D_in' iff s - 2 >= -2W - 1 iff s >= -2W + 1: holds. The tooth
keeps a FIXED distance from the bottom of its dial (both move -2 a round). The quotient never falls, never rises.
With push >= 0 the same: q = 1 for ever. With push < 0 the tooth falls to the bottom and q -> 0.
Nature's (the text's own continuum): W v' + v^2/2 = 0 -> sqrt(W) v kept -> v = sqrt(W0/W) falls; W ~ t^(2/3).

## D3. v = +2, push = 0: the tooth drifts -8 a round, the bottom bound -4 a round: it falls out after ~ (s0 + 2W0)/4
rounds; on the overflow q = 1 and s+ lands at the TOP (s+ = 2W, D_out = 2W + 1); then v = 1 and D2 applies: locked at
1 for ever. So a free rising clock under the symmetric form: v decelerates about like nature while |v| >= 2, then
sticks at 1 for ever.

## D4. v = -1 (falling): D_in = 2W + 1, M = 4W^2 - 4W - 1 + s; cell of u = 2W - 1 is [4W^2 - 6W + 2, 4W^2 - 2W - 1];
M in it iff s >= -2W + 3; s+ = s - 2 while the bottom bound -(D_in) RISES 2 a round (W falls): the tooth hits the bottom
after ~ (s0 + 2W0)/4 rounds, q = -2 for a round, and the fall accelerates: v -> -2 -> -3 ... Nature's too (sqrt(W) v
kept with v < 0: |v| grows as W falls; W reaches 0 in finite time, the probe's "no lawful split" at round 6667 for
v0 = -100 from 10^6 is nature's own W^(3/2) = W0^(3/2) - 150 t = 0 at t = 6667). The quirk is one-sided: rising at +1.

## D5. No integer invariant: the symmetric form has no books
Seek Q = s + g(W(a), W(b)) with Q+ = Q + 4 push. Needs g(x, W) - g(W, y) = x^2 + y^2 + 2W(x + y) - 6W^2 for all x, W, y.
Setting y = W then x = W gives g(W, W) - g(y, y) = -2 (W - y)^2, impossible for a function of one variable (W = y + 1
gives g(y+1, y+1) - g(y, y) = -2, so g(y, y) = -2y + c, then g(W, W) - g(y, y) = -2(W - y) != -2(W - y)^2).
The carry forms have P = 2 D v + s with P+ - P = 4 push exactly (the second difference of W^2 is the push: W v' + v^2 = F,
W v kept). The symmetric form's "books: the round's identity 0 misses" (TIMEGEAR table, s.3) is the law restated: a
tautology, not a book. Its sqrt(W) v is kept only in the continuum, to be read by windows.

## D6. The register's pump needs the spacing 2 exactly
E+ = -E - (W(a+) - 2 W(a) + W(b)). Quotients 1, 0, 1, 0: second differences -1, +1, ...: |E| grows 1 a round.
Quotients 1, 0, 0, 1, 0, 0: second differences -1, 0, +1, ...: E = 1, -1, 0, 1, -1, 0: BOUNDED. Any zero-sum pattern of
odd period, or any even period other than 2, gives a bounded E. So "growing without bound" needs v = 1/2 held exactly.
To measure: does the alternation hold for 10^6 rounds, or does the pumped dial move v off 1/2 and stop the pump?

## D7. The twin's parting is the same half-count event
A on B's dials: N_A = 4 W(b_B) v_A + s_A at 4 W(a_B): s_A+ = s_A - 4 at v = 1 while the dial grows 2: A's tooth
reaches the bottom after ~W0 rounds (10,000), q_A = 0, A freezes; B's dials 2 W(a_A), 2 W(a_A+) then stand, and B's
momentum 4 W(a_A) v_B + s_B at a standing dial keeps v_B = 1 for ever. The parting is the whole-number quotient at
v = 1/2, as is the carried dial's pump and the symmetric form's lock-in: three faces of one coin.

## D8. Nature's W at the text's marks (rest 10,000, v0 = 1, 30,000 rounds)
W^(3/2) = 10^6 + 1.5 x 100 x 30,000 = 5.5 x 10^6 -> W = 31,15x (176.5^2). The text and probe_tg9 print "about 26,600":
wrong; 26,458 is W v kept. Check by whole numbers (the probe's own formula 4 W0 W^3 = W0^2 (2 W0 + 3 v0 t)^2 gives
W^3 = 10^12 x 30.25 -> W = 31,153).

## D9. The forms at v0 = 1 against nature's 31,15x: the carried dial 29,999 (-3.7%), the twin's halves 19,999 and
40,000 (the mean 30,000: -3.7%), the symmetric form 40,000 (+28%). By the clock's course the symmetric form is the
farthest from nature at the one velocity the text's own calibre words put the clock at ("2 counts a round against
2W ~ 10^23"). To be measured longer (10^6 rounds) and at W0 = 10^5, 10^6.

## D10. "Nature's form" for the lapse itself
sqrt(W) d_t (sqrt(W) d_t a) = F is the equation of a TEST field under the lapse N = sqrt(rest / W) with a uniform N
(mc_phys item 1). Applied to the 00 row it says: the lapse is a test field in its own lapse. GR gives the lapse no
equation (a uniform lapse is pure gauge; with flat slices and zero shift the Hamiltonian constraint leaves N no
dynamics); Nordstrom's scalar has a flat d'Alembertian (v kept uniformly) and a conformally flat metric, not the
engine's lapse-only one. Nature therefore gives the 00 row's own motion no form; it gives two constraints only: one
cone for its wave, and a uniform rate change unseen by two clocks at one site. The text's "nature's form" is the same
over-claim the final physicist struck from EDGE (item 1: "strike nature's, name it CHOSEN"). The one honest sense:
"the form every other field obeys under the lapse, applied to the lapse itself" -- a self-consistency choice.

## D11. The mean's drift under the 00 wave (tg7 C)
Summing the law over the sites of a periodic line (SUM push = 0) and over time: 4 SUM_t SUM_x W (q - v) = -SUM (q^2 + v^2)
+ bounded: the W-weighted mean acceleration is negative; the mean of the 00 slot falls quadratically, by about
<v^2> t^2 / (4 W). With A = grip/1000 (2A at site 0), omega = 2 pi / 21.7: v ~ 2A omega ~ 0.58 A/round... the drift
reaches A within ~ sqrt(4 W A / <v^2>) ~ sqrt(4 x 12000 A^2 / (0.17 A^2)) ~ 530 rounds: the probe's crossings of the
fixed base stop at round 1037 for that reason. The carry forms conserve SUM_x P exactly, so their mean does not drift.
The measured 1008 and 1006 permille are then a measurement on a drifting baseline (and of only 48 periods), not the
cone. To be measured drift-free: the period of the mode's projection SUM_z m_z a_z, m = (2, 1, -1, -2, -1, 1), which
kills the uniform drift; at three amplitudes; by windows (first and last 3000 rounds). If the deviation scales as A^2
it is the nonlinearity; if it vanishes it was the baseline.
