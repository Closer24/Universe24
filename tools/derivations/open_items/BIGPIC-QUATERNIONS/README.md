# The one algebra in whole numbers: the quaternions as the board's gears

Big Pic, 2026-10-30. These are the local checks behind my posts on #2187: 6526641319, 6526805415, 6526947202, 6527540022,
6528097443, 6528150081 and 6528217535. They are pushed at the Boss's ask (6527072352 item 2), for his quaternion deriver
and his families reader.

**Status:** local checks (Solution24's step 8), not DERIVED. Nothing here is law or code.

**Rules kept:**
- Every division is Rule3's carry (`tensor24.algebra.carry.carry`).
- No probe holds a float, a root, a circular call, a random draw or a fraction.
- Test cases come from a whole-number stream (`qlib.Stream`, a linear congruential map).

Run one: `python3 tools/derivations/open_items/BIGPIC-QUATERNIONS/p1_ring.py`. Each output is the `.txt` beside it. All
twelve run in about half a minute.

## The probes

| Probe | What it checks | Backs |
|---|---|---|
| `qlib.py` | The shared pieces, all whole: Hamilton's product; the 48 gears, as (u, s) and as y = 2q over Z[root 2]; the turns; Bareiss's determinant; the eight-part order's basis (Hermite form, determinant 16). | all |
| `p1_ring.py` | The 48 gears give the 24 turns, two gears to a turn. Hurwitz's 24 units give the 12 even turns, and the root-2 gears the 12 odd ones. The hand turns by twice the gear's angle. Which gear makes which turn. A quarter turn's gear to the 4th power is -1 and to the 8th is 1. A2 is the Galois sign (a character). The Spokes are permuted. The mirror is the bar, and the turns with their mirrors are the cube's 48. | 6526641319, 6527540022 item 2 |
| `p2_product.py` | The vertex's two tables are one product. The norm multiplies (four squares). The click's two readings: conj(before) x now is unmoved by the board (three inner charges), and now x conj(before) turns with it (the spin). The books split exactly. The six turns are the 4-d area. With no carry, the free step keeps the wind and all six turns. | 6527540022 items 2 and 3.1; 6528097443 item 2 |
| `p3_trains.py` | The units' own train of 24 gears is a signed permutation for every gear, with -1 as -I, holding 2 E1/2 + 2 E5/2 + 4 G3/2. Of the 30 subgroups holding -1, only {+-1} and the four sixfold C6 carry a sign character sending -1 to -1. Their trains are 24 gears (all three half-speed kinds) and 8 gears (G3/2 alone). Without -1, only orders 1 and 3 occur. So spin 1/2 rides no signed-permutation train of fewer than 24 gears. | 6528097443 item 3 D |
| `p4_wall.py` | The centred per-gear carry commutes only with signed permutations (exhaustive on two gears, dials 3 and 5). A unit other than 1 fixes a non-zero class mod W exactly when W shares a factor with 6: Hurwitz at W 1 to 13, the eight-part order at W 1 to 5. Ties of the nearest lift at W 5 and 7. | 6527540022 item 4 |
| `p5_square.py` | The half-speed hand's square is isotropic, with \|re\| = \|im\| = \|psi\|^2. Its re x im is the root's spin times its size. psi and -psi give one square. The pair hand is read from the squares. Every gear turns the square by one whole signed permutation of determinant 1. | 6527540022 item 5.2 |
| `p6_time.py` | The beat has determinant 1, and its powers' traces follow 2 cos(n w). The time mirror is the swap: S M S = M^-1. On the act, the hand rides its ellipse inside the window and runs away outside it. | 6528097443 item 2.5 |
| `p7_e8.py` | The eight-part whole hand under Q = 2 (N0 + N1): its Gram matrix is whole, even, of determinant 1 and positive, so it is E8. | 6528097443 item 2.6 |
| `p8_euclid.py` | Hurwitz's division, N(r) <= N(b)/2, with one compare. The covering radii on the grid of eighths: part by part 64/64 (the four-fold tie), with the halves 32/64, half-D4 16/64. The octahedral order: its double deep holes sit at exactly 1/2, and no nearby point met exceeds it. | 6526805415; 6527540022 item 4.1 |
| `p9_act.py` | Free two-part and four-part hands on the act with the carry, window means of 12,000 rounds over 240,000. The two-part turn holds to under one grain, its wind wanders up to 10, and the four-part turns wander up to 27. | 6527540022 item 3.2 |
| `p10_cells.py` | The half-open carry's mirror. The draw's run back: the mirrored pointer against the parts read from the other end picks the same part (8,790 cases). An odd increment's tooth is kept on the run back, not flipped. A beat with a whole sine: W = a^2 + b^2 and k = 4 b^2. | 6528150081; 6528217535 |
| `p11_hand_per_quantum.py` | The owner's word (18:4x UTC): "Try a hand per quantum." Each quantum has its own hand, moved by the one act, and the record weighs a pair of clicks by the determinant (half-speed) or the permanent (whole-speed) of the two hands at the two clicked places. One mode twice: every pair weight 0, on the lay and after 300 rounds (the exclusion). One hand per family cannot exclude: the sum 2 psi gives a weight that is not 0. Two orthogonal modes of one spin: 0 at one place (the exchange hole), not 0 in all (the triplet and the Fermi sea fill). Up and down in one mode: not 0, together at one place. A third quantum in one orbital: 0, with a control that is not. The permanent at one place is twice the told-apart weight (bunching) where the determinant is 0. The family's one hand moved equals the sum of its quanta's hands moved, to the teeth (18 counts in 729,829,905). | the owner's word of 18:4x UTC |
| `p12_time_density.py` | The Boss's ask (6531004963 item 3): does the time gear's own law have a whole form with no root? Part A, the deriver's law D_in^2 + D_out^2 = 8 W^2 + 4 push + s - s+: the out edge's states (D, s), s in [-D, D), counted by the fine value D^2 + s, tile the whole numbers one to one; the law is a reflection of the fine value, a bijection whose run back is the mirror (189,504 cases); D_out read from its fine value is one carry by 4 W and one compare while it moves less than twice the root of W from 2 W (measured at W = 10,000: 200); with no push it keeps W v^2 (998 permille as W triples). Part B, the books road on a ring of 64: the 00 row by d_t^2 A = -d_x^2 G at a fixed dial with no beat of its own, the grips' row and the matter row by the edge act at the dial it produced first: the run back exact over 300 rounds, the 00 row dividing nothing, the dial's total standing, a uniform rest standing at every rest tried, a bump in the dial alone standing (no wave of its own), the dial moving only inside the grips' reach, a matter lay equal to the grips' lay moving equal to it (one cone), and a raised dial delaying a matter packet (125 against 139 rounds). | the Boss's 6531004963 item 3 |

## Numbers that differ from the posts by the stream

- **p10 item 3:** flipped by (iii), the tooth comes back 913 of 20,000 times. My 6528217535 quoted 866 of 20,000 from a scratch run on another stream. Both are chance.
- **p8 item 3:** the largest least norm met near the double deep holes is 37,470,473 / 84,934,656 (0.441). My 6526805415's scratch stream met 112 / 256 (0.4375). Both are below 1/2.

## Two corrections these probes carry

- **6526947202 item 3, "the spin":** wrong. conj(before) x now holds three inner charges, and the spin is the other order (p2 item 3).
- **6526947202 item 3, "no drift":** too strong. It holds for the two-part turn alone (p9).
