#!/bin/sh
W=$(cd "$(dirname "$0")/../../.." && pwd)
export PYTHONPATH=$W/src TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
cd "$W/tools/derivations/bb2"
$PY -m event_universe.run worlds/world_wave3_400.json out/wave3_400.json back 10 > out/wave3_400.log 2>&1
$PY bb2_course.py worlds/world_one3_400.json out/course_one3_400.json 50 > out/course_one3_400.log 2>&1
$PY bb2_course.py worlds/world_hole3_400.json out/course_hole3_400.json 50 > out/course_hole3_400.log 2>&1
$PY bb2_course.py worlds/world_wave3_400.json out/course_wave3_400.json 50 > out/course_wave3_400.log 2>&1
$PY bb2_course.py worlds/world_chiral5_300.json out/course_chiral5_300.json 50 > out/course_chiral5_300.log 2>&1
$PY bb2_course.py worlds/world_holeat5_400.json out/course_holeat5_400.json 50 > out/course_holeat5_400.log 2>&1
echo done
