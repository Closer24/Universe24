#!/bin/sh
# cs1: the main records, 400 intervals, run back 10 (no loop; every command written out)
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
cd $S/hands/cs1/tools/derivations/cs1
export PYTHONPATH=$S/hands/cs1/src TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
nice -n 19 $PY cs_run.py worlds/empty4_400.json out/h1m_400.json worlds/helix_m.json back 10 > out/h1m_400.log 2>&1 &
nice -n 19 $PY cs_run.py worlds/empty4_400.json out/h1p_400.json worlds/helix_p.json back 10 > out/h1p_400.log 2>&1 &
nice -n 19 $PY cs_run.py worlds/sea4_400.json out/h2m_400.json worlds/helix_m.json back 10 > out/h2m_400.log 2>&1 &
nice -n 19 $PY cs_run.py worlds/empty4_400.json out/t1m_400.json worlds/twisted_m.json back 10 > out/t1m_400.log 2>&1 &
nice -n 19 $PY cs_run.py worlds/sea4_400.json out/t2m_400.json worlds/twisted_m.json back 10 > out/t2m_400.log 2>&1 &
nice -n 19 $PY cs_run.py worlds/empty4_400.json out/t1m2_400.json worlds/twisted_m2.json back 10 > out/t1m2_400.log 2>&1 &
nice -n 19 $PY -m event_universe.run worlds/sea4_400.json out/sea4_400.json back 10 > out/sea4_400.log 2>&1 &
wait
echo done > out/run_main.done
