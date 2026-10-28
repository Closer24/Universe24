#!/bin/bash
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad; V=$S/derive/I_verify; PY=/home/user/Universe24/venv314/bin/python
cd $V/run
for w in hole nature; do
  for v in head fix1 fix2 fix12; do
    $PY -I i4x.py world_$w.json 60 $v > $V/i4_rerun/${w}_$v.txt 2>&1 &
  done
  wait
done
for w in hole nature; do for v in head fix12 fix1 fix2; do $PY -I i4_head.py world_$w.json 20 $v rewind > $V/i4_rerun/rewind_${w}_$v.txt 2>&1 & done; wait; done
echo done > $V/i4_rerun/DONE
