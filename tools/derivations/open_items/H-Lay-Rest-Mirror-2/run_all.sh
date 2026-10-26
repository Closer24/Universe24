#!/bin/sh
# lr2: every measurement in parallel under nice; L = the lay's rest flag, P = the centred pick flag
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
W=../../../..
R=../../../../../../records/2ab32b518
export TMPDIR=/dev/shm/tmp
run() { out=$1; shift; nice -n 19 "$@" > out/$out.stdout 2> out/$out.stderr; echo done > out/$out.done; }
LR2_LAY=1 LR2_PICK=1 run c48_3cube_60_LP $PY run_48.py src_lr2 worlds/world_chiral_3_30.json 60 out/c48_3cube_60_LP.json &
LR2_LAY=  LR2_PICK=1 run c48_3cube_60_P $PY run_48.py src_lr2 worlds/world_chiral_3_30.json 60 out/c48_3cube_60_P.json &
LR2_LAY=1 LR2_PICK=  run c48_3cube_60_L $PY run_48.py src_lr2 worlds/world_chiral_3_30.json 60 out/c48_3cube_60_L.json &
LR2_LAY=1 LR2_PICK=1 run ga2_LP $PY ga2_course.py src_lr2 $W/tests/worlds/world_ga2.json 450 10 out/ga2_LP.json 2,218,442 &
LR2_LAY=  LR2_PICK=1 run ga2_P $PY ga2_course.py src_lr2 $W/tests/worlds/world_ga2.json 450 10 out/ga2_P.json 2,218,442 &
LR2_LAY=1 LR2_PICK=  run ga2_L $PY ga2_course.py src_lr2 $W/tests/worlds/world_ga2.json 450 10 out/ga2_L.json 2,218,442 &
LR2_LAY=  LR2_PICK=  run ga2_off $PY ga2_course.py src_lr2 $W/tests/worlds/world_ga2.json 450 10 out/ga2_off.json 2,218,442 &
wait
LR2_LAY=1 LR2_PICK=1 run c48_5cube_60_LP $PY run_48.py src_lr2 worlds/world_chiral_5_60.json 60 out/c48_5cube_60_LP.json &
LR2_LAY=1 LR2_PICK=1 run hole60_LP $PY run_record.py src_lr2 $W/tests/worlds/world_hole.json 60 10 out/hole60_LP.json $R/world_hole_60.json &
LR2_LAY=1 LR2_PICK=1 run chiral60_LP $PY run_record.py src_lr2 $W/tests/worlds/world_chiral.json 60 10 out/chiral60_LP.json $R/world_chiral_60.json &
LR2_LAY=1 LR2_PICK=1 run bodies300_LP $PY run_record.py src_lr2 $W/tests/worlds/world_bodies.json 300 10 out/bodies300_LP.json $R/world_bodies_300.json &
wait
LR2_LAY=1 LR2_PICK=1 run sea240_LP $PY run_record.py src_lr2 $W/tests/worlds/world_sea_3.json 240 10 out/sea240_LP.json &
LR2_LAY=  LR2_PICK=  run sea240_off $PY run_record.py src_lr2 $W/tests/worlds/world_sea_3.json 240 10 out/sea240_off.json &
LR2_LAY=1 LR2_PICK=1 run universe400_LP $PY run_record.py src_lr2 $W/tests/worlds/world_universe.json 400 10 out/universe400_LP.json $R/world_universe_400.json &
LR2_LAY=1 LR2_PICK=1 run plasma170_LP $PY run_record.py src_lr2 $W/tests/worlds/world_plasma_3.json 170 10 out/plasma170_LP.json $R/world_plasma_3_170.json &
wait
echo all > out/run_all.done
