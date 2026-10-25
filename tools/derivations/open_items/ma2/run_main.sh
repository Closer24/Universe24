#!/bin/sh
# ma2: the main records, 400 intervals, run back 10 (no loop; every command written out)
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
cd $S/hands/ma2/tools/derivations/ma2
export PYTHONPATH=$S/hands/ma2/src TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
nice -n 19 $PY ma_run.py worlds/sea3_400.json out/sea3_400.json back 10 > out/sea3_400.log 2>&1 &
nice -n 19 $PY ma_run.py worlds/sea4_400.json out/sea4_400.json back 10 > out/sea4_400.log 2>&1 &
nice -n 19 $PY ma_run.py worlds/sea4_400.json out/a4_400.json back 10 lays worlds/lay_a.json > out/a4_400.log 2>&1 &
nice -n 19 $PY ma_run.py worlds/sea4_400.json out/b4_400.json back 10 lays worlds/lay_b.json > out/b4_400.log 2>&1 &
wait
nice -n 19 $PY ma_run.py worlds/sea4_400.json out/c4_400.json back 10 lays worlds/lay_c.json > out/c4_400.log 2>&1 &
nice -n 19 $PY ma_run.py worlds/sea4_400.json out/bx4_400.json back 10 lays worlds/lay_bx.json > out/bx4_400.log 2>&1 &
nice -n 19 $PY ma_run.py worlds/sea5_400.json out/sea5_400.json back 10 > out/sea5_400.log 2>&1 &
nice -n 19 $PY ma_run.py worlds/sea3_400.json out/a3_400.json back 10 lays worlds/lay_a.json > out/a3_400.log 2>&1 &
wait
echo done
