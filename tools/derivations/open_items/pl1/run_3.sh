#!/bin/sh
D=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/pl1/tools/derivations/pl1
P=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp
cd $D
PYTHONPATH=$D/../../../src nice -n 19 $P pl1_run.py worlds/h3.json out/base_h3.json back 10 > out/base_h3.log 2>&1 &
PYTHONPATH=$D/src_pl1 EQ2_CLICK=a nice -n 19 $P pl1_run.py worlds/h3.json out/a_h3.json back 10 > out/a_h3.log 2>&1 &
PYTHONPATH=$D/src_pl1 EQ2_CLICK=a PL1_SIGN=sym nice -n 19 $P pl1_run.py worlds/h3.json out/a_sym_h3.json back 10 > out/a_sym_h3.log 2>&1 &
PYTHONPATH=$D/src_pl1 EQ2_CLICK=a PL1_SIGN=none nice -n 19 $P pl1_run.py worlds/h3.json out/a_none_h3.json back 10 > out/a_none_h3.log 2>&1 &
wait
PYTHONPATH=$D/src_pl1 EQ2_CLICK=a PL1_SIGN=odd nice -n 19 $P pl1_run.py worlds/h3.json out/a_odd_h3.json back 10 > out/a_odd_h3.log 2>&1 &
PYTHONPATH=$D/src_pl1 EQ2_CLICK=a PL1_SIGN=pre nice -n 19 $P pl1_run.py worlds/h3.json out/a_pre_h3.json back 10 > out/a_pre_h3.log 2>&1 &
PYTHONPATH=$D/src_pl1 EQ2_CLICK=a nice -n 19 $P pl1_run.py worlds/n3.json out/a_n3.json back 10 > out/a_n3.log 2>&1 &
PYTHONPATH=$D/src_pl1 EQ2_CLICK=a nice -n 19 $P pl1_run.py worlds/dh3.json out/a_dh3.json back 10 > out/a_dh3.log 2>&1 &
wait
PYTHONPATH=$D/src_pl1 EQ2_CLICK=b PL1_SIGN=sym nice -n 19 $P pl1_run.py worlds/h3.json out/b_sym_h3.json back 10 > out/b_sym_h3.log 2>&1 &
PYTHONPATH=$D/src_pl1 EQ2_CLICK=b nice -n 19 $P pl1_run.py worlds/n3.json out/b_n3.json back 10 > out/b_n3.log 2>&1 &
wait
echo RUN3_DONE
