#!/bin/sh
# fr2: the fed one-Node world to 2,000 under the flag: standing (before = now), rising gently (before at 3,780), rising hard (before at 3,700); the run back 100
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
W=../../../..
export TMPDIR=/dev/shm/tmp
run() { out=$1; shift; nice -n 19 "$@" > out/$out.stdout 2> out/$out.stderr; echo done > out/$out.done; }
FR2_RELEASE=1 run one_node_standing_2000 $PY one_node_fr2.py src_fr2 $W/tests/worlds/world_node.json 3793 3793 2000 100 out/one_node_standing_3793_2000.json &
FR2_RELEASE=1 run one_node_gentle_2000 $PY one_node_fr2.py src_fr2 $W/tests/worlds/world_node.json 3793 3780 2000 100 out/one_node_rising_3793_3780_2000.json &
FR2_RELEASE=1 run one_node_hard_2000 $PY one_node_fr2.py src_fr2 $W/tests/worlds/world_node.json 3793 3700 2000 100 out/one_node_rising_3793_3700_2000.json &
FR2_RELEASE=  run one_node_hard_off_60 $PY one_node_fr2.py src_fr2 $W/tests/worlds/world_node.json 3793 3700 60 60 out/one_node_rising_3793_3700_off_60.json &
wait
echo all > out/run_one_node.done
