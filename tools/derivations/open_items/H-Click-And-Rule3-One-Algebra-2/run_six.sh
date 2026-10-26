#!/bin/bash
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/ca2
F=$W/tools/derivations/open_items/H-Click-And-Rule3-One-Algebra-2
P=/home/user/Universe24/venv314/bin/python; export TMPDIR=/dev/shm/tmp; cd $F
C=/dev/shm/tmp/ca2/src_ca2
PYTHONPATH=$W/src $P run_flag_3cube.py $W/src world_hole.json 60 > out/flag_hole_head.txt
PYTHONPATH=$C $P run_flag_3cube.py $C world_hole.json 60 > out/flag_hole_off.txt
CA2_EVEN_LAY=1 PYTHONPATH=$C $P run_flag_3cube.py $C world_hole.json 60 > out/flag_hole_on.txt
PYTHONPATH=$W/src $P run_flag_3cube.py $W/src world_chiral.json 60 > out/flag_chiral_head.txt
PYTHONPATH=$C $P run_flag_3cube.py $C world_chiral.json 60 > out/flag_chiral_off.txt
CA2_EVEN_LAY=1 PYTHONPATH=$C $P run_flag_3cube.py $C world_chiral.json 60 > out/flag_chiral_on.txt
echo six done; date -u
