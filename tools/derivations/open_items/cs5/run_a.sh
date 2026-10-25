#!/bin/sh
# cs5: the control and the reproduction (no loop)
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
cd $S/hands/cs5/tools/derivations/cs5
export TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
HEAD=$S/hands/cs5/src
COPY=$S/hands/cs5/tools/derivations/cs5/src_cs5
PYTHONPATH=$HEAD nice -n 19 $PY cs5_run.py worlds/empty4_l3_50.json out/ctl_head_50.json worlds/cycle_m5.json > out/ctl_head_50.log 2>&1 &
PYTHONPATH=$COPY nice -n 19 $PY cs5_run.py worlds/empty4_l3_50.json out/ctl_copy_50.json worlds/cycle_m5.json > out/ctl_copy_50.log 2>&1 &
CS4_TAKE_FARTHEST=1 CS4_LIGHT_NO_BODY=1 PYTHONPATH=$COPY nice -n 19 $PY cs5_run.py worlds/empty4_l4_400.json out/l4_q5_nb_far_400.json worlds/cycle_m5.json back 10 > out/l4_q5_nb_far_400.log 2>&1 &
wait
echo done > out/run_a.done
