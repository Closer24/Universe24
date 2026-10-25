#!/bin/sh
D=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/cs6/tools/derivations/cs6
cd $D
export TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
PYTHONPATH=$D/src_cs6:$D CS4_TAKE_FARTHEST=1 CS4_LIGHT_NO_BODY=1 CS5_BIRTHS_UNTIL=2 nice -n 19 $PY cs6_run.py worlds/empty4_hh3_800.json out/hh3_until2_800.json worlds/cycle_m5_m0.json back 10 > out/hh3_until2_800.log 2>&1
PYTHONPATH=$D/src_cs6 nice -n 19 $PY -m event_universe.gates out/hh3_until2_800.json > out/hh3_until2_800_gates.jsonl 2>&1
PYTHONPATH=$D/src_cs6 nice -n 19 $PY -m event_universe.gates out/hh3_letter_lol_800.json > out/hh3_letter_lol_800_gates.jsonl 2>&1
echo done > out/run_f.done
