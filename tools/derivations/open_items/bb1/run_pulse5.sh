#!/bin/sh
PY=/home/user/Universe24/venv314/bin/python
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/bb1
D=$W/tools/derivations/bb1
cd $D
export TMPDIR=/dev/shm/tmp PYTHONPATH=$W/src
$PY bb_run.py worlds/sea5_300.json out/pulse5_12 back 10 sym pulse 12 > out/pulse5_12.log 2>&1
$PY bb_run.py worlds/sea5_300.json out/pulse5_47 back 10 sym pulse 47 > out/pulse5_47.log 2>&1
$PY bb_run.py worlds/sea5_300.json out/pulse5_94 back 10 sym pulse 94 > out/pulse5_94.log 2>&1
