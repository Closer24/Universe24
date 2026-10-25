#!/bin/sh
# mg1 batch A (no loop): ga2 to 450 under four readings in parallel at nice 19
D=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mg1/tools/derivations/mg1
cd $D
export TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
export PYTHONPATH=$D/src_mg1:$D
F="CS4_TAKE_FARTHEST=1 CS8_REST=1 CS8_MERGER_LAY=1 MG1_WALL=own"
env CS4_TAKE_FARTHEST=1 nice -n 19 $PY cs6_run.py worlds/empty4_ga2_450.json out/ga2_ctrl_450.json worlds/cycle_m5_m0.json back 10 > out/ga2_ctrl_450.log 2>&1 &
env $F nice -n 19 $PY cs6_run.py worlds/empty4_ga2_450.json out/ga2_own_450.json worlds/cycle_m5_m0.json back 10 > out/ga2_own_450.log 2>&1 &
env $F MG1_TAKE=two nice -n 19 $PY cs6_run.py worlds/empty4_ga2_450.json out/ga2_two_450.json worlds/cycle_m5_m0.json back 10 > out/ga2_two_450.log 2>&1 &
env $F MG1_TAKE=whole nice -n 19 $PY cs6_run.py worlds/empty4_ga2_450.json out/ga2_whole_450.json worlds/cycle_m5_m0.json back 10 > out/ga2_whole_450.log 2>&1 &
wait
echo done > out/run_a.done
