# H-The-Bang-That-Births-1 (bb1): the report, the commands and the numbers (2026-10-26, 12:5x to 14:2x UTC, the engine head 338820837)

The derivation, the algebra, the prediction's corrections, the sentence, the bugs and the ledger row
stand in DERIVATION.md beside this file. The prediction, written at 13:0x UTC before the first command,
stands unedited in out/PREDICTIONS.md. This file holds the commands and where each number came from.

## The setting of every command

    P=/home/user/Universe24/venv314/bin/python
    W=<this worktree>
    D=$W/tools/derivations/open_items/H-The-Bang-That-Births-1
    K=<the hands' kit folder>
    export PYTHONPATH=$W/src TMPDIR=/dev/shm/tmp
    cd /dev/shm/tmp/bb1

Every run under `nice -n 19`, one at a time, the records (the largest 55 MB) under /dev/shm/tmp/bb1 and
never in the worktree, the tables and the readings under $D/out. Nothing under src/ or tests/ edited; no
commit and no push. The 1-minute load stood between 0.74 and 1.13 at every launch, so the kit's
wait_load.py was not needed before any of them (the longest run took 76 seconds).

## The worlds (under worlds/, each a file of numbers, the universe file a copy of tests/worlds/universe_ga2.json)

| file | lay form | count | intervals |
| --- | --- | --- | --- |
| b1_sea_q50000_3600.json | the fourth (the uniform sea, the plane with a gap) | 50,000 | 3,600 |
| b11_sea_q500000_800.json | the fourth | 500,000 | 800 |
| b2_cyc_q{5,6,7,8,9,10,12,16,20,40,100}_24.json | the fifth (the cycle lay, the plane at the gap 0) | as named | 24 |
| b8_cyc_q700000_40.json | the fifth | 700,000 | 40 |
| b9_cyc_q750000_40.json | the fifth | 750,000 | 40 |
| b5_cyc_q2500000_40.json | the fifth | 2,500,000 | 40 |

The cycle lay's digits are world_ga2.json's own (p1 and cz 1, mirror 0); no family's name anywhere.

## The commands, in the order they were run

1. **The band's first probe** (eleven counts, 24 intervals each, 41 seconds in all):
   `nice -n 19 $D/band.sh "$D" "$W"`, which runs
   `$P -m event_universe.run <world> <record> back 10` and then `$P $D/read_record.py <record> <table> 1`
   per world. Output: out/band_readings.txt, out/b2_cyc_q*_24.tsv.
