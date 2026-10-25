#!/bin/sh
F=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/fd2/tools/derivations/fd2
PY=/home/user/Universe24/venv314/bin/python
export PYTHONPATH=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/fd2/src
export TMPDIR=/dev/shm/tmp
cd $F
$PY fd2_compare2.py toy_r_odd toy_david/world_chiral.json > out/r_odd_chiral_60.json 2>&1
$PY fd2_compare2.py toy_r_imcomp toy_david/world_chiral.json > out/r_imcomp_chiral_60.json 2>&1
$PY fd2_compare2.py toy_r_imcomp worlds/world_hole_60.json > out/r_imcomp_hole_60.json 2>&1
$PY fd2_compare2.py toy_r_fold toy_david/world_chiral.json folded > out/r_fold_chiral_60_folded.json 2>&1
$PY fd2_compare2.py toy_r_fold toy_david/world_chiral.json > out/r_fold_chiral_60_default.json 2>&1
cd $F/toy_r_imcomp && $PY runback_test.py world_chiral.json 60 > ../out/r_imcomp_runback_chiral_60.txt 2>&1 && $PY cube48_test.py world_chiral.json 3 20 > ../out/r_imcomp_48_3cube_20.txt 2>&1
cd $F/toy_david && $PY cube48_test.py world_chiral.json 3 20 > ../out/david_48_3cube_20.txt 2>&1
echo DONE > $F/out/remainder.done
