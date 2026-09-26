# The fraction-free law: every count an accumulator on the reader's record (read-only, the mathematician, 2026-09-20)

> Section 1's claim that the constant-rate counts are bit-identical on the
> register is corrected by records 147 and 148 of 2026-09-20 and
> [BEAM_LAW note 41](../../BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation): on the register no paid
> lamp and no crowd on a fan runs at a constant rate (a lamp pays at every
> birth, a crowd changes at every interval), so every lamp world and every
> crowd world moves under the accumulator, which is the law's count (the
> physics-rule reviewer's [REVIEW_COUNTS.md](REVIEW_COUNTS.md)). The rest
> of this design stands as written.

On the Boss's question after the signed drive landed (PR #377, `by_drive`
in `core/integer.py`: `drive += rate`, a count of +-1 when the drive
reaches +-denominator, that much subtracted, the remainder kept; record
130 on G = 2^12): the model owner's "what about a rule without
fractions?". The law's counts today are whole parts off a clock,
`by_clock(age, n, d) = floor((age + 1) n / d) - floor(age n / d)`, no
remainder kept anywhere (BEAM_LAW note 17): the clock's owed count, a
free family's release, a lamp's rate, the turn, the push per column at
the reader's clock age, the doppler grain flux's weight on the flow
(GRAIN.md), the step rule until the drive replaced it. The primitive
proposed: one accumulator per count on the record, `acc += numerator`
each self-creation, one unit each time `acc` crosses the denominator,
`acc -= denominator`, the remainder owned in `acc`, bounded below the
denominator, local. Every integer below is from `accumulator_map.py`
beside this file (`accumulator_map.out`). No src change, no run.

## 1. Bit-identical under the accumulator: every count at a constant rate from age 0

