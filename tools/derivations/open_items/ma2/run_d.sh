#!/bin/sh
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
cd $S/hands/ma2/tools/derivations/ma2
export PYTHONPATH=$S/hands/ma2/src TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
nice -n 19 $PY ma_run.py worlds/sea4_400.json out/d4_400.json back 10 lays worlds/lay_d.json > out/d4_400.log 2>&1 &
nice -n 19 $PY ma_run.py worlds/sea3_400.json out/d3_400.json back 10 lays worlds/lay_d.json > out/d3_400.log 2>&1 &
nice -n 19 $PY ma_run.py worlds/sea4_400.json out/dh4_400.json back 10 lays worlds/lay_d_heavy_pair.json > out/dh4_400.log 2>&1 &
wait
echo done
