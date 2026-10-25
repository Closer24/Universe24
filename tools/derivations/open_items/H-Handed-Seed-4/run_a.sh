#!/bin/sh
# cs4: the first set (no loop): the control, P1, P2, P3, P4 (l3), P5
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
cd $S/hands/cs4/tools/derivations/cs4
export TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
HEAD=$S/hands/cs4/src
COPY=$S/hands/cs4/tools/derivations/cs4/src_cs4
PYTHONPATH=$HEAD nice -n 19 $PY cs4_run.py worlds/empty4_l3_50.json out/ctl_head_50.json worlds/cycle_m2.json > out/ctl_head_50.log 2>&1 &
PYTHONPATH=$COPY nice -n 19 $PY cs4_run.py worlds/empty4_l3_50.json out/ctl_copy_50.json worlds/cycle_m2.json > out/ctl_copy_50.log 2>&1 &
PYTHONPATH=$HEAD nice -n 19 $PY cs4_run.py worlds/empty4_lift_400.json out/lift_q1_400.json worlds/cycle_m.json back 10 > out/lift_q1_400.log 2>&1 &
PYTHONPATH=$HEAD nice -n 19 $PY cs4_run.py worlds/empty4_l4_400.json out/l4_q1_400.json worlds/cycle_m.json back 10 > out/l4_q1_400.log 2>&1 &
PYTHONPATH=$HEAD nice -n 19 $PY cs4_run.py worlds/empty4_l3_400.json out/l3_q2_400.json worlds/cycle_m2.json back 10 > out/l3_q2_400.log 2>&1 &
CS4_LIGHT_NO_BODY=1 PYTHONPATH=$COPY nice -n 19 $PY cs4_run.py worlds/empty4_l3_400.json out/l3_q2_nb_400.json worlds/cycle_m2.json back 10 > out/l3_q2_nb_400.log 2>&1 &
CK1_CROSS=1 PYTHONPATH=$COPY nice -n 19 $PY cs4_run.py worlds/empty4_l3_400.json out/l3_q2_cross_400.json worlds/cycle_m2.json back 10 > out/l3_q2_cross_400.log 2>&1 &
CS4_LIGHT_NO_BODY=1 PYTHONPATH=$COPY nice -n 19 $PY cs4_run.py worlds/empty4_l4_400.json out/l4_q2_nb_400.json worlds/cycle_m2.json back 10 > out/l4_q2_nb_400.log 2>&1 &
wait
echo done > out/run_a.done
