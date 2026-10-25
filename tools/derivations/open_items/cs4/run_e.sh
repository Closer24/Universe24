#!/bin/sh
# cs4: the mended take, the second form (no loop)
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
cd $S/hands/cs4/tools/derivations/cs4
export TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
COPYC=$S/hands/cs4/tools/derivations/cs4/src_cs4c
CS4_TAKE_FARTHEST=1 CS4_LIGHT_NO_BODY=1 PYTHONPATH=$COPYC nice -n 19 $PY cs4_run.py worlds/empty4_c14_400.json out/c14_q5_nb_far_400.json worlds/cycle_m5.json back 10 > out/c14_q5_nb_far_400.log 2>&1 &
CS4_TAKE_FARTHEST=1 CS4_LIGHT_NO_BODY=1 PYTHONPATH=$COPYC nice -n 19 $PY cs4_run.py worlds/empty4_l4_400.json out/l4_q5_nb_far_400.json worlds/cycle_m5.json back 10 > out/l4_q5_nb_far_400.log 2>&1 &
wait
echo done > out/run_e.done
