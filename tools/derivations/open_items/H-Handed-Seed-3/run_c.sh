#!/bin/sh
# cs3: the flagged copy's records (no loop)
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
cd $S/hands/cs3/tools/derivations/cs3
export TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
PYTHONPATH=$S/hands/cs3/tools/derivations/cs3/src_cs3 nice -n 19 $PY cs_run.py worlds/empty4_50_c14.json out/ctl_copy_50.json worlds/cycle_m2.json > out/ctl_copy_50.log 2>&1 &
PYTHONPATH=$S/hands/cs3/src nice -n 19 $PY cs_run.py worlds/empty4_50_c14.json out/ctl_head_50.json worlds/cycle_m2.json > out/ctl_head_50.log 2>&1 &
CK1_CROSS=1 PYTHONPATH=$S/hands/cs3/tools/derivations/cs3/src_cs3 nice -n 19 $PY cs_run.py worlds/empty4_c14_400.json out/cyc_c14_q2_cross_400.json worlds/cycle_m2.json back 10 > out/cyc_c14_q2_cross_400.log 2>&1 &
CK1_CROSS=1 PYTHONPATH=$S/hands/cs3/tools/derivations/cs3/src_cs3 nice -n 19 $PY cs_run.py worlds/empty4_400.json out/s2_cross_400.json worlds/s2_dump.json back 10 > out/s2_cross_400.log 2>&1 &
wait
echo done > out/run_c.done
