# Findings on TIMEGEAR (tg_math, hostile mathematician), measured

Probes here: probe_tgm1_onestep (live venv), probe_tgm2_floor (live venv), probe_tgm3_board (t24b venv: the harness's
own tree; the live loader and State have moved, edge_lib cannot load a board under live). Whole numbers, Rule3's carry
the one division, no root, no search, no float.

## F1 (MINOR, the one-line result, s.2 Theorem 2, s.5): "its one division is an integer root" holds only beyond a
bound the text does not name. With c = 4 W(a) - D_in = 2 W(a) + v (from the two slots) and R = M - c^2 = 4 push -
2 v^2 + s: k0 = the half-open carry of R at 2 c (Rule3), low = k0 (2 c + k0 - 1) - c, k = k0 - [R < low] (one
sign-carry, d div (d^2 + 1), the same formula for every integer, as lit()), u = c + k. Proof (01_paper_derivation
s.4): k0 = k + floor((k^2 + s+ + c) / 2c), the floor 0 or 1 for every tooth iff k (k + 1) <= 2 c. Measured (tgm1 A):
over 2670 pairs (c, k), c <= 60, the rule is exact on 896 and the predicate k (k + 1) <= 2 c holds on exactly those
896; the post-check u (u - 1) <= M < u (u + 1) (two products) catches 25484 of 25484 misses. So wherever the
velocity's change in one round, k = q - v, obeys k (k + 1) <= 2 c = 4 W(a) + 2 v, the root form's act is two Rule3
carries and products: that is every one-gear course on which the text measures its physics (probe_tg7 B, probe_tg9,
tgm2: k in {0, -1}, the check never failed over 10^6 rounds). Beyond the bound the carry's estimate is off by about
k^2 / 2c cells and only a search closes it: on the text's own boards (the mode A = grip / 1000 on the 00 row, W = 12
grips) the 00 count's change of velocity is ~10^17 counts a round squared against 2 sqrt(W) ~ 8.5 x 10^11 (tgm3 A1,
A2: refused at round 1 down to A = grip / 10^9; exact at grip / 10^10), and a swing of one notch (a grip = 1.5 x 10^22
counts) with term 9's 140 rounds is ~3 x 10^19. The text's notes_02 line 26 ("u = c + k, k the cell of R among
[...]") is one line short of saying this. Fix: name the bound in the result and in s.5 ("a root where k (k + 1) >
2 c, Rule3's carry and a sign-carry within"); the owner's question stays "the root or a price", because notch-scale
motion of the clock lies beyond the bound.

## F2 (MINOR, s.2 Theorem 2 and s.5 the law line): "the whole number nearest the root" misnames the quotient at the
tie M = u (u + 1): the cell [u (u - 1), u (u + 1) - 1] gives u + 1 there while the integer nearest sqrt(M) is u
((2u + 1)^2 = 4 M + 1); with the words as written the tooth would be s+ = u, outside [-u, u - 1] (tgm1 C, u = 1..6).
The cells are right (the only ones whose tooth range is mirror-symmetric). Fix: "the u with u (u - 1) <= M < u (u + 1)".

## F3 (MINOR, s.2 "a bijection"): the forward map is injective and runs back exactly where defined (tgm1 B: 0
collisions, 0 misses on 12 exhaustive sets) but it is not total and its image is not its domain: no image where
W(a+) < 1 (M < W (W + 1), roughly v < -0.646 W), 36 of 264 states at rest 6, a = 0, push 0; and of 204 images 50 have
no image of their own. The same holds of every W-form (the falling clock reaching 0). Fix: "injective, inverse exact,
on the states whose next teeth are at least 1" in place of "a bijection on the state".

## F4 (MINOR, s.2 Theorem 1, wording): "an in dial that moves with its before slot ... so the forward map collides"
is refuted by the text's own Theorem 2 (the symmetric form's in dial moves with the before slot and is injective).
Theorem 1 holds for cells of ONE length (the standard centre 2 q D_out). Fix: add the hypothesis.

## F5 (MINOR, s.2 Theorem 2, last sentence): "any other centre ... keeps the forward bijection and loses the run back
(probe_tg1: 95 misses of 176)" contradicts probe_tg1's own line for that centre: 36 collisions and 70 with no lawful
split. Fix: "collides forward and misses the run back".

