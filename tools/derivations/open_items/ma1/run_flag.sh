#!/bin/sh
# ma1's flagged runs: the copy engine_ma1 with the flag absent (bit for bit), MA1_ODD=1 (the odd rounding), MA1_ODD=2 (the odd floor)
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
D=$S/hands/ma1/tools/derivations/ma1
PY=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp
export PYTHONPATH=$D/engine_ma1
cd $D
nice -n 19 $PY ma_run.py worlds/b4_400.json out/flag0_b4_400 back 10 every 50 > out/flag0_b4_400.log 2>&1
MA1_ODD=1 nice -n 19 $PY ma_run.py worlds/b4_400.json out/odd1_b4_400 back 10 every 50 > out/odd1_b4_400.log 2>&1
MA1_ODD=2 nice -n 19 $PY ma_run.py worlds/b4_400.json out/odd2_b4_400 back 10 every 50 > out/odd2_b4_400.log 2>&1
MA1_ODD=2 nice -n 19 $PY ma_run.py worlds/b4_flip_400.json out/odd2_b4_flip_400 back 10 every 50 > out/odd2_b4_flip_400.log 2>&1
MA1_ODD=2 nice -n 19 $PY ma_run.py worlds/s4_400.json out/odd2_s4_400 back 10 every 50 > out/odd2_s4_400.log 2>&1
MA1_ODD=2 nice -n 19 $PY -m event_universe.run $S/hands/ma1/tests/worlds/world_chiral.json out/odd2_chiral60_record.json back 10 > out/odd2_chiral60.log 2>&1
nice -n 19 $PY -m event_universe.run $S/hands/ma1/tests/worlds/world_chiral.json out/flag0_chiral60_record.json back 10 > out/flag0_chiral60.log 2>&1
echo DONE > out/run_flag.done
