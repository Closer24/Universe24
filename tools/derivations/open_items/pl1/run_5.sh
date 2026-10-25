#!/bin/sh
D=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/pl1/tools/derivations/pl1
P=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp
cd $D
PYTHONPATH=$D/src_pl1 EQ2_CLICK=a nice -n 19 $P pl1_run.py worlds/h5.json out/a_h5.json back 10 > out/a_h5.log 2>&1 &
PYTHONPATH=$D/src_pl1 EQ2_CLICK=a PL1_SIGN=sym nice -n 19 $P pl1_run.py worlds/h5.json out/a_sym_h5.json back 10 > out/a_sym_h5.log 2>&1 &
PYTHONPATH=$D/src_pl1 EQ2_CLICK=a nice -n 19 $P pl1_run.py worlds/n5.json out/a_n5.json back 10 > out/a_n5.log 2>&1 &
PYTHONPATH=$D/src_pl1 EQ2_CLICK=b nice -n 19 $P pl1_run.py worlds/n5.json out/b_n5.json back 10 > out/b_n5.log 2>&1 &
wait
echo RUN5_DONE
