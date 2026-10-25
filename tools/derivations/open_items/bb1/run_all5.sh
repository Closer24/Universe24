#!/bin/sh
PY=/home/user/Universe24/venv314/bin/python
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/bb1
D=$W/tools/derivations/bb1
cd $D
export TMPDIR=/dev/shm/tmp PYTHONPATH=$W/src
$PY bb_run.py worlds/hole5_300.json out/hole5_300 back 10 sym > out/hole5_300.log 2>&1
$PY bb_run.py worlds/one5_300.json out/one5_300 back 10 sym > out/one5_300.log 2>&1
$PY bb_run.py worlds/chiral5_300.json out/chiral5_300 back 10 > out/chiral5_300.log 2>&1
