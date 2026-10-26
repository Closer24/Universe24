#!/bin/sh
# cp2: the second run (the gain read at the quarter turn) of the worlds with births
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
SRC=/dev/shm/tmp/cp2/src_cp2
O=/dev/shm/tmp/cp2/out
W=../../../..
R=../../../../../../records/2ab32b518
export TMPDIR=/dev/shm/tmp
run() { out=$1; shift; nice -n 19 "$@" > out/$out.stdout 2> out/$out.stderr; echo done > out/$out.done; }
CP2_FORM=1 run hole60_f2 $PY run_record.py $SRC $W/tests/worlds/world_hole.json 60 10 $O/hole60_f2.json $R/world_hole_60.json &
CP2_FORM=1 run chiral60_f2 $PY run_record.py $SRC $W/tests/worlds/world_chiral.json 60 10 $O/chiral60_f2.json $R/world_chiral_60.json &
CP2_FORM=1 run ga2_f2 $PY ga2_course.py $SRC $W/tests/worlds/world_ga2.json 450 10 $O/ga2_f2.json 2,218,442 &
CP2_FORM=1 run c48_3cube_60_f2 $PY run_48.py $SRC worlds/world_chiral_3_30.json 60 $O/c48_3cube_60_f2.json &
CP2_FORM= run c48_3cube_60_off $PY run_48.py $SRC worlds/world_chiral_3_30.json 60 $O/c48_3cube_60_off.json &
wait
echo all > out/run_f2.done
