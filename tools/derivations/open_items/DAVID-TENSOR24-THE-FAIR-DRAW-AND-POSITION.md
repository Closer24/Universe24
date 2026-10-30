# The fair draw on the dial, and Born's rule for position

David, 2026-10-29, for stage 9's split click: the plan's law 9 (the draw) and its item 6 (the draw's fairness, OPEN), with M2's figures, and Born for position, single quanta and Bell's late choice (open steps 5 and 6 of 6488233005, the owner's word of 04:1x UTC: "close every open step"). The probes p1 to p4 sit in derive/david_open/born/, exact integers, each with its .txt. The act read is stage 7a's at tensor24-review 298bec5d8; the integers are the example universe's (den 15,162,856,759,112,389, Gamma 1,000, G 16, T = 6 den Gamma^2 G^2).

## 1. The rule

- **The number:** d = (c + V) mod L, one carry, where:
  - c is the Node-clock's beat count, its own dial, one step at every due beat;
  - V is the sum, over the Node-clock and its six neighbours, of its A1 rows' fine teeth, each read in units of its row's pitch g (the digit r div g). The pitch is the gcd of the row's W and its push's coefficients (s grip and s D), read once at load;
  - L is the parts' sizes' total.
- **The part:** the rank count of d among the cumulative sizes S_i = sigma_1 + ... + sigma_i, part = SUM_i nonneg(d - S_i). There is no sort and no if.
- **On a hand's twins against a detector:**
  - sigma_up = N(<phi, psi>) = (rho rho_d + S . m) / 2, exactly on Gaussian integers (Fierz's identity);
  - L = rho rho_d;
  - down = (2 d - S . m + L) div (2 L), one carry.
- **Law 9 unchanged:** "one number, from the digits that do not change under the 24, modulo M". V is the 24's invariant sum of the board's digits, c is the clock's own count, and M is the sizes' total.

## 2. Why it is fair, exactly (p1)

1. **Over a full turn of the dial,** any L consecutive beats, d takes each value of [0, L) once, so part i is drawn exactly sigma_i times.
   - Checked in 2,880 of 2,880 cases: L from 1 to 120, from 1 to 6 parts, parts of size 0 among them.
   - The same holds over a full turn of any one of the seven digits with the dial held, since a sum is a bijection of each of its terms.
2. **The twins:** Fierz's identity is exact in 400 of 400 random pairs of Gaussian spinors. Up is drawn exactly sigma_up times over the full turn in 400 of 400, so ups / L equals cos^2(theta / 2) exactly.
3. **The 24:** V is a sum over the seven Node-clocks as a set, which no turn changes, and c is the Node-clock's own. The rank count compares d with the sizes, never the digits with one another, so no sort enters.
4. **The run back:** the draw writes nothing. It is a reading of the state at its beat, and the click's record carries the part. On 7a's act the draws read on the way back equal the way out's at every beat and every Node-clock (p2, 120 beats).

## 3. Why the head's draw was not fair (p1, p4)

1. **The sort is no bijection of any digit.** The head's vernier sorts the digits and composes them by Horner modulo M. Over every combination of its digits, on equal parts, where a fair draw gives 1/2:

   | digits | P(up) |
   | --- | --- |
   | 2 of base 2 | 3/4 |
   | 3 of base 2 | 7/8 |
   | 4 of base 2 | 15/16 |
   | 3 of base 3 | 20/27 |
   | 7 of base 2 | 127/128 |

   The 7/8 and 15/16 are the plan's M2 figures, 0.875 and 0.9375, exactly. The sum modulo L over the same digits gives 1/2 in every row.
2. **The frame:** the own digit framed o + |r - o| on the whole base puts 16 of 17 values in the upper half.
3. **On a pair that clicks as one,** the sorted draw gives S = -13/4, past Tsirelson's bound. B's marginal also reads A's axis: P(B+) is 1/4 at (a, b') and 7/8 at (a', b'), so the click would signal. That is the plan's warning on item (l) ("with the sorted vernier's 7/8 it would signal"), in numbers.

## 4. The pitch: the digits must be read in its units (p2)

- **The fine teeth stand on cosets.** On 7a's act the time gear's fine tooth moves only by multiples of its pitch, 256,000,000 = 2^14 5^6, and light's by T / 3, six values.
- **Read raw, the sum is frozen** modulo every L made of those factors:
  - at L = 2, two Node-clocks one Mesh apart always draw alike, and one Node-clock alternates;
  - at L = 1,000 and 16,384, every draw falls in the first half, from a start with every fine tooth at its home.
- **Read in pitch units, every L reads flat and apart.** The numbers below come from a (6, 6, 6) board, 400 beats, read from beat 50, with every fine tooth laid at its home (all alike at the start). The start laid at random reads the same.

  | L | chi-square of the tenths, on 9 | one Mesh apart, in one half | two beats in a row, in one half |
  | --- | --- | --- | --- |
  | 2 | (halves only) | 37,516 of 75,600 | 37,668 of 75,600 |
  | 10 | 12.8 | 37,792 | 37,733 |
  | 97 | 11.4 | 37,840 | 37,638 |
  | 1,000 | 8.0 | 37,962 | 37,698 |
  | 4,060 | 2.8 | 37,798 | 37,856 |
  | 16,384 | 3.1 | 37,966 | 37,779 |
  | 1,048,583 | 6.8 | 37,776 | 37,741 |

  Every correlation lies within 0.01 of 0, and L = 3 gives its own 2/3 in the first half and 5/9 alike.
