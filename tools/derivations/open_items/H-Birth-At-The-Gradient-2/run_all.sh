#!/bin/sh
# bg2: every measurement in parallel under nice; FR2_RELEASE=1 and BG2_FORM=1 from the environment on the copy src_bg2 (both unset: the head bit for bit)
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
W=../../../..
S=../../../../../..
R=$S/records/2ab32b518
export TMPDIR=/dev/shm/tmp
run() { out=$1; shift; date -u +%T > out/$out.start; nice -n 19 "$@" > out/$out.stdout 2> out/$out.stderr; date -u +%T > out/$out.done; }
export FR2_RELEASE=1 BG2_FORM=1
run chiral3000_form $PY bg2_probe.py src_bg2 $W/tests/worlds/world_chiral.json 3000 10 out/chiral3000_form.jsonl &
run node400_form $PY bg2_probe.py src_bg2 $W/tests/worlds/world_node.json 400 10 out/node400_form.jsonl 4268834097 2560000000 &
run universe400_form $PY run_record.py src_bg2 $W/tests/worlds/world_universe.json 400 10 /dev/shm/tmp/bg2_universe400.json $R/world_universe_400.json &
run pair3_400_form $PY run_record.py src_bg2 $W/tests/worlds/world_pair_3.json 400 10 /dev/shm/tmp/bg2_pair3_400.json $R/world_pair_3_400.json &
run plasma3_170_form $PY run_record.py src_bg2 $W/tests/worlds/world_plasma_3.json 170 10 /dev/shm/tmp/bg2_plasma3_170.json $R/world_plasma_3_170.json &
run ga2_450_form $PY ga2_course.py src_bg2 $W/tests/worlds/world_ga2.json 450 10 out/ga2_450_form.json 2,218,442 &
run hole60_form $PY run_record.py src_bg2 $W/tests/worlds/world_hole.json 60 10 /dev/shm/tmp/bg2_hole60.json $R/world_hole_60.json &
run chiral60_form $PY run_record.py src_bg2 $W/tests/worlds/world_chiral.json 60 10 /dev/shm/tmp/bg2_chiral60.json $R/world_chiral_60.json &
run bodies300_form $PY run_record.py src_bg2 $W/tests/worlds/world_bodies.json 300 10 /dev/shm/tmp/bg2_bodies300.json $R/world_bodies_300.json &
run c48_3cube_60_form $PY run_48.py src_bg2 worlds/world_chiral_3_30.json 60 out/c48_3cube_60_form.json &
wait
echo all > out/run_all.done
