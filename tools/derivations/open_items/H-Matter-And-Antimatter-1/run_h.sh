#!/bin/sh
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
D=$S/hands/ma1/tools/derivations/ma1
PY=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp
export PYTHONPATH=$S/hands/ma1/src
cd $D
nice -n 19 $PY ma_run.py worlds/h3_400.json out/h3_400 back 10 every 50 > out/h3_400.log 2>&1
nice -n 19 $PY ma_run.py worlds/l3_400.json out/l3_400 back 10 every 50 > out/l3_400.log 2>&1
nice -n 19 $PY ma_run.py worlds/h5_400.json out/h5_400 back 10 every 100 > out/h5_400.log 2>&1
echo DONE > out/run_h.done
