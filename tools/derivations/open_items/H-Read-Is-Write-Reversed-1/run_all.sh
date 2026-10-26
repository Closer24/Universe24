#!/bin/sh
# rw1: every measurement under nice on the flagged copy at /dev/shm/tmp/rw1/src_rw1 (RW1_FORM=1 the fold, empty the head bit for bit)
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
W=$S/hands/rw1
R=$S/records/2ab32b518
PY=/home/user/Universe24/venv314/bin/python
REC=$W/tools/derivations/open_items/H-Lay-Rest-Mirror-2/run_record.py
R48=$W/tools/derivations/open_items/H-48-In-The-Clicks-3/run_48.py
OUT=/dev/shm/tmp/rw1/out
SRC=/dev/shm/tmp/rw1/src_rw1
export TMPDIR=/dev/shm/tmp
cd /dev/shm/tmp/rw1
run() { out=$1; shift; t0=$(date +%s); nice -n 19 "$@" > $OUT/$out.stdout 2> $OUT/$out.stderr; echo "done $(( $(date +%s) - t0 )) s" > $OUT/$out.done; }
RW1_FORM=1 run hole60 $PY $REC $SRC $W/tests/worlds/world_hole.json 60 20 $OUT/hole60.json $R/world_hole_60.json &
RW1_FORM=1 run chiral60 $PY $REC $SRC $W/tests/worlds/world_chiral.json 60 20 $OUT/chiral60.json $R/world_chiral_60.json &
RW1_FORM=1 run ga2_450 $PY $REC $SRC $W/tests/worlds/world_ga2.json 450 10 $OUT/ga2_450.json $R/world_ga2_450.json &
RW1_FORM=1 run universe400 $PY $REC $SRC $W/tests/worlds/world_universe.json 400 10 $OUT/universe400.json $R/world_universe_400.json &
wait
RW1_FORM=1 run bodies300 $PY $REC $SRC $W/tests/worlds/world_bodies.json 300 10 $OUT/bodies300.json $R/world_bodies_300.json &
RW1_FORM=1 run pair3_400 $PY $REC $SRC $W/tests/worlds/world_pair_3.json 400 10 $OUT/pair3_400.json $R/world_pair_3_400.json &
RW1_FORM=1 run plasma3_170 $PY $REC $SRC $W/tests/worlds/world_plasma_3.json 170 10 $OUT/plasma3_170.json $R/world_plasma_3_170.json &
RW1_FORM=1 run c48_3cube_60 $PY $R48 $SRC $W/tools/derivations/open_items/H-48-In-The-Clicks-3/worlds/world_chiral_3_30.json 60 $OUT/c48_3cube_60.json &
wait
RW1_FORM=1 run sea3_240_on $PY $REC $SRC $W/tests/worlds/world_sea_3.json 240 10 $OUT/sea3_240_on.json &
RW1_FORM= run sea3_240_off $PY $REC $SRC $W/tests/worlds/world_sea_3.json 240 10 $OUT/sea3_240_off.json &
RW1_FORM=1 run universe3_100_on $PY $REC $SRC $W/tests/worlds/world_universe_3.json 100 10 $OUT/universe3_100_on.json &
RW1_FORM= run universe3_100_off $PY $REC $SRC $W/tests/worlds/world_universe_3.json 100 10 $OUT/universe3_100_off.json &
wait
RW1_FORM=1 run plasma_170_on $PY $REC $SRC $W/tests/worlds/world_plasma.json 170 10 $OUT/plasma_170_on.json &
RW1_FORM= run plasma_170_off $PY $REC $SRC $W/tests/worlds/world_plasma.json 170 10 $OUT/plasma_170_off.json &
(cd $W && RW1_FORM=1 run suite_on $PY -m pytest -q -x -o pythonpath=$SRC tests -p no:cacheprovider) &
wait
echo all > $OUT/run_all.done
