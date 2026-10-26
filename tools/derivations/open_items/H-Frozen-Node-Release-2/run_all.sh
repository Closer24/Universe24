#!/bin/sh
# fr2: every board measurement, in parallel, under nice; the flag FR2_RELEASE from the environment (unset: the head bit for bit)
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
W=../../../..
S=../../../../../..
R=$S/records/2ab32b518
export TMPDIR=/dev/shm/tmp
run() { out=$1; shift; nice -n 19 "$@" > out/$out.stdout 2> out/$out.stderr; echo done > out/$out.done; }
FR2_RELEASE=1 run chiral2400_f $PY run_record.py src_fr2 $W/tests/worlds/world_chiral.json 2400 10 /dev/shm/tmp/fr2_chiral2400_f.json $S/bh/chiral_2400.json &
FR2_RELEASE=1 run universe400_f $PY run_record.py src_fr2 $W/tests/worlds/world_universe.json 400 10 /dev/shm/tmp/fr2_universe400_f.json $R/world_universe_400.json &
FR2_RELEASE=1 run pair3_400_f $PY run_record.py src_fr2 $W/tests/worlds/world_pair_3.json 400 10 /dev/shm/tmp/fr2_pair3_400_f.json $R/world_pair_3_400.json &
FR2_RELEASE=1 run plasma3_170_f $PY run_record.py src_fr2 $W/tests/worlds/world_plasma_3.json 170 10 /dev/shm/tmp/fr2_plasma3_170_f.json $R/world_plasma_3_170.json &
FR2_RELEASE=1 run ga2_f $PY ga2_course.py src_fr2 $W/tests/worlds/world_ga2.json 450 10 out/ga2_f.json 2,218,442 &
FR2_RELEASE=1 run c48_3cube_60_f $PY run_48.py src_fr2 worlds/world_chiral_3_30.json 60 out/c48_3cube_60_f.json &
FR2_RELEASE=  run c48_3cube_60_off $PY run_48.py src_fr2 worlds/world_chiral_3_30.json 60 out/c48_3cube_60_off.json &
FR2_RELEASE=  run hole60_off $PY run_record.py src_fr2 $W/tests/worlds/world_hole.json 60 10 /dev/shm/tmp/fr2_hole60_off.json $R/world_hole_60.json &
FR2_RELEASE=1 run hole60_f $PY run_record.py src_fr2 $W/tests/worlds/world_hole.json 60 10 /dev/shm/tmp/fr2_hole60_f.json $R/world_hole_60.json &
FR2_RELEASE=  run chiral60_off $PY run_record.py src_fr2 $W/tests/worlds/world_chiral.json 60 10 /dev/shm/tmp/fr2_chiral60_off.json $R/world_chiral_60.json &
wait
echo all > out/run_all.done