2. **The band's scan** (the engine's own writer through `event_universe.run.record`, so no process per
   count): `nice -n 19 $P $D/scan_counts.py $D/worlds/universe_ga2.json 8 /dev/shm/tmp/bb1/scan_a.json
   5 12 24 36 48 60 96 144 192 300 500 1000` (15 s), then the same at the counts
   `108 324 972 2916 8748 26244 78732 236196 708588 2125764 2500000` (9 s), then at 10 intervals
   `700000 750000 800000 850000 900000 1000000 1100000 1200000 1400000 1600000 1800000 2000000 2200000
   2400000 2800000 3200000` (12 s), then at 30 intervals `550000 600000 625000 650000 675000` (the
   freeze's own edge).
3. **The decisive records**: `nice -n 19 $D/run_one.sh "$D" "$W" b8_cyc_q700000_40 20` (3.7 s) and the
   same for b9_cyc_q750000_40.
4. **The lead carried past its returns**: `nice -n 19 $D/run_one.sh "$D" "$W" b1_sea_q50000_3600 20`
   (76 s forward and back, the record 55 MB, the reader 90 s more). Output: out/b1_sea_q50000_3600.tsv
   (3,600 rows).
5. **The period's second count and the width's rate**: `nice -n 19 $D/rest.sh "$D" "$W" "$K"`, which runs
   b11 (800 intervals), b5 (40 intervals), the gates on b8 and the kit's
   `conservation_check.py /dev/shm/tmp/bb1/b8_cyc_q700000_40.json out $D/out/b8_cons.json`.
6. **The gates and the flag**: `nice -n 19 $D/last.sh "$D" "$W" "$K"`, which runs
   `$P -m event_universe.gates /dev/shm/tmp/bb1/b1_sea_q50000_3600.json`, then
   `$P $K/make_flagged_copy.py bb1 BB1_STATE_WIDTH $D/flag_width.json src $W/src worlds
   $W/tests/worlds/world_hole.json,$W/tests/worlds/world_nature.json python $P`, then the gates on b5
   with `PYTHONPATH=/dev/shm/tmp/bb1/src_bb1 BB1_STATE_WIDTH=1024` and again with the flag empty.

## Where each headline number came from

| the number | the file | the reading |
| --- | --- | --- |
| the frozen content 3,793 and the mark 4,268,834,097 = 4 Gamma^3 | the law's own tables (core/paces.py, features/volume) read through the gates' row 14 | out/b8_gates.txt, "frozen content": 3793 |
| 690,432 of 690,432 meetings refused `orientation` on the lead | /dev/shm/tmp/bb1/b1_sea_q50000_3600.out, the writer's last line | the counts `met` and `refused_orientation` equal |
| the lead's four freezes (43, 1,205, 2,367, 3,529) and seven tops (44 + 581 k) | out/b1_sea_q50000_3600.tsv | the columns `frozen`, `turned`, `held` |
| the period 1,162 and the eight bangs | out/b1_gates.txt, gate 1 | "7 exact returns to Gamma at every Node ... 8 bangs" |
| the lead's width 117 bits, no interval past it | out/b1_gates.txt, the three constants | "max state bits": 117, "first interval past the width": null |
| the counts 5, 12 and 36 births at 64 of 64 with the board alike | out/band_readings.txt and the scans | "first round nodes": 64 with "alike intervals" equal to the record's length |
| every count at or above 550,000 freezes and births | the scans at 30 and 10 intervals | "frozen max": 64 with "births" non-empty |
| b8's freeze at 8, release at 9, retrace at 9 to 7 and 10 to 6, 76 births, 506 credits | out/b8_cyc_q700000_40.tsv and the reader's summary | the columns and "returns (interval, to)" |
| b8's 23 gates SHOWN and 3 in part of 74, gate 14 SHOWN as silence | out/b8_gates.txt | "rows by the verdict's kind" |
| b8's conserved form 11 of 12, EX-S1 548 of 548 | out/b8_cons.txt, out/b8_cons.json | "laws held in full: 11 of 12" |
| the width's rate 141, 225, 394, 733 bits at 34, 36, 38, 40 | out/b5_cyc_q2500000_40.tsv, the column `x_bits` | the reader's "bits by interval" |
| the flag empty bit for bit, 2 of 2 EQUAL | out/flag_check.txt | the two hashes, head and copy equal |
| the gate's width raised buys no numbered gate | out/b5_gates_128.txt against out/b5_gates_1024.txt | the identical "rows by the verdict's kind" |

## The scripts of this hand (all under $D, integers only, no float, ASCII only)

- `read_record.py`: a record's own table per interval (the animation's data) and its summary.
- `scan_counts.py`: the band's scan through `event_universe.run.record`.
- `band.sh`, `run_one.sh`, `rest.sh`, `last.sh`: the drivers (the loops live in scripts and never in a
  command).
- `flag_width.json`: the one replacement of the flagged copy (the reader's gate alone).

No script imports `event_universe.node` or `event_universe.interval`: the writer (`run.py`), the gates
and the kit are the only doors used, as the brief requires.

## What was cut short

Named in DERIVATION.md section 7. The three the box cut by name: the conserved form in full on the
lead's own 3,600 record (the kit's board re-run on a 55 MB record); the kit's `clicks_48.py` on b8 (the
first record of the project that both freezes and clicks); the kit's `reach.py` on b8 and on the lead.
No chain of this hand is still running: every command above exited before the hand-back.

## A note on the one large table

out/b1_sea_q50000_3600.tsv holds the lead's 3,600 rows with the columns
`i, content, X, spread, frozen, turned, held, births, credits, x_bits` (the board being alike at every
interval, the min, the mean and the max of the content and of the volume are one number each, so the
three columns are kept as one). The full fourteen-column table stands at
/dev/shm/tmp/bb1/b1_sea_q50000_3600_full.tsv, outside the worktree, as the brief's size rule requires.

## The commands of the second half (the band's edges, after the measure overturned the prediction)

7. **The huge counts** (the births' first interval against the freeze's):
   `nice -n 19 $P $D/scan_counts.py $D/worlds/universe_ga2.json 8 /dev/shm/tmp/bb1/scan_e.json
   10000000 40000000 100000000 400000000` -- the births at the interval 4 at every one, so the freeze at
   2 and the bang at 4.
