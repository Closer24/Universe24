#!/bin/bash
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
H=$S/hands/vf16/tools/derivations/open_items/H-Confirm-Build-16
export PYTHONPATH=$S/hands/vf16/src TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
R=$S/records/50c73c972
one() { # name worldfile back
  local t0=$(date +%s)
  nice -n 19 $PY -m event_universe.run $H/worlds/$2 $R/$1.json back $3 > $H/logs/$1.out 2>&1; echo "$1 exit $? $(( $(date +%s) - t0 )) s" >> $H/logs/times.txt
}
export -f one; export S H PY R PYTHONPATH TMPDIR
printf '%s\n' "world_bodies_300 world_bodies.json 20" "world_universe_400 world_universe.json 10" "world_ga2_450 world_ga2_450.json 10" "world_chiral_60 world_chiral.json 20" "world_hole_60 world_hole.json 20" "world_pair_3_400 world_pair_3.json 10" "world_plasma_3_170 world_plasma_3_170.json 10" | xargs -P 4 -L 1 bash -c 'one $0 $1 $2'
echo ALL_DONE >> $H/logs/times.txt
