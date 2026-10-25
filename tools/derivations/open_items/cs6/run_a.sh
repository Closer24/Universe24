#!/bin/sh
# cs6 batch A, B, C (no loop): four jobs at a time, nice 19
D=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/cs6/tools/derivations/cs6
cd $D
export TMPDIR=/dev/shm/tmp
export PYTHONPATH=$D/src_cs6:$D
PY=/home/user/Universe24/venv314/bin/python
F="CS4_TAKE_FARTHEST=1 CS4_LIGHT_NO_BODY=1"
env $F CS6_SL_S3=1 nice -n 19 $PY cs6_run.py worlds/empty4_hh3_800.json out/hh3_letter_sls3_800.json worlds/cycle_m5_m0.json back 10 > out/hh3_letter_sls3_800.log 2>&1 &
env $F CS6_LIGHT_ON_LIGHT=1 nice -n 19 $PY cs6_run.py worlds/empty4_hh3_800.json out/hh3_letter_lol_800.json worlds/cycle_m5_m0.json back 10 > out/hh3_letter_lol_800.log 2>&1 &
env $F CS4_NO_BIRTH=1 nice -n 19 $PY cs6_run.py worlds/empty4_hh3_400.json out/twinA_q5_400.json worlds/twinA_q5.json back 10 > out/twinA_q5_400.log 2>&1 &
env $F CS4_NO_BIRTH=1 nice -n 19 $PY cs6_run.py worlds/empty4_hh3_400.json out/twinB_q5_400.json worlds/twinB_q5.json back 10 > out/twinB_q5_400.log 2>&1 &
wait
echo done > out/run_a.done
nice -n 19 $PY cs6_run.py worlds/empty4_toy_400_sea.json out/seaB_toy_400.json worlds/seaB_toy.json back 10 > out/seaB_toy_400.log 2>&1 &
env $F nice -n 19 $PY cs6_run.py worlds/empty4_hh3_400_sea.json out/seaB_hh3_400.json worlds/seaB_hh3.json back 10 > out/seaB_hh3_400.log 2>&1 &
env $F CS5_BIRTHS_UNTIL=2 nice -n 19 $PY cs6_run.py worlds/empty4_hh3_400_sea.json out/hh3_sea_until2_400.json worlds/cycle_m5_m0.json back 10 > out/hh3_sea_until2_400.log 2>&1 &
env $F CS4_NO_BIRTH=1 nice -n 19 $PY cs6_run.py worlds/empty4_hh3_400.json out/twinA_q3_400.json worlds/twinA_q3.json back 10 > out/twinA_q3_400.log 2>&1 &
wait
echo done > out/run_b.done
env $F nice -n 19 $PY cs6_run.py worlds/empty4_hh3_240.json out/sv_hh3_m0_sm_240.json worlds/cycle_m5_m0_sm.json > out/sv_hh3_m0_sm_240.log 2>&1 &
env $F nice -n 19 $PY cs6_run.py worlds/empty4_hh3_240.json out/sv_hh3_m0_cz3_240.json worlds/cycle_m5_m0_cz3.json > out/sv_hh3_m0_cz3_240.log 2>&1 &
env $F nice -n 19 $PY cs6_run.py worlds/empty4_hh3_240.json out/sv_hh3_m0_q6_240.json worlds/cycle_m6_m0.json > out/sv_hh3_m0_q6_240.log 2>&1 &
env $F nice -n 19 $PY cs6_run.py worlds/empty4_hh3_240.json out/sv_hh3_m0_q8_240.json worlds/cycle_m8_m0.json > out/sv_hh3_m0_q8_240.log 2>&1 &
wait
env $F nice -n 19 $PY cs6_run.py worlds/empty4_hh3_240.json out/sv_hh3_m0_q6sm_240.json worlds/cycle_m6_m0_sm.json > out/sv_hh3_m0_q6sm_240.log 2>&1 &
env $F nice -n 19 $PY cs6_run.py worlds/empty4_hh3_240.json out/sv_hh3_m0_q8sm_240.json worlds/cycle_m8_m0_sm.json > out/sv_hh3_m0_q8sm_240.log 2>&1 &
env $F nice -n 19 $PY cs6_run.py worlds/empty4_ht6_240.json out/sv_ht6_m0_240.json worlds/cycle_m5_m0.json > out/sv_ht6_m0_240.log 2>&1 &
env $F nice -n 19 $PY cs6_run.py worlds/empty4_hh6_240.json out/sv_hh6_m0_240.json worlds/cycle_m5_m0.json > out/sv_hh6_m0_240.log 2>&1 &
wait
env $F nice -n 19 $PY cs6_run.py worlds/empty4_hh8_240.json out/sv_hh8_m0_240.json worlds/cycle_m5_m0.json > out/sv_hh8_m0_240.log 2>&1 &
env $F nice -n 19 $PY cs6_run.py worlds/empty4_hh8_240.json out/sv_hh8_m1_240.json worlds/cycle_m5.json > out/sv_hh8_m1_240.log 2>&1 &
env $F nice -n 19 $PY cs6_run.py worlds/empty4_hh7_240.json out/sv_hh7_m1_240.json worlds/cycle_m5.json > out/sv_hh7_m1_240.log 2>&1 &
env $F nice -n 19 $PY cs6_run.py worlds/empty4_ht8_240.json out/sv_ht8_m1_240.json worlds/cycle_m5.json > out/sv_ht8_m1_240.log 2>&1 &
wait
env $F nice -n 19 $PY cs6_run.py worlds/empty4_hh4_240.json out/sv_hh4_m1_240.json worlds/cycle_m5.json > out/sv_hh4_m1_240.log 2>&1 &
wait
echo done > out/run_c.done
