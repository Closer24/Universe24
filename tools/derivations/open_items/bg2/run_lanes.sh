#!/bin/bash
# bg2's runs in three lanes (no loop; each lane a chain), the copy's src and the flag in the environment
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp
export PYTHONPATH=$PWD/src_bg2
lane1() {
  BG2_FLAG=a $PY -m event_universe.run worlds/world_chiral_300.json out/chiral_300_a.json back 10 > out/chiral_300_a.log 2>&1
  BG2_FLAG=b $PY -m event_universe.run worlds/world_chiral_300.json out/chiral_300_b.json back 10 > out/chiral_300_b.log 2>&1
  BG2_FLAG=c $PY -m event_universe.run worlds/world_chiral_300.json out/chiral_300_c.json back 10 > out/chiral_300_c.log 2>&1
  BG2_FLAG=a $PY -m event_universe.run worlds/world_chiral_2400.json out/chiral_2400_a.json back 10 > out/chiral_2400_a.log 2>&1
  BG2_FLAG=a $PY -m event_universe.run worlds/world_bodies_120.json out/bodies_120_a.json back 10 > out/bodies_120_a.log 2>&1
}
lane2() {
  BG2_FLAG= $PY -m event_universe.run worlds/world_collapse_800_400.json out/collapse_800_400_default.json back 10 > out/collapse_800_400_default.log 2>&1
  BG2_FLAG=c $PY -m event_universe.run worlds/world_chiral_2400.json out/chiral_2400_c.json back 10 > out/chiral_2400_c.log 2>&1
  BG2_FLAG= $PY -m event_universe.run worlds/world_bodies_120.json out/bodies_120_default.json back 10 > out/bodies_120_default.log 2>&1
}
lane3() {
  BG2_FLAG=a $PY -m event_universe.run worlds/world_collapse_800_400.json out/collapse_800_400_a.json back 10 > out/collapse_800_400_a.log 2>&1
  BG2_FLAG= BG2_SRC=$PWD/src_bg2 $PY bg2_course.py worlds/world_uniform_3_600.json out/course_uniform_600_default.json 20 > out/course_uniform_600_default.log 2>&1
  BG2_FLAG=a BG2_SRC=$PWD/src_bg2 $PY bg2_course.py worlds/world_uniform_3_600.json out/course_uniform_600_a.json 20 > out/course_uniform_600_a.log 2>&1
  BG2_FLAG=a BG2_SRC=$PWD/src_bg2 $PY bg2_course.py worlds/world_chiral_2400.json out/course_chiral_2400_a.json 100 > out/course_chiral_2400_a.log 2>&1
}
lane1 & lane2 & lane3 & wait
echo LANES DONE > out/LANES_DONE