## F6 (MINOR, the uniqueness theorem's hypotheses): forced only under (H1) the tooth's range is the edge's dial
W(x) + W(y); (H2) the round is N = C(q, v, a) + s+; (H3) the cells in the ORDER of q; (H4) W linear in the count
(the gap (2q + 1) dD uses dD = 1). Every reversible two-slot law is M o phi^-1 o R o phi with phi a bijection of
(slot, tooth) pairs onto a range of Z and R an involution of Z (01_paper_derivation s.1); the text's law is the
ordered phi with R(X) = -1 - 4 push - X. Fix: list the four as hypotheses; (H3) is physics (velocities ordered).

## F7 (MINOR, s.4 "nature's form", s.5 "none measured but the quirk"): the quirk is the asymptote of every free
rising clock. At v = 1 the cell of u = 2W + 1 contains the whole tooth range (s in [-2W + 1, 2W + 2] against
[-(2W - 1), 2W - 2]), so q = 1 for every tooth and s+ = s - 2 with s + 2W - 1 invariant: the clock never slows again.
Measured (tgm2 A, rest 10^4, 10^6 rounds): v reaches 1 at round 5000 (v0 = 2), 16665 (3), 51181 (5), 209369 (10)
and W then runs linearly; W against nature's course at 10^6 rounds: 45186 permille (v0 = 1), 11541 (2), 5346 (3),
2195 (5); nature is kept (999 to 1011) only while v >= 2 (v0 = 30: v = 2 at 10^6 rounds, 990; rest 10^6, v0 = 100:
999 at 10^6 rounds with v = 19). The falling clock has no floor (tgm2 C: v = -1 to -2 at round 5001, the fall
quickening to the end at W = 15). Weighing: one count a round is 10^-22 notch a round at the file's grip (den
full_rate^2 = 1.5 x 10^22 counts a notch), so the floor lies beyond any physical course; but the carried dial's "pump
at the half count" (2 counts a round against 2 W ~ 10^23, the text's own words) is a sub-count effect of the same size,
and the text weighs it as a price while calling this one a quirk. Fix: name the regime (|v| >= 2 counts a round) and
weigh the two sub-count effects alike; the discriminating physics is the equation of motion (W v kept against
sqrt(W) v kept, and EDGE3's resonance at half the beat), not the half count.

## F8 (MINOR, s.2 Theorem 3): "the affine involutions are D -> g(a) - D" restricts without reason; the conclusion
survives for every involution: a register's departure E' = f_a(2W - v + E) - 2W - q cannot be 0 for all (v, q) at a
pivot (f_a would be many-valued), and a bijection has no attractor, so no register is damped. State it so.

## F9 (BLOCKING, s.2 "no carry meets ...", notes_02 "The theorem for the Boss", s.4 bullet 1, s.5): the theorem's
case analysis misses a sixth carry form, so "no carry meets the four conditions ... proved in section 2" is not proved,
and s.4's universal "every one-cone carry at W puts the velocity's weight at the dial ... W v kept" is false. The
form: the cut's constant dial 2 rest on the 00 row with its push carried at rest / W(a) by one carry (the nearest
whole, (2 P rest + W(a)) div 2 W(a), the remainder dropped), every other row on the edge. Two slots, two carries, no
register, no root; (C1) and (C2) hold at once (the dial constant), so the forward map is a TOTAL bijection and the run
back is the same act. Measured (tgm3 B, C, the harness's own lays): the cone T_light^2 / T_00^2 = 1012 and 1009
permille at A = grip / 1000 (W = 12 and 24 grips), 1066 and 1084 at grip / 10 -- the order's and the act as built's
numbers to the round (34 periods over 733 rounds, 48 over 1468), which the text's s.5 table counts as one cone;
untick(tick s) = s 40 of 40 and rewound on the standing, rising and falling lays (the falling one running all 40
rounds, W from 60 to 20 grips); the 24 at every one of the 40 rounds; the 00 row's books close on 4 SUM P' (0 misses).
Its price, named: the push's remainder at W(a) is dropped (a floor on the push, the sub-notch push lost; a kept
remainder tooth at the modulus W(a) is impossible, since the modulus changes between the round that makes it and the
round that reads it and no slot-symmetric flip is then an involution), and the clock's own physics is the act as
built's (v kept free; a'' = P / W(now), which EDGE3 measures pumped x4.92 at half the beat). None of the five prices
the text lists (a second cone, a booked line, a pumped register, a parting pair, the edge's W v) is this one. The
conclusion "no carry meets one cone, a bijection, nothing written AND no price" may yet stand on the fourth condition,
but it is the owner who weighs a floor on the push against a root, and he has not been shown the form. Fix: add the
form to s.5's table with its numbers and its price; restate the theorem's proof with the case "two carries, the dial
constant, the push scaled" and the general statement of 01_paper_derivation s.2 (any dial read from the counts is
non-constant in the next count; a constant dial needs the push scaled; a scaled push drops a remainder).

