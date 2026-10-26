#!/bin/sh
# bb1: the records, each its own command (no loop); PY, W set by the caller
PY=/home/user/Universe24/venv314/bin/python
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/bb1
D=$W/tools/derivations/bb1
cd $D
export TMPDIR=/dev/shm/tmp PYTHONPATH=$W/src
$PY bb_run.py worlds/sea3_400.json out/sea3_400 back 10 sym > out/sea3_400.log 2>&1
$PY bb_run.py worlds/sea5_400.json out/sea5_400 back 10 sym > out/sea5_400.log 2>&1
$PY bb_run.py worlds/hole3_300.json out/hole3_300 back 10 sym > out/hole3_300.log 2>&1
$PY bb_run.py worlds/one3_300.json out/one3_300 back 10 sym > out/one3_300.log 2>&1
$PY bb_run.py worlds/sea3_300.json out/pulse3_6 back 10 sym pulse 6 > out/pulse3_6.log 2>&1
$PY bb_run.py worlds/sea3_300.json out/pulse3_24 back 10 sym pulse 24 > out/pulse3_24.log 2>&1
$PY bb_run.py worlds/sea3_300.json out/pulse3_94 back 10 sym pulse 94 > out/pulse3_94.log 2>&1
$PY bb_run.py worlds/sea3_300.json out/wave3_24 back 10 sym wave 24 > out/wave3_24.log 2>&1
$PY bb_run.py worlds/sea3_300.json out/wave3_96 back 10 sym wave 96 > out/wave3_96.log 2>&1
