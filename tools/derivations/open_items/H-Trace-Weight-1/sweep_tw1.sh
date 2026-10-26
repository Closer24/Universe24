#!/bin/sh
# tw1's sweep: every candidate weight on the five records, four at a time, nice 19; one summary line per run under runs/.
cd /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/tw1
export TMPDIR=/dev/shm/tmp PYTHONPATH=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/tw1/tools/derivations/open_items/H-Trace-Weight-1/src_tw1
for W in 3 6 12 18 27 36 48 54 60 72 108; do
  echo "$W world_hole.json 60 hole60"
  echo "$W world_chiral.json 60 chiral60"
  echo "$W world_sea_3.json 240 sea240"
  echo "$W world_plasma_3.json 170 plasma170"
  echo "$W world_universe.json 400 universe400"
done | xargs -P 4 -L 1 sh -c 'TW1_TRACE=$0 nice -n 19 /home/user/Universe24/venv314/bin/python /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/tw1/tools/derivations/open_items/H-Trace-Weight-1/run_tw1.py tests/worlds/$1 $2 10 $3_w$0 > /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/tw1/tools/derivations/open_items/H-Trace-Weight-1/runs/$3_w$0.out 2>&1'
echo SWEEP DONE
