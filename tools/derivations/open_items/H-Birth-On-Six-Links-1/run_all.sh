#!/bin/sh
# sl1: every measurement, in parallel, under nice; the records' cache read for the head's records; the records above 200 KB under /dev/shm/tmp/sl1/out
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
SRC=/dev/shm/tmp/sl1/src_sl1
W=../../../..
R=../../../../../../records/2ab32b518
O=/dev/shm/tmp/sl1/out
export TMPDIR=/dev/shm/tmp
run() { out=$1; shift; nice -n 19 "$@" > out/$out.stdout 2> out/$out.stderr; echo done > out/$out.done; }
( SL1_FORM=1 run hole60_f1 $PY run_record.py $SRC $W/tests/worlds/world_hole.json 60 10 $O/hole60_f1.json $R/world_hole_60.json
  SL1_FORM=1 run compton60_f1 $PY run_record.py $SRC worlds/world_compton.json 60 10 $O/compton60_f1.json
  SL1_FORM=  run hole60_off $PY run_record.py $SRC $W/tests/worlds/world_hole.json 60 10 $O/hole60_off.json $R/world_hole_60.json
  SL1_FORM=2 run hole60_f2 $PY run_record.py $SRC $W/tests/worlds/world_hole.json 60 10 $O/hole60_f2.json $R/world_hole_60.json ) &
( SL1_FORM=1 run chiral60_f1 $PY run_record.py $SRC $W/tests/worlds/world_chiral.json 60 10 $O/chiral60_f1.json $R/world_chiral_60.json
  SL1_FORM=1 run pair3_400_f1 $PY run_record.py $SRC $W/tests/worlds/world_pair_3.json 400 10 $O/pair3_400_f1.json $R/world_pair_3_400.json
  SL1_FORM=2 run chiral60_f2 $PY run_record.py $SRC $W/tests/worlds/world_chiral.json 60 10 $O/chiral60_f2.json $R/world_chiral_60.json ) &
( SL1_FORM=1 run ga2_450_f1 $PY ga2_course.py $SRC $W/tests/worlds/world_ga2.json 450 10 $O/ga2_450_f1.json 2,218,442
  SL1_FORM=1 run plasma3_170_f1 $PY run_record.py $SRC $W/tests/worlds/world_plasma_3.json 170 10 $O/plasma3_170_f1.json $R/world_plasma_3_170.json ) &
( SL1_FORM=1 run c48_3cube_60_f1 $PY run_48.py $SRC worlds/world_chiral_3_30.json 60 $O/c48_3cube_60_f1.json
  SL1_FORM=1 run bodies300_f1 $PY run_record.py $SRC $W/tests/worlds/world_bodies.json 300 10 $O/bodies300_f1.json $R/world_bodies_300.json
  SL1_FORM=1 run universe400_f1 $PY run_record.py $SRC $W/tests/worlds/world_universe.json 400 10 $O/universe400_f1.json $R/world_universe_400.json ) &
wait
echo all > out/run_all.done
