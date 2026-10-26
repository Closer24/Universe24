#!/bin/bash
# the load rule: poll until the 1-minute load is below 3 before each record; one record at a time
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/ca2
F=$W/tools/derivations/open_items/H-Click-And-Rule3-One-Algebra-2
P=/home/user/Universe24/venv314/bin/python
export PYTHONPATH=$W/src TMPDIR=/dev/shm/tmp
cd $F
$P poll_load.py && date -u && (time $P q8_takes.py world_hole.json 60 out/q8_hole_60.txt) > /dev/shm/tmp/ca2/hole.log 2>&1
$P poll_load.py && date -u && (time $P q8_takes.py world_chiral.json 60 out/q8_chiral_60.txt) > /dev/shm/tmp/ca2/chiral.log 2>&1
date -u; echo done
