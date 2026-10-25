#!/bin/sh
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/ex1
PY=/home/user/Universe24/venv314/bin/python
D=$W/tools/derivations/ex1
cd $D/runs
export PYTHONPATH=$D/engine TMPDIR=/dev/shm/tmp
$PY $D/toy_ex1.py $D/worlds/world_chiral60_zero.json chiral60_zero.json back 10 > chiral60_zero.out 2>&1; echo "chiral60 zero exit $?"
$PY $D/toy_ex1.py $D/worlds/world_chiral60_half.json chiral60_half.json back 10 > chiral60_half.out 2>&1; echo "chiral60 half exit $?"
$PY $D/toy_ex1.py $D/worlds/world_bodies120_zero.json bodies120_zero.json back 10 > bodies120_zero.out 2>&1; echo "bodies120 zero exit $?"
$PY $D/cube48_ex1.py $W/src $D/worlds/world_chiral3_30.json cube48_control.json > cube48_control.out 2>&1; echo "cube48 control exit $?"
$PY $D/cube48_ex1.py $D/engine $D/worlds/world_chiral3_30_zero.json cube48_zero.json > cube48_zero.out 2>&1; echo "cube48 zero exit $?"
$PY $D/toy_ex1.py $D/worlds/world_chiral300_zero.json chiral300_zero.json back 10 > chiral300_zero.out 2>&1; echo "chiral300 zero exit $?"
