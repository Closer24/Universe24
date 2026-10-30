# The close's law: seven findings, each one clock act

David, 2026-10-27, 15:4x UTC, for the Boss (the task of 11:4x UTC), measured on the head 608d97134 (DAVID-CLOSE-LAW_CHECKS.txt; every run's rewind 20 of 20). No src touched. Ranked by what the owner gains.

## 1. The take's fall has the wrong sign (the owner's word: every chart moves)

**The finding.**

- EX-S1 names the fall as the clock's wind falling by what is owed.
- unwind.fall_of computes it in closed form as w (now^2 - moved^2) - t s pull. The wind's own fall is w (now^2 - moved^2) + t s pull, because d wind / d now = 2 w now - pull.
- TC-S1's text carries the wrong sign too: its price reads "2 w now + S before + SUM R_j before_j".

**Measured** (every light take, against the whole board's wind before and after the move):

| chart | takes | claimed / own fall | takes where the wind did not fall |
|---|---|---|---|
| hole | 236 | 10.9 to 1,197 | 34 |
| chiral | 203 | 1.5 to 1,636 | 30 |
| bodies | 986 | 0.27 to 28,295 | 79 |

**The fix:** the take reads the wind's own fall over its window (hands.wind, as the unspringing does), with its count by the one search (rule3.least_at) bounded by the move. The closed form, a formula, goes.

**With the fix:**

| chart | fittings | chimes |
|---|---|---|
| hole | 18 to 0 | 2,262 to 0 |
| chiral | 16 to 3 | 3,003 to 1 |
| bodies | 23 to 0 | 17,944 to 83 |

At these seeds one clock's light holds about one light quantum, and a fitting costs two. **The charts' matter was booked from nothing.**

## 2. The unspringing drops its excess (the owner's word)

**The finding:** the merger books only the child's wall, so the takes' falls above it are carried nowhere, and so are the light's rises above it.

**Measured from the committed logs:**

| chart | unspringings | dropped by the takes | dropped by the light's rises |
|---|---|---|---|
| bodies | 15 | 181.9 walls (up to 24.5 at one end) | 2.19 walls |
| chiral | 1 | 0.11 walls | 0.15 walls |

**The fix:** EX-S1's one remainder carries every excess, signed. This needs the owner's word, because a negative remainder leaves EX-S1's range [0, one notch).

## 3. The vernier reads the mesh beyond (the owner's word)

**The finding:** at the neighbour across spoke p the code reads grips[p]. The law's one-mesh read names R_ji, which is grips[p xor 1].

**Measured:** 385,260 of 732,090 neighbour lattices differ through the hole's 60 ticks.

**With the fix:**

| chart | fittings | chimes |
|---|---|---|
| hole | 18 to 17 | 2,262 to 1,887 |
| chiral | 16 to 17 | |
| bodies | 23 to 19 | 17,944 to 13,812 |

On the bodies, row 8b goes from NOT SHOWN to SHOWN.

## 4. One moment for the take's push, CL-S2 (the owner's word)

**The finding:** the light's take reads the live board, while the sprung take reads the tick's start, the one moment CL-S2 names.

**The fix:** read node.start_gears.

**With the fix:** fittings move 18 to 17 on the hole, 16 to 19 on the chiral and 23 to 22 on the bodies.

## 5. The lay-back leaves the remainder (a fold of the charts)

**The finding:** the lay-back puts the levels back but leaves the take's excess standing.

**Measured:** on pair_3 and plasma_3 (100 ticks), 81 and 135 lay-backs each leave a remainder, up to 3.3 x 10^20.

**The fix:** the whole take at -1 (CR-S1), with the remainder restored. After it, none stands.

**The three charts lay nothing back.**

## 6. Two tie rules for one orbit (a fold at the records' X)

**The finding:** the table stops where the cosine does not fall; the floor stops where it rises.

**Measured at 23 Gamma:** the table's half turn is 1 (20 flat steps among the first 40 counts) and the floor's is 3,161. **At the records' X** both are 3,142.

**The fix:** the floor's one rule.

## 7. The rows' tension range reads every axis gear (a reader's fold)

**The finding:** run.py reads the regulator's gears 1 to 9.

**Measured:** 50 of the hole's 60 rows show another range than the tensions'.

**The fix:** gears[1 : 1 + AXES]. No reading reads the field.

## For the owner's word

1. **Item 1** is the wind's conservation at every take, by EX-S1's letter. It leaves these seeds almost without matter.
2. **Items 2 to 4** are the same kind of book-keeping, smaller, and each moves the charts.
3. **Items 5 to 7 are folds.**
