#!/bin/sh
# lc2: the matrix of records (no loop: each line one run), nice 19
cd "$(dirname "$0")/out"
PY=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp
export PYTHONPATH=../src_lc2
run() { echo "== $1 $2"; LC2_REACH=$2 nice -n 19 $PY ../lc2_course.py $1 course_$3_$2.json 10; }
unset LC2_REACH
echo "== world_sea3_400 default"; nice -n 19 $PY ../lc2_course.py world_sea3_400.json course_sea3_default.json 10
run world_sea3_400.json harmonic sea3
run world_sea3_400.json product sea3
echo "== world_q1 default"; nice -n 19 $PY ../lc2_course.py world_q1_3_400.json course_q1_default.json 10
run world_q1_3_400.json harmonic q1
run world_q1_3_400.json product q1
echo "== world_hole3 default"; nice -n 19 $PY ../lc2_course.py world_hole3_400.json course_hole3_default.json 10
run world_hole3_400.json harmonic hole3
run world_hole3_400.json product hole3
echo "== chiral300 default"; nice -n 19 $PY ../lc2_course.py world_chiral_300.json course_chiral300_default.json 10
run world_chiral_300.json harmonic chiral300
run world_chiral_300.json product chiral300
run world_chiral_300.json mean chiral300
echo "== hole60 default"; nice -n 19 $PY ../lc2_course.py world_hole.json course_hole60_default.json 10
run world_hole.json harmonic hole60
echo "== bodies120 default"; nice -n 19 $PY ../lc2_course.py world_bodies_120.json course_bodies120_default.json 10
run world_bodies_120.json harmonic bodies120
echo "== done"
