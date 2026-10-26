#!/bin/bash
export PYTHONPATH=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/src TMPDIR=/dev/shm/tmp
cd /dev/shm/tmp/mf1
/home/user/Universe24/venv314/bin/python /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/tools/derivations/open_items/H-Matter-From-The-Floor-1/wait_file.py /dev/shm/tmp/mf1/flag.log DONE
/home/user/Universe24/venv314/bin/python /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/kit/wait_load.py 3
date -u > parity.log
nice -n 19 /home/user/Universe24/venv314/bin/python /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/tools/derivations/open_items/H-Matter-From-The-Floor-1/parity_mf1.py /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/tests/worlds/world_hole.json 60 C pr_hole_60_C.json > pr_hole_60_C.stdout 2>&1
nice -n 19 /home/user/Universe24/venv314/bin/python /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/tools/derivations/open_items/H-Matter-From-The-Floor-1/parity_mf1.py /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/tests/worlds/world_hole.json 60 P pr_hole_60_P.json > pr_hole_60_P.stdout 2>&1
nice -n 19 /home/user/Universe24/venv314/bin/python /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/tools/derivations/open_items/H-Matter-From-The-Floor-1/parity_mf1.py /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/tests/worlds/world_hole.json 60 CP pr_hole_60_CP.json > pr_hole_60_CP.stdout 2>&1
date -u >> parity.log
nice -n 19 /home/user/Universe24/venv314/bin/python /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/tools/derivations/open_items/H-Matter-From-The-Floor-1/parity_mf1.py /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/tests/worlds/world_nature.json 60 C pr_chiral_60_C.json > pr_chiral_60_C.stdout 2>&1
nice -n 19 /home/user/Universe24/venv314/bin/python /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/tools/derivations/open_items/H-Matter-From-The-Floor-1/parity_mf1.py /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/tests/worlds/world_nature.json 60 P pr_chiral_60_P.json > pr_chiral_60_P.stdout 2>&1
nice -n 19 /home/user/Universe24/venv314/bin/python /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/tools/derivations/open_items/H-Matter-From-The-Floor-1/parity_mf1.py /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/tests/worlds/world_nature.json 60 CP pr_chiral_60_CP.json > pr_chiral_60_CP.stdout 2>&1
date -u >> parity.log
nice -n 19 /home/user/Universe24/venv314/bin/python /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/tools/derivations/open_items/H-Matter-From-The-Floor-1/parity_mf1.py world_ga2_450.json 450 CP pr_ga2_450_CP.json > pr_ga2_450_CP.stdout 2>&1
nice -n 19 /home/user/Universe24/venv314/bin/python /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/tools/derivations/open_items/H-Matter-From-The-Floor-1/parity_mf1.py world_ga2_450.json 450 C pr_ga2_450_C.json > pr_ga2_450_C.stdout 2>&1
nice -n 19 /home/user/Universe24/venv314/bin/python /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/tools/derivations/open_items/H-Matter-From-The-Floor-1/parity_mf1.py world_ga2_450.json 450 P pr_ga2_450_P.json > pr_ga2_450_P.stdout 2>&1
date -u >> parity.log
echo PARITY_DONE >> parity.log
export PYTHONPATH=/dev/shm/tmp/mf1/src_mf1
MF1_FOLD=1 nice -n 19 /home/user/Universe24/venv314/bin/python /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/tools/derivations/open_items/H-Matter-From-The-Floor-1/parity_mf1.py /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/tests/worlds/world_nature.json 60 CP pr_chiral_60_CP_fold.json > pr_chiral_60_CP_fold.stdout 2>&1
MF1_FOLD=1 nice -n 19 /home/user/Universe24/venv314/bin/python /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/tools/derivations/open_items/H-Matter-From-The-Floor-1/parity_mf1.py /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/tests/worlds/world_nature.json 60 P pr_chiral_60_P_fold.json > pr_chiral_60_P_fold.stdout 2>&1
MF1_FOLD=1 nice -n 19 /home/user/Universe24/venv314/bin/python /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/tools/derivations/open_items/H-Matter-From-The-Floor-1/parity_mf1.py world_ga2_450.json 450 CP pr_ga2_450_CP_fold.json > pr_ga2_450_CP_fold.stdout 2>&1
date -u >> parity.log
echo FOLD_PARITY_DONE >> parity.log
/home/user/Universe24/venv314/bin/python /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/kit/wait_load.py 3
/home/user/Universe24/venv314/bin/python - <<'PY'
import json
w=json.load(open('/dev/shm/tmp/mf1/world_nature.json')) if False else None
PY
MF1_FOLD=1 nice -n 19 /home/user/Universe24/venv314/bin/python /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/kit/clicks_48.py /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/tests/worlds/world_nature.json 60 c48_chiral_60_cube3_fold.json cube 3 > c48_chiral_60_cube3_fold.stdout 2>&1
date -u >> parity.log
echo C48_DONE >> parity.log
