#!/bin/sh
D=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/pl1/tools/derivations/pl1
W=$D/../../../tests/worlds
P=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp
cd $D
PYTHONPATH=$D/../../../src nice -n 19 $P -m event_universe.run $W/world_hole.json out/rec_base_hole_60.json back 10 > out/rec_base_hole_60.log 2>&1 &
PYTHONPATH=$D/src_pl1 nice -n 19 $P -m event_universe.run $W/world_hole.json out/rec_absent_hole_60.json back 10 > out/rec_absent_hole_60.log 2>&1 &
PYTHONPATH=$D/src_pl1 PL1_SIGN=sym nice -n 19 $P -m event_universe.run $W/world_hole.json out/rec_sym_hole_60.json back 10 > out/rec_sym_hole_60.log 2>&1 &
PYTHONPATH=$D/../../../src nice -n 19 $P -m event_universe.run $W/world_chiral.json out/rec_base_chiral_60.json back 10 > out/rec_base_chiral_60.log 2>&1 &
wait
PYTHONPATH=$D/src_pl1 nice -n 19 $P -m event_universe.run $W/world_chiral.json out/rec_absent_chiral_60.json back 10 > out/rec_absent_chiral_60.log 2>&1 &
PYTHONPATH=$D/src_pl1 PL1_SIGN=sym nice -n 19 $P -m event_universe.run $W/world_chiral.json out/rec_sym_chiral_60.json back 10 > out/rec_sym_chiral_60.log 2>&1 &
PYTHONPATH=$D/../../../src nice -n 19 $P -m event_universe.run $W/world_bodies.json out/rec_base_bodies_300.json back 10 > out/rec_base_bodies_300.log 2>&1 &
PYTHONPATH=$D/src_pl1 nice -n 19 $P -m event_universe.run $W/world_bodies.json out/rec_absent_bodies_300.json back 10 > out/rec_absent_bodies_300.log 2>&1 &
wait
PYTHONPATH=$D/src_pl1 PL1_SIGN=sym nice -n 19 $P -m event_universe.run $W/world_bodies.json out/rec_sym_bodies_300.json back 10 > out/rec_sym_bodies_300.log 2>&1 &
PYTHONPATH=$D/src_pl1 EQ2_CLICK=b nice -n 19 $P -m event_universe.run $W/world_bodies.json out/rec_b_bodies_300.json back 10 > out/rec_b_bodies_300.log 2>&1 &
PYTHONPATH=$D/src_pl1 EQ2_CLICK=b nice -n 19 $P -m event_universe.run $W/world_hole.json out/rec_b_hole_60.json back 10 > out/rec_b_hole_60.log 2>&1 &
PYTHONPATH=$D/src_pl1 EQ2_CLICK=b nice -n 19 $P -m event_universe.run $W/world_chiral.json out/rec_b_chiral_60.json back 10 > out/rec_b_chiral_60.log 2>&1 &
wait
echo RECORDS_DONE