**Theorem.** With a constant numerator n and denominator d from age 0,
the accumulator after k self-creations is `acc = k n - count x d` with
`0 <= acc < d` (the invariant of the subtraction), so `count = floor(k n /
d)` exactly and the count gained at the k-th self-creation is `floor(k n /
d) - floor((k - 1) n / d) = by_clock(k - 1, n, d)`; the accumulator holds
`(k n) mod d`, the remainder `by_clock` recomputes from the age every
time. Checked on seven rates from 1 / 3 to a star's 9.7 x 10^12 / 2.9 x
10^14 over 20 000 self-creations: identical, and `acc = (k n) mod d`
(`accumulator_map.out` 1). So these counts are **bit-identical**, every
registered world byte for byte: the clock's owed count (`by_clock(age, k
n, d)` with k the count read: constant only while the crowd is constant,
see section 2), a free family's release (`content x n / d`, constant while
the content is), a lamp's `rate`, the turn (`content / K`), the age
against a key (`ages_at_key`: a lifetime, a `become` at `at`), the drive
at constant momentum (already so, note 38's test (a)).

**The exact condition when they differ.** (i) A start at a nonzero age
with an empty accumulator: `by_clock(a0 + k, n, d)` reads the phase of
the clock at `a0`, the accumulator started at 0 does not; the per-step
difference is in {-1, 0, +1} and sums to 0 over a period; they are
identical iff the accumulator is initialised to `(a0 n) mod d`
(`accumulator_map.out` 2: for a0 = 1, 7, 30 at 32 / 55). So a declared
`in_transit`-like start (a body declared at an age, a world resumed from
`state.json`) must carry the accumulator, or the phase of every count at
that age; `state.json` carrying `acc` per count is the exact form (as
`drive` is carried). (ii) A changed rate: `by_clock` at the current rate
reads `floor(age n' / d) - floor((age - 1) n' / d)`, the whole part of a
history that never happened (the stall and burst of RULES.md section 1),
the accumulator the whole part of the sum of the rates: equal only while
the rate is constant from the start; the drive is this case for the step,
and the same holds for the owed count when the crowd changes, for the
release when the content changes (a click joined it), for the turn when
the content changes. Every registered world whose bodies change content
(the cavity worlds, every world with paid clicks on a body with a rate)
would move in those counts too, by the same kind of difference: at most
1 per interval, exact in the sum.

## 2. Counts that change per interval and are exact over a period: the push

The push per column is `by_clock(age_A, |V_t E n|, D d)` with `V_t` the
interval's flow, a numerator that changes every interval. Per interval
both forms give `floor(X_t / D)` or one more, so they differ by **at most
1 label unit per column per axis per interval** (`accumulator_map.out` 3:
the largest difference 1 over 5000 intervals). Over a period the
accumulator's sum is `floor(sum_t X_t / D)` **exactly**, the remainder
below D in the accumulator; `by_clock`'s sum is a drift with no owner: the
remainder discarded each interval is up to `D d - 1`, and the sum of the
discarded parts does not average to zero when the numerator varies (the
map: +38.7 label units off the exact 12 239.3 over 5000 intervals on a
uniform sequence; a constant numerator is exact, a varying one has no
bound of its own). The same for the doppler grain flux's weight on the
flow (the flow times a per-direction factor, a varying numerator) and for
the owed count under a varying crowd. **Which registered worlds move:**
every pushed body, again (the coupling `1b` probes, the orbit series D,
Bohr's H, the planet, series G and G2, I and J's contacts: the same list
the drive re-registered, the second time today), by at most 1 unit per
column per axis per interval, with the sum over a period exact; fixed
probes (series C's `read` records) move too where their numerator varies
(the arriving flow of a fan varies by the age), by the same bound; the
Bell, slit, lamp and detector worlds do not (no column push).

## 3. The commutativity claim: true as an identity, and what it buys

`acc += a; acc += b` is `acc += a + b` exactly (the integers' addition is
associative and the subtraction of the denominator commutes with the
order of the additions: the count and the remainder after all the
additions depend on their sum alone). Checked on 290 directions summed
one by one, shuffled, and all at once (`accumulator_map.out` 4: equal
counts and equal remainders in every trial). Two consequences, one of
them the one the claim names:

- **The per-direction floors' loss is gone.** Today's per-direction
  floors (doppler-v1 per (direction, column); GRAIN.md's flow weight per
  direction) sum to less than the floor of the sum by up to (directions
  - 1) units per interval per column (the map: 136 to 148 units short of
  the exact count on 290 directions), which is why note 38 needed the rule
  "per-direction floors only on an axis where the reader moves" to keep
  bit-identity at rest on a fan; with one accumulator per (body, column,
  axis) taking every direction's numerator, the count is the count of the
  sum, exact, and that rule is unnecessary.
- **Covariance under the 48.** A signed axis permutation g permutes the
  directions and the axes with signs; today's floors are already
  invariant under it, because a permutation of the terms of a sum of
  floors is the same sum, and `floor(|x|)` is sign-blind: the per-direction
  floors do not break the 48-covariance, they break the equality with the
  per-column floor. So the accumulator does not restore a covariance the
  floors lost; it restores the equality of the split with the whole, and
  keeps the covariance (the accumulator's count is a function of the sum
  of the permuted terms). **What still breaks covariance**, and the
  accumulator does not touch: the collision table's tie (the sorted order
  of a class, that is Port order, section 4 of BEAM_LAW: not
  O_h-equivariant by the mathematician's 2.4); the apportioning tie
  (`apportion_whole` over the declared direction order and `age mod n`);
  the Bresenham tie of a fan direction (the axis furthest behind first,
  ties by axis order); the frame's number order at the contact (G1); the
  sets' and the arms' order at the ladder (record 105's S2, the second
  party rounded); the tables' entries themselves (C, S of the circle and
  the half-angle tables are exact under the 48 because the circle is not
  on the GameBoard; `u_d` and `T_d` are exact under the 48, `u_{gD} = g
  u_D`). A parity test of a hand world (hand/FORM.md) reads through none
  of these when the world is on headings.

## 4. The accumulators' cost

One bounded integer per (body, count) on the record, each below its
denominator (so below 2^62 by the label bound), nothing at a Node:

| Count | Accumulators per body | Denominator |
| --- | --- | --- |
| the push per column | 3 per column (one per axis): 6 with gravity and charge, 9 with the strong column, at most 24 (COLUMN_LIMIT 8) | `D_c d_c` |
| the doppler flow weight | 3 (one per axis, the weighted flow's floor) | `G Q |D|^2` per direction: one accumulator per axis takes every direction's numerator scaled to a common denominator, or the weight is folded into the column's accumulator (the product's denominator `G Q |D|^2 D_c d_c`, tested by division) |
| the step (the drive) | 3 | `Q S M + |p_a|` (as built) |
| the owed count | 1 | `d` of `suspension` |
| the release per family held | 1 per family the body releases (the same count on every direction of a fan) | `d` of `release` |
| a lamp's rate | 1 | `d` of `rate` |
| the turn | 1 (the phase is the turn's own accumulator mod N already; the sub-step remainder is the new integer) | `K` |
| the age against a key | 0 (a comparison, no rate) | |

On the register's worlds: the deuteron (two bodies, three columns, a
release each): 2 x (9 + 3 + 1 + 1 + 1) = 30 integers; the G2 stars (25
bodies, gravity and charge, a lamp, a release, the drive): 25 x (6 + 3 +
1 + 1 + 1 + 1) = 325; Bohr (two bodies): about 30. In `state.json` and
`run.json` as `drive` is carried today (`acc` per count by name); a
declared accumulator in a world file refused (the start is 0, or the
phase of the age for a declared age, section 1 (i)). The host's work is
one addition and one comparison per count per interval, the same as
`by_clock`'s two multiplications and two divisions or fewer.

## 5. The ladder at the click

The rungs `b_k = (2 N C_k + T) // (2 T)` are one division per record at
one place, the click; there is no sequence of intervals to accumulate
over, and an accumulator across records at one set would be a memory at
the detector, which the owner refused (#359 step B). Two facts decide it:
(i) the rung is not needed as a number: the cell of u is the first k with
`2 T u + T <= 2 N C_k` (from `u < b_k` with `b_k` the floor: `u + 1 <=
(2 N C_k + T) / (2 T)`), a comparison of two products, **no division, no
rounding, the same integers as today**; so the click is fraction-free
already in that form, and the record's `rungs` line is a report; (ii) u
is not an accumulator's state: it is the birth phase, the clock's count
at the birth mod N, an accumulator of the emitter's turn already (the
phase register is the turn's accumulator mod N). My view: leave the
ladder as it is, written as the comparison of products in the note (a
spelling, not a change of an integer), and say that the click's rounding
is the nearest-integer rung, declared, once per record.

## 6. Recommendation

**Do it, as one unification, after today's four merges land**, for four
reasons: (i) it is the drive's rule made the rule of every count, one
primitive (`by_drive` with a signed or unsigned rate) in place of two
(`by_clock` and `by_drive`), which is the owner's "one mechanism";
(ii) the discarded remainder of note 17 becomes an owned one, which is
what the local integer operation contract asks ("a rule that permits
division with remainder must declare the existing bounded remainder
owner"), on the reader's own record, local, one bounded integer per
count; (iii) the sums become exact over any period and the per-direction
split exact at every interval, so the doppler rule loses its special
case and every future rule that splits a count over directions or
families (colour, matter as a record) gets exactness for free; (iv) the
constant-rate counts are bit-identical, so the re-registration is the
pushed worlds only, once more, in one batch with dated lines, which is
cheaper now than after the next rule that splits a count. Under a new
implementation note of `beam-v1` (no new identity: an integer form of the
same counts, the constant-rate ones unchanged), with the tests: (a) the
identity at a constant rate on every count over 10^4 self-creations;
(b) the sum over a period equal to the floor of the sum of the
numerators on a varying flow; (c) the accumulator carried in `state.json`
and a resumed run identical to the unbroken one; (d) the per-direction
split equal to the whole on a fan at rest (bit-identical to the
unweighted push at p = 0); (e) the bound of every accumulator below its
denominator at every tick; (f) the click's cell by the comparison of
products equal to the rungs' cell on every keyed world. What it does not
give: the ties of section 3 stay ties; the click's rounding stays a
declared rounding; the counts that already ran at a constant rate do not
change, so the physics of series C, E, K, J is untouched and only the
moving-body and varying-flow readings move, by at most one unit per
column per axis per interval.

## 7. The five lines

1. Constant-rate counts (the owed count, the release, the lamp, the turn,
   the age against a key, the drive) are bit-identical to `by_clock` from
   age 0 (proved and checked); they differ only from a nonzero start age
   with an empty accumulator (initialise it to `a0 n mod d`) or when the
   rate changes (then the accumulator is the exact whole part of the sum,
   `by_clock` the stall and burst).
2. The push per column and the doppler weight differ by at most 1 unit per
   column per axis per interval and are exact in the sum over any period
   under the accumulator (`by_clock`'s sum drifts, +38.7 over 5000 on a
   uniform test); every pushed body's world moves again, by that bound.
3. `acc += a; acc += b = acc += a + b` exactly: the per-direction split
   equals the whole (the floors' loss of up to directions - 1 units per
   interval is gone, note 38's special rule unnecessary); the 48-covariance
   was not broken by the floors and is kept; the ties that break it stay:
   the collision table's Port order, the apportioning and Bresenham ties,
   the contact's number order, the sets' and arms' order at the ladder.
4. Cost: one bounded integer per (body, count) on the record, 30 on the
   deuteron world, 325 on the G2 stars, in `state.json` and `run.json`,
   nothing at a Node.
5. The ladder: leave it, spelled as the comparison `2 T u + T <= 2 N C_k`
   (no division, the same integers); u is already the turn's accumulator
   mod N. Recommendation: one unification after the four merges, a new
   note under `beam-v1`, the pushed worlds re-registered once in one
   batch.

> The scripts of this folder (`accumulator_map.py`, `fan_sphere_map.py`, `two_slits_map.py`, `wheel_map.py`) were deleted on 2026-09-26 (the model owner's word, record 2229: code not in use goes); git history keeps them at `6d2a92e2` (`git checkout 6d2a92e2 -- docs/designs/fraction_free/<script>`).
