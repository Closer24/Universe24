# REPORT: a horizon on the returning board (H-Horizon-On-The-Returning-Board-1, sb1, 2026-10-26, 16:0x to 17:1x UTC)

**Verdict: works with the sentence.** One seed of the law does return and freeze. The cycle lay on the 4-cube at the quanta 2,500,000 (the amplitude 212,133, the universe file unchanged) carries the whole board of 64 Nodes past the frozen content 3,793 at once at the interval 3 (the content 3,885, X 5,218,578,156 against the mark's 4,268,834,097, the spread 0), the swap's own trigger releases every frozen Node at the interval 4 and that release is the board's top (64 turns at once), and the board's volume vector stands at its first interval's state again at the interval 5. On that one record the engine's own reader names **"14 the horizon": "SHOWN as silence (no credit at a frozen Node)"** at the interval 3 and **"1b the board tops, every Node turning at once": "SHOWN"** at the interval 4, 26 of the 74 rows SHOWN. Two clauses of the letter keep it from being the recurring bang: gate 1 reads the return against Gamma and not against the seed's own first state, so it reads "NOT SHOWN" on the record that returns (bug 1); and after the return the births fall at 8 of 64 Nodes by the exclusion's own refusal, the likeness ends, and the state's integers leave the 128-bit width (141 bits at the interval 10, 815 at 40: bug 4). The side is not a lever at all: the 8-cube's amplitude, content max and top interval are the 4-cube's Node for Node; the quanta are the one lever, the top's content rising as (Gamma div 4) ln n. The laws checked with numbers: the conserved form (11 of 12 in full on the quanta-5 record, EX-S1's identity 410 of 410), the run back exact (20 of 20 on every one of twelve records, the decisive one among them), the one-Link reach (no act changed), the cube's 48 (not reachable for the cycle lay: no 3-cube image), the fixed count (90 integers per Node), integers only (the decoder's "floats used": 0 on every record), one act on every row alike, the click's exact take. **The one unmet: the 128 bits, past the frozen content.**

The derivation, the predictions written before every run, the measures and the sentence SB-S1: `DERIVATION.md` beside this file. The worlds: `worlds/`. The scripts: `algebra.py` (the frozen mark and the volume reading through the engine's own readers), `measure.py` (the record's frozen Nodes, tops, bottoms, state hash, births, credits, run back), `spread.py` (the board's spread in thousandths of the mean and the births per interval), `period.py` (the volume vector hashed at every interval, the period search).

## The commands (P the venv's python, W the worktree, F this folder, K the kit; PYTHONPATH=$W/src, TMPDIR=/dev/shm/tmp, every run under nice -n 19, the records under /dev/shm/tmp/sb1)

```
nice -n 19 $P $F/algebra.py 1000
nice -n 19 $P -m event_universe.run $F/worlds/w4_q5.json /dev/shm/tmp/sb1/r_q5.json back 20
nice -n 19 $P -m event_universe.run $F/worlds/w4_q5_500.json /dev/shm/tmp/sb1/r_q5_500.json back 20
nice -n 19 $P -m event_universe.run $F/worlds/w4_q10_500.json /dev/shm/tmp/sb1/r_q10.json back 20
nice -n 19 $P -m event_universe.run $F/worlds/w4_q20_500.json /dev/shm/tmp/sb1/r_q20.json back 20
nice -n 19 $P -m event_universe.run $F/worlds/w4_q50_500.json /dev/shm/tmp/sb1/r_q50_500.json back 20
nice -n 19 $P -m event_universe.run $F/worlds/w4_q500.json /dev/shm/tmp/sb1/r_q500.json back 20
nice -n 19 $P -m event_universe.run $F/worlds/w4_q5_hole.json /dev/shm/tmp/sb1/r_q5_hole.json back 20
nice -n 19 $P -m event_universe.run $F/worlds/w8_q5.json /dev/shm/tmp/sb1/r_w8.json back 20
nice -n 19 $P -m event_universe.run $F/worlds/w4_q5000_500.json /dev/shm/tmp/sb1/r_q5000.json back 20
nice -n 19 $P -m event_universe.run $F/worlds/w4_q500000_400.json /dev/shm/tmp/sb1/r_q500k.json back 20   # stopped at the interval 166, the width
nice -n 19 $P -m event_universe.run $F/worlds/w4_q2500000_40.json /dev/shm/tmp/sb1/r_q25m.json back 20    # the decisive record
nice -n 19 $P -m event_universe.run $F/worlds/w5_q5.json /dev/shm/tmp/sb1/r_w5.json back 5   # refused by name
nice -n 19 $P -m event_universe.run $F/worlds/w6_q5.json /dev/shm/tmp/sb1/r_w6.json back 5   # refused by name
nice -n 19 $P -m event_universe.run $F/worlds/w7_q5.json /dev/shm/tmp/sb1/r_w7.json back 5   # refused by name
nice -n 19 $P -m event_universe.run $W/tests/worlds/world_nature.json /dev/shm/tmp/sb1/r_chiral60.json back 20
nice -n 19 $P $F/measure.py <record.json>...
nice -n 19 $P $F/spread.py <record.json>...
nice -n 19 $P $F/period.py <record.json>...
nice -n 19 $P -m event_universe.gates <record.json>          # the engine's own gate reader, one line per row
nice -n 19 $P $K/conservation_check.py /dev/shm/tmp/sb1/r_q5.json out /dev/shm/tmp/sb1/cons_q5.json
```

The kit's `clicks_48.py` was not run: the cycle lay is refused on a cube whose extent is not a multiple of 4, so the candidate has no 3-cube image (named in DERIVATION.md section 5). The kit's `wait_load.py` was not needed: the longest run of the round was under two minutes and the box's 1-minute load stayed near half of one.

## The numbers in one table

| world | amplitude | content max | X max (interval) | top | the state back at its first pair | frozen | gate 14 | gate 1b |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| the 4-cube, quanta 5, 500 | 300 | 1,003 | 55,474 (500) | 111 | 219 | 0 | not reached | SHOWN |
| the 4-cube, quanta 10, 500 | 425 | 1,277 | 167,715 (406) | none | none | 0 | not reached | not shown |
| the 4-cube, quanta 20, 500 | 600 | 1,488 | 410,540 (475) | none | none | 0 | not reached | not shown |
| the 4-cube, quanta 50, 500 | 949 | 1,502 | 408,428 (500) | none | none | 0 | not reached | not shown |
| the 4-cube, quanta 500, 230 | 3,000 | 1,873 | 1,806,608 (230) | none | none | 0 | not reached | not shown |
| the 4-cube, quanta 5, a hole, 500 | 300 | 1,274 | 169,855 (431) | none | none | 0 | not reached | not shown |
| the 8-cube, quanta 5, 140 | 300 | 777 | 22,585 (110) | 111 | the mirror pairs | 0 | not reached | SHOWN |
| the 5-cube, 6-cube, 7-cube | - | - | - | - | - | - | refused by name | refused by name |
| the 4-cube, quanta 5,000, 500 | 9,487 | 2,926 | 122,795,260 (500) | none | none | 0 | not reached | not shown |
| the 4-cube, quanta 500,000, stopped at 166 | 94,868 | 7,597 | - | 16 | none | some | reached | shown |
| **the 4-cube, quanta 2,500,000, 40** | **212,133** | **7,597** | **5,218,578,156 at the interval 3 (alike)** | **4** | **5** | **64 of 64 at 3** | **SHOWN** | **SHOWN** |
| the chiral seed, the 5-cube, 60 | - | - | 27,598 (60) | none | none | 0 | not reached | not shown |

## What was cut short

One run was stopped by name: the 4-cube at the quanta 500,000 to 400 intervals (`/dev/shm/tmp/sb1/run_q500k.txt`), stopped at the interval 166 because the state's integers had reached 64,102 bits and the writer's own clock had passed 10 seconds per mark; its marks are read in DERIVATION.md section 3.9 and no record file was written for it. Not run for want of the box: the conservation check in full and the clicks' readings on the decisive record (its run back is 20 of 20); the quanta between 500,000 and 2,500,000 that brackets the top at the mark exactly; the chiral period search past 60. No chain of this hand is still running; every other record named above is written and measured.
