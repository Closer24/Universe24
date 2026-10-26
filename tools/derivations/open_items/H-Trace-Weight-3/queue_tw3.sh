#!/bin/sh
# tw3's queue: every run four at a time at nice 19 on the flagged copy; one summary line per run under out/<tag>.out.
# Lines: <weight or 54 unflagged (-)> <src dir> <script> <world> <intervals> <back> <tag>
cd /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/tw3
export TMPDIR=/dev/shm/tmp
D=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/tw3/tools/derivations/open_items/H-Trace-Weight-3
export PY=/home/user/Universe24/venv314/bin/python
cat <<LIST | xargs -P 4 -L 1 sh -c 'cd /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/tw3; if [ "$0" = "-" ]; then unset TW3_TRACE; else export TW3_TRACE=$0; fi; export PYTHONPATH=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/tw3/tools/derivations/open_items/H-Trace-Weight-3/$1; S0=$(date +%s); if [ "$2" = "clicks" ]; then nice -n 19 $PY /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/tw3/tools/derivations/open_items/H-Trace-Weight-3/clicks_48_tw3.py tests/worlds/$3 $4 /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/tw3/tools/derivations/open_items/H-Trace-Weight-3/out/$6.json > /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/tw3/tools/derivations/open_items/H-Trace-Weight-3/out/$6.out 2>&1; else nice -n 19 $PY /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/tw3/tools/derivations/open_items/H-Trace-Weight-3/run_tw3.py tests/worlds/$3 $4 $5 $6 > /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/tw3/tools/derivations/open_items/H-Trace-Weight-3/out/$6.out 2>&1; fi; echo "$6 exit $? $(($(date +%s)-S0)) s" >> /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/tw3/tools/derivations/open_items/H-Trace-Weight-3/out/queue.log' 
54 src_tw3 run world_chiral.json 2400 10 world_chiral_2400_K54
18 src_tw3 run world_chiral.json 2400 10 world_chiral_2400_K18
6 src_tw3 run world_chiral.json 2400 10 world_chiral_2400_K6
6 src_tw3 clicks world_hole.json 60 - clicks48_hole60_K6
54 src_tw3 clicks world_hole.json 60 - clicks48_hole60_K54
54 src_tw3 run world_chiral.json 900 10 world_chiral_900_K54
18 src_tw3 run world_chiral.json 900 10 world_chiral_900_K18
6 src_tw3 run world_chiral.json 900 10 world_chiral_900_K6
54 src_tw3 run world_hole.json 900 10 world_hole_900_K54
18 src_tw3 run world_hole.json 900 10 world_hole_900_K18
6 src_tw3 run world_hole.json 900 10 world_hole_900_K6
54 src_tw3 run world_ga2.json 450 10 world_ga2_450_K54
18 src_tw3 run world_ga2.json 450 10 world_ga2_450_K18
6 src_tw3 run world_ga2.json 450 10 world_ga2_450_K6
54 src_tw3_rev run world_ga2.json 450 10 world_ga2_450_K54_revA48
18 src_tw3_rev run world_ga2.json 450 10 world_ga2_450_K18_revA48
6 src_tw3_rev run world_ga2.json 450 10 world_ga2_450_K6_revA48
54 src_tw3 run world_bodies.json 300 10 world_bodies_300_K54
18 src_tw3 run world_bodies.json 300 10 world_bodies_300_K18
6 src_tw3 run world_bodies.json 300 10 world_bodies_300_K6
6 src_tw3 run world_universe.json 400 10 world_universe_400_K6
LIST
echo QUEUE DONE >> /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/tw3/tools/derivations/open_items/H-Trace-Weight-3/out/queue.log
