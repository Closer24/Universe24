#!/bin/bash
# lc1: the controls (the default engine) and the flag d, sequential, nice 19
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
cd $S/hands/lc1/tools/derivations/lc1
PY=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp
ENG=$S/hands/lc1/src
CPY=$S/hands/lc1/tools/derivations/lc1/src_lc1
# P0: the flag off bit for bit
PYTHONPATH=$ENG nice -n 19 $PY -m event_universe.run worlds/chiral_5_60.json out/chiral_60_default.json back 10 > out/chiral_60_default.log 2>&1
PYTHONPATH=$CPY nice -n 19 $PY -m event_universe.run worlds/chiral_5_60.json out/chiral_60_copy_off.json back 10 > out/chiral_60_copy_off.log 2>&1
$PY compare_records.py out/chiral_60_default.json out/chiral_60_copy_off.json > out/P0_compare.txt 2>&1
# the controls: the course and the engine's record with the gates
for_world() {
  W=$1; TAG=$2; FLAG=$3
  LC1_FLAG=$FLAG LC1_SRC=$CPY nice -n 19 $PY lc1_course.py worlds/$W.json out/course_${W}_${TAG}.json 50 > out/course_${W}_${TAG}.log 2>&1
  $PY lc1_read.py out/course_${W}_${TAG}.json > out/summary_${W}_${TAG}.txt 2>&1
  LC1_FLAG=$FLAG PYTHONPATH=$CPY nice -n 19 $PY -m event_universe.run worlds/$W.json out/rec_${W}_${TAG}.json back 10 > out/rec_${W}_${TAG}.log 2>&1
  LC1_FLAG=$FLAG PYTHONPATH=$CPY nice -n 19 $PY -m event_universe.gates out/rec_${W}_${TAG}.json > out/gates_${W}_${TAG}.txt 2>&1
}
for_world bare_3_400 default ""
for_world quantum_3_400 default ""
for_world hole_3_400 default ""
for_world chiral_5_300 default ""
for_world bare_3_400 d d
for_world quantum_3_400 d d
for_world hole_3_400 d d
for_world chiral_5_300 d d
echo DONE > out/A_DONE
