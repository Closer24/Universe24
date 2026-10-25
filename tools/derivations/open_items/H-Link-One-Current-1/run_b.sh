#!/bin/bash
# lc1: the flags g and v, sequential, nice 19
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
cd $S/hands/lc1/tools/derivations/lc1
PY=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp
CPY=$S/hands/lc1/tools/derivations/lc1/src_lc1
for_world() {
  W=$1; TAG=$2; FLAG=$3
  LC1_FLAG=$FLAG LC1_SRC=$CPY nice -n 19 $PY lc1_course.py worlds/$W.json out/course_${W}_${TAG}.json 50 > out/course_${W}_${TAG}.log 2>&1
  $PY lc1_read.py out/course_${W}_${TAG}.json > out/summary_${W}_${TAG}.txt 2>&1
  LC1_FLAG=$FLAG PYTHONPATH=$CPY nice -n 19 $PY -m event_universe.run worlds/$W.json out/rec_${W}_${TAG}.json back 10 > out/rec_${W}_${TAG}.log 2>&1
  LC1_FLAG=$FLAG PYTHONPATH=$CPY nice -n 19 $PY -m event_universe.gates out/rec_${W}_${TAG}.json > out/gates_${W}_${TAG}.txt 2>&1
}
for_world quantum_3_400 g g
for_world hole_3_400 g g
for_world chiral_5_300 g g
for_world quantum_3_400 v v
for_world hole_3_400 v v
for_world chiral_5_300 v v
for_world bare_3_400 v v
echo DONE > out/B_DONE
