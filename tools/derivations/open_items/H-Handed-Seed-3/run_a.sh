#!/bin/sh
# cs3: the first set of records, 400 intervals, run back 10 (every command written out, no loop)
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
cd $S/hands/cs3/tools/derivations/cs3
export PYTHONPATH=$S/hands/cs3/src TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
nice -n 19 $PY cs_run.py worlds/empty4_c5_400.json out/z_c5_400.json worlds/zigzag_m.json back 10 > out/z_c5_400.log 2>&1 &
nice -n 19 $PY cs_run.py worlds/empty4_c14_400.json out/z_c14_400.json worlds/zigzag_m.json back 10 > out/z_c14_400.log 2>&1 &
nice -n 19 $PY cs_run.py worlds/empty4_400.json out/cyc_q1_400.json worlds/cycle_m.json back 10 > out/cyc_q1_400.log 2>&1 &
nice -n 19 $PY cs_run.py worlds/empty4_400.json out/cyc_q2_400.json worlds/cycle_m2.json back 10 > out/cyc_q2_400.log 2>&1 &
wait
nice -n 19 $PY cs_run.py worlds/empty4_400.json out/cyc_q3_400.json worlds/cycle_m3.json back 10 > out/cyc_q3_400.log 2>&1 &
nice -n 19 $PY cs_run.py worlds/empty4_c14_400.json out/cyc_c14_q1_400.json worlds/cycle_m.json back 10 > out/cyc_c14_q1_400.log 2>&1 &
nice -n 19 $PY cs_run.py worlds/empty4_c14_400.json out/cyc_c14_q2_400.json worlds/cycle_m2.json back 10 > out/cyc_c14_q2_400.log 2>&1 &
nice -n 19 $PY cs_run.py worlds/empty4_171.json out/s2_171.json worlds/s2_dump.json > out/s2_171.log 2>&1 &
wait
echo done > out/run_a.done
