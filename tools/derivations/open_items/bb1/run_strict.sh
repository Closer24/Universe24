#!/bin/sh
PY=/home/user/Universe24/venv314/bin/python
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/bb1
D=$W/tools/derivations/bb1
cd $D
export TMPDIR=/dev/shm/tmp BB1_SRC=$D/engine_bb1
$PY bb_run.py worlds/sea3_300.json out/pulse3_6_copyoff back 10 sym pulse 6 > out/pulse3_6_copyoff.log 2>&1
BB1_STRICT=1 $PY bb_run.py worlds/sea3_300.json out/pulse3_6_strict back 10 sym pulse 6 > out/pulse3_6_strict.log 2>&1
BB1_STRICT=1 $PY bb_run.py worlds/sea3_400.json out/sea3_400_strict back 10 sym > out/sea3_400_strict.log 2>&1
BB1_STRICT=1 $PY bb_run.py worlds/sea5_300.json out/pulse5_12_strict back 10 sym pulse 12 > out/pulse5_12_strict.log 2>&1
BB1_STRICT=1 $PY bb_run.py worlds/chiral5_300.json out/chiral5_300_strict back 10 > out/chiral5_300_strict.log 2>&1
