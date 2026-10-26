#!/bin/sh
# cm1: every measurement in parallel under nice on the flagged copy /dev/shm/tmp/cm1/src; records above 200 KB under /dev/shm/tmp/cm1/out
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
W=../../../..
R=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/records/2ab32b518
SRC=/dev/shm/tmp/cm1/src
O=/dev/shm/tmp/cm1/out
RR=../H-Lay-Rest-Mirror-2/run_record.py
export TMPDIR=/dev/shm/tmp
run() { out=$1; shift; nice -n 19 "$@" > out/$out.stdout 2> out/$out.stderr; echo done > out/$out.done; }
CM1_FORM=1 run hole60_f $PY $RR $SRC $W/tests/worlds/world_hole.json 60 10 $O/hole60_f.json $R/world_hole_60.json &
CM1_FORM=  run hole60_off $PY $RR $SRC $W/tests/worlds/world_hole.json 60 10 $O/hole60_off.json $R/world_hole_60.json &
CM1_FORM=1 run chiral60_f $PY $RR $SRC $W/tests/worlds/world_chiral.json 60 10 $O/chiral60_f.json $R/world_chiral_60.json &
CM1_FORM=1 run bodies300_f $PY $RR $SRC $W/tests/worlds/world_bodies.json 300 10 $O/bodies300_f.json $R/world_bodies_300.json &
CM1_FORM=1 run compton60_f $PY $RR $SRC worlds/world_compton.json 60 10 $O/compton60_f.json &
CM1_FORM=1 run universe400_f $PY $RR $SRC $W/tests/worlds/world_universe.json 400 10 $O/universe400_f.json $R/world_universe_400.json &
CM1_FORM=1 run pair3_400_f $PY $RR $SRC $W/tests/worlds/world_pair_3.json 400 10 $O/pair3_400_f.json $R/world_pair_3_400.json &
CM1_FORM=1 run plasma3_170_f $PY $RR $SRC $W/tests/worlds/world_plasma_3.json 170 10 $O/plasma3_170_f.json $R/world_plasma_3_170.json &
CM1_FORM=1 run ga2_450_f $PY $RR $SRC $W/tests/worlds/world_ga2.json 450 10 $O/ga2_450_f.json $R/world_ga2_450.json &
CM1_FORM=1 run ga2_course_f $PY ga2_course_cm1.py $SRC $W/tests/worlds/world_ga2.json 450 10 $O/ga2_course_f.json 2,218,442 &
CM1_FORM=1 run c48_3cube_60_f $PY run_48_cm1.py $SRC worlds/world_chiral_3_30.json 60 $O/c48_3cube_60_f.json &
CM1_FORM=  run c48_3cube_60_off $PY run_48_cm1.py $SRC worlds/world_chiral_3_30.json 60 $O/c48_3cube_60_off.json &
wait
echo all > out/run_all.done
