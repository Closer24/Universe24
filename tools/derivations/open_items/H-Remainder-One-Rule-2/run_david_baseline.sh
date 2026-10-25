#!/bin/sh
# David's toy (pristine copy) on the three records with back 10; outputs under out/
F=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/fd2/tools/derivations/fd2
PY=/home/user/Universe24/venv314/bin/python
export PYTHONPATH=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/fd2/src
export TMPDIR=/dev/shm/tmp
cd $F/toy_david
$PY lean_full.py ../worlds/world_hole_60.json ../out/david_hole_60.json back 10 > ../out/david_hole_60.log 2>&1
$PY lean_full.py ../worlds/world_chiral_300.json ../out/david_chiral_300.json back 10 > ../out/david_chiral_300.log 2>&1
$PY lean_full.py ../worlds/world_bodies_120.json ../out/david_bodies_120.json back 10 > ../out/david_bodies_120.log 2>&1
$PY decoder_full.py ../out/david_hole_60.json > ../out/david_hole_60.gates 2>&1
$PY decoder_full.py ../out/david_chiral_300.json > ../out/david_chiral_300.gates 2>&1
$PY decoder_full.py ../out/david_bodies_120.json > ../out/david_bodies_120.gates 2>&1
echo DONE > ../out/david_baseline.done
