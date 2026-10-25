#!/bin/sh
D=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/cs6/tools/derivations/cs6
cd $D
export TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
F="CS4_TAKE_FARTHEST=1 CS4_LIGHT_NO_BODY=1"
cp worlds/empty4_ga2_400.json worlds/empty4_ga2_800.json; sed -i 's/"intervals": 400/"intervals": 800/' worlds/empty4_ga2_800.json
cp worlds/empty4_gl2_400.json worlds/empty4_gl2_800.json; sed -i 's/"intervals": 400/"intervals": 800/' worlds/empty4_gl2_800.json
env PYTHONPATH=$D/src_cs6:$D $F nice -n 19 $PY cs6_run.py worlds/empty4_ga2_800.json out/ga2_letter_800.json worlds/cycle_m5_m0.json back 10 > out/ga2_letter_800.log 2>&1 &
env PYTHONPATH=$D/src_cs6:$D $F nice -n 19 $PY cs6_run.py worlds/empty4_gl2_800.json out/gl2_letter_800.json worlds/cycle_m5_m0.json back 10 > out/gl2_letter_800.log 2>&1 &
env PYTHONPATH=$D/src_cs6b:$D $F CS6_NO_CREDIT=1 CS5_BIRTHS_UNTIL=2 nice -n 19 $PY cs6_run.py worlds/empty4_ga2_400.json out/ga2_until2_nocredit_400.json worlds/cycle_m5_m0.json back 10 > out/ga2_until2_nocredit_400.log 2>&1 &
env PYTHONPATH=$D/src_cs6b:$D $F CS6_NO_CREDIT=1 CS5_BIRTHS_UNTIL=2 nice -n 19 $PY cs6_run.py worlds/empty4_gl2_400.json out/gl2_until2_nocredit_400.json worlds/cycle_m5_m0.json back 10 > out/gl2_until2_nocredit_400.log 2>&1 &
wait
echo done > out/run_g.done
