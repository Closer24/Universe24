#!/bin/sh
# sl2: every measurement in parallel under nice; SL2_FORM=1 the six-Link lay, unset the head's form; the records to /dev/shm/tmp/sl2/out, the summaries to out/
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
SRC=/dev/shm/tmp/sl2/src_sl2
W=../../../../tests/worlds
R=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/records/2ab32b518
O=/dev/shm/tmp/sl2/out
export TMPDIR=/dev/shm/tmp
mkdir -p out $O
run() { out=$1; shift; nice -n 19 "$@" > out/$out.stdout 2> out/$out.stderr; echo done > out/$out.done; }
SL2_FORM=1 run hole60_f $PY run_record_sl2.py $SRC $W/world_hole.json 60 10 $O/hole60_f.json $R/world_hole_60.json &
SL2_FORM=1 run chiral60_f $PY run_record_sl2.py $SRC $W/world_chiral.json 60 10 $O/chiral60_f.json $R/world_chiral_60.json &
SL2_FORM=1 run ga2_450_f $PY ga2_course_sl2.py $SRC $W/world_ga2.json 450 10 $O/ga2_450_course_f.json 2,218,442 &
SL2_FORM=1 run ga2_450_rec_f $PY run_record_sl2.py $SRC $W/world_ga2.json 450 10 $O/ga2_450_f.json $R/world_ga2_450.json &
SL2_FORM=1 run bodies300_f $PY run_record_sl2.py $SRC $W/world_bodies.json 300 10 $O/bodies300_f.json $R/world_bodies_300.json &
SL2_FORM=1 run compton60_f $PY run_record_sl2.py $SRC worlds/world_compton.json 60 10 $O/compton60_f.json &
SL2_FORM=1 run universe400_f $PY run_record_sl2.py $SRC $W/world_universe.json 400 10 $O/universe400_f.json $R/world_universe_400.json &
SL2_FORM=1 run pair3_400_f $PY run_record_sl2.py $SRC $W/world_pair_3.json 400 10 $O/pair3_400_f.json $R/world_pair_3_400.json &
SL2_FORM=1 run plasma3_170_f $PY run_record_sl2.py $SRC $W/world_plasma_3.json 170 10 $O/plasma3_170_f.json $R/world_plasma_3_170.json &
SL2_FORM=  run hole60_off $PY run_record_sl2.py $SRC $W/world_hole.json 60 10 $O/hole60_off.json $R/world_hole_60.json &
SL2_FORM=1 run c48_3cube_60_f $PY run_48_sl2.py $SRC worlds/world_chiral_3_30.json 60 $O/c48_3cube_60_f.json &
wait
echo all > out/run_all.done
