#!/bin/bash
# runs each cut world to its record and its reading, timing each
cd /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/pg1; export PYTHONPATH=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/pg1/src TMPDIR=/dev/shm/tmp
for w in hole_60 plasma_3_170 packet_6 universe_6; do
  s=$(date +%s)
  nice -n 19 /home/user/Universe24/venv314/bin/python -m event_universe.run /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/pg1/tools/derivations/open_items/H-Confirm-Page-1/worlds/$w.json /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/pg1/tools/derivations/open_items/H-Confirm-Page-1/out/$w.json > /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/pg1/tools/derivations/open_items/H-Confirm-Page-1/out/$w.run.log 2>&1; echo "record $w exit=$? seconds=$(( $(date +%s) - s ))"
  nice -n 19 /home/user/Universe24/venv314/bin/python -m event_universe.gates /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/pg1/tools/derivations/open_items/H-Confirm-Page-1/out/$w.json > /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/pg1/tools/derivations/open_items/H-Confirm-Page-1/out/$w.reading.jsonl 2> /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/pg1/tools/derivations/open_items/H-Confirm-Page-1/out/$w.gates.err; echo "reading $w exit=$?"
done
