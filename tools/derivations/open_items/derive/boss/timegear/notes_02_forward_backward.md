# Notes 02: time forward and backward on the 00 row (after the owner's word of 18:1x, "no price")

The obstacle: a dial moved by its own quotient has no lawful split. Three leads from the Boss, weighed one by one.

## Lead 1 and lead 3: the 00 row's own two slots read symmetrically in time; the read and the produced state together

Take the dials as the edge has them, the read state's edge in and the produced state's edge out, both the symmetric read
of their two ends: D_in = W(b) + W(a), D_out = W(a) + W(a+). The round's split is N = C(q) + s+ with s+ in
[-D_out, D_out - 1]; the centre C(q) is free. Two demands:

 (T) the cells tile the integers at fixed D_in: C(q + 1) - C(q) = D_out(q) + D_out(q + 1);
 (R) the run back is the same act: C(q) - 2 q D_out(q) = C(-v) - 2 (-v) D_out(-v) (notes_01), i.e. with
     e(q, D_in) := C(q) - 2 q D_out(q) and D_in = D_out(-v): e(q, D_out(-v)) = e(-v, D_out(q)).

(R) says g(x, y) := e(x, D_out(y)) is symmetric, g(q, -v) = g(-v, q). (T) at fixed v says g(q + 1, -v) - g(q, -v)
= -(2 q + 1), so g(q, y) = -q^2 + k(y), and symmetry makes k(y) = -y^2 + c. Hence, uniquely,

   C(q) = 2 q D_out(q) - q^2 - v^2 + c,  and the round's law (c = 0) is

   D_in^2 + D_out^2 = 8 W(a)^2 + 4 push + s - s+ .

It is symmetric under the swap (D_in, s) <-> (D_out, -1 - s+): the two edges enter squared and summed, as term 11's
click runs back only with X(S) + X(S+). Its act: M = 8 W(a)^2 - D_in^2 + s + 4 push (sums and products), then
D_out = the u with u (u - 1) <= M < u (u + 1) and s+ = M - u^2 (the cells [u(u - 1), u(u + 1) - 1] tile the
non-negative integers), W(a+) = u - W(a). The quotient of this split is a ROOT: u is the integer nearest sqrt(M).
With the carried estimate c = 4 W(a) - D_in and R = 4 push - 2 v^2 + s: u = c + k, k the cell of R among
[k (2 c + k - 1) - c, k (2 c + k + 1) + c - 1]; k = 0 is the carried dial. The two forms differ by the k^2 in the
cells' ends, which is what no carry does (a carry's cells have one length).

