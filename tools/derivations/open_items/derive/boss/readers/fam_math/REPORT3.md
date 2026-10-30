# The hostile mathematician's third report: FAMILIES3.md against N1 (the G3/2 pair reading needs the whole wedge)

Reader as before, 2026-10-30, for the Boss. Read: FAMILIES3.md whole, NOTES.md's new sections, probe_pauli3.py/.txt,
probe_quaternion.py/.txt, probe_click.py/.txt, the revised probe_induced.py. Rerun into fam_math/rerun/ with the
worktree's .venv/bin/python -I -B: all four byte-identical (probe_pauli3 1m54s, probe_quaternion 12s, probe_click 2s,
probe_induced 1m44s). My checks: p7_third.py/.txt (whole numbers, the carry the one division).

## VERDICT on FAMILIES3, N1: CLOSED (for G3/2, the kind N1 was about), with one new BLOCKING sentence and two MINOR items

**N1 closed, my numbers (p7_third.txt 1-2).** D(phi, chi) = |phi|^2 |chi|^2 - (phi . chi)^2 - (phi . I chi)^2 on G3/2's
eight gears with the kind's forced phase I (+-I the only units of its commutant): D >= 0 and (D = 0) <=> rank(phi,
I phi, chi, I chi) <= 2 on 390,624 of 390,624 chi in [-2, 2]^8 for each of three phi whose one-state hands lie in the
box (24, 24 and 8 of them: D = 0 exactly there, nowhere else); kept by all 48 lifts and by I on either hand;
symmetric in the two hands; D = SUM_(j<k) (phi_j chi_k - phi_k chi_j)^2 - (phi . I chi)^2 (Lagrange: the complex
wedge's squared norm, the whole of Alt^2 = A1 + E + T2 in one invariant number). My chi = (-1, -1, 0, 0, 0, 0, 0, 1)
against phi = (1, 1, 1, 3, 1, 2, -2, -3): D = 56 of 90 = 622 thousandths, epsilon = 0; the 292 chi with epsilon = 0: D > 0
on all 292. probe_pauli3 1 says the same (its "kept by the 48" was checked on 12 lifts and 4 pairs; here all 48 and 20).
So the whole wedge is read by one whole number, D is the one to read, and N1 is met.

## New items

### A. BLOCKING (one sentence, the spin-1/2 extension): "D reads it whole either way" (FAMILIES3 line 89) is false, and the first text's phase (FAMILIES.md lines 102-103, probe_pair 2) and the third text's phase I are different groups.

Measurement (p7_third.txt 3-5), on Lambda's eight gears in the first text's Gaussian basis (1, j) Z[zeta_8], I = right
multiplication by i (probe_pair's mult_i): the ring's determinant (probe_pair 2) and D disagree on the hand's own
declared phase. For the hands 1 = (1, 0, ..., 0) and zeta = (0, 1, 0, ..., 0) (the hand advanced by one eighth of the
first text's "own phase, right multiplication by zeta^k"): det(1, zeta) = 0 over Z[zeta_8] (one state by the ring)
while D(1, zeta) = 1 of 1, a FULL pair by D (<1, zeta>_I = (0, 0)). Twelve random phi against phi zeta: det = 0 on 12 of
12, D in thousandths of the room 884, 980, 983, 980, 844, 994, 518, 998, 604, 253, 934, 977, rank(phi, I phi, chi, I chi)
= 4 on all. The ring's line (phi, phi i, phi zeta, phi zeta i) has rank 4; the I-line rank 2. The reason: on
Lambda x R = H_1 + H_2 (the two real places of Q(sqrt 2)) right-zeta acts as +zeta on the E1/2 half and -zeta on the
E5/2 half (sigma(zeta) = -zeta), so it is a Galois-twisted turn, not a phase of one complex line; only zeta^2 = i is.
Alt^2 over I of E1/2 + E5/2 = 2 A1 + A2 + T2 (the text's "A1 + A1 + A2 + T2", right), the two A1 the two ring
determinants, one per Galois half; D is their joint norm with the cross terms, and vanishes only when both halves are
proportional by ONE scalar. Consequence: a pair click reading D counts phi and phi zeta as a full pair and admits two
keys where the first text's "phase" calls them one state; "two per orbital" is then four per ring line. The texts
must choose one phase group for spin 1/2: U(1)_I alone (the physicist's one charge; then strike "the hand's own
phase is right multiplication by zeta^k" and read zeta^odd as the Galois twist, the E5/2 doubler's sign), or the
ring's scalars (then D is not the reading and "one state" is a four-dimensional line). G3/2 is untouched: no zeta in
its commutant, I forced. Fix: strike "either way" at line 89, correct FAMILIES.md lines 102-103, and say which group.

### B. MINOR. D depends on which right unit is named the phase (p7_third.txt 4).

On the 24-gear train (spin 1/2 with company) the right units keeping D with I = right i are 16 of 48 (the normalizer
of I: those commuting or anticommuting with it), the left 48 (the board's turns) keep it 48 of 48. For G3/2 the phase
is forced (+-I the only units); for spin 1/2 it is a declaration, the table's U(1) as the text says: then say that
"one state" is relative to it, and that a vertex keeping another right unit would name another "one state".

### C. MINOR. The DRAFTED click (probe_click; FAMILIES3 lines 161-185) does not deliver the partner's key to an occupied taker (p7_third.txt 6).

A taker standing on phi's line (A phi turning in I) fed through the dot by a giver on the partner's line J phi takes 1
key in 3,000 rounds (an empty taker fed on one line takes 7, probe_click 1): term 11's transfer (I a_t) . a_g vanishes
between Hermitian-orthogonal hands (J phi, K phi are orthogonal to phi, I phi), so with the dot vertex and term 11's
winding as the key, the partner's key never arrives where a quantum stands; "two per orbital, where the partner's line
is laid by a partner's giver" (lines 179-181, probe_click 3) is the algebra S_-(phi, T phi) = |phi|^4, not a delivered
key. The rule's "standing against the gain since the last key" reads cleanly only on a taker that was empty (an
occupied taker's gain holds its own turning on its line). The text's Open ("term 11's winding click cannot be a matter
family's light click") covers this in other words; the click's part stays DRAFTED, rightly.

## Out of remit, read only

The quaternion section (probe_quaternion: the eight ways of the 48 units against the engine's kinds, 48 of 48 each; the
two tables as one product on 20 of 20; N(conj(b) a) = N(b) N(a) on 20 of 20) and the price of the 24-gear train (the leak
out of spin 1/2 998 thousandths under the train's table) reproduce byte for byte; I did not audit them beyond that.
