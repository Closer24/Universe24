#!/bin/sh
# lr1: the seven cached records of the head re-run on the flagged copy (LR1_PICK=1 LR1_LAY=1), compared key by key with the cache; the uniform boards expected bit for bit.
cd /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/lr1/tools/derivations/open_items/H-Lay-Rest-Mirror-1
for spec in world_pair_3:400 world_plasma_3:170 world_universe:400 world_hole:60 world_chiral:60 world_bodies:300; do
  w=${spec%%:*}; n=${spec##*:}
  LR1_PICK=1 LR1_LAY=1 TMPDIR=/dev/shm/tmp nice -n 19 /home/user/Universe24/venv314/bin/python /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/lr1/tools/derivations/open_items/H-48-In-The-Clicks-3/run_record.py /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/lr1/tools/derivations/open_items/H-Lay-Rest-Mirror-1/src_lr1 /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/lr1/tests/worlds/$w.json $n 10 /dev/shm/tmp/lr1_$w.json /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/records/2ab32b518/${w}_$n.json > out/record_${w}_$n.log 2>&1
done
echo done > out/records.done
