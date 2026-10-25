#!/bin/sh
# fd2's measurements, in order: the side-by-side records (rule 4), the ties, the 48 on the clicks, David's run back and reach tests on both copies
F=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/fd2/tools/derivations/fd2
PY=/home/user/Universe24/venv314/bin/python
export PYTHONPATH=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/fd2/src
export TMPDIR=/dev/shm/tmp
cd $F
$PY fd2_compare.py worlds/world_hole_60.json 10 hole_60 > out/compare_hole_60.log 2>&1
$PY fd2_compare.py worlds/world_bodies_120.json 10 bodies_120 > out/compare_bodies_120.log 2>&1
$PY fd2_compare.py worlds/world_chiral_300.json 10 chiral_300 > out/compare_chiral_300.log 2>&1
$PY fd2_ties.py worlds/world_chiral_300.json 300 > out/ties_chiral_300.json 2>&1
$PY fd2_ties.py worlds/world_bodies_120.json 120 > out/ties_bodies_120.json 2>&1
$PY fd2_48.py toy_david/world_chiral.json 5 30 out/48_chiral_5cube_30.json > out/48_chiral_5cube_30.log 2>&1
cd $F/toy_david && $PY runback_test.py world_chiral.json 60 > ../out/runback_david_chiral_60.txt 2>&1 && $PY reach_test.py world_chiral.json 20 2,2,2 > ../out/reach_david_chiral.txt 2>&1
cd $F/toy_fd2 && $PY runback_test.py world_chiral.json 60 > ../out/runback_fd2_chiral_60.txt 2>&1 && $PY reach_test.py world_chiral.json 20 2,2,2 > ../out/reach_fd2_chiral.txt 2>&1
echo DONE > $F/out/measurements.done
