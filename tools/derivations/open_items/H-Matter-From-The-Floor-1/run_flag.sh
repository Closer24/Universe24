#!/bin/bash
export TMPDIR=/dev/shm/tmp
cd /dev/shm/tmp/mf1
date -u > flag.log
nice -n 19 /home/user/Universe24/venv314/bin/python /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/kit/make_flagged_copy.py mf1 MF1_FOLD /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/tools/derivations/open_items/H-Matter-From-The-Floor-1/replacements_mf1.json src /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/src python /home/user/Universe24/venv314/bin/python > make_flagged.stdout 2>&1
date -u >> flag.log
echo MADE >> flag.log
export PYTHONPATH=/dev/shm/tmp/mf1/src_mf1
MF1_DRAW_LOG=1 nice -n 19 /home/user/Universe24/venv314/bin/python -m event_universe.run world_ga2_450.json ga2_450_drawlog.json back 20 > ga2_450_drawlog.stdout 2>&1
MF1_DRAW_LOG=1 nice -n 19 /home/user/Universe24/venv314/bin/python -m event_universe.run /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/tests/worlds/world_nature.json chiral_60_drawlog.json back 20 > chiral_60_drawlog.stdout 2>&1
MF1_DRAW_LOG=1 nice -n 19 /home/user/Universe24/venv314/bin/python -m event_universe.run /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/tests/worlds/world_hole.json hole_60_drawlog.json back 20 > hole_60_drawlog.stdout 2>&1
date -u >> flag.log
MF1_FOLD=1 nice -n 19 /home/user/Universe24/venv314/bin/python -m event_universe.run world_ga2_450.json ga2_450_fold.json back 20 > ga2_450_fold.stdout 2>&1
MF1_FOLD=1 nice -n 19 /home/user/Universe24/venv314/bin/python -m event_universe.run /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/tests/worlds/world_nature.json chiral_60_fold.json back 20 > chiral_60_fold.stdout 2>&1
MF1_FOLD=1 nice -n 19 /home/user/Universe24/venv314/bin/python -m event_universe.run /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/tests/worlds/world_hole.json hole_60_fold.json back 20 > hole_60_fold.stdout 2>&1
date -u >> flag.log
export PYTHONPATH=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/src
nice -n 19 /home/user/Universe24/venv314/bin/python -m event_universe.run world_ga2_450_mirror1.json ga2_450_mirror1.json back 20 > ga2_450_mirror1.stdout 2>&1
nice -n 19 /home/user/Universe24/venv314/bin/python -m event_universe.run world_ga2_450_cz3.json ga2_450_cz3.json back 20 > ga2_450_cz3.stdout 2>&1
nice -n 19 /home/user/Universe24/venv314/bin/python -m event_universe.run world_nature_mirrorx.json chiral_60_mirrorx.json back 20 > chiral_60_mirrorx.stdout 2>&1
date -u >> flag.log
echo DONE >> flag.log
