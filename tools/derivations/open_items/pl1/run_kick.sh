#!/bin/sh
D=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/pl1/tools/derivations/pl1
W=$D/../../../tests/worlds
P=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp
cd $D
PYTHONPATH=$D/src_pl1 EQ2_CLICK=a PL1_SIGN=kick nice -n 19 $P pl1_run.py worlds/h3.json out/a_kick_h3.json back 10 > out/a_kick_h3.log 2>&1 &
PYTHONPATH=$D/src_pl1 EQ2_CLICK=b PL1_SIGN=kick nice -n 19 $P pl1_run.py worlds/h3.json out/b_kick_h3.json back 10 > out/b_kick_h3.log 2>&1 &
PYTHONPATH=$D/src_pl1 PL1_SIGN=kick nice -n 19 $P -m event_universe.run $W/world_hole.json out/rec_kick_hole_60.json back 10 > out/rec_kick_hole_60.log 2>&1 &
PYTHONPATH=$D/src_pl1 PL1_SIGN=kick nice -n 19 $P -m event_universe.run $W/world_chiral.json out/rec_kick_chiral_60.json back 10 > out/rec_kick_chiral_60.log 2>&1 &
wait
PYTHONPATH=$D/src_pl1 EQ2_CLICK=b PL1_SIGN=kick nice -n 19 $P pl1_run.py worlds/h5.json out/b_kick_h5.json back 10 > out/b_kick_h5.log 2>&1 &
PYTHONPATH=$D/src_pl1 PL1_SIGN=kick nice -n 19 $P -m event_universe.run $W/world_bodies.json out/rec_kick_bodies_300.json back 10 > out/rec_kick_bodies_300.log 2>&1 &
PYTHONPATH=$D/src_pl1 PL1_SIGN=kick nice -n 19 $P pl1_run.py worlds/h3.json out/kick_h3.json back 10 > out/kick_h3.log 2>&1 &
PYTHONPATH=$D/src_pl1 EQ2_CLICK=b PL1_SIGN=kick nice -n 19 $P pl1_run.py worlds/dh3.json out/b_kick_dh3.json back 10 > out/b_kick_dh3.log 2>&1 &
wait
echo KICK_DONE
