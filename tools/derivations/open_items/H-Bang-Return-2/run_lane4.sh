#!/bin/bash
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp
export PYTHONPATH=$PWD/src_bg2
BG2_FLAG=d BG2_SRC=$PWD/src_bg2 $PY bg2_course.py worlds/world_chiral_300.json out/course_chiral_300_d.json 20 > out/course_chiral_300_d.log 2>&1
BG2_FLAG=d $PY -m event_universe.run worlds/world_chiral_2400.json out/chiral_2400_d.json back 10 > out/chiral_2400_d.log 2>&1
BG2_FLAG=b BG2_SRC=$PWD/src_bg2 $PY bg2_course.py worlds/world_chiral_300.json out/course_chiral_300_b.json 20 > out/course_chiral_300_b.log 2>&1
echo LANE4 DONE > out/LANE4_DONE
