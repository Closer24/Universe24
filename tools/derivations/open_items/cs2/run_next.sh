#!/bin/sh
# cs2: the next three records (no loop)
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
cd $S/hands/cs2/tools/derivations/cs2
export PYTHONPATH=$S/hands/cs2/src TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
nice -n 19 $PY cs_run.py worlds/empty4_400.json out/s3_400.json back 10 screw 01101023 111 189 complex > out/s3_400.log 2>&1 &
nice -n 19 $PY cs_run.py worlds/empty8_400.json out/s2_8cube_400.json back 10 screw 00111320 111 189 complex > out/s2_8cube_400.log 2>&1 &
nice -n 19 $PY cs_run.py worlds/empty4_400.json out/s2r_400.json back 10 screw 00111320 111 189 > out/s2r_400.log 2>&1 &
wait
echo done > out/run_next.done
