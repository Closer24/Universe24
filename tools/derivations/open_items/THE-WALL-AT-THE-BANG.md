# The wall at the bang: the width of the remainders, the merger's lcm and the lowest-terms fold (David, 2026-10-26, 22:4x UTC; the Boss's width task of 22:38 UTC, items 1 and 2; measured on the engine head 8363981de, unchanged in src through c6279863c)

The Boss's reading, to confirm or refute (22:38 UTC): on the record of nature's seed (`tools/derivations/open_items/The-One-Record-Of-Nature/worlds/b20_cyc_q12000000_20.json`, 20 intervals) the remainders `line.rem` read 108 to 128 bits from the first interval and drift by six or seven bits between the bang's two cycles (the interval 7 at 121 against 17 at 127, 8 at 121 against 18 at 128) where every other place repeats; node.py carries the division against the wall, so the remainders are bounded by the wall by construction; a merger at the bang's top widens the common denominator by an lcm (predicates.py's `den * d // gcd(den, d)`), so the wall widens and the remainders with it. Item 2 on that reading: the lowest-terms fold, the levels and the wall divided together by the lattice's gcd (`core/rule3.lattice`, gcd(w, D, R_1..R_6) at a Node), an identity of the algebra, with the hard marks that no ratio moves, the three records stay bit for bit on the levels, every verdict stays, and the drift goes.

## 1. The verdict

The lcm reading is refuted and the drift is the physics' own level. The riders' wall is the carrier's level's and nothing else, W = scale (w div 2)(X_before + X_now) exactly at every interval and every Node; no lcm stands anywhere in the engine's path; the bang's top (the interval 11, 8 births, all 8 mergers) does not widen the wall; the six-bit drift at 17 and 18 is X_now, the carrier's level at the second cycle's rise, about 109 times its value at 7 at every one of the 64 Nodes, which the remainders follow by being one bit under W. The lines are in lowest terms already where they move (the gcd of W with every remainder of a row over the board is 1 at the intervals 3 to 7 and 13 to 20), and the fold could not meet the marks: an identity on the representation leaves the levels and so leaves the drift. Nothing built; the numbers are below.

## 2. The wall, interval by interval

`interval.division`: every riding line's one carried division is at the mean wall of the carrier's two levels at its end times the row's scale, W = scale (w div 2)(X_before + X_now), the remainder born at W div 2 (`acts.born`) and kept in [0, W). Measured at every interval and every Node of the 64: W equals that product exactly (every row, every Node, 20 of 20 intervals), every remainder lies in [0, W), and w div 2 reads 84 bits (w = 6 den Gamma^2 G^2, 85 bits; den 54 bits, Gamma 1,000, G 16), so W reads 84 bits plus the bits of X_before + X_now:

| interval | X_now (bits) | X_before + X_now (bits) | W of the riding rows (bits) | the remainders (bits) | the event |
|---|---|---|---|---|---|
| 1 | 26 | 26 | 109 | 108 | |
| 2 | 37 | 37 | 121 | 120 | frozen 64 |
| 3 | 26 | 37 | 121 | 120 | turned 64 |
| 4 | 10 | 26 | 109 | 108 | 8 births |
| 5 | 31 | 31 | 115 | 114 to 115 | |
| 6 | 32 | 33 | 116 | 115 to 116 | |
| 7 | 38 (231,512,260,072) | 38 | 122 | 121 | frozen 64 |
| 8 | 32 | 38 | 122 | 121 | turned 64 |
| 9 | 31 | 33 | 116 | 115 to 116 | |
| 10 | 10 | 31 | 115 | 114 to 115 | |
| 11 | 26 | 26 | 109 | 108 | 8 births, 8 mergers |
| 12 | 37 | 37 | 121 | 120 | frozen 64 |
| 13 | 26 | 37 | 121 | 120 | turned 64 |
| 14 | 10 | 26 | 109 | 108 | |
| 15 | 31 | 31 | 115 | 114 to 115 | |
| 16 | 32 | 33 | 116 | 115 | 2 births, turned 8 |
| 17 | 45 (25,203,451,717,686) | 45 | 128 | 127 | frozen 64 |
| 18 | 32 | 45 | 128 | 127 to 128 | turned 64 |
| 19 | 31 | 33 | 116 | 115 to 116 | |
| 20 | 30 | 31 | 115 | 114 to 115 | turned 16 |

The wall at the bang's top is narrower than before it, not wider: 109 bits at 11 against 115 at 10 and 121 at 12. The walled row (the shape 10, the carrier) keeps its own wall at 85 bits throughout, its write remainders at 112 to 115.

## 3. No lcm in the engine

- `predicates.py:312` (`den = den * d // gcd(den, d)`) is the Reader's Bell row, a reading of the record summing fractions, no act of the engine.
- The one lcm in `src` is `loader/quartet.py:354`, the quartet's den composed with its vector's at the load, once, in no close.
- A merger's child's wall (`merger.walls_of`) is a share summed under the row's rule over the end and its six neighbours, no denominator in it; the mergers at 11 leave W at 109 bits as at 1.

## 4. The drift is the physics' own level

X_now compared Node by Node between the two cycles (the interval i against i - 10):

| i against i - 10 | Nodes where X_now agrees (of 64) | max abs dX | note |
|---|---|---|---|
| 11 against 1 | 64 | 0 | the same, 44,445,633 at the top |
| 12 against 2 | 0 | 11,249,424 | 122,289,546,493 against 122,278,297,069 |
| 13 against 3 | 64 | 0 | |
| 14 against 4 | 64 | 0 | X at Gamma at the bang's bottom, both |
| 15 against 5 | 48 | 1,987,856,655 | whole Nodes, the pattern moved |
| 16 against 6 | 0 | 3,888,014,756 | |
| 17 against 7 | 0 | 25,128,307,762,608 | 25,203,451,717,686 against 231,512,260,072 at the top |
| 18 against 8 | 0 | 3,888,014,756 | |
| 19 against 9 | 48 | 1,987,856,655 | |
| 20 against 10 | 16 | 702,985,534 | 702,986,534 where the first cycle read Gamma |

The first cycle's event at 4 is 8 births and the second's at 11 is 8 mergers, two different events; the riders' levels agree at no pair of intervals ten apart. So the second cycle is not the first, the levels drift, and the remainders' width is theirs.

## 5. The lowest-terms fold, measured before building

- The gcd of W with every remainder of a row over the whole board, per riding row: 1 at the intervals 3 to 7 and 13 to 20 on every riding row (the moving lines are in lowest terms already); W div 2 or a factor of it at 1, 2 and 8 to 12 alone, where the remainders sit at the birth W div 2 on resting lines (at rest the lowest terms are the wall 2 and the remainder 1, and the next interval's gcd is 1 again, nothing to carry).
- Rule3's lattice gcd(w, D, R_1..R_6) at a Node reads 5 to 85 bits of w's 85 by the paces (6 bits at 1, 19 at 2, 31 at 4, 5 to 25 at 5, 12 to 19 at 7, the shape-4 row's 55 to 85), and it is the draw's lattice (`draw.py:26-32`, the draw's digit already divided by it), no wall of the riders' division, which is at W and not at w.
- A gcd taken per Node would give each Node its own wall where the kick's momenta are summed in the one unit W; a gcd over the board is 1 where the lines move.
- So the fold is empty where it could act and could not reach the drift, which is X_now's: the three records would stay bit for bit (nothing divided), every verdict would stay, and the interval 17 would still read X_now at 45 bits against 7's 38.

## Appendix: the scripts

The measurement is `step1.py` and `step1b.py` of the session's scratch (2 s a run): the Node stepped interval by interval; per riding row W compared with scale (w div 2)(X_before + X_now) by array equality, the remainders' range, the gcd of W with every remainder over the board and per Node, the count of remainders at the birth; per record row the rule's lattice gcd(w, D, R_1..R_6) per Node from `readings.rule_of` at the interval's start; X_now kept per interval and compared Node by Node with the interval ten before.
