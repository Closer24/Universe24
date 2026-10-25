#!/bin/sh
# cs1: the zigzag records, 400 intervals, run back 10 (no loop)
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
cd $S/hands/cs1/tools/derivations/cs1
export PYTHONPATH=$S/hands/cs1/src TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
nice -n 19 $PY cs_run.py worlds/empty4_400.json out/z1m_400.json worlds/zigzag_m.json back 10 > out/z1m_400.log 2>&1 &
nice -n 19 $PY cs_run.py worlds/empty4_400.json out/z1m2_400.json worlds/zigzag_m2.json back 10 > out/z1m2_400.log 2>&1 &
wait
echo done > out/run_zigzag.done
