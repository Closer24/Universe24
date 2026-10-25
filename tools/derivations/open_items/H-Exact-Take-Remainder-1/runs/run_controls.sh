#!/bin/sh
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/ex1
K=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/kit
PY=/home/user/Universe24/venv314/bin/python
cd $W/tools/derivations/ex1/runs
export PYTHONPATH=$W/src TMPDIR=/dev/shm/tmp
$PY $W/tools/derivations/toys/lean/toy.py $W/tools/derivations/ex1/worlds/world_chiral.json chiral60_base.json back 10 > chiral60_base.out 2>&1; echo "chiral60 exit $?"
$PY $W/tools/derivations/toys/lean/toy.py $W/tools/derivations/ex1/worlds/world_bodies.json bodies120_base.json back 10 > bodies120_base.out 2>&1; echo "bodies120 exit $?"
cp $K/world_chiral_300.json $W/tools/derivations/ex1/worlds/world_chiral_300.json
$PY $W/tools/derivations/toys/lean/toy.py $W/tools/derivations/ex1/worlds/world_chiral_300.json chiral300_base.json back 10 > chiral300_base.out 2>&1; echo "chiral300 exit $?"
