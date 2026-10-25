#!/bin/sh
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
D=$S/hands/ma1/tools/derivations/ma1
PY=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp
export PYTHONPATH=$S/hands/ma1/src
cd $D
nice -n 19 $PY ma_run.py worlds/b4_nosea_400.json out/b4_nosea_400 back 10 every 50 > out/b4_nosea_400.log 2>&1
nice -n 19 $PY ma_run.py worlds/s4_nosea_400.json out/s4_nosea_400 back 10 every 50 > out/s4_nosea_400.log 2>&1
nice -n 19 $PY ma_run.py worlds/b4_flip_nosea_400.json out/b4_flip_nosea_400 back 10 every 50 > out/b4_flip_nosea_400.log 2>&1
echo DONE > out/run_nosea.done
