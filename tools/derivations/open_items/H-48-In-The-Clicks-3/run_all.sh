#!/bin/sh
# a483: every measurement, in parallel, under nice; the records' cache read for the head's three records and the uniform boards
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
W=../../../..
R=../../../../../../records/d9d7914ff
export TMPDIR=/dev/shm/tmp
run() { out=$1; shift; nice -n 19 "$@" > out/$out.stdout 2> out/$out.stderr; echo done > out/$out.done; }
A483_READ=  run hole60_off $PY run_record.py src_a483 $W/tests/worlds/world_hole.json 60 10 out/hole60_off.json $R/world_hole_60.json &
A483_READ=1 run c48_3cube_60_f1 $PY run_48.py src_a483 worlds/world_chiral_3_30.json 60 out/c48_3cube_60_f1.json &
A483_READ=2 run c48_3cube_60_f2 $PY run_48.py src_a483 worlds/world_chiral_3_30.json 60 out/c48_3cube_60_f2.json &
A483_READ=1 run ga2_f1 $PY ga2_course.py src_a483 $W/tests/worlds/world_ga2.json 450 10 out/ga2_f1.json 2,218,442 &
A483_READ=2 run ga2_f2 $PY ga2_course.py src_a483 $W/tests/worlds/world_ga2.json 450 10 out/ga2_f2.json 2,218,442 &
A483_READ=  run ga2_off $PY ga2_course.py src_a483 $W/tests/worlds/world_ga2.json 12 2 out/ga2_off.json 2 &
A483_READ=1 run c48_5cube_60_f1 $PY run_48.py src_a483 worlds/world_chiral_5_60.json 60 out/c48_5cube_60_f1.json &
A483_READ=1 run hole60_f1 $PY run_record.py src_a483 $W/tests/worlds/world_hole.json 60 10 out/hole60_f1.json $R/world_hole_60.json &
A483_READ=1 run chiral60_f1 $PY run_record.py src_a483 $W/tests/worlds/world_chiral.json 60 10 out/chiral60_f1.json $R/world_chiral_60.json &
A483_READ=1 run bodies300_f1 $PY run_record.py src_a483 $W/tests/worlds/world_bodies.json 300 10 out/bodies300_f1.json $R/world_bodies_300.json &
A483_READ=1 run universe400_f1 $PY run_record.py src_a483 $W/tests/worlds/world_universe.json 400 10 out/universe400_f1.json $R/world_universe_400.json &
A483_READ=1 run plasma170_f1 $PY run_record.py src_a483 $W/tests/worlds/world_plasma_3.json 170 10 out/plasma170_f1.json $R/world_plasma_3_170.json &
A483_READ=1 run sea240_f1 $PY run_record.py src_a483 $W/tests/worlds/world_sea_3.json 240 10 out/sea240_f1.json &
A483_READ=  run sea240_off $PY run_record.py src_a483 $W/tests/worlds/world_sea_3.json 240 10 out/sea240_off.json &
wait
echo all > out/run_all.done