8. **The band's upper edge in full**: `nice -n 19 $D/run_one.sh "$D" "$W" b12_cyc_q10000000_24 10`,
   then `$P -m event_universe.gates /dev/shm/tmp/bb1/b12_cyc_q10000000_24.json` and
   `$P $K/conservation_check.py /dev/shm/tmp/bb1/b12_cyc_q10000000_24.json out $D/out/b12_cons.json`
   (**12 of 12 laws in full**). Output: out/b12_cyc_q10000000_24.tsv, out/b12_gates.txt, out/b12_cons.txt.
9. **The band's edges**: `nice -n 19 $D/edge.sh "$D" "$W"` (the counts 2,500,000, 5,000,000,
   20,000,000 and 40,000,000 at 24 intervals, each with its gates). Output: out/b13_cyc_q*_24.tsv,
   out/b13_cyc_q*_24_gates.txt, out/b13_cyc_q*_24_read.txt.
10. **The decisive record**: `nice -n 19 $D/run_one.sh "$D" "$W" b14_cyc_q5000000_240 20` and
   `$P -m event_universe.gates /dev/shm/tmp/bb1/b14_cyc_q5000000_240.json`. Output:
   out/b14_cyc_q5000000_240.tsv (the animation's own table, 240 rows) and out/b14_gates.txt:
   **gate 14 SHOWN, gate 1 SHOWN, gate 1b SHOWN, gate 1c SHOWN, gate 46 SHOWN, the three constants
   SHOWN at 125 bits of state and 127 of transient, 26 SHOWN and 2 in part of 74, 24 births, 454 body
   credits, the run back 20 of 20.**

The worlds added in that half: worlds/b12_cyc_q10000000_24.json, worlds/b13_cyc_q{2500000,5000000,
20000000,40000000}_24.json, worlds/b14_cyc_q5000000_240.json, and worlds/universe_g{100,200,500}.json
(written for the resolution's own reading, which the box did not reach: named missing).

## The commands of the third half (the band's edges to the count, and the three bangs)

11. **The conserved form in full and the reach on the decisive record**:
    `nice -n 19 $D/close.sh "$D" "$W" "$K"`, which runs
    `$P $K/conservation_check.py /dev/shm/tmp/bb1/b14_cyc_q5000000_240.json out $D/out/b14_cons.json`
    (**11 of 12 laws in full**; the log 35,669 of 35,669, EX-S1 478 of 478, the charge 24 of 24, the
    credits' beats 454 of 454, the one short taken >= booked per birth 20 of 24) and
    `$P $K/reach.py $D/worlds/b14_cyc_q5000000_240.json 6 0,0,0 5 $D/out/b14_reach.json cube 4`
    (**"reach one Link": true**, 102 of 102 Links at the distance two or more equal).
12. **The band's edges to the count**: `nice -n 19 $D/edge2.sh "$D" "$W"` (3,000,000, 4,000,000,
    12,000,000 and 15,000,000 at 24 intervals, each with its gates). Output: out/b15_cyc_q*_24*.
13. **The three bangs**: `nice -n 19 $D/run_one.sh "$D" "$W" b16_cyc_q12000000_17 10` (the transient at
    129, two bits past the width) and then
    `nice -n 19 $D/run_one.sh "$D" "$W" b17_cyc_q12000000_16 10` with its gates and the kit's
    conservation check. Output: out/b17_cyc_q12000000_16.tsv (the animation's table of the three bangs),
    out/b17_gates.txt, out/b17_cons.txt: **three freezes, three releases, three bangs at the resolution,
    18 births, the state 121 bits and the transient 124 of 128, gate 1 and gate 14 SHOWN, the three
    constants SHOWN, the run back 10 of 10, 11 of 12 laws in full.**

The worlds added: worlds/b15_cyc_q{3000000,4000000,12000000,15000000}_24.json,
worlds/b16_cyc_q12000000_17.json, worlds/b17_cyc_q12000000_16.json.

14. **The cube's 48 on the record of three bangs**: `nice -n 19 $D/fortyeight.sh "$D" "$W" "$K"`, which
    runs `$P $K/clicks_48.py $D/worlds/b17_cyc_q12000000_16.json 16 $D/out/b17_48.json cube 4` (the 49
    boards in about three minutes). Output: out/b17_48.txt and out/b17_48.json: **1 EQUAL, 0 CONJUGATE,
    47 APART, every image apart at the interval 4**, read with the checker's named limit in
    DERIVATION.md section 3.11 (the images are run from the same sixteen digits of the lay instead of
    the digits carried through the image, so the reading is the tool's and not the law's).
