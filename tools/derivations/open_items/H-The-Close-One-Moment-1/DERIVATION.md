# H-The-Close-One-Moment-1 (cm1): the close reads one moment (the engine head 3067fd522)

Verdict line: the close's one moment HOLDS for every reading the close LOGS and is REFUSED for the two
readings the close ACTS on. Measured: the credit's sense, the credit's frame and the take's per-end
momentum brought to the interval's start leave the board bit for bit (the hole 60 and the chiral 60:
nodes equal, births 17 and 17, taken and booked to the digit, credits 2,288 and 2,903, turns 539 and
612, every refusal by name equal, the run back 20 of 20), changing three logged fields and nothing
else; the share's fall and the exact count at a take brought to the start make the hole 60 RUN AWAY
past the law's width (max bits 112 at the interval 15, 116 at 20, 742 at 25, 10,465 at 30, against a
head of 17 births over 60 intervals and 112 bits throughout), so that half of the candidate is refused
by the width law. The two ends of a Link COMMUTE under the one moment, measured, and do not on the
head: the prize of (b) is won. The prize of (a) is REFUSED as free and priced: the frame's second
moment is not a doubling of the close's read but the PRE-SWAP level, equal to the now slot at every
unturned credit (2,147 of 2,288; 2,573 of 2,903) and apart at every turned one (141 of 141; 330 of
330), so the array leaves only at the price of the decoder's solve at 141 of 2,288 and 330 of 2,903
credits. Laws checked: the flag empty bit for bit 2 of 2 worlds; the run back 20 of 20 on both records;
the exact take (taken and booked to the digit, unchanged); the charge law (the births equal line for
line); the count of integers 99 and 112 bits; integers only (0 floats in the scripts); the one-Link
reach untouched. The one unmet: the width under the take's own read at the start, and the kit's
conservation check in full, which the box did not reach.

## 0. The unification above the item (the brief's unification block, step 0)

The item IS the unification: the close's one moment (CL-S1 of The-Merger-Premise_COMPARISON.md
section 3). By the four roads: (1) the algebra holds ONE bilinear, F_ij = SUM over a row's lines of
(now_i before_j - before_i now_j), read as the current, the twist, the charge and the credit's sense at
four different moments; (2) the matrix: the Link's record read once per Link per record; (3) the cube:
the start state is the one the 48 images carry, the live state is not (the swap stands in it); (4)
Rule3: one step, and the close after it. The generic problem above the item, found on the way and named
first by the priority of 07:10 UTC: **the close has FIVE moments, not two, because the SWAP (interval
act 4) stands between the step and the close**, and the engine's own name for the fourth moment
("stepped") is the pre-swap level. The four roads do not reach it; the measure does.

## 1. The algebra (one page): the four moments by file and line, and what is written when each is read

