#!/bin/sh
# cs5: the one-plane file under the crowd lifted (no loop): the heaviest point alone, the mirror 0 (every class draws alike)
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
cd $S/hands/cs5/tools/derivations/cs5
export TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
COPYD=$S/hands/cs5/tools/derivations/cs5/src_cs5d
CS5_CROWD_OFF=1 CS4_TAKE_FARTHEST=1 CS4_LIGHT_NO_BODY=1 PYTHONPATH=$COPYD nice -n 19 $PY cs5_run.py worlds/empty4_p00_400.json out/p00_q5_m0_crowdoff_400.json worlds/cycle_m5_m0.json back 10 > out/p00_q5_m0_crowdoff_400.log 2>&1 &
CS5_CROWD_OFF=1 CS4_TAKE_FARTHEST=1 CS4_LIGHT_NO_BODY=1 PYTHONPATH=$COPYD nice -n 19 $PY cs5_run.py worlds/empty4_p05_400.json out/p05_q5_m0_crowdoff_400.json worlds/cycle_m5_m0.json back 10 > out/p05_q5_m0_crowdoff_400.log 2>&1 &
wait
$PY shrink2.py out/p00_q5_m0_crowdoff_400.json out/p05_q5_m0_crowdoff_400.json >> out/shrink2.txt 2>&1
echo done > out/run_h.done
