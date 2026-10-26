#!/bin/bash
# The three records from the engine's own runner (src unedited), one at a time, nice 19, the load polled before the long one.
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/cc1
F=$W/tools/derivations/open_items/H-Children-Charge-Bug-1
P=/home/user/Universe24/venv314/bin/python; export TMPDIR=/dev/shm/tmp PYTHONPATH=${SRC:-$W/src}; cd $F
TAG=${TAG:-head}
date -u
(time nice -n 19 $P -m event_universe.run $W/tests/worlds/world_hole.json /dev/shm/tmp/cc1/hole_60_$TAG.json back 10) > out/run_hole_60_$TAG.txt 2>&1
(time nice -n 19 $P -m event_universe.run $W/tests/worlds/world_nature.json /dev/shm/tmp/cc1/chiral_60_$TAG.json back 10) > out/run_chiral_60_$TAG.txt 2>&1
date -u
$P poll_load.py
(time nice -n 19 timeout 1200 $P -m event_universe.run /dev/shm/tmp/cc1/world_ga2_450.json /dev/shm/tmp/cc1/ga2_450_$TAG.json back 10) > out/run_ga2_450_$TAG.txt 2>&1
date -u; echo done $TAG
