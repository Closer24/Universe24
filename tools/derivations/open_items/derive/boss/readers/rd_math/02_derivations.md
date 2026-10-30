# Derivations on paper (whole numbers), the root dial in the half-open convention

Notation. L(x) = L_rest + c00(x): the clock's count read at a state's slot x (the 00 row's value there, through the
clocks' linear read). D_in = L(b) + L(a), D_out = L(a) + L(a+). The tooth s in [-D_in, D_in - 1]. The push
F = F(a) (pull + kick, a function of the now slot alone, and of the drive's tooth r_d). q_F = odd(F, L(a)).
The round: N = 2 (D_in (a - b) + 2 q_F) + s; (q, s1) = split_up(N, 2 D_out), i.e. N + D_out = q 2 D_out + r0,
s1 = r0 - D_out in [-D_out, D_out - 1]; a+ = a + q, b+ = a.
The mirror: (a, b, s, r_d) -> (b, a, -1 - s, T_d - 1 - r_d).

## D1. The half-open split is odd with the tooth -1 - s, at EVERY dial parity (the dial 2D is always even)

If X = Q m + R with R in [-m/2, m/2 - 1] (m = 2D), then -1 - X = -Q m + (-1 - R) and -1 - R in [-m/2, m/2 - 1].
So split_up(-1 - X, m) = (-Q, -1 - R). No parity condition on D enters: the split is at the dial 2D, even by
construction, from its exact half D. (The parity that DOES matter is L's, for the push's rounding, D3.)

## D2. The run back is exact, given (H) the clock row's own dial stands (the cut)

Forward: N = 2 D_in v + 4 q_F + s = 2 D_out q + s1, v = a - b.
Mirror the result: (a, a+, -1 - s1). The act on it: v' = a - a+ = -q; the pivot is a, so q_F' = q_F and
D_in' = L(a+) + L(a) = D_out. N' = 2 D_out (-q) + 4 q_F - 1 - s1 = -(2 D_out q + s1) + 4 q_F - 1 = -N + 4 q_F - 1
= -(2 D_in v + s) - 1.
The split of N' at the OUT dial of the backward round, 2 D_out' = 2 (L(a) + L(a + q1')), where q1' is the
provisional quotient of N' at 2 D_in' = 2 D_out. The run back needs D_out' = D_in, i.e. L(a + q1') = L(b): the
00 row's provisional step must be its actual backward step. For the 00 row itself, under (H), D_in = D_out =
2 L_rest, so its provisional split IS its final split, q1' = -v_00, a_00 + q1' = b_00, and every row reads L(b)
exactly. Then by D1 the split of -1 - (2 D_in v + s) at 2 D_in is (-v, -1 - s) because s is in [-D_in, D_in - 1]
by the promise: a'+ = a - v = b, s1' = -1 - s. Mirrored back: (a, b, s). The drive: J(a) + T_d - 1 - r_d1
= q_d T_d + (T_d - 1 - r_d), the same q_d, and the remainder flips back. QED.
Without (H) the step's exactness is not derived: the provisional split differs from the final one wherever the
00 row's own D_in differs from its D_out (its own law, OPEN). So "the run back exact" is DERIVED under the cut and
MEASURED only on lays that keep it; the derivers' 40 of 40 stands on (H).

## D3. The push's one-carry rounding is odd iff L is odd

half_up(F, L) = floor((2F + L) / (2L)). Put x = (2F + L)/(2L); then (-2F + L)/(2L) = 1 - x, and
floor(x) + floor(1 - x) = 0 unless x is an integer, where it is 1. x is an integer iff 2F = L (2k - 1), which needs
L even and F = L/2 mod L. So half_up(-F) = -half_up(F) for every F iff L is odd; at an even L it fails exactly at
the ties F = L/2 mod L. Line 100: "A rule that holds at one parity only is not a rule of the law." The derivers'
cure is the odd rounding (iv): odd(F, L) = sign(F) half_up(|F|, L), which needs the sign of F (a state quantity),
i.e. a sign test in the Node-clock every round: ROOT.md's round_odd is 5 carries (2 half-ups, 2 for the sign, 1 to
combine). A 3-carry form: q_dn = -half_up(-F, L), q_up = half_up(F, L), pos(F) = 1 + floor(F / (F^2 + 1)) (1 for
F >= 0, 0 for F < 0): odd = q_dn + (q_up - q_dn) pos(F). No one-carry odd rounding exists at an even L: one carry
is floor((cF + e)/(2L)) for whole c, e, and the floor of an affine map is odd under F -> -F only where the map never
lands on an integer at a tie, which at even L it does for every e (D3 above with the shift e). L's parity: L_rest =
6 k Gamma is even, so L = L_rest + c00 has c00's parity, which varies by site and round.

## D4. P_(t+1) - P_t = 4 q_F is an identity

P_t := 2 D_in v + s and N = P_t + 4 q_F = 2 D_out q + s1 = P_(t+1) (since D_in of round t+1 is D_out and v+ = q).
So "books per gear 0 misses" tests the code, not the physics: it is the definition of N. MEASURED as a tautology.
The non-trivial book is the sum over a row's sites: SUM P_(t+1) - SUM P_t = 4 SUM q_F. On a uniform standing clock
with the pull alone, SUM F = 0 exactly (each Mesh pushes its two ends oppositely), so the built act and the edge keep
SUM P to the bit (their push enters unrounded). The root dial adds 4 SUM odd(F_i / L), which is 0 only if the
rounding errors cancel: it does not in general (F = (3, -1, -1, -1), L = 2: 2 - 1 - 1 - 1 = -1). So an exact
conservation of the board (the row's total momentum on a uniform standing clock) is lost; measured on the board in
probe_rd3_board.py.

## D5. The 24

A turn is a signed permutation of rows times a site map. L (the 00 row) is fixed by every turn (kinds.square's
first row). F turns covariantly (the pull with uniform grips, the plan from the tables). odd() is odd. By D1 the
split is covariant with -1 - s on flipped rows. The drive: -J + T_d - 1 - r_d = -q_d T_d + (T_d - 1 - r_d1): the
quotient negates, the remainder flips. So the 24 hold at every round, DERIVED given the engine's covariance,
MEASURED 24 of 24. Half-up in place of odd() breaks at the ties of an even L (D3): their 3 of 24 from round 3.

## D6. L at or below 0

The root dial's state admits a negative L with a positive W = L^2: a negative lapse, which the W dial cannot
represent. D_in = L(b) + L(a) = 0 (L(b) = -L(a)) is a dial 0: Rule3 has no carry there (ZeroDivisionError in the
act; no if to stop it). D_in < 0 breaks the carry's contract 0 <= r' < d. The promise (compares) stands outside
the Node-clock, as for the edge, but the domain is c00 > -L_rest = -sqrt(rest), not c > -rest: the 00 slot's unit
has changed (D7).

## D7. The 00 slot's unit

The law's W = rest + c with c in teeth. The root dial: W = (L_rest + c00)^2 = rest + 2 L_rest c00 + c00^2, so the
law's c = 2 L_rest c00 + c00^2: one count of the 00 slot is 2 L_rest + 1 teeth (about 6 x 10^11 at the calibre),
while the ii slots stay linear in the grips (den Gamma^2 + c_ii). The metric's ten rows no longer share a unit:
00 in root counts, ii in teeth. Under the frame reading (ONE_ALGEBRA) kk = l_k^2 too, so the consistent form is the
frame train (4 gears, the ten slots read), OPEN by ONE_ALGEBRA's own word.
