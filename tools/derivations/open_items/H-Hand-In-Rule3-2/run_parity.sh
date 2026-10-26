#!/bin/sh
# hd2: the three reversals on the chiral 60 and the hole 60 (the 5-cube, the engine's own worlds), one run at a time, nice 19.
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/hd2
H=$W/tools/derivations/open_items/H-Hand-In-Rule3-2
P=/home/user/Universe24/venv314/bin/python
export PYTHONPATH=$W/src TMPDIR=/dev/shm/tmp
cd /dev/shm/tmp/hd2
nice -n 19 $P $H/parity_hd2.py $W/src $W/tests/worlds/world_nature.json 60 /dev/shm/tmp/hd2/par_chiral60_x.json P,R,I,T,PR,PI,RT,PT,PRT,PIT 4 > /dev/shm/tmp/hd2/par_chiral60_x.stdout 2>&1
nice -n 19 $P $H/parity_hd2.py $W/src $W/tests/worlds/world_nature.json 60 /dev/shm/tmp/hd2/par_chiral60_inv.json P,PR,PI 7 > /dev/shm/tmp/hd2/par_chiral60_inv.stdout 2>&1
nice -n 19 $P $H/parity_hd2.py $W/src $W/tests/worlds/world_hole.json 60 /dev/shm/tmp/hd2/par_hole60_x.json P,R,I,T,PR,PI,RT,PT,PRT,PIT 4 > /dev/shm/tmp/hd2/par_hole60_x.stdout 2>&1
nice -n 19 $P $H/parity_hd2.py $W/src $W/tests/worlds/world_hole.json 60 /dev/shm/tmp/hd2/par_hole60_inv.json P,PR,PI 7 > /dev/shm/tmp/hd2/par_hole60_inv.stdout 2>&1
echo DONE > /dev/shm/tmp/hd2/par.done
