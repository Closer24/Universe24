#!/bin/sh
# cs8 batch C (no loop): R2 mended (the pair's click read as standing + 1 >= beat at both ends) on ga2 to 800; the flag-absent hole and chiral under src_cs8 for the comparison
D=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/cs8/tools/derivations/cs8
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/cs8
cd $D
export TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
export PYTHONPATH=$D/src_cs8:$D
F="CS4_TAKE_FARTHEST=1 CS7_EQ=n CS8_MERGER_LAY=1"
env $F CS8_REST=2 nice -n 19 $PY cs6_run.py worlds/empty4_ga2_800.json out/ga2_r2b_800.json worlds/cycle_m5_m0.json back 10 > out/ga2_r2b_800.log 2>&1 &
(nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_hole.json out/three/abs_hole.json back 10 > out/three/abs_hole.log 2>&1; nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_chiral.json out/three/abs_chiral.json back 10 > out/three/abs_chiral.log 2>&1) &
wait
echo done > out/run_c.done