The interval's five acts (interval.py:285, `run`): (1) the readings, (2) the kick, (3) the division
(Rule3's step), (4) the swap at the top, (5) the close. So at the close, the step AND the swap have
written, and the close's own lays and takes write as it goes.

**Moment 1, the interval's start** (the state the previous close left; nothing of this interval
written): close.py:304 `node.read_lines(held, plane_starts, ...)` (the rows' rules); close.py:308
`owns` = gram.share of plane_starts[rec] (the standing share), read by close.py:116 (`refuse`);
close.py:74-76 in `meet`, the Link's current `den row_current(start, ...)`, the twist
`row_twist(start, axis)` and the two ends' charges `gram.charge(row.shape, start)`; bodies.py:31, the
body's net current `row_current(plane_starts[rec0], port)` summed over the six Ports; bodies.py:97-110,
the frame's `re_start_now`, `re_start_before`, the neighbours, the phases, the frames, the odd lines
and the factors. `plane_starts` is built at interval.py:231 from `self.rows[k]`, the row as the
interval began.

**Moment 2, the live board** (the step's write, then the swap's exchange at the turned Nodes, then
every write this close has already made): merger.py:130 `levels_at(row, where)` (the levels a merger
takes whole); merger.py:99-107 `share_fall` with merger.py:58-87 `share_at` (the share the board loses);
take.py:39-65 `fall_of` through merger.py:134 (the taken line's choice k = argmax(now^2 - before^2), the
count s and the fall); merger.py:154-156 and :178 `write_ends` (the momentum each end books);
merger.py:27-28 `child_at` (the lay's momentum); merger.py:260 and :269 `light_children` (the levels
that stood and the children's senses); close.py:192 and :195 `child_laid` (the same for a birth).

**Moment 3, the credit's sense**: bodies.py:147, `gram.charge(row.shape, row.lines)[at]` - the live
board again, after the close's own writes, so a third moment in the order of the acts even where it is
the second in the state.

**Moment 4, the frame's stepped levels**: bodies.py:89 `sre, sim = node.stepped[rec]`, logged at
bodies.py:95-96 as `re_stepped` and `im_stepped`, built at interval.py:232-233 (one `line.copy()` per
record per interval), declared at interval.py:67 and node.py:102, read by decoder.py:240 as `zx`, the
step's own output a_next in the species solve.

**What changes when each is brought to the start, by the algebra.**
- The frame's levels (moment 4 to moment 1): the array holds the level AFTER the division and BEFORE
  the swap. At an unturned Node the swap writes nothing, so the stepped level IS the now slot of the
  live line at the credit (the credited record's own lines are never written by the close at a credited
  Node: bodies.py:59 skips `born_nodes` and the frozen, and the body's own take writes the emitter row
  at bodies.py:76). At a TURNED Node the swap has exchanged the levels, so the stepped level is
  readable NOWHERE else: the change is not NONE, it is the whole of the swap. **Prediction: equal at
  every unturned credit, apart at every turned one.**
- The credit's sense (moment 3 to moment 1): W = re_now im_before - im_now re_before is a different
  integer at the start, and its SIGN can differ. **Prediction: a different integer at a minority of the
  credits; no change on the board, the sense being logged alone (read by predicates.py:51-52 for the
  gates).**
- The take's own momentum (merger.py:154-156): momentum_of reads the NEIGHBOUR levels of the line. The
  two ends of a merger are neighbours on one Link, so the first end's write changes the second end's
  read: the per-end booking depends on the naming and the sum does not. At the start the neighbour
  levels are untouched by any write of the close. **Prediction: order-free per end, measured.**
- The take's own count and fall (TC-S1's division at take.py:58-65, EX-S1's remainder at
  merger.py:177): the line chosen k, the count s and the fall f(s) are all functions of (now, before)
  at the Node. At the start these are other integers, so the take pays a different count of levels,
  and the exact take's identity (taken + remainder before - remainder after = booked) still holds by
  construction while the BOARD changes. **Prediction: a different integer at essentially every take,
  the three records parting at their first take, and the gate 15 inequality and the width at risk,
  since the take no longer removes what the board actually holds.**

The predictions as written before any run stand in out/PREDICTIONS.txt (P1 to P9). P1 is REFUTED by the
measure (the swap), P2, P4, P5, P6, P7 and P8's count are confirmed, P3 is confirmed and worse than
predicted (a runaway, not a parting), P9 is confirmed for the take's reading and refuted for the
logged readings (which part in no count at all).

## 2. The flag

The kit's maker, one copy, every mend under the names ONE_MOMENT (the three logged readings) and
TAKE_AT_START (the take's own read), the nine replacements in repl_cm1.json over close.py, merger.py
and bodies.py (the one line of close.py:299 stashing `plane_starts` on the Node for the take act to
read, the rest the moment of a read alone; the second flag ENDS_REVERSED names a merger's two ends in
the reverse order, for the test of (b)). No act of the engine changed, no number in a src line, no
name, ASCII only.

    $P $K/make_flagged_copy.py cm1 ONE_MOMENT $D/repl_cm1.json src $W/src \
       worlds $W/tests/worlds/world_hole.json,$W/tests/worlds/world_nature.json python $P

**The flag empty, bit for bit with the head, 2 of 2 worlds**: the hole 60
c7060288e55c497b24f74111e1fd559df2434d7874cfc783fa48fece371f3c1f and the chiral 60
4e5b63f9ac2f2fa7cc686ad902a42bd5ce567854c81618a3a6fff46ae6496374 (the same two hashes the premise and
the click pairs report). The copy: /dev/shm/tmp/cm1/src_cm1. After the check the one line of
merger.takes was put under the second name TAKE_AT_START, which cannot change the path with both names
empty (the same branch is taken), and the control run `empty_hole` confirms it: equal to the head's
record in every count and every Node line.

## 3. The measure

Commands: `export PYTHONPATH=/dev/shm/tmp/cm1/src_cm1 TMPDIR=/dev/shm/tmp`, every run `nice -n 19`,
one at a time, the chain /dev/shm/tmp/cm1/chain2.py (its log /dev/shm/tmp/cm1/chain2.log), the readings
by `cm1_read.py part|ends|frame <record.json> ...` (no import of the engine: the records' own logs).

**(i) The three logged readings at the start (ONE_MOMENT), against the head.**

| record | nodes | births | taken | booked | credits | turns | refusals by name | run back | first parting |
|---|---|---|---|---|---|---|---|---|---|
| hole 60 | equal | 17 = 17 | 91,524,260,120,888,090,397,359 both | 89,041,969,164,090,056,764,412 both | 2,288 = 2,288 | 539 = 539 | stop 9,146, lay 497, orientation 248, twist 229, sense 9,274, all equal | 20 of 20 | i 10, a credit's `frame` |
| chiral 60 | equal | 17 = 17 | 70,769,943,529,221,060,875,807 both | 69,862,070,318,996,095,731,587 both | 2,903 = 2,903 | 612 = 612 | stop 9,371, lay 683, orientation 110, twist 42, sense 10,393, all equal | 20 of 20 | i 5, a credit's `frame` |
| bodies 120 | equal | 0 = 0 | 0 both | 0 both | 1,337 = 1,337 | 1,795 = 1,795 | stop 256, lay 112, orientation 1,183, twist 5,636, sense 3,024, all equal | 20 of 20 | i 9, a credit's `frame` |

The log's length is the same to the line (21,699, 23,519 and 11,550) and `met` is the same (19,300,
20,497 and 9,955). The bodies 120 (the kit's world_bodies_120.json, two packets on the 7-cube) has no
birth and no merger, so its only parting is the frame's two fields at 118 of 1,337 credits, its
credit's sense apart at 0 of 1,337 (no credited Node of it changes sign under the start read).
**The record's own fields that change, and nothing else: three.** The credit's `sense` at **425 of
2,288**, **443 of 2,903** and **0 of 1,337** credits; the frame's `re_stepped` and `im_stepped` at **141 of 2,288**,
**330 of 2,903** and **118 of 1,337**; and the merger birth's per-end `dP_take` with its sum, at its one birth of the chiral
60. No field of any birth, any refusal or any Node line moves.

**(ii) The frame's second moment, read on the HEAD's own records (cm1_read.py frame).**

| record | credits | plane frames | stepped equals now | apart | apart and turned | equal and turned |
|---|---|---|---|---|---|---|
| hole 60 | 2,288 | 2,288 | 2,147 | 141 | **141 of 141** | **0 of 2,147** |
| chiral 60 | 2,903 | 2,903 | 2,573 | 330 | **330 of 330** | **0 of 2,573** |

The two moments are ONE at every unturned credit and TWO at every turned one, exactly. The field named
`stepped` is the pre-swap level, and at a turned Node it is the only record of it. (The start level
equals the stepped level at 2 of 141 and 0 of 330 of the apart credits, so the start is no substitute.)

**(iii) The ends of a Link (the prize of (b)): the chiral 60's one merger birth, i 11, node [3,0,2],
the ends [3,0,1] (minus) and [3,0,2] (plus), the same taken (4,231,679,883,420,625,324,531) and booked
(4,030,822,135,692,823,649,270) in every run.**

| path | naming | per-end dP_take | sum |
|---|---|---|---|
| head | minus first | [3,0,1]: [4,773,843,982,646,141,250, 693,215,243,618,028,750, -5,604,718,990,954,275,000]; [3,0,2]: [7,433,627,293,265,670,000, 3,716,813,646,632,835,000, 0] | [12,207,471,275,911,811,250, 4,410,028,890,250,863,750, -5,604,718,990,954,275,000] |
| head | plus first | [3,0,2]: [..., -9,292,034,116,582,087,500]; [3,0,1]: [..., +3,687,315,125,627,812,500] | the same sum |
| flag | minus first | [3,0,1]: [2,384,463,781,239,318,750, 614,552,520,937,968,750, -33,008,845,004,620,177,500]; [3,0,2]: [0, 0, 24,513,270,955,173,697,500] | [2,384,463,781,239,318,750, 614,552,520,937,968,750, -8,495,574,049,446,480,000] |
| flag | plus first | **the same two triples, end for end** | the same sum |

**On the head: per end APART, sum EQUAL (1 merger of 1). Under the one moment: per end EQUAL, sum
EQUAL (1 merger of 1).** The attribution becomes order-free: the prize of (b) is measured and won, and
it belongs in the sentence. The SUM itself moves (the third axis -5,604,718,990,954,275,000 on the head
to -8,495,574,049,446,480,000 under the flag), because the start read is a different integer: the
lattice momentum law (the births' dP_take + dP_lay_ends summing to 0) therefore wants the LAY's read
(merger.py:27-28, close.py:192) moved to the start in the same sentence, which this box did not measure.

**(iv) The take's own read at the start (TAKE_AT_START) on the hole 60: the width breaks.**

| interval | 1 | 5 | 10 | 15 | 20 | 25 | 30 |
|---|---|---|---|---|---|---|---|
| births | 0 | 0 | 36 | 147 | 362 | 617 | 693 |
| body clicks | 0 | 0 | 16 | 203 | 368 | 582 | 908 |
| refused | 0 | 41 | 326 | 2,162 | 4,882 | 7,667 | 9,870 |
| max bits | 112 | 112 | 112 | 112 | **116** | **742** | **10,465** |
| volume mean | 1,001 | 1,028 | 1,126 | 1,944 | 54,480,628 | a 200-digit integer | larger |
| milliseconds | 87 | 235 | 517 | 1,660 | 4,495 | 6,774 | 9,273 |

The head's hole 60 has 17 births and 2,288 credits over the whole 60 intervals and stays at 112 bits.
**So the take's own fall and count read at the interval's start break the law "every integer within 128
bits" by the interval 25, and the record is no record.** By the brief's rule (5) a mend that breaks a
law is refused whatever it buys: this half of CL-S1 is refused, and the reason is in the algebra - the
take must remove what the board HOLDS, and what the board holds at the take is the live level; a take
sized on a level the board no longer has leaves the difference behind at every click, which is a source.
(The marks: /dev/shm/tmp/cm1/diag.out, the run aborted at the interval 45 by the box's clock.)

## 4. The 48 under the flag

Not run (named as not run): the box's time went to (iv)'s diagnosis. The prediction stands and is
unmeasured: the three logged readings do not part the board, so the kit's clicks_48 on the chiral
seed's 3-cube image at 60 must read the head's own 3 EQUAL and 45 APART, with the credits' `sense` and
`frame` fields the only parting; the command is
`ONE_MOMENT=1 $P $K/clicks_48.py $W/tests/worlds/world_nature.json 60 <out.json> cube 3`.

## 5. The laws

- The run back exact: **20 of 20** on the hole 60 and the chiral 60 under ONE_MOMENT (the head's 20 of
  20 kept); the undo reads the log's own `taken_now_was` and `taken_levels`, which the flag does not
  move.
- The exact take: `taken` and `booked` equal to the digit on both records (EX-S1 untouched; no take's
  count or remainder moves under ONE_MOMENT).
- The charge law: the births are equal line for line on both records, so the children's W sum to 0 at
  the same count as the head.
- The count of integers per Node and the width: 99 integers, 112 bits, both records, the reader's own
  row, unchanged. Under TAKE_AT_START the width breaks (section 3 (iv)): REFUSED.
- Integers only: no float in cm1_read.py or in any replacement (grepped).
- The one-Link reach: no replacement reaches beyond the Node and its Link; `node.at_start` is the
  record's own start lines, read at the same Node as the live lines were.
- The kit's conservation check in full with every law named: **NOT RUN** (the box ended). The one law
  the head itself misses on the chiral 60 (gate 15's pre-EX-S1 inequality) is unmeasured under the flag.

## 6. The sentence

> **CL-S2 (the close's one moment, bounded by the width; CL-S1 of the comparison of 15:4x UTC refined,
> MG-S1, SL-S1, CR-S1, CR-S2, TC-S1, EX-S1, MK-S2 and CA-S1 kept by name).** Every reading of a record
> that the close LOGS is read at the record's levels at the interval's start, the state the previous
> close left: the sense a credit carries, the levels a credit's frame shows, and the momentum a take
> books at each of its ends, so that the two ends of one Link commute and the per-Node attribution does
> not depend on the order the meeting named them. The two readings the close ACTS on, the share's fall
> and the exact count at a take, are read on the board the take writes and not at the start, because a
> take sized on a level the board no longer holds leaves that difference at every click and breaks the
> law's width (the hole 60 at 742 bits by the interval 25 against 112 throughout on the head). The
> frame's stepped level is no second moment of the close but the one record of the state the swap
> replaced, kept by name and read at the turned Nodes alone (141 of 2,288 and 330 of 2,903 credits).

The courses it changes, with their numbers: on the hole 60 and the chiral 60 nothing of the board (the
tables of section 3 (i)); the credit's `sense` at 425 of 2,288 and 443 of 2,903 credits, which
predicates.py:51-52 reads, so the gate rows that ride on the sense move with it (not measured through
the gates module: named); the merger's per-end `dP_take` and its sum at the chiral's one birth; the
frame's two fields at 141 and 330 credits.

**The prize of (a): REFUSED as free, priced.** The lines the one moment would take out of the engine,
with their files: interval.py:67 (the list declared), interval.py:232 (the `line.copy()` per record per
interval), interval.py:233 (`node.stepped = self.stepped`), node.py:102 (the Node's own declaration),
bodies.py:89 (the read), bodies.py:95 and :96 (the two logged fields) - **seven lines out** - and
decoder.py:240 changed to the now slot - **one line changed**. The record's own fields that lose: the
two, `re_stepped` and `im_stepped`, as the brief expects, and nothing else. But the array is NOT a
doubling: at 141 of 2,288 and 330 of 2,903 credits (every turned Node, 6 and 11 percent) its value is
the pre-swap level, which no other field of the close carries, and the decoder's species solve reads it
as a_next. **The array leaves at the price of the decoder's solve at those credits** (the decoder
already logs `turned` and can drop them), or it stays and is renamed for what it is.

**The prize of (b): WON and measured** (section 3 (iii)), and it is in the sentence above.

## 7. Bugs, by file and line

- **merger.py:154-156 (`write_ends`): the per-end momentum is read on the live board, so the two ends
  of one Link do not commute** - measured on the chiral 60's one merger (i 11, node [3,0,2]): the
  third-axis bookings -5,604,718,990,954,275,000 and 0 under one naming against
  -9,292,034,116,582,087,500 and +3,687,315,125,627,812,500 under the other, the sum the same integer
  both ways. The start read mends it (equal end for end under both namings). The same read stands at
  merger.py:178 for the gap-0 end and at merger.py:27-28 and close.py:192 for the lay.
- **bodies.py:89 with :95-96 and decoder.py:240: the field named `stepped` is the PRE-SWAP level.** It
  differs from the now slot at every turned Node and at no other (141 of 141 and 330 of 330 apart; 0 of
  2,147 and 0 of 2,573 of the unturned), and the decoder's solve uses it as the step's output a_next at
  a Node where the swap replaced a_next. Either the name or the read is wrong.
- **bodies.py:147: the credit's sense is read after the close's own writes**; 425 of 2,288 and 443 of
  2,903 credits carry a different sign from the start read, and predicates.py:51-52 reads that sense
  for the gates.
- **take.py:60-62: the shortfall iteration can stall.** `s = s - quotient(-(walls * weight - s *
  (price - x * w * s)), slope)` advances by 0 when the exact numerator vanishes while the floored
  `fall(s)` is still below `walls`, and the `while` then never ends. Not reached on the head; named as
  a latent stall under any other read of the levels.
- **run.py (the world's loading): a world file copied to another folder with its `intervals` changed
  fails with code 1**, the `universe` key being resolved against the world file's own folder; the kit's
  own worlds carry their universe beside them and work. (This cost this hand the short TAKE_AT_START
  record: /dev/shm/tmp/cm1/head_hole12.log and take_hole12.log.)
- interval.py:231-233 with close.py:263 and :299: the close is handed `plane_starts` and writes on the
  swapped board, so the close's reads and its writes stand on two boards; the swap, not the step, is
  what parts them at a turned Node. This is the generic problem above the item (section 0).

## 8. What was cut short, by name, with the paths

- **The kit's conservation check in full on one record under the flag** (12 laws, every law named): not
  run. The command: `$P $K/conservation_check.py /dev/shm/tmp/cm1/one_hole.json out <summary.json>`.
- The bodies 120 landed inside the box and is measured above; the chain is finished and nothing of this
  hand is still running.
- **The 48 under the flag** (section 4) and **the gates' rows through the engine's own gates module**:
  not run.
- **The TAKE_AT_START record's first parting interval and its log**: the 12-interval world failed to
  load (section 7); the runaway is read from the marks of the aborted 60-interval run,
  /dev/shm/tmp/cm1/diag.out.
- **The lay's momentum read** (merger.py:27-28, close.py:192) under the one moment, which the changed
  momentum sum of section 3 (iii) asks for: derived as wanted, not measured.

## 9. The ledger row

item | derived | one-Node test | toy (records, numbers) | gates touched | Universe | spec | missing by name
---|---|---|---|---|---|---|---
the close's one moment (CL-S2) | four moments by file and line, and a fifth found: the swap stands between the step and the close | the frame's two moments read off the head's own log at 2,288 and 2,903 credits, apart at the turned Nodes alone | hole 60 and chiral 60 under ONE_MOMENT: the board bit for bit, three logged fields apart (sense 425 and 443, frame 141 and 330, the merger's per-end dP); under TAKE_AT_START the hole 60 past 128 bits by i 25 | the credit's sense through predicates.py:51-52 (named, not read through the gates module); gate 24's merger untouched | the records' length 60; the width breaks under the take's read at 742 bits by i 25 | CL-S2 above; seven lines out (interval.py:67, :232, :233, node.py:102, bodies.py:89, :95, :96) and one changed (decoder.py:240), at the price of the decoder's solve at the turned credits | the conservation check in full; the bodies 120; the 48; the gates' rows; the lay's momentum at the start
