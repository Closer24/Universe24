#!/bin/sh
# cs2: the five records of 400, back 10 (every command written out, no loop)
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
cd $S/hands/cs2/tools/derivations/cs2
export PYTHONPATH=$S/hands/cs2/src TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
nice -n 19 $PY cs_run.py worlds/sea4_400.json out/s1_400.json back 10 screw 00111320 111 20 complex > out/s1_400.log 2>&1 &
nice -n 19 $PY cs_run.py worlds/sea4_400.json out/s1r_400.json back 10 screw 00111320 111 20 > out/s1r_400.log 2>&1 &
nice -n 19 $PY cs_run.py worlds/sea4_400.json out/s1a10_400.json back 10 screw 00111320 111 10 complex > out/s1a10_400.log 2>&1 &
nice -n 19 $PY cs_run.py worlds/empty4_400.json out/s2_400.json back 10 screw 00111320 111 189 complex > out/s2_400.log 2>&1 &
nice -n 19 $PY cs_run.py worlds/sea4_400.json out/prod_400.json back 10 screw 01101001 111 20 complex > out/prod_400.log 2>&1 &
wait
echo done > out/run_main.done