## F10 (MINOR, s.4 one cone, probe_tg7 C): the symmetric form's 1008 / 1006 permille is the amplitude's. Measured
with no root (tgm3 A2) at A = grip / 10^10 and grip / 10^11: 275 periods over 5965 rounds at W = 12 grips and 194
over 5961 at 24 grips, light's to the round, 1000 permille (the carried 00 the same). At A = grip / 1000 the one-step
rule is refused (the root regime), so the text's 1008 / 1006 there stands as measured by its search, with the wave's
mean drifting off its base (crossings over 1037 and 2113 rounds against light's 5965). Fix: say "1000 at small
amplitude; 1008 / 1006 at A = grip / 1000 from the q^2 + v^2 term".

## F11 (MINOR, process): probe_tg7 and probe_tg9 compute the root by a Newton search. As a MEASUREMENT it is fair:
the while loops make u the exact cell, verified by u (u - 1) <= M < u (u + 1), and the course measured is the form's.
Under the owner's word of 2026-10-30, 03:0x UTC ("A root is forbidden" of the derivation probes, ALGEBRA.md line 102)
the probes themselves stand outside the law; tgm1 to tgm3 measure the same form with two carries and the cell check,
so the measurement can be made lawfully (and F1 follows from doing so).

## F12 (MINOR, s.5 "it touches Postulate 6 nowhere"): EDGE2 s.4 names Postulate 6 ("no coupling of the time gear
with itself") as the cut's law line; every form of this page has the 00 row's dial read its own count. Whether a
dial read is "a coupling" is the Boss's to settle with the writer; the text should say which reading it takes.

## Sound (checked on paper and by probe)
- The run-back identity (R) and the forced centre under (H1)-(H4): re-derived by hand, exact.
- The law D_in^2 + D_out^2 = 8 W(a)^2 + 4 push + s - s+, its symmetry under (D_in, s) <-> (D_out, -1 - s+), its
  act M, u, s+ = M - u^2, W(a+) = u - W(a): consistent; injective (D^2 - s on [-D, D - 1] tiles [1, inf)).
- 0 collisions and 0 run-back misses on 12 exhaustive one-gear sets (tgm1 B), as probe_tg7 A (300 states, 0, 0).
- Two slots, one carry of one length, one cone, exact mirror: only the cut (the text's Theorem 1 with its hypothesis;
  my section 2: any symmetric dial with D'(x, x) = 2 W(x) has non-constant cell widths).
- The carried dial's departure E' = -E - (q - v) (second differences) and its pump at q = 1, 0, 1, 0 (1 a round):
  re-derived; probe_tg9 A's 20,001 at round 30,000 follows.
- The twin's run back (notes_02): re-derived line by line, exact; its parting at the half count (A at q = 0 with
  dials 2 W(b_B), 2 W(a_B) rising, B at q = 1 on A's standing dials): re-derived; probe_tg9 B's 19,999 / 40,000 follows.
- The free course of the symmetric form keeps sqrt(W) v while v >= 2: 999 to 1011 permille over 10^6 rounds
  (tgm2 A v0 = 10, 30; B v0 = 100), extending probe_tg7 B's 30,000 rounds by 33 times.
- One cone for the symmetric form: 1000 permille at A = grip / 10^10 and 10^11 (tgm3 A2), light's crossings to the round.
- The root is a root on the text's boards: at A = grip / 1000 the carry's estimate is 8.8 x 10^12 cells off (tgm3 A1).
- probe_tg7's and probe_tg9's search computes the exact cell (the while loops), so their courses are the form's own.

## F13 (MINOR, s.3 table, probe_tg7 D): the symmetric form's "40 of 40 and rewound" on the lay falling by 1 grip a
round from W = 60 grips ends with W_00 at "0 grips - 382 permille" (the probe's own line): the clock's teeth below 0
on the last state. tick_sq (the board) checks only that the root exists, not W(a+) >= 1 as step_sq (one gear) does,
and run_sq checks the promise before a tick, never on the last state; nature's course from 60 grips at -1 grip a round
reaches W = 0 at round (2/3) 60 = 40 exactly. The carried forms' rows say "falling lays end where the clock reaches 0";
the symmetric form's row should say the same (39 lawful rounds, not 40). Fix: the board tick refuses W(a+) < 1.
