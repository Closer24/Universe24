#!/bin/sh
# cs7 batch A (no loop): the control (the head against src_cs7 unflagged, 6 intervals of hh3; the hole 3-cube at 20), then P2, P3, P4 in parallel at nice 19
D=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/cs7/tools/derivations/cs7
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/cs7
cd $D
export TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
env PYTHONPATH=$W/src:$D nice -n 19 $PY cs6_run.py worlds/empty4_hh3_6.json out/ctl_head_6.json worlds/cycle_m5_m0.json back 6 > out/ctl_head_6.log 2>&1 &
env PYTHONPATH=$D/src_cs7:$D nice -n 19 $PY cs6_run.py worlds/empty4_hh3_6.json out/ctl_copy_6.json worlds/cycle_m5_m0.json back 6 > out/ctl_copy_6.log 2>&1 &
wait
$PY compare.py out/ctl_head_6.json out/ctl_copy_6.json > out/ctl_compare.txt 2>&1
F="CS4_TAKE_FARTHEST=1 CS4_LIGHT_NO_BODY=1"
export PYTHONPATH=$D/src_cs7:$D
env $F CS7_EQ=b nice -n 19 $PY cs6_run.py worlds/empty4_hh3_800.json out/hh3_eq_b_800.json worlds/cycle_m5_m0.json back 10 > out/hh3_eq_b_800.log 2>&1 &
env $F CS7_EQ=n nice -n 19 $PY cs6_run.py worlds/empty4_hh3_800.json out/hh3_eq_n_800.json worlds/cycle_m5_m0.json back 10 > out/hh3_eq_n_800.log 2>&1 &
env $F CS7_EQ=c nice -n 19 $PY cs6_run.py worlds/empty4_hh3_800.json out/hh3_eq_c_800.json worlds/cycle_m5_m0.json back 10 > out/hh3_eq_c_800.log 2>&1 &
wait
echo done > out/run_a.done
