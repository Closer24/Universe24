#!/bin/sh
# cs6 batch D (no loop): the no-credit controls, then the count survey of the circle's other pairs
D=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/cs6/tools/derivations/cs6
cd $D
export TMPDIR=/dev/shm/tmp
export PYTHONPATH=$D/src_cs6b:$D
PY=/home/user/Universe24/venv314/bin/python
F="CS4_TAKE_FARTHEST=1 CS4_LIGHT_NO_BODY=1 CS6_NO_CREDIT=1"
env $F CS4_NO_BIRTH=1 nice -n 19 $PY cs6_run.py worlds/empty4_hh3_400.json out/twinA_q5_nocredit_400.json worlds/twinA_q5.json back 10 > out/twinA_q5_nocredit_400.log 2>&1 &
env $F CS5_BIRTHS_UNTIL=2 nice -n 19 $PY cs6_run.py worlds/empty4_hh3_400.json out/hh3_until2_nocredit_400.json worlds/cycle_m5_m0.json back 10 > out/hh3_until2_nocredit_400.log 2>&1 &
env $F CS4_NO_BIRTH=1 nice -n 19 $PY cs6_run.py worlds/empty4_hh3_400.json out/twinB_q5_nocredit_400.json worlds/twinB_q5.json back 10 > out/twinB_q5_nocredit_400.log 2>&1 &
env $F nice -n 19 $PY cs6_run.py worlds/empty4_hh3_400_sea.json out/seaB_hh3_nocredit_400.json worlds/seaB_hh3.json back 10 > out/seaB_hh3_nocredit_400.log 2>&1 &
wait
echo done > out/run_d.done
nice -n 19 $PY survey.py out/survey 4 ga gl gm gb > out/survey_a.txt 2>&1
echo done > out/run_e.done
