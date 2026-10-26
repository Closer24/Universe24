#!/bin/sh
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
SRC=/dev/shm/tmp/sl1/src_sl1
W=../../../..
R=../../../../../../records/2ab32b518
O=/dev/shm/tmp/sl1/out
export TMPDIR=/dev/shm/tmp
run() { out=$1; shift; nice -n 19 "$@" > out/$out.stdout 2> out/$out.stderr; echo done > out/$out.done; }
( SL1_FORM=1 run hole60_f1 $PY run_record.py $SRC $W/tests/worlds/world_hole.json 60 10 $O/hole60_f1.json $R/world_hole_60.json
  SL1_FORM=2 run hole60_f2 $PY run_record.py $SRC $W/tests/worlds/world_hole.json 60 10 $O/hole60_f2.json $R/world_hole_60.json ) &
( SL1_FORM=1 run chiral60_f1 $PY run_record.py $SRC $W/tests/worlds/world_chiral.json 60 10 $O/chiral60_f1.json $R/world_chiral_60.json
  SL1_FORM=2 run chiral60_f2 $PY run_record.py $SRC $W/tests/worlds/world_chiral.json 60 10 $O/chiral60_f2.json $R/world_chiral_60.json ) &
( SL1_FORM=1 run ga2_450_f1 $PY ga2_course.py $SRC $W/tests/worlds/world_ga2.json 450 10 $O/ga2_450_f1.json 2,218,442 ) &
( SL1_FORM=1 run c48_3cube_60_f1b $PY run_48.py $SRC worlds/world_chiral_3_30.json 60 $O/c48_3cube_60_f1b.json ) &
wait
echo all > out/run_rest.done
