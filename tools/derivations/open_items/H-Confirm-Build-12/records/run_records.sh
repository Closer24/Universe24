#!/bin/sh
# vf12: the three records (hole 60, chiral 60, bodies 300, back 20 as the committed records carry) and world_pair_3 / world_universe at 400 (back 10) under David's build e1209f752 and under the parent 99a9ee860
R=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/vf12/tools/derivations/open_items/H-Confirm-Build-12/records
cd $R
export TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
for w in hole chiral bodies; do
  env PYTHONPATH=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/vf12/src nice -n 19 $PY -m event_universe.run world_$w.json ${w}_david.json back 20 > ${w}_david.log 2>&1 &
  env PYTHONPATH=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/vf12/tools/derivations/open_items/H-Confirm-Build-12/parent/src nice -n 19 $PY -m event_universe.run world_$w.json ${w}_parent.json back 20 > ${w}_parent.log 2>&1 &
done
for w in pair_3 universe; do
  env PYTHONPATH=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/vf12/src nice -n 19 $PY -m event_universe.run world_$w.json ${w}_david.json back 10 > ${w}_david.log 2>&1 &
  env PYTHONPATH=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/vf12/tools/derivations/open_items/H-Confirm-Build-12/parent/src nice -n 19 $PY -m event_universe.run world_$w.json ${w}_parent.json back 10 > ${w}_parent.log 2>&1 &
done
wait
echo done > run_records.done