Its physics: 4 W (q - v) + q^2 + v^2 = 4 push + s - s+, i.e. W dv/dt + v^2 / 2 = F with dW/dt = v: exactly
sqrt(W) d_t (sqrt(W) d_t a) = F, nature's form for the 00 row's own motion (the physicist's), at the edge dial, W linear
in the count (no law change), the push entering whole (no floor), no register, no cut. Free: sqrt(W) v kept.

So leads 1 and 3 give one form, and it is nature's; its one carry is an integer root, which decision 41 forbids.

## Lead 2: backward gears beside the forward ones (the twin)

The 00 row as two half-gears A and B, each the other's time-reverse in role. The round: A steps reading B's two slots
as its two dials, (D_in, D_out) = (2 W(b_B), 2 W(a_B)); then B steps reading A's new two slots, (2 W(a_A), 2 W(a_A+)).
The mirror swaps A and B, swaps slots and takes s -> -1 - s. Proof of the run back (one gear pair):
 A's split: N_A = 4 W(b_B) v_A + 4 P_A + s_A = 4 W(a_B) q_A + s_A+ ; B's: N_B = 4 W(a_A) v_B + 4 P_B + s_B =
 4 W(a_A+) q_B + s_B+ . Mirror and swap: A' = (a_B+, a_B, -1 - s_B+), B' = (a_A+, a_A, -1 - s_A+). A' steps first
 with (2 W(b_B'), 2 W(a_B')) = (2 W(a_A+), 2 W(a_A)): N = -4 W(a_A+) q_B + 4 P_B - 1 - s_B+ = -1 - 4 W(a_A) v_B - s_B,
 which splits at 4 W(a_A) into (b_B - a_B, -1 - s_B): A' -> mirror of B's old state. Then B' steps with
 (2 W(a_B), 2 W(b_B)): N = -4 W(a_B) q_A + 4 P_A - 1 - s_A+ = -1 - 4 W(b_B) v_A - s_A, splitting at 4 W(b_B) into
 (b_A - a_A, -1 - s_A): B' -> mirror of A's old state. Un-mirror and un-swap: the old pair.
Every other row X steps between A and B with (D_in, D_out) = (W(b_B) + W(a_A), W(a_B) + W(a_A+)), the one choice of
one slot from each half that (C1) and (C2) allow with X not swapped (the four-slot sum works too, X stepping last);
or every row is twinned and every X_A reads B's 00 slots, every X_B reads A's new ones: the doubled board.
What it is: the two halves are one field sampled at staggered half-rounds, each half the midpoint clock of the other.
No register, no root, no cut, no floor, dials exactly 2 W, one cone, nothing written, the run back the same act. Its
cost: the 00 row's state is doubled (two counts and a tooth more), and the halves' difference A - B is a free field
on light's cone (d_t (W d_t delta) ~ grip Lap delta, sourced by nothing to first order), read by B's dial alone.
The owner's "more gears, with differences between them" names exactly this shape; his decision 34 ("one hand") is
against a doubled Node-clock.

## The register (notes_01), re-read under "no price"

The carried dial D_out = 4 W(a) - D is the k = 0 case of the symmetric form: it is what the symmetric read gives when
the quotient's cell is taken from the carry alone. Its departure E from the edge's dial is the alternating sum of the
clock's second differences; under a fast swing of the clock it is of the order omega^2 A / 2 (bounded, not secular),
a pump of the same kind the owner refused on the edge. With W = L^2 (the root dial) the same involution D -> 4 L(a) - D
keeps L v: nature's physics for the 00 row with no root, one register, the law change and the push at the pivot's root
(the fwdback deriver's matter).

## The theorem for the Boss (no price)

For the 00 row, a one-carry act on the two slots and the tooth has a constant dial (notes_01): the cut, a second cone.
Beyond that the dial must come from one of: (i) the state beyond the two slots, a register whose update is an
involution at the pivot (neutral, so undamped and resonant) or a twin whose counts are the dials (a doubled field);
(ii) a root of the state (the symmetric form, nature's physics, no other cost). Every form that keeps the three
conditions carries one of: a second cone, a register's departure, a doubled field, a root. The run back forbids damping
(an involution contracts nothing), so no form's extra integer settles by itself. Which of these the owner counts as no
price is his: the root is the one his decision 41 names; the doubling is the one his words "more gears, with
differences between them" seem to name.

## Measured (probe_tg9_pump, one course, the 00 gear free and its own clock)

rest 10,000, v0 = 1 count a round, 30,000 rounds (nature: W about 26,600 at the end; W v kept: 26,458; v kept: 40,000):
 - the carried dial: at round 10,000 the momentum P = 2 D v + s meets the half count, the quotient jitters 1, 0, 1, 0
   and the reflected dial grows 2 a round for ever: the departure 0 -> 1 -> 5,001 -> 10,001 -> 20,001 (D 74,999
   against 2 W 57,498 at 27,500). The register is pumped by the clock's own whole-velocity jitter, a Nyquist drive no
   lay can avoid; the physics is lost with it (W 29,999 at the end).
 - the twin: at the same half count A's quotient falls to 0 while B's stays 1; A freezes (W(A) 19,999 for ever) and
   B runs away at v = 1 for ever (W(B) 40,000): the halves part by W itself. The pair's free difference is unstable
   at the frozen hand.
 - the symmetric form: the quotient stays 1 at every round, the tooth drifts -2 a round while the dial grows 2 a round,
   so the quotient never falls: W linear, 40,000 (the act as built's course). The one velocity at which it departs
   from nature is |v| = 1 (at |v| >= 2 the tooth overflows and the quotient falls).
rest 10^6, 30,000 rounds, v0 = 1, 2, 3, 10, 100, -2, -10: the carried dial and the twin keep W v (999, 1002 permille
against W v kept at v0 = 100, -10) and miss nature (612, 839); the symmetric form keeps nature (1000, 1002) and misses
W v kept (1386, 1128); below v0 = 10 the course is too short to tell. The carried departure 14 counts at v0 = 100, the
twin's A - B -139: small here, the half count not met.

## The theorem, sharpened by the measurements

One cone with a carry puts the velocity's weight at the dial, so every carry form at W keeps W v (the edge's physics,
which breathes under a swing: the price the owner refused), and at L (W = L^2, the law change) keeps L v but needs the
register or the twin, each unstable at the frozen hand. Nature's form for the 00 row's own motion is the symmetric
form, D_in^2 + D_out^2 = 8 W(a)^2 + 4 push + s - s+, and its act is an integer root. So: no carry meets one cone, a
bijection, nothing written and no price together; the root does, with the one quirk at |v| = 1.
