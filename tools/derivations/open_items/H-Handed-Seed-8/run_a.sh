#!/bin/sh
# cs8 batch A (no loop): the control, then the merger at rest on ga2 to 800 under four lay readings, in parallel at nice 19
D=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/cs8/tools/derivations/cs8
cd $D
export TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
$PY check_flag_absent.py > out/check_flag_absent.txt 2>&1
export PYTHONPATH=$D/src_cs8:$D
F="CS4_TAKE_FARTHEST=1 CS7_EQ=n CS8_REST=1"
env $F CS6_LIGHT_ON_LIGHT=1 nice -n 19 $PY cs6_run.py worlds/empty4_ga2_800.json out/ga2_rest_lol_800.json worlds/cycle_m5_m0.json back 10 > out/ga2_rest_lol_800.log 2>&1 &
env $F CS6_LIGHT_ON_LIGHT=1 CS5_CROWD_OFF=1 nice -n 19 $PY cs6_run.py worlds/empty4_ga2_800.json out/ga2_rest_lol_nocrowd_800.json worlds/cycle_m5_m0.json back 10 > out/ga2_rest_lol_nocrowd_800.log 2>&1 &
env $F CS6_SL_S3=1 CS5_CROWD_OFF=1 nice -n 19 $PY cs6_run.py worlds/empty4_ga2_800.json out/ga2_rest_sls3_nocrowd_800.json worlds/cycle_m5_m0.json back 10 > out/ga2_rest_sls3_nocrowd_800.log 2>&1 &
env $F CS5_CROWD_OFF=1 nice -n 19 $PY cs6_run.py worlds/empty4_ga2_800.json out/ga2_rest_letter_nocrowd_800.json worlds/cycle_m5_m0.json back 10 > out/ga2_rest_letter_nocrowd_800.log 2>&1 &
wait
echo done > out/run_a.done
