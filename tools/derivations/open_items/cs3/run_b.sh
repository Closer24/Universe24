#!/bin/sh
# cs3: the second set (no loop)
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
cd $S/hands/cs3/tools/derivations/cs3
export PYTHONPATH=$S/hands/cs3/src TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
nice -n 19 $PY cs_run.py worlds/empty4_400.json out/s2t_400.json worlds/s2_turned.json back 10 > out/s2t_400.log 2>&1 &
nice -n 19 $PY cs_run.py worlds/empty4_c14_800.json out/cyc_c14_q1_800.json worlds/cycle_m.json back 10 > out/cyc_c14_q1_800.log 2>&1 &
nice -n 19 $PY -m event_universe.gates out/cyc_c14_q1_400.json > out/cyc_c14_q1_400_gates.jsonl 2>&1 &
nice -n 19 $PY -m event_universe.gates out/cyc_c14_q2_400.json > out/cyc_c14_q2_400_gates.jsonl 2>&1 &
wait
echo done > out/run_b.done
