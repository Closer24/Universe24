# Report: H-The-Bang-That-Births-2 (bb2, 2026-10-26, 12:5x to 14:2x UTC, the engine head 338820837)

The derivation, the prediction, the measures, the period, the sentence, the bugs and the ledger row stand in
DERIVATION.md beside this file. This report holds the commands and the files, so that every number above can be
re-run.

## The setting for every command
    P=/home/user/Universe24/venv314/bin/python
    W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/bb2
    H=$W/tools/derivations/open_items/H-The-Bang-That-Births-2
    K=$W/tools/derivations/open_items/H-Kit-48-Re-Cut-1
    export PYTHONPATH=$W/src TMPDIR=/dev/shm/tmp
    cd /dev/shm/tmp/bb2   # every record above 200 KB lives here, never in the worktree

## The runs, in the order they were made
1. The calibration (named in out/PREDICTIONS.md as the one run before the predictions):
   `nice -n 19 $P -m event_universe.run $H/worlds/t0_cal.json /dev/shm/tmp/bb2/t0_cal.json back 5`
2. The lead carried past its returns (the one long run of the box, about 80 s):
   `nice -n 19 $P -m event_universe.run $H/worlds/b0_sea_q50000_long.json /dev/shm/tmp/bb2/b0_long.json back 20`
   `nice -n 19 $P $H/read_band.py /dev/shm/tmp/bb2/b0_long.json $H/out/b0_long_table.tsv $H/out/b0_long_summary.json`
3. The band, ten short runs through $H/../../../../../chain (the script /dev/shm/tmp/bb2/chain.sh, each run
   `-m event_universe.run $H/worlds/<w>.json /dev/shm/tmp/bb2/<w>.json back 20` then read_band.py):
   b1_sea_q1, b2_sea_q5000, b3_sea_q7500, b4_sea_q8000, b5_sea_q50000_sense1, ba_sea_q100000, b8_sea_q500000,
   b9_sea_q5000000, b6_wave_q50000, b7_wave_q2500000.
4. The conserved form on the lead:
   `nice -n 19 $P $K/conservation_check.py /dev/shm/tmp/bb2/b0_long.json board off out $H/out/b0_long_cons.json`
   (7 of 7 laws in full; the five that read clicks read 0 of 0 on a record with no click.)
5. The gates on the lead, by the engine's own board module (the decoder has no main entry: bug 1):
   `$P -c "import json,sys; sys.set_int_max_str_digits(1000000); from event_universe import board; from
   event_universe.events import Record; r=Record(json.load(open('/dev/shm/tmp/bb2/b0_long.json'))); ..."`
   with board.recurring_bang, board.horizon, board.stopped_clock and board.same_gates; out/b0_long_gates.txt.
6. The flagged copy (a measure under a flag; it changes no law):
   `nice -n 19 $P $K/make_flagged_copy.py bb2 WIDEWORD $H/repl_wideword.json src $W/src worlds
   $W/tests/worlds/world_hole.json,$W/tests/worlds/world_nature.json python $P`
   -> 2 of 2 worlds bit for bit with the head, exit 0, the two hashes in DERIVATION.md section 3.5.

## The files
- worlds/: t0_cal, b0_sea_q50000_long (the lead at 3,600), b1_sea_q1, b2_sea_q5000, b3_sea_q7500, b4_sea_q8000,
  b5_sea_q50000_sense1, ba_sea_q100000, b8_sea_q500000, b9_sea_q5000000, b6_wave_q50000, b7_wave_q2500000,
  and universe_ga2.json beside them. Every world is a file of numbers; no act and no world key was added.
- read_band.py: the reader of one record (the animation's table and the band's readings), integers only, the
  mean as a quotient with its remainder; it raises the digit limit because a record past the law's width cannot
  otherwise be parsed (bug 4).
- repl_wideword.json: the one replacement of the flagged copy (rows.py:15, the gate's width constant).
- out/PREDICTIONS.md: the predictions, written before every run but the calibration.
- out/*_table.tsv: the animation's own data, a row per interval, for the Reader.
- out/*_summary.json: the readings per record.
- out/b0_long_gates.txt, out/b0_long_cons.txt, out/b0_long_cons.json.

## The rules kept
Integers only (no float in any script; grep clean). No number in a proposed src line: no src line is proposed;
the one flagged line reads the law's own 128 as its default. No family's name in src or in a world file. ASCII
only. None of the brief's barred words (grep clean on DERIVATION.md, REPORT.md, PREDICTIONS.md and read_band.py).
No run of three all-caps words (grep clean). Nothing under src/ or tests/ of the worktree edited; no commit, no
push. Every file above 200 KB under /dev/shm/tmp/bb2/. One run at a time; the load read before the long run
(0.57 and 1.02 on the 1-minute reading, below 3).