- **The head's vernier read the pitch too** (fine div F); it was the sort and the frame that skewed it.

## 5. Born's rule for position, carried along the Meshes (p3)

- **The click of a spread hand is a tournament of two-part split clicks,** each at one Mesh:
  - the two parts' sizes meet at the Mesh;
  - the draw at the Mesh's Node-clock picks a side by the sizes;
  - the winner keeps the whole winding of both;
  - the loser's wind travels to it, one Mesh per tick.

  Each Node-clock reads its own dial and its neighbours alone.
- **Exact:** P(x) = rho(x) / SUM rho at every Node-clock, since the product of the sides' odds telescopes.
  - The hand: psi = (3, 1), (2, -2), (0, 1), (1, 4), (-2, 0), (5, 1), (1, 1), (0, -3) on 8 Node-clocks, rho = 10, 8, 1, 17, 4, 26, 2, 9.
  - P = 10/77, 8/77, 1/77, 17/77, 4/77, 26/77, 2/77 and 9/77, exactly, both for a tree by position and for the larger-neighbour matching, a schedule the 24 leave alike.
- **Its time:** the losers' wind travels at most 11 Meshes on the ring of 8. The click is final once the closure has crossed the hand.
- **On 7a's act:** 2,947 quanta, each round of merges read at a later beat by the merging Node-clocks' own dials, land at 383, 309, 29, 628, 154, 989, 95 and 360, against Born's 382.7, 306.2, 38.3, 650.6, 153.1, 995.1, 76.5 and 344.5. The chi-square is 8.3 on 7.

## 6. One quantum at two detectors (p3)

- **The split gives the whole winding to one detector.** Over the full turn P(A) = P(B) = 1/2 and both 0, so g2 = 0 exactly: Grangier's anticorrelation.
- **Two quanta, each with its own full turn:** g2 = 1/2, the 1 - 1/n of n = 2.
- **On 7a's act,** 2,950 single quanta: A 1,437, B 1,513, both 0.

## 7. Bell's late choice (p4)

- **The detectors:** a = (1, 0), a' = (1, 1), b = (5, 2), b' = (5, -2), with the axes z, x, (20, 0, 21) / 29 and (-20, 0, 21) / 29.
- **The pair clicking as one** (the plan's item (l)), the axes read at the click:
  - E(a, b) = E(a, b') = -21/29, E(a', b) = -20/29, E(a', b') = 20/29;
  - S = -82/29 = -2.82759, the plan's value;
  - every marginal is 1/2 at every setting, so no side reads the other's axis.
- **The pair carried along the Meshes** (the local Bell click's closure), the partner's axis chosen late:
  - a partner that clicks after the closure lands gives S = -82/29;
  - one that clicks before it lands, outside the closure's cone, gives S = 0.
- **On 7a's act,** 3,950 pairs, with the settings drawn at the click by a third Node-clock's dial: S = -2.8589, spread 0.0445, against -2.8276.
- **Tsirelson:** over every CHSH of exact integer cosines from real spinors with parts from -6 to 6, the largest |S| is 478/169 = 2.828402, below 2 sqrt 2 = 2.828427. Exact integer cosines approach the bound and never pass it, so the head's -3.018 was the draw's.

## 8. For the Boss, at stage 9

1. **The split click's draw:** d = (c + V) mod L with the rank count, in place of the sorted vernier. The plan's "law 9's sorted draw as a rank count" (section 11, item 11) keeps its rank count, applied to d among the sizes rather than to the digits.
2. **The load** reads each A1 row's pitch once: the gcd of its W and its push's coefficients at the vacuum.
3. **The test** (stage 9's "the draw's distribution"):
   - each part drawn exactly sigma_i times over L beats;
   - flat tenths and halves apart on the act's own digits, at L that share the pitch's factors (2, 1,000, 16,384);
   - the pair's marginals 1/2 at every setting.
4. **Born for position** as the tournament of two-part splits, with the losers' wind moving along the Meshes.

## 9. What stays open

1. **Two draws are apart only as far as the board's digits are.** Each draw's full turn is exact; the independence of two draws is measured (|corr| at most 0.01 here), not proved.
2. **Off the vacuum,** 7b's W and W+ part, so a row's pitch moves. Read at the vacuum's pitch the digit is still a reading, with nothing written, but its coset is no longer fixed. That is for 7b's act to measure.
3. **Bell at a distance, with a late choice outside the closure's cone,** needs item (l), which is the owner's. The fair draw removes its one named obstacle, the signal; its cost (a shared state held by no Node-clock, and a global order of clicks) stands as the plan names it.
4. **The tournament's schedule must be the 24's alike, bit for bit,** at stage 9. The larger-neighbour matching is, but two neighbours of equal sizes need the digits to break their tie.
5. **The turnover:** the draw is not asked to read alike under T. If the plan asks it, each digit folds exactly at its own half, min(r, w - 1 - r), which keeps the full turn's exactness at the half base.
