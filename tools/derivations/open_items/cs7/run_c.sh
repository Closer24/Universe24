#!/bin/sh
# cs7 batch C (no loop): the 2-row files to 800 under the net reading (T5 / P7)
D=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/cs7/tools/derivations/cs7
cd $D
export TMPDIR=/dev/shm/tmp
export PYTHONPATH=$D/src_cs7:$D
PY=/home/user/Universe24/venv314/bin/python
F="CS4_TAKE_FARTHEST=1 CS4_LIGHT_NO_BODY=1 CS7_EQ=n"
env $F nice -n 19 $PY cs6_run.py worlds/empty4_ga2_800.json out/ga2_n_800.json worlds/cycle_m5_m0.json back 10 > out/ga2_n_800.log 2>&1 &
env $F nice -n 19 $PY cs6_run.py worlds/empty4_gl2_800.json out/gl2_n_800.json worlds/cycle_m5_m0.json back 10 > out/gl2_n_800.log 2>&1 &
wait
echo done > out/run_c.done
