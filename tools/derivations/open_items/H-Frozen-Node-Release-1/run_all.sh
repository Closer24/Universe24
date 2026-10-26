#!/bin/sh
# fr1: every measurement in parallel under nice; the flag FR1_RELEASE from the environment (empty: the head bit for bit)
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
W=../../../..
R=../../../../../../records/2ab32b518
BH=../../../../../../bh
export TMPDIR=/dev/shm/tmp
export PYTHONPATH=
run() { out=$1; shift; nice -n 19 "$@" > out/$out.stdout 2> out/$out.stderr; echo done > out/$out.done; }
# the fed one-Node world (the 3-cube's centre at the frozen content 3,793; with a velocity: the before slot at the content 3,700; at rest)
FR1_RELEASE=1 run one_node_v3700_on  $PY one_node_fr1.py src_fr1 worlds/world_node.json 3793 2000 none out/one_node_v3700_on.json 3700 &
FR1_RELEASE=  run one_node_v3700_off $PY one_node_fr1.py src_fr1 worlds/world_node.json 3793 2000 none out/one_node_v3700_off.json 3700 &
FR1_RELEASE=1 run one_node_rest_on   $PY one_node_fr1.py src_fr1 worlds/world_node.json 3793 2000 none out/one_node_rest_on.json &
# the chiral 2,400 with the run back 10 (against the Boss's record)
FR1_RELEASE=1 run chiral2400_on $PY run_record.py src_fr1 $W/tests/worlds/world_chiral.json 2400 10 out/chiral2400_on.json $BH/chiral_2400.json &
wait
echo stage1 > out/stage1.done
# the uniform boards against the cache, ga2 450, the 48 on the chiral 3-cube to 60
FR1_RELEASE=1 run universe400_on $PY run_record.py src_fr1 $W/tests/worlds/world_universe.json 400 10 out/universe400_on.json $R/world_universe_400.json &
FR1_RELEASE=1 run pair3_400_on   $PY run_record.py src_fr1 $W/tests/worlds/world_pair_3.json 400 10 out/pair3_400_on.json $R/world_pair_3_400.json &
FR1_RELEASE=1 run plasma170_on   $PY run_record.py src_fr1 $W/tests/worlds/world_plasma_3.json 170 10 out/plasma170_on.json $R/world_plasma_3_170.json &
FR1_RELEASE=1 run ga2_on $PY ga2_course.py src_fr1 $W/tests/worlds/world_ga2.json 450 10 out/ga2_on.json 2,218,442 &
wait
FR1_RELEASE=1 run c48_3cube_60_on  $PY run_48.py src_fr1 worlds/world_chiral_3_30.json 60 out/c48_3cube_60_on.json &
FR1_RELEASE=  run c48_3cube_60_off $PY run_48.py src_fr1 worlds/world_chiral_3_30.json 60 out/c48_3cube_60_off.json &
wait
echo all > out/run_all.done
